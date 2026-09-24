# TapTap Open API MCP 服务器

> 基于 Model Context Protocol (MCP) 的 **TapTap 小游戏和 H5 游戏**服务器，提供排行榜、分享、多人联机、云存档，以及当前游戏 DC 数据查询、统计概览与评价操作能力，并支持 **OAuth 2.0 零配置认证**。

🔐 **零配置 OAuth** | 📚 **完整文档** | 🎯 **丰富 Tools & Resources** | 🌍 **小游戏 & H5** | 📦 **单文件 Bundle**

## ✨ 核心特性

- **🔐 零配置认证** - OAuth 2.0 Device Code Flow，扫码即用
- **📖 完整 API 文档** - 6 个排行榜 API + 详细代码示例
- **⚙️ 服务端管理** - 创建/管理排行榜，自动处理 ID
- **🎮 H5 游戏支持** - 上传、发布、状态查询
- **📺 广告接入闭环** - 仅用于 TapTap 小游戏/H5，自动查询广告状态和广告位 ID；方向缺失时先刷新
  服务端应用信息，确认仍未设置后引导用户选择方向，不与 Maker MCP 混用
- **🧭 当前游戏 DC 能力** - 商店/评价/社区统计概览、商店快照、论坛内容、评价列表、评价点赞、官方回复
- **🦞 OpenClaw Plugin** - 提供一个原生 OpenClaw plugin 子包，内部复用 TapTap MCP 运行时并暴露 raw JSON 工具 + bundled skill
- **🚀 三种传输模式** - stdio（本地）、SSE（远程/实时）、HTTP（兼容）
- **🔌 多客户端并发** - 独立会话管理，无限并发
- **📦 单文件 Bundle** - 零依赖，包体积减少 96%（567 KB）
- **🤖 智能引导** - AI Agent 自动验证前置条件，主动询问用户选择

**NPM**: [@taptap/instant-games-open-mcp](https://www.npmjs.com/package/@taptap/instant-games-open-mcp)
**Maker NPM**: [@taptap/maker](https://www.npmjs.com/package/@taptap/maker)

Maker 支持[本地控制台](docs/MAKER_CONSOLE.md)管理项目、构建和 Git 历史，并在文件不冲突时拉取远端代码；项目页可查看所有项目
共用的本机 Runtime 与独立 Lua LSP 安装状态，构建页可单独检查 Lua，构建前默认可选检查。构建失败信息
默认展开。构建与本地预览快捷操作会自动切换到对应工作页。构建页按当前阶段显示真实进度，
构建详情与 Runtime 日志使用整行宽度；
[本地窗口预览](docs/MAKER_LOCAL_PREVIEW.md)会在启动 Runtime 前区分普通单机、联机/server
和无配置新项目：不依赖资源索引的单机直接加载原目录；存在资源/构建配置、资源元数据、
Windows 旧 dist、联机/server 或缺配置的项目使用受管理副本生成
本轮 manifest。所有需要准备产物的项目在 Windows/macOS 均通过仅本机可访问的资源服务加载，
统一读取配置和资源索引；单机不会因此申请测试服。Windows 使用每轮独立的短临时下载缓存，退出后清理。
联网项目复用 Maker 登录，自动连接线上测试服，无需扫码；服务端改动仍需
提交构建后生效，联机项目缺少构建产物时直接报错，不静默降级为离线窗口。
新项目缺少发布配置也可预览：默认入口为 `scripts/main.lua`、窗口为横屏 1920×1080，
仅在临时副本补齐缺省配置，不修改项目；已有方向和已保存窗口设置优先。
公共资源在多个 source 中转引同一资源时，预览会校验本轮索引并显示警告，不再误判为构建失败；
真正的资源冲突、其他 Builder 错误及不完整产物仍阻止启动。
“文档 / Skill”页按分类浏览 Maker 内置及当前项目资料，支持目录搜索与 Markdown 阅读。
任务执行中可切换项目，日志和后续操作仍归属原项目；首次点击本地预览可在确认安装 Runtime 后继续启动。
主操作区提供“测试二维码”，缺少名称、分类或首次发布方向时在确认框补齐；
需要同步配置时明确确认提交、推送本地改动，再由二维码工具完成构建上传，不额外重复构建。
Lua 检查开关与构建结果集中在远端构建区域，窗口设置默认折叠，通栏日志支持清理、复制与自动换行。
任务列表默认显示摘要，最新失败与运行中任务展开；二维码结果及日志按项目展示。
需要选择开发者时弹窗确认；成功后弹出大图二维码，关闭后可从任务中重新查看。取消不执行操作。
本地预览异常可确认提交问题反馈，自动附带脱敏日志和环境信息，并按出错环节分类；
自动上传复用现有 GitHub CLI，需本机已安装并登录；提交状态与 Issue 链接显示在原任务中。
控制台链接无需 token，服务运行时直接打开本机地址即可使用，支持刷新、新标签和项目选择。
标题旁提供 Maker MCP 版本选择，支持查看最近 5 个版本并确认更新；独立发行复用 CLI
更新流程，插件发行仍通过插件市场更新，安装后重新连接 MCP 生效。
控制台提供 16:9、21:9、4:3 窗口预设及可保存的自定义尺寸；横竖屏默认读取项目配置，
未配置时使用横屏，也可随时手动选择。设置按项目保存，下次启动或刷新预览时生效，不修改发布配置。
受管理 Runtime 在安装和启动时会自动补齐引擎所需目录与中文兜底字体；项目自带字体仍按项目隔离，
不会写入所有项目共用的 Runtime。
相同 Maker 版本从不同 AI IDE 打开时复用同一个用户级控制台；Windows 使用系统进程代理启动，
避免 AI 命令结束时连带关闭控制台服务。本地预览 supervisor 共用该启动方式；
意外断开后确认两个预览进程均已退出时，可直接重新启动，无需手动删除会话文件。
FrameCrate 控制台集成已改为通用插件注册与持久内嵌标签页（2026-09-16，本地验证及独立复核完成），
不再以独立浏览器标签作为控制台入口。显式设置 `FRAMECRATE_STUDIO_DIR` 指向已安装的
framepacker Studio，按已登记项目嵌入完整本地编辑器与 AI 工作流；切换项目或标签应保留编辑现场。
控制台不安装或下载 Studio，不提供 ZIP 安装或插件市场。协议与验收边界见
[本地控制台文档](docs/MAKER_CONSOLE.md)。

## TapTap Maker 客户端插件

[`plugins/taptap-maker`](plugins/taptap-maker) 是插件专属安装与下载页面。Codex 和 WorkBuddy
插件共用独立插件版本，当前值读取 `config/maker-plugin-version.json`；内置 Maker MCP 版本读取
`config/maker-version-policy.json`，两条版本线互不覆盖。插件内置 Maker MCP 单文件运行时、CLI、
Skills 和排障文档，不通过 npm/npx 下载或启动 Maker。

对外安装应把对应渠道的 GitHub Release 页面交给 AI，由页面中的统一安装指南选择客户端 ZIP、
校验并执行安装前后的旧 MCP 兼容检查。下面的仓库 marketplace 命令仅用于维护者从源码验证；
执行 `marketplace add` 前，必须用刚生成的插件 CLI 完成下文同样的安装前检查和迁移。

```bash
npm run maker:codex-plugin:prepare
node plugins/taptap-maker/dist/maker.js plugin inspect --client codex --json
node plugins/taptap-maker/dist/maker.js plugin migrate --client codex --confirm --json
node plugins/taptap-maker/dist/maker.js plugin inspect --client codex --json
codex plugin marketplace add taptap/instant-games-open-mcp --ref main \
  --sparse .agents/plugins --sparse plugins/taptap-maker
codex plugin add taptap-maker@taptap-maker
node plugins/taptap-maker/dist/maker.js plugin migrate --client codex --confirm --json
node plugins/taptap-maker/dist/maker.js plugin inspect --client codex --json
```

插件 manifest 和 marketplace 版本读取 `config/maker-plugin-version.json`；bundle 运行时身份继续读取
`config/maker-version-policy.json`。运行 GitHub Actions 中的 `Prepare Maker Plugin Release` 会自动把
插件 patch 加一、重新生成两端产物并创建 PR；合并后 `Publish Maker Plugin` 自动发布两份 ZIP、
`INSTALL.md`、`SHA256SUMS` 和机器可读发布清单，不触发 npm 发布。

旧用户安装插件前，先用 ZIP 解压目录或本地生成目录中的插件 CLI 执行
`taptap-maker plugin inspect --client codex --json`。如果旧的独立 Maker MCP 仍启用，向用户说明
已发现重复注册并直接执行
`taptap-maker plugin migrate --client codex --confirm --json`。迁移只写入 `enabled = false`，保留
原配置、最近备份、PAT、项目绑定和游戏文件；插件安装请求即为这次兼容迁移的授权，不再单独询问，
重复执行也是幂等的。检查返回 `ambiguous` 时必须在安装前停止；安装完成后必须再次迁移并检查，
只有状态为 `disabled` 或 `not_found` 才能报告插件可用。需要卸载插件并恢复旧 MCP 时，仍要先取得明确确认，再执行
`taptap-maker plugin restore --client codex --confirm --json`。
如果本次安装中任一次迁移实际禁用了旧注册，但插件安装或验证失败，则用同一 restore 命令自动回滚；
回滚前先移除本次已安装的插件并确认其不再启用，不能在插件仍启用时恢复旧 MCP。原本已禁用、未找到
或不是本次迁移的注册不恢复。安装前迁移失败时立即停止，不进入插件安装。

插件模式初始化使用 `taptap-maker init --skip-mcp-install`，避免 CLI 再写一份独立 MCP 配置。
插件更新通过插件内专用 `update-taptap-mcp` Skill 和 Codex marketplace 完成，不执行 npm/npx
或独立 `taptap-maker upgrade`。旧 MCP 恢复前会核对迁移时记录的注册指纹，同名注册已被替换时
保持禁用并返回 `not_owned`。插件故障上报读取插件自己的 `.mcp.json` 并验证当前 bundle；独立
Maker MCP 仍沿用原有用户配置和 self runtime 诊断。

WorkBuddy 插件是独立产物，位于
[`plugins/workbuddy/taptap-maker`](plugins/workbuddy/taptap-maker)，通过共享的 CodeBuddy 插件
规范聚合 Maker MCP、CLI、Skills 和两个快捷命令：

```text
/taptap-maker:create-project
/taptap-maker:sync-project
```

两个入口都要求当前 WorkBuddy workspace 为空目录。插件启动器优先解析 WorkBuddy managed
Node.js（包括 Windows 上未加入 PATH 的 `node.exe`），必要时才回退系统 Node.js；运行插件内
`${CODEBUDDY_PLUGIN_ROOT}/dist/maker.js`，不依赖 npm/npx。仓库 marketplace 位于
`.codebuddy-plugin/marketplace.json`：

```text
/plugin marketplace add <REPOSITORY_ROOT>
/plugin install taptap-maker@taptap-maker
/reload-plugins
```

上述 marketplace 只用于从仓库源码验证。正式 WorkBuddy 市场发布 ZIP 直接以插件内容为根，
不包含额外的 `taptap-maker/` 或 `plugins/workbuddy/taptap-maker/` 目录；根目录包含
`.codebuddy-plugin/plugin.json`、`.mcp.json`、`README.md` 和 `SKILL.md`，所有文件的父目录深度
最多为两层。普通用户通过 WorkBuddy 官方插件市场安装，不把发布 ZIP 当成本地 marketplace。

WorkBuddy 旧独立 MCP 的迁移使用 `--client workbuddy`，只把旧注册的 `disabled` 设为 `true`，
同时支持幂等检查和确认式恢复。插件更新通过 WorkBuddy `/plugin` 完成。

## 🦞 OpenClaw Plugin（实验中）

仓库内提供了一个可独立使用的 OpenClaw plugin 子包：

- [`packages/openclaw-dc-plugin`](packages/openclaw-dc-plugin)

这个子包的设计目标是：

- 让 OpenClaw 用户只安装一个 plugin
- plugin 内部复用 `@taptap/instant-games-open-mcp` 运行时
- 对 OpenClaw 暴露 raw JSON 工具
- 同时内置 `taptap-dc-ops-brief` skill，让模型自己做简报解读

说明：

- 主包里的 `*_raw` tools 默认不会暴露给普通 MCP 客户端
- 只有设置 `TAPTAP_MCP_ENABLE_RAW_TOOLS=true` 时才会注册
- OpenClaw plugin 会自动打开这个开关，因此插件用户不需要额外配置

详见：

- [OpenClaw Plugin 说明](docs/OPENCLAW_PLUGIN.md)

## 🛠️ TapTap Maker 本地开发（CLI-first）

Maker 本地开发独立发布为 `@taptap/maker`。首次配置推荐直接运行：

```bash
npx -y @taptap/maker init
```

CLI 负责一次性流程：Git 检查、Python 和 maker-lua-lsp 本地 Lua 诊断环境检查、CLI 登录、
TapTap token 换取、app 列表选择或新建 Maker 项目、Maker Git clone、AI dev kit 准备、MCP 配置写入与基础验证。Python 环境准备连续 3 次失败时，
初始化会暂停在登录、项目拉取和 MCP 配置之前；修复后重新运行 `taptap-maker init`。首次安装，或 Maker MCP 包/
静态工具 schema 发生变化后，Claude Code / Codex / Cursor / Trae / OpenCode / WorkBuddy 通常需要重连或刷新一次 MCP，
才能加载新的 MCP tools；DeepSeek Harness（DSH）会监听用户补丁并热重载，不要求重启 IDE。单纯绑定或切换 Maker 项目
不会修改用户级 MCP 配置，也不需要重启会话或新开对话。当前终端里的
CLI 初始化流程可以继续完成到 PAT 鉴权和项目绑定。

常用 CLI：

```bash
taptap-maker init
taptap-maker login
taptap-maker doctor
taptap-maker apps --json
taptap-maker install
taptap-maker agents update
taptap-maker upgrade
taptap-maker mcp verify
npx -y --package @taptap/maker@<exact-version> taptap-maker mcp report --ide <client> --target-dir <project> --context-stdin --consent --json
taptap-maker dev-kit update
taptap-maker user-skills pull --target-dir <project>
```

普通初始化、clone、下载或拉取远端项目的标准命令是 `taptap-maker init`，CLI 会展示 app 列表，
让用户选择已有 app 或 `0`/`new`。`--create` 只用于用户明确要求创建新 Maker 项目的场景。
如果需要创建新 Maker 项目，仍从 `taptap-maker init` 进入。app 列表底部会固定显示
`0. Create a new Maker project`，输入 `0` 或 `new` 后填写项目名称；自动化场景可用
`taptap-maker init --create --name "my-local-game"`。当前目录已绑定 Maker 项目时，不允许在同一目录
创建并覆盖绑定；请先切到一个新的独立目录再运行 `taptap-maker init`。

`taptap-maker login` 是 CLI 登录入口；它会按需打开 Maker 授权页，CLI 轮询