"""Tiền xử lý văn bản dùng chung cho Retriever (BM25 + dense).

Hai cách tách token:
  - "syl": âm tiết — tách theo ký tự chữ/số (\\w+), bỏ dấu câu.
           "Điện Biên Phủ, 1954" -> ["điện", "biên", "phủ", "1954"]
  - "seg": từ — tách từ tiếng Việt bằng underthesea, nối âm tiết bằng "_".
           "Điện Biên Phủ, 1954" -> ["điện_biên_phủ", "1954"]

Mô hình dense `bkai-foundation-models/vietnamese-bi-encoder` (PhoBERT) BẮT BUỘC
input đã tách từ -> dùng segment().
"""
from __future__ import annotations

import re
import unicodedata
from functools import lru_cache

_WORD_RE = re.compile(r"\w+", re.UNICODE)


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text or "")


@lru_cache(maxsize=200_000)
def segment(text: str) -> str:
    """Tách từ tiếng Việt: 'Điện Biên Phủ diễn ra' -> 'Điện_Biên_Phủ diễn ra'."""
    from underthesea import word_tokenize
    return word_tokenize(nfc(text), format="text")


def tokens(text: str, mode: str = "seg") -> list[str]:
    """Token cho BM25 (chữ thường, bỏ dấu câu). mode: 'syl' | 'seg'."""
    if mode == "seg":
        text = segment(text)
    elif mode != "syl":
        raise ValueError(f"mode phải là 'syl' hoặc 'seg', nhận {mode!r}")
    # \w khớp cả "_" nên từ ghép "điện_biên_phủ" được giữ nguyên một token
    return _WORD_RE.findall(nfc(text).lower())
