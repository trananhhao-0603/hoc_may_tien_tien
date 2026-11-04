"""Test metric EM/F1 tiếng Việt (src/eval/metrics.py)."""
import sys
import unicodedata
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "eval"))
from metrics import (NO_ANSWER, aggregate, exact_match, f1_score,  # noqa: E402
                     is_no_answer, normalize_answer, score)


def test_normalize_basic():
    assert normalize_answer("  Điện Biên Phủ,  năm 1954! ") == "điện biên phủ năm 1954"
    assert normalize_answer("“Bình Ngô đại cáo”") == "bình ngô đại cáo"
    assert normalize_answer(None) == ""


def test_keeps_tone_marks():
    assert normalize_answer("Hà Nội") != normalize_answer("Ha Noi")
    assert exact_match("Hà Nội", "Ha Noi") == 0.0


def test_nfc_vs_nfd():
    nfd = unicodedata.normalize("NFD", "Nguyễn Trãi")
    assert exact_match(nfd, "Nguyễn Trãi") == 1.0


def test_tone_position_old_vs_new():
    assert exact_match("hòa ước", "hoà ước") == 1.0
    assert exact_match("Thủy quân", "thuỷ quân") == 1.0
    assert exact_match("khỏe", "khoẻ") == 1.0
    # không đụng chữ có mũ/móc hay khi sau nguyên âm còn phụ âm
    assert normalize_answer("hoàng hậu") == "hoàng hậu"
    assert normalize_answer("người") == "người"
    assert exact_match("hòa", "hóa") == 0.0


def test_case_insensitive():
    assert exact_match("LÊ LỢI", "lê lợi") == 1.0


def test_year_partial():
    # "năm 1954" so với "1954": EM 0, F1 = 2·(1/2·1)/(1/2+1) = 2/3
    assert exact_match("năm 1954", "1954") == 0.0
    assert f1_score("năm 1954", "1954") == pytest.approx(2 / 3)
    assert f1_score("1954", "năm 1954") == pytest.approx(2 / 3)


def test_f1_no_overlap_and_repeats():
    assert f1_score("Lý Thái Tổ", "Trần Hưng Đạo") == 0.0
    # Counter giao nhau: "năm năm 1010" vs "năm 1010" -> common=2, P=2/3, R=1
    assert f1_score("năm năm 1010", "năm 1010") == pytest.approx(0.8)


def test_empty_answers():
    assert f1_score("", "") == 1.0
    assert f1_score("", "1954") == 0.0
    assert f1_score("1954", "") == 0.0
    assert f1_score("...", "1954") == 0.0     # chỉ có dấu câu = rỗng


def test_no_answer_label():
    assert is_no_answer(NO_ANSWER)
    assert is_no_answer("Không có câu trả lời.")
    assert is_no_answer("")
    assert not is_no_answer("không")
    # rác chỉ có ký hiệu không phải là từ chối (ViT5 zero-shot sinh "*>+>")
    assert not is_no_answer("*>+>")
    assert score("*>+>", [""], is_impossible=True)["em"] == 0.0


def test_score_squad_v2():
    # câu không trả lời được
    assert score(NO_ANSWER, [""], is_impossible=True)["em"] == 1.0
    assert score("", [], is_impossible=True)["f1"] == 1.0
    assert score("năm 1954", [""], is_impossible=True)["f1"] == 0.0
    # câu trả lời được mà từ chối
    s = score(NO_ANSWER, ["1954"])
    assert s == {"em": 0.0, "f1": 0.0, "abstain": True}
    # nhiều đáp án chuẩn -> lấy max
    s = score("năm 1954", ["1954", "năm 1954"])
    assert s["em"] == 1.0 and s["f1"] == 1.0
    with pytest.raises(ValueError):
        score("x", [""])


def test_aggregate():
    rows = [
        {**score("1954", ["1954"]), "is_impossible": False},          # 1, 1
        {**score("năm 1954", ["1954"]), "is_impossible": False},      # 0, 2/3
        {**score(NO_ANSWER, [""], True), "is_impossible": True},      # 1, 1
        {**score("Huế", [""], True), "is_impossible": True},          # 0, 0
    ]
    m = aggregate(rows)
    assert (m["n"], m["n_has"], m["n_no"]) == (4, 2, 2)
    assert m["EM"] == pytest.approx(50.0)
    assert m["HasAns_EM"] == pytest.approx(50.0)
    assert m["HasAns_F1"] == pytest.approx(100 * (1 + 2 / 3) / 2)
    assert m["NoAns_acc"] == pytest.approx(50.0)
    assert m["F1"] == pytest.approx(100 * (1 + 2 / 3 + 1 + 0) / 4)
    assert m["HasAns_abstain"] == 0.0
