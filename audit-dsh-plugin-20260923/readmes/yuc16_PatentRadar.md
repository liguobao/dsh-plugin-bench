<div align="center">

# PatentRadar

**专利侵权竞品分析**

输入一个专利公开号，输出一份竞品侵权分析报告——内容包括：逐项技术特征对比表、可点击的公开证据 URL、以及“还缺什么证据 / 下一步去哪查”的可执行建议。


[![uv](https://img.shields.io/badge/managed_with-uv-DE5FE9?logo=python&logoColor=white)](https://github.com/astral-sh/uv)
[![LLM](https://img.shields.io/badge/LLM-ChatGPT_auth_/_OpenAI_compatible-10A37F?logo=openai&logoColor=white)](#-llm-后端)
[![Skill](https://img.shields.io/badge/Claude_Code-Skill-D97757?logo=anthropic&logoColor=white)](#模式-b作为-skill-嵌入-claude-code--codex-cli)
[![License](https://img.shields.io/badge/license-MIT-blue)](#-license)

https://github.com/user-attachments/assets/94f8f758-6a43-49a8-b16b-2e04e1d8e110

[快速开始](#-快速开始) · [Skill安装（推荐使用）](#模式-b作为-skill-嵌入-claude-code--codex-cli) · [Examples](examples/README.md) · [评估](evaluate/EVALUATION.md)

</div>

---

## 为什么需要 PatentRadar

> 传统侵权排查靠人工：律师团队读专利权 → 拆特征 → 翻竞品手册 → 搜证据 → 写 claim chart，一份高质量报告动辄 3-5 天。

PatentRadar 把这条链路压到 **1 小时**：4 个模块串行流水线 + 多源搜索 + 多模态证据抓取 + 严苛评分规则，让 LLM 做"信息整理"和"逐特征对比"，把 **可追溯复核** 的 侵权分析报告直接交到律师手上。

## 🚀 快速开始

### 部署：两种模式

| 维度 | 模式A：独立部署（高性能） | 模式B：skill 嵌入（最简单，推荐） |
|---|---|---|
| **所需依赖** | **1、至少一个搜索工具（Tavily/Bocha/Exa/Brave）2、大模型的api** | **零额外依赖，只需要codex或其他agent** |
| 调度 | [`server/runner.py`](src/patentradar/server/runner.py) 串 4 个 CLI subprocess | 主 agent spawn 4 个 subagent |
| LLM 调用 | 项目内的 [`llm/provider.py`](src/patentradar/llm/provider.py) 统一发包 | 由宿主 agent（Claude Code / Codex）的对话能力直接调用 |
| 搜索 / 抓页 | 项目内的 [`search/`](src/patentradar/search/) + [`fetcher/`](src/patentradar/fetcher/) 模块 | 由宿主 agent 的 WebSearch / WebFetch 工具直接调用 |
| 可观测追溯 | Web Dashboard + 4 个 module log 文件 | 宿主 agent 的对话窗口 + 落盘 JSON |

#### 注：关于模式A的所需依赖说明
- **搜索工具**：**推荐四个搜索工具全部连接，性能最强**，模式A综合使用四个搜索工具，将不同工具的搜索性能极致发挥，其中tavily是主力搜索工具，消耗额度较高，所以.env中可配置多个tavily的api-key轮换使用。（如需大量低价api-key，可前往闲鱼购买）
    - [Tavily](https://www.tavily.com/)
    - [博查 API](https://open.bochaai.com/)
    - [Exa](https://exa.ai/)
    - [Brave Search API](https://brave.com/search/api/)
- **大模型**：模式A需要自己配置大模型的api-key，支持两种大模型的配置方式（推荐**chatgpt auth**，便宜、模型强、额度多）：
  - **chatgpt auth**（ChatGPT plus以上订阅可用，需本机安装codex cli后在终端运行 `codex login` 完成 OAuth）
  - **其他OpenAI 兼容格式**（aihubmix / DeepSeek / 自建网关）——请参考 [`.env.example`](.env.example)


---
### 模式A：分两种部署方式

#### 方式 （1） · 本地 uv（推荐）

```bash
git clone https://github.com/yuc16/PatentRadar.git
cd PatentRadar
uv sync                              # 装全部依赖
cp .env.example .env                 # 在.env中填入你的所有API keys
```

> **PDF 渲染的系统层依赖** —— `uv sync` 只装 Python 包；WeasyPrint 另需系统级图形库（Pango / Cairo 等），Linux 还需中文字体（macOS / Windows 系统自带中文字体，无需另装）。缺图形库 → 只产出 md、无 PDF；缺中文字体 → PDF 中文乱码。按平台装一次即可（可以让AI帮你装）

**Linux**（Debian / Ubuntu）
```bash
apt install -y libpango-1.0-0 libpangoft2-1.0-0 libcairo2 \
               libgdk-pixbuf-2.0-0 libffi8 shared-mime-info fonts-noto-cjk
```
> 其它发行版换包名，如 Fedora：`pango cairo gdk-pixbuf2` + `google-noto-sans-cjk-fonts`。

**macOS**（Homebrew）
```bash
brew install pango          # 连带 cairo / gdk-pixbuf 等依赖；中文走系统自带 PingFang SC
```

**Windows**
1. 安装 [MSYS2](https://www.msys2.org/)（默认选项）
2. 在 MSYS2 shell 内执行：`pacman -S mingw-w64-x86_64-pango`
3. 中文走系统自带「微软雅黑」，无需另装字体
> 若 `uv run` 报找不到 libgobject / pango 等 DLL，把 `C:\msys64\mingw64\bin` 加入系统 PATH

> 若选 Codex 后端：到宿主机跑 `codex login` 完成 OAuth；选 OpenAI 兼容后端：直接填 `.env`

---
#### 方式 （2） · Docker（无法使用 chatgpt auth）

宿主机只要装 Docker，不需要 Python / uv / weasyprint 系统库。

```bash
git clone https://github.com/yuc16/PatentRadar.git
cd PatentRadar
cp .env.example .env                 # 填入 API keys（容器里必须用 openai 兼容后端）
docker compose up -d --build         # 首次构建并后台启动
open http://localhost:8000           # 浏览器打开 dashboard 即可使用
```

常用维护命令：

```bash
docker compose logs -f                                  # 跟随日志
docker compose down                                     # 关停
docker compose down && docker compose up -d            # 改了 .env 后重启
docker compose down && docker compose up -d --build    # 改了 src/Dockerfile/pyproject 后重建
```

容器内 `/app/data`、`/app/logs`、`/app/configs`、`/app/patentradar_output` 通过 volume 挂到宿主机同名目录，产物落盘后宿主机能直接看到。
### 使用：跑一篇专利

> 命令前缀按你的部署方式替换，命令体和产物路径完全一致：
> - **Docker**：`docker compose exec patentradar <命令>`
> - **本地 uv**：`uv run <命令>`

#### Web Dashboard（**推荐**，可视化 + 完整日志）

Docker 方式启动后即可访问；本地 uv 需要手动起 server，终端运行以下一行命令即可：

```bash
uv run uvicorn patentradar.server.app:app --reload --port 8000
```

浏览器打开 `http://localhost:8000`：

- 输入专利公开号，点「开始分析」即可端到端跑完 4 模块
- 4 个模块进度、每一次 LLM 调用 / 搜索调用 / 网页 fetch 实时显示
- 跑完后可回放（1x / 20x / 100x / 600x 倍速），支持导出离线 HTML 分享给同事
- 完整结构化日志写入 `logs/<PUB>/`：`run.jsonl` + `module_N.log` + `module_N.stream.jsonl`

#### HTTP API（脚本化 / CI 集成）

与 Web Dashboard 同源同接口，适合无人值守：

```bash
curl -X POST http://localhost:8000/api/run/CN110293961B
curl -N    http://localhost:8000/api/stream/CN110293961B   # SSE 实时事件
curl       http://localhost:8000/api/status/CN110293961B   # JSON 快照
```

`POST /api/run/{pub}` 同步校验格式（不合法专利号 → **400** + 错误信息）；
若该 pub 已经在跑则直接 **409**，避免重复启动 BackgroundTask。

#### 分步 CLI（调试 / 重跑某一步）

直接调每个模块的 CLI，业务产物正常落到 `data/output/<PUB>/`，但**没有 `logs/<PUB>/` 结构化日志**（那是 server 模式专属）：

```bash
uv run patentradar decompose CN110293961B
uv run patentradar competitor-search data/output/CN110293961B/task_package.json
uv run patentradar full-claim-chart  data/output/CN110293961B/task_package.json \
                                     data/output/CN110293961B/step5_top5_claim1_candidates.json
uv run patentradar report            data/output/CN110293961B/task_package.json \
                                     data/output/CN110293961B/top5_full_claim_chart.json
```

产物落盘位置（**三种使用方式一致**）：

```
data/output/CN110293961B/
├── task_package.json                # 模块 1：权利要求拆解
├── step1_query_plan.json            # 模块 2 step1：查询计划
├── step2_search_results.json        # 模块 2 step2：搜索原始结果
├── step3_candidate_shortlist.json   #          step3：候选清单
├── step4_candidate_evidence.json    #          step4：逐候选权 1 证据
├── step4_fetched_pages/<cid>.json   #          step4：全文证据池（供模块 3 复用）
├── step4_visual_log_fetched/        #          step4：fetch 阶段抓回的全部图（审计用）
├── step4_visual_log_sent/           #          step4：实际送给 LLM 的图（审计用）
├── step5_top5_claim1_candidates.json#          step5：TOP-N 排名
├── top5_full_claim_chart.json       # 模块 3：全 claim 对比
├── report.md                        # 模块 4：最终报告（markdown）
└── report.pdf                       #         最终报告（PDF）
```

> [`scripts/run_full_pipeline.py`](scripts/run_full_pipeline.py) 是模块 2-4 的**测试 wrapper**（固定从 `tests/decompose/outputs/<PUB>/` 读模块一 fixture），仅供开发期调试，不适合跑生产专利。

---

### 模式 B：作为 skill 嵌入 Claude Code / Codex CLI

把 [`skills/patentradar/`](skills/patentradar/) 目录放到你的 agent 的 skill 路径下（或软链）。

或者直接在你的 agent 中（推荐 codex 或claude code）输入：
```text
> 帮我安装https://github.com/yuc16/PatentRadar这个skill
```
即可完成部署，随后只需要自然语言输入你想要分析的专利公开号

```text
> 帮我跑下 CN114512759B 的侵权竞品分析
```

skill 会自动触发，按顺序 spawn 4 个独立 subagent，每个 subagent 跑完用 JSON Schema 自动校验产物（失败时把错误清单透传给该 subagent 让它修正后重交，最多重试 2 次），4 个模块全跑完后告诉你 `report.md` / `report.pdf` 落盘位置。



---

## 🏗️ 架构

系统采用**分层解耦**设计，从顶到底共 6 层：接入层 → 调度层 → 业务模块层 → 适配层 → 外部服务层 → 持久层。下面给出三个视图：**系统分层架构**、**模块内部工作流**、**核心数据流时序**。

### 视图 1：系统分层架构（6 层）

```mermaid
graph TB
    subgraph L1["①  接入层 · Access Layer"]
        direction LR
        CLI["🖥️  CLI<br/><i>typer</i><br/>patentradar decompose / search / chart / report"]
        WEB["🌐  Web Dashboard<br/><i>FastAPI + SSE 流式推送</i><br/>· 4 模块进度可视化<br/>· 回放 1x ~ 600x · 离线 HTML 导出"]
        SKILL["🤖  Skill Adapter<br/><i>Claude Code / Codex CLI</i><br/>spawn 4 个 subagent 串行 + schema 自校验"]
    end

    subgraph L2["②  调度层 · Orchestration"]
        direction LR
        ORCH["⚙️  Pipeline Orchestrator<br/><code>server/runner.py</code><br/>4 模块按序 subprocess 调度 · 失败重试 · 产物落盘"]
        VAL["✅  Schema Validator<br/><code>schemas/validate.py</code><br/>每模块跑完自动校验 → 失败回填 LLM 重交（最多 2 次）"]
        STREAM["📡  LLM Stream Writer<br/><code>llm/stream.py</code><br/>所有 LLM payload / response → <code>logs/&lt;PUB&gt;/module_N/</code>"]
    end

    subgraph L3["③  业务模块层 · Business Modu