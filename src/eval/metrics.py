"""
Metric hỏi đáp tiếng Việt: EM và F1 theo token (âm tiết), kiểu squad_v2.

Chuẩn hoá trước khi so (normalize_answer):
  1. NFC
  2. chữ thường
  3. thống nhất vị trí dấu thanh kiểu cũ/mới: "hòa" == "hoà", "thủy" == "thuỷ"
     (kho dữ liệu dùng lẫn cả hai: "hòa" 605 lần, "hoà" 953 lần)
  4. bỏ dấu câu (mọi ký tự Unicode loại P*, và S* như ký hiệu tiền tệ/toán)
  5. gộp khoảng trắng
KHÔNG bỏ dấu thanh: "Hà" và "Ha" là hai đáp án khác nhau.

Câu không trả lời được (squad_v2): đáp án chuẩn là rỗng. Dự đoán được coi là
"không trả lời" nếu chuỗi thô rỗng hoặc bằng nhãn NO_ANSWER (sau chuẩn hoá).
  - câu không trả lời được: EM = F1 = 1 nếu mô hình từ chối, ngược lại 0
  - câu trả lời được mà mô hình từ chối: EM = F1 = 0

    from metrics import score, aggregate
    s = score("năm 1954", ["1954"])      # {"em": 0.0, "f1": 0.667}
"""
from __future__ import annotations

import re
import unicodedata
from collections import Counter
from typing import Iterable, Optional

NO_ANSWER = "không có câu trả lời"

_TONES = "̣̀́̃̉"          # huyền, sắc, ngã, hỏi, nặng
# Kiểu mới -> kiểu cũ: dấu thanh đặt trên o/u (không mũ, không móc) khi theo sau
# là a/e/y ở cuối âm tiết: "hòa" -> "hoà", "thủy" -> "thuỷ". Làm trên dạng NFD,
# nên "o" đứng ngay trước dấu thanh chắc chắn là o trơn (ô/ơ có dấu phụ chen giữa).
# Cũng biến "của" -> "cuả" — vô hại vì gold và dự đoán qua cùng một phép chuẩn hoá.
_TONE_POS_RE = re.compile(rf"([ou])([{_TONES}])([aey])(?![\ẁ-ͯ])")
_SPACE_RE = re.compile(r"\s+")


def _unify_tone_position(text: str) -> str:
    d = unicodedata.normalize("NFD", text)
    d = _TONE_POS_RE.sub(lambda m: m.group(1) + m.group(3) + m.group(2), d)
    return unicodedata.normalize("NFC", d)


def _strip_punct(text: str) -> str:
    return "".join(" " if unicodedata.category(ch)[0] in "PS" else ch for ch in text)


def normalize_answer(text: Optional[str]) -> str:
    text = unicodedata.normalize("NFC", text or "").lower()
    text = _unify_tone_position(text)
    text = _strip_punct(text)
    return _SPACE_RE.sub(" ", text).strip()


_NO_ANSWER_NORM = normalize_answer(NO_ANSWER)


def is_no_answer(text: Optional[str]) -> bool:
    """Từ chối = chuỗi thô rỗng, hoặc đúng nhãn NO_ANSWER sau chuẩn hoá.
    Chuỗi chỉ có dấu câu/ký hiệu ("*>+>") KHÔNG tính là từ chối — nếu không, mô hình
    sinh rác (ViT5 zero-shot) sẽ được điểm NoAns cao một cách ảo."""
    if not (text or "").strip():
        return True
    return normalize_answer(text) == _NO_ANSWER_NORM


def answer_tokens(text: Optional[str]) -> list[str]:
    return normalize_answer(text).split()


# ---------------------------------------------------------------- một cặp
def exact_match(pred: str, gold: str) -> float:
    return float(normalize_answer(pred) == normalize_answer(gold))


def f1_score(pred: str, gold: str) -> float:
    p, g = answer_tokens(pred), answer_tokens(gold)
    if not p or not g:                      # một bên rỗng: đúng chỉ khi cả hai rỗng
        return float(p == g)
    common = sum((Counter(p) & Counter(g)).values())
    if common == 0:
        return 0.0
    prec, rec = common / len(p), common / len(g)
    return 2 * prec * rec / (prec + rec)


# ---------------------------------------------------------------- squad_v2
def score(pred: Optional[str], golds: Iterable[str], is_impossible: bool = False) -> dict:
    """EM/F1 của một câu; lấy max trên các đáp án chuẩn (như squad)."""
    abstain = is_no_answer(pred)
    if is_impossible:
        v = float(abstain)
        return {"em": v, "f1": v, "abstain": abstain}
    golds = [g for g in golds if not is_no_answer(g)]
    if not golds:
        raise ValueError("Câu trả lời được nhưng không có đáp án chuẩn nào")
    if abstain:
        return {"em": 0.0, "f1": 0.0, "abstain": True}
    return {"em": max(exact_match(pred, g) for g in golds),
            "f1": max(f1_score(pred, g) for g in golds),
            "abstain": False}


def aggregate(rows: list[dict]) -> dict:
    """
    rows: list các dict có em, f1, abstain, is_impossible (đầu ra score + cờ).
    Trả về chỉ số theo thang 0–100 (như squad_v2), kèm số câu.
    """
    n = len(rows)
    has = [r for r in rows if not r["is_impossible"]]
    no = [r for r in rows if r["is_impossible"]]

    def mean(xs, key):
        return 100.0 * sum(x[key] for x in xs) / len(xs) if xs else float("nan")

    return {
        "n": n, "n_has": len(has), "n_no": len(no),
        "EM": mean(rows, "em"), "F1": mean(rows, "f1"),
        "HasAns_EM": mean(has, "em"), "HasAns_F1": mean(has, "f1"),
        "NoAns_acc": mean(no, "em"),
        # tỉ lệ từ chối sai: câu trả lời được mà mô hình nói "không có câu trả lời"
        "HasAns_abstain": mean(has, "abstain"),
    }
