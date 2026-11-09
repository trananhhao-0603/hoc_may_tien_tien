"""
Cập nhật mục TÀI LIỆU THAM KHẢO trong file Word ĐÃ ĐƯỢC SỬA TAY (không dựng lại báo cáo):
thay chữ của 15 đoạn [1]..[15] bằng trích dẫn đã kiểm chứng + hyperlink (DOI / ACL Anthology / arXiv),
giữ nguyên định dạng đoạn và phần còn lại của tài liệu.

    python scripts/add_reference_links.py baocao/<file>.docx
"""
from __future__ import annotations

import re
import shutil
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

# (văn bản trích dẫn, [(nhãn, url), ...]) — mọi link đã kiểm tra ngày 09/11/2026
REFS = [
    ("P. Rajpurkar, R. Jia, P. Liang. Know What You Don't Know: Unanswerable Questions for SQuAD. ACL 2018, tr. 784–789.",
     [("https://aclanthology.org/P18-2124/", "https://aclanthology.org/P18-2124/")]),
    ("K. Van Nguyen, S. Q. Tran, L. T. Nguyen, T. V. Huynh, S. T. Luu, N. L.-T. Nguyen. VLSP 2021 - ViMRC Challenge: "
     "Vietnamese Machine Reading Comprehension. arXiv:2203.11400, 2022 (bộ dữ liệu UIT-ViQuAD 2.0).",
     [("https://arxiv.org/abs/2203.11400", "https://arxiv.org/abs/2203.11400"),
      ("Dữ liệu: https://huggingface.co/datasets/taidng/UIT-ViQuAD2.0", "https://huggingface.co/datasets/taidng/UIT-ViQuAD2.0")]),
    ("D. Chen, A. Fisch, J. Weston, A. Bordes. Reading Wikipedia to Answer Open-Domain Questions. ACL 2017, tr. 1870–1879.",
     [("https://aclanthology.org/P17-1171/", "https://aclanthology.org/P17-1171/")]),
    ("V. Karpukhin, B. Oğuz, S. Min, P. Lewis, L. Wu, S. Edunov, D. Chen, W. Yih. Dense Passage Retrieval for "
     "Open-Domain Question Answering. EMNLP 2020, tr. 6769–6781.",
     [("https://aclanthology.org/2020.emnlp-main.550/", "https://aclanthology.org/2020.emnlp-main.550/")]),
    ("P. Lewis, E. Perez, A. Piktus, et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. "
     "NeurIPS 2020 (Advances in Neural Information Processing Systems 33).",
     [("https://arxiv.org/abs/2005.11401", "https://arxiv.org/abs/2005.11401")]),
    ("G. Izacard, E. Grave. Leveraging Passage Retrieval with Generative Models for Open Domain Question Answering. "
     "EACL 2021, tr. 874–880.",
     [("https://aclanthology.org/2021.eacl-main.74/", "https://aclanthology.org/2021.eacl-main.74/")]),
    ("L. Phan, H. Tran, H. Nguyen, T. H. Trinh. ViT5: Pretrained Text-to-Text Transformer for Vietnamese Language "
     "Generation. NAACL 2022 Student Research Workshop, tr. 136–142.",
     [("https://aclanthology.org/2022.naacl-srw.18/", "https://aclanthology.org/2022.naacl-srw.18/")]),
    ("C. Raffel, N. Shazeer, A. Roberts, et al. Exploring the Limits of Transfer Learning with a Unified Text-to-Text "
     "Transformer. JMLR 21(140):1–67, 2020.",
     [("https://jmlr.org/papers/v21/20-074.html", "https://jmlr.org/papers/v21/20-074.html")]),
    ("S. Robertson, H. Zaragoza. The Probabilistic Relevance Framework: BM25 and Beyond. Foundations and Trends in "
     "Information Retrieval 3(4):333–389, 2009.",
     [("https://doi.org/10.1561/1500000019", "https://doi.org/10.1561/1500000019")]),
    ("G. V. Cormack, C. L. A. Clarke, S. Büttcher. Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank "
     "Learning Methods. SIGIR 2009, tr. 758–759.",
     [("https://doi.org/10.1145/1571941.1572114", "https://doi.org/10.1145/1571941.1572114")]),
    ("A. Conneau, K. Khandelwal, N. Goyal, et al. Unsupervised Cross-lingual Representation Learning at Scale. "
     "ACL 2020, tr. 8440–8451.",
     [("https://aclanthology.org/2020.acl-main.747/", "https://aclanthology.org/2020.acl-main.747/")]),
    ("D. Q. Nguyen, A. T. Nguyen. PhoBERT: Pre-trained Language Models for Vietnamese. Findings of EMNLP 2020, "
     "tr. 1037–1042.",
     [("https://aclanthology.org/2020.findings-emnlp.92/", "https://aclanthology.org/2020.findings-emnlp.92/")]),
    ("J. Johnson, M. Douze, H. Jégou. Billion-Scale Similarity Search with GPUs. IEEE Transactions on Big Data "
     "7(3):535–547, 2019.",
     [("https://doi.org/10.1109/TBDATA.2019.2921572", "https://doi.org/10.1109/TBDATA.2019.2921572")]),
    ("N. Q. Duc, L. H. Son, N. D. Nhan, N. D. N. Minh, L. T. Huong, D. V. Sang. Towards Comprehensive Vietnamese "
     "Retrieval-Augmented Generation and Large Language Models. arXiv:2403.01616, 2024 (mô hình "
     "bkai-foundation-models/vietnamese-bi-encoder, dựa trên PhoBERT-base-v2).",
     [("https://arxiv.org/abs/2403.01616", "https://arxiv.org/abs/2403.01616"),
      ("Mô hình: https://huggingface.co/bkai-foundation-models/vietnamese-bi-encoder",
       "https://huggingface.co/bkai-foundation-models/vietnamese-bi-encoder")]),
    ("B. Efron, R. J. Tibshirani. An Introduction to the Bootstrap. Chapman & Hall/CRC, 1993.",
     [("https://doi.org/10.1201/9780429246593", "https://doi.org/10.1201/9780429246593")]),
]

HL_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"


def para_text(p: str) -> str:
    return "".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", p))


def main(path: Path):
    src = zipfile.ZipFile(path)
    doc = src.read("word/document.xml").decode("utf-8")
    rels = src.read("word/_rels/document.xml.rels").decode("utf-8")

    start = doc.index("TÀI LIỆU THAM KHẢO")
    paras = [(m.start(), m.end()) for m in re.finditer(r"<w:p[ >].*?</w:p>", doc[start:], flags=re.S)]
    targets = {}
    for a, b in paras:
        p = doc[start + a:start + b]
        m = re.match(r"\[(\d+)\] ", para_text(p))
        if m:
            targets[int(m.group(1))] = (start + a, start + b, p)
    assert sorted(targets) == list(range(1, len(REFS) + 1)), f"tìm thấy {sorted(targets)}"

    existing = set(re.findall(r'Id="([^"]+)"', rels))
    new_rels, rid_n = [], 0

    def rid_for(url):
        nonlocal rid_n
        while True:
            rid_n += 1
            rid = f"rIdRef{rid_n}"
            if rid not in existing:
                break
        new_rels.append(f'<Relationship Id="{rid}" Type="{HL_TYPE}" Target="{escape(url)}" TargetMode="External"/>')
        return rid

    out, pos = [], 0
    for n in sorted(targets):
        a, b, p = targets[n]
        ppr = re.search(r"<w:pPr>.*?</w:pPr>", p, flags=re.S)
        ppr = ppr.group(0) if ppr else ""
        rpr = re.search(r"<w:r(?: [^>]*)?><w:rPr>(.*?)</w:rPr>", p, flags=re.S)
        rpr = rpr.group(1) if rpr else ""
        text, links = REFS[n - 1]
        runs = f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">[{n}] {escape(text)} </w:t></w:r>'
        for i, (label, url) in enumerate(links):
            if i:
                runs += f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve"> · </w:t></w:r>'
            link_rpr = re.sub(r"<w:color [^>]*/>|<w:u [^>]*/>", "", rpr) + '<w:color w:val="0563C1"/><w:u w:val="single"/>'
            runs += (f'<w:hyperlink r:id="{rid_for(url)}" w:history="1"><w:r><w:rPr>{link_rpr}</w:rPr>'
                     f'<w:t xml:space="preserve">{escape(label)}</w:t></w:r></w:hyperlink>')
        out.append(doc[pos:a] + f"<w:p>{ppr}{runs}</w:p>")
        pos = b
    out.append(doc[pos:])
    new_doc = "".join(out)
    new_rels_xml = rels.replace("</Relationships>", "".join(new_rels) + "</Relationships>")

    tmp = path.with_suffix(".tmp.docx")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for item in src.infolist():
            if item.filename.endswith("/"):
                continue
            if item.filename == "word/document.xml":
                z.writestr(item, new_doc)
            elif item.filename == "word/_rels/document.xml.rels":
                z.writestr(item, new_rels_xml)
            else:
                z.writestr(item, src.read(item.filename))
    src.close()
    shutil.move(tmp, path)
    print(f"Đã cập nhật {len(targets)} tài liệu tham khảo, thêm {len(new_rels)} hyperlink -> {path}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
