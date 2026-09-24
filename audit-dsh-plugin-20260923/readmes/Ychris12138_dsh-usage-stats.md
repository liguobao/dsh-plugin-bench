# dsh-usage-stats

<!-- stable-version: 0.3.3 -->

[![GitHub Release](https://img.shields.io/github/v/release/Ychris12138/dsh-usage-stats?display_name=tag&sort=semver&color=1f6feb)](https://github.com/Ychris12138/dsh-usage-stats/releases/latest)
[![CI](https://github.com/Ychris12138/dsh-usage-stats/actions/workflows/ci.yml/badge.svg)](https://github.com/Ychris12138/dsh-usage-stats/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-2da44e)](LICENSE)

为 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) 网页端提供多供应商账户监测与 Token 用量分析。

Provider balances, subscription quotas, and token-usage analytics for the DeepSeek Harness Web GUI (`dsh web`).

![dsh-usage-stats interface preview](docs/images/usage-panel.svg)

> 展示图使用脱敏演示数据；插件不会把 API Key、Cookie、管理 PAT 或上游原始响应发送到浏览器。

[![Powered by OrcaRouter](https://img.shields.io/badge/Powered_by-OrcaRouter-2563eb)](https://www.orcarouter.ai/ref/ref_13c34663d1527ac16963)

> 🐋 OrcaRouter sponsors this project and is available as an optional OpenAI-compatible provider. [Learn more](https://www.orcarouter.ai/ref/ref_13c34663d1527ac16963) · Referral link.

## 一眼看懂 / At a glance

| | 能力 | 说明 |
| --- | --- | --- |
| 💳 | 统一账户卡片 | API 供应商显示余额，Token Plan 显示分窗口额度；面板一次只呈现当前供应商 |
| 📊 | Token 用量分析 | 今日、本月、累计、缓存命中率、月历热图，以及按日期/供应商/模型下钻 |
| 💰 | 估算费用与预算 | 按事件时间匹配历史价格，提供日/月费用、session 级聚合及可选预算预警 |
| 🔄 | 后台监测 | 账户按 active/detail/background 自适应刷新；间隔可配置或完全关闭，本地 Token 聚合保持独立运行 |
| 🧩 | 可扩展适配器 | 支持 New API、Sub2API、通用余额模板，以及声明式 JSON Pointer 自定义查询 |
| 📦 | 安全导出 | 提供 daily/session CSV 与版本化 JSON；Unicode、CSV 公式前缀和不完整费用均安全处理 |
| 🔒 | 本机安全边界 | 数据端点仅接受回环 GET；OrcaRouter preset 仅由带防跨站请求头的显式回环 POST 写入；凭据只在服务端解析 |

界面支持中文和英文。浏览器只请求当前选择的 provider；账户自动刷新由服务端统一调度。手动刷新会更新用量、供应商列表，并强制刷新当前账户，不会批量强制请求其他供应商。

## 快速安装 / Quick start

需要 DeepSeek Harness `web` profile（`@deepseek-ai/dsh >= 0.1.0-rc.6`）。

稳定版优先安装 npm 上的精确版本；这也是 DSH Desktop Market 使用的同一个包：

```bash
dsh plugin --profile web add "@ychris12138/dsh-usage-stats@0.3.3"
```

只有测试尚未发布的 source/RC 时才使用 `dsh plugin --profile web add "github:Ychris12138/dsh-usage-stats"`。GitHub `main` 可能领先 npm stable，不应把 source 安装当作市场安装验收。

然后重启已经运行的 `dsh web`，并在浏览器中硬刷新。侧边栏底部会出现“用量/余额”（Usage/Balance）入口。

### 插件市场 GUI 安装（DSH Community Market，Path A 标准来源）

本仓库按 [DSH Community Market 目录 adapter 指南](https://github.com/anywhere-labs/deepseek-harness-desktop/blob/master/dsh-community-market/docs/catalog-adapter-guide.zh.md) 的**标准来源（Path A）** 接入，无需修改 Market 代码。内置两份目录数据：

- `catalog/catalog-source.json` — 来源 manifest（`catalog-source.schema.json` v1.0.0）
- `catalog/v1/plugins.json` — 标准 provider page（`catalog-provider-page.schema.json` v1.0.0）

**使用前提（重要）**：市场托管安装只接受 npm registry 的精确稳定版本，git 条目仅可浏览。`dsh-usage-stats` 这个 npm 名已被其他项目占用，因此目录条目身份使用 `@ychris12138/dsh-usage-stats`。当前 stable/catalog 版本是 `0.3.3`；每个新版本都按以下顺序发布：

1. 运行 `npm run release:sync -- <version>` 同步 `package.json` / `package-lock.json` / `catalog/v1/plugins.json`，再由 `npm run check:release` 阻止身份或版本漂移。
2. 发布 scoped 公共包：`npm publish --access public`。
3. 把 `catalog/v1/plugins.json` 内容发布到 `https://ychris12138.github.io/dsh-usage-stats/v1/plugins`（GitHub Pages，manifest 与 endpoint 必须同源、HTTPS 443、无凭据）。
4. 在 DSH 插件市场 → 来源管理 → 添加来源，粘贴 manifest URL：`https://ychris12138.github.io/dsh-usage-stats/catalog-source.json`，选择后即可走「可恢复安装边界」GUI 安装。

> 目录若先指向尚未发布的版本，市场安装会 fail-closed，这是预期行为。只有 npm、Pages catalog 与 Desktop Market 实际安装全部验证后，才算完成发布。

升级或卸载：

```bash
dsh plugin --profile web update "@ychris12138/dsh-usage-stats"
dsh plugin --profile web remove "@ychris12138/dsh-usage-stats"
```

<details>
<summary><strong>兼容安装器：无法使用 dsh plugin 时展开</strong></summary>

PowerShell、命令提示符和 macOS/Linux 终端使用同一条命令：

```bash
npx --yes github:Ychris12138/dsh-usage-stats
```

安装器会把运行文件复制到 `~/.dsh/profiles/node_modules/@ychris12138/dsh-usage-stats`，并在 `profiles/web/cordis.patch.yml` 中以带引号的 scoped identity 幂等启用插件。重复运行即可更新，不会重复追加配置；旧版 `name: dsh-usage-stats` 和未加引号的 `name: @ychris12138/dsh-usage-stats` 会自动迁移。设置了 `DSH_HOME` 时使用该目录。

`dsh plugin` 与 `npx` 是两条独立安装路径，请选择其中一种；不要同时保留手工 Cordis entry 和 bundle 注册，否则会重复挂载。

```bash
# 预览，不修改文件
npx --yes github:Ychris12138/dsh-usage-stats --dry-run

# 检查现有安装
npx --yes github:Ychris12138/dsh-usage-stats --check

# 安装但不修改 Cordis patch
npx --yes github:Ychris12138/dsh-usage-stats --no-enable
```

无法使用 `npx` 时可从源码运行 `node scripts/install.mjs`。

</details>

## 支持的账户类型 / Providers

插件自动发现官方 DeepSeek 路由和 `llm-pi-ai` 中的 provider profile。只有存在公开账户接口或显式 monitor 的供应商才会查询远端账户；Token 用量统计不需要额外凭据。

| Provider / adapter | 模式 | 默认凭据 | 上游接口 |
| --- | --- | --- | --- |
| DeepSeek | 余额 | provider `apiKeyEnv` | `/user/balance` |
| OpenRouter | 余额 | `OPENROUTER_MANAGEMENT_KEY` | `/api/v1/credits` |
| OrcaRouter | 余额 | `ORCAROUTER_API_KEY` | `/v1/balance`（旧部署回退到账单摘要接口） |
| Moonshot / Kimi API | 余额 | provider `apiKeyEnv` | `/v1/users/me/balance` |
| OpenCode Go | 订阅 | `OPENCODE_GO_API_KEY` 或本地 `auth.json` | `/zen/go/v1/usage` |
| Z.ai / 智谱 | 订阅 | `ZAI_API_KEY` | Coding Plan quota/subscription |
| Kimi For Coding | 订阅 | `KIMI_API_KEY` | `/coding/v1/usages` |
| MiniMax Coding Plan | 订阅 | `MINIMAX_API_KEY` | `/v1/token_plan/remains` |
| Ollama 云 | 订阅 | `OLLAMA_API_KEY` | `/api/usage`（5小时 + 周窗口） |
| New API | 余额 | provider 推理 Token | `/api/usage/token/` |
| Sub2API / Passion | 自动判别 | provider `apiKeyEnv` | `/v1/usage` |
| Sub2API 面板（真实） | 余额 | provider 推理 Token | `/user/balance`（复用 apiKey） |
| General / Declarative | 余额或订阅 | 配置中的 credential ref | 受限 GET + JSON |

没有公开账户接口的供应商仍会正常统计 Token；账户卡片会明确显示“不支持”，不会猜测余额。

## 凭据与供应商配置 / Configuration

凭据由 Harness 从 `~/.dsh/.credentials.yaml` 解析。安装器不会读取、创建或修改该文件。不要把真实 Key、Cookie 或管理令牌提交到 Git、公开 issue，或粘贴给编码 Agent。

### 账户刷新 / Account refresh

默认刷新间隔是 active 1 分钟、detail 2 分钟、background 15 分钟。严格限流的 New API 或公司中转可以调整全局策略，或完全关闭账户自动刷新：

```yaml
# ~/.dsh/profiles/web/cordis.patch.yml
- insert:
    - id: usage-stats
      name: "@ychris12138/dsh-usage-stats"
      config:
        refresh:
          enabled: false
          activeMs: 60000
          detailMs: 120000
          backgroundMs: 900000
```

三个间隔必须是 `60000` 至 `86400000` 毫秒之间的整数。需要停止时使用 `refresh.enabled: false`，不要填写超大的 timeout。关闭后，每个相同 provider 配置仍允许首次查询；之后普通面板读取只返回缓存，不会因缓存过期访问上游。账户端点的 `refresh=1`（Retry）仍可显式刷新，provider/monitor 配置变化后也会为新配置重新查询一次。

旧配置 `disableBackgroundRefresh: true` 继续等价于 `refresh.enabled: false`；两者同时存在时，显式的 `refresh.enabled` 优先。该开关只关闭账户上游自动刷新，不会关闭本地 Token 用量聚合。

### 估算费用与预算 / Estimated cost and budgets

预算是可选的非敏感配置，默认关闭。金额只在 provider、model、事件时间与货币均能由内置价格规则可靠确定时计算；未知中转、订阅路线、无价格的 cache write 或混合币种会整体显示 `—`，不会展示部分费用或进行汇率换算。

```yaml
# ~/.dsh/profiles/web/cordis.patch.yml
- insert:
    - id: usage-stats
      name: "@ychris12138/dsh-usage-stats"
      config:
        budgets:
          currency: USD
          daily: 5
          monthly: 100
```

预算使用本机日历日/月边界：低于 80% 为正常，达到 80% 为 warning，达到 100% 为 critical。`daily` / `monthly` 必须是正数或 `null`；当前版本不做 FX 换算，因此预算货币与可靠价格货币不兼容时状态保持 unknown。

面板的当前 provider 会保存在浏览器的命名空间 localStorage 中；刷新页面或重启 DSH 后恢复。若该 provider 已被删除，插件会清除旧值并使用原有的 DeepSeek/已配置 provider fallback。该选择不会写入 DSH 设置、服务端缓存或新 API。

### 余额型供应商

DeepSeek、Moonshot 等默认复用对应 provider profile 的 `apiKeyEnv`。例如：

```yaml
# ~/.dsh/.credentials.yaml
DEEPSEEK_API_KEY: sk-your-key-here
```

OpenRouter 是明确的例外：官方账户 credits 接口要求 **Management Key**，不能复用普通推理 `OPENROUTER_API_KEY`。插件默认读取独立引用；未配置时显示“未配置”，不会拿推理 Key 试探：

```yaml
# ~/.dsh/.credentials.yaml
OPENROUTER_MANAGEMENT_KEY: sk-or-v1-your-management-key
```

插件按 `total_credits - total_usage` 显示 OpenRouter 余额，并同时展示累计已用和总 credits。普通 Key 的 `/api/v1/key` 只描述单个 Key 的 spending limit，不会被当作账户余额。自定义引用可在 `monitors.openrouter` 中设置 `adapter: openrouter-balance` 与 `credentialRef`。

OrcaRouter 优先读取其余额接口 `/v1/balance`，将 paid、free 和 promo credits 汇总为当前可用余额；旧部署没有该接口时，回退到官方文档提供的 OpenAI-compatible 账单摘要接口（订阅端点总额度 + usage 端点累计用量，按美分换算）。任一可用路径返回无法识别的数据时会显示明确的错误状态，不会把未知结果当作 0；无限额度哨兵值会显示为 `∞`，OrcaRouter 路由仍不参与本插件的模型价格估算。

### Token Plan 供应商

```yaml
# ~/.dsh/.credentials.yaml
OPENCODE_GO_API_KEY: sk-opencode-your-key
ZAI_API_KEY: your-zai-key
# 中国区 Z.ai 用