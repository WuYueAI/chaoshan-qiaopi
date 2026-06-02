/**
 * chaoshan-qiaopi renderer
 * Background: 正1.png (潮汕侨批信笺底图, PNG format)
 * Paper: 1536x2727, aged paper texture, "侨批" title at top, red frame + 11 columns + circular seal
 * charsPerColumn default=27, 前置截断输入文本。
 *       totalCap = 11×27 = 297. 超长文字在渲染前就截断，绝不溢出。
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

  // Paper dimensions for 正1.png (v26)
  // Background: 1536x2727, aged paper, "侨批" title prominent at top
  // Red frame + 11 vertical column lines + photo element at bottom-right
  // Column boundaries (user-calibrated): 146,232,335,444,555,675,790,908,1026,1144,1261,1379
  // Frame borders: text-area top=796, bottom=2199
  // Photo zone: left≈795, top≈1830, width≈662, height≈473 (text must avoid this area)
  // Writing columns are BETWEEN the red lines, right-to-left (traditional Chinese)

  return [
    "<!DOCTYPE html>",
    "<html>",
    "<head>",
    "<meta charset=\"utf-8\">",
    "<style>",
    "/* v26: 使用本地内嵌字体，不依赖 Google Fonts CDN，彻底解决无头模式乱码 */",
    fontFaceCSS,
    "* { margin: 0; padding: 0; box-sizing: border-box; }",
    "html, body { width: 100%; height: 100%; overflow: hidden; }",
    "body { background: #f5f0e6; display: flex; justify-content: center; align-items: center; }",
    
    ".paper {",
    "  width: 1536px;",
    "  height: 2727px;",
    "  position: relative;",
    "  background-image: url('" + bgUri + "');",
    "  background-size: 1536px 2727px;",
    "  background-position: center center;",
    "  background-repeat: no-repeat;",
    "}",
    /* Text container - positioned within the frame */
    ".text-wrap {",
    "  position: absolute;",
    "  top: 796px;",          // Below title, user-calibrated
    "  left: 0;",
    "  right: 0;",
    "  bottom: 528px;",       // 2727-2199=528, user-calibrated
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
  
  // v26: 11 columns (was 7)
  const maxCols = 11;
  if (columns.length > maxCols) {
    columns.splice(maxCols);
  }
  
  // Column left positions (absolute paper coordinates, center of each column interval)
  // v27: 11 columns, user-calibrated on 正1.png (1536×2727)
  // col centers: 189,284,390,500,615,733,849,967,1085,1203,1320
  // col left = center - fontSize/2
  const halfW = Math.round(fontSize / 2);
  const colCenters = [1320, 1203, 1085, 967, 849, 733, 615, 500, 390, 284, 189];
  
  // ===== 照片回避区 (v28: 扩大覆盖以完整遮住船型装饰) =====
  var PHOTO_LEFT     = 780,  PHOTO_RIGHT    = 780 + 690;   // 780~1470
  var PHOTO_TOP      = 1700, PHOTO_BOTTOM   = 1700 + 650;  // 1700~2350
  var TEXT_Y         = 796;
  var blockedStart   = Math.floor((PHOTO_TOP - TEXT_Y) / fontSize);
  var blockedEnd     = Math.floor((PHOTO_BOTTOM - TEXT_Y) / fontSize);
  
  return columns.map((col, idx) => {
    var center = colCenters[idx] || 0;
    var leftPx = center - halfW;
    var colL = center - halfW, colR = center + halfW;
    var inPhotoX = (colR > PHOTO_LEFT && colL < PHOTO_RIGHT);
    
    var chars = [...col];
    var spansHtml = '';
    
    for (var ci = 0; ci < chars.length; ci++) {
      if (inPhotoX && ci >= blockedStart && ci <= blockedEnd) {
        spansHtml += '<span style="visibility:hidden">&nbsp;</span>';
      } else {
        spansHtml += '<span>' + escapeHtml(chars[ci]) + '</span>';
      }
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
    await page.setViewport({ width: 1536, height: 2727, deviceScaleFactor: 1 });
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

// v26: 前置截断 — 在渲染前就把文字裁到纸面容得下的长度
// 垂直上限: floor((2199-796) / fontSize) = floor(1403/52) = 26
// 默认每列 27 字、11 列总容量 297，只在用户强行指定 --cols 超限时才用 maxPerCol
var PAPER_H      = 2727;
var TEXT_TOP     = 796;
var TEXT_BOTTOM  = 528;   // 2727-2199=528
var maxPerCol    = Math.round((PAPER_H - TEXT_TOP - TEXT_BOTTOM) / fontSize);

var userCols     = get("cols", "c");
var charsPerColumn;

if (userCols) {
  charsPerColumn = parseInt(userCols, 10);
  if (charsPerColumn > maxPerCol) {
    console.log("⚠ 每列字数从 " + charsPerColumn + " 调整为 " + maxPerCol + "（纸面容量上限，fontSize=" + fontSize + "）");
    charsPerColumn = maxPerCol;
  }
} else {
  charsPerColumn = 27;   // v26: 11列×27字=297字容量
}

// ===== 前置截断：文字在渲染前就裁好 =====
var totalCap = 11 * charsPerColumn;
var cleanText = text.replace(/\r?\n/g, "");
if (cleanText.length > totalCap) {
  var dropped = cleanText.length - totalCap;
  // 按实际每列字数精确截断
  var truncated = "";
  for (var ci = 0; ci < 11 && ci * charsPerColumn < cleanText.length; ci++) {
    truncated += cleanText.substring(ci * charsPerColumn, (ci + 1) * charsPerColumn);
  }
  console.log("✂ 原文 " + cleanText.length + " 字，信纸仅容 " + totalCap + " 字，截断尾部 " + dropped + " 字");
  console.log("  提示：减小 --fontSize 可容纳更多字，如 --fontSize 40");
  text = truncated;
}

var rotation   = parseInt(get("rotate", "r") || "0", 10);
var bgPath   = get("bg",      "b") || path.join(__dirname, "fonts", "正1.png");
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
