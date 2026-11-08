"""
Suy luận Reader seq2seq (ViT5) trên đoạn văn đúng hoặc đoạn retriever tìm được.

  B2 (zero-shot):  python src/reader/infer.py --model VietAI/vit5-base --context gold --run b2_gold_dev
  R1/R2 (GG4):     python src/reader/infer.py --model <checkpoint> --context retrieved --k 3

Với k > 1: đọc TỪNG đoạn riêng (Giai đoạn 1: ghép k đoạn vượt 512 token), mỗi đoạn
sinh một đáp án kèm điểm = log-xác suất trung bình mỗi token. Chọn đáp án có điểm cao
nhất trong các đáp án KHÁC "không có câu trả lời"; nếu mọi đoạn đều từ chối thì từ chối.

Ghi data/predictions/{run}.jsonl (định dạng ở src/eval/predictions.py).

--refusal_scores (Giai đoạn 5): mỗi cặp (câu, đoạn) ghi thêm refuse_score (log-prob trung
bình của "không có câu trả lời" khi ép giải mã) và alt_answer/alt_score (đáp án tốt nhất khi
cấm từ chối; trùng đáp án gốc nếu mô hình vốn không từ chối). tune_refusal.py dùng các
trường này để chọn ngưỡng δ trên dev mà không phải chạy lại mô hình.
"""
from __future__ import annotations

import argparse
import time

from common import get_contexts, load_corpus_text, load_questions
from metrics import NO_ANSWER, is_no_answer
from predictions import PRED_DIR, gold_fields, write_predictions

MAX_SOURCE = 512     # Giai đoạn 1: p99 input 1 đoạn = 516 token
MAX_TARGET = 64      # p99 đáp án = 59 token


def format_input(question: str, passage: str) -> str:
    """Định dạng input dùng chung cho train (Giai đoạn 4) và suy luận."""
    return f"<q> {question} </q> <ctx> {passage} </ctx>"


class Seq2SeqReader:
    def __init__(self, model_name: str, device: str | None = None, num_beams: int = 1,
                 max_source: int = MAX_SOURCE, max_target: int = MAX_TARGET):
        import torch
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        self.torch = torch
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tok = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device).eval()
        if self.device == "cuda" and torch.cuda.is_bf16_supported():
            self.model = self.model.to(torch.bfloat16)
        self.num_beams, self.max_source, self.max_target = num_beams, max_source, max_target

    def read(self, questions: list[str], passages: list[str]) -> list[tuple[str, float]]:
        """Trả về [(đáp án, điểm)] — điểm = log-prob trung bình mỗi token sinh ra."""
        torch = self.torch
        enc = self.tok([format_input(q, p) for q, p in zip(questions, passages)],
                       max_length=self.max_source, truncation=True, padding=True,
                       return_tensors="pt").to(self.device)
        with torch.inference_mode():
            out = self.model.generate(**enc, max_new_tokens=self.max_target,
                                      num_beams=self.num_beams, do_sample=False,
                                      output_scores=True, return_dict_in_generate=True,
                                      logits_processor=getattr(self, "_extra_lp", None))
        seqs = out.sequences
        trans = self.model.compute_transition_scores(seqs, out.scores, out.get("beam_indices"),
                                                     normalize_logits=True)
        texts = self.tok.batch_decode(seqs, skip_special_tokens=True)
        gen = seqs[:, 1:]                                   # bỏ decoder_start_token
        mask = (gen != self.tok.pad_token_id).float()[:, :trans.shape[1]]
        lp = (trans.float().nan_to_num(0.0) * mask).sum(1) / mask.sum(1).clamp(min=1)
        return [(t.strip(), float(s)) for t, s in zip(texts, lp.tolist())]

    def read_alt(self, questions: list[str], passages: list[str]) -> list[tuple[str, float]]:
        """Như read() nhưng cấm token đầu của NO_ANSWER ở bước sinh đầu tiên -> đáp án thay
        thế tốt nhất khi mô hình muốn từ chối (dùng cho chỉnh ngưỡng từ chối)."""
        from transformers import LogitsProcessor, LogitsProcessorList
        ban = self.tok(NO_ANSWER, add_special_tokens=False)["input_ids"][0]

        class BanFirst(LogitsProcessor):
            def __call__(self, input_ids, scores):
                if input_ids.shape[1] == 1:               # chỉ có decoder_start_token
                    scores[:, ban] = -float("inf")
                return scores

        self._extra_lp = LogitsProcessorList([BanFirst()])
        try:
            return self.read(questions, passages)
        finally:
            self._extra_lp = None

    def refuse_score(self, questions: list[str], passages: list[str]) -> list[float]:
        """Log-prob trung bình mỗi token của NO_ANSWER (ép giải mã), cùng thang với read()."""
        torch = self.torch
        enc = self.tok([format_input(q, p) for q, p in zip(questions, passages)],
                       max_length=self.max_source, truncation=True, padding=True,
                       return_tensors="pt").to(self.device)
        lab = self.tok([NO_ANSWER] * len(questions), return_tensors="pt").input_ids.to(self.device)
        with torch.inference_mode():
            logits = self.model(**enc, labels=lab).logits.float()
        lp = torch.log_softmax(logits, -1).gather(-1, lab.unsqueeze(-1)).squeeze(-1)
        return lp.mean(1).tolist()


def pick(cands: list[tuple[str, float, str]]) -> tuple[str, float, str | None]:
    """cands: [(đáp án, điểm, context_id)] -> đáp án tốt nhất không phải từ chối."""
    real = [c for c in cands if not is_no_answer(c[0])]
    if not real:
        best = max(cands, key=lambda c: c[1])
        return best[0], best[1], None
    return max(real, key=lambda c: c[1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="VietAI/vit5-base")
    ap.add_argument("--split", default="dev")
    ap.add_argument("--context", choices=["gold", "retrieved"], default="gold")
    ap.add_argument("--mode", default="hybrid")
    ap.add_argument("--k", type=int, default=1)
    ap.add_argument("--batch_size", type=int, default=16)
    ap.add_argument("--num_beams", type=int, default=1)
    ap.add_argument("--limit", type=int, default=None, help="lấy ngẫu nhiên N câu (chạy thử)")
    ap.add_argument("--run", default=None)
    ap.add_argument("--refusal_scores", action="store_true",
                    help="ghi thêm điểm từ chối + đáp án thay thế (cho src/reader/tune_refusal.py)")
    args = ap.parse_args()

    run = args.run or f"vit5_{args.context}_k{args.k}_{args.split}"
    qa = load_questions(args.split, args.limit)
    text = load_corpus_text()
    k = 1 if args.context == "gold" else args.k
    ctxs, ret_ms = get_contexts(qa, args.context, k=k, mode=args.mode)
    reader = Seq2SeqReader(args.model, num_beams=args.num_beams)
    print(f"Reader {args.model} trên {reader.device}; {len(qa)} câu × {k} đoạn")

    # trải phẳng (câu, đoạn) để chạy theo batch
    pairs = [(i, c["context_id"]) for i, cs in enumerate(ctxs) for c in cs]
    pairs.sort(key=lambda p: len(text[p[1]]))              # gom độ dài gần nhau -> ít padding
    answers: dict[int, list] = {i: [] for i in range(len(qa))}
    refusal: dict[tuple[int, str], dict] = {}             # chỉ điền khi --refusal_scores
    t0 = time.perf_counter()
    for b in range(0, len(pairs), args.batch_size):
        chunk = pairs[b:b + args.batch_size]
        qs, ps = [qa.question[i] for i, _ in chunk], [text[c] for _, c in chunk]
        res = reader.read(qs, ps)
        for (i, cid), (ans, sc) in zip(chunk, res):
            answers[i].append((ans, sc, cid))
        if args.refusal_scores:
            rsc = reader.refuse_score(qs, ps)
            ref = [j for j, (a, _) in enumerate(res) if is_no_answer(a)]
            alt = dict(zip(ref, reader.read_alt([qs[j] for j in ref], [ps[j] for j in ref])
                           if ref else []))
            for j, (i, cid) in enumerate(chunk):
                a, s = alt.get(j, res[j])
                refusal[(i, cid)] = {"refuse_score": rsc[j], "alt_answer": a, "alt_score": s}
        if (b // args.batch_size) % 10 == 0:
            done = b + len(chunk)
            el = time.perf_counter() - t0
            print(f"  {done}/{len(pairs)}  {el:.0f}s  (còn ~{el / done * (len(pairs) - done):.0f}s)",
                  flush=True)
    read_ms = 1000 * (time.perf_counter() - t0) / max(len(qa), 1)

    rows = []
    for i, q in enumerate(qa.itertuples()):
        ans, sc, used = pick(answers[i])
        rows.append({**gold_fields(q), "prediction": ans, "context_source": args.context,
                     "contexts": ctxs[i], "used_context_id": used,
                     "latency_ms": {"retrieve": ret_ms, "read": read_ms},
                     "extra": {"score": sc,
                               "per_context": [{"context_id": c, "answer": a, "score": s,
                                                **refusal.get((i, c), {})}
                                               for a, s, c in answers[i]]}})
    write_predictions(PRED_DIR / f"{run}.jsonl", rows,
                      meta={**vars(args), "run": run, "device": reader.device})


if __name__ == "__main__":
    main()
