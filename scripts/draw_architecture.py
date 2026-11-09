"""Vẽ sơ đồ kiến trúc pipeline -> reports/figures/architecture.png (dùng trong báo cáo)."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "reports/figures/architecture.png"
INK, INK2, LINE = "#0b0b0b", "#52514e", "#8a8984"
BLUE, BLUE_BG = "#2a78d6", "#e8f0fb"
ORANGE, ORANGE_BG = "#eb6834", "#fdeee7"
GREEN, GREEN_BG = "#1baf7a", "#e5f6ef"
GRAY_BG = "#f3f2ef"
NL = "\n"

fig, ax = plt.subplots(figsize=(12, 4.8))
ax.set_xlim(0, 119)
ax.set_ylim(0, 46)
ax.axis("off")


def box(x, y, w, h, title, sub, edge, bg, fs=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.2",
                                linewidth=1.4, edgecolor=edge, facecolor=bg))
    if title:
        ax.text(x + w / 2, y + h - 2.6, title, ha="center", va="top", fontsize=fs, color=INK, weight="bold")
    if sub:
        ax.text(x + w / 2, y + h - 6.4, sub, ha="center", va="top", fontsize=8.2, color=INK2, linespacing=1.35)


def arrow(x1, y1, x2, y2, label=None, dy=1.4):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=12,
                                 linewidth=1.3, color=LINE))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + dy, label, ha="center", va="bottom", fontsize=8, color=INK2)


def group(x, y, w, h, title, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.5",
                                linewidth=1.2, edgecolor=color, facecolor="white", linestyle="--"))
    ax.text(x + w / 2, y + h - 1.4, title, ha="center", va="top", fontsize=10, color=color, weight="bold")


# Câu hỏi
box(0.5, 18, 12, 10, "Câu hỏi", "tiếng Việt", LINE, GRAY_BG)
# Retriever
group(17, 6, 44, 36, "RETRIEVER (hybrid)", BLUE)
box(19, 24, 19, 12, "BM25", NL.join(["tách âm tiết,", "chấm điểm toàn kho"]), BLUE, BLUE_BG, 9.5)
box(40, 24, 19, 12, "Dense", NL.join(["bi-encoder PhoBERT,", "câu hỏi tách từ"]), BLUE, BLUE_BG, 9.5)
box(27.5, 8, 23, 11, "Gộp RRF", NL.join(["Σ wᵢ / (5 + hạngᵢ)", "w_BM25 = 1; w_dense = 0,7"]), BLUE, BLUE_BG, 9.5)
arrow(28.5, 23.7, 35, 19.3)
arrow(49.5, 23.7, 43, 19.3)
arrow(12.8, 23, 18.6, 29)
# Kho
box(22, 0.4, 34, 3.2, "", None, LINE, GRAY_BG)
ax.text(39, 2.0, "Kho tri thức: 1.862 đoạn Wikipedia lịch sử", ha="center", va="center", fontsize=8.2, color=INK2)
arrow(39, 3.9, 39, 7.6)
# Reader
group(68, 6, 30, 36, "READER (ViT5-base)", ORANGE)
box(70, 22, 26, 14, "Đọc từng đoạn",
    NL.join(["<q> câu hỏi </q>", "<ctx> đoạn văn </ctx>", "→ đáp án / \"không có câu trả lời\""]),
    ORANGE, ORANGE_BG, 9.5)
box(70, 8, 26, 11, "Chọn đáp án",
    NL.join(["log-prob TB cao nhất trong", "các đáp án không phải từ chối"]), ORANGE, ORANGE_BG, 9.5)
arrow(50.9, 13.5, 69.6, 28, "top-k đoạn", dy=-4.2)
arrow(83, 21.7, 83, 19.3)
# Đầu ra
box(103, 17, 15, 12, "Đáp án", NL.join(["kèm đoạn", "bằng chứng,", "hoặc từ chối"]), GREEN, GREEN_BG)
arrow(96.3, 13.5, 102.6, 20)

OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, dpi=200, bbox_inches="tight", facecolor="white")
print("->", OUT)
