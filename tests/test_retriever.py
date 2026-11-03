"""Test logic Retriever trên kho nhỏ, encoder giả (không tải model).
Cần: numpy, pandas, rank-bm25, underthesea.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "retriever"))
from hybrid import Retriever  # noqa: E402
from text import segment, tokens  # noqa: E402

DOCS = [
    ("c0", "Điện Biên Phủ", "Chiến thắng Điện Biên Phủ diễn ra năm 1954 dưới sự chỉ huy của Võ Nguyên Giáp."),
    ("c1", "La Mã", "Đế quốc La Mã sụp đổ năm 476 do áp lực từ các bộ tộc Germanic."),
    ("c2", "Nhà Lý", "Lý Công Uẩn dời đô từ Hoa Lư ra Thăng Long vào năm 1010."),
]
meta = pd.DataFrame(DOCS, columns=["context_id", "title", "context"])
meta["context_seg"] = [segment(c) for c in meta.context]

# encoder giả: túi từ trên từ vựng của kho (đủ để kiểm logic dense)
VOCAB = sorted({t for c in meta.context for t in tokens(c, "syl")})


def fake_encoder(texts):
    m = np.zeros((len(texts), len(VOCAB)), dtype="float32")
    for i, t in enumerate(texts):
        for w in tokens(t.replace("_", " "), "syl"):
            if w in VOCAB:
                m[i, VOCAB.index(w)] += 1
    return m / np.maximum(np.linalg.norm(m, axis=1, keepdims=True), 1e-9)


emb = fake_encoder(meta.context.tolist())
r = Retriever(meta, dense={"seg": emb, "raw": emb}, encoder=fake_encoder)

# --- tách token ---
assert tokens("Điện Biên Phủ, 1954!", "syl") == ["điện", "biên", "phủ", "1954"]
assert "điện_biên_phủ" in tokens("Chiến thắng Điện Biên Phủ năm 1954", "seg")
assert "," not in tokens("A, B", "syl")

# --- ranks: hạng 0 = điểm cao nhất ---
rk = Retriever.ranks(np.array([[0.1, 0.9, 0.5]]))
assert rk.tolist() == [[2, 0, 1]], rk

# --- RRF: đoạn đứng đầu ở cả hai nhánh phải đứng đầu khi gộp ---
fused = r.rrf(np.array([[3.0, 1.0, 2.0]]), np.array([[0.9, 0.1, 0.5]]))
assert int(np.argmax(fused[0])) == 0

# --- mỗi mode đều tìm đúng đoạn cho câu hỏi dễ ---
cases = [("Chiến thắng Điện Biên Phủ diễn ra năm nào?", "c0"),
         ("Đế quốc La Mã sụp đổ vì sao?", "c1"),
         ("Lý Công Uẩn dời đô ra đâu?", "c2")]
for mode in ("bm25", "dense", "hybrid"):
    for tok in ("syl", "seg"):
        for q, gold in cases:
            top = r.search(q, k=1, mode=mode, bm25_tok=tok)[0]
            assert top["context_id"] == gold, (mode, tok, q, top)

# --- ma trận điểm đúng kích thước, search trả đủ k kết quả có thứ hạng ---
S = r.score_matrix([c[0] for c in cases], mode="hybrid")
assert S.shape == (3, 3)
res = r.search(cases[0][0], k=3)
assert [x["rank"] for x in res] == [1, 2, 3] and len({x["context_id"] for x in res}) == 3

print("✅ TẤT CẢ TEST PASS — tách token, xếp hạng, RRF, BM25/dense/hybrid đúng.")
