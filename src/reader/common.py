"""Phần dùng chung cho các Reader / baseline: nạp câu hỏi, lấy đoạn văn (gold hoặc retriever)."""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
for sub in ("eval", "retriever"):
    sys.path.insert(0, str(ROOT / "src" / sub))

QA_PATH = ROOT / "data/processed/qa_pairs.parquet"
CORPUS_PATH = ROOT / "data/processed/corpus.parquet"
INDEX_DIR = ROOT / "data/index_qa"


def load_questions(split: str, limit: int | None = None, seed: int = 0) -> pd.DataFrame:
    if split == "test":
        print("⚠️  Đang chạy trên TEST — chỉ nên làm MỘT LẦN cho cấu hình cuối (PLAN.md §5).")
    qa = pd.read_parquet(QA_PATH)
    qa = qa[qa.split == split].reset_index(drop=True)
    if limit and limit < len(qa):
        qa = qa.sample(limit, random_state=seed).reset_index(drop=True)
    return qa


def load_corpus_text() -> dict[str, str]:
    c = pd.read_parquet(CORPUS_PATH, columns=["context_id", "context"])
    return dict(zip(c.context_id, c.context))


def cache_path(mode: str) -> Path:
    return ROOT / f"data/processed/retrieved_{mode}.parquet"


def _from_cache(qa: pd.DataFrame, k: int, mode: str):
    """Đọc top-k từ cache (src/retriever/cache_retrieval.py); None nếu cache thiếu câu / thiếu k."""
    p = cache_path(mode)
    if not p.exists():
        return None
    c = pd.read_parquet(p)
    c = c[c.qa_id.isin(set(qa.qa_id)) & (c["rank"] <= k)]
    groups = {qid: g.sort_values("rank") for qid, g in c.groupby("qa_id")}
    if len(groups) < len(qa) or any(len(g) < k for g in groups.values()):
        return None
    out = [[{"context_id": r.context_id, "rank": int(r.rank), "score": float(r.score)}
            for r in groups[qid].itertuples()] for qid in qa.qa_id]
    return out, float(c.retrieve_ms.mean())


def get_contexts(qa: pd.DataFrame, source: str, k: int = 1, mode: str = "hybrid",
                 batch: int = 256, use_cache: bool = True) -> tuple[list[list[dict]], float]:
    """
    source = "gold"      -> mỗi câu một đoạn đúng (score None)
    source = "retrieved" -> top-k của Retriever (chấm toàn kho); dùng cache
                            data/processed/retrieved_{mode}.parquet nếu đủ (khi đó ms là
                            thời gian đo lúc tạo cache trên máy local)
    Trả về (danh sách contexts theo câu, ms truy hồi trung bình mỗi câu).
    """
    if source == "gold":
        return [[{"context_id": cid, "rank": 1, "score": None}] for cid in qa.context_id], 0.0
    if source != "retrieved":
        raise ValueError(f"source phải là gold | retrieved, nhận {source!r}")
    if use_cache:
        cached = _from_cache(qa, k, mode)
        if cached is not None:
            print(f"Dùng cache truy hồi {cache_path(mode).name} (top-{k})")
            return cached

    from hybrid import Retriever
    r = Retriever.load(str(INDEX_DIR))
    ids = r.meta.context_id.to_numpy()
    out, t0 = [], time.perf_counter()
    qs = qa.question.tolist()
    for i in range(0, len(qs), batch):
        s = r.score_matrix(qs[i:i + batch], mode)
        top = np.argsort(-s, axis=1, kind="stable")[:, :k]
        for row, idx in zip(s, top):
            out.append([{"context_id": str(ids[j]), "rank": n + 1, "score": float(row[j])}
                        for n, j in enumerate(idx)])
    ms = 1000 * (time.perf_counter() - t0) / max(len(qs), 1)
    return out, ms
