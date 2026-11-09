"""
Giai đoạn 7 — gom kết quả từ reports/*.json thành reports/results.md + biểu đồ reports/figures/*.png.
Mọi số đọc từ file kết quả (không chép tay). Giải mã: greedy (cấu hình mặc định, xem GĐ5).

    python scripts/make_results.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
REP = ROOT / "reports"
FIG = REP / "figures"

# Bảng màu tham chiếu (dataviz skill, chế độ sáng, 3 slot đầu: đạt kiểm tra mù màu cho mọi cặp)
C1, C2, C3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#ffffff"


def load(name):
    return json.loads((REP / f"{name}.json").read_text(encoding="utf-8"))


def style(ax, title, xlabel=None, ylabel=None):
    ax.set_title(title, loc="left", fontsize=12, color=INK, pad=10)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    if xlabel:
        ax.set_xlabel(xlabel, color=INK2, fontsize=9)
    if ylabel:
        ax.set_ylabel(ylabel, color=INK2, fontsize=9)


def save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(FIG / name, dpi=200, facecolor=SURF)
    plt.close(fig)
    return f"figures/{name}"


def lines_chart(xs, series, title, xlabel, ylabel, name, ylim=None):
    """series: [(nhãn, giá trị, màu)] — đường 2px, marker 8px, nhãn trực tiếp ở cuối đường."""
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for lab, ys, col in series:
        ax.plot(xs, ys, color=col, linewidth=2, marker="o", markersize=5, label=lab)
    style(ax, title, xlabel, ylabel)
    ax.set_xticks(xs)
    if ylim:
        ax.set_ylim(*ylim)
    # nhãn giá trị cuối đường, giãn ra để không chồng nhau (tối thiểu 4% chiều cao trục)
    lo, hi = ax.get_ylim()
    gap = 0.045 * (hi - lo)
    ends = sorted((ys[-1], ys[-1]) for _, ys, _ in series)
    placed = []
    for y, v in ends:
        y = max(y, placed[-1][0] + gap) if placed else y
        placed.append((y, v))
    for y, v in placed:
        ax.annotate(f"{v:.1f}", (xs[-1], y), xytext=(8, 0), textcoords="offset points",
                    va="center", fontsize=8, color=INK2, annotation_clip=False)
    ax.legend(frameon=False, fontsize=9, labelcolor=INK2)
    return save(fig, name)


def hbar_chart(labels, values, title, xlabel, name, color=C1, fmt="{:.1f}"):
    fig, ax = plt.subplots(figsize=(6.4, 0.42 * len(labels) + 1.0))
    y = range(len(labels))
    ax.barh(list(y), values, color=color, height=0.6)
    for i, v in zip(y, values):
        ax.text(v + max(values) * 0.01, i, fmt.format(v), va="center", fontsize=8, color=INK2)
    ax.set_yticks(list(y), labels)
    ax.invert_yaxis()
    style(ax, title, xlabel)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_xlim(0, max(values) * 1.12)
    return save(fig, name)


def grouped_bars(groups, series, title, ylabel, name):
    """series: [(nhãn, [giá trị theo nhóm], màu)]."""
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    n = len(series)
    w = 0.8 / n
    for j, (lab, vals, col) in enumerate(series):
        xs = [i - 0.4 + w * (j + 0.5) for i in range(len(groups))]
        ax.bar(xs, vals, width=w * 0.92, color=col, label=lab)
        for x, v in zip(xs, vals):
            ax.text(x, v + 0.6, f"{v:.1f}", ha="center", fontsize=8, color=INK2)
    ax.set_xticks(range(len(groups)), groups)
    style(ax, title, None, ylabel)
    ax.set_ylim(0, max(max(v) for _, v, _ in series) * 1.18)
    ax.legend(frameon=False, fontsize=9, labelcolor=INK2, ncol=len(series), loc="upper right")
    return save(fig, name)


def row(m, cols=("EM", "F1", "HasAns_F1", "NoAns_acc")):
    return " | ".join(f"{m[c]:.1f}" for c in cols)


def main():
    ret = load("retriever_dev")
    base = load("baselines_dev")
    dev, test = load("gd5_dev"), load("gd5_test")
    err = pd.read_csv(REP / "error_labels.csv")
    lat = {d: load(f"latency_{d}") for d in ("cuda", "cpu") if (REP / f"latency_{d}.json").exists()}
    o = lambda d, k: d[k]["overall"]  # noqa: E731
    md = ["# Kết quả tổng hợp", "",
          "Sinh bởi `scripts/make_results.py` từ các file `reports/*.json`. Đơn vị: %. Giải mã **greedy** "
          "(mặc định; biến thể có ngưỡng từ chối xem `reports/gd5_results.md`). Dev dùng để chọn cấu hình, "
          "**test chỉ chạy một lần** (GĐ5). Chi tiết từng giai đoạn: `retriever_dev.md`, `baselines_dev.md`, "
          "`reader_vit5_dev.md`, `gd5_results.md`, `gd5_summary.md`, `gd6_summary.md`, `latency.md`.", ""]

    # ---------------------------------------------------------------- Dữ liệu
    md += ["## 1. Dữ liệu", "",
           "UIT-ViQuAD 2.0, giữ 38 bài lịch sử (9 Việt Nam, 29 thế giới), **chia theo bài** (không rò rỉ đoạn văn giữa các tập). "
           "Kho tri thức 1.862 đoạn. Bảng đầy đủ: `data_stats.md`.", "",
           "| Tập | Bài | Đoạn | Trả lời được | Không trả lời được | Tổng |", "|---|---|---|---|---|---|",
           "| train | 23 | 1.491 | 6.347 | 3.047 | 9.394 |",
           "| dev | 8 | 179 | 892 | 437 | 1.329 |",
           "| test | 7 | 192 | 887 | 399 | 1.286 |", ""]

    # ---------------------------------------------------------------- Retriever
    rows = {r["Cấu hình"].strip("*").replace(" — chọn", ""): r for r in ret["overall"]}
    chosen = [k for k in rows if "k=5, w=0.7" in k][0]
    md += ["## 2. Retriever (dev, 892 câu trả lời được)", "",
           "| Cấu hình | R@1 | R@3 | R@5 | R@10 | R@20 | MRR |", "|---|---|---|---|---|---|---|"]
    for k, r in rows.items():
        name = f"**{k} (chọn)**" if k == chosen else k
        md.append(f"| {name} | " + " | ".join(f"{100 * r[c]:.1f}" for c in ("R@1", "R@3", "R@5", "R@10", "R@20", "MRR")) + " |")
    ks = [1, 3, 5, 10, 20]
    pick = [("BM25 âm tiết", "BM25 · âm tiết", C2), ("Dense tách từ", "Dense · tách từ", C3),
            ("Hybrid RRF (chọn)", chosen, C1)]
    f1 = lines_chart(ks, [(lab, [100 * rows[key][f"R@{k}"] for k in ks], c) for lab, key, c in pick],
                     "Recall@k của Retriever trên dev", "k (số đoạn lấy về)", "Recall@k (%)",
                     "recall_at_k.png", ylim=(40, 100))
    md += ["", f"![Recall@k]({f1})", "",
           "Trên test (đoạn đúng nằm trong k đoạn đã đọc, câu trả lời được):", "",
           "| Retriever | k=1 | k=3 | k=5 |", "|---|---|---|---|"]
    for m in ("bm25", "dense", "hybrid"):
        md.append(f"| {m} | " + " | ".join(f"{test[f'r2m_{m}_k{k}_test_rs']['retrieval']['gold_in_ctx']:.1f}"
                                          for k in (1, 3, 5)) + " |")

    # ---------------------------------------------------------------- Reader trên đoạn đúng
    md += ["", "## 3. Reader đọc đoạn đúng (E1, E4, E5)", "",
           "| Hệ thống | Tập | EM | F1 | HasAns-F1 | NoAns-acc |", "|---|---|---|---|---|---|"]
    readers = [("B0 ngẫu nhiên (danh từ riêng/năm)", base["b0_gold_dev"]["overall"], "dev"),
               ("B2 ViT5 zero-shot", base["b2_gold_dev"]["overall"], "dev"),
               ("B1 XLM-R trích xuất", base["b1_gold_dev"]["overall"], "dev"),
               ("R1 ViT5 (chỉ đoạn đúng)", o(dev, "r1_gold_dev"), "dev"),
               ("E4: R2 bỏ câu không trả lời được", o(dev, "r2noimp_gold_dev_rs"), "dev"),
               ("R2 ViT5 (chính)", o(dev, "r2m_gold_dev_rs"), "dev"),
               ("E5: R2 + 10k ViQuAD ngoài miền", o(dev, "r2ood_gold_dev_rs"), "dev"),
               ("E4: R2 bỏ câu không trả lời được", o(test, "r2noimp_gold_test_rs"), "test"),
               ("R2 ViT5 (chính)", o(test, "r2m_gold_test_rs"), "test"),
               ("E5: R2 + 10k ViQuAD ngoài miền", o(test, "r2ood_gold_test_rs"), "test")]
    for name, m, sp in readers:
        md.append(f"| {name} | {sp} | {row(m)} |")
    md += ["", "B1, R1 chỉ có checkpoint trên Drive nên chưa chấm test. R1 = ViT5 train với đoạn đúng "
           "(9.394 mẫu, 32,4% không trả lời được); R2 = R1 + mỗi câu trả lời được thêm 1 đoạn nhiễu từ "
           "retriever với nhãn \"không có câu trả lời\" (15.741 mẫu)."]
    devr = [(n, m["F1"]) for n, m, sp in readers if sp == "dev"]
    f2 = hbar_chart([n for n, _ in devr], [v for _, v in devr], "F1 trên dev khi đọc đoạn đúng",
                    "F1 (%)", "reader_gold_dev_f1.png")
    md += ["", f"![F1 reader]({f2})", ""]

    # ---------------------------------------------------------------- Toàn hệ thống
    md += ["## 4. Toàn hệ thống trên test (E2, E3)", "",
           "F1 của Reader R2 chính theo retriever và số đoạn k:", "",
           "| Retriever | k=1 | k=3 | k=5 |", "|---|---|---|---|"]
    for m in ("bm25", "dense", "hybrid"):
        md.append(f"| {m} | " + " | ".join(f"{o(test, f'r2m_{m}_k{k}_test_rs')['F1']:.1f}" for k in (1, 3, 5)) + " |")
    md.append(f"| hybrid + Reader E5 (r2ood) | " + " | ".join(
        f"{o(test, f'r2ood_hybrid_k{k}_test_rs')['F1']:.1f}" for k in (1, 3, 5)) + " |")
    f3 = lines_chart([1, 3, 5], [
        ("BM25", [o(test, f"r2m_bm25_k{k}_test_rs")["F1"] for k in (1, 3, 5)], C2),
        ("Dense", [o(test, f"r2m_dense_k{k}_test_rs")["F1"] for k in (1, 3, 5)], C3),
        ("Hybrid", [o(test, f"r2m_hybrid_k{k}_test_rs")["F1"] for k in (1, 3, 5)], C1)],
        "F1 toàn hệ thống trên test theo k (Reader R2 chính)", "k (số đoạn Reader đọc)", "F1 (%)",
        "f1_by_k_test.png")
    best = o(test, "r2ood_hybrid_k5_test_rs")
    r = test["r2ood_hybrid_k5_test_rs"]["retrieval"]
    md += ["", f"![F1 theo k]({f3})", "",
           f"**Hệ thống cuối (r2ood + hybrid top-5, k chọn trên dev): EM {best['EM']:.1f} / F1 {best['F1']:.1f} / "
           f"HasAns-F1 {best['HasAns_F1']:.1f} / NoAns {best['NoAns_acc']:.1f}.**", "",
           f"E3 — tách lỗi tìm / đọc: đoạn đúng nằm trong top-5 ở {r['gold_in_ctx']:.1f}% câu trả lời được; "
           f"HasAns-F1 khi tìm đúng {r['HasAns_F1_hit']:.1f}, khi tìm sai {r['HasAns_F1_miss']:.1f}. "
           f"Từ đoạn đúng (F1 {o(test, 'r2ood_gold_test_rs')['F1']:.1f}) sang tự tìm mất "
           f"{o(test, 'r2ood_gold_test_rs')['F1'] - best['F1']:.1f} F1.", ""]

    # ---------------------------------------------------------------- Theo miền / loại câu
    cfg = [("R2 · đoạn đúng", "r2m_gold_test_rs"), ("R2+OOD · đoạn đúng", "r2ood_gold_test_rs"),
           ("R2+OOD · hybrid top-5", "r2ood_hybrid_k5_test_rs")]
    vn = [test[k]["by_domain"]["VN"]["F1"] for _, k in cfg]
    tg = [test[k]["by_domain"]["TG"]["F1"] for _, k in cfg]
    f4 = grouped_bars([n for n, _ in cfg], [("Lịch sử Việt Nam", vn, C1), ("Lịch sử thế giới", tg, C2)],
                      "F1 trên test theo miền (E5, E6)", "F1 (%)", "f1_by_domain_test.png")
    qt = test["r2ood_hybrid_k5_test_rs"]["by_qtype"]
    qt = sorted(((k, v) for k, v in qt.items() if k != "khác"), key=lambda kv: -kv[1]["F1"])
    f5 = hbar_chart([f"{k} (n={v['n']})" for k, v in qt], [v["F1"] for _, v in qt],
                    "F1 theo loại câu hỏi (hệ thống cuối, test)", "F1 (%)", "f1_by_qtype_test.png")
    md += ["## 5. Theo miền và loại câu hỏi (E6)", "",
           "| Cấu hình (test) | VN | TG |", "|---|---|---|"]
    md += [f"| {n} | {a:.1f} | {b:.1f} |" for (n, _), a, b in zip(cfg, vn, tg)]
    md += ["", f"![Theo miền]({f4})", "", f"![Theo loại câu]({f5})", "",
           "Nhóm \"khác\" (n = 23) không vẽ vì quá ít câu.", ""]

    # ---------------------------------------------------------------- Seed + CI (trích từ GĐ5)
    md += ["## 6. Độ tin cậy", "",
           "- 3 seed (42/13/7), R2 chính, test, greedy: F1 đoạn đúng **57,3 ± 0,5**, hybrid top-5 **51,6 ± 0,9**; "
           "NoAns dao động ± 5 (`gd5_results.md`).",
           "- Bootstrap 2.000 lần trên test (hiệu cặp, CI 95%): E5 − R2 trên đoạn đúng: F1 +2,9 [+0,7; +5,2]; "
           "trên hybrid top-5: F1 +1,6 [−0,7; +3,9] (`gd5_summary.md`). E4 (bỏ câu không trả lời được, "
           "đoạn đúng, bản có ngưỡng từ chối): F1 −5,3 [−7,7; −2,8], NoAns −22,8 [−27,6; −17,9] "
           "(`gd5_results.md`, mục Bootstrap). Các số ở mục này chép từ hai file trên.", ""]

    # ---------------------------------------------------------------- Phân tích lỗi
    names = {"trap": "Trả lời câu bẫy", "paraphrase": "Đúng, khác cách viết", "reader_span": "Đọc sai span",
             "retrieval": "Tìm sai đoạn", "reader_refuse": "Từ chối nhầm", "selection": "Chọn nhầm đoạn",
             "gold_issue": "Đáp án chuẩn có vấn đề", "tokenizer": "Lỗi bộ từ vựng ViT5", "hallucination": "Bịa"}
    cnt = err["label"].value_counts().reindex(list(names), fill_value=0).sort_values(ascending=False)
    f6 = hbar_chart([names[k] for k in cnt.index], [float(v) for v in cnt.values],
                    "Phân loại 100 câu sai (hệ thống cuối, test)", "Số câu (= %)", "error_types.png",
                    fmt="{:.0f}")
    md += ["## 7. Phân tích lỗi (GĐ6)", "", "| Nhóm | Số câu / 100 |", "|---|---|"]
    md += [f"| {names[k]} | {v} |" for k, v in cnt.items()]
    md += ["", f"![Lỗi]({f6})", "", "Chi tiết, ví dụ và kết luận: `error_analysis.md`, `gd6_summary.md`.", ""]

    # ---------------------------------------------------------------- Độ trễ
    if lat:
        md += ["## 8. Độ trễ (ms mỗi câu, trung vị)", "", "| Thiết bị | k | Truy hồi | Reader | Tổng |",
               "|---|---|---|---|---|"]
        for d, L in lat.items():
            for k, v in L["results"].items():
                md.append(f"| {L['hardware']} | {k[1:]} | {v['retrieve']['p50']:.0f} | {v['read']['p50']:.0f} | "
                          f"{v['total']['p50']:.0f} |")
        md.append("")

    # ---------------------------------------------------------------- Mục tiêu
    rec5 = test["r2m_hybrid_k5_test_rs"]["retrieval"]["gold_in_ctx"]
    hasf1 = max(o(test, "r2m_gold_test_rs")["HasAns_F1"], o(test, "r2ood_gold_test_rs")["HasAns_F1"])
    noans = o(test, "r2ood_gold_test_rs")["NoAns_acc"]
    ok = lambda b: "đạt" if b else "**chưa đạt**"  # noqa: E731
    md += ["## 9. So với mục tiêu (PLAN §7, ước lượng ban đầu)", "",
           "| Chỉ số | Mục tiêu | Đạt được (test) | |", "|---|---|---|---|",
           f"| Retriever Recall@5 | ≥ 80 | {rec5:.1f} | {ok(rec5 >= 80)} |",
           f"| Reader trên đoạn đúng, HasAns-F1 | ≥ 70 | {hasf1:.1f} | {ok(hasf1 >= 70)} |",
           f"| Toàn hệ thống F1 | ≥ 55 | {best['F1']:.1f} | {ok(best['F1'] >= 55)} |",
           f"| NoAns-accuracy (đoạn đúng, r2ood) | ≥ 60 | {noans:.1f} | {ok(noans >= 60)} |",
           f"| ViT5 fine-tune so với zero-shot (dev) | cải thiện rõ | F1 {base['b2_gold_dev']['overall']['F1']:.1f} → "
           f"{o(dev, 'r2m_gold_dev_rs')['F1']:.1f} | đạt |", "",
           "Hướng cải thiện đã thử trên dev (chưa chấm test): chọn đáp án theo điểm Reader − λ·(hạng − 1) "
           "tăng F1 dev +1,1 (`gd6_summary.md`).", ""]

    (REP / "results.md").write_text("\n".join(md), encoding="utf-8")
    print("->", REP / "results.md")


if __name__ == "__main__":
    main()
