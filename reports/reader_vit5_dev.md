# Kết quả đánh giá

## So sánh

| Run | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| b1_gold_dev | 1329 | 37.4 | 51.5 | 40.6 | 61.7 | 30.9 | 20.5 |
| r1_gold_dev | 1329 | 37.4 | 51.1 | 37.0 | 57.3 | 38.2 | 27.7 |
| r1_retrieved_k3_dev | 1329 | 30.2 | 42.7 | 30.6 | 49.2 | 29.5 | 21.5 |
| r2_gold_dev | 1329 | 42.0 | 55.7 | 40.5 | 60.8 | 45.1 | 22.1 |
| r2_retrieved_k3_dev | 1329 | 38.7 | 51.5 | 36.3 | 55.5 | 43.5 | 23.1 |

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

## r1_gold_dev

`{"commit": "5f83231-zip", "time": "2026-11-08 11:08:02", "model": "models/r1_vit5", "split": "dev", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r1_gold_dev", "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 37.4 | 51.1 | 37.0 | 57.3 | 38.2 | 27.7 |
| VN | 407 | 34.6 | 49.2 | 40.5 | 64.4 | 25.6 | 16.6 |
| TG | 922 | 38.6 | 51.9 | 35.7 | 54.6 | 45.5 | 31.9 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 43.3 | 57.5 | 50.0 | 71.2 | 29.5 | 20.0 |
| ai | 159 | 49.1 | 55.1 | 55.5 | 64.3 | 34.7 | 22.7 |
| ở đâu | 100 | 44.0 | 55.2 | 44.6 | 61.8 | 42.9 | 27.7 |
| bao nhiêu | 131 | 32.8 | 48.4 | 38.4 | 62.0 | 22.2 | 16.3 |
| vì sao | 120 | 34.2 | 51.1 | 27.3 | 53.6 | 46.5 | 31.2 |
| như thế nào | 129 | 27.1 | 45.2 | 20.7 | 46.0 | 43.2 | 26.1 |
| cái gì | 514 | 36.0 | 49.7 | 33.7 | 54.8 | 40.2 | 32.5 |
| khác | 42 | 31.0 | 48.0 | 24.3 | 43.7 | 80.0 | 40.5 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 57.3 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.3%

## r1_retrieved_k3_dev

`{"commit": "5f83231-zip", "time": "2026-11-08 11:12:14", "model": "models/r1_vit5", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r1_retrieved_k3_dev", "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 30.2 | 42.7 | 30.6 | 49.2 | 29.5 | 21.5 |
| VN | 407 | 29.7 | 42.1 | 36.8 | 57.3 | 18.8 | 12.1 |
| TG | 922 | 30.5 | 43.0 | 28.2 | 46.1 | 35.7 | 25.1 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 32.1 | 47.2 | 41.1 | 63.6 | 13.6 | 10.0 |
| ai | 159 | 39.0 | 45.7 | 46.4 | 56.0 | 22.4 | 17.3 |
| ở đâu | 100 | 37.0 | 46.7 | 38.5 | 53.4 | 34.3 | 21.5 |
| bao nhiêu | 131 | 30.5 | 43.6 | 33.7 | 53.6 | 24.4 | 11.6 |
| vì sao | 120 | 25.0 | 39.0 | 20.8 | 42.6 | 32.6 | 20.8 |
| như thế nào | 129 | 20.2 | 35.6 | 16.3 | 37.9 | 29.7 | 21.7 |
| cái gì | 514 | 30.0 | 42.2 | 27.8 | 46.6 | 34.1 | 27.5 |
| khác | 42 | 23.8 | 44.1 | 18.9 | 41.9 | 60.0 | 32.4 |

- Đoạn đúng nằm trong các đoạn đã đọc: **89.3%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 54.1 · khi tìm sai: 8.1
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.0%

## r2_gold_dev

`{"commit": "69dc93b-dirty", "time": "2026-11-08 22:23:37", "model": "models/r2_vit5", "split": "dev", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2_gold_dev", "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 42.0 | 55.7 | 40.5 | 60.8 | 45.1 | 22.1 |
| VN | 407 | 41.3 | 54.7 | 48.6 | 70.7 | 30.0 | 8.9 |
| TG | 922 | 42.3 | 56.1 | 37.4 | 57.1 | 53.8 | 27.1 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 50.7 | 64.7 | 57.8 | 78.6 | 36.4 | 11.1 |
| ai | 159 | 51.6 | 57.6 | 59.1 | 67.8 | 34.7 | 20.0 |
| ở đâu | 100 | 45.0 | 53.5 | 50.8 | 63.8 | 34.3 | 24.6 |
| bao nhiêu | 131 | 42.0 | 56.0 | 41.9 | 63.2 | 42.2 | 15.1 |
| vì sao | 120 | 35.8 | 54.6 | 27.3 | 56.5 | 51.2 | 26.0 |
| như thế nào | 129 | 29.5 | 46.3 | 23.9 | 47.6 | 43.2 | 23.9 |
| cái gì | 514 | 42.2 | 56.6 | 37.3 | 59.4 | 51.4 | 24.8 |
| khác | 42 | 23.8 | 43.6 | 18.9 | 41.4 | 60.0 | 29.7 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 60.8 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.1%

## r2_retrieved_k3_dev

`{"commit": "69dc93b-dirty", "time": "2026-11-08 22:24:48", "model": "models/r2_vit5", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2_retrieved_k3_dev", "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 38.7 | 51.5 | 36.3 | 55.5 | 43.5 | 23.1 |
| VN | 407 | 38.1 | 51.0 | 44.5 | 65.9 | 28.1 | 8.1 |
| TG | 922 | 38.9 | 51.8 | 33.2 | 51.5 | 52.3 | 28.8 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 45.5 | 59.8 | 53.3 | 74.5 | 29.5 | 13.3 |
| ai | 159 | 47.2 | 53.5 | 52.7 | 61.9 | 34.7 | 23.6 |
| ở đâu | 100 | 43.0 | 51.3 | 46.2 | 58.9 | 37.1 | 26.2 |
| bao nhiêu | 131 | 39.7 | 53.7 | 38.4 | 59.8 | 42.2 | 15.1 |
| vì sao | 120 | 30.0 | 48.5 | 20.8 | 49.7 | 46.5 | 23.4 |
| như thế nào | 129 | 27.9 | 43.0 | 22.8 | 44.0 | 40.5 | 23.9 |
| cái gì | 514 | 39.1 | 52.1 | 33.1 | 53.0 | 50.3 | 25.7 |
| khác | 42 | 23.8 | 39.6 | 18.9 | 36.9 | 60.0 | 32.4 |

- Đoạn đúng nằm trong các đoạn đã đọc: **89.3%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 61.5 · khi tìm sai: 4.6
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.3%
