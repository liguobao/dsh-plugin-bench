# Token Bank

> **Personal AI Hub · Token Manager**
>
> See clearly · Spend less · Stay simple · Get smarter with you · Earn from idle
>
> One-click Claude / Cursor / Codex / WorkBuddy onboarding · one-stop trace & routing · portrait-driven discovery · community sharing & remote agents

[中文文档](./README.zh-CN.md) · [Download Latest](https://github.com/wink-run/tokenbank/releases/latest) · [Architecture](./DESIGN.md) · [Privacy Policy](./docs/PRIVACY_POLICY.md)

---

## Overview

**Token Bank is a next-generation personal AI resource hub** that enables one-click onboarding and intelligent orchestration of mainstream AI tools like Claude, Cursor, Codex, and WorkBuddy through a local gateway architecture.

### Core Value Proposition

- **Usage Transparency**: Full-chain trace makes every token consumption accountable
- **Cost Optimization**: Smart routing automatically switches between local models, free quotas, paid subscriptions, and community-shared compute with lossless protocol adaptation
- **Sharing Economy**: P2P compute-sharing network creates a decentralized exchange for models and agents, monetizing idle resources into credits

### Technical Highlights

**Zero-Intrusion Integration**  
Declarative application handlers (CLI env injection + config hot-patching) enable seamless onboarding without modifying agent applications.

**Multi-Protocol Adaptation Layer**  
Transparent protocol conversion (Anthropic Messages, OpenAI Chat, Codex Responses) allows agents to use third-party models without awareness.

**Unified Asset Layer Architecture**  
Community agents run directly on users' existing agent applications (Codex, Claude, Cursor, etc.) without rebuilding harnesses, executing within user-accumulated MCP/Skill/Prompt assets for dual reuse of runtimes and tool ecosystems.

**Scenario Routing Engine**  
- Routing policy learning from usage patterns
- Lossless context compression
- Vision enhancement layer for non-multimodal models (automatic image recognition injection)

**MCP Built-in Relay & Resource Projection Gating**  
Constructs personal knowledge and tool ecosystems with controlled resource deployment.

**AI-Native Architecture**  
Abandons traditional hard-coded rules; lets agents dynamically construct core capabilities (asset discovery, personalized recommendations, routing optimization) based on actual scenarios and continuously evolve—building an agent management platform with agents—achieving high flexibility and robustness.

**Usage-Based Evolution**  
The system automatically extracts work portraits from real call records and session patterns, driving personalized recommendations for MCP/Skill/Prompt/Agent and continuous optimization of routing strategies. Multi-device usage aggregation, agent orchestration, and more make Token Bank truly **smarter with you**.

---

## Why Token Bank

Pain points it tackles:

- Many model plans, little clarity on where tokens go each day
- Free quotas sit unused while paid bills rise; local models idle
- Tools, accounts, and devices don’t line up; Skills / MCP / prompts pile up
- Month-end plan credits expire unused

**Token Bank is your personal AI hub.** Plug Claude Code, Codex, Cursor, WorkBuddy, Kimi Code and more into a local gateway—keep familiar clients, **see clearly, spend less, stay simple**, grow resources from your habits (**get smarter with you**), and turn idle capacity into credits via **community sharing**; community agents can run on someone else’s machine (**earn from idle**).

**Five pillars:**

| Pillar | What you get |
|---|---|
| **See clearly** | One-click onboard; full trace; multi-device analytics; subscriptions vs PAYG side by side |
| **Spend less** | Seamless model swap; smart local-first + task-type routing; scene strategies; optional lossless compression |
| **Stay simple** | One-click onboard/restore; multi-account CLI by directory; tray status; one local address |
| **Get smarter with you** | Work portrait; personalized MCP / Skill / Prompt / Agent discover · accumulate · iterate |
| **Earn from idle** | Contribute idle capacity for credits; **hire agents**; circles & network map |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Desktop (Electron · Mac / Windows) or CLI / Docker Web UI      │
│  Gateway · Providers · Resources · Playground · Usage · …       │
└────────────────────────────┬────────────────────────────────────┘
                             │ loopback
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Local gateway  :11430/v1                                       │
│  · Anthropic Messages / OpenAI Chat / Codex Responses adapters  │
│  · keyScene rewrite · scene/task-type routing · compression     │
│  · Built-in MCP relay (prompts / models / resources / bridge)   │
└───────────────┬─────────────────────────────┬───────────────────┘
                │ local keys stay on device     │ login + relay key
                ▼                             ▼
     Ollama / free API / sub / PAYG      Token Bank cloud
                                             │
                              ┌──────────────┼──────────────┐
                              ▼              ▼              ▼
                         Community P2P   Remote agents   Multi-device
                         (WebSocket)     (run elsewhere) usage merge
```

**Implementation notes:**

| Layer | What it does |
|---|---|
| **App handlers** | Declarative `app-handlers.yaml` for CLI shim / config-file patch / session scan; WorkBuddy, Trae, Hermes, Kimi use strong install signals |
| **Routing** | Unified “route = selector chain”: personal/community/free/paid filters + task-type presets (`design` / `repo-qa` / `chore` / `debug`) |
| **Resource projection** | Skill / Prompt / MCP only onto **hosted and installed** targets; apps without stdio use the built-in MCP relay |
| **Telemetry** | Live gateway logs + local session import (Claude / Codex / Cursor / WorkBuddy Trace, …) with auto-dedupe |

---

## Core capabilities: one-click onboarding · seamless model swap · full trace

Token Bank is more than an API proxy — it brings **Claude Code, Codex, Cursor, WorkBuddy, Kimi Code, OpenClaw**, and other mainstream agents under one local gateway. **No agent-side changes required** for usage tracing, third-party model switching, and smart routing.

### One-click agent onboarding

Open the **Gateway** tab — installed tools appear automatically (desktop apps can be added manually):

| Agent | How it connects |
|---|---|
| Claude Code / Codex CLI / OpenCode / Hermes / Kimi Code | CLI shim: injects `BASE_URL` (and related) env vars — no command changes |
| Claude Desktop / Codex Desktop / OpenClaw / WorkBuddy | Config-file patch: one click to point at the local gateway (missing configs may be created after strong install detection) |
| Trae Work | Session import + manual gateway params inside the IDE |
| Cursor / Copilot / Qwen / Grok / … | Session stats, or set `OPENAI_BASE_URL` / a dedicated Gateway key |

**Onboarding flow:**

1. Click **Track** → start counting that app's token usage (even on the official subscription)
2. Pick a **model or scene route** in the dropdown → config is rewritten automatically; traffic goes through the gateway
3. Click **Revert** → restore the official config and stop tracking

Three states, clearly separated: **stats only** (official sub + session import), **via gateway** (route bound + live proxy), **reverted** (original config restored).

### Seamless third-party model switching

Agents keep their native model names (`claude-sonnet-4-6`, `gpt-5`, …). **The client never needs to change:**

```
Claude Code requests claude-sonnet-4-6
        ↓  gateway keyScene transparent rewrite
Actually routed → Groq llama-3.3-70b / local Ollama / DeepSeek / …
        ↓  protocol adapter
Anthropic Messages ↔ OpenAI Chat ↔ Codex Responses
```

- **Model names unchanged** — Claude client validation and UI