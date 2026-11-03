"""
Thống kê dữ liệu QA + độ dài theo tokenizer ViT5 -> reports/data_stats.md.
Dùng để chọn max_length cho Reader (Giai đoạn 1 trong PLAN.md).

Chạy:
    python src/data/length_stats.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

PCTS = [50, 90, 95, 99, 100]
TAG_OVERHEAD = 12   # token cho thẻ "<q> </q> <ctx> </ctx>" + </s>


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--processed", default="data/processed")
    ap.add_argument("--tokenizer", default="VietAI/vit5-base")
    ap.add_argument("--out", default="reports/data_stats.md")
    args = ap.parse_args()

    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(args.tokenizer)

    p = Path(args.processed)
    cx = pd.read_parquet(p / "corpus.parquet")
    qa = pd.read_parquet(p / "qa_pairs.parquet")

    def n_tok(texts):
        return np.array([len(tok(t, add_special_tokens=False).input_ids) for t in texts])

    lc = n_tok(cx.context)
    lq = n_tok(qa.question)
    la = n_tok(qa.loc[~qa.is_impossible, "answer_text"])
    ctx_len = dict(zip(cx.context_id, lc))
    l_in = lq + np.array([ctx_len[c] for c in qa.context_id]) + TAG_OVERHEAD

    L = [f"# Thống kê dữ liệu QA (tokenizer `{args.tokenizer}`)", "",
         "## Số câu hỏi theo split", "",
         "| Split | Số bài | Số đoạn | Trả lời được | Không trả lời được | Tổng | VN / TG (câu hỏi) |",
         "|---|---|---|---|---|---|---|"]
    for sp in ["train", "dev", "test"]:
        q = qa[qa.split == sp]
        c = cx[cx.split == sp]
        L.append(f"| {sp} | {c.title.nunique()} | {len(c):,} | {(~q.is_impossible).sum():,} | "
                 f"{q.is_impossible.sum():,} | {len(q):,} | "
                 f"{q.is_vietnam.sum():,} / {(~q.is_vietnam).sum():,} |")
    no_q = sorted(set(cx.title) - set(qa.title))
    if no_q:
        L += ["", "Bài **không có câu hỏi có nhãn** (chỉ có trong split test không nhãn của "
              "ViQuAD; đoạn văn vẫn nằm trong kho tri thức): "
              + ", ".join(f"{t} ({cx[cx.title == t].split.iloc[0]})" for t in no_q)]

    L += ["", "## Độ dài (token)", "",
          "| Thành phần | p50 | p90 | p95 | p99 | max | TB |", "|---|---|---|---|---|---|---|"]
    for name, a in [("Đoạn văn", lc), ("Câu hỏi", lq), ("Đáp án", la),
                    ("Input Reader, 1 đoạn", l_in)]:
        L.append(f"| {name} | " + " | ".join(str(int(np.percentile(a, x))) for x in PCTS)
                 + f" | {a.mean():.0f} |")

    L += ["", "## Tỉ lệ bị cắt cụt", "", "| Ngưỡng | Input 1 đoạn bị cắt | Ngưỡng | Đáp án bị cắt |",
          "|---|---|---|---|"]
    for m_in, m_out in zip([256, 384, 512, 1024], [16, 32, 64, 128]):
        L.append(f"| {m_in} | {100 * (l_in > m_in).mean():.1f}% | {m_out} | "
                 f"{100 * (la > m_out).mean():.2f}% |")

    L += ["", "## Ghép k đoạn vào một input (ước lượng)", "", "| k | p50 | p90 |", "|---|---|---|"]
    for k in [1, 3, 5]:
        L.append(f"| {k} | {int(np.median(lq) + k * np.median(lc) + TAG_OVERHEAD)} | "
                 f"{int(np.percentile(lq, 90) + k * np.percentile(lc, 90) + TAG_OVERHEAD)} |")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
    print(f"\nĐã lưu -> {out}")


if __name__ == "__main__":
    main()
