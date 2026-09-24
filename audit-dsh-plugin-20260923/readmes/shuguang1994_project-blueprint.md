# Project Blueprint 🏗️

> **One command to make any project AI-agent-ready.**
> 一键为新项目建立完整 AI 编程规范体系。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![skills.sh](https://img.shields.io/badge/skills.sh-project--blueprint-orange)](https://skills.sh)

**Topics** ·
[![dsh-plugin](https://img.shields.io/badge/dsh--plugin-blue)](https://github.com/topics/dsh-plugin)
[![deepseek-harness](https://img.shields.io/badge/deepseek--harness-1f6feb)](https://github.com/topics/deepseek-harness)
[![agent-skills](https://img.shields.io/badge/agent--skills-8A2BE2)](https://github.com/topics/agent-skills)
[![claude-code](https://img.shields.io/badge/claude--code-D97757)](https://github.com/topics/claude-code)
[![cursor](https://img.shields.io/badge/cursor-00A67E)](https://github.com/topics/cursor)
[![codex](https://img.shields.io/badge/codex-18181B)](https://github.com/topics/codex)

[中文文档](README_CN.md)

---

## What is this?

Project Blueprint is a reusable AI agent skill that transforms any new project into an AI-ready codebase in one sentence. It's not a static template — it's an **autonomous discovery engine**: scan your project files, intelligently classify dependencies, and dynamically assemble a customized AGENTS.md, documentation skeleton, CI/CD pipeline, and testing policy from a 95-entry component knowledge base.

Just say: **"Initialize this project's development standards"** and the agent does the rest.

## Quick Install

```bash
# Global (GitHub)
npx skills add shuguang1994/project-blueprint

# China (Gitee mirror, no proxy needed)
npx skills add https://gitee.com/shuguang1994/project-blueprint.git

# Update later
npx skills update project-blueprint
```

**DeepSeek Harness (dsh) plugin**:

```bash
dsh plugin --profile web add 'github:shuguang1994/project-blueprint'
```

Supported agents: Claude Code, Cursor, GitHub Copilot, Codex, Windsurf, Trae, OpenCode, DeepSeek Harness, and 28+ more.

## Why

**AGENTS.md is now an industry standard in 2026** — used by 60,000+ open-source repos, co-promoted by OpenAI, Google, Anthropic, and Microsoft. 76% of developers use AI coding assistants (Stack Overflow 2025), but without AGENTS.md, AI agents are like "new hires with no onboarding" — producing inconsistent code styles, broken architecture, and failing CI.

**Industry data**: Anthropic benchmarks show AGENTS.md reduces wrong-pattern rewrites by **40-60%**. But writing a quality AGENTS.md by hand takes half a day to a full day — repeated for every new project.

**Project Blueprint's approach**: No preset templates. Autonomous scanning → intelligent classification → dynamic assembly. The AGENTS.md you get reflects your project's actual tech stack. And it's the only tool that generates AGENTS.md + docs skeleton + CI pipeline + testing policy + Git conventions — all from one sentence.

## Core Capabilities

| Capability | Description |
|------------|-------------|
| **Autonomous File Discovery** | Scan and classify 30+ file patterns — no preset file checklist |
| **Project Structure Detection** | Auto-identify monorepo, 2/3-tier frontend-backend, or single project |
| **Monorepo Nested AGENTS.md** | Root `AGENTS.md` (global constraints + sub-project index) + per-package `AGENTS.md` (closest-file-wins) when ≥2 build/manifest files |
| **Intelligent Dep Classification** | 3-tier: knowledge base exact match → 29 heuristic patterns → web search |
| **Business Type Inference** | 2-tier heuristic (structure + config features), 12 business types |
| **Dynamic AGENTS.md** | Assembled from a 95-entry component knowledge base, not a template |
| **Module Table Generation** | Reads actual source dirs, infers responsibilities via file patterns, web search fallback |
| **Documentation System** | A/B/C/D/E 5-tier classification, generated per business type |
| **Testing Policy** | Phase-appropriate layered strategy, not forced example files |
| **Multi-IDE Support** | Auto-generates CLAUDE.md, .cursor/rules, copilot-instructions, and more |
| **Vendor Private Enhancement Layer** | Beyond breadcrumbs: Cursor `.mdc` glob activation, Claude Code hooks/subagents skeleton, Copilot instructions layering |
| **Incremental Mode** | Only fills gaps on existing projects, never overwrites |
| **MCP Tool Recommendation** | Recommends MCP tool list + combinations from detected stack, generates `docs/B/B-05-MCP工具清单.md` with install commands (MD only, minimal intrusion) |
| **Self-Evolving** | Generated AGENTS.md includes auto-maintenance rules — updates module table, tech stack, and decisions as the project grows |
| **Progressive Step Loading** | `SKILL.md` slimmed to a ≤200-line index; Step details load on demand from `references/step-*.md` |
| **Real Coding Conventions** | Writes base coding conventions at init (naming/structure/error handling/logging/security/performance 6 categories), B-01 as real 8-chapter doc, not a placeholder |
| **AI Mistake Prevention** | Built-in 7-category 27-item AI common-mistakes KB, injected into core rules at init, iterated via BUG feedback loop |
| **Constitution & Gate Growth** | Writes meta-rules + a 6-step growth loop into AGENTS.md, so the project's AI grows domain gates from the constitution while it works |
| **Gate Registry & Unified Entry** | `scripts/gates.json` as single source of truth + `verify.*` unified entry + `check-constitution` self-check |
| **Doc Contract & Validation** | Doc state headers / numbering / index contract + `docs-check` script (error blocks, warning does not) |
| **AI Work Protocol** | 7-step task lifecycle + evidence standards + DoD + defect retrospective template |
| **Spec-Driven Development (6 phases)** | specify → plan → tasks → checklist → implement → verify; a spec checklist can register directly as a gate (`source: spec#<change-id>`) |
| **Spec-Code Drift Gate** | Seed gate checks deps ↔ AGENTS.md tech-stack row, module table ↔ actual dirs, and gate validity (`drift-check.*`) |

## What It Generates

| Output | Description |
|--------|-------------|
| `AGENTS.md` | Project conventions (governed by architecture principles); in a monorepo: global constraints + sub-project index |
| `<sub-project>/AGENTS.md` | Per-package conventions when ≥2 build/manifest files (monorepo: root = global + index, package = local, closest-file-wins) |
| `docs/` | A/B/C/D/E classified documentation skeleton + README maintenance guides (incl. B-01-开发规范, real 8-chapter conventions) |
| `.github/workflows/ci.yml` | CI pipeline (auto-adapts to language + platform) |
| `.gitignore` | Curated rules per language |
| `CHANGELOG.md` | Version log ([Unreleased] init placeholder, updated per AGENTS.md release policy) |
| `.husky/pre-commit` | Pre-commit lint hook (JS/TS only) |
| `CLAUDE.md` | Claude Code vendor breadcrumb (baseline) |
| `.cursor/rules/project.mdc` | Cursor vendor breadcrumb (baseline + private enhancement layer) |
| `docs/B/B-03-测试指南.md` | Testing policy (layers, timing, framework-specific patterns) |
| `docs/B/B-05-MCP工具清单.md` | MCP tool list + combination suggestions + install commands (on demand) |
| `scripts/gates.json` | Gate registry (single source of truth: source / level / stage / command; seeds 2 seed gates by default) |
| `scripts/verify.*` | Unified gate entry (host auto-selected: Node / Python / make / shell) |
| `scripts/check-constitution.*` | Constitution self-check (AGENTS.md red lines ↔ gate registry, two-way) |
| `scripts/docs-check.*` | Doc consistency check (numbering / state headers / index / archive conflicts + size; **scan range adaptive**: iterates the `docs/` sub-dirs that actually exist; error blocks) |
| `scripts/drift-check.*` | Spec-code drift check (deps ↔ tech-stack row / module table ↔ actual dirs / gate validity) — the 2nd seed gate `spec-drift` |
| `docs/B/B-06-门禁与工作协议.md` | Gate growth loop + evidence standards + DoD (on demand for mid/large projects) |

> **On demand**: small projects only get a single gate + unified entry — no full gate layer or protocol doc (stays 