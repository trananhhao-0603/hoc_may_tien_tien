# Hệ hỏi đáp Lịch sử tiếng Việt (Retriever + Reader ViT5)

Người dùng nhập một câu hỏi lịch sử. Hệ thống tìm đoạn văn liên quan (BM25 + FAISS) rồi dùng ViT5 đã fine-tune để **sinh** câu trả lời (text-to-text). Nếu kho tri thức không có thông tin, hệ thống trả lời "không có câu trả lời".

- Kế hoạch chi tiết: [`PLAN.md`](PLAN.md)
- Đánh giá dự án cũ (DSS sinh trắc nghiệm): [`phan_tich.md`](phan_tich.md)

## Trạng thái

| Giai đoạn | Nội dung | Trạng thái |
|---|---|---|
| 0 | Dọn dẹp, bảo mật, git, `requirements.txt` | ✅ |
| 1 | Chuẩn hoá dữ liệu QA | ✅ |
| 2 | Retriever (hybrid BM25 + dense, R@5 dev 93,4%) | ✅ |
| 3 | Metric & baseline | ⬜ |
| 4 | Reader ViT5 | ⬜ |
| 5 | Thí nghiệm | ⬜ |
| 6 | Phân tích lỗi & demo | ⬜ |
| 7 | Báo cáo | ⬜ |

## Cấu trúc

```
src/data/        build_corpus.py, split_balanced.py, survey_viquad.py   — xây corpus từ ViQuAD 2.0
                 length_stats.py                                        — thống kê độ dài -> reports/data_stats.md
src/retriever/   text.py         — tách token (âm tiết / tách từ underthesea)
                 build_index.py  — build data/index_qa/ (meta + FAISS, cả 3 split)
                 hybrid.py       — Retriever: bm25 | dense | hybrid (RRF có trọng số)
                 eval_retriever.py — Recall@k, MRR -> reports/retriever_<split>.md
tests/           test_build.py, test_survey.py, test_retriever.py (logic, không cần dữ liệu)
                 test_split_leak.py (kiểm tra dữ liệu thật: chống rò rỉ, nhãn hợp lệ)
data/processed/  corpus.parquet (1.862 đoạn), qa_pairs.parquet (12.009 câu hỏi có nhãn),
                 titles_inventory.csv (bài nào là lịch sử / Việt Nam — đã rà tay), splits_report.txt
reports/         data_stats.md, retriever_{dev,train}.md/.json, retriever_*_sweep.csv
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
python tests/test_split_leak.py
python tests/test_retriever.py
```

## Retriever

```bash
python src/retriever/build_index.py                     # ~4 phút trên CPU -> data/index_qa/
python src/retriever/eval_retriever.py --split dev --sweep
```

```python
from hybrid import Retriever          # sys.path gồm src/retriever
r = Retriever.load("data/index_qa")   # mặc định: hybrid, BM25 âm tiết + dense tách từ, RRF k=5, w_dense=0.7
r.search("Chiến thắng Điện Biên Phủ diễn ra năm nào?", k=5)
```

## Dữ liệu

- Nguồn: [UIT-ViQuAD 2.0](https://huggingface.co/datasets/taidng/UIT-ViQuAD2.0), 38 bài lịch sử (9 bài Việt Nam, 29 bài thế giới).
- Split chia **theo bài** để chống rò rỉ: train 23 bài / dev 8 / test 7 (≈ 80/10/10 số đoạn); câu hỏi có nhãn: 9.394 / 1.329 / 1.286.
- Split `test` chính thức của ViQuAD trên HF **không có nhãn**: chỉ dùng đoạn văn (kho tri thức), bỏ câu hỏi.
- Tạo lại corpus: `python src/data/build_corpus.py --inventory data/processed/titles_inventory.csv --outdir data/processed`
