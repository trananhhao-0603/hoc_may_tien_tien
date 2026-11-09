# Độ trễ pipeline (Giai đoạn 6)

Mỗi lần một câu hỏi, đơn vị ms, trung vị (p90 trong ngoặc). Câu hỏi ngẫu nhiên từ dev; 5 câu khởi động không tính. Reader đọc k đoạn trong một batch. Tạo bởi `scripts/latency.py`.

- **CPU**: Intel(R) Core(TM) i5-14600KF, torch 2.15.0+cu132, 14 luồng, n = 50 câu, model `r2_ood`
- **CUDA**: NVIDIA GeForce RTX 3060, torch 2.15.0+cu132, 14 luồng, n = 100 câu, model `r2_ood`

| Khâu | CPU k=1 | CPU k=5 | CUDA k=1 | CUDA k=5 |
|---|---|---|---|---|
| BM25 | 5 (7) | 5 (8) | 4 (6) | 4 (6) |
| Dense (mã hoá câu hỏi + cosine) | 46 (57) | 47 (58) | 6 (7) | 6 (7) |
| RRF + top-k | 0.7 (0.7) | 1 (1) | 0.4 (0.5) | 0.6 (0.7) |
| **Truy hồi (tổng)** | 51 (64) | 54 (65) | 11 (14) | 11 (13) |
| **Reader ViT5 (k đoạn)** | 208 (395) | 969 (1281) | 66 (175) | 118 (264) |
| **Tổng** | 250 (435) | 1029 (1336) | 78 (187) | 128 (274) |
