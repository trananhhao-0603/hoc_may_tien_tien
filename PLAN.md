# PLAN — Hệ hỏi đáp Lịch sử tiếng Việt (Retriever + Reader ViT5)

> Ngày lập: 03/11/2026
> Đổi đề tài từ "DSS sinh câu hỏi trắc nghiệm" sang **hỏi đáp mở (open-domain QA)**: người dùng nhập câu hỏi, hệ thống tìm đoạn văn liên quan rồi sinh câu trả lời.
> Phần học máy chính là **Reader text-to-text (ViT5)**.
> Tham chiếu: `phan_tich.md` (đánh giá dự án cũ), [HF QA tutorial](https://huggingface.co/docs/transformers/en/tasks/question_answering) (dùng làm baseline trích xuất).

---

## 1. Phát biểu bài toán

```
Input : câu hỏi tiếng Việt về lịch sử
          "Chiến thắng Điện Biên Phủ diễn ra năm nào?"
Output: câu trả lời ngắn + đoạn văn làm bằng chứng
          "1954"   (nguồn: ctx_…, bài "Chiến tranh Đông Dương")
          hoặc "không có câu trả lời" nếu kho tri thức không có thông tin
```

```
Câu hỏi ──► [Retriever]  BM25 + FAISS + RRF  ──► top-k đoạn văn
                                                     │
                                                     ▼
            [Reader]  ViT5 fine-tune (text-to-text)
            "<q> câu hỏi </q> <ctx> đoạn 1 … đoạn k </ctx>"  ──►  "đáp án"
```

**Câu hỏi nghiên cứu**
- RQ1: Reader sinh đáp án (ViT5) so với Reader trích xuất (encoder + dự đoán vị trí): bên nào tốt hơn trên dữ liệu lịch sử tiếng Việt?
- RQ2: Truy hồi kết hợp (BM25 + FAISS) có tốt hơn từng phương pháp riêng không? Sai số của toàn hệ thống đến từ khâu tìm hay khâu đọc?
- RQ3: Huấn luyện với câu không trả lời được có giúp mô hình biết từ chối thay vì bịa không?
- RQ4: Thêm dữ liệu ViQuAD ngoài miền lịch sử có giúp ích không? Hiệu năng trên bài Việt Nam và bài thế giới khác nhau thế nào?

---

## 2. Dữ liệu (đã có sẵn)

| Tài nguyên | Số lượng | Dùng cho |
|---|---|---|
| `corpus.parquet` | 1.862 đoạn / 38 bài (VN 536, TG 1.326) | Kho tri thức cho Retriever |
| `qa_pairs.parquet` | 13.997 câu hỏi (10.114 trả lời được, 3.883 không trả lời được) | Train/đánh giá Reader |
| Split theo bài | train 11.103 / dev 1.536 / test 1.358 câu hỏi | Giữ nguyên |
| `corpus_all.parquet` | toàn bộ ViQuAD (~176–184 bài) | Thí nghiệm thêm dữ liệu ngoài miền (RQ4) |

**Nguyên tắc chống rò rỉ cho hỏi đáp** (khác với dự án cũ):
- **Kho đoạn văn chứa cả 3 split.** Đây là tri thức hệ thống được phép tra cứu.
- **Cặp hỏi–đáp của test chỉ dùng để đánh giá**, không bao giờ dùng để train hay chọn siêu tham số.
- Dữ liệu ngoài miền (RQ4) chỉ lấy từ các bài **không** thuộc 38 bài lịch sử.
- Baseline trích xuất chỉ được dùng checkpoint **chưa từng fine-tune trên ViQuAD**. Ví dụ có thể dùng `xlm-roberta-base`; không dùng các checkpoint dạng "vi-mrc" vì có thể đã thấy dữ liệu test.

---

## 3. Giữ / Bỏ từ dự án cũ

| Thành phần | Quyết định |
|---|---|
| `build_corpus.py`, `split_balanced.py`, `survey_viquad.py` | **Giữ** |
| `corpus.parquet`, `qa_pairs.parquet`, `splits_report.txt` | **Giữ** |
| `build_index.py`, `HybridRetriever` (trong `rag_llm.py`) | **Giữ, tách ra** thành `src/retriever/` |
| Notebook ViT5 | **Viết lại** thành Reader (dùng lại phần tokenize/Trainer) |
| `rule_based.py`, `rag_llm.py` (phần sinh), `mcq_schema.py`, NER/KB, `distractor_pool.pkl`, `data/generated/` | **Chuyển vào `legacy/`**, không dùng tiếp |
| Verifier, AHP/TOPSIS, ILP, dashboard DSS | **Bỏ** |

---

## 4. Cấu trúc thư mục mới

```
HMTT/
├── PLAN.md, README.md, requirements.txt, .gitignore, .env.example
├── configs/            reader_vit5.yaml, reader_extractive.yaml, retriever.yaml
├── data/
│   ├── processed/      corpus.parquet, qa_pairs.parquet (+ qa_clean.parquet)
│   ├── index_qa/       faiss.index, bm25.pkl, index_meta.parquet   ← index cả 3 split
│   └── predictions/    {run_name}.jsonl
├── src/
│   ├── data/           build_corpus.py, split_balanced.py, clean_qa.py
│   ├── retriever/      build_index.py, hybrid.py, eval_retriever.py
│   ├── reader/         train_seq2seq.py, train_extractive.py, infer.py
│   ├── eval/           metrics.py (EM/F1 tiếng Việt, squad_v2), evaluate_pipeline.py
│   └── app/            demo.py (Gradio)
├── notebooks/          colab_train_reader.ipynb (chỉ gọi src/, không chép code)
├── tests/              test_metrics.py, test_retriever.py, test_split_leak.py
├── reports/            results.md, figures/, error_analysis.md
└── legacy/             mã nguồn DSS cũ
```

---

## 5. Các giai đoạn

### Giai đoạn 0 — Dọn dẹp & bảo mật (½ ngày)
- [x] Gỡ OpenAI API key khỏi `rag_llm.py` (ngày 03/11/2026). Key thuộc **người khác**, nên đã/sẽ báo chủ key tự thu hồi. Dự án mới **không cần** key OpenAI; chỉ dùng mô hình mở trên Hugging Face.
- [x] `git init`; thêm `.gitignore` (cho `__pycache__`, `models/`, `data/index*`, `.env`).
- [x] Làm phẳng `files_v1/files_v1/`, chuyển mã cũ vào `legacy/`.
- [x] Viết `requirements.txt` ghim phiên bản cố định cho `transformers`, `datasets`, `evaluate`, `faiss-cpu`, `sentence-transformers`, `rank-bm25`. Phải dùng cùng phiên bản trên máy local và Colab.

**Xong khi:** repo sạch, không còn khoá bí mật, `pip install -r requirements.txt` chạy được.

### Giai đoạn 1 — Chuẩn hoá dữ liệu QA (1 ngày)
- [ ] Điều tra khoảng 1.988 câu trả lời được nhưng `answer_span_ok = False`. Nghi do `normalize_vi` sửa context mà không sửa `answer_start`. Sửa lại hoặc tính lại span.
- [ ] Tạo `qa_clean.parquet` với các cột: `qa_id, question, context_id, answer_text, answer_start, is_impossible, split, is_vietnam`.
- [ ] Nhãn đích cho Reader sinh: `answer_text`, hoặc `"không có câu trả lời"` nếu `is_impossible`.
- [ ] Viết test chống rò rỉ: không `qa_id` nào nằm ở 2 split; mỗi bài chỉ thuộc 1 split.
- [ ] Thống kê độ dài câu hỏi, đáp án và đoạn văn (theo token ViT5) để chọn `max_length`.

**Xong khi:** có `qa_clean.parquet`, test chống rò rỉ chạy qua, có bảng thống kê độ dài.

### Giai đoạn 2 — Retriever (2 ngày)
- [ ] Tách `HybridRetriever` ra `src/retriever/hybrid.py`, cho phép chọn chế độ `bm25 | dense | hybrid`.
- [ ] Build `data/index_qa/` trên **cả 3 split** (1.862 đoạn).
- [ ] Cải thiện BM25: tách từ tiếng Việt (ví dụ `underthesea.word_tokenize`) thay cho `.split()`, rồi so sánh hai cách.
- [ ] `eval_retriever.py`: đo Recall@{1,3,5,10} và MRR trên câu hỏi **dev/test trả lời được**. Đoạn đúng (gold) là `context_id` của câu hỏi.
- [ ] Chọn cấu hình retriever và k bằng tập **dev**.

**Xong khi:** có bảng Recall@k cho 3 chế độ × 2 cách tách từ; đã chốt cấu hình.

### Giai đoạn 3 — Metric & baseline (2 ngày)
- [ ] `metrics.py`: EM và F1 theo token, chuẩn hoá tiếng Việt (NFC, chữ thường, bỏ dấu câu, gộp khoảng trắng; **không** bỏ dấu thanh). Ghi riêng: HasAns-EM/F1, NoAns-accuracy (theo kiểu `squad_v2`).
- [ ] Unit test cho metric (các trường hợp: "năm 1954" so với "1954", chữ hoa/thường, đáp án rỗng).
- [ ] **Baseline B0:** chọn ngẫu nhiên một cụm danh từ hoặc năm trong đoạn văn đứng đầu (mốc sàn).
- [ ] **Baseline B1 — Reader trích xuất:** fine-tune `xlm-roberta-base` theo HF QA tutorial, trên đoạn văn đúng (gold).
- [ ] **Baseline B2 — ViT5 zero-shot:** `VietAI/vit5-base` chưa fine-tune.

**Xong khi:** `evaluate_pipeline.py` nhận một file dự đoán và in ra đủ bảng chỉ số.

### Giai đoạn 4 — Reader ViT5 text-to-text (3–4 ngày, Colab GPU)
- [ ] `train_seq2seq.py` dùng `Seq2SeqTrainer`; cấu hình đọc từ `configs/reader_vit5.yaml`.
  - Input: `"<q> {question} </q> <ctx> {passages} </ctx>"`, max 512 token (thử 1024 nếu dùng A100).
  - Target: đáp án, max 32 token.
  - Mặc định: lr 3e-5, effective batch 32, 5 epoch, early stopping theo F1 trên dev, bf16, seed cố định.
- [ ] **R1 — train trên đoạn văn đúng** (cách đơn giản nhất).
- [ ] **R2 — train trên đoạn văn retriever tìm được** (gold + top-k, có xáo trộn). Mục đích: Reader quen với nhiễu khi chạy thực tế.
- [ ] `infer.py`: chạy toàn hệ thống (retrieve → read), lưu `data/predictions/{run}.jsonl` gồm câu hỏi, đoạn văn tìm được, dự đoán, đáp án chuẩn, độ trễ.
- [ ] Lưu checkpoint tốt nhất lên Drive; ghi lại cấu hình và commit hash vào mỗi lần chạy.

**Xong khi:** R1 và R2 có kết quả EM/F1 trên dev; checkpoint tải lại và chạy suy luận được.

### Giai đoạn 5 — Thí nghiệm (3–4 ngày)
Mọi lựa chọn đều làm trên **dev**. **Test chỉ chạy một lần** cho các cấu hình cuối cùng.

| ID | Thí nghiệm | Trả lời RQ |
|---|---|---|
| E1 | B1 (trích xuất) vs R1/R2 (ViT5 sinh), đọc trên đoạn văn đúng | RQ1 |
| E2 | Toàn hệ thống: retriever {BM25, dense, hybrid} × k {1, 3, 5} → Reader tốt nhất | RQ2 |
| E3 | Đọc trên đoạn văn đúng vs đoạn văn tự tìm, để tách sai số tìm và sai số đọc | RQ2 |
| E4 | Train có vs không có câu không trả lời được; đo NoAns-acc và HasAns-F1 | RQ3 |
| E5 | Train chỉ dữ liệu lịch sử vs thêm ViQuAD ngoài miền | RQ4 |
| E6 | Tách kết quả theo VN / TG, theo loại câu hỏi (khi nào / ai / ở đâu / vì sao) | RQ4 |
| E7 (tuỳ chọn) | `vit5-base` vs `vit5-large` | — |

- [ ] Chạy 3 seed cho cấu hình chính, báo cáo trung bình ± độ lệch chuẩn.
- [ ] Bootstrap khoảng tin cậy 95% cho EM/F1 trên test (test chỉ có khoảng 1.358 câu, 7 bài).

### Giai đoạn 6 — Phân tích lỗi & demo (2 ngày)
- [ ] Lấy ngẫu nhiên 100 câu trả lời sai, phân loại lỗi: tìm sai đoạn / đọc sai / đáp án chuẩn có vấn đề / đúng nhưng khác cách viết / bịa.
- [ ] Demo Gradio: ô nhập câu hỏi → đáp án + đoạn văn bằng chứng (tô đậm) + top-k nguồn.
- [ ] Đo độ trễ của từng khâu trên CPU và GPU.

### Giai đoạn 7 — Báo cáo (2–3 ngày)
- [ ] `reports/results.md`: các bảng E1–E6 và biểu đồ (Recall@k, F1 theo k, theo miền).
- [ ] Viết báo cáo theo mục: Giới thiệu, Liên quan (ViQuAD, DPR/RAG, T5/ViT5), Dữ liệu, Phương pháp, Thí nghiệm, Phân tích lỗi, Hạn chế, Kết luận.
- [ ] README mới: cài đặt, tái lập từng bảng kết quả bằng một lệnh.

---

## 6. Lịch dự kiến

Tổng khoảng 3–4 tuần. Hạn nộp chưa biết, cần điều chỉnh khi có.

| Tuần | Giai đoạn | Kết quả đầu ra |
|---|---|---|
| 1 | 0, 1, 2 | Repo sạch, `qa_clean.parquet`, bảng Recall@k |
| 2 | 3, 4 | Metric + baseline, ViT5 R1/R2 trên dev |
| 3 | 5 | Kết quả E1–E6 |
| 4 | 6, 7 | Phân tích lỗi, demo, báo cáo |

---

## 7. Chỉ số mục tiêu (ước lượng, cần kiểm chứng ở Giai đoạn 3)

| Chỉ số | Mục tiêu tối thiểu |
|---|---|
| Retriever Recall@5 (test) | ≥ 80% |
| Reader ViT5 trên đoạn văn đúng, HasAns-F1 | ≥ 70 |
| Toàn hệ thống F1 (test) | ≥ 55 |
| NoAns-accuracy | ≥ 60% |
| ViT5 fine-tune so với zero-shot | Cải thiện rõ ràng, có ý nghĩa thống kê |

---

## 8. Rủi ro & cách xử lý

| Rủi ro | Khả năng | Cách xử lý |
|---|---|---|
| Tập test nhỏ (7 bài), kết quả dao động | Cao | Bootstrap CI, nhiều seed, báo cáo thêm trên dev |
| Ghép k đoạn vượt 512 token | Cao | Cắt mỗi đoạn theo ngân sách token; thử 1024; hoặc đọc từng đoạn rồi chọn đáp án có điểm cao nhất |
| Lỗi phiên bản `transformers` trên Colab (như dự án cũ) | Trung bình | Ghim phiên bản trong `requirements.txt` và dùng đúng nó trên Colab |
| Không có GPU mạnh | Trung bình | `vit5-base` + 512 token chạy được trên T4; bỏ E7 |
| ViT5 bịa đáp án không có trong đoạn văn | Trung bình | Đo tỉ lệ "đáp án có trong đoạn văn", thêm ràng buộc khi sinh, phân tích ở Giai đoạn 6 |
| Đáp án chuẩn của ViQuAD có lỗi hoặc nhiều cách viết | Thấp–TB | F1 theo token, ghi nhận trong phân tích lỗi |

---

## 9. Sản phẩm bàn giao

1. Mã nguồn tái lập được (`src/`, `configs/`, `tests/`, `requirements.txt`).
2. Notebook Colab train Reader.
3. Checkpoint ViT5 Reader tốt nhất (lưu trên Drive/HF Hub, không đưa vào git).
4. File dự đoán + `reports/results.md` + phân tích lỗi.
5. Demo Gradio.
6. Báo cáo cuối kỳ.

---

## 10. Việc làm ngay

1. Thu hồi API key cũ.
2. Giai đoạn 0: dọn repo, `git init`, `requirements.txt`.
3. Giai đoạn 1: điều tra khoảng 1.988 span lỗi trong `qa_pairs.parquet`.
