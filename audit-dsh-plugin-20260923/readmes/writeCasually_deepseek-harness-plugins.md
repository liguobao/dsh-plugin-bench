# DeepSeek Harness 插件汇总

[中文](README.md) | [English](README.en.md)

一个用于收集、展示和安全审查 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)
（简称 DSH）社区插件的汇总项目。插件列表同时以网页和本 README 两种形式呈现，并每天自动检索
GitHub 上带 `dsh-plugin` 话题的仓库，经过代码安全审查后补充到汇总中。

汇总页面（GitHub Pages）：

[https://writeCasually.github.io/deepseek-harness-plugins/](https://writeCasually.github.io/deepseek-harness-plugins/)

## 项目简介

DeepSeek Harness 以“一切都是插件”为核心设计，社区围绕它产出了大量插件、皮肤与发行版。
本项目把这些分散在 GitHub 上的项目汇总到一处，方便开发者按名称、作者与功能快速查找。

主要能力：

- 网页汇总页：支持搜索、按分类与官方标记筛选，展示每个插件的名称、作者、功能简介与项目链接。
- 单一数据源：`docs/plugins.json` 同时驱动网页与 README 插件列表。
- 多语言简介：插件仓库存在 `README.zh*.md` / `README.en*.md` 等简洁文档时，网页会按当前语言展示对应简介，中文优先、英文兜底。
- DSH 适用性判断：先确认插件是否真正能在 DeepSeek Harness 运行，无法确认的不予收录。
- 分层安全与隐私审查：对非官方插件做证据化静态扫描（危险命令 / 代码执行 / 密钥泄露 / 混淆检测）
  与供应链漏洞检查（OSV），可选 LLM 深度复核；审查留痕（commit、证据、覆盖率），详见
  [docs/security-review.md](docs/security-review.md)。
- 官方优先：DeepSeek AI 官方插件排在最前。
- 人工复核入口：自动检索结果以 Pull Request 形式提交，合并后即可发布到汇总页。

## 官方预设插件

DSH 随包分发一组官方内置插件（`@deepseek-ai/*`，位于官方仓库
[packages/](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages) 目录）。它们的“作用”说明
**独立维护**、不参与社区插件的发现与安全审查 workflow：

- 独立数据源：`docs/official-plugins.json`（`plugins` 数组共 210 个内置插件）。
- 随网页独立“官方预设插件”区块展示；发现/审查脚本（`scripts/*`）与 `.github/workflows/*` **只读写
  `docs/plugins.json`，从不改写或审查官方数据文件**。

可部署的官方 profile bundle：

| 包名 | 作用 |
| --- | --- |
| [`@deepseek-ai/dsh-base`](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/bundle/base) | 共享 dsh 核心，作为每个 profile 的第一层 patch：在空 profile 根上插入全套基础内置插件。 |
| [`@deepseek-ai/dsh-web-app`](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/bundle/web-app) | 浏览器界面 bundle：在 `dsh-base` 上叠加 web patch 层与运行期 glue 插件。 |
| [`@deepseek-ai/dsh-headless`](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/bundle/headless) | 一次性 bundle：无 Host/HTTP/浏览器，直接跑核心 Agent/Session。 |

完整清单与每个包的作用见 [docs/official-plugins.json](docs/official-plugins.json)。

## 插件列表

<!-- PLUGINS_START -->

| 插件名称 | 作者 | 功能简介 |
| --- | --- | --- |
| [archify](https://github.com/tt-a1i/archify) | [@tt-a1i](https://github.com/tt-a1i) | Agent skill for beautiful, verifiable architecture, workflow, sequence, data-flow, and lifecycle diagrams—self-contained HTML with motion and crisp export. |
| [reactive-resume](https://github.com/amruthpillai/reactive-resume) | [@amruthpillai](https://github.com/amruthpillai) | A one-of-a-kind resume builder that keeps your privacy in mind. Completely secure, customizable, portable, open-source and free forever. Try it out today! |
| [app](https://github.com/reactive-resume/app) | [@reactive-resume](https://github.com/reactive-resume) | A one-of-a-kind resume builder that keeps your privacy in mind. Completely secure, customizable, portable, open-source and free forever. Try it out today! |
| [reactive-resume](https://github.com/reactive-resume/reactive-resume) | [@reactive-resume](https://github.com/reactive-resume) | A one-of-a-kind resume builder that keeps your privacy in mind. Completely secure, customizable, portable, open-source and free forever. Try it out today! |
| [OpenViking](https://github.com/volcengine/OpenViking) | [@volcengine](https://github.com/volcengine) | Self-evolving Context Database for AI Agents. Unify Agent Memory, Knowledge RAG and Skills. |
| [WeKnora](https://github.com/Tencent/WeKnora) | [@Tencent](https://github.com/Tencent) | Open-source LLM knowledge platform: turn raw documents into a queryable RAG, an autonomous reasoning agent, and a self-maintaining Wiki. |
| [deepseek-harness-desktop](https://github.com/anywhere-labs/deepseek-harness-desktop) | [@anywhere-labs](https://github.com/anywhere-labs) | 为 DeepSeek Harness (DSH) 插件生态打造的现代化桌面端解决方案。万物皆「插件」，桌面本身也是「插件」。 |
| [dsh-desktop](https://github.com/anywhere-labs/dsh-desktop) | [@anywhere-labs](https://github.com/anywhere-labs) | 为 DeepSeek Harness (DSH) 插件生态打造的现代化桌面端解决方案。万物皆「插件」，桌面本身也是「插件」。 |
| [voyager](https://github.com/Nagi-ovo/voyager) | [@Nagi-ovo](https://github.com/Nagi-ovo) | Enhancement suite for Gemini, AI Studio, Claude & ChatGPT — plus a prompt manager for any web UI, DeepSeek Harness included. / 面向 Gemini、AI Studio、Claude 与 ChatGPT 的增强套件；提示词管理器可用于任意 Web UI，含 DeepSeek Harness。 |
| [awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) | [@awesome-dsh-plugin](https://github.com/awesome-dsh-plugin) | A curated list of plugins for DeepSeek Harness (dsh) · DeepSeek Harness 插件精选列表 |
| [EverOS](https://github.com/EverMind-AI/EverOS) | [@EverMind-AI](https://github.com/EverMind-AI) | One portable memory layer for every AI agent: local-first, Markdown-native, user-owned, and self-evolving across apps, tools, and workflows. |
| [MemOS](https://github.com/MemTensor/MemOS) | [@MemTensor](https://github.com/MemTensor) | Self-evolving memory OS for LLM & AI Agents: ultra-persistent memory, hybrid-retrieval, and cross-task skill reuse, with 35.24% token savings and DeepSeek Harness support. |
| [dsh-desktop](https://github.com/dataelement/dsh-desktop) | [@dataelement](https://github.com/dataelement) | DSHDesktop：DeepSeek Harness Desktop / DeepSeek Harness 桌面版 |
| [dsh-web-ui](https://github.com/zhu1090093659/dsh-web-ui) | [@zhu1090093659](https://github.com/zhu1090093659) | Plugin and skin collection for DeepSeek Harness (DSH) Web UI - task board, git graph, right-side panel, remote mobile UI, pet, live token stats, and skin center. |
| [dsh-web](https://github.com/zhu1090093659/dsh-web) | [@zhu1090093659](https://github.com/zhu1090093659) | DeepSeek Harness（DSH）Web 插件聚合生态包 · 一切皆插件，创意工坊分发 |
| [dsh-routing-suite](https://github.com/yjh051108/dsh-routing-suite) | [@yjh051108](https://github.com/yjh051108) | dsh-routing-suite — injector + router-standard kit: install the runtime injector first, then the task-aware reasoning-mode router preset (measured P1-P23). |
| [BrowserSkill](https://github.com/Tencent/BrowserSkill) | [@Tencent](https://github.com/Tencent) | Let AI agents use your real, logged-in browser without interrupting your work. CLI + extension for browser automation across any shell-capable AI agent. |
| [ouroboros](https://github.com/Q00/ouroboros) | [@Q00](https://github.com/Q00) | Agent OS: the agent gets smarter on its own. We just hold the line: the grading command and expected result never make it into the success contract we hand it. Interview-gated, staged evaluation, budgeted evolution loop. MCP server, 13 runtimes: Claude Code, Codex CLI, Gemini CLI, OpenCode, Copilot, Kiro and more. |
| [loopx](https://github.com/huangruiteng/loopx) | [@huangruiteng](https://github.com/huangruiteng) | Long-horizon agent control plane for durable, governed work across Codex, Claude Code, and other harnesses. |
| [loopx](https://github.com/loopx-project/loopx) | [@loopx-project](https://github.com/loopx-project) | Long-horizon agent control plane for durable, governed work across Codex, Claude Code, and other harnesses. |
| [petdex](https://github.com/crafter-station/petdex) | [@crafter-station](https://github.com/crafter-station) | A public gallery of animated pets for Codex, Claude Code, DeepSeek Harness, Hermes, OpenCode, Gemini CLI, and more. |
| [dsh-anchored-standard](https://github.com/xiaobright/dsh-anchored-standard) | [@xiaobright](https://github.com/xiaobright) | Two-phase DeepSeek Harness preset: Minimal-aligned bootstrap, then full Standard tools (Project2 98/99) |
| [DSH-better-sidebar](https://github.com/omdsh-dev/DSH-better-sidebar) | [@omdsh-dev](https://github.com/omdsh-dev) | 开放的侧边栏底座，支持三方拓展注册新侧边栏页面。内置文件渲染编辑/终端/侧边对话/Git/子代理页面 ｜ Open sidebar foundation, supports third-party extensions to register new sidebar pages. Built-in file rendering/editing, terminal, side chat, Git, and sub-agent pages. |
| [mirage](https://github.com/strukto-ai/mirage) | [@strukto-ai](https://github.com/strukto-ai) | The World's First Unified Virtual Filesystem For AI Agents |
| [ReMe](https://github.com/agentscope-ai/ReMe) | [@agentscope-ai](https:/