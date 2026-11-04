# Giải thích quá trình làm đề tài — Hệ hỏi đáp Lịch sử tiếng Việt

> Tài liệu này kể lại **từng bước đã làm, làm để làm gì, và vì sao chọn cách đó**, từ lúc nhận dự án cũ đến hiện tại (04/11/2026).
> Kế hoạch đầy đủ nằm trong [`PLAN.md`](PLAN.md). Số liệu chi tiết nằm trong `reports/`.

---

## Mục lục

0. [Bức tranh tổng thể: hệ thống làm gì](#0-bức-tranh-tổng-thể)
1. [Bước 0 — Đánh giá dự án cũ và đổi đề tài](#bước-0--đánh-giá-dự-án-cũ-và-đổi-đề-tài)
2. [Giai đoạn 0 — Dọn repo và bảo mật](#giai-đoạn-0--dọn-repo-và-bảo-mật)
3. [Giai đoạn 1 — Làm sạch dữ liệu hỏi đáp](#giai-đoạn-1--làm-sạch-dữ-liệu-hỏi-đáp)
4. [Giai đoạn 2 — Retriever: tìm đoạn văn liên quan](#giai-đoạn-2--retriever-tìm-đoạn-văn-liên-quan)
5. [Giai đoạn 3 — Thước đo và các mốc so sánh (baseline)](#giai-đoạn-3--thước-đo-và-các-mốc-so-sánh-baseline)
6. [Các giai đoạn còn lại](#các-giai-đoạn-còn-lại)
7. [Các nguyên tắc xuyên suốt](#các-nguyên-tắc-xuyên-suốt)
8. [Bảng thuật ngữ](#bảng-thuật-ngữ)

---

## 0. Bức tranh tổng thể

Người dùng gõ một câu hỏi lịch sử, hệ thống trả về câu trả lời ngắn kèm đoạn văn làm bằng chứng. Nếu kho tài liệu không có thông tin thì hệ thống phải nói **"không có câu trả lời"** thay vì bịa.

```
"Chiến thắng Điện Biên Phủ diễn ra năm nào?"
        │
        ▼
[1. Retriever]  tìm trong kho 1.862 đoạn văn → lấy k đoạn liên quan nhất
        │
        ▼
[2. Reader]     đọc câu hỏi + đoạn văn → sinh câu trả lời
        │
        ▼
"1954"   (bằng chứng: đoạn ctx_…, bài "Chiến tranh Đông Dương")
```

Hệ thống có hai khâu, và phải làm tốt cả hai:
- **Retriever** (bộ tìm kiếm) không cần huấn luyện. Ta chỉ chọn phương pháp và cấu hình tốt nhất.
- **Reader** (bộ đọc hiểu) là phần học máy chính: fine-tune mô hình **ViT5**, một mô hình text-to-text tiếng Việt, để nó *sinh* ra câu trả lời.

Đề tài trả lời 4 câu hỏi nghiên cứu (RQ):

| RQ | Câu hỏi | Trả lời bằng thí nghiệm nào |
|---|---|---|
| RQ1 | Mô hình **sinh** đáp án (ViT5) có tốt hơn mô hình **trích xuất** (chọn một đoạn chữ có sẵn trong văn bản) không? | So ViT5 với baseline B1 |
| RQ2 | Tìm kiếm kết hợp có tốt hơn từng cách riêng không? Hệ thống sai chủ yếu ở khâu **tìm** hay khâu **đọc**? | So các retriever; đọc trên đoạn đúng và đoạn tự tìm |
| RQ3 | Cho mô hình học cả những câu không trả lời được thì nó có biết từ chối không? | Train có và không có các câu đó |
| RQ4 | Thêm dữ liệu ngoài lịch sử có giúp không? Bài Việt Nam và bài thế giới khác nhau thế nào? | Tách kết quả theo miền |

---

## Bước 0 — Đánh giá dự án cũ và đổi đề tài

**Đã làm:** đọc toàn bộ dự án cũ (thư mục `files_v1`, một "hệ hỗ trợ ra quyết định sinh câu hỏi trắc nghiệm"), tự tính lại các số liệu rồi so với README. Kết quả nằm trong [`phan_tich.md`](phan_tich.md).

**Phát hiện chính:**
- Câu hỏi sinh bằng luật chất lượng kém: 423 câu nhưng chỉ có 75 câu khác nhau.
- Câu hỏi sinh bằng LLM khá hơn, nhưng 20% đáp án không nằm trong ngữ cảnh.
- So sánh giữa các phương pháp không công bằng: mỗi phương pháp chạy trên một tập dữ liệu khác nhau.
- Phần ViT5 chưa có kết quả.
- **Lỗi bảo mật nghiêm trọng:** một OpenAI API key bị ghi thẳng vào mã nguồn.

**Quyết định:** đổi sang bài toán **hỏi đáp mở (open-domain QA)**, vì bài toán này:
- dùng lại được phần tốt nhất của dự án cũ: kho dữ liệu ViQuAD đã lọc bài lịch sử và chia split theo bài;
- có thước đo khách quan (EM/F1 so với đáp án chuẩn), không phải chấm tay "câu hỏi hay hay dở";
- vẫn giữ ViT5 làm trọng tâm học máy.

---

## Giai đoạn 0 — Dọn repo và bảo mật

**Mục tiêu:** có một repo sạch, an toàn, cài đặt được.

| Việc | Lý do |
|---|---|
| Gỡ API key khỏi `rag_llm.py` | Key nằm trong git thì ai có repo cũng dùng được. Key thuộc người khác nên phải báo chủ key thu hồi. Dự án mới chỉ dùng mô hình mở nên không cần key. |
| Làm phẳng thư mục `files_v1/files_v1/`, chuyển code cũ vào `legacy/` | Code còn dùng nằm trong `src/data`, `src/retriever`; code không dùng tiếp vẫn giữ để tham khảo nhưng tách riêng. |
| `git init`, `.gitignore` | Không đưa vào git mô hình, index, `.env`: file quá lớn, tạo lại được, hoặc là bí mật. |
| `requirements.txt` ghim phiên bản cố định | Dự án cũ từng hỏng vì phiên bản thư viện trên Colab khác máy local. Ghim phiên bản để hai nơi chạy giống nhau. |

---

## Giai đoạn 1 — Làm sạch dữ liệu hỏi đáp

**Mục tiêu:** đảm bảo mỗi câu hỏi có đáp án đúng và nằm đúng chỗ trong đoạn văn trước khi train. Dữ liệu sai thì mọi kết quả phía sau đều sai.

### 1.1. Dữ liệu là gì

Dữ liệu lấy từ **UIT-ViQuAD 2.0**, bộ hỏi đáp tiếng Việt dựa trên Wikipedia. Dự án chỉ giữ **38 bài lịch sử** (9 bài Việt Nam, 29 bài thế giới):
- `corpus.parquet`: 1.862 đoạn văn. Đây là "kho tri thức" mà hệ thống được phép tra cứu.
- `qa_pairs.parquet`: 12.009 câu hỏi có nhãn, gồm 8.126 câu trả lời được và 3.883 câu **không trả lời được** (ViQuAD 2.0 cố ý tạo các câu hỏi nghe hợp lý nhưng đoạn văn không chứa đáp án).

### 1.2. Chia train / dev / test **theo bài**

| Split | Số bài | Số câu hỏi | Dùng để |
|---|---|---|---|
| train | 23 | 9.394 | huấn luyện |
| dev | 8 | 1.329 | chọn cấu hình, siêu tham số |
| test | 7 | 1.286 | **chỉ đánh giá một lần** ở cuối |

Phải chia theo bài vì các câu hỏi trong cùng một bài thường hỏi về cùng sự kiện. Nếu chia ngẫu nhiên theo câu, mô hình sẽ "thấy trước" nội dung của test, và điểm số bị thổi phồng.

Tất cả đoạn văn của cả 3 split đều nằm trong kho tri thức. Điều này hợp lệ vì kho tri thức là tài liệu hệ thống được tra cứu. Cái cần giấu là **cặp hỏi–đáp** của test.

### 1.3. Lỗi đã phát hiện và sửa

1. **1.988 câu hỏi "trả lời được" nhưng không tìm thấy đáp án trong đoạn văn.** Giả thuyết ban đầu là lỗi lệch vị trí, nhưng sai. Nguyên nhân thật: split `test` chính thức của ViQuAD trên HuggingFace **không có nhãn** (đáp án rỗng), nhưng code cũ coi các câu đó là có đáp án. → Bỏ các câu hỏi không nhãn này, vẫn giữ đoạn văn trong kho.
2. **Trường `plausible_answer` rỗng ở mọi dòng**, do code cũ đọc nhầm tên trường (`plausible` thay vì `plausible_answers`). Đã sửa, giờ đủ 3.883/3.883.
3. **`id` câu hỏi bị trùng** giữa train và validation gốc (152 id). Đã đổi thành dạng `train:0013-0001-0001`.
4. **74 câu có vị trí đáp án lệch vài ký tự** do chuẩn hoá khoảng trắng. Đã căn lại theo lần xuất hiện gần nhất nếu lệch ≤ 20 ký tự. Một câu lệch 608 ký tự thì đánh dấu lỗi, không đoán.
5. **Phát sinh:** `transformers` 5.x không tải được tokenizer ViT5. Đã ghim lại bản 4.57.6.

### 1.4. Kiểm tra tự động

`tests/test_split_leak.py` chạy trên dữ liệu thật và kiểm tra: không có bài, đoạn hay câu hỏi nào nằm ở hai split; đáp án nằm đúng vị trí; câu không trả lời được có `plausible_answer`.

### 1.5. Thống kê độ dài để chọn tham số cho ViT5

`src/data/length_stats.py` → `reports/data_stats.md`, đo bằng tokenizer của ViT5:

| Kết luận | Bằng chứng |
|---|---|
| Input tối đa **512 token** là đủ | Câu hỏi + 1 đoạn: p99 = 516 token, chỉ 1% bị cắt |
| Đáp án tối đa **64 token** | p99 = 59. Nếu đặt 32 thì 8% đáp án bị cắt |
| Khi lấy nhiều đoạn, **đọc từng đoạn riêng** chứ không ghép | Ghép 3 đoạn ≈ 631 token, ghép 5 đoạn ≈ 1.033 token, vượt 512 |

---

## Giai đoạn 2 — Retriever: tìm đoạn văn liên quan

**Mục tiêu:** với mỗi câu hỏi, đưa đoạn văn chứa đáp án lên càng cao càng tốt. Retriever bỏ sót thì Reader giỏi đến đâu cũng chịu.

### 2.1. Ba cách tìm kiếm đã thử

| Cách | Ý tưởng | Mạnh / yếu |
|---|---|---|
| **BM25** | Đếm từ trùng giữa câu hỏi và đoạn văn; từ hiếm như tên riêng hay năm được tính nặng hơn | Rất mạnh với tên người, địa danh, năm. Không hiểu từ đồng nghĩa. |
| **Dense** (FAISS + `vietnamese-bi-encoder`) | Biến câu hỏi và đoạn văn thành vector, so độ gần về nghĩa | Hiểu diễn đạt khác nhau. Yếu với tên riêng; đoạn dài hơn 256 token bị cắt khi nhúng. |
| **Hybrid (RRF)** | Gộp *thứ hạng* của hai cách trên: điểm = Σ wᵢ / (k + hạngᵢ) | Tận dụng điểm mạnh của cả hai |

Kho chỉ có 1.862 đoạn, nên với mỗi câu hỏi ta **chấm điểm toàn bộ kho** thay vì tìm gần đúng. Kết quả vì vậy chính xác tuyệt đối, và RRF gộp được trên thứ hạng đầy đủ (code cũ chỉ gộp top 3.000).

Tiếng Việt có một điểm riêng: một từ có thể gồm nhiều âm tiết ("Điện Biên Phủ"). Vì vậy mình thử hai cách tách:
- theo **âm tiết**: `điện | biên | phủ`
- theo **từ** (dùng underthesea): `điện_biên_phủ`

### 2.2. Cách đánh giá

- **Recall@k**: tỉ lệ câu hỏi có đoạn đúng nằm trong top-k.
- **MRR**: trung bình của 1/hạng của đoạn đúng.

Chỉ tính trên câu trả lời được. Cấu hình chọn trên **dev**, kiểm lại trên **train**. Retriever không học gì nên dùng train để kiểm là hợp lệ, và mẫu lớn hơn. **Chưa chạy test.**

### 2.3. Kết quả và lựa chọn

| Cấu hình | R@1 dev | R@5 dev | R@5 train |
|---|---|---|---|
| BM25 âm tiết | 76.1 | 90.4 | 82.4 |
| Dense tách từ | 52.2 | 73.7 | — |
| Hybrid gộp đều (k=60, w=1) | 67.3 | 86.2 | 84.6 |
| **Hybrid k=5, w_dense=0.7 — chọn** | 71.9 | **93.4** | **88.0** |

**Nhận xét:**
- Tách từ bằng underthesea **không giúp** BM25, có thể do tách sai tên riêng nước ngoài.
- Dense yếu khi dùng một mình, nhưng là bổ sung tốt cho BM25 nếu được cho trọng số thấp hơn.
- Gộp hai cách "bằng nhau" (công thức RRF mặc định k=60) còn **thua** BM25. Phải chỉnh thì hybrid mới thắng. Đây là ví dụ cho thấy vì sao cần chọn cấu hình trên dev thay vì dùng mặc định.
- Hạn chế: R@1 của hybrid thấp hơn BM25. Nếu Reader chỉ đọc 1 đoạn thì cần xem lại ở thí nghiệm E2.

**Code:** `src/retriever/text.py` (tách token), `build_index.py` (tạo index), `hybrid.py` (lớp `Retriever`), `eval_retriever.py` (đánh giá).

---

## Giai đoạn 3 — Thước đo và các mốc so sánh (baseline)

**Mục tiêu:** trước khi train ViT5, cần (1) một **thước đo** chuẩn và đúng cho tiếng Việt, và (2) các **mốc so sánh** để biết kết quả ViT5 là tốt hay chỉ bình thường.

### 3.1. Thước đo EM và F1 (`src/eval/metrics.py`)

- **EM (Exact Match):** dự đoán trùng khớp hoàn toàn với đáp án chuẩn thì được 1, ngược lại 0.
- **F1:** cho điểm khi đúng một phần, tính theo âm tiết trùng nhau.
  Ví dụ: đáp án "1954", dự đoán "năm 1954" → EM = 0. F1: precision = 1/2 (1 trong 2 âm tiết dự đoán là đúng), recall = 1/1 → F1 = 2/3.

Trước khi so sánh, cả dự đoán và đáp án đều được **chuẩn hoá**:

| Bước | Ví dụ | Vì sao |
|---|---|---|
| Chuẩn Unicode NFC | "ễ" gõ kiểu tổ hợp = "ễ" dựng sẵn | Cùng chữ nhưng máy thấy khác |
| Chữ thường | "LÊ LỢI" = "lê lợi" | |
| **Thống nhất vị trí dấu thanh** | "hòa" = "hoà", "thủy" = "thuỷ" | Kho dữ liệu dùng lẫn hai kiểu ("hòa" 605 lần, "hoà" 953 lần). Không chuẩn hoá thì mô hình trả lời đúng vẫn bị chấm sai. |
| Bỏ dấu câu, gộp khoảng trắng | "“Bình Ngô đại cáo”" = "bình ngô đại cáo" | |
| **Không** bỏ dấu thanh | "Hà" ≠ "Ha" | Bỏ dấu thanh sẽ làm nhiều từ khác nghĩa thành giống nhau |

**Câu không trả lời được** được chấm theo kiểu `squad_v2`:
- Với câu không trả lời được: mô hình nói "không có câu trả lời" thì được 1 điểm, trả lời bất kỳ thứ gì khác thì 0.
- Với câu trả lời được mà mô hình từ chối: 0 điểm.

Các chỉ số được báo cáo riêng:
- **HasAns-EM/F1**: điểm trên câu trả lời được, đo khả năng đọc hiểu.
- **NoAns-acc**: tỉ lệ từ chối đúng trên câu không trả lời được, đo khả năng "biết mình không biết" (RQ3).
- **HasAns_abstain**: tỉ lệ từ chối *sai*, tức có đáp án mà mô hình không dám trả lời.

**Một lỗi tinh vi đã phát hiện và sửa:** ban đầu, dự đoán nào thành rỗng sau chuẩn hoá đều bị coi là từ chối. ViT5 chưa fine-tune sinh ra chuỗi rác như `*>+>`; chuỗi này chỉ có ký hiệu, bỏ dấu câu xong thành rỗng, nên bị tính là từ chối. Kết quả là nó được NoAns-acc **62%** và EM **20,4**, hoàn toàn ảo. Quy tắc đã sửa: chỉ coi là từ chối khi chuỗi gốc rỗng hoặc đúng là "không có câu trả lời". Có unit test để lỗi này không quay lại.

**Unit test:** `tests/test_metrics.py`, `tests/test_evaluate.py`, gồm các trường hợp "năm 1954" vs "1954", hoa/thường, hai kiểu dấu thanh, đáp án rỗng, chuỗi rác.

### 3.2. Định dạng file dự đoán chung và công cụ chấm điểm

Mọi mô hình (baseline, ViT5, các thí nghiệm sau) đều ghi kết quả ra **cùng một định dạng**: `data/predictions/{tên_run}.jsonl`, mỗi dòng một câu hỏi, gồm dự đoán, đáp án chuẩn, các đoạn đã đọc và thời gian chạy. Dòng đầu ghi cấu hình và commit git, để biết kết quả sinh ra từ phiên bản code nào.

`src/eval/evaluate_pipeline.py` đọc một hoặc nhiều file như vậy và in ra:
- bảng chỉ số tổng, tách theo **bài Việt Nam / thế giới** (RQ4);
- tách theo **loại câu hỏi**: khi nào / ai / ở đâu / bao nhiêu / vì sao / như thế nào / cái gì (`src/eval/qtype.py`);
- **tỉ lệ đoạn đúng nằm trong các đoạn đã đọc**, và F1 khi tìm đúng so với khi tìm sai. Phần này tách sai số của khâu tìm khỏi sai số của khâu đọc (RQ2);
- **tỉ lệ dự đoán xuất hiện nguyên văn trong đoạn văn**. Mô hình sinh có thể bịa, và chỉ số này đo việc đó;
- bảng so sánh khi đưa vào nhiều file.

Nhờ vậy, mọi thí nghiệm về sau đều được chấm bằng **cùng một công cụ**. Đây là điều dự án cũ thiếu.

### 3.3. Ba baseline

| Baseline | Là gì | Để làm gì |
|---|---|---|
| **B0** ngẫu nhiên | Chọn bừa một cụm danh từ hoặc một năm trong đoạn văn | **Mốc sàn**: mô hình nào cũng phải vượt xa mức này |
| **B1** trích xuất | Fine-tune `xlm-roberta-base` chọn đoạn chữ (vị trí bắt đầu–kết thúc) trong văn bản | **Đối thủ chính** của ViT5 (RQ1) |
| **B2** ViT5 zero-shot | ViT5 gốc, chưa fine-tune | Chứng minh việc fine-tune thực sự có tác dụng |

Chi tiết từng baseline:
- **B0** (`src/reader/baseline_random.py`): dùng underthesea để tìm cụm danh từ, cộng thêm các năm. Chạy cả trên đoạn đúng và trên đoạn top-1 do retriever tìm.
- **B1** (`src/reader/train_extractive.py`, cấu hình `configs/reader_extractive.yaml`): làm theo hướng dẫn hỏi đáp của HuggingFace.
  - Đoạn văn dài được cắt thành nhiều mảnh 384 token, các mảnh chồng lên nhau 128 token để đáp án không bị cắt đôi.
  - Câu không trả lời được thì mô hình học trỏ vào token đầu `<s>`.
  - Lúc dự đoán, so điểm "không có đáp án" với điểm của đoạn chữ tốt nhất. Ngưỡng so sánh được chọn trên dev.
  - Cố ý **không** dùng các checkpoint "vi-mrc" có sẵn, vì chúng có thể đã được train trên chính ViQuAD, kể cả phần mình dùng làm test.
  - Đã kiểm tra cách gán nhãn: 425/429 mảnh khớp đúng đáp án. 4 mảnh lệch là do đáp án gốc của ViQuAD bị cắt giữa từ (vd. "60 máy bay" trong khi văn bản là "160 máy bay").
  - Đã chạy thử toàn bộ luồng trên CPU. Bản train thật **đang chạy trên Colab GPU** (`notebooks/colab_train_reader.ipynb`).
- **B2** (`src/reader/infer.py`): file này cũng là công cụ suy luận cho ViT5 ở Giai đoạn 4.
  - Input có dạng `<q> câu hỏi </q> <ctx> đoạn văn </ctx>`.
  - Khi đọc nhiều đoạn, mỗi đoạn sinh một đáp án kèm điểm tin cậy (xác suất trung bình mỗi token). Chọn đáp án có điểm cao nhất trong các đáp án không phải "không có câu trả lời".

### 3.4. Kết quả trên dev

| Baseline | Đoạn văn | EM | F1 | HasAns-F1 | NoAns-acc |
|---|---|---|---|---|---|
| B0 ngẫu nhiên | đoạn đúng | 0.1 | 1.6 | 2.4 | 0.0 |
| B0 ngẫu nhiên | hybrid top-1 | 0.1 | 1.7 | 2.5 | 0.0 |
| B2 ViT5 zero-shot | đoạn đúng | 0.0 | 0.4 | 0.6 | 0.0 |
| B1 XLM-R trích xuất | đoạn đúng | *đang train* | | | |

**Cách đọc:**
- B0 gần như bằng 0, vì đáp án ViQuAD khá dài (trung vị 8 âm tiết) mà cụm danh từ chọn ngẫu nhiên thì ngắn.
- B2 còn thấp hơn B0: ViT5 gốc chỉ được pretrain để điền chữ bị che, chưa từng học trả lời câu hỏi, nên chỉ sinh ra ký hiệu rác. Mọi cải thiện sau khi fine-tune đều là công của việc fine-tune.
- B0 trên hybrid top-1 có 71,9% câu tìm đúng đoạn, khớp với R@1 ở Giai đoạn 2. Đây là một kiểm tra chéo cho thấy công cụ chấm điểm hoạt động đúng.

---

## Các giai đoạn còn lại

| Giai đoạn | Việc chính | Kết quả mong đợi |
|---|---|---|
| **4 — Reader ViT5** | Fine-tune `vit5-base` trên Colab. **R1:** train trên đoạn đúng. **R2:** train trên đoạn retriever tìm được (có lẫn nhiễu) để mô hình quen với điều kiện thực tế. Câu không trả lời được có nhãn "không có câu trả lời". | HasAns-F1 ≥ 70 trên đoạn đúng |
| **5 — Thí nghiệm** | E1–E6 trả lời RQ1–RQ4 (xem PLAN §5). Chạy 3 seed, bootstrap khoảng tin cậy 95%. **Test chỉ chạy một lần** cho cấu hình cuối. | Toàn hệ thống F1 ≥ 55, NoAns-acc ≥ 60% |
| **6 — Phân tích lỗi & demo** | Phân loại 100 câu sai (tìm sai / đọc sai / đáp án chuẩn có vấn đề / khác cách viết / bịa). Demo Gradio. Đo thời gian chạy. | |
| **7 — Báo cáo** | Bảng và biểu đồ E1–E6, báo cáo cuối kỳ, README hướng dẫn tái lập kết quả. | |

---

## Các nguyên tắc xuyên suốt

1. **Không đụng test cho đến khi chốt cấu hình.** Mọi lựa chọn (cấu hình retriever, ngưỡng từ chối, siêu tham số) đều làm trên dev. Nếu chọn dựa trên test thì điểm test bị thổi phồng và không còn là đánh giá khách quan.
2. **Chia dữ liệu theo bài**, không theo câu, để chống rò rỉ.
3. **Cùng thước đo, cùng định dạng, cùng dữ liệu cho mọi phương pháp**, để so sánh công bằng. Đây là lỗi lớn nhất của dự án cũ.
4. **Kiểm tra số liệu "đẹp bất thường".** Ví dụ: NoAns 62% của ViT5 zero-shot là ảo; 1.988 câu "lỗi vị trí" thực ra là câu không có nhãn.
5. **Tái lập được.** Phiên bản thư viện được ghim, mỗi file dự đoán ghi commit git và cấu hình, có unit test cho mọi phần logic.
6. **Mỗi giai đoạn một commit**, và PLAN.md cập nhật kết quả cùng các vấn đề phát sinh.

---

## Bảng thuật ngữ

| Thuật ngữ | Nghĩa |
|---|---|
| Open-domain QA | Hỏi đáp mà hệ thống phải tự tìm tài liệu, không được cho sẵn đoạn văn |
| Retriever / Reader | Khâu tìm đoạn văn / khâu đọc và trả lời |
| Gold passage (đoạn đúng) | Đoạn văn thật sự chứa đáp án, theo nhãn của bộ dữ liệu |
| BM25 | Chấm điểm theo từ khoá trùng, có trọng số theo độ hiếm của từ |
| Dense retrieval / FAISS | Tìm theo độ gần của vector ngữ nghĩa / thư viện tìm vector |
| RRF | Reciprocal Rank Fusion: gộp nhiều bảng xếp hạng bằng tổng của 1/(k + hạng) |
| Recall@k, MRR | Tỉ lệ đoạn đúng lọt top-k / trung bình của 1/hạng của đoạn đúng |
| Extractive vs generative | Chọn một đoạn chữ có sẵn trong văn bản / sinh ra câu trả lời mới |
| Fine-tune / zero-shot | Huấn luyện tiếp trên dữ liệu của bài toán / dùng nguyên mô hình chưa huấn luyện thêm |
| EM / F1 | Khớp hoàn toàn / điểm trùng một phần theo âm tiết |
| squad_v2 | Chuẩn chấm điểm có câu không trả lời được (theo bộ SQuAD 2.0) |
| HasAns / NoAns | Nhóm câu trả lời được / không trả lời được |
| Baseline | Mốc so sánh để biết mô hình chính tốt đến đâu |
| Dev / test | Tập để chọn cấu hình / tập để đánh giá cuối cùng, chỉ dùng một lần |
