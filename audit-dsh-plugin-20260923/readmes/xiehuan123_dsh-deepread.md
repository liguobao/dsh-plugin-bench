# 📖 DeepRead — Make AI reading traceable

[Website](https://xiehuan123.github.io/dsh-deepread/) · [Real outputs](examples/README.md) · English · [中文](README.zh.md)

> Turn articles, books, PDFs, and document sets into claims you can trace back to evidence and source locations.

[![npm version](https://img.shields.io/npm/v/dsh-deepread)](https://www.npmjs.com/package/dsh-deepread)
[![GitHub release](https://img.shields.io/github/v/release/xiehuan123/dsh-deepread?display_name=tag)](https://github.com/xiehuan123/dsh-deepread/releases/latest)
[![GitHub stars](https://img.shields.io/github/stars/xiehuan123/dsh-deepread?style=flat&label=stars)](https://github.com/xiehuan123/dsh-deepread/stargazers)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-Codex%20%7C%20Claude%20Code-6366f1)](./skills/dsh-deepread/SKILL.md)
[![Awesome DSH Plugin](https://beancookie.github.io/awesome-dsh-plugin/badge.svg)](https://beancookie.github.io/awesome-dsh-plugin)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

![DeepRead evidence-first reading workflow](assets/deepread-demo.svg)

DeepRead is available in two compatible forms:

- **Portable Agent Skill** for Codex, Claude Code, and other Agent Skills-compatible tools. Zero runtime dependencies; the agent follows the evidence-first reading workflow with its own file and web tools.
- **Host plugin package** for DeepSeek Harness Web/headless and dsh-TUI, with a `deepread` tool, PDF extraction, optional persistence/jobs/Web route, batch comparison, cost preview, and HTML/XMind-compatible export. Its browser client is an optional Web-only entry.

## Why it is different

| A typical summary | DeepRead |
| --- | --- |
| Compresses the topic | Extracts complete claims and the reasoning behind them |
| Blends source facts with model inference | Labels author intent, source facts, reasoned inference, and unverified content |
| Makes conclusions hard to check | Pairs important claims with evidence and page/paragraph locations |
| Stops at an answer | Adds knowledge maps, conflicts, limitations, and active-recall questions |

If the source does not support a claim, DeepRead says **“source does not provide evidence”** instead of filling the gap.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/xiehuan123/dsh-deepread/main/.github/assets/deepread-panel-dark.jpg">
    <img src="https://raw.githubusercontent.com/xiehuan123/dsh-deepread/main/.github/assets/deepread-panel-light.jpg" width="470" alt="DeepRead reading panel with input, reading mode, export, focus, and budget controls">
  </picture>
  <br>
  <sub>The real DeepSeek Harness Web reading panel. The portable Agent Skill uses the same evidence-first workflow without this runtime UI.</sub>
</p>

## Quick start

### Portable Agent Skill

```sh
npx skills@latest add xiehuan123/dsh-deepread
```

Then ask your agent:

```text
Deep-read docs/architecture.pdf in knowledge-map mode.
For every important claim, show the supporting evidence and source location.
```

### Full DeepSeek Harness plugin

```sh
dsh plugin --profile web add dsh-deepread
```

If pnpm reports `ERR_PNPM_ADDING_TO_ROOT`, retry with the profile workspace made explicit:

```sh
dsh plugin --profile web add -w dsh-deepread
```

Restart `dsh web`, then use the 📖 reading panel or call the `deepread` tool in chat.

## See real outputs

These are complete reports generated from public articles, not hand-written mockups:

| Report | What DeepRead made visible |
| --- | --- |
| [`deep` · Claude Code token optimization](examples/claude-code-token-optimization.md) | Reconstructed the engineering chain from visibility to input, output, and retrieval-path compression; separated recommendations from project-authored benchmarks. |
| [`map` · Marketing-claim fact check](examples/ad-fact-check-knowledge-map.md) | Found that the article's “90%”, “¥1.28M salary”, and “¥2,000/day” claims had no source, sample, or baseline; marked each one unverified. |
| [`deep` · vivo Tauri architecture](examples/vivo-tauri-architecture.md) | Connected architecture choices to reported size/performance evidence while preserving the article's untested assumptions and deployment limits. |

[Browse all reproducible examples →](examples/README.md)

## Features

| Capability | Details |
| --- | --- |
| 🎛️ Five modes | `quick` key takeaways · `deep` in-depth reading · `map` knowledge map · `feynman` Feynman technique (11-step loop + spaced repetition) · `book` whole-book reading (see the comparison below) |
| 🗺️ Knowledge-map mode | Core question / core conclusion / ten content categories (conclusion, sub-claim, mechanism, fact, data, case, hidden premise, objection, limitation, actionable advice) / every claim paired with evidence (unverifiable claims marked "no evidence provided in the original text") / key data table (value & unit, time range, sample, baseline, source, location) / eight relation labels (supports, refutes, causes, explains, depends on, exemplifies, contrasts, limits) / **four confidence levels** (author intent, original facts & data, reasonable inference, unverifiable) / Mermaid mindmap / XMind outline / 5 active-recall questions |
| 📥 Three inputs | WeChat article URLs (`mp.weixin.qq.com` stable links) · files (`.txt/.md/.html/.pdf`, PDF via a built-in pure-JS extractor with Chinese ToUnicode mapping, page markers, and object-stream/xref-stream support) · pasted text |
| 📤 Optional export | Displayed in-session by default; `export` accepts `md` / `mm` (FreeMind, importable by XMind) / `html` (editor-style web report with light/dark theme) / `all`, written to `deepread-output/` in the workspace |
| 🎨 Browser UI | `deepread` tool result card (four-color confidence legend, collapsible sections) + a 📖 shortcut button next to the input area that opens a card-style reading panel (link/path/text + mode/export selection + reading focus + one-click start) |
| 🔀 Batch compare | Pass 2-10 documents via `batch` (url/path/text each) to get per-document summaries plus a cross-document report: comparison matrix, conflicts, complementarity, and synthesis |
| 📍 Citations | Reports carry page/paragraph provenance: arguments, quotes, and a dedicated citation table locate claims back to `【第N页】` markers in the source |
| 🧮 Cost preview | `estimate: true` previews token spend, model-call count, and expected time per mode without calling the model (CJK≈0.6 tok/char heuristic; rate/latency defaults are picked per model family and can be overridden explicitly) |
| 📚 Recently read | The Web panel keeps a local history of recent reads with one-click re-read (localStorage, no server round-trip) |
| ⏳ Progress transparency | Long reads / big PDFs / batches become official background jobs: the label states segment count and budget; the progress stream pushes 「精读第 3/20 段…」 line by line; job_output polls progress and the final report, job_kill cancels |
| 🔍 Parse progress | Full PDF extraction moves inside the background job and streams **per page** — 「解析 PDF 中… 42%（10/24 页）」 — after a fast sampling preflight decides length (no more silent wait before the background job appears); batches stream per document — 「解析第 2/5 篇… / 精读第 2/5 篇… / 完成第 2/5 篇」 plus 「跨篇对比汇总中…」 |
| 🧮 Panel budget | The Web panel shows per-mode token + time hints above the mode chips (e.g. 深度精读 (≈38k token · ≈8分钟)), instantly for pasted text; calibrated by real model speed; links/file paths are fetched and estimated by the Host through a same-origin API (`POST /api/deepread/budget`) and the panel's 🔍 budget-preflight button shows a one-line result (≈N chars · ≈X token · ≈Y min) right inside the panel — no chat round-trip, no table |
| ⚡ Fast preflight | estimate mode samples the first 2 PDF pages and extrapolates by page count, so big PDF budgets come back in milliseconds |
| 🎯 Self-calibration | Real token/s measured from every model call feeds a rolling average persisted in storage — estimates co