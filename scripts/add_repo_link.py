"""
Thêm link repo GitHub vào báo cáo Word đã sửa tay (mục 1.4 và 5.1), giữ nguyên phần còn lại.

    python scripts/add_repo_link.py baocao/<file>.docx
"""
from __future__ import annotations

import re
import shutil
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

URL = "https://github.com/trananhhao-0603/hoc_may_tien_tien"
HL_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"
FONT = ('<w:rFonts w:ascii="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman" '
        'w:hAnsi="Times New Roman"/>')


def run(text, bold=False):
    b = "<w:b/><w:bCs/>" if bold else ""
    return (f'<w:r><w:rPr>{FONT}{b}<w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>'
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r>')


def link(rid):
    return (f'<w:hyperlink r:id="{rid}" w:history="1"><w:r><w:rPr>{FONT}<w:color w:val="0563C1"/>'
            f'<w:u w:val="single"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>'
            f'<w:t xml:space="preserve">{URL}</w:t></w:r></w:hyperlink>')


def para_text(p):
    return "".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", p))


def find_para(doc, startswith=None, contains=None):
    for m in re.finditer(r"<w:p[ >].*?</w:p>", doc, flags=re.S):
        t = para_text(m.group(0))
        if (startswith and t.startswith(startswith)) or (contains and contains in t):
            return m.start(), m.end()
    raise SystemExit(f"không tìm thấy đoạn: {startswith or contains}")


def main(path: Path):
    src = zipfile.ZipFile(path)
    doc = src.read("word/document.xml").decode("utf-8")
    rels = src.read("word/_rels/document.xml.rels").decode("utf-8")
    if URL in rels:
        raise SystemExit("Đã có link repo, bỏ qua.")
    rid = "rIdRepo1"
    rels = rels.replace("</Relationships>",
                        f'<Relationship Id="{rid}" Type="{HL_TYPE}" Target="{URL}" TargetMode="External"/></Relationships>')

    # 5.1: nối câu vào cuối đoạn thiết lập
    a, b = find_para(doc, contains="Nếu không ghi khác, kết quả dùng giải mã greedy.")
    p = doc[a:b]
    p = p[:p.rindex("</w:p>")] + run(" Mã nguồn, dữ liệu đã xử lý và các file kết quả (reports/) có tại ") + link(rid) \
        + run("; README hướng dẫn chạy lại từng bảng.") + "</w:p>"
    doc = doc[:a] + p + doc[b:]

    # 1.4: đoạn mới ngay sau gạch đầu dòng cuối cùng ("Mã nguồn tái lập được...")
    a, b = find_para(doc, contains="Mã nguồn tái lập được")
    new_p = ('<w:p><w:pPr><w:spacing w:before="120" w:after="80" w:line="288" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>'
             + run("Mã nguồn: ", bold=True) + link(rid)
             + run(" (mã, dữ liệu đã xử lý, toàn bộ bảng kết quả và lịch sử commit; checkpoint mô hình không đưa lên "
                   "vì dung lượng lớn, có thể huấn luyện lại theo README).") + "</w:p>")
    doc = doc[:b] + new_p + doc[b:]

    tmp = path.with_suffix(".tmp.docx")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for item in src.infolist():
            if item.filename.endswith("/"):
                continue
            if item.filename == "word/document.xml":
                z.writestr(item, doc)
            elif item.filename == "word/_rels/document.xml.rels":
                z.writestr(item, rels)
            else:
                z.writestr(item, src.read(item.filename))
    src.close()
    shutil.move(tmp, path)
    print("Đã thêm link repo vào mục 1.4 và 5.1 ->", path)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
