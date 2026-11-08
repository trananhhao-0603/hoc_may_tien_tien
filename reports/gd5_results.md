# Giai đoạn 5 — Kết quả thí nghiệm

Sinh bởi `scripts/gd5_report.py`. **greedy** = giải mã tham lam như GĐ4; **ngưỡng** = từ chối chỉ khi `điểm từ chối − điểm đáp án thay thế > δ`, δ chọn trên dev theo F1 cho từng cấu hình và áp nguyên cho test. Test chạy đúng một lần.

Model chính: `models/r2_lr1e-4_e8` (lr 0.0001, 8.0 epoch); ứng viên (F1 dev đoạn đúng): `models/r2_vit5` 55.9, `models/r2_lr3e-4_e5` 46.9, `models/r2_lr1e-4_e8` 57.5

Cấu hình hybrid tốt nhất trên dev: `r2m_hybrid_k5`; tốt nhất mọi retriever: `r2m_hybrid_k5`.

## E1 — Trích xuất (B1) vs sinh (ViT5), đọc trên đoạn đúng

| Run | EM | F1 | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|
| B1 XLM-R (dev) | 37.4 | 51.5 | 61.7 | 30.9 | 20.5 |
| R1 ViT5 (dev) | 37.4 | 51.1 | 57.3 | 38.2 | 27.7 |
| R2 greedy (dev) | 44.1 | 57.5 | 59.2 | 54.0 | 23.0 |
| R2 ngưỡng (dev) | 44.6 | 57.8 | 58.0 | 57.4 | 24.6 |
| R2 greedy (test) | 40.4 | 57.4 | 58.3 | 55.4 | 23.2 |
| R2 ngưỡng (test) | 40.4 | 56.9 | 56.6 | 57.4 | 25.9 |

B1, R1 chỉ có checkpoint trên Drive nên chưa chấm test (cần chạy trên Colab).

## E2 — Retriever × k (Reader R2 chính, F1 sau ngưỡng; trong ngoặc: greedy)

**dev**

| Retriever | k=1 | k=3 | k=5 |
|---|---|---|---|
| bm25 | 52.2 (52.0) | 53.7 (53.2) | 53.8 (53.2) |
| dense | 45.9 (45.5) | 48.4 (48.0) | 49.2 (48.5) |
| hybrid | 51.2 (50.8) | 54.2 (53.6) | 54.3 (53.7) |

**test**

| Retriever | k=1 | k=3 | k=5 |
|---|---|---|---|
| bm25 | 50.0 (50.0) | 51.2 (51.1) | 51.7 (51.4) |
| dense | 43.5 (43.9) | 48.2 (48.3) | 49.3 (49.2) |
| hybrid | 49.2 (49.7) | 51.3 (51.3) | 51.7 (51.8) |

Tỉ lệ đoạn đúng nằm trong k đoạn đã đọc (dev, câu trả lời được):

| Retriever | k=1 | k=3 | k=5 |
|---|---|---|---|
| bm25 | 76.1 | 86.5 | 90.4 |
| dense | 52.2 | 67.5 | 73.7 |
| hybrid | 71.9 | 89.3 | 93.4 |

## E3 — Đoạn đúng vs đoạn tự tìm (tách sai số tìm / đọc)

| Tập | F1 đoạn đúng | F1 r2m_hybrid_k5 | đoạn đúng trong top-k % | HasAns-F1 khi tìm đúng | HasAns-F1 khi tìm sai |
|---|---|---|---|---|---|
| dev | 57.8 | 54.3 | 93.4 | 57.5 | 6.4 |
| test | 56.9 | 51.7 | 90.2 | 55.7 | 4.1 |

## E4 — Có vs không có câu không trả lời được khi train

| Tập | Đoạn | Giải mã | Model | EM | F1 | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|---|
| dev | gold | greedy | R2 (chính, seed 42) | 44.1 | 57.5 | 59.2 | 54.0 | 23.0 |
| dev | gold | greedy | E4: R2 bỏ câu không trả lời được | 36.0 | 50.6 | 62.2 | 27.0 | 18.0 |
| dev | gold | ngưỡng | R2 (chính, seed 42) | 44.6 | 57.8 | 58.0 | 57.4 | 24.6 |
| dev | gold | ngưỡng | E4: R2 bỏ câu không trả lời được | 37.4 | 51.7 | 60.8 | 33.0 | 20.9 |
| dev | hybrid_k3 | greedy | R2 (chính, seed 42) | 41.2 | 53.6 | 54.0 | 52.9 | 24.4 |
| dev | hybrid_k3 | greedy | E4: R2 bỏ câu không trả lời được | 33.1 | 46.6 | 55.4 | 28.6 | 20.2 |
| dev | hybrid_k3 | ngưỡng | R2 (chính, seed 42) | 42.1 | 54.2 | 52.8 | 57.0 | 27.0 |
| dev | hybrid_k3 | ngưỡng | E4: R2 bỏ câu không trả lời được | 39.0 | 49.1 | 45.7 | 56.1 | 41.5 |
| test | gold | greedy | R2 (chính, seed 42) | 40.4 | 57.4 | 58.3 | 55.4 | 23.2 |
| test | gold | greedy | E4: R2 bỏ câu không trả lời được | 33.8 | 51.2 | 60.9 | 29.6 | 16.9 |
| test | gold | ngưỡng | R2 (chính, seed 42) | 40.4 | 56.9 | 56.6 | 57.4 | 25.9 |
| test | gold | ngưỡng | E4: R2 bỏ câu không trả lời được | 34.8 | 51.6 | 59.2 | 34.6 | 20.4 |
| test | hybrid_k3 | greedy | R2 (chính, seed 42) | 36.1 | 51.3 | 50.6 | 52.9 | 25.4 |
| test | hybrid_k3 | greedy | E4: R2 bỏ câu không trả lời được | 31.4 | 46.7 | 53.1 | 32.3 | 18.7 |
| test | hybrid_k3 | ngưỡng | R2 (chính, seed 42) | 36.5 | 51.3 | 49.2 | 55.9 | 28.3 |
| test | hybrid_k3 | ngưỡng | E4: R2 bỏ câu không trả lời được | 35.0 | 46.6 | 41.4 | 58.1 | 43.4 |

## E5 — Thêm ViQuAD ngoài miền khi train

| Tập | Đoạn | Giải mã | Model | EM | F1 | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|---|
| dev | gold | greedy | R2 (chính, seed 42) | 44.1 | 57.5 | 59.2 | 54.0 | 23.0 |
| dev | gold | greedy | E5: R2 + 10k ViQuAD ngoài miền | 44.2 | 58.9 | 63.4 | 49.9 | 18.6 |
| dev | gold | ngưỡng | R2 (chính, seed 42) | 44.6 | 57.8 | 58.0 | 57.4 | 24.6 |
| dev | gold | ngưỡng | E5: R2 + 10k ViQuAD ngoài miền | 46.8 | 59.7 | 56.6 | 65.9 | 30.3 |
| dev | hybrid_k3 | greedy | R2 (chính, seed 42) | 41.2 | 53.6 | 54.0 | 52.9 | 24.4 |
| dev | hybrid_k3 | greedy | E5: R2 + 10k ViQuAD ngoài miền | 40.0 | 53.6 | 56.6 | 47.6 | 20.7 |
| dev | hybrid_k3 | ngưỡng | R2 (chính, seed 42) | 42.1 | 54.2 | 52.8 | 57.0 | 27.0 |
| dev | hybrid_k3 | ngưỡng | E5: R2 + 10k ViQuAD ngoài miền | 44.1 | 56.0 | 51.2 | 65.7 | 32.3 |
| test | gold | greedy | R2 (chính, seed 42) | 40.4 | 57.4 | 58.3 | 55.4 | 23.2 |
| test | gold | greedy | E5: R2 + 10k ViQuAD ngoài miền | 44.6 | 60.3 | 60.1 | 60.7 | 21.2 |
| test | gold | ngưỡng | R2 (chính, seed 42) | 40.4 | 56.9 | 56.6 | 57.4 | 25.9 |
| test | gold | ngưỡng | E5: R2 + 10k ViQuAD ngoài miền | 44.9 | 58.0 | 51.2 | 73.2 | 34.6 |
| test | hybrid_k3 | greedy | R2 (chính, seed 42) | 36.1 | 51.3 | 50.6 | 52.9 | 25.4 |
| test | hybrid_k3 | greedy | E5: R2 + 10k ViQuAD ngoài miền | 40.0 | 54.0 | 51.6 | 59.1 | 23.3 |
| test | hybrid_k3 | ngưỡng | R2 (chính, seed 42) | 36.5 | 51.3 | 49.2 | 55.9 | 28.3 |
| test | hybrid_k3 | ngưỡng | E5: R2 + 10k ViQuAD ngoài miền | 41.8 | 53.6 | 44.8 | 72.9 | 37.5 |

F1 theo miền (đoạn đúng, ngưỡng):

| Tập | Model | VN | TG |
|---|---|---|---|
| dev | R2 (chính, seed 42) | 61.3 | 56.3 |
| dev | E5: R2 + 10k ViQuAD ngoài miền | 62.0 | 58.6 |
| test | R2 (chính, seed 42) | 58.1 | 56.2 |
| test | E5: R2 + 10k ViQuAD ngoài miền | 59.1 | 57.5 |

## E6 — Tách theo miền và loại câu hỏi (R2 chính, ngưỡng)

**gold, dev**

| Nhóm | n | EM | F1 | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|
| VN | 407.0 | 47.4 | 61.3 | 71.0 | 46.2 | 10.1 |
| TG | 922.0 | 43.4 | 56.3 | 53.0 | 63.9 | 30.1 |
| khi nào | 134.0 | 52.2 | 67.1 | 74.4 | 52.3 | 14.4 |
| ai | 159.0 | 52.8 | 57.5 | 60.4 | 51.0 | 20.0 |
| ở đâu | 100.0 | 45.0 | 52.7 | 59.5 | 40.0 | 26.2 |
| bao nhiêu | 131.0 | 48.1 | 62.1 | 62.0 | 62.2 | 19.8 |
| vì sao | 120.0 | 42.5 | 59.1 | 54.4 | 67.4 | 27.3 |
| như thế nào | 129.0 | 30.2 | 46.6 | 45.7 | 48.6 | 28.3 |
| cái gì | 514.0 | 44.6 | 58.7 | 57.2 | 61.5 | 27.8 |
| khác | 42.0 | 28.6 | 47.5 | 43.1 | 80.0 | 27.0 |

**gold, test**

| Nhóm | n | EM | F1 | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|
| VN | 420.0 | 42.4 | 58.1 | 60.1 | 53.8 | 21.0 |
| TG | 866.0 | 39.5 | 56.2 | 54.9 | 59.1 | 28.3 |
| khi nào | 88.0 | 44.3 | 61.7 | 58.1 | 69.0 | 25.4 |
| ai | 216.0 | 50.9 | 60.9 | 60.8 | 61.1 | 22.9 |
| ở đâu | 75.0 | 41.3 | 58.0 | 61.0 | 50.0 | 21.8 |
| bao nhiêu | 49.0 | 40.8 | 58.4 | 67.6 | 41.2 | 9.4 |
| vì sao | 155.0 | 33.5 | 52.8 | 52.1 | 54.3 | 27.5 |
| như thế nào | 117.0 | 32.5 | 48.6 | 47.3 | 51.3 | 34.6 |
| cái gì | 563.0 | 39.8 | 58.2 | 57.8 | 59.0 | 25.4 |
| khác | 23.0 | 26.1 | 30.3 | 29.9 | 33.3 | 55.0 |

**hybrid_k5, dev**

| Nhóm | n | EM | F1 | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|
| VN | 407.0 | 45.0 | 58.2 | 66.7 | 45.0 | 8.1 |
| TG | 922.0 | 40.5 | 52.5 | 49.4 | 59.9 | 30.9 |
| khi nào | 134.0 | 44.8 | 61.5 | 68.2 | 47.7 | 15.6 |
| ai | 159.0 | 50.9 | 55.6 | 57.7 | 51.0 | 20.0 |
| ở đâu | 100.0 | 45.0 | 52.6 | 57.9 | 42.9 | 24.6 |
| bao nhiêu | 131.0 | 46.6 | 59.3 | 59.0 | 60.0 | 19.8 |
| vì sao | 120.0 | 37.5 | 51.4 | 46.3 | 60.5 | 26.0 |
| như thế nào | 129.0 | 27.9 | 43.3 | 42.3 | 45.9 | 27.2 |
| cái gì | 514.0 | 42.2 | 55.4 | 54.2 | 57.5 | 27.8 |
| khác | 42.0 | 26.2 | 42.1 | 37.0 | 80.0 | 32.4 |

**hybrid_k5, test**

| Nhóm | n | EM | F1 | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|
| VN | 420.0 | 39.0 | 53.8 | 54.9 | 51.5 | 21.4 |
| TG | 866.0 | 35.6 | 50.7 | 48.6 | 55.4 | 28.0 |
| khi nào | 88.0 | 43.2 | 58.3 | 54.7 | 65.5 | 25.4 |
| ai | 216.0 | 45.4 | 56.2 | 57.2 | 54.2 | 19.4 |
| ở đâu | 75.0 | 36.0 | 50.7 | 52.7 | 45.0 | 21.8 |
| bao nhiêu | 49.0 | 38.8 | 54.5 | 61.5 | 41.2 | 15.6 |
| vì sao | 155.0 | 31.0 | 49.4 | 47.3 | 54.3 | 26.6 |
| như thế nào | 117.0 | 28.2 | 42.9 | 42.6 | 43.6 | 33.3 |
| cái gì | 563.0 | 36.1 | 52.1 | 49.8 | 57.2 | 27.2 |
| khác | 23.0 | 26.1 | 34.8 | 35.0 | 33.3 | 40.0 |

## Ổn định theo seed (R2, seed 42 / 13 / 7): trung bình ± độ lệch chuẩn

| Tập | Đoạn | Giải mã | số seed | EM | F1 | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|---|
| dev | gold | greedy | 3 | 42.7 ± 1.2 | 56.1 ± 1.3 | 57.8 ± 1.8 | 52.6 ± 1.8 | 24.6 ± 2.0 |
| dev | gold | ngưỡng | 3 | 44.0 ± 0.6 | 56.5 ± 1.3 | 54.6 ± 4.2 | 60.3 ± 4.9 | 29.6 ± 5.8 |
| dev | hybrid_k3 | greedy | 3 | 40.4 ± 1.1 | 52.7 ± 1.2 | 53.2 ± 1.5 | 51.6 ± 1.1 | 25.6 ± 1.8 |
| dev | hybrid_k3 | ngưỡng | 3 | 42.0 ± 0.1 | 53.5 ± 1.0 | 50.4 ± 3.9 | 59.8 ± 4.9 | 31.3 ± 5.6 |
| dev | hybrid_k5 | greedy | 3 | 39.9 ± 0.9 | 52.4 ± 1.1 | 54.3 ± 1.3 | 48.6 ± 1.6 | 23.1 ± 2.0 |
| dev | hybrid_k5 | ngưỡng | 3 | 41.9 ± 0.2 | 53.7 ± 0.7 | 51.7 ± 3.7 | 57.7 ± 5.3 | 28.7 ± 5.8 |
| test | gold | greedy | 3 | 41.0 ± 1.4 | 57.3 ± 0.5 | 57.4 ± 1.7 | 57.0 ± 5.3 | 24.5 ± 3.0 |
| test | gold | ngưỡng | 3 | 41.3 ± 1.2 | 56.3 ± 0.5 | 53.4 ± 4.0 | 62.8 ± 7.3 | 30.8 ± 6.3 |
| test | hybrid_k3 | greedy | 3 | 36.8 ± 1.5 | 51.5 ± 0.9 | 49.9 ± 1.1 | 55.1 ± 5.4 | 26.8 ± 2.1 |
| test | hybrid_k3 | ngưỡng | 3 | 37.9 ± 1.6 | 51.4 ± 0.1 | 46.6 ± 3.4 | 62.0 ± 7.9 | 32.9 ± 5.9 |
| test | hybrid_k5 | greedy | 3 | 36.8 ± 1.3 | 51.6 ± 0.9 | 51.0 ± 1.1 | 53.1 ± 4.7 | 24.2 ± 2.0 |
| test | hybrid_k5 | ngưỡng | 3 | 37.9 ± 1.5 | 51.5 ± 0.3 | 47.7 ± 3.5 | 60.2 ± 7.8 | 30.4 ± 5.9 |

## Ngưỡng δ chọn trên dev

| Cấu hình | δ | F1 dev |
|---|---|---|
| r2m_bm25_k1 | -0.12 | 52.2 |
| r2m_bm25_k3 | -0.12 | 53.7 |
| r2m_bm25_k5 | -0.12 | 53.8 |
| r2m_dense_k1 | -0.14 | 45.9 |
| r2m_dense_k3 | -0.14 | 48.4 |
| r2m_dense_k5 | -0.52 | 49.2 |
| r2m_gold | -0.12 | 57.8 |
| r2m_hybrid_k1 | -0.14 | 51.2 |
| r2m_hybrid_k3 | -0.14 | 54.2 |
| r2m_hybrid_k5 | -0.14 | 54.3 |
| r2noimp_gold | -0.16 | 51.7 |
| r2noimp_hybrid_k1 | -0.64 | 47.2 |
| r2noimp_hybrid_k3 | -0.66 | 49.1 |
| r2noimp_hybrid_k5 | -0.64 | 49.7 |
| r2ood_gold | -0.40 | 59.7 |
| r2ood_hybrid_k1 | -0.44 | 52.7 |
| r2ood_hybrid_k3 | -0.42 | 56.0 |
| r2ood_hybrid_k5 | -0.42 | 56.4 |
| r2s13_gold | -0.22 | 55.2 |
| r2s13_hybrid_k1 | -0.20 | 50.0 |
| r2s13_hybrid_k3 | -0.24 | 52.3 |
| r2s13_hybrid_k5 | -0.24 | 52.9 |
| r2s7_gold | -0.20 | 56.4 |
| r2s7_hybrid_k1 | -0.20 | 50.9 |
| r2s7_hybrid_k3 | -0.20 | 53.9 |
| r2s7_hybrid_k5 | -0.20 | 54.0 |

## Bootstrap CI 95% trên test (2000 lần lấy mẫu lại câu hỏi)

| Run | EM | F1 | HasAns_F1 | NoAns_acc |
|---|---|---|---|---|
| r2m_gold_test_thr | 40.4 [37.7, 43.1] | 56.9 [54.3, 59.4] | 56.6 [53.7, 59.5] | 57.4 [52.4, 61.9] |
| r2m_hybrid_k5_test_thr | 36.7 [34.1, 39.3] | 51.7 [49.2, 54.3] | 50.7 [47.8, 53.6] | 54.1 [49.4, 58.9] |
| r2m_gold_test_rs | 40.4 [37.7, 43.1] | 57.4 [54.9, 59.8] | 58.3 [55.3, 61.1] | 55.4 [50.4, 60.1] |
| r2m_hybrid_k5_test_rs | 36.3 [33.6, 39.0] | 51.8 [49.3, 54.3] | 51.9 [49.0, 54.7] | 51.6 [46.8, 56.3] |

Hiệu cặp (cùng câu hỏi):

| So sánh | EM | F1 | HasAns_F1 | NoAns_acc |
|---|---|---|---|---|
| r2m_gold_test_thr − r2m_gold_test_rs | +0.0 [-0.6, +0.6] | -0.5 [-1.3, +0.2] | -1.6 [-2.6, -0.8] | +2.0 [+0.8, +3.4] |
| r2m_gold_test_thr − r2noimp_gold_test_thr | +5.6 [+3.0, +8.2] | +5.3 [+2.8, +7.7] | -2.6 [-5.3, -0.0] | +22.8 [+17.9, +27.6] |
| r2m_gold_test_thr − r2ood_gold_test_thr | -4.4 [-6.8, -1.9] | -1.2 [-3.5, +1.1] | +5.4 [+2.9, +7.9] | -15.8 [-20.7, -11.4] |
| r2m_gold_test_thr − r2m_hybrid_k5_test_thr | +3.7 [+2.5, +4.9] | +5.1 [+3.8, +6.4] | +5.9 [+4.4, +7.5] | +3.3 [+1.0, +5.7] |
