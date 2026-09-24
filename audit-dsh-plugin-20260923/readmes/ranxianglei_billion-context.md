# billion-context

[English](./README.md) | [中文](./README.zh-CN.md)

<p align="center">
<strong>Universal context-compression proxy</strong> for AI coding agents
<br />
Any agent that can set a base URL — <em>zero per-agent adapter code</em>.
</p>

---

## Community

QQ Group:
1056132097 (full)
1108730198 (open)

---

## 📄 Paper / Preprint

- **[Model-Driven Incremental Hierarchical Compression: Training-Free Multi-Generational Context Management for Long-Lived Coding Agents](./paper/model-driven-incremental-hierarchical-compression-training-free-multi-generational-context-management-for-long-lived-coding-agents.md)** (English, v0.2)

> 📝 **The paper itself is open-sourced under the MIT License as part of the codebase (`paper/`). It is a living document — anyone may edit it; improvements are welcome via pull request.**

A production-scale longitudinal study: 4.5 months, three hosts, 174,327 model calls, 18.76B cumulative input tokens (~24.7B across all hosts), zero window violations on 204,800-token models, marathon sessions of 8,584–12,049 calls.

---

<p align="center">
<a href="https://www.npmjs.com/package/billion-context"><img src="https://img.shields.io/npm/v/billion-context.svg?style=flat-square" alt="npm"></a>
<a href="https://github.com/ranxianglei/billion-context/blob/master/LICENSE"><img src="https://img.shields.io/npm/l/billion-context.svg?style=flat-square" alt="license"></a>
<a href="https://github.com/ranxianglei/billion-context"><img src="https://img.shields.io/badge/GitHub-ranxianglei%2Fbillion--context-181717?style=flat-square&logo=github" alt="GitHub"></a>
</p>

<p align="center">
<code>npm install -g billion-context</code>
</p>

---

`billion-context` sits between **any** agent and its model API, rewriting Anthropic/OpenAI streams with [acp-kernel](https://github.com/ranxianglei/acp-kernel) compression. The model decides **when** and **what** to compress into high-fidelity summaries — not a hard truncation limit.

## Why

Long coding sessions blow up context. Each provider charges per token, and once you pass the context window the session degrades or dies. `billion-context` compresses consumed conversation into layered summaries so you can run a single session for days — billions of tokens through one context window.

Unlike a host's built-in summarizer, compression here is **incremental, reversible, and prefix-cache friendly**: summaries are written in small ranges, can be decompressed on demand, and the cache prefix stays intact.

## How it works

```
Agent (Claude Code / Codex / Cursor / Aider ...)
        │  you point the agent's base URL at the proxy
        ▼
┌─────────────────┐
│  billion-context│   1. parse the request (Anthropic or OpenAI shape)
│     proxy       │   2. run acp-kernel compression on the conversation
│                 │   3. inject a `compress` tool + compression philosophy
│                 │   4. forward to the real model API
│                 │   5. rewrite the streaming response
└─────────────────┘
        │
        ▼
   real model API (Anthropic / OpenAI / compatible)
```

The proxy injects four context-management tools (`compress`, `decompress`, `search_context`, `acp_status`) into the conversation. The model calls `compress` when the conversation grows, and the proxy executes it server-side — the compressed ranges are folded into the conversation history before the next turn.

An opt-in fifth tool, `absorb` (`compress.absorb.enabled: true` — see [CONFIGURATION.md](CONFIGURATION.md)), compresses **individual tool results the moment they arrive**: large results (builds, logs, greps) get a forced absorb instruction, the model distills each into a compact summary, and the original pair is hidden from the wire from the next turn on — keeping mid-session pressure lower between fold rounds (#605).

An opt-in sixth tool, `acp_rule` (`compress.rules: true` — see [CONFIGURATION.md](CONFIGURATION.md)), records **persistent principle-level reminders**: a short rule recorded by the model (user-emphasized lessons, behaviors to remember, major pitfalls hit) is hard-protected from compression — the call and its result stay in context across every fold — and omitting the argument lists the recorded rules ([ranxianglei/billion-context-pi#433](https://github.com/ranxianglei/billion-context-pi/issues/433)).

An opt-in seventh tool, `acp_retrieve` (`compress.ccr.enabled: true` — see [CONFIGURATION.md](CONFIGURATION.md)), backs the **content-addressed message store** (built-in CCR, #1097): oversized tool results are **ID-referenced at arrival instead of force-distilled** — the wire keeps a byte-stable placeholder and the original goes into a per-session content-store envelope (hash-deduped), retrievable on demand via one cheap tool call. Lossless by default: a retrieve not made costs nothing but the call; a detail distilled away by absorb is gone for good. Proxy mode and native-tools wires only in v1 (the marker/text protocol has no channel to execute the retrieve, so the store disarms itself there rather than silently losing content).

A sibling protection knob, `compress.protectedLatestTools` (see [CONFIGURATION.md](CONFIGURATION.md)), keeps the **latest** snapshot of a cumulative tool (a client's todo/task list, e.g. `["todo_list", "TodoWrite"]`) un-compressible while older instances fold normally — so the agent never loses its live task list to a fold (#639). Its full-history counterpart `compress.protectedTools` hard-excludes **every** instance of a tool — for independent-content results no later result supersedes (e.g. opencode/pi `skill` loads); protecting all instances of a chatty or cumulative-snapshot tool grows context without bound (#639), so keep it to low-frequency, high-value tools.

### Two compression modes — who executes `compress`

The proxy runs in one of two modes, and **the mode decides who executes
`compress`, which in turn decides how the summary travels to the model** (the
"carrier"). This distinction is the root of #377.

| | **Launcher / plugin mode** (`bili pi`, `bili codex`, …) | **Proxy mode** (plain client → `/bili/`) |
|---|---|---|
| Client | ACP-native agent with the bili extension (pi/omp) | Any OpenAI/Anthropic client, no extension |
| Who executes `compress` | **The agent** (pi runs it locally) | **The proxy** (server-side compress loop) |
| `compress` tool call in the re-sent history? | Yes — part of the agent's own conversation | No — ephemeral proxy-loop traffic |
| Preflight blocks (no tool call)? | Last-resort backstop — the agent normally compresses on its own `compress` calls, but `src/preflight.ts` still fires (in both modes) when the input alone exceeds the window (#470) | Yes — `src/preflight.ts` compresses behind the client's back |
| **Summary carrier on the wire** | **the `compress` tool call** | **an `acp_summary` user message** |
| System messages on the wire | always exactly 1 (client + prompt) | always exactly 1 (client + prompt) — summaries ride on user messages |
| SGLang "single system" 400 (#377) | cannot happen | cannot happen (summaries are user messages, not system) |
| Proxy-injected `compress` tools | none — the agent registers the 4 ACP tools natively | the 4 context tools (when enabled) |
| Proxy-injected nudge | **yes** — the agent has no nudge channel of its own, so the proxy-side nudge is the proactive compression trigger (preflight alone only fires at the hard limit; #451) | yes (when enabled) |

**Why the carriers differ.** In plugin mode the agent owns compression: the
`compress` call + result live in the agent's own history and are re-sent every
turn, so the summary rides on the tool call and the agent's view never renders
the kernel's `acp_summary` fallback (`billion-context-pi` `src/messages.ts`
skips `acp_summary_*`). In proxy mode the client is not ACP-native, so the
proxy executes `compress` server-side; the tool call never enters the client's
history, and preflight blocks have no tool call at all — so the kernel's
`acp_summary` message is th