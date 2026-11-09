"""Test highlight_span (src/pipeline.py): tìm đáp án trong đoạn, kể cả khi ViT5 làm rơi ký tự."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.pipeline import highlight_span  # noqa: E402


def _get(p, a):
    sp = highlight_span(p, a)
    return p[sp[0]:sp[1]] if sp else None


def test_exact_case_insensitive():
    p = "Năm 1400, Hồ Quý Ly chiếm ngôi nhà Trần."
    assert _get(p, "năm 1400") == "Năm 1400"
    assert _get(p, "Hồ Quý Ly") == "Hồ Quý Ly"


def test_dropped_oov_chars():
    p = "Mary là vợ của Vua nước Pháp, François II. Năm 1559, Mary tuyên bố."
    assert _get(p, "Franois II") == "François II"
    p2 = "ông được gọi một cách tôn kính là Mahātmā, nghĩa là Linh hồn lớn"
    assert _get(p2, "Mahtm") == "Mahātmā"
    p3 = "cử Trần Khắc Chung (陳克終) cướp công chúa về"
    assert _get(p3, "cử Trần Khắc Chung () cướp công chúa về") == p3


def test_vietnamese_diacritics_not_dropped():
    # chữ tiếng Việt có dấu không bị bỏ khi khớp gần đúng -> không khớp nhầm
    assert highlight_span("Trần Thái Tông lên ngôi", "Trn Thái Tông") is None


def test_refusal_and_missing():
    p = "Năm 1400, Hồ Quý Ly chiếm ngôi nhà Trần."
    assert highlight_span(p, "không có câu trả lời") is None
    assert highlight_span(p, "") is None
    assert highlight_span(p, "nhà Lý") is None
