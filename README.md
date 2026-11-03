# Hệ hỏi đáp Lịch sử tiếng Việt (Retriever + Reader ViT5)

Người dùng nhập một câu hỏi lịch sử. Hệ thống tìm đoạn văn liên quan (BM25 + FAISS) rồi dùng ViT5 đã fine-tune để **sinh** câu trả lời (text-to-text). Nếu kho tri thức không có thông tin, hệ thống trả lời "không có câu trả lời".

- Kế hoạch chi tiết: [`PLAN.md`](PLAN.md)
- Đánh giá dự án cũ (DSS sinh trắc nghiệm): [`phan_tich.md`](phan_tich.md)

## Trạng thái

| Giai đoạn | Nội dung | Trạng thái |
|---|---|---|
| 0 | Dọn dẹp, bảo mật, git, `requirements.txt` | ✅ |
| 1 | Chuẩn hoá dữ liệu QA | ⬜ |
| 2 | Retriever | ⬜ |
| 3 | Metric & baseline | ⬜ |
| 4 | Reader ViT5 | ⬜ |
| 5 | Thí nghiệm | ⬜ |
| 6 | Phân tích lỗi & demo | ⬜ |
| 7 | Báo cáo | ⬜ |

## Cấu trúc

```
src/data/        build_corpus.py, split_balanced.py, survey_viquad.py   — xây corpus từ ViQuAD 2.0
src/retriever/   build_index.py                                         — index BM25 + FAISS
tests/           test_build.py, test_survey.py
data/processed/  corpus.parquet (1.862 đoạn), qa_pairs.parquet (13.997 câu hỏi),
                 titles_inventory.csv (bài nào là lịch sử / Việt Nam — đã rà tay), splits_report.txt
legacy/          mã nguồn và dữ liệu của dự án DSS cũ (không dùng tiếp, giữ để tham khảo)
```

## Cài đặt

```bash
# Python 3.12 (khớp Colab). Cài torch trước theo https://pytorch.org/get-started/locally/
pip install -r requirements.txt
```

Trên Colab, torch đã có sẵn, chỉ cần chạy `pip install -r requirements.txt`.

## Chạy test

```bash
python tests/test_build.py
python tests/test_survey.py
```

## Dữ liệu

- Nguồn: [UIT-ViQuAD 2.0](https://huggingface.co/datasets/taidng/UIT-ViQuAD2.0), 38 bài lịch sử (9 bài Việt Nam, 29 bài thế giới).
- Split chia **theo bài** để chống rò rỉ: train 23 bài / dev 8 / test 7 (≈ 80/10/10 số đoạn).
- Tạo lại corpus: `python src/data/build_corpus.py --inventory data/processed/titles_inventory.csv --outdir data/processed`
