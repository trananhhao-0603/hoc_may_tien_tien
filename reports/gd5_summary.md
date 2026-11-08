# GĐ5 — Kết luận

Bảng đầy đủ: `reports/gd5_results.md`; chi tiết từng run: `reports/gd5_dev.md`, `reports/gd5_test.md`.

## Kết luận GĐ5 (viết tay từ các bảng trên)

Thêm phép so sánh cặp bằng bootstrap trên test, giải mã greedy (`src/eval/bootstrap.py --paired`):

| So sánh | EM | F1 | HasAns_F1 | NoAns_acc |
|---|---|---|---|---|
| r2ood_gold_test_rs − r2m_gold_test_rs | +4.1 [+1.6, +6.5] | +2.9 [+0.7, +5.2] | +1.8 [-0.5, +4.3] | +5.3 [+0.7, +10.0] |
| r2ood_hybrid_k5_test_rs − r2m_hybrid_k5_test_rs | +3.1 [+0.7, +5.5] | +1.6 [-0.7, +3.9] | +0.4 [-2.2, +2.8] | +4.3 [-0.5, +9.0] |

Toàn hệ thống tốt nhất trên test: **R2 + ViQuAD ngoài miền (r2ood), hybrid top-5, greedy: EM 39.4 / F1 53.4 / HasAns-F1 52.2 / NoAns 55.9**
(top-3: F1 54.0; nhưng k chọn trên dev là 5). Model chính r2m (không có dữ liệu ngoài miền) hybrid top-5: F1 51.8.

1. **Dò tham số:** 8 epoch, lr 1e-4 tốt nhất (F1 dev 57.5). lr 3e-4 kém hơn rõ (46.9).
2. **E1:** R2 (8 epoch) hơn B1 XLM-R trên dev: F1 57.5 so với 51.5, NoAns 54.0 so với 30.9; HasAns-F1 kém hơn một chút (59.2 so với 61.7).
3. **E2:** hybrid ≈ BM25 > dense nhiều. k = 3–5 tốt hơn k = 1 khoảng 2–3 F1. Trên test, hybrid k5 và BM25 k5 bằng nhau (51.7).
4. **E3:** khi retriever tìm đúng đoạn, HasAns-F1 là 55.7 (test); khi tìm sai chỉ còn 4.1. Từ đoạn đúng sang tự tìm mất 5.1 F1 (CI [+3.8, +6.4]).
5. **Ngưỡng từ chối:** tăng NoAns (+2.0) nhưng giảm HasAns-F1 (−1.6). Tổng F1 trên test không đổi (−0.5, CI chứa 0). Ngưỡng chỉ là núm điều chỉnh đánh đổi, không phải cải tiến. Mặc định dùng greedy.
6. **E4:** câu không trả lời được trong train là thiết yếu. Bỏ chúng làm mất 5.3 F1 và 22.8 điểm NoAns trên test.
7. **E5:** thêm 10k câu ViQuAD ngoài miền giúp tăng: F1 đoạn đúng trên test +2.9 (có ý nghĩa), toàn hệ thống +1.6 (chưa có ý nghĩa ở mức 95%). Cả VN và TG đều tăng.
8. **E6:** VN dễ hơn TG. Câu "như thế nào" và "khác" khó nhất (F1 khoảng 43–49); "khi nào" và "ai" dễ nhất.
9. **Seed:** F1 test đoạn đúng 57.3 ± 0.5 (greedy); NoAns dao động nhiều (± 5).
10. **Mục tiêu §7:** toàn hệ thống F1 test ≥ 55 **chưa đạt** (53.4); HasAns-F1 ≥ 70 **chưa đạt** (khoảng 60); NoAns ≥ 60% **đạt** với r2ood trên đoạn đúng (60.7, greedy).
