# Hệ hỏi đáp Lịch sử tiếng Việt (Retriever + Reader ViT5)

Người dùng nhập một câu hỏi lịch sử. **Retriever** hybrid (BM25 âm tiết + bi-encoder tiếng Việt, gộp bằng RRF) tìm
top-k đoạn văn trong kho 1.862 đoạn Wikipedia lịch sử. **Reader** ViT5-base đã fine-tune đọc từng đoạn và *sinh*
câu trả lời, hoặc trả lời "không có câu trả lời" nếu kho không chứa thông tin.

## Kết quả chính (test, chạy một lần)

| Hệ thống | EM | F1 | HasAns-F1 | NoAns-acc |
|---|---|---|---|---|
| Reader R2 + ViQuAD ngoài miền, **đọc đoạn đúng** | 44,6 | 60,3 | 60,1 | 60,7 |
| **Toàn hệ thống**: hybrid top-5 → Reader R2 + ViQuAD ngoài miền | **39,4** | **53,4** | 52,2 | 55,9 |
| Toàn hệ thống với Reader R2 chính (không có dữ liệu ngoài miền) | 36,3 | 51,8 | 51,9 | 51,6 |

Retriever Recall@5 trên test là 90,2%. Trên dev, Reader R2 đạt F1 57,5 khi đọc đoạn đúng, cao hơn baseline trích xuất
XLM-R (51,5) và ViT5 zero-shot (0,4). Mỗi câu hỏi mất khoảng 0,13 s trên RTX 3060 và khoảng 1 s trên CPU.
Bảng đầy đủ, biểu đồ và so sánh với mục tiêu ở [`reports/results.md`](reports/results.md). Phân tích lỗi ở
[`reports/gd6_summary.md`](reports/gd6_summary.md).

Tài liệu khác:
- [`PLAN.md`](PLAN.md): kế hoạch, checkbox từng giai đoạn, các vấn đề phát sinh.
- [`explain.md`](explain.md): giải thích từng bước bằng lời thường.
- [`phan_tich.md`](phan_tich.md): đánh giá dự án cũ (DSS sinh trắc nghiệm).

## Cài đặt

```bash
# Python 3.12. Cài torch trước theo https://pytorch.org/get-started/locally/ (đã kiểm với torch 2.15.0, CUDA 13.2)
pip install -r requirements.txt
```

- `transformers` được ghim ở 4.57.6, vì bản 5.x không tải được tokenizer của ViT5.
- Trên Windows, đặt `PYTHONIOENCODING=utf-8` để in được tiếng Việt.
- Trên Colab, torch có sẵn: chỉ cần `pip install -r requirements.txt` rồi restart runtime.

**Không có trong git** (`.gitignore`): `models/` (checkpoint), `data/index_qa/` (chỉ mục FAISS) và `data/predictions/`
(file dự đoán). Chỉ mục tạo lại được bằng lệnh ở bước 2. Checkpoint phải train lại (bước 4–5), hoặc lấy từ Drive của nhóm.
Mọi số liệu tổng hợp nằm trong `reports/*.json`, đã commit.

## Chạy demo

```bash
python app.py                       # http://127.0.0.1:7860, model mặc định models/r2_ood
python app.py --device cpu --share  # chạy CPU, tạo link công khai tạm thời
```

Demo hiện đáp án, đoạn văn bằng chứng có tô đậm đáp án, bảng top-k nguồn kèm đáp án đọc được ở từng đoạn, và thời
gian từng khâu. Dùng trong code:

```python
from src.pipeline import QAPipeline
qa = QAPipeline.load("models/r2_ood")
qa.answer("Ai là vị vua đầu tiên của nhà Trần?", k=5)["answer_text"]   # 'Trần Thái Tông'
```

## Tái lập kết quả

Các lệnh chạy từ thư mục gốc repo. Thời gian ghi kèm là đo trên RTX 3060.

| # | Bước | Lệnh | Đầu ra |
|---|---|---|---|
| 1 | Dữ liệu (GĐ1) | `python src/data/build_corpus.py --inventory data/processed/titles_inventory.csv --outdir data/processed`<br>`python src/data/length_stats.py` | `data/processed/*.parquet` (đã commit), `reports/data_stats.md` |
| 2 | Retriever (GĐ2) | `python src/retriever/build_index.py` (~4 phút CPU)<br>`python src/retriever/eval_retriever.py --split dev --sweep`<br>`python src/retriever/cache_retrieval.py` | `data/index_qa/`, `reports/retriever_dev.md`, cache top-20 |
| 3 | Baseline (GĐ3) | `python src/reader/baseline_random.py --split dev --context gold` (B0)<br>`python src/reader/infer.py --model VietAI/vit5-base --context gold --run b2_gold_dev` (B2)<br>`python src/reader/train_extractive.py --tune_threshold` (B1, GPU)<br>`python src/eval/evaluate_pipeline.py data/predictions/*_dev.jsonl --out reports/baselines_dev` | `reports/baselines_dev.md` |
| 4 | Reader ViT5 (GĐ4) | `python src/reader/train_seq2seq.py --data r1` / `--data r2` (~45 phút)<br>Colab: `notebooks/colab_train_vit5.ipynb` | `models/{r1,r2}_vit5`, `reports/reader_vit5_dev.md` |
| 5 | Thí nghiệm E1–E6 (GĐ5) | Dò tham số (các ứng viên mà pipeline sẽ chọn):<br>`python src/reader/train_seq2seq.py --data r2 --lr 1e-4 --epochs 8 --output_dir models/r2_lr1e-4_e8`<br>`python src/reader/train_seq2seq.py --data r2 --lr 3e-4 --epochs 5 --output_dir models/r2_lr3e-4_e5`<br>`python scripts/gd5_pipeline.py` (mọi bước GPU còn lại, ~5,5 giờ, bỏ qua bước đã có)<br>`python scripts/gd5_report.py` | `reports/gd5_results.md`, `gd5_{dev,test}.json` |
| 6 | Phân tích lỗi, độ trễ (GĐ6) | `python -m src.eval.error_analysis sample` → chấm tay `reports/error_labels.csv` → `python -m src.eval.error_analysis report`<br>`python scripts/latency.py --device cuda` / `--device cpu`, rồi `--report` | `reports/error_analysis.md`, `reports/latency.md` |
| 7 | Tổng hợp | `python scripts/make_results.py` | `reports/results.md`, `reports/figures/*.png` |

Bước 7 chỉ đọc `reports/*.json` (đã commit), nên chạy được ngay sau khi clone, không cần GPU.

Các lệnh lẻ hay dùng:

```bash
# suy luận toàn hệ thống: hybrid top-5, ghi thêm điểm từ chối
python src/reader/infer.py --model models/r2_ood --split dev --context retrieved --mode hybrid --k 5 --refusal_scores --run r2ood_hybrid_k5_dev_rs
python src/eval/evaluate_pipeline.py data/predictions/r2ood_hybrid_k5_dev_rs.jsonl        # chấm
python src/reader/tune_refusal.py data/predictions/r2ood_hybrid_k5_dev_rs.jsonl --run r2ood_hybrid_k5_dev_thr  # chọn ngưỡng trên dev
python src/eval/bootstrap.py A.jsonl B.jsonl --paired                                      # CI 95% hiệu cặp
```

## Thước đo

EM và F1 tính theo âm tiết, sau khi chuẩn hoá: NFC, chữ thường, thống nhất vị trí dấu thanh ("hòa"/"hoà"), bỏ dấu câu,
gộp khoảng trắng. Dấu thanh vẫn **giữ** khi so khớp. Câu không trả lời được chấm theo kiểu squad_v2: tính là đúng khi
mô hình trả "không có câu trả lời" (hoặc chuỗi rỗng). HasAns và NoAns là chỉ số tính riêng cho hai nhóm câu.

## Dữ liệu

- Nguồn: [UIT-ViQuAD 2.0](https://huggingface.co/datasets/taidng/UIT-ViQuAD2.0), 38 bài lịch sử (9 bài Việt Nam, 29 bài thế giới).
- Chia **theo bài** để chống rò rỉ: train 23 bài, dev 8, test 7. Số câu hỏi có nhãn: 9.394 / 1.329 / 1.286.
- Split `test` chính thức của ViQuAD trên HF **không có nhãn**, nên chỉ lấy đoạn văn của nó đưa vào kho tri thức.
- Mọi lựa chọn cấu hình làm trên dev. Test chỉ chạy một lần ở GĐ5.

## Cấu trúc

```
app.py           demo Gradio
src/pipeline.py  pipeline hoàn chỉnh (retriever + reader) dùng cho demo và đo độ trễ
src/data/        build_corpus.py, split_balanced.py, survey_viquad.py, length_stats.py   — xây corpus, thống kê
src/retriever/   text.py (tách token), build_index.py, hybrid.py (bm25 | dense | hybrid RRF),
                 eval_retriever.py (Recall@k, MRR), cache_retrieval.py (cache top-20 cho Colab)
src/reader/      common.py, baseline_random.py (B0), train_extractive.py (B1 XLM-R),
                 train_seq2seq.py (ViT5 R1/R2, E4 --no_impossible, E5 --ood), infer.py (suy luận ViT5),
                 subset_k.py (suy top-1/3 từ top-5), tune_refusal.py (ngưỡng từ chối)
src/eval/        metrics.py (EM/F1), predictions.py (định dạng .jsonl), qtype.py, evaluate_pipeline.py,
                 bootstrap.py (CI 95%), error_analysis.py (GĐ6)
scripts/         gd5_pipeline.py, gd5_report.py, latency.py, make_results.py
configs/         reader_extractive.yaml, reader_vit5.yaml
notebooks/       colab_train_reader.ipynb (B1), colab_train_vit5.ipynb (R1/R2)
tests/           unit test cho dữ liệu, retriever, metric, reader, ngưỡng, highlight (python -m pytest tests -q)
reports/         mọi bảng kết quả (.md + .json), figures/, error_analysis/
baocao/          báo cáo cuối kỳ (.docx/.pdf) và slide (.pptx)
legacy/          mã nguồn và dữ liệu của dự án DSS cũ (không dùng tiếp, giữ để tham khảo)
```
