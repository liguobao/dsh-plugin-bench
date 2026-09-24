# 🤖 Browser4

<p align="center">
  <a href="https://github.com/platonai/Browser4/actions/workflows/ci.yml"><img alt="CI build" src="https://img.shields.io/github/actions/workflow/status/platonai/Browser4/ci.yml?branch=main&style=flat-square"></a>
  <a href="https://github.com/platonai/Browser4/releases"><img alt="Release" src="https://img.shields.io/github/v/release/platonai/Browser4?style=flat-square"></a>
  <a href="https://github.com/platonai/Browser4"><img alt="Stars" src="https://img.shields.io/github/stars/platonai/Browser4?style=flat-square"></a>
  <a href="https://central.sonatype.com/artifact/ai.platon.pulsar/browser4-core"><img alt="Maven Central" src="https://img.shields.io/maven-central/v/ai.platon.pulsar/browser4-core?style=flat-square"></a>
  <a href="https://www.npmjs.com/package/browser4-cli"><img alt="npm" src="https://img.shields.io/npm/v/browser4-cli?style=flat-square"></a>
  <a href="https://browser4.io"><img alt="Website" src="https://img.shields.io/website?url=https%3A%2F%2Fbrowser4.io&style=flat-square"></a>
  <a href="https://github.com/platonai/Browser4"><img alt="Top language" src="https://img.shields.io/github/languages/top/platonai/Browser4?style=flat-square"></a>
  <a href="https://github.com/platonai/Browser4/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/badge/license-APACHE2-green?style=flat-square"></a>
</p>

---

English | [简体中文](README.zh.md) | [中国镜像](https://gitee.com/platonai_galaxyeye/Browser4)

<!-- TOC -->
**Table of Contents**
- [🤖 Browser4](#-browser4)
  - [🌟 Introduction](#-introduction)
    - [✨ Key Capabilities](#-key-capabilities)
  - [Quick Start](#quick-start)
  - [🧭 Tool Selection Guide](#-tool-selection-guide)
    - [How to Interact with a Page](#how-to-interact-with-a-page)
    - [How to Extract Data](#how-to-extract-data)
    - [How to Process at Scale](#how-to-process-at-scale)
    - [How to Turn HTML into Spreadsheets — Zero Tokens](#how-to-turn-html-into-spreadsheets--zero-tokens)
  - [📦 Installation](#-installation)
  - [💡 CLI Guide for Humans](#-cli-guide-for-humans)
    - [Quick start](#quick-start-1)
    - [Mental model](#mental-model)
    - [Global options](#global-options)
    - [Key concepts before the command list](#key-concepts-before-the-command-list)
    - [Complete command reference](#complete-command-reference)
    - [Timeout environment variables](#timeout-environment-variables)
    - [State persistence](#state-persistence)
  - [🚀 Build from Source](#-build-from-source)
  - [Architecture](#architecture)
  - [📦 Modules Overview](#-modules-overview)
  - [🧩 Programming-Agent Kernel (browser4-coding)](#-programming-agent-kernel-browser4-coding)
  - [🧪 Test Fixture Server (MockSite)](#-test-fixture-server-mocksite)
  - [🤝 Support & Community](#-support--community)
  - [📜 Documentation](#-documentation)
  - [🔧 Proxy Configuration](#-proxy-configuration---unblock-website-access)
  - [License](#license)
<!-- /TOC -->

## 🌟 Introduction

💖 **Browser4 — an AI-native browser engine for autonomous agents, intelligent extraction, and large-scale web automation.** 💖

### ✨ Key Capabilities

* 🤖 **Agent Browser** — AI agents and humans drive real browsers via a Rust CLI, MCP, and an agentic backend: navigate, click, fill, snapshot, batch, and loop.
* 🧬 **Zero-Token Extraction** — X-SQL + CSS selectors for deterministic extraction from live pages or stored HTML snapshots; WebMiner ML clustering turns HTML corpora into spreadsheet and report views with no LLM tokens.
* 🧠 **Hybrid Intelligence** — Combine LLM extraction, ML clustering, X-SQL, and a progressive experience store that reuses learned selectors and blockers.
* ⚡ **High-Performance Runtime** — Coroutine-safe, CDP-native engine designed for 100k–200k complex page visits per machine per day via swarm/crawl scale-out.
* 📦 **Enterprise-Scale Automation** — Swarm crawling, batch/loop jobs, stateful sessions, plugins, runtime skills, browser extension, and MCP-over-HTTP.
* 🛠️ **Programming-Agent Kernel** — 50+ `coding.*` tools (sandboxed shell/fs, scaffolding, validation, self-development) for agents building Browser4 artifacts — or Browser4 itself.

## Quick Start

Paste the following instruction to your favorite AI agent like dsh, claude, codex, workbuddy or openclaw and run it:

```
Read https://browser4.io/SKILL.md, install or upgrade browser4-cli for browser automation, perform the following task:

1. Open the browser in headed mode (`open --headed`) so the window is visible — this is a human-facing demo
2. go to amazon.com
3. search for pens to draw on whiteboards
4. compare the first 4 ones
5. write the result to a markdown file
```

## DeepSeek Harness integration

https://github.com/platonai/dsh-browser4

```
dsh plugin --profile web add dsh-browser4                  # npm registry
dsh plugin --profile web add github:platonai/dsh-browser4  # GitHub
```

## 🧭 Tool Selection Guide

Choosing the right tool for your task:

### How to Interact with a Page

Use `snapshot -i --boxes` to see clickable/typeable elements with refs like `e15`, then `click <ref>`, `fill <ref> "<text>"`, `type`/`press`, `select`, `hover`/`drag`/`scroll`, and `wait` to drive the page. All interaction commands accept CSS selectors too. Chain multiple steps efficiently with `batch`.

Content embedded in `<iframe>`s (payment forms, editors, widgets) is reached with the built-in frame switching: `frames` lists the frame tree, `frame "<iframe selector>"` scopes subsequent element commands into that frame (same-origin iframes fully supported), and `frame main` returns to the main document — no manual `contentDocument` eval needed.

Typical interactive flow:

```bash
# Humans usually want to see the browser — open it headed
browser4-cli open --headed https://example.com/login
browser4-cli snapshot -i --boxes
browser4-cli fill e3 "user@example.com"
browser4-cli fill e4 "secret" --submit
browser4-cli wait --load networkidle
browser4-cli snapshot -i
# iframe-heavy page:
browser4-cli frame "#pay-frame"
browser4-cli fill "#card-number" "4111 1111 1111 1111"
browser4-cli frame main
```

### How to Extract Data

```
Need to extract data from a page?
├─ Interactive page (click, fill, scroll first)? → snapshot + refs, then extract
├─ Static page, one field? → htmlsnapshot get text "<selector>"
├─ Static page, all matches of one field? → htmlsnapshot get all text "<selector>"
├─ Static page, multiple correlated fields (title+price+url per item)?
│  → htmlsnapshot query --sql @query.sql
├─ Live JS / complex DOM logic? → eval --json
├─ Natural language ("find the product price")? → extract (needs LLM key)
└─ High volume, many pages? → crawl or swarm with --sql
```

### How to Process at Scale

```
Need to process multiple pages?
├─ Single list page (search results)? → htmlsnapshot query with DOM_LOAD_AND_SELECT
├─ List of known URLs (in a file)? → crawl --seed-file urls.txt --depth 0 --sql @query.sql
├─ Crawl from a start URL (follow links)? → crawl <url> --out-link-selector "..." --depth N
├─ Need parallel execution (high throughput)? → swarm create → swarm query --seed-file ...
├─ Repeated monitoring (check every hour)? → loop -i 3600 -- eval "..."
└─ Just a few URLs in a shell script?
   → browser4-cli open --headed "https://first-url"   # humans: open once, visibly
   → for url in ...; do browser4-cli goto "$url"; ... done
```

### How to Turn HTML into Spreadsheets — Zero Tokens

[WebMiner](https://github.com/platonai/web-miner) runs ML clustering on downloaded HTML files to produce structured spreadsheets and interactive reports — **no LLM tokens, everything runs locally.** webminer is a first-class Browser4 CLI citizen: `browser4-cli webminer install` + `browser4-cli webminer all <html-dir>` runs the whole pipeline without PowerShell.

```
Have HTML files and want structured data — without tokens?
├─ < 20 pages? → browser4-cli crawl --seed-file urls.txt --depth 0 --sql @query.sql
├─ < 1,000 pages (small to medium)? → WebMiner Free (SMILE ML engine)
│  browse