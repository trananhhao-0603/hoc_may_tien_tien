"""
Giai đoạn 5 — phần CPU sau scripts/gd5_pipeline.py: top-k con, chọn ngưỡng từ chối, chấm, bảng E1–E6.

    python scripts/gd5_report.py

1. Mỗi file *_k5_{split}_rs.jsonl -> k1, k3 (src/reader/subset_k.py).
2. Mỗi file dev *_rs: chọn δ tối đa F1 trên dev (tune_refusal) -> *_thr; file test cùng cấu hình
   dùng ĐÚNG δ đó (không chọn lại trên test).
3. Chấm toàn bộ (evaluate_pipeline) -> reports/gd5_dev.{md,json}, reports/gd5_test.{md,json}.
4. Bảng tổng hợp E1–E6, 3 seed, bootstrap CI test -> reports/gd5_results.md (+ gd5_deltas.json).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
for sub in ("src/reader", "src/eval"):
    sys.path.insert(0, str(ROOT / sub))
from subset_k import subset  # noqa: E402
from tune_refusal import decide, sweep  # noqa: E402
from predictions import PRED_DIR, read_predictions, write_predictions  # noqa: E402
from evaluate_pipeline import _fill_gold, evaluate, report, score_rows  # noqa: E402
import bootstrap  # noqa: E402

GRID = np.round(np.arange(-1.5, 1.5 + 1e-9, 0.02), 4)
COLS = ["EM", "F1", "HasAns_F1", "NoAns_acc", "HasAns_abstain"]
TAGS = {"r2m": "R2 (chính, seed 42)", "r2noimp": "E4: R2 bỏ câu không trả lời được",
        "r2ood": "E5: R2 + 10k ViQuAD ngoài miền", "r2s13": "R2 seed 13", "r2s7": "R2 seed 7"}


def step_subset() -> None:
    for f in sorted(PRED_DIR.glob("r2*_k5_*_rs.jsonl")):
        meta, rows = read_predictions(f)
        for k in (1, 3):
            run = f.stem.replace("_k5_", f"_k{k}_")
            if not (PRED_DIR / f"{run}.jsonl").exists():
                write_predictions(PRED_DIR / f"{run}.jsonl", [subset(r, k) for r in rows],
                                  meta={**meta, "run": run, "k": k, "derived_from": f.name})


def apply_delta(src: Path, delta: float, chosen_on: str) -> None:
    meta, rows = read_predictions(src)
    out = []
    for r in rows:
        ans, sc, used = decide(r, delta)
        out.append({**r, "prediction": ans, "used_context_id": used,
                    "extra": {**r["extra"], "score": sc, "refusal_delta": delta}})
    run = src.stem.removesuffix("_rs") + "_thr"
    write_predictions(PRED_DIR / f"{run}.jsonl", out,
                      meta={**meta, "run": run, "refusal_delta": delta,
                            "refusal_delta_chosen_on": chosen_on, "source": src.name})


def step_thresholds() -> dict:
    deltas = {}
    for f in sorted(PRED_DIR.glob("r2*_dev_rs.jsonl")):
        _, rows = read_predictions(f)
        best_d, best = max(sweep(rows, GRID), key=lambda x: (x[1]["F1"], -abs(x[0])))
        key = f.stem.removesuffix("_dev_rs")
        deltas[key] = {"delta": float(best_d), "dev_F1": best["F1"]}
        apply_delta(f, float(best_d), "dev")
        t = PRED_DIR / f"{key}_test_rs.jsonl"
        if t.exists():
            apply_delta(t, float(best_d), f"dev ({f.name})")
    (ROOT / "reports/gd5_deltas.json").write_text(json.dumps(deltas, indent=2), encoding="utf-8")
    return deltas


def step_evaluate(split: str) -> dict:
    qa = pd.read_parquet(ROOT / "data/processed/qa_pairs.parquet")
    corpus = pd.read_parquet(ROOT / "data/processed/corpus.parquet", columns=["context_id", "context"])
    text = dict(zip(corpus.context_id, corpus.context))
    files = sorted(PRED_DIR.glob(f"r2*_{split}_rs.jsonl")) + sorted(PRED_DIR.glob(f"r2*_{split}_thr.jsonl"))
    if split == "dev":
        files = [PRED_DIR / f"{r}.jsonl" for r in ("b1_gold_dev", "r1_gold_dev", "r1_retrieved_k3_dev")
                 if (PRED_DIR / f"{r}.jsonl").exists()] + files
    res, md = {}, []
    for f in files:
        meta, rows = read_predictions(f)
        _fill_gold(rows, qa)
        r = evaluate(score_rows(rows, text))
        res[f.stem] = {"meta": meta, **r}
        md.append(report(f.stem, meta, r))
    out = ROOT / f"reports/gd5_{split}"
    out.with_suffix(".md").write_text(f"# Kết quả GĐ5 — {split}\n\n" + "\n".join(md), encoding="utf-8")
    out.with_suffix(".json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    return res


# ------------------------------------------------------------------ bảng
def fmt(x) -> str:
    return "–" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.1f}"


def row_of(res: dict, run: str, cols=COLS) -> list:
    r = res.get(run)
    return [r["overall"][c] if r else None for c in cols]


def table(head: list[str], rows: list[list]) -> str:
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(x if isinstance(x, str) else fmt(x) for x in r) + " |" for r in rows]
    return "\n".join(out) + "\n"


def best_cfg(dev: dict, tag: str, modes=("hybrid", "bm25", "dense")) -> str | None:
    """Cấu hình truy hồi (mode, k) tốt nhất trên dev theo F1 sau ngưỡng."""
    cands = [f"{tag}_{m}_k{k}" for m in modes for k in (1, 3, 5) if f"{tag}_{m}_k{k}_dev_thr" in dev]
    return max(cands, key=lambda c: dev[f"{c}_dev_thr"]["overall"]["F1"]) if cands else None


def build_tables(dev: dict, test: dict, deltas: dict) -> str:
    md = ["# Giai đoạn 5 — Kết quả thí nghiệm\n",
          "Sinh bởi `scripts/gd5_report.py`. **greedy** = giải mã tham lam như GĐ4; **ngưỡng** = "
          "từ chối chỉ khi `điểm từ chối − điểm đáp án thay thế > δ`, δ chọn trên dev theo F1 "
          "cho từng cấu hình và áp nguyên cho test. Test chạy đúng một lần.\n"]
    main = json.loads((ROOT / "models/gd5_main.json").read_text(encoding="utf-8"))
    md.append(f"Model chính: `{main['main_model']}` (lr {main['lr']}, {main['epochs']} epoch); "
              f"ứng viên (F1 dev đoạn đúng): "
              + ", ".join(f"`{k}` {v:.1f}" for k, v in main["candidates"].items()) + "\n")
    bc = best_cfg(dev, "r2m", ("hybrid",)) or "r2m_hybrid_k3"
    bc_any = best_cfg(dev, "r2m") or bc
    md.append(f"Cấu hình hybrid tốt nhất trên dev: `{bc}`; tốt nhất mọi retriever: `{bc_any}`.\n")

    # E1
    md.append("## E1 — Trích xuất (B1) vs sinh (ViT5), đọc trên đoạn đúng\n")
    rows = [["B1 XLM-R (dev)", *row_of(dev, "b1_gold_dev")], ["R1 ViT5 (dev)", *row_of(dev, "r1_gold_dev")],
            ["R2 greedy (dev)", *row_of(dev, "r2m_gold_dev_rs")], ["R2 ngưỡng (dev)", *row_of(dev, "r2m_gold_dev_thr")],
            ["R2 greedy (test)", *row_of(test, "r2m_gold_test_rs")], ["R2 ngưỡng (test)", *row_of(test, "r2m_gold_test_thr")]]
    md.append(table(["Run", *COLS], rows))
    md.append("B1, R1 chỉ có checkpoint trên Drive nên chưa chấm test (cần chạy trên Colab).\n")

    # E2
    md.append("## E2 — Retriever × k (Reader R2 chính, F1 sau ngưỡng; trong ngoặc: greedy)\n")
    for split, res in (("dev", dev), ("test", test)):
        rows = []
        for m in ("bm25", "dense", "hybrid"):
            cells = []
            for k in (1, 3, 5):
                a, g = res.get(f"r2m_{m}_k{k}_{split}_thr"), res.get(f"r2m_{m}_k{k}_{split}_rs")
                cells.append(f"{fmt(a['overall']['F1']) if a else '–'} ({fmt(g['overall']['F1']) if g else '–'})")
            rows.append([m, *cells])
        md.append(f"**{split}**\n\n" + table(["Retriever", "k=1", "k=3", "k=5"], rows))
    rows = []
    for m in ("bm25", "dense", "hybrid"):
        rows.append([m, *[(dev.get(f"r2m_{m}_k{k}_dev_thr") or {}).get("retrieval", {}).get("gold_in_ctx")
                          for k in (1, 3, 5)]])
    md.append("Tỉ lệ đoạn đúng nằm trong k đoạn đã đọc (dev, câu trả lời được):\n\n"
              + table(["Retriever", "k=1", "k=3", "k=5"], rows))

    # E3
    md.append("## E3 — Đoạn đúng vs đoạn tự tìm (tách sai số tìm / đọc)\n")
    rows = []
    for split, res in (("dev", dev), ("test", test)):
        g, r = res.get(f"r2m_gold_{split}_thr"), res.get(f"{bc}_{split}_thr")
        ret = (r or {}).get("retrieval", {})
        rows.append([split, fmt(g["overall"]["F1"]) if g else "–", fmt(r["overall"]["F1"]) if r else "–",
                     fmt(ret.get("gold_in_ctx")), fmt(ret.get("HasAns_F1_hit")), fmt(ret.get("HasAns_F1_miss"))])
    md.append(table(["Tập", "F1 đoạn đúng", f"F1 {bc}", "đoạn đúng trong top-k %",
                     "HasAns-F1 khi tìm đúng", "HasAns-F1 khi tìm sai"], rows))

    # E4, E5
    for title, tag in (("E4 — Có vs không có câu không trả lời được khi train", "r2noimp"),
                       ("E5 — Thêm ViQuAD ngoài miền khi train", "r2ood")):
        md.append(f"## {title}\n")
        rows = []
        for split, res in (("dev", dev), ("test", test)):
            for ctx in ("gold", "hybrid_k3"):
                for mode in ("rs", "thr"):
                    for t in ("r2m", tag):
                        rows.append([split, ctx, "greedy" if mode == "rs" else "ngưỡng", TAGS[t],
                                     *row_of(res, f"{t}_{ctx}_{split}_{mode}")])
        md.append(table(["Tập", "Đoạn", "Giải mã", "Model", *COLS], rows))
        if tag == "r2ood":
            rows = []
            for split, res in (("dev", dev), ("test", test)):
                for t in ("r2m", tag):
                    r = res.get(f"{t}_gold_{split}_thr")
                    rows.append([split, TAGS[t], *[r["by_domain"][d]["F1"] if r else None for d in ("VN", "TG")]])
            md.append("F1 theo miền (đoạn đúng, ngưỡng):\n\n" + table(["Tập", "Model", "VN", "TG"], rows))

    # E6
    md.append("## E6 — Tách theo miền và loại câu hỏi (R2 chính, ngưỡng)\n")
    for run_ctx in ("gold", bc.removeprefix("r2m_")):
        for split, res in (("dev", dev), ("test", test)):
            r = res.get(f"r2m_{run_ctx}_{split}_thr")
            if not r:
                continue
            rows = [[d, r["by_domain"][d]["n"], *[r["by_domain"][d][c] for c in COLS]] for d in r["by_domain"]]
            rows += [[q, v["n"], *[v[c] for c in COLS]] for q, v in r["by_qtype"].items()]
            md.append(f"**{run_ctx}, {split}**\n\n" + table(["Nhóm", "n", *COLS], rows))

    # seeds
    md.append("## Ổn định theo seed (R2, seed 42 / 13 / 7): trung bình ± độ lệch chuẩn\n")
    rows = []
    for split, res in (("dev", dev), ("test", test)):
        for ctx in ("gold", "hybrid_k3", bc.removeprefix("r2m_")):
            for mode in ("rs", "thr"):
                vals = [row_of(res, f"{t}_{ctx}_{split}_{mode}") for t in ("r2m", "r2s13", "r2s7")]
                vals = [v for v in vals if v[0] is not None]
                if not vals:
                    continue
                a = np.array(vals, dtype=float)
                rows.append([split, ctx, "greedy" if mode == "rs" else "ngưỡng", str(len(a)),
                             *[f"{m:.1f} ± {s:.1f}" for m, s in zip(a.mean(0), a.std(0, ddof=1) if len(a) > 1 else [0] * len(COLS))]])
    seen, uniq = set(), []
    for r in rows:
        if tuple(r[:3]) not in seen:
            seen.add(tuple(r[:3]))
            uniq.append(r)
    md.append(table(["Tập", "Đoạn", "Giải mã", "số seed", *COLS], uniq))

    # δ
    md.append("## Ngưỡng δ chọn trên dev\n")
    md.append(table(["Cấu hình", "δ", "F1 dev"], [[k, f"{v['delta']:+.2f}", v["dev_F1"]] for k, v in deltas.items()]))
    return "\n".join(md)


def bootstrap_md(test: dict, bc: str) -> str:
    md = ["## Bootstrap CI 95% trên test (2000 lần lấy mẫu lại câu hỏi)\n"]
    rng = np.random.default_rng(0)
    singles = [r for r in (f"r2m_gold_test_thr", f"{bc}_test_thr", "r2m_gold_test_rs", f"{bc}_test_rs")
               if (PRED_DIR / f"{r}.jsonl").exists()]
    if not singles:
        return ""
    data = {r: bootstrap.per_question(PRED_DIR / f"{r}.jsonl") for r in singles}
    n = len(next(iter(data.values()))[0])
    idx = rng.integers(0, n, size=(2000, n))
    full = np.arange(n)[None]
    rows = []
    for r, (_, m, imp) in data.items():
        b, v = bootstrap.stats(m, imp, idx), bootstrap.stats(m, imp, full)[0]
        rows.append([r, *[f"{v[j]:.1f} [{np.percentile(b[:, j], 2.5):.1f}, {np.percentile(b[:, j], 97.5):.1f}]"
                          for j in range(4)]])
    md.append(table(["Run", *bootstrap.METRICS], rows))
    pairs = [("r2m_gold_test_rs", "r2m_gold_test_thr"), ("r2noimp_gold_test_thr", "r2m_gold_test_thr"),
             ("r2ood_gold_test_thr", "r2m_gold_test_thr"), (f"{bc}_test_thr", "r2m_gold_test_thr")]
    rows = []
    for a, b in pairs:
        pa, pb = PRED_DIR / f"{a}.jsonl", PRED_DIR / f"{b}.jsonl"
        if not (pa.exists() and pb.exists()):
            continue
        (ia, ma, xa), (ib, mb, xb) = bootstrap.per_question(pa), bootstrap.per_question(pb)
        if ia != ib:
            continue
        d = bootstrap.stats(mb, xb, idx) - bootstrap.stats(ma, xa, idx)
        d0 = bootstrap.stats(mb, xb, full)[0] - bootstrap.stats(ma, xa, full)[0]
        rows.append([f"{b} − {a}", *[f"{d0[j]:+.1f} [{np.percentile(d[:, j], 2.5):+.1f}, "
                                     f"{np.percentile(d[:, j], 97.5):+.1f}]" for j in range(4)]])
    md.append("Hiệu cặp (cùng câu hỏi):\n\n" + table(["So sánh", *bootstrap.METRICS], rows))
    return "\n".join(md)


def main():
    step_subset()
    deltas = step_thresholds()
    dev, test = step_evaluate("dev"), step_evaluate("test")
    bc = best_cfg(dev, "r2m", ("hybrid",)) or "r2m_hybrid_k3"
    text = build_tables(dev, test, deltas) + "\n" + bootstrap_md(test, bc)
    (ROOT / "reports/gd5_results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
