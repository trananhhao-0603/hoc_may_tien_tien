"""
Baseline B0 (mốc sàn): chọn ngẫu nhiên một cụm danh từ hoặc một năm trong đoạn văn
đứng đầu. Không bao giờ từ chối trả lời -> NoAns-acc = 0.

Cụm danh từ lấy từ underthesea.chunk (gộp các token B-NP/I-NP liền nhau).

Chạy:
    python src/reader/baseline_random.py --split dev --context retrieved
    python src/reader/baseline_random.py --split dev --context gold
"""
from __future__ import annotations

import argparse
import random
import re
import time

from common import ROOT, get_contexts, load_corpus_text, load_questions
from predictions import PRED_DIR, gold_fields, write_predictions

_YEAR_RE = re.compile(r"(?<!\d)(?:1\d{3}|20\d{2})(?!\d)")
_cache: dict[str, list[str]] = {}


def candidates(passage: str) -> list[str]:
    """Các cụm danh từ + năm (không trùng, giữ thứ tự xuất hiện)."""
    if passage in _cache:
        return _cache[passage]
    from underthesea import chunk
    spans, cur = [], []
    for word, _pos, tag in chunk(passage):
        if tag == "B-NP" or (tag == "I-NP" and not cur):
            if cur:
                spans.append(" ".join(cur))
            cur = [word]
        elif tag == "I-NP":
            cur.append(word)
        else:
            if cur:
                spans.append(" ".join(cur))
            cur = []
    if cur:
        spans.append(" ".join(cur))
    spans += _YEAR_RE.findall(passage)
    seen, out = set(), []
    for s in spans:
        if s not in seen and re.search(r"\w", s):
            seen.add(s)
            out.append(s)
    _cache[passage] = out
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="dev")
    ap.add_argument("--context", choices=["gold", "retrieved"], default="retrieved")
    ap.add_argument("--mode", default="hybrid", help="chế độ retriever khi --context retrieved")
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--run", default=None)
    args = ap.parse_args()

    run = args.run or f"b0_{args.context}_{args.split}"
    qa = load_questions(args.split, args.limit)
    text = load_corpus_text()
    ctxs, ret_ms = get_contexts(qa, args.context, k=1, mode=args.mode)

    rng = random.Random(args.seed)
    rows, t0 = [], time.perf_counter()
    for q, cs in zip(qa.itertuples(), ctxs):
        top = cs[0]["context_id"]
        cands = candidates(text[top])
        pred = rng.choice(cands) if cands else ""
        rows.append({**gold_fields(q), "prediction": pred, "context_source": args.context,
                     "contexts": cs, "used_context_id": top,
                     "latency_ms": {"retrieve": ret_ms}, "extra": {"n_candidates": len(cands)}})
    print(f"B0: {len(rows)} câu, {time.perf_counter() - t0:.1f}s")
    write_predictions(PRED_DIR / f"{run}.jsonl", rows,
                      meta={**vars(args), "run": run, "model": "B0-random-NP/year"})


if __name__ == "__main__":
    main()
