<div align="center">

<img src="./assets/img/Hero.png" width="100%"
alt="DeepSeek Harness hero 横幅：对话自动分层蒸馏成记忆，模型每步前自动召回注入——右侧对话气泡逐层溶解为三层渐亮光带，流入带发光圆球与渐变轨道的玻璃胶囊（下有 日常·工作·智能·关闭 四档刻度），光丝回流示意召回注入">

# dsh-prime-memory

**DeepSeek Harness 的分层蒸馏记忆插件：对话在后台自动完成 L0 捕获 → L1 原子记忆 → L2 场景整合 → L3 画像蒸馏，模型每一步前自动把相关记忆注入上下文。**

[English](README.en.md) · [最新发行版](https://github.com/drscrewdriver/dsh-prime-memory/releases/latest) · [反馈问题](https://github.com/drscrewdriver/dsh-prime-memory/issues)

[![npm version](https://img.shields.io/npm/v/dsh-prime-memory?color=6f83ff\&style=flat-square\&label=npm)](https://www.npmjs.com/package/dsh-prime-memory)
[![DSH 0.1.1-rc.2](https://img.shields.io/badge/DSH-0.1.1--rc.2-8b5cf6?style=flat-square)](https://github.com/deepseek-ai/deepseek-harness)
[![MIT License](https://img.shields.io/badge/license-MIT-536990?style=flat-square)](LICENSE)

</div>

<details open>
<summary>🌐 语言 / Language</summary>

- [中文 README](./README.md)
- [English README](./README.en.md)
- [日本語 README](./README.ja.md)
- [한국어 README](./README.ko.md)
- [安装指南（中文）](./INSTALL.md)
- [Installation guide (English)](./INSTALL.en.md)
- [日本語インストールガイド](./INSTALL.ja.md)
- [한국어 설치 안내](./INSTALL.ko.md)
- [更新日志（中文）](./CHANGELOG.md)
- [Changelog (English)](./CHANGELOG.en.md)
- [日本語 changelog](./CHANGELOG.ja.md)
- [한국어 changelog](./CHANGELOG.ko.md)

</details>

## DSH 版本兼容矩阵

| DSH 版本 | settings 注册 API | 状态 |
|---|---|---|
| 0.1.1-rc.2 | `settings.register()`（live scope） | ✅ 已验证 |
| 0.1.2-rc.1 | `settings.register()`（回退可用） | ⚠️ 按框架文档推断，未实测 |
| 0.1.3-rc.1 | `settings.register()`（回退可用） | ⚠️ 未实测（0.1.3+ 命名空间已改字符串，本插件已兼容） |
| 0.1.5-rc.2 | `settings.register()`（回退可用） | ⚠️ 未实测；Session V3 surface 语义与输入栏/设置槽位待回归 |

> 兼容机制：settings 注册走运行时三分支（`register` → `installSection` 桥接 → 恒开降级），
> 详见 [CHANGELOG.md](./CHANGELOG.md) 的 0.11.0 条目。`dsh.plugin.json` 声明
> `engines.dsh: ">=0.1.1-rc.2 <0.2.0-0"`。

## 快速开始

需要 Node ≥ 22.16。两种调用方式任选（`npx` 前缀可替换下面任何 `dsh` 命令）：

```bash
# 方式一：npx 直接跑官方 CLI（无需预装 dsh；可 pin 版本，如 dsh-prime-memory@0.8.4）
npx -y @deepseek-ai/dsh plugin --profile web add dsh-prime-memory

# 方式二：已装 dsh CLI（dsh 是 pnpm 转发器，未装 pnpm 时先 npm i -g pnpm）
dsh plugin --profile web add dsh-prime-memory

# 包源备选：GitHub 仓库 / 本地路径（开发调试，link: 指向仓库，npm run build + 重启 dsh 即生效）
dsh plugin --profile web add https://github.com/drscrewdriver/dsh-prime-memory
dsh plugin --profile web add /path/to/dsh-prime-memory
```

### 让 Agent 安装（推荐）

如果当前 Agent 可以执行终端命令，把下面这段话完整发送给它：

```text
请为 DeepSeek Harness 的 web Profile 安装 dsh-prime-memory 插件。

只执行下面两条命令，不要修改其他 Profile：
dsh plugin --profile web add dsh-prime-memory
dsh --profile web --dump-config

确认输出中出现 dsh-prime-memory 后告诉我安装结果。
不要替我关闭或重启正在运行的 DSH；安装完成后提醒我手动重启 DSH Web Host。
```

Agent 应当返回安装结果，并明确告诉你配置中是否已经出现 `dsh-prime-memory`。

本包声明了 `dsh.bundle` 组合包层（`cordis.patch.yml`），安装后会**自动挂载插件行**——
不需要再手改 `$DSH_HOME/profiles/web/cordis.patch.yml`。然后重启 DeepSeek Harness，
验证：`~/.dsh/memory/` 下出现 `conversations/ records/ scenes/` 目录和 `memory.db`
即插件 apply 成功；设置页出现"记忆"页面、输入栏出现档位 pill 即 client 半边就绪。

**卸载**：`dsh plugin --profile web remove dsh-prime-memory` + 重启。数据保留在
`~/.dsh/memory/`，不需要时手动删除整个目录即可。

### 从源码开发

```bash
git clone https://github.com/drscrewdriver/dsh-prime-memory
cd dsh-prime-memory
npm install && npm run build
dsh plugin --profile web add .        # link: 安装，改代码后 npm run build + 重启 dsh 即生效
npm run smoke                         # 冒烟测试（先重编：见下方命令）
npx tsc src/smoke.ts --outDir dist-smoke --module nodenext --moduleResolution nodenext --target es2022 --strict --skipLibCheck --esModuleInterop
```

## 运行时数据流

<p align="center">
  <img src="./assets/readme/flow.svg" width="100%"
       alt="dsh-prime-memory 运行时数据流：左侧 User 与 Assistant 的会话事件流入插件（L0 捕获、L1–L3 蒸馏、检索召回、记忆工具），插件经 agent/pre-step 把相关记忆注入右侧 DSH 核心；蒸馏复用核心的 ctx.llm，数据双写 ~/.dsh/memory/">
</p>

插件挂在 dsh 原生事件上（`session/event` 捕获、`agent/pre-step` 注入），蒸馏调用复用宿主 `ctx.llm`。召回以**消息侧注入**呈现：相关记忆作为一条合成消息排在用户新消息之前，会话流里显示为\*\*"上下文注入 · memory"\*\*行（点开看命中内容）——用户能直接看到"记忆生效了"；注入内容有长度预算与时间预算，超限截断/超时跳过，绝不拖慢对话。**同会话去重**：已注入过的记忆不再重复注入（模型上下文里已经有了，追问同类问题时省 token）；上下文被 `/compact` 压缩或清空时自动重置，记忆可重新注入；被更新的记忆（内容变化换新 id）不受旧压制。**时效加权**：召回排序按 `相关度 × max(0.5, 0.5^(距上次更新天数/30))` 软加权——相关度相近的候选之间新鲜记忆优先（名额自然轮转），相关度足够高的老记忆照常召回（地板保证最多损失一半排序分，长期事实不沉底）；`recall.decayHalfLifeDays` 可调，0=关闭。

**成本看板**：每次蒸馏 LLM 调用（抽取/去重/L2/L3）的 token 成本按 `provider/model` 写入
SQLite 明细表（保留期可配置，默认 365 天，写入时滚动清理；记账失败只告警、绝不阻塞蒸馏），
设置页 → 记忆 → **成本** Tab 可视化：按模型分色的趋势折线（日/周/月粒度 + 近 N 天窗口 +
L1/L2/L3 层级过滤）、层级 × 时间窗口表格（调用数 / 输出与思考 token / 均值 / 中位数）、
按模型累计——蒸馏开销一目了然。输入按字符计（dsh 流式 usage 不含输入 token），
输出与思考按 token 计。

**记忆工具(3):**

- memory\_search

- conversation\_search

- memory\_read\_scene

真机实录：召回注入与工具调用在对话里的样子——"上下文注入 · memory"行先带出相关记忆，模型再按需调 `memory_read_scene` 读取场景块，凭记忆直接作答：

<p align="center">
  <img src="./assets/img/MemoryTools.png" width="60%"
       alt="对话界面实录（浅色主题）：用户消息"我们最近要干什么？"上方可见"上下文注入 · memory"行；助手回答前列出 4 次 memory_read_scene 工具调用（参数为 scenes 场景块的 .md 文件名），随后凭记忆梳理近期目标与推进路线">
</p>

在只开放代码执行入口的受限会话中，模型经由 `run_code` 间接调用记忆工具（轨迹视图中的 SUBTOOL 嵌套）：

<p align="center">
  <img src="./assets/img/ToolTrajectory.png" width="80%"
       alt="工具调用轨迹视图：顶部彩色时间线与左侧步骤列表（SYSTEM/CONTEXT/USER/ASSISTANT/TOOL/SUBTOOL 彩色标签），run_code 工具步骤内嵌套 5 次 memory_read_scene 子工具调用（SUBTOOL 标记），右侧为所选步骤的详情面板">
</p>

## 分层记忆（L0–L3）

<p align="center">
  <img src="./assets/img/Layers.png" width="100%"
       alt="分层记忆四层（自左上向右下逐层精炼）：L0 原始对话（对话气泡）→ L1 原子记忆（发光事实粒子）→ L2 场景块（玻璃文档板）→ L3 核心画像（发光晶核）；层间由 LLM 提取/整合/蒸馏光束相连，宽度递减表示数据逐层精炼">
</p>

## 会话级记忆档位

<p align="center">
  <img src="./assets/img/Modes.png" width="100%"
       alt="会话级记忆档位：一条玻璃胶囊滑轨四个停点（日常·工作·智能·关闭），发光圆球停在智能（默认）档；各档上方微场景——日常为个人聊天气泡、工作为代码文档窗格、智能为双流合流最亮、关闭为暗淡虚线幽灵泡">
</p>

- **控件**：输入栏内、模式选择器右侧的 pill（`记忆·自动`），点击在上方浮出档位滑块深浅主题自适应；

- 悬浮板下半部是**会话信息区**：召回命中（命中/检索轮次与累计条数）、攒批进度
  （本会话切片 x/生效阈值；关闭档显示挂起切片数）、本会话产出记忆条数、会话消息数，
  外加异常状态行（存储降级 / 向量检索不可用）与全局摘要（待蒸馏条数、上次蒸馏时间）；
  数据走 `dsh-memory/session-stats` 端点（纯内存注册表 + 索引 COUNT，零文件 I/O），
  打开期间自适应轮询（忙 2s / 静 5s），关闭即停；

- 每会话的选择按 sessionId 持久化到 `session-modes.json`，重启/恢复会话不丢；
  与全局开关叠加（全局是总闸）；L2/L3 完全分类，分类内容不渗透。

- **只写不读（#38）**：悬浮板内「注入」三态开关（跟随全局 / 开 / 关）——设为「关」
  即**只写会话**：捕获与蒸馏照常（对话照常沉淀为 L0→L1→L2/L3），但不向本会话注入
  任何记忆（召回注入、画像/导航稳定区、工具指南一并停止；`memory_search` 等读工具
  返回只写提示）。pill 面文换作 `记忆·只写` 提示状态；覆盖按会话持久化，切回
  「跟随全局」即清除、跟随设置页召回开关；适合调试/评测/敏感会话「只吸收不干扰」。
  与 off 档正交：off 仍是完全隐身（连捕获都关），只写保留「进」关「出」。

## 界面预览

<p align="center">
  <img src="./assets/img/ui-dark.jpg" width="49.5%"
       alt="深色主题下的设置页记忆浏览器概览：状态卡（插件版本、捕获/蒸馏/召回开关状态、FTS 与向量能力、L1 记忆计数、蒸馏模型）与统计瓦片，玻璃质感控件与冷蓝强调色">
  <img src="./assets/img/ui-light.jpg" width="49.5%"
       alt="浅色主题下的同一设置页记忆浏览器概览：同款布局与信息，浅色卡片底与同套强调色，主题切换无需重载">
</p>

## 实测对比（DSH-MemBench：自动化基准）

图文回答"长什么样"，这一节用**自动化基准**的实测数字回答"**开了到底有什么用**"（[`bench/`](./bench/)，一条命令可复现）。方法：同场景库、逐字相同输入，**A 组（记忆开）跑 3 次取合并值，B 组（记忆关）跑 1 次**（无记忆的长任务每场景要吞数倍 token，成本护栏）；对话赛道只跑 A 组（B 组会话独立无记忆必然失败，对照无信息量，已下线）。对话赛道环境：DeepSeek 官方 `deepseek-v4-flash`、插件 0.8.5（判卷与被测同源，答案原文全部留痕可人工复核）、Windows；题型设计借鉴 [LongMemEval](https://github.com/xiaowu0162/longmemeval) / [LoCoMo](https://snap-research.github.io/locomo/) / [AMB](https://github.com/vectorize-io/agent-memory-benchmark)，扩展题型与生命周期赛道参照 [MemoryAgentBench](https://arxiv.org/abs/2507.05257) / [GoodAI LTM](https://github.com/GoodAI/goodai-ltm-benchmark) / BEAM。

> 对话赛道为 **0.8.5 新基线**（修复版插件 + 修正后的判卷口径）；工作流赛道数字仍为 0.8.3 存档（0.8.5 起场景库扩至 8 个，新增前瞻记忆场景，重跑待做）。

### 对话赛道（20 场景 × 10 题型 × 3 次 = 420 题）：答得准吗

> 0.8.5 基线（A 组数据；对话赛道 B 组已下线，只跑 A 组）。

<p align="center">
  <img src="./assets/readme/bench-dialog.svg" width="100%"
       alt="DSH-MemBench 对话赛道准确率图（A 组·记忆开）：总准确率 95.2%（400/420）；核心六题型各 60 题——抽取 58/60、多跳 60/60、时序 56/60、更新 55/60、场景回忆 52/60、拒答 60/60 且 0 编造；扩展四题型各 15 题——增量积累 15/15、连锁更新 15/15、事件排序 14/15、同义改写 15/15">
</p>

**召回双通道**（A 组）：被动注入召回率 **78.1%**（该题要点出现在召回注入中，281/360），其余多数由模型**主动调用记忆工具**查回——106 题主动查询、**75 题靠工具兜底答对**；端到端 95.2% 是两通道 + 模型利用的合成结果。记忆库跨场景全程累积下，探针召回注入混入其他场景记忆 295 次（已如实计数），总准确率反而前段 92.8% → 后段 97.7%——抗干扰能力经受住了膨胀记忆库的考验（离线灌水再灌 600 条合成噪声，检索层 recall\@5 也只降 2.8pp）。

**分层看短板**：检索层离线指标（recall\@5 受控复