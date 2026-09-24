<!--
(c) 2026 Jose AI (https://www.linhut.cn)
https://github.com/linhut/gongwen-skill
Licensed under the MIT License. See the LICENSE file for details.
-->

# 公文全流程处理专家

<p align="center">
  <img src="./logo/2026-08-19_11-17-43.png" alt="公文全流程处理专家" width="760">
</p>

> 中文公文全流程处理专家——基于 **GB/T 9704《党政机关公文格式》** 国家标准，支持 **格式检查与修复、内容优化（Word 原生修订+批注/差异对比版）、模板生成、Markdown 转公文、版头版记页码注入、事实核验、风格增强** 等完整能力。原生支持 **DeepSeek Harness (DSH)** 技能系统，打包为可被 AI Agent 直接调用的 Skill，完全自包含，克隆即用。

[![CI](https://img.shields.io/badge/CI-Passing-brightgreen)](https://github.com/linhut/gongwen-skill/actions)
[![PyPI](https://img.shields.io/pypi/v/gongwen-skill)](https://pypi.org/project/gongwen-skill/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![GB/T 9704](https://img.shields.io/badge/standard-GB%2FT%209704-red.svg)
![DSH](https://img.shields.io/badge/DSH-Compatible-brightgreen)
![Downloads](https://img.shields.io/badge/Downloads-0-blue)

本 Skill 源自开源桌面项目 [AI 公文智能优化助手](https://github.com/linhut/document-ai-assistant)，将其核心格式引擎抽取、剥离桌面端/数据库依赖后独立发行，支持公文的**模板建立、解析、规则检查、自动修复、内容优化、Markdown 转公文**全流程能力。同时原生集成 **DeepSeek Harness (DSH)** 技能系统，支持 DSH Agent 自动发现与加载。

---

## ✨ 能力一览

| 能力 | 命令 | 说明 |
|------|------|------|
| 📋 列类型 | `list-types` | 列出 25 种支持的公文类型（新增主持词 host_speech；含新闻稿/讲话稿） |
| 🏗️ 模板生成 | `template` | 按类型生成 GB/T 9704 标准空白模板 |
| 🔍 解析 | `parse` | `.docx` → 结构化 DocumentModel |
| ✅ 格式检查 | `check` | 按国标检查，分级 P0/P1/P2（只读） |
| 🔧 格式修复 | `optimize` | 自动修复字体/字号/行距/页边距，输出合规文档；`--verify` 单命令闭环自动复查、P0 存在时退出码非 0；`--json` 结构化输出 |
| ✍️ **内容优化** | **`optimize-content`** | 内容润色：默认 **Word 原生修订+批注**（审阅面板逐条接受/拒绝），可选行内差异对比版；`--precheck` 预检 changes 与原文一致性、`--preset quick/full/review` 参数收敛 |
| 📝 草稿转公文 | `md2docx` | Markdown 文本直接转为格式化 `.docx`（支持 Front Matter） |
| 🚀 一站式生成 | `draft` | Markdown 草稿 → 国标成品 + 自动验证（路径 C 四步合一） |
| 📄 模型生成 | `generate` | 从 JSON 模型生成 `.docx` |
| 🔴 版头 | `header` | 注入发文机关标志 + 发文字号 + 签发人 + 红色反线 |
| 📑 版记 | `footer` | 注入抄送机关 + 印发机关 + 印发日期 + 分隔线 |
| 🔢 页码 | `pagenum` | 注入 Word PAGE 域动态页码（宋体 4 号，默认单右双左适配双面打印） |
| 🖊️ 首句加粗 | `bold-first` | 正文段落首句自动加粗（公文规范） |
| 🧰 一键修复 | `fix-common` | 路径 D 一键修复常见格式：段落类型修正 + 编号拆分 + 首句加粗 + 加粗范围修复 |
| 📋 桌签生成 | `table-signs` | 批量生成 A5 横版会议桌签 |
| 🔍 审稿生成 | `review` | 按五角色审稿机制生成审稿意见 |
| 🧩 完整审校 | `full-review` | 修订+批注联合命令（句子级差异修订 + 分类批注） |
| 🎨 样式学习 | `style-learn` / `style-list` | 上传标准文档学习 Run/段落/页面三级样式（字体/字号/字间距/行距/缩进/页边距），生成命名模板持久化，后续用 `optimize -t 模板名` 套用 |
| 🔄 版本自检 | `check-update` | 版本自检（PyPI pip 包权威判定 + GitHub 备用，GitCode/AtomGit 作国内镜像提示；GitHub 不可达时自动做 DNS 污染诊断 + hosts 建议） |
| 🩺 自我诊断 | `doctor` / `repair` | 全面诊断 23 项（Python/依赖/版本一致性/字体/DSH 文件/DSH 技能 frontmatter/代码风格/网络 DNS），自动修复常见问题；`--offline` 跳过网络检查 |
| 🕵️ 文档审计 | `audit` | 检查删除线/加粗/AI 声明等痕迹 |
| 🤝 会话交接 | `handoff` | 跨会话上下文传递（`--list` / `--latest` / Agent 长任务收尾必写） |
| ⚙️ 规则管理 | `rule-export/import/list` | YAML 规则三层定制（官方/单位/用户） |
| 🧭 向导式交互 | `wizard` | 交互式路径引导（A/B/C/D/E）+ 一键执行；Agent 用 `--answers` 非交互 / `--dry-run` 只打印命令 |

## 使用示例

> 在 AI 对话中调用 gongwen-skill，输入自然语言指令，自动生成符合 GB/T 9704 国标格式的正式公文。

### 🤖 调用环境的适配指引（AI Agent 必读）

本工具针对不同能力层级的 AI 调用环境，提供不同的使用方式。**AI 读取本文件后，请先判断自身环境属于哪一类，再按对应指引执行：**

| 环境类型 | 典型平台 | 能力 | 使用方式 |
|:---------|:---------|:-----|:---------|
| **① 可执行代码的 Agent** | WorkBuddy、CloudCode、Claude Code、AtomCode、DeepSeek Harness | 可运行命令、读写本地文件 | 直接执行 `python -m gongwen <命令>`，见下方「快速开始」与「通过 Agent 调用」 |
| **② 纯对话 LLM（无代码执行能力）** | 豆包、Kimi、ChatGPT 网页版等 | 只能阅读文本、给出建议，**不能运行命令或读写文件** | 引导用户手动执行，见下方「纯对话 LLM 使用指引」 |

#### 纯对话 LLM 使用指引（环境 ②）

> **如果你是无法执行代码的纯对话 AI**（如豆包、Kimi、ChatGPT 网页版等），请按以下方式协助用户：

1. **告知工具性质**：向用户说明「这是一个本地运行的 Python 命令行工具，需要在你自己的电脑上安装后使用」，并说明它能做什么（格式检查、自动修复、内容优化、模板生成等 29 项命令能力）。
2. **引导安装**：请用户在自己的电脑上执行以下步骤：
   ```bash
   # 步骤 1：克隆仓库
   git clone https://github.com/linhut/gongwen-skill.git
   cd gongwen-skill

   # 步骤 2：安装依赖（需要 Python 3.10+）
   pip install -r requirements.txt
   # 或直接安装 PyPI 包：
   # pip install gongwen-skill
   ```
3. **按需给出具体命令**：根据用户的实际需求，给出对应的命令让用户自行执行：

   | 用户需求 | 建议用户执行 |
   |:---------|:-------------|
   | 检查公文格式 | `python -m gongwen check 公文.docx -t notice --json` |
   | 自动修复格式 | `python -m gongwen optimize 公文.docx -o 成品.docx -t notice --apply` |
   | 生成标准模板 | `python -m gongwen template notice -o 通知模板.docx` |
   | Markdown 转公文 | `python -m gongwen md2docx 草稿.md -o 正式公文.docx -t report` |
   | 内容润色（修订+批注） | `python -m gongwen optimize-content 原文.docx --changes 修订内容.json --apply --mode tracked` |
   | 注入版头/版记/页码 | `python -m gongwen header/footer/pagenum 公文.docx ...` |
   | 从标准文档学样式做模板 | `python -m gongwen style-learn 标准公文.docx -n 模板名`，之后用 `optimize -t 模板名` 套用 |
   | 安装标准字体 | `python -m gongwen font install` |

4. **解释输出**：用户执行后，把命令输出结果（问题清单、修复报告、生成文件等）发给你时，你能继续帮助解读、判断下一步操作。
5. **注意事项**：你**不能**代替用户执行任何命令，也**不能**读取用户本地的文件内容——所有文件操作都必须由用户在你的指引下完成。

#### 文字性资源库（纯对话 LLM 可读的知识源）

项目内置以下文字性资源，纯对话 AI 可以直接读取，用作**公文写作指导的知识库**：

| 资源 | 位置 | 内容 |
|:-----|:-----|:------|
| **公文语言风格提示词库** | `prompts/style-prompts.md` | 6 套风格（庄重严谨/平实简洁/宏观概括/请示商洽/法规条文/讲话稿），每套含用词规范、句式和语气指导 |
| **使用指引与决策速查** | `prompts/usage-prompts.md` | 最小可用指引、决策速查、每种公文类型的用法模板、常见问题解答 |
| **公文类型规则库** | `rules/official/*.yaml`（25 个文件） | 每种公文类型的格式规范 + 内容层定义（如"请示应以'妥否，请批示'结尾""通知应以'特此通知'结尾"） |
| **通用格式标准** | `rules/official/_common.yaml` | GB/T 9704 国标全文参数：字体/字号/行距/页边距等 |
| **技能完整指令** | `SKILL.md` | 路径路由、执行标准、质量评审、禁令清单、审稿机制 |

**使用方式**：纯对话 AI 在回答用户关于公文写作的问题时，可直接引用上述资源中的内容，例如：
- 用户问"通知怎么写" → 引用 `rules/official/notice.yaml` 的结语规范和 `style-prompts.md` 的庄重严谨风格
- 用户问"请示和报告的区别" → 引用 `request.yaml` 和 `report.yaml` 的规则说明
- 用户问"公文用什么字体" → 引用 `_common.yaml` 中的 GB/T 9704 标准
- 用户需要润色文字 → 引用 `style-prompts.md` 中对应的风格提示词

> 这些资源均以纯文本格式存储，纯对话 AI 可直接读取解读，无需执行任何代码即可提供专业的公文写作指导。

## 🚀 快速开始

```bash
git clone https://github.com/linhut/gongwen-skill.git
cd gongwen-skill
pip install -r requirements.txt

# 生成一份标准通知模板
python -m gongwen template notice -o 通知模板.docx

# 检查公文格式（只读）
python -m gongwen check 公文.docx -t notice --json

# 自动修复格式（--apply 确认执行，默认预览）；--verify 生成后自动复查，P0 存在时退出码非 0
python -m gongwen optimize 公文.docx -o 成品.docx -t notice --apply --verify

# 一步到位：检查 + 修复 + 版头/版记/页码全注入（--layout 指向 JSON 配置）
python -m gongwen optimize 公文.docx -o 成品.docx --layout 版式.json

# Markdown 草稿 → 正式公文（支持管道输入和 Front Matter 元数据）
python -m gongwen md2docx 草稿.md -o 正式公文.docx -t report --signer "XX单位" --date "2026年8月1日"

# 一步到位：Markdown 草稿 → 国标成品 + 自动验证（路径 C 四步合一）
python -m gongwen draft 草稿.md -o 正式公文.docx -t report --signer "XX单位" --date "2026年8月1日"

# 内容优化（默认 tracked 模式：Word 原生修订+批注，审阅面板逐条接受/拒绝）
python -m gongwen optimize-content 原文.docx --changes 修订内容.json --apply --mode tracked -t news

# 预检 changes 与原文一致性（不生成文档，输出不匹配清单+相似度诊断；不匹配时退出码 1）
python -m gongwen optimize-content 原文.docx --changes 修订内容.json --precheck

# 预设组合：quick 精简快速 / full 完整默认 / review 完整审稿（显式参数优先）
python -m gongwen optimize-content 原文.docx --changes 修订内容.json --apply --preset full

# 注入版头（发文机关标志 + 发文字号 + 签发人 + 红色反线）
python -m gongwen header 公文.docx -o 红头公文.docx --org-name "XX单位" --doc-number "〔2026〕1号"

# 注入版记（抄送 + 印发机关 + 印发日期）
python -m gongwen footer 红头公文.docx --cc "各单位" --printer "XX办公室" --print-date "2026年8月1日"

# 注入页码（Word PAGE 域动态页码）
python -m gongwen pagenum 红头公文.docx --alignment right

# 版本自检（PyPI pip 包权威判定 + GitHub 备用渠道）
python -m gongwen check-update

# 安装公文标准字体（方正小标宋简体/仿宋_GB2312/楷体_GB2312）
python -m gongwen font install          # 安装字体到系统
python -m gongwen font check            # 检查字体安装状态
python -m gongwen font list             # 列出字体清单

# 从标准文档学习排版样式，生成自定义模板（后续用 optimize -t 模板名 套用）
python -m gongwen style-learn 标准公文.docx -n 模板名
python -m gongwen style-list            # 列出已学习的模板
```

### 🖥️ Windows 控制台编码（GBK 乱码排查）

工具内部已统一按 UTF-8 输出（`gongwen/_bootstrap.py` 强制 stdout/stderr/stdin 重配置为 UTF-8，
保证管道/Agent 调用无编码问题）。若在原生 `cmd`（默认 GBK 代码页 936）看到中文乱码，任选其一：

- **推荐**：改用 Windows Terminal / VS Code 终端（默认 UTF-8，无乱码）
- 在 cmd 中先执行 `chcp 65001` 切换 UTF-8 代码页，再运行命令
- 或设置环境变量 `PYTHONIOENCODING=utf-8`（与工具内部行为一致）

> 说明：GBK 乱码仅影响原生 cmd 的**交互显示**，不影响文件内容与 `--json` 的机器可解析性。

### 🔤 字体管理

公文标准字体是 GB/T 