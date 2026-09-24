<p align="center">
  <a href="README.md"><img alt="English" src="https://img.shields.io/badge/EN-English-blue?style=flat-square"></a>
  <a href="docs-readme/zh-CN/README.md"><img alt="简体中文" src="https://img.shields.io/badge/ZH-简体中文-red?style=flat-square"></a>
  <a href="docs-readme/zh-TW/README.md"><img alt="繁體中文" src="https://img.shields.io/badge/ZH--TW-繁體中文-orange?style=flat-square"></a>
  <a href="docs-readme/ja-JP/README.md"><img alt="日本語" src="https://img.shields.io/badge/JA-日本語-green?style=flat-square"></a>
  <a href="docs-readme/ko-KR/README.md"><img alt="한국어" src="https://img.shields.io/badge/KO-한국어-blueviolet?style=flat-square"></a>
  <a href="docs-readme/es-ES/README.md"><img alt="Español" src="https://img.shields.io/badge/ES-Español-yellow?style=flat-square"></a>
  <a href="docs-readme/fr-FR/README.md"><img alt="Français" src="https://img.shields.io/badge/FR-Français-007EC6?style=flat-square"></a>
  <a href="docs-readme/ru-RU/README.md"><img alt="Русский" src="https://img.shields.io/badge/RU-Русский-informational?style=flat-square"></a>
  <a href="docs-readme/de-DE/README.md"><img alt="Deutsch" src="https://img.shields.io/badge/DE-Deutsch-2EA043?style=flat-square"></a>
  <a href="docs-readme/ar-SA/README.md"><img alt="العربية" src="https://img.shields.io/badge/AR-العربية-success?style=flat-square"></a>
  <a href="docs-readme/vi-VN/README.md"><img alt="Tiếng Việt" src="https://img.shields.io/badge/VI-Tiếng_Việt-cc6699?style=flat-square"></a>
  <a href="docs-readme/uz-UZ/README.md"><img alt="Oʻzbekcha" src="https://img.shields.io/badge/UZ-Oʻzbekcha-1A8BBA?style=flat-square"></a>
  <a href="docs-readme/tr-TR/README.md"><img alt="Türkçe" src="https://img.shields.io/badge/TR-Türkçe-E30A17?style=flat-square"></a>
  <a href="docs-readme/pt-BR/README.md"><img alt="Português-BR" src="https://img.shields.io/badge/PT--BR-Português-1A8BBA?style=flat-square"></a>
  <a href="docs-readme/uk-UA/README.md"><img alt="Українська" src="https://img.shields.io/badge/UK-Українська-0057B7?style=flat-square"></a>
</p>

<h1 align="center">Learn Harness Engineering</h1>

<p align="center"><strong>A project-based course on building the environment, state management, verification, and control mechanisms that make AI coding agents work reliably.</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/Lectures-14-blue?style=flat-square" alt="14 Lectures">
  <img src="https://img.shields.io/badge/Projects-8-green?style=flat-square" alt="8 Projects">
  <img src="https://img.shields.io/badge/Languages-15-yellow?style=flat-square" alt="15 Languages">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square" alt="MIT License">
  <a href="https://github.com/walkinglabs"><img src="https://img.shields.io/badge/Discord-Join_Community-5865F2?style=flat-square&logo=discord&logoColor=white" alt="Join the Discord community"></a>
</p>

> 🌍 This course is available in **15 languages**: English, 简体中文, 繁體中文, 日本語, 한국어, Español, Français, Русский, Deutsch, العربية, Tiếng Việt, Oʻzbekcha, Türkçe, Portuguese (BR), Українська. Choose your language from the badges above.

## 🆕 What's New — August 2026

**Frontier Harness Design Breakdowns — new section (4 breakdowns)**

| What | Details |
|------|---------|
| **New section** | [Frontier Harness Design Breakdowns](docs/en/harness-designs/index.md) — Apply the course's five-subsystem framework (instructions, tools, environment, state, feedback) to reverse-engineer how four frontier products build real harnesses. |
| **Pi** | [How Pi builds its harness](docs/en/harness-designs/pi/index.md) — a minimal kernel, programmable expansion, and context engineering behind "ask Pi to build what you want." |
| **Claude Code** | [How Claude Code builds its harness](docs/en/harness-designs/claude-code/index.md) — four-layer memory, five-level compaction, hooks, and sub-agent isolation. |
| **Codex** | [How Codex builds its harness](docs/en/harness-designs/codex/index.md) — the repository as source of truth, AGENTS.md as a directory page, and worktree isolation. |
| **DeepSeek** | [How DeepSeek builds its harness](docs/en/harness-designs/deepseek/index.md) — "everything is a plugin," capability seams, and an event pipeline. |
| **All 15 languages** | Full translation coverage across all supported languages. |

**Key idea:** The course gives you a framework; these breakdowns show you how the same principles actually play out in production harnesses.

---

**Graph Engineering Update — 1 new lecture, 1 new project**

| What | Details |
|------|---------|
| **Lecture 14** | [From Single Loops to Graph Engineering](docs/en/lectures/lecture-14-graph-engineering/index.md) — Why a single loop grows into a graph: the four stacked layers (prompt → context → loop → graph) and where harness sits in that stack, the four parts of a graph (nodes, edges, shared state, routing), why in-loop checkpoints can't fix the three structural failures at scale (Goodhart, blindness upward, conflict), a framework-agnostic six-step walkthrough for building your first graph, graph vs. workflow, anchors, which open-source "graph engineering" projects existed before the name vs. after it, the orchestration tax, and when a graph is actually worth drawing. |
| **Project 08** | [Draw Your Workflow as a Graph](docs/en/projects/project-08-graph-engineering-first-graph/index.md) — Three progressive experiments: draw your maker-checker loop as an explicit graph, add a parallel fan-out/fan-in node, then add a conditional rollback edge and a human-approval node. |

**Key idea:** A loop is a graph with one node. When your task needs specialization, parallelism, shared state, verification, and recovery — it has stopped being a loop. It's a graph.

---

## 🆕 What's New — July 2026

**Loop Engineering Update — 1 new lecture, 1 new project**

| What | Details |
|------|---------|
| **Lecture 13** | [Why You Need to Stop Prompting Your Agent](docs/en/lectures/lecture-13-loop-engineering/index.md) — From `/goal` to the six primitives of loop engineering (automations, worktrees, skills, connectors, sub-agents, external state), the generator/evaluator split, four silent costs, and a step-by-step guide to building your first loop. |
| **Project 07** | [Build Your First Automated Loop](docs/en/projects/project-07-loop-engineering-first-loop/index.md) — Three progressive experiments: goal loop, timer loop, and maker-checker loop. Compare manual vs. automated, measure intervention reduction, and learn to step outside the loop. |
| **Code templates** | `goal-template.md`, `loop-state-template.md`, `maker-prompt.md`, `checker-prompt.md` — drop-in templates for building loops immediately. |
| **All 15 languages** | Full translation coverage across all supported languages. |

**Key idea:** Harness engineering builds the vehicle. Loop engineering designs the road it drives on — and you design the road from outside the car.

---

Learn Harness Engineering is a course dedicated to the engineering of AI coding agents. We have deeply studied and synthesized the most advanced Harness Engineering theories and practices in the industry. Our core references include:

- [OpenAI: Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
- [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Anthropic: Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [Awesome Harness Engineering](https://github.com/walkinglabs/awesome-harness-engineering)

> **Quick start?** The [`skills/harness-creator/`](./skills/harness-creator/) skill can help you scaffold a production-grade harness (AGENTS.md, feature lists, init.sh, verification workflows) for your own project in minutes.

---

## Table of Contents

- [🆕 What's New](#-whats-new--august-2026)
- [✨ Visual Preview](#-visual-previ