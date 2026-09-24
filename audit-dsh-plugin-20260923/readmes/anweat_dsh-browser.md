# dsh-browser

本地整合候选的修复、工具清单与安全边界见 [AUDIT.md](AUDIT.md)。`allowedDomains` 只限制认证状态装载，不是网络防火墙或 Agent 隔离边界。

自包含的浏览器运行时插件 for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)（DSH）。

把 **Playwright / Patchright（可选 Chromium 驱动）** 与 **OpenCLI** 作为插件自身的 npm 依赖打包（优先插件本地，缺省回退全局复用），对外提供一个 `browser` 服务 + 一组交互式浏览器工具。`dsh-web-search-pro` 通过 `inject: ['browser']` 注入该服务，驱动它的浏览器 / OpenCLI 后端——**不再依赖全局 CLI**。

## 兼容与发布通道

| 插件发布通道 | DSH 基线 | 兼容承诺 |
|---|---|---|
| npm `latest`（`0.1.12`） | `dsh-v0.1.1-rc.2` 至 `dsh-v0.1.2-rc.1` | 已验证维护基线 |
| npm `next` 候选（`0.1.15-alpha.2`） | `dsh-v0.1.5-alpha.1` | 精确依赖与真实 profile 验收目标 |

`0.1.15-alpha.2` 使用 DSH 新客户端分包：状态存储来自
`dsh-client-store`，设置契约来自 `dsh-client-ui-settings`，客户端 Context
来自 Cordis。该候选不会覆盖 npm `latest`。

## 安装

```bash
dsh plugin --profile web add @anweat/dsh-browser
# 或本地目录 / tarball：
dsh plugin --profile web add ./dsh-browser
# 重启（web profile 关闭了 HMR）：
dsh --profile web
```

> npm `latest` 延续现有维护基线；本开发分支精确适配 `dsh-v0.1.5-alpha.1`。
> 若你的 harness 是包含未发布提交的本地源码 checkout，版本号可能有出入——用
> `dsh plugin --profile web add ./<path>` 并在 profile 的 `pnpm-workspace.yaml`
> 里对齐版本后重装即可。

## 从旧版本升级

Web Search Pro 与浏览器插件应同步升级；`dsh-web-search-pro >= 0.1.8` 需要 `@anweat/dsh-browser >= 0.1.8`。面向 `dsh-v0.1.5-alpha.1` 联调时，使用 browser 与 Web Search Pro 的 npm `next` 候选并完整重启 profile。0.1.11 移除了对旧版 `dsh-settings` 的运行时 `settingsNamespace` 导入；0.1.10 修复工具描述被 DSH 误解析为 prompt 变量。

```bash
dsh plugin --profile web add @anweat/dsh-browser@next dsh-web-search-pro@next
```

升级后完整停止并重启 Web profile，再调用 `browser_status`、`browser_opencli_status` 和 `web_backend_status`；仅刷新网页不会重新加载插件服务或 Web Search Pro 配置面板。尤其不要只升级 Web Search Pro：新的工具目录、Patchright 运行时和调用缓冲都来自浏览器插件。

## 快速使用与适用情形

安装并重启后，可先让模型调用 `browser_status`，再按任务选择工具。默认
`automationMode: standard`：读取直接执行，点击、输入、按键、选择、勾选、悬停、文件上传及页面写操作走 DSH 原生一次性审批。页面脚本和本地文件上传在 `autonomous` 下仍需审批，只有 `unrestricted` 会跳过确认。

| 情形 | 推荐方式 | 关键边界 |
|---|---|---|
| 公开网页读取、截图 | `browser_open` → `browser_read` / `browser_screenshot` | 不需要登录态 |
| 表单、分页、懒加载 | `browser_click` / `browser_type` / `browser_press` / `browser_select` / `browser_check` / `browser_scroll` | CSS 或 role/text/label 语义定位；`standard` 下审批 |
| SPA 条件等待 | `browser_wait` | 支持 locator、URL glob、networkidle 或最多 10 秒固定等待 |
| 悬停菜单与提示 | `browser_hover` | 与直接页面交互使用相同审批策略 |
| 文件上传 | `browser_set_files` | 只接受现有绝对文件路径；最多 20 个、合计 512 MiB；除 `unrestricted` 外审批会显示路径 |
| 页面脚本表达式 | `browser_evaluate` | 使用当前页面来源和登录态；可访问 DOM、非 HttpOnly Cookie、Web Storage 和浏览器允许的网络 API |
| 页面故障排查 | `browser_open(capture=[console,network])` → `browser_console` / `browser_requests` | 只在内存保留最多 200 条；网络仅记录失败及 4xx/5xx，不记录 body/header |
| 登录后站点 | `authProfile` | 必须配置 `allowedDomains`；默认不回写 Cookie |
| 固定站点增强 | `rulePack` | 只允许有界步骤；本地 init script 必须 SHA-256 固定且 ≤64KB |
| 模型生成的多步操作 | `browser_recipe_run` | 声明式步骤；审批策略由 `automationMode` 决定 |
| 默认只读脚本 | `browser_script_catalog` → `browser_script_run_builtin` | 内置 article/links/JSON-LD/forms，不执行外来代码 |
| 外部模型生成 UserScript | `browser_script_validate` → `browser_userscript_run` | 必须 `@match` + `@grant none`；除 `unrestricted` 外执行前审批 |
| 有限站点遍历 | `browser_crawl` | 页数、深度、并发、突发与退避始终受 `usagePolicy` 约束 |
| Reddit/小红书等 OpenCLI 平台 | `browser_opencli_status` → `browser_opencli_catalog` → `browser_opencli_run` | 先发现精确 adapter；通用调用除 `unrestricted` 外需审批 |
| 普通站点兼容性不佳 | `browserRuntime: patchright` | Chromium-only；建议专用 Chrome profile，不与指纹注入库叠加 |

所有网页访问、交互、脚本、Cookie 使用、上传和下载都必须由调用方或操作者根据目标网站规则及适用要求判断并使用。插件只执行被请求或批准的浏览器操作，不判断具体用途是否获得网站授权，也不承担调用方的合规责任。限流、审批、域名和文件边界用于约束执行面，不能替代目标网站规则。

DSH 会话示例：

```text
先调用 browser_status；然后用 browser_open 打开目标页。
若页面需要登录，使用 authProfile=forum；不要把 Cookie 放进工具参数。
```

## 内核与依赖的"打包 vs 复用"

| 层 | 实际是什么 | 打包还是复用 |
|---|---|---|
| **chromium 内核** | 共享缓存 `%LOCALAPPDATA%\ms-playwright`（约 400MB） | **永远复用共享缓存**，不塞进插件、不重复下载；缺失时 `browser_install` 一键补 |
| **playwright 驱动**（JS 包） | `playwright` npm 依赖 | 插件本地 node_modules 优先，缺省回退全局 npm |
| **patchright 驱动**（可选） | 与 Playwright 同版本的 Chromium 兼容驱动 | 插件内置；配置 `browserRuntime: patchright` 才启用 |
| **opencli**（纯 Node CLI） | `@jackwener/opencli` npm 依赖 | 同上，本地优先 / 全局复用 |

## 服务：`browser`

`dsh-browser` 在 `apply()` 里 `ctx.provide('browser', service)`。任何插件声明
`inject: ['browser']` 即可消费：

```ts
export const inject = ['tools', 'browser']
export function apply(ctx: Context) {
  const browser = ctx.get('browser') as BrowserService
  // browser.render / snapshot / searchResults / opencli / recipe /
  // runBuiltinScript / runUserscript / open / click / type / scroll / read / screenshot / close
}
```

服务接口（结构性，无需共享类型包）见 `src/browser-service.ts`。

## 自动化自由度

`automationMode` 控制模型可见的工具集合和执行审批。建议从 `standard` 开始，仅在完全只读任务或受控自动化环境中切换：

| 模式 | 浏览器与 Web Search Pro 写操作 | 仍需审批或拒绝 | 不可取消的安全底线 |
|---|---|---|---|
| `read-only` | 只读工具与只读 Recipe；缓存清理、规则写入和安装拒绝 | 页面交互、写 Recipe、UserScript、OpenCLI run 均隐藏或拒绝 | 只能读取、校验、截图及运行只读脚本/Recipe |
| `standard`（默认） | 页面交互、写 Recipe、缓存清理和规则写入均需一次性审批 | UserScript、通用 OpenCLI、浏览器/后端安装也需审批 | 所有安全校验持续启用 |
| `autonomous` | 页面交互、写 Recipe、缓存清理和规则写入可直接执行 | 外部 UserScript、通用 OpenCLI、浏览器/后端安装仍强制审批 | 所有安全校验持续启用 |
| `unrestricted` | 所有上述工具均不触发审批，适合隔离环境中的无人值守测试 | 无审批提示 | 仍执行域名、元数据、参数、大小和步骤数校验 |

`unrestricted` 会允许模型直接运行外部脚本、通用 CLI 和安装命令，只应在隔离的测试 profile 或明确授权的自动化环境中使用；日常 profile 保持 `standard`。它只取消人工确认，**不会取消 `usagePolicy` 的并发、突发、页数、深度、重试与冷却保护**。模式改变后需要重启 DSH profile，工具目录才会按新配置重新注册。

## 工具（最多 30 个）

| 工具 | 作用 |
|---|---|
| `browser_open` | 打开 URL，返回标题/可读文本/全页截图路径；可显式启用 console/network 内存捕获 |
| `browser_click` | 按 CSS 或结构化 Playwright locator 点击 |
| `browser_type` | 向 CSS 或语义定位的 input/textarea 输入 |
| `browser_wait` | 等待 locator 状态、URL glob、networkidle 或固定时间 |
| `browser_press` | 对 locator 或全局键盘发送按键 |
| `browser_select` | 按 locator 选择一个或多个 option value |
| `browser_check` | 按 locator 勾选或取消勾选控件 |
| `browser_hover` | 悬停 CSS 或语义 locator 并返回页面状态与截图 |
| `browser_set_files` | 把现有本地文件设置到 `input[type=file]`；绝对路径、数量和总大小受限 |
| `browser_evaluate` | 在当前页执行最长 20,000 字符的 JavaScript 表达式，返回最多 100,000 字符 JSON |
| `browser_console` | 读取本次显式捕获的脱敏 console 记录 |
| `browser_requests` | 读取本次显式捕获的失败及 HTTP 4xx/5xx 请求；无 body/header |
| `browser_scroll` | 纵向滚动（触发懒加载） |
| `browser_read` | 读当前页 URL/标题/文本（不截图） |
| `browser_screenshot` | 当前页、locator 或区域截图；普通文件名固定落在 `snapshotDir` |
| `browser_close` | 关闭当前页（下次 open 全新） |
| `browser_status` | 运行时状态（含 automationMode、已暴露工具及各类审批策略） |
| `browser_install` | 安装 playwright chromium（`browser_status` 报缺失时执行一次） |
| `browser_script_catalog` | 列出内置只读脚本及其 SHA-256 |
| `browser_script_validate` | 解析外部 UserScript 的元数据、域名、grant、能力与哈希，不执行 |
| `browser_script_run_builtin` | 在独立 Playwright context 中运行内置只读脚本 |
| `browser_userscript_run` | 运行外部 UserScript；强制域名匹配，审批策略由模式决定 |
| `browser_recipe_run` | 最多 25 步 Playwright Recipe；支持等待、定位、表单、键盘、提取、断言和截图 |
| `browser_automation_search` | 只有显式关键词调用才检索；可限定 active/draft/all、域名和类型，最多返回 `retrievalTopK` 条摘要 |
| `browser_automation_develop` | 按确切 ID 读取源码，或显式保存、静态校验、真实回放草稿；永远不能激活资产 |
| `browser_automation_run` | 按 ID 运行已激活资产；再次执行限域和输入大小校验，审批由 `automationMode` 决定 |
| `browser_opencli_status` | 实际运行 OpenCLI doctor，报告 daemon/extension/profile 连通性 |
| `browser_opencli_catalog` | 对 OpenCLI 大目录按 query/site/access/strategy 过滤，单次最多返回 100 条 |
| `browser_opencli_run` | 通用 OpenCLI argv 网关；除 `unrestricted` 外触发 DSH 原生一次性审批 |
| `browser_crawl` | 匿名、有限广度遍历；默认同源，强制使用全局调用缓冲和单次页数/深度预算 |

## 可复用自动化资产（实验性）

> **Experimental:** Recipe/UserScript 的积累、模型开发、检索和复用接口仍可能调整。建议先在隔离 profile 中启用，审阅草稿并完成真实浏览器回放后再手动激活；不要把它作为无人监管的生产写操作入口。

自动化执行自由度与资产持久化是两套独立开关。`automationMode: unrestricted` 只影响执行审批，不会让 Agent 自动保存脚本；默认 `automationAssets.persistenceMode: suggest` 仅对成功的 `browser_recipe_run` 记录脱敏语义步骤。具体输入会替换为 `{{input}}` / `{{secret}}`，会话 ID 只保存短哈希，不保存页面正文、cookie、token、密码或聊天记录。

默认在 14 天窗口内，同一域名和步骤指纹至少成功 3 次、来自至少 2 个会话且成功率达到 80%，面板才出现“是否总结”候选。每天最多提示 2 次；候选、草稿和已激活资产均有数量上限。推荐流程是：

1. 候选达到阈值后，在“浏览器自动化 → 可复用自动化资产”选择“总结为草稿”或“暂不总结”。
2. 在脚本列表点选草稿；只有此时前端才按 ID 读取完整 recipe / UserScript。编辑器支持 recipe 和带 `@match`、`@grant none` 的 UserScript。UserScript 可从只读对象 `__DSH_INPUTS__` 读取 `inputNames` 声明的运行时输入，输入不会写入资产文件。
3. 保存后先做静态校验，再填写测试 URL/输入执行真实浏览器回放。只