"""
Phân loại câu hỏi theo từ để hỏi (luật đơn giản) — dùng cho E6.
Thứ tự luật quan trọng: luật cụ thể đứng trước ("năm nào" trước "nào").
"""
from __future__ import annotations

import re
import unicodedata

QTYPES = ("khi nào", "ai", "ở đâu", "bao nhiêu", "vì sao", "như thế nào", "cái gì", "khác")

_RULES = [
    ("khi nào", r"khi nào|bao giờ|lúc nào|năm nào|năm bao nhiêu|thế kỷ nào|thế kỉ nào|"
                r"thời gian nào|thời điểm nào|thời kỳ nào|giai đoạn nào|ngày nào|tháng nào|"
                r"triều đại nào|niên hiệu nào"),
    ("vì sao", r"vì sao|tại sao|vì lý do gì|lý do|nguyên nhân|vì đâu|do đâu|nhằm mục đích gì|mục đích"),
    ("ở đâu", r"ở đâu|tại đâu|nơi nào|đâu|địa điểm|vùng nào|vùng đất nào|nước nào|quốc gia nào|"
              r"thành phố nào|tỉnh nào|khu vực nào"),
    ("ai", r"\bai\b|người nào|những người nào|vị vua nào|vị tướng nào|nhân vật nào|"
           r"vua nào|tướng nào|của ai"),
    ("bao nhiêu", r"bao nhiêu|\bmấy\b|số lượng"),
    ("như thế nào", r"như thế nào|thế nào|ra sao|bằng cách nào|cách nào"),
    ("cái gì", r"\bgì\b|cái gì|điều gì|việc gì|\bnào\b"),
]
_COMPILED = [(name, re.compile(p)) for name, p in _RULES]


def question_type(question: str) -> str:
    q = unicodedata.normalize("NFC", question or "").lower()
    for name, rx in _COMPILED:
        if rx.search(q):
            return name
    return "khác"
