"""
Build kho tri thức cho Retriever: metadata + FAISS (dense). Chạy MỘT LẦN.

Khác dự án cũ:
  - Index CẢ 3 split. Với hỏi đáp, đoạn văn là KHO TRI THỨC hệ thống được tra cứu;
    thứ phải giấu là cặp hỏi–đáp của test (xem PLAN.md §2), không phải đoạn văn.
  - Đoạn văn được TÁCH TỪ trước khi nhúng: bkai vietnamese-bi-encoder (PhoBERT)
    yêu cầu input đã tách từ. Bản "raw" (không tách từ) chỉ để so sánh.
  - BM25 KHÔNG lưu pickle: dựng lại từ meta.parquet khi load (< 1 giây).

Đầu ra (data/index_qa/):
  meta.parquet        context_id, title, context, context_seg, split, is_vietnam
  dense_seg.faiss     FAISS IndexFlatIP trên embedding đã chuẩn hoá (cosine)
  dense_raw.faiss     (tuỳ chọn, --dense_inputs seg,raw)
  info.json           model, số đoạn, tỉ lệ đoạn bị cắt do max_seq_length...

Chạy:
    python src/retriever/build_index.py
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from text import segment  # noqa: E402

EMBED_MODEL = "bkai-foundation-models/vietnamese-bi-encoder"


def encode(model, texts: list[str], batch_size: int):
    return model.encode(texts, batch_size=batch_size, show_progress_bar=True,
                        normalize_embeddings=True, convert_to_numpy=True).astype("float32")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="data/processed/corpus.parquet")
    ap.add_argument("--outdir", default="data/index_qa")
    ap.add_argument("--splits", default="train,dev,test")
    ap.add_argument("--model", default=EMBED_MODEL)
    ap.add_argument("--dense_inputs", default="seg,raw",
                    help="seg = đã tách từ (đúng yêu cầu model); raw = văn bản thô (so sánh)")
    ap.add_argument("--batch_size", type=int, default=32)
    args = ap.parse_args()

    import faiss
    import pandas as pd
    from sentence_transformers import SentenceTransformer

    df = pd.read_parquet(args.corpus)
    df = df[df.split.isin({s.strip() for s in args.splits.split(",")})].reset_index(drop=True)
    print(f"Index {len(df)} đoạn | split: {df.split.value_counts().to_dict()}")

    t0 = time.time()
    df["context_seg"] = [segment(c) for c in df.context]
    print(f"Tách từ xong ({time.time() - t0:.0f}s)")

    model = SentenceTransformer(args.model)
    max_len = model.max_seq_length
    n_tok = [len(model.tokenizer(s, add_special_tokens=True).input_ids) for s in df.context_seg]
    truncated = sum(n > max_len for n in n_tok) / len(n_tok)
    print(f"max_seq_length={max_len} | đoạn bị cắt khi nhúng: {truncated:.1%}")

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    info = {"model": args.model, "n_passages": len(df),
            "splits": df.split.value_counts().to_dict(), "max_seq_length": max_len,
            "pct_passages_truncated": round(100 * truncated, 2), "dense_inputs": []}

    for kind in [k.strip() for k in args.dense_inputs.split(",") if k.strip()]:
        texts = df.context_seg.tolist() if kind == "seg" else df.context.tolist()
        t0 = time.time()
        emb = encode(model, texts, args.batch_size)
        index = faiss.IndexFlatIP(emb.shape[1])     # cosine vì đã normalize
        index.add(emb)
        faiss.write_index(index, str(outdir / f"dense_{kind}.faiss"))
        info["dense_inputs"].append(kind)
        print(f"  dense_{kind}.faiss: {emb.shape} ({time.time() - t0:.0f}s)")

    df[["context_id", "title", "context", "context_seg", "split", "is_vietnam"]].to_parquet(
        outdir / "meta.parquet", index=False)
    (outdir / "info.json").write_text(json.dumps(info, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"\n✅ Đã lưu -> {outdir}/  ({', '.join(p.name for p in sorted(outdir.iterdir()))})")


if __name__ == "__main__":
    main()
