<p align="center">
  <img src="docs/icon.png" alt="EchoBird" width="140" />
</p>

<h1 align="center">EchoBird</h1>

<p align="center">Multi-account switching for <strong>ChatGPT, Codex CLI, and Claude Code</strong> · Multi-model smart routing with automatic failover · One-click AI tool setup</p>

<p align="center">
  <a href="https://github.com/edison7009/EchoBird/releases">
    <img src="https://img.shields.io/github/v/release/edison7009/EchoBird?style=flat-square&color=D97757" alt="Release" />
  </a>
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue?style=flat-square" alt="Platform" />
  <img src="https://img.shields.io/badge/built%20with-Tauri%20%2B%20Rust-orange?style=flat-square" alt="Tauri + Rust" />
  <img src="https://img.shields.io/github/license/edison7009/EchoBird?style=flat-square" alt="MIT License" />
</p>

<p align="center">
  <a href="https://echobird.ai">Website</a> ·
  <a href="https://github.com/edison7009/EchoBird/releases/latest">Download</a> ·
  <a href="https://echobird.ai/support/">☕ Buy a coffee</a> ·
  <a href="README.zh-CN.md">中文 README</a>
</p>

> **Note** — This repository is just one of several download channels
> and an issue tracker. For product information, announcements, and
> commercial inquiries, visit [echobird.ai](https://echobird.ai).

---

## 💜 Sponsors

<table>
  <tr>
    <td width="150" align="center">
      <a href="https://go.apimart.ai/gh-echobird"><img src="docs/sponsors/apimart.png" width="140" alt="APIMart" /></a>
    </td>
    <td>
      <a href="https://go.apimart.ai/gh-echobird"><strong>APIMart</strong></a><br/>
      Thanks to <strong>APIMart</strong> for sponsoring this project! APIMart is a low-cost API platform for AI image &amp; video generation — GPT-Image-2 from $0.006/image, 160+ images per dollar. One async API covers both image and video: submit a task, get an ID, fetch results via polling or callback. Batch tens of thousands of images without timeouts, switch models without changing code. Pay-as-you-go with no monthly fee — <a href="https://go.apimart.ai/gh-echobird">sign up here</a> to get started.
    </td>
  </tr>
  <tr>
    <td width="150" align="center">
      <a href="https://88api.ai/sign-up?aff=knFS"><img src="docs/sponsors/88api.png" width="92" alt="88API" /></a>
    </td>
    <td>
      <a href="https://88api.ai/sign-up?aff=knFS"><strong>88API</strong></a> — AI token aggregation platform<br/>
      Thanks to <strong>88API</strong> for sponsoring this project! 88API is a one-stop token aggregation platform: a single API key provides stable access to language &amp; coding models — GPT, Claude, Gemini, Grok, DeepSeek, Kimi, GLM and more — along with image models (GPT-Image, Gemini, Grok), video models (Seedance, Veo, MiniMax Hailuo H3, Kling) and speech (Whisper, TTS), covering everything from copywriting and image creation/editing to video generation and voice-overs. New users get free trial credits to test model capabilities, with human support on site. Operated with overseas corporate credentials — stable and dependable, official invoices, and a 1:1 top-up ratio.
    </td>
  </tr>
  <tr>
    <td width="150" align="center">
      <a href="https://grooroute.com/register?aff=FWGVPMYENJQ8"><img src="docs/sponsors/grooroute.png" width="92" alt="GrooRoute" /></a>
    </td>
    <td>
      <a href="https://grooroute.com/register?aff=FWGVPMYENJQ8"><strong>GrooRoute</strong></a> — Official Claude and GPT models<br/>
      Thanks to <strong>GrooRoute</strong> for sponsoring this project! Official Claude and GPT models are now available. We invite everyone with a curious mind to explore advanced AI, including Fable 5 and GPT-5.6. Connect directly from mainland China and get started with a single line of configuration — <a href="https://grooroute.com/register?aff=FWGVPMYENJQ8">sign up here</a>.
    </td>
  </tr>
  <tr>
    <td width="150" align="center">
      <a href="https://fluxionai.space/register?source=github&amp;campaign=github-echobird&amp;promo=ECHOBIRD"><img src="docs/sponsors/fluxion.png" width="92" alt="Fluxion AI" /></a>
    </td>
    <td>
      <a href="https://fluxionai.space/register?source=github&amp;campaign=github-echobird&amp;promo=ECHOBIRD"><strong>Fluxion AI</strong></a><br/>
      Fluxion AI helps individual developers and businesses access and manage leading AI models worldwide through a unified API. Dynamic routing across multiple upstream connections improves availability, with transparent model performance, response times, and costs. When using Fable 5.1, Fluxion AI can save up to approximately 90% compared with Claude's official API pricing.
    </td>
  </tr>
</table>

Sponsorship contact: [hi@echobird.ai](mailto:hi@echobird.ai)

---

## What is EchoBird?

Friends kept asking me to install **Claude Code**, **OpenClaw**, **Hermes Agent**… every machine was different, and some refused to pay for an LLM. Setup and explanations took forever. So I built **EchoBird** — an Agent inspired by **Songbird**, the genius netrunner from _Cyberpunk 2077_ who solves any tech problem for V…

<p align="center">
  <img src="docs/screenshots/deepseek-harness-demo.gif" alt="DeepSeek Harness One-click install + model switch （DEMO）" width="820" />
  <br/>
  <sub><strong>DeepSeek Harness One-click install + model switch （DEMO）</strong></sub>
</p>

## Highlights

EchoBird offers **4 scenarios** sharing a **unified model data hub** — **configure once, used everywhere**.

### 4 scenarios

- **Install & Repair Agent** — let an AI install and fix mainstream tools (Claude Code, OpenClaw, Hermes Agent, …); works locally and remotely
- **One-click local LLM** — bundled vLLM / SGLang / llama.cpp runtimes; pick a quant, hit START
- **My AI Projects** — onboard and manage your own vibe-coded apps and games inside EchoBird
- **App Manager** — one-click launch and management for every AI / Agent app & game

### Shared foundation

- **Model Nexus** — a unified data hub for OpenAI / Anthropic / local LLMs / API Routers; configure once and all 4 scenarios pick it up; one-click latency check before you commit

**Cross-platform** — Windows, macOS, Linux (x64 + arm64)

## Multi-account switching — ChatGPT, Codex CLI, and Claude Code

Manage multiple saved accounts in EchoBird's **App Manager**, view their usage quota, and choose the account to use when launching a tool.

- **ChatGPT desktop and Codex CLI** — add OpenAI accounts through browser sign-in, then select a saved account and launch. Both tools share the local Codex account configuration, so switching affects the shared login.
- **Claude Code** — add accounts through browser authorization, select an account, and launch Claude Code with it. View the plan, remaining 5-hour and 7-day quota, and reset countdowns when available.
- **Quota at a glance** — check remaining quota and reset times, refresh account usage, and remove saved accounts from the same panel.

**Get started:** open App Manager → choose ChatGPT, Codex CLI, or Claude Code → add and authorize your accounts → select an account → launch. Account selection takes effect on launch; choose a third-party model instead when you want to use an API provider.

## Multi-model smart routing — priority and automatic failover

EchoBird's **Smart Router** puts multiple model providers behind one local API. Add free, paid, or private models from Model Nexus, then drag the cards into your preferred order. The router tries models in that order and automatically falls back when a model is rate-limited, out of quota, or temporarily unavailable. After cooldown, it retries models in priority order.

- **Up to 20 models** — reuse your configured models without entering their API keys again.
- **One endpoint for compatible tools** — supports OpenAI Chat Completions and Anthropic Messages, including clients such as Claude Code.
- **Explicit priority** — you control the order; routing follows that order rather than selecting models by task or price.

**Get started:** open S