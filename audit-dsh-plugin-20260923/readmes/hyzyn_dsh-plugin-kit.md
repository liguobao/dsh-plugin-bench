# dsh-plugin-kit · DSH 插件全家桶

中文 | [English](README.en.md)

<p align="center">
  <img src="https://img.shields.io/github/v/release/hyzyn/dsh-plugin-kit?style=flat-square" alt="Version">
  &nbsp;
  <img src="https://img.shields.io/github/stars/hyzyn/dsh-plugin-kit?style=flat-square" alt="Stars">
  &nbsp;
  <img src="https://img.shields.io/github/forks/hyzyn/dsh-plugin-kit?style=flat-square" alt="Forks">
  &nbsp;
  <img src="https://img.shields.io/npm/v/@hyzyn%2Fdsh-all?style=flat-square&label=npm" alt="npm">
  &nbsp;
  <img src="https://img.shields.io/npm/dt/@hyzyn%2Fdsh-all?style=flat-square&label=downloads" alt="Downloads">
  &nbsp;
  <img src="https://img.shields.io/badge/license-Apache--2.0-blue?style=flat-square" alt="License">
</p>

仓库门禁：`pnpm typecheck` / `pnpm build` / `pnpm test` / `pnpm aggregate`。

<p align="center">
  <strong>DeepSeek Harness（DSH）Web GUI 的插件全家桶</strong><br>
  <em>环境变量 · MCP 服务器 · Prompt · Profile · RSS · 全局搜索 · Codegraph 集成 · 终端面板 · 容器面板 · 插件脚手架</em>
</p>

<p align="center">

[是什么](#是什么) · [功能插件](#功能插件) · [快速开始](#快速开始) · [开发新插件](#开发新插件) · [常见问题](#常见问题) · [已知限制](#已知限制) · [参与贡献](#参与贡献)

</p>

## 是什么

dsh-plugin-kit 是给 DeepSeek Harness（DSH）Web GUI 用的通用插件集合：MCP 服务器配置、Profile 管理、RSS / 新闻聚合、全局搜索、Codegraph 集成、终端面板（本地 + SSH 终端、SFTP 文件传输）、Docker 容器面板（本机 / SSH 主机上的容器与镜像查看，默认只读）、环境变量 / 密钥管理、Prompt 管理，外加一条命令生成新插件的开发脚手架。所有插件都走官方 profile 机制挂载到 `dsh web`，不改 DSH 源码；可以逐个安装，也可以用聚合包一次装齐。

![SFTP 双栏：左本机 / 右远程，行内直传](https://cdn.jsdelivr.net/gh/hyzyn/dsh-plugin-kit@main/docs/dsh-plugin-kit-tty-sftp-dual.png)

![终端面板：侧边栏入口打开 xterm.js 多标签终端](https://cdn.jsdelivr.net/gh/hyzyn/dsh-plugin-kit@main/docs/dsh-plugin-kit-tty.png)

| 能力 | 原生 dsh web | dsh-plugin-kit 全家桶 |
| --- | --- | --- |
| MCP 服务器 | 手改 patch / 命令行 | 可视化卡片 + 连接测试 + 保存后热加载 |
| Profile 管理 | 命令行 | 可视化创建 / 复制 / 重命名 / 删除 |
| RSS 聚合 | 无 | 多源订阅 + 每日「今日值得读」+ 可选 AI 摘要（跟随宿主默认模型，零配置） |
| 全局搜索 | 仅会话标题/内容 | 侧边栏统一全文搜索历史会话、Prompt、MCP 工具与设置面板 |
| Codegraph 集成 | 无 | 代码图谱卡片：索引状态 / 符号搜索 / 调用链 / 影响面 / 一键 sync-index |
| 终端面板 | 无 | 侧边栏「终端」入口 + xterm.js 多标签真实 PTY 终端（vim/htop/dev server）；SSH 直连远程主机（连接簿、指纹钉扎、断线重连）；**SFTP 文件传输**（单窗体 / 左本机右远程双栏直传、拖拽上传）；agent 配套 `tty_*` / `sftp_*` 工具 |
| Docker 容器面板 | 无 | 侧边栏「容器」入口 + 多目标（本机 / SSH）容器列表（搜索 / 状态筛选）、启停删、详情、日志（快照 + **SSE 实时跟随**）、资源占用（快照 + **实时跟随 + sparkline**）、**多目标总览（只读）**、**Compose 项目视图 + 项目级聚合日志**、镜像列表与详情（层 / 构建历史）、**`docker pull` 进度流**、删除 / dangling 清理；**默认只读**，变更与 exec 需显式开关；agent 配套 `docker_*` 工具 |
| 环境变量管理 | 命令行 / 手改配置 | Web GUI 卡片，保存即写入 `process.env` |
| Prompt 管理 | 手改配置 | 可视化编辑 + 版本管理 / A/B 测试 / 导出分享 |
| 插件开发 | 手写样板 | `pnpm create-plugin` 脚手架 + `@hyzyn/dsh-kit` 类型助手与宿主半体共享工具库（HTTP 围栏 / 托管区块 / !!js 表达式） |

## 功能插件

### MCP 服务器配置（@hyzyn/dsh-mcp）

- **做什么**：给 DSH 添加 MCP 服务器，保存后 1~2 秒内热加载为 `mcp__<服务器名>__<工具名>` 工具，模型即可直接调用，无需重启。
- **怎么用**：打开 插件配置里的「MCP 服务器配置」→ 添加服务器（选传输方式）→（建议先点「连接测试」）→ 保存。
- **支持**：两种传输——stdio（本地子进程，如 `npx -y @modelcontextprotocol/server-filesystem`）与 streamable-http（远程服务）；`js:` 前缀表达式（如 `js:process.env.GITHUB_TOKEN`）；启用 / 停用、编辑、删除；状态徽章。
- **存哪里**：`~/.dsh/cordis.patch.yml` 的托管区块。
- **注意**：**不要**手工往该文件里追加插件行，否则启动时报 `duplicate loader entry id` 直接退出。

![MCP 服务器配置插件](https://cdn.jsdelivr.net/gh/hyzyn/dsh-plugin-kit@main/docs/dsh-plugin-kit-mcp.png)

### Profile 管理（@hyzyn/dsh-profile）

- **做什么**：可视化查看 `~/.dsh/profiles` 下的全部 DSH profile，支持创建、复制、重命名、删除，方便维护多套 DSH 环境。
- **怎么用**：打开 插件配置里的「Profile 管理」→ 查看 profile 列表 → 新建 / 复制 / 重命名 / 删除；可为每个 profile 设置端口并复制带 `--port` 的启动命令。
- **支持**：初始化状态、bundle 层与依赖展示；基础模板 / `web` / `headless` 模板新建；复制排除 `node_modules` 与锁文件并自动安装依赖；重命名；端口配置与复制启动命令。
- **存哪里**：直接管理 `~/.dsh/profiles/<name>` 目录。
- **注意**：删除为递归删除，操作前请二次确认；内置的 `web` 默认 profile 不允许删除，`headless` 可以删除；新建后首次使用 `dsh plugin --profile <name> add ...` 时按需安装依赖。

![Profile 管理配置界面](https://cdn.jsdelivr.net/gh/hyzyn/dsh-plugin-kit@main/docs/dsh-plugin-kit-profile.png)

![命令行启动 headless profile 示例](https://cdn.jsdelivr.net/gh/hyzyn/dsh-plugin-kit@main/docs/dsh-plugin-kit-profile-example-headless1.png)

### RSS / 新闻聚合（@hyzyn/dsh-rss）

- **做什么**：订阅多个 RSS / Atom 源，每天自动汇总成一篇「今日值得读」Markdown，并注入 systemPrompt 供模型直接引用。
- **怎么用**：安装后可在侧边栏「新建会话」下方点击「今日值得读」直接查看新闻；也可打开 插件配置里的「RSS / 新闻聚合」勾选内置渠道、添加自定义渠道（保存时即时校验地址）、从 [awesome-rsshub-routes](https://jackyst0.github.io/awesome-rsshub-routes/) 订阅源目录搜索并一键添加，维护新闻分类与聚合设置，保存后自动刷新。
- **内置渠道**：阮一峰、少数派、Solidot、Hacker News、掘金、IT之家、36氪（36氪官方 feed 被反爬拦截，内置为第三方 RSSHub 镜像），勾选即展示、取消勾选即不抓取。
- **自定义渠道**：填写任意 RSS / Atom 地址，保存时真实抓取校验——官网首页、非 feed、抓不到内容的地址会报错且不保存。
- **订阅源目录**：内置 awesome-rsshub-routes 精选目录（官方 RSS 与 RSSHub 路由，98 条 / 12 分类），可搜索 / 按分类筛选并一键加入自定义渠道；快照随插件内置，运行时每 12 小时从上游 OPML 静默刷新。
- **新闻分类**：渠道的分类从「新闻分类」列表里选择；digest（Markdown、systemPrompt、弹窗）按分类分组展示，保存时自动把使用中的分类合并进列表。
- **AI 摘要（可选）**：卡片里开启后，每天 digest 的条目由宿主已配置的默认模型各生成一句中文摘要（无需填 API key；也可在卡片里成对指定 provider/model 用别的模型）。结果按条目缓存 30 天，重复生成不重复计费；单条失败自动回落原文截断，不影响其它条目。摘要同时进 Markdown、弹窗、搜索与 systemPrompt。
- **支持**：RSS 2.0 / Atom 解析、按来源去重、每源条数限制、每日定时生成、启动补生成、自定义输出目录、内置渠道库。
- **存哪里**：`~/.dsh/rss-digest/YYYY-MM-DD.md`（可用 `DSH_RSS_DIGEST_DIR` 覆盖）。
- **注意**：首次安装启动时会联网抓取一次；某个源不可达时会在 digest 的「抓取失败」里列出，不影响其它源。AI 摘要开启时生成耗时取决于模型响应（失败条目回落，不会卡死生成）。

![RSS / 新闻聚合设置卡片](https://cdn.jsdelivr.net/gh/hyzyn/dsh-plugin-kit@main/docs/dsh-plugin-kit-rss-setting.png)

![侧边栏「今日值得读」弹窗：按分类分组，来源带「查看更多」直达官网](https://cdn.jsdelivr.net/gh/hyzyn/dsh-plugin-kit@main/docs/dsh-plugin-kit-rss-view.png)

![查询今日新闻：向模型提问「今日值得读」直接引用当天 digest](https://cdn.jsdelivr.net/gh/hyzyn/dsh-plugin-kit@main/docs/dsh-plugin-kit-rss-query-news.png)

### 全局搜索（@hyzyn/dsh-search）

- **做什么**：在 Web GUI 侧边栏加一个「全局搜索」入口（⌘/Ctrl+K 同样唤出），打开的是命令面板式搜索窗：分组列出最近会话、历史会话全文命中、Prompt、MCP 工具、快捷操作与设置大类。
- **怎么用**：点侧边栏搜索框或按 ⌘/Ctrl+K 打开——**打开即出内容**（最近会话 + 快捷操作 + 设置大类，零延迟，不发请求）；输入关键词后本地候选即时过滤、宿主全文命中异步补齐。↑↓ 选择、↵ 打开、esc 关闭；⌥1-9 直接打开第 N 条最近会话，⌥N / ⌥O / ⌥, 触发新会话 / 打开文件夹 / 打开设置。点会话会打开并尝试定位到匹配文字；点 Prompt / MCP 工具跳对应设置卡片；点设置大类跳到设置窗对应分区。
- **支持**：历史会话全文搜索（走 DSH 自带的 sessionQuery 索引）+ 会话标题即时候选；设置大类实时读客户端 slots 注册表（第三方插件注册的「皮肤」「宠物」「侧边卡片」等同样在列，顺序与设置窗导航一致）；Prompt 读 `~/.dsh/prompts.yml` 托管区块；MCP 工具按 `mcp__` 前缀枚举并标注所属 server；结果关键词高亮；结果数量可配置。
- **存哪里**：无独立配置。
- **注意**：需要宿主已安装 `sessionQuery` 服务；缺失时会话搜索返回空列表。若 `session-query` 全文索引配置为 `openAt: "never"`，历史会话会自动降级为逐会话扫描；会话结果会过滤为当前可跳转的可见会话。「新会话」复用 GUI 自己的 `uiWorkspace.startSession()`；「打开文件夹」在未安装目录选择器插件时不出现。

![全局搜索插件](https://cdn.jsdelivr.net/gh/hyzyn/dsh-plugin-kit@main/docs/dsh-plugin-kit-search.png)

![全局搜索的检索结果（最近会话 / 历史会话 / Prompt / MCP 工具 / 设置分组）](https://cdn.jsdelivr.net/gh/hyzyn/dsh-plugin-kit@main/docs/dsh-plugin-kit-search-query.png)

### Codegraph 集成（@hyzyn/dsh-codegraph）

- **做什么**：代码图谱集成——插件配置里的「Codegraph」卡片提供索引状态、符号搜索、callers / callees / impact 查看和一键 sync / index；安装后自动向 systemPrompt 注入 CodeGraph 使用指引，模型在已索引项目里优先用 `codegraph_explore` / `codegraph explore` 查询代码而不是 grep / read。
- **怎么用**：打开 插件配置里的「Codegraph」→ 查看索引状态、搜索符号、点击结果查看源码与调用链 / 影响面、手动 Sync / 重建索引。
- **支持**：索引状态（版本、文件 / 符号 / 边数量、最后索引时间、待同步变更）；符号搜索与 node / callers / callees / impact 详情；**默认路径跟随当前活动会话的工作目录**（切换项目会话自动切换，手动输入可临时覆盖）；一键增量 sync 与全量重建。
- **MCP 托管（默认开）**：DSH 的 MCP 客户端不声明 roots，`codegraph serve --mcp` 只能从工作目录向上找 `.codegraph/`——宿主若从家目录启动，模型调用 `mcp__codegraph__*` 会拿到 "No CodeGraph project is loaded"。本插件自动在 `~/.dsh/cordis.patch.yml` 托管 codegraph MCP 服务器行并把 cwd 对齐默认项目路径（卡片「设为默认项目」一键切换，保存即热重启 MCP 服务器）；已在 MCP 卡片配置过的行只补 cwd 不动其它字段。可用 `mcpIntegration: false` 关闭。
- **存哪里**：索引在项目 `.codegraph/` 目录（由 `codegraph index` 生成）；默认项目路径与各开关持久化在本插件 entry 的 profile 配置（写进当前 profile 的 `cordis.patch.yml` 用户层）。
- **注意**：查询目标项目需要先有 Codegraph 索引；未索引项目会返回指引改用常规工具。索引 / 重建为本地 CLI 操作，消耗真实磁盘与 CPU。一台 codegraph MCP 服务器同一时刻只挂载一个默认项目，其它已索引项目可在工具调用里传 `projectPath` 查询。
- **兼容与调优**：当前适配基线 DSH `0.1.7-rc.1`（声明 `peerDependencies: @deepseek-ai/dsh ^0.1.7-rc.1`）+ codegraph CLI `1.5.0`；CLI 命令与旗标见包内 README。大仓库全量重建可调 `indexTimeoutMs`（默认 600s，查询档 `cliTimeoutMs` 默认 60s），CLI 拒绝索引家目录 / 文件系统根时开 `indexForce`。

![Codegraph 设置卡片](https://cdn.jsdelivr.net/gh/hyzyn/dsh-plugin-kit@main/docs/dsh-plugin-kit-codegraph.png)

### 终端面板（@hyzyn/dsh-tty）

- **做什么**：在 Web GUI 侧边栏加一个「终端」入口，点击打开大弹窗，内嵌 xterm.js 全交互终端（node-pty 真实 PTY），支持多标签页，可运行任意命令与 TUI