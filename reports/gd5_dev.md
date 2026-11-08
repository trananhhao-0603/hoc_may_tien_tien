# Kết quả GĐ5 — dev

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

## r2m_bm25_k1_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:30:28", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "bm25", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_bm25_k1_dev_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_bm25_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 40.9 | 52.0 | 31.7 | 48.4 | 59.5 | 34.5 |
| VN | 407 | 45.2 | 57.2 | 44.9 | 64.7 | 45.6 | 16.6 |
| TG | 922 | 38.9 | 49.8 | 26.7 | 42.1 | 67.5 | 41.4 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 44.8 | 57.7 | 41.1 | 60.4 | 52.3 | 27.8 |
| ai | 159 | 47.8 | 52.9 | 45.5 | 52.8 | 53.1 | 28.2 |
| ở đâu | 100 | 42.0 | 48.1 | 36.9 | 46.3 | 51.4 | 40.0 |
| bao nhiêu | 131 | 43.5 | 56.4 | 33.7 | 53.4 | 62.2 | 26.7 |
| vì sao | 120 | 40.0 | 53.8 | 23.4 | 44.8 | 69.8 | 32.5 |
| như thế nào | 129 | 26.4 | 40.5 | 17.4 | 37.2 | 48.6 | 37.0 |
| cái gì | 514 | 41.4 | 53.1 | 29.9 | 47.7 | 63.1 | 38.5 |
| khác | 42 | 31.0 | 44.0 | 24.3 | 39.1 | 80.0 | 40.5 |

- Đoạn đúng nằm trong các đoạn đã đọc: **76.1%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 62.5 · khi tìm sai: 3.5
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.3%

## r2m_bm25_k3_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:30:28", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "bm25", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_bm25_k3_dev_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_bm25_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 40.9 | 53.2 | 34.9 | 53.1 | 53.3 | 25.8 |
| VN | 407 | 44.0 | 57.3 | 44.9 | 67.0 | 42.5 | 9.3 |
| TG | 922 | 39.6 | 51.3 | 31.0 | 47.8 | 59.6 | 32.1 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 43.3 | 59.9 | 42.2 | 67.0 | 45.5 | 15.6 |
| ai | 159 | 49.7 | 55.0 | 50.9 | 58.5 | 46.9 | 20.9 |
| ở đâu | 100 | 45.0 | 52.3 | 44.6 | 55.9 | 45.7 | 27.7 |
| bao nhiêu | 131 | 45.0 | 58.8 | 37.2 | 58.1 | 60.0 | 17.4 |
| vì sao | 120 | 38.3 | 52.2 | 27.3 | 49.0 | 58.1 | 27.3 |
| như thế nào | 129 | 28.7 | 43.4 | 20.7 | 41.3 | 48.6 | 29.3 |
| cái gì | 514 | 40.5 | 53.1 | 32.2 | 51.6 | 55.9 | 29.9 |
| khác | 42 | 28.6 | 42.9 | 21.6 | 37.9 | 80.0 | 32.4 |

- Đoạn đúng nằm trong các đoạn đã đọc: **86.5%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 60.5 · khi tìm sai: 5.4
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.0%

## r2m_bm25_k5_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:30:28", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "bm25", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_bm25_k5_dev_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 40.9 | 53.2 | 36.0 | 54.4 | 50.8 | 23.8 |
| VN | 407 | 43.7 | 57.4 | 46.2 | 68.6 | 40.0 | 7.7 |
| TG | 922 | 39.6 | 51.4 | 32.1 | 48.9 | 57.0 | 29.9 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 43.3 | 59.2 | 43.3 | 67.1 | 43.2 | 15.6 |
| ai | 159 | 50.9 | 55.8 | 52.7 | 59.7 | 46.9 | 19.1 |
| ở đâu | 100 | 45.0 | 52.4 | 46.2 | 57.6 | 42.9 | 21.5 |
| bao nhiêu | 131 | 45.0 | 58.7 | 39.5 | 60.4 | 55.6 | 17.4 |
| vì sao | 120 | 36.7 | 51.2 | 27.3 | 50.0 | 53.5 | 26.0 |
| như thế nào | 129 | 27.9 | 42.7 | 20.7 | 41.4 | 45.9 | 28.3 |
| cái gì | 514 | 40.5 | 53.5 | 33.4 | 53.4 | 53.6 | 27.2 |
| khác | 42 | 28.6 | 43.0 | 21.6 | 38.0 | 80.0 | 29.7 |

- Đoạn đúng nằm trong các đoạn đã đọc: **90.4%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 59.7 · khi tìm sai: 4.4
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.2%

## r2m_dense_k1_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:35:02", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "dense", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_dense_k1_dev_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_dense_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 38.0 | 45.5 | 21.5 | 32.8 | 71.6 | 53.6 |
| VN | 407 | 43.2 | 52.4 | 33.6 | 48.6 | 58.1 | 33.2 |
| TG | 922 | 35.7 | 42.5 | 16.9 | 26.7 | 79.4 | 61.4 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 40.3 | 50.5 | 30.0 | 45.2 | 61.4 | 44.4 |
| ai | 159 | 37.1 | 40.6 | 23.6 | 28.7 | 67.3 | 58.2 |
| ở đâu | 100 | 38.0 | 40.9 | 23.1 | 27.5 | 65.7 | 61.5 |
| bao nhiêu | 131 | 44.3 | 53.8 | 32.6 | 47.0 | 66.7 | 33.7 |
| vì sao | 120 | 39.2 | 51.0 | 18.2 | 36.6 | 76.7 | 49.4 |
| như thế nào | 129 | 27.9 | 38.5 | 10.9 | 25.7 | 70.3 | 51.1 |
| cái gì | 514 | 39.9 | 46.6 | 20.3 | 30.5 | 76.5 | 58.5 |
| khác | 42 | 19.0 | 27.4 | 10.8 | 20.3 | 80.0 | 64.9 |

- Đoạn đúng nằm trong các đoạn đã đọc: **52.2%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 61.2 · khi tìm sai: 1.6
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.4%

## r2m_dense_k3_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:35:02", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "dense", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_dense_k3_dev_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_dense_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 38.6 | 48.0 | 27.1 | 41.1 | 62.0 | 41.1 |
| VN | 407 | 42.8 | 53.9 | 38.9 | 57.2 | 48.8 | 20.2 |
| TG | 922 | 36.8 | 45.4 | 22.6 | 34.9 | 69.7 | 49.1 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 41.0 | 52.2 | 33.3 | 50.0 | 56.8 | 37.8 |
| ai | 159 | 42.1 | 46.1 | 35.5 | 41.1 | 57.1 | 40.9 |
| ở đâu | 100 | 36.0 | 42.1 | 29.2 | 38.6 | 48.6 | 46.2 |
| bao nhiêu | 131 | 44.3 | 56.7 | 36.0 | 54.9 | 60.0 | 27.9 |
| vì sao | 120 | 40.0 | 51.8 | 22.1 | 40.5 | 72.1 | 36.4 |
| như thế nào | 129 | 28.7 | 41.0 | 17.4 | 34.7 | 56.8 | 37.0 |
| cái gì | 514 | 39.3 | 48.3 | 24.8 | 38.6 | 66.5 | 46.6 |
| khác | 42 | 23.8 | 35.1 | 18.9 | 31.7 | 60.0 | 43.2 |

- Đoạn đúng nằm trong các đoạn đã đọc: **67.5%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 60.0 · khi tìm sai: 1.9
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.0%

## r2m_dense_k5_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:35:02", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "dense", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_dense_k5_dev_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 38.3 | 48.5 | 28.6 | 43.7 | 58.1 | 36.8 |
| VN | 407 | 41.0 | 52.3 | 39.7 | 58.3 | 43.1 | 18.2 |
| TG | 922 | 37.1 | 46.8 | 24.3 | 38.2 | 66.8 | 43.9 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 40.3 | 52.7 | 35.6 | 54.0 | 50.0 | 33.3 |
| ai | 159 | 45.3 | 49.0 | 40.9 | 46.3 | 55.1 | 34.5 |
| ở đâu | 100 | 37.0 | 43.7 | 30.8 | 41.0 | 48.6 | 41.5 |
| bao nhiêu | 131 | 42.7 | 56.2 | 36.0 | 56.6 | 55.6 | 25.6 |
| vì sao | 120 | 38.3 | 50.3 | 22.1 | 40.7 | 67.4 | 32.5 |
| như thế nào | 129 | 27.1 | 40.8 | 16.3 | 35.4 | 54.1 | 33.7 |
| cái gì | 514 | 38.5 | 48.5 | 26.0 | 41.2 | 62.0 | 42.4 |
| khác | 42 | 26.2 | 38.9 | 21.6 | 36.0 | 60.0 | 35.1 |

- Đoạn đúng nằm trong các đoạn đã đọc: **73.7%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 58.5 · khi tìm sai: 2.3
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.0%

## r2m_gold_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:21:08", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_gold_dev_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 44.1 | 57.5 | 39.2 | 59.2 | 54.0 | 23.0 |
| VN | 407 | 46.2 | 60.1 | 49.0 | 71.8 | 41.9 | 9.3 |
| TG | 922 | 43.2 | 56.4 | 35.5 | 54.4 | 61.0 | 28.2 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 51.5 | 66.9 | 53.3 | 76.2 | 47.7 | 12.2 |
| ai | 159 | 51.6 | 57.0 | 54.5 | 62.4 | 44.9 | 16.4 |
| ở đâu | 100 | 46.0 | 54.6 | 49.2 | 62.4 | 40.0 | 23.1 |
| bao nhiêu | 131 | 45.0 | 59.5 | 40.7 | 62.8 | 53.3 | 17.4 |
| vì sao | 120 | 41.7 | 58.3 | 28.6 | 54.4 | 65.1 | 27.3 |
| như thế nào | 129 | 30.2 | 47.1 | 22.8 | 46.4 | 48.6 | 26.1 |
| cái gì | 514 | 44.4 | 58.5 | 36.7 | 58.4 | 58.7 | 27.2 |
| khác | 42 | 31.0 | 48.3 | 24.3 | 44.0 | 80.0 | 27.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 59.2 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.3%

## r2m_hybrid_k1_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:25:49", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_hybrid_k1_dev_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_hybrid_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 40.5 | 50.8 | 29.8 | 45.2 | 62.2 | 38.0 |
| VN | 407 | 45.0 | 56.5 | 42.9 | 61.9 | 48.1 | 17.8 |
| TG | 922 | 38.5 | 48.3 | 24.8 | 38.8 | 70.4 | 45.7 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 43.3 | 56.5 | 37.8 | 57.5 | 54.5 | 31.1 |
| ai | 159 | 46.5 | 51.6 | 42.7 | 50.0 | 55.1 | 33.6 |
| ở đâu | 100 | 42.0 | 46.5 | 33.8 | 40.7 | 57.1 | 49.2 |
| bao nhiêu | 131 | 44.3 | 56.0 | 34.9 | 52.7 | 62.2 | 27.9 |
| vì sao | 120 | 40.8 | 52.5 | 22.1 | 40.2 | 74.4 | 37.7 |
| như thế nào | 129 | 26.4 | 39.1 | 15.2 | 33.2 | 54.1 | 39.1 |
| cái gì | 514 | 40.9 | 51.7 | 27.8 | 44.5 | 65.4 | 41.2 |
| khác | 42 | 31.0 | 43.0 | 24.3 | 38.0 | 80.0 | 40.5 |

- Đoạn đúng nằm trong các đoạn đã đọc: **71.9%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 61.6 · khi tìm sai: 3.3
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.2%

## r2m_hybrid_k3_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:25:49", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_hybrid_k3_dev_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_hybrid_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 41.2 | 53.6 | 35.5 | 54.0 | 52.9 | 24.4 |
| VN | 407 | 44.0 | 57.4 | 46.2 | 68.3 | 40.6 | 7.3 |
| TG | 922 | 40.0 | 52.0 | 31.5 | 48.6 | 59.9 | 31.0 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 43.3 | 59.2 | 43.3 | 67.1 | 43.2 | 15.6 |
| ai | 159 | 49.1 | 54.5 | 50.0 | 57.9 | 46.9 | 20.0 |
| ở đâu | 100 | 44.0 | 51.5 | 44.6 | 56.2 | 42.9 | 24.6 |
| bao nhiêu | 131 | 45.0 | 58.7 | 39.5 | 60.3 | 55.6 | 17.4 |
| vì sao | 120 | 39.2 | 53.7 | 26.0 | 48.7 | 62.8 | 27.3 |
| như thế nào | 129 | 27.9 | 43.5 | 20.7 | 42.5 | 45.9 | 27.2 |
| cái gì | 514 | 41.6 | 54.4 | 33.7 | 53.4 | 56.4 | 27.8 |
| khác | 42 | 28.6 | 42.9 | 21.6 | 37.9 | 80.0 | 32.4 |

- Đoạn đúng nằm trong các đoạn đã đọc: **89.3%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 59.9 · khi tìm sai: 4.5
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.4%

## r2m_hybrid_k5_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:25:49", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_hybrid_k5_dev_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 40.9 | 53.7 | 36.4 | 55.4 | 50.1 | 22.1 |
| VN | 407 | 43.7 | 57.0 | 45.7 | 67.7 | 40.6 | 6.5 |
| TG | 922 | 39.7 | 52.2 | 32.9 | 50.7 | 55.6 | 28.1 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 43.3 | 60.1 | 43.3 | 68.3 | 43.2 | 13.3 |
| ai | 159 | 49.7 | 54.9 | 51.8 | 59.3 | 44.9 | 17.3 |
| ở đâu | 100 | 45.0 | 53.5 | 47.7 | 60.8 | 40.0 | 20.0 |
| bao nhiêu | 131 | 43.5 | 56.8 | 39.5 | 59.8 | 51.1 | 17.4 |
| vì sao | 120 | 35.8 | 49.7 | 24.7 | 46.3 | 55.8 | 26.0 |
| như thế nào | 129 | 27.9 | 44.4 | 20.7 | 43.8 | 45.9 | 23.9 |
| cái gì | 514 | 41.6 | 54.9 | 35.2 | 55.6 | 53.6 | 25.1 |
| khác | 42 | 28.6 | 42.9 | 21.6 | 37.9 | 80.0 | 32.4 |

- Đoạn đúng nằm trong các đoạn đã đọc: **93.4%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 58.9 · khi tìm sai: 5.9
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.2%

## r2noimp_gold_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 01:08:14", "model": "models/r2_noimp", "split": "dev", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2noimp_gold_dev_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 36.0 | 50.6 | 40.5 | 62.2 | 27.0 | 18.0 |
| VN | 407 | 32.7 | 48.2 | 44.1 | 69.7 | 15.0 | 8.9 |
| TG | 922 | 37.5 | 51.7 | 39.1 | 59.3 | 33.9 | 21.6 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 43.3 | 57.2 | 56.7 | 77.4 | 15.9 | 11.1 |
| ai | 159 | 47.8 | 53.7 | 55.5 | 64.0 | 30.6 | 17.3 |
| ở đâu | 100 | 36.0 | 49.5 | 44.6 | 65.4 | 20.0 | 10.8 |
| bao nhiêu | 131 | 36.6 | 52.7 | 43.0 | 67.5 | 24.4 | 5.8 |
| vì sao | 120 | 30.0 | 50.7 | 32.5 | 64.8 | 25.6 | 10.4 |
| như thế nào | 129 | 24.8 | 41.7 | 20.7 | 44.3 | 35.1 | 29.3 |
| cái gì | 514 | 35.4 | 49.8 | 38.5 | 60.5 | 29.6 | 23.3 |
| khác | 42 | 26.2 | 51.6 | 27.0 | 55.9 | 20.0 | 18.9 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 62.2 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.3%

## r2noimp_hybrid_k1_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 01:12:19", "model": "models/r2_noimp", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2noimp_hybrid_k1_dev_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2noimp_hybrid_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 34.5 | 45.7 | 30.9 | 47.6 | 41.9 | 34.0 |
| VN | 407 | 33.7 | 47.0 | 39.7 | 61.7 | 24.4 | 16.6 |
| TG | 922 | 34.9 | 45.1 | 27.6 | 42.2 | 52.0 | 40.6 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 40.3 | 50.7 | 44.4 | 59.9 | 31.8 | 31.1 |
| ai | 159 | 41.5 | 45.9 | 40.9 | 47.3 | 42.9 | 37.3 |
| ở đâu | 100 | 37.0 | 43.8 | 32.3 | 42.8 | 45.7 | 44.6 |
| bao nhiêu | 131 | 35.9 | 47.7 | 36.0 | 54.1 | 35.6 | 18.6 |
| vì sao | 120 | 30.0 | 46.0 | 22.1 | 47.0 | 44.2 | 26.0 |
| như thế nào | 129 | 21.7 | 35.2 | 14.1 | 33.1 | 40.5 | 43.5 |
| cái gì | 514 | 35.0 | 46.6 | 29.9 | 47.6 | 44.7 | 35.5 |
| khác | 42 | 26.2 | 47.5 | 24.3 | 48.5 | 40.0 | 27.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **71.9%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 64.6 · khi tìm sai: 4.1
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.0%

## r2noimp_hybrid_k3_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 01:12:19", "model": "models/r2_noimp", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2noimp_hybrid_k3_dev_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2noimp_hybrid_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 33.1 | 46.6 | 35.3 | 55.4 | 28.6 | 20.2 |
| VN | 407 | 30.5 | 44.6 | 40.5 | 63.8 | 15.0 | 8.1 |
| TG | 922 | 34.3 | 47.5 | 33.3 | 52.2 | 36.5 | 24.8 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 38.8 | 52.5 | 50.0 | 70.4 | 15.9 | 13.3 |
| ai | 159 | 43.4 | 49.6 | 47.3 | 56.3 | 34.7 | 20.9 |
| ở đâu | 100 | 33.0 | 43.6 | 38.5 | 54.7 | 22.9 | 18.5 |
| bao nhiêu | 131 | 35.1 | 49.1 | 40.7 | 62.0 | 24.4 | 7.0 |
| vì sao | 120 | 27.5 | 47.2 | 27.3 | 58.0 | 27.9 | 11.7 |
| như thế nào | 129 | 21.7 | 37.7 | 18.5 | 41.0 | 29.7 | 30.4 |
| cái gì | 514 | 32.7 | 45.7 | 33.1 | 53.1 | 31.8 | 24.8 |
| khác | 42 | 26.2 | 51.4 | 24.3 | 52.9 | 40.0 | 18.9 |

- Đoạn đúng nằm trong các đoạn đã đọc: **89.3%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 61.5 · khi tìm sai: 4.3
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.5%

## r2noimp_hybrid_k5_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 01:12:19", "model": "models/r2_noimp", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2noimp_hybrid_k5_dev_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 32.7 | 46.4 | 35.8 | 56.3 | 26.3 | 18.2 |
| VN | 407 | 29.2 | 43.8 | 39.3 | 63.3 | 13.8 | 7.3 |
| TG | 922 | 34.2 | 47.6 | 34.4 | 53.6 | 33.6 | 22.3 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 37.3 | 51.5 | 48.9 | 70.0 | 13.6 | 12.2 |
| ai | 159 | 44.0 | 49.9 | 49.1 | 57.6 | 32.7 | 17.3 |
| ở đâu | 100 | 34.0 | 45.3 | 43.1 | 60.4 | 17.1 | 13.8 |
| bao nhiêu | 131 | 33.6 | 47.2 | 39.5 | 60.2 | 22.2 | 7.0 |
| vì sao | 120 | 25.8 | 46.0 | 26.0 | 57.4 | 25.6 | 10.4 |
| như thế nào | 129 | 21.7 | 38.2 | 18.5 | 41.5 | 29.7 | 28.3 |
| cái gì | 514 | 32.5 | 46.1 | 33.7 | 54.7 | 30.2 | 22.7 |
| khác | 42 | 23.8 | 47.8 | 24.3 | 51.6 | 20.0 | 18.9 |

- Đoạn đúng nằm trong các đoạn đã đọc: **93.4%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 59.9 · khi tìm sai: 4.9
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.7%

## r2ood_gold_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 02:44:55", "model": "models/r2_ood", "split": "dev", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2ood_gold_dev_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 44.2 | 58.9 | 41.5 | 63.4 | 49.9 | 18.6 |
| VN | 407 | 42.8 | 58.2 | 46.6 | 72.1 | 36.9 | 8.5 |
| TG | 922 | 44.9 | 59.2 | 39.5 | 60.0 | 57.4 | 22.5 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 54.5 | 68.1 | 56.7 | 76.9 | 50.0 | 14.4 |
| ai | 159 | 56.6 | 62.8 | 60.9 | 69.9 | 46.9 | 10.9 |
| ở đâu | 100 | 39.0 | 50.0 | 44.6 | 61.5 | 28.6 | 15.4 |
| bao nhiêu | 131 | 40.5 | 58.2 | 37.2 | 64.3 | 46.7 | 14.0 |
| vì sao | 120 | 36.7 | 53.7 | 27.3 | 53.8 | 53.5 | 23.4 |
| như thế nào | 129 | 34.1 | 52.8 | 26.1 | 52.3 | 54.1 | 21.7 |
| cái gì | 514 | 45.1 | 60.7 | 40.3 | 64.2 | 54.2 | 21.8 |
| khác | 42 | 31.0 | 50.4 | 29.7 | 51.8 | 40.0 | 21.6 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 63.4 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.5%

## r2ood_hybrid_k1_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 02:49:37", "model": "models/r2_ood", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2ood_hybrid_k1_dev_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2ood_hybrid_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 40.6 | 51.7 | 32.1 | 48.6 | 58.1 | 33.5 |
| VN | 407 | 43.2 | 56.0 | 42.5 | 63.5 | 44.4 | 17.0 |
| TG | 922 | 39.5 | 49.8 | 28.1 | 42.9 | 66.1 | 39.8 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 44.8 | 54.3 | 44.4 | 58.6 | 45.5 | 32.2 |
| ai | 159 | 49.7 | 54.5 | 46.4 | 53.3 | 57.1 | 30.0 |
| ở đâu | 100 | 37.0 | 42.9 | 33.8 | 43.0 | 42.9 | 40.0 |
| bao nhiêu | 131 | 41.2 | 54.5 | 33.7 | 53.9 | 55.6 | 25.6 |
| vì sao | 120 | 35.0 | 49.7 | 18.2 | 41.0 | 65.1 | 29.9 |
| như thế nào | 129 | 29.5 | 43.7 | 18.5 | 38.4 | 56.8 | 37.0 |
| cái gì | 514 | 42.4 | 54.5 | 30.7 | 49.3 | 64.2 | 35.5 |
| khác | 42 | 28.6 | 41.7 | 27.0 | 41.9 | 40.0 | 35.1 |

- Đoạn đúng nằm trong các đoạn đã đọc: **71.9%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 65.8 · khi tìm sai: 4.6
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.2%

## r2ood_hybrid_k3_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 02:49:37", "model": "models/r2_ood", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2ood_hybrid_k3_dev_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2ood_hybrid_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 40.0 | 53.6 | 36.3 | 56.6 | 47.6 | 20.7 |
| VN | 407 | 40.0 | 54.8 | 42.9 | 67.3 | 35.6 | 7.7 |
| TG | 922 | 40.0 | 53.1 | 33.8 | 52.5 | 54.5 | 25.7 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 46.3 | 59.4 | 48.9 | 68.4 | 40.9 | 17.8 |
| ai | 159 | 51.6 | 57.5 | 53.6 | 62.1 | 46.9 | 17.3 |
| ở đâu | 100 | 35.0 | 44.7 | 36.9 | 51.9 | 31.4 | 20.0 |
| bao nhiêu | 131 | 37.4 | 54.0 | 34.9 | 60.2 | 42.2 | 15.1 |
| vì sao | 120 | 35.0 | 50.7 | 23.4 | 47.9 | 55.8 | 22.1 |
| như thế nào | 129 | 30.2 | 47.1 | 22.8 | 46.5 | 48.6 | 25.0 |
| cái gì | 514 | 41.1 | 55.5 | 35.2 | 57.3 | 52.0 | 22.4 |
| khác | 42 | 28.6 | 47.1 | 27.0 | 48.1 | 40.0 | 24.3 |

- Đoạn đúng nằm trong các đoạn đã đọc: **89.3%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 62.9 · khi tìm sai: 3.8
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.1%

## r2ood_hybrid_k5_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 02:49:37", "model": "models/r2_ood", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2ood_hybrid_k5_dev_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 39.4 | 52.9 | 37.2 | 57.3 | 43.9 | 18.4 |
| VN | 407 | 38.3 | 53.0 | 42.1 | 66.3 | 32.5 | 6.9 |
| TG | 922 | 39.9 | 52.9 | 35.3 | 53.9 | 50.5 | 22.8 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 46.3 | 60.1 | 48.9 | 69.5 | 40.9 | 16.7 |
| ai | 159 | 51.6 | 56.9 | 55.5 | 63.1 | 42.9 | 13.6 |
| ở đâu | 100 | 34.0 | 43.7 | 40.0 | 55.0 | 22.9 | 16.9 |
| bao nhiêu | 131 | 36.6 | 52.6 | 34.9 | 59.2 | 40.0 | 15.1 |
| vì sao | 120 | 33.3 | 48.6 | 22.1 | 45.9 | 53.5 | 20.8 |
| như thế nào | 129 | 31.0 | 47.2 | 23.9 | 46.6 | 48.6 | 22.8 |
| cái gì | 514 | 40.1 | 54.7 | 36.4 | 58.9 | 46.9 | 19.4 |
| khác | 42 | 28.6 | 46.0 | 27.0 | 46.8 | 40.0 | 21.6 |

- Đoạn đúng nằm trong các đoạn đã đọc: **93.4%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 61.1 · khi tìm sai: 4.6
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.5%

## r2s13_gold_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 03:51:53", "model": "models/r2_s13", "split": "dev", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s13_gold_dev_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 41.7 | 54.9 | 36.1 | 55.8 | 53.1 | 26.8 |
| VN | 407 | 44.5 | 58.0 | 44.5 | 66.8 | 44.4 | 14.6 |
| TG | 922 | 40.5 | 53.5 | 32.9 | 51.6 | 58.1 | 31.5 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 45.5 | 60.3 | 46.7 | 68.7 | 43.2 | 20.0 |
| ai | 159 | 50.3 | 56.1 | 52.7 | 61.1 | 44.9 | 22.7 |
| ở đâu | 100 | 38.0 | 50.7 | 41.5 | 61.0 | 31.4 | 20.0 |
| bao nhiêu | 131 | 41.2 | 54.7 | 40.7 | 61.2 | 42.2 | 14.0 |
| vì sao | 120 | 39.2 | 55.4 | 26.0 | 51.3 | 62.8 | 31.2 |
| như thế nào | 129 | 31.0 | 46.2 | 18.5 | 39.7 | 62.2 | 37.0 |
| cái gì | 514 | 43.0 | 56.6 | 33.7 | 54.7 | 60.3 | 30.1 |
| khác | 42 | 31.0 | 48.2 | 27.0 | 46.6 | 60.0 | 32.4 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 55.8 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.3%

## r2s13_hybrid_k1_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 03:56:23", "model": "models/r2_s13", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s13_hybrid_k1_dev_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2s13_hybrid_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 39.4 | 49.4 | 28.5 | 43.5 | 61.6 | 40.1 |
| VN | 407 | 43.7 | 55.4 | 40.5 | 59.6 | 48.8 | 22.3 |
| TG | 922 | 37.4 | 46.8 | 23.9 | 37.3 | 69.0 | 47.0 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 38.1 | 49.9 | 35.6 | 53.1 | 43.2 | 37.8 |
| ai | 159 | 47.2 | 51.1 | 41.8 | 47.5 | 59.2 | 40.0 |
| ở đâu | 100 | 37.0 | 45.6 | 29.2 | 42.5 | 51.4 | 44.6 |
| bao nhiêu | 131 | 38.9 | 49.6 | 33.7 | 49.9 | 48.9 | 23.3 |
| vì sao | 120 | 38.3 | 52.4 | 19.5 | 41.4 | 72.1 | 39.0 |
| như thế nào | 129 | 27.9 | 39.0 | 13.0 | 28.5 | 64.9 | 48.9 |
| cái gì | 514 | 41.8 | 52.3 | 27.5 | 43.6 | 68.7 | 42.1 |
| khác | 42 | 28.6 | 39.1 | 24.3 | 36.3 | 60.0 | 40.5 |

- Đoạn đúng nằm trong các đoạn đã đọc: **71.9%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 59.3 · khi tìm sai: 3.3
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.7%

## r2s13_hybrid_k3_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 03:56:23", "model": "models/r2_s13", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s13_hybrid_k3_dev_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2s13_hybrid_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 39.2 | 51.3 | 33.4 | 51.5 | 51.0 | 27.6 |
| VN | 407 | 42.3 | 54.9 | 43.3 | 64.1 | 40.6 | 13.0 |
| TG | 922 | 37.9 | 49.8 | 29.6 | 46.7 | 57.0 | 33.2 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 39.6 | 53.5 | 42.2 | 63.0 | 34.1 | 24.4 |
| ai | 159 | 47.8 | 52.8 | 47.3 | 54.5 | 49.0 | 25.5 |
| ở đâu | 100 | 38.0 | 49.2 | 38.5 | 55.8 | 37.1 | 21.5 |
| bao nhiêu | 131 | 38.9 | 52.8 | 38.4 | 59.4 | 40.0 | 14.0 |
| vì sao | 120 | 36.7 | 52.7 | 24.7 | 49.6 | 58.1 | 28.6 |
| như thế nào | 129 | 30.2 | 43.6 | 18.5 | 37.3 | 59.5 | 38.0 |
| cái gì | 514 | 40.7 | 52.8 | 31.6 | 50.3 | 57.5 | 30.1 |
| khác | 42 | 26.2 | 40.7 | 21.6 | 38.1 | 60.0 | 32.4 |

- Đoạn đúng nằm trong các đoạn đã đọc: **89.3%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 57.1 · khi tìm sai: 4.8
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.1%

## r2s13_hybrid_k5_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 03:56:23", "model": "models/r2_s13", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s13_hybrid_k5_dev_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 39.2 | 51.5 | 34.5 | 52.9 | 48.7 | 25.4 |
| VN | 407 | 41.8 | 54.4 | 42.5 | 63.3 | 40.6 | 11.3 |
| TG | 922 | 38.1 | 50.2 | 31.5 | 48.9 | 53.4 | 30.9 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 38.8 | 53.6 | 42.2 | 64.2 | 31.8 | 22.2 |
| ai | 159 | 49.1 | 53.4 | 50.0 | 56.3 | 46.9 | 22.7 |
| ở đâu | 100 | 39.0 | 50.7 | 43.1 | 61.1 | 31.4 | 16.9 |
| bao nhiêu | 131 | 38.2 | 51.3 | 38.4 | 58.4 | 37.8 | 14.0 |
| vì sao | 120 | 35.8 | 51.3 | 23.4 | 47.4 | 58.1 | 27.3 |
| như thế nào | 129 | 30.2 | 44.6 | 18.5 | 38.7 | 59.5 | 35.9 |
| cái gì | 514 | 40.7 | 53.2 | 33.1 | 52.4 | 54.7 | 27.8 |
| khác | 42 | 26.2 | 40.7 | 21.6 | 38.1 | 60.0 | 32.4 |

- Đoạn đúng nằm trong các đoạn đã đọc: **93.4%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 56.3 · khi tìm sai: 4.6
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.1%

## r2s7_gold_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 04:58:44", "model": "models/r2_s7", "split": "dev", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s7_gold_dev_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 42.4 | 55.8 | 38.5 | 58.3 | 50.6 | 24.0 |
| VN | 407 | 44.2 | 57.1 | 46.6 | 67.7 | 40.6 | 14.2 |
| TG | 922 | 41.6 | 55.2 | 35.3 | 54.7 | 56.3 | 27.8 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 48.5 | 62.8 | 53.3 | 74.6 | 38.6 | 15.6 |
| ai | 159 | 54.7 | 60.6 | 56.4 | 64.9 | 51.0 | 17.3 |
| ở đâu | 100 | 40.0 | 49.6 | 43.1 | 57.9 | 34.3 | 26.2 |
| bao nhiêu | 131 | 42.7 | 57.8 | 43.0 | 65.9 | 42.2 | 11.6 |
| vì sao | 120 | 38.3 | 56.5 | 27.3 | 55.6 | 58.1 | 24.7 |
| như thế nào | 129 | 28.7 | 45.4 | 18.5 | 41.9 | 54.1 | 32.6 |
| cái gì | 514 | 43.0 | 56.3 | 35.8 | 56.3 | 56.4 | 28.4 |
| khác | 42 | 28.6 | 46.3 | 27.0 | 47.2 | 40.0 | 27.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 58.3 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.9%

## r2s7_hybrid_k1_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:03:29", "model": "models/r2_s7", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s7_hybrid_k1_dev_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2s7_hybrid_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 40.4 | 50.4 | 30.8 | 45.7 | 60.0 | 38.1 |
| VN | 407 | 43.2 | 53.9 | 42.1 | 59.7 | 45.0 | 21.5 |
| TG | 922 | 39.2 | 48.9 | 26.5 | 40.4 | 68.6 | 44.5 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 44.8 | 54.3 | 43.3 | 57.5 | 47.7 | 34.4 |
| ai | 159 | 50.3 | 54.4 | 45.5 | 51.3 | 61.2 | 34.5 |
| ở đâu | 100 | 40.0 | 47.4 | 32.3 | 43.7 | 54.3 | 47.7 |
| bao nhiêu | 131 | 41.2 | 52.1 | 37.2 | 53.8 | 48.9 | 23.3 |
| vì sao | 120 | 37.5 | 51.9 | 20.8 | 43.3 | 67.4 | 33.8 |
| như thế nào | 129 | 26.4 | 39.4 | 14.1 | 32.5 | 56.8 | 42.4 |
| cái gì | 514 | 41.1 | 51.2 | 28.1 | 43.6 | 65.4 | 42.4 |
| khác | 42 | 31.0 | 44.8 | 27.0 | 42.8 | 60.0 | 35.1 |

- Đoạn đúng nằm trong các đoạn đã đọc: **71.9%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 62.0 · khi tìm sai: 4.1
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.5%

## r2s7_hybrid_k3_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:03:29", "model": "models/r2_s7", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s7_hybrid_k3_dev_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2s7_hybrid_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 40.8 | 53.0 | 35.9 | 54.1 | 50.8 | 24.7 |
| VN | 407 | 42.5 | 54.6 | 44.9 | 64.8 | 38.8 | 12.6 |
| TG | 922 | 40.0 | 52.4 | 32.4 | 50.1 | 57.8 | 29.3 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 44.8 | 56.5 | 48.9 | 66.4 | 36.4 | 18.9 |
| ai | 159 | 51.6 | 56.9 | 50.9 | 58.6 | 53.1 | 20.0 |
| ở đâu | 100 | 42.0 | 51.8 | 41.5 | 56.7 | 42.9 | 24.6 |
| bao nhiêu | 131 | 43.5 | 56.7 | 44.2 | 64.3 | 42.2 | 10.5 |
| vì sao | 120 | 36.7 | 54.7 | 24.7 | 52.8 | 58.1 | 23.4 |
| như thế nào | 129 | 27.1 | 42.6 | 18.5 | 40.2 | 48.6 | 31.5 |
| cái gì | 514 | 40.9 | 53.1 | 32.8 | 51.7 | 55.9 | 29.6 |
| khác | 42 | 28.6 | 44.9 | 24.3 | 42.9 | 60.0 | 27.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **89.3%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 60.0 · khi tìm sai: 5.0
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 99.0%

## r2s7_hybrid_k5_dev_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:03:29", "model": "models/r2_s7", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s7_hybrid_k5_dev_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 39.7 | 52.2 | 36.1 | 54.8 | 46.9 | 21.9 |
| VN | 407 | 41.3 | 53.2 | 44.1 | 63.7 | 36.9 | 10.5 |
| TG | 922 | 38.9 | 51.7 | 33.0 | 51.3 | 52.7 | 26.2 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 42.5 | 56.1 | 48.9 | 69.1 | 29.5 | 14.4 |
| ai | 159 | 52.2 | 56.8 | 52.7 | 59.4 | 51.0 | 16.4 |
| ở đâu | 100 | 40.0 | 50.4 | 43.1 | 59.1 | 34.3 | 20.0 |
| bao nhiêu | 131 | 40.5 | 53.6 | 40.7 | 60.8 | 40.0 | 10.5 |
| vì sao | 120 | 35.8 | 53.1 | 24.7 | 51.5 | 55.8 | 22.1 |
| như thế nào | 129 | 27.1 | 43.6 | 18.5 | 41.6 | 48.6 | 28.3 |
| cái gì | 514 | 40.1 | 52.6 | 33.7 | 52.9 | 52.0 | 26.6 |
| khác | 42 | 23.8 | 40.8 | 21.6 | 40.9 | 40.0 | 27.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **93.4%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 58.1 · khi tìm sai: 7.5
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.9%

## r2m_bm25_k1_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:30:28", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "bm25", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_bm25_k1_dev_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_bm25_k5_dev_rs.jsonl", "refusal_delta": -0.12, "refusal_delta_chosen_on": "dev", "source": "r2m_bm25_k1_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 41.3 | 52.2 | 31.1 | 47.3 | 62.2 | 36.2 |
| VN | 407 | 45.7 | 57.5 | 44.1 | 63.5 | 48.1 | 18.2 |
| TG | 922 | 39.4 | 49.9 | 26.0 | 41.0 | 70.4 | 43.1 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 45.5 | 58.0 | 40.0 | 58.5 | 56.8 | 30.0 |
| ai | 159 | 48.4 | 53.0 | 44.5 | 51.2 | 57.1 | 30.9 |
| ở đâu | 100 | 41.0 | 46.2 | 35.4 | 43.4 | 51.4 | 44.6 |
| bao nhiêu | 131 | 46.6 | 58.3 | 33.7 | 51.6 | 71.1 | 29.1 |
| vì sao | 120 | 40.8 | 54.6 | 23.4 | 44.8 | 72.1 | 32.5 |
| như thế nào | 129 | 26.4 | 40.0 | 17.4 | 36.5 | 48.6 | 39.1 |
| cái gì | 514 | 41.6 | 53.3 | 29.3 | 47.1 | 64.8 | 39.4 |
| khác | 42 | 28.6 | 43.2 | 21.6 | 38.2 | 80.0 | 40.5 |

- Đoạn đúng nằm trong các đoạn đã đọc: **76.1%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 61.1 · khi tìm sai: 3.0
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.4%

## r2m_bm25_k3_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:30:28", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "bm25", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_bm25_k3_dev_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_bm25_k5_dev_rs.jsonl", "refusal_delta": -0.12, "refusal_delta_chosen_on": "dev", "source": "r2m_bm25_k3_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 41.7 | 53.7 | 34.3 | 52.2 | 56.8 | 27.6 |
| VN | 407 | 45.2 | 58.6 | 44.5 | 66.6 | 46.2 | 10.1 |
| TG | 922 | 40.1 | 51.6 | 30.4 | 46.7 | 62.8 | 34.3 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 45.5 | 62.1 | 42.2 | 67.0 | 52.3 | 16.7 |
| ai | 159 | 50.3 | 55.1 | 50.0 | 56.9 | 51.0 | 23.6 |
| ở đâu | 100 | 45.0 | 51.4 | 43.1 | 53.0 | 48.6 | 32.3 |
| bao nhiêu | 131 | 48.1 | 61.3 | 37.2 | 57.3 | 68.9 | 19.8 |
| vì sao | 120 | 39.2 | 53.1 | 27.3 | 49.0 | 60.5 | 27.3 |
| như thế nào | 129 | 28.7 | 42.9 | 20.7 | 40.6 | 48.6 | 31.5 |
| cái gì | 514 | 40.9 | 53.4 | 31.6 | 50.9 | 58.1 | 31.3 |
| khác | 42 | 26.2 | 42.1 | 18.9 | 37.0 | 80.0 | 32.4 |

- Đoạn đúng nằm trong các đoạn đã đọc: **86.5%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 59.5 · khi tìm sai: 5.3
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.1%

## r2m_bm25_k5_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:30:28", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "bm25", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_bm25_k5_dev_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.12, "refusal_delta_chosen_on": "dev", "source": "r2m_bm25_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 41.6 | 53.8 | 35.4 | 53.6 | 54.2 | 25.2 |
| VN | 407 | 45.2 | 58.8 | 45.7 | 68.2 | 44.4 | 8.5 |
| TG | 922 | 40.0 | 51.6 | 31.5 | 48.0 | 59.9 | 31.6 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 45.5 | 61.5 | 43.3 | 67.2 | 50.0 | 16.7 |
| ai | 159 | 51.6 | 55.9 | 51.8 | 58.1 | 51.0 | 21.8 |
| ở đâu | 100 | 44.0 | 50.6 | 44.6 | 54.7 | 42.9 | 26.2 |
| bao nhiêu | 131 | 48.1 | 61.3 | 39.5 | 59.6 | 64.4 | 19.8 |
| vì sao | 120 | 37.5 | 52.1 | 27.3 | 50.0 | 55.8 | 26.0 |
| như thế nào | 129 | 27.9 | 42.2 | 20.7 | 40.8 | 45.9 | 30.4 |
| cái gì | 514 | 41.1 | 54.1 | 32.8 | 52.8 | 56.4 | 27.8 |
| khác | 42 | 26.2 | 42.2 | 18.9 | 37.1 | 80.0 | 29.7 |

- Đoạn đúng nằm trong các đoạn đã đọc: **90.4%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 58.8 · khi tìm sai: 4.4
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.3%

## r2m_dense_k1_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:35:02", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "dense", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_dense_k1_dev_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_dense_k5_dev_rs.jsonl", "refusal_delta": -0.14, "refusal_delta_chosen_on": "dev", "source": "r2m_dense_k1_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 38.7 | 45.9 | 21.2 | 32.0 | 74.4 | 55.4 |
| VN | 407 | 44.5 | 53.4 | 33.2 | 47.9 | 61.9 | 34.4 |
| TG | 922 | 36.1 | 42.6 | 16.6 | 25.9 | 81.6 | 63.4 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 41.8 | 51.4 | 30.0 | 44.3 | 65.9 | 46.7 |
| ai | 159 | 38.4 | 41.3 | 23.6 | 27.9 | 71.4 | 60.0 |
| ở đâu | 100 | 37.0 | 39.0 | 21.5 | 24.6 | 65.7 | 69.2 |
| bao nhiêu | 131 | 45.8 | 55.3 | 32.6 | 47.0 | 71.1 | 36.0 |
| vì sao | 120 | 40.0 | 51.8 | 18.2 | 36.6 | 79.1 | 49.4 |
| như thế nào | 129 | 27.9 | 38.2 | 10.9 | 25.3 | 70.3 | 52.2 |
| cái gì | 514 | 40.5 | 46.9 | 19.7 | 29.6 | 79.3 | 59.7 |
| khác | 42 | 19.0 | 27.4 | 10.8 | 20.3 | 80.0 | 64.9 |

- Đoạn đúng nằm trong các đoạn đã đọc: **52.2%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 59.7 · khi tìm sai: 1.6
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.5%

## r2m_dense_k3_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:35:02", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "dense", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_dense_k3_dev_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_dense_k5_dev_rs.jsonl", "refusal_delta": -0.14, "refusal_delta_chosen_on": "dev", "source": "r2m_dense_k3_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 39.5 | 48.4 | 26.7 | 40.0 | 65.7 | 43.5 |
| VN | 407 | 44.0 | 54.8 | 38.5 | 56.3 | 52.5 | 21.9 |
| TG | 922 | 37.5 | 45.6 | 22.2 | 33.7 | 73.3 | 51.8 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 41.8 | 52.4 | 33.3 | 49.1 | 59.1 | 40.0 |
| ai | 159 | 42.8 | 46.0 | 34.5 | 39.2 | 61.2 | 44.5 |
| ở đâu | 100 | 35.0 | 40.2 | 27.7 | 35.7 | 48.6 | 52.3 |
| bao nhiêu | 131 | 47.3 | 58.6 | 36.0 | 53.1 | 68.9 | 31.4 |
| vì sao | 120 | 41.7 | 53.5 | 22.1 | 40.5 | 76.7 | 36.4 |
| như thế nào | 129 | 28.7 | 40.5 | 17.4 | 34.0 | 56.8 | 39.1 |
| cái gì | 514 | 40.3 | 49.1 | 24.2 | 37.7 | 70.4 | 48.1 |
| khác | 42 | 23.8 | 34.6 | 18.9 | 31.1 | 60.0 | 45.9 |

- Đoạn đúng nằm trong các đoạn đã đọc: **67.5%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 58.5 · khi tìm sai: 1.5
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.0%

## r2m_dense_k5_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:35:02", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "dense", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_dense_k5_dev_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.52, "refusal_delta_chosen_on": "dev", "source": "r2m_dense_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 41.4 | 49.2 | 24.7 | 36.3 | 75.5 | 51.0 |
| VN | 407 | 46.4 | 55.4 | 35.2 | 50.0 | 63.8 | 33.6 |
| TG | 922 | 39.2 | 46.5 | 20.6 | 31.1 | 82.3 | 57.7 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 47.0 | 56.9 | 33.3 | 48.1 | 75.0 | 43.3 |
| ai | 159 | 49.7 | 52.1 | 39.1 | 42.6 | 73.5 | 43.6 |
| ở đâu | 100 | 41.0 | 44.3 | 26.2 | 31.3 | 68.6 | 63.1 |
| bao nhiêu | 131 | 44.3 | 54.9 | 27.9 | 44.1 | 75.6 | 43.0 |
| vì sao | 120 | 44.2 | 56.5 | 20.8 | 40.0 | 86.0 | 42.9 |
| như thế nào | 129 | 29.5 | 38.5 | 12.0 | 24.7 | 73.0 | 51.1 |
| cái gì | 514 | 40.9 | 48.6 | 22.1 | 34.0 | 76.0 | 55.2 |
| khác | 42 | 19.0 | 26.8 | 13.5 | 22.3 | 60.0 | 67.6 |

- Đoạn đúng nằm trong các đoạn đã đọc: **73.7%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 48.9 · khi tìm sai: 1.1
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.2%

## r2m_gold_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:21:08", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_gold_dev_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.12, "refusal_delta_chosen_on": "dev", "source": "r2m_gold_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 44.6 | 57.8 | 38.3 | 58.0 | 57.4 | 24.6 |
| VN | 407 | 47.4 | 61.3 | 48.2 | 71.0 | 46.2 | 10.1 |
| TG | 922 | 43.4 | 56.3 | 34.6 | 53.0 | 63.9 | 30.1 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 52.2 | 67.1 | 52.2 | 74.4 | 52.3 | 14.4 |
| ai | 159 | 52.8 | 57.5 | 53.6 | 60.4 | 51.0 | 20.0 |
| ở đâu | 100 | 45.0 | 52.7 | 47.7 | 59.5 | 40.0 | 26.2 |
| bao nhiêu | 131 | 48.1 | 62.1 | 40.7 | 62.0 | 62.2 | 19.8 |
| vì sao | 120 | 42.5 | 59.1 | 28.6 | 54.4 | 67.4 | 27.3 |
| như thế nào | 129 | 30.2 | 46.6 | 22.8 | 45.7 | 48.6 | 28.3 |
| cái gì | 514 | 44.6 | 58.7 | 35.5 | 57.2 | 61.5 | 27.8 |
| khác | 42 | 28.6 | 47.5 | 21.6 | 43.1 | 80.0 | 27.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 58.0 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.4%

## r2m_hybrid_k1_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:25:49", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_hybrid_k1_dev_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_hybrid_k5_dev_rs.jsonl", "refusal_delta": -0.14, "refusal_delta_chosen_on": "dev", "source": "r2m_hybrid_k1_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 41.2 | 51.2 | 29.3 | 44.1 | 65.7 | 39.8 |
| VN | 407 | 45.9 | 57.2 | 42.1 | 60.7 | 51.9 | 19.4 |
| TG | 922 | 39.2 | 48.6 | 24.3 | 37.8 | 73.6 | 47.6 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 44.0 | 56.7 | 37.8 | 56.6 | 56.8 | 33.3 |
| ai | 159 | 47.2 | 51.7 | 41.8 | 48.4 | 59.2 | 36.4 |
| ở đâu | 100 | 41.0 | 44.6 | 32.3 | 37.8 | 57.1 | 53.8 |
| bao nhiêu | 131 | 47.3 | 58.5 | 34.9 | 51.9 | 71.1 | 29.1 |
| vì sao | 120 | 41.7 | 53.3 | 22.1 | 40.2 | 76.7 | 37.7 |
| như thế nào | 129 | 26.4 | 38.6 | 15.2 | 32.5 | 54.1 | 41.3 |
| cái gì | 514 | 41.8 | 52.5 | 27.2 | 43.5 | 69.3 | 42.7 |
| khác | 42 | 28.6 | 42.2 | 21.6 | 37.1 | 80.0 | 40.5 |

- Đoạn đúng nằm trong các đoạn đã đọc: **71.9%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 60.2 · khi tìm sai: 3.2
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.3%

## r2m_hybrid_k3_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:25:49", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_hybrid_k3_dev_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_hybrid_k5_dev_rs.jsonl", "refusal_delta": -0.14, "refusal_delta_chosen_on": "dev", "source": "r2m_hybrid_k3_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 42.1 | 54.2 | 34.8 | 52.8 | 57.0 | 27.0 |
| VN | 407 | 45.2 | 58.6 | 45.3 | 67.4 | 45.0 | 9.3 |
| TG | 922 | 40.7 | 52.3 | 30.7 | 47.3 | 63.9 | 33.8 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 44.8 | 60.7 | 43.3 | 67.0 | 47.7 | 17.8 |
| ai | 159 | 49.7 | 54.7 | 49.1 | 56.3 | 51.0 | 22.7 |
| ở đâu | 100 | 44.0 | 50.6 | 43.1 | 53.3 | 45.7 | 29.2 |
| bao nhiêu | 131 | 48.1 | 61.2 | 39.5 | 59.6 | 64.4 | 19.8 |
| vì sao | 120 | 40.8 | 55.4 | 26.0 | 48.7 | 67.4 | 27.3 |
| như thế nào | 129 | 27.9 | 43.0 | 20.7 | 41.8 | 45.9 | 29.3 |
| cái gì | 514 | 42.2 | 54.8 | 32.5 | 51.8 | 60.3 | 31.0 |
| khác | 42 | 26.2 | 42.1 | 18.9 | 37.0 | 80.0 | 32.4 |

- Đoạn đúng nằm trong các đoạn đã đọc: **89.3%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 58.6 · khi tìm sai: 4.3
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.5%

## r2m_hybrid_k5_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 00:25:49", "model": "models/r2_lr1e-4_e8", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_hybrid_k5_dev_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.14, "refusal_delta_chosen_on": "dev", "source": "r2m_hybrid_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 41.8 | 54.3 | 35.7 | 54.2 | 54.5 | 24.6 |
| VN | 407 | 45.0 | 58.2 | 44.9 | 66.7 | 45.0 | 8.1 |
| TG | 922 | 40.5 | 52.5 | 32.1 | 49.4 | 59.9 | 30.9 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 44.8 | 61.5 | 43.3 | 68.2 | 47.7 | 15.6 |
| ai | 159 | 50.9 | 55.6 | 50.9 | 57.7 | 51.0 | 20.0 |
| ở đâu | 100 | 45.0 | 52.6 | 46.2 | 57.9 | 42.9 | 24.6 |
| bao nhiêu | 131 | 46.6 | 59.3 | 39.5 | 59.0 | 60.0 | 19.8 |
| vì sao | 120 | 37.5 | 51.4 | 24.7 | 46.3 | 60.5 | 26.0 |
| như thế nào | 129 | 27.9 | 43.3 | 20.7 | 42.3 | 45.9 | 27.2 |
| cái gì | 514 | 42.2 | 55.4 | 34.0 | 54.2 | 57.5 | 27.8 |
| khác | 42 | 26.2 | 42.1 | 18.9 | 37.0 | 80.0 | 32.4 |

- Đoạn đúng nằm trong các đoạn đã đọc: **93.4%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 57.5 · khi tìm sai: 6.4
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.3%

## r2noimp_gold_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 01:08:14", "model": "models/r2_noimp", "split": "dev", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2noimp_gold_dev_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.16, "refusal_delta_chosen_on": "dev", "source": "r2noimp_gold_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 37.4 | 51.7 | 39.6 | 60.8 | 33.0 | 20.9 |
| VN | 407 | 34.9 | 50.4 | 43.7 | 69.3 | 21.2 | 10.1 |
| TG | 922 | 38.5 | 52.2 | 38.0 | 57.6 | 39.7 | 25.0 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 46.3 | 60.2 | 55.6 | 76.3 | 27.3 | 12.2 |
| ai | 159 | 47.2 | 53.1 | 53.6 | 62.2 | 32.7 | 21.8 |
| ở đâu | 100 | 36.0 | 49.5 | 41.5 | 62.3 | 25.7 | 15.4 |
| bao nhiêu | 131 | 38.2 | 53.1 | 40.7 | 63.4 | 33.3 | 11.6 |
| vì sao | 120 | 30.0 | 50.7 | 32.5 | 64.8 | 25.6 | 11.7 |
| như thế nào | 129 | 26.4 | 43.2 | 20.7 | 44.3 | 40.5 | 29.3 |
| cái gì | 514 | 37.4 | 51.2 | 38.2 | 59.5 | 35.8 | 26.3 |
| khác | 42 | 28.6 | 54.0 | 27.0 | 55.9 | 40.0 | 18.9 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 60.8 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.6%

## r2noimp_hybrid_k1_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 01:12:19", "model": "models/r2_noimp", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2noimp_hybrid_k1_dev_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2noimp_hybrid_k5_dev_rs.jsonl", "refusal_delta": -0.64, "refusal_delta_chosen_on": "dev", "source": "r2noimp_hybrid_k1_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 38.7 | 47.2 | 25.9 | 38.6 | 64.8 | 50.9 |
| VN | 407 | 39.3 | 50.5 | 33.6 | 52.0 | 48.1 | 35.2 |
| TG | 922 | 38.4 | 45.8 | 22.9 | 33.5 | 74.4 | 56.9 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 49.3 | 57.5 | 41.1 | 53.4 | 65.9 | 40.0 |
| ai | 159 | 42.8 | 46.9 | 34.5 | 40.5 | 61.2 | 50.0 |
| ở đâu | 100 | 37.0 | 42.6 | 26.2 | 34.8 | 57.1 | 58.5 |
| bao nhiêu | 131 | 41.2 | 52.0 | 29.1 | 45.5 | 64.4 | 36.0 |
| vì sao | 120 | 31.7 | 44.4 | 19.5 | 39.3 | 53.5 | 45.5 |
| như thế nào | 129 | 28.7 | 38.1 | 13.0 | 26.3 | 67.6 | 63.0 |
| cái gì | 514 | 39.7 | 48.1 | 23.9 | 36.8 | 69.3 | 54.6 |
| khác | 42 | 23.8 | 36.9 | 18.9 | 33.7 | 60.0 | 48.6 |

- Đoạn đúng nằm trong các đoạn đã đọc: **71.9%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 52.9 · khi tìm sai: 2.1
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.1%

## r2noimp_hybrid_k3_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 01:12:19", "model": "models/r2_noimp", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2noimp_hybrid_k3_dev_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2noimp_hybrid_k5_dev_rs.jsonl", "refusal_delta": -0.66, "refusal_delta_chosen_on": "dev", "source": "r2noimp_hybrid_k3_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 39.0 | 49.1 | 30.6 | 45.7 | 56.1 | 41.5 |
| VN | 407 | 37.8 | 50.1 | 36.0 | 56.2 | 40.6 | 27.5 |
| TG | 922 | 39.5 | 48.6 | 28.5 | 41.6 | 65.0 | 46.8 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 50.0 | 61.0 | 46.7 | 63.0 | 56.8 | 26.7 |
| ai | 159 | 45.3 | 50.1 | 40.9 | 47.9 | 55.1 | 42.7 |
| ở đâu | 100 | 40.0 | 47.7 | 33.8 | 45.6 | 51.4 | 40.0 |
| bao nhiêu | 131 | 39.7 | 53.1 | 32.6 | 53.0 | 53.3 | 26.7 |
| vì sao | 120 | 30.0 | 45.8 | 24.7 | 49.3 | 39.5 | 32.5 |
| như thế nào | 129 | 31.8 | 42.4 | 17.4 | 32.3 | 67.6 | 55.4 |
| cái gì | 514 | 38.9 | 48.2 | 28.1 | 42.3 | 59.2 | 47.2 |
| khác | 42 | 23.8 | 39.2 | 18.9 | 36.4 | 60.0 | 43.2 |

- Đoạn đúng nằm trong các đoạn đã đọc: **89.3%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 51.0 · khi tìm sai: 1.0
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.6%

## r2noimp_hybrid_k5_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 01:12:19", "model": "models/r2_noimp", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2noimp_hybrid_k5_dev_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.64, "refusal_delta_chosen_on": "dev", "source": "r2noimp_hybrid_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 38.8 | 49.7 | 31.5 | 47.9 | 53.5 | 38.1 |
| VN | 407 | 36.4 | 49.3 | 36.0 | 57.4 | 36.9 | 26.3 |
| TG | 922 | 39.8 | 49.9 | 29.8 | 44.2 | 63.2 | 42.6 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 48.5 | 60.8 | 44.4 | 62.8 | 56.8 | 23.3 |
| ai | 159 | 46.5 | 51.1 | 43.6 | 50.2 | 53.1 | 38.2 |
| ở đâu | 100 | 39.0 | 49.3 | 38.5 | 54.3 | 40.0 | 30.8 |
| bao nhiêu | 131 | 39.7 | 53.1 | 32.6 | 53.0 | 53.3 | 26.7 |
| vì sao | 120 | 29.2 | 45.2 | 23.4 | 48.4 | 39.5 | 32.5 |
| như thế nào | 129 | 31.0 | 43.3 | 18.5 | 35.8 | 62.2 | 50.0 |
| cái gì | 514 | 38.9 | 49.1 | 29.3 | 44.9 | 57.0 | 44.2 |
| khác | 42 | 23.8 | 40.3 | 18.9 | 37.6 | 60.0 | 40.5 |

- Đoạn đúng nằm trong các đoạn đã đọc: **93.4%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 51.0 · khi tìm sai: 3.3
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.7%

## r2ood_gold_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 02:44:55", "model": "models/r2_ood", "split": "dev", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2ood_gold_dev_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.4, "refusal_delta_chosen_on": "dev", "source": "r2ood_gold_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 46.8 | 59.7 | 37.4 | 56.6 | 65.9 | 30.3 |
| VN | 407 | 47.7 | 62.0 | 43.3 | 66.9 | 54.4 | 17.4 |
| TG | 922 | 46.4 | 58.6 | 35.2 | 52.7 | 72.6 | 35.2 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 57.5 | 69.8 | 54.4 | 72.8 | 63.6 | 20.0 |
| ai | 159 | 54.7 | 59.4 | 54.5 | 61.3 | 55.1 | 24.5 |
| ở đâu | 100 | 42.0 | 52.4 | 38.5 | 54.5 | 48.6 | 30.8 |
| bao nhiêu | 131 | 44.3 | 59.1 | 32.6 | 55.2 | 66.7 | 29.1 |
| vì sao | 120 | 43.3 | 57.0 | 24.7 | 46.0 | 76.7 | 40.3 |
| như thế nào | 129 | 38.0 | 54.7 | 26.1 | 49.5 | 67.6 | 30.4 |
| cái gì | 514 | 48.1 | 62.0 | 36.4 | 57.8 | 69.8 | 31.3 |
| khác | 42 | 23.8 | 42.1 | 18.9 | 39.7 | 60.0 | 43.2 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 56.6 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 99.1%

## r2ood_hybrid_k1_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 02:49:37", "model": "models/r2_ood", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2ood_hybrid_k1_dev_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2ood_hybrid_k5_dev_rs.jsonl", "refusal_delta": -0.44, "refusal_delta_chosen_on": "dev", "source": "r2ood_hybrid_k1_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 43.6 | 52.7 | 28.9 | 42.6 | 73.5 | 45.3 |
| VN | 407 | 47.2 | 58.2 | 38.5 | 56.7 | 60.6 | 29.6 |
| TG | 922 | 42.0 | 50.3 | 25.3 | 37.2 | 80.9 | 51.3 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 48.5 | 57.0 | 41.1 | 53.7 | 63.6 | 40.0 |
| ai | 159 | 49.7 | 53.8 | 42.7 | 48.7 | 65.3 | 40.0 |
| ở đâu | 100 | 41.0 | 46.2 | 29.2 | 37.2 | 62.9 | 53.8 |
| bao nhiêu | 131 | 45.0 | 55.5 | 30.2 | 46.2 | 73.3 | 40.7 |
| vì sao | 120 | 42.5 | 53.9 | 15.6 | 33.4 | 90.7 | 46.8 |
| như thế nào | 129 | 33.3 | 45.6 | 18.5 | 35.6 | 70.3 | 45.7 |
| cái gì | 514 | 45.1 | 55.0 | 28.1 | 43.1 | 77.1 | 46.6 |
| khác | 42 | 21.4 | 33.4 | 16.2 | 29.8 | 60.0 | 54.1 |

- Đoạn đúng nằm trong các đoạn đã đọc: **71.9%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 58.1 · khi tìm sai: 2.9
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 99.3%

## r2ood_hybrid_k3_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 02:49:37", "model": "models/r2_ood", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2ood_hybrid_k3_dev_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2ood_hybrid_k5_dev_rs.jsonl", "refusal_delta": -0.42, "refusal_delta_chosen_on": "dev", "source": "r2ood_hybrid_k3_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 44.1 | 56.0 | 33.5 | 51.2 | 65.7 | 32.3 |
| VN | 407 | 46.9 | 60.1 | 40.5 | 62.3 | 56.9 | 19.0 |
| TG | 922 | 42.8 | 54.2 | 30.9 | 47.0 | 70.8 | 37.4 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 51.5 | 63.8 | 48.9 | 67.2 | 56.8 | 24.4 |
| ai | 159 | 50.9 | 54.8 | 50.0 | 55.5 | 53.1 | 28.2 |
| ở đâu | 100 | 39.0 | 48.8 | 33.8 | 49.0 | 48.6 | 32.3 |
| bao nhiêu | 131 | 44.3 | 58.7 | 31.4 | 53.4 | 68.9 | 27.9 |
| vì sao | 120 | 41.7 | 54.4 | 20.8 | 40.6 | 79.1 | 40.3 |
| như thế nào | 129 | 34.9 | 50.0 | 22.8 | 44.0 | 64.9 | 34.8 |
| cái gì | 514 | 45.7 | 58.4 | 32.2 | 51.7 | 70.9 | 32.8 |
| khác | 42 | 21.4 | 37.7 | 16.2 | 34.7 | 60.0 | 45.9 |

- Đoạn đúng nằm trong các đoạn đã đọc: **89.3%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 56.9 · khi tìm sai: 3.5
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.7%

## r2ood_hybrid_k5_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 02:49:37", "model": "models/r2_ood", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2ood_hybrid_k5_dev_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.42, "refusal_delta_chosen_on": "dev", "source": "r2ood_hybrid_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 44.3 | 56.4 | 34.4 | 52.4 | 64.5 | 29.6 |
| VN | 407 | 45.9 | 59.2 | 39.7 | 61.5 | 55.6 | 18.2 |
| TG | 922 | 43.6 | 55.1 | 32.4 | 48.9 | 69.7 | 34.0 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 51.5 | 65.2 | 48.9 | 69.3 | 56.8 | 21.1 |
| ai | 159 | 52.2 | 55.7 | 51.8 | 56.8 | 53.1 | 24.5 |
| ở đâu | 100 | 39.0 | 48.8 | 36.9 | 52.1 | 42.9 | 29.2 |
| bao nhiêu | 131 | 44.3 | 58.1 | 31.4 | 52.5 | 68.9 | 27.9 |
| vì sao | 120 | 40.8 | 53.9 | 19.5 | 39.9 | 79.1 | 35.1 |
| như thế nào | 129 | 35.7 | 51.1 | 23.9 | 45.6 | 64.9 | 32.6 |
| cái gì | 514 | 45.9 | 58.7 | 33.4 | 53.1 | 69.3 | 30.4 |
| khác | 42 | 21.4 | 37.8 | 16.2 | 34.8 | 60.0 | 43.2 |

- Đoạn đúng nằm trong các đoạn đã đọc: **93.4%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 55.7 · khi tìm sai: 4.8
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.7%

## r2s13_gold_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 03:51:53", "model": "models/r2_s13", "split": "dev", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s13_gold_dev_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.22, "refusal_delta_chosen_on": "dev", "source": "r2s13_gold_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 43.6 | 55.2 | 32.6 | 49.9 | 65.9 | 36.0 |
| VN | 407 | 46.9 | 58.8 | 39.3 | 58.9 | 58.8 | 24.3 |
| TG | 922 | 42.1 | 53.6 | 30.1 | 46.5 | 70.0 | 40.5 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 48.5 | 61.6 | 44.4 | 63.9 | 56.8 | 25.6 |
| ai | 159 | 53.5 | 58.1 | 49.1 | 55.8 | 63.3 | 30.0 |
| ở đâu | 100 | 37.0 | 47.3 | 36.9 | 52.7 | 37.1 | 29.2 |
| bao nhiêu | 131 | 44.3 | 55.7 | 33.7 | 51.2 | 64.4 | 32.6 |
| vì sao | 120 | 42.5 | 57.7 | 26.0 | 49.7 | 72.1 | 37.7 |
| như thế nào | 129 | 29.5 | 44.4 | 14.1 | 35.1 | 67.6 | 44.6 |
| cái gì | 514 | 45.3 | 57.0 | 30.4 | 48.4 | 73.2 | 39.4 |
| khác | 42 | 28.6 | 44.3 | 24.3 | 42.2 | 60.0 | 43.2 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 49.9 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.2%

## r2s13_hybrid_k1_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 03:56:23", "model": "models/r2_s13", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s13_hybrid_k1_dev_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2s13_hybrid_k5_dev_rs.jsonl", "refusal_delta": -0.2, "refusal_delta_chosen_on": "dev", "source": "r2s13_hybrid_k1_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 41.2 | 50.0 | 26.2 | 39.4 | 71.6 | 48.0 |
| VN | 407 | 46.4 | 56.8 | 36.4 | 53.5 | 61.9 | 30.4 |
| TG | 922 | 38.8 | 46.9 | 22.3 | 33.9 | 77.3 | 54.7 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 41.8 | 51.9 | 34.4 | 49.5 | 56.8 | 42.2 |
| ai | 159 | 50.3 | 53.8 | 40.9 | 46.0 | 71.4 | 43.6 |
| ở đâu | 100 | 37.0 | 43.6 | 27.7 | 37.8 | 54.3 | 52.3 |
| bao nhiêu | 131 | 43.5 | 52.4 | 30.2 | 43.8 | 68.9 | 39.5 |
| vì sao | 120 | 39.2 | 52.1 | 19.5 | 39.7 | 74.4 | 46.8 |
| như thế nào | 129 | 26.4 | 37.4 | 9.8 | 25.3 | 67.6 | 56.5 |
| cái gì | 514 | 43.8 | 52.7 | 24.5 | 38.2 | 79.9 | 49.9 |
| khác | 42 | 26.2 | 35.2 | 21.6 | 31.8 | 60.0 | 51.4 |

- Đoạn đúng nằm trong các đoạn đã đọc: **71.9%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 53.8 · khi tìm sai: 2.4
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.6%

## r2s13_hybrid_k3_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 03:56:23", "model": "models/r2_s13", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s13_hybrid_k3_dev_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2s13_hybrid_k5_dev_rs.jsonl", "refusal_delta": -0.24, "refusal_delta_chosen_on": "dev", "source": "r2s13_hybrid_k3_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 41.9 | 52.3 | 30.4 | 45.9 | 65.4 | 37.7 |
| VN | 407 | 45.9 | 56.8 | 38.1 | 55.9 | 58.1 | 25.5 |
| TG | 922 | 40.1 | 50.4 | 27.4 | 42.1 | 69.7 | 42.3 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 44.8 | 57.1 | 41.1 | 59.4 | 52.3 | 30.0 |
| ai | 159 | 49.7 | 54.3 | 44.5 | 51.2 | 61.2 | 30.9 |
| ở đâu | 100 | 38.0 | 46.4 | 35.4 | 48.3 | 42.9 | 33.8 |
| bao nhiêu | 131 | 42.7 | 53.9 | 31.4 | 48.4 | 64.4 | 32.6 |
| vì sao | 120 | 40.0 | 53.6 | 24.7 | 45.8 | 67.4 | 37.7 |
| như thế nào | 129 | 28.7 | 42.0 | 14.1 | 32.8 | 64.9 | 45.7 |
| cái gì | 514 | 44.4 | 54.6 | 28.4 | 44.1 | 74.3 | 41.5 |
| khác | 42 | 26.2 | 39.2 | 21.6 | 36.4 | 60.0 | 40.5 |

- Đoạn đúng nằm trong các đoạn đã đọc: **89.3%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 51.1 · khi tìm sai: 2.6
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.6%

## r2s13_hybrid_k5_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 03:56:23", "model": "models/r2_s13", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s13_hybrid_k5_dev_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.24, "refusal_delta_chosen_on": "dev", "source": "r2s13_hybrid_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 42.1 | 52.9 | 31.5 | 47.5 | 63.8 | 35.3 |
| VN | 407 | 45.2 | 56.5 | 37.2 | 55.8 | 57.5 | 23.9 |
| TG | 922 | 40.8 | 51.3 | 29.3 | 44.3 | 67.5 | 39.7 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 44.8 | 57.5 | 41.1 | 60.1 | 52.3 | 28.9 |
| ai | 159 | 50.9 | 55.0 | 47.3 | 53.1 | 59.2 | 27.3 |
| ở đâu | 100 | 39.0 | 48.3 | 40.0 | 54.3 | 37.1 | 27.7 |
| bao nhiêu | 131 | 42.7 | 53.9 | 31.4 | 48.4 | 64.4 | 31.4 |
| vì sao | 120 | 38.3 | 52.0 | 23.4 | 44.6 | 65.1 | 37.7 |
| như thế nào | 129 | 28.7 | 43.1 | 14.1 | 34.3 | 64.9 | 42.4 |
| cái gì | 514 | 44.7 | 55.4 | 29.9 | 46.3 | 72.6 | 39.1 |
| khác | 42 | 26.2 | 39.2 | 21.6 | 36.4 | 60.0 | 40.5 |

- Đoạn đúng nằm trong các đoạn đã đọc: **93.4%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 50.6 · khi tìm sai: 4.6
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.5%

## r2s7_gold_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 04:58:44", "model": "models/r2_s7", "split": "dev", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s7_gold_dev_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.2, "refusal_delta_chosen_on": "dev", "source": "r2s7_gold_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 43.7 | 56.4 | 37.0 | 56.0 | 57.4 | 28.1 |
| VN | 407 | 46.2 | 58.3 | 46.2 | 66.1 | 46.2 | 17.4 |
| TG | 922 | 42.6 | 55.6 | 33.5 | 52.1 | 63.9 | 32.2 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 52.2 | 65.5 | 53.3 | 73.1 | 50.0 | 17.8 |
| ai | 159 | 56.0 | 60.6 | 54.5 | 61.2 | 59.2 | 22.7 |
| ở đâu | 100 | 40.0 | 49.5 | 41.5 | 56.2 | 37.1 | 29.2 |
| bao nhiêu | 131 | 45.0 | 59.3 | 38.4 | 60.0 | 57.8 | 22.1 |
| vì sao | 120 | 39.2 | 57.4 | 24.7 | 53.0 | 65.1 | 27.3 |
| như thế nào | 129 | 28.7 | 44.6 | 18.5 | 40.7 | 54.1 | 39.1 |
| cái gì | 514 | 44.6 | 57.4 | 35.2 | 55.0 | 62.0 | 30.7 |
| khác | 42 | 23.8 | 41.6 | 21.6 | 41.8 | 40.0 | 32.4 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 56.0 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.8%

## r2s7_hybrid_k1_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:03:29", "model": "models/r2_s7", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s7_hybrid_k1_dev_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2s7_hybrid_k5_dev_rs.jsonl", "refusal_delta": -0.2, "refusal_delta_chosen_on": "dev", "source": "r2s7_hybrid_k1_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 41.5 | 50.9 | 29.6 | 43.5 | 65.9 | 42.4 |
| VN | 407 | 45.2 | 54.9 | 41.7 | 57.7 | 50.6 | 25.9 |
| TG | 922 | 39.9 | 49.1 | 25.0 | 38.1 | 74.7 | 48.7 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 47.8 | 56.7 | 43.3 | 56.6 | 56.8 | 35.6 |
| ai | 159 | 51.6 | 55.3 | 43.6 | 49.0 | 69.4 | 38.2 |
| ở đâu | 100 | 40.0 | 46.7 | 30.8 | 41.1 | 57.1 | 50.8 |
| bao nhiêu | 131 | 42.7 | 52.4 | 32.6 | 47.3 | 62.2 | 33.7 |
| vì sao | 120 | 38.3 | 52.0 | 19.5 | 40.8 | 72.1 | 39.0 |
| như thế nào | 129 | 26.4 | 38.2 | 14.1 | 30.8 | 56.8 | 50.0 |
| cái gì | 514 | 42.6 | 52.2 | 27.8 | 42.5 | 70.4 | 44.8 |
| khác | 42 | 26.2 | 40.1 | 21.6 | 37.4 | 60.0 | 43.2 |

- Đoạn đúng nằm trong các đoạn đã đọc: **71.9%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 59.4 · khi tìm sai: 3.0
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.5%

## r2s7_hybrid_k3_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:03:29", "model": "models/r2_s7", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s7_hybrid_k3_dev_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2s7_hybrid_k5_dev_rs.jsonl", "refusal_delta": -0.2, "refusal_delta_chosen_on": "dev", "source": "r2s7_hybrid_k3_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 42.0 | 53.9 | 34.6 | 52.4 | 57.0 | 29.3 |
| VN | 407 | 44.2 | 55.3 | 44.5 | 62.8 | 43.8 | 17.4 |
| TG | 922 | 41.0 | 53.3 | 30.9 | 48.4 | 64.6 | 33.8 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 47.8 | 59.4 | 48.9 | 66.3 | 45.5 | 21.1 |
| ai | 159 | 53.5 | 58.4 | 50.0 | 57.2 | 61.2 | 23.6 |
| ở đâu | 100 | 42.0 | 51.1 | 40.0 | 54.0 | 45.7 | 30.8 |
| bao nhiêu | 131 | 44.3 | 56.8 | 39.5 | 58.6 | 53.3 | 20.9 |
| vì sao | 120 | 38.3 | 56.6 | 23.4 | 51.9 | 65.1 | 26.0 |
| như thế nào | 129 | 27.1 | 41.8 | 18.5 | 39.1 | 48.6 | 39.1 |
| cái gì | 514 | 42.4 | 54.3 | 32.2 | 50.5 | 61.5 | 32.8 |
| khác | 42 | 23.8 | 41.7 | 18.9 | 39.2 | 60.0 | 32.4 |

- Đoạn đúng nằm trong các đoạn đã đọc: **89.3%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 58.2 · khi tìm sai: 4.1
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.9%

## r2s7_hybrid_k5_dev_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:03:29", "model": "models/r2_s7", "split": "dev", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s7_hybrid_k5_dev_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.2, "refusal_delta_chosen_on": "dev", "source": "r2s7_hybrid_k5_dev_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1329 | 41.8 | 54.0 | 35.3 | 53.5 | 54.9 | 26.3 |
| VN | 407 | 44.0 | 55.1 | 44.1 | 62.4 | 43.8 | 15.8 |
| TG | 922 | 40.8 | 53.5 | 31.9 | 50.1 | 61.4 | 30.4 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 134 | 46.3 | 59.8 | 48.9 | 69.0 | 40.9 | 16.7 |
| ai | 159 | 54.7 | 59.0 | 51.8 | 58.0 | 61.2 | 20.0 |
| ở đâu | 100 | 42.0 | 52.3 | 41.5 | 57.4 | 42.9 | 24.6 |
| bao nhiêu | 131 | 42.7 | 55.2 | 38.4 | 57.4 | 51.1 | 20.9 |
| vì sao | 120 | 38.3 | 55.8 | 24.7 | 51.9 | 62.8 | 24.7 |
| như thế nào | 129 | 27.1 | 42.8 | 18.5 | 40.5 | 48.6 | 35.9 |
| cái gì | 514 | 42.2 | 54.3 | 33.1 | 51.7 | 59.2 | 29.9 |
| khác | 42 | 23.8 | 41.7 | 18.9 | 39.2 | 60.0 | 32.4 |

- Đoạn đúng nằm trong các đoạn đã đọc: **93.4%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 56.8 · khi tìm sai: 7.1
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.8%
