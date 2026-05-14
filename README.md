# 🎬 TermCast

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Zero-Dependencies-brightgreen.svg" alt="Zero Dependencies">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL-orange.svg" alt="Platform">
</p>

<p align="center">
  <b>🎬 TermCast - Lightweight Terminal Session Recording & Smart Replay Engine</b><br>
  <b>轻量级终端会话录制与智能回放引擎</b>
</p>

<p align="center">
  <a href="#简体中文">简体中文</a> |
  <a href="#繁體中文">繁體中文</a> |
  <a href="#english">English</a>
</p>

---

## 简体中文

### 🎉 项目介绍

TermCast 是一款轻量级终端会话录制与智能回放引擎，专为开发者设计，解决教学演示、故障排查、操作审计等场景下终端操作记录与分享的痛点。

**核心灵感来源**：在日常开发工作中，我们经常需要向同事展示某个命令的执行过程、记录部署步骤用于文档、或者复盘故障排查过程。传统的屏幕录制工具文件体积大、编辑困难，而简单的文本复制又丢失了操作的时序和上下文。TermCast 正是为解决这一痛点而生。

**自研差异化亮点**：
- 🎯 **零依赖设计**：仅使用 Python 标准库，无需安装任何第三方包
- 🧠 **智能命令分类**：自动识别 10+ 类命令（Git、Docker、构建、测试等）
- 📊 **会话统计分析**：可视化展示命令分布、执行成功率、常用命令排行
- 🎮 **交互式回放**：支持步进、跳转、查看详情的交互式回放模式
- 📤 **多格式导出**：支持文本、Asciinema、JSON 等多种格式导出
- 🚀 **双模式录制**：支持系统 `script` 命令录制和纯 Python 实现的双模式

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🎬 **会话录制** | 完整记录终端命令输入和输出，保留时序信息 |
| 🧠 **智能分类** | 自动识别命令类型：Git、Docker、构建、测试、部署等 |
| 📊 **统计分析** | 命令分类占比、执行成功率、Top 命令排行 |
| 🎮 **交互回放** | 支持自动播放和交互式步进回放 |
| 📤 **格式导出** | 文本、Asciinema、JSON 多格式支持 |
| 🎯 **零依赖** | 纯 Python 标准库实现，开箱即用 |
| 🔒 **隐私安全** | 本地录制，数据不上传云端 |

### 🚀 快速开始

#### 环境要求

- Python 3.8+
- Linux / macOS / WSL
- `script` 命令（可选，用于增强录制模式）

#### 安装

```bash
# 方式一：直接下载使用
git clone https://github.com/gitstq/termcast-recorder.git
cd termcast-recorder
python3 termcast.py --help

# 方式二：安装到系统
pip install .
# 或
python3 setup.py install
```

#### 快速使用

```bash
# 开始录制会话
termcast record

# 使用自定义输出文件名
termcast record -o my_session.json

# 播放录制的会话
termcast play session.json

# 交互式回放
termcast play session.json -i

# 查看会话统计
termcast stats session.json

# 导出为文本格式
termcast export session.json -t text -o output.txt

# 导出为 Asciinema 格式
termcast export session.json -t asciinema -o output.cast

# 列出所有录制的会话
termcast list
```

### 📖 详细使用指南

#### 录制会话

```bash
$ termcast record -o deploy_session.json
🎬 TermCast Recording Started
   Session ID: session_1754728394
   Output: deploy_session.json
   Working Dir: /home/user/myproject
   Type commands below. Enter 'exit' or press Ctrl+C to stop.

user@hostname:/home/user/myproject$ git status
On branch main
Your branch is up to date with 'origin/main'.

user@hostname:/home/user/myproject$ docker build -t myapp .
[... docker build output ...]

user@hostname:/home/user/myproject$ exit

✅ Recording Stopped
   Commands recorded: 3
   Duration: 45.2s
   Saved to: deploy_session.json
```

#### 交互式回放

```bash
$ termcast play deploy_session.json -i
🎬 Playing Session: session_1754728394
   Recorded: 2025-05-14T10:30:00
   Commands: 3
   Speed: 1.0x

────────────────────────────────────────────────────────────
[1/3] $ git status
Category: 🌿 Version Control
────────────────────────────────────────────────────────────
On branch main
Your branch is up to date with 'origin/main'.

[Enter: Next | b: Back | q: Quit | j: Jump | s: Stats]
> 
```

#### 会话统计示例

```bash
$ termcast stats deploy_session.json

📊 Session Statistics
──────────────────────────────────────────────────
Session ID: session_1754728394
Recorded: 2025-05-14T10:30:00
User: user@hostname
Shell: /bin/bash
Working Directory: /home/user/myproject
Terminal Size: 120x30

Total Commands: 3
Total Duration: 45.2s

📈 Command Categories:
   🌿 Version Control: ████████ 1 (33.3%)
   🐳 Container Operations: ████████ 1 (33.3%)
   📁 File Operations: ████████ 1 (33.3%)

🔝 Top Commands:
   git          ● 1
   docker       ● 1
   ls           ● 1

✅ Success Rate: 100.0% (3/3)
```

### 💡 设计思路与迭代规划

#### 技术选型原因

- **纯 Python 标准库**：确保零依赖，任何 Python 环境都能直接运行
- **JSON 格式存储**：人类可读，便于版本控制和后续处理
- **正则表达式分类**：轻量级命令识别，无需机器学习依赖
- **模块化架构**：Recorder、Player、Classifier 独立，便于扩展

#### 后续功能迭代计划

- [ ] 🎨 **GIF/视频导出**：支持导出为可分享的 GIF 或 MP4
- [ ] 🔍 **全文搜索**：支持在会话历史中搜索命令和输出
- [ ] 🏷️ **标签系统**：为会话添加自定义标签和备注
- [ ] 🔐 **敏感信息过滤**：自动检测并脱敏密码、密钥等信息
- [ ] 📤 **云端同步**：可选的加密云端备份功能
- [ ] 🎙️ **语音注释**：录制时添加语音说明

### 📦 打包与部署指南

#### 打包为可执行文件

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包为单文件可执行程序
pyinstaller --onefile --name termcast termcast.py

# 打包后的可执行文件位于 dist/termcast
```

#### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY termcast.py .

ENTRYPOINT ["python3", "termcast.py"]
```

```bash
docker build -t termcast .
docker run -it -v $(pwd):/recordings termcast record -o /recordings/session.json
```

### 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

**提交规范**：
- `feat:` 新增功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关

### 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 繁體中文

### 🎉 專案介紹

TermCast 是一款輕量級終端機工作階段錄製與智慧回放引擎，專為開發者設計，解決教學演示、故障排查、操作稽核等場景下終端機操作記錄與分享的痛點。

**核心差異化亮點**：
- 🎯 **零依賴設計**：僅使用 Python 標準函式庫，無需安裝任何第三方套件
- 🧠 **智慧命令分類**：自動識別 10+ 類命令（Git、Docker、建置、測試等）
- 📊 **工作階段統計分析**：視覺化展示命令分佈、執行成功率、常用命令排行
- 🎮 **互動式回放**：支援步進、跳轉、查看詳情的互動式回放模式
- 📤 **多格式匯出**：支援文字、Asciinema、JSON 等多種格式匯出

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🎬 **工作階段錄製** | 完整記錄終端機命令輸入和輸出，保留時序資訊 |
| 🧠 **智慧分類** | 自動識別命令類型：Git、Docker、建置、測試、部署等 |
| 📊 **統計分析** | 命令分類佔比、執行成功率、Top 命令排行 |
| 🎮 **互動回放** | 支援自動播放和互動式步進回放 |
| 📤 **格式匯出** | 文字、Asciinema、JSON 多格式支援 |
| 🎯 **零依賴** | 純 Python 標準函式庫實作，開箱即用 |

### 🚀 快速開始

#### 安裝

```bash
git clone https://github.com/gitstq/termcast-recorder.git
cd termcast-recorder
python3 termcast.py --help
```

#### 快速使用

```bash
# 開始錄製工作階段
termcast record

# 播放錄製的工作階段
termcast play session.json

# 互動式回放
termcast play session.json -i

# 查看工作階段統計
termcast stats session.json

# 匯出為文字格式
termcast export session.json -t text -o output.txt
```

### 📄 開源協議

本專案採用 [MIT License](LICENSE) 開源協議。

---

## English

### 🎉 Project Introduction

TermCast is a lightweight terminal session recording and intelligent replay engine designed for developers. It solves the pain points of recording and sharing terminal operations in scenarios such as teaching demonstrations, troubleshooting, and operation auditing.

**Core Inspiration**: In daily development work, we often need to show colleagues the execution process of a command, record deployment steps for documentation, or review troubleshooting processes. Traditional screen recording tools produce large files that are difficult to edit, while simple text copying loses the timing and context of operations. TermCast was born to solve this pain point.

**Key Differentiators**:
- 🎯 **Zero Dependencies**: Uses only Python standard library, no third-party packages required
- 🧠 **Intelligent Command Classification**: Automatically identifies 10+ command categories (Git, Docker, Build, Test, etc.)
- 📊 **Session Statistics**: Visualize command distribution, success rates, and top commands
- 🎮 **Interactive Replay**: Step-by-step playback with jump and detail view capabilities
- 📤 **Multi-format Export**: Supports Text, Asciinema, and JSON export formats
- 🚀 **Dual Recording Modes**: Supports both system `script` command and pure Python implementation

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🎬 **Session Recording** | Complete recording of terminal commands and outputs with timing information |
| 🧠 **Smart Classification** | Auto-detect command types: Git, Docker, Build, Test, Deploy, etc. |
| 📊 **Statistics** | Command category breakdown, success rate, top commands ranking |
| 🎮 **Interactive Playback** | Auto-play and interactive step-by-step replay modes |
| 📤 **Format Export** | Text, Asciinema, and JSON format support |
| 🎯 **Zero Dependencies** | Pure Python standard library implementation, works out of the box |
| 🔒 **Privacy First** | Local recording, data never uploaded to cloud |

### 🚀 Quick Start

#### Requirements

- Python 3.8+
- Linux / macOS / WSL
- `script` command (optional, for enhanced recording mode)

#### Installation

```bash
# Method 1: Direct download
git clone https://github.com/gitstq/termcast-recorder.git
cd termcast-recorder
python3 termcast.py --help

# Method 2: Install to system
pip install .
# or
python3 setup.py install
```

#### Quick Usage

```bash
# Start recording session
termcast record

# Use custom output filename
termcast record -o my_session.json

# Play recorded session
termcast play session.json

# Interactive playback
termcast play session.json -i

# View session statistics
termcast stats session.json

# Export to text format
termcast export session.json -t text -o output.txt

# Export to Asciinema format
termcast export session.json -t asciinema -o output.cast

# List all recorded sessions
termcast list
```

### 📖 Detailed Usage Guide

#### Recording a Session

```bash
$ termcast record -o deploy_session.json
🎬 TermCast Recording Started
   Session ID: session_1754728394
   Output: deploy_session.json
   Working Dir: /home/user/myproject
   Type commands below. Enter 'exit' or press Ctrl+C to stop.

user@hostname:/home/user/myproject$ git status
On branch main
Your branch is up to date with 'origin/main'.

user@hostname:/home/user/myproject$ docker build -t myapp .
[... docker build output ...]

user@hostname:/home/user/myproject$ exit

✅ Recording Stopped
   Commands recorded: 3
   Duration: 45.2s
   Saved to: deploy_session.json
```

#### Interactive Playback

```bash
$ termcast play deploy_session.json -i
🎬 Playing Session: session_1754728394
   Recorded: 2025-05-14T10:30:00
   Commands: 3
   Speed: 1.0x

────────────────────────────────────────────────────────────
[1/3] $ git status
Category: 🌿 Version Control
────────────────────────────────────────────────────────────
On branch main
Your branch is up to date with 'origin/main'.

[Enter: Next | b: Back | q: Quit | j: Jump | s: Stats]
> 
```

#### Session Statistics Example

```bash
$ termcast stats deploy_session.json

📊 Session Statistics
──────────────────────────────────────────────────
Session ID: session_1754728394
Recorded: 2025-05-14T10:30:00
User: user@hostname
Shell: /bin/bash
Working Directory: /home/user/myproject
Terminal Size: 120x30

Total Commands: 3
Total Duration: 45.2s

📈 Command Categories:
   🌿 Version Control: ████████ 1 (33.3%)
   🐳 Container Operations: ████████ 1 (33.3%)
   📁 File Operations: ████████ 1 (33.3%)

🔝 Top Commands:
   git          ● 1
   docker       ● 1
   ls           ● 1

✅ Success Rate: 100.0% (3/3)
```

### 💡 Design Philosophy & Roadmap

#### Technical Choices

- **Pure Python Standard Library**: Ensures zero dependencies, runs in any Python environment
- **JSON Format Storage**: Human-readable, version-control friendly
- **Regex-based Classification**: Lightweight command recognition without ML dependencies
- **Modular Architecture**: Recorder, Player, and Classifier are independent for easy extension

#### Roadmap

- [ ] 🎨 **GIF/Video Export**: Export to shareable GIF or MP4 formats
- [ ] 🔍 **Full-text Search**: Search command history for commands and outputs
- [ ] 🏷️ **Tagging System**: Add custom tags and notes to sessions
- [ ] 🔐 **Sensitive Data Filtering**: Auto-detect and mask passwords, keys, etc.
- [ ] 📤 **Cloud Sync**: Optional encrypted cloud backup
- [ ] 🎙️ **Voice Annotations**: Add voice explanations during recording

### 📦 Packaging & Deployment

#### Build as Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build single-file executable
pyinstaller --onefile --name termcast termcast.py

# Executable will be at dist/termcast
```

#### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY termcast.py .

ENTRYPOINT ["python3", "termcast.py"]
```

```bash
docker build -t termcast .
docker run -it -v $(pwd):/recordings termcast record -o /recordings/session.json
```

### 🤝 Contributing

Issues and Pull Requests are welcome!

**Commit Convention**:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code refactoring
- `test:` Test related

### 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ by TermCast Team<br>
  <a href="https://github.com/gitstq/termcast-recorder">GitHub Repository</a>
</p>
