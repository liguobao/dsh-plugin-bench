<p align="center"><img src="web/brand/icon.svg" width="160" alt="AginxBrowser"></p>

# AginxBrowser

English | [中文](README.zh-CN.md)

**The Browser for AI Agents. See the live web. Read it. Act on it. Remember it.**

[![skills.sh](https://skills.sh/b/yinnho/aginxbrowser)](https://skills.sh/yinnho/aginxbrowser) [![MCP Queen operational grade](https://mcpqueen.com/badge/net.aginx/aginxbrowser.svg)](https://mcpqueen.com/s/net.aginx/aginxbrowser)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-compatible-brightgreen)](https://browser.aginx.net/mcp)
[![Hosted](https://img.shields.io/badge/hosted-browser.aginx.net-4dd0ff)](https://browser.aginx.net/)
[![X](https://img.shields.io/badge/X-%40aginxbrowser-black?logo=x)](https://x.com/aginxbrowser)

A browser built for agents from the first line of code — not a human browser bolted onto automation. See the world, read it, search it, act on it, and keep what you read: one Rust binary with built-in V8, **no Chromium required**.

> Humans have Chrome. Agents have AginxBrowser.

One binary, zero dependencies, instant service. HTTP API + native MCP + CDP — agents plug in and go, and existing Playwright / Puppeteer / browser-use code attaches directly.

<video src="https://github.com/yinnho/aginxbrowser/releases/download/v0.5.3/lightpanda-star-story.mp4" controls muted width="720"></video>

*The star that got our attention: Pierre Tachoire, co-founder of [Lightpanda](https://lightpanda.com) — the headless browser our [bench](bench/README.md) measures against — starred the repo. 90 seconds on why that mattered to us.*

*Real pages rendered by AginxBrowser's diting engine (no Chromium) — Wikipedia, this repo, Rust. [Screenshot it yourself →](docs/API.md#screenshot)*

![AginxBrowser rendering real pages](docs/demo.gif)

## Why Agents Need Their Own Browser

Measured against headless Chrome on the same 20 pages, same network ([bench](bench/README.md), 2026-08-28): **7.6× faster** to agent-usable text (p50 532 ms vs 4 053 ms), **~10× less memory** (227 MB for the whole process vs ~2.1 GB per Chrome page), and 0 hard failures where Chrome's `--dump-dom` produced no DOM on 5 of 40 loads. An agent's total cost is browser efficiency × model efficiency — this is the browser half.

Existing "browser automation" was built for humans or for one-shot scraping — not for agents:

| | AginxBrowser | Puppeteer/Playwright | Firecrawl | Browser-use |
|---|---|---|---|---|
| Designed for | **Agents first** | Human debugging | Scraping service | LLM wrapper |
| Dependencies | Single binary, no Chromium | Chromium ~500MB | Docker ~1GB | Chromium |
| Sees (screenshots) | ✅ built-in diting rendering engine | Needs Chromium | ❌ | Needs Chromium |
| Reads | markdown + js_extract + fetch receipts | DIY | markdown | DIY |
| Writes documents | ✅ `render_markdown`: deterministic HTML + inline-SVG diagrams | ❌ | ❌ | ❌ |
| Finds (search) | ✅ 15 engines, 7 categories, merged | ❌ | ❌ | ❌ |
| Acts | indexed session interaction | DevTools API | ❌ | LLM-driven |
| Remembers | ✅ local fetch/search cache (SQLite FTS5) | ❌ | crawl cache | ❌ |
| Protocol | HTTP + native MCP + CDP | Node API | HTTP | Python |
| TLS fingerprints | ✅ Chrome/Firefox/Safari/Edge | Plugin required | ❌ | ❌ |
| CAPTCHA | ✅ detect + auto-wait + optional 2captcha | DIY | ❌ | ❌ |
| Interactive sessions | ✅ persistent | ✅ | ❌ | ✅ |

An agent needs five things from a browser: **see, read, find, act, remember.** One binary covers them all — systemd-friendly, MCP-native for Claude/Cursor, zero dependencies.

**Core advantage: no Chromium.** AginxBrowser inlines a full browser engine (V8 + Rust HTTP stack + the diting CSS/layout/paint rendering engine, with the Blitz/Stylo/Taffy lineage as its reference implementation). No Puppeteer, no Chrome, no Docker. One Rust binary under systemd is your agent browsing infrastructure.

## Three Things Stateless Renderers Can't Do

Most new "agent browsers" are stateless, fingerprint-less one-shot renderers — fine for public pages, dead on arrival against Cloudflare or login flows. AginxBrowser goes the opposite way:

- **🔐 Real TLS fingerprints** — stealth mode replicates the complete Chrome145 / Firefox133 / Safari / Edge TLS handshakes via BoringSSL (not just a UA string), switchable per request; Cloudflare Turnstile challenges wait automatically for `cf_clearance`. Fingerprint-less engines eat 403s — we get through.
- **🤝 Stateful interactive sessions** — login state injectable and exportable (`session_create(cookies=...)` ↔ `session_cookies`), surviving pagination and multi-step flows; `persistent: true` even survives idle eviction and server restarts — the same session id comes back logged in. One-shot engines throw state away.
- **🔌 MCP native** — 37 tools as first-class citizens (not a CDP shim). Claude Code / Cursor / Claude Desktop connect in one line. HTTP + MCP dual protocol — plus a CDP bridge, so the DevTools ecosystem works too.

> Reference point: Cloudflare's Kitesurf explicitly ships neither real TLS-fingerprint negotiation nor persistent auth sessions — anti-bot and login territory is exactly where AginxBrowser plays.

Apache-2.0 open source, single binary — self-host today, no cloud lock-in.

## Every Fetch Is a Receipt

Agents act on what a browser tells them, so the response reports what actually happened — not just "got a 200":

- **`tier`** — which path served the page: plain HTTP (~100 ms) or the V8-rendered browser tier. An agent can see *why* a fetch was fast or slow.
- **`redirected_from`** — the full redirect trail. `redirected_from[0]` is the URL you asked for, `url` is where the content actually came from — requested paired with effective, every hop visible.
- **`content_hash` + `changed_since_prev`** — every fetch is hashed; consecutive samples of the same URL can be diffed. A rate-limited origin serving the same frozen 200 body for days reads as `changed_since_prev: false` — the cheapest drift detector there is.
- **`captcha_event`** — when a challenge page was detected (and solved, if a solver is configured), the response says so instead of handing over a challenge page as if it were content.

The [local cache](#capabilities) builds on the same idea: search hits come back with `[§ heading]` section prefixes so an agent knows *where on the page* a hit landed, and ranking fuses keyword relevance with freshness.

## Capabilities

- **Tiered rendering**: static pages over plain HTTP (~100ms); V8 spins up only when JS rendering is needed (~1-2s) — 90% of the [bench](bench/README.md) page set served without spinning up V8 at all; every response reports which tier served it (`tier` field)
- **Multi-engine meta-search**: general web (Baidu / Bing / Sogou / WeChat / Google / DuckDuckGo), news (Bing News), code (Stack Overflow, GitHub), packages (npm, PyPI), academic (arXiv), AI models (Hugging Face) — 15 engines across 7 categories, queried concurrently, merged and deduplicated. Operators can plug a private Meilisearch index into the same `/search`. Search → read in one step
- **Image search**: `categories=images` hits Baidu/Bing image indexes and returns direct binary `image_url` links (downloadable straight to jpg/png) plus `source_url` provenance
- **Interactive sessions**: persistent browser sessions with indexed interaction (`state/click/input/scroll/eval`) — agents browse like humans do, and `session_export` turns what an agent figured out into a runnable curl replay script (zero model tokens on re-run) — or, with `format=json`, into a flow document (`flow_run` replays it server-side with `{{var}}` substitution, `wait`/`expect` gates and saved outputs; installed flows live in `workflow/<name>/flow.json`, dropped in without a rebuild). Session tools also cover the acting part: `session_viewport` simulates device viewports (media queries respond), `session_wait` blocks on a selector or predicate with a timeout, `session_screenshot` renders the live 