"""Test cách tạo mẫu train cho Reader ViT5 (R1 / R2) trên dữ liệu giả."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "reader"))
from common import _from_cache  # noqa: E402
from infer import format_input  # noqa: E402
from metrics import NO_ANSWER  # noqa: E402
from train_seq2seq import build_examples  # noqa: E402

QA = pd.DataFrame([
    ("q1", "c1", "Chiến thắng Điện Biên Phủ năm nào?", "1954", False),
    ("q2", "c2", "Ai dời đô ra Thăng Long?", "Lý Công Uẩn", False),
    ("q3", "c3", "La Mã sụp đổ vì sao?", "", True),
], columns=["qa_id", "context_id", "question", "answer_text", "is_impossible"])
TEXT = {"c1": "Chiến thắng Điện Biên Phủ năm 1954.", "c2": "Lý Công Uẩn dời đô năm 1010.",
        "c3": "Đế quốc La Mã sụp đổ năm 476.", "c4": "Năm 1010, Lý Công Uẩn ban Chiếu dời đô.",
        "c5": "Hiệp định Genève ký năm 1954."}
RET = pd.DataFrame([  # q1: c5 (chứa "1954") đứng trên đoạn đúng; q2: c4 chứa đáp án
    ("q1", 1, "c5"), ("q1", 2, "c1"), ("q2", 1, "c2"), ("q2", 2, "c4"),
    ("q3", 1, "c1"), ("q3", 2, "c3"),
], columns=["qa_id", "rank", "context_id"])


def test_r1_gold_only():
    df = build_examples(QA, TEXT)
    assert list(df.kind) == ["gold"] * 3
    assert list(df.target) == ["1954", "Lý Công Uẩn", NO_ANSWER]
    assert df.source[0] == format_input(QA.question[0], TEXT["c1"])


def test_r2_negatives():
    r2 = {"neg_top_k": 2, "neg_per_question": 1, "neg_for_impossible": False}
    df = build_examples(QA, TEXT, RET, r2)
    neg = df[df.kind != "gold"].set_index("qa_id")
    assert len(df) == 5 and "q3" not in neg.index          # không thêm nhiễu cho câu không trả lời được
    assert neg.loc["q1", "context_id"] == "c5"              # bỏ đoạn đúng
    # đoạn nhiễu chứa nguyên văn đáp án -> giữ đáp án
    assert neg.loc["q1", "target"] == "1954" and neg.loc["q1", "kind"] == "neg_has_answer"
    assert neg.loc["q2", "target"] == "Lý Công Uẩn"


def test_r2_negative_without_answer():
    ret = pd.DataFrame([("q1", 1, "c3")], columns=["qa_id", "rank", "context_id"])
    df = build_examples(QA.iloc[:1], TEXT, ret, {"neg_top_k": 5, "neg_per_question": 1})
    neg = df[df.kind == "neg"]
    assert len(neg) == 1 and neg.target.iloc[0] == NO_ANSWER


def test_r2_impossible_negatives_optional():
    r2 = {"neg_top_k": 2, "neg_per_question": 1, "neg_for_impossible": True}
    df = build_examples(QA, TEXT, RET, r2)
    q3 = df[(df.qa_id == "q3") & (df.kind != "gold")]
    assert len(q3) == 1 and q3.target.iloc[0] == NO_ANSWER and q3.context_id.iloc[0] == "c1"


def test_cache_reader(tmp_path, monkeypatch):
    import common
    ret = RET.assign(score=1.0, retrieve_ms=5.0, split="dev")
    ret.to_parquet(tmp_path / "retrieved_hybrid.parquet")
    monkeypatch.setattr(common, "cache_path", lambda mode: tmp_path / f"retrieved_{mode}.parquet")
    ctxs, ms = _from_cache(QA, 2, "hybrid")
    assert ms == 5.0 and [c["context_id"] for c in ctxs[0]] == ["c5", "c1"]
    assert _from_cache(QA, 3, "hybrid") is None              # cache không đủ top-3
