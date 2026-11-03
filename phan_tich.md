# Phân tích dự án `files_v1` — DSS sinh câu hỏi trắc nghiệm Lịch sử

> Ngày phân tích: 03/11/2026
> Phạm vi: toàn bộ `files_v1/files_v1/` (README, mã nguồn `src/`, notebook ViT5, test, dữ liệu trong `data/`).
> Cách làm: đọc mã nguồn, rồi tự tính thống kê lại trên hai file `rule_based.jsonl` và `rag_llm.jsonl` để so với số liệu trong README.

---

## 1. Tóm tắt nhanh

| Hạng mục | Đánh giá |
|---|---|
| Ý tưởng & thiết kế | **Tốt.** Có schema chung (Pydantic), chia split theo bài để chống rò rỉ, có kế hoạch rõ ràng cho Verifier, AHP/TOPSIS và ILP. |
| Tiến độ thực tế | Xong Bước 1–4 (corpus, NER/KB, Rule-based, RAG+LLM). ViT5 **chưa có kết quả** trong thư mục. Chưa bắt đầu Bước 6–9. |
| Chất lượng câu hỏi Rule-based | **Yếu.** Chỉ có 75 câu hỏi khác nhau trên 423 item; câu hỏi không gắn với đáp án nên nhiều câu vô nghĩa. |
| Chất lượng câu hỏi RAG+LLM | **Khá.** Câu hỏi tự nhiên hơn, nhưng 20% đáp án không nằm trong ngữ cảnh và có thiên lệch "đáp án dài nhất là đáp án đúng". |
| Tính công bằng khi so sánh | **Chưa đạt.** Ba phương pháp chạy trên ba tập ngữ cảnh khác nhau và tính VQR theo ba cách khác nhau. |
| Bảo mật | **NGHIÊM TRỌNG:** OpenAI API key bị ghi cứng trong `src/generators/rag_llm.py`. |
| Độ khớp README ↔ thực tế | Nhiều chỗ lệch (file/thư mục không tồn tại, số liệu không khớp, chưa chấm tay NER). |

---

## 2. Cấu trúc thực tế của thư mục

```
files_v1/files_v1/            (lưu ý: thư mục bị lồng 2 cấp)
├── README.md, setup.py
├── test_rag_llm.py, test_rule_based.py        ← test nằm ở gốc
├── src/
│   ├── schema/mcq_schema.py                   (+ __pycache__)
│   ├── preprocess/  survey_viquad, build_corpus, split_balanced,
│   │                ner_kb, clean_entities, test_build/clean/ner/survey,
│   │                titles_inventory_suggested.csv   (+ __pycache__)
│   └── generators/  rule_based, rag_llm, build_index, vit5_train_colab.ipynb
└── data/
    ├── processed/  corpus(.parquet, _all, _history), qa_pairs, entities,
    │               distractor_pool.pkl, splits_report.txt,
    │               ner_quality_sample.csv, titles_inventory(_origin).csv
    ├── index/      faiss.index (5,1 MB), bm25.pkl, index_meta.parquet
    └── generated/  rule_based.jsonl (423 câu), rag_llm.jsonl (90 câu)
```

**README mô tả nhưng KHÔNG có trong thư mục:**

| README ghi | Thực tế |
|---|---|
| `tests/` + `test_schema.py` | Không có thư mục `tests/`; không có `test_schema.py`. Test nằm rải rác ở gốc và trong `src/preprocess/`. |
| `notebooks/vit5_train_colab_v2.ipynb` | Chỉ có `src/generators/vit5_train_colab.ipynb` (bản **cũ**, xem §5.3). |
| `extract_corpus.py`, `review_sample.py` | Không có. |
| `models/vit5_qg`, `models/vit5_dg`, `vit5_ft.jsonl` | Không có (ViT5 chưa xong). |
| `src/verifier/`, `src/evaluation/`, `src/dss/`, `src/app/` | Chưa có (đúng với trạng thái "dự kiến"). |

---

## 3. Pipeline dữ liệu (Bước 1–2)

### 3.1. Corpus (`build_corpus.py`, `split_balanced.py`)

Số liệu trong `splits_report.txt` khớp với README:

| Split | Số bài | Số đoạn | % | VN / TG | Số câu hỏi (không trả lời được) |
|---|---|---|---|---|---|
| train | 23 | 1.491 | 80,1% | 427 / 1.064 | 11.103 (3.047) |
| dev | 8 | 179 | 9,6% | 52 / 127 | 1.536 (437) |
| test | 7 | 192 | 10,3% | 57 / 135 | 1.358 (399) |

**Điểm tốt**
- Chia theo `title` và có `assert` kiểm tra rò rỉ cả ở cấp đoạn và cấp bài.
- Thuật toán greedy cân tải chạy riêng cho từng tiểu miền (VN / TG), nên split nào cũng có cả hai.
- Lưu `is_impossible` và `plausible_answer` để làm nhãn vàng cho Verifier.

**Hạn chế**
- Tập test chỉ có **7 bài**. Mỗi bài là một chủ đề lớn, nên kết quả trên test phụ thuộc mạnh vào việc 7 bài đó là bài nào (phương sai cao). Nên báo cáo thêm kết quả theo từng bài hoặc dùng cross-validation theo bài.
- Có 10.114 câu trả lời được nhưng chỉ **8.126** câu có `answer_span_ok`. Khoảng 2.000 câu (≈20%) bị lệch span; nguyên nhân rất có thể là `normalize_vi` thay đổi ký tự trong context nhưng không cập nhật lại `answer_start`. Cần kiểm tra thêm.
  > **Đính chính (03/11/2026, Giai đoạn 1):** giả thuyết trên sai. 1.988 câu đó đến từ split `test` chính thức của ViQuAD trên HF, vốn **không có nhãn** (`answers=None`), và bị tính nhầm là "trả lời được". Lệch offset do chuẩn hoá thật ra chỉ có 74 câu. Ngoài ra `plausible_answer` rỗng ở mọi dòng vì code đọc sai tên trường. Đã sửa hết trong `src/data/build_corpus.py`; xem `PLAN.md`, Giai đoạn 1.
- `first_answer` chỉ lấy đáp án đầu tiên, bỏ qua các đáp án thay thế.
- README ghi ViQuAD có 184 bài, còn docstring trong code ghi 176. Cần thống nhất một con số.

### 3.2. NER + Knowledge Base (`ner_kb.py`, `clean_entities.py`)

**Điểm tốt:** thời gian được trích bằng regex (rất chính xác), PER/LOC/ORG dùng ELECTRA, sau đó qua một lớp lọc luật hậu xử lý. Bucket chia theo thế kỷ (YEAR) hoặc theo miền VN/TG (thực thể có tên).

**Vấn đề**
- **`ner_quality_sample.csv` có cột `correct` trống ở cả 100 dòng.** Vì vậy các con số precision trong README (YEAR=100%, LOC=97%, PER=90%, ORG=80%) **không có bằng chứng đi kèm**. Có thể file đã chấm nằm ở chỗ khác. Nếu vậy cần đưa vào thư mục, nếu không thì phải chấm lại.
- Mẫu 100 thực thể được lấy ngẫu nhiên theo **tổng thể**, không phân tầng theo type. Với LOC chiếm khoảng 48%, mỗi type như ORG hay DATE chỉ có vài mẫu, nên precision theo từng type có khoảng tin cậy rất rộng. Nên lấy mẫu phân tầng, ví dụ 30 mẫu cho mỗi type.
- README nói có "7 khuôn mẫu lỗi", docstring của `clean_entities.py` ghi 4 (thực tế code có khoảng 4 khuôn mẫu + A/B/C).
- `YEAR_BARE` chỉ bắt năm từ 900 đến 2029. Năm dưới 900 chỉ bắt được khi có chữ "năm" đứng trước.
- Docstring đầu `ner_kb.py` vẫn ghi underthesea là backend chính, trong khi mặc định hiện tại là ELECTRA.

---

## 4. Phân tích dữ liệu đã sinh (số liệu tôi tự tính lại)

### 4.1. Bảng so sánh

| Chỉ số | Rule-Based | RAG+LLM |
|---|---|---|
| Số item | 423 | 90 |
| Số câu hỏi **khác nhau** | **75** (17,7%) | 88 |
| `item_id` trùng | 0 | **1** |
| Số bài (title) được phủ | **5** | 11 |
| Số ngữ cảnh khác nhau | 193 | 44 |
| Tỉ lệ VN / TG | **0 / 423** | 36 / 54 |
| Wh-type | dia_diem 166, nhan_vat 141, thoi_gian 116 | thoi_gian 30, nhan_vat 30, nguyen_nhan 30 |
| Bloom yêu cầu | 100% `nhan_biet` | 100% `nhan_biet` |
| `evidence.found_in_context` | 412/423 = 97% | 74/90 = 82% |
| Đáp án đúng nằm nguyên văn trong context | 414/423 = 98% | **72/90 = 80%** |
| Phân bố A/B/C/D | 118/107/108/90 | 26/23/21/20 |
| Đáp án dài nhất cũng là đáp án đúng | 72/423 = 17% | **51/90 = 57%** |
| Có distractor xuất hiện nguyên văn trong context | 8 | 32 |
| Latency ghi trong file | **không ghi (null)** | TB 3.187 ms/câu |
| Tổng chi phí | $0 | $0,0174 (≈ $0,00019/câu) |

### 4.2. Rule-Based: vấn đề chất lượng

Các câu hỏi lặp lại nhiều nhất:

```
21×  "Người nào thực hiện Edward I của Anh?"
16×  "Edward I của Anh diễn ra tại đâu?"
16×  "Người nào thực hiện Karl Marx?"
14×  "Năm sinh của Edward I của Anh là năm nào?"
13×  "Địa điểm nào liên quan đến Edward I của Anh?"
```

Ví dụ một item sinh ra:

```
Lịch sử thế giới xảy ra tại địa điểm nào?
A. Tân Pháp   B. lâu đài Caernarfon   C. Diêm Nguyên   D. châu Á ✓
```

Nguyên nhân gốc nằm trong `rule_based.py`:

1. **`{subj}` luôn là tiêu đề bài** (`_extract_subject`). Câu hỏi vì thế không liên quan gì tới câu chứa đáp án. Ví dụ "Edward I của Anh diễn ra tại đâu?": hỏi một con người "diễn ra" ở đâu là sai ngữ nghĩa, và đáp án đúng chỉ là một LOC bất kỳ trong đoạn. Đây là lỗi lớn nhất: câu hỏi không có đáp án duy nhất.
2. **Đáp án được chọn ngẫu nhiên** trong các thực thể cùng type ở câu đầu đoạn (`select_answer`). Docstring nói "ưu tiên entity có answer_start (từ QA gold)" nhưng code không làm điều đó.
3. **Template `thoi_gian_person` ("sinh năm nào / qua đời năm nào") được chọn ngẫu nhiên**, không dựa trên ngữ cảnh. Kết quả là năm 1286 có thể được gán làm "năm mất của Edward I" (thực tế ông mất năm 1307).
4. **Động từ mặc định là "thực hiện"** khi không khớp danh sách 10 động từ, sinh ra những câu như "Người nào thực hiện Karl Marx?".
5. **Mất cân bằng mẫu:** `df.head(limit)` lấy 200 đoạn đầu của split train, nên chỉ phủ 5 bài và **toàn bộ là bài thế giới**. Như vậy không thể đánh giá "độ bền miền VN vs TG" cho Rule-based từ dữ liệu này. Nên dùng `sample()` phân tầng theo bài và theo miền.
6. **Distractor cho LOC/PER lấy từ toàn bộ pool của miền TG**, nên các phương án như "Dholavira", "Nakdong", "Vịnh Péc xích" quá xa chủ đề và người làm dễ loại trừ.
7. Một số bug nhỏ:
   - `finalize_options`: `etype = correct_entity_type if is_corr else correct_entity_type` là phép gán vô nghĩa, distractor luôn bị gán type của đáp án đúng.
   - `get_distractors`: vòng `for alt_type ...: if alt_type != answer_type: continue` chỉ chạy lại đúng type cũ, tức là code thừa.
   - `FAMOUS_YEARS` có "1945" lặp hai lần.
   - Distractor chỉ được `_normalize_surface` **sau** bước khử trùng, nên "năm 1954" và "1954" có thể lọt qua rồi trùng với đáp án. Lỗi này được `finalize_options` bắt lại, nhưng làm giảm VQR.
   - `char_start`/`char_end` là offset của chuỗi gốc ("năm 1954"), trong khi `answer_text` đã bỏ chữ "năm", nên hai giá trị lệch nhau.
   - `latency_ms` không được ghi vào item. Con số "8 ms/câu" trong README chỉ được in ra console, không lưu ở đâu.

### 4.3. RAG+LLM: vấn đề chất lượng

- **20% đáp án không nằm nguyên văn trong context** dù prompt yêu cầu trích nguyên văn. Với `nguyen_nhan`, LLM thường diễn đạt lại.
- **Thiên lệch độ dài:** đáp án đúng là phương án dài nhất ở 57% số câu (ngẫu nhiên sẽ khoảng 25%). Lý do là đáp án đúng được trích từ văn bản (dài, cụ thể) còn distractor do LLM tự viết (ngắn, chung chung). Ví dụ:
  ```
  D. "Các quan chức Mỹ cho rằng lô cốt đó là một trung tâm thông tin quân đội…" ✓
  A. "Lô cốt bị tấn công do sự phản kháng của quân đội Iraq"
  ```
  Người làm bài có thể đoán đúng mà không cần đọc đoạn văn. Verifier nên thêm tiêu chí "chênh lệch độ dài phương án".
- **Distractor dễ đoán hoặc thiếu chặt chẽ:** "1500 đến 2000" làm phương án nhiễu cho thời gian tồn tại của Ottoman là quá dễ loại. Có 32/90 item có distractor xuất hiện nguyên văn trong context, tức là có nguy cơ distractor đó cũng đúng.
- **`bloom_predicted` không phải là dự đoán:** prompt cài sẵn `"bloom_level": "{bloom.value}"`, nên LLM chỉ chép lại giá trị yêu cầu (90/90 = `nhan_biet`). Không được dùng trường này để đo Bloom Fidelity.
- **Mâu thuẫn Bloom:** câu `nguyen_nhan` được yêu cầu ở mức `nhan_biet`, trong khi few-shot mẫu của chính `nguyen_nhan` lại ghi `thong_hieu`.
- **Fuzzy evidence quá lỏng** (`parse_llm_output`): chỉ cần một **tiền tố** gồm khoảng ≥ 50% số từ khớp với context là đặt `found_in_context=True`. Như vậy con số 82% có thể cao hơn thực tế.
- **VQR 100% = 90/90 dễ gây hiểu nhầm:** con số này chỉ có nghĩa là "LLM trả JSON hợp lệ", chưa qua bất kỳ kiểm định nội dung nào.
- Có 2 câu hỏi trùng nhau và 1 `item_id` trùng (do cùng context được retrieve cho hai topic). Cần khử trùng trước khi tính chỉ số.
- Latency trung bình thực tế là **3.187 ms**, không phải 5.114 ms như README ghi.
- `main()` chép lại logic của `generate_batch()`, nên hai hàm có thể dần lệch nhau.
- `latency_ms` và `cost_usd` của một item chỉ là chi phí cho lần gọi của ngữ cảnh đó (đúng). Tuy nhiên chi phí retrieval/embedding không được tính.

---

## 5. Các vấn đề phương pháp luận (ảnh hưởng tới kết luận DSS)

### 5.1. So sánh chưa công bằng (vi phạm nguyên tắc chính README tự đặt ra)

README cam kết: *"Cả 3 phương pháp nhận cùng `(context, wh_type, bloom)` làm input"*. Thực tế không như vậy:

| | Rule-Based | RAG+LLM | ViT5 (notebook) |
|---|---|---|---|
| Ngữ cảnh | 200 đoạn **đầu** của split **train** | Top-k retrieve từ **train+dev** theo 10 topic ngẫu nhiên | 300 mẫu từ split **test** |
| Đáp án | Thực thể NER chọn ngẫu nhiên | LLM tự chọn | **Đáp án vàng ViQuAD** (answer-aware) |
| Wh-type | thoi_gian, nhan_vat, dia_diem | thoi_gian, nhan_vat, nguyen_nhan | Suy ra từ câu hỏi gold |
| Mẫu số VQR | #đoạn × #wh | #topic × #wh × top_k | #mẫu test |

Hệ quả:
- Không thể so sánh trực tiếp VQR, Evidence hay chất lượng giữa ba phương pháp.
- Rule-based và RAG được đánh giá trên **train**, nơi ViT5 được huấn luyện, còn ViT5 lại được đánh giá trên test. Ngoài ra RAG có thể retrieve chính đoạn văn mà nó đang sinh câu hỏi, tức là đề bài "dễ" hơn.
- ViT5 được cho sẵn đáp án vàng, nên đây là một bài toán dễ hơn hẳn so với hai phương pháp còn lại.

**Khuyến nghị:** tạo một file `eval_requests.jsonl` cố định, gồm N bộ `(context_id ∈ test, wh_type, bloom)`. Cho cả ba phương pháp chạy trên đúng file này. Với RAG, ngữ cảnh chính là context của request, còn retrieval chỉ dùng để bổ sung thêm thông tin. Định nghĩa VQR chung là `#accepted / #requests`.

### 5.2. Chỉ có Bloom `nhan_biet`

Cả hai bộ dữ liệu đã sinh đều 100% `nhan_biet`. Tiêu chí Bloom Fidelity và ma trận đặc tả cho ILP (tỉ lệ 0.3/0.4/0.3) đều cần câu hỏi ở mức `thong_hieu` và `van_dung`. Hiện tại chưa có dữ liệu này. Ngoài ra classifier Bloom dự kiến dựa trên VNHSGE, nhưng dataset này **chưa được tải về hay xử lý**.

### 5.3. Notebook ViT5 là bản cũ

- Notebook vẫn dùng `Seq2SeqTrainer`. Trong khi đó README ghi đã thay bằng training loop thủ công vì lỗi `EncoderDecoderCache`, đồng thời có xử lý `resize_token_embeddings`. Hai thay đổi này **không có** trong file. Bản v2 bị thiếu.
- Notebook bỏ qua `MCQItem`. Nó tự định nghĩa `finalize_options` riêng và ghi dict thô, nên **không được Pydantic kiểm tra 4 bất biến**.
- **Distractor gold của Stage B** là "các đáp án khác trong cùng context". Đó thường là những sự thật **đúng** của đoạn văn và khác type với đáp án. Mô hình vì thế học sinh distractor có thể cũng đúng. Thêm nữa:
  - Chỉ cần có ≥ 1 đáp án khác là mẫu được nhận, nên target có thể chỉ có 1–2 distractor.
  - `pool[:3]` lấy từ một `set`, nên thứ tự không cố định giữa các lần chạy.
- `infer_wh_type` fallback về `su_kien` và dựa vào từ khoá. Ví dụ từ khoá "tháng" hay "vùng" dễ gán nhầm loại câu hỏi.
- Evidence được tách câu bằng `split('.')`, nên sai với các chữ viết tắt hay số thập phân.

### 5.4. Đo lường chi phí/latency chưa nhất quán

- Rule-based không ghi `latency_ms`.
- RAG không tính thời gian retrieval và tải model embedding.
- Giá GPT-4o-mini được hard-code ("tháng 7/2025"). Nên đưa vào config và ghi lại ngày lấy giá.

---

## 6. Bảo mật — CẦN XỬ LÝ NGAY

`src/generators/rag_llm.py`, hàm `call_openai()`:

```python
client = OpenAI(api_key="sk-proj-…(đã che)")
```

- API key bị **ghi cứng trong mã nguồn**, đồng thời README lại hướng dẫn dùng biến môi trường `OPENAI_API_KEY`, và code đang bỏ qua biến này.
- README hướng dẫn upload cả thư mục `files_v1/` lên Google Drive, nên key rất có thể đã bị lộ (Drive, nộp bài, chia sẻ cho nhóm).

**Việc cần làm:**
1. **Thu hồi (revoke) key này** trên trang quản lý của OpenAI và tạo key mới.
2. Sửa thành `client = OpenAI()`, thư viện sẽ tự đọc `OPENAI_API_KEY`.
3. Kiểm tra lại mọi bản sao đã chia sẻ (Drive, zip nộp bài, git nếu có) và xoá key khỏi đó.

---

## 7. Chất lượng mã & khả năng tái lập

| Vấn đề | Chi tiết |
|---|---|
| Import qua `sys.path.insert` | Các script tự thêm `src/schema` và `src/preprocess` vào path. `setup.py` tồn tại nhưng các module lại import kiểu phẳng (`from mcq_schema import …`), nên `pip install -e .` không thực sự giúp được gì. `build_corpus.py` còn nạp `split_balanced` qua `importlib`. |
| Trùng lặp code | `normalize_vi`, `make_context_id`, `year_stats` được chép lại ở 2–3 file. |
| Không có `requirements.txt` | README liệt kê package nhưng không ghi phiên bản. Notebook ghim `transformers==4.40.0`. |
| `__pycache__/*.pyc` | Bị đưa vào thư mục nộp, nên xoá đi. |
| Test | Có 6 file test với khoảng 87 `assert`, chạy offline. Thiếu `test_schema.py`. `test_clean.py` chỉ có 1 assert. Test dùng `sys.path.insert(0, "src/schema")` (đường dẫn tương đối), nên chỉ chạy được khi đứng ở gốc dự án. |
| Không phải git repo | Không có lịch sử thay đổi. Cũng không có cấu hình seed/tham số được lưu kèm output (`params_hash` luôn là `null`). |
| Thư mục lồng | `files_v1/files_v1/` nên được làm phẳng lại. |

---

## 8. Điểm mạnh nên giữ

1. **Schema `MCQItem` chung** với 4 bất biến được Pydantic ép buộc. Đây là nền tảng tốt cho Verifier và DSS.
2. **Chống rò rỉ** được thiết kế cẩn thận: chia theo bài, RAG chỉ index train+dev, có assert tự kiểm.
3. **Ghi lại provenance** (`context_span`, `kb`, `generated`) và `generation_trace` cho từng câu. Thuận lợi cho việc phân tích chi phí.
4. **Tài liệu tốt:** README chi tiết, có bảng "vấn đề đã gặp → cách xử lý". Điều này có giá trị cho báo cáo.
5. Kiến trúc DSS ba tầng (chọn phương pháp → kiểm định → ráp đề) hợp lý và đúng tinh thần môn học.

---

## 9. Khuyến nghị theo thứ tự ưu tiên

| # | Việc | Lý do |
|---|---|---|
| 1 | **Thu hồi API key**, chuyển sang biến môi trường | Bảo mật |
| 2 | Tạo bộ `eval_requests` cố định trên split **test**, chạy lại cả 3 phương pháp trên cùng bộ này | Nếu không làm, so sánh và AHP/TOPSIS không có giá trị |
| 3 | Sửa Rule-based: lấy `{subj}` từ câu chứa đáp án thay vì tiêu đề bài, bỏ template "sinh/mất" ngẫu nhiên, lấy mẫu phân tầng theo bài và miền | Hiện chỉ 75 câu khác nhau, nhiều câu vô nghĩa |
| 4 | Chấm tay `ner_quality_sample.csv` (phân tầng theo type) hoặc đưa file đã chấm vào thư mục | Precision trong README hiện chưa có bằng chứng |
| 5 | Sinh thêm câu ở mức Bloom `thong_hieu` / `van_dung` | Cần cho Bloom Fidelity và ma trận đặc tả ILP |
| 6 | Đưa notebook ViT5 **v2** vào, cho output đi qua `MCQItem`, sửa cách tạo distractor gold | Đồng bộ schema, tránh distractor đúng |
| 7 | Bổ sung tiêu chí Verifier: **chênh lệch độ dài phương án**, **distractor xuất hiện trong context** | Từ phát hiện ở §4.3 |
| 8 | Siết fuzzy evidence trong RAG (yêu cầu khớp toàn câu hoặc dùng NLI) | 82% có thể đang bị thổi phồng |
| 9 | Ghi `latency_ms` cho Rule-based. Khử trùng `item_id`/câu hỏi trước khi tính chỉ số | Số liệu nhất quán |
| 10 | Cập nhật README cho khớp thực tế (cấu trúc thư mục, latency 3.187 ms, số bài 176/184) | Tránh bị hỏi khó khi bảo vệ |
| 11 | Thêm `requirements.txt`, làm phẳng thư mục, xoá `__pycache__`, khởi tạo git | Tái lập |

---

## 10. Kết luận

Dự án có **thiết kế tốt và tài liệu rõ ràng**, phần tiền xử lý dữ liệu (corpus, split, chống rò rỉ) được làm cẩn thận. Tuy vậy, các **số liệu so sánh hiện tại (VQR 70% vs 100%, Evidence 97% vs 82%) chưa đủ tin cậy để đưa vào AHP/TOPSIS**, vì ba lý do:
(1) ba phương pháp chạy trên ba tập input khác nhau;
(2) VQR chỉ đo việc sinh ra được câu đúng định dạng, chưa đo chất lượng;
(3) mẫu Rule-based lệch nặng (5 bài, 0 bài VN, 75 câu khác nhau).

Việc cần làm ngay là **thu hồi API key bị lộ**. Sau đó, việc quan trọng nhất về mặt khoa học là **chuẩn hoá bộ đánh giá chung trên split test** trước khi xây Verifier và tầng DSS.
