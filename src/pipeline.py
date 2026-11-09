"""
Pipeline hỏi đáp hoàn chỉnh cho demo và đo độ trễ (Giai đoạn 6):
câu hỏi -> Retriever hybrid (BM25 âm tiết + dense, RRF) top-k -> Reader ViT5 đọc từng đoạn
-> chọn đáp án có điểm cao nhất khác "không có câu trả lời" (giống src/reader/infer.py).

    from src.pipeline import QAPipeline
    qa = QAPipeline.load("models/r2_ood")
    out = qa.answer("Chiến thắng Bạch Đằng năm 938 do ai lãnh đạo?", k=5)
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for sub in ("src/reader", "src/retriever", "src/eval"):
    p = str(ROOT / sub)
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np  # noqa: E402

from hybrid import Retriever  # noqa: E402
from infer import Seq2SeqReader, pick  # noqa: E402
from metrics import NO_ANSWER, is_no_answer  # noqa: E402

DEFAULT_MODEL = ROOT / "models/r2_ood"      # GĐ5: tốt nhất trên test (hybrid top-5)
INDEX_DIR = ROOT / "data/index_qa"


def _sync(device: str):
    if device == "cuda":
        import torch
        torch.cuda.synchronize()


class QAPipeline:
    def __init__(self, retriever: Retriever, reader: Seq2SeqReader):
        self.retriever, self.reader = retriever, reader

    @classmethod
    def load(cls, model: str | Path = DEFAULT_MODEL, device: str | None = None) -> "QAPipeline":
        r = Retriever.load(str(INDEX_DIR))
        r.bm25_scores(["khởi động"])                        # dựng chỉ mục BM25 một lần
        return cls(r, Seq2SeqReader(str(model), device=device))

    def answer(self, question: str, k: int = 5) -> dict:
        """Trả về đáp án, đoạn bằng chứng, top-k nguồn và thời gian từng khâu (ms)."""
        dev = self.reader.device
        t = {}
        t0 = time.perf_counter()
        bm = self.retriever.bm25_scores([question])
        t["bm25"] = time.perf_counter() - t0
        t0 = time.perf_counter()
        de = self.retriever.dense_scores([question])
        t["dense"] = time.perf_counter() - t0
        t0 = time.perf_counter()
        s = self.retriever.rrf(bm, de, weights=[1.0, self.retriever.w_dense])[0]
        top = np.argsort(-s, kind="stable")[:k]
        meta = self.retriever.meta
        ctxs = [{"rank": j + 1, "context_id": meta.context_id.iat[i], "title": meta.title.iat[i],
                 "context": meta.context.iat[i], "score": float(s[i])} for j, i in enumerate(top)]
        t["fuse"] = time.perf_counter() - t0

        _sync(dev)
        t0 = time.perf_counter()
        res = self.reader.read([question] * len(ctxs), [c["context"] for c in ctxs])
        _sync(dev)
        t["read"] = time.perf_counter() - t0
        for c, (a, sc) in zip(ctxs, res):
            c["answer"], c["answer_score"] = a, sc
        ans, sc, used = pick([(a, sc, c["context_id"]) for c, (a, sc) in zip(ctxs, res)])
        evidence = next((c for c in ctxs if c["context_id"] == used), None)
        span = highlight_span(evidence["context"], ans) if evidence else None
        ms = {key: 1000 * v for key, v in t.items()}
        ms["retrieve"] = ms["bm25"] + ms["dense"] + ms["fuse"]
        ms["total"] = ms["retrieve"] + ms["read"]
        return {"question": question, "answer": ans, "refused": is_no_answer(ans), "score": sc,
                # đáp án lấy nguyên văn từ đoạn bằng chứng (sửa ký tự ViT5 làm rơi, vd. ç, ā)
                "answer_text": evidence["context"][span[0]:span[1]] if span else ans,
                "span": span, "evidence": evidence, "contexts": ctxs, "latency_ms": ms}


def highlight_span(passage: str, answer: str) -> tuple[int, int] | None:
    """Vị trí (đầu, cuối) của đáp án trong đoạn văn, không phân biệt hoa thường.
    Nếu không khớp nguyên văn (ViT5 làm rơi ký tự ngoài từ vựng như ç, ā), thử khớp
    sau khi bỏ các ký tự đó khỏi đoạn văn rồi ánh xạ ngược lại vị trí gốc."""
    if not answer or is_no_answer(answer):
        return None
    low, a = passage.lower(), answer.lower().strip()
    pos = low.find(a)
    if pos >= 0:
        return pos, pos + len(a)
    def dropped(ch: str) -> bool:
        return ch.isalpha() and not ch.isascii() and ch not in a and not _in_vocab(ch)

    keep = [i for i, ch in enumerate(low) if not dropped(ch)]
    squeezed = "".join(low[i] for i in keep)
    pos = squeezed.find(a)
    if pos < 0:
        return None
    start, end = keep[pos], keep[pos + len(a) - 1] + 1
    while start > 0 and dropped(low[start - 1]):          # ký tự bị rơi sát hai đầu ("Mahtm" -> "Mahātmā")
        start -= 1
    while end < len(low) and dropped(low[end]):
        end += 1
    return start, end


_VI = set("àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ")


def _in_vocab(ch: str) -> bool:
    """Xấp xỉ: chữ tiếng Việt có dấu nằm trong từ vựng ViT5; chữ Latin mở rộng khác (ç, ā) thì không."""
    return ch in _VI


__all__ = ["QAPipeline", "highlight_span", "NO_ANSWER"]
