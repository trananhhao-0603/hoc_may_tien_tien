# Phân tích lỗi — `r2ood_hybrid_k5_test_rs`

Mẫu ngẫu nhiên 100 câu có EM = 0 (seed 0), chấm tay từng câu. Mỗi câu một nhãn chính.

| Nhóm lỗi | Số câu | % | trong đó VN | TG |
|---|---|---|---|---|
| Tìm sai đoạn: đoạn đúng không có trong top-k | 12 | 12 | 2 | 10 |
| Chọn nhầm đoạn: đoạn đúng có trong top-k nhưng đáp án lấy từ đoạn khác | 7 | 7 | 0 | 7 |
| Đọc sai: có đoạn đúng nhưng trích sai/thiếu/thừa ý | 13 | 13 | 5 | 8 |
| Đọc sai: từ chối nhầm dù đoạn đúng có đáp án | 11 | 11 | 6 | 5 |
| Trả lời câu không có đáp án (bị câu bẫy đánh lừa) | 28 | 28 | 14 | 14 |
| Bịa: đáp án không có trong đoạn đã đọc | 0 | 0 | 0 | 0 |
| Lỗi bộ từ vựng ViT5: ký tự ngoài từ vựng (ç, ā, …) bị rơi khi sinh | 2 | 2 | 0 | 2 |
| Đáp án chuẩn có vấn đề (sai, mơ hồ, câu hỏi lỗi) | 7 | 7 | 1 | 6 |
| Đúng nhưng khác cách viết / chấp nhận được | 20 | 20 | 7 | 13 |

Nhãn gợi ý tự động trùng nhãn chấm tay ở 70% số câu.

F1 trung bình theo nhóm (câu có EM = 0 vẫn có thể có F1 > 0):

| Nhóm | F1 TB |
|---|---|
| retrieval | 3.0 |
| selection | 2.0 |
| reader_span | 35.9 |
| reader_refuse | 0.0 |
| trap | 0.0 |
| tokenizer | 25.0 |
| gold_issue | 6.8 |
| paraphrase | 75.6 |

## Nhãn tự động trên toàn bộ 779 câu sai của test

Chỉ dựa vào cờ (không đọc tay), nên không tách được nhóm đáp án chuẩn có vấn đề hay khác cách viết. Các câu này nằm trong `reader_span`/`trap`.

| Nhãn tự động | Số câu | % |
|---|---|---|
| reader_span | 290 | 37 |
| trap | 173 | 22 |
| reader_refuse | 128 | 16 |
| selection | 88 | 11 |
| retrieval | 86 | 11 |
| hallucination | 14 | 2 |

Đáp án chuẩn của test không qua được tokenizer ViT5 nguyên vẹn (encode rồi decode bị mất ký tự): **9/887** (1.0%). Với những câu này, Reader không bao giờ đạt EM = 1. Ví dụ: `Histoire de la Révolution Française của Michelet và nhất là quyển Histoire des Girondins của Alphonse de Lamartine`; `cử Trần Khắc Chung (陳克終) cướp công chúa về`; `François II`; `Chấp trì chân lý (sa. satyāgraha)`; `Mahātmā`

## Ví dụ tiêu biểu

- **retrieval** (`validation:0012-0001-0003`, #10): Đoạn đúng không có trong top-5 nên Reader từ chối
- **selection** (`validation:0014-0008-0001`, #22): Đoạn đúng ở hạng 1, nhưng đáp án lấy từ đoạn hạng khác (nhà Đông Hán) có điểm cao hơn
- **selection** (`validation:0012-0014-0001`, #78): Đoạn đúng ở hạng 5, nhưng Reader lấy đáp án từ một đoạn về Việt Minh không liên quan
- **reader_span** (`train:0134-0012-0002`, #1): Có đoạn đúng nhưng trích câu liền sau (bổ nhiệm Hội đồng Tư vấn) thay vì câu trả lời (bãi chức)
- **reader_refuse** (`train:0065-0012-0003`, #16): Đoạn đúng ở hạng 5 có đáp án, nhưng Reader từ chối ở cả 5 đoạn
- **reader_refuse** (`train:0065-0003-0005`, #57): Cần suy luận hai bước (ông nội = cha của Trần Thừa); Reader từ chối
- **trap** (`train:0062-0009-0006`, #15): Câu bẫy đổi 'rút về' thành 'vào Thăng Long'; Reader vẫn trả lời 'tháng 12'
- **trap** (`train:0039-0021-0006`, #68): Câu bẫy đổi 'đại biểu' thành 'người dân'; Reader trả lời 361
- **tokenizer** (`validation:0012-0002-0008`, #7): 'Mahātmā' thành 'Mahtm': ký tự ā không có trong từ vựng ViT5 nên bị rơi
- **tokenizer** (`train:0134-0017-0001`, #8): 'François II' thành 'Franois II': ký tự ç bị rơi
- **gold_issue** (`validation:0014-0017-0006`, #2): Câu hỏi 'lí do gì' nhưng đáp án chuẩn là mệnh đề thời gian; dự đoán ('bảo vệ họ khỏi tham vọng của Hoàng đế') hợp lý hơn
- **gold_issue** (`train:0134-0004-0006`, #11): Câu được gắn nhãn không trả lời được nhưng đoạn văn ghi rõ mẹ của Mary là Catherine xứ Aragon; dự đoán đúng
- **paraphrase** (`train:0134-0022-0003`, #3): Thừa 'như là' ở đầu, nội dung trùng khớp (F1 0.97)
- **paraphrase** (`train:0039-0010-0002`, #4): 'Hiệp ước Versailles' so với 'Versailles'
