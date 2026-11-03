"""Kiểm tra dữ liệu THẬT trong data/processed (cần pandas + pyarrow).

Chạy: python tests/test_split_leak.py   (hoặc pytest tests/)
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
SPLITS = {"train", "dev", "test"}


def _load():
    return (pd.read_parquet(PROC / "corpus.parquet"),
            pd.read_parquet(PROC / "qa_pairs.parquet"))


def test_khong_ro_ri_split():
    cx, qa = _load()
    assert set(cx.split) == SPLITS and set(qa.split) == SPLITS
    # mỗi bài / đoạn / câu hỏi chỉ thuộc đúng 1 split
    assert (cx.groupby("title").split.nunique() == 1).all(), "bài nằm ở nhiều split"
    assert cx.context_id.is_unique, "context_id trùng"
    assert qa.qa_id.is_unique, "qa_id trùng"
    # split của câu hỏi phải trùng split của đoạn văn chứa nó
    m = qa.merge(cx[["context_id", "split"]], on="context_id",
                 suffixes=("", "_ctx"), how="left", validate="many_to_one")
    assert m.split_ctx.notna().all(), "câu hỏi trỏ tới đoạn không có trong corpus"
    assert (m.split == m.split_ctx).all(), "split câu hỏi ≠ split đoạn văn"
    # không bài nào xuất hiện ở hai split khác nhau qua bảng câu hỏi
    assert (qa.groupby("title").split.nunique() == 1).all()


def test_nhan_qa_hop_le():
    cx, qa = _load()
    ctx = dict(zip(cx.context_id, cx.context))
    ans = qa[~qa.is_impossible]
    imp = qa[qa.is_impossible]
    # câu trả lời được: có đáp án; nếu span_ok thì đáp án nằm ĐÚNG vị trí answer_start
    assert (ans.answer_text.str.len() > 0).all(), "answerable mà đáp án rỗng"
    assert ans.answer_span_ok.mean() > 0.99, "quá nhiều span không hợp lệ"
    for r in ans[ans.answer_span_ok].itertuples():
        s = int(r.answer_start)
        assert ctx[r.context_id][s:s + len(r.answer_text)] == r.answer_text, r.qa_id
    # câu không trả lời được: không có đáp án, có plausible_answer
    assert (imp.answer_text == "").all()
    assert (imp.plausible_answer.str.len() > 0).all()
    # không còn câu nào từ split test chính thức (không có nhãn) của ViQuAD
    assert set(qa.viquad_split) <= {"train", "validation"}


if __name__ == "__main__":
    test_khong_ro_ri_split()
    test_nhan_qa_hop_le()
    print("✅ TẤT CẢ TEST PASS — dữ liệu thật: không rò rỉ, nhãn QA hợp lệ.")
