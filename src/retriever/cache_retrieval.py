"""
Tính sẵn top-K của Retriever cho train + dev -> data/processed/retrieved_{mode}.parquet.

Lý do: data/index_qa/ không nằm trong git (nên không có trong hmtt.zip trên Colab).
File cache nhỏ (~200k dòng) nên commit được; get_contexts() dùng cache nếu có.
KHÔNG tính cho test (test chỉ chạy một lần ở Giai đoạn 5).

    python src/retriever/cache_retrieval.py            # hybrid, top 20, train+dev
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "reader"))
from common import get_contexts, load_questions  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="hybrid")
    ap.add_argument("--k", type=int, default=20)
    ap.add_argument("--splits", default="train,dev")
    args = ap.parse_args()
    if "test" in args.splits.split(","):
        raise SystemExit("Không cache test (PLAN.md §5)")

    rows = []
    for split in args.splits.split(","):
        qa = load_questions(split)
        ctxs, ms = get_contexts(qa, "retrieved", k=args.k, mode=args.mode, use_cache=False)
        print(f"{split}: {len(qa)} câu, {ms:.1f} ms/câu")
        for qid, cs in zip(qa.qa_id, ctxs):
            rows += [{"qa_id": qid, "split": split, "rank": c["rank"], "context_id": c["context_id"],
                      "score": c["score"], "retrieve_ms": ms} for c in cs]
    out = ROOT / f"data/processed/retrieved_{args.mode}.parquet"
    pd.DataFrame(rows).to_parquet(out, index=False)
    print(f"Đã ghi {len(rows)} dòng -> {out}")


if __name__ == "__main__":
    main()
