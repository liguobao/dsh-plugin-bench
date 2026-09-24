# Dockyard DSH

**A native account-pool and provider plugin for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (`dsh`).**

[中文](#中文) · [English](#english)

> **Current status / 当前状态:** Developer preview · **macOS DMG available** · **Windows EXE built; upload in progress.**

## 中文

### Dockyard DSH 是什么

Dockyard DSH 把多个官方 OAuth / 官方客户端会话接入 DeepSeek Harness，提供一个统一的账号池、模型目录、额度状态和 provider-native 请求入口。它是 DSH 的原生 bundle/plugin，不需要另起一个代理网关，也不把 provider 逻辑塞进 DSH 核心。

当前包含的 provider 模块：

- **Codex** — 官方浏览器 OAuth、CLI fallback 和原生 Responses 请求链路。
- **Antigravity** — Google 官方浏览器 OAuth、官方本机会话、实时模型目录、额度/credits 和原生 Gemini SSE 请求链路。
- **Grok** — xAI 官方浏览器 OAuth、CLI fallback、实时模型目录、官方 Build credits 周期和 provider-native streaming 请求。额度读取使用官方 `/billing?format=credits`（转发 `GetGrokCreditsConfig`）；若上游只返回周期，剩余值保持未知。
- **Claude** — Claude 官方浏览器 OAuth（支持带 state 的手动回调地址/授权码）、CLI fallback 与原生请求适配。
- **Cursor** — Cursor 官方浏览器登录轮询、CLI fallback 与原生请求适配。

如果对应的官方客户端、CLI 或 OAuth 源没有安装、没有登录，Dockyard 会返回明确的 unavailable/degraded 状态；不会用硬编码的账号、模型、版本、套餐或额度伪造可用结果。

### 主要功能

- 在 DSH 内使用 `/dockyard` 命令管理账号和 provider。
- 点击“登录添加账号”直接打开 provider 官方浏览器授权页，选择账号并安全导入账号池；provider 不可用时保留 CLI fallback。
- 扫描本机已有的官方登录态；扫描和新增账号是两个独立操作，已有账号不会被“新增”静默重复导入。
- 支持手动选择、sticky session、round-robin 和 failover 账号池策略。
- 读取 provider 返回的实时模型目录、推理档位、套餐和额度窗口。
- 所有命令、模型选择和 LLM 生成都读取同一个 Dockyard runtime，不维护第二套账号池或额度缓存。

### 平台支持：macOS 已发布，Windows 构建完成

**当前 0.1.2 版本正在整理；macOS DMG 已提供，Windows EXE 已完成构建，待上传到 v0.1.2 Release。**

macOS 完整功能依赖以下原生能力：

- 凭据存储使用 macOS Keychain 和 Swift helper。
- 浏览器 OAuth 由 DSH GUI 打开 provider 官方授权页面，并使用 PKCE、state 校验和 loopback/manual-code 回调；CLI fallback 才使用官方 CLI。
- 扫描模式仍可读取 Cursor、Antigravity 等 provider 的 macOS 官方桌面端或本机 CLI 会话状态。

Windows 版本已完成 EXE 构建，待上传到 v0.1.2 Release；上传完成后再进行发布页下载验证。

### macOS 独立应用与 DMG

如果不想手动安装 Node.js、pnpm 或 DSH，可以直接下载自带完整运行时的 macOS 通用 DMG：

[下载最新 Dockyard DSH DMG](https://github.com/AITabby/dockyard-dsh/releases/latest/download/Dockyard-DSH-macos-universal.dmg)

也可以在 Mac 上自行构建：

```sh
./apps/macos/build-dmg.sh
```

DMG 内置 Node.js、DSH CLI、完整 `web` profile 和 Dockyard 插件；双击 App 即可运行，不需要另外安装 Node.js、pnpm 或 DSH。它会在原生 WebKit 窗口中显示内置的 DSH Web profile；OAuth 授权页会交给系统默认浏览器打开。当前构建包含 Apple Silicon 和 Intel 两个架构。详细说明见 [`apps/macos/README.md`](apps/macos/README.md)。

仍需注意：这是 macOS 专用、当前为本地 ad-hoc 签名的开发预览；某些 provider 的官方 CLI 扫描/兼容性 fallback 仍可能需要对应 CLI，Antigravity 浏览器授权仍需要配置官方 OAuth client 信息。

### 一条命令安装 Dockyard plugin

如果已经有 Node.js，直接把下面这一行交给终端或智能体执行即可：

```sh
npx -y @dockyard-dsh/install@latest
```

它会自动检查 DSH 和 pnpm，并把预构建的 Dockyard host/client bundle 安装到默认 `web` profile。安装完成后重启 DSH Web。

### 从源码安装 Dockyard plugin / Web profile

Dockyard DSH 作为源码 plugin 安装到已有 DSH Web profile 时，才需要先安装 DSH CLI，并确认 `dsh` 命令可用。

当前上游 DSH CLI 的 npm 安装方式：

```sh
# DSH 当前是 developer preview；请使用上游要求的 Node.js 版本。
# 当前上游 package.json 要求 Node 22.19+ 的 22.x，或 Node 24+。
npm install --global @deepseek-ai/dsh
npm install --global pnpm

dsh --version
pnpm --version
```

上游安装和兼容性变化以 [DeepSeek Harness 官方仓库](https://github.com/deepseek-ai/deepseek-harness) 为准。当前 bundle 已按 `@deepseek-ai/dsh@0.1.1-rc.2` 验证。DSH 仍处于 developer preview，升级已有 DSH_HOME 前请先备份数据，并先用独立的 `DSH_HOME` 验证。

#### 最简便的方式：直接安装到 DSH Web profile

`web` 是 DSH 自带的完整 Web profile；不要新建只包含 Dockyard bundle 的空 profile，否则不会启动 Web GUI。

```sh
dsh plugin --profile web add github:AITabby/dockyard-dsh
dsh web
```

默认访问 `http://127.0.0.1:3080`。首次启动可先检查组合配置：

```sh
dsh web --dump-config
```

如需固定版本，建议 pin 到已验证的 commit：

```sh
dsh plugin --profile web add github:AITabby/dockyard-dsh#<commit-sha>
```

当前发布 commit 已提交可运行的 host/client bundle，安装时不执行 `prepare`，因此 GitHub 直装不需要额外的 `allowBuilds` 配置。若你 pin 到旧 commit，或 pnpm 明确报告了其他构建脚本，请只在检查源码后按终端提示配置对应 profile 的 `pnpm-workspace.yaml`。

#### 需要本地修改时：克隆后安装

```sh
git clone https://github.com/AITabby/dockyard-dsh.git
cd dockyard-dsh
npm install
npm test                 # 可选：验证环境
npm run build            # 修改 source 或 bundle 过期时需要

dsh plugin --profile web add .
dsh web
```

要隔离测试、不影响默认 DSH home：

```sh
DSH_HOME=/tmp/dockyard-dsh-home dsh plugin --profile web add .
DSH_HOME=/tmp/dockyard-dsh-home dsh web --dump-config
DSH_HOME=/tmp/dockyard-dsh-home dsh web
```

仓库已提交 `packages/dsh-plugin/dist/index.mjs` 和 `packages/dsh-plugin/lib/client.js`；普通用户不需要先运行测试或构建即可使用已发布 commit。

### DSH 内的命令

在运行中的 DSH profile 中：

```text
/dockyard status
/dockyard scan [provider]
/dockyard add [provider] [candidateId]
/dockyard login <provider>
/dockyard refresh [provider]
/dockyard models <provider>
/dockyard policy <provider> <manual|sticky_session|round_robin|failover> [accountId]
/dockyard use <provider> <accountId>
/dockyard remove <provider> <accountId>
```

新增账号流程是 `/dockyard login <provider>`（直接打开官方浏览器 OAuth）；如果要导入已有本机登录态，则使用 `/dockyard scan <provider>` 后再 `/dockyard add <provider>`，最后用 `/dockyard status` 和 `/dockyard models <provider>` 检查实时状态。

### 官方浏览器 OAuth / active session 边界

- **Codex、Antigravity、Grok、Claude、Cursor** 的“登录添加账号”默认由 DSH 直接打开官方浏览器授权页，不要求本机先安装 CLI；CLI 仅作为兼容性 fallback。
- Codex 使用 loopback PKCE；Antigravity 使用 Google loopback OAuth；Grok 使用 xAI loopback OAuth；Cursor 使用官方 `loginDeepControl` + `/auth/poll`；Claude 使用官方网页回调，手动输入时要求粘贴带 `state` 的完整回调地址或 `code#state`。
- Antigravity 的 Google OAuth client ID/secret 必须通过 `DOCKYARD_ANTIGRAVITY_CLIENT_ID` 和 `DOCKYARD_ANTIGRAVITY_CLIENT_SECRET` 提供，仓库不内置凭据；需要浏览器 OAuth 时，先在启动 DSH 的 shell 中设置这两个环境变量（或写入 `~/.zshrc`），不要提交到仓库。
- **扫描**仍可读取本机已有的官方客户端/CLI 会话；扫描和浏览器新增账号不会互相替代。
- provider 的 OAuth endpoint、token response 或授权范围变化时，Dockyard 会显示 unavailable/degraded，不猜测未验证的字段。

### 凭据和安全边界

- 原始 OAuth/token 不写入 Git、账号池快照或页面状态；运行时只传递 opaque credential reference。
- 浏览器 OAuth 的 refresh token 持久化在安全凭据存储中；支持 refresh 的 provider 会在重启后自动刷新短期 access token，只有 provider 撤销 refresh token 或改变协议时才需要重新授权。
- macOS 默认使用 Keychain；非 macOS 默认 credential store 会 fail closed，不会静默退回不安全的内存存储。
- 额度、模型、套餐、账号身份和过期时间都来自 provider 的实时结果；provider 不返回时保持 `unknown`/`null`。
- 发布和提 issue 前请阅读 [`SECURITY.md`](SECURITY.md)，不要提交 token、OAuth 文件、Keychain 值或包含敏感信息的日志。

### 开发与验证

```sh
npm install
npm test
npm run build
npm run build:plugin
npm pack --dry-run
```

发布包的关键内容是：

```text
packages/dsh-plugin/dist/index.mjs   # Node/host bundle
packages/dsh-plugin/lib/client.js    # browser client bundle
packages/dsh-plugin/cordis.patch.yml # DSH bundle layer
```

`npm pack --dry-run` 应只显示发布入口、client bundle、patch、必要的 package metadata 和安全说明。修改 provider source 后，重新执行 `npm run build`，再提交更新后的构建产物。

### 项目结构

```text
packages/core/              模块生命周期、契约、事件和 DSH route
packages/account-pool/      账号发现、选择、健康状态和 credential reference
packages/runtime/           一个共享的 Dockyard runtime
packages/dsh-plugin/        DSH bundle、LLM adapter、命令和 client UI
packages/vault/             macOS Keychain backend
modules/provider-*/         各 provider 自己的 OAuth、目录、额度和 native transport
tests/                      安全、生命周期、provider 和 runtime 测试
```

核心原则是：provider-specific 逻辑留在 provider module，账号选择留在 runtime，host 只消费稳定契约。不要在 host 中新增 provider 特判，也不要把动态 provider 数据写成常量。

### 已知限制

- DSH 本身仍处于 developer preview，上游可能发生 breaking changes。
- provider 的官方 CLI、客户端路径、OAuth 返回字段和额度接口都可能变化；Dockyard 对缺失字段保持未知。
- 浏览器 OAuth 多账号依赖 provider 官方授权页和 token response；如果 provider 暂停或改变该流程，必须重新验证 endpoint，而不是猜测协议。
- Windows EXE 已完成构建但仍在上传和验证中；在发布页出现并完成验证前，请勿用于 Windows 生产环境。

## English

### What it is

Dockyard DSH is a native DeepSeek Harness bundle/plugin that connects official OAuth and official client sessions to one shared account pool, model catalog, quota view, and provider-native request path. It does not require a second proxy gateway and it does not put provider-specific branches into the DSH core.

Current provider modules:

- **Codex** — official browser OAuth, CLI fallback, and native Responses transport.
- **Antigravity** — Google browser OAuth, official local session, live model catalog, quota/credits, and native Gemini SSE transport.
- **Grok** — xAI browser OAuth, CLI fallback, live model catalog, official Build credits periods, and provider-native streaming.