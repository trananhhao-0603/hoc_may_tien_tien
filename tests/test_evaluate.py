"""Test evaluate_pipeline (chấm file dự đoán) và phân loại câu hỏi, trên dữ liệu giả."""
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "eval"))
from evaluate_pipeline import _fill_gold, evaluate, score_rows  # noqa: E402
from metrics import NO_ANSWER  # noqa: E402
from predictions import read_predictions, write_predictions  # noqa: E402
from qtype import question_type  # noqa: E402

QA = pd.DataFrame([
    ("q1", "c1", "Chiến thắng Điện Biên Phủ năm nào?", "1954", False, True, "dev"),
    ("q2", "c2", "Ai dời đô ra Thăng Long?", "Lý Công Uẩn", False, True, "dev"),
    ("q3", "c3", "La Mã sụp đổ vì sao?", "", True, False, "dev"),
], columns=["qa_id", "context_id", "question", "answer_text", "is_impossible", "is_vietnam", "split"])
TEXT = {"c1": "Chiến thắng Điện Biên Phủ năm 1954.", "c2": "Lý Công Uẩn dời đô năm 1010.",
        "c3": "Đế quốc La Mã sụp đổ năm 476."}


def test_qtype():
    assert question_type("Chiến thắng Điện Biên Phủ diễn ra năm nào?") == "khi nào"
    assert question_type("Ai là người dời đô?") == "ai"
    assert question_type("Vì sao nhà Hồ thất bại?") == "vì sao"
    assert question_type("Kinh đô đặt ở đâu?") == "ở đâu"
    assert question_type("Có bao nhiêu quân?") == "bao nhiêu"
    assert question_type("Hiệp định có nội dung gì?") == "cái gì"


def test_roundtrip_and_evaluate(tmp_path):
    rows = [
        {"qa_id": "q1", "prediction": "năm 1954",
         "contexts": [{"context_id": "c1", "rank": 1, "score": 1.0}]},
        {"qa_id": "q2", "prediction": "Nguyễn Huệ",                  # tìm sai đoạn, đáp án bịa
         "contexts": [{"context_id": "c1", "rank": 1, "score": 1.0}]},
        {"qa_id": "q3", "prediction": NO_ANSWER,
         "contexts": [{"context_id": "c3", "rank": 1, "score": 1.0}]},
    ]
    p = write_predictions(tmp_path / "run.jsonl", rows, meta={"run": "t"})
    meta, back = read_predictions(p)
    assert meta["run"] == "t" and len(back) == 3
    _fill_gold(back, QA)
    res = evaluate(score_rows(back, TEXT))
    o = res["overall"]
    assert (o["n_has"], o["n_no"]) == (2, 1)
    assert o["HasAns_EM"] == 0.0
    assert o["HasAns_F1"] == pytest.approx(100 * (2 / 3) / 2)
    assert o["NoAns_acc"] == 100.0
    assert res["retrieval"]["gold_in_ctx"] == 50.0
    assert res["pred_in_ctx"] == 50.0                              # "năm 1954" có, "Nguyễn Huệ" không
    assert res["by_domain"]["TG"]["n"] == 1
    json.dumps(res)                                                # ghi được ra json


def test_unknown_qa_id():
    with pytest.raises(KeyError):
        _fill_gold([{"qa_id": "zzz", "prediction": ""}], QA)
