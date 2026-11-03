"""
Đánh giá Retriever: Recall@k, MRR cho mọi cấu hình (BM25 / dense / hybrid × cách tách).
Đoạn đúng (gold) = context_id của câu hỏi.

Mặc định chỉ chạy trên DEV (chọn cấu hình). Test chỉ chạy một lần ở Giai đoạn 5.
Retriever không được huấn luyện nên chạy trên train cũng hợp lệ (mẫu lớn hơn).

Chạy:
    python src/retriever/eval_retriever.py --split dev
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hybrid import Retriever  # noqa: E402

KS = (1, 3, 5, 10, 20)
# (tên, mode, bm25_tok, dense_input, rrf_k, w_dense)
CONFIGS = [
    ("BM25 · âm tiết",            "bm25",   "syl", None,  None, None),
    ("BM25 · tách từ",            "bm25",   "seg", None,  None, None),
    ("Dense · văn bản thô",       "dense",  None,  "raw", None, None),
    ("Dense · tách từ",           "dense",  None,  "seg", None, None),
    ("Hybrid · BM25 âm tiết + Dense tách từ (k=60, w=1)", "hybrid", "syl", "seg", 60, 1.0),
    ("Hybrid · BM25 tách từ + Dense tách từ (k=60, w=1)", "hybrid", "seg", "seg", 60, 1.0),
    ("**Hybrid · BM25 âm tiết + Dense tách từ (k=5, w=0.7) — chọn**",
     "hybrid", "syl", "seg", 5, 0.7),
]


def metrics(gold_rank: np.ndarray) -> dict:
    m = {f"R@{k}": float((gold_rank < k).mean()) for k in KS}
    m["MRR"] = float((1.0 / (gold_rank + 1)).mean())
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index_dir", default="data/index_qa")
    ap.add_argument("--qa", default="data/processed/qa_pairs.parquet")
    ap.add_argument("--split", default="dev")
    ap.add_argument("--include_impossible", action="store_true",
                    help="tính cả câu không trả lời được (mặc định: chỉ câu trả lời được)")
    ap.add_argument("--outdir", default="reports")
    ap.add_argument("--sweep", action="store_true",
                    help="quét trọng số dense / k của RRF (chỉ dev) -> reports/retriever_<split>_sweep.csv")
    args = ap.parse_args()

    if args.split == "test":
        print("⚠️  Đang chạy trên TEST — chỉ nên làm MỘT LẦN cho cấu hình cuối (PLAN.md §5).")

    r = Retriever.load(args.index_dir)
    qa = pd.read_parquet(args.qa)
    qa = qa[qa.split == args.split]
    if not args.include_impossible:
        qa = qa[~qa.is_impossible]
    qa = qa.reset_index(drop=True)
    pos = {cid: i for i, cid in enumerate(r.meta.context_id)}
    missing = (~qa.context_id.isin(pos)).sum()
    assert missing == 0, f"{missing} câu hỏi có đoạn đúng không nằm trong index"
    gold = qa.context_id.map(pos).to_numpy()
    questions = qa.question.tolist()
    n = len(questions)
    print(f"Đánh giá {n} câu hỏi ({args.split}) trên {len(r.meta)} đoạn")

    # tính mỗi ma trận điểm một lần, tái dùng cho hybrid
    cache, secs = {}, {}
    for name, mode, tok, inp, _, _ in CONFIGS:
        for key in ([("bm25", tok)] if mode in ("bm25", "hybrid") else []) + \
                   ([("dense", inp)] if mode in ("dense", "hybrid") else []):
            if key not in cache:
                t0 = time.time()
                cache[key] = (r.bm25_scores(questions, key[1]) if key[0] == "bm25"
                              else r.dense_scores(questions, key[1]))
                secs[key] = time.time() - t0

    rows, by_domain = [], []
    rows_idx = np.arange(n)
    for name, mode, tok, inp, rk, w in CONFIGS:
        if mode == "bm25":
            s, t = cache[("bm25", tok)], secs[("bm25", tok)]
        elif mode == "dense":
            s, t = cache[("dense", inp)], secs[("dense", inp)]
        else:
            s = r.rrf(cache[("bm25", tok)], cache[("dense", inp)], weights=[1.0, w], k=rk)
            t = secs[("bm25", tok)] + secs[("dense", inp)]
        gr = Retriever.ranks(s)[rows_idx, gold]
        rows.append({"Cấu hình": name, **metrics(gr), "ms/câu": 1000 * t / n})
        for vn, lab in [(True, "VN"), (False, "TG")]:
            mask = (qa.is_vietnam == vn).to_numpy()
            if mask.any():
                by_domain.append({"Cấu hình": name, "Miền": lab, "n": int(mask.sum()),
                                  **{k: v for k, v in metrics(gr[mask]).items()
                                     if k in ("R@1", "R@5", "MRR")}})

    res = pd.DataFrame(rows)
    dom = pd.DataFrame(by_domain)
    best = res.sort_values(["R@5", "MRR"], ascending=False).iloc[0]["Cấu hình"]

    def md(df: pd.DataFrame) -> str:
        cols = list(df.columns)
        out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
        for _, row in df.iterrows():
            cells = []
            for c in cols:
                v = row[c]
                if c.startswith("R@") or c == "MRR":
                    cells.append(f"{100 * v:.1f}" if c != "MRR" else f"{v:.3f}")
                elif c == "ms/câu":
                    cells.append(f"{v:.1f}")
                else:
                    cells.append(str(v))
            out.append("| " + " | ".join(cells) + " |")
        return "\n".join(out)

    scope = "mọi câu" if args.include_impossible else "câu trả lời được"
    report = "\n".join([
        f"# Đánh giá Retriever — split `{args.split}` ({n} {scope}, {len(r.meta)} đoạn)", "",
        "R@k tính bằng %. ms/câu: thời gian chấm điểm toàn kho trên CPU (đã gồm tách từ, "
        "nhúng câu hỏi).", "",
        md(res), "", f"**Tốt nhất theo R@5:** {best}", "",
        "## Theo tiểu miền", "", md(dom), ""])
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    suffix = "_all" if args.include_impossible else ""
    (out / f"retriever_{args.split}{suffix}.md").write_text(report, encoding="utf-8")
    (out / f"retriever_{args.split}{suffix}.json").write_text(
        json.dumps({"overall": rows, "by_domain": by_domain, "best": best},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(report)

    if args.sweep:
        sweep(r, cache, gold, args, n)


W_DENSE = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0)
RRF_KS = (5, 10, 30, 60)


def sweep(r: Retriever, cache: dict, gold: np.ndarray, args, n: int):
    """Quét trọng số dense và hằng số k của RRF (BM25 luôn trọng số 1). Chỉ chạy trên dev."""
    if args.split == "test":
        raise SystemExit("Không quét siêu tham số trên test.")
    rows_idx = np.arange(n)
    rows = []
    for tok in ("syl", "seg"):
        for k in RRF_KS:
            for w in W_DENSE:
                s = r.rrf(cache[("bm25", tok)], cache[("dense", "seg")], weights=[1.0, w], k=k)
                gr = Retriever.ranks(s)[rows_idx, gold]
                rows.append({"BM25": tok, "k": k, "w_dense": w, **metrics(gr)})
    df = pd.DataFrame(rows)
    df.to_csv(Path(args.outdir) / f"retriever_{args.split}_sweep.csv", index=False)
    top = df.sort_values(["R@5", "MRR"], ascending=False).head(10)
    piv = df[df.k == 60].pivot_table(index="w_dense", columns="BM25", values=["R@1", "R@5", "MRR"])
    print("\n# Quét RRF có trọng số (dense = tách từ) — top 10 theo R@5\n")
    print(top.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\n# k = 60, theo w_dense\n")
    print(piv.to_string(float_format=lambda x: f"{x:.3f}"))


if __name__ == "__main__":
    main()
