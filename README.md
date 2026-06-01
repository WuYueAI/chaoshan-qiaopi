# 潮汕侨批书写馆 (chaoshan-qiaopi)

将任意文本转换为潮汕传统侨批风格书信，并渲染为传统信笺图片。

## 安装

```bash
cd scripts
npm install
```

## 使用方法

### 1. 生成侨批书信

根据 [SKILL.md](SKILL.md) 中的写作规则，AI 将用户输入转换为侨批风格书信。

### 2. 渲染为图片

```bash
node scripts/render-qiaopi.js --text "书信正文..." --output output.png
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--text` | - | 书信正文（必需） |
| `--output` | - | 输出文件路径（必需） |
| `--fontSize` | 52 | 字号（px） |
| `--cols` | 28 | 每列字数（总容量 8×28=224） |
| `--format` | png | 输出格式 png/jpg |
| `--bg` | fonts/ama-jpg.jpg | 背景图路径 |
| `--font` | - | 自定义字体 .ttf/.otf |
| `--rotate` | 0 | 旋转角度 |

### 示例

```bash
# 基本用法
node scripts/render-qiaopi.js --text "阿嬷大人：展信安好..." --output letter.png

# 小号字 + 多列（容纳更长文本）
node scripts/render-qiaopi.js --text "..." --output letter.png --fontSize 40 --cols 30

# JPG 格式
node scripts/render-qiaopi.js --text "..." --output letter.jpg --format jpg
```

## 版本历史

- **v24**（当前）：前置截断机制，28字/列，总容量224字，超长自动截断+提示
- **v23-v21**：JPG 底图切换、纸面利用率修复、印章穿透优化
- **v20 及更早**：列对齐精调、水印去除、字体嵌入

## 文件结构

- `SKILL.md` - WorkBuddy 技能定义
- `README.md` - 本文件
- `references/style-guide.md` - 详细写作风格指南
- `scripts/render-qiaopi.js` - HTML→图片渲染脚本（v24）
- `scripts/fonts/` - 底图 + 内嵌字体文件
- `scripts/package.json` - Node.js 依赖配置

## 系统要求

- Node.js 18+
- Windows（使用 Edge 无头模式）+ macOS/Linux（需安装 Chromium）
- 无需联网（字体已 base64 内嵌）
