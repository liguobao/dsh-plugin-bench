# @dsh-external/dsh-ui-progress

DSH Web UI 会话进度插件：为 DeepSeek Harness 的 Web GUI 的输入框停靠区提供常驻会话进度条，**零核心改动**（纯 client 插件，不触碰 agent-loop）。

> **你的 DSH 版本决定装哪个插件版本**（装错会崩：常见症状 `useConversation is not a function`）
> - DSH **0.1.1-rc.2**（npm 最新）：装**旧版** `'@dsh-external/dsh-ui-progress@github:lhh010/dsh-ui-progress#v0.9.3'`
> - DSH **0.1.2-alpha.1 / alpha.2 / alpha.3 / alpha.4 / alpha.5 / rc.1**：装**新版**（下方默认命令）
## 安装

```sh
# 方式一：git 依赖固定 tag（公开镜像，推荐；也可用 github:lhh010/dsh-ui-progress）
dsh plugin --profile web add '@dsh-external/dsh-ui-progress@github:lhh010/dsh-ui-progress#v0.10.5'

# 方式二：本地 link（开发）
git clone https://github.com/lhh010/dsh-ui-progress.git
cd dsh-ui-progress && pnpm install && pnpm run build
dsh plugin --profile web add link:/path/to/dsh-ui-progress
```

配置行（`$DSH_HOME/profiles/web/cordis.patch.yml`，热重载，无需重启）：

```yaml
- insert:
    - id: dsh-ui-progress
      name: '@dsh-external/dsh-ui-progress'
```

> **安装提示**：pnpm 11 首次安装可能拦截 node-pty 等构建脚本——在 `~/.dsh/profiles/web` 下执行 `pnpm approve-builds --all` 放行后重跑安装命令；装完**硬刷新浏览器**（Ctrl/Cmd+Shift+R）。

### 提示词安装（让 DSH 自己装）

把下面这段提示词发给任意一个 DSH 会话，模型会替你完成安装：

> 帮我安装 dsh-ui-progress 插件（DSH 会话进度条：输入框常驻会话进度条/todos 真实进度/中断橘红态），步骤：
> 1. 执行 `dsh plugin --profile web add '@dsh-external/dsh-ui-progress@github:lhh010/dsh-ui-progress#v0.10.5'`（首次可能被 pnpm 11 拦截 node-pty 构建脚本而失败）
> 2. 在 `~/.dsh/profiles/web` 下执行 `pnpm approve-builds --all`（放行构建脚本）
> 3. 再执行一次第 1 步的安装命令
> 4. 完成后提醒我硬刷新浏览器（Ctrl/Cmd+Shift+R）
> 遇到报错先查 https://github.com/lhh010/dsh-ui-progress README 的常见问题/已知限制。

## 版本对应 / Version compatibility

## 智能版本门控更新提示 / DSH-gated update chip

更新浮标会结合**当前运行的 DSH 版本**（宿主端从 dsh 安装清单读取，随 `/dsh-ui-progress/latest` 一并返回）与仓库根的 [`compatibility.json`](compatibility.json)（版本→支持的 DSH 列表，精确匹配）判定提示形态：

- 最新版支持当前 DSH → 正常「新版本 vX 可用，点击更新」；
- 最新版需要更高 DSH、但存在支持当前 DSH 的中间新版 → 提示更新到中间版，并注明「另有 vX 需更高 DSH」；
- 最新版需要更高 DSH、且当前 DSH 无任何可用新版 → 琥珀色信息条：「新版本 vX 支持更高 DSH 版本，当前 DSH vY 暂不可用」，不提供直接升级。

兼容数据拉取失败或无该版本条目时，自动回退为旧的普通升级提示（离线安全）。**发版时需同步维护 `compatibility.json`**（与下表同一步骤新增一行）。

## 版本对应 / Version compatibility

构建产物随 DSH 快照版本更新，安装时按快照选择对应版本：

| 插件版本 | DSH 快照 | 说明 |
| --- | --- | --- |
| `v0.10.5`（默认） | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`~`0.1.7-alpha.2`、`0.1.7-rc.1` | 声明支持 dsh-v0.1.7-rc.1（舰队扫检零错误零崩溃，零适配改动） |
| `v0.10.4` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`~`0.1.6-alpha.2`、`0.1.7-alpha.1`、`0.1.7-alpha.2` | **新增 DSH 版本门控更新提示**：浮标结合当前运行 DSH 版本（宿主端读取）与 compatibility.json 判定——最新版不支持当前 DSH 时改提示「需更高 DSH」（琥珀色）或中间版本（蓝+备注），数据缺失回退旧行为。声明支持 dsh-v0.1.7-alpha.2（实机验证）；typecheck/52 单测/构建全绿 |
| `v0.10.3` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`~`0.1.6-alpha.1`、`0.1.7-alpha.1` | **适配 dsh 0.1.7-alpha.1 图标集改名**：primitives 全部 `*16` 图标取消（→ `*Medium`/`*Regular` 双变体），静态解构得 `undefined` → React #130 → slot 错误边界卸载整个输入栏 dock（症状：进度条消失，控制台仅一条压缩报错）。改为运行时回退解析（`*16` → `*Medium` → `*Regular`），单构建兼容 0.1.5/0.1.6/0.1.7+ 宿主；typecheck/45 单测/构建全绿，无头浏览器 E2E 验证 dock 恢复渲染、零控制台报错 |
| `v0.10.2` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`~`0.1.6-alpha.2` | **适配 dsh 0.1.6-alpha.2 运行时解析重构**：dock 标准 props 移除 `useSessions`/`useSessionPendingInteraction`，子代理待办/运行指示降级隐藏，其余（todos 进度、token 速率/面板、ETA、状态文案）全功能；typecheck/45 单测/构建全绿，alpha.2 实机验证（进度条恢复显示）。v0.10.1 为纯版本号发布（声明支持 0.1.6-alpha.1），未单独建行 |
| `v0.10.0` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`~`0.1.5-rc.2` | **新功能双发**：①「后台运行中」状态（青色）——主会话完成而子代理树仍在执行时，进度条不再误显就绪绿；②Token 用量徽标 + 悬停/点击明细面板（总量/未缓存输入/缓存读取/缓存写入/输出/缓存命中%，实时更新）。typecheck/45 单测/构建全绿，热挂载实机验证 |
| `v0.9.17` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`~`0.1.5-rc.2` | 声明支持 0.1.5-rc.1~rc.2（npm 已发布，钉版本实机验证；rc.1 为 0.1.5 系列首个候选版本，client 插件面零代码差异；typecheck/build/39 单测全绿，热挂载实机验证） |
| `v0.9.16` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`~`0.1.5-alpha.2` | 声明支持 0.1.5-alpha.2（npm 已发布，钉版本实机验证；alpha.2 改动为 Sidebar 文档预览、模型文件交付、minimal 默认工具调整与 `fs-ext` 安装修复，client 插件面零代码差异；typecheck/build/39 单测全绿，启动清单确认加载） |
| `v0.9.15` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`~`0.1.5-alpha.1` | 声明支持 0.1.5-alpha.1（npm 已发布，钉版本实机验证；0.1.5 改动在会话格式 V3 / ctx.agent 移除 / 宿主 bundle 服务路由 `/plugins/??`，client 插件面零代码差异；typecheck/build/单测全绿，启动清单确认加载） |
| `v0.9.14` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1`、`0.1.3-alpha.2` | 声明支持 0.1.3-alpha.2（npm 已发布，钉版本实机验证；alpha.2 改动全在 pi-ai/Web 顶栏/子代理消息/host 面，client 插件面零代码差异；typecheck/build/单测全绿） |
| `v0.9.13` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1`、`0.1.3-alpha.1` | 声明支持 0.1.3-alpha.1（npm 未发布，源码宿主实机验证；0.1.3 破坏性变更集中在 host/session 侧，client 插件面零代码差异；typecheck/build/单测全绿） |
| `v0.9.12` | `dsh-v0.1.2-alpha.1`~`alpha.5`、`rc.1` | 声明支持 rc.1（alpha.5→rc.1 为纯版本号提交，零代码差异；实机 rc.1 验证通过） |
| `v0.9.11` | `dsh-v0.1.2-alpha.1`~`alpha.5` | 声明支持 alpha.5（typecheck/build 全绿；alpha.5 为纯 bug 修复，无 API 变更） |
| `v0.9.10` | `dsh-v0.1.2-alpha.1`~`alpha.4` | 声明支持 alpha.4（typecheck/build 全绿） |
| `v0.9.9` | `dsh-v0.1.2-alpha.1`~`alpha.3` | 更新提示词补「按 DSH 版本选 tag」路由说明与排查指引 |
| `v0.9.8` | `dsh-v0.1.2-alpha.3`（npm alpha） | 兼容 DSH 0.1.2-alpha.3：typecheck/build/单测全绿 + 实机验证 |
| `v0.9.3` | npm `@deepseek-ai/dsh@0.1.1-rc.1` | 修复中断检测：0.1.x 的停止不再留旧式节点痕迹，改以最新回合的 `turn/end reason` 为主信号（`aborted`/`interrupted` 区分手动停止与崩溃），窗口节点痕迹降级为旧宿主回退路径；新增 12 例单测，npm 0.1.1-rc.1 实机核验 |
| `v0.9.2` | npm `@deepseek-ai/dsh@0.1.1-rc.1` | 0.1.1-rc.1 实机 boot 验证通过（boot 清单 + client.js 200），依赖的槽位/服务不变 |
| `v0.9.1` | `snapshots/20260810T155924Z`（snapshot0810） | 兼容性构建：客户端插件元数据从顶层 `dshClient` 迁移为嵌套 `dsh.client`（0810 的 ClientModuleHostService 只读该字段；顶层 `dshClient` 被静默忽略），inject/platform 原样保留 |
| `v0.9.0` | `snapshots/20260809T140917Z`（snapshot0809） | 新构建（原生 0809）：运行中新增**实时 token 生成速率**（自校准估算 + 1s 滑动窗口平滑，首 token 到达起算，贴近真实 provider usage） |
| `v0.8.0` | `snapshots/20260808T121140Z`（snapshot0808） | 新构建：移除自带 `report_progress` 工具与上报引导（宿主 half 置空）、移除工具卡片；填充改为 todos 真实比例（无 todos 默认 100%）；新增中断橘红态（手动打断/API 错误等意外停止） |
| `v0.7.0` | `snapshots/20260808T121140Z`（snapshot0808） | 新构建：适配 0808 的 slot 迁移（`conversation.chat.toolview` → `tool.call.toolview`，注册经 `slots.inject` 等待声明） |
| `v0.6.0` | `snapshots/20260807T130646Z`（snapshot0807） | 新构建：已耗时 0.1s 步进（满分钟折叠）+ subagent 待办琥珀提示 |
| `v0.5.1` | `snapshots/20260807T130646Z`（snapshot0807） | 同快照上一构建：会话完成进度条浅绿色 |
| `v0.5.0` | `snapshots/20260807T130646Z`（snapshot0807） | 同快照上一构建：自带工具 + 上报引导 |
| `v0.4.0` | `snapshots/20260806T160212Z`（snapshot0806） | 同快照上一构建（ETA 仅来自模型上报） |
| `v0.3.1` | `snapshots/20260806T160212Z`（snapshot0806） | 同快照上一构建（ETA 为线性外推） |
| `v0.3.0` | `snapshots/20260806T160212Z`（snapshot0806） | 同快照上一构建（卡片耗时/ETA 文案插值缺失） |
| `v0.2.0` | `snapshots/20260806T160212Z`（snapshot0806） | 同快照早期构建（无耗时/ETA/失败态/阶段时间线） |
| `v0.1.0` | `snapshots/20260805T134133Z`（snapshot0805） | 旧构建，按旧安装方式（`~/.dsh/config.yaml` + `pnpm add -w link:`） |

> **兼容性说明**：当前版本为 `v0.9.12`（面向 `dsh-v0.1.2-rc.1`）；以下为历史快照兼容记录。`v0.8.0` 构建基于 snapshot0808 开发，同时兼容 snapshot0809（`snapshots/20260809T140917Z`），实机验证通过；`v0.9.0` 为原生 snapshot0809 构建；`v0.9.1` 面向 snapshot0810（`snapshots/20260810T155924Z`，默认版本），同时兼容 snapshot0811（`snapshots/20260811T152241Z`）与最终快照 snapshot0812（`snapshots/20260812T172954Z-final`）——0811 与 0812 实机 boot 验证通过（见下）。

> **npm 发版兼容**：兼容 DSH npm 发版 `@deepseek-ai/dsh@0.1.1-rc.1`（v0.9.2 实机 boot 验证通过：`dsh --profile web` 启动后 boot 清单包含 `@dsh-external/dsh-ui-progress`，`/plugins/@dsh-external/dsh-ui-progress/client.js` 返回 200；`conversation.input.dock` 槽位与 `locale`/`invariants` 服务在 0.1.1-rc.1 上保持不变），同时兼容 `@deepseek-ai/dsh@0.0.1-rc.5`（dist-tag `next`，即最终快照 snapshot0812 的 npm 发版；`npm exec -p @deepseek-ai/dsh@0.0.1-rc.5 -- dsh --profile web --port <port>` 可访问指定版本并启动，lib 生产模式），同时保持兼容 `@deepseek-ai/dsh@0.0.1-rc.2`（snapshot0811 的 npm 发版）。实测（npm rc.5 基线）：`dsh web` 启动后 `window.__DSH_BOOT__` 清单包含 `@dsh-external/dsh-ui-progress`（inject: `dsh-client-locale`/`dsh-client-runtime`/`dsh-client-ui-conversation`），`/plugins/@dsh-external/dsh-ui-progress/client.js` 返回 200；src 对 rc.5 基线构建产物 typecheck 全绿（本插件已把 cordis 类型导入与 peer 迁移至 `@deepseek-ai/cordis`，见下）。注意：0811 起 vendored cordis 更名为 `@deepseek-ai/cordis`（npm 发版不再发布 `cordis` 名义的 vendored 包），本插件已迁移（peer 声明 `@deepseek-ai/