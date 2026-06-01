---
name: chaoshan-qiaopi
description: 将任意输入文本转换为《给阿嫲的情书》同款潮汕传统侨批（南洋家书）风格书信，并生成一张传统信笺图片。技能名称「潮汕侨批书写馆」。当用户要求用旧式家书、侨批、南洋家书、给阿嬷/阿嫲的情书等风格书写，或需要生成传统手写信笺图片时触发。
---

# 潮汕侨批书写馆 (chaoshan-qiaopi)

将用户输入的任意内容，转化为白话文言结合的潮汕传统侨批风格书信，并渲染为一张传统信笺图片（HTML渲染 → PNG/JPG）。

## 工作流程

### 第一步：生成侨批书信正文

严格遵循以下写作铁律，将用户输入转化为侨批文体：

**写作铁律（硬性规则）：**

1. **文风**：民国末、建国后老式家书口吻，白话文言结合，朴素、温柔、隐忍、克制，不煽情、不鸡汤、不现代词。
2. **结构顺序绝对不能乱**：称呼问好 → 告知寄银钱款 → 自身报平安 → 家中近况/细碎小事思念 → 叮嘱保重 → 收尾寄语 → 落款。
3. **侨批本质：先银、后情**。正文第一段事务必须先交代汇款（即使金额为"薄资些许，聊补家用"），这是侨批灵魂。
4. **永远报喜不报忧**：在外辛苦、磨难、委屈一律不写，只写顺遂、平安、尚可。
5. **思念不直白**：不说"我想你""我爱你"，只用景物、时节、家常小事寄托想念。
6. **句式短句干净**，有年代纸质信的停顿感，不冗长、不排比、不文艺过度。
7. **自动适配关系**：夫妻、祖孙、亲子、亲人皆可，自动匹配称谓。
8. **禁止出现**：网络词、现代口语、书面八股、空洞大话。

**固定金句库（按需融入，不堆砌）：**
- 江海万里，心有所寄，便不觉远。
- 身在异乡，日夜心念家中人事。
- 诸事尚可，身体安稳，勿劳挂念。
- 家中大小平安，便是人间圆满。
- 岁月匆匆，唯愿亲人安稳，岁岁如常。

**标准结构模板：**

1. **开头**：专属旧式称谓 + 展信安好/展信佳
2. **首段**：明确写出「随信寄入XX钱款，祈为查收」（无则写"薄资些许，聊补家用"）
3. **二段**：自述在外近况，平安顺遂，不报忧
4. **三段**：由时节、风物、小事牵起思念（最核心氛围感段落）
5. **四段**：叮嘱家人保重身体、勿操劳、放宽心
6. **结尾**：一句简短侨批式收尾寄语
7. **落款**：身份 + 字（例：夫XX字、孙XX谨书）

**关系称谓自动适配：**

| 关系 | 称谓示例 |
|------|---------|
| 祖孙 | 阿嬷、阿公、阿祖、嬷嬷 |
| 亲子 | 母亲、父亲、吾娘、吾父 |
| 夫妻 | 娘子、夫君、吾妻、拙夫 |
| 亲人 | 家中老小、诸亲、长辈 |

详细模板、金句库、范例信件 → 参见 [references/style-guide.md](references/style-guide.md)

### 第二步：渲染为传统信笺图片（HTML → PNG/JPG）

**渲染脚本**：`scripts/render-qiaopi.js`（当前版本：v24）

**执行方式：**
```bash
node scripts/render-qiaopi.js --text "书信正文..." --output output.png [--format png|jpg] [--fontSize 52] [--cols 28]
```

**渲染特性：**
- **背景**：《阿嫲情书》侨批信笺原图（1773x2364，JPG），带8条红栏线 + 传统圆形印章
- **字体**：本地嵌入 simkai/simfang/simsun 三级回退（base64 内嵌，无需联网）
- **字体大小**：默认 52px（可调 `--fontSize`），每列自动适配纸面高度
- **列数**：默认 28 字/列，8 列竖排从右至左阅读，总容量 224 字
- **溢出防护**：超长文字在渲染前自动截断并提示（v24 前置截断机制）
- **输出**：PNG（默认）或 JPG

**前置要求：**
- 系统需要 Edge 浏览器（脚本使用 `puppeteer-core` + Edge 无头模式，无需额外安装 Chrome）
- Node.js 环境（v18+）
- 安装依赖：`cd scripts && npm install`

**图片输出参数：**
| 参数 | 短参 | 说明 | 默认值 |
|------|------|------|--------|
| `--text` | `-t` | 书信正文（必需） | - |
| `--output` | `-o` | 输出文件路径（必需） | - |
| `--format` | `-f` | 输出格式：`png` 或 `jpg` | `png` |
| `--fontSize` | `-s` | 字号（px） | `52` |
| `--cols` | `-c` | 每列字符数 | `28` |
| `--rotate` | `-r` | 旋转角度（度） | `0` |
| `--bg` | `-b` | 背景图路径 | `scripts/fonts/ama-jpg.jpg` |
| `--font` | `-F` | 自定义字体文件路径（.ttf/.otf） | - |

**示例：**
```bash
# 基本用法
node scripts/render-qiaopi.js --text "阿嬷大人：展信安好..." --output letter.png

# 自定义字号和列数
node scripts/render-qiaopi.js --text "..." --output letter.png --fontSize 48 --cols 24

# 输出 JPG
node scripts/render-qiaopi.js --text "..." --output letter.jpg --format jpg

# 自定义背景和字体
node scripts/render-qiaopi.js --text "..." --output letter.png --bg ./custom-bg.jpg --font ./my-font.ttf
```

### 第三步：输出给用户

依次输出：
1. 生成的侨批书信正文（纯正文，无任何解释说明）
2. 生成的信笺图片文件路径

---

## 附加功能：接入 AI 生图（可选）

如需 AI 生成真实手写风格的信笺图片，可额外接入 `baoyu-image-gen` 技能。

**生图提示词模板：**
```
Chinese traditional handwritten letter paper, qiaopi style, old paper texture, red vertical lines, elegant traditional design, warm sepia tones, faint grid lines, handcrafted paper feel, vintage ink style, the letter text is clearly visible in traditional Chinese calligraphy style, realistic paper edges, nostalgic atmosphere, 19th century southern Chinese overseas Chinese letter paper aesthetic, high quality photograph of an actual old letter
```

执行方式：调用 `baoyu-image-gen` 技能，传入侨批正文作为 prompt，生成图片。

**优先级**：优先使用 HTML 渲染方案（无需 API key）。如用户有 AI 生图需求，再调用 baoyu-image-gen。
