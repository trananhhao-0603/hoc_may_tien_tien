"""
Retriever: BM25 | dense | hybrid (Reciprocal Rank Fusion).

Kho chỉ ~1.9k đoạn nên chấm điểm TOÀN BỘ kho cho mỗi câu hỏi rồi xếp hạng — không
cần top-k gần đúng, và RRF gộp trên thứ hạng đầy đủ (bản cũ chỉ gộp top 3k nên
đoạn đúng có thể rơi khỏi danh sách của một nhánh).

    from hybrid import Retriever
    r = Retriever.load("data/index_qa")
    r.search("Chiến thắng Điện Biên Phủ diễn ra năm nào?", k=5)
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable, Optional

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from text import segment, tokens  # noqa: E402

# Cấu hình chọn ở Giai đoạn 2 (quét trên dev, kiểm lại trên train — reports/retriever_dev.md):
# BM25 âm tiết + dense tách từ, RRF k=5, trọng số dense 0.7.
RRF_K = 5
W_DENSE = 0.7
MODES = ("bm25", "dense", "hybrid")


class Retriever:
    def __init__(self, meta, dense: Optional[dict[str, np.ndarray]] = None,
                 encoder: Optional[Callable[[list[str]], np.ndarray]] = None,
                 bm25_tok: str = "syl", dense_input: str = "seg", rrf_k: int = RRF_K,
                 w_dense: float = W_DENSE):
        """
        meta       : DataFrame có cột context_id, title, context (+ context_seg nếu dùng "seg")
        dense      : {"seg"|"raw": ma trận embedding (n_đoạn, d) đã chuẩn hoá L2}
        encoder    : hàm list[str] -> ma trận embedding câu hỏi đã chuẩn hoá L2
        bm25_tok   : "seg" | "syl" — cách tách token cho BM25 (mặc định)
        dense_input: "seg" | "raw" — câu hỏi/đoạn văn có tách từ trước khi nhúng không
        """
        self.meta = meta.reset_index(drop=True)
        self.dense = dense or {}
        self.encoder = encoder
        self.bm25_tok, self.dense_input, self.rrf_k = bm25_tok, dense_input, rrf_k
        self.w_dense = w_dense    # trọng số nhánh dense trong RRF (BM25 luôn = 1)
        self._bm25: dict[str, object] = {}

    # ------------------------------------------------------------------ load
    @classmethod
    def load(cls, index_dir: str = "data/index_qa", model_name: Optional[str] = None,
             **kw) -> "Retriever":
        import json
        import faiss
        import pandas as pd

        d = Path(index_dir)
        meta = pd.read_parquet(d / "meta.parquet")
        info = json.loads((d / "info.json").read_text(encoding="utf-8"))
        dense = {}
        for kind in info.get("dense_inputs", []):
            idx = faiss.read_index(str(d / f"dense_{kind}.faiss"))
            dense[kind] = idx.reconstruct_n(0, idx.ntotal)    # kho nhỏ: giữ cả ma trận

        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(model_name or info["model"])

        def encoder(texts: list[str]) -> np.ndarray:
            return model.encode(texts, batch_size=64, normalize_embeddings=True,
                                convert_to_numpy=True).astype("float32")

        return cls(meta, dense=dense, encoder=encoder, **kw)

    # ------------------------------------------------------------------ BM25
    def _bm25_index(self, tok: str):
        if tok not in self._bm25:
            from rank_bm25 import BM25Okapi
            # "seg" dùng sẵn context_seg (đã tách từ lúc build) -> khỏi tách lại
            if tok == "seg" and "context_seg" in self.meta:
                docs = [tokens(t, "syl") for t in self.meta.context_seg]
            else:
                docs = [tokens(t, tok) for t in self.meta.context]
            self._bm25[tok] = BM25Okapi(docs)
        return self._bm25[tok]

    def bm25_scores(self, queries: list[str], tok: Optional[str] = None) -> np.ndarray:
        tok = tok or self.bm25_tok
        bm = self._bm25_index(tok)
        return np.vstack([bm.get_scores(tokens(q, tok)) for q in queries])

    # ------------------------------------------------------------------ dense
    def dense_scores(self, queries: list[str], inp: Optional[str] = None) -> np.ndarray:
        inp = inp or self.dense_input
        if inp not in self.dense:
            raise KeyError(f"Chưa có embedding dense_{inp} (có: {list(self.dense)})")
        if self.encoder is None:
            raise RuntimeError("Cần encoder để nhúng câu hỏi")
        q = [segment(x) for x in queries] if inp == "seg" else list(queries)
        return self.encoder(q) @ self.dense[inp].T          # cosine

    # ------------------------------------------------------------------ fuse
    @staticmethod
    def ranks(scores: np.ndarray) -> np.ndarray:
        """Hạng 0-based của từng đoạn (0 = điểm cao nhất), theo từng hàng."""
        order = np.argsort(-scores, axis=1, kind="stable")
        r = np.empty_like(order)
        rows = np.arange(scores.shape[0])[:, None]
        r[rows, order] = np.arange(scores.shape[1])[None, :]
        return r

    def rrf(self, *score_mats: np.ndarray, weights=None, k: Optional[int] = None) -> np.ndarray:
        """RRF có trọng số: sum_i w_i / (k + rank_i + 1)."""
        k = self.rrf_k if k is None else k
        weights = weights or [1.0] * len(score_mats)
        return sum(w / (k + self.ranks(s) + 1) for w, s in zip(weights, score_mats))

    def score_matrix(self, queries: list[str], mode: str = "hybrid",
                     bm25_tok: Optional[str] = None,
                     dense_input: Optional[str] = None) -> np.ndarray:
        """Điểm (n_câu_hỏi, n_đoạn), càng cao càng liên quan."""
        if mode == "bm25":
            return self.bm25_scores(queries, bm25_tok)
        if mode == "dense":
            return self.dense_scores(queries, dense_input)
        if mode == "hybrid":
            return self.rrf(self.bm25_scores(queries, bm25_tok),
                            self.dense_scores(queries, dense_input),
                            weights=[1.0, self.w_dense])
        raise ValueError(f"mode phải thuộc {MODES}, nhận {mode!r}")

    # ------------------------------------------------------------------ API
    def search(self, query: str, k: int = 5, mode: str = "hybrid", **kw) -> list[dict]:
        s = self.score_matrix([query], mode, **kw)[0]
        top = np.argsort(-s, kind="stable")[:k]
        out = []
        for rank, i in enumerate(top):
            row = self.meta.iloc[int(i)]
            out.append({"rank": rank + 1, "context_id": row.context_id, "title": row.title,
                        "context": row.context, "score": float(s[i])})
        return out
