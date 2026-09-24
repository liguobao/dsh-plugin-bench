# stock-analysis-plugin

[![npm](https://img.shields.io/npm/v/@weaxs/stock-analysis-plugin?label=npm&logo=npm)](https://www.npmjs.com/package/@weaxs/stock-analysis-plugin)
[![PyPI](https://img.shields.io/pypi/v/stock-analysis-plugin?label=pypi&logo=pypi&logoColor=white)](https://pypi.org/project/stock-analysis-plugin/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-%3E=3.10-blue?logo=python&logoColor=white)](https://www.python.org/)

A 股 / 港股 / 美股 / 日股 / 韩股 / 台股综合分析、多因子选股和策略回测工具集，可作为 [Pi Agent](https://github.com/anthropics/pi-agent) Extension、[Hermes Agent](https://github.com/NousResearch/hermes-agent) Plugin、[OpenClaw](https://docs.openclaw.ai/) Plugin，或 [DeepSeek Harness (dsh)](https://github.com/deepseek-ai/deepseek-harness) Plugin 使用。

底层共享同一套 Python CLI 工具和 SKILL.md 工作流，上层分别适配四个平台的注册机制。

## 目录

- [功能概览](#功能概览)
- [安装](#安装)
  - [Pi Agent Extension](#pi-agent-extension)
  - [Hermes Agent Plugin](#hermes-agent-plugin)
  - [OpenClaw Plugin](#openclaw-plugin)
  - [dsh (DeepSeek Harness) Plugin](#dsh-deepseek-harness-plugin)
  - [Python 依赖](#python-依赖)
- [快速开始](#快速开始)
- [Skills 一览](#skills-一览)
- [工具列表](#工具列表)
- [策略回测 DSL](#策略回测-dsl)
- [市场路由规则](#市场路由规则)
- [独立 CLI 使用](#独立-cli-使用)
- [项目结构](#项目结构)
- [致谢](#致谢)
- [常见问题](#常见问题)
- [License](#license)

## 功能概览

- **51 个工具** — 行情数据、技术分析、K 线形态、资金流向、财务指标、新闻舆情、风险筛查、市场状态等
- **20 个 Skills** — 综合分析、全市场选股、策略回测 + 17 个策略方法论（缠论、波浪、龙头、情绪周期等）
- **策略回测引擎** — YAML DSL 定义策略，参数化条件组合，自动诊断，按需进行有限轮参数优化
- **多数据源 Failover** — 11 个数据源自动容灾切换（akshare / tushare / efinance / 腾讯行情 / 新浪行情 / pytdx / baostock / yfinance / finnhub / longbridge / alphavantage），A 股链路带粘性优选（最近成功的数据源下次优先尝试）
- **社交舆情增强** — A 股（东财股吧 + 雪球）/ 美港股（Reddit / X / Polymarket），市场自动路由
- **四平台适配** — 同一套工具同时支持 Pi Agent、Hermes Agent、OpenClaw 和 dsh

## 安装

> 所有 npm 包同时以 scoped（`@weaxs/*`）和非 scoped 同名两种名字发布，内容一致，任选其一即可。

插件包地址：

| 平台 | 包名 | 地址 | 安装命令 |
|------|------|------|----------|
| Pi Agent | `@weaxs/stock-analysis-plugin`（或 `stock-analysis-plugin`） | [npm](https://www.npmjs.com/package/@weaxs/stock-analysis-plugin) | `npm install @weaxs/stock-analysis-plugin` |
| Hermes Agent | `stock-analysis-plugin` | [PyPI](https://pypi.org/project/stock-analysis-plugin/) | `pip install stock-analysis-plugin` |
| OpenClaw | `@weaxs/openclaw-stock-analysis`（或 `openclaw-stock-analysis`） | [npm](https://www.npmjs.com/package/@weaxs/openclaw-stock-analysis) | `openclaw plugins install clawhub:@weaxs/openclaw-stock-analysis` |
| DeepSeek Harness (dsh) | `@weaxs/dsh-stock-analysis`（或 `dsh-stock-analysis`） | [npm](https://www.npmjs.com/package/@weaxs/dsh-stock-analysis) | `dsh plugin --profile <profile> add @weaxs/dsh-stock-analysis` |

各平台的详细安装步骤见下方对应小节。

### Pi Agent Extension

```bash
# 全局安装
cd ~/.pi/agent/extensions
npm install @weaxs/stock-analysis-plugin

# 或项目级安装
mkdir -p .pi/extensions && cd .pi/extensions
npm install @weaxs/stock-analysis-plugin
```

> 也可以直接 `git clone git@github.com:Weaxs/stock-analysis-plugin.git` 使用源码版本。

Pi 启动后自动加载，输入 `/skills` 确认。详见 [Pi Agent 接入指南](docs/pi-integration.md)（[English](docs/pi-integration.en.md)）。

### Hermes Agent Plugin

```bash
pip install stock-analysis-plugin
```

安装后 Hermes 通过 `hermes_agent.plugins` entry point 自动发现并注册，无需手动复制目录。

或在 Python 中直接注册：

```python
from hermes import register
register(ctx)
```

详见 [Hermes Agent 接入指南](docs/hermes-integration.md)（[English](docs/hermes-integration.en.md)）。

### OpenClaw Plugin

```bash
openclaw plugins install clawhub:@weaxs/openclaw-stock-analysis
```

OpenClaw Gateway 启动后自动加载并注册 51 个 tool。安装时 postinstall 会自动建 `.venv` 并装好 Python 依赖（前提：本机有 `python3 >= 3.10`）。

详见 [OpenClaw 接入指南](docs/openclaw-integration.md)，或 plugin 自身说明 [`openclaw/README.md`](openclaw/README.md)。

### dsh (DeepSeek Harness) Plugin

```bash
dsh plugin --profile <你的profile> add @weaxs/dsh-stock-analysis
dsh --profile <你的profile>
```

作为 dsh bundle 安装：`dsh plugin add` 会把 `cordis.patch.yml` 叠加进 profile 组合，注册 51 个 tool + 20 个 skill。postinstall 自动建 `.venv`（pnpm 需在 profile 的 `pnpm-workspace.yaml` 里给本包配 `allowBuilds`，否则回退系统 `python3`）。

详见 [`dsh/README.md`](dsh/README.md)。

### Python 依赖

```bash
pip install -r tools/requirements.txt
```

主要依赖：

| 包 | 用途 |
|---|------|
| akshare | A 股数据源（行情、资金流、财务、新闻，含 A 股 ETF） |
| yfinance | 港股 / 美股 / 日股 / 韩股 / 台股数据源 |
| pandas / numpy | 数据处理和数值计算 |
| exchange-calendars | 交易日历（A/HK/US/JP/KR/TW） |
| newspaper4k | 新闻正文提取 |
| pypinyin | 股票名称拼音搜索 |
| pytdx | A 股 TDX 行情（免费兜底源） |
| longport | 港股 / 美股 Longbridge SDK |

> A 股行情另有**腾讯（qt.gtimg.cn）/ 新浪（hq.sinajs.cn）**两个免鉴权兜底源，不依赖任何 Python 包（直接 HTTP 调用），用于东财域名不可达的网络环境（境外主机、企业出网限制等）。

### 环境变量

**数据源（可选，配置后自动加入 Failover 链）：**

| 环境变量 | 用途 |
|---------|------|
| `TUSHARE_TOKEN` | Tushare 数据源（A 股 K 线 / 行情） |
| `LONGBRIDGE_APP_KEY` | Longbridge SDK（港股 / 美股） |
| `LONGBRIDGE_APP_SECRET` | Longbridge SDK |
| `LONGBRIDGE_ACCESS_TOKEN` | Longbridge SDK |
| `ALPHAVANTAGE_API_KEY` | Alpha Vantage（美股 K 线 / 行情） |
| `FINNHUB_API_KEY` | Finnhub（港股 / 美股） |
| `XUEQIU_TOKEN` | 雪球（A 股个股所属板块反查，东财不可用时的兜底） |

**搜索引擎（可选，配置任一即可）：**

| 环境变量 | 用途 |
|---------|------|
| `TAVILY_API_KEY` | Tavily 搜索 |
| `BRAVE_API_KEY` | Brave 搜索 |
| `SERPAPI_KEY` | SerpAPI |
| `BOCHA_API_KEY` | Bocha AI 搜索 |
| `SEARXNG_BASE_URLS` | SearXNG 自建实例地址（逗号分隔多个，无需 Key，兜底用） |

**社交舆情（可选）：**

| 环境变量 | 用途 |
|---------|------|
| `SENTIMENT_API_URL` | 舆情 API 地址（默认 `https://api.adanos.org`） |
| `SENTIMENT_API_KEY` | 舆情 API 密钥 |

## 快速开始

### 综合分析

```
/skill:stock-analysis

帮我分析贵州茅台（600519）
```

Agent 会自动调用行情 → 技术面 → 基本面 → 资金面 → 消息面，输出多维度研报。

### 全市场选股

```
/skill:stock-screener

帮我从 A 股中筛选出低估值+高成长的股票，要求 PE < 30、PB < 5、市值 > 100 亿
```

### 策略回测

```
/skill:strategy-backtest

用 RSI 超卖反弹策略回测茅台，时间段 2024 年全年
```

### 特定策略视角

```
/skill:chan-theory
用缠论分析一下 600519 当前的走势结构

/skill:wave-theory
用波浪理论分析 AAPL 的浪形位置
```

## Skills 一览

### 核心 Workflow（3 个）

| Skill | 调用方式 | 功能 |
|-------|----------|------|
| 综合分析 | `/skill:stock-analysis` | 技术面 + 基本面 + 资金面 + 消息面多维研判，输出结构化研报 |
| 全市场选股 | `/skill:stock-screener` | L1 多因子硬筛（市场情绪调节，可选 `--l2` 量化增强）→ L2 LLM 智能排序 → 输出推荐列表 |
| 策略回测 | `/skill:strategy-backtest` | YAML 策略定义 → 回测 → 诊断；按需进行最多 3 轮参数优化 |

### 策略、复盘与研究（17 个）

| Skill | 调用方式 | 方法论 |
|-------|----------|--------|
| 趋势追踪 | `/skill:bull-trend` | 均线排列 + MACD 方向 + 趋势阶段判断 |
| 缩量回调 | `/skill:shrink-pullback` | 上升趋势中的缩量洗盘识别 |
| 均线金叉 | `/skill:ma-crossover` | MA5/10/20/60 交叉信号 + 金叉质量评估 |
| 放量突破 | `/skill:volume-breakout` | 关键阻力位的放量突破确认 |
| 底部放量 | `/skill:bottom-volume` | 底部区域异动放量 → 主力建仓信号 |
| 龙头战法 | `/skill:dragon-head` | 板块龙头识别 + 龙头 vs 跟风判断 |
| 缠论 | `/skill:chan-theory` | 笔 → 段 → 中枢 → 背驰 → 买卖点 |
| 波浪理论 | `/skill:wave-theory` | Elliott 5 浪推动 + 3 浪调整 + 斐波那契 |
| 箱体震荡 | `/skill:box-oscillation` | 箱体区间识别 + 支撑压力间波段操作 |
| 情绪周期 | `/skill:emotion-cycle` | 市场情绪冰点 → 回暖 → 狂热 → 退潮周期判断 |
| 一阳穿三阴 | `/skill:one-yang-three-yin` | K 线形态识别 + 反转信号质量评级 |
| 事件驱动 | `/skill:event-driven` | 公告/政策/业绩事件的影响路径与失效条件 |
| 预期重估 | `/skill:expectation-repricing` | 市场预期与实际数据的偏差 |
| 成长质量 | `/skill:growth-quality` | 收入、利润、现金流与盈利能力的多期验证 |
| 热点题材 | `/skill:hot-theme` | 板块强度、扩散度、关联度与节奏 |
| 市场复盘 | `/skill:market-review` | 指数、宽度、板块、温度与次日策略 |
| Wisburg 投研 | `/skill:wisburg-research` | 检索机构研报、公告、电话会纪要和市场日报 |

## 工具列表

### 数据获取

| 工具 | 说明 |
|------|------|
| `get_kline` | K 线数据（OHLCV），支持日/周/月线 |
| `get_quote` | 实时行情快照（非交易时段返回最近交易日收盘价并以 as_of/stale 标注；ETF 的 premium_discount_rate 为正=溢价、负=折价） |
| `get_capital_flow` | 资金流向（仅 A 股） |
| `get_news` | 个股相关新闻 |
| `get_financials` | 财务指标 |
| `get_stock_info` | 股票基本信息 |
| `get_chip_distribution` | 筹码分布 |
| `get_market_indices` | 主要指数行情 |
| `get_sector_rankings` | 板块涨跌排行（行业/概念） |
| `get_sector_constituents` | 板块成分股查询（仅 A 股，板块名模糊匹配） |
| `resolve_stock_sectors` | 个股所属板块查询（A 股行业+概念 / 港股 GICS） |
| `get_market_stats` | 市场统计（涨跌家数、涨停等） |
| `get_limit_up_pool` | 涨停池/涨停板复盘（连板数、封板资金、炸板次数等，仅 A 股；非交易日自动回退到最近交易日并以 requested_date/stale 标注） |
| `get_dragon_tiger` | 龙虎榜（净买额/上榜原因/解读，仅 A 股；非交易日自动回退到最近交易日并以 requested_date/stale 标注） |
| `get_hot_stocks` | 全市场人气热搜榜（东财→百度，仅 A 股） |
| `get_margin_tra