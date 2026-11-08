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
| `qa_pairs.parquet` | **12.009** câu hỏi có nhãn (8.126 trả lời được, 3.883 không trả lời được) — đã sửa ở Giai đoạn 1 | Train/đánh giá Reader |
| Split theo bài | train 9.394 / dev 1.329 / test 1.286 câu hỏi | Giữ nguyên |
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
│   ├── processed/      corpus.parquet, qa_pairs.parquet
│   ├── index_qa/       faiss.index, bm25.pkl, index_meta.parquet   ← index cả 3 split
│   └── predictions/    {run_name}.jsonl
├── src/
│   ├── data/           build_corpus.py, split_balanced.py, survey_viquad.py, length_stats.py
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

### Giai đoạn 1 — Chuẩn hoá dữ liệu QA (1 ngày) ✅
- [x] Điều tra 1.988 câu "trả lời được" nhưng `answer_span_ok = False`. **Giả thuyết ban đầu sai.** Nguyên nhân thật: split `test` chính thức của ViQuAD trên HF **không có nhãn** (`answers=None`, `is_impossible` luôn `False`). → `build_corpus.py` bỏ các câu không nhãn nhưng giữ đoạn văn trong kho tri thức.
- [x] Lỗi kèm theo: code cũ đọc trường `plausible` (không tồn tại) → `plausible_answer` rỗng ở mọi dòng. Sửa thành `plausible_answers` (giờ có đủ 3.883/3.883).
- [x] `qa_id` dùng `id` gốc của ViQuAD, ghép tên split (`train:0013-0001-0001`), vì `id` chỉ duy nhất trong từng split chính thức (152 id bị trùng giữa train và validation).
- [x] 74 câu có `answer_start` lệch (chủ yếu ±1 ký tự do chuẩn hoá khoảng trắng): căn lại theo lần xuất hiện gần nhất nếu lệch ≤ 20 ký tự. 1 câu lệch 608 ký tự → đánh `answer_span_ok=False`, không đoán.
- [x] Không tạo file `qa_clean.parquet` riêng: `qa_pairs.parquet` giờ đã sạch. Có thêm cột `viquad_split`. Nhãn `"không có câu trả lời"` cho câu `is_impossible` sẽ được gán lúc tạo dataset ở Giai đoạn 4.
- [x] `tests/test_split_leak.py`: kiểm tra trên dữ liệu thật (không rò rỉ bài/đoạn/câu hỏi, split câu hỏi trùng split đoạn văn, đáp án nằm đúng vị trí, câu không trả lời được có `plausible_answer`).
- [x] `src/data/length_stats.py` → `reports/data_stats.md`.
- [x] **Phát sinh:** `transformers` 5.x không tải được tokenizer của `VietAI/vit5-base` → ghim lại `transformers==4.57.6` (cùng `tokenizers`, `huggingface-hub`, `datasets`, `sentence-transformers`, `gradio` tương thích; đã giải phụ thuộc thử cho Colab và máy local).

**Kết quả quan trọng cho các giai đoạn sau** (xem `reports/data_stats.md`):
- Input 1 đoạn: p99 = 516 token → `max_source_length=512` chỉ cắt 1,0%.
- Đáp án: p99 = 59 token → **`max_target_length=64`** (32 sẽ cắt 8,1% đáp án).
- Ghép k=3 đoạn ≈ 631 token (p90 ≈ 1.020), k=5 ≈ 1.033 token (p90 ≈ 1.676). → Với k > 1, mặc định **đọc từng đoạn riêng rồi chọn đáp án có điểm cao nhất**; ghép đoạn (1024 token) chỉ là thí nghiệm phụ.
- 3 bài không có câu hỏi có nhãn: Edward II của Anh, Đế quốc Đức (train), Đế quốc Nga (test). Đoạn văn của chúng vẫn nằm trong kho, đóng vai trò nhiễu khi truy hồi.

### Giai đoạn 2 — Retriever (2 ngày) ✅
- [x] `src/retriever/hybrid.py`: lớp `Retriever` với 3 chế độ `bm25 | dense | hybrid`. Kho chỉ 1.862 đoạn nên chấm điểm toàn bộ kho cho mỗi câu hỏi, và RRF gộp trên thứ hạng đầy đủ (bản cũ chỉ gộp top 3k). Tiền xử lý dùng chung nằm ở `text.py`.
- [x] Build `data/index_qa/` trên **cả 3 split** (1.862 đoạn): `meta.parquet`, `dense_seg.faiss`, `dense_raw.faiss`, `info.json`. BM25 dựng lại khi load (< 1 giây), không lưu pickle.
- [x] So sánh 2 cách tách token cho BM25: theo âm tiết (`\w+`) và theo từ (`underthesea`). Dense dùng `bkai-foundation-models/vietnamese-bi-encoder`, model này yêu cầu input đã tách từ; có so sánh với văn bản thô.
- [x] `eval_retriever.py`: Recall@{1,3,5,10,20} và MRR trên câu **trả lời được**, tách theo VN/TG. Tuỳ chọn `--sweep` quét trọng số RRF.
- [x] Chọn cấu hình trên **dev**, kiểm lại trên **train** (retriever không huấn luyện nên dùng train được). **Test chưa chạy.**

**Kết quả** (`reports/retriever_{dev,train}.md`, `*_sweep.csv`):

| Cấu hình | R@1 dev | R@5 dev | MRR dev | R@5 train | MRR train |
|---|---|---|---|---|---|
| BM25 âm tiết | 76.1 | 90.4 | 0.824 | 82.4 | 0.721 |
| BM25 tách từ | 74.8 | 88.7 | 0.809 | 81.8 | 0.722 |
| Dense tách từ | 52.2 | 73.7 | 0.617 | — | — |
| Hybrid RRF (k=60, w=1) | 67.3 | 86.2 | 0.763 | 84.6 | 0.719 |
| **Hybrid RRF (k=5, w_dense=0.7) — chọn** | 71.9 | **93.4** | 0.813 | **88.0** | **0.752** |

- Tách từ bằng underthesea **không giúp** BM25: nhỉnh hơn ở bài VN, kém hơn ở bài TG (có thể do tách sai tên riêng nước ngoài).
- Dense yếu khi dùng một mình: 11,8% số đoạn dài hơn 256 token nên bị cắt khi nhúng. Dù vậy, dense vẫn bổ sung tốt cho BM25 nếu RRF dùng k nhỏ và trọng số dense thấp hơn BM25. Gộp bằng nhau (k=60, w=1) thì hybrid thua BM25 trên dev.
- Dev dễ hơn train với BM25 (R@5 90.4 so với 82.4). Cấu hình được chọn đứng trong nhóm đầu ở cả hai tập.
- Hạn chế: R@1 của hybrid thấp hơn BM25 trên dev. Nếu Reader chỉ đọc 1 đoạn thì cần xem lại ở E2.
- Mặc định cho Giai đoạn 4–5: hybrid đã chọn, k ∈ {1, 3, 5}. BM25 và dense vẫn giữ để so sánh trong E2.

**Xong khi:** có bảng Recall@k cho 3 chế độ × 2 cách tách từ; đã chốt cấu hình. ✅

### Giai đoạn 3 — Metric & baseline (2 ngày) ✅
- [x] `src/eval/metrics.py`: EM và F1 theo âm tiết, chuẩn hoá tiếng Việt (NFC, chữ thường, bỏ dấu câu, gộp khoảng trắng; **không** bỏ dấu thanh). Ghi riêng: HasAns-EM/F1, NoAns-accuracy, tỉ lệ từ chối sai (theo kiểu `squad_v2`).
  - **Phát sinh:** kho dùng lẫn hai kiểu đặt dấu thanh ("hòa" 605 lần / "hoà" 953 lần, "thủy"/"thuỷ") → chuẩn hoá thêm vị trí dấu thanh (oa/oe/uy cuối âm tiết).
  - **Phát sinh:** "từ chối" = chuỗi thô rỗng hoặc đúng nhãn `"không có câu trả lời"`. Chuỗi chỉ toàn ký hiệu **không** tính là từ chối, vì nếu tính thì ViT5 zero-shot (sinh `*>+>`) được NoAns-acc 62% và EM 20,4 một cách ảo.
- [x] Unit test: `tests/test_metrics.py` ("năm 1954" vs "1954" → F1 2/3, hoa/thường, NFC/NFD, vị trí dấu thanh, đáp án rỗng, nhãn từ chối) và `tests/test_evaluate.py`.
- [x] `src/eval/evaluate_pipeline.py`: nhận một hoặc nhiều file `data/predictions/{run}.jsonl` (định dạng ở `src/eval/predictions.py`), in bảng tổng / VN–TG / loại câu hỏi (`qtype.py`), tỉ lệ đoạn đúng nằm trong các đoạn đã đọc, HasAns-F1 khi tìm đúng/sai, tỉ lệ dự đoán có nguyên văn trong đoạn (chỉ báo "bịa"). `--out` ghi `.md` + `.json`.
- [x] **Baseline B0** (`src/reader/baseline_random.py`): cụm danh từ (underthesea chunk) hoặc năm ngẫu nhiên trong đoạn top-1; chạy trên cả đoạn đúng và đoạn retriever tìm được.
- [x] **Baseline B1 — Reader trích xuất** (`src/reader/train_extractive.py`, `configs/reader_extractive.yaml`): `xlm-roberta-base`, squad_v2 (câu không trả lời được → token `<s>`), ngưỡng null chọn trên dev. Đã kiểm gán nhãn span (425/429 feature khớp; 4 feature lệch do đáp án gốc cắt giữa từ) và chạy thử toàn luồng trên CPU. Train trên Colab T4 (`notebooks/colab_train_reader.ipynb`, code tại commit `1dcad97`), 3 epoch, ngưỡng null chọn trên dev = −0,10.
- [x] **Baseline B2 — ViT5 zero-shot** (`src/reader/infer.py`, dùng lại ở Giai đoạn 4): `VietAI/vit5-base` chưa fine-tune, input `"<q> … </q> <ctx> … </ctx>"`. CPU ~0,2 s/câu.

**Kết quả trên dev** (`reports/baselines_dev.md`):

| Run | Đoạn văn | EM | F1 | HasAns-F1 | NoAns-acc |
|---|---|---|---|---|---|
| B0 ngẫu nhiên | đúng | 0.1 | 1.6 | 2.4 | 0.0 |
| B0 ngẫu nhiên | hybrid top-1 | 0.1 | 1.7 | 2.5 | 0.0 |
| B2 ViT5 zero-shot | đúng | 0.0 | 0.4 | 0.6 | 0.0 |
| **B1 XLM-R trích xuất** | đúng | **37.4** | **51.5** | **61.7** | **30.9** |

- B0 rất thấp vì đáp án ViQuAD dài (trung vị 8 âm tiết) còn cụm danh từ của underthesea ngắn. Đây chỉ là mốc sàn.
- ViT5 chưa fine-tune chỉ sinh ra ký hiệu rác (`*>+>`, `ctx>`): mô hình chỉ được pretrain bằng span-corruption nên chưa biết làm QA. Vì vậy so sánh "fine-tune vs zero-shot" (§7) sẽ chênh lệch rất rõ. Mốc so sánh có ý nghĩa thật là B1.
- B0 trên hybrid top-1: đoạn đúng nằm trong top-1 ở 71,9% câu, khớp R@1 ở Giai đoạn 2.
- **B1 là mốc chính ViT5 phải vượt** (RQ1). HasAns-F1 61,7 nhưng EM chỉ 40,6: mô hình thường tìm đúng vùng nhưng lệch ranh giới đáp án (đáp án ViQuAD dài, trung vị 8 âm tiết). VN 64,4 so với TG 60,6.
- **Điểm yếu là từ chối:** NoAns-acc chỉ 30,9%, trong khi 20,5% câu có đáp án lại bị từ chối nhầm. Mô hình chưa phân biệt được câu nào không trả lời được; ngưỡng chọn theo F1 tổng chỉ đổi qua lại giữa hai loại lỗi này. Đây là điểm ViT5 cần cải thiện (RQ3, mục tiêu NoAns ≥ 60%).
- Theo loại câu hỏi: "khi nào" dễ nhất (HasAns-F1 81,1), "như thế nào" khó nhất (53,9) — đáp án dài, ranh giới mơ hồ.
- Dự đoán từ Colab chưa ghi được commit (zip không có `.git`) → đã sửa: zip mang file `COMMIT` (`git archive --add-virtual-file=COMMIT:… -o hmtt.zip HEAD src configs data/processed notebooks requirements.txt`).

**Xong khi:** `evaluate_pipeline.py` nhận một file dự đoán và in ra đủ bảng chỉ số. ✅

### Giai đoạn 4 — Reader ViT5 text-to-text (3–4 ngày, Colab GPU)
- [x] `src/reader/train_seq2seq.py` dùng `Seq2SeqTrainer`; cấu hình đọc từ `configs/reader_vit5.yaml`. Unit test tạo mẫu: `tests/test_seq2seq_data.py`. Đã chạy thử toàn luồng trên CPU (R1 và R2, 32 mẫu).
  - Input: `format_input()` của `infer.py` = `"<q> {question} </q> <ctx> {passage} </ctx>"`, max 512 token, mỗi input **một đoạn**.
  - Target: đáp án, max 64 token; câu không trả lời được → `"không có câu trả lời"`.
  - Mặc định: effective batch 32 (8 × 4), 5 epoch, early stopping (patience 2) theo F1 dev **trên đoạn đúng** (sinh greedy), bf16 nếu GPU hỗ trợ, nếu không thì fp16; seed 42.
  - **Phát sinh — lr 1e-4 thay vì 3e-5:** 3e-5 là mức của encoder kiểu BERT; T5/ViT5 với AdamW thường cần 1e-4 – 3e-4. Nếu F1 dev vẫn tăng ở epoch cuối thì thử 3e-4 (chọn trên dev).
  - **Phát sinh — fp16 trên T4:** T5 + fp16 có thể ra loss NaN. Script tự dừng khi gặp NaN và nhắc chạy lại với `--no_fp16`.
- [ ] **R1 — train trên đoạn văn đúng**: 9.394 mẫu, 32,4% target là từ chối.
- [ ] **R2 — đoạn đúng + đoạn nhiễu của retriever**: mỗi câu trả lời được thêm 1 đoạn lấy ngẫu nhiên trong top-5 hybrid (bỏ đoạn đúng). Đoạn nhiễu → target từ chối; nếu đoạn nhiễu chứa nguyên văn đáp án thì giữ đáp án (183 mẫu). Tổng 15.741 mẫu, **58,5% target là từ chối** → cần xem R2 có từ chối nhầm nhiều hơn R1 trên đoạn đúng không. Trainer tự xáo trộn mẫu.
  - **Phát sinh — cache truy hồi:** `data/index_qa/` không nằm trong git nên không có trên Colab → `src/retriever/cache_retrieval.py` tính sẵn top-20 hybrid cho train + dev vào `data/processed/retrieved_hybrid.parquet` (1 MB, commit được; kiểm lại R@5 dev 93,4 / train 88,0 khớp Giai đoạn 2). `get_contexts()` dùng cache nếu đủ; độ trễ truy hồi lấy theo số đo khi tạo cache. Test không cache.
- [x] `infer.py`: chạy toàn hệ thống (retrieve → read), lưu `data/predictions/{run}.jsonl` gồm câu hỏi, đoạn văn tìm được, dự đoán, đáp án chuẩn, độ trễ (có từ Giai đoạn 3).
- [x] Model tốt nhất lưu ở `models/{r1,r2}_vit5` kèm `train_config.json` (cấu hình, commit, số mẫu, lịch sử F1 dev theo epoch); notebook `notebooks/colab_train_vit5.ipynb` chép lên Drive.

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
- [ ] **Cập nhật báo cáo PDF và slide trong `baocao/`** (`10-250201078-240104052-2502010243-2502010484-250201058.docx` / `.pdf` / `.pptx`). Đây là **bản cũ**, làm trước khi có dự án mới. Chỉ làm **sau khi xong hết** Giai đoạn 4–6. Đi lần lượt từng phần (mục của báo cáo, slide tương ứng), thay nội dung cũ bằng phương pháp và kết quả thực tế: dữ liệu và cách chia (GĐ1), retriever hybrid và Recall@k (GĐ2), metric và baseline B0/B1/B2 (GĐ3), ViT5 R1/R2 (GĐ4), E1–E6 trên test (GĐ5), phân tích lỗi và demo (GĐ6). Mọi số liệu lấy từ `reports/`, không chép tay từ hội thoại. Sửa trên file nguồn `.docx` (giữ định dạng, mục lục, chú thích hình/bảng của bản cũ), rồi xuất lại `.pdf` từ `.docx`. Không sửa PDF trực tiếp.

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
| Lỗi phiên bản `transformers` trên Colab (như dự án cũ) | **Đã xảy ra** (5.x hỏng tokenizer ViT5) | Đã ghim `transformers==4.57.6`; trên Colab phải `pip install -r requirements.txt` rồi **restart runtime** |
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
6. Báo cáo cuối kỳ (PDF) và slide trình bày (PPTX) trong `baocao/`, cập nhật theo kết quả thực tế.

---

## 10. Việc làm ngay

1. Thu hồi API key cũ.
2. Giai đoạn 0: dọn repo, `git init`, `requirements.txt`.
3. Giai đoạn 1: điều tra khoảng 1.988 span lỗi trong `qa_pairs.parquet`.
