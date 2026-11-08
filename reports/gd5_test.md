# Kết quả GĐ5 — test

## r2m_bm25_k1_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:13:25", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "bm25", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_bm25_k1_test_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_bm25_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 36.5 | 50.0 | 23.9 | 43.5 | 64.4 | 38.2 |
| VN | 420 | 39.8 | 52.9 | 30.3 | 49.3 | 60.8 | 32.8 |
| TG | 866 | 34.9 | 48.6 | 20.8 | 40.7 | 66.2 | 40.9 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 37.5 | 49.1 | 23.7 | 41.0 | 65.5 | 39.0 |
| ai | 216 | 45.4 | 54.3 | 33.3 | 46.7 | 69.4 | 31.9 |
| ở đâu | 75 | 40.0 | 55.3 | 32.7 | 53.7 | 60.0 | 30.9 |
| bao nhiêu | 49 | 40.8 | 53.1 | 28.1 | 47.0 | 64.7 | 31.2 |
| vì sao | 155 | 29.0 | 44.9 | 19.3 | 41.9 | 52.2 | 38.5 |
| như thế nào | 117 | 31.6 | 45.6 | 15.4 | 36.4 | 64.1 | 46.2 |
| cái gì | 563 | 35.5 | 50.4 | 21.8 | 43.3 | 66.5 | 40.0 |
| khác | 23 | 26.1 | 34.3 | 25.0 | 34.5 | 33.3 | 45.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **67.8%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 63.0 · khi tìm sai: 2.4
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.2%

## r2m_bm25_k3_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:13:25", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "bm25", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_bm25_k3_test_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_bm25_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 36.5 | 51.1 | 28.0 | 49.1 | 55.6 | 28.6 |
| VN | 420 | 40.2 | 54.9 | 34.5 | 55.7 | 53.1 | 22.1 |
| TG | 866 | 34.8 | 49.3 | 24.8 | 45.8 | 56.9 | 31.8 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 39.8 | 53.8 | 28.8 | 49.7 | 62.1 | 30.5 |
| ai | 216 | 45.8 | 56.2 | 40.3 | 55.8 | 56.9 | 19.4 |
| ở đâu | 75 | 38.7 | 52.6 | 36.4 | 55.4 | 45.0 | 23.6 |
| bao nhiêu | 49 | 38.8 | 54.1 | 37.5 | 60.9 | 41.2 | 15.6 |
| vì sao | 155 | 30.3 | 47.6 | 21.1 | 45.7 | 52.2 | 32.1 |
| như thế nào | 117 | 29.1 | 43.6 | 19.2 | 41.1 | 48.7 | 38.5 |
| cái gì | 563 | 35.7 | 51.5 | 25.1 | 47.9 | 59.5 | 30.3 |
| khác | 23 | 26.1 | 34.3 | 25.0 | 34.5 | 33.3 | 35.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **80.8%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 59.8 · khi tìm sai: 3.7
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.7%

## r2m_bm25_k5_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:13:25", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "bm25", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_bm25_k5_test_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 36.6 | 51.4 | 29.0 | 50.4 | 53.6 | 25.9 |
| VN | 420 | 39.5 | 54.7 | 34.5 | 56.5 | 50.8 | 19.3 |
| TG | 866 | 35.2 | 49.8 | 26.3 | 47.5 | 55.0 | 29.1 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 40.9 | 56.2 | 32.2 | 55.0 | 58.6 | 22.0 |
| ai | 216 | 44.4 | 55.4 | 41.0 | 57.3 | 51.4 | 18.1 |
| ở đâu | 75 | 36.0 | 51.1 | 34.5 | 55.2 | 40.0 | 21.8 |
| bao nhiêu | 49 | 36.7 | 52.0 | 37.5 | 60.9 | 35.3 | 12.5 |
| vì sao | 155 | 29.7 | 47.5 | 20.2 | 45.5 | 52.2 | 29.4 |
| như thế nào | 117 | 30.8 | 44.8 | 21.8 | 42.9 | 48.7 | 34.6 |
| cái gì | 563 | 36.4 | 52.1 | 26.4 | 49.1 | 59.0 | 28.2 |
| khác | 23 | 30.4 | 38.7 | 30.0 | 39.5 | 33.3 | 30.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **86.1%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 58.0 · khi tìm sai: 3.3
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.5%

## r2m_dense_k1_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:17:45", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "dense", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_dense_k1_test_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_dense_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 34.8 | 43.9 | 16.2 | 29.5 | 75.9 | 56.0 |
| VN | 420 | 34.5 | 43.9 | 19.3 | 33.0 | 68.5 | 52.4 |
| TG | 866 | 34.9 | 43.8 | 14.7 | 27.8 | 79.6 | 57.8 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 37.5 | 43.4 | 15.3 | 24.1 | 82.8 | 67.8 |
| ai | 216 | 40.3 | 48.7 | 21.5 | 34.2 | 77.8 | 50.0 |
| ở đâu | 75 | 34.7 | 44.8 | 23.6 | 37.4 | 65.0 | 49.1 |
| bao nhiêu | 49 | 38.8 | 47.3 | 21.9 | 35.0 | 70.6 | 50.0 |
| vì sao | 155 | 31.6 | 41.0 | 11.9 | 25.3 | 78.3 | 57.8 |
| như thế nào | 117 | 29.1 | 38.8 | 12.8 | 27.5 | 61.5 | 59.0 |
| cái gì | 563 | 34.5 | 44.1 | 14.9 | 28.7 | 78.6 | 57.2 |
| khác | 23 | 21.7 | 30.4 | 15.0 | 25.0 | 66.7 | 50.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **46.6%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 61.4 · khi tìm sai: 1.6
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 96.9%

## r2m_dense_k3_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:17:45", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "dense", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_dense_k3_test_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_dense_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 36.2 | 48.3 | 21.8 | 39.4 | 68.2 | 40.7 |
| VN | 420 | 36.7 | 49.2 | 25.9 | 44.1 | 60.8 | 35.5 |
| TG | 866 | 35.9 | 47.8 | 19.8 | 37.1 | 71.7 | 43.2 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 43.2 | 51.5 | 27.1 | 39.6 | 75.9 | 45.8 |
| ai | 216 | 43.1 | 52.0 | 31.9 | 45.4 | 65.3 | 34.7 |
| ở đâu | 75 | 37.3 | 50.1 | 29.1 | 46.5 | 60.0 | 36.4 |
| bao nhiêu | 49 | 38.8 | 49.7 | 28.1 | 44.9 | 58.8 | 34.4 |
| vì sao | 155 | 32.9 | 47.1 | 14.7 | 34.8 | 76.1 | 46.8 |
| như thế nào | 117 | 27.4 | 41.6 | 12.8 | 34.2 | 56.4 | 42.3 |
| cái gì | 563 | 35.2 | 48.3 | 19.5 | 38.4 | 70.5 | 41.5 |
| khác | 23 | 26.1 | 35.5 | 20.0 | 30.8 | 66.7 | 35.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **65.1%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 59.8 · khi tìm sai: 1.3
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.1%

## r2m_dense_k5_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:17:45", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "dense", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_dense_k5_test_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 36.2 | 49.2 | 23.6 | 42.4 | 64.4 | 35.1 |
| VN | 420 | 37.4 | 50.3 | 28.3 | 47.0 | 57.7 | 30.7 |
| TG | 866 | 35.7 | 48.7 | 21.3 | 40.2 | 67.7 | 37.2 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 45.5 | 56.7 | 32.2 | 49.0 | 72.4 | 32.2 |
| ai | 216 | 44.4 | 54.3 | 35.4 | 50.2 | 62.5 | 26.4 |
| ở đâu | 75 | 37.3 | 48.7 | 29.1 | 44.6 | 60.0 | 36.4 |
| bao nhiêu | 49 | 40.8 | 51.8 | 31.2 | 48.0 | 58.8 | 31.2 |
| vì sao | 155 | 30.3 | 45.5 | 14.7 | 36.3 | 67.4 | 41.3 |
| như thế nào | 117 | 27.4 | 41.5 | 14.1 | 35.3 | 53.8 | 37.2 |
| cái gì | 563 | 35.0 | 49.1 | 21.0 | 41.4 | 66.5 | 36.7 |
| khác | 23 | 26.1 | 35.5 | 20.0 | 30.8 | 66.7 | 35.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **71.8%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 58.4 · khi tìm sai: 1.7
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.1%

## r2m_gold_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:04:28", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_gold_test_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 40.4 | 57.4 | 33.7 | 58.3 | 55.4 | 23.2 |
| VN | 420 | 42.4 | 59.1 | 38.3 | 62.5 | 51.5 | 17.2 |
| TG | 866 | 39.5 | 56.5 | 31.5 | 56.2 | 57.2 | 26.1 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 45.5 | 63.9 | 35.6 | 63.0 | 65.5 | 18.6 |
| ai | 216 | 50.5 | 61.4 | 47.2 | 63.6 | 56.9 | 18.1 |
| ở đâu | 75 | 41.3 | 58.8 | 40.0 | 63.8 | 45.0 | 18.2 |
| bao nhiêu | 49 | 38.8 | 56.4 | 40.6 | 67.6 | 35.3 | 9.4 |
| vì sao | 155 | 32.3 | 51.5 | 23.9 | 51.3 | 52.2 | 27.5 |
| như thế nào | 117 | 32.5 | 49.1 | 23.1 | 48.0 | 51.3 | 33.3 |
| cái gì | 563 | 40.0 | 58.6 | 31.8 | 58.7 | 58.4 | 23.8 |
| khác | 23 | 34.8 | 43.0 | 35.0 | 44.5 | 33.3 | 35.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 58.3 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.4%

## r2m_hybrid_k1_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:09:00", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_hybrid_k1_test_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_hybrid_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 36.5 | 49.7 | 24.1 | 43.1 | 64.2 | 38.1 |
| VN | 420 | 39.0 | 52.1 | 29.7 | 48.6 | 60.0 | 32.8 |
| TG | 866 | 35.3 | 48.5 | 21.4 | 40.5 | 66.2 | 40.7 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 43.2 | 53.1 | 30.5 | 45.2 | 69.0 | 40.7 |
| ai | 216 | 45.8 | 55.1 | 34.0 | 47.9 | 69.4 | 30.6 |
| ở đâu | 75 | 40.0 | 55.1 | 36.4 | 57.0 | 50.0 | 27.3 |
| bao nhiêu | 49 | 34.7 | 49.6 | 28.1 | 50.9 | 47.1 | 28.1 |
| vì sao | 155 | 29.0 | 42.7 | 16.5 | 35.9 | 58.7 | 44.0 |
| như thế nào | 117 | 32.5 | 46.2 | 14.1 | 34.7 | 69.2 | 46.2 |
| cái gì | 563 | 35.0 | 49.6 | 21.8 | 42.9 | 64.7 | 39.5 |
| khác | 23 | 26.1 | 34.3 | 20.0 | 29.5 | 66.7 | 40.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **67.6%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 62.6 · khi tìm sai: 2.5
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.1%

## r2m_hybrid_k3_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:09:00", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_hybrid_k3_test_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_hybrid_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 36.1 | 51.3 | 28.5 | 50.6 | 52.9 | 25.4 |
| VN | 420 | 37.9 | 53.3 | 33.1 | 55.4 | 48.5 | 20.3 |
| TG | 866 | 35.2 | 50.3 | 26.3 | 48.2 | 55.0 | 27.8 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 42.0 | 57.7 | 32.2 | 55.6 | 62.1 | 22.0 |
| ai | 216 | 44.0 | 54.8 | 41.0 | 57.1 | 50.0 | 18.8 |
| ở đâu | 75 | 36.0 | 50.3 | 34.5 | 54.0 | 40.0 | 23.6 |
| bao nhiêu | 49 | 36.7 | 52.4 | 37.5 | 61.5 | 35.3 | 12.5 |
| vì sao | 155 | 29.7 | 47.5 | 20.2 | 45.5 | 52.2 | 30.3 |
| như thế nào | 117 | 31.6 | 46.4 | 21.8 | 44.0 | 51.3 | 32.1 |
| cái gì | 563 | 35.3 | 51.9 | 25.9 | 49.8 | 56.6 | 26.4 |
| khác | 23 | 21.7 | 30.4 | 20.0 | 30.0 | 33.3 | 35.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **86.7%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 57.7 · khi tìm sai: 4.5
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.5%

## r2m_hybrid_k5_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:09:00", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_hybrid_k5_test_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 36.3 | 51.8 | 29.4 | 51.9 | 51.6 | 23.2 |
| VN | 420 | 38.3 | 54.0 | 34.5 | 57.1 | 46.9 | 17.6 |
| TG | 866 | 35.3 | 50.7 | 27.0 | 49.3 | 53.9 | 26.0 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 43.2 | 59.1 | 33.9 | 57.6 | 62.1 | 20.3 |
| ai | 216 | 44.0 | 55.3 | 41.7 | 58.7 | 48.6 | 16.7 |
| ở đâu | 75 | 36.0 | 51.4 | 34.5 | 55.6 | 40.0 | 18.2 |
| bao nhiêu | 49 | 36.7 | 52.4 | 37.5 | 61.5 | 35.3 | 12.5 |
| vì sao | 155 | 30.3 | 48.7 | 21.1 | 47.3 | 52.2 | 26.6 |
| như thế nào | 117 | 29.1 | 43.9 | 21.8 | 44.0 | 43.6 | 30.8 |
| cái gì | 563 | 35.9 | 52.5 | 26.9 | 50.9 | 56.1 | 24.9 |
| khác | 23 | 26.1 | 34.8 | 25.0 | 35.0 | 33.3 | 30.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **90.2%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 57.0 · khi tìm sai: 4.1
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.3%

## r2noimp_gold_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:18:35", "model": "models/r2_noimp", "split": "test", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2noimp_gold_test_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 33.8 | 51.2 | 35.7 | 60.9 | 29.6 | 16.9 |
| VN | 420 | 36.0 | 51.2 | 41.0 | 63.1 | 24.6 | 13.1 |
| TG | 866 | 32.8 | 51.2 | 33.2 | 59.8 | 32.0 | 18.8 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 40.9 | 56.7 | 52.5 | 76.1 | 17.2 | 6.8 |
| ai | 216 | 42.1 | 51.0 | 47.9 | 61.1 | 30.6 | 18.8 |
| ở đâu | 75 | 29.3 | 47.8 | 34.5 | 59.7 | 15.0 | 14.5 |
| bao nhiêu | 49 | 32.7 | 54.2 | 37.5 | 70.5 | 23.5 | 0.0 |
| vì sao | 155 | 23.9 | 43.9 | 25.7 | 54.2 | 19.6 | 14.7 |
| như thế nào | 117 | 24.8 | 44.8 | 16.7 | 46.7 | 41.0 | 38.5 |
| cái gì | 563 | 35.2 | 54.3 | 35.6 | 63.2 | 34.1 | 16.2 |
| khác | 23 | 26.1 | 41.2 | 30.0 | 47.4 | 0.0 | 10.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 60.9 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.4%

## r2noimp_hybrid_k1_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:22:43", "model": "models/r2_noimp", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2noimp_hybrid_k1_test_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2noimp_hybrid_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 32.4 | 45.7 | 25.9 | 45.1 | 46.9 | 33.4 |
| VN | 420 | 34.0 | 46.1 | 31.0 | 48.5 | 40.8 | 29.0 |
| TG | 866 | 31.6 | 45.5 | 23.5 | 43.5 | 49.8 | 35.5 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 40.9 | 50.1 | 39.0 | 52.7 | 44.8 | 30.5 |
| ai | 216 | 39.4 | 46.6 | 36.8 | 47.6 | 44.4 | 29.2 |
| ở đâu | 75 | 30.7 | 46.8 | 29.1 | 51.0 | 35.0 | 25.5 |
| bao nhiêu | 49 | 36.7 | 52.6 | 34.4 | 58.7 | 41.2 | 18.8 |
| vì sao | 155 | 24.5 | 36.4 | 21.1 | 38.0 | 32.6 | 34.9 |
| như thế nào | 117 | 26.5 | 44.1 | 10.3 | 36.7 | 59.0 | 47.4 |
| cái gì | 563 | 32.3 | 47.3 | 23.8 | 45.5 | 51.4 | 34.6 |
| khác | 23 | 17.4 | 31.6 | 15.0 | 31.4 | 33.3 | 30.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **67.6%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 65.1 · khi tìm sai: 3.3
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.4%

## r2noimp_hybrid_k3_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:22:43", "model": "models/r2_noimp", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2noimp_hybrid_k3_test_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2noimp_hybrid_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 31.4 | 46.7 | 31.0 | 53.1 | 32.3 | 18.7 |
| VN | 420 | 32.9 | 46.7 | 35.9 | 55.9 | 26.2 | 15.2 |
| TG | 866 | 30.7 | 46.6 | 28.6 | 51.7 | 35.3 | 20.4 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 37.5 | 50.6 | 45.8 | 65.3 | 20.7 | 11.9 |
| ai | 216 | 41.2 | 48.6 | 45.1 | 56.3 | 33.3 | 16.7 |
| ở đâu | 75 | 29.3 | 44.4 | 32.7 | 53.3 | 20.0 | 12.7 |
| bao nhiêu | 49 | 34.7 | 52.5 | 37.5 | 64.7 | 29.4 | 3.1 |
| vì sao | 155 | 20.6 | 38.3 | 22.0 | 47.2 | 17.4 | 16.5 |
| như thế nào | 117 | 23.9 | 43.7 | 14.1 | 43.7 | 43.6 | 33.3 |
| cái gì | 563 | 31.8 | 48.6 | 29.2 | 53.5 | 37.6 | 20.5 |
| khác | 23 | 17.4 | 30.9 | 20.0 | 35.5 | 0.0 | 15.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **86.7%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 60.5 · khi tìm sai: 4.8
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.4%

## r2noimp_hybrid_k5_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:22:43", "model": "models/r2_noimp", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2noimp_hybrid_k5_test_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 30.4 | 45.9 | 31.3 | 53.8 | 28.3 | 16.2 |
| VN | 420 | 32.9 | 46.4 | 36.9 | 56.5 | 23.8 | 12.1 |
| TG | 866 | 29.2 | 45.6 | 28.6 | 52.4 | 30.5 | 18.3 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 37.5 | 50.7 | 49.2 | 68.9 | 13.8 | 10.2 |
| ai | 216 | 39.8 | 48.5 | 45.1 | 58.1 | 29.2 | 13.2 |
| ở đâu | 75 | 28.0 | 43.2 | 32.7 | 53.4 | 15.0 | 10.9 |
| bao nhiêu | 49 | 30.6 | 48.4 | 37.5 | 64.7 | 17.6 | 3.1 |
| vì sao | 155 | 21.9 | 39.9 | 23.9 | 49.4 | 17.4 | 14.7 |
| như thế nào | 117 | 23.1 | 42.6 | 14.1 | 43.4 | 41.0 | 32.1 |
| cái gì | 563 | 30.2 | 47.1 | 28.7 | 53.1 | 33.5 | 17.7 |
| khác | 23 | 21.7 | 33.8 | 25.0 | 38.8 | 0.0 | 10.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **90.2%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 59.1 · khi tìm sai: 4.2
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.4%

## r2ood_gold_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:23:43", "model": "models/r2_ood", "split": "test", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2ood_gold_test_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 44.6 | 60.3 | 37.3 | 60.1 | 60.7 | 21.2 |
| VN | 420 | 47.6 | 61.3 | 43.8 | 63.6 | 56.2 | 17.9 |
| TG | 866 | 43.1 | 59.8 | 34.2 | 58.4 | 62.8 | 22.8 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 53.4 | 69.1 | 45.8 | 69.1 | 69.0 | 13.6 |
| ai | 216 | 53.2 | 62.7 | 50.7 | 65.0 | 58.3 | 18.8 |
| ở đâu | 75 | 46.7 | 61.3 | 41.8 | 61.7 | 60.0 | 16.4 |
| bao nhiêu | 49 | 44.9 | 57.9 | 46.9 | 66.8 | 41.2 | 9.4 |
| vì sao | 155 | 36.1 | 50.7 | 27.5 | 48.3 | 56.5 | 27.5 |
| như thế nào | 117 | 35.9 | 54.0 | 23.1 | 50.3 | 61.5 | 32.1 |
| cái gì | 563 | 44.0 | 62.2 | 35.6 | 61.8 | 63.0 | 20.8 |
| khác | 23 | 34.8 | 54.6 | 30.0 | 52.8 | 66.7 | 25.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 60.1 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.6%

## r2ood_hybrid_k1_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:28:19", "model": "models/r2_ood", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2ood_hybrid_k1_test_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2ood_hybrid_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 39.6 | 51.9 | 26.2 | 43.9 | 69.4 | 37.2 |
| VN | 420 | 41.7 | 52.6 | 32.1 | 47.9 | 63.1 | 34.5 |
| TG | 866 | 38.6 | 51.5 | 23.3 | 42.0 | 72.5 | 38.5 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 43.2 | 57.2 | 28.8 | 49.7 | 72.4 | 32.2 |
| ai | 216 | 44.4 | 53.6 | 34.7 | 48.4 | 63.9 | 32.6 |
| ở đâu | 75 | 44.0 | 56.4 | 32.7 | 49.6 | 75.0 | 30.9 |
| bao nhiêu | 49 | 42.9 | 51.8 | 34.4 | 48.0 | 58.8 | 28.1 |
| vì sao | 155 | 35.5 | 44.9 | 22.9 | 36.3 | 65.2 | 41.3 |
| như thế nào | 117 | 32.5 | 48.2 | 12.8 | 36.4 | 71.8 | 44.9 |
| cái gì | 563 | 39.6 | 53.0 | 24.9 | 44.2 | 72.8 | 38.5 |
| khác | 23 | 21.7 | 37.4 | 20.0 | 38.0 | 33.3 | 40.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **67.6%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 63.7 · khi tìm sai: 2.6
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.8%

## r2ood_hybrid_k3_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:28:19", "model": "models/r2_ood", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2ood_hybrid_k3_test_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2ood_hybrid_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 40.0 | 54.0 | 31.3 | 51.6 | 59.1 | 23.3 |
| VN | 420 | 42.1 | 54.5 | 37.9 | 55.8 | 51.5 | 21.0 |
| TG | 866 | 38.9 | 53.7 | 28.1 | 49.6 | 62.8 | 24.5 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 43.2 | 57.0 | 35.6 | 56.1 | 58.6 | 15.3 |
| ai | 216 | 47.2 | 56.7 | 43.8 | 57.9 | 54.2 | 20.1 |
| ở đâu | 75 | 41.3 | 55.0 | 36.4 | 55.1 | 55.0 | 20.0 |
| bao nhiêu | 49 | 44.9 | 55.6 | 43.8 | 60.1 | 47.1 | 12.5 |
| vì sao | 155 | 31.0 | 44.2 | 22.0 | 40.8 | 52.2 | 28.4 |
| như thế nào | 117 | 34.2 | 51.3 | 20.5 | 46.2 | 61.5 | 30.8 |
| cái gì | 563 | 40.3 | 56.0 | 29.2 | 51.9 | 65.3 | 23.8 |
| khác | 23 | 26.1 | 38.9 | 30.0 | 44.7 | 0.0 | 30.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **86.7%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 59.0 · khi tìm sai: 3.7
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.0%

## r2ood_hybrid_k5_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:28:19", "model": "models/r2_ood", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2ood_hybrid_k5_test_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 39.4 | 53.4 | 32.0 | 52.2 | 55.9 | 20.6 |
| VN | 420 | 42.1 | 54.5 | 39.7 | 57.6 | 47.7 | 17.6 |
| TG | 866 | 38.1 | 52.8 | 28.3 | 49.6 | 59.9 | 22.1 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 44.3 | 58.1 | 39.0 | 59.5 | 55.2 | 11.9 |
| ai | 216 | 45.8 | 55.8 | 43.1 | 58.0 | 51.4 | 16.7 |
| ở đâu | 75 | 44.0 | 58.2 | 40.0 | 59.3 | 55.0 | 16.4 |
| bao nhiêu | 49 | 44.9 | 55.6 | 43.8 | 60.1 | 47.1 | 12.5 |
| vì sao | 155 | 32.3 | 46.0 | 23.9 | 43.4 | 52.2 | 25.7 |
| như thế nào | 117 | 33.3 | 49.9 | 20.5 | 45.4 | 59.0 | 29.5 |
| cái gì | 563 | 38.9 | 54.2 | 29.5 | 51.6 | 60.1 | 21.3 |
| khác | 23 | 26.1 | 38.9 | 30.0 | 44.7 | 0.0 | 25.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **90.2%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 57.5 · khi tìm sai: 4.2
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.3%

## r2s13_gold_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:29:22", "model": "models/r2_s13", "split": "test", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s13_gold_test_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 42.5 | 57.8 | 33.4 | 55.4 | 62.9 | 28.0 |
| VN | 420 | 44.8 | 59.1 | 39.7 | 60.4 | 56.2 | 22.8 |
| TG | 866 | 41.5 | 57.1 | 30.3 | 53.0 | 66.2 | 30.5 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 45.5 | 58.4 | 35.6 | 54.9 | 65.5 | 30.5 |
| ai | 216 | 51.9 | 59.7 | 47.2 | 59.0 | 61.1 | 28.5 |
| ở đâu | 75 | 50.7 | 65.4 | 45.5 | 65.5 | 65.0 | 18.2 |
| bao nhiêu | 49 | 42.9 | 57.6 | 46.9 | 69.4 | 35.3 | 6.2 |
| vì sao | 155 | 32.9 | 49.4 | 21.1 | 44.5 | 60.9 | 31.2 |
| như thế nào | 117 | 35.0 | 52.4 | 21.8 | 47.8 | 61.5 | 34.6 |
| cái gì | 563 | 41.9 | 60.0 | 30.5 | 56.6 | 67.6 | 29.0 |
| khác | 23 | 34.8 | 41.4 | 40.0 | 47.6 | 0.0 | 15.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 55.4 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.5%

## r2s13_hybrid_k1_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:33:56", "model": "models/r2_s13", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s13_hybrid_k1_test_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2s13_hybrid_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 38.5 | 50.3 | 24.8 | 41.9 | 68.9 | 41.0 |
| VN | 420 | 40.5 | 52.0 | 30.7 | 47.3 | 62.3 | 36.2 |
| TG | 866 | 37.5 | 49.5 | 21.9 | 39.3 | 72.1 | 43.4 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 46.6 | 52.3 | 32.2 | 40.7 | 75.9 | 47.5 |
| ai | 216 | 46.3 | 53.6 | 35.4 | 46.3 | 68.1 | 37.5 |
| ở đâu | 75 | 45.3 | 58.8 | 36.4 | 54.8 | 70.0 | 29.1 |
| bao nhiêu | 49 | 38.8 | 50.4 | 34.4 | 52.2 | 47.1 | 21.9 |
| vì sao | 155 | 31.6 | 43.2 | 17.4 | 33.9 | 65.2 | 44.0 |
| như thế nào | 117 | 32.5 | 47.6 | 12.8 | 35.5 | 71.8 | 48.7 |
| cái gì | 563 | 36.9 | 51.0 | 21.8 | 42.1 | 71.1 | 41.8 |
| khác | 23 | 26.1 | 27.2 | 25.0 | 26.2 | 33.3 | 50.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **67.6%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 60.9 · khi tìm sai: 2.2
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.1%

## r2s13_hybrid_k3_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:33:56", "model": "models/r2_s13", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s13_hybrid_k3_test_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2s13_hybrid_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 38.6 | 52.5 | 28.4 | 48.6 | 61.2 | 29.2 |
| VN | 420 | 40.2 | 53.5 | 34.5 | 53.7 | 53.1 | 23.1 |
| TG | 866 | 37.8 | 52.0 | 25.5 | 46.1 | 65.1 | 32.2 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 43.2 | 54.0 | 32.2 | 48.4 | 65.5 | 33.9 |
| ai | 216 | 48.1 | 55.5 | 42.4 | 53.4 | 59.7 | 27.1 |
| ở đâu | 75 | 46.7 | 60.5 | 40.0 | 58.9 | 65.0 | 20.0 |
| bao nhiêu | 49 | 40.8 | 52.5 | 43.8 | 61.6 | 35.3 | 9.4 |
| vì sao | 155 | 30.3 | 45.5 | 18.3 | 40.0 | 58.7 | 30.3 |
| như thế nào | 117 | 32.5 | 49.8 | 17.9 | 44.0 | 61.5 | 37.2 |
| cái gì | 563 | 36.9 | 53.3 | 24.6 | 48.3 | 64.7 | 30.5 |
| khác | 23 | 26.1 | 32.7 | 30.0 | 37.6 | 0.0 | 25.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **86.7%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 55.6 · khi tìm sai: 3.0
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.1%

## r2s13_hybrid_k5_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:33:56", "model": "models/r2_s13", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s13_hybrid_k5_test_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 38.3 | 52.4 | 29.2 | 49.7 | 58.4 | 26.5 |
| VN | 420 | 40.5 | 54.2 | 35.2 | 55.0 | 52.3 | 20.0 |
| TG | 866 | 37.2 | 51.6 | 26.3 | 47.1 | 61.3 | 29.6 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 44.3 | 54.9 | 33.9 | 49.6 | 65.5 | 32.2 |
| ai | 216 | 46.3 | 53.6 | 42.4 | 53.3 | 54.2 | 24.3 |
| ở đâu | 75 | 46.7 | 61.0 | 41.8 | 61.3 | 60.0 | 16.4 |
| bao nhiêu | 49 | 38.8 | 50.5 | 43.8 | 61.6 | 29.4 | 9.4 |
| vì sao | 155 | 31.0 | 47.4 | 19.3 | 42.6 | 58.7 | 27.5 |
| như thế nào | 117 | 30.8 | 48.1 | 16.7 | 42.7 | 59.0 | 35.9 |
| cái gì | 563 | 36.9 | 53.5 | 25.6 | 49.5 | 62.4 | 27.7 |
| khác | 23 | 30.4 | 38.5 | 35.0 | 44.3 | 0.0 | 15.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **90.2%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 54.8 · khi tìm sai: 3.2
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.0%

## r2s7_gold_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:34:56", "model": "models/r2_s7", "split": "test", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s7_gold_test_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 39.9 | 56.7 | 34.2 | 58.6 | 52.6 | 22.4 |
| VN | 420 | 42.1 | 56.9 | 41.4 | 62.7 | 43.8 | 17.6 |
| TG | 866 | 38.8 | 56.6 | 30.7 | 56.5 | 56.9 | 24.8 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 46.6 | 59.9 | 42.4 | 62.2 | 55.2 | 20.3 |
| ai | 216 | 45.8 | 54.9 | 45.8 | 59.5 | 45.8 | 20.1 |
| ở đâu | 75 | 37.3 | 55.0 | 34.5 | 58.6 | 45.0 | 16.4 |
| bao nhiêu | 49 | 38.8 | 58.4 | 37.5 | 67.6 | 41.2 | 9.4 |
| vì sao | 155 | 30.3 | 47.9 | 26.6 | 51.6 | 39.1 | 23.9 |
| như thế nào | 117 | 33.3 | 53.3 | 20.5 | 50.5 | 59.0 | 32.1 |
| cái gì | 563 | 41.2 | 60.4 | 33.1 | 60.8 | 59.5 | 22.8 |
| khác | 23 | 34.8 | 50.6 | 35.0 | 53.2 | 33.3 | 30.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 58.6 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.3%

## r2s7_hybrid_k1_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:39:36", "model": "models/r2_s7", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s7_hybrid_k1_test_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2s7_hybrid_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 35.8 | 48.7 | 24.5 | 43.2 | 60.9 | 39.2 |
| VN | 420 | 38.1 | 49.9 | 31.4 | 48.4 | 53.1 | 34.8 |
| TG | 866 | 34.6 | 48.1 | 21.1 | 40.7 | 64.7 | 41.4 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 45.5 | 54.3 | 33.9 | 47.1 | 69.0 | 39.0 |
| ai | 216 | 40.3 | 49.1 | 31.9 | 45.2 | 56.9 | 31.9 |
| ở đâu | 75 | 34.7 | 51.0 | 30.9 | 53.1 | 45.0 | 27.3 |
| bao nhiêu | 49 | 36.7 | 52.7 | 28.1 | 52.6 | 52.9 | 25.0 |
| vì sao | 155 | 29.0 | 40.1 | 21.1 | 36.9 | 47.8 | 41.3 |
| như thế nào | 117 | 30.8 | 48.3 | 10.3 | 36.5 | 71.8 | 47.4 |
| cái gì | 563 | 35.9 | 49.9 | 23.1 | 43.3 | 64.7 | 42.1 |
| khác | 23 | 26.1 | 38.4 | 20.0 | 34.2 | 66.7 | 50.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **67.6%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 62.8 · khi tìm sai: 2.3
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.4%

## r2s7_hybrid_k3_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:39:36", "model": "models/r2_s7", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s7_hybrid_k3_test_rs", "refusal_scores": true, "device": "cuda", "derived_from": "r2s7_hybrid_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 35.8 | 50.7 | 29.0 | 50.5 | 51.1 | 25.9 |
| VN | 420 | 37.6 | 50.7 | 35.5 | 54.4 | 42.3 | 21.7 |
| TG | 866 | 35.0 | 50.7 | 25.8 | 48.6 | 55.4 | 28.0 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 40.9 | 51.6 | 35.6 | 51.6 | 51.7 | 22.0 |
| ai | 216 | 42.6 | 51.3 | 41.7 | 54.8 | 44.4 | 21.5 |
| ở đâu | 75 | 33.3 | 48.9 | 30.9 | 52.1 | 40.0 | 20.0 |
| bao nhiêu | 49 | 38.8 | 55.2 | 37.5 | 62.7 | 41.2 | 12.5 |
| vì sao | 155 | 28.4 | 43.9 | 22.9 | 45.0 | 41.3 | 27.5 |
| như thế nào | 117 | 30.8 | 49.3 | 17.9 | 45.8 | 56.4 | 34.6 |
| cái gì | 563 | 35.9 | 52.5 | 26.2 | 50.2 | 57.8 | 27.4 |
| khác | 23 | 30.4 | 46.3 | 30.0 | 48.2 | 33.3 | 35.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **86.7%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 57.9 · khi tìm sai: 2.5
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.4%

## r2s7_hybrid_k5_test_rs

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:39:36", "model": "models/r2_s7", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s7_hybrid_k5_test_rs", "refusal_scores": true, "device": "cuda"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 35.8 | 50.7 | 29.7 | 51.3 | 49.4 | 23.0 |
| VN | 420 | 38.3 | 51.5 | 36.9 | 55.9 | 41.5 | 18.6 |
| TG | 866 | 34.5 | 50.3 | 26.1 | 49.0 | 53.2 | 25.1 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 40.9 | 51.8 | 35.6 | 51.9 | 51.7 | 20.3 |
| ai | 216 | 42.1 | 51.3 | 41.7 | 55.4 | 43.1 | 19.4 |
| ở đâu | 75 | 33.3 | 49.9 | 30.9 | 53.5 | 40.0 | 14.5 |
| bao nhiêu | 49 | 38.8 | 55.2 | 37.5 | 62.7 | 41.2 | 12.5 |
| vì sao | 155 | 29.7 | 45.8 | 24.8 | 47.7 | 41.3 | 22.0 |
| như thế nào | 117 | 29.9 | 48.6 | 17.9 | 45.9 | 53.8 | 32.1 |
| cái gì | 563 | 35.5 | 51.8 | 26.9 | 50.5 | 54.9 | 24.9 |
| khác | 23 | 34.8 | 50.6 | 35.0 | 53.2 | 33.3 | 30.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **90.2%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 56.6 · khi tìm sai: 2.7
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.3%

## r2m_bm25_k1_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:13:25", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "bm25", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_bm25_k1_test_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_bm25_k5_test_rs.jsonl", "refusal_delta": -0.12, "refusal_delta_chosen_on": "dev (r2m_bm25_k1_dev_rs.jsonl)", "source": "r2m_bm25_k1_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 36.8 | 50.0 | 23.7 | 42.9 | 65.9 | 39.8 |
| VN | 420 | 40.0 | 52.5 | 30.3 | 48.4 | 61.5 | 34.8 |
| TG | 866 | 35.2 | 48.9 | 20.4 | 40.2 | 68.0 | 42.2 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 39.8 | 51.1 | 23.7 | 40.6 | 72.4 | 40.7 |
| ai | 216 | 46.3 | 55.0 | 33.3 | 46.4 | 72.2 | 34.7 |
| ở đâu | 75 | 40.0 | 54.6 | 32.7 | 52.6 | 60.0 | 32.7 |
| bao nhiêu | 49 | 40.8 | 53.1 | 28.1 | 47.0 | 64.7 | 31.2 |
| vì sao | 155 | 29.7 | 45.6 | 19.3 | 41.9 | 54.3 | 37.6 |
| như thế nào | 117 | 31.6 | 45.6 | 15.4 | 36.4 | 64.1 | 46.2 |
| cái gì | 563 | 35.7 | 50.3 | 21.8 | 42.8 | 67.1 | 41.5 |
| khác | 23 | 17.4 | 24.5 | 15.0 | 23.2 | 33.3 | 60.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **67.8%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 62.3 · khi tìm sai: 2.2
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.3%

## r2m_bm25_k3_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:13:25", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "bm25", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_bm25_k3_test_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_bm25_k5_test_rs.jsonl", "refusal_delta": -0.12, "refusal_delta_chosen_on": "dev (r2m_bm25_k3_dev_rs.jsonl)", "source": "r2m_bm25_k3_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 36.9 | 51.2 | 27.6 | 48.3 | 57.4 | 30.2 |
| VN | 420 | 40.7 | 54.7 | 34.5 | 54.8 | 54.6 | 24.1 |
| TG | 866 | 35.0 | 49.4 | 24.3 | 45.2 | 58.7 | 33.2 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 42.0 | 55.3 | 28.8 | 48.6 | 69.0 | 32.2 |
| ai | 216 | 46.3 | 56.1 | 39.6 | 54.3 | 59.7 | 23.6 |
| ở đâu | 75 | 38.7 | 51.8 | 36.4 | 54.3 | 45.0 | 25.5 |
| bao nhiêu | 49 | 40.8 | 56.1 | 37.5 | 60.9 | 47.1 | 15.6 |
| vì sao | 155 | 31.0 | 48.3 | 21.1 | 45.7 | 54.3 | 32.1 |
| như thế nào | 117 | 29.1 | 43.6 | 19.2 | 41.1 | 48.7 | 38.5 |
| cái gì | 563 | 35.7 | 51.3 | 24.9 | 47.4 | 60.1 | 31.0 |
| khác | 23 | 21.7 | 30.0 | 20.0 | 29.5 | 33.3 | 50.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **80.8%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 58.9 · khi tìm sai: 3.7
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.6%

## r2m_bm25_k5_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:13:25", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "bm25", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_bm25_k5_test_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.12, "refusal_delta_chosen_on": "dev (r2m_bm25_k5_dev_rs.jsonl)", "source": "r2m_bm25_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 37.2 | 51.7 | 28.6 | 49.7 | 56.1 | 27.4 |
| VN | 420 | 40.7 | 55.3 | 34.5 | 55.5 | 54.6 | 21.0 |
| TG | 866 | 35.5 | 49.9 | 25.8 | 46.8 | 56.9 | 30.5 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 42.0 | 56.6 | 32.2 | 53.9 | 62.1 | 25.4 |
| ai | 216 | 46.3 | 56.7 | 40.3 | 55.9 | 58.3 | 21.5 |
| ở đâu | 75 | 37.3 | 51.7 | 34.5 | 54.1 | 45.0 | 23.6 |
| bao nhiêu | 49 | 38.8 | 54.1 | 37.5 | 60.9 | 41.2 | 12.5 |
| vì sao | 155 | 30.3 | 48.1 | 20.2 | 45.5 | 54.3 | 29.4 |
| như thế nào | 117 | 30.8 | 44.8 | 21.8 | 42.9 | 48.7 | 34.6 |
| cái gì | 563 | 36.4 | 51.9 | 26.2 | 48.5 | 59.5 | 28.7 |
| khác | 23 | 26.1 | 34.3 | 25.0 | 34.5 | 33.3 | 45.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **86.1%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 57.1 · khi tìm sai: 3.4
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.4%

## r2m_dense_k1_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:17:45", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "dense", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_dense_k1_test_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_dense_k5_test_rs.jsonl", "refusal_delta": -0.14, "refusal_delta_chosen_on": "dev (r2m_dense_k1_dev_rs.jsonl)", "source": "r2m_dense_k1_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 34.8 | 43.5 | 15.8 | 28.4 | 76.9 | 58.4 |
| VN | 420 | 34.0 | 42.7 | 18.3 | 30.8 | 69.2 | 55.9 |
| TG | 866 | 35.1 | 43.9 | 14.6 | 27.3 | 80.7 | 59.6 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 38.6 | 44.6 | 15.3 | 24.1 | 86.2 | 67.8 |
| ai | 216 | 40.7 | 48.5 | 21.5 | 33.2 | 79.2 | 54.2 |
| ở đâu | 75 | 34.7 | 44.8 | 21.8 | 35.6 | 70.0 | 50.9 |
| bao nhiêu | 49 | 38.8 | 47.3 | 21.9 | 35.0 | 70.6 | 53.1 |
| vì sao | 155 | 31.6 | 41.0 | 11.9 | 25.3 | 78.3 | 57.8 |
| như thế nào | 117 | 28.2 | 38.0 | 11.5 | 26.2 | 61.5 | 60.3 |
| cái gì | 563 | 34.5 | 43.6 | 14.6 | 27.7 | 79.2 | 59.5 |
| khác | 23 | 17.4 | 23.2 | 10.0 | 16.6 | 66.7 | 65.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **46.6%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 59.3 · khi tìm sai: 1.6
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 96.7%

## r2m_dense_k3_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:17:45", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "dense", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_dense_k3_test_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_dense_k5_test_rs.jsonl", "refusal_delta": -0.14, "refusal_delta_chosen_on": "dev (r2m_dense_k3_dev_rs.jsonl)", "source": "r2m_dense_k3_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 36.4 | 48.2 | 21.3 | 38.4 | 69.9 | 43.4 |
| VN | 420 | 36.9 | 48.8 | 24.8 | 42.0 | 63.8 | 39.3 |
| TG | 866 | 36.1 | 47.9 | 19.6 | 36.7 | 72.9 | 45.4 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 42.0 | 50.1 | 25.4 | 37.5 | 75.9 | 49.2 |
| ai | 216 | 44.4 | 53.1 | 31.2 | 44.3 | 70.8 | 38.9 |
| ở đâu | 75 | 37.3 | 49.3 | 27.3 | 43.6 | 65.0 | 40.0 |
| bao nhiêu | 49 | 38.8 | 49.7 | 28.1 | 44.9 | 58.8 | 40.6 |
| vì sao | 155 | 32.9 | 47.1 | 14.7 | 34.8 | 76.1 | 46.8 |
| như thế nào | 117 | 26.5 | 40.7 | 11.5 | 32.8 | 56.4 | 47.4 |
| cái gì | 563 | 35.5 | 48.1 | 19.5 | 37.7 | 71.7 | 43.6 |
| khác | 23 | 26.1 | 35.5 | 20.0 | 30.8 | 66.7 | 35.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **65.1%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 58.4 · khi tìm sai: 1.3
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 96.9%

## r2m_dense_k5_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:17:45", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "dense", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_dense_k5_test_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.52, "refusal_delta_chosen_on": "dev (r2m_dense_k5_dev_rs.jsonl)", "source": "r2m_dense_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 39.0 | 49.3 | 20.3 | 35.2 | 80.7 | 49.5 |
| VN | 420 | 41.4 | 51.0 | 24.1 | 38.0 | 80.0 | 45.9 |
| TG | 866 | 37.9 | 48.5 | 18.4 | 33.8 | 81.0 | 51.3 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 45.5 | 55.8 | 28.8 | 44.2 | 79.3 | 42.4 |
| ai | 216 | 49.1 | 56.3 | 31.2 | 42.1 | 84.7 | 41.0 |
| ở đâu | 75 | 36.0 | 46.5 | 23.6 | 38.0 | 70.0 | 47.3 |
| bao nhiêu | 49 | 44.9 | 53.8 | 25.0 | 38.6 | 82.4 | 50.0 |
| vì sao | 155 | 31.6 | 44.0 | 13.8 | 31.3 | 73.9 | 52.3 |
| như thế nào | 117 | 31.6 | 42.6 | 10.3 | 26.7 | 74.4 | 55.1 |
| cái gì | 563 | 38.0 | 48.9 | 17.9 | 33.7 | 83.2 | 51.8 |
| khác | 23 | 30.4 | 36.5 | 20.0 | 27.0 | 100.0 | 55.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **71.8%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 48.7 · khi tìm sai: 0.7
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.0%

## r2m_gold_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:04:28", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_gold_test_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.12, "refusal_delta_chosen_on": "dev (r2m_gold_dev_rs.jsonl)", "source": "r2m_gold_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 40.4 | 56.9 | 32.8 | 56.6 | 57.4 | 25.9 |
| VN | 420 | 42.4 | 58.1 | 37.2 | 60.1 | 53.8 | 21.0 |
| TG | 866 | 39.5 | 56.2 | 30.7 | 54.9 | 59.1 | 28.3 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 44.3 | 61.7 | 32.2 | 58.1 | 69.0 | 25.4 |
| ai | 216 | 50.9 | 60.9 | 45.8 | 60.8 | 61.1 | 22.9 |
| ở đâu | 75 | 41.3 | 58.0 | 38.2 | 61.0 | 50.0 | 21.8 |
| bao nhiêu | 49 | 40.8 | 58.4 | 40.6 | 67.6 | 41.2 | 9.4 |
| vì sao | 155 | 33.5 | 52.8 | 24.8 | 52.1 | 54.3 | 27.5 |
| như thế nào | 117 | 32.5 | 48.6 | 23.1 | 47.3 | 51.3 | 34.6 |
| cái gì | 563 | 39.8 | 58.2 | 31.3 | 57.8 | 59.0 | 25.4 |
| khác | 23 | 26.1 | 30.3 | 25.0 | 29.9 | 33.3 | 55.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 56.6 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.5%

## r2m_hybrid_k1_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:09:00", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_hybrid_k1_test_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_hybrid_k5_test_rs.jsonl", "refusal_delta": -0.14, "refusal_delta_chosen_on": "dev (r2m_hybrid_k1_dev_rs.jsonl)", "source": "r2m_hybrid_k1_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 36.5 | 49.2 | 23.4 | 41.9 | 65.7 | 40.8 |
| VN | 420 | 38.8 | 51.2 | 28.6 | 46.6 | 61.5 | 36.2 |
| TG | 866 | 35.5 | 48.3 | 20.9 | 39.6 | 67.7 | 43.0 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 43.2 | 53.1 | 28.8 | 43.5 | 72.4 | 42.4 |
| ai | 216 | 45.8 | 54.9 | 32.6 | 46.2 | 72.2 | 34.0 |
| ở đâu | 75 | 41.3 | 55.7 | 36.4 | 55.9 | 55.0 | 29.1 |
| bao nhiêu | 49 | 36.7 | 51.6 | 28.1 | 50.9 | 52.9 | 31.2 |
| vì sao | 155 | 29.0 | 42.7 | 16.5 | 35.9 | 58.7 | 44.0 |
| như thế nào | 117 | 31.6 | 45.4 | 12.8 | 33.4 | 69.2 | 47.4 |
| cái gì | 563 | 35.0 | 49.0 | 21.5 | 41.7 | 65.3 | 42.1 |
| khác | 23 | 21.7 | 26.0 | 15.0 | 19.9 | 66.7 | 65.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **67.6%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 60.7 · khi tìm sai: 2.4
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.0%

## r2m_hybrid_k3_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:09:00", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_hybrid_k3_test_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2m_hybrid_k5_test_rs.jsonl", "refusal_delta": -0.14, "refusal_delta_chosen_on": "dev (r2m_hybrid_k3_dev_rs.jsonl)", "source": "r2m_hybrid_k3_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 36.5 | 51.3 | 27.7 | 49.2 | 55.9 | 28.3 |
| VN | 420 | 38.6 | 53.1 | 32.1 | 53.2 | 53.1 | 24.1 |
| TG | 866 | 35.5 | 50.3 | 25.6 | 47.2 | 57.2 | 30.3 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 42.0 | 57.0 | 30.5 | 52.8 | 65.5 | 27.1 |
| ai | 216 | 45.8 | 56.1 | 40.3 | 55.7 | 56.9 | 22.2 |
| ở đâu | 75 | 36.0 | 49.5 | 32.7 | 51.2 | 45.0 | 27.3 |
| bao nhiêu | 49 | 38.8 | 54.5 | 37.5 | 61.5 | 41.2 | 15.6 |
| vì sao | 155 | 30.3 | 48.1 | 20.2 | 45.5 | 54.3 | 30.3 |
| như thế nào | 117 | 30.8 | 45.5 | 20.5 | 42.6 | 51.3 | 34.6 |
| cái gì | 563 | 35.5 | 51.5 | 25.4 | 48.5 | 58.4 | 29.0 |
| khác | 23 | 17.4 | 26.1 | 15.0 | 25.0 | 33.3 | 50.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **86.7%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 56.0 · khi tìm sai: 4.5
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.5%

## r2m_hybrid_k5_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:09:00", "model": "models/r2_lr1e-4_e8", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2m_hybrid_k5_test_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.14, "refusal_delta_chosen_on": "dev (r2m_hybrid_k5_dev_rs.jsonl)", "source": "r2m_hybrid_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 36.7 | 51.7 | 28.9 | 50.7 | 54.1 | 25.8 |
| VN | 420 | 39.0 | 53.8 | 33.4 | 54.9 | 51.5 | 21.4 |
| TG | 866 | 35.6 | 50.7 | 26.6 | 48.6 | 55.4 | 28.0 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 43.2 | 58.3 | 32.2 | 54.7 | 65.5 | 25.4 |
| ai | 216 | 45.4 | 56.2 | 41.0 | 57.2 | 54.2 | 19.4 |
| ở đâu | 75 | 36.0 | 50.7 | 32.7 | 52.7 | 45.0 | 21.8 |
| bao nhiêu | 49 | 38.8 | 54.5 | 37.5 | 61.5 | 41.2 | 15.6 |
| vì sao | 155 | 31.0 | 49.4 | 21.1 | 47.3 | 54.3 | 26.6 |
| như thế nào | 117 | 28.2 | 42.9 | 20.5 | 42.6 | 43.6 | 33.3 |
| cái gì | 563 | 36.1 | 52.1 | 26.7 | 49.8 | 57.2 | 27.2 |
| khác | 23 | 26.1 | 34.8 | 25.0 | 35.0 | 33.3 | 40.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **90.2%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 55.7 · khi tìm sai: 4.1
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.3%

## r2noimp_gold_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:18:35", "model": "models/r2_noimp", "split": "test", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2noimp_gold_test_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.16, "refusal_delta_chosen_on": "dev (r2noimp_gold_dev_rs.jsonl)", "source": "r2noimp_gold_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 34.8 | 51.6 | 34.9 | 59.2 | 34.6 | 20.4 |
| VN | 420 | 37.6 | 52.2 | 40.0 | 61.0 | 32.3 | 16.6 |
| TG | 866 | 33.5 | 51.3 | 32.5 | 58.3 | 35.7 | 22.3 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 39.8 | 54.3 | 50.8 | 72.5 | 17.2 | 11.9 |
| ai | 216 | 43.1 | 50.7 | 45.8 | 57.4 | 37.5 | 25.7 |
| ở đâu | 75 | 33.3 | 51.8 | 34.5 | 59.7 | 30.0 | 16.4 |
| bao nhiêu | 49 | 34.7 | 55.2 | 37.5 | 68.9 | 29.4 | 6.2 |
| vì sao | 155 | 25.2 | 44.8 | 25.7 | 53.6 | 23.9 | 17.4 |
| như thế nào | 117 | 26.5 | 45.9 | 17.9 | 47.1 | 43.6 | 38.5 |
| cái gì | 563 | 35.9 | 54.6 | 34.6 | 61.6 | 38.7 | 19.0 |
| khác | 23 | 26.1 | 41.2 | 30.0 | 47.4 | 0.0 | 15.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 59.2 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.6%

## r2noimp_hybrid_k1_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:22:43", "model": "models/r2_noimp", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2noimp_hybrid_k1_test_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2noimp_hybrid_k5_test_rs.jsonl", "refusal_delta": -0.64, "refusal_delta_chosen_on": "dev (r2noimp_hybrid_k1_dev_rs.jsonl)", "source": "r2noimp_hybrid_k1_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 34.3 | 44.5 | 20.1 | 34.8 | 65.9 | 53.4 |
| VN | 420 | 35.2 | 44.5 | 22.4 | 35.8 | 63.8 | 51.4 |
| TG | 866 | 33.8 | 44.5 | 18.9 | 34.4 | 66.9 | 54.4 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 40.9 | 47.6 | 27.1 | 37.1 | 69.0 | 55.9 |
| ai | 216 | 43.1 | 47.6 | 29.9 | 36.6 | 69.4 | 50.7 |
| ở đâu | 75 | 34.7 | 50.8 | 23.6 | 45.6 | 65.0 | 38.2 |
| bao nhiêu | 49 | 38.8 | 51.6 | 28.1 | 47.7 | 58.8 | 37.5 |
| vì sao | 155 | 28.4 | 37.7 | 16.5 | 29.7 | 56.5 | 56.9 |
| như thế nào | 117 | 28.2 | 42.4 | 5.1 | 26.4 | 74.4 | 66.7 |
| cái gì | 563 | 33.0 | 44.3 | 18.7 | 35.0 | 65.3 | 53.3 |
| khác | 23 | 17.4 | 28.7 | 10.0 | 23.0 | 66.7 | 65.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **67.6%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 50.6 · khi tìm sai: 1.8
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 99.1%

## r2noimp_hybrid_k3_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:22:43", "model": "models/r2_noimp", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2noimp_hybrid_k3_test_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2noimp_hybrid_k5_test_rs.jsonl", "refusal_delta": -0.66, "refusal_delta_chosen_on": "dev (r2noimp_hybrid_k3_dev_rs.jsonl)", "source": "r2noimp_hybrid_k3_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 35.0 | 46.6 | 24.6 | 41.4 | 58.1 | 43.4 |
| VN | 420 | 36.9 | 47.7 | 27.6 | 43.2 | 57.7 | 40.3 |
| TG | 866 | 34.1 | 46.1 | 23.1 | 40.5 | 58.4 | 44.9 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 40.9 | 48.8 | 30.5 | 42.3 | 62.1 | 47.5 |
| ai | 216 | 47.2 | 51.9 | 37.5 | 44.5 | 66.7 | 41.0 |
| ở đâu | 75 | 34.7 | 50.2 | 27.3 | 48.5 | 55.0 | 30.9 |
| bao nhiêu | 49 | 36.7 | 49.3 | 31.2 | 50.5 | 47.1 | 31.2 |
| vì sao | 155 | 26.5 | 41.1 | 17.4 | 38.2 | 47.8 | 39.4 |
| như thế nào | 117 | 28.2 | 44.5 | 9.0 | 33.4 | 66.7 | 57.7 |
| cái gì | 563 | 33.7 | 46.2 | 23.6 | 41.6 | 56.6 | 44.1 |
| khác | 23 | 17.4 | 28.7 | 15.0 | 28.0 | 33.3 | 55.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **86.7%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 47.5 · khi tìm sai: 1.7
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.7%

## r2noimp_hybrid_k5_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:22:43", "model": "models/r2_noimp", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2noimp_hybrid_k5_test_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.64, "refusal_delta_chosen_on": "dev (r2noimp_hybrid_k5_dev_rs.jsonl)", "source": "r2noimp_hybrid_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 34.7 | 46.7 | 25.6 | 43.0 | 54.9 | 40.9 |
| VN | 420 | 36.9 | 47.8 | 29.0 | 44.8 | 54.6 | 38.3 |
| TG | 866 | 33.6 | 46.2 | 24.0 | 42.2 | 55.0 | 42.2 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 40.9 | 49.3 | 32.2 | 44.7 | 58.6 | 44.1 |
| ai | 216 | 46.3 | 51.5 | 37.5 | 45.3 | 63.9 | 39.6 |
| ở đâu | 75 | 34.7 | 50.2 | 27.3 | 48.5 | 55.0 | 29.1 |
| bao nhiêu | 49 | 36.7 | 49.9 | 34.4 | 54.6 | 41.2 | 25.0 |
| vì sao | 155 | 27.1 | 42.2 | 19.3 | 40.8 | 45.7 | 35.8 |
| như thế nào | 117 | 26.5 | 42.7 | 9.0 | 33.4 | 61.5 | 57.7 |
| cái gì | 563 | 33.4 | 46.4 | 24.6 | 43.3 | 53.2 | 41.5 |
| khác | 23 | 21.7 | 33.1 | 20.0 | 33.0 | 33.3 | 50.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **90.2%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 47.6 · khi tìm sai: 1.6
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.6%

## r2ood_gold_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:23:43", "model": "models/r2_ood", "split": "test", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2ood_gold_test_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.4, "refusal_delta_chosen_on": "dev (r2ood_gold_dev_rs.jsonl)", "source": "r2ood_gold_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 44.9 | 58.0 | 32.1 | 51.2 | 73.2 | 34.6 |
| VN | 420 | 47.1 | 59.1 | 38.3 | 55.6 | 66.9 | 31.7 |
| TG | 866 | 43.8 | 57.5 | 29.1 | 49.1 | 76.2 | 36.0 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 51.1 | 63.5 | 39.0 | 57.4 | 75.9 | 27.1 |
| ai | 216 | 50.9 | 59.1 | 41.7 | 54.0 | 69.4 | 32.6 |
| ở đâu | 75 | 45.3 | 58.4 | 36.4 | 54.2 | 70.0 | 29.1 |
| bao nhiêu | 49 | 46.9 | 57.9 | 43.8 | 60.6 | 52.9 | 21.9 |
| vì sao | 155 | 36.1 | 49.7 | 23.9 | 43.2 | 65.2 | 36.7 |
| như thế nào | 117 | 35.9 | 51.0 | 17.9 | 40.6 | 71.8 | 46.2 |
| cái gì | 563 | 46.0 | 60.9 | 31.5 | 53.1 | 78.6 | 34.4 |
| khác | 23 | 34.8 | 46.5 | 25.0 | 38.5 | 100.0 | 55.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 51.2 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.7%

## r2ood_hybrid_k1_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:28:19", "model": "models/r2_ood", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2ood_hybrid_k1_test_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2ood_hybrid_k5_test_rs.jsonl", "refusal_delta": -0.44, "refusal_delta_chosen_on": "dev (r2ood_hybrid_k1_dev_rs.jsonl)", "source": "r2ood_hybrid_k1_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 40.8 | 51.1 | 22.7 | 37.6 | 81.2 | 49.3 |
| VN | 420 | 42.4 | 52.0 | 27.2 | 41.2 | 76.2 | 46.6 |
| TG | 866 | 40.1 | 50.7 | 20.4 | 35.8 | 83.6 | 50.6 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 42.0 | 52.0 | 22.0 | 36.9 | 82.8 | 50.8 |
| ai | 216 | 46.3 | 54.1 | 30.6 | 42.3 | 77.8 | 43.1 |
| ở đâu | 75 | 44.0 | 55.3 | 30.9 | 46.3 | 80.0 | 38.2 |
| bao nhiêu | 49 | 42.9 | 49.7 | 31.2 | 41.8 | 64.7 | 40.6 |
| vì sao | 155 | 36.1 | 44.7 | 19.3 | 31.4 | 76.1 | 50.5 |
| như thế nào | 117 | 33.3 | 46.2 | 10.3 | 29.6 | 79.5 | 60.3 |
| cái gì | 563 | 41.4 | 52.7 | 21.8 | 38.2 | 85.5 | 50.0 |
| khác | 23 | 26.1 | 37.8 | 15.0 | 28.5 | 100.0 | 70.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **67.6%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 54.6 · khi tìm sai: 2.1
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.9%

## r2ood_hybrid_k3_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:28:19", "model": "models/r2_ood", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2ood_hybrid_k3_test_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2ood_hybrid_k5_test_rs.jsonl", "refusal_delta": -0.42, "refusal_delta_chosen_on": "dev (r2ood_hybrid_k3_dev_rs.jsonl)", "source": "r2ood_hybrid_k3_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 41.8 | 53.6 | 27.7 | 44.8 | 72.9 | 37.5 |
| VN | 420 | 44.5 | 55.4 | 33.8 | 49.6 | 68.5 | 33.4 |
| TG | 866 | 40.4 | 52.7 | 24.8 | 42.5 | 75.1 | 39.5 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 44.3 | 54.0 | 30.5 | 44.9 | 72.4 | 35.6 |
| ai | 216 | 47.7 | 55.8 | 38.2 | 50.4 | 66.7 | 31.2 |
| ở đâu | 75 | 42.7 | 54.9 | 32.7 | 49.3 | 70.0 | 32.7 |
| bao nhiêu | 49 | 42.9 | 51.5 | 40.6 | 53.8 | 47.1 | 25.0 |
| vì sao | 155 | 34.2 | 46.5 | 20.2 | 37.7 | 67.4 | 38.5 |
| như thế nào | 117 | 34.2 | 47.9 | 16.7 | 37.3 | 69.2 | 48.7 |
| cái gì | 563 | 42.8 | 56.0 | 26.2 | 45.2 | 80.3 | 38.2 |
| khác | 23 | 34.8 | 46.5 | 25.0 | 38.5 | 100.0 | 60.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **86.7%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 51.4 · khi tìm sai: 1.9
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.5%

## r2ood_hybrid_k5_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:28:19", "model": "models/r2_ood", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2ood_hybrid_k5_test_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.42, "refusal_delta_chosen_on": "dev (r2ood_hybrid_k5_dev_rs.jsonl)", "source": "r2ood_hybrid_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 41.8 | 53.7 | 28.6 | 45.9 | 71.2 | 34.7 |
| VN | 420 | 44.8 | 55.7 | 35.2 | 51.1 | 66.2 | 31.0 |
| TG | 866 | 40.4 | 52.7 | 25.5 | 43.3 | 73.6 | 36.5 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 44.3 | 54.0 | 32.2 | 46.6 | 69.0 | 33.9 |
| ai | 216 | 46.8 | 55.4 | 37.5 | 50.5 | 65.3 | 29.2 |
| ở đâu | 75 | 44.0 | 56.6 | 34.5 | 51.8 | 70.0 | 29.1 |
| bao nhiêu | 49 | 42.9 | 51.5 | 40.6 | 53.8 | 47.1 | 21.9 |
| vì sao | 155 | 35.5 | 48.2 | 22.0 | 40.1 | 67.4 | 35.8 |
| như thế nào | 117 | 33.3 | 47.2 | 16.7 | 37.4 | 66.7 | 44.9 |
| cái gì | 563 | 43.0 | 56.0 | 27.4 | 46.2 | 78.0 | 35.4 |
| khác | 23 | 34.8 | 46.5 | 25.0 | 38.5 | 100.0 | 55.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **90.2%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 50.6 · khi tìm sai: 2.7
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.7%

## r2s13_gold_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:29:22", "model": "models/r2_s13", "split": "test", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s13_gold_test_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.22, "refusal_delta_chosen_on": "dev (r2s13_gold_dev_rs.jsonl)", "source": "r2s13_gold_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 42.8 | 55.8 | 30.0 | 48.9 | 71.2 | 37.9 |
| VN | 420 | 46.4 | 59.0 | 37.6 | 55.8 | 66.2 | 31.4 |
| TG | 866 | 41.0 | 54.3 | 26.3 | 45.6 | 73.6 | 41.0 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 45.5 | 55.8 | 33.9 | 49.3 | 69.0 | 39.0 |
| ai | 216 | 52.3 | 58.9 | 43.1 | 52.9 | 70.8 | 37.5 |
| ở đâu | 75 | 46.7 | 59.9 | 36.4 | 54.4 | 75.0 | 30.9 |
| bao nhiêu | 49 | 46.9 | 61.0 | 46.9 | 68.4 | 47.1 | 12.5 |
| vì sao | 155 | 33.5 | 49.8 | 19.3 | 42.4 | 67.4 | 34.9 |
| như thế nào | 117 | 34.2 | 47.7 | 16.7 | 37.0 | 69.2 | 52.6 |
| cái gì | 563 | 42.6 | 57.8 | 28.2 | 50.1 | 75.1 | 37.9 |
| khác | 23 | 30.4 | 37.0 | 25.0 | 32.6 | 66.7 | 55.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 48.9 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.6%

## r2s13_hybrid_k1_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:33:56", "model": "models/r2_s13", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s13_hybrid_k1_test_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2s13_hybrid_k5_test_rs.jsonl", "refusal_delta": -0.2, "refusal_delta_chosen_on": "dev (r2s13_hybrid_k1_dev_rs.jsonl)", "source": "r2s13_hybrid_k1_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 39.0 | 49.7 | 22.7 | 38.2 | 75.2 | 47.8 |
| VN | 420 | 41.4 | 51.5 | 28.3 | 42.9 | 70.8 | 44.5 |
| TG | 866 | 37.8 | 48.8 | 19.9 | 35.9 | 77.3 | 49.4 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 46.6 | 51.5 | 30.5 | 37.8 | 79.3 | 52.5 |
| ai | 216 | 45.4 | 51.8 | 31.9 | 41.7 | 72.2 | 44.4 |
| ở đâu | 75 | 44.0 | 57.5 | 30.9 | 49.3 | 80.0 | 34.5 |
| bao nhiêu | 49 | 40.8 | 51.8 | 31.2 | 48.0 | 58.8 | 34.4 |
| vì sao | 155 | 32.3 | 43.8 | 16.5 | 32.9 | 69.6 | 46.8 |
| như thế nào | 117 | 32.5 | 45.3 | 9.0 | 28.2 | 79.5 | 60.3 |
| cái gì | 563 | 38.2 | 50.8 | 21.0 | 39.2 | 76.9 | 47.7 |
| khác | 23 | 26.1 | 27.2 | 15.0 | 16.2 | 100.0 | 75.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **67.6%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 55.7 · khi tìm sai: 1.5
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.4%

## r2s13_hybrid_k3_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:33:56", "model": "models/r2_s13", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s13_hybrid_k3_test_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2s13_hybrid_k5_test_rs.jsonl", "refusal_delta": -0.24, "refusal_delta_chosen_on": "dev (r2s13_hybrid_k3_dev_rs.jsonl)", "source": "r2s13_hybrid_k3_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 39.7 | 51.5 | 25.6 | 42.7 | 70.9 | 39.6 |
| VN | 420 | 41.9 | 53.3 | 32.8 | 49.2 | 62.3 | 33.4 |
| TG | 866 | 38.6 | 50.6 | 22.1 | 39.6 | 75.1 | 42.5 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 45.5 | 54.2 | 30.5 | 43.6 | 75.9 | 42.4 |
| ai | 216 | 50.0 | 55.8 | 40.3 | 49.0 | 69.4 | 36.8 |
| ở đâu | 75 | 45.3 | 57.7 | 34.5 | 51.4 | 75.0 | 29.1 |
| bao nhiêu | 49 | 40.8 | 51.8 | 40.6 | 57.5 | 41.2 | 18.8 |
| vì sao | 155 | 31.0 | 45.7 | 16.5 | 37.5 | 65.2 | 35.8 |
| như thế nào | 117 | 33.3 | 46.9 | 14.1 | 34.5 | 71.8 | 52.6 |
| cái gì | 563 | 38.2 | 51.8 | 22.1 | 41.7 | 74.6 | 41.3 |
| khác | 23 | 26.1 | 32.7 | 20.0 | 27.6 | 66.7 | 50.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **86.7%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 49.0 · khi tìm sai: 2.2
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.2%

## r2s13_hybrid_k5_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:33:56", "model": "models/r2_s13", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s13_hybrid_k5_test_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.24, "refusal_delta_chosen_on": "dev (r2s13_hybrid_k5_dev_rs.jsonl)", "source": "r2s13_hybrid_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 39.6 | 51.6 | 26.4 | 43.9 | 68.9 | 37.1 |
| VN | 420 | 42.4 | 54.3 | 33.4 | 50.6 | 62.3 | 31.0 |
| TG | 866 | 38.2 | 50.4 | 22.9 | 40.6 | 72.1 | 40.0 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 45.5 | 54.8 | 30.5 | 44.4 | 75.9 | 40.7 |
| ai | 216 | 48.1 | 54.2 | 40.3 | 49.4 | 63.9 | 34.7 |
| ở đâu | 75 | 46.7 | 59.5 | 36.4 | 53.9 | 75.0 | 25.5 |
| bao nhiêu | 49 | 38.8 | 49.8 | 40.6 | 57.5 | 35.3 | 18.8 |
| vì sao | 155 | 31.6 | 47.5 | 17.4 | 40.0 | 65.2 | 33.0 |
| như thế nào | 117 | 32.5 | 46.1 | 14.1 | 34.5 | 69.2 | 51.3 |
| cái gì | 563 | 38.7 | 52.3 | 23.1 | 42.7 | 74.0 | 38.5 |
| khác | 23 | 26.1 | 32.7 | 25.0 | 32.6 | 33.3 | 45.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **90.2%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 48.4 · khi tìm sai: 2.5
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.1%

## r2s7_gold_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:34:56", "model": "models/r2_s7", "split": "test", "context": "gold", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s7_gold_test_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.2, "refusal_delta_chosen_on": "dev (r2s7_gold_dev_rs.jsonl)", "source": "r2s7_gold_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 40.8 | 56.3 | 32.2 | 54.7 | 59.9 | 28.5 |
| VN | 420 | 44.3 | 58.6 | 39.7 | 60.4 | 54.6 | 21.7 |
| TG | 866 | 39.1 | 55.2 | 28.6 | 52.0 | 62.5 | 31.8 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 44.3 | 55.3 | 39.0 | 55.4 | 55.2 | 30.5 |
| ai | 216 | 50.9 | 59.2 | 44.4 | 56.8 | 63.9 | 25.0 |
| ở đâu | 75 | 40.0 | 56.5 | 30.9 | 53.4 | 65.0 | 27.3 |
| bao nhiêu | 49 | 38.8 | 58.4 | 37.5 | 67.6 | 41.2 | 12.5 |
| vì sao | 155 | 32.9 | 49.5 | 25.7 | 49.3 | 50.0 | 30.3 |
| như thế nào | 117 | 30.8 | 49.8 | 16.7 | 45.3 | 59.0 | 38.5 |
| cái gì | 563 | 41.0 | 58.8 | 31.3 | 56.9 | 63.0 | 27.9 |
| khác | 23 | 39.1 | 47.9 | 35.0 | 45.1 | 66.7 | 40.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **100.0%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 54.7 · khi tìm sai: —
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.1%

## r2s7_hybrid_k1_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:39:36", "model": "models/r2_s7", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 1, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s7_hybrid_k1_test_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2s7_hybrid_k5_test_rs.jsonl", "refusal_delta": -0.2, "refusal_delta_chosen_on": "dev (r2s7_hybrid_k1_dev_rs.jsonl)", "source": "r2s7_hybrid_k1_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 37.1 | 49.1 | 23.2 | 40.6 | 67.9 | 43.9 |
| VN | 420 | 40.5 | 51.9 | 29.7 | 46.2 | 64.6 | 38.6 |
| TG | 866 | 35.5 | 47.7 | 20.1 | 37.8 | 69.5 | 46.4 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 44.3 | 52.7 | 30.5 | 43.1 | 72.4 | 44.1 |
| ai | 216 | 45.4 | 53.7 | 31.2 | 43.7 | 73.6 | 36.1 |
| ở đâu | 75 | 38.7 | 54.4 | 29.1 | 50.5 | 65.0 | 34.5 |
| bao nhiêu | 49 | 34.7 | 49.9 | 25.0 | 48.2 | 52.9 | 34.4 |
| vì sao | 155 | 31.0 | 41.8 | 20.2 | 35.5 | 56.5 | 45.9 |
| như thế nào | 117 | 29.9 | 47.4 | 9.0 | 35.2 | 71.8 | 48.7 |
| cái gì | 563 | 36.2 | 48.8 | 22.1 | 40.2 | 68.2 | 46.4 |
| khác | 23 | 30.4 | 35.8 | 20.0 | 26.1 | 100.0 | 60.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **67.6%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 59.2 · khi tìm sai: 1.5
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 97.1%

## r2s7_hybrid_k3_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:39:36", "model": "models/r2_s7", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 3, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s7_hybrid_k3_test_thr", "refusal_scores": true, "device": "cuda", "derived_from": "r2s7_hybrid_k5_test_rs.jsonl", "refusal_delta": -0.2, "refusal_delta_chosen_on": "dev (r2s7_hybrid_k3_dev_rs.jsonl)", "source": "r2s7_hybrid_k3_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 37.5 | 51.4 | 27.7 | 47.9 | 59.1 | 30.9 |
| VN | 420 | 40.2 | 53.1 | 34.1 | 52.8 | 53.8 | 25.2 |
| TG | 866 | 36.1 | 50.5 | 24.6 | 45.4 | 61.7 | 33.7 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 40.9 | 51.2 | 33.9 | 49.3 | 55.2 | 25.4 |
| ai | 216 | 47.7 | 55.9 | 40.3 | 52.6 | 62.5 | 26.4 |
| ở đâu | 75 | 37.3 | 52.3 | 29.1 | 49.5 | 60.0 | 27.3 |
| bao nhiêu | 49 | 38.8 | 55.2 | 37.5 | 62.7 | 41.2 | 12.5 |
| vì sao | 155 | 31.0 | 45.5 | 22.0 | 42.7 | 52.2 | 33.9 |
| như thế nào | 117 | 29.9 | 48.4 | 15.4 | 43.1 | 59.0 | 38.5 |
| cái gì | 563 | 36.4 | 51.7 | 25.1 | 47.2 | 61.8 | 32.3 |
| khác | 23 | 34.8 | 43.6 | 30.0 | 40.1 | 66.7 | 45.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **86.7%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 54.8 · khi tìm sai: 2.3
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.2%

## r2s7_hybrid_k5_test_thr

`{"commit": "ce83d68-dirty", "time": "2026-11-09 05:39:36", "model": "models/r2_s7", "split": "test", "context": "retrieved", "mode": "hybrid", "k": 5, "batch_size": 16, "num_beams": 1, "limit": null, "run": "r2s7_hybrid_k5_test_thr", "refusal_scores": true, "device": "cuda", "refusal_delta": -0.2, "refusal_delta_chosen_on": "dev (r2s7_hybrid_k5_dev_rs.jsonl)", "source": "r2s7_hybrid_k5_test_rs.jsonl"}`

| Tập | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| Tổng | 1286 | 37.3 | 51.2 | 28.3 | 48.5 | 57.4 | 28.4 |
| VN | 420 | 40.5 | 53.5 | 35.2 | 54.0 | 52.3 | 22.8 |
| TG | 866 | 35.8 | 50.2 | 25.0 | 45.8 | 59.9 | 31.2 |

**Theo loại câu hỏi**

| Loại | n | EM | F1 | HasAns_EM | HasAns_F1 | NoAns_acc | HasAns_abstain |
|---|---|---|---|---|---|---|---|
| khi nào | 88 | 40.9 | 51.4 | 33.9 | 49.6 | 55.2 | 23.7 |
| ai | 216 | 46.8 | 55.2 | 40.3 | 53.0 | 59.7 | 25.0 |
| ở đâu | 75 | 37.3 | 52.9 | 29.1 | 50.3 | 60.0 | 23.6 |
| bao nhiêu | 49 | 38.8 | 55.2 | 37.5 | 62.7 | 41.2 | 12.5 |
| vì sao | 155 | 32.3 | 47.4 | 23.9 | 45.4 | 52.2 | 29.4 |
| như thế nào | 117 | 29.1 | 47.6 | 15.4 | 43.3 | 56.4 | 35.9 |
| cái gì | 563 | 36.1 | 51.1 | 25.6 | 47.3 | 59.5 | 30.0 |
| khác | 23 | 39.1 | 47.9 | 35.0 | 45.1 | 66.7 | 40.0 |

- Đoạn đúng nằm trong các đoạn đã đọc: **90.2%** (câu trả lời được)
- HasAns-F1 khi tìm đúng: 53.5 · khi tìm sai: 2.0
- Dự đoán xuất hiện nguyên văn trong đoạn đã đọc: 98.1%
