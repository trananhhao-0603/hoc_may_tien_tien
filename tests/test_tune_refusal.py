"""Test quy tắc ngưỡng từ chối (src/reader/tune_refusal.py) trên dự đoán giả."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "reader"))
from tune_refusal import decide, sweep  # noqa: E402  (import common -> thêm src/eval)
from metrics import NO_ANSWER, is_no_answer  # noqa: E402


def pc(cid, refuse, alt_answer, alt):
    return {"context_id": cid, "refuse_score": refuse, "alt_answer": alt_answer, "alt_score": alt}


def row(pcs, gold=("1954",), imp=False):
    return {"extra": {"per_context": pcs}, "gold_answers": [] if imp else list(gold),
            "is_impossible": imp}


def test_delta_controls_refusal():
    r = row([pc("c1", -0.2, "1954", -0.5)])          # refuse - alt = 0.3
    assert is_no_answer(decide(r, 0.0)[0])           # 0.3 > 0   -> từ chối
    assert decide(r, 0.5)[0] == "1954"               # 0.3 <= 0.5 -> trả lời
    assert decide(r, 0.3)[0] == "1954"               # bằng ngưỡng -> trả lời


def test_multi_context_picks_best_non_refusal():
    r = row([pc("c1", -0.1, "1945", -2.0),           # margin 1.9 -> từ chối
             pc("c2", -3.0, "1954", -0.4),           # margin -2.6 -> trả lời
             pc("c3", -3.0, "1975", -0.9)])          # trả lời nhưng điểm thấp hơn
    ans, _, used = decide(r, 0.0)
    assert (ans, used) == ("1954", "c2")


def test_all_refuse_returns_no_answer():
    r = row([pc("c1", -0.1, "1945", -2.0), pc("c2", -0.2, "1954", -3.0)])
    ans, _, used = decide(r, 0.0)
    assert ans == NO_ANSWER and used is None


def test_sweep_extremes():
    rows = [row([pc("c1", -0.2, "1954", -0.5)]),
            row([pc("c2", -0.1, "1975", -1.0)], imp=True)]
    (d_lo, m_lo), (d_hi, m_hi) = sweep(rows, [-5.0, 5.0])
    assert m_lo["NoAns_acc"] == 100.0 and m_lo["HasAns_abstain"] == 100.0   # luôn từ chối
    assert m_hi["NoAns_acc"] == 0.0 and m_hi["HasAns_F1"] == 100.0         # không bao giờ
