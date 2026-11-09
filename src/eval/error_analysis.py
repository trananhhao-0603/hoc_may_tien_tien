"""
Giai đoạn 6 — phân tích lỗi trên 100 câu trả lời sai.

  sample : lấy ngẫu nhiên N câu có EM = 0 từ một file dự đoán, gắn cờ tự động
           (đoạn đúng có trong top-k không, Reader dùng đoạn nào, đáp án có nằm nguyên văn
           trong đoạn không) và in ra file markdown để đọc tay.
  report : ghép nhãn chấm tay (reports/error_labels.csv) với cờ tự động -> bảng tổng hợp.

  python -m src.eval.error_analysis sample --run r2ood_hybrid_k5_test_rs
  python -m src.eval.error_analysis report --run r2ood_hybrid_k5_test_rs
"""
from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from pathlib import Path

import pandas as pd

from src.eval.metrics import is_no_answer, normalize_answer, score
from src.eval.predictions import PRED_DIR, read_predictions

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "reports" / "error_analysis"
LABELS = ROOT / "reports" / "error_labels.csv"

# Nhãn (PLAN §5, GĐ6) — mỗi câu đúng một nhãn chính
CATS = {
    "retrieval": "Tìm sai đoạn: đoạn đúng không có trong top-k",
    "selection": "Chọn nhầm đoạn: đoạn đúng có trong top-k nhưng đáp án lấy từ đoạn khác",
    "reader_span": "Đọc sai: có đoạn đúng nhưng trích sai/thiếu/thừa ý",
    "reader_refuse": "Đọc sai: từ chối nhầm dù đoạn đúng có đáp án",
    "trap": "Trả lời câu không có đáp án (bị câu bẫy đánh lừa)",
    "hallucination": "Bịa: đáp án không có trong đoạn đã đọc",
    "tokenizer": "Lỗi bộ từ vựng ViT5: ký tự ngoài từ vựng (ç, ā, …) bị rơi khi sinh",
    "gold_issue": "Đáp án chuẩn có vấn đề (sai, mơ hồ, câu hỏi lỗi)",
    "paraphrase": "Đúng nhưng khác cách viết / chấp nhận được",
}


def _window(text: str, needle: str, width: int = 260) -> str:
    """Đoạn trích quanh `needle` (nếu tìm thấy), đánh dấu bằng **...**."""
    if not text:
        return ""
    pos = text.lower().find(needle.lower()) if needle else -1
    if pos < 0:
        return text[: 2 * width] + ("…" if len(text) > 2 * width else "")
    a, b = max(0, pos - width), min(len(text), pos + len(needle) + width)
    return (("…" if a else "") + text[a:pos] + "**" + text[pos:pos + len(needle)] + "**"
            + text[pos + len(needle):b] + ("…" if b < len(text) else ""))


def flags(r: dict, corpus: dict[str, str]) -> dict:
    s = score(r["prediction"], r["gold_answers"], r["is_impossible"])
    ctx_ids = [c["context_id"] for c in r.get("contexts") or []]
    used = r.get("used_context_id")
    pred = r["prediction"]
    abst = is_no_answer(pred)
    pred_in = None
    if not abst:
        read = [used] if used else ctx_ids
        pn = normalize_answer(pred)
        pred_in = any(pn in normalize_answer(corpus.get(c, "")) for c in read)
    return {
        "qa_id": r["qa_id"], "em": s["em"], "f1": round(s["f1"], 3),
        "is_impossible": r["is_impossible"], "abstain": abst,
        "domain": "VN" if r["is_vietnam"] else "TG",
        "gold_rank": (ctx_ids.index(r["context_id"]) + 1) if r["context_id"] in ctx_ids else None,
        "used_is_gold": (used == r["context_id"]) if used else None,
        "pred_in_ctx": pred_in,
    }


def auto_label(f: dict) -> str:
    """Nhãn gợi ý từ cờ tự động; người chấm sửa lại sau khi đọc."""
    if f["is_impossible"]:
        return "trap" if f["pred_in_ctx"] else "hallucination"
    if f["gold_rank"] is None:
        return "retrieval"
    if f["abstain"]:
        return "reader_refuse"
    if f["pred_in_ctx"] is False:
        return "hallucination"
    if f["used_is_gold"] is False:
        return "selection"
    return "reader_span"


def cmd_sample(args):
    meta, rows = read_predictions(PRED_DIR / f"{args.run}.jsonl")
    corpus = pd.read_parquet(ROOT / "data/processed/corpus.parquet").set_index("context_id")["context"].to_dict()
    qa = pd.read_parquet(ROOT / "data/processed/qa_pairs.parquet").set_index("qa_id")
    wrong = [r for r in rows if score(r["prediction"], r["gold_answers"], r["is_impossible"])["em"] == 0]
    print(f"{args.run}: {len(wrong)}/{len(rows)} câu sai (EM = 0)")
    sample = random.Random(args.seed).sample(wrong, min(args.n, len(wrong)))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    recs, md = [], [f"# Mẫu {len(sample)} câu sai — `{args.run}` (seed {args.seed})\n",
                    f"Tổng số câu sai (EM = 0): {len(wrong)}/{len(rows)}.\n"]
    for i, r in enumerate(sample, 1):
        f = flags(r, corpus)
        f["auto_label"] = auto_label(f)
        f["idx"] = i
        recs.append(f)
        gold_ctx = corpus.get(r["context_id"], "")
        used = r.get("used_context_id")
        plaus = qa.loc[r["qa_id"], "plausible_answer"] if r["is_impossible"] else None
        gold = "; ".join(r["gold_answers"]) or "(không có câu trả lời)"
        md += [f"## {i}. `{r['qa_id']}` [{f['domain']}] — gợi ý: {f['auto_label']}\n",
               f"- **Câu hỏi:** {r['question']}",
               f"- **Đáp án chuẩn:** {gold}" + (f"  _(đáp án mồi: {plaus})_" if plaus else ""),
               f"- **Dự đoán:** {r['prediction']}  (F1 {f['f1']})",
               f"- Đoạn đúng ở hạng: {f['gold_rank']}; Reader dùng đoạn đúng: {f['used_is_gold']}; "
               f"dự đoán có trong đoạn: {f['pred_in_ctx']}",
               f"- Đoạn đúng: {_window(gold_ctx, r['gold_answers'][0] if r['gold_answers'] else (plaus or ''))}"]
        if used and used != r["context_id"]:
            md.append(f"- Đoạn Reader dùng (`{used}`): {_window(corpus.get(used, ''), r['prediction'])}")
        md.append("")
    (OUT_DIR / f"{args.run}_sample.md").write_text("\n".join(md), encoding="utf-8")
    pd.DataFrame(recs).to_csv(OUT_DIR / f"{args.run}_sample.csv", index=False, encoding="utf-8")
    print("Gợi ý nhãn:", Counter(r["auto_label"] for r in recs))
    print(f"-> {OUT_DIR / (args.run + '_sample.md')}")


def cmd_report(args):
    s = pd.read_csv(OUT_DIR / f"{args.run}_sample.csv")
    lab = pd.read_csv(LABELS)
    df = s.merge(lab, on="qa_id", how="left", validate="1:1")
    miss = df["label"].isna().sum()
    if miss:
        raise SystemExit(f"Thiếu nhãn cho {miss} câu")
    bad = set(df["label"]) - set(CATS)
    if bad:
        raise SystemExit(f"Nhãn lạ: {bad}")
    n = len(df)
    lines = [f"# Phân tích lỗi — `{args.run}`\n",
             f"Mẫu ngẫu nhiên {n} câu có EM = 0 (seed {args.seed}), chấm tay từng câu. "
             "Mỗi câu một nhãn chính.\n",
             "| Nhóm lỗi | Số câu | % | trong đó VN | TG |", "|---|---|---|---|---|"]
    for k, name in CATS.items():
        sub = df[df["label"] == k]
        lines.append(f"| {name} | {len(sub)} | {100 * len(sub) / n:.0f} | "
                     f"{(sub['domain'] == 'VN').sum()} | {(sub['domain'] == 'TG').sum()} |")
    agree = (df["label"] == df["auto_label"]).mean()
    lines += ["", f"Nhãn gợi ý tự động trùng nhãn chấm tay ở {100 * agree:.0f}% số câu.",
              "", "F1 trung bình theo nhóm (câu có EM = 0 vẫn có thể có F1 > 0):", "",
              "| Nhóm | F1 TB |", "|---|---|"]
    for k in CATS:
        sub = df[df["label"] == k]
        if len(sub):
            lines.append(f"| {k} | {100 * sub['f1'].mean():.1f} |")
    # Cờ tự động trên TẤT CẢ câu sai (không chỉ mẫu): chỉ tách được các nhóm có cờ rõ ràng
    _, rows = read_predictions(PRED_DIR / f"{args.run}.jsonl")
    corpus = pd.read_parquet(ROOT / "data/processed/corpus.parquet").set_index("context_id")["context"].to_dict()
    allf = [flags(r, corpus) for r in rows]
    wrong = [f for f in allf if f["em"] == 0]
    cnt = Counter(auto_label(f) for f in wrong)
    lines += ["", f"## Nhãn tự động trên toàn bộ {len(wrong)} câu sai của test", "",
              "Chỉ dựa vào cờ (không đọc tay), nên không tách được nhóm đáp án chuẩn có vấn đề hay khác "
              "cách viết. Các câu này nằm trong `reader_span`/`trap`.", "",
              "| Nhãn tự động | Số câu | % |", "|---|---|---|"]
    for k, v in cnt.most_common():
        lines.append(f"| {k} | {v} | {100 * v / len(wrong):.0f} |")
    # Ký tự ngoài từ vựng: đáp án chuẩn nào không đi qua tokenizer nguyên vẹn
    try:
        from transformers import AutoTokenizer
        tok = AutoTokenizer.from_pretrained(args.tokenizer)
        golds = [g for r in rows for g in r["gold_answers"]]
        bad = [g for g in golds if normalize_answer(tok.decode(tok(g).input_ids, skip_special_tokens=True))
               != normalize_answer(g)]
        lines += ["", f"Đáp án chuẩn của test không qua được tokenizer ViT5 nguyên vẹn (encode rồi decode "
                  f"bị mất ký tự): **{len(bad)}/{len(golds)}** ({100 * len(bad) / len(golds):.1f}%). "
                  f"Với những câu này, Reader không bao giờ đạt EM = 1. Ví dụ: "
                  + "; ".join(f"`{g}`" for g in bad[:5])]
    except Exception as e:                                   # tokenizer không có sẵn -> bỏ qua
        print("Bỏ qua kiểm tra tokenizer:", e)
    lines += ["", "## Ví dụ tiêu biểu", ""]
    for k in CATS:
        for _, r in df[(df["label"] == k) & df["note"].notna()].head(2).iterrows():
            lines.append(f"- **{k}** (`{r['qa_id']}`, #{r['idx']}): {r['note']}")
    out = ROOT / "reports" / "error_analysis.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"-> {out}")


def cmd_snap(args):
    """Hậu xử lý: dự đoán không khớp nguyên văn đoạn đã đọc (ViT5 làm rơi ký tự ngoài từ vựng)
    -> thay bằng chuỗi gốc trong đoạn (src/pipeline.highlight_span). In điểm trước/sau."""
    from src.eval.metrics import aggregate
    from src.pipeline import highlight_span
    corpus = pd.read_parquet(ROOT / "data/processed/corpus.parquet").set_index("context_id")["context"].to_dict()
    lines = ["| Run | Số câu đổi | EM trước → sau | F1 trước → sau |", "|---|---|---|---|"]
    for run in args.runs:
        _, rows = read_predictions(PRED_DIR / f"{run}.jsonl")
        before, after, changed = [], [], 0
        for r in rows:
            pred = r["prediction"]
            cid = r.get("used_context_id") or (r["context_id"] if r.get("context_source") == "gold" else None)
            new = pred
            if cid and not is_no_answer(pred) and pred.lower() not in corpus[cid].lower():
                sp = highlight_span(corpus[cid], pred)
                if sp:
                    new = corpus[cid][sp[0]:sp[1]]
                    changed += 1
            for lst, p in ((before, pred), (after, new)):
                lst.append({**score(p, r["gold_answers"], r["is_impossible"]),
                            "is_impossible": r["is_impossible"]})
        a, b = aggregate(before), aggregate(after)
        lines.append(f"| {run} | {changed} | {a['EM']:.2f} → {b['EM']:.2f} | {a['F1']:.2f} → {b['F1']:.2f} |")
    print("\n".join(lines))


def cmd_rankpen(args):
    """Thử trên DEV: chọn đáp án theo điểm Reader − λ·(hạng − 1) thay vì chỉ điểm Reader
    (sửa nhóm lỗi 'chọn nhầm đoạn'). Chỉ dùng file dự đoán có sẵn, không chạy lại mô hình.
    Cố ý KHÔNG chấm test (test chỉ dùng một lần, ở GĐ5)."""
    from src.eval.metrics import NO_ANSWER, aggregate
    run = args.run.replace("_test_", "_dev_")
    assert "_dev_" in run, "rankpen chỉ chạy trên dev"
    _, rows = read_predictions(PRED_DIR / f"{run}.jsonl")
    lines = [f"Run `{run}`", "", "| λ | EM | F1 | HasAns_F1 | NoAns_acc |", "|---|---|---|---|---|"]
    for lam in (0, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0):
        out = []
        for r in rows:
            rank = {c["context_id"]: c["rank"] for c in r["contexts"]}
            real = [p for p in r["extra"]["per_context"] if not is_no_answer(p["answer"])]
            pred = (max(real, key=lambda p: p["score"] - lam * (rank[p["context_id"]] - 1))["answer"]
                    if real else NO_ANSWER)
            out.append({**score(pred, r["gold_answers"], r["is_impossible"]),
                        "is_impossible": r["is_impossible"]})
        a = aggregate(out)
        lines.append(f"| {lam} | {a['EM']:.2f} | {a['F1']:.2f} | {a['HasAns_F1']:.2f} | {a['NoAns_acc']:.2f} |")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sample", "report", "snap", "rankpen"])
    ap.add_argument("--run", default="r2ood_hybrid_k5_test_rs")
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--runs", nargs="+", default=[
        "r2ood_gold_dev_rs", "r2ood_hybrid_k5_dev_rs", "r2ood_gold_test_rs", "r2ood_hybrid_k5_test_rs",
        "r2m_gold_test_rs", "r2m_hybrid_k5_test_rs"])
    ap.add_argument("--tokenizer", default=str(ROOT / "models/r2_ood"))
    args = ap.parse_args()
    {"sample": cmd_sample, "report": cmd_report, "snap": cmd_snap, "rankpen": cmd_rankpen}[args.cmd](args)


if __name__ == "__main__":
    main()
