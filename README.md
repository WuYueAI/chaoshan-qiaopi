# 潮汕侨批书写馆 (chaoshan-qiaopi)

将大白话转换为潮汕传统侨批（南洋家书）风格书信，生成传统信笺图片。

## 在 WorkBuddy 中使用

在工作聊天中直接说「帮我写一封侨批给阿嬷」，或触发关键词「侨批」「南洋家书」「给阿嬷的信」等，AI 会自动代笔生成书信并渲染为图片。

## 命令行渲染

如需在自己脚本中调用渲染：

```bash
cd scripts && npm install
node render-qiaopi.js --text "书信正文..." --output output.png
```

## 文件结构

```
chaoshan-qiaopi/
├── SKILL.md                ← WorkBuddy 技能定义
├── references/
│   └── style-guide.md    ← 侨批写作风格指南
└── scripts/
    ├── render-qiaopi.js   ← 命令行渲染引擎（puppeteer 无头渲染）
    ├── package.json
    └── fonts/
        ├── 正1.png / 正2.png / 正3.png   ← 信笺底图
        ├── simkai.ttf                    ← 楷体
        ├── simfang.ttf                   ← 仿宋
        └── simsun.ttc                    ← 宋体
```

## 渲染脚本参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--text` / `-t` | 书信正文（必需） | - |
| `--output` / `-o` | 输出路径（必需，绝对路径） | - |
| `--format` / `-f` | png 或 jpg | png |
| `--fontSize` / `-s` | 字号 px | 52 |
| `--cols` / `-c` | 每列字数 | 27 |
| `--bg` / `-b` | 背景图路径 | scripts/fonts/正1.png |

## 前置要求

- Edge 浏览器（puppeteer-core 调用）
- Node.js v18+
- 依赖已预装于 `scripts/node_modules/`

## 写作铁律

1. **文风**：民国末、建国后老式家书口吻，白话文言结合
2. **结构**：称呼问好 → 告知寄银 → 自身报平安 → 思念 → 叮嘱 → 落款
3. **先银后情**：第一段必须先交代汇款
4. **永远报喜不报忧**
5. **思念不直白**：用景物、时节、家常小事寄托
