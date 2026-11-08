"""
Giai đoạn 5: chỉnh ngưỡng từ chối cho Reader ViT5, không chạy lại mô hình.

Đầu vào là file dự đoán sinh bằng `infer.py --refusal_scores`. Với mỗi cặp (câu, đoạn):
    từ chối  <=>  refuse_score - alt_score > δ
(alt = đáp án tốt nhất khi cấm từ chối). δ lớn -> mô hình trả lời nhiều hơn. Sau đó chọn
đáp án giữa các đoạn như cũ (pick(): điểm cao nhất trong các đáp án không phải từ chối).

  Chọn δ trên dev (tối đa F1), ghi file dự đoán mới:
    python src/reader/tune_refusal.py data/predictions/r2_gold_dev_rs.jsonl --run r2_gold_dev_thr
  Áp δ đã chọn cho file khác (vd. top-3 dev, hoặc test — KHÔNG chọn lại δ trên test):
    python src/reader/tune_refusal.py data/predictions/r2_retrieved_k3_test_rs.jsonl --delta 0.35
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

import common  # noqa: F401  (thêm src/eval vào sys.path)
from infer import pick
from metrics import NO_ANSWER, aggregate, score
from predictions import PRED_DIR, read_predictions, write_predictions


def decide(row: dict, delta: float) -> tuple[str, float, str | None]:
    cands = []
    for pc in row["extra"]["per_context"]:
        if "refuse_score" not in pc:
            raise SystemExit("File thiếu refuse_score — chạy infer.py với --refusal_scores")
        if pc["refuse_score"] - pc["alt_score"] > delta:
            cands.append((NO_ANSWER, pc["refuse_score"], pc["context_id"]))
        else:
            cands.append((pc["alt_answer"], pc["alt_score"], pc["context_id"]))
    return pick(cands)


def evaluate(rows: list[dict], preds: list[str]) -> dict:
    return aggregate([{**score(p, r["gold_answers"], r["is_impossible"]),
                       "is_impossible": r["is_impossible"]} for p, r in zip(preds, rows)])


def sweep(rows: list[dict], deltas) -> list[tuple[float, dict]]:
    return [(d, evaluate(rows, [decide(r, d)[0] for r in rows])) for d in deltas]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pred", help="file .jsonl sinh bằng infer.py --refusal_scores")
    ap.add_argument("--delta", type=float, default=None, help="áp δ cố định (không dò)")
    ap.add_argument("--grid", default="-1.5,1.5,0.02", help="dò δ: min,max,bước")
    ap.add_argument("--run", default=None, help="tên file dự đoán ghi ra (mặc định <tên>_thr)")
    args = ap.parse_args()

    meta, rows = read_predictions(args.pred)
    greedy = evaluate(rows, [r["prediction"] for r in rows])
    cols = ["EM", "F1", "HasAns_F1", "NoAns_acc", "HasAns_abstain"]
    print("Greedy (không ngưỡng): " + "  ".join(f"{c} {greedy[c]:.1f}" for c in cols))

    if args.delta is None:
        lo, hi, step = (float(x) for x in args.grid.split(","))
        res = sweep(rows, np.round(np.arange(lo, hi + step / 2, step), 4))
        best_d, best = max(res, key=lambda x: (x[1]["F1"], -abs(x[0])))
        print(f"\n{'δ':>6} " + " ".join(f"{c:>14}" for c in cols))
        for d, m in res[:: max(1, len(res) // 24)] + [(best_d, best)]:
            mark = "  <- tốt nhất" if d == best_d else ""
            print(f"{d:>6.2f} " + " ".join(f"{m[c]:>14.1f}" for c in cols) + mark)
        delta, chosen = best_d, "dev"
    else:
        delta, chosen = args.delta, "cố định"
    m = evaluate(rows, [decide(r, delta)[0] for r in rows])
    print(f"\nδ = {delta} ({chosen}): " + "  ".join(f"{c} {m[c]:.1f}" for c in cols))

    out = []
    for r in rows:
        ans, sc, used = decide(r, delta)
        out.append({**r, "prediction": ans, "used_context_id": used,
                    "extra": {**r["extra"], "score": sc, "refusal_delta": delta}})
    run = args.run or Path(args.pred).stem.removesuffix("_rs") + "_thr"
    write_predictions(PRED_DIR / f"{run}.jsonl", out,
                      meta={**meta, "run": run, "refusal_delta": delta,
                            "refusal_delta_chosen_on": chosen, "source": Path(args.pred).name})


if __name__ == "__main__":
    main()
