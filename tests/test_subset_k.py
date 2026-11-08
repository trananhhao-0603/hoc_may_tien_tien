"""Test suy ra top-k nhỏ hơn từ file top-K (src/reader/subset_k.py)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "reader"))
from subset_k import subset  # noqa: E402
from metrics import NO_ANSWER  # noqa: E402


def make_row():
    ctx = [{"context_id": f"c{i}", "rank": i, "score": 1.0 / i} for i in (1, 2, 3)]
    pcs = [{"context_id": "c1", "answer": NO_ANSWER, "score": -0.1},
           {"context_id": "c2", "answer": "1954", "score": -0.5},
           {"context_id": "c3", "answer": "1975", "score": -0.2}]
    return {"qa_id": "q", "contexts": ctx, "prediction": "1975", "extra": {"per_context": pcs}}


def test_k1_refuses_when_only_refusal():
    r = subset(make_row(), 1)
    assert r["prediction"] == NO_ANSWER and r["used_context_id"] is None
    assert [c["context_id"] for c in r["contexts"]] == ["c1"]


def test_k2_and_k3_repick():
    assert subset(make_row(), 2)["prediction"] == "1954"
    r = subset(make_row(), 3)
    assert (r["prediction"], r["used_context_id"]) == ("1975", "c3")
