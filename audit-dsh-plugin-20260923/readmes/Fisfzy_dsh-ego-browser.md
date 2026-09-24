# ego-browser — 看得见的 Agent 浏览器

<p align="center">
  <a href="https://dshfind.com/zh/plugins/Fisfzy/ego-browser?ref=badge"><img src="https://dshfind.com/api/badge/Fisfzy/ego-browser?lang=zh" alt="dshfind - ego-browser"></a>
  <a href="https://dshfind.com/zh/plugins/Fisfzy/ego-browser"><img src="https://dshfind.com/api/card/Fisfzy/ego-browser?lang=zh" alt="ego-browser card"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/DSH-%3E%3D0.1.2--rc.1-blue" alt="DSH >= 0.1.2-rc.1">
  <img src="https://img.shields.io/badge/DSH--better--sidebar-%3E%3D0.12.2(optional)-red" alt="dsh-better-sidebar >= 0.12.2 (optional)">
  <img src="https://img.shields.io/badge/Node-%3E%3D22-brightgreen?logo=node.js&logoColor=white" alt="Node >= 22">
</p>

> **仓库**：`github.com/Fisfzy/ego-browser`｜版本历史见 [CHANGELOG.md](CHANGELOG.md)｜详情页：[dshfind](https://dshfind.com/zh/plugins/Fisfzy/ego-browser)

### 版本兼容矩阵

| 依赖 | 最低版本 | 推荐版本 | 说明 |
|---|---|---|---|
| **DSH** (DeepSeek Harness) | `0.1.2-rc.1` | `≥ 0.1.2-rc.1`（截至 v0.1.5-rc.2 验证通过） | `engines.dsh` 声明地板；peer 依赖同步锁定 `>=0.1.2-rc.1`。0.1.0-rc.x / 0.1.1-rc.x 请使用 v0.8.0 及更早版本 |
| **dsh-better-sidebar** | `0.12.2`（可选） | `≥ 0.17.1` | 未安装时自动回退浮动观察球；`< 0.12.2` 可运行但外部链接拦截（`urlTarget`）静默降级 |
| **Node.js** | `22` | — | harness 环境自带 |

**DSH 全版本适配说明**：本版本 v0.8.3 已通过源码审计确认与 DSH `0.1.2-rc.1` 至 `0.1.5-rc.2` 全部发布版本兼容（`defineTool`、`ctx.tools.register`、`ctx.subprocess.spawn`、`ctx.webServer.register`、`ctx.inject`、`ModuleLoader` CJS factory、`cordis.patch.yml` 等核心 API 在 v0.1.0-rc.7 → v0.1.5-rc.2 无破坏性变更）。0.1.2-alpha.x 系列按声明可装但未实测。

**dsh-better-sidebar 适配说明**：ego-browser 通过 `ctx.betterSidebar` 服务（try-catch 防御性获取）注册侧边栏 Tab 并监听外部链接。关键 API 引入版本：

| API | ego-browser 用法 | better-sidebar 引入版本 |
|---|---|---|
| `registerTab()` / `openTab()` / `ctx.betterSidebar` | Tab 注册 + 打开 | v0.9.0+ |
| `TabDescriptor.single` | 单实例 Tab | v0.9.0+ |
| `TabDescriptor.urlTarget` | 外部链接拦截 | **v0.12.2+**（低于此版本链接拦截静默失效） |

---

**DSH 版本支持详情**：v0.8.2 → v0.8.3 主要变更：合并 6 个社区 PR（root/xvfb/macOS headless 适配、rc.1 兼容、Windows 稳定性），修复无认证 `/api/ego/*` 路由安全漏洞、无 dsh-better-sidebar 宿主 client 启动失败（#29）、Windows 冷启动回归（#22 引入的 Xvfb 误判），并修复 gateway 设置白名单缺 `egoCliArgs`/`chromeArgs`。适配点：client 运行时改名（`@deepseek-ai/dsh-client-store`）、client 模块注册 id 与装载行名按声明包名、`dsh.client.inject` 仅声明真实模块图行、`webServer` 以嵌套注入交付（可选服务），并同步侧边栏 Tab（dsh-better-sidebar）模式。

**侧边栏支持（[dsh-better-sidebar](https://www.npmjs.com/package/dsh-better-sidebar)）**：当宿主安装了 `dsh-better-sidebar`（推荐 ≥ v0.12.2）时，实时观察窗注册为**侧边栏原生 Tab**——「Agent 浏览器」出现在侧边栏「+」菜单中，点击即打开并随侧边栏抽屉固定展示；agent 首次调用 `ego_*` 工具时会自动打开该 Tab（v0.8.5 起按调用会话作用域打开，多会话不再弹错位置）。未安装 `dsh-better-sidebar` 时自动回退为右下角**浮动观察球**（`#dsh-ego-fab`）模式。两种形态共用同一套 SSE 实时推流 / 点击 / 输入 / 下载捕获能力。观察窗还提供一个「弹出窗口」按钮：无头（headless）运行的 agent 浏览器可一键替换为同 Profile 的有头窗口（标签页保留），方便手动接管。

**登录态导入（v0.8.5 新增）**：设置页「从系统浏览器导入登录态」或工具 `ego_login_import`，把你日常 Chrome/Edge/Brave 里的登录 cookie **按域名**复制进 agent 浏览器（真实二进制无头启动 + CDP 透传读取，兼容 Chrome 127+ 的 App-Bound Encryption，不做离线解密；源浏览器运行中可选择优雅关闭后导入，窗口下次启动自动恢复）。cookie 值不出现在任何日志与输出中；导入前自动备份源 cookie 库，异常清空自动还原。配合默认的磁盘持久化 Profile，导入的登录态跨重启永久保留。

把 [CitroLabs/ego-lite](https://github.com/CitroLabs/ego-lite)（给 AI Agent 用的 Chromium）接入 DeepSeek Harness：以 **33 个结构化 `ego_*` 工具**驱动浏览器，并配一套**实时观察前端口**——agent 后台操作网页时，你能像看直播一样看到它正在浏览的每个页面，还能直接操作它。

**一点私藏的独特之处（self-observation）**：agent 用的就是这一个 Chromium——连它操作 **DSH 自身**（管理会话、任务看板、调设置）时，观察窗也实时显示、你能随时接手。不只是"看得见 agent 在网页上干活"，连 agent 操作 DSH 界面本身都是全程可见、可掌控的。

**开箱即用**：插件包内置 ego 运行时（`runtime/`，MIT，见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)）——无需克隆官方仓库、无需手动构建，`--no-sandbox` wrapper 随包自带，root / Docker / 无显示器一键跑。

---

## 我们的真正优势（不是口号，是能对照代码和竞品核实的能力）

同样把 ego-lite 接进 DSH，市面上已有同类插件用它**只做了 3 个工具**——一个 `run` 脚本、一个 `help` 指南、一个 `status` 体检，浏览器仍是**后台黑盒**。`ego-browser` 走的是另一条路：**把黑盒打开，并且一上来就把"看"和"控"的能力做到位**。

| 能力 | ego-browser（本仓库） | 同类插件（Da1dr1em/dsh-ego-browser） |
|---|---|---|
| 结构化工具数 | **32 个**，职责单一、可确定性调用 | **3 个**（`run`/`help`/`status`） |
| 实时观察窗（CDP JPEG / FFmpeg H.264 双后端 + 标签条 + 历史抽屉） | ✅ 有 | ❌ 无 |
| 监控窗鼠标**直接操作**真实浏览器（点击/拖拽/滚动回传 CDP） | ✅ 有 | ❌ 无 |
| worker 单实例守卫 + 崩溃/重复自愈 | ✅ 有 | ❌ 无 |
| 下载捕获 `ego_download` / 人机验证检测 `ego_captcha`/`ego_page_info` | ✅ 有 | ❌ 无 |
| 平台自适应（Linux/macOS/Windows 自动探测 + root/无头/`--no-sandbox` 兜底） | ✅ 全平台 | 仅 Windows 预览宿主，需手动配 |
| 登录态落盘持久化 `ego_auth_flush` | ✅ 有 | ⚠️ 仅文档级说明 |

**关键差异两条：**
- **看得到**：别家是"跑完告诉你结果"的黑盒；我们实时推流，你**看着 agent 操作**，卡在验证码/走岔立刻发现。
- **控得住**：别家只读；我们监控窗**直接驱动**同一个 agent 浏览器，需要时你亲手接管（缩放/拖拽/点击），不必打断 agent 重来。

> 以上对比基于公开可见的可核实事实：本仓库代码（`bin/ego-cast-worker.mjs` 实时推流 + CDP 输入回传、`lib/index.js` 32 个注册工具、`lib/cast-server.js` host 桥接）与同类插件的源码/README。此文档不含对任何他人的贬低——我们只陈述自己多实现并验证了哪些能力。

**相对 [ego-lite](https://github.com/CitroLabs/ego-lite) 本体，我们多做了这些（都可对照本仓库代码核实）：**

| 能力 | 说明（对应代码） |
|---|---|
| **观察窗前端口** | ego-lite 本体是无头 CLI（只有 heredoc 脚本 + 文本输出）；我们在其上加了 **SSE 实时推流 + 标签条 + 历史抽屉 + 监控窗鼠标直操**（`bin/ego-cast-worker.mjs`、`lib/cast-server.js`、`lib/client.js`），让"看"和"控"成为一等能力 |
| **开箱即用 + 跨平台自足** | `resolveEgoEnv` 自动探测 Chrome/Edge/Brave，内置 `--no-sandbox` wrapper，root / Docker / 无显示器免配置（`lib/index.js`）；不必像官方那样先装一个 GUI 宿主 |
| **健壮性层** | 冷启动自动重试（只重试 CDP 瞬态，不吞真错）、worker 单实例守卫 + 崩溃自动重启、插件卸载 fire-and-forget 不阻塞宿主退出、前端帧缓存上限（`withWarmupRetry` / `makeEnsureWorker` / `frameCache`） |
| **运维型工具** | `ego_doctor`（环境体检）、`ego_captcha`（人机验证探测）、`ego_auth_flush`（登录落盘）、`ego_login_import`（系统浏览器登录态导入）、`ego_http`（浏览器上下文请求）等，是原生 CLI helper 没有的一层 |
| **self-observation** | agent 操作 DSH 自身界面时同样实时可见、可接手 |

> 我们不声称媲美官方 macOS App 的内核级快照或原生多窗口体验；本仓库解决的是"把同一套浏览器能力带进 DSH + Linux/WSL + 看得见"这件事。

---

## 它解决什么问题

通用浏览器不是为 agent 设计的，而 Web 上大量交互（登录态、验证码、动态渲染、表单、需真人会话的站点）只有真浏览器能面对——这正是 ego 系 **"让 agent 用你已登录的浏览器，而不打扰你"**（[官网](https://github.com/CitroLabs/ego-lite)）的由来。

`ego-browser` 把它接进 DSH，并把最痛的一点——**你看不见 agent 在干什么、也插不上手**——用一套观察窗解决：

> 🌐 小球一点看直播；🟦 标签条切换/关闭；🕘 历史抽屉回看；🔍 缩放拖拽；🖱️ 监控窗直接接管真实浏览器。**一句话：让 agent 在浏览器里干活，你在旁边既看得见、又随时能接手。**

### 几个常见的上手场景

- **文献 / 数据抓取**：让 agent 登录知网 / 谷歌学术翻页收集，你在观察窗看着它滚动、点下一页、下载 PDF，中途卡住立刻能发现。
- **表单与登录**：agent 填表到一半，观察窗弹出验证码——你直接接管把验证码点了，再交还给 agent 继续。
- **QA / 冒烟测试**：让 agent 在自己产品上点一圈，观察窗等于一台"会说话的录屏"，顺手还能回看历史轨迹。
- **看 agent 操作 DSH 自身**（self-observation）：agent 在管理会话 / 调设置时，观察窗同样全程可见、可接手。

---

## ✨ 近期亮点

- **v0.8.0**：**侧边栏 Tab 集成**——当 `dsh-better-sidebar` 可用时，实时查看窗注册为侧边栏原生 Tab（而非浮动浮窗），`ego_browser` 工具首次调用自动展开；内置 `EgoBrowserTab` React 组件 + `LivePreviewController` 实时帧管道。`dsh-better-sidebar` **不是 peer 依赖**（`ctx.get()` 机会性消费），没装就退回浮动浮窗，两种部署都干净。
- **v0.7.0**：观察窗状态灯**干活常绿、空闲呼吸**；`ego_script` 每次运行超时 `timeoutMs` 真正生效；前端 `frameCache`/`pageMeta` 按标签清理 + 上限兜底，杜绝长会话内存增长；状态路径家目录回退改 `os.homedir()` 跨平台化；新增 `.gitattributes` 统一 LF 换行。
- **v0.6.1**：卸载不再阻塞宿主退出（自愈链路稳定）；观察窗 worker **单实例守卫** + stale 状态清理；登录/人机验证引导条可关闭且互斥；**观察窗主动跟随 agent 正在操作的页面**（不再被后台重绘页抢占视图）。
- **v0.6.0**：工程收敛——`lib/` 定为唯一源，`build` 改语法校验，杜绝"一构建全回归"。（TS 重构后源码移至 `src/`，`lib/` 为构建产物，见「开发」一节。）
- **v0.5.0**：实时 SSE 推流 + 监控窗直接操作 agent 浏览器。
- **v0.4.0**：Windows 适配。
- 完整历史见 [CHANGELOG.md](CHANGELOG.md)。

---

## 前置条件

| 要求 | 说明 |
|---|---|
| Node ≥ 22 | harness 环境自带 |
| **任意 Chrome / Chromium / Brave / Edge** | 自动发现，或 `EGO_LINUX_CHROME` 指定；root 下用自带 wrapper |
| DSH + dshx | 插件装载机制 |
| 带图形界面的 DSH Web（观察窗） | headless 会话仍可用 `ego_*` 工具，仅无观察窗 |

## 安装

> **包名迁移（DSH Desktop 2.0.5+）**：本插件包名是 **`dsh-ego-browser`**（非 `@dsh-external/ego-browser`）。DSH Desktop 2.0.5 起增加了「profile 依赖名 == 包实际 name」的一致性校验，若 profile 仍用旧名 `@dsh-external/ego-browser` 引用，启动会挂进恢复模式（`profile package identity is invalid for @dsh-external/ego-browser`）。升级到 2.0.5 后请把 profile 的 `package.json` 依赖键 **和** `dsh.profile.bundles` 条目**两处**都改为 `dsh-ego-browser`：

   ```diff
   - "@dsh-external/ego-browser": "git+https://github.com/Fisfzy/ego-browser.git",
   + "dsh-ego-browser": "git+https://github.com/Fisfzy/ego-browser.git",
   ```

   ```diff
   - "@dsh-external/ego-browser",
   + "dsh-ego-browser",
   ```

```sh
dshx install ego-browser <ego-browser.tgz>                             # tarball 或 git URL 均可
dshx list                                                # 应显示：[on] ego-browser
```

观察窗设置中可选 `captureBacke