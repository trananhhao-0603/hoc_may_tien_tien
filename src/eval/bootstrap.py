"""
Giai đoạn 5: khoảng tin cậy 95% bằng bootstrap (lấy mẫu lại câu hỏi, có hoàn lại).

  Một file:      python src/eval/bootstrap.py data/predictions/r2_gold_test_thr.jsonl
  So sánh cặp:   python src/eval/bootstrap.py A.jsonl B.jsonl --paired
                 (cùng tập câu; CI của hiệu B − A và p ≈ tỉ lệ mẫu có hiệu ≤ 0)
  Ghi markdown:  --out reports/bootstrap_test.md

Mặc định 2000 lần lấy mẫu, seed 0. Chỉ số: EM, F1, HasAns_F1, NoAns_acc (thang 0–100).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from metrics import score  # noqa: E402
from predictions import read_predictions  # noqa: E402

METRICS = ["EM", "F1", "HasAns_F1", "NoAns_acc"]


def per_question(path) -> tuple[list[str], np.ndarray, np.ndarray]:
    """-> (qa_ids, ma trận [n, 2] = (exact, f1) thang 0–1, mảng is_impossible)."""
    _, rows = read_predictions(path)
    s = [score(r["prediction"], r["gold_answers"], r["is_impossible"]) for r in rows]
    m = np.array([[x["em"], x["f1"]] for x in s], dtype=float)
    return [r["qa_id"] for r in rows], m, np.array([bool(r["is_impossible"]) for r in rows])


def stats(m: np.ndarray, imp: np.ndarray, idx: np.ndarray) -> np.ndarray:
    """idx: [B, n] chỉ số lấy mẫu -> [B, 4] (EM, F1, HasAns_F1, NoAns_acc)."""
    ex, f1, im = m[idx, 0], m[idx, 1], imp[idx]
    has = ~im
    with np.errstate(invalid="ignore", divide="ignore"):
        hf1 = (f1 * has).sum(1) / has.sum(1)
        nacc = (ex * im).sum(1) / im.sum(1)
    return 100 * np.stack([ex.mean(1), f1.mean(1), hf1, nacc], 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("preds", nargs="+")
    ap.add_argument("--paired", action="store_true")
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)

    data = [per_question(p) for p in args.preds]
    n = len(data[0][0])
    idx = rng.integers(0, n, size=(args.n, n))
    full = np.arange(n)[None]
    lines = []
    if args.paired:
        if len(data) != 2 or data[0][0] != data[1][0]:
            raise SystemExit("--paired cần đúng 2 file cùng danh sách qa_id, cùng thứ tự")
        (_, ma, ia), (_, mb, ib) = data
        d = stats(mb, ib, idx) - stats(ma, ia, idx)
        d0 = stats(mb, ib, full)[0] - stats(ma, ia, full)[0]
        lines.append(f"| {Path(args.preds[1]).stem} − {Path(args.preds[0]).stem} | "
                     + " | ".join(f"{d0[j]:+.1f} [{np.percentile(d[:, j], 2.5):+.1f}, "
                                  f"{np.percentile(d[:, j], 97.5):+.1f}] p={np.mean(d[:, j] <= 0):.3f}"
                                  for j in range(len(METRICS))) + " |")
    else:
        for p, (_, m, imp) in zip(args.preds, data):
            if len(m) != n:
                raise SystemExit("Các file phải cùng số câu")
            b, v = stats(m, imp, idx), stats(m, imp, full)[0]
            lines.append(f"| {Path(p).stem} | " + " | ".join(
                f"{v[j]:.1f} [{np.percentile(b[:, j], 2.5):.1f}, {np.percentile(b[:, j], 97.5):.1f}]"
                for j in range(len(METRICS))) + " |")
    head = (f"| run | {' | '.join(METRICS)} |\n|---|" + "---|" * len(METRICS)
            + f"\n")
    txt = (f"Bootstrap {args.n} lần, n = {n} câu, CI 95%"
           + (" (hiệu cặp)" if args.paired else "") + "\n\n" + head + "\n".join(lines) + "\n")
    print(txt)
    if args.out:
        out = Path(args.out).with_suffix(".md")
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("a", encoding="utf-8") as f:
            f.write(txt + "\n")


if __name__ == "__main__":
    main()
