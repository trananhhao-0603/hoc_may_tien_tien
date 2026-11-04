"""
Định dạng file dự đoán dùng chung: data/predictions/{run}.jsonl, mỗi dòng một câu hỏi.

Bắt buộc:
  qa_id        : khớp qa_pairs.parquet
  prediction   : chuỗi đáp án ("không có câu trả lời" hoặc "" = từ chối)
Nên có (evaluate_pipeline tự bổ sung từ qa_pairs nếu thiếu):
  question, gold_answers (list), is_impossible, is_vietnam, split, context_id (đoạn đúng)
Tuỳ chọn:
  context_source : "gold" | "retrieved"
  contexts       : [{"context_id", "rank", "score"}] — các đoạn Reader đã đọc, theo thứ tự
  used_context_id: đoạn chứa đáp án được chọn (khi đọc từng đoạn rồi chọn)
  latency_ms     : {"retrieve": .., "read": ..}
  extra          : dict tuỳ ý (điểm của Reader, ...)

Dòng đầu tiên có thể là header {"_meta": {...}} (cấu hình, commit, thời gian chạy).
"""
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
PRED_DIR = ROOT / "data" / "predictions"


def git_commit() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                             capture_output=True, text=True, timeout=10)
        dirty = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                               capture_output=True, text=True, timeout=10).stdout.strip()
        return out.stdout.strip() + ("-dirty" if dirty else "")
    except Exception:
        return "unknown"


def write_predictions(path, rows: Iterable[dict], meta: dict | None = None) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = {"commit": git_commit(), "time": time.strftime("%Y-%m-%d %H:%M:%S"), **(meta or {})}
    n = 0
    with path.open("w", encoding="utf-8") as f:
        f.write(json.dumps({"_meta": meta}, ensure_ascii=False) + "\n")
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += 1
    print(f"Đã ghi {n} dự đoán -> {path}")
    return path


def read_predictions(path) -> tuple[dict, list[dict]]:
    meta, rows = {}, []
    with Path(path).open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            if "_meta" in obj:
                meta = obj["_meta"]
            else:
                rows.append(obj)
    return meta, rows


def gold_fields(qa_row) -> dict:
    """Trường đáp án chuẩn từ một dòng qa_pairs (dùng khi ghi dự đoán)."""
    imp = bool(qa_row.is_impossible)
    return {
        "qa_id": qa_row.qa_id, "question": qa_row.question,
        "gold_answers": [] if imp else [qa_row.answer_text],
        "is_impossible": imp, "is_vietnam": bool(qa_row.is_vietnam),
        "split": qa_row.split, "context_id": qa_row.context_id,
    }
