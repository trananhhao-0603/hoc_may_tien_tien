/*
 * Giai đoạn 7 — slide trình bày (pptxgenjs). Phong cách theo slide cũ của nhóm: nền trắng, đỏ đô / vàng đồng /
 * nâu đen, nhãn "PHẦN X · ..." trên tiêu đề, thẻ bo góc, slide cuối nền tối. Số liệu đọc từ reports/*.json.
 *
 *   NODE_PATH=<thư mục có node_modules/pptxgenjs> node scripts/build_slides.js <out.pptx> [apply_theme.js]
 */
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const ROOT = path.resolve(__dirname, "..");
const REP = path.join(ROOT, "reports");
const FIG = path.join(REP, "figures");
const OUT = process.argv[2] || path.join(ROOT, "baocao/slides.pptx");
const APPLY_THEME = process.argv[3];

// file JSON do Python ghi có thể chứa NaN (không hợp lệ theo chuẩn JSON) -> đổi thành null
const J = (n) => JSON.parse(fs.readFileSync(path.join(REP, n + ".json"), "utf8").replace(/\bNaN\b/g, "null"));
const RET = J("retriever_dev"), BASE = J("baselines_dev"), DEV = J("gd5_dev"), TEST = J("gd5_test");
const LAT = { cuda: J("latency_cuda"), cpu: J("latency_cpu") };
const ERR = fs.readFileSync(path.join(REP, "error_labels.csv"), "utf8").trim().split(/\r?\n/).slice(1)
  .map((l) => l.split(",")[1]);
const o = (d, k) => d[k].overall;
const png = (file) => { const b = fs.readFileSync(file); return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) }; };
const f = (x, nd = 1) => x.toFixed(nd).replace(".", ",");

// ------------------------------------------------------------------ bảng màu (lấy từ slide cũ)
const INK = "2B2430", MAROON = "8E1F2F", MAROON_D = "6E1622", GOLD = "A8841C", GOLD_L = "C9A227",
  MUTED = "756A70", ROSE = "F7EDEE", ROSE_L = "E4DADC", CREAM = "FAF3DC", SAND = "E8DCCF",
  BLUE = "3E6990", BLUE_L = "E9EFF5", GREEN = "3E7C4F", GREEN_L = "EAF3EC", WHITE = "FFFFFF", LINE = "E4DADC";
const HEAD = "Cambria", BODY = "Calibri", MONO = "Courier New";

const THEME = {
  name: "HMTT Lịch sử", headFontFace: HEAD, bodyFontFace: BODY,
  colors: { dk1: INK, lt1: WHITE, dk2: MAROON_D, lt2: ROSE, accent1: MAROON, accent2: GOLD, accent3: BLUE,
            accent4: GREEN, accent5: MUTED, accent6: GOLD_L, hlink: BLUE, folHlink: MAROON_D },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.theme = { headFontFace: HEAD, bodyFontFace: BODY };
pres.title = "Hệ hỏi đáp lịch sử tiếng Việt";
pres.author = "Nhóm 10";

const W = 13.333, MX = 0.6;
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: WHITE },
  objects: [
    { text: { text: "Nhóm 10 · Hệ hỏi đáp lịch sử tiếng Việt", options: {
      x: MX, y: 7.05, w: 6, h: 0.3, fontFace: BODY, fontSize: 10, color: MUTED, margin: 0 } } },
    { placeholder: { options: { name: "kicker", type: "body", x: MX, y: 0.32, w: 12, h: 0.32, fontFace: BODY,
      fontSize: 12, bold: true, color: GOLD, charSpacing: 3, margin: 0 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: MX, y: 0.62, w: 12.1, h: 0.8, fontFace: HEAD,
      fontSize: 30, bold: true, color: INK, margin: 0, valign: "middle", align: "left" }, text: "" } },
  ],
  slideNumber: { x: 12.2, y: 7.02, w: 0.6, h: 0.3, fontFace: BODY, fontSize: 10, color: MUTED, align: "right" },
});
pres.defineSlideMaster({ title: "DARK", background: { color: INK } });

// ------------------------------------------------------------------ helpers
function content(kicker, title, notes) {
  const s = pres.addSlide({ masterName: "CONTENT" });
  s.addText(kicker.toUpperCase(), { placeholder: "kicker" });
  s.addText(title, { placeholder: "title" });
  if (notes) s.addNotes(notes);
  return s;
}
function card(s, x, y, w, h, fill = ROSE, line = null) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.1, fill: { color: fill },
    line: line ? { color: line, width: 1 } : { type: "none" } });
}
function txt(s, text, opt) {
  s.addText(text, { isTextBox: true, fontFace: BODY, fontSize: 14, color: INK, margin: 0, valign: "top", ...opt });
}
function badge(s, x, y, label, fill = MAROON, size = 0.5) {
  s.addShape(pres.shapes.OVAL, { x, y, w: size, h: size, fill: { color: fill }, line: { type: "none" } });
  s.addText(label, { isTextBox: true, x, y, w: size, h: size, fontFace: BODY, fontSize: size > 0.45 ? 14 : 11,
    bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
}
function stat(s, x, y, w, big, label, color = MAROON, fill = ROSE) {
  card(s, x, y, w, 1.45, fill);
  txt(s, big, { x: x + 0.25, y: y + 0.18, w: w - 0.5, h: 0.7, fontFace: HEAD, fontSize: 34, bold: true, color });
  txt(s, label, { x: x + 0.25, y: y + 0.9, w: w - 0.5, h: 0.45, fontSize: 13, color: MUTED });
}
// nhãn số kiểu Việt Nam (51,5): truyền giá trị x10 và định dạng 0","0 (trục giá trị phải ẩn)
const VN1 = { dataLabelFormatCode: '0","0' };
const x10 = (v) => Math.round(v * 10);
const chartBase = () => ({
  catAxisLabelColor: MUTED, valAxisLabelColor: MUTED, catAxisLabelFontFace: BODY, valAxisLabelFontFace: BODY,
  catAxisLabelFontSize: 12, valAxisLabelFontSize: 11, dataLabelFontFace: BODY, dataLabelFontSize: 11,
  dataLabelColor: INK, valGridLine: { color: "E9E4E5", size: 0.75 }, catGridLine: { style: "none" },
  legendFontFace: BODY, legendFontSize: 12, legendColor: INK, titleFontFace: BODY, titleFontSize: 13, titleColor: INK,
  catAxisLineShow: true, valAxisLineShow: false,
});

// ================================================================== 1. Bìa
{
  const s = pres.addSlide({ masterName: "CONTENT" });
  s.addImage({ path: path.join(FIG, "uit_logo.png"), x: MX, y: 0.45, w: 0.95, h: 0.95 * 257 / 337 });
  txt(s, [{ text: "ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH", options: { breakLine: true } },
          { text: "TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN" }],
      { x: 1.75, y: 0.5, w: 6, h: 0.65, fontSize: 13, bold: true, color: INK, valign: "middle" });
  txt(s, "BÁO CÁO CUỐI KỲ · MÔN HỌC MÁY TIÊN TIẾN", { x: MX, y: 1.95, w: 7.4, h: 0.35, fontSize: 13, bold: true,
      color: GOLD, charSpacing: 3 });
  txt(s, "Hệ hỏi đáp lịch sử tiếng Việt", { x: MX, y: 2.35, w: 7.4, h: 0.95, fontFace: HEAD, fontSize: 40,
      bold: true, color: INK, valign: "middle" });
  txt(s, "Truy hồi kết hợp BM25 + dense và mô hình sinh ViT5, biết từ chối khi tài liệu không có câu trả lời",
      { x: MX, y: 3.35, w: 7.2, h: 0.8, fontSize: 18, color: MAROON, italic: true });
  txt(s, [{ text: "Giảng viên hướng dẫn: ", options: { bold: true } }, { text: "TS. Hà Minh Tân", options: { breakLine: true } },
          { text: "Nhóm 10: ", options: { bold: true } },
          { text: "Nguyễn Duy Phong (240201021) · Hoàng Hải Đăng (250201048) · Trần Anh Hào (250201058)" }],
      { x: MX, y: 4.75, w: 7.6, h: 0.9, fontSize: 14, paraSpaceAfter: 6 });
  // minh hoạ: một lượt hỏi đáp thật của hệ thống
  card(s, 8.55, 1.55, 4.2, 4.75, ROSE);
  txt(s, "VÍ DỤ CHẠY THẬT", { x: 8.85, y: 1.8, w: 3.6, h: 0.3, fontSize: 11, bold: true, color: GOLD, charSpacing: 3 });
  card(s, 8.85, 2.2, 3.6, 0.95, WHITE);
  txt(s, "Ai là vị vua đầu tiên của nhà Trần?", { x: 9.05, y: 2.3, w: 3.25, h: 0.75, fontSize: 15, bold: true,
      valign: "middle" });
  s.addShape(pres.shapes.DOWN_ARROW, { x: 10.45, y: 3.25, w: 0.4, h: 0.4, fill: { color: GOLD }, line: { type: "none" } });
  card(s, 8.85, 3.75, 3.6, 0.75, MAROON);
  txt(s, "Trần Thái Tông", { x: 9.05, y: 3.75, w: 3.25, h: 0.75, fontFace: HEAD, fontSize: 20, bold: true,
      color: WHITE, valign: "middle" });
  txt(s, "Bằng chứng: bài \"Nhà Trần\", đoạn hạng 1 trong 5 đoạn tìm được · 0,13 giây trên GPU",
      { x: 8.85, y: 4.65, w: 3.6, h: 0.75, fontSize: 12, color: MUTED });
  txt(s, "Không có thông tin → trả lời \"không có câu trả lời\"", { x: 8.85, y: 5.45, w: 3.6, h: 0.6, fontSize: 12,
      color: MAROON, bold: true });
  s.addNotes("Giới thiệu đề tài: hệ hỏi đáp lịch sử tiếng Việt miền mở. Người dùng chỉ nhập câu hỏi; hệ thống tự tìm "
    + "đoạn văn trong kho Wikipedia lịch sử và sinh câu trả lời bằng ViT5, hoặc từ chối nếu kho không có thông tin.");
}

// ================================================================== 2. Bài toán
{
  const s = content("Phần 1 · Mở đầu", "Bài toán: trả lời đúng, hoặc biết từ chối",
    "Đầu vào là câu hỏi; tài liệu là kho 1.862 đoạn. Hai yêu cầu: tìm đúng đoạn và rút ra câu trả lời ngắn. "
    + "Điểm khó: khoảng một phần ba câu hỏi trong ViQuAD 2.0 là câu bẫy, nghe hợp lý nhưng đoạn văn không chứa đáp án.");
  const rows = [["Đầu vào", "Một câu hỏi lịch sử bằng tiếng Việt, không kèm tài liệu"],
                ["Tài liệu", "Kho 1.862 đoạn văn từ 38 bài Wikipedia lịch sử"],
                ["Đầu ra", "Câu trả lời ngắn + đoạn bằng chứng, hoặc \"không có câu trả lời\""]];
  rows.forEach(([h, d], i) => {
    const y = 1.75 + i * 1.2;
    badge(s, MX, y + 0.12, String(i + 1));
    txt(s, h, { x: MX + 0.7, y, w: 5, h: 0.4, fontSize: 17, bold: true });
    txt(s, d, { x: MX + 0.7, y: y + 0.42, w: 5.3, h: 0.6, fontSize: 14, color: MUTED });
  });
  card(s, MX, 5.5, 5.9, 1.2, CREAM);
  txt(s, [{ text: "Vì sao khó? ", options: { bold: true, color: GOLD } },
          { text: "32% câu hỏi là câu bẫy: gần giống đoạn văn nhưng đổi một chi tiết, nên phải biết từ chối thay vì bịa." }],
      { x: MX + 0.25, y: 5.62, w: 5.45, h: 1.0, fontSize: 14, valign: "middle" });
  // hai ví dụ
  const ex = [
    { tag: "CÂU TRẢ LỜI ĐƯỢC", fill: GREEN_L, col: GREEN, q: "Vị vua Pháp nào là chồng của Mary Stuart?",
      ctx: "\"...Mary Stuart, Nữ vương Scotland và là vợ của Vua nước Pháp, François II.\"", a: "François II" },
    { tag: "CÂU BẪY (KHÔNG TRẢ LỜI ĐƯỢC)", fill: ROSE, col: MAROON, q: "Quân Chiêm dẫn quân vào Thăng Long tháng mấy?",
      ctx: "\"...tháng 12 quân Chiêm dẫn quân về.\" (đoạn văn nói rút về, không nói tiến vào)", a: "không có câu trả lời" },
  ];
  ex.forEach((e, i) => {
    const y = 1.6 + i * 2.65;
    card(s, 7.05, y, 5.7, 2.45, e.fill);
    txt(s, e.tag, { x: 7.35, y: y + 0.2, w: 5.2, h: 0.3, fontSize: 11, bold: true, color: e.col, charSpacing: 2 });
    txt(s, e.q, { x: 7.35, y: y + 0.55, w: 5.2, h: 0.45, fontSize: 16, bold: true });
    txt(s, e.ctx, { x: 7.35, y: y + 1.02, w: 5.2, h: 0.7, fontSize: 13, italic: true, color: MUTED });
    txt(s, [{ text: "→ ", options: { color: e.col, bold: true } }, { text: e.a, options: { bold: true, color: e.col } }],
        { x: 7.35, y: y + 1.8, w: 5.2, h: 0.45, fontSize: 16 });
  });
}

// ================================================================== 3. Kiến trúc
{
  const s = content("Phần 1 · Mở đầu", "Kiến trúc Retriever – Reader",
    "Retriever chấm điểm toàn bộ kho bằng BM25 và bi-encoder rồi gộp thứ hạng bằng RRF. Reader ViT5 đọc từng đoạn "
    + "trong top-k, mỗi đoạn cho một đáp án kèm điểm; chọn đáp án điểm cao nhất trong các đáp án không phải từ chối.");
  const ar = png(path.join(FIG, "architecture.png")), aw = Math.min(11.0, 4.15 * ar.w / ar.h);
  s.addImage({ path: path.join(FIG, "architecture.png"), x: (W - aw) / 2, y: 1.6, w: aw, h: aw * ar.h / ar.w });
  const chips = [["Chấm toàn kho", "1.862 đoạn, không cần tìm gần đúng"],
                 ["Đọc từng đoạn", "≤ 512 token mỗi lần; ghép 5 đoạn sẽ quá dài"],
                 ["Từ chối có điều kiện", "chỉ khi mọi đoạn đều nói \"không có câu trả lời\""]];
  chips.forEach(([h, d], i) => {
    const x = MX + i * 4.1;
    card(s, x, 5.95, 3.9, 0.95, i === 2 ? ROSE : BLUE_L);
    txt(s, h, { x: x + 0.22, y: 6.03, w: 3.5, h: 0.35, fontSize: 15, bold: true, color: i === 2 ? MAROON : BLUE });
    txt(s, d, { x: x + 0.22, y: 6.4, w: 3.5, h: 0.45, fontSize: 12, color: MUTED });
  });
}

// ================================================================== 4. Câu hỏi nghiên cứu
{
  const s = content("Phần 1 · Mở đầu", "Bốn câu hỏi nghiên cứu, sáu thí nghiệm",
    "Mỗi câu hỏi nghiên cứu ứng với một hoặc hai thí nghiệm. Nguyên tắc xuyên suốt: mọi lựa chọn làm trên dev, "
    + "test chỉ chấm đúng một lần ở cuối giai đoạn 5.");
  const rq = [["RQ1", "Sinh hay trích xuất?", "ViT5 sinh đáp án so với XLM-R trích xuất trên cùng dữ liệu", "E1", MAROON],
              ["RQ2", "Lỗi do tìm hay do đọc?", "BM25, dense, hybrid × k ∈ {1, 3, 5}; đọc đoạn đúng so với tự tìm", "E2 · E3", BLUE],
              ["RQ3", "Mô hình có biết từ chối?", "Huấn luyện có so với không có câu không trả lời được", "E4", GOLD],
              ["RQ4", "Dữ liệu ngoài miền có giúp?", "Thêm 10.000 câu ViQuAD ngoài lịch sử; tách Việt Nam / thế giới", "E5 · E6", GREEN]];
  rq.forEach(([id, h, d, e, c], i) => {
    const x = MX + (i % 2) * 6.15, y = 1.65 + Math.floor(i / 2) * 2.25;
    card(s, x, y, 5.95, 2.0, [ROSE, BLUE_L, CREAM, GREEN_L][i]);
    badge(s, x + 0.3, y + 0.3, id, c, 0.75);
    txt(s, h, { x: x + 1.3, y: y + 0.3, w: 3.4, h: 0.45, fontSize: 18, bold: true });
    txt(s, d, { x: x + 1.3, y: y + 0.8, w: 4.4, h: 0.9, fontSize: 14, color: MUTED });
    txt(s, e, { x: x + 4.45, y: y + 0.32, w: 1.25, h: 0.4, fontSize: 13, bold: true, color: c, align: "right" });
  });
  txt(s, [{ text: "Nguyên tắc: ", options: { bold: true, color: MAROON } },
          { text: "chọn cấu hình trên dev · test chấm một lần · cùng thước đo và cùng định dạng dự đoán cho mọi mô hình" }],
      { x: MX, y: 6.3, w: 12.1, h: 0.45, fontSize: 14 });
}

// ================================================================== 5. Dữ liệu
{
  const s = content("Phần 2 · Dữ liệu", "UIT-ViQuAD 2.0: 38 bài lịch sử, chia theo bài",
    "Giữ 38 bài lịch sử (9 Việt Nam, 29 thế giới). Chia theo bài chứ không theo câu, vì câu hỏi cùng bài hỏi về cùng "
    + "sự kiện; chia theo câu sẽ rò rỉ nội dung test. Kho tri thức chứa đoạn của cả ba tập, chỉ giấu cặp hỏi–đáp của test.");
  [["38", "bài lịch sử (9 VN · 29 TG)"], ["1.862", "đoạn văn trong kho"], ["12.009", "câu hỏi có nhãn"],
   ["32,3%", "câu không trả lời được"]].forEach(([b, l], i) => stat(s, MX + i * 3.08, 1.6, 2.88, b, l,
     i === 3 ? MAROON : INK, i === 3 ? ROSE : "F4F1F1"));
  const head = ["Tập", "Bài", "Đoạn", "Trả lời được", "Không trả lời được", "Tổng câu", "VN / TG"]
    .map((t) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: INK }, align: "center" } }));
  const rows = [["train", "23", "1.491", "6.347", "3.047", "9.394", "2.610 / 6.784"],
                ["dev", "8", "179", "892", "437", "1.329", "407 / 922"],
                ["test", "7", "192", "887", "399", "1.286", "420 / 866"]]
    .map((r, i) => r.map((t, j) => ({ text: t, options: { align: j ? "center" : "left", bold: j === 0,
      fill: { color: i % 2 ? "FBF8F8" : WHITE } } })));
  s.addTable([head, ...rows], { x: MX, y: 3.35, w: 7.6, colW: [0.8, 0.65, 0.85, 1.3, 1.85, 0.95, 1.2],
    fontFace: BODY, fontSize: 13, color: INK, border: { type: "solid", pt: 0.75, color: LINE }, rowH: 0.42 });
  card(s, 8.5, 3.35, 4.25, 2.85, CREAM);
  txt(s, "VÌ SAO CHIA THEO BÀI?", { x: 8.75, y: 3.55, w: 3.8, h: 0.3, fontSize: 11, bold: true, color: GOLD, charSpacing: 2 });
  txt(s, "Câu hỏi trong cùng một bài hỏi về cùng sự kiện. Chia ngẫu nhiên theo câu thì mô hình \"thấy trước\" "
      + "nội dung test và điểm bị thổi phồng.", { x: 8.75, y: 3.95, w: 3.8, h: 1.5, fontSize: 14 });
  txt(s, "Test: Gandhi, Elizabeth I, Hồ Quý Ly, Nhà Trần, Louis XVI, Đế quốc La Mã Thần thánh",
      { x: 8.75, y: 5.15, w: 3.8, h: 0.9, fontSize: 12, color: MUTED, italic: true });
  txt(s, "Đầu vào ≤ 512 token (cắt 1,0% mẫu) · đáp án ≤ 64 token (cắt 0,7%) · đáp án trung vị khoảng 8 âm tiết",
      { x: MX, y: 5.55, w: 7.6, h: 0.5, fontSize: 13, color: MUTED });
}

// ================================================================== 6. Kiểm tra số liệu
{
  const s = content("Phần 2 · Dữ liệu", "Kiểm tra mọi con số \"đẹp bất thường\"",
    "Nhóm phát hiện và sửa nhiều lỗi kế thừa trước khi huấn luyện. Hai lỗi đáng chú ý nhất là ở công cụ chấm điểm "
    + "và ở quá trình đánh giá dev: nếu không sửa, kết quả sẽ sai mà nhìn vẫn hợp lý.");
  const errs = [["1.988", "câu \"trả lời được\" nhưng không có đáp án", "split test gốc của ViQuAD không có nhãn → bỏ câu, giữ đoạn"],
                ["3.883", "plausible_answer rỗng ở mọi dòng", "đọc nhầm tên trường → sửa, đủ 3.883/3.883"],
                ["152", "id câu hỏi trùng giữa hai split gốc", "đổi id thành dạng train:0013-0001-0001"],
                ["74", "câu lệch vị trí đáp án vài ký tự", "căn lại nếu lệch ≤ 20 ký tự, không đoán khi lệch xa"]];
  errs.forEach(([n, h, d], i) => {
    const y = 1.6 + i * 1.12;
    card(s, MX, y, 6.3, 1.0, i % 2 ? WHITE : "F8F5F5", LINE);
    txt(s, n, { x: MX + 0.2, y: y + 0.12, w: 1.25, h: 0.75, fontFace: HEAD, fontSize: 24, bold: true, color: MAROON,
        valign: "middle" });
    txt(s, h, { x: MX + 1.5, y: y + 0.13, w: 4.65, h: 0.38, fontSize: 14, bold: true });
    txt(s, d, { x: MX + 1.5, y: y + 0.52, w: 4.65, h: 0.4, fontSize: 12, color: MUTED });
  });
  const bugs = [["NoAns 62% của ViT5 zero-shot là ảo",
                 "Chuỗi rác toàn ký hiệu (*>+>) sau khi bỏ dấu câu thành rỗng và bị tính là \"từ chối đúng\". Sửa: chỉ chuỗi rỗng gốc hoặc đúng câu từ chối mới tính."],
                ["F1 dev lúc huấn luyện vô nghĩa (HasAns-F1 ≈ 1%)",
                 "group_by_length của transformers 4.57 xáo cả tập dev: 1.328/1.329 dự đoán bị so với đáp án câu khác. Sửa: đánh giá theo thứ tự gốc + kiểm tra nhãn trước khi tính điểm."]];
  bugs.forEach(([h, d], i) => {
    const y = 1.6 + i * 2.5;
    card(s, 7.2, y, 5.55, 2.3, ROSE);
    txt(s, "LỖI TINH VI " + (i + 1), { x: 7.45, y: y + 0.2, w: 5, h: 0.3, fontSize: 11, bold: true, color: MAROON, charSpacing: 2 });
    txt(s, h, { x: 7.45, y: y + 0.5, w: 5.1, h: 0.45, fontSize: 16, bold: true });
    txt(s, d, { x: 7.45, y: y + 1.0, w: 5.1, h: 1.2, fontSize: 13, color: INK });
  });
  txt(s, "Có unit test cho từng lỗi để không tái diễn (tests/, 31 test).", { x: MX, y: 6.2, w: 6.3, h: 0.4,
      fontSize: 13, italic: true, color: MUTED });
}

// ================================================================== 7. Retriever
{
  const s = content("Phần 3 · Phương pháp", "Retriever hybrid: BM25 + bi-encoder, gộp bằng RRF",
    "BM25 tách âm tiết mạnh với tên riêng và năm. Dense dùng bi-encoder tiếng Việt dựa trên PhoBERT, câu hỏi phải tách "
    + "từ trước. RRF gộp theo thứ hạng; quét trên dev chọn k = 5 và trọng số dense 0,7. Công thức mặc định k = 60, w = 1 "
    + "còn thua BM25 dùng một mình.");
  const rows = [["BM25", "Tách âm tiết, chấm toàn kho. Mạnh với tên riêng, năm.", BLUE],
                ["Dense", "vietnamese-bi-encoder (PhoBERT), câu hỏi tách từ bằng underthesea.", GOLD],
                ["RRF", "1/(5+hạng_BM25) + 0,7/(5+hạng_dense)", MAROON]];
  rows.forEach(([h, d, c], i) => {
    const y = 1.65 + i * 1.25;
    card(s, MX, y, 5.4, 1.1, i === 2 ? ROSE : "F8F5F5");
    badge(s, MX + 0.22, y + 0.3, h.slice(0, 1), c);
    txt(s, h, { x: MX + 0.95, y: y + 0.12, w: 4.2, h: 0.38, fontSize: 16, bold: true, color: c });
    txt(s, d, { x: MX + 0.95, y: y + 0.5, w: 4.3, h: 0.55, fontSize: 13, color: i === 2 ? INK : MUTED,
        fontFace: i === 2 ? MONO : BODY });
  });
  const rows2 = RET.overall.map((r) => [r["Cấu hình"].replace(/\*/g, ""), r]);
  const pick = (k) => rows2.find(([n]) => n.startsWith(k))[1];
  const bm = pick("BM25 · âm tiết"), de = pick("Dense · tách từ"), hy = rows2.find(([n]) => n.includes("k=5, w=0.7"))[1];
  const ks = ["1", "3", "5", "10", "20"];
  s.addChart(pres.charts.LINE, [
    { name: "BM25", labels: ks, values: ks.map((k) => 100 * bm["R@" + k]) },
    { name: "Dense", labels: ks, values: ks.map((k) => 100 * de["R@" + k]) },
    { name: "Hybrid (chọn)", labels: ks, values: ks.map((k) => 100 * hy["R@" + k]) },
  ], { x: 6.3, y: 1.55, w: 6.45, h: 4.0, ...chartBase(), chartColors: [BLUE, GOLD, MAROON], lineSize: 2.5,
       lineDataSymbolSize: 7, showLegend: true, legendPos: "b", valAxisMinVal: 40, valAxisMaxVal: 100,
       showTitle: true, title: "Recall@k trên dev (%)", catAxisTitle: "k", showCatAxisTitle: true,
       catAxisTitleColor: MUTED, catAxisTitleFontSize: 11 });
  const t5 = TEST["r2m_hybrid_k5_test_rs"].retrieval.gold_in_ctx;
  stat(s, MX, 5.4, 2.6, f(100 * hy["R@5"]) + "%", "R@5 trên dev", MAROON);
  stat(s, MX + 2.8, 5.4, 2.6, f(t5) + "%", "R@5 test (mục tiêu ≥ 80%)", GREEN, GREEN_L);
  txt(s, "R@1 của hybrid thấp hơn BM25 → Reader nên đọc 3–5 đoạn.", { x: 6.4, y: 5.85, w: 6.3, h: 0.6,
      fontSize: 13, italic: true, color: MUTED });
}

// ================================================================== 8. Reader
{
  const s = content("Phần 3 · Phương pháp", "Reader ViT5: sinh đáp án hoặc câu từ chối",
    "Mỗi mẫu là văn bản → văn bản. R1 chỉ dùng đoạn đúng. R2 thêm, với mỗi câu trả lời được, một đoạn sai do retriever "
    + "tìm ra và dạy mô hình nói 'không có câu trả lời'. Đây là chìa khoá để Reader bền khi đọc nhiều đoạn.");
  card(s, MX, 1.6, 6.0, 2.15, INK);
  txt(s, "ĐỊNH DẠNG MẪU", { x: MX + 0.3, y: 1.8, w: 5, h: 0.3, fontSize: 11, bold: true, color: GOLD_L, charSpacing: 2 });
  txt(s, [{ text: "vào: ", options: { color: GOLD_L } },
          { text: "<q> câu hỏi </q> <ctx> đoạn văn </ctx>", options: { color: WHITE, breakLine: true } },
          { text: "ra:  ", options: { color: GOLD_L } }, { text: "đáp án", options: { color: WHITE, breakLine: true } },
          { text: "     hoặc ", options: { color: GOLD_L } }, { text: "\"không có câu trả lời\"", options: { color: WHITE } }],
      { x: MX + 0.3, y: 2.2, w: 5.5, h: 1.4, fontFace: MONO, fontSize: 14, paraSpaceAfter: 4 });
  const cmp = [["R1 · chỉ đoạn đúng", "9.394 mẫu, 32,4% đích là từ chối", "F1 dev 51,1, ngang B1", ROSE_L, MUTED],
               ["R2 · thêm đoạn nhiễu", "15.741 mẫu, 58,5% đích là từ chối", "F1 dev 57,5, mô hình chính", ROSE, MAROON]];
  cmp.forEach(([h, a, b, fill, c], i) => {
    const x = MX + i * 3.08;
    card(s, x, 4.0, 2.92, 2.55, fill);
    txt(s, h, { x: x + 0.22, y: 4.18, w: 2.55, h: 0.7, fontSize: 15, bold: true, color: c });
    txt(s, a, { x: x + 0.22, y: 4.9, w: 2.55, h: 0.7, fontSize: 13 });
    txt(s, b, { x: x + 0.22, y: 5.65, w: 2.55, h: 0.7, fontSize: 13, bold: true, color: c });
  });
  const cfg = [["Mô hình", "VietAI/vit5-base"], ["Learning rate", "1e-4 (AdamW); 3e-4 kém hơn"],
               ["Batch hiệu dụng", "32 (8 × tích luỹ 4)"], ["Số epoch", "8 (chọn theo F1 dev)"],
               ["Độ dài vào / ra", "512 / 64 token"], ["Phần cứng", "Colab T4 · RTX 3060 12 GB, bf16"],
               ["Chọn đáp án", "log-prob TB cao nhất, bỏ qua câu từ chối"]];
  card(s, 7.0, 1.6, 5.75, 4.95, "F8F5F5");
  txt(s, "CẤU HÌNH HUẤN LUYỆN", { x: 7.25, y: 1.8, w: 5, h: 0.3, fontSize: 11, bold: true, color: GOLD, charSpacing: 2 });
  cfg.forEach(([k, v], i) => {
    const y = 2.25 + i * 0.6;
    txt(s, k, { x: 7.25, y, w: 1.9, h: 0.5, fontSize: 13, color: MUTED, valign: "middle" });
    txt(s, v, { x: 9.15, y, w: 3.45, h: 0.5, fontSize: 14, bold: true, valign: "middle" });
  });
}

// ================================================================== 9. Thước đo & baseline
{
  const s = content("Phần 3 · Phương pháp", "Thước đo và các mốc so sánh",
    "EM khắt khe; F1 theo âm tiết là thước đo chính. Chuẩn hoá NFC, chữ thường, thống nhất vị trí dấu thanh, bỏ dấu câu "
    + "nhưng giữ dấu thanh. Câu không trả lời được chấm kiểu SQuAD 2.0. Ba baseline: B0 sàn, B1 đối thủ chính, B2 ViT5 chưa fine-tune.");
  const m = [["EM", "khớp hoàn toàn sau chuẩn hoá"], ["F1", "trùng một phần theo âm tiết · thước đo chính"],
             ["HasAns-F1", "F1 trên câu trả lời được"], ["NoAns-acc", "tỉ lệ từ chối đúng câu bẫy"]];
  m.forEach(([k, v], i) => {
    const y = 1.65 + i * 0.78;
    txt(s, k, { x: MX, y, w: 1.75, h: 0.6, fontFace: HEAD, fontSize: 18, bold: true, color: MAROON, valign: "middle" });
    txt(s, v, { x: MX + 1.8, y, w: 4.1, h: 0.6, fontSize: 14, valign: "middle" });
  });
  card(s, MX, 4.9, 5.9, 1.75, CREAM);
  txt(s, "CHUẨN HOÁ TIẾNG VIỆT", { x: MX + 0.25, y: 5.05, w: 5, h: 0.3, fontSize: 11, bold: true, color: GOLD, charSpacing: 2 });
  txt(s, [{ text: "\"hòa\" = \"hoà\"", options: { bold: true } }, { text: " (kho dùng lẫn: 605 và 953 lần)", options: { breakLine: true } },
          { text: "\"Hà\" ≠ \"Ha\"", options: { bold: true } }, { text: " (giữ dấu thanh)", options: { breakLine: true } },
          { text: "\"năm 1954\" so với \"1954\"", options: { bold: true } }, { text: ": EM = 0, F1 = 0,67" }],
      { x: MX + 0.25, y: 5.4, w: 5.5, h: 1.15, fontSize: 14, paraSpaceAfter: 3 });
  const b = [["B0", "Ngẫu nhiên: cụm danh từ / năm trong đoạn", BASE.b0_gold_dev.overall.F1, "mốc sàn"],
             ["B1", "XLM-RoBERTa trích xuất (SQuAD 2.0)", BASE.b1_gold_dev.overall.F1, "đối thủ chính"],
             ["B2", "ViT5 chưa fine-tune (zero-shot)", BASE.b2_gold_dev.overall.F1, "chỉ sinh ký hiệu rác"]];
  b.forEach(([id, d, v, note], i) => {
    const y = 1.65 + i * 1.65;
    card(s, 7.0, y, 5.75, 1.45, i === 1 ? ROSE : "F8F5F5");
    badge(s, 7.25, y + 0.42, id, i === 1 ? MAROON : MUTED, 0.6);
    txt(s, d, { x: 8.05, y: y + 0.2, w: 3.0, h: 0.75, fontSize: 14, bold: true });
    txt(s, note, { x: 8.05, y: y + 0.95, w: 3.0, h: 0.35, fontSize: 12, color: MUTED });
    txt(s, f(v), { x: 11.0, y: y + 0.2, w: 1.55, h: 0.7, fontFace: HEAD, fontSize: 28, bold: true,
        color: i === 1 ? MAROON : MUTED, align: "right" });
    txt(s, "F1 dev", { x: 11.0, y: y + 0.92, w: 1.55, h: 0.35, fontSize: 11, color: MUTED, align: "right" });
  });
}

// ================================================================== 10. E1
{
  const s = content("Phần 4 · Kết quả", "E1: ViT5 vượt mô hình trích xuất nhờ biết từ chối",
    "Khi được cho sẵn đoạn đúng, R2 hơn B1 6 điểm F1 trên dev. Gần như toàn bộ lợi thế nằm ở khả năng từ chối: NoAns 54% "
    + "so với 31%. Với câu trả lời được, B1 vẫn nhỉnh hơn. Fine-tune là thiết yếu: ViT5 zero-shot chỉ đạt F1 0,4.");
  const sys = [["B0 ngẫu nhiên", BASE.b0_gold_dev.overall], ["B2 ViT5 zero-shot", BASE.b2_gold_dev.overall],
               ["B1 XLM-R", BASE.b1_gold_dev.overall], ["R1 ViT5", o(DEV, "r1_gold_dev")],
               ["E4: R2 bỏ câu bẫy", o(DEV, "r2noimp_gold_dev_rs")], ["R2 ViT5 (chính)", o(DEV, "r2m_gold_dev_rs")],
               ["E5: R2 + ngoài miền", o(DEV, "r2ood_gold_dev_rs")]];
  s.addChart(pres.charts.BAR, [{ name: "F1 dev", labels: sys.map((x) => x[0]), values: sys.map((x) => x10(x[1].F1)) }],
    { x: MX, y: 1.5, w: 7.0, h: 5.2, barDir: "bar", ...chartBase(), chartColors: [MUTED, MUTED, BLUE, MUTED, MUTED, MAROON, MAROON],
      showValue: true, dataLabelPosition: "outEnd", ...VN1, showLegend: false, valAxisMaxVal: 700,
      valAxisMinVal: 0, catAxisOrientation: "maxMin", barGapWidthPct: 45, showTitle: true,
      title: "F1 trên dev khi đọc đoạn văn đúng", valAxisHidden: true, valGridLine: { style: "none" } });
  const b1 = BASE.b1_gold_dev.overall, r2 = o(DEV, "r2m_gold_dev_rs");
  const cmp = [["F1", b1.F1, r2.F1, true], ["NoAns-acc", b1.NoAns_acc, r2.NoAns_acc, true], ["HasAns-F1", b1.HasAns_F1, r2.HasAns_F1, false]];
  card(s, 8.0, 1.6, 4.75, 3.65, ROSE);
  txt(s, "B1 XLM-R  →  R2 ViT5", { x: 8.25, y: 1.78, w: 4.3, h: 0.4, fontSize: 15, bold: true, color: MAROON });
  cmp.forEach(([k, a, b, win], i) => {
    const y = 2.35 + i * 0.95;
    txt(s, k, { x: 8.25, y, w: 1.55, h: 0.6, fontSize: 14, color: MUTED, valign: "middle" });
    txt(s, f(a), { x: 9.8, y, w: 1.0, h: 0.6, fontSize: 20, color: MUTED, align: "right", valign: "middle" });
    txt(s, "→", { x: 10.85, y, w: 0.4, h: 0.6, fontSize: 18, color: MUTED, align: "center", valign: "middle" });
    txt(s, f(b), { x: 11.3, y, w: 1.25, h: 0.6, fontFace: HEAD, fontSize: 24, bold: true,
        color: win ? MAROON : MUTED, valign: "middle" });
  });
  txt(s, "Đoạn nhiễu khi huấn luyện là điều kiện để ViT5 vượt B1: R1 (không có đoạn nhiễu) chỉ ngang B1.",
      { x: 8.0, y: 5.45, w: 4.75, h: 1.1, fontSize: 14, italic: true, color: INK });
}

// ================================================================== 11. E2/E3
{
  const s = content("Phần 4 · Kết quả", "E2 – E3: khi tìm đúng đoạn, Reader đọc gần như hoàn hảo",
    "BM25 và hybrid ngang nhau, cả hai hơn hẳn dense. Đọc 3–5 đoạn tốt hơn 1 đoạn. Khi retriever tìm đúng, HasAns-F1 gần "
    + "bằng lúc cho sẵn đoạn đúng; khi tìm sai gần như bằng 0. Từ cho sẵn sang tự tìm mất khoảng 7 điểm F1.");
  const ks = ["1", "3", "5"];
  s.addChart(pres.charts.LINE, ["bm25", "dense", "hybrid"].map((m, i) => ({
    name: ["BM25", "Dense", "Hybrid"][i], labels: ks.map((k) => "k = " + k),
    values: ks.map((k) => +o(TEST, `r2m_${m}_k${k}_test_rs`).F1.toFixed(1)) })),
    { x: MX, y: 1.5, w: 6.6, h: 4.5, ...chartBase(), chartColors: [BLUE, GOLD, MAROON], lineSize: 2.5,
      lineDataSymbolSize: 8, showLegend: true, legendPos: "b", valAxisMinVal: 40, valAxisMaxVal: 55,
      showTitle: true, title: "F1 toàn hệ thống trên test theo số đoạn k (Reader R2)" });
  const r = TEST["r2ood_hybrid_k5_test_rs"].retrieval, gold = o(TEST, "r2ood_gold_test_rs"), best = o(TEST, "r2ood_hybrid_k5_test_rs");
  stat(s, 7.5, 1.6, 2.55, f(r.HasAns_F1_hit), "HasAns-F1 khi tìm đúng", GREEN, GREEN_L);
  stat(s, 10.2, 1.6, 2.55, f(r.HasAns_F1_miss), "HasAns-F1 khi tìm sai", MAROON);
  stat(s, 7.5, 3.25, 2.55, f(r.gold_in_ctx) + "%", "câu có đoạn đúng trong top-5", INK, "F4F1F1");
  stat(s, 10.2, 3.25, 2.55, "−" + f(gold.F1 - best.F1), "F1 khi chuyển từ đoạn đúng sang tự tìm", INK, "F4F1F1");
  card(s, 7.5, 4.9, 5.25, 1.1, CREAM);
  txt(s, [{ text: "Kết luận RQ2: ", options: { bold: true, color: GOLD } },
          { text: "sai số chủ yếu nằm ở khâu đọc, không phải khâu tìm." }],
      { x: 7.75, y: 4.98, w: 4.85, h: 0.95, fontSize: 15, valign: "middle" });
  txt(s, `Mô hình sinh gần như không bịa: ${f(TEST["r2ood_hybrid_k5_test_rs"].pred_in_ctx)}% đáp án có nguyên văn trong đoạn đã đọc.`,
      { x: MX, y: 6.2, w: 12.1, h: 0.45, fontSize: 13, italic: true, color: MUTED });
}

// ================================================================== 12. E4, E5, ngưỡng
{
  const s = content("Phần 4 · Kết quả", "E4 – E5: câu bẫy là thiết yếu, dữ liệu ngoài miền có ích",
    "Số liệu là hiệu cặp trên test với khoảng tin cậy 95% bootstrap 2.000 lần. E4: bỏ câu không trả lời được thì mô hình "
    + "gần như mất khả năng từ chối. E5: thêm 10.000 câu ViQuAD ngoài lịch sử tăng F1 có ý nghĩa thống kê. Ngưỡng từ chối "
    + "chỉ là núm đánh đổi giữa thận trọng và mạnh dạn.");
  const cards = [
    ["E4 · RQ3", "Bỏ câu không trả lời được khi huấn luyện", "−22,8", "NoAns-acc", "CI 95% [−27,6; −17,9] · F1 −5,3 [−7,7; −2,8] (đoạn đúng, bản có ngưỡng)", MAROON, ROSE],
    ["E5 · RQ4", "Thêm 10.000 câu ViQuAD ngoài miền", "+2,9", "F1 (đọc đoạn đúng)", "CI 95% [+0,7; +5,2] · EM +4,1 [+1,6; +6,5] (đoạn đúng, greedy)", GREEN, GREEN_L],
    ["Ngưỡng từ chối", "Chọn δ trên dev, áp cho test", "−0,5", "F1 tổng", "CI [−1,3; +0,2]: NoAns +2,0 nhưng HasAns-F1 −1,6", GOLD, CREAM],
  ];
  cards.forEach(([tag, h, big, lab, ci, c, fill], i) => {
    const x = MX + i * 4.1;
    card(s, x, 1.65, 3.9, 4.0, fill);
    txt(s, tag.toUpperCase(), { x: x + 0.28, y: 1.85, w: 3.4, h: 0.3, fontSize: 11, bold: true, color: c, charSpacing: 2 });
    txt(s, h, { x: x + 0.28, y: 2.2, w: 3.4, h: 0.8, fontSize: 16, bold: true });
    txt(s, big, { x: x + 0.28, y: 3.05, w: 3.4, h: 1.0, fontFace: HEAD, fontSize: 48, bold: true, color: c });
    txt(s, lab, { x: x + 0.28, y: 4.05, w: 3.4, h: 0.4, fontSize: 14, bold: true, color: c });
    txt(s, ci, { x: x + 0.28, y: 4.55, w: 3.4, h: 0.9, fontSize: 13, color: MUTED });
  });
  txt(s, [{ text: "Độ ổn định: ", options: { bold: true } },
          { text: "huấn luyện lại 3 seed, F1 test (đoạn đúng) 57,3 ± 0,5; chênh lệch dưới ~1 điểm F1 là nhiễu." }],
      { x: MX, y: 5.95, w: 12.1, h: 0.5, fontSize: 14 });
}

// ================================================================== 13. Kết quả cuối
{
  const s = content("Phần 4 · Kết quả", "Hệ thống cuối trên test: F1 53,4",
    "Hệ thống cuối: Reader E5 cộng hybrid top-5, k chọn trên dev. Đạt mục tiêu retriever và khả năng từ chối; chưa đạt "
    + "F1 toàn hệ thống 55 và HasAns-F1 70. Nhóm giữ nguyên con số, không chấm lại test.");
  const best = o(TEST, "r2ood_hybrid_k5_test_rs"), gold = o(TEST, "r2ood_gold_test_rs");
  [["EM", best.EM], ["F1", best.F1], ["HasAns-F1", best.HasAns_F1], ["NoAns-acc", best.NoAns_acc]]
    .forEach(([k, v], i) => stat(s, MX + i * 3.08, 1.6, 2.88, f(v), k + " · hybrid top-5 · test", i === 1 ? MAROON : INK,
      i === 1 ? ROSE : "F4F1F1"));
  const rec5 = TEST["r2m_hybrid_k5_test_rs"].retrieval.gold_in_ctx;
  const hasf1 = Math.max(o(TEST, "r2m_gold_test_rs").HasAns_F1, gold.HasAns_F1);
  const rows = [["Retriever Recall@5", "≥ 80", f(rec5), rec5 >= 80],
                ["Reader đọc đoạn đúng, HasAns-F1", "≥ 70", f(hasf1), hasf1 >= 70],
                ["Toàn hệ thống, F1", "≥ 55", f(best.F1), best.F1 >= 55],
                ["NoAns-acc (Reader E5, đoạn đúng)", "≥ 60", f(gold.NoAns_acc), gold.NoAns_acc >= 60],
                ["ViT5 fine-tune so với zero-shot (F1 dev)", "cải thiện rõ", f(BASE.b2_gold_dev.overall.F1) + " → " + f(o(DEV, "r2m_gold_dev_rs").F1), true]];
  const head = ["Chỉ số", "Mục tiêu", "Đạt được", ""].map((t) => ({ text: t, options: { bold: true, color: WHITE,
    fill: { color: INK }, align: t === "Chỉ số" ? "left" : "center" } }));
  s.addTable([head, ...rows.map(([a, b, c, ok], i) => [
    { text: a, options: { fill: { color: i % 2 ? "FBF8F8" : WHITE } } },
    { text: b, options: { align: "center", fill: { color: i % 2 ? "FBF8F8" : WHITE } } },
    { text: c, options: { align: "center", bold: true, fill: { color: i % 2 ? "FBF8F8" : WHITE } } },
    { text: ok ? "Đạt" : "Chưa đạt", options: { align: "center", bold: true, color: ok ? GREEN : MAROON,
      fill: { color: ok ? GREEN_L : ROSE } } }])],
    { x: MX, y: 3.35, w: 8.0, colW: [3.9, 1.35, 1.6, 1.15], fontFace: BODY, fontSize: 14, color: INK,
      border: { type: "solid", pt: 0.75, color: LINE }, rowH: 0.5 });
  card(s, 8.95, 3.35, 3.8, 3.0, CREAM);
  txt(s, "VÌ SAO CHƯA ĐẠT 55?", { x: 9.2, y: 3.55, w: 3.4, h: 0.3, fontSize: 11, bold: true, color: GOLD, charSpacing: 2 });
  txt(s, "Mục tiêu là ước lượng ban đầu. Phân tích lỗi (phần 5) cho thấy câu bẫy và cách chọn đoạn là hai chỗ kéo điểm "
      + "xuống; một cải tiến thử trên dev được +1,1 F1 (phần 6).", { x: 9.2, y: 3.95, w: 3.35, h: 2.3, fontSize: 14 });
}

// ================================================================== 14. E6
{
  const s = content("Phần 4 · Kết quả", "E6: theo miền và theo loại câu hỏi",
    "Lịch sử Việt Nam dễ hơn thế giới một chút ở mọi cấu hình; dữ liệu ngoài miền giúp cả hai. Câu ở đâu, khi nào, ai "
    + "dễ nhất vì đáp án ngắn là thực thể; câu vì sao và như thế nào khó nhất vì đáp án dài, khó xác định ranh giới.");
  const cfg = [["R2 · đoạn đúng", "r2m_gold_test_rs"], ["R2+OOD · đoạn đúng", "r2ood_gold_test_rs"],
               ["R2+OOD · top-5", "r2ood_hybrid_k5_test_rs"]];
  s.addChart(pres.charts.BAR, [
    { name: "Lịch sử Việt Nam", labels: cfg.map((c) => c[0]), values: cfg.map((c) => x10(TEST[c[1]].by_domain.VN.F1)) },
    { name: "Lịch sử thế giới", labels: cfg.map((c) => c[0]), values: cfg.map((c) => x10(TEST[c[1]].by_domain.TG.F1)) },
  ], { x: MX, y: 1.5, w: 6.0, h: 5.1, barDir: "col", barGrouping: "clustered", ...chartBase(), chartColors: [MAROON, GOLD],
       showValue: true, dataLabelPosition: "outEnd", ...VN1, showLegend: true, legendPos: "b",
       valAxisMinVal: 0, valAxisMaxVal: 700, valAxisHidden: true, valGridLine: { style: "none" }, barGapWidthPct: 60, showTitle: true, title: "F1 trên test theo miền" });
  const qt = Object.entries(TEST["r2ood_hybrid_k5_test_rs"].by_qtype).filter(([k]) => k !== "khác")
    .sort((a, b) => b[1].F1 - a[1].F1);
  s.addChart(pres.charts.BAR, [{ name: "F1", labels: qt.map(([k, v]) => `${k} (n=${v.n})`), values: qt.map(([, v]) => x10(v.F1)) }],
    { x: 6.9, y: 1.5, w: 5.85, h: 5.1, barDir: "bar", ...chartBase(), chartColors: [BLUE], showValue: true,
      dataLabelPosition: "outEnd", ...VN1, showLegend: false, valAxisMinVal: 0, valAxisMaxVal: 700,
      catAxisOrientation: "maxMin", barGapWidthPct: 45, valAxisHidden: true, valGridLine: { style: "none" },
      showTitle: true, title: "F1 theo loại câu hỏi (hệ thống cuối, test)" });
}

// ================================================================== 15. Phân tích lỗi
{
  const s = content("Phần 5 · Phân tích lỗi", "100 câu sai: lỗi nằm ở khâu đọc",
    "Lấy ngẫu nhiên 100 trong 779 câu sai của hệ thống cuối trên test, đọc từng câu và gán một nhãn. Khâu đọc chiếm 52%, "
    + "khâu tìm và chọn đoạn 19%. Khoảng 27% thật ra chấp nhận được. Hệ thống gần như không bịa.");
  const names = { trap: "Trả lời câu bẫy", paraphrase: "Đúng, khác cách viết", reader_span: "Đọc sai span",
    retrieval: "Tìm sai đoạn", reader_refuse: "Từ chối nhầm", selection: "Chọn nhầm đoạn",
    gold_issue: "Đáp án chuẩn có vấn đề", tokenizer: "Lỗi bộ từ vựng ViT5", hallucination: "Bịa" };
  const cnt = {}; ERR.forEach((l) => { cnt[l] = (cnt[l] || 0) + 1; });
  const order = Object.keys(names).sort((a, b) => (cnt[b] || 0) - (cnt[a] || 0));
  const colorOf = (k) => (["trap", "reader_span", "reader_refuse"].includes(k) ? MAROON
    : ["retrieval", "selection"].includes(k) ? BLUE : ["paraphrase", "gold_issue"].includes(k) ? GREEN : MUTED);
  s.addChart(pres.charts.BAR, [{ name: "Số câu", labels: order.map((k) => names[k]), values: order.map((k) => cnt[k] || 0) }],
    { x: MX, y: 1.5, w: 7.0, h: 5.2, barDir: "bar", ...chartBase(), chartColors: order.map(colorOf), showValue: true,
      dataLabelPosition: "outEnd", showLegend: false, valAxisMinVal: 0, valAxisMaxVal: 32, catAxisOrientation: "maxMin",
      barGapWidthPct: 40, valAxisHidden: true, valGridLine: { style: "none" }, showTitle: true,
      title: "Số câu trong 100 câu sai (màu theo nhóm bên phải)" });
  const ins = [["52%", "lỗi ở khâu đọc", "câu bẫy 28 + span 13 + từ chối nhầm 11", MAROON, ROSE],
               ["19%", "lỗi ở khâu tìm", "tìm sai 12 + chọn nhầm đoạn 7", BLUE, BLUE_L],
               ["27%", "thật ra chấp nhận được", "khác cách viết 20 + đáp án chuẩn có vấn đề 7", GREEN, GREEN_L],
               ["0", "câu bịa trong mẫu", "12/14 câu \"không có trong đoạn\" là do bộ từ vựng", INK, "F4F1F1"]];
  ins.forEach(([b, h, d, c, fill], i) => {
    const y = 1.55 + i * 1.3;
    card(s, 7.95, y, 4.8, 1.15, fill);
    txt(s, b, { x: 8.15, y: y + 0.1, w: 1.35, h: 0.95, fontFace: HEAD, fontSize: 30, bold: true, color: c, valign: "middle" });
    txt(s, h, { x: 9.55, y: y + 0.14, w: 3.1, h: 0.4, fontSize: 15, bold: true, color: c });
    txt(s, d, { x: 9.55, y: y + 0.55, w: 3.1, h: 0.55, fontSize: 12, color: MUTED });
  });
}

// ================================================================== 16. Ví dụ lỗi
{
  const s = content("Phần 5 · Phân tích lỗi", "Ba kiểu lỗi điển hình",
    "Câu bẫy chỉ đổi một chi tiết, Reader vẫn trích đáp án mồi. Lỗi bộ từ vựng: ViT5 không có các ký tự như ç, ā nên làm "
    + "rơi chúng; demo khôi phục bằng cách tìm chuỗi gốc trong đoạn. Chọn nhầm đoạn: điểm tin cậy giữa các đoạn khác "
    + "nhau không so sánh trực tiếp được.");
  const ex = [
    ["CÂU BẪY · 28%", "Bao nhiêu người dân muốn hành quyết Louis?", "Đoạn văn: \"...361 đại biểu đòi hành quyết Louis ngay lập tức\"",
     "361", "Đúng: không có câu trả lời (đoạn nói đại biểu, không phải người dân)", MAROON, ROSE],
    ["BỘ TỪ VỰNG · 2%", "Hàng triệu dân Ấn Độ tôn kính gọi ông là gì?", "Đoạn văn: \"...gọi một cách tôn kính là Mahātmā\"",
     "Mahtm", "ViT5 làm rơi ký tự ā; 1,0% đáp án test không qua được tokenizer", GOLD, CREAM],
    ["CHỌN NHẦM ĐOẠN · 7%", "Nguyên nhân khiến đế quốc suy thoái sau này là gì?", "Đoạn đúng ở hạng 1, nhưng đáp án lấy từ đoạn về nhà Đông Hán",
     "tranh chấp chính quyền...", "Đúng: \"ngai vàng và đế quốc đã được Thượng đế định đoạt\"", BLUE, BLUE_L],
  ];
  ex.forEach(([tag, q, c, pred, note, col, fill], i) => {
    const x = MX + i * 4.1;
    card(s, x, 1.6, 3.9, 4.55, fill);
    txt(s, tag, { x: x + 0.25, y: 1.8, w: 3.4, h: 0.3, fontSize: 11, bold: true, color: col, charSpacing: 2 });
    txt(s, q, { x: x + 0.25, y: 2.2, w: 3.4, h: 0.95, fontSize: 16, bold: true });
    txt(s, c, { x: x + 0.25, y: 3.2, w: 3.4, h: 1.0, fontSize: 13, italic: true, color: MUTED });
    card(s, x + 0.25, 4.3, 3.4, 0.7, WHITE);
    txt(s, [{ text: "Dự đoán: ", options: { color: MUTED } }, { text: pred, options: { bold: true, color: col } }],
        { x: x + 0.45, y: 4.3, w: 3.1, h: 0.7, fontSize: 15, valign: "middle" });
    txt(s, note, { x: x + 0.25, y: 5.15, w: 3.4, h: 1.3, fontSize: 13 });
  });
}

// ================================================================== 17. Demo
{
  const s = content("Phần 6 · Demo", "Demo Gradio và độ trễ",
    "Demo chạy bằng python app.py. Hiển thị đáp án, đoạn bằng chứng tô đậm, top-k nguồn kèm đáp án đọc được ở từng đoạn, "
    + "và thời gian từng khâu. Reader chiếm 80–95% thời gian; truy hồi rẻ vì kho nhỏ.");
  // chỉ lấy phần trên ảnh chụp (câu hỏi, đáp án, đoạn bằng chứng, độ trễ): khung 7.2 x 5.1 inch
  const dm = png(path.join(FIG, "demo_gradio.png"));
  s.addImage({ path: path.join(FIG, "demo_gradio.png"), x: MX, y: 1.55, w: 7.2, h: 7.2 * dm.h / dm.w,
    sizing: { type: "crop", x: 0, y: 0, w: 7.2, h: 5.1 } });
  s.addShape(pres.shapes.RECTANGLE, { x: MX, y: 1.55, w: 7.2, h: 5.1, fill: { type: "none" }, line: { color: LINE, width: 1 } });
  const gpu = LAT.cuda.results.k5, cpu = LAT.cpu.results.k5;
  stat(s, 8.1, 1.6, 2.2, Math.round(gpu.total.p50) + " ms", "mỗi câu · GPU · top-5", MAROON);
  stat(s, 10.55, 1.6, 2.2, f(cpu.total.p50 / 1000) + " s", "mỗi câu · CPU · top-5", INK, "F4F1F1");
  const rows = [["Khâu (ms)", "GPU", "CPU"], ["BM25", gpu.bm25.p50, cpu.bm25.p50], ["Dense", gpu.dense.p50, cpu.dense.p50],
                ["Reader (5 đoạn)", gpu.read.p50, cpu.read.p50]];
  s.addTable(rows.map((r, i) => r.map((c, j) => ({ text: typeof c === "number" ? String(Math.round(c)) : c,
    options: { bold: i === 0 || j === 0, color: i === 0 ? WHITE : INK, fill: { color: i === 0 ? INK : (i % 2 ? WHITE : "FBF8F8") },
      align: j ? "center" : "left" } }))), { x: 8.1, y: 3.3, w: 4.65, colW: [2.25, 1.2, 1.2], fontFace: BODY, fontSize: 14,
    border: { type: "solid", pt: 0.75, color: LINE }, rowH: 0.45 });
  txt(s, "Bảng: trung vị đo riêng trên 100 câu dev. Số trên ảnh (365 ms) gồm cả thời gian của giao diện. "
      + "Đáp án \"François II\" được khôi phục từ đoạn văn; đầu ra thô của ViT5 là \"Franois II\".",
      { x: 8.1, y: 5.3, w: 4.65, h: 1.4, fontSize: 13, italic: true, color: MUTED });
}

// ================================================================== 18. Kết luận
{
  const s = content("Phần 7 · Kết luận", "Kết luận, hạn chế và hướng phát triển",
    "Trả lời bốn câu hỏi nghiên cứu, nêu thẳng hạn chế, và hướng phát triển. Hướng đầu tiên đã thử trên dev được +1,1 F1 "
    + "nhưng chưa chấm test để giữ nguyên tắc chỉ dùng test một lần.");
  const cols = [
    ["ĐẠT ĐƯỢC", GREEN, GREEN_L, ["RQ1: ViT5 vượt XLM-R (F1 dev 57,5 so với 51,5) nhờ từ chối tốt",
      "RQ2: hybrid R@5 90,2% test; sai số chủ yếu ở khâu đọc", "RQ3: câu bẫy khi huấn luyện là thiết yếu (NoAns −22,8 nếu bỏ)",
      "RQ4: dữ liệu ngoài miền +2,9 F1 có ý nghĩa", "Hầu như không bịa; 0,13 s/câu trên GPU"]],
    ["HẠN CHẾ", GOLD, CREAM, ["F1 toàn hệ thống 53,4 < 55; HasAns-F1 ≈ 60 < 70", "Test nhỏ: 7 bài, 1.286 câu (CI ≈ ± 2,5 F1)",
      "Nhãn \"lịch sử\" kế thừa: vài bài chỉ liên quan một phần", "Phân tích lỗi do một người chấm", "ViT5-base, đọc từng đoạn độc lập, ≤ 512 token"]],
    ["HƯỚNG PHÁT TRIỂN", MAROON, ROSE, ["Chọn đáp án có xét hạng retriever: +1,1 F1 trên dev",
      "Sinh thêm câu bẫy / thêm bước kiểm chứng", "Fusion-in-Decoder hoặc ViT5-large", "Đánh giá bằng người cho câu khác cách viết",
      "Mở rộng kho ra toàn bộ Wikipedia lịch sử"]],
  ];
  cols.forEach(([h, c, fill, items], i) => {
    const x = MX + i * 4.1;
    card(s, x, 1.6, 3.9, 4.4, fill);
    txt(s, h, { x: x + 0.28, y: 1.82, w: 3.4, h: 0.35, fontSize: 14, bold: true, color: c, charSpacing: 2 });
    txt(s, items.map((t, j) => ({ text: t, options: { bullet: { indent: 15 }, breakLine: j < items.length - 1 } })),
        { x: x + 0.28, y: 2.3, w: 3.42, h: 3.55, fontSize: 15, paraSpaceAfter: 9 });
  });
}

// ================================================================== 19. Cảm ơn
{
  const s = pres.addSlide({ masterName: "DARK" });
  txt(s, "CẢM ƠN THẦY VÀ CÁC BẠN ĐÃ LẮNG NGHE", { x: 0.8, y: 2.3, w: 11.7, h: 0.9, fontFace: HEAD, fontSize: 34,
      bold: true, color: WHITE, align: "center", valign: "middle" });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 5.42, y: 3.5, w: 2.5, h: 0.7, rectRadius: 0.35, fill: { color: GOLD },
    line: { type: "none" } });
  txt(s, "HỎI & ĐÁP", { x: 5.42, y: 3.5, w: 2.5, h: 0.7, fontSize: 18, bold: true, color: INK, align: "center",
      valign: "middle", charSpacing: 4 });
  txt(s, [{ text: "Mã nguồn, dữ liệu và toàn bộ kết quả: ", options: { color: "C9B4B9" } },
          { text: "github.com/trananhhao-0603/hoc_may_tien_tien",
            options: { color: GOLD_L, bold: true, hyperlink: { url: "https://github.com/trananhhao-0603/hoc_may_tien_tien" } } }],
      { x: 0.8, y: 5.0, w: 11.7, h: 0.5, fontSize: 16, align: "center" });
  txt(s, "Nhóm 10 · Nguyễn Duy Phong · Hoàng Hải Đăng · Trần Anh Hào", { x: 0.8, y: 5.55, w: 11.7, h: 0.4,
      fontSize: 14, color: "C9B4B9", align: "center" });
  s.addNotes("Cảm ơn. Mời thầy và các bạn đặt câu hỏi. Mọi số liệu trong slide có thể tái lập từ repo.");
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  if (APPLY_THEME) {
    const { applyTheme } = require(APPLY_THEME);
    await applyTheme(OUT, THEME);
  }
  console.log("->", OUT);
})();
