/**
 * chaoshan-qiaopi renderer v24
 * Background: ama-jpg.jpg (阿嫲情书侨批信笺生成(1).jpg, JPG format)
 * Paper: 1773x2364, aged paper texture, "侨批" title at top, red frame + 8 columns + circular seal
 * v23 fix: dynamic maxPerCol = floor(1704/fontSize), clamp --cols.
 * v24 fix (BETTER): charsPerColumn default=28, 前置截断输入文本。
 *       totalCap = 8×28 = 224. 超长文字在渲染前就截断，绝不溢出。
 *       同时保留 maxPerCol 防护 --cols 超限。
 */

const puppeteer = require("puppeteer-core");
const path = require("node:path");
const fs = require("node:fs");

const EDGE_PATHS = [
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
  process.env.LOCALAPPDATA + "\\Microsoft\\Edge\\Application\\msedge.exe",
];

function getEdgePath() {
  for (const p of EDGE_PATHS) {
    if (fs.existsSync(p)) return p;
  }
  throw new Error("Edge browser not found.");
}

function fileToDataUri(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const mimeMap = { ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg" };
  const mime = mimeMap[ext] || "image/png";
  const buf = fs.readFileSync(filePath);
  return "data:" + mime + ";base64," + buf.toString("base64");
}

/**
 * Load a local font file and return a @font-face CSS block with base64 data URI.
 * Supports .ttf, .otf, .ttc (treated as truetype).
 */
function loadLocalFontCSS(fontFilePath, fontFamilyName) {
  if (!fs.existsSync(fontFilePath)) return "";
  const ext = path.extname(fontFilePath).toLowerCase();
  const fmtMap = { ".ttf": "truetype", ".otf": "opentype", ".ttc": "truetype" };
  const fmt = fmtMap[ext] || "truetype";
  const mimeMap = { ".ttf": "font/truetype", ".otf": "font/opentype", ".ttc": "font/truetype" };
  const mime = mimeMap[ext] || "font/truetype";
  const b64 = fs.readFileSync(fontFilePath).toString("base64");
  return [
    "@font-face {",
    "  font-family: '" + fontFamilyName + "';",
    "  src: url('data:" + mime + ";base64," + b64 + "') format('" + fmt + "');",
    "  font-weight: normal;",
    "  font-style: normal;",
    "}"
  ].join("\n");
}

function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function buildHtml(letterText, opts) {
  const fontSize = opts.fontSize || 52;
  const charsPerColumn = opts.charsPerColumn || 18;
  const rotation = opts.rotation || 0;
  const bgUri    = opts.bgUri;
  const fontPath = opts.fontPath || "";

  // --- 本地字体加载（优先级：用户指定 > 楷体 > 仿宋 > 宋体）---
  const fontsDir = path.join(__dirname, "fonts");
  const builtinFonts = [
    { file: path.join(fontsDir, "simkai.ttf"),  family: "SimKai"  },   // 楷体 - 最适合手写信件
    { file: path.join(fontsDir, "simfang.ttf"), family: "SimFang" },   // 仿宋 - 备用
    { file: path.join(fontsDir, "simsun.ttc"),  family: "SimSun"  },   // 宋体 - 最终保底
  ];

  let fontFaceCSS = "";
  let primaryFont = "";

  // 用户指定字体优先
  if (fontPath && fs.existsSync(fontPath)) {
    fontFaceCSS += loadLocalFontCSS(fontPath, "QiaopiFont");
    primaryFont = "'QiaopiFont', ";
  }

  // 内嵌内置字体（全部加载，让浏览器按 font-family 顺序回退）
  for (const f of builtinFonts) {
    fontFaceCSS += "\n" + loadLocalFontCSS(f.file, f.family);
  }

  // font-family 回退链（楷体 > 仿宋 > 宋体）
  const fontStack = primaryFont + "'SimKai', 'SimFang', 'SimSun', serif;";

  // Paper dimensions for 阿嫲情书侨批信笺生成(1).png (v16 default)
  // Background: 1773x2364, aged paper, "侨批" title prominent at top
  // Red frame + 8 vertical column lines + circular seal at lower-center
  // Red lines approx: x≈190, 410, 598, 790, 972, 1158, 1340, 1536
  // Frame borders approx: left~185, right~1540, top~400, bottom~2210
  // Seal area: center approx (886, 1600), radius~180px, y: 1420-1780
  // Writing columns are BETWEEN the red lines, right-to-left (traditional Chinese)

  // Column width calculation:
  // Red line spacing ~193-198px (relatively even).
  // In vertical-rl mode, line-height controls the horizontal gap between columns.

  return [
    "<!DOCTYPE html>",
    "<html>",
    "<head>",
    "<meta charset=\"utf-8\">",
    "<style>",
    "/* v15: 使用本地内嵌字体，不依赖 Google Fonts CDN，彻底解决无头模式乱码 */",
    fontFaceCSS,
    "* { margin: 0; padding: 0; box-sizing: border-box; }",
    "html, body { width: 100%; height: 100%; overflow: hidden; }",
    "body { background: #f5f0e6; display: flex; justify-content: center; align-items: center; }",
    
    ".paper {",
    "  width: 1773px;",
    "  height: 2364px;",
    "  position: relative;",
    "  background-image: url('" + bgUri + "');",
    "  background-size: 1773px 2364px;",
    "  background-position: center center;",
    "  background-repeat: no-repeat;",
    "}",
    /* Text container - positioned within the frame */
    ".text-wrap {",
    "  position: absolute;",
    "  top: 580px;",          // Below title (v18: increased from 520)
    "  left: 0;",             // v18: full width, columns use absolute coords
    "  right: 0;",            // v18: full width
    "  bottom: 80px;",        // v22: 160→80, text reaches deeper into seal
    "  transform: rotate(" + rotation + "deg);",
    "  transform-origin: center center;",
    "}",
    /* Each vertical column - absolute position + inline left style */
    ".col {",
    "  position: absolute;",
    "  top: 0;",
    "  width: " + fontSize + "px;",
    "  font-family: " + fontStack,
    "  font-size: " + fontSize + "px;",
    "  color: #2a1810;",
    "  overflow: visible;",
    "}",
    ".col span {",
    "  display: block;",
    "  text-align: center;",
    "  line-height: 1;",
    "  letter-spacing: 2px;",
    "}",
    "/* v19: seal-gap removed - text can overlap seal */",
    "</style>",
    "</head>",
    "<body>",
    "<div class=\"paper\">",
    "<div class=\"text-wrap\">",
    buildColumnsHtml(letterText, charsPerColumn, fontSize),
    "</div>",
    "</div>",
    "</body>",
    "</html>"
  ].join("\n");
}

function buildColumnsHtml(letterText, charsPerColumn, fontSize) {
  const text = letterText.replace(/\r\n/g, "").replace(/\n/g, "");
  const columns = [];
  
  for (let i = 0; i < text.length; i += charsPerColumn) {
    columns.push(text.substring(i, i + charsPerColumn));
  }
  
  // Limit to 8 columns (the paper only has 8 writing zones)
  const maxCols = 8;
  if (columns.length > maxCols) {
    columns.splice(maxCols);
  }
  
  // Column left positions (absolute paper coordinates, center of each red-line interval)
  // v21: JPG底图红线 at y=472: 194, 413, 601, 791, 974, 1159, 1342, 1535
  // col left = interval_center - fontSize/2, +1px correction for text-align:center rendering
  const halfW = Math.round(fontSize / 2);
  const colLefts = [
    1440 - halfW,   // col-1 (rightmost): between 1342-1535, center=1439 (+1px)
    1252 - halfW,   // col-2: between 1159-1342, center=1251 (+1px)
    1068 - halfW,   // col-3: between 974-1159, center=1067 (+1px)
    884 - halfW,    // col-4: between 791-974, center=883 (+1px)
    697 - halfW,    // col-5: between 601-791, center=696 (+1px)
    508 - halfW,    // col-6: between 413-601, center=507 (+1px)
    305 - halfW,    // col-7: between 194-413, center=304 (+1px)
    191 - halfW,    // col-8 (leftmost): between frame~185-194, center=190 (+1px)
  ];
  
  // v19: seal-gap removed - text can overlay the circular seal area
  
  return columns.map((col, idx) => {
    const leftPx = colLefts[idx] || 0;
    
    // Build spans for each character
    const chars = [...col];  // split into individual characters
    let spansHtml = '';
    
    for (let ci = 0; ci < chars.length; ci++) {
      spansHtml += '<span>' + escapeHtml(chars[ci]) + '</span>';
    }
    
    return '<div class="col" style="transform:translateX(' + leftPx + 'px)">' + spansHtml + '</div>';
  }).join("");
}

async function renderLetter(letterText, outputPath, format, fontSize, bgPath, fontPath, charsPerColumn, rotation) {
  const edgePath = getEdgePath();
  
  console.log("Loading background image...");
  let bgUri;
  if (fs.existsSync(bgPath)) {
    bgUri = fileToDataUri(bgPath);
    console.log("Background loaded (" + Math.round(bgUri.length / 1024) + "KB base64)");
  } else {
    console.warn("Warning: Background image not found at " + bgPath + ", using fallback color.");
    bgUri = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==";
  }

  const html = buildHtml(letterText, { fontSize, bgUri, fontPath, charsPerColumn, rotation });

  const browser = await puppeteer.launch({
    executablePath: edgePath,
    headless: true,
    args: [
      "--no-sandbox", "--disable-setuid-sandbox",
      "--disable-dev-shm-usage", "--disable-gpu",
      "--disable-web-security",
      "--allow-file-access-from-files",
      "--font-render-hinting=none",     // 禁用字体渲染提示，避免无头模式字体问题
      "--disable-font-subpixel-positioning",
    ],
  });

  let page;
  try {

    page = await browser.newPage();
    await page.setViewport({ width: 1773, height: 2364, deviceScaleFactor: 1 });
    await page.setContent(html, { waitUntil: "domcontentloaded" });
    // 本地字体以 base64 内嵌，不依赖网络，等待 1.5s 确保字体解码完成后渲染稳定
    await new Promise(function(r) { setTimeout(r, 1500); });

    let buffer;
    if (format === "jpg" || format === "jpeg") {
      buffer = await page.screenshot({ type: "jpeg", quality: 95, fullPage: true });
    } else {
      buffer = await page.screenshot({ type: "png", fullPage: true });
    }

    await browser.close();

    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(outputPath, buffer);
    console.log("Saved: " + outputPath);
    return outputPath;
  } catch (err) {
    if (browser) await browser.close();
    throw err;
  }
}

// CLI
var args = process.argv.slice(2);

function get(flag, short) {
  var idx = args.indexOf("--" + flag);
  if (idx === -1 && short) idx = args.indexOf("-" + short);
  return idx !== -1 ? args[idx + 1] : null;
}

function getFlag(flag, short) {
  var idx = args.indexOf("--" + flag);
  if (idx === -1 && short) idx = args.indexOf("-" + short);
  return idx !== -1;
}

var text     = get("text",    "t");
var output   = get("output",  "o");
var format   = get("format",  "f") || "png";
var fontSize = parseInt(get("fontSize", "s") || "52", 10);

// v24: 前置截断 — 在渲染前就把文字裁到纸面容得下的长度
// 垂直上限: floor((2364-580-80) / fontSize) = floor(1704/52) = 32
// 但默认每列 28 字、8 列总容量 224，只在用户强行指定 --cols 超限时才用 maxPerCol
var PAPER_H      = 2364;
var TEXT_TOP     = 580;
var TEXT_BOTTOM  = 80;
var maxPerCol    = Math.floor((PAPER_H - TEXT_TOP - TEXT_BOTTOM) / fontSize);

var userCols     = get("cols", "c");
var charsPerColumn;

if (userCols) {
  charsPerColumn = parseInt(userCols, 10);
  if (charsPerColumn > maxPerCol) {
    console.log("⚠ 每列字数从 " + charsPerColumn + " 调整为 " + maxPerCol + "（纸面容量上限，fontSize=" + fontSize + "）");
    charsPerColumn = maxPerCol;
  }
} else {
  charsPerColumn = 28;   // v24: 回到 28 默认
}

// ===== 前置截断：文字在渲染前就裁好 =====
var totalCap = 8 * charsPerColumn;
var cleanText = text.replace(/\r?\n/g, "");
if (cleanText.length > totalCap) {
  var dropped = cleanText.length - totalCap;
  // 按实际每列字数精确截断
  var truncated = "";
  for (var ci = 0; ci < 8 && ci * charsPerColumn < cleanText.length; ci++) {
    truncated += cleanText.substring(ci * charsPerColumn, (ci + 1) * charsPerColumn);
  }
  console.log("✂ 原文 " + cleanText.length + " 字，信纸仅容 " + totalCap + " 字，截断尾部 " + dropped + " 字");
  console.log("  提示：减小 --fontSize 可容纳更多字，如 --fontSize 40");
  text = truncated;
}

var rotation   = parseInt(get("rotate", "r") || "0", 10);
var bgPath   = get("bg",      "b") || path.join(__dirname, "fonts", "ama-jpg.jpg");
var fontPath = get("font",    "F") || "";
var help     = getFlag("help", "h");

if (help || !text || !output) {
  console.log("Usage: node render-qiaopi.js --text <text> --output <out.png> [--format png|jpg] [--fontSize 52] [--cols 18] [--rotate 0] [--font <font.ttf>] [--bg <bg.jpg>]");
  process.exit(0);
}

renderLetter(text, output, format, fontSize, bgPath, fontPath, charsPerColumn, rotation).catch(function(err) {
  console.error("Error: " + err.message);
  process.exit(1);
});
