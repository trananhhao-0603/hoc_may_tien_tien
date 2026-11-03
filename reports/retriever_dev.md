# Đánh giá Retriever — split `dev` (892 câu trả lời được, 1862 đoạn)

R@k tính bằng %. ms/câu: thời gian chấm điểm toàn kho trên CPU (đã gồm tách từ, nhúng câu hỏi).

| Cấu hình | R@1 | R@3 | R@5 | R@10 | R@20 | MRR | ms/câu |
|---|---|---|---|---|---|---|---|
| BM25 · âm tiết | 76.1 | 86.5 | 90.4 | 93.5 | 95.2 | 0.824 | 3.0 |
| BM25 · tách từ | 74.8 | 85.1 | 88.7 | 91.5 | 93.5 | 0.809 | 2.9 |
| Dense · văn bản thô | 49.4 | 63.7 | 71.0 | 76.9 | 81.6 | 0.588 | 6.7 |
| Dense · tách từ | 52.2 | 67.5 | 73.7 | 80.6 | 85.2 | 0.617 | 5.9 |
| Hybrid · BM25 âm tiết + Dense tách từ (k=60, w=1) | 67.3 | 82.1 | 86.2 | 92.3 | 96.7 | 0.763 | 8.9 |
| Hybrid · BM25 tách từ + Dense tách từ (k=60, w=1) | 67.4 | 80.9 | 84.8 | 90.7 | 95.2 | 0.755 | 8.7 |
| **Hybrid · BM25 âm tiết + Dense tách từ (k=5, w=0.7) — chọn** | 71.9 | 89.3 | 93.4 | 95.6 | 97.2 | 0.813 | 8.9 |

**Tốt nhất theo R@5:** **Hybrid · BM25 âm tiết + Dense tách từ (k=5, w=0.7) — chọn**

## Theo tiểu miền

| Cấu hình | Miền | n | R@1 | R@5 | MRR |
|---|---|---|---|---|---|
| BM25 · âm tiết | VN | 247 | 83.8 | 94.7 | 0.885 |
| BM25 · âm tiết | TG | 645 | 73.2 | 88.7 | 0.800 |
| BM25 · tách từ | VN | 247 | 85.4 | 95.1 | 0.899 |
| BM25 · tách từ | TG | 645 | 70.7 | 86.2 | 0.774 |
| Dense · văn bản thô | VN | 247 | 67.2 | 84.2 | 0.747 |
| Dense · văn bản thô | TG | 645 | 42.6 | 65.9 | 0.527 |
| Dense · tách từ | VN | 247 | 67.2 | 83.8 | 0.752 |
| Dense · tách từ | TG | 645 | 46.5 | 69.8 | 0.566 |
| Hybrid · BM25 âm tiết + Dense tách từ (k=60, w=1) | VN | 247 | 78.1 | 93.9 | 0.858 |
| Hybrid · BM25 âm tiết + Dense tách từ (k=60, w=1) | TG | 645 | 63.1 | 83.3 | 0.727 |
| Hybrid · BM25 tách từ + Dense tách từ (k=60, w=1) | VN | 247 | 81.4 | 95.5 | 0.875 |
| Hybrid · BM25 tách từ + Dense tách từ (k=60, w=1) | TG | 645 | 62.0 | 80.6 | 0.709 |
| **Hybrid · BM25 âm tiết + Dense tách từ (k=5, w=0.7) — chọn** | VN | 247 | 81.8 | 96.4 | 0.886 |
| **Hybrid · BM25 âm tiết + Dense tách từ (k=5, w=0.7) — chọn** | TG | 645 | 68.1 | 92.2 | 0.785 |
