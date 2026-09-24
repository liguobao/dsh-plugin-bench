# DeepSeek Harness 白皮书 · dsh-handbook

> **DeepSeek Harness 中文手册 × 生态观察中心**——从 0 到 1 玩转 dsh，跟着 780 帖讨论区看懂生态 · 中文 · [English](./README.en.md)

**📖 [在线阅读](https://electricitysheep.github.io/dsh-handbook/) · 📄 [下载 PDF](https://github.com/Electricitysheep/dsh-handbook/releases) · ⭐ [点 Star 支持](https://github.com/Electricitysheep/dsh-handbook/stargazers)**

*· 15 章手册 · 195 帖社区响应 · 280+ Stars**

<p align="center">
  <img src="./docs/assets/banner.svg" alt="dsh-handbook banner" width="720"/>
</p>

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/Electricitysheep/dsh-handbook?style=flat&color=yellow)
![GitHub release](https://img.shields.io/github/v/tag/Electricitysheep/dsh-handbook?label=release&color=success)
![dsh-handbook](https://img.shields.io/badge/dsh--handbook-白皮书-blue)
![chapters](https://img.shields.io/badge/章节-15-green)
![pdf](https://img.shields.io/badge/PDF-5.5MB-orange)
![license](https://img.shields.io/badge/license-CC--BY--NC--SA--4.0-lightgrey)
![dsh](https://img.shields.io/badge/dsh-v0.1.3--alpha.1-8A2BE2)

</div>

> [!WARNING]
> dsh 当前 GitHub 版本为 `v0.1.3-alpha.1`（预发布 tag；npm 已发布线 `0.1.2-rc.1`），生产环境请谨慎评估，详见 [ℹ️ 版本说明](#ℹ️-版本说明)。

## 🚀 快速体验（30 秒）

```bash
# 1. 安装（需要 Node.js ≥ 22）
npx -y @deepseek-ai/dsh web

# 2. 浏览器打开 http://127.0.0.1:3080，开始对话
# 3. 或跑一次性任务（适合脚本/CI）
dsh --profile headless "你好，请用一句话介绍自己"
```

> 想系统学？看 [🗺 学习路径（3 天计划）](./docs/roadmap.md)；想先跑？[第 2 章：五分钟快速上手](./docs/02-quickstart.md)；想速查？[📇 一页速查卡](./docs/cheatsheet.md)

<p align="center">
  <img src="./docs/assets/demo-webui.gif" alt="dsh Web UI 实测演示" width="720"/>
  <br/>
  <sub><b>30 秒看懂 dsh Web UI</b>：新建会话 → 输入任务 → 模型选择 → 发送 → AI 回复</sub>
</p>

## 🎯 这是什么

**DeepSeek Harness（`dsh`）**是 DeepSeek 官方 2026-08-13 开源的 Agent 运行时——一个"一切皆插件"（everything is a plugin）的框架。

<img width="614" height="230" alt="image" src="https://github.com/user-attachments/assets/19482c24-2208-468e-ad38-9096d9270f8d" />

但官方文档以架构说明为主，**缺少一条从零上手的路径**。

**这本白皮书补上这条路**：从"什么是 Agent 运行时"讲起，到安装、使用、开发插件、性能调优——每一章都有可复制、可运行的命令，全部在本机实测验证。**目标是：任何一个开发者，跟着这本书都能从 0 到 1 用起来、写起来。**

### 为什么值得读（而不是只看官方文档）

| 官方文档 | 本白皮书|
|---|---|
| 架构视角（AGENTS.md / architecture.md） | **新手视角**：一条从 0 到 1 的路径|
| 零散示例 | **每章可运行**，命令全部实测|
| 无中文教程 | **中文优先**，英文同步|
| 无生态实操 | **真实插件/PR 拆解**（含踩坑与安全约束）|

## 🎁 这本能给你什么


| 如果你是… | 你会得到 |
|---|---|
| 🆕 **第一次接触 dsh** | 3 天从 0 到 1 学习路径（每天有目标+验收） |
| 🛠 **开发者** | 可克隆的插件模板 + 配置参考大全（照抄能跑） |
| ⚖️ **正在选型** | 6 个主流 Agent 对比（表格+文字）+ 同模型实测 benchmark |
| ⚡ **要调优** | 推理档位策略 + 缓存命中率专题（实测 97%） |
| 📚 **要案例** | 5 个真实复杂案例（含耗时/产物/验证） |

## 🌟 感谢与社区

首先要感谢每一位 Star、回复和投稿——这本手册不是一个人的作品，是 dsh 社区一起"长"出来的。

发布两天，很幸运得到了这些反馈：

- ⭐ **280+ Stars**——对一份刚发布的教程来说远超预期，感谢大家认可
- 💬 **官方库 195 帖回应**——我们持续在[讨论区](https://github.com/deepseek-ai/deepseek-harness/discussions)和大家一起踩坑、排障、交流
- 🧠 **FAQ 里的 39 条问题大多来自真实提问**——社区问什么，我们沉淀什么（#380/#817/#1052…）
- 📦 已向 [awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) 提交收录 PR（[#33](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin/pull/33)，待合并）；阮一峰周刊自荐已提交
- 🤝 与 30+ 社区项目互链（dsh-usage / dsh-sgme / AgentSoul / dsh-vault / egress-guard / agentmemory…）

> 内容随讨论区持续更新（[沉淀流水线](./docs/research/feedback-pipeline.md)，19 项可追踪）。如果你觉得有用，Star 是对我们最大的支持。

## 🔭 生态观察（第 15 章·全景报告）

> 把 **1804 个插件仓库**的数据盘点 × **780 帖讨论区**定性观察交叉验证，5 个关键结论：

| 结论 | 一句话 |
|---|---|
| 🪟 **Windows 是第一痛点** | 中文路径（15+ 帖同根因）/ koffi / 端口 / 子进程——数据讨论双证实 |
| 🧩 **"官方没做，社区全做"** | 桌面壳 140+ / TUI / 记忆 77 / 视觉 132——健康互补 |
| 🛡️ **安全审计活跃，工具稀缺** | sandbox 分类仅 9 个插件——**供给缺口** |
| 🐛 **序列化 bug 家族** | unknown tool / reasoning 省略 / run_code 丢弃——rc 期主战场 |
| 💰 **成本透明化是刚需** | 缓存命中 97% 实测 + 成本工具雨后春笋 |

**6 个能力缝**（官方可优先建）：视觉通道 · 记忆 seam · 桌面 TUI 协议 · 评测闭环 · Windows 一等支持 · 插件 registry
> 完整报告（含对开发者/选型者/观望者的建议）：[第 15 章](./docs/15-ecosystem-report.md)

## 📚 目录（从 0 到 1）

<div align="center">

| 🗺️ **[学习路径（3 天计划）](./docs/roadmap.md)** | 从 0 到 1：每天目标 + 验收标准 + 学习原则 |
|---|---|

</div>

### 🟢 阶段 1 · 入门：认知与上手

<div align="center">

| 📖 **[第 1 章 · 认识 Harness](./docs/01-intro.md)** | ⚡ **[第 2 章 · 五分钟上手](./docs/02-quickstart.md)** |
|---|---|
| 与主流 Agent 全面对比 · FAQ · [EN](./docs/01-intro.en.md) | 安装 · web/headless 双模式 · 推理档位 · [EN](./docs/02-quickstart.en.md) |

</div>

### 🔵 阶段 2 · 开发：骨架与插件

<div align="center">

| 🧩 **[第 3 章 · profile 与插件系统](./docs/03-profiles.md)** | 🛠️ **[第 4 章 · 插件开发实战](./docs/04-plugin-dev.md)** |
|---|---|
| 可定制骨架 · 插件挂载 · 扩展点 · 真实坑 | 从零写第一个插件（完整代码 + 测试 + 实机验证） |

</div>

### 🟠 阶段 3 · 实战：场景与调优

<div align="center">

| 📦 **[第 5 章 · dsh 应用场景](./docs/05-cases.md)** | 🚀 **[第 6 章 · 进阶与性能调优](./docs/06-advanced.md)** |
|---|---|
| 5 大场景 · 高缓存命中率专题 · 5 行业视角 | 推理档位策略 · 耗时分析 · 踩坑清单 |

</div>

### 🟣 阶段 4 · 生态：能力与编排

<div align="center">

| 🌐 **[第 7 章 · 生态与资源](./docs/07-ecosystem.md)** | 🧰 **[第 8 章 · 工具与上下文系统](./docs/08-tools-context.md)** | 🔗 **[第 9 章 · MCP 子代理与工作流](./docs/09-mcp-subagent-workflow.md)** |
|---|---|---|
| 官方入口 · 参与路径 · 阅读建议 | 60+ 能力包地图 · 内置工具 · compaction | 外部工具接入 · 并行子代理 · 多步编排 |

</div>

### 🔴 阶段 5 · 进阶：复杂案例与展望

<div align="center">

| 🧪 **[第 10 章 · 复杂实战案例](./docs/10-complex-cases.md)** | 🔮 **[第 11 章 · 未来展望](./docs/11-future.md)** | ⚠️ **[第 12 章 · 已知不足与边界](./docs/12-limitations.md)** |
|---|---|---|
| dsh 真实跑出：数据清洗管线 186s · 5-bug 修复 94s | 技术/生态/竞争/机会/风险 预测 + 时间线 | rc 版诚实版：不稳定性 · 生态早期 · 跨平台短板 |

</div>

<div align="center">

| 🛡️ **[第 13 章 · 安全与沙箱](./docs/13-security.md)** | 💰 **[第 14 章 · 缓存与成本](./docs/14-cost.md)** |
|---|---|
| 沙箱机制 · 权限模型 · 审批流 · 插件安全审计清单 | 缓存命中率实测 97% · 成本模型 · 推理档位联动 · 预算实战 |

</div>

| 📊 **[第 15 章 · 生态全景报告](./docs/15-ecosystem-report.md)** | |
|---|---|
| 1804 插件 × 780 帖交叉验证：5 大洞察 + 6 个能力缝 + 生态参与者建议 |

### 📎 附录

<div align="center">

| 📚 **[附录 A·术语表](./docs/appendix-glossary.md)** · 📦 **[附录 B·官方包速查](./docs/appendix-packages.md)** · 📊 **[附录 C·Benchmark](./docs/benchmark.md)** |
|---|
| 30+ 术语 · 命令速查 · 官方 @deepseek-ai/* 包清单 · 同模型 3 Agent 实测 |

</div>

## 💎 内容精华速览（点开即看，不止链接）

<details>
<summary><b>📖 第 1 章：认识 DeepSeek Harness —— 三个直觉 + 能力矩阵</b></summary>

- **三个直觉**：dsh = Agent 的乐高底座；harness = 套在模型外的工程层；2026 = Agent 可编程时代
- **核心事实**：MIT 开源 · TypeScript · "一切皆插件" · 2026-08-13 发布
- **dsh vs 5 个主流 Agent 能力矩阵**（Claude Code / Codex / OpenCode / Gemini / Kimi）：开源✅、模型无关✅、**官方级插件体系**（独有）、自定义界面✅、headless CI✅
- **选型决策**：深度定制+生态 → dsh；开箱即用 → Claude Code
</details>

<details>
<summary><b>⚡ 第 2 章：五分钟快速上手 —— 30 秒跑起来</b></summary>

- **一条命令启动**：`npx -y @deepseek-ai/dsh web` → http://127.0.0.1:3080
- **双模式**：web（对话 UI）/ headless（`dsh --profile headless "任务"`，CI 友好）

- **推理档位三档**：`low`（最快/简单任务）· `high`（默认）· `max`（最强/复杂推理）——**性能关键：思考占工具链 90% 时间**。>注：`low` 为本白皮书实测网关（pi-ai/opencode-go）档位；**DeepSeek 官方适配器为 `off`（关闭思考/最快）/ `high` / `max`**（见 02-quickstart 2.3 注）
- **第一个插件**：Git 面板 4 步挂载
</details>

<details>
<summary><b>🧩 第 3 章：profile 与插件系统 —— 可定制骨架</b></summary>

- **profile** = bundle 栈 + 你的 patch 层（`package.json` + `cordis.patch.yml`）
- **挂载插件只需 2 处改动**（加依赖 + 加 insert 行）
- **host/client 双半**：一个 npm 包 = Node 侧工具/服务 + 浏览器侧 UI
- **5 大扩展点**：`agent/request` waterfall、`conversationEvents`、`ctx.slots`、`settings`、`ctx.provide`
- **6 个真实踩坑**：rc.1 依赖断裂、插件缺 main、`next()` 忘 await、类型不识别、ModuleLoader、端口占用
</details>

<details>
<summary><b>🛠 第 4 章：插件开发实战 —— 完整可运行代码</b></summary>

- **从零写提速插件**（完整拆解）：纯函数决策 + `agent/request` waterfall 注入
- **核心技巧**：决策逻辑抽纯函数（单测毫秒级）→ 实机只验证"注入是否发生"
- **3 条开发纪律**：先找扩展点 / 逻辑抽纯函数 / 实机验证不能省
- **实机日志证据**：`calls=[{name:"write"}] => reasoningEffort=low`
</details>

<details>
<summary><b>📦 第 5 章：实战案例 —— 三个真实开源 PR 的完整闭环</b></summary>

- **Git 面板 push/pull/fetch**（PR #10）：`--force-with-lease` 安全红线 + 本地 bare-repo 集成测试 + Playwright 实机验证
- **HTML 草稿预览**（PR #11）：沙箱安全约束下的 srcdoc 决策纯函数
- **提速插件示例**：长工具链每步思考降档
</details>

<details>
<summary><b>🚀 第 6 章：进阶与性能调优 —— 时间花在哪</b></summary>

- **性能模型**：工具链任务 90% 时间在模型思考（每次工具调用前）
- **档位策略**：简单轮次 low / 日常 high / 复杂 max——降档是最高杠杆提速
- **7 个真实坑**：含"简单任务突然变快 = 缓存命中"的评测陷阱
- **看成绩单三问**：谁测的 / 什么 harness / 验证器多严
</details>

<details>
<summary><b>🌐 第 7 章：生态与资源 —— 加入 dsh 生态的地图</b></summary>

- **官方入口**：仓库 / API 文档 / Discord / Discussions
- **当前状态**：官方暂不收外部 PR → **做 dsh-p