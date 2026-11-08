"""
Giai đoạn 5 (E2): suy ra kết quả top-k (k nhỏ hơn) từ một file dự đoán top-K, không chạy lại.

infer.py đọc TỪNG đoạn riêng rồi chọn đáp án bằng pick(), nên kết quả top-k đúng bằng việc
giữ k đoạn có rank nhỏ nhất trong per_context rồi chọn lại. Giữ nguyên các trường
refuse_score / alt_* để tune_refusal.py dùng tiếp.

    python src/reader/subset_k.py data/predictions/r2_hybrid_k5_dev_rs.jsonl --k 1 3
      -> r2_hybrid_k1_dev_rs.jsonl, r2_hybrid_k3_dev_rs.jsonl
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import common  # noqa: F401  (thêm src/eval vào sys.path)
from infer import pick
from predictions import PRED_DIR, read_predictions, write_predictions


def subset(row: dict, k: int) -> dict:
    keep = [c for c in row["contexts"] if c["rank"] <= k]
    ids = {c["context_id"] for c in keep}
    pcs = [pc for pc in row["extra"]["per_context"] if pc["context_id"] in ids]
    ans, sc, used = pick([(pc["answer"], pc["score"], pc["context_id"]) for pc in pcs])
    return {**row, "contexts": keep, "prediction": ans, "used_context_id": used,
            "extra": {**row["extra"], "score": sc, "per_context": pcs}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pred")
    ap.add_argument("--k", type=int, nargs="+", required=True)
    args = ap.parse_args()
    meta, rows = read_predictions(args.pred)
    stem = Path(args.pred).stem
    if not re.search(r"_k\d+", stem):
        raise SystemExit("Tên file phải chứa _k<K>")
    for k in args.k:
        if k > int(meta.get("k", 10 ** 9)):
            raise SystemExit(f"k={k} lớn hơn K của file ({meta.get('k')})")
        run = re.sub(r"_k\d+", f"_k{k}", stem, count=1)
        write_predictions(PRED_DIR / f"{run}.jsonl", [subset(r, k) for r in rows],
                          meta={**meta, "run": run, "k": k, "derived_from": Path(args.pred).name})


if __name__ == "__main__":
    main()
