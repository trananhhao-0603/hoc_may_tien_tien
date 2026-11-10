"""
Demo Gradio — Hỏi đáp Lịch sử tiếng Việt (Giai đoạn 6).

    python app.py                       # model mặc định models/r2_ood, http://127.0.0.1:7860
    python app.py --model models/r2_lr1e-4_e8 --device cpu --share

Nhập câu hỏi -> đáp án + đoạn văn bằng chứng (tô đậm đáp án) + top-k nguồn kèm đáp án
Reader đọc được ở từng đoạn + thời gian từng khâu.
"""
from __future__ import annotations

import argparse
import html
import os

import pandas as pd

from src.pipeline import DEFAULT_MODEL, ROOT, QAPipeline

# Câu hỏi mẫu lấy từ tập dev (không dùng test cho demo)
def _examples(n: int = 6) -> list[str]:
    qa = pd.read_parquet(ROOT / "data/processed/qa_pairs.parquet",
                         columns=["question", "title", "split", "is_impossible"])
    # mỗi bài dev một câu; bỏ bài Phong Nha - Kẻ Bàng (nội dung chủ yếu là địa lý)
    dev = qa[(qa.split == "dev") & ~qa.is_impossible & ~qa.title.str.startswith("Vườn quốc gia")]
    picks = dev.groupby("title").sample(1, random_state=1).question.tolist()[:n]
    return picks + [
        "Chiến dịch Điện Biên Phủ kết thúc vào năm nào?",
        "Ai là người sáng lập ra Microsoft?",          # ngoài phạm vi kho -> mong đợi từ chối
    ]


CSS = """
.evidence {line-height:1.6; padding:12px; border-radius:8px; background:var(--block-background-fill);}
.evidence mark {background:#fde68a; color:#111; padding:0 2px; border-radius:3px; font-weight:600;}
.answer {font-size:1.3em; font-weight:600;}
"""


def _evidence_html(passage: str, span: tuple[int, int] | None, title: str) -> str:
    if span:
        a, b = span
        body = (html.escape(passage[:a]) + "<mark>" + html.escape(passage[a:b]) + "</mark>"
                + html.escape(passage[b:]))
    else:
        body = html.escape(passage)
    return f"<div class='evidence'><b>{html.escape(title)}</b><br>{body}</div>"


def build(pipe: QAPipeline):
    import gradio as gr

    def run(question: str, k: int):
        question = (question or "").strip()
        if not question:
            return "Hãy nhập câu hỏi.", "", None, ""
        out = pipe.answer(question, k=int(k))
        if out["refused"]:
            ans_md = "<div class='answer'>Không có câu trả lời</div>" \
                     "Không đoạn nào trong top-k chứa đáp án (theo Reader)."
            ev = ""
        else:
            e = out["evidence"]
            ans_md = (f"<div class='answer'>{html.escape(out['answer_text'])}</div>"
                      f"Nguồn: đoạn hạng {e['rank']} — <i>{html.escape(e['title'])}</i> "
                      f"(log-prob TB mỗi token {out['score']:.3f})")
            ev = _evidence_html(e["context"], out["span"], e["title"])
        table = pd.DataFrame([{
            "Hạng": c["rank"], "Bài": c["title"], "Điểm RRF": round(c["score"], 4),
            "Đáp án đọc được": c["answer"], "Điểm Reader": round(c["answer_score"], 3),
            "Trích đoạn": c["context"][:160] + ("…" if len(c["context"]) > 160 else ""),
        } for c in out["contexts"]])
        ms = out["latency_ms"]
        lat = (f"Truy hồi {ms['retrieve']:.0f} ms (BM25 {ms['bm25']:.0f} · dense {ms['dense']:.0f} · "
               f"RRF {ms['fuse']:.1f}) · Reader {ms['read']:.0f} ms ({len(out['contexts'])} đoạn, "
               f"{pipe.reader.device}) · **Tổng {ms['total']:.0f} ms**")
        return ans_md, ev, table, lat

    with gr.Blocks(title="Hỏi đáp Lịch sử tiếng Việt") as demo:
        gr.Markdown("# Hỏi đáp Lịch sử tiếng Việt\n"
                    "Retriever hybrid (BM25 + bi-encoder, RRF) tìm top-k đoạn trong kho 1.862 đoạn "
                    "Wikipedia lịch sử → Reader ViT5 (fine-tune trên ViQuAD lịch sử) sinh đáp án "
                    "hoặc trả lời *không có câu trả lời*.")
        with gr.Row():
            q = gr.Textbox(label="Câu hỏi", placeholder="Ví dụ: Ai là vị vua đầu tiên của nhà Trần?",
                           scale=5, lines=2)
            k = gr.Slider(1, 10, value=5, step=1, label="Số đoạn top-k", scale=1)
        btn = gr.Button("Trả lời", variant="primary")
        ans = gr.HTML(label="Đáp án")
        ev = gr.HTML(label="Đoạn văn bằng chứng")
        lat = gr.Markdown()
        tab = gr.Dataframe(label="Top-k nguồn", wrap=True)
        gr.Examples(_examples(), inputs=q)
        btn.click(run, [q, k], [ans, ev, tab, lat])
        q.submit(run, [q, k], [ans, ev, tab, lat])
    return demo


def main():
    ap = argparse.ArgumentParser()
    # QA_MODEL: thư mục checkpoint hoặc tên repo trên HF Hub (Space đặt biến này)
    ap.add_argument("--model", default=os.environ.get("QA_MODEL", str(DEFAULT_MODEL)))
    ap.add_argument("--device", default=None, help="cuda | cpu (mặc định: tự chọn)")
    ap.add_argument("--port", type=int, default=7860)
    ap.add_argument("--share", action="store_true")
    args = ap.parse_args()
    pipe = QAPipeline.load(args.model, device=args.device)
    build(pipe).launch(server_port=args.port, share=args.share, css=CSS)


if __name__ == "__main__":
    main()
