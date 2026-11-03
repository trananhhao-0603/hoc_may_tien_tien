# Thống kê dữ liệu QA (tokenizer `VietAI/vit5-base`)

## Số câu hỏi theo split

| Split | Số bài | Số đoạn | Trả lời được | Không trả lời được | Tổng | VN / TG (câu hỏi) |
|---|---|---|---|---|---|---|
| train | 23 | 1,491 | 6,347 | 3,047 | 9,394 | 2,610 / 6,784 |
| dev | 8 | 179 | 892 | 437 | 1,329 | 407 / 922 |
| test | 7 | 192 | 887 | 399 | 1,286 | 420 / 866 |

Bài **không có câu hỏi có nhãn** (chỉ có trong split test không nhãn của ViQuAD; đoạn văn vẫn nằm trong kho tri thức): Edward II của Anh (train), Đế quốc Nga (test), Đế quốc Đức (train)

## Độ dài (token)

| Thành phần | p50 | p90 | p95 | p99 | max | TB |
|---|---|---|---|---|---|---|
| Đoạn văn | 201 | 328 | 379 | 478 | 895 | 220 |
| Câu hỏi | 16 | 24 | 26 | 32 | 71 | 17 |
| Đáp án | 9 | 30 | 39 | 59 | 143 | 13 |
| Input Reader, 1 đoạn | 231 | 365 | 418 | 516 | 930 | 251 |

## Tỉ lệ bị cắt cụt

| Ngưỡng | Input 1 đoạn bị cắt | Ngưỡng | Đáp án bị cắt |
|---|---|---|---|
| 256 | 37.8% | 16 | 27.26% |
| 384 | 7.8% | 32 | 8.10% |
| 512 | 1.0% | 64 | 0.69% |
| 1024 | 0.0% | 128 | 0.01% |

## Ghép k đoạn vào một input (ước lượng)

| k | p50 | p90 |
|---|---|---|
| 1 | 229 | 364 |
| 3 | 631 | 1020 |
| 5 | 1033 | 1676 |
