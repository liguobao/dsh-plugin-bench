# minecraft-dev

[![Awesome DSH Plugin](https://awesome-dsh-plugin.com/badge.svg)](https://awesome-dsh-plugin.com)

Minecraft 开发插件 for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (`dsh`)：让 agent 更擅长写 Minecraft 服务端插件与模组，覆盖 **MC 1.7.10 ~ 26.3 全时代**。适配 dsh **≥ 0.1.5-rc.1**（profile/bundle 插件体系；低于此版本请用 0.7.0 及更早版本）。两条线各实测一种形态：**0.1.5-rc.2 走目录形态、0.1.7-rc.1 走 agentPresets 注册形态**（0.1.5-rc.3 未单独实测，但 peer 范围覆盖它）。0.1.7-alpha 通道未验证。

已被 [awesome-dsh-plugin](https://awesome-dsh-plugin.com) 收录（`Skills` 分类）。

> **dsh 0.1.7 起 preset 的声明方式变了**，本插件两种都支持并在运行时自动选择：0.1.5–0.1.6 的 preset 是 `$DSH_HOME/.agent-presets/<id>/` 目录（插件启动时拷贝，已存在则不覆盖本地修改）；0.1.7 起 preset 改为 Cordis 声明行（`@deepseek-ai/dsh-agent-preset`）交给 `agentPresets` 服务，插件随之改用 `agentPresets.register()` 提交同一批行（`preset/*/rows.js`）。两种形态由同一个源生成，并由测试锁死一致。0.1.7-alpha 通道未验证。

已发布 npm：[`minecraft-dev`](https://www.npmjs.com/package/minecraft-dev)（MIT）｜ 源码：[GitHub](https://github.com/sikadi233-hub/minecraft-dev)

## 功能一览

### 8 个技能（模型按需加载，不占常驻上下文）

| 技能 | 内容 |
|---|---|
| `minecraft-java-build` | 全时代 Java/Gradle 构建知识：JDK 配对表、wrapper、foojay toolchain、依赖仓库、常见坑 |
| `minecraft-paper-plugin` | Paper/Spigot 现代线插件（1.20.x / 1.21.x / 26.x）+ 5 份 API 参考 |
| `minecraft-fabric-mod` | Fabric 模组（loom/loader/fabric-api/yarn 配合）+ 4 份 API 参考 |
| `minecraft-forge-mod` | 传统 Forge 四时代（1.7.10 FG2 / 1.12.2 FG3 / 1.16.5 FG5 / 1.20.1 FG6）+ 3 份时代 API 参考 |
| `minecraft-neoforge-mod` | NeoForge（1.20.1 legacyforge / **1.21.1** / 1.21.x / 26.2 stable + **26.3 beta-only**）+ 3 份 API 参考 |
| `minecraft-spigot-legacy` | 1.7.10 / 1.12.2 老线 Bukkit 插件 + Cauldron/Thermos/Mohist 混合服说明 + 2 份老线 API 参考 |
| `minecraft-major-mods` | 大型模组附属开发：28 个模组条目（1.7.10×10 / 1.12.2×8 / 现代×10，含拔刀剑、神秘时代、匠魂、植物魔法、Create、Botania、AE2、Mekanism、Curios、JEI/REI 等），每条含核实过的 curse.maven 坐标与扩展点 |
| `minecraft-intake` | **任务信息核对（v0.7）**：用户请求写插件/mod/附属但信息不足时，按场景批量提问（版本/平台/加载器/核心/混合端/兼容性/部署），一次问全、不重复问、授权默认 |

### 3 个工具

| 工具 | 用途 |
|---|---|
| `mc_scaffold` | 一句话创建完整可构建项目：paper / fabric / forge / neoforge / spigot 五平台，自动配好构建脚本、主类、元数据、**时代对应的 Gradle wrapper** |
| `mc_gradle` | 在项目里跑 `gradlew <task>`：终端卡片显示、超时自动杀进程树、输出头尾截断、非零退出码不报错而是可读呈现 |
| `mc_codex` | **只在「Minecraft 架构师」预设里可用**：把架构 brief 写到 `<项目>/.dsh/codex-architect.md`，再用**你自己的 Codex CLI** 跑一次完全可见的架构会话——默认走官方 `codex app-server --stdio` 协议（**会话会出现在 Codex 桌面版列表里、可续聊**），也可 `mode: "exec"` 退回 `codex exec`；命令、完整输出、退出码、用时、改动文件、会话 id/线程 id、rollout 路径、token 用量全部回到会话里 |

### 4 个内置子代理（v0.5.0，四子代理团队）

| 子代理（toolName） | 环节与产出 |
|---|---|
| `subagent_mc_plan` | A 方案：勘察项目 + web_search 联网查证 → 写 `<项目>/PLAN.md` + 5 行摘要 |
| `subagent_mc_skeleton` | B 框架：按 PLAN.md 用 mc_scaffold 搭骨架 + 资源模板 + 测试桩 → 变更清单 |
| `subagent_mc_content` | C 内容：按 PLAN.md 与骨架填充功能代码 → 变更清单 + 不确定点 |
| `subagent_mc_verify` | D 编译审查：mc_gradle 编译/测试、修小错 → 验证报告 |

（注：4 个子代理为宿主层工具，任何 preset 会话可见；使用说明见 Minecraft 专家 preset persona。）

### 2 个 Agent 预设

| 预设 | 内容 |
|---|---|
| `minecraft`（Minecraft 专家） | 一键切换的专精 agent：standard 全工具集（shell / 文件 / 检索 / 技能 / 计划 / 目标 / 子代理 / 工作流）+ 中文专家人设 + 全局可见的 8 个技能与 4 个内置子代理 subagent_mc_plan/skeleton/content/verify（v0.6.0 起装完插件重启 dsh 后**自动安装**到 `$DSH_HOME/.agent-presets/minecraft/`，见下方「Minecraft 专家 agent 的安装」） |
| `minecraft-architect`（**Minecraft 架构师（Astra神的瞥视）**，v0.8.0） | 专家预设**逐字节复制**后只多两处：一段人设 + 一行 `minecraft-dev/codex` 模块（注册 `mc_codex` 工具与 `minecraft-codex-architect` 技能）。因此专家预设的工具/技能目录完全不变，只有本预设能看到 `mc_codex` |

#### Minecraft 架构师：Codex 做架构，DSH 填内容（v0.8.0）

分工照搬 Cherry Studio 里的 Architect / Coder 两个智能体（`// [TODO: Agent B] 描述` 标记就是交接协议）：

1. DSH 先按 `minecraft-intake` 把版本/平台/加载器核对清楚，整理成一段 `goal`；
2. 点名后调用 `mc_codex`：它把架构 brief 写到 `<项目>/.dsh/codex-architect.md`（**可读可改**），然后用**你自己的 Codex**在项目目录里跑一次架构会话。默认 `mode: "app-server"`，实际执行的是
   `"…codex.exe" app-server --stdio`
   协议（`thread/start` + `turn/start`，prompt 就是那个文件的内容）——这条命令原样回显在会话里；`mode: "exec"` 时则是
   `"…codex.exe" exec - -C "<项目>" -s workspace-write --skip-git-repo-check -o "<项目>/.dsh/codex-last-message.md" < "<项目>/.dsh/codex-architect.md"`
3. Codex 只写骨架：接口/签名/build 脚本/资源模板/主类注册，所有业务逻辑方法体留 `// [TODO: Agent B] 描述`，并额外产出 `FILL-SPEC.md`（标记位置 × 方法契约 × 构建命令 × UNVERIFIED 清单 × 完成判据）；
4. DSH 只替换这些标记（不动签名/结构/接口），最后用 `mc_gradle` 跑到 build exitCode 0，并确认标记计数为 0。

**透明度**（本预设的硬要求）：执行前先声明这一步会消耗**你自己的 Codex**（订阅账号计入 Codex 用量窗口；API key 计入余额），而且 DSH 侧不会显示这笔消耗；返回完整输出、退出码、用时、改动文件清单、会话/线程 id、rollout 文件路径与 token 用量（从 rollout 的 `token_count` 事件读，源码写的是 `turn/completed` 不带 usage）；失败不静默重试，委派次数上限为「架构 1 次 + 修复 ≤1 次」。

**关于"这次会话在 Codex 桌面版里看得见吗"（实测结论）**：默认的 `mode: "app-server"` **看得见**——app-server 建的线程是 `source = vscode`、`originator = DeepSeek Harness`，实测跑完立刻能被桌面版用的 `thread/list {}` 查到（同一条 App 侧边栏查询只会返回 `vscode`/`appServer` 一类，不返回 `exec`/`cli`），所以你可以直接在 App 里点开续聊，或在命令行 `codex resume <threadId>`。两种模式都会把内容**持久化**在 `~/.codex/sessions/<年>/<月>/<日>/rollout-…-<id>.jsonl`（`mc_codex` 直接回报这条路径，打开就是 Codex 的完整过程）：

- `mode: "app-server"`（默认）：桌面版列表可见、可续聊；续接用 `codex resume <threadId>`。
- `mode: "exec"`：`source = exec`、`originator = codex_exec`，**桌面版列表不会显示**（App 里没有"显示 CLI 会话"的开关）；此时用 `codex exec resume <sessionId> "…"` 续接。
- 想让架构这一步由你**亲手在桌面版里操作**（例如先改 prompt）：把 `.dsh/codex-architect.md` 写好（可只生成不执行），在桌面版新建线程、工作目录选该项目、把内容粘进去跑完，再回来说"架构做完了"，DSH 就从磁盘上的 `FILL-SPEC.md` 与 `[TODO: Agent B]` 标记接手。
- 不建议直接改 `state_5.sqlite` 的 `source`/`originator`：rollout 的 `session_meta` 写死了 `codex_exec`，桌面版的 rollout 回填（`rollout_migration_state`/`backfill_state`）可能把它改回去，且 App 运行时持有该库。

**前提**：只需要本机装着 Codex（桌面版会顺带提供 CLI；`mc_codex` 会自己探测 PATH、`~/.codex/plugins/.plugin-appserver/`、`%LOCALAPPDATA%\OpenAI\Codex\bin\<hash>\` 三处）。**不用打开 Codex 桌面版**——每次都 spawn 一个非交互会话；app-server 模式下的会话结束后会出现在桌面版列表里（想看就开，不想看也不用开）。Codex 探不到/跑失败时，本预设会退回普通做法（自己写或走 A–D 链），并且**绝不留下 `[TODO: Agent B]` 标记**。

## 安装

### 方式一：npm 安装（推荐）

```sh
dsh plugin --profile web add minecraft-dev
```

> **国内用户注意**：npm 默认源 npmmirror 会在发布后几分钟内同步；若报 `ERR_PNPM_FETCH_404` 说明镜像还没同步，加官方源即可：
> `dsh plugin --profile web add minecraft-dev --registry=https://registry.npmjs.org`

### 方式二：本地 tarball（离线/内网）

```sh
cd minecraft-dev && pnpm pack        # 产出 minecraft-dev-x.y.z.tgz
dsh plugin --profile web add ./minecraft-dev-0.5.0.tgz
```

### 方式三：源码直连（开发迭代，改完即生效）

```sh
dsh plugin --profile web add /path/to/minecraft-dev
```

### ⚠️ 如果你从源码运行 dsh：命令是 `pnpm dsh` 不是 `dsh`

**只有通过 npm 安装的 dsh**（`npx @deepseek-ai/dsh` 或 `npm i -g`）才有 `dsh` 命令。
如果你是从仓库源码跑的（比如 `C:\Users\...\deepseek-harness-master`），必须：

1. 先 `cd` 到 dsh 仓库根目录
2. 用 `pnpm dsh` 代替 `dsh`：

```sh
cd C:\Users\YX-ASUS\Desktop\deepseek-harness-master
pnpm dsh plugin --profile web add minecraft-dev --registry=https://registry.npmjs.org
```

### ⚠️ 安装后必须重启 dsh 服务

**正在运行的 dsh 不会自动加载新装的插件**。装完后：

1. 在跑 `pnpm dsh web` 的窗口按 `Ctrl+C` 停掉
2. 重新启动 `pnpm dsh web`
3. 新会话里插件生效

### 验证安装

```sh
pnpm dsh --profile web --dump-config     # 应出现 "# == minecraft-dev" 层与七行插件（skills/tools/preset + 4 个 subagent 实例）
```

### 卸载

```sh
dsh plugin --profile web remove minecraft-dev
```

### 安装 Minecraft 专家 agent（v0.6.0 起自动）

**装完插件重启 dsh 后自动安装，无需手动复制**：插件每次启动（挂载）时把自带的 `preset/minecraft/` 与 `preset/minecraft-architect/`（v0.8.0 起）分别复制到 preset 扫描根：

- 目标：`$DSH_HOME/.agent-presets/minecraft/` 与 `$DSH_HOME/.agent-presets/minecraft-architect/`（默认 `C:\Users\<用户>\.dsh\.agent-presets\`；设了 `DSH_HOME` 时以 `$DSH_HOME` 为准）。
- 幂等：目标已有 `agent.cordis.yml` 就跳过，**绝不覆盖本地修改**；目录存在但缺 composition 文件时视为损坏并自动修复。两个预设各自独立跳过，互不影响。
- **升级到 v0.8.0 想看新的架构师预设**：删掉 `$DSH_HOME/.agent-presets/minecraft-architect/` → 重启 dsh → 自动重装（专家预设目录不用动，它本来就不变）。
- 关闭：在 `$DSH_HOME/cordis.patch.yml`（或 profile 的 `cordis.patch.yml`）追加：

```yaml
- id: minecraft-preset
  config:
    autoInstallPreset: false
```

- 老版本（<0.6.0）或关闭自动安装时，手动复制：

```sh
# 1. 建用户 preset 根（dsh 自动把 ~/.dsh/.agent-presets 追加为 user 根，
#    但目录不存在时发现为空，需先创建）
mkdir -p ~/.dsh/.agent-presets

# 2. 复制 preset 目录（含 preset.yml + agent.cordis.yml）
cp -r <minecraft-dev 仓库>/preset/minecraft ~/.dsh/.agent-presets/
```

- 最终落盘：`~/.dsh/.agent-presets/minecraft/preset.yml` 与 `agent.cordis.yml`（本机默认 `C:\Users\YX-ASUS\.dsh\.agent-presets\minecraft\`；设了 `DSH_HOME` 时以 `$DSH_HOME` 为准）。
- **禁止*