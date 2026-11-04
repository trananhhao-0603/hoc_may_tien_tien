# Kết quả đánh giá

## So sánh

| Run | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| b0_gold_dev | 1329 | 0.1 | 1.6 | 0.1 | 2.4 | 0.0 | 0.0 |
| b0_retrieved_dev | 1329 | 0.1 | 1.7 | 0.1 | 2.5 | 0.0 | 0.0 |
| b2_gold_dev | 1329 | 0.0 | 0.4 | 0.0 | 0.6 | 0.0 | 0.0 |

## b0_gold_dev

`{"commit": "6b01a5c-dirty", "time": "2026-11-04 21:30:08", "run": null, "model": "B0-random-NP/year", "split": "dev", "context": "gold", "mode": "hybrid", "seed": 13, "limit": null}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 0.1 | 1.6 | 0.1 | 2.4 | 0.0 | 0.0 |
| VN | 407 | 0.2 | 1.8 | 0.4 | 2.9 | 0.0 | 0.0 |
| TG | 922 | 0.0 | 1.6 | 0.0 | 2.3 | 0.0 | 0.0 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 0.0 | 2.1 | 0.0 | 3.2 | 0.0 | 0.0 |
| ai | 159 | 0.0 | 2.1 | 0.0 | 3.0 | 0.0 | 0.0 |
| ở đâu | 100 | 0.0 | 1.5 | 0.0 | 2.3 | 0.0 | 0.0 |
| bao nhiêu | 131 | 0.0 | 1.0 | 0.0 | 1.6 | 0.0 | 0.0 |
| vì sao | 120 | 0.0 | 0.9 | 0.0 | 1.4 | 0.0 | 0.0 |
| như thế nào | 129 | 0.0 | 0.8 | 0.0 | 1.2 | 0.0 | 0.0 |
| cái gì | 514 | 0.2 | 1.9 | 0.3 | 3.0 | 0.0 | 0.0 |
| khác | 42 | 0.0 | 1.7 | 0.0 | 1.9 | 0.0 | 0.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 2.4 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 99.8%

## b0_retrieved_dev

`{"commit": "6b01a5c-dirty", "time": "2026-11-04 21:30:56", "run": null, "model": "B0-random-NP/year", "split": "dev", "context": "retrieved", "mode": "hybrid", "seed": 13, "limit": null}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 0.1 | 1.7 | 0.1 | 2.5 | 0.0 | 0.0 |
| VN | 407 | 0.2 | 2.7 | 0.4 | 4.4 | 0.0 | 0.0 |
| TG | 922 | 0.0 | 1.3 | 0.0 | 1.8 | 0.0 | 0.0 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 0.0 | 0.9 | 0.0 | 1.4 | 0.0 | 0.0 |
| ai | 159 | 0.0 | 1.9 | 0.0 | 2.8 | 0.0 | 0.0 |
| ở đâu | 100 | 1.0 | 2.1 | 1.5 | 3.3 | 0.0 | 0.0 |
| bao nhiêu | 131 | 0.0 | 2.1 | 0.0 | 3.3 | 0.0 | 0.0 |
| vì sao | 120 | 0.0 | 1.0 | 0.0 | 1.6 | 0.0 | 0.0 |
| như thế nào | 129 | 0.0 | 1.1 | 0.0 | 1.5 | 0.0 | 0.0 |
| cái gì | 514 | 0.0 | 1.8 | 0.0 | 2.8 | 0.0 | 0.0 |
| khác | 42 | 0.0 | 2.9 | 0.0 | 3.3 | 0.0 | 0.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **71.9%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 3.0 · khi tìm sai: 1.2
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 99.8%

## b2_gold_dev

`{"commit": "6b01a5c-dirty", "time": "2026-11-04 21:37:25", "model": "VietAI/vit5-base", "split": "dev", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 8, "num_beams": 1, "limit": null, "run": "b2_gold_dev", "device": "cpu"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 0.0 | 0.4 | 0.0 | 0.6 | 0.0 | 0.0 |
| VN | 407 | 0.0 | 0.4 | 0.0 | 0.6 | 0.0 | 0.0 |
| TG | 922 | 0.0 | 0.4 | 0.0 | 0.5 | 0.0 | 0.0 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 0.0 | 0.3 | 0.0 | 0.4 | 0.0 | 0.0 |
| ai | 159 | 0.0 | 0.4 | 0.0 | 0.5 | 0.0 | 0.0 |
| ở đâu | 100 | 0.0 | 0.5 | 0.0 | 0.8 | 0.0 | 0.0 |
| bao nhiêu | 131 | 0.0 | 0.3 | 0.0 | 0.5 | 0.0 | 0.0 |
| vì sao | 120 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| như thế nào | 129 | 0.0 | 0.6 | 0.0 | 0.8 | 0.0 | 0.0 |
| cái gì | 514 | 0.0 | 0.4 | 0.0 | 0.6 | 0.0 | 0.0 |
| khác | 42 | 0.0 | 0.2 | 0.0 | 0.2 | 0.0 | 0.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 0.6 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 64.3%
