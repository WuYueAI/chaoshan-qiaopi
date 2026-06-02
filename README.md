# 潮汕侨批书写馆 (chaoshan-qiaopi)

将大白话转换为潮汕传统侨批（南洋家书）风格书信，生成传统信笺图片。

## 快速使用（零安装）

**双击 `qiaopi-demo.html` 即可使用。** 输入大白话 → 点击"研墨成笺" → 下载信笺图片。

| 特点 | 说明 |
|------|------|
| 单文件 | 一个 HTML，约 17MB |
| 零依赖 | 不需要 Node.js、Python、Docker |
| 完全离线 | 3 张底图、3 款字体全部内嵌 |
| 随机底图 | 每次生成从 3 张侨批信笺中随机选一张 |
| 可调参数 | 字号、每列字数实时调节 |

[下载 qiaopi-demo.html](https://raw.githubusercontent.com/WuYueAI/chaoshan-qiaopi/main/qiaopi-demo.html)（右键另存为）

## WorkBuddy 聊天内使用

在工作聊天中直接说「帮我写一封侨批给阿嬷」，或触发关键词「侨批」「南洋家书」「给阿嫲的信」等，AI 会自动代笔生成书信并渲染为图片。

## 自行构建

```bash
python build-v46.py    # 需要正1.png / 正2.png / 正3.png 在项目目录
```

## 命令行渲染

```bash
cd scripts && npm install
node render-qiaopi.js --text "书信正文..." --output output.png
```

## 文件结构

```
chaoshan-qiaopi/
├── qiaopi-demo.html          ← 独立网页版（推荐，双击即用）
├── build-v46.py              ← 网页版构建脚本
├── SKILL.md                  ← WorkBuddy 技能定义
├── scripts/
│   ├── render-qiaopi.js      ← 命令行渲染引擎
│   ├── package.json
│   └── fonts/
│       ├── 正1.png / 正2.png / 正3.png   ← 底图
│       ├── simkai.ttf                    ← 楷体
│       ├── simfang.ttf                   ← 仿宋
│       └── simsun.ttc                    ← 宋体
└── references/
    └── style-guide.md        ← 侨批写作风格指南
```
