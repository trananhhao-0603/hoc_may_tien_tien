"""
Giai đoạn 5: chạy tuần tự mọi bước cần GPU (train + suy luận), bỏ qua bước đã có đầu ra.

    python scripts/gd5_pipeline.py [--wait_log models/sweep_r2.log]

1. Chọn model R2 chính: F1 dev cao nhất trong các ứng viên (train_config.json -> best_dev_f1);
   lr/epoch của model đó dùng cho mọi lần train sau.
2. Model chính: suy luận dev có --refusal_scores trên đoạn đúng và top-5 của {hybrid, bm25, dense}
   (top-1/top-3 suy ra bằng src/reader/subset_k.py).
3. Train E4 (--no_impossible), E5 (--ood 10000), 2 seed thêm (13, 7); mỗi model suy luận dev
   đoạn đúng + hybrid top-5.
4. TEST (một lần): mọi model đoạn đúng + hybrid top-5; model chính thêm bm25/dense top-5.
Phần chấm điểm / chọn ngưỡng (CPU) làm sau bằng tune_refusal.py, subset_k.py, evaluate_pipeline.py.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
PRED = ROOT / "data/predictions"
CANDIDATES = ["models/r2_vit5", "models/r2_lr3e-4_e5", "models/r2_lr1e-4_e8"]
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUNBUFFERED": "1",
       "HF_HUB_OFFLINE": "1", "HF_DATASETS_OFFLINE": "1"}
FAILED: list[str] = []


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def run(name: str, args: list[str], done: Path) -> bool:
    if done.exists():
        log(f"BỎ QUA {name} (đã có {done.relative_to(ROOT)})")
        return True
    log(f"BẮT ĐẦU {name}: {' '.join(args)}")
    t0 = time.time()
    rc = subprocess.run([PY, *args], cwd=ROOT, env=ENV).returncode
    log(f"{'XONG' if rc == 0 else 'LỖI rc=' + str(rc)} {name} ({(time.time() - t0) / 60:.1f} phút)")
    if rc != 0:
        FAILED.append(name)
    return rc == 0


def infer(tag: str, model: str, split: str, ctx: str) -> None:
    """ctx = gold | hybrid | bm25 | dense (top-5)."""
    if ctx == "gold":
        run_name, extra = f"{tag}_gold_{split}_rs", ["--context", "gold"]
    else:
        run_name, extra = f"{tag}_{ctx}_k5_{split}_rs", ["--context", "retrieved", "--mode", ctx, "--k", "5"]
    run(f"infer {run_name}", ["src/reader/infer.py", "--model", model, "--split", split, *extra,
                              "--refusal_scores", "--run", run_name], PRED / f"{run_name}.jsonl")


def train(out: str, base: dict, extra: list[str]) -> bool:
    return run(f"train {out}", ["src/reader/train_seq2seq.py", "--data", "r2", "--lr", str(base["lr"]),
                                "--epochs", str(base["epochs"]), "--output_dir", out, *extra],
               ROOT / out / "train_config.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wait_log", default="models/sweep_r2.log")
    args = ap.parse_args()

    marker = ROOT / args.wait_log
    def sweep_done() -> bool:   # log PowerShell có thể là UTF-16 LE không BOM hoặc UTF-8
        raw = marker.read_bytes()
        return any(m.encode(e) in raw for m in ["SWEEP_ALL_DONE"] for e in ("utf-16-le", "utf-8"))
    while marker.exists() and not sweep_done():
        log("chờ lượt dò tham số xong ...")
        time.sleep(300)

    # 1. chọn model chính
    scores = {}
    for c in CANDIDATES:
        p = ROOT / c / "train_config.json"
        if p.exists():
            info = json.loads(p.read_text(encoding="utf-8"))
            scores[c] = (info["best_dev_f1"], info["config"])
            log(f"ứng viên {c}: best dev F1 {info['best_dev_f1']:.2f}")
    main_model = max(scores, key=lambda c: scores[c][0])
    base = {"lr": scores[main_model][1]["lr"], "epochs": scores[main_model][1]["epochs"]}
    (ROOT / "models/gd5_main.json").write_text(json.dumps(
        {"main_model": main_model, **base, "candidates": {c: s[0] for c, s in scores.items()}},
        indent=2), encoding="utf-8")
    log(f"MODEL CHÍNH: {main_model} (lr {base['lr']}, {base['epochs']} epoch)")

    # 2. model chính trên dev
    for ctx in ["gold", "hybrid", "bm25", "dense"]:
        infer("r2m", main_model, "dev", ctx)

    # 3. E4, E5, seed
    variants = {"r2noimp": ("models/r2_noimp", ["--no_impossible"]),
                "r2ood": ("models/r2_ood", ["--ood", "10000"]),
                "r2s13": ("models/r2_s13", ["--seed", "13"]),
                "r2s7": ("models/r2_s7", ["--seed", "7"])}
    for tag, (out, extra) in variants.items():
        if train(out, base, extra):
            for ctx in ["gold", "hybrid"]:
                infer(tag, out, "dev", ctx)

    # 4. TEST — một lần
    for ctx in ["gold", "hybrid", "bm25", "dense"]:
        infer("r2m", main_model, "test", ctx)
    for tag, (out, _) in variants.items():
        if (ROOT / out / "train_config.json").exists():
            for ctx in ["gold", "hybrid"]:
                infer(tag, out, "test", ctx)

    log(f"GD5_PIPELINE_DONE; lỗi: {FAILED or 'không'}")


if __name__ == "__main__":
    main()
