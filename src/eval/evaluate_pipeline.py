"""
Chấm một hoặc nhiều file dự đoán (data/predictions/{run}.jsonl) và in bảng chỉ số.

Chạy:
    python src/eval/evaluate_pipeline.py data/predictions/b0_retrieved_dev.jsonl
    python src/eval/evaluate_pipeline.py data/predictions/*_dev.jsonl --out reports/baselines_dev

Với mỗi file:
  - Tổng: EM, F1, HasAns-EM/F1, NoAns-acc, tỉ lệ từ chối sai (squad_v2, thang 0–100)
  - Tách theo miền (VN / TG) và theo loại câu hỏi (qtype.py)
  - Nếu có `contexts`: tỉ lệ đoạn đúng nằm trong các đoạn đã đọc, và HasAns-F1 tách
    theo "tìm đúng / tìm sai" (để tách sai số tìm và sai số đọc — E3)
  - Tỉ lệ dự đoán xuất hiện nguyên văn trong đoạn đã đọc (chỉ báo "bịa" của mô hình sinh)
Nhiều file -> thêm bảng so sánh.
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from metrics import aggregate, is_no_answer, normalize_answer, score  # noqa: E402
from predictions import ROOT, read_predictions  # noqa: E402
from qtype import QTYPES, question_type  # noqa: E402

COLS = ["n", "EM", "F1", "HasAns_EM", "HasAns_F1", "NoAns_acc", "HasAns_abstain"]


def _fill_gold(rows: list[dict], qa: pd.DataFrame) -> None:
    by_id = qa.set_index("qa_id")
    missing = [r["qa_id"] for r in rows if r["qa_id"] not in by_id.index]
    if missing:
        raise KeyError(f"{len(missing)} qa_id không có trong qa_pairs, ví dụ {missing[:3]}")
    for r in rows:
        q = by_id.loc[r["qa_id"]]
        imp = bool(q.is_impossible)
        r.setdefault("question", q.question)
        r.setdefault("is_impossible", imp)
        r.setdefault("gold_answers", [] if imp else [q.answer_text])
        r.setdefault("is_vietnam", bool(q.is_vietnam))
        r.setdefault("split", q.split)
        r.setdefault("context_id", q.context_id)


def score_rows(rows: list[dict], corpus_text: dict[str, str]) -> pd.DataFrame:
    out = []
    for r in rows:
        s = score(r.get("prediction"), r["gold_answers"], r["is_impossible"])
        ctx_ids = [c["context_id"] for c in r.get("contexts") or []]
        rec = {
            "qa_id": r["qa_id"], **s, "is_impossible": r["is_impossible"],
            "domain": "VN" if r["is_vietnam"] else "TG",
            "qtype": question_type(r["question"]),
            "gold_in_ctx": (r["context_id"] in ctx_ids) if ctx_ids else None,
            "pred_in_ctx": None,
        }
        # dự đoán có nằm nguyên văn trong (các) đoạn đã đọc không
        read_ids = [r["used_context_id"]] if r.get("used_context_id") else ctx_ids
        if not read_ids and r.get("context_source") == "gold":
            read_ids = [r["context_id"]]
        if read_ids and not is_no_answer(r.get("prediction")):
            pred = normalize_answer(r["prediction"])
            rec["pred_in_ctx"] = any(pred in normalize_answer(corpus_text.get(c, ""))
                                     for c in read_ids)
        out.append(rec)
    return pd.DataFrame(out)


def _agg(df: pd.DataFrame) -> dict:
    return aggregate(df.to_dict("records")) if len(df) else {c: float("nan") for c in COLS}


def evaluate(df: pd.DataFrame) -> dict:
    res = {"overall": _agg(df),
           "by_domain": {d: _agg(df[df.domain == d]) for d in ("VN", "TG")},
           "by_qtype": {t: _agg(df[df.qtype == t]) for t in QTYPES if (df.qtype == t).any()}}
    has = df[~df.is_impossible]
    if has.gold_in_ctx.notna().any():
        hit = has.gold_in_ctx.astype(bool)
        res["retrieval"] = {
            "gold_in_ctx": 100.0 * hit.mean(),
            "HasAns_F1_hit": 100.0 * has[hit].f1.mean() if hit.any() else float("nan"),
            "HasAns_F1_miss": 100.0 * has[~hit].f1.mean() if (~hit).any() else float("nan"),
        }
    answered = df[df.pred_in_ctx.notna()]
    if len(answered):
        res["pred_in_ctx"] = 100.0 * answered.pred_in_ctx.astype(bool).mean()
    return res


def _fmt(v) -> str:
    if isinstance(v, (int,)) and not isinstance(v, bool):
        return str(v)
    return "—" if v is None or (isinstance(v, float) and math.isnan(v)) else f"{v:.1f}"


def _table(rows: dict[str, dict], first: str) -> str:
    lines = [f"| {first} | " + " | ".join(COLS) + " |", "|---" * (len(COLS) + 1) + "|"]
    for name, m in rows.items():
        lines.append(f"| {name} | " + " | ".join(_fmt(m.get(c)) for c in COLS) + " |")
    return "\n".join(lines)


def report(run: str, meta: dict, res: dict) -> str:
    md = [f"## {run}", ""]
    if meta:
        md += ["`" + json.dumps(meta, ensure_ascii=False) + "`", ""]
    md += [_table({"Tổng": res["overall"], **res["by_domain"]}, "Tập"), "",
           "**Theo loại câu hỏi**", "", _table(res["by_qtype"], "Loại"), ""]
    if "retrieval" in res:
        r = res["retrieval"]
        md += [f"- Đoạn đúng nằm trong các đoạn đã đọc: **{r['gold_in_ctx']:.1f}%** (câu trả lời được)",
               f"- HasAns-F1 khi tìm đúng: {_fmt(r['HasAns_F1_hit'])} · khi tìm sai: {_fmt(r['HasAns_F1_miss'])}"]
    if "pred_in_ctx" in res:
        md += [f"- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: {res['pred_in_ctx']:.1f}%"]
    return "\n".join(md) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--qa", default=str(ROOT / "data/processed/qa_pairs.parquet"))
    ap.add_argument("--corpus", default=str(ROOT / "data/processed/corpus.parquet"))
    ap.add_argument("--out", default=None, help="tiền tố file báo cáo: <out>.md và <out>.json")
    args = ap.parse_args()

    files = sorted({p for f in args.files for p in (glob.glob(f) or [f])})
    qa = pd.read_parquet(args.qa)
    corpus = pd.read_parquet(args.corpus, columns=["context_id", "context"])
    corpus_text = dict(zip(corpus.context_id, corpus.context))

    all_res, md = {}, []
    for f in files:
        run = Path(f).stem
        meta, rows = read_predictions(f)
        _fill_gold(rows, qa)
        if any(r.get("split") == "test" for r in rows):
            print(f"⚠️  {run}: có câu thuộc TEST — chỉ chấm test một lần cho cấu hình cuối.")
        res = evaluate(score_rows(rows, corpus_text))
        all_res[run] = {"meta": meta, **res}
        md.append(report(run, meta, res))

    if len(files) > 1:
        cmp_rows = {}
        for run, r in all_res.items():
            cmp_rows[run] = {**r["overall"]}
        md.insert(0, "## So sánh\n\n" + _table(cmp_rows, "Run") + "\n")

    text = "\n".join(md)
    print(text)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.with_suffix(".md").write_text("# Kết quả đánh giá\n\n" + text, encoding="utf-8")
        out.with_suffix(".json").write_text(json.dumps(all_res, ensure_ascii=False, indent=2),
                                            encoding="utf-8")
        print(f"-> {out.with_suffix('.md')}, {out.with_suffix('.json')}")


if __name__ == "__main__":
    main()
