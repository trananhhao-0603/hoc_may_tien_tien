"""
Giai đoạn 7 — dựng lại báo cáo Word từ file nguồn cũ trong baocao/.

Giữ nguyên: bìa (sửa tên đề tài, thành viên, ngày), header/footer, styles, logo, khổ giấy.
Thay toàn bộ phần thân bằng nội dung dự án mới. Mọi bảng số liệu đọc từ reports/*.json
(không chép tay). Mục lục là field TOC; scripts/export_report.ps1 mở Word để cập nhật
số trang và xuất PDF.

    python scripts/build_report.py            # -> baocao/<tên mới>.docx

CẢNH BÁO (09/11/2026): bản nộp `baocao/10-250201078-240201021-250201058.docx` đã được nhóm SỬA TAY
(tên môn, giảng viên, thành viên...) và thêm link tài liệu tham khảo bằng scripts/add_reference_links.py.
Chạy lại script này sẽ tạo bản khác, KHÔNG chứa các chỉnh sửa đó. Sửa tiếp trực tiếp trên file .docx.
"""
from __future__ import annotations

import json
import re
import shutil
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

import pandas as pd
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
REP = ROOT / "reports"
FIG = REP / "figures"
OLD = ROOT / "baocao/10-250201078-240104052-2502010243-2502010484-250201058.docx"
NEW = ROOT / "baocao/10-250201078-2502010484-250201058.docx"

TITLE = "HỆ HỎI ĐÁP LỊCH SỬ TIẾNG VIỆT DỰA TRÊN TRUY HỒI VÀ MÔ HÌNH SINH VIT5"
MEMBERS = [("Nguyễn Bình Nguyên", "250201078"), ("Hoàng Hải Đăng", "2502010484"),
           ("Trần Anh Hào", "250201058")]
DATE = "TP. Hồ Chí Minh, tháng 11 năm 2026"

DARK, MID, LIGHT = "1F4E79", "2E75B6", "DEEAF6"
FONT = '<w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman"/>'


# ============================================================== số liệu
def load(name):
    return json.loads((REP / f"{name}.json").read_text(encoding="utf-8"))


RET, BASE = load("retriever_dev"), load("baselines_dev")
DEV, TEST = load("gd5_dev"), load("gd5_test")
LAT = {d: load(f"latency_{d}") for d in ("cuda", "cpu")}
ERR = pd.read_csv(REP / "error_labels.csv")


def f(x, nd=1):
    """Số kiểu Việt Nam: 57,5."""
    return f"{x:.{nd}f}".replace(".", ",")


def o(d, k):
    return d[k]["overall"]


# ============================================================== XML helpers
def runs(text: str, size=24, bold=False, italic=False, color=None) -> str:
    """Hỗ trợ **đậm** và *nghiêng* trong chuỗi."""
    out = []
    for part in re.split(r"(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)", text):
        if not part:
            continue
        b, i, t = bold, italic, part
        if part.startswith("`"):
            rpr = ('<w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:cs="Courier New"/>'
                   f'<w:sz w:val="{size - 2}"/><w:szCs w:val="{size - 2}"/>')
            out.append(f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{escape(part[1:-1])}</w:t></w:r>')
            continue
        if part.startswith("**"):
            b, t = True, part[2:-2]
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            i, t = True, part[1:-1]
        rpr = FONT + ("<w:b/><w:bCs/>" if b else "") + ("<w:i/><w:iCs/>" if i else "")
        rpr += (f'<w:color w:val="{color}"/>' if color else "") + f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        out.append(f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{escape(t)}</w:t></w:r>')
    return "".join(out)


def para(inner: str, jc="both", before=60, after=80, extra="", keep_next=False) -> str:
    kn = "<w:keepNext/>" if keep_next else ""
    return (f'<w:p><w:pPr>{kn}{extra}<w:spacing w:before="{before}" w:after="{after}" w:line="288" '
            f'w:lineRule="auto"/><w:jc w:val="{jc}"/></w:pPr>{inner}</w:p>')


def P(text, **kw):
    return para(runs(text), **kw)


def H1(text):
    return (f'<w:p><w:pPr><w:pStyle w:val="Heading1"/><w:keepNext/><w:pageBreakBefore/><w:pBdr><w:bottom w:val="single" '
            f'w:sz="6" w:space="0" w:color="{DARK}"/></w:pBdr></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')


def H2(text):
    return (f'<w:p><w:pPr><w:pStyle w:val="Heading2"/><w:keepNext/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')


def H3(text):
    return (f'<w:p><w:pPr><w:pStyle w:val="Heading3"/><w:keepNext/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')


def BUL(items):
    return "".join(
        f'<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
        f'<w:spacing w:before="30" w:after="30" w:line="288" w:lineRule="auto"/><w:ind w:left="720" w:hanging="360"/>'
        f'<w:jc w:val="both"/></w:pPr>{runs(t)}</w:p>' for t in items)


def PAGEBREAK():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def CENTER_TITLE(text, new_page=True):
    """Tiêu đề trang phụ (MỤC LỤC, DANH MỤC...) giống bản cũ: không vào mục lục."""
    pb = "<w:pageBreakBefore/>" if new_page else ""
    return (f'<w:p><w:pPr>{pb}<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="0" w:color="{DARK}"/></w:pBdr>'
            f'<w:spacing w:after="160"/><w:jc w:val="center"/></w:pPr>'
            f'{runs(text, size=30, bold=True, color=DARK)}</w:p>')


FIGS: list[tuple[str, str]] = []
TABS: list[tuple[str, str]] = []
_chap = [0]
_cnt = {"fig": 0, "tab": 0}


def chapter(n):
    _chap[0] = n
    _cnt["fig"] = _cnt["tab"] = 0


def CAPTION(kind, text):
    _cnt[kind] += 1
    label = f"{'Hình' if kind == 'fig' else 'Bảng'} {_chap[0]}.{_cnt[kind]}"
    (FIGS if kind == "fig" else TABS).append((label, text))
    return para(runs(f"{label}: {text}", size=22, italic=True, color="444444"), jc="center", before=60, after=160)


class Media:
    def __init__(self):
        self.items: list[tuple[str, Path]] = []   # (rId, path)

    def add(self, path: Path) -> str:
        rid = f"rIdN{len(self.items) + 1}"
        self.items.append((rid, path))
        return rid


MEDIA = Media()
_docpr = [100]


def IMG(path: Path, width_cm: float, caption: str) -> str:
    rid = MEDIA.add(path)
    w, h = Image.open(path).size
    cx = int(width_cm * 360000)
    cy = int(cx * h / w)
    _docpr[0] += 1
    n = _docpr[0]
    pic = (f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
           f'<wp:docPr id="{n}" name="Hinh{n}"/><wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/>'
           f'</wp:cNvGraphicFramePr><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
           f'<pic:pic><pic:nvPicPr><pic:cNvPr id="{n}" name="{path.name}"/><pic:cNvPicPr/></pic:nvPicPr>'
           f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
           f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect">'
           f'<a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>')
    return para(pic, jc="center", before=120, after=40, keep_next=True) + CAPTION("fig", caption)


def _cell(text, width, fill=None, bold=False, color=None, jc="left", size=20, vmerge=None):
    shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>' if fill else ""
    vm = f'<w:vMerge w:val="{vmerge}"/>' if vmerge == "restart" else ("<w:vMerge/>" if vmerge else "")
    paras = text if isinstance(text, list) else [text]
    body = "".join(
        f'<w:p><w:pPr><w:spacing w:before="30" w:after="30"/><w:jc w:val="{jc}"/></w:pPr>'
        f'{runs(t, size=size, bold=bold, color=color)}</w:p>' for t in paras)
    return (f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{vm}{shd}<w:vAlign w:val="center"/></w:tcPr>'
            f'{body}</w:tc>')


def TABLE(header, rows, widths, caption=None, align=None, total=None):
    """Bảng dữ liệu kiểu bản cũ: hàng tiêu đề nền xanh đậm chữ trắng, viền xám, hàng xen kẽ nhạt."""
    align = align or ["left"] + ["center"] * (len(header) - 1)
    W = sum(widths)
    borders = "".join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="8C8C8C"/>'
                      for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
    x = (f'<w:tbl><w:tblPr><w:tblW w:w="{W}" w:type="dxa"/><w:jc w:val="center"/><w:tblBorders>{borders}'
         f'</w:tblBorders><w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="90" w:type="dxa"/>'
         f'<w:right w:w="90" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>'
         + "".join(f'<w:gridCol w:w="{w}"/>' for w in widths) + "</w:tblGrid>")
    x += ('<w:tr><w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>'
          + "".join(_cell(h, w, DARK, True, "FFFFFF", "center") for h, w in zip(header, widths)) + "</w:tr>")
    for i, r in enumerate(rows):
        fill = "F2F6FB" if i % 2 else None
        x += ('<w:tr><w:trPr><w:cantSplit/></w:trPr>'
              + "".join(_cell(str(c), w, fill, False, None, a) for c, w, a in zip(r, widths, align)) + "</w:tr>")
    if total:
        x += ('<w:tr><w:trPr><w:cantSplit/></w:trPr>'
              + "".join(_cell(str(c), w, LIGHT, True, None, a) for c, w, a in zip(total, widths, align)) + "</w:tr>")
    x += "</w:tbl>"
    return x + (CAPTION("tab", caption) if caption else para("", before=0, after=60))


def NOTE(text, kind="info"):
    """Hộp ghi chú một ô (bản cũ dùng 💡/⚠️/✅): nền nhạt, viền trái đậm."""
    edge, fill, ink = {"info": ("C08A00", "FFF8E6", "7B4F00"), "warn": ("C0504D", "FDEDEC", "7F1D1D"),
                       "ok": ("1E7145", "E8F5EC", "1E4D2B")}[kind]
    label = {"info": "Nhận xét", "warn": "Lưu ý", "ok": "Kết luận"}[kind]
    b = (f'<w:top w:val="single" w:sz="4" w:color="{edge}"/><w:bottom w:val="single" w:sz="4" w:color="{edge}"/>'
         f'<w:right w:val="single" w:sz="4" w:color="{edge}"/><w:left w:val="single" w:sz="24" w:color="{edge}"/>')
    return (f'<w:tbl><w:tblPr><w:tblW w:w="9000" w:type="dxa"/><w:jc w:val="center"/><w:tblBorders>{b}</w:tblBorders>'
            f'<w:tblLayout w:type="fixed"/></w:tblPr><w:tblGrid><w:gridCol w:w="9000"/></w:tblGrid><w:tr><w:tc>'
            f'<w:tcPr><w:tcW w:w="9000" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="{fill}"/></w:tcPr>'
            f'<w:p><w:pPr><w:spacing w:before="80" w:after="80" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>'
            f'{runs(label + ": ", size=22, bold=True, color=ink)}{runs(text, size=22, color=ink)}</w:p></w:tc></w:tr></w:tbl>'
            + para("", before=0, after=60))


def TOC_FIELD():
    return ('<w:p><w:pPr><w:spacing w:after="0"/></w:pPr><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
            '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-2" \\h \\z \\u </w:instrText></w:r>'
            '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
            f'{runs("Mục lục sẽ được Word cập nhật (chuột phải → Update Field).", italic=True)}'
            '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')


# ============================================================== nội dung
def body() -> list[str]:
    B: list[str] = []
    a = B.append

    # ------------------------------------------------------------ 1. GIỚI THIỆU
    chapter(1)
    a(H1("1. GIỚI THIỆU"))
    a(H2("1.1. Bối cảnh và động lực"))
    a(P("Người học và người tra cứu lịch sử thường đặt những câu hỏi cụ thể: một sự kiện xảy ra khi nào, ai lãnh đạo, "
        "vì sao một triều đại suy yếu. Câu trả lời thường nằm sẵn trong các bài viết bách khoa như Wikipedia, nhưng "
        "rải rác trong hàng nghìn đoạn văn. Một hệ thống hỏi đáp tự động cần làm được hai việc: tìm đúng đoạn văn có "
        "thông tin, rồi rút ra câu trả lời ngắn gọn từ đoạn đó. Ngoài ra, hệ thống phải biết **từ chối** khi tài liệu "
        "không chứa câu trả lời, thay vì đưa ra một đáp án nghe hợp lý nhưng sai."))
    a(P("Với tiếng Việt, bộ dữ liệu UIT-ViQuAD 2.0 [2] cung cấp câu hỏi trên Wikipedia tiếng Việt, gồm cả câu hỏi "
        "*không trả lời được*. Mô hình ViT5 [7] là mô hình sinh văn bản được huấn luyện trước trên tiếng Việt. Đề tài "
        "kết hợp hai nguồn lực này để xây dựng một hệ hỏi đáp **miền mở** cho lĩnh vực lịch sử: người dùng chỉ nhập "
        "câu hỏi, hệ thống tự tìm tài liệu và trả lời."))
    a(H2("1.2. Phát biểu bài toán"))
    a(P("**Đầu vào:** một câu hỏi lịch sử bằng tiếng Việt. **Tài liệu:** kho tri thức gồm 1.862 đoạn văn từ 38 bài "
        "Wikipedia lịch sử. **Đầu ra:** một câu trả lời ngắn kèm đoạn văn làm bằng chứng, hoặc câu \"không có câu trả "
        "lời\" khi kho không chứa thông tin cần thiết."))
    a(P("Hệ thống gồm hai khâu theo kiến trúc Retriever–Reader [3] (Hình 1.1). **Retriever** chấm điểm toàn bộ kho và "
        "lấy k đoạn liên quan nhất, kết hợp tìm theo từ khoá (BM25) và tìm theo ngữ nghĩa (bi-encoder). **Reader** là "
        "ViT5 đã fine-tune, đọc từng đoạn và *sinh* ra câu trả lời. Khác với mô hình trích xuất, Reader không bị buộc "
        "phải chọn một đoạn chữ có sẵn, nên học được cách nói \"không có câu trả lời\" như một đầu ra bình thường."))
    a(IMG(FIG / "architecture.png", 16.0, "Kiến trúc hệ hỏi đáp: Retriever hybrid tìm top-k đoạn, Reader ViT5 đọc từng đoạn và chọn đáp án"))
    a(H2("1.3. Câu hỏi nghiên cứu"))
    a(BUL(["**RQ1:** Reader sinh đáp án (ViT5) so với Reader trích xuất (XLM-R) thì bên nào tốt hơn trên dữ liệu lịch sử tiếng Việt?",
           "**RQ2:** Truy hồi kết hợp (BM25 + dense) có tốt hơn từng phương pháp riêng không? Sai số của toàn hệ thống đến từ khâu tìm hay khâu đọc?",
           "**RQ3:** Huấn luyện với câu không trả lời được có giúp mô hình biết từ chối thay vì bịa không?",
           "**RQ4:** Thêm dữ liệu ViQuAD ngoài miền lịch sử có giúp ích không? Hiệu năng trên bài lịch sử Việt Nam và lịch sử thế giới khác nhau thế nào?"]))
    a(P("Sáu thí nghiệm E1–E6 trả lời các câu hỏi trên (Bảng 1.1). Mọi lựa chọn cấu hình đều làm trên tập dev; tập "
        "test chỉ được chấm **một lần** cho các cấu hình cuối cùng."))
    a(TABLE(["Mã", "Thí nghiệm", "Trả lời"],
            [["E1", "Reader trích xuất (B1) so với ViT5 sinh (R1/R2), đọc trên đoạn văn đúng", "RQ1"],
             ["E2", "Toàn hệ thống: retriever {BM25, dense, hybrid} × số đoạn k {1, 3, 5}", "RQ2"],
             ["E3", "Đọc đoạn đúng so với đoạn tự tìm, để tách sai số tìm và sai số đọc", "RQ2"],
             ["E4", "Huấn luyện có so với không có câu không trả lời được", "RQ3"],
             ["E5", "Thêm 10.000 câu ViQuAD ngoài miền lịch sử khi huấn luyện", "RQ4"],
             ["E6", "Tách kết quả theo miền (Việt Nam / thế giới) và loại câu hỏi", "RQ4"]],
            [900, 7000, 1100], "Các thí nghiệm và câu hỏi nghiên cứu tương ứng", ["center", "left", "center"]))
    a(H2("1.4. Đóng góp chính"))
    a(BUL(["Một kho dữ liệu hỏi đáp lịch sử sạch, chia train/dev/test **theo bài** để chống rò rỉ, đã sửa 5 nhóm lỗi dữ liệu kế thừa (mục 3.3).",
           "Retriever hybrid có trọng số, đưa đoạn đúng vào top-5 ở 93,4% câu trên dev và 90,2% trên test.",
           "Reader ViT5 được huấn luyện thêm với đoạn văn nhiễu do retriever tìm ra. Reader này vượt mô hình trích xuất XLM-R chủ yếu nhờ khả năng từ chối.",
           "Bộ thí nghiệm có đối chứng: cùng thước đo, cùng định dạng dự đoán, khoảng tin cậy bootstrap, ba seed. Kèm phân tích tay 100 câu sai, demo Gradio và số đo độ trễ.",
           "Mã nguồn tái lập được: phiên bản thư viện được ghim, mỗi file dự đoán ghi commit git, có unit test, README hướng dẫn tái lập từng bảng."]))

    # ------------------------------------------------------------ 2. LIÊN QUAN
    chapter(2)
    a(H1("2. CƠ SỞ LÝ THUYẾT VÀ NGHIÊN CỨU LIÊN QUAN"))
    a(H2("2.1. Đọc hiểu máy và câu hỏi không trả lời được"))
    a(P("Bài toán đọc hiểu máy (MRC) cho mô hình một đoạn văn và một câu hỏi, yêu cầu chỉ ra đoạn chữ trả lời. SQuAD 2.0 "
        "[1] bổ sung câu hỏi *không trả lời được*: các câu này được viết sao cho nghe hợp lý và gần với đoạn văn, nhưng "
        "đoạn văn không chứa đáp án. Mô hình phải nhận ra để từ chối. UIT-ViQuAD 2.0 [2] áp dụng cách làm này cho tiếng "
        "Việt và kèm một *đáp án mồi* (plausible answer) cho mỗi câu không trả lời được."))
    a(H2("2.2. Hỏi đáp miền mở theo kiến trúc Retriever–Reader"))
    a(P("DrQA [3] là hệ đầu tiên kết hợp một bộ tìm kiếm TF-IDF trên Wikipedia với một mô hình đọc hiểu. DPR [4] thay "
        "tìm kiếm từ khoá bằng tìm kiếm vector với hai bộ mã hoá BERT. RAG [5] và Fusion-in-Decoder (FiD) [6] dùng mô "
        "hình sinh làm Reader: RAG sinh câu trả lời dựa trên các đoạn tìm được, còn FiD mã hoá riêng từng đoạn rồi để "
        "bộ giải mã đọc tất cả cùng lúc. Đề tài dùng cách đơn giản hơn FiD: đọc từng đoạn độc lập rồi chọn đáp án theo "
        "điểm tin cậy. Lý do là bộ nhớ GPU có hạn và trung vị một đoạn văn đã khoảng 200 token."))
    a(H2("2.3. Truy hồi thưa, truy hồi dày và gộp thứ hạng"))
    a(P("BM25 [9] chấm điểm theo các từ trùng giữa câu hỏi và đoạn văn, có trọng số theo độ hiếm của từ. Cách này rất "
        "mạnh với tên riêng và năm, vốn dày đặc trong văn bản lịch sử. Truy hồi dày mã hoá câu hỏi và đoạn văn thành "
        "vector rồi so độ gần, hiểu được cách diễn đạt khác nhau. Đề tài dùng mô hình vietnamese-bi-encoder [14] dựa trên "
        "PhoBERT [12] và thư viện FAISS [13]. Reciprocal Rank Fusion (RRF) [10] gộp hai danh sách theo *thứ hạng*: "
        "điểm = Σ wᵢ / (k + hạngᵢ). Nhờ vậy không cần chuẩn hoá hai thang điểm khác nhau."))
    a(H2("2.4. Mô hình sinh T5/ViT5 và mô hình trích xuất"))
    a(P("T5 [8] đưa mọi bài toán xử lý ngôn ngữ về dạng văn bản → văn bản. ViT5 [7] là T5 được huấn luyện trước trên "
        "kho văn bản tiếng Việt lớn; đề tài dùng bản base. Đối chứng là mô hình *trích xuất* XLM-RoBERTa "
        "[11]: mô hình dự đoán vị trí bắt đầu và kết thúc của đáp án, và trỏ vào token đặc biệt đầu chuỗi khi từ chối. "
        "Mô hình trích xuất không thể bịa, nhưng phải cắt đúng ranh giới đáp án. Mô hình sinh linh hoạt hơn, nhưng có "
        "nguy cơ sinh ra nội dung không có trong văn bản. Đề tài đo trực tiếp nguy cơ này (mục 5.4, 6)."))

    # ------------------------------------------------------------ 3. DỮ LIỆU
    chapter(3)
    a(H1("3. DỮ LIỆU"))
    a(H2("3.1. Nguồn dữ liệu và kho tri thức"))
    a(P("Dữ liệu lấy từ UIT-ViQuAD 2.0 trên HuggingFace (taidng/UIT-ViQuAD2.0). Nhóm khảo sát toàn bộ bài viết, rà tay "
        "để đánh dấu bài thuộc lĩnh vực lịch sử và bài về Việt Nam, rồi giữ lại **38 bài** (9 bài lịch sử Việt Nam, 29 "
        "bài lịch sử thế giới). Kho tri thức gồm **1.862 đoạn văn**. Tập câu hỏi có nhãn gồm **12.009 câu**: 8.126 câu "
        "trả lời được và 3.883 câu không trả lời được (32,3%)."))
    a(H2("3.2. Chia train / dev / test theo bài"))
    a(P("Các câu hỏi trong cùng một bài thường hỏi về cùng các sự kiện. Nếu chia ngẫu nhiên theo câu, mô hình sẽ \"thấy "
        "trước\" nội dung của tập test và điểm bị thổi phồng. Vì vậy dữ liệu được chia **theo bài**, cân bằng số đoạn "
        "khoảng 80/10/10 (Bảng 3.1). Kho tri thức chứa đoạn văn của cả ba tập. Điều này hợp lệ vì kho là tài liệu hệ "
        "thống được phép tra cứu; thứ cần giấu là các cặp hỏi–đáp của tập test."))
    a(TABLE(["Tập", "Số bài", "Số đoạn", "Trả lời được", "Không trả lời được", "Tổng câu hỏi", "VN / TG"],
            [["train", "23", "1.491", "6.347", "3.047", "9.394", "2.610 / 6.784"],
             ["dev", "8", "179", "892", "437", "1.329", "407 / 922"],
             ["test", "7", "192", "887", "399", "1.286", "420 / 866"]],
            [1000, 1000, 1100, 1450, 1650, 1400, 1400], "Phân chia dữ liệu theo bài (VN/TG: số câu hỏi về lịch sử Việt Nam / thế giới)"))
    a(P("Test gồm các bài Mahatma Gandhi, Elizabeth I của Anh, Hồ Quý Ly, Nhà Trần, Louis XVI của Pháp và Đế quốc La Mã "
        "Thần thánh. Unit test `test_split_leak.py` kiểm tra trên dữ liệu thật rằng không có bài, đoạn hay câu hỏi nào "
        "nằm ở hai tập."))
    a(H2("3.3. Làm sạch dữ liệu"))
    a(P("Dữ liệu kế thừa từ dự án trước có nhiều lỗi. Nhóm đã tìm ra và sửa các lỗi trong Bảng 3.2 trước khi huấn luyện."))
    a(TABLE(["Lỗi phát hiện", "Nguyên nhân", "Cách xử lý"],
            [["1.988 câu \"trả lời được\" nhưng đáp án không có trong đoạn văn", "Split test chính thức của ViQuAD không có nhãn (đáp án rỗng) nhưng bị coi là có đáp án", "Bỏ các câu không nhãn, vẫn giữ đoạn văn trong kho"],
             ["Trường plausible_answer rỗng ở mọi dòng", "Đọc nhầm tên trường plausible thay vì plausible_answers", "Sửa lại, đủ 3.883/3.883 câu"],
             ["152 id câu hỏi trùng giữa train và validation gốc", "Hai split gốc dùng chung dạng id", "Đổi thành dạng train:0013-0001-0001"],
             ["74 câu lệch vị trí đáp án vài ký tự", "Chuẩn hoá khoảng trắng làm dịch vị trí", "Căn lại theo lần xuất hiện gần nhất nếu lệch ≤ 20 ký tự"],
             ["transformers 5.x không tải được tokenizer ViT5", "Lỗi chuyển đổi spiece.model", "Ghim transformers 4.57.6"]],
            [2900, 3200, 2900], "Các lỗi dữ liệu đã phát hiện và sửa", ["left", "left", "left"]))
    a(H2("3.4. Thống kê độ dài và lựa chọn tham số"))
    a(P("Độ dài được đo bằng tokenizer của ViT5 (Bảng 3.3). Đầu vào gồm câu hỏi và một đoạn văn có p99 là 516 token, "
        "nên giới hạn **512 token** chỉ cắt 1,0% mẫu. Đáp án có p99 là 59 token, nên giới hạn đầu ra là **64 token** "
        "(nếu đặt 32 sẽ cắt 8,1% đáp án). Ghép 3 đoạn đã khoảng 631 token và ghép 5 đoạn khoảng 1.033 token, vượt quá "
        "512. Vì vậy Reader **đọc từng đoạn riêng** thay vì ghép."))
    a(TABLE(["Thành phần", "p50", "p90", "p99", "Lớn nhất", "Trung bình"],
            [["Đoạn văn", "201", "328", "478", "895", "220"],
             ["Câu hỏi", "16", "24", "32", "71", "17"],
             ["Đáp án", "9", "30", "59", "143", "13"],
             ["Đầu vào Reader (câu hỏi + 1 đoạn)", "231", "365", "516", "930", "251"]],
            [3400, 1000, 1000, 1000, 1300, 1300], "Độ dài theo token ViT5 (nguồn: reports/data_stats.md)"))
    a(NOTE("Đáp án ViQuAD khá dài (trung vị 9 token, tức khoảng 8 âm tiết). Vì vậy EM khắt khe hơn nhiều so với F1: "
           "chỉ cần thừa hoặc thiếu một chữ ở biên là EM bằng 0. Báo cáo dùng F1 làm thước đo chính."))

    # ------------------------------------------------------------ 4. PHƯƠNG PHÁP
    chapter(4)
    a(H1("4. PHƯƠNG PHÁP"))
    a(H2("4.1. Retriever hybrid"))
    a(P("Kho chỉ có 1.862 đoạn, nên với mỗi câu hỏi Retriever **chấm điểm toàn bộ kho** thay vì tìm gần đúng. Nhờ vậy "
        "RRF gộp được trên thứ hạng đầy đủ của cả hai nhánh."))
    a(BUL(["**Nhánh BM25** (rank-bm25): tách token theo **âm tiết** (\"điện | biên | phủ\"), chữ thường, bỏ dấu câu. Thử tách theo từ bằng underthesea nhưng kết quả kém hơn, có thể do tách sai tên riêng nước ngoài.",
           "**Nhánh dense:** mô hình bkai-foundation-models/vietnamese-bi-encoder. Câu hỏi và đoạn văn được tách từ trước, vì mô hình dựa trên PhoBERT yêu cầu vậy. Độ dài tối đa 256 token (11,8% đoạn bị cắt khi mã hoá). Embedding chuẩn hoá L2 và so bằng cosine trong FAISS.",
           "**Gộp RRF có trọng số:** điểm(d) = 1/(k + hạng_BM25(d)) + w · 1/(k + hạng_dense(d)), với hạng tính từ 1. Quét k và w trên dev, chọn **k = 5, w = 0,7**. Công thức RRF mặc định (k = 60, w = 1) còn thua BM25 dùng một mình."]))
    a(H2("4.2. Reader ViT5"))
    a(H3("4.2.1. Định dạng dữ liệu"))
    a(P("Mỗi mẫu là một cặp văn bản → văn bản. Đầu vào có dạng `<q> câu hỏi </q> <ctx> đoạn văn </ctx>` (tối đa 512 "
        "token). Đầu ra là văn bản đáp án, hoặc chuỗi \"không có câu trả lời\" (tối đa 64 token). Cùng một hàm định "
        "dạng được dùng cho cả huấn luyện và suy luận."))
    a(H3("4.2.2. Hai cách tạo dữ liệu huấn luyện"))
    a(BUL(["**R1 (chỉ đoạn đúng):** mỗi câu hỏi đi kèm đoạn văn gốc của nó. Có 9.394 mẫu, trong đó 32,4% có đích là \"không có câu trả lời\".",
           "**R2 (thêm đoạn nhiễu):** ngoài các mẫu của R1, với mỗi câu trả lời được, lấy thêm một đoạn *sai* chọn ngẫu nhiên trong top-5 của retriever và gán đích \"không có câu trả lời\". Lúc chạy thật Reader phải đọc cả những đoạn retriever tìm nhầm, nên cần học cách nhận ra đoạn không liên quan. Có tổng 15.741 mẫu (58,5% đích từ chối). 183 đoạn nhiễu hoá ra vẫn chứa nguyên văn đáp án nên được giữ đáp án."]))
    a(H3("4.2.3. Huấn luyện"))
    a(P("Cấu hình được chọn trên dev (Bảng 4.1). Sau mỗi epoch, mô hình sinh greedy trên dev (đọc đoạn đúng) và giữ "
        "checkpoint có F1 cao nhất. R1 được huấn luyện trên Colab (GPU T4). R2 và các biến thể ở GĐ5 được huấn luyện "
        "trên GPU RTX 3060 12 GB với bf16."))
    a(TABLE(["Tham số", "Giá trị", "Ghi chú"],
            [["Mô hình", "VietAI/vit5-base", "khởi tạo từ checkpoint huấn luyện trước"],
             ["Learning rate", "1e-4 (AdamW)", "3e-4 kém hơn rõ: F1 dev 46,9 so với 57,5"],
             ["Batch hiệu dụng", "32 (8 × tích luỹ 4)", ""],
             ["Số epoch", "8", "5 epoch cho F1 dev 55,9, F1 vẫn còn tăng ở epoch cuối"],
             ["Warmup / weight decay", "5% / 0,01", ""],
             ["Độ dài đầu vào / đầu ra", "512 / 64 token", "theo thống kê ở mục 3.4"],
             ["Chọn checkpoint", "F1 dev (đoạn đúng), dừng sớm sau 2 epoch không tăng", ""],
             ["Giải mã", "greedy (num_beams = 1)", ""]],
            [2600, 3000, 3400], "Cấu hình huấn luyện Reader ViT5 (R2 chính)", ["left", "left", "left"]))
    a(NOTE("Lần huấn luyện đầu cho F1 dev vô nghĩa (HasAns-F1 khoảng 1%) dù loss giảm đều. Nguyên nhân: tuỳ chọn "
           "group_by_length của transformers 4.57 xáo cả thứ tự tập dev, nên dự đoán bị so với đáp án của câu khác "
           "(1.328/1.329 câu lệch). Nhóm đã sửa bằng cách luôn đánh giá dev theo thứ tự gốc, và thêm một bước kiểm tra "
           "nhãn trước khi tính điểm. Kết quả lần đầu bị loại bỏ.", "warn"))
    a(H3("4.2.4. Đọc nhiều đoạn và chọn đáp án"))
    a(P("Với top-k đoạn, Reader đọc từng đoạn trong cùng một batch. Mỗi đoạn cho một đáp án kèm điểm tin cậy, là "
        "log-xác suất trung bình mỗi token sinh ra. Hệ thống chọn đáp án có điểm cao nhất **trong các đáp án không phải "
        "từ chối**. Hệ thống chỉ từ chối khi mọi đoạn đều cho \"không có câu trả lời\"."))
    a(H2("4.3. Ngưỡng từ chối"))
    a(P("Khi Reader định từ chối một đoạn, hệ thống cấm token đầu của câu từ chối để buộc mô hình sinh ra đáp án thay "
        "thế tốt nhất. Sau đó so hai điểm: chỉ từ chối khi điểm từ chối lớn hơn điểm đáp án thay thế một khoảng δ. "
        "Ngưỡng δ được chọn trên dev theo F1 cho từng cấu hình, rồi áp nguyên cho test. Cả hai chế độ (greedy và có "
        "ngưỡng) đều được báo cáo."))
    a(H2("4.4. Các baseline"))
    a(TABLE(["Mã", "Mô hình", "Mục đích"],
            [["B0", "Chọn ngẫu nhiên một cụm danh từ hoặc một năm trong đoạn văn (underthesea)", "Mốc sàn"],
             ["B1", "xlm-roberta-base trích xuất kiểu SQuAD 2.0: cửa sổ 384 token, trượt 128; lr 3e-5, 3 epoch; ngưỡng từ chối chọn trên dev", "Đối thủ chính (RQ1)"],
             ["B2", "ViT5-base chưa fine-tune (zero-shot)", "Chứng minh tác dụng của fine-tune"]],
            [800, 6000, 2200], "Các baseline", ["center", "left", "left"]))
    a(P("Nhóm cố ý không dùng các checkpoint \"vi-mrc\" có sẵn trên mạng, vì chúng có thể đã được huấn luyện trên chính "
        "ViQuAD, kể cả phần dữ liệu dùng làm test ở đây."))
    a(H2("4.5. Thước đo và kiểm định"))
    a(P("**EM** (khớp hoàn toàn) và **F1** (trùng một phần theo âm tiết) được tính sau khi chuẩn hoá (Bảng 4.3). Câu "
        "không trả lời được chấm theo kiểu SQuAD 2.0: được 1 điểm nếu mô hình từ chối, ngược lại 0. Các chỉ số tách "
        "riêng gồm **HasAns-F1** (câu trả lời được), **NoAns-acc** (tỉ lệ từ chối đúng) và tỉ lệ *từ chối nhầm* trên câu "
        "trả lời được."))
    a(TABLE(["Bước chuẩn hoá", "Ví dụ", "Lý do"],
            [["Unicode NFC", "ễ tổ hợp = ễ dựng sẵn", "cùng chữ nhưng khác mã"],
             ["Chữ thường", "LÊ LỢI = lê lợi", ""],
             ["Thống nhất vị trí dấu thanh", "hòa = hoà, thủy = thuỷ", "kho dùng lẫn hai kiểu (605 và 953 lần)"],
             ["Bỏ dấu câu, gộp khoảng trắng", "“Bình Ngô đại cáo” = bình ngô đại cáo", ""],
             ["Giữ dấu thanh", "Hà ≠ Ha", "bỏ dấu làm nhiều từ khác nghĩa thành giống nhau"]],
            [2800, 3300, 2900], "Chuẩn hoá trước khi tính EM/F1", ["left", "left", "left"]))
    a(P("Chỉ chuỗi gốc rỗng hoặc đúng \"không có câu trả lời\" mới được coi là từ chối. Quy tắc này sửa một lỗi tinh "
        "vi: chuỗi rác toàn ký hiệu của ViT5 zero-shot, sau khi bỏ dấu câu, thành rỗng và từng được tính là từ chối "
        "đúng (NoAns ảo 62%). Khoảng tin cậy 95% được ước lượng bằng bootstrap [15] với 2.000 lần lấy mẫu lại câu hỏi. "
        "Khi so hai hệ thống, dùng bootstrap cặp trên cùng các câu hỏi."))

    # ------------------------------------------------------------ 5. THỰC NGHIỆM
    chapter(5)
    a(H1("5. THỰC NGHIỆM VÀ KẾT QUẢ"))
    a(H2("5.1. Thiết lập"))
    a(P("Phần cứng: GPU NVIDIA RTX 3060 12 GB, CPU Intel Core i5-14600KF; một phần huấn luyện chạy trên Colab T4. "
        "Phần mềm: Python 3.12, PyTorch 2.15, transformers 4.57.6, sentence-transformers 5.7, faiss-cpu 1.15. Mọi dự "
        "đoán được ghi vào cùng một định dạng .jsonl kèm commit git, và chấm bằng cùng một công cụ. Nếu không ghi "
        "khác, kết quả dùng giải mã greedy."))
    # 5.2 retriever
    a(H2("5.2. Retriever (E2)"))
    rows = []
    for r in RET["overall"]:
        name = r["Cấu hình"].strip("*").replace(" — chọn", "")
        chosen = "k=5, w=0.7" in name
        name = name.replace("k=5, w=0.7", "k=5, w=0,7")
        rows.append([("**" + name + " (chọn)**") if chosen else name] +
                    [f(100 * r[c]) for c in ("R@1", "R@3", "R@5", "R@10", "R@20", "MRR")])
    a(TABLE(["Cấu hình", "R@1", "R@3", "R@5", "R@10", "R@20", "MRR"], rows,
            [3600, 900, 900, 900, 900, 900, 900], "Recall@k và MRR của retriever trên dev (892 câu trả lời được)"))
    a(IMG(FIG / "recall_at_k.png", 14.5, "Recall@k trên dev của BM25, dense và hybrid đã chọn"))
    tr = {m: [TEST[f"r2m_{m}_k{k}_test_rs"]["retrieval"]["gold_in_ctx"] for k in (1, 3, 5)] for m in ("bm25", "dense", "hybrid")}
    a(P(f"Hybrid đạt R@5 = 93,4% trên dev và **{f(tr['hybrid'][2])}% trên test**, vượt mục tiêu 80%. Dense dùng một mình "
        f"yếu hơn nhiều (R@5 test {f(tr['dense'][2])}%), nhưng bổ sung tốt cho BM25 ({f(tr['bm25'][2])}%) khi được cho trọng số "
        "thấp hơn. R@1 của hybrid thấp hơn BM25. Vì vậy Reader nên đọc nhiều đoạn (k = 3–5) thay vì chỉ một đoạn."))

    # 5.3 reader gold
    a(H2("5.3. Reader đọc đoạn văn đúng (E1, E4, E5)"))
    rd = [("B0 ngẫu nhiên", BASE["b0_gold_dev"]["overall"], "dev"),
          ("B2 ViT5 zero-shot", BASE["b2_gold_dev"]["overall"], "dev"),
          ("B1 XLM-R trích xuất", BASE["b1_gold_dev"]["overall"], "dev"),
          ("R1 ViT5 (chỉ đoạn đúng)", o(DEV, "r1_gold_dev"), "dev"),
          ("E4: R2 bỏ câu không trả lời được", o(DEV, "r2noimp_gold_dev_rs"), "dev"),
          ("**R2 ViT5 (chính)**", o(DEV, "r2m_gold_dev_rs"), "dev"),
          ("E5: R2 + 10k ViQuAD ngoài miền", o(DEV, "r2ood_gold_dev_rs"), "dev"),
          ("E4: R2 bỏ câu không trả lời được", o(TEST, "r2noimp_gold_test_rs"), "test"),
          ("**R2 ViT5 (chính)**", o(TEST, "r2m_gold_test_rs"), "test"),
          ("E5: R2 + 10k ViQuAD ngoài miền", o(TEST, "r2ood_gold_test_rs"), "test")]
    a(TABLE(["Hệ thống", "Tập", "EM", "F1", "HasAns-F1", "NoAns-acc", "Từ chối nhầm"],
            [[n, s, f(m["EM"]), f(m["F1"]), f(m["HasAns_F1"]), f(m["NoAns_acc"]), f(m["HasAns_abstain"])] for n, m, s in rd],
            [3300, 800, 900, 900, 1100, 1100, 900], "Reader khi được cho sẵn đoạn văn đúng (greedy)"))
    a(IMG(FIG / "reader_gold_dev_f1.png", 14.0, "F1 trên dev của các Reader khi đọc đoạn đúng"))
    b1, r2d = BASE["b1_gold_dev"]["overall"], o(DEV, "r2m_gold_dev_rs")
    a(BUL([f"**E1 (RQ1):** R2 hơn B1 {f(r2d['F1'] - b1['F1'])} điểm F1 trên dev ({f(r2d['F1'])} so với {f(b1['F1'])}). Lợi thế nằm gần như hoàn toàn ở khả năng từ chối: NoAns {f(r2d['NoAns_acc'])}% so với {f(b1['NoAns_acc'])}%. Trên câu trả lời được, B1 vẫn nhỉnh hơn (HasAns-F1 {f(b1['HasAns_F1'])} so với {f(r2d['HasAns_F1'])}). R1 chỉ ngang B1, cho thấy đoạn nhiễu khi huấn luyện là điều kiện để ViT5 vượt B1.",
           "**Fine-tune là thiết yếu:** ViT5 zero-shot chỉ sinh ký hiệu rác (F1 0,4), thấp hơn cả B0.",
           "**E4 (RQ3):** bỏ câu không trả lời được khỏi dữ liệu huấn luyện thì mô hình gần như không biết từ chối. Trên test, NoAns giảm 22,8 điểm [−27,6; −17,9] và F1 giảm 5,3 điểm [−7,7; −2,8] (bản có ngưỡng, bootstrap cặp). Đổi lại, HasAns-F1 tăng nhẹ vì mô hình mạnh dạn trả lời hơn.",
           "**E5 (RQ4):** thêm 10.000 câu ViQuAD ngoài miền lịch sử làm F1 test tăng **+2,9 [+0,7; +5,2]** và EM tăng +4,1 [+1,6; +6,5], cả hai có ý nghĩa thống kê. NoAns tăng +5,3."]))

    # 5.4 full system
    a(H2("5.4. Toàn hệ thống (E2, E3)"))
    sysrows = [[m, *[f(o(TEST, f"r2m_{m}_k{k}_test_rs")["F1"]) for k in (1, 3, 5)]] for m in ("bm25", "dense", "hybrid")]
    sysrows.append(["hybrid + Reader E5", *[f(o(TEST, f"r2ood_hybrid_k{k}_test_rs")["F1"]) for k in (1, 3, 5)]])
    a(TABLE(["Retriever", "k = 1", "k = 3", "k = 5"], sysrows, [3600, 1800, 1800, 1800],
            "F1 toàn hệ thống trên test theo retriever và số đoạn k (Reader R2 chính, trừ dòng cuối)"))
    a(IMG(FIG / "f1_by_k_test.png", 14.0, "F1 toàn hệ thống trên test theo k"))
    best, rt = o(TEST, "r2ood_hybrid_k5_test_rs"), TEST["r2ood_hybrid_k5_test_rs"]["retrieval"]
    gold_ood = o(TEST, "r2ood_gold_test_rs")
    a(P(f"Số đoạn k được chọn trên dev là k = 5. **Hệ thống cuối** (Reader E5 + hybrid top-5) đạt trên test **EM "
        f"{f(best['EM'])} / F1 {f(best['F1'])} / HasAns-F1 {f(best['HasAns_F1'])} / NoAns {f(best['NoAns_acc'])}**. "
        "Trên test, k = 3 cho F1 cao hơn một chút (54,0), nhưng nhóm giữ k = 5 vì đây là lựa chọn trên dev. "
        "BM25 và hybrid gần bằng nhau, cả hai hơn hẳn dense."))
    a(P(f"**E3 — tách lỗi tìm và lỗi đọc (RQ2):** đoạn đúng nằm trong top-5 ở {f(rt['gold_in_ctx'])}% câu trả lời được. "
        f"Khi retriever tìm đúng, HasAns-F1 là {f(rt['HasAns_F1_hit'])}, gần bằng mức khi cho sẵn đoạn đúng. Khi tìm sai, "
        f"HasAns-F1 chỉ còn {f(rt['HasAns_F1_miss'])}. Từ \"cho sẵn đoạn đúng\" (F1 {f(gold_ood['F1'])}) sang \"tự tìm\" mất "
        f"{f(gold_ood['F1'] - best['F1'])} điểm F1. Như vậy phần lớn sai số còn lại nằm ở **khâu đọc**. Mô hình sinh hầu "
        f"như không bịa: {f(TEST['r2ood_hybrid_k5_test_rs']['pred_in_ctx'])}% câu trả lời xuất hiện nguyên văn trong đoạn đã đọc."))

    # 5.5 threshold
    a(H2("5.5. Ngưỡng từ chối"))
    a(P("Trên test, với Reader R2 đọc đoạn đúng, ngưỡng δ chọn trên dev làm NoAns tăng +2,0 [+0,8; +3,4] nhưng HasAns-F1 "
        "giảm −1,6 [−2,6; −0,8]. Tổng F1 thay đổi −0,5 [−1,3; +0,2], không có ý nghĩa thống kê. Ngưỡng vì vậy chỉ là núm "
        "điều chỉnh giữa \"thận trọng\" và \"mạnh dạn\", không phải một cải tiến. Cấu hình mặc định dùng greedy."))

    # 5.6 E6
    a(H2("5.6. Theo miền và loại câu hỏi (E6)"))
    cfg = [("R2 · đoạn đúng", "r2m_gold_test_rs"), ("R2 + ngoài miền · đoạn đúng", "r2ood_gold_test_rs"),
           ("R2 + ngoài miền · hybrid top-5", "r2ood_hybrid_k5_test_rs")]
    a(TABLE(["Cấu hình (test)", "Lịch sử Việt Nam", "Lịch sử thế giới"],
            [[n, f(TEST[k]["by_domain"]["VN"]["F1"]), f(TEST[k]["by_domain"]["TG"]["F1"])] for n, k in cfg],
            [4600, 2200, 2200], "F1 theo miền trên test"))
    a(IMG(FIG / "f1_by_domain_test.png", 13.5, "F1 trên test theo miền"))
    a(IMG(FIG / "f1_by_qtype_test.png", 13.5, "F1 theo loại câu hỏi của hệ thống cuối trên test"))
    a(P("Câu hỏi về lịch sử Việt Nam dễ hơn lịch sử thế giới một chút ở mọi cấu hình. Dữ liệu ngoài miền giúp cả hai "
        "miền. Theo loại câu hỏi, câu \"ở đâu\", \"khi nào\" và \"ai\" dễ nhất, vì đáp án ngắn và là thực thể. Câu \"vì "
        "sao\" và \"như thế nào\" khó nhất, vì đáp án dài và khó xác định ranh giới."))

    # 5.7 reliability
    a(H2("5.7. Độ ổn định"))
    a(P("Huấn luyện lại R2 với 3 seed (42, 13, 7). F1 test khi đọc đoạn đúng là **57,3 ± 0,5**, hybrid top-5 là **51,6 ± "
        "0,9**. NoAns dao động nhiều hơn (± 5). Các chênh lệch dưới khoảng 1 điểm F1 vì vậy nằm trong nhiễu giữa các lần "
        "huấn luyện. Báo cáo dựa vào khoảng tin cậy bootstrap thay vì so điểm đơn lẻ."))

    # 5.8 targets
    a(H2("5.8. So với mục tiêu đặt ra"))
    rec5 = TEST["r2m_hybrid_k5_test_rs"]["retrieval"]["gold_in_ctx"]
    hasf1 = max(o(TEST, "r2m_gold_test_rs")["HasAns_F1"], gold_ood["HasAns_F1"])
    ok = lambda b: "Đạt" if b else "**Chưa đạt**"  # noqa: E731
    a(TABLE(["Chỉ số (test)", "Mục tiêu", "Đạt được", "Kết luận"],
            [["Retriever Recall@5", "≥ 80", f(rec5), ok(rec5 >= 80)],
             ["Reader trên đoạn đúng, HasAns-F1", "≥ 70", f(hasf1), ok(hasf1 >= 70)],
             ["Toàn hệ thống, F1", "≥ 55", f(best["F1"]), ok(best["F1"] >= 55)],
             ["NoAns-acc (Reader E5, đoạn đúng)", "≥ 60", f(gold_ood["NoAns_acc"]), ok(gold_ood["NoAns_acc"] >= 60)],
             ["ViT5 fine-tune so với zero-shot (dev, F1)", "cải thiện rõ", f"{f(BASE['b2_gold_dev']['overall']['F1'])} → {f(r2d['F1'])}", "Đạt"]],
            [3900, 1400, 1700, 2000], "So sánh với các chỉ số mục tiêu đặt ra khi lập kế hoạch"))
    a(NOTE(f"Các mục tiêu là ước lượng lúc lập kế hoạch. Toàn hệ thống đạt F1 {f(best['F1'])}, thấp hơn mục tiêu 55 khoảng "
           f"{f(55 - best['F1'])} điểm. Nhóm giữ nguyên con số này và không chấm lại test. Mục 6 phân tích nguyên nhân, và một "
           "hướng cải tiến đã thử trên dev được trình bày ở mục 8.3.", "warn"))

    # ------------------------------------------------------------ 6. PHÂN TÍCH LỖI
    chapter(6)
    a(H1("6. PHÂN TÍCH LỖI"))
    a(P("Từ 779 câu sai (EM = 0) của hệ thống cuối trên test, lấy ngẫu nhiên 100 câu (seed 0). Với mỗi câu, người chấm "
        "đọc câu hỏi, đáp án chuẩn, dự đoán, đoạn văn đúng và đoạn mô hình đã dùng, rồi gán một nhãn chính. Công cụ "
        "(`src/eval/error_analysis.py`) gợi ý nhãn từ các cờ tự động; nhãn gợi ý trùng nhãn chấm tay ở 70% số câu."))
    names = {"trap": "Trả lời câu bẫy (câu không trả lời được)", "paraphrase": "Đúng nhưng khác cách viết",
             "reader_span": "Đọc sai span (có đoạn đúng)", "retrieval": "Tìm sai đoạn (đoạn đúng ngoài top-5)",
             "reader_refuse": "Từ chối nhầm", "selection": "Chọn nhầm đoạn (đoạn đúng có trong top-5)",
             "gold_issue": "Đáp án chuẩn có vấn đề", "tokenizer": "Lỗi bộ từ vựng ViT5", "hallucination": "Bịa (đáp án không có trong đoạn)"}
    ex = {"trap": "\"Quân Chiêm dẫn quân **vào** Thăng Long tháng mấy?\" (đoạn văn: quân Chiêm **rút về**) → \"tháng 12\"",
          "paraphrase": "\"năm 1910\" so với \"1910\"; \"Hiệp ước Versailles\" so với \"Versailles\"",
          "reader_span": "trích câu liền sau câu chứa đáp án; thiếu nửa sau của đáp án dài",
          "retrieval": "câu hỏi quá chung: \"Khuyết điểm của vua Louis là gì?\"",
          "reader_refuse": "cần suy luận: ông nội của Trần Cảnh = cha của Trần Thừa",
          "selection": "đoạn đúng ở hạng 1, nhưng đáp án lấy từ đoạn về nhà Đông Hán",
          "gold_issue": "câu gắn nhãn không trả lời được nhưng đoạn văn có đáp án",
          "tokenizer": "\"François II\" → \"Franois II\"; \"Mahātmā\" → \"Mahtm\"", "hallucination": "không gặp trong mẫu"}
    cnt = ERR["label"].value_counts()
    order = sorted(names, key=lambda k: -cnt.get(k, 0))
    a(TABLE(["Nhóm lỗi", "Số câu / 100", "Ví dụ"],
            [[names[k], str(int(cnt.get(k, 0))), ex[k]] for k in order],
            [3300, 1300, 4400], "Phân loại 100 câu sai của hệ thống cuối trên test", ["left", "center", "left"]))
    a(IMG(FIG / "error_types.png", 13.0, "Phân bố các nhóm lỗi trong 100 câu sai"))
    a(P("**Nhận xét chính:**"))
    a(BUL(["**Khâu đọc là nút thắt, không phải khâu tìm.** Lỗi do khâu đọc (câu bẫy, span, từ chối nhầm) chiếm 52%. Lỗi do khâu tìm và chọn đoạn chỉ chiếm 19%. Kết quả này khớp với E3.",
           "**Câu bẫy là điểm yếu lớn nhất (28%).** Câu bẫy của ViQuAD gần trùng đoạn văn, chỉ đổi một chi tiết (\"đại biểu\" thành \"người dân\", \"hằng năm\" thành \"hàng tháng\"). Reader vẫn trích đáp án mồi.",
           "**Khoảng 27% \"lỗi\" thật ra chấp nhận được** (20% khác cách viết, 7% đáp án chuẩn có vấn đề). Độ chính xác thực tế khi người chấm cao hơn EM 39,4. F1 phản ánh tốt hơn EM, nhưng vẫn phạt các đáp án đúng mà dài hơn.",
           "**Hệ thống gần như không bịa.** Trên toàn bộ 779 câu sai, cờ tự động chỉ thấy 14 câu có đáp án không nằm trong đoạn văn. Trong đó 12 câu là lỗi bộ từ vựng: ViT5 không có các ký tự như ç, ā trong từ vựng nên làm rơi chúng. 9/887 đáp án chuẩn của test (1,0%) không qua được tokenizer nguyên vẹn.",
           "**Chọn đoạn bằng log-prob trung bình chưa tốt (7%).** Điểm tin cậy của các đoạn khác nhau không so sánh được trực tiếp với nhau."]))
    a(P("Lỗi bộ từ vựng sửa được bằng hậu xử lý: tìm trong đoạn văn chuỗi gốc khớp với dự đoán sau khi bỏ các ký tự "
        "ngoài từ vựng. Cách này làm F1 test của hệ thống cuối tăng từ 53,37 lên 53,58, nhưng không đổi gì trên dev. Ý "
        "tưởng lại nảy ra từ việc đọc lỗi trên test, nên nhóm **không tính đây là cải tiến** và không sửa số liệu ở "
        "chương 5. Demo dùng hậu xử lý này để hiển thị đúng tên riêng."))

    # ------------------------------------------------------------ 7. DEMO
    chapter(7)
    a(H1("7. DEMO VÀ ĐỘ TRỄ"))
    a(H2("7.1. Giao diện demo"))
    a(P("Demo xây dựng bằng Gradio (`python app.py`), dùng Reader E5 và retriever hybrid. Người dùng nhập câu hỏi và chọn "
        "số đoạn k. Giao diện hiển thị đáp án kèm tên bài và hạng của đoạn nguồn, đoạn văn bằng chứng có tô đậm đáp án, "
        "bảng top-k đoạn (điểm RRF, đáp án Reader đọc được ở từng đoạn, điểm Reader) và thời gian từng khâu (Hình 7.1). "
        "Câu hỏi ngoài phạm vi kho, ví dụ \"Ai là người sáng lập ra Microsoft?\", thì hệ thống trả lời \"không có câu trả "
        "lời\"."))
    a(IMG(FIG / "demo_gradio.png", 15.5, "Demo Gradio: câu hỏi về chồng của Mary Stuart, đáp án François II được tô đậm trong đoạn bằng chứng"))
    a(P("Hình 7.1 cũng minh hoạ lỗi bộ từ vựng ở mục 6. Cột \"Đáp án đọc được\" là đầu ra thô của ViT5 (\"Franois II\"); "
        "đáp án hiển thị đã được khôi phục từ đoạn văn (\"François II\")."))
    a(H2("7.2. Độ trễ"))
    latrows = []
    for d in ("cuda", "cpu"):
        L = LAT[d]
        for k in ("k1", "k5"):
            v = L["results"][k]
            latrows.append([L["hardware"].replace("(R)", "").replace("(TM)", ""), k[1:],
                            f(v["bm25"]["p50"], 0), f(v["dense"]["p50"], 0), f(v["retrieve"]["p50"], 0),
                            f(v["read"]["p50"], 0), f"**{f(v['total']['p50'], 0)}**"])
    a(TABLE(["Thiết bị", "k", "BM25", "Dense", "Truy hồi", "Reader", "Tổng"], latrows,
            [2900, 600, 900, 900, 1200, 1200, 1300], "Độ trễ mỗi câu hỏi (ms, trung vị; câu hỏi ngẫu nhiên từ dev)"))
    a(BUL(["**Reader chiếm 80–95% thời gian.** Truy hồi rẻ vì kho nhỏ: BM25 khoảng 5 ms; mã hoá câu hỏi khoảng 6 ms trên GPU và 46 ms trên CPU (gồm cả tách từ).",
           "Trên CPU, thời gian Reader tăng gần tuyến tính theo k (208 → 969 ms). Trên GPU, 5 đoạn chạy chung một batch nên chỉ tăng gần gấp đôi (66 → 118 ms).",
           "Cấu hình chính (top-5) mất khoảng 0,13 giây trên GPU và khoảng 1 giây trên CPU, đủ cho sử dụng tương tác."]))

    # ------------------------------------------------------------ 8. KẾT LUẬN
    chapter(8)
    a(H1("8. KẾT LUẬN, HẠN CHẾ VÀ HƯỚNG PHÁT TRIỂN"))
    a(H2("8.1. Kết luận"))
    a(BUL([f"**RQ1:** ViT5 sinh đáp án (R2) vượt mô hình trích xuất XLM-R (F1 dev {f(r2d['F1'])} so với {f(b1['F1'])}), nhờ biết từ chối tốt hơn hẳn. Với câu trả lời được, hai cách gần ngang nhau.",
           "**RQ2:** Hybrid có trọng số vượt từng phương pháp riêng về Recall@5. Ở cấp toàn hệ thống, hybrid và BM25 ngang nhau và cùng hơn hẳn dense. Sai số chủ yếu đến từ khâu đọc: khi retriever tìm đúng, Reader đạt gần như mức khi được cho sẵn đoạn đúng.",
           "**RQ3:** Câu không trả lời được trong dữ liệu huấn luyện là thiết yếu. Bỏ chúng đi thì NoAns giảm 22,8 điểm. Đoạn nhiễu do retriever tìm ra (R2) giúp Reader bền vững khi đọc nhiều đoạn.",
           "**RQ4:** Dữ liệu ngoài miền giúp tăng F1 (+2,9 khi đọc đoạn đúng, có ý nghĩa thống kê) ở cả hai miền. Lịch sử Việt Nam dễ hơn lịch sử thế giới một chút.",
           f"Hệ thống cuối đạt **F1 {f(best['F1'])}** trên test, trả lời mỗi câu trong khoảng 0,13 giây trên GPU, và hầu như không bịa."]))
    a(H2("8.2. Hạn chế"))
    a(BUL(["**Chưa đạt hai mục tiêu:** F1 toàn hệ thống (53,4 so với 55) và HasAns-F1 khi đọc đoạn đúng (khoảng 60 so với 70).",
           "**Tập đánh giá nhỏ:** test chỉ có 7 bài và 1.286 câu, nên khoảng tin cậy rộng khoảng ± 2,5 điểm F1. B1 và R1 chưa được chấm trên test vì checkpoint chỉ lưu trên Colab.",
           "**Nhãn \"lịch sử\" của bài viết kế thừa từ bước rà tay của dự án trước.** Một vài bài chỉ liên quan một phần tới lịch sử, ví dụ Vườn quốc gia Phong Nha - Kẻ Bàng chiếm 327/1.329 câu của dev.",
           "**Phân tích lỗi do một người chấm,** chưa có đánh giá độ đồng thuận giữa nhiều người chấm. Mẫu được lấy từ test, sau khi test đã chấm xong.",
           "**Mô hình:** chỉ dùng ViT5-base; Reader đọc từng đoạn độc lập nên không tổng hợp được thông tin từ nhiều đoạn; đầu vào giới hạn 512 token."]))
    a(H2("8.3. Hướng phát triển"))
    a(BUL(["**Chọn đáp án có xét hạng retriever:** điểm = điểm Reader − λ·(hạng − 1). Thử trên dev (dùng lại dự đoán sẵn có), cách này làm F1 tăng từ 52,92 lên 54,02 (+1,1), ổn định với mọi λ ≥ 0,02. Nhóm **chưa chấm trên test** để giữ nguyên tắc chỉ dùng test một lần.",
           "**Tăng khả năng nhận diện câu bẫy:** sinh thêm câu bẫy khi huấn luyện, hoặc thêm bước kiểm chứng (verifier) so khớp câu hỏi với câu chứa đáp án.",
           "**Reader đọc nhiều đoạn cùng lúc** theo kiểu Fusion-in-Decoder [6], hoặc thử ViT5-large.",
           "**Đánh giá bằng người** cho các câu \"khác cách viết\", để có độ chính xác thực tế bên cạnh EM/F1.",
           "**Mở rộng kho tri thức** ra toàn bộ Wikipedia lịch sử tiếng Việt. Khi đó cần chỉ mục FAISS gần đúng thay vì chấm toàn kho."]))

    # ------------------------------------------------------------ TÀI LIỆU THAM KHẢO
    a(H1("TÀI LIỆU THAM KHẢO"))
    refs = [
        "P. Rajpurkar, R. Jia, P. Liang. Know What You Don't Know: Unanswerable Questions for SQuAD. ACL, 2018.",
        "K. Van Nguyen, S. Q. Tran, L. T. Nguyen, T. V. Huynh, S. T. Luu, N. L.-T. Nguyen. VLSP 2021 - ViMRC Challenge: Vietnamese Machine Reading Comprehension. arXiv:2203.11400, 2022 (bộ dữ liệu UIT-ViQuAD 2.0).",
        "D. Chen, A. Fisch, J. Weston, A. Bordes. Reading Wikipedia to Answer Open-Domain Questions. ACL, 2017.",
        "V. Karpukhin, B. Oğuz, S. Min, P. Lewis, L. Wu, S. Edunov, D. Chen, W. Yih. Dense Passage Retrieval for Open-Domain Question Answering. EMNLP, 2020.",
        "P. Lewis, E. Perez, A. Piktus, et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS, 2020.",
        "G. Izacard, E. Grave. Leveraging Passage Retrieval with Generative Models for Open Domain Question Answering. EACL, 2021.",
        "L. Phan, H. Tran, H. Nguyen, T. H. Trinh. ViT5: Pretrained Text-to-Text Transformer for Vietnamese Language Generation. NAACL Student Research Workshop, 2022.",
        "C. Raffel, N. Shazeer, A. Roberts, et al. Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer. JMLR 21(140), 2020.",
        "S. Robertson, H. Zaragoza. The Probabilistic Relevance Framework: BM25 and Beyond. Foundations and Trends in Information Retrieval 3(4), 2009.",
        "G. V. Cormack, C. L. A. Clarke, S. Büttcher. Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods. SIGIR, 2009.",
        "A. Conneau, K. Khandelwal, N. Goyal, et al. Unsupervised Cross-lingual Representation Learning at Scale. ACL, 2020.",
        "D. Q. Nguyen, A. T. Nguyen. PhoBERT: Pre-trained Language Models for Vietnamese. Findings of EMNLP, 2020.",
        "J. Johnson, M. Douze, H. Jégou. Billion-Scale Similarity Search with GPUs. IEEE Transactions on Big Data 7(3), 2019.",
        "BKAI Foundation Models. vietnamese-bi-encoder. HuggingFace Hub: huggingface.co/bkai-foundation-models/vietnamese-bi-encoder.",
        "B. Efron, R. J. Tibshirani. An Introduction to the Bootstrap. Chapman & Hall/CRC, 1993.",
    ]
    for i, r in enumerate(refs, 1):
        a(para(runs(f"[{i}] {r}"), jc="left", before=40, after=60,
               extra='<w:ind w:left="567" w:hanging="567"/>'))
    return B


# ============================================================== phần đầu
def front_matter() -> list[str]:
    F = []                           # đoạn ngày ở bìa đã có ngắt trang
    F.append(CENTER_TITLE("MỤC LỤC", new_page=False))
    F.append(TOC_FIELD())
    F.append(CENTER_TITLE("DANH MỤC HÌNH ẢNH"))
    F.append(TABLE(["Số hiệu", "Tên hình"], [[f"**{l}**", t] for l, t in FIGS], [1400, 7600], align=["left", "left"]))
    F.append(CENTER_TITLE("DANH MỤC BẢNG BIỂU", new_page=False))
    F.append(TABLE(["Số hiệu", "Tên bảng"], [[f"**{l}**", t] for l, t in TABS], [1400, 7600], align=["left", "left"]))
    F.append(CENTER_TITLE("DANH MỤC TỪ VIẾT TẮT"))
    abbr = [("BM25", "Best Matching 25 – hàm xếp hạng tìm kiếm theo từ khoá"),
            ("CI", "Confidence Interval – khoảng tin cậy"),
            ("Dense", "Truy hồi dày, dựa trên vector ngữ nghĩa"),
            ("EM", "Exact Match – khớp hoàn toàn"),
            ("F1", "Trung bình điều hoà của precision và recall theo âm tiết"),
            ("FAISS", "Facebook AI Similarity Search – thư viện tìm kiếm vector"),
            ("FiD", "Fusion-in-Decoder"),
            ("HasAns / NoAns", "Nhóm câu trả lời được / không trả lời được"),
            ("MRC", "Machine Reading Comprehension – đọc hiểu máy"),
            ("MRR", "Mean Reciprocal Rank"),
            ("QA", "Question Answering – hỏi đáp"),
            ("R@k", "Recall@k – tỉ lệ câu hỏi có đoạn đúng trong top-k"),
            ("RAG", "Retrieval-Augmented Generation"),
            ("RQ", "Research Question – câu hỏi nghiên cứu"),
            ("RRF", "Reciprocal Rank Fusion – gộp thứ hạng nghịch đảo"),
            ("TG / VN", "Lịch sử thế giới / lịch sử Việt Nam"),
            ("ViQuAD", "Vietnamese Question Answering Dataset"),
            ("ViT5", "Mô hình T5 huấn luyện trước cho tiếng Việt")]
    F.append(TABLE(["Từ viết tắt", "Ý nghĩa"], [[f"**{a}**", b] for a, b in abbr], [2200, 6800], align=["left", "left"]))
    F.append(CENTER_TITLE("BẢNG PHÂN CÔNG CÔNG VIỆC"))
    work = [
        ("Nguyễn Bình Nguyên - 250201078", "Nhóm trưởng", "32,5%",
         ["[GĐ0 – Dọn dẹp và bảo mật]", "• Đánh giá dự án cũ, thu hồi API key lộ, dựng lại repo, ghim requirements.txt",
          "[GĐ1 – Dữ liệu]", "• Rà soát và sửa 5 nhóm lỗi dữ liệu (1.988 câu không nhãn, plausible_answer, id trùng, lệch vị trí)",
          "• Chia train/dev/test theo bài, test chống rò rỉ; thống kê độ dài token",
          "[GĐ2 – Retriever]", "• BM25 âm tiết/tách từ, dense bi-encoder + FAISS, RRF có trọng số; quét tham số trên dev",
          "[Báo cáo]", "• Viết chương 2–3, slide trình bày"]),
        ("Hoàng Hải Đăng - 2502010484", "Thành viên", "32,5%",
         ["[GĐ3 – Thước đo và baseline]", "• Metric EM/F1 tiếng Việt kiểu SQuAD 2.0, định dạng dự đoán chung, công cụ chấm",
          "• Baseline B0 (ngẫu nhiên), B1 (XLM-R trích xuất, Colab), B2 (ViT5 zero-shot)",
          "[GĐ6 – Demo và độ trễ]", "• Pipeline dùng chung, demo Gradio, đo độ trễ CPU/GPU",
          "[GĐ7 – Tổng hợp]", "• results.md, biểu đồ, README tái lập", "[Báo cáo]", "• Viết chương 4 và 7"]),
        ("Trần Anh Hào - 250201058", "Thành viên", "35%",
         ["[GĐ4 – Reader ViT5]", "• Dữ liệu R1/R2 (đoạn nhiễu), huấn luyện ViT5 trên Colab và GPU local, sửa lỗi đánh giá dev",
          "[GĐ5 – Thí nghiệm E1–E6]", "• Dò tham số, ngưỡng từ chối, E4/E5, 3 seed, bootstrap CI, chạy test một lần",
          "[GĐ6 – Phân tích lỗi]", "• Phân loại 100 câu sai, hậu xử lý ký tự ngoài từ vựng",
          "[Báo cáo]", "• Viết chương 1, 5, 6, 8; tổng hợp báo cáo"]),
    ]
    widths = [700, 2100, 1300, 3900, 1000]
    rows = []
    for i, (name, role, pct, items) in enumerate(work, 1):
        rows.append([str(i), name, role, items, pct])
    # bảng tự dựng để ô nội dung có nhiều đoạn
    borders = "".join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="8C8C8C"/>'
                      for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
    x = (f'<w:tbl><w:tblPr><w:tblW w:w="{sum(widths)}" w:type="dxa"/><w:jc w:val="center"/><w:tblBorders>{borders}'
         f'</w:tblBorders><w:tblLayout w:type="fixed"/></w:tblPr><w:tblGrid>'
         + "".join(f'<w:gridCol w:w="{w}"/>' for w in widths) + "</w:tblGrid>")
    x += ('<w:tr><w:trPr><w:tblHeader/></w:trPr>' + "".join(
        _cell(h, w, DARK, True, "FFFFFF", "center") for h, w in
        zip(["STT", "Thành viên", "Vai trò", "Nội dung công việc chi tiết", "Đóng góp"], widths)) + "</w:tr>")
    for r in rows:
        items = [("**" + t + "**") if t.startswith("[") else t for t in r[3]]
        x += ("<w:tr>" + _cell(r[0], widths[0], DARK, True, "FFFFFF", "center")
              + _cell(r[1], widths[1], LIGHT, True, None, "center") + _cell(r[2], widths[2], LIGHT, True, None, "center")
              + _cell(items, widths[3], "F7F9FC", False, None, "left") + _cell(r[4], widths[4], "E2F0D9", True, None, "center")
              + "</w:tr>")
    x += ("<w:tr>" + _cell("", widths[0], DARK) + _cell("", widths[1], DARK) + _cell("", widths[2], DARK)
          + _cell("TỔNG CỘNG", widths[3], DARK, True, "FFFFFF", "center") + _cell("100%", widths[4], "1E7145", True, "FFFFFF", "center")
          + "</w:tr></w:tbl>")
    F.append(x)
    F.append(para(runs("Ghi chú:", bold=True), jc="left", before=160, after=40))
    F.append(para(runs("• Tổng đóng góp: 32,5% + 32,5% + 35% = 100%."), jc="left", before=0, after=30))
    F.append(para(runs("• Cả ba thành viên cùng tham gia kiểm thử, chạy lại kết quả và demo hệ thống."), jc="left", before=0, after=30))
    return F


# ============================================================== ráp file
def split_body(xml: str) -> tuple[str, list[str], str]:
    s, e = xml.index("<w:body>") + 8, xml.rindex("</w:body>")
    body_xml = xml[s:e]
    tag_re = re.compile(r"<(/?)(w:p|w:tbl|w:sectPr)\b[^>]*?(/?)>")
    els, depth, start, cur = [], 0, None, None
    for m in tag_re.finditer(body_xml):
        close, name, selfclose = m.group(1), m.group(2), m.group(3)
        if depth == 0 and not close:
            start, cur = m.start(), name
            if selfclose:
                els.append(body_xml[start:m.end()])
                continue
            depth = 1
            continue
        if name == cur:
            if close:
                depth -= 1
                if depth == 0:
                    els.append(body_xml[start:m.end()])
            elif not selfclose:
                depth += 1
    return xml[:s], els, xml[e:]


def set_text(p_xml: str, text: str) -> str:
    """Thay chữ của đoạn (giữ định dạng run đầu tiên, xoá các run chữ sau)."""
    ts = list(re.finditer(r"<w:t( [^>]*)?>[^<]*</w:t>", p_xml))
    first = ts[0]
    out = p_xml[:first.start()] + f'<w:t xml:space="preserve">{escape(text)}</w:t>'
    rest = p_xml[first.end():]
    rest = re.sub(r"<w:t( [^>]*)?>[^<]*</w:t>", "", rest)
    return out + rest


def add_toc_styles(styles: str) -> str:
    """Thêm style TOC 1/TOC 2 gọn (bản cũ không có, Word dùng mặc định cách dòng rộng)."""
    def st(sid, name, ind, bold):
        b = "<w:b/><w:bCs/>" if bold else ""
        return (f'<w:style w:type="paragraph" w:styleId="{sid}"><w:name w:val="{name}"/><w:basedOn w:val="Normal"/>'
                f'<w:next w:val="Normal"/><w:uiPriority w:val="39"/><w:unhideWhenUsed/><w:pPr>'
                f'<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9350"/></w:tabs>'
                f'<w:spacing w:before="{60 if bold else 0}" w:after="20" w:line="264" w:lineRule="auto"/>'
                f'<w:ind w:left="{ind}"/></w:pPr><w:rPr>{FONT}{b}<w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>')
    if 'w:styleId="TOC1"' in styles:
        return styles
    return styles.replace("</w:styles>", st("TOC1", "toc 1", 0, True) + st("TOC2", "toc 2", 360, False) + "</w:styles>")


def main():
    z = zipfile.ZipFile(OLD)
    doc = z.read("word/document.xml").decode("utf-8")
    head, els, tail = split_body(doc)
    assert "HỆ HỖ TRỢ RA QUYẾT ĐỊNH SINH" in els[14] and "Nguyễn Bình Nguyên" in els[19] and "tháng 7" in els[31]
    sect = els[-1]
    assert sect.startswith("<w:sectPr")

    cover = els[:32]
    cover[14] = set_text(cover[14], TITLE)
    member_tpl = cover[19]
    new_members = [set_text(member_tpl, f"{i}. {n} - {m}") for i, (n, m) in enumerate(MEMBERS, 1)]
    blank = cover[24]
    cover = cover[:19] + new_members + [blank, blank] + cover[24:]
    cover[-1] = set_text(cover[-1], DATE)

    content = body()                 # phải chạy trước front_matter (điền FIGS/TABS)
    front = front_matter()
    new_body = "".join(cover) + "".join(front) + "".join(content) + sect
    # đoạn đệm rỗng sau bảng/ghi chú ngay trước tiêu đề có ngắt trang -> bỏ (tránh trang trắng)
    spacer = para("", before=0, after=60)
    n0 = new_body.count(spacer)
    new_body = re.sub(re.escape(spacer) + r'(?=<w:p><w:pPr>(?:<w:pStyle w:val="Heading1"/><w:keepNext/>)?<w:pageBreakBefore/>)',
                      "", new_body)
    print(f"bỏ {n0 - new_body.count(spacer)} đoạn đệm trước ngắt trang")

    # ảnh: giữ ảnh ở bìa (logo), bỏ ảnh cũ không dùng, thêm ảnh mới
    rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
    keep = set(re.findall(r'r:embed="(rId\d+)"', "".join(cover)))
    rel_items = re.findall(r"<Relationship [^>]*/>", rels)
    new_rels, keep_media = [], set()
    for r in rel_items:
        rid = re.search(r'Id="([^"]+)"', r).group(1)
        if "/image" in r and rid not in keep:
            continue
        if "/image" in r:
            keep_media.add("word/" + re.search(r'Target="([^"]+)"', r).group(1))
        new_rels.append(r)
    for rid, path in MEDIA.items:
        new_rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                        f'relationships/image" Target="media/new_{path.name}"/>')
    rels_xml = rels[:rels.index("<Relationship ")] + "".join(new_rels) + "</Relationships>"

    NEW.parent.mkdir(parents=True, exist_ok=True)
    tmp = NEW.with_suffix(".tmp.docx")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        for item in z.infolist():
            n = item.filename
            if n.endswith("/"):
                continue
            if n.startswith("word/media/") and n not in keep_media:
                continue
            if n == "word/document.xml":
                out.writestr(n, head + new_body + tail)
            elif n == "word/styles.xml":
                out.writestr(n, add_toc_styles(z.read(n).decode("utf-8")))
            elif n == "word/_rels/document.xml.rels":
                out.writestr(n, rels_xml)
            else:
                out.writestr(item, z.read(n))
        for rid, path in MEDIA.items:
            out.write(path, f"word/media/new_{path.name}")
    shutil.move(tmp, NEW)
    print(f"-> {NEW}  ({NEW.stat().st_size / 1e6:.1f} MB; {len(FIGS)} hình, {len(TABS)} bảng)")


if __name__ == "__main__":
    main()
