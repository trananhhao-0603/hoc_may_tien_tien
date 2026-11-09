# GĐ6 — Phân tích lỗi, demo, độ trễ

Hệ thống phân tích: **r2ood + hybrid top-5, greedy, trên test** (`r2ood_hybrid_k5_test_rs`, EM 39,4 / F1 53,4).
Bảng gốc: `reports/error_analysis.md` (tạo bởi `python -m src.eval.error_analysis report`),
nhãn chấm tay `reports/error_labels.csv`, mẫu để đọc `reports/error_analysis/r2ood_hybrid_k5_test_rs_sample.md`.
Độ trễ: `reports/latency.md`.

## 1. Phân tích 100 câu sai (viết tay từ các bảng trên)

Lấy ngẫu nhiên 100 trong 779 câu có EM = 0 (seed 0), đọc từng câu, gán một nhãn chính.

| Nhóm | % | Nhận xét |
|---|---|---|
| Trả lời câu bẫy (câu không trả lời được) | 28 | Nhóm lớn nhất. Câu bẫy của ViQuAD chỉ đổi một chi tiết so với đoạn văn ("rút về" → "vào Thăng Long", "đại biểu" → "người dân", "hằng năm" → "hàng tháng"). Reader vẫn trích đáp án mồi. |
| Đúng nhưng khác cách viết | 20 | Thừa hoặc thiếu vài chữ ở biên ("năm 1910" so với "1910", "Hiệp ước Versailles" so với "Versailles"). F1 TB của nhóm này 75,6. EM đánh giá thấp hệ thống. |
| Đọc sai span (có đoạn đúng) | 13 | Trích câu bên cạnh, thiếu nửa sau của đáp án dài, hoặc thừa một mệnh đề có nội dung khác. |
| Tìm sai đoạn (đoạn đúng ngoài top-5) | 12 | Câu hỏi ngắn, chung chung ("Khuyết điểm của vua Louis là gì?", "Thái độ cuối đời của nhà vua ra sao?"). 10/12 câu thuộc lịch sử thế giới. |
| Từ chối nhầm | 11 | Thường là câu cần diễn giải hoặc suy luận: "Hoa Kỳ" so với "phiến quân Mỹ", ông nội = cha của cha, tính thuế theo bậc ruộng. |
| Chọn nhầm đoạn | 7 | Đoạn đúng có trong top-5, có khi ở hạng 1, nhưng một đoạn khác cho đáp án có log-prob cao hơn. Điểm của các đoạn không so sánh được với nhau. |
| Đáp án chuẩn có vấn đề | 7 | Câu gắn nhãn "không trả lời được" nhưng đoạn có đáp án (#11, #93). Đáp án chuẩn không trả lời câu hỏi (#2, #87). Câu hỏi mơ hồ (#31). |
| Lỗi bộ từ vựng ViT5 | 2 | "François" → "Franois", "Mahātmā" → "Mahtm". 9/887 đáp án chuẩn của test (1,0%) không encode/decode nguyên vẹn được. |
| Bịa (đáp án không có trong đoạn) | 0 | Không gặp trong mẫu. Trên toàn bộ câu sai, cờ tự động thấy 14/779 câu (2%). Trong đó 12 câu là lỗi bộ từ vựng (khớp lại được với đoạn văn khi bỏ ký tự ngoài từ vựng). Chỉ 2 câu bịa thật. |

**Kết luận:**
1. **Khâu Reader là nút thắt chính, không phải Retriever.** Lỗi do retriever (tìm sai + chọn nhầm đoạn) chiếm 19%. Lỗi đọc (câu bẫy + span + từ chối nhầm) chiếm 52%.
2. **Câu bẫy là điểm yếu lớn nhất.** Đây là nơi NoAns còn kém (55,9% trên test). Câu bẫy gần như trùng đoạn văn, chỉ lệch một thực thể hoặc một chi tiết. Cải tiến khả dĩ: tăng tỉ lệ câu bẫy khi train, hoặc thêm bước kiểm tra lại (verifier) giữa câu hỏi và câu chứa đáp án.
3. **Khoảng 27% "lỗi" không hẳn là lỗi** (20% khác cách viết, 7% đáp án chuẩn có vấn đề). Nếu chấm bằng người, độ chính xác thật cao hơn EM 39,4. F1 phản ánh tốt hơn EM, nhưng vẫn phạt đáp án đúng mà dài hơn.
4. **Chọn đoạn bằng log-prob trung bình chưa tốt.** 7% số câu sai có đoạn đúng trong top-5 mà vẫn sai vì chọn nhầm. Có thể cộng điểm retriever vào điểm chọn, hoặc huấn luyện Reader đọc nhiều đoạn cùng lúc (FiD). Việc này cần chọn lại trên dev nên chưa làm.
5. **Hậu xử lý "lấy nguyên văn từ đoạn"** sửa được lỗi bộ từ vựng: khi dự đoán không khớp nguyên văn đoạn đã đọc, thay bằng chuỗi gốc trong đoạn (`src/pipeline.highlight_span`, chạy bằng `python -m src.eval.error_analysis snap`):

   | Run | Số câu đổi | EM trước → sau | F1 trước → sau |
   |---|---|---|---|
   | r2ood_gold_dev_rs | 1 | 44.24 → 44.24 | 58.94 → 58.94 |
   | r2ood_hybrid_k5_dev_rs | 2 | 39.43 → 39.43 | 52.92 → 52.92 |
   | r2ood_gold_test_rs | 7 | 44.56 → 45.02 | 60.28 → 60.48 |
   | r2ood_hybrid_k5_test_rs | 12 | 39.42 → 39.89 | 53.37 → 53.58 |
   | r2m_gold_test_rs | 9 | 40.44 → 40.82 | 57.37 → 57.55 |
   | r2m_hybrid_k5_test_rs | 10 | 36.31 → 36.70 | 51.79 → 51.97 |

   Trên dev không đổi gì. Ý tưởng này lại nảy ra từ việc đọc lỗi trên test. Vì vậy **không coi là cải tiến** và không sửa số liệu GĐ5 (mức tăng +0,2 F1 cũng nhỏ hơn nhiều so với độ dao động giữa các seed). Demo dùng nó để hiển thị đúng tên riêng.

6. **Hướng phát triển: phạt hạng đoạn khi chọn đáp án (chỉ thử trên DEV).** Ý tưởng sửa nhóm lỗi "chọn nhầm đoạn": chọn đáp án theo điểm Reader − λ·(hạng − 1) thay vì chỉ theo điểm Reader. Lấy lại từ file dự đoán có sẵn bằng `python -m src.eval.error_analysis rankpen`, không chạy lại mô hình:

   | λ | EM | F1 | HasAns_F1 | NoAns_acc |
   |---|---|---|---|---|
   | 0 (hiện tại) | 39.43 | 52.92 | 57.32 | 43.94 |
   | 0.02 | 40.03 | 53.91 | 58.80 | 43.94 |
   | 0.05 | 40.18 | 54.02 | 58.95 | 43.94 |
   | 0.2 | 40.33 | 54.06 | 59.02 | 43.94 |
   | 1.0 | 40.33 | 53.91 | 58.79 | 43.94 |

   F1 dev tăng khoảng +1,1 và ổn định với mọi λ ≥ 0,02. NoAns không đổi vì phạt hạng không ảnh hưởng tới việc từ chối. **Cố ý không chấm trên test**: test đã dùng một lần ở GĐ5, và nhóm quyết định (09/11) giữ nguyên số chính thức F1 test 53,4. Báo cáo ghi ý này ở mục Hướng phát triển, kèm nhận xét: mục tiêu F1 ≥ 55 (PLAN §7) là ước lượng ban đầu và chưa đạt.

## 2. Demo Gradio

`python app.py` (mặc định `models/r2_ood`, cổng 7860; có `--device cpu`, `--share`).
Demo gồm: ô câu hỏi, thanh chọn k, đáp án kèm hạng và tên bài của đoạn nguồn, đoạn bằng chứng có tô đậm đáp án,
bảng top-k (điểm RRF, đáp án Reader đọc ở từng đoạn, điểm Reader) và thời gian từng khâu.
Câu hỏi mẫu lấy từ dev, kèm một câu ngoài phạm vi kho ("Ai là người sáng lập ra Microsoft?") để thấy hệ thống từ chối.
Code pipeline dùng chung với phép đo độ trễ: `src/pipeline.py`.

## 3. Độ trễ

Chi tiết ở `reports/latency.md` (`python scripts/latency.py --device cuda|cpu`, rồi `--report`).
Mỗi lần một câu hỏi, đo trung vị trên câu hỏi dev. Máy dùng RTX 3060 12GB và i5-14600KF (14 luồng).

| Khâu (ms, trung vị) | CPU k=1 | CPU k=5 | GPU k=1 | GPU k=5 |
|---|---|---|---|---|
| Truy hồi (BM25 + dense + RRF) | 51 | 54 | 11 | 11 |
| Reader ViT5 | 208 | 969 | 66 | 118 |
| **Tổng** | **250** | **1029** | **78** | **128** |

- **Reader chiếm 80–95% thời gian.** Truy hồi rẻ vì kho chỉ có 1.862 đoạn: BM25 khoảng 5 ms, mã hoá câu hỏi bằng bi-encoder khoảng 6 ms trên GPU và 46 ms trên CPU (gồm cả tách từ underthesea).
- Trên CPU, thời gian Reader gần như tỉ lệ với k (208 → 969 ms). Trên GPU, 5 đoạn chạy cùng một batch nên chỉ tăng gần gấp đôi (66 → 118 ms).
- Cấu hình chính (top-5) mất khoảng 0,13 s trên GPU và khoảng 1 s trên CPU, đủ dùng cho demo tương tác. Trên CPU, k = 3 là lựa chọn dung hoà: theo GĐ5, F1 test của k = 3 gần bằng k = 5.
