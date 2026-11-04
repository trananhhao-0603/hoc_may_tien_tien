# Kết quả đánh giá

## So sánh

| Run | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| b0_gold_dev | 1329 | 0.1 | 1.6 | 0.1 | 2.4 | 0.0 | 0.0 |
| b0_retrieved_dev | 1329 | 0.1 | 1.7 | 0.1 | 2.5 | 0.0 | 0.0 |
| b1_gold_dev | 1329 | 37.4 | 51.5 | 40.6 | 61.7 | 30.9 | 20.5 |
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

## b1_gold_dev

`{"commit": "", "time": "2026-11-04 15:44:56", "config": {"model": "xlm-roberta-base", "output_dir": "models/b1_xlmr", "max_length": 384, "doc_stride": 128, "max_answer_length": 100, "n_best": 20, "lr": 3e-05, "epochs": 3, "batch_size": 16, "grad_accum": 2, "warmup_ratio": 0.1, "weight_decay": 0.01, "seed": 42, "bf16": true, "null_threshold": 0.0}, "predict_only": null, "split": "dev", "context": "gold", "mode": "hybrid", "k": 1, "tune_threshold": true, "threshold": null, "max_train": null, "max_eval": null, "epochs": null, "run": "b1_gold_dev", "model": "xlm-roberta-base", "checkpoint": "/content/HMTT/models/b1_xlmr", "null_threshold": -0.10359999999999979}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 37.4 | 51.5 | 40.6 | 61.7 | 30.9 | 20.5 |
| VN | 407 | 37.6 | 51.4 | 41.7 | 64.4 | 31.2 | 16.2 |
| TG | 922 | 37.3 | 51.6 | 40.2 | 60.6 | 30.7 | 22.2 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 47.8 | 58.2 | 65.6 | 81.1 | 11.4 | 7.8 |
| ai | 159 | 47.2 | 53.2 | 57.3 | 66.1 | 24.5 | 15.5 |
| ở đâu | 100 | 38.0 | 48.5 | 46.2 | 62.3 | 22.9 | 23.1 |
| bao nhiêu | 131 | 35.1 | 50.2 | 43.0 | 66.1 | 20.0 | 12.8 |
| vì sao | 120 | 30.8 | 48.5 | 32.5 | 60.1 | 27.9 | 20.8 |
| như thế nào | 129 | 26.4 | 49.3 | 21.7 | 53.9 | 37.8 | 20.7 |
| cái gì | 514 | 37.4 | 51.9 | 35.8 | 58.1 | 40.2 | 25.7 |
| khác | 42 | 26.2 | 47.1 | 21.6 | 45.3 | 60.0 | 32.4 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 61.7 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 100.0%

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
