"""
Giai đoạn 6 — đo độ trễ từng khâu của pipeline, mỗi lần một câu hỏi (như khi dùng demo).

    python scripts/latency.py --device cuda --n 100
    python scripts/latency.py --device cpu  --n 50
    python scripts/latency.py --report          # gộp reports/latency_*.json -> reports/latency.md

Câu hỏi lấy ngẫu nhiên từ dev (seed 0). Chạy 5 câu khởi động trước, không tính.
--device cpu ẩn GPU (CUDA_VISIBLE_DEVICES="") để cả bi-encoder lẫn ViT5 chạy trên CPU.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGES = ["bm25", "dense", "fuse", "retrieve", "read", "total"]


def cpu_name() -> str:
    try:                                                   # Windows: tên đầy đủ trong registry
        import winreg
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
        return winreg.QueryValueEx(k, "ProcessorNameString")[0].strip()
    except Exception:
        return platform.processor() or platform.machine()


def measure(args):
    if args.device == "cpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
    sys.path.insert(0, str(ROOT))
    import numpy as np
    import pandas as pd
    import torch

    from src.pipeline import QAPipeline

    if args.threads:
        torch.set_num_threads(args.threads)
    qa = pd.read_parquet(ROOT / "data/processed/qa_pairs.parquet", columns=["question", "split"])
    qs = qa[qa.split == "dev"].sample(args.n + 5, random_state=0).question.tolist()
    pipe = QAPipeline.load(args.model, device=args.device)
    res = {}
    for k in args.k:
        for q in qs[:5]:
            pipe.answer(q, k)                                   # khởi động
        rows = [pipe.answer(q, k)["latency_ms"] for q in qs[5:]]
        res[f"k{k}"] = {s: {"mean": float(np.mean([r[s] for r in rows])),
                            "p50": float(np.percentile([r[s] for r in rows], 50)),
                            "p90": float(np.percentile([r[s] for r in rows], 90))} for s in STAGES}
        print(f"k={k}: " + ", ".join(f"{s} {res[f'k{k}'][s]['p50']:.0f}" for s in STAGES) + " ms (p50)")
    hw = torch.cuda.get_device_name(0) if args.device == "cuda" else cpu_name()
    out = {"device": args.device, "hardware": hw, "threads": torch.get_num_threads(),
           "n": args.n, "model": str(args.model), "torch": torch.__version__, "results": res}
    p = ROOT / f"reports/latency_{args.device}.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("->", p)


def report():
    runs = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "reports").glob("latency_*.json"))]
    names = {"bm25": "BM25", "dense": "Dense (mã hoá câu hỏi + cosine)", "fuse": "RRF + top-k",
             "retrieve": "**Truy hồi (tổng)**", "read": "**Reader ViT5 (k đoạn)**", "total": "**Tổng**"}
    lines = ["# Độ trễ pipeline (Giai đoạn 6)", "",
             "Mỗi lần một câu hỏi, đơn vị ms, trung vị (p90 trong ngoặc). Câu hỏi ngẫu nhiên từ dev; "
             "5 câu khởi động không tính. Reader đọc k đoạn trong một batch. "
             "Tạo bởi `scripts/latency.py`.", ""]
    for r in runs:
        lines.append(f"- **{r['device'].upper()}**: {r['hardware']}, torch {r['torch']}, "
                     f"{r['threads']} luồng, n = {r['n']} câu, model `{Path(r['model']).name}`")
    cols = [(r["device"], k) for r in runs for k in r["results"]]
    lines += ["", "| Khâu | " + " | ".join(f"{d.upper()} k={k[1:]}" for d, k in cols) + " |",
              "|---|" + "---|" * len(cols)]
    by = {(r["device"], k): r["results"][k] for r in runs for k in r["results"]}
    for s in STAGES:
        lines.append(f"| {names[s]} | " + " | ".join(
            f"{by[c][s]['p50']:.0f} ({by[c][s]['p90']:.0f})" if by[c][s]['p50'] >= 1
            else f"{by[c][s]['p50']:.1f} ({by[c][s]['p90']:.1f})" for c in cols) + " |")
    out = ROOT / "reports/latency.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", choices=["cuda", "cpu"], default="cuda")
    ap.add_argument("--model", default=str(ROOT / "models/r2_ood"))
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--k", type=int, nargs="+", default=[1, 5])
    ap.add_argument("--threads", type=int, default=None)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    report() if args.report else measure(args)


if __name__ == "__main__":
    main()
