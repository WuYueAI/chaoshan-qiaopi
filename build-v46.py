#!/usr/bin/env python3
"""Build qiaopi-demo.html v46 — 大规模扩池去重复 + 结构变体"""

import base64

bg_uris = []
for i in [1, 2, 3]:
    path = rf"C:\Users\EDY\WorkBuddy\20260601100602\正{i}.png"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    bg_uris.append(f"data:image/png;base64,{b64}")

bg_uris_js = "var BG_URIS = [\n  " + ",\n  ".join(f'"{uri}"' for uri in bg_uris) + "\n];"

CSS = """\
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:#efe6d5;color:#3b2616;min-height:100vh}
.topbar{background:#2a1a0c;color:#c9b086;font-size:12px;text-align:center;padding:6px 16px;letter-spacing:1px}
.container{max-width:680px;margin:0 auto;padding:24px 18px 60px}
.header{text-align:center;padding:24px 0 20px}
.seal-mark{display:inline-flex;align-items:center;justify-content:center;width:60px;height:60px;border:2.5px solid #b53a25;border-radius:50%;color:#b53a25;font-family:"KaiTi","楷体","STKaiti",serif;font-size:20px;font-weight:bold;letter-spacing:4px;transform:rotate(-12deg);background:rgba(181,58,37,.04);margin-bottom:10px}
.header h1{font-family:"KaiTi","楷体","STKaiti",serif;font-size:28px;color:#3b2210;letter-spacing:8px;margin-bottom:2px}
.subtitle{color:#8b6e50;font-size:13px;letter-spacing:4px}
.card{background:#fefcf6;border:1px solid #ddd0b8;border-radius:4px;padding:20px 22px;margin-bottom:12px;box-shadow:0 1px 4px rgba(100,70,30,.06)}
.card-label{font-family:"KaiTi","楷体","STKaiti",serif;font-size:15px;color:#6b4c2a;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid #ede0c8;letter-spacing:2px}
.card-label::before{content:"";display:inline-block;width:3px;height:15px;background:#b53a25;margin-right:8px;vertical-align:middle;border-radius:1px}
textarea#ta{width:100%;height:150px;padding:14px 16px;border:2px solid #ddd0b8;border-radius:4px;font-family:"KaiTi","楷体","STKaiti","FangSong","仿宋",serif;font-size:16px;line-height:2;color:#2a1810;background:#fffef9;resize:vertical}
textarea#ta:focus{outline:none;border-color:#b53a25;box-shadow:0 0 0 3px rgba(181,58,37,.06)}
.char-stat{display:flex;justify-content:space-between;align-items:center;margin-top:8px;font-size:12px;color:#9b8b72;letter-spacing:1px}
.char-stat .bar-wrap{flex:1;height:4px;background:#e8dcc8;border-radius:2px;margin:0 12px;max-width:160px}
.char-stat .bar-inner{height:100%;border-radius:2px;transition:width .3s,background .3s}
.bar-ok{background:#8bb88b}.bar-warn{background:#d4a54a}.bar-over{background:#c04030}
.param-row{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:12px}
.param label{display:flex;justify-content:space-between;align-items:baseline;font-size:12px;color:#5c3a1a;margin-bottom:3px;letter-spacing:1px}
.param label .val{font-family:"KaiTi","楷体","STKaiti",serif;font-size:13px;color:#b53a25}
.param input[type=range]{width:100%;accent-color:#b53a25;height:4px}
.param .desc{font-size:10px;color:#b5a58a;margin-top:1px}
.btn-row{display:flex;gap:10px;margin-top:14px}
.btn{font-family:"KaiTi","楷体","STKaiti",serif;cursor:pointer;letter-spacing:2px;transition:all .2s;border:none;border-radius:4px;text-align:center}
.btn-gen{flex:1;padding:12px 0;font-size:15px;color:#fff;background:#b53a25;letter-spacing:3px}
.btn-gen:hover{background:#9a301e}
.btn-gen:disabled{background:#cfc0a8;color:#f5efe0;cursor:not-allowed}
.btn-gen.loading{background:#9a7b5c;cursor:wait;animation:pulse 0.8s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.65}}
.btn-dl{padding:10px 28px;font-family:"KaiTi","楷体","STKaiti",serif;font-size:14px;color:#fff;background:#5a8040;border:none;border-radius:4px;letter-spacing:3px;cursor:pointer}
.btn-dl:hover{background:#4a6e32}
.btn-re{padding:10px 24px;font-family:"KaiTi","楷体","STKaiti",serif;font-size:13px;color:#6b4c2a;background:transparent;border:1px solid #ddd0b8;border-radius:3px;letter-spacing:1px;cursor:pointer}
.btn-re:hover{background:#faf6ee;border-color:#c8b080}
.toast{display:none;padding:10px 16px;border-radius:4px;font-size:13px;margin-bottom:10px;letter-spacing:1px;white-space:pre-wrap}
.toast.show{display:block}
.toast-info{background:#fef9e8;border:1px solid #e8d28a;color:#8b6e2a}
.toast-error{background:#fef0f0;border:1px solid #e8b0b0;color:#8b2a2a}
.result-section{display:none}
.result-section.show{display:block}
.result-wrap{text-align:center}
.result-wrap img{max-width:100%;border-radius:3px;box-shadow:0 4px 24px rgba(60,30,10,.18);border:1px solid #d4c0a0}
.result-btns{display:flex;gap:12px;justify-content:center;margin-top:12px}
.footer{text-align:center;padding:24px 0 12px;font-size:12px;color:#b5a58a;letter-spacing:1px;line-height:1.8}
.footer .sep{display:inline-block;margin:0 8px;color:#d5c8a8}
"""

JS_CORE = r"""
/* ================================================================
   v44 重构 — 输入差异化文本转换引擎
   - 渲染：纯 Canvas 逐字绘制（先画底图、后画竖排文字），彻底脱离 html2canvas
   - 转换：多维度信息提取 + 动态模板选择 + 关键内容保留
     不再丢弃用户的原始内容，而是将其转换为侨批文体
   ================================================================ */

var bgDims = { w: 1536, h: 2727, textTop: 796, textBottom: 528, cols: 11 };

// 11 列中心坐标（从右到左，用户校准于正1.png 1536x2727）
var COL_CENTERS = [1320, 1203, 1085, 967, 849, 733, 615, 500, 390, 284, 189];

// 照片回避区（右下角船型装饰，文字自动跳过此区域）
var PHOTO = { left: 780, right: 1470, top_y: 1700, bottom_y: 2350 };

// ========== 预加载底图（随机三选一，onload/onerror 必须在 src 之前）==========
var bgReady = false;
var _renderCallback = null;
var bgImage = new Image();
bgImage.onload = function() {
  bgReady = true;
  console.log("底图加载成功");
  if (_renderCallback) { var cb = _renderCallback; _renderCallback = null; cb(); }
};
bgImage.onerror = function() {
  bgReady = false;
  console.warn("底图加载失败");
  if (_renderCallback) { var cb = _renderCallback; _renderCallback = null; cb(); }
};

// 初始化：随机选一张底图
bgImage.src = BG_URIS[Math.floor(Math.random() * BG_URIS.length)];

// 随机切换底图并等待加载完成后回调
function loadRandomBGThen(callback) {
  bgReady = false;
  _renderCallback = callback;
  var uri = BG_URIS[Math.floor(Math.random() * BG_URIS.length)];
  // 防止选中同一张导致 onload 不触发（Image 缓存可能跳过）
  if (uri === bgImage.src) {
    bgReady = true;
    if (callback) callback();
  } else {
    bgImage.src = uri;
  }
}

// ========== DOM ==========
var ta = document.getElementById("ta"),
    fs = document.getElementById("fs"),
    cc = document.getElementById("cc"),
    btnGen = document.getElementById("btnGen"),
    resultSec = document.getElementById("resultSec"),
    toast = document.getElementById("toast");
var _blobUrl = null;

// ========== 字数统计 ==========
function updateCap() {
  var f = +fs.value, c = +cc.value;
  var textH = bgDims.h - bgDims.textTop - bgDims.textBottom;
  var mpc = Math.floor(textH / f), ac = Math.min(c, mpc);
  var cap = bgDims.cols * ac, len = (ta.value||"").replace(/\r?\n/g,"").length;
  document.getElementById("fsv").textContent = f;
  document.getElementById("cv").textContent = ac;
  document.getElementById("charCnt").textContent = len;
  document.getElementById("capNum").textContent = bgDims.cols + "\u00d7" + ac + "=" + cap;
  var bar = document.getElementById("capBar");
  var pct = Math.min(100, len / cap * 100);
  bar.style.width = pct + "%";
  bar.className = "bar-inner " + (len > cap ? "bar-over" : len > cap * 0.8 ? "bar-warn" : "bar-ok");
}
ta.addEventListener("input", updateCap);
fs.addEventListener("input", updateCap);
cc.addEventListener("input", updateCap);
updateCap();

/* ================================================================
   侨批文体转换 — 多维度信息提取 + 动态模板选择
   核心理念：保留用户输入的核心内容，仅做文体转换，不做内容替换
   ================================================================ */

// ---- 关系识别 ----
var RELATION_MAP = {
  "\u5976\u5976":   { who: "\u963f\u5b37", sign: "\u5b59\u67d0\u67d0 \u8c28\u4e66" },
  "\u963f\u5b37":   { who: "\u963f\u5b37", sign: "\u5b59\u67d0\u67d0 \u8c28\u4e66" },
  "\u5916\u5a46":   { who: "\u5916\u5a46", sign: "\u5b59\u67d0\u67d0 \u8c28\u4e66" },
  "\u7237\u7237":   { who: "\u963f\u516c", sign: "\u5b59\u67d0\u67d0 \u8c28\u4e66" },
  "\u963f\u516c":   { who: "\u963f\u516c", sign: "\u5b59\u67d0\u67d0 \u8c28\u4e66" },
  "\u5916\u516c":   { who: "\u5916\u516c", sign: "\u5b59\u67d0\u67d0 \u8c28\u4e66" },
  "\u7238\u7238":   { who: "\u7236\u4eb2", sign: "\u513f\u67d0\u67d0 \u53e9\u4e0a" },
  "\u7236\u4eb2":   { who: "\u7236\u4eb2", sign: "\u513f\u67d0\u67d0 \u53e9\u4e0a" },
  "\u8001\u7238":   { who: "\u7236\u4eb2", sign: "\u513f\u67d0\u67d0 \u53e9\u4e0a" },
  "\u5988\u5988":   { who: "\u6bcd\u4eb2", sign: "\u513f\u67d0\u67d0 \u53e9\u4e0a" },
  "\u6bcd\u4eb2":   { who: "\u6bcd\u4eb2", sign: "\u513f\u67d0\u67d0 \u53e9\u4e0a" },
  "\u8001\u5988":   { who: "\u6bcd\u4eb2", sign: "\u513f\u67d0\u67d0 \u53e9\u4e0a" },
  "\u8001\u5a46":   { who: "\u5a18\u5b50", sign: "\u592b\u67d0\u67d0 \u5b57" },
  "\u5a18\u5b50":   { who: "\u5a18\u5b50", sign: "\u592b\u67d0\u67d0 \u5b57" },
  "\u59bb\u5b50":   { who: "\u5a18\u5b50", sign: "\u592b\u67d0\u67d0 \u5b57" },
  "\u8001\u516c":   { who: "\u592b\u541b", sign: "\u59bb\u67d0\u67d0 \u5b57" },
  "\u592b\u541b":   { who: "\u592b\u541b", sign: "\u59bb\u67d0\u67d0 \u5b57" },
  "\u4e08\u592b":   { who: "\u592b\u541b", sign: "\u59bb\u67d0\u67d0 \u5b57" },
  "\u670b\u53cb":   { who: "\u543e\u53cb", sign: "\u53cb\u67d0\u67d0" },
  "\u5144\u5f1f":   { who: "\u543e\u5144", sign: "\u5f1f\u67d0\u67d0" },
  "\u963f\u5144":   { who: "\u963f\u5144", sign: "\u5f1f\u67d0\u67d0" },
  "\u54e5\u54e5":   { who: "\u963f\u5144", sign: "\u5f1f\u67d0\u67d0" },
  "\u963f\u59d0":   { who: "\u963f\u59d0", sign: "\u59b9\u67d0\u67d0" },
  "\u59d0\u59d0":   { who: "\u963f\u59d0", sign: "\u59b9\u67d0\u67d0" },
};

function detectRelation(text) {
  // 复合称谓优先（双亲）
  if (/老爸老妈|爸妈|父母|双亲|阿爸阿妈|爸爸妈妈/.test(text))
    return { who: "\u7236\u6bcd", sign: "\u513f\u67d0\u67d0 \u53e9\u4e0a" };

  for (var k in RELATION_MAP) {
    if (text.indexOf(k) >= 0) return RELATION_MAP[k];
  }
  return { who: "\u4eb2\u957f", sign: "\u67d0\u67d0 \u656c\u4e0a" };
}

// ---- 多维度信息提取 ----
// 从输入中提取尽可能多的信息，让输出真正因输入而异

function extractAllInfo(text) {
  var info = {
    rel: detectRelation(text),
    // 汇款信息
    hasMoney: false,
    moneyAmount: "",
    moneyExtra: "",  // 寄钱的具体说明
    // 地域/工作
    location: "",
    locationExtra: "", // 城市名/地名
    workDesc: "",    // 工作具体情况
    workType: "normal", // good/busy/hard/none
    // 身体
    health: "",      // 身体状况的具体描述
    healthType: "",  // good/tired/sick/injured
    // 季节/天气
    season: "",
    weather: "",
    // 生活
    living: "",      // 生活状况的具体描述
    // 思念/回忆
    memories: [],    // 用户提到回忆的内容
    memoryText: "",  // 合并后的回忆文本
    // 对家人的关心
    concerns: "",
    concernItems: [],
    // 其他要告知的事
    news: [],
  };

  // --- 汇款检测 ---
  var mm = text.match(/(?:寄|汇|打)(?:了|的)?(?:\d+[块元百千万]?)?(?:一点|些|点)?(?:钱|款|银|工资|薪水)/);
  if (mm) info.hasMoney = true;

  // 金额提取：支持 数字+元/块/百/千/万
  var ams = [
    { re: /(\d+)\s*万/, mul: "万" },
    { re: /(\d+)\s*千/, mul: "千" },
    { re: /(\d+)\s*百/, mul: "百" },
    { re: /(\d+)\s*元/, mul: "元" },
    { re: /(\d+)\s*块/, mul: "元" },
  ];
  for (var ai = 0; ai < ams.length; ai++) {
    var m = text.match(ams[ai].re);
    if (m) {
      info.moneyAmount = chineseNumber(m[1]) + ams[ai].mul;
      break;
    }
  }
  if (!info.moneyAmount && info.hasMoney) info.moneyAmount = "\u4e9b\u8bb8";
  // moneyExtra 仅匹配寄/汇（排除"打"，因"打工"会误匹配）
  var me = text.match(/(?:寄|汇).*?(?:钱|款|银)[^，,。.!！\n]*(?=[，,。.!！\n]|$)/);
  if (me) info.moneyExtra = me[0].replace(/[我你]|的|了/g, "");

  // --- 地点提取 ---
  var lm = text.match(/(?:在|来到?|到了?|去到?)([\u4e00-\u9fff]{2,4})(?:工作|打工|上班|做工|开店|这边|那边|这里|那里|城里|市|区)/);
  if (lm) {
    info.location = lm[1];
    info.locationExtra = lm[1];
  } else {
    // 尝试提取纯地名
    var pm = text.match(/(?:在|来到?)([\u4e00-\u9fff]{2,3})(?:，|。|！|,|\.|\n|$|这边|那边)/);
    if (pm) { info.location = pm[1]; info.locationExtra = pm[1]; }
  }
  if (!info.location) info.location = "\u5916\u4e61";

  // --- 工作状况 ---
  if (/生意.*好|生意.*不错|发财|赚.*钱/.test(text)) {
    info.workType = "good";
    info.workDesc = "\u751f\u610f\u5c1a\u7a33\uff0c\u52c9\u53ef\u7ef4\u6301";
  } else if (/忙|加班|没空|赶工|赶货/.test(text)) {
    info.workType = "busy";
    info.workDesc = "\u8fd1\u65e5\u5341\u5206\u5fd9\u788c";
  } else if (/累|辛苦|难做|不好做|不容易|撑/.test(text)) {
    info.workType = "hard";
    info.workDesc = "\u505a\u5de5\u751a\u4e3a\u8f9b\u82e6";
  } else if (/没.*工|失业|找不到.*工作|闲/.test(text)) {
    info.workType = "none";
    info.workDesc = "\u8fd1\u6765\u6d3b\u8ba1\u4e0d\u592a\u987a\u9042";
  } else if (/上班|做工|打工|工作|开店|摆摊/.test(text)) {
    info.workType = "normal";
    info.workDesc = "\u8bf8\u4e8b\u52c9\u53ef\u5e94\u4ed8";
  }

  // --- 身体状况 ---
  if (/身体.*好|身体.*不错|健康|没.*病|结实/.test(text)) {
    info.healthType = "good";
    info.health = "\u8eab\u4f53\u5b89\u7a33\uff0c\u996e\u98df\u5982\u5e38";
  } else if (/累|疲倦|疲劳|没精神/.test(text)) {
    info.healthType = "tired";
    info.health = "\u8eab\u4f53\u7565\u89c9\u4e4f\u5026\uff0c\u597d\u5728\u5c1a\u80fd\u652f\u6491";
  } else if (/病|发烧|感冒|咳嗽|头疼|不舒服|难受/.test(text)) {
    info.healthType = "sick";
    var sm = text.match(/(?:病|发烧|感冒|咳嗽|头疼)(?:了)?[^，,。.!！\n]{0,10}/);
    if (sm) info.health = "\u8fd1\u6765" + sm[0] + "\uff0c\u6b63\u5728\u8c03\u6cbb";
    else info.health = "\u8fd1\u6765\u8d31\u4f53\u6b20\u5b89\uff0c\u6b63\u5ef6\u533b\u8c03\u6cbb";
  } else if (/受伤|扭|摔|跌/.test(text)) {
    info.healthType = "injured";
    info.health = "\u65e5\u524d\u4e0d\u614e\u53d7\u4f24\uff0c\u73b0\u6b63\u4f11\u517b";
  } else {
    info.health = "\u8eab\u4f53\u5b89\u7a33\uff0c\u996e\u98df\u5982\u5e38";
  }

  // --- 季节/天气 ---
  if (/\u6625\u5929|\u5f00\u6625|\u6625\u6696|\u6625\u8282/.test(text)) info.season = "\u6625";
  else if (/\u590f\u5929|\u6691|\u70ed|三伏/.test(text)) info.season = "\u590f";
  else if (/\u79cb\u5929|\u79cb\u51c9|\u4e2d\u79cb|\u843d\u53f6/.test(text)) info.season = "\u79cb";
  else if (/\u51ac\u5929|\u5bd2|\u51b7|\u8fc7\u5e74|\u65b0\u5e74/.test(text)) info.season = "\u51ac";
  // 温度关键词辅助判断
  if (/热|高温|暑/.test(text) && !info.season) info.season = "\u590f";
  if (/冷|降温|寒/.test(text) && !info.season) info.season = "\u51ac";
  if (!info.season) info.season = getCurrentSeasonFallback();

  if (/\u4e0b\u96e8|\u96e8/.test(text)) info.weather = "rain";
  else if (/\u592a\u9633|\u6652|\u6691/.test(text)) info.weather = "hot";
  else if (/\u51b7|\u5bd2|\u51bb/.test(text)) info.weather = "cold";
  else if (/\u98ce.*\u5927|\u53f0\u98ce/.test(text)) info.weather = "windy";

  // --- 思念/回忆内容 ---
  var memPatterns = [
    /(?:想|念|记得|回忆|想起|梦见|时常)[^，,。.!！\n]{3,20}/g,
    /小时候[^，,。.!！\n]{2,20}/g,
    /从前[^，,。.!！\n]{2,20}/g,
    /以前[^，,。.!！\n]{2,20}/g,
  ];
  for (var mi = 0; mi < memPatterns.length; mi++) {
    var mm2;
    while ((mm2 = memPatterns[mi].exec(text)) !== null) {
      var memContent = mm2[0];
      // 过滤掉太短的
      var cleaned = memContent.replace(/真的好|真的太|特别|非常|很/g, "");
      if (cleaned.length >= 4) info.memories.push(cleaned);
    }
  }
  // 去重
  info.memories = info.memories.filter(function(v, i, a) { return a.indexOf(v) === i; });
  if (info.memories.length > 0) {
    info.memoryText = info.memories[0];
  }

  // --- 关心/叮嘱家人 ---
  var concernPatterns = [
    /(?:注意|保重|小心|别|不要|该|要记得|多穿|多喝|多吃|好好)[^，,。.!！\n]{2,20}/g,
    /身体[^，,。.!！\n]{1,10}(?:好|注意)/g,
    /别.*累/g,
  ];
  for (var ci = 0; ci < concernPatterns.length; ci++) {
    var cm;
    while ((cm = concernPatterns[ci].exec(text)) !== null) {
      var raw = cm[0];
      // 过滤纯疑问句、太短的、纯口语
      if (raw.length >= 3 && !/\uff1f|\u5417|\u597d\u4e0d\u597d/.test(raw) && !/^\u522b\u592a.*$/.test(raw)) {
        info.concernItems.push(raw);
      }
    }
  }
  // 最多保留 3 条，优先保留更长的
  if (info.concernItems.length > 3) {
    info.concernItems.sort(function(a, b) { return b.length - a.length; });
    info.concernItems = info.concernItems.slice(0, 3);
  }
  if (info.concernItems.length > 0) {
    info.concerns = info.concernItems[0];
  }

  // --- 生活状况 ---
  var livingRe = /(?:生活|日子|吃饭|睡觉|住|伙食)[^，,。.!！\n]{2,20}/g;
  var lm2;
  while ((lm2 = livingRe.exec(text)) !== null) {
    info.living = lm2[0];
  }

  // --- 其他事由 ---
  // 提取用户提到的一些具体事情
  var newsPatterns = [
    /(?:最近|近来|近期)[^，,。.!！\n]{4,30}/g,
    /(?:告诉|跟你说|说一下)[^，,。.!！\n]{4,20}/g,
  ];
  for (var ni = 0; ni < newsPatterns.length; ni++) {
    var nm;
    while ((nm = newsPatterns[ni].exec(text)) !== null) {
      info.news.push(nm[0]);
    }
  }

  return info;
}

// 阿拉伯数字转中文数字（按位值转换：300→三百，312→三百一十二）
function chineseNumber(n) {
  if (n === 0) return "\u96f6";
  var digits = ["\u96f6","\u4e00","\u4e8c","\u4e09","\u56db","\u4e94","\u516d","\u4e03","\u516b","\u4e5d"];
  var units  = ["","\u5341","\u767e","\u5343","\u4e07"];
  var s = String(n), result = "";
  var len = s.length, hasZero = false;
  for (var i = 0; i < len; i++) {
    var d = parseInt(s[i]);
    var u = len - i - 1; // 位数: 0=个,1=十,2=百,3=千,4=万
    if (d === 0) {
      if (u === 4 && result.length > 0) result += units[4];
      else hasZero = true;
    } else {
      if (hasZero && result.length > 0) result += "\u96f6";
      hasZero = false;
      result += digits[d] + units[u];
    }
  }
  // "一十X" → "十X" (10-19)
  if (result.length >= 2 && result[0] === "\u4e00" && result[1] === "\u5341")
    result = result.substring(1);
  if (result[result.length - 1] === "\u96f6")
    result = result.slice(0, -1);
  return result;
}

// 根据当前月份推测季节
function getCurrentSeasonFallback() {
  var m = new Date().getMonth() + 1;
  if (m >= 3 && m <= 5) return "\u6625";
  if (m >= 6 && m <= 8) return "\u590f";
  if (m >= 9 && m <= 11) return "\u79cb";
  return "\u51ac";
}

// ---- 句子级别文体转换 ----
// 将用户的白话句子逐一转换为侨批文体

var VOCAB_MAP = {
  // 时间
  "\u6700\u8fd1": "\u8fd1\u6765", "\u8fd9\u51e0\u5929": "\u8fd1\u65e5",
  "\u8fd9\u4e24\u5929": "\u8fd1\u65e5", "\u8fd9\u4e00\u9635": "\u8fd1\u6bb5\u65f6\u65e5",
  "\u4eca\u5929": "\u4eca\u65e5", "\u6628\u5929": "\u6628\u65e5",
  "\u660e\u5929": "\u660e\u65e5", "\u65e9\u4e0a": "\u6e05\u6668",
  // 感觉/情绪
  "\u60f3": "\u5ff5", "\u597d\u60f3": "\u6df1\u5ff5",
  "\u62c5\u5fc3": "\u6302\u5ff5", "\u5f88\u5f00\u5fc3": "\u751a\u611f\u6b23\u6170",
  "\u96be\u8fc7": "\u5fc3\u4e2d\u6c89\u91cd", "\u4e0d\u597d\u610f\u601d": "\u6127\u759a\u4e0d\u5b89",
  // 生活
  "\u5403\u996d": "\u996e\u98df", "\u7761\u89c9": "\u5b89\u5bdd",
  "\u4f4f": "\u5c45\u4f4f", "\u5929\u6c14": "\u5929\u5019",
  "\u5f88\u597d": "\u5c1a\u597d", "\u633a\u597d\u7684": "\u8fd8\u7b97\u987a\u9042",
  "\u6ca1\u4e8b": "\u65e0\u788e", "\u4e0d\u9519": "\u5c1a\u53ef",
  // 强调
  "\u771f\u7684": "", "\u7279\u522b": "\u5c24", "\u975e\u5e38": "\u751a",
  // 称呼
  "\u6211": "\u6211", "\u4f60": "\u4f60",
  // 扩展：高频白话→文言
  "\u77e5\u9053\u4e86": "\u77e5\u6089", "\u653e\u5fc3": "\u5bbd\u5fc3",
  "\u4fdd\u91cd": "\u4fdd\u91cd", "\u5c0f\u5fc3": "\u7559\u610f",
  "\u8fc7\u5f97\u597d": "\u8fc7\u5f97\u53bb", "\u591a\u4f11\u606f": "\u591a\u52a0\u6b47\u606f",
  "\u522b\u592a\u7d2f": "\u5207\u52ff\u8fc7\u52b3", "\u522b\u7740\u6025": "\u5207\u52ff\u5fe7\u5fc3",
  "\u65e9\u70b9\u7761": "\u65e9\u4e9b\u5b89\u5bdd",
};

function convertSentence(sent) {
  sent = sent.trim();
  if (!sent || sent.length < 2) return "";

  // 先做词汇替换
  var result = sent;
  for (var k in VOCAB_MAP) {
    result = result.split(k).join(VOCAB_MAP[k]);
  }

  // 清理口语语气词（啊、呢、吧、呀、哦、咯、嘛、呗）
  result = result.replace(/[\u554a\u5462\u5427\u5440\u54e6\u54af\u563b\u5457]/g, "");

  // 清理多余的空格和重复标点
  result = result.replace(/\s+/g, "").replace(/([\uff0c\u3002\uff01\uff1f\u3001])\1+/g, "$1");

  // 去除因语气词删除留下的多余标点
  result = result.replace(/\uff0c\uff0c+/g, "\uff0c");

  // 确保句末有标点
  if (!/[\uff0c\u3002\uff01\uff1f\u3001]$/.test(result) && !/[\u3000-\u303f\uff00-\uffef]$/.test(result)) {
    result += "\u3002";
  }

  return result;
}

// ---- 侨批文体模板池 v46（大规模扩充） ----
// 核心改进：从硬编码文本 → 大容量模板池 + 确定性随机选择
// 六季思乡文本 × 6、四季关心 × 4、结尾 × 30+、附言 × 6 等

var TEMPLATES = {

  // --- 开头问候（6选1，原1） ---
  openings: [
    "{who}\u5c0a\u524d\uff0c\u5c55\u4fe1\u4f73\u5b89\u3002",
    "{who}\u5c0a\u524d\uff0c\u5c55\u4fe1\u5b89\u597d\u3002",
    "{who}\u5c0a\u9274\uff0c\u89c1\u5b57\u5982\u9762\u3002",
    "{who}\u5c0a\u524d\uff0c\u53e9\u8bf7\u798f\u5b89\u3002",
    "{who}\u819d\u4e0b\uff0c\u656c\u7980\u8005\uff1a",
    "{who}\u5927\u4eba\u5c0a\u524d\uff0c\u8c28\u6b64\u53e9\u5b89\u3002",
  ],

  // --- 无汇款开头（10选1，原3） ---
  noMoney: [
    "\u5306\u5306\u4e66\u6b64\u6570\u884c\uff0c\u804a\u8868\u5b58\u5ff5\u4e4b\u610f\u3002",
    "\u4e45\u672a\u4fee\u4e66\u95ee\u5b89\uff0c\u6b63\u6b64\u5949\u4e0a\u6570\u8a00\u3002",
    "\u5fd9\u4e2d\u62bd\u6687\uff0c\u8349\u8349\u6570\u8a00\u5949\u4e0a\uff0c\u7948\u4e3a\u5b89\u5eb7\u3002",
    "\u8fdc\u9694\u5c71\u6d77\uff0c\u804a\u5bc4\u7247\u7eb8\uff0c\u4ee5\u6170\u60ac\u5ff5\u3002",
    "\u97f3\u4e66\u4e45\u758f\uff0c\u4e2d\u5fc3\u803f\u803f\uff0c\u7279\u6b64\u62dc\u4e66\u8bf7\u5b89\u3002",
    "\u4e00\u7eb8\u5bb6\u4e66\uff0c\u4e07\u822c\u5fc3\u610f\uff0c\u4f0f\u60df\u73cd\u91cd\u3002",
    "\u8fd1\u65e5\u8bf8\u4e8b\u7a0d\u5b9a\uff0c\u7279\u4fee\u5bf8\u7b3a\u95ee\u5b89\u3002",
    "\u522b\u6765\u826f\u4e45\uff0c\u751a\u4ee5\u4e3a\u6000\uff0c\u8349\u6b64\u6570\u884c\u5949\u8fbe\u3002",
    "\u79bb\u4e61\u65e5\u4e45\uff0c\u60ac\u5ff5\u65e5\u6df1\uff0c\u706f\u4e0b\u63e1\u7ba1\uff0c\u601d\u7eea\u4e07\u5343\u3002",
    "\u6628\u591c\u53c8\u68a6\u89c1\u5bb6\u4e2d\u5149\u666f\uff0c\u9192\u6765\u540e\u4fbf\u51b3\u610f\u4fee\u4e66\u3002",
  ],

  // --- 汇款后续交代（5选1，原1） ---
  moneyFollowup: [
    "\u5bb6\u4e2d\u82e5\u6709\u6025\u9700\uff0c\u6765\u4fe1\u544a\u77e5\uff0c\u5f53\u5373\u5bc4\u4ed8\u3002",
    "\u5018\u5bb6\u4e2d\u5c1a\u6709\u4e0d\u8db3\uff0c\u52a1\u8bf7\u6765\u4fe1\uff0c\u81ea\u5f53\u518d\u5bc4\u3002",
    "\u94b1\u867d\u4e0d\u591a\uff0c\u804a\u8868\u5fc3\u610f\u3002\u82e5\u4e0d\u591f\u7528\uff0c\u5343\u4e07\u6765\u4fe1\u8bf4\u4e00\u58f0\u3002",
    "\u6b64\u6570\u5fae\u8584\uff0c\u8fd8\u671b\u7b11\u7eb3\u3002\u82e5\u6709\u4e0d\u65f6\u4e4b\u9700\uff0c\u5207\u52ff\u9690\u5fcd\u4e0d\u8a00\u3002",
    "\u5bc4\u4e0a\u6b64\u6570\uff0c\u5148\u5e94\u6025\u9700\u3002\u5f85\u4e0b\u6708\u53d1\u85aa\uff0c\u5f53\u518d\u5bc4\u4e9b\u56de\u53bb\u3002",
  ],

  // --- 状态行模板（4选1，原1） ---
  statusLine: [
    "\u6211\u5728{loc}\uff0c{work}\uff0c{health}\uff0c\u8bf7\u52ff\u6302\u5ff5\u3002",
    "\u5728{loc}\u4e00\u5207\u5c1a\u597d\uff0c{work}\u3002{health}\u3002",
    "\u6765{loc}\u5df2\u6709\u4e9b\u65f6\u65e5\uff0c{work}\u3002{health}\uff0c\u4e07\u52ff\u8fdc\u8651\u3002",
    "\u5230{loc}\u540e\uff0c{work}\u3002{health}\uff0c\u5e78\u65e0\u5927\u788d\u3002",
  ],

  // --- 季节思乡文本（每季6选1，原每季1） ---
  nostalgia: {
    "\u6625": [
      "\u8def\u65c1\u91ce\u82b1\u5df2\u5f00\uff0c\u60f3\u8d77\u4ece\u524d\u5728\u5bb6\u65f6\uff0c\u6625\u65e5\u6a90\u4e0b\u71d5\u5f52\u5de2\u7684\u5149\u666f\u3002\u4e0d\u77e5\u5bb6\u4e2d\u90a3\u68f5\u8001\u6811\uff0c\u4eca\u6625\u53ef\u66fe\u53d1\u4e86\u65b0\u82bd\uff1f",
      "\u8fd9\u51e0\u65e5\u6625\u98ce\u548c\u6696\uff0c\u5ead\u524d\u6843\u82b1\u8be5\u662f\u5f00\u4e86\u3002\u8bb0\u5f97\u5e7c\u65f6\u603b\u5728\u82b1\u4e0b\u73a9\u800d\uff0c\u90a3\u5149\u666f\u5982\u5728\u773c\u524d\u3002",
      "\u95e8\u524d\u6eaa\u6c34\u6e10\u6da8\uff0c\u60f3\u662f\u5c71\u96ea\u6d88\u878d\u4e86\u3002\u4ece\u524d\u8fd9\u65f6\u5019\uff0c\u603b\u8981\u5e2e\u7740\u5bb6\u91cc\u6311\u6c34\u6d47\u83dc\u3002",
      "\u6e05\u660e\u8fc7\u4e86\uff0c\u8be5\u662f\u63d2\u79e7\u65f6\u8282\u3002\u4e0d\u77e5\u5bb6\u4e2d\u7530\u91cc\uff0c\u4eca\u5e74\u79e7\u82d7\u53ef\u58ee\uff1f",
      "\u6625\u96e8\u7ef5\u7ef5\uff0c\u591c\u6df1\u4eba\u9759\u65f6\u603b\u80fd\u542c\u89c1\u5c4b\u5916\u6ef4\u7b54\u58f0\u2014\u2014\u50cf\u6781\u4e86\u8001\u5c4b\u5929\u4e95\u7684\u96e8\u58f0\u3002",
      "\u71d5\u5b50\u5df2\u5f52\uff0c\u8857\u8fb9\u6728\u68c9\u82b1\u843d\u4e86\u4e00\u5730\u3002\u5e74\u5e74\u6b64\u666f\uff0c\u53ea\u662f\u4eba\u5df2\u4e0d\u5728\u5bb6\u4e2d\u4e86\u3002",
    ],
    "\u590f": [
      "\u591c\u77ed\u663c\u957f\uff0c\u8749\u9e23\u4e0d\u6b62\u3002\u60f3\u8d77\u4ece\u524d\u590f\u591c\u91cc\uff0c\u5728\u9662\u4e2d\u7eb3\u51c9\u7684\u6a21\u6837\uff0c\u81f3\u4eca\u96be\u5fd8\u3002",
      "\u6691\u6c14\u84b8\u4eba\uff0c\u767d\u65e5\u91cc\u8fde\u98ce\u90fd\u662f\u70ed\u7684\u3002\u8bb0\u5f97\u5728\u5bb6\u65f6\uff0c\u603b\u6709\u4e00\u7897\u51c9\u8336\u89e3\u6691\u3002",
      "\u8fd9\u51e0\u65e5\u5348\u540e\u5e38\u4e0b\u96f7\u96e8\uff0c\u8f70\u9686\u58f0\u4e2d\u603b\u60f3\u8d77\u4ece\u524d\u5728\u8001\u5c4b\u5c4b\u6a90\u4e0b\u7b49\u96e8\u505c\u7684\u65e5\u5b50\u3002",
      "\u8354\u679d\u7ea2\u4e86\uff0c\u8857\u8fb9\u5df2\u6709\u4eba\u53eb\u5356\u3002\u60f3\u8d77\u5bb6\u4e61\u90a3\u68f5\u8001\u8354\u679d\u6811\uff0c\u4e0d\u77e5\u4eca\u5e74\u6302\u679c\u5982\u4f55\u3002",
      "\u868a\u866b\u6e10\u591a\u4e86\uff0c\u591c\u91cc\u8981\u70b9\u868a\u9999\u2014\u2014\u8fd9\u6c14\u5473\u5012\u8ba9\u6211\u60f3\u8d77\u4ece\u524d\u9601\u697c\u4e0a\u7684\u590f\u5929\u3002",
      "\u5357\u98ce\u6e29\u70ed\uff0c\u5439\u5f97\u4eba\u660f\u660f\u6b32\u7761\u3002\u60f3\u8d77\u4ece\u524d\u590f\u591c\uff0c\u8eba\u5728\u7af9\u5e2d\u4e0a\u542c\u963f\u5b37\u8bb2\u6545\u4e8b\u3002",
    ],
    "\u79cb": [
      "\u68a7\u6850\u53f6\u843d\uff0c\u79cb\u98ce\u4e00\u9635\u7d27\u4f3c\u4e00\u9635\u3002\u60f3\u8d77\u5bb6\u4e2d\u6842\u82b1\uff0c\u6b64\u65f6\u8be5\u662f\u6ee1\u6811\u91d1\u9ec4\u4e86\u3002",
      "\u5929\u9ad8\u4e91\u6de1\uff0c\u96c1\u9635\u5357\u98de\u3002\u770b\u89c1\u5927\u96c1\uff0c\u4fbf\u60f3\u8d77\u2018\u96c1\u5b57\u56de\u65f6\u6708\u6ee1\u897f\u697c\u2019\u7684\u53e5\u5b50\u6765\u3002",
      "\u8fd9\u51e0\u65e5\u79cb\u51c9\u5165\u9aa8\uff0c\u65e9\u8d77\u5df2\u8981\u62ab\u4ef6\u8584\u886b\u3002\u4e0d\u77e5\u5bb6\u4e2d\u53ef\u66fe\u6dfb\u8863\uff1f",
      "\u4e2d\u79cb\u5c06\u8fd1\uff0c\u6708\u6e10\u5706\u6ee1\u3002\u60f3\u8d77\u4ece\u524d\u4e00\u5bb6\u4eba\u5750\u5728\u9662\u4e2d\u5206\u6708\u997c\u7684\u5149\u666f\uff0c\u4e0d\u7981\u6cea\u4e0b\u3002",
      "\u98ce\u8d77\u65f6\u68a7\u6850\u53f6\u7c0c\u7c0c\u5730\u54cd\u2014\u2014\u8fd9\u58f0\u97f3\u603b\u8ba9\u6211\u60f3\u8d77\u79bb\u5bb6\u90a3\u5929\u7684\u6e05\u6668\u3002",
      "\u83ca\u82b1\u5f00\u4e86\uff0c\u8857\u5e02\u4e0a\u6709\u4eba\u53eb\u5356\u3002\u8bb0\u5f97\u6bcf\u5e74\u79cb\u5929\uff0c\u5bb6\u91cc\u603b\u8981\u6652\u4e9b\u83ca\u82b1\u6ce1\u8336\u3002",
    ],
    "\u51ac": [
      "\u5929\u5bd2\u5730\u51bb\uff0c\u60f3\u8d77\u5bb6\u4e2d\u7076\u5934\u7684\u6e29\u6696\uff0c\u56f4\u7089\u716e\u8336\u7684\u5149\u666f\uff0c\u604d\u5982\u6628\u65e5\u3002",
      "\u8fd9\u51e0\u65e5\u51b7\u5f97\u5389\u5bb3\uff0c\u65e9\u8d77\u7a97\u4e0a\u90fd\u7ed3\u4e86\u971c\u82b1\u3002\u8bb0\u5f97\u4ece\u524d\u51ac\u65e5\uff0c\u963f\u5b37\u603b\u628a\u6211\u7684\u624b\u6342\u5728\u5979\u6000\u91cc\u6696\u3002",
      "\u814a\u6708\u5df2\u81f3\uff0c\u5e74\u5173\u5c06\u8fd1\u3002\u60f3\u8d77\u5bb6\u4e2d\u8be5\u662f\u5fd9\u7740\u84b8\u5e74\u7cd5\u3001\u505a\u7ea2\u6843\u7cbf\u4e86\u3002",
      "\u5317\u98ce\u5982\u5200\uff0c\u5439\u5f97\u4eba\u9aa8\u5934\u90fd\u51b7\u3002\u4e0d\u77e5\u5bb6\u4e2d\u8001\u5c0f\u53ef\u6709\u7a7f\u6696\uff1f",
      "\u591c\u6df1\u98ce\u5bd2\uff0c\u72ec\u81ea\u5bf9\u7740\u6cb9\u706f\u5199\u5b57\uff0c\u4fbf\u60f3\u8d77\u4ece\u524d\u4e00\u5bb6\u4eba\u56f4\u5750\u706f\u4e0b\u7684\u60c5\u666f\u3002",
      "\u51ac\u81f3\u5df2\u8fc7\uff0c\u65e5\u5934\u6e10\u957f\u3002\u60f3\u8d77\u5bb6\u4e2d\u51ac\u81f3\u7684\u6c64\u5706\uff0c\u751c\u7cef\u7684\u6ecb\u5473\u81f3\u4eca\u8bb0\u5f97\u3002",
    ],
  },

  // --- 季节关心（每季4选1，原每季1） ---
  careSeason: {
    "\u6625": [
      "\u6625\u5bd2\u672a\u6d88\uff0c\u671b\u591a\u52a0\u8863\u88f3\u3002",
      "\u4e4d\u6696\u8fd8\u5bd2\u65f6\u5019\uff0c\u6700\u6613\u4f24\u98ce\uff0c\u52a1\u5fc5\u7559\u610f\u3002",
      "\u6625\u96e8\u6e7f\u51b7\uff0c\u51fa\u95e8\u8bb0\u5f97\u5e26\u4f1e\u6dfb\u8863\u3002",
      "\u6625\u6342\u79cb\u51bb\uff0c\u83ab\u6025\u7740\u51cf\u8863\u886b\u3002",
    ],
    "\u590f": [
      "\u6691\u6c14\u903c\u4eba\uff0c\u996e\u98df\u5b9c\u6e05\u6de1\uff0c\u5207\u8bb0\u907f\u6691\u3002",
      "\u4e09\u4f0f\u5929\u91cc\uff0c\u5348\u65f6\u83ab\u5728\u65e5\u5934\u4e0b\u4e45\u7ad9\uff0c\u591a\u559d\u51c9\u8336\u3002",
      "\u5929\u6c14\u708e\u70ed\uff0c\u996d\u83dc\u83ab\u9694\u591c\uff0c\u5f53\u5fc3\u5403\u574f\u809a\u5b50\u3002",
      "\u65e5\u5934\u6bd2\u8fa3\uff0c\u51fa\u95e8\u6234\u9876\u8349\u5e3d\uff0c\u522b\u6652\u51fa\u75c5\u6765\u3002",
    ],
    "\u79cb": [
      "\u79cb\u98ce\u6e10\u8d77\uff0c\u65e9\u665a\u6dfb\u8863\u3002",
      "\u5929\u5e72\u7269\u71e5\uff0c\u591a\u559d\u6c64\u6c34\uff0c\u6da6\u80ba\u9632\u54b3\u3002",
      "\u79cb\u51c9\u5982\u6c34\uff0c\u591c\u91cc\u8bb0\u5f97\u76d6\u597d\u88ab\u5b50\u3002",
      "\u4e00\u5c42\u79cb\u96e8\u4e00\u5c42\u51c9\uff0c\u51fa\u95e8\u591a\u5e26\u4ef6\u886b\u3002",
    ],
    "\u51ac": [
      "\u5929\u6c14\u5bd2\u51b7\uff0c\u52a1\u5fc5\u6dfb\u8863\u5fa1\u5bd2\uff0c\u5207\u52ff\u53d7\u51c9\u3002",
      "\u5bd2\u51ac\u814a\u6708\uff0c\u522b\u7701\u90a3\u70b9\u70ad\u706b\u94b1\uff0c\u8eab\u5b50\u8981\u7d27\u3002",
      "\u6570\u4e5d\u5bd2\u5929\uff0c\u65e9\u8d77\u83ab\u6025\u7740\u51fa\u95e8\uff0c\u7b49\u65e5\u5934\u51fa\u6765\u518d\u8bf4\u3002",
      "\u624b\u811a\u6613\u51bb\uff0c\u7761\u524d\u7528\u70ed\u6c34\u6ce1\u6ce1\u811a\uff0c\u591c\u91cc\u597d\u7761\u4e9b\u3002",
    ],
  },

  // --- 关心收尾（7选1，原1） ---
  careClosing: [
    "\u5bb6\u4e2d\u5927\u5c0f\u4e8b\u52a1\uff0c\u91cf\u529b\u800c\u884c\u4fbf\u662f\uff0c\u5207\u52ff\u8fc7\u52b3\u3002",
    "\u51e1\u4e8b\u5bbd\u5fc3\u4e3a\u4e0a\uff0c\u83ab\u4e3a\u7410\u4e8b\u70e6\u607c\u3002\u5bb6\u4e2d\u5b89\u5b81\uff0c\u513f\u5728\u5916\u4fbf\u5fc3\u5b89\u3002",
    "\u5bb6\u4e2d\u8001\u5c0f\uff0c\u5404\u81ea\u73cd\u91cd\u3002\u7c97\u8336\u6de1\u996d\u4e5f\u662f\u798f\uff0c\u4e0d\u5fc5\u592a\u8fc7\u64cd\u52b3\u3002",
    "\u7530\u5730\u91cc\u7684\u6d3b\u8ba1\uff0c\u80fd\u505a\u591a\u5c11\u4fbf\u505a\u591a\u5c11\uff0c\u4e0d\u8981\u786c\u6491\u3002",
    "\u94b1\u8d22\u8eab\u5916\u4e4b\u7269\uff0c\u5e73\u5b89\u624d\u662f\u771f\u3002\u82e5\u662f\u7d2f\u7740\u4e86\uff0c\u518d\u591a\u7684\u94b1\u53c8\u6709\u4f55\u7528\u3002",
    "\u5bb6\u91cc\u7684\u4e8b\uff0c\u653e\u5bbd\u5fc3\u4e9b\u3002\u65e5\u5b50\u8fc7\u5f97\u53bb\u4fbf\u597d\uff0c\u4e0d\u5fc5\u4e0e\u4eba\u6bd4\u8f83\u3002",
    "\u67f4\u7c73\u6cb9\u76d0\u7684\u4e8b\uff0c\u7701\u7740\u70b9\u7528\u4fbf\u662f\uff0c\u4e0d\u5fc5\u592a\u8282\u4fed\uff0c\u8be5\u82b1\u5c31\u82b1\u3002",
  ],

  // --- 收尾寄语（按心情分类，共30+条，原8条） ---
  endings: {
    homesick: [
      "\u6c5f\u6d77\u4e07\u91cc\uff0c\u5fc3\u6709\u6240\u5bc4\uff0c\u4fbf\u4e0d\u89c9\u8fdc\u3002",
      "\u4e0d\u77e5\u4f55\u65e5\u5f97\u5f52\u6545\u91cc\uff0c\u4e0e\u4eb2\u4eba\u5171\u53d9\u5929\u4f26\u3002",
      "\u6bcf\u9022\u4f73\u8282\u500d\u601d\u4eb2\uff0c\u53ea\u662f\u8c0b\u751f\u5728\u5916\uff0c\u8eab\u4e0d\u7531\u5df1\u3002",
      "\u5e74\u5e74\u671b\u5f52\uff0c\u5c81\u5c81\u5728\u5916\u3002\u53ea\u76fc\u6765\u5e74\uff0c\u80fd\u4e0e\u5bb6\u4eba\u56e2\u805a\u3002",
      "\u591c\u6df1\u4eba\u9759\uff0c\u5bf9\u6708\u72ec\u5750\uff0c\u5343\u8a00\u4e07\u8bed\uff0c\u4e0d\u77e5\u4ece\u4f55\u8bf4\u8d77\u3002",
      "\u8def\u8fdc\u8fe2\u8fe2\uff0c\u5f52\u671f\u96be\u5b9a\u3002\u552f\u613f\u5bb6\u4e2d\u5e73\u5b89\uff0c\u4fbf\u662f\u6700\u5927\u5b89\u6170\u3002",
    ],
    worried: [
      "\u8eab\u5728\u5f02\u4e61\uff0c\u65e5\u591c\u5fc3\u5ff5\u5bb6\u4e2d\u4eba\u4e8b\u3002\u76fc\u6765\u4fe1\u544a\u77e5\u8fd1\u51b5\uff0c\u4ee5\u91ca\u8fdc\u5ff5\u3002",
      "\u6bcf\u5ff5\u53ca\u5bb6\u4e2d\uff0c\u5fc3\u4fbf\u60ac\u7740\u3002\u4f46\u613f\u8fd1\u65e5\u6709\u4fe1\u6765\u62a5\u5e73\u5b89\u3002",
      "\u51fa\u95e8\u5728\u5916\uff0c\u6700\u653e\u4e0d\u4e0b\u7684\u4fbf\u662f\u5bb6\u4e2d\u8001\u5c0f\u3002\u671b\u5e38\u6765\u4fe1\u3002",
      "\u591c\u6df1\u96be\u5bd0\uff0c\u8f97\u8f6c\u53cd\u4fa7\uff0c\u60f3\u7684\u90fd\u662f\u5bb6\u4e2d\u7684\u4e8b\u3002\u613f\u4e00\u5207\u5b89\u597d\u3002",
      "\u8fd1\u6765\u603b\u68a6\u89c1\u56de\u5bb6\uff0c\u9192\u6765\u540e\u5fc3\u7eea\u96be\u5e73\u3002\u76fc\u5bb6\u4e2d\u8bf8\u4e8b\u987a\u9042\u3002",
    ],
    normal: [
      "\u5c81\u6708\u5306\u5306\uff0c\u552f\u613f\u4eb2\u4eba\u5b89\u7a33\uff0c\u5c81\u5c81\u5982\u5e38\u3002",
      "\u5317\u9e3f\u5357\u96c1\uff0c\u4e0d\u65ad\u97f3\u4e66\uff0c\u5fc3\u5b89\u4fbf\u597d\u3002",
      "\u518d\u62dc\u8bf7\u5b89\uff0c\u4f59\u8a00\u4e0d\u53ca\u3002",
      "\u7eb8\u77ed\u60c5\u957f\uff0c\u8a00\u4e0d\u5c3d\u610f\u3002\u613f\u5bb6\u4e2d\u4e00\u5207\u5b89\u597d\u3002",
      "\u65e5\u5934\u897f\u659c\uff0c\u5c31\u6b64\u6401\u7b14\u3002\u4e0b\u6b21\u518d\u591a\u5199\u4e9b\u3002",
      "\u591c\u5df2\u6df1\u6c89\uff0c\u660e\u65e5\u8fd8\u8981\u65e9\u8d77\uff0c\u5c31\u6b64\u6b47\u7b14\u3002",
      "\u8bf8\u4e8b\u987a\u9042\uff0c\u52ff\u4ee5\u4e3a\u5ff5\u3002\u4ed6\u65e5\u5f97\u95f2\uff0c\u518d\u7eed\u97f3\u4e66\u3002",
    ],
    money: [
      "\u4ed6\u65e5\u82e5\u6709\u4f59\u8d44\uff0c\u5f53\u518d\u5bc4\u4ed8\u3002",
      "\u4e0b\u6708\u82e5\u662f\u5bbd\u88d5\uff0c\u518d\u591a\u5bc4\u4e9b\u56de\u53bb\u3002",
      "\u624b\u5934\u7565\u7d27\uff0c\u5bb9\u540e\u518d\u5bc4\u3002\u671b\u8c05\u3002",
    ],
    newsy: [
      "\u8fd1\u65e5\u57ce\u91cc\u6709\u4e9b\u65b0\u9c9c\u4e8b\uff0c\u4e0b\u6b21\u518d\u8be6\u8bf4\u3002",
      "\u8857\u574a\u90bb\u5c45\u90fd\u5ff5\u7740\u4f60\u4eec\uff0c\u6258\u6211\u4ee3\u4e3a\u95ee\u597d\u3002",
      "\u540c\u4e61\u738b\u5148\u751f\u8fd1\u65e5\u8fd4\u4e61\uff0c\u6258\u4ed6\u5e26\u4e86\u4e9b\u4e1c\u897f\u56de\u53bb\u3002",
    ],
  },

  // --- 附言池（35%概率追加） ---
  postscripts: [
    "\u53c8\u53ca\uff1a\u90bb\u5bb6\u963f\u5a76\u6258\u6211\u95ee\u5019\u5bb6\u4e2d\u8001\u5c0f\u3002",
    "\u53c8\u53ca\uff1a\u5bc4\u56de\u7684\u5e03\u6599\uff0c\u7ed9\u963f\u5b37\u505a\u4ef6\u65b0\u886b\u3002",
    "\u53c8\u53ca\uff1a\u4e0a\u6b21\u5bc4\u7684\u836f\u54c1\uff0c\u4e0d\u77e5\u53ef\u66fe\u6536\u5230\uff1f",
    "\u53c8\u53ca\uff1a\u8fc7\u5e74\u7684\u4e8b\uff0c\u5bb9\u540e\u518d\u8bae\u3002\u6b64\u523b\u5148\u62a5\u5e73\u5b89\u3002",
    "\u518d\u542f\uff1a\u8fd1\u65e5\u6e2f\u53e3\u67e5\u9a8c\u751a\u4e25\uff0c\u5bc4\u7269\u6050\u6709\u5ef6\u8bef\uff0c\u671b\u8010\u5fc3\u7b49\u5019\u3002",
    "\u518d\u542f\uff1a\u82e5\u6709\u540c\u4e61\u8fd4\u4e61\uff0c\u5b9a\u6258\u4ed6\u4eec\u634e\u4e9b\u4e1c\u897f\u56de\u53bb\u3002",
  ],
};

// ---- 辅助：从池中按种子选一条（避免 Math.random 的非确定性） ----
function pickFrom(pool, seed) {
  return pool[Math.floor(textSeed(seed) * pool.length)];
}

// ---- 七段式动态模板 v46（扩池 + 结构变体） ----
function buildLetter(info, rawText) {
  var who = info.rel.who;
  var sign = info.rel.sign;
  var T = TEMPLATES;
  var parts = [];

  // ====== 第一段：称呼问安（6选1） ======
  var seedBase = rawText.charAt(0) + rawText.charAt(rawText.length - 1);
  var opening = pickFrom(T.openings, seedBase + "op").replace("{who}", who);
  parts.push(opening);

  // ====== 第二段：寄银交代 ======
  if (info.hasMoney) {
    if (info.moneyAmount) {
      parts.push("\u8c28\u5bc4\u4e0a" + info.moneyAmount + "\uff0c\u7948\u4e3a\u67e5\u6536\u3002");
    } else {
      parts.push("\u968f\u4fe1\u5bc4\u5165\u4e9b\u8bb8\u94f6\u8d44\uff0c\u7948\u4e3a\u7b11\u7eb3\u3002");
    }
    parts.push(pickFrom(T.moneyFollowup, seedBase + "mf"));
  } else {
    parts.push(pickFrom(T.noMoney, seedBase + "nm"));
  }

  // ====== 第三段：自述近况（4选1状态行模板） ======
  var locationPart = info.locationExtra && info.locationExtra !== "\u5916\u4e61"
    ? info.locationExtra : "\u5916\u4e61";
  var workPart = info.workDesc || "\u8bf8\u4e8b\u52c9\u53ef\u5e94\u4ed8";
  var healthPart = info.health;
  var stTmpl = pickFrom(T.statusLine, seedBase + "st");
  var statusLine = stTmpl.replace("{loc}", locationPart)
                         .replace("{work}", workPart)
                         .replace("{health}", healthPart);
  parts.push(statusLine);

  // ====== 第四段：借景思乡 / 具体回忆 ======
  var weatherPrefix = "";
  if (info.weather === "rain") weatherPrefix = "\u8fd1\u6765\u8fde\u65e5\u96e8\u6c34\uff0c";
  else if (info.weather === "hot") weatherPrefix = "\u8fd1\u6765\u5929\u6c14\u708e\u70ed\uff0c";
  else if (info.weather === "cold") weatherPrefix = "\u5929\u6c14\u6e10\u5bd2\uff0c";
  else if (info.weather === "windy") weatherPrefix = "\u8fd1\u65e5\u98ce\u52bf\u8f83\u5927\uff0c";

  if (info.memoryText) {
    // 用户提到具体回忆 → 保留
    var memConverted = convertSentence(info.memoryText);
    parts.push(weatherPrefix + memConverted);
  } else {
    // 从季节池中选（6选1，原1）
    var season = info.season || "\u6625";
    var nosPool = T.nostalgia[season] || T.nostalgia["\u6625"];
    var nosText = pickFrom(nosPool, seedBase + "nos");
    var seasonLabels = {
      "\u6625": "\u6625\u5bd2\u6599\u5ced", "\u590f": "\u6691\u6c14\u6e10\u76db",
      "\u79cb": "\u79cb\u610f\u6e10\u6d53", "\u51ac": "\u5bd2\u610f\u6e10\u6df1",
    };
    var seasonLabel = seasonLabels[season] || "\u65f6\u4ee4\u66ff\u66f4";
    parts.push(weatherPrefix + seasonLabel + "\uff0c" + nosText);
  }

  // ====== 第五段：叮嘱保重 ======
  var careLines = [];
  var carePool = T.careSeason[info.season] || T.careSeason["\u6625"];
  careLines.push(pickFrom(carePool, seedBase + "cs"));

  // 用户具体关心的内容（仅纳入转换后有效的，最多2条）
  if (info.concernItems.length > 0) {
    var addedConcerns = 0;
    for (var cii = 0; cii < info.concernItems.length && addedConcerns < 2; cii++) {
      var ccConverted = convertSentence(info.concernItems[cii]);
      // 跳过转换后仍含问号或太短的
      if (ccConverted && ccConverted.length >= 3 && !/\uff1f|\u5417/.test(ccConverted)) {
        var cleaned = ccConverted.replace(/[\uff0c\u3002\uff01\uff1f\u3001]$/, "");
        // 避免重复已有关心内容
        var alreadyHave = false;
        for (var j = 0; j < careLines.length; j++) {
          if (careLines[j].indexOf(cleaned) >= 0 || cleaned.indexOf(careLines[j]) >= 0) {
            alreadyHave = true; break;
          }
        }
        if (!alreadyHave) {
          careLines.push(cleaned);
          addedConcerns++;
        }
      }
    }
  }

  // 交替合并：季节关心 + 用户关心 → 自然段落
  // 如果只有季节关心 → 单句；如果有用户关心 → "季节关心，用户关心一。用户关心二。"
  var careText = "";
  if (careLines.length === 1) {
    careText = careLines[0] + "\u3002";
  } else {
    // 多条时：第一条用"，"连接，后续各自成句
    careText = careLines[0] + "\uff0c";
    for (var cli = 1; cli < careLines.length; cli++) {
      careText += careLines[cli] + "\u3002";
    }
  }
  // 关心收尾（7选1，原固定）
  careText += pickFrom(T.careClosing, seedBase + "cc");
  parts.push(careText);

  // ====== 第六段：收尾寄语 ======
  var mood = "normal";
  if (info.healthType === "sick" || info.healthType === "tired" || info.workType === "hard")
    mood = "worried";
  else if (info.memories.length >= 2)
    mood = "homesick";
  else if (info.hasMoney && info.news.length === 0)
    mood = "money";
  else if (info.news.length > 0 && textSeed(seedBase + "md") > 0.5)
    mood = "newsy";
  else if (textSeed(seedBase + "md2") > 0.6)
    mood = "homesick";  // 偶尔走思乡风（增加多样性）

  var endingsPool = T.endings[mood] || T.endings["normal"];
  parts.push(pickFrom(endingsPool, seedBase + "end" + mood));

  // ====== 结构变体：35%概率加附言 ======
  if (textSeed(seedBase + "ps") < 0.35) {
    parts.push(pickFrom(T.postscripts, seedBase + "pst"));
  }

  // ====== 第七段：落款 ======
  parts.push(sign);

  return parts.join("\n");
}


// 基于文本生成确定性"随机数"
function textSeed(str) {
  var h = 0;
  for (var i = 0; i < str.length; i++) {
    h = ((h << 5) - h) + str.charCodeAt(i);
    h |= 0;
  }
  return Math.abs(h) / 2147483648;
}

// ---- 主转换入口 ----
function toQiaopi(raw) {
  var text = raw.trim();
  if (!text) return "";
  var info = extractAllInfo(text);
  return buildLetter(info, text);
}

/* ================================================================
   Canvas 渲染引擎 — 纯前端，无需外部依赖
   ================================================================ */

function renderToCanvas(qiaopiText, fontSize, charsCol) {
  var canvas = document.createElement("canvas");
  canvas.width = bgDims.w;
  canvas.height = bgDims.h;
  var ctx = canvas.getContext("2d");

  // 1. 绘制底图
  if (bgReady) {
    ctx.drawImage(bgImage, 0, 0, bgDims.w, bgDims.h);
  } else {
    ctx.fillStyle = "#f5f0e6";
    ctx.fillRect(0, 0, bgDims.w, bgDims.h);
  }

  // 2. 设置文字样式
  var textH = bgDims.h - bgDims.textTop - bgDims.textBottom;
  var mpc = Math.floor(textH / fontSize);
  var actualCols = Math.min(charsCol, mpc);

  ctx.font = fontSize + 'px "KaiTi","楷体","STKaiti",serif';
  ctx.fillStyle = "#2a1810";
  ctx.textAlign = "center";
  ctx.textBaseline = "top";

  // 3. 逐字竖排绘制（从右到左）
  var cleanText = qiaopiText.replace(/\r?\n/g, "");
  var totalCap = bgDims.cols * actualCols;
  if (cleanText.length > totalCap) cleanText = cleanText.substring(0, totalCap);

  var textTop = bgDims.textTop;
  var blockedStart = Math.floor((PHOTO.top_y - textTop) / fontSize);
  var blockedEnd = Math.floor((PHOTO.bottom_y - textTop) / fontSize);

  for (var ci = 0; ci < bgDims.cols; ci++) {
    var startIdx = ci * actualCols;
    if (startIdx >= cleanText.length) break;
    var colChars = cleanText.substring(startIdx, startIdx + actualCols);
    var center = COL_CENTERS[ci] || 0;

    var colL = center - fontSize / 2;
    var colR = center + fontSize / 2;
    var inPhotoX = (colR > PHOTO.left && colL < PHOTO.right);

    for (var si = 0; si < colChars.length; si++) {
      if (inPhotoX && si >= blockedStart && si <= blockedEnd) continue;
      var x = center;
      var y = textTop + si * fontSize;
      ctx.fillText(colChars[si], x, y);
    }
  }

  return canvas;
}

// ========== 研墨成笺 ==========
function doGenerate() {
  var raw = ta.value.trim();
  if (!raw) { ta.focus(); showToast("\u8bf7\u5148\u5199\u4e0b\u4f60\u60f3\u8bf4\u7684\u8bdd", "error"); return; }

  btnGen.disabled = true;
  btnGen.textContent = "\u7814\u58a8\u4e2d\u2026";
  btnGen.classList.add("loading");
  resultSec.classList.remove("show");
  toast.classList.remove("show");

  try {
    // 1. 白话 → 侨批文体
    var qiaopi = toQiaopi(raw);
    ta.value = qiaopi;
    updateCap();

    // 2. Canvas 渲染
    var f = +fs.value, c = +cc.value;
    function doCanvasRender() {
      var canvas = renderToCanvas(qiaopi, f, c);
      if (_blobUrl) URL.revokeObjectURL(_blobUrl);
      var dataUrl = canvas.toDataURL("image/png");
      document.getElementById("outImg").src = dataUrl;
      resultSec.classList.add("show");
      canvas.toBlob(function(b) { _blobUrl = URL.createObjectURL(b); }, "image/png");
      finishGenerate();
    }

    function finishGenerate() {
      btnGen.disabled = false;
      btnGen.textContent = "\u7814\u58a8\u6210\u7b3a";
      btnGen.classList.remove("loading");

      // 字数超限提醒
      var textH = bgDims.h - bgDims.textTop - bgDims.textBottom;
      var mpc = Math.floor(textH / f), ac = Math.min(c, mpc);
      var cap = bgDims.cols * ac;
      var cleanLen = qiaopi.replace(/\r?\n/g, "").length;
      if (cleanLen > cap) {
        showToast("\u4fe1\u7b3a\u4ec5\u5bb9 " + cap + " \u5b57\uff0c\u5c3e\u90e8 " + (cleanLen - cap) + " \u5b57\u5df2\u622a\u65ad\u3002\u51cf\u5c0f\u5b57\u53f7\u53ef\u5bb9\u7eb3\u66f4\u591a\u3002", "info");
      }
    }

    // 随机切换底图后渲染（三底图每次不同）
    loadRandomBGThen(function() {
      // 即使加载失败也渲染（灰色背景兜底）
      doCanvasRender();
    });
  } catch (e) {
    finishGenerate();
    showToast("\u751f\u6210\u5931\u8d25\uff1a" + e.message, "error");
  }
}

function doDownload() {
  if (_blobUrl) {
    var a = document.createElement("a");
    a.href = _blobUrl;
    a.download = "侨批信笺_" + new Date().toISOString().slice(0,10) + ".png";
    a.click();
  }
}

function doReset() {
  resultSec.classList.remove("show");
  toast.classList.remove("show");
  ta.value = "";
  ta.focus();
  updateCap();
  if (_blobUrl) { URL.revokeObjectURL(_blobUrl); _blobUrl = null; }
}

function showToast(msg, type) {
  toast.textContent = msg;
  toast.className = "toast toast-" + (type || "info") + " show";
  var delay = (type === "error") ? 8000 : 5000;
  setTimeout(function() { toast.classList.remove("show"); }, delay);
}

ta.addEventListener("keydown", function(e) {
  if (e.ctrlKey && e.key === "Enter") doGenerate();
});
"""

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>潮汕侨批信笺</title>
<style>
""" + CSS + """\
</style>
</head>
<body>
<div class="topbar">潮汕侨批信笺 &mdash; 一字一泪 &middot; 万里传情</div>
<div class="container">
  <div class="header">
    <div class="seal-mark">侨批</div>
    <h1>潮汕侨批信笺</h1>
    <div class="subtitle">一字一泪 &middot; 万里传情</div>
  </div>
  <div class="card" id="writeCard">
      <div class="card-label">书写</div>
      <textarea id="ta" placeholder="用大白话写下你想说的话……&#10;例如：奶奶我好想你，最近总想起小时候的事。我在外面挺好的。寄了点钱回家"></textarea>
      <div class="char-stat">
        <span>已书 <b id="charCnt">0</b> 字</span>
        <div class="bar-wrap"><div class="bar-inner bar-ok" id="capBar" style="width:0%"></div></div>
        <span>信笺容量 <b id="capNum">297</b> 字</span>
      </div>
      <div class="param-row">
        <div class="param">
          <label>字号 <span class="val" id="fsv">52</span></label>
          <input type="range" id="fs" min="28" max="80" value="52" step="1">
          <div class="desc">字小则多言，字大则气足</div>
        </div>
        <div class="param">
          <label>每列字数 <span class="val" id="cv">27</span></label>
          <input type="range" id="cc" min="10" max="32" value="27" step="1">
          <div class="desc">十一列竖排，从右至左</div>
        </div>
      </div>
      <div class="btn-row">
        <button class="btn btn-gen" id="btnGen" onclick="doGenerate()">研墨成笺</button>
      </div>
    </div>
    <div class="result-section" id="resultSec">
      <div class="card result-wrap">
        <img id="outImg" src="" alt="侨批信笺">
        <div class="result-btns">
          <button class="btn-dl" onclick="doDownload()">保存信笺</button>
          <button class="btn-re" onclick="doReset()">再写一封</button>
        </div>
      </div>
    </div>
  <div class="toast toast-info" id="toast"></div>
  <div class="footer">
    潮汕侨批 &middot; 非物质文化遗产
    <span class="sep">|</span>
    双击 HTML 即用，无需安装
  </div>
</div>
<script>
""" + bg_uris_js + """
</script>
<script>
""" + JS_CORE + """
</script>
</body>
</html>"""

out_path = r"C:\Users\EDY\WorkBuddy\20260601100602\qiaopi-demo.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(HTML_TEMPLATE)

size_mb = len(HTML_TEMPLATE.encode("utf-8")) / (1024 * 1024)
print(f"Written: {out_path} ({size_mb:.2f} MB)")
print("v44 Done — 输入差异化文本转换引擎")
