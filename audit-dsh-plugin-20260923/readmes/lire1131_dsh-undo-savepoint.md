# dsh-undo-savepoint — DSH 安全管家（撤销 / 回退 / 崩溃自愈）

[![awesome · DSH plugin](https://awesome-dsh-plugin.com/badge.svg)](https://awesome-dsh-plugin.com)
[![CI](https://github.com/lire1131/dsh-undo-savepoint/actions/workflows/ci.yml/badge.svg)](https://github.com/lire1131/dsh-undo-savepoint/actions/workflows/ci.yml)

> 中文 | [English](README.en.md) | [更新日志](CHANGELOG.md)

**为 [DeepSeek Harness (DSH)](https://github.com/deepseek-ai/deepseek-harness) 打造的安全管家：改设置自动存档，一键撤销 / 恢复 / 回退到任意版本；主动体检、升级护航、崩溃自愈；DSH 起不来时局外 WebUI / GUI / CLI 依然可用。**

管家的做事方式是主动检查，有异常才说话，正常时安静。启动 30 秒后完成第一次体检；崩溃后给出可回退的最后正常快照；检测到 DSH 版本变化时先打升级保险快照再放行。

## 预览

| 会话头部：撤销 / 恢复 / 快照 / 对话撤回全部图标化 + 自动快照状态徽章（已存 24 份 · 3 小时前） |
|---|
| ![header](https://cdn.jsdelivr.net/gh/lire1131/dsh-undo-savepoint@master/docs/shots/webui-header.png) |

| WebUI 快照面板：手动保存 / 撤销 / 恢复 / 清理 / 导出导入 / 安全模式，逐条「差异 / 回退到此版本 / 删除」 | DSH 设置「快照」独立栏目（自动保存 / 保留数量 / 敏感模式 / 插件白名单 / 定时快照） |
|---|---|
| ![panel](https://cdn.jsdelivr.net/gh/lire1131/dsh-undo-savepoint@95230c2/docs/shots/webui-panel.png) | ![settings](https://cdn.jsdelivr.net/gh/lire1131/dsh-undo-savepoint@master/docs/shots/webui-settings-section.png) |

| 局外 WebUI：崩溃横幅 + 撤销 / 重做 / 安全模式 / 诊断 / 对话撤回 / 设置，不依赖 DSH 运行（快照对比与设置见[局外工具](#局外工具dsh-挂了也能用)一节） |
|---|
| ![gui](https://cdn.jsdelivr.net/gh/lire1131/dsh-undo-savepoint@95230c2/docs/shots/gui-main.png) |

## 安全管家

| 管家职责 | 对应能力 |
|---|---|
| 启动健康体检 | 启动 30 秒后自动检查会话目录、容错补丁、快照覆盖与磁盘占用，有异常才告警 |
| 崩溃自愈 | DSH 完全起不来时一键安全模式，只保留本插件保证能启动；崩溃归因给出最后正常快照，一键回退 |
| 会话医生 | undo_scan 扫描会话文件，修复单帧布局违规与 seq 重叠两类损伤，修不了的隔离，绝不动原件 |
| 升级护航 | 检测到 DSH 版本变化自动打升级保险快照，升级后首次启动出兼容体检与会话普查报告 |
| 快照不泄密 | .env、凭据、home 级设置进快照自动脱敏，真实值只存本机 vault，导出包零泄露 |
| 容错补丁 | 对 DSH 历史版本的已知缺陷点做运行时兜底，官方修复后补丁自然失效，不影响功能 |

## 核心能力

| 能力 | 说明 |
|---|---|
| **配置 + 插件代码一键回滚** | 快照覆盖配置与用户插件代码树，改坏任何一处都能撤销（含 yield\* 类纯代码事故）；支持 undo / redo / 回退任意版本，WebUI / 对话 / 离线 CLI 三入口 |
| **消息级撤销** | 按 AI 消息（或 60s 批次）记录工作区文件变更，一句话回滚「这条消息改了什么」（恢复原内容 / 删除新建文件）；不依赖 git、不碰会话存储；「跟踪工作区目录」可在设置中配置（逗号 / 分号多选，非空时覆盖默认工作目录） |
| **局内对话撤回** | 对话头部「对话撤回」入口 + 消息级撤回面板，在 DSH 面板里即可撤回指定消息批次的文件改动 |
| **密钥脱敏 + 本机 vault** | `.env` / 凭据进快照自动脱敏（结构保留），导出 ZIP 零泄露；真实值存本机 vault，本机回滚完整还原 |
| **一键安全模式** | DSH 完全起不来时，禁用除撤销系统外所有插件保证能启动；自动快照 + 备份配置（profile / home 双级 patch 一并备份恢复，并中和 `dsh.profile.bundles` 里会导致启动器硬校验失败的条目），一键退出；家目录被重建 / 换机时残留状态自动降级不激活 |
| **崩溃归因** | 上次异常退出时直接给出「最后正常快照」id + 一键回退按钮；按日志签名分类崩溃原因（`session-corrupt` / `bundle-check` / `patch-tree`），横幅给出对应处置建议 |
| **会话文件扫描修复** | `undo_scan` 扫描 `<home>/sessions/**/session.jsonl.zstd`：单帧布局违规（8/18 崩溃根因）与 synthetic-closer seq 重叠（撤销/快照还原后的中断恢复 seq 重叠）可一键修复（原件留 `.bak` + 隔离区副本）；无法解码的只隔离不动；DSH 起不来时用 `dsh-undo.ps1 scan [--fix]` 离线处理（需 Node ≥22.15，Node 20 下降级为提示） |
| **快照时间线（Time Machine）** | 快照按日期分组卡片化（备注 / 标签芯片，尊重 `prefers-reduced-motion`）+ 文件级 diff（新增 / 删除行高亮、目录树导航、逐文件浏览）+ 一键回滚 |
| **快照管理** | 备注 / 标签（`undo_note`，时间线可直接编辑）、定时快照（间隔制，自动建档 + 保留清理）、孤儿 blob GC（`undo_compact`，释放磁盘）、ZIP 导出 / 导入（可选 AES-256-GCM 加密，兼容 PowerShell 明文互操作） |
| **一键诊断与启动预检 `undo_doctor`** | 存储侧：快照目录可写性、blob 完整性（缺失 / 孤儿）、设置文件健康、快照规模分布。启动侧预检那些会让 DSH 在挂载任何插件之前就崩掉的硬失败：profile 清单 BOM / JSON / 结构、`dsh.profile.bundles` 逐项可解析、`patchReload` 取值、`link:` junction 落点、patch 里重复的 loader id、上次启动未完成。输出 ok / warn / err 结构化报告，可修项标 `[fixable]`，对话里 `undo_doctor fix=true`、离线 `dsh-undo.ps1 doctor -Fix`、局外 WebUI 诊断面板的「修复可修项」按钮都能一键修复（改前先落手动快照，修完自动复查） |
| **跨机迁移安全** | 恢复前自动预检缺失插件并明确提示；快照可一键导出 / 导入 ZIP 迁移（见 [docs/migration.md](docs/migration.md)） |
| **局外急救** | DSH 挂了也能用：WebUI + GUI 窗口 + CLI + 桌面快捷方式，时间线 / 回滚 / 对比 / 安全模式 / 诊断一应俱全 |

> 基础能力（键盘快捷键、对话指令、自动清理、双模式保存、可配置参数等）见下文与[更新日志](CHANGELOG.md)。

## 平台支持

v0.4.0 起核心抽取为纯 Node 零依赖模块（`lib/core.mjs` / `lib/zip.mjs`），外围按平台分发，Windows / macOS / Linux 三平台可用：

| 能力 | Windows | macOS | Linux |
|---|---|---|---|
| 配置 / 插件快照、撤销 / 重做 | ✅ | ✅ | ✅ |
| 局外 CLI / GUI | ✅（.bat / .ps1） | ✅（.command） | ✅（.sh） |
| 局外 WebUI（undo-server） | ✅ | ✅ | ✅ |
| 文件选择对话框 | PowerShell 原生 | osascript | zenity → kdialog（都没有则回退手输） |
| CI 回归 | windows-latest | macos-latest | ubuntu-latest |

> CI 为三平台矩阵（`windows/ubuntu/macos × node[20,22]`）。ZIP 导出 / 导入由纯 Node 零依赖 `lib/zip.mjs` 实现（deflate / 存储、CRC32、UTF-8），不引入运行时依赖，与 PowerShell 互操作已双向验证。

> ![icon](https://cdn.jsdelivr.net/gh/lire1131/dsh-undo-savepoint@master/docs/app-icon.png)
>
> Logo / 图标：生成提示词见 `docs/logo-prompt.md`；WebUI favicon 用内置 `tools/webui/logo.svg`。自定义图标：透明 PNG 存为 `tools/webui/logo.png`，运行 `node tools/make-ico.mjs tools/webui/logo.png tools/webui/logo.ico` 生成 `.ico`，下次创建快捷方式时自动启用（回退顺序 `logo.ico` → `logo.png` → 系统默认）。

## 崩溃急救速查（按场景选工具）

| 场景 | 操作 |
|---|---|
| 配置 / 插件被改坏 | 对话 / WebUI / CLI：`undo` 或 `restore -Id <id>` |
| 插件代码被改坏 | 同上（快照含插件代码树，一键还原） |
| 上次异常退出，不知回退到哪 | WebUI / GUI 横幅显示 last-good 快照，一键回退 |
| **DSH 完全起不来** | 桌面「DSH撤销管理器」→ **安全模式**按钮（或 CLI `safe-mode -Label on`）→ 重启 DSH 保证能启动 |
| 崩溃横幅提示会话损坏 | 对话 / CLI：`undo_scan quarantine=true` 修复（或离线 `dsh-undo.ps1 scan --fix`） |
| 恢复后可能缺插件（跨机） | 恢复报告预检提示；先装插件或进安全模式 |
| 配置「突然变了」 | CLI `recent` / 对话 `undo_recent` 查回滚日志 |
| 撤销涉及插件 / 挂载 | 报告提示「重启 DSH 后生效」 |

| 安全模式确认：一键禁用除本插件外的全部用户插件，保证 DSH 能启动，之后再逐个排查 |
|---|
| ![safemode](https://cdn.jsdelivr.net/gh/lire1131/dsh-undo-savepoint@master/docs/shots/safe-mode-confirm.png) |

## 安装

前置：已安装 DSH（`@deepseek-ai/dsh`）与 Node.js（≥20）。宿主模式运行于提供
tools / systemPrompt / webServer 服务的 profile（Web 型 profile 均满足）；
DSH 完全无法启动时改用局外 CLI / GUI，不依赖宿主。

### 方式 A：GitHub 直装（推荐）

安装 master 最新提交：

```bat
dsh plugin --profile web add github:lire1131/dsh-undo-savepoint#master
```

安装完成后重启 DSH 即生效（快照目录、参数等均可在设置中修改）。

### 方式 C：npm 源安装

```bat
dsh plugin --profile web add dsh-undo-savepoint
```

`dsh plugin add` 转发 pnpm 在 profile 目录完成安装，本包的 `package.json` 声明了
`dsh.bundle.patch`，安装后自动登记进 profile 的 bundle 清单，重启 DSH 即生效。

### 方式 B：本地源码 / 免发布

1. **把仓库放到本地插件目录**（无中文路径更稳妥），例如 `D:\dsh\plugins\dsh-undo-savepoint`：

```bat
git clone https://github.com/lire1131/dsh-undo-savepoint.git D:\dsh\plugins\dsh-undo-savepoint
```

2. **建立 junction**（Windows），让 DSH 的模块解析器通过包名 `dsh-undo-savepoint` 找到本地源码（host 插件与 WebUI client 插件都靠它）：

```bat
mklink /J "<你的DSH安装>\node_modules\dsh-undo-savepoint" "D:\dsh\plugins\dsh-undo-savepoint"
```

> DSH 从它自己的 `node_modules` 向上解析包名。默认安装位置是 `C:\Users\<用户名>\node_modules`（npm 安装在用户目录时）；若用 npx 缓存运行，则对 npx 缓存目录下的 `node_modules` 建 junction。执行 `npm root -g` 或检查 DSH 启动报错路径即可确认。

3. **挂载到 profile 补丁层**：编辑 `<DSH_HOME>\profiles\web\cordis.patch.yml`，追加：

```yaml
- insert:
    - id: dsh-undo-savepoint
      name: dsh-undo-savepoint
```

4. **生效**：保存即热加载（host 部分）；刷新页面出现头部按钮与设置项；重启 DSH 后一切进入稳态（旧版扁平快照会自动迁移）。

> 依赖说明：host 插件通过 `createRequire('<DSH安装根>/package.json')` 加载 `@deepseek-ai/dsh-tools`。若 DSH 安装在其他位置，设置环境变量 `DSH_ROOT=<DSH安装根>` 即可，无需额外安装依赖。

## 卸载

### 标准卸载

两条命令，第二条负责清理残留：

```bat
dsh plugin remove dsh-undo-savepoint
node tools\uninstall.mjs
```

`uninstall.mjs` 默认**温和清理**：摘掉挂载声明、删掉 junction 与桌面快捷方式，**保留快照库与设置**（重装即可恢复历史快照）。确认不再需要历史快照时加 `--purge`：

```bat
node tools\uninstall.mjs --purge
```

常用参数：

| 参数 | 作用 |
|---|---|
| `--purge` | 连带删除 `undo\`（设置/状态）与 `undo-snapshots\`（快照库） |
| `--yes` | 跳过确认（非交互环境必须显式给出，防脚本误删） |
| `--home <dir>` | 覆盖 DSH 主目录 |
| `--profile <n>` | 只处理指定 profile（默认全部） |
| `--json` | 输出机器可读的清理计划 |

不带 `--yes` 时，命令先列出**每一项将要删除的路径**再询问；非交互环境（CI/管道）会拒绝执行，必须显式 `--yes`。

### 手动卸载对照表

确实要手动清理时，六处落盘位置与各自的正确删法：

| # | 落盘位置 | 正确删法 |
|---|---|---|
| 1 | `<DSH安装根>\node_modules\dsh-undo-savepoint`（或 profile 的 `node_modules` 下） | **删除链接本体，勿跟随**。这是 junction，直接删除即可；在资源管理器里进入它再删内容，删的是你的插件源码 |
| 2 | `<DSH_HOME>\profiles\<profile>\cordis.patch.yml` 里的 `id: dsh-undo-savepoint` 条目 | 手工摘掉该 `insert` 条目（可整条删）；文件变空可直接删文件 |
| 3 | `<DSH_HOME>\profiles\<profile>\package.json` 的 `dsh.profile.bundles` 数组 | 从数组里移除 `dsh-undo-savepoint` 一项 |
| 4 | `<DSH_HOME>\undo\` | 设置与状态（含 `settings.json`）。确认要重置设置时才删 |
| 5 | `<DSH_HOME>\undo-snapshots\` | 快照库。**先确认不再需要回退**再删 |
| 6 | 桌面 `dsh-undo-savepoint.lnk`（macOS `.command` / Linux `.desktop`） | 直接删除 |

### Windows 长路径提示

Windows 用户目录较深或使用中文用户名时，快照文件的路径可能超出资源管理器（MAX_PATH 260）的删除上限，手删会报「文件名过长」或删到一半留下残骸。**推荐用上面的 `uninstall.mjs`**：它按固定路径逐项删除，不遍历快照内部结构，不受该限制。

## 使用（