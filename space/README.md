---
title: Hỏi đáp Lịch sử tiếng Việt
emoji: 📜
colorFrom: yellow
colorTo: red
sdk: gradio
sdk_version: 6.17.3
python_version: "3.12"
app_file: app.py
pinned: false
---

# Hỏi đáp Lịch sử tiếng Việt

Nhập một câu hỏi lịch sử. Retriever hybrid (BM25 + bi-encoder, gộp bằng RRF) tìm top-k đoạn trong kho 1.862 đoạn
Wikipedia lịch sử, rồi Reader ViT5 đã fine-tune sinh đáp án hoặc trả lời "không có câu trả lời".

Space chạy trên CPU nên mỗi câu mất khoảng 1 giây. Mã nguồn và kết quả đánh giá:
<https://github.com/trananhhao-0603/hoc_may_tien_tien>
