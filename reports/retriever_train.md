# Đánh giá Retriever — split `train` (6347 câu trả lời được, 1862 đoạn)

R@k tính bằng %. ms/câu: thời gian chấm điểm toàn kho trên CPU (đã gồm tách từ, nhúng câu hỏi).

| Cấu hình | R@1 | R@3 | R@5 | R@10 | R@20 | MRR | ms/câu |
|---|---|---|---|---|---|---|---|
| BM25 · âm tiết | 63.6 | 77.9 | 82.4 | 86.9 | 90.7 | 0.721 | 3.1 |
| BM25 · tách từ | 64.1 | 77.7 | 81.8 | 86.7 | 90.1 | 0.722 | 2.9 |
| Dense · văn bản thô | 45.4 | 61.7 | 68.1 | 75.7 | 82.1 | 0.559 | 7.0 |
| Dense · tách từ | 49.9 | 65.5 | 71.8 | 79.1 | 85.4 | 0.600 | 6.4 |
| Hybrid · BM25 âm tiết + Dense tách từ (k=60, w=1) | 61.5 | 78.8 | 84.6 | 91.6 | 96.0 | 0.719 | 9.5 |
| Hybrid · BM25 tách từ + Dense tách từ (k=60, w=1) | 61.8 | 78.7 | 84.0 | 90.4 | 95.1 | 0.719 | 9.3 |
| **Hybrid · BM25 âm tiết + Dense tách từ (k=5, w=0.7) — chọn** | 65.1 | 83.0 | 88.0 | 92.5 | 95.7 | 0.752 | 9.5 |

**Tốt nhất theo R@5:** **Hybrid · BM25 âm tiết + Dense tách từ (k=5, w=0.7) — chọn**

## Theo tiểu miền

| Cấu hình | Miền | n | R@1 | R@5 | MRR |
|---|---|---|---|---|---|
| BM25 · âm tiết | VN | 1751 | 51.0 | 73.0 | 0.611 |
| BM25 · âm tiết | TG | 4596 | 68.4 | 86.0 | 0.763 |
| BM25 · tách từ | VN | 1751 | 55.5 | 75.3 | 0.645 |
| BM25 · tách từ | TG | 4596 | 67.4 | 84.3 | 0.751 |
| Dense · văn bản thô | VN | 1751 | 39.5 | 62.1 | 0.502 |
| Dense · văn bản thô | TG | 4596 | 47.7 | 70.4 | 0.581 |
| Dense · tách từ | VN | 1751 | 45.1 | 68.8 | 0.560 |
| Dense · tách từ | TG | 4596 | 51.7 | 72.9 | 0.615 |
| Hybrid · BM25 âm tiết + Dense tách từ (k=60, w=1) | VN | 1751 | 55.2 | 80.2 | 0.663 |
| Hybrid · BM25 âm tiết + Dense tách từ (k=60, w=1) | TG | 4596 | 63.9 | 86.2 | 0.740 |
| Hybrid · BM25 tách từ + Dense tách từ (k=60, w=1) | VN | 1751 | 56.3 | 80.4 | 0.671 |
| Hybrid · BM25 tách từ + Dense tách từ (k=60, w=1) | TG | 4596 | 63.9 | 85.4 | 0.737 |
| **Hybrid · BM25 âm tiết + Dense tách từ (k=5, w=0.7) — chọn** | VN | 1751 | 56.9 | 80.9 | 0.676 |
| **Hybrid · BM25 âm tiết + Dense tách từ (k=5, w=0.7) — chọn** | TG | 4596 | 68.1 | 90.7 | 0.781 |
