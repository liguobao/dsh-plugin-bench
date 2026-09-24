<div align="center">

# OpenContext

**Your agent forgets why it made decisions. OpenContext fixes that.**

_The context layer for AI agents — a temporal context graph, memory API, and self-evolving loop in one dependency._

</div>

**Context is the missing layer.** Retrieval answers _what_ happened. OpenContext answers _how_ what happened became what is.

**Unlike memory libs that only retrieve,** OpenContext keeps the _why_ — temporal timelines, belief revision, and provenance.

<div align="center">

<p align="center">
<a href="./README.md">English</a> · <a href="./README-zh.md">简体中文</a>
</p>

[![License](https://img.shields.io/badge/License-Apache_2.0-F8D52A?logo=apache)](./LICENSE)
[![npm version](https://img.shields.io/npm/v/@melandlabs/opencontext.svg)](https://www.npmjs.com/package/@melandlabs/opencontext)
[![Discord](https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&logoColor=white)](https://discord.com/invite/xkJaJyWcsv)

</div>

<div align="center">

⭐ **If you find opencontext useful, please consider giving us a star on GitHub!** It helps more people discover the project and motivates us to keep building. 🙏

[![GitHub Repo stars](https://img.shields.io/github/stars/melandlabs/opencontext?style=social&label=Star)](https://github.com/melandlabs/opencontext)

</div>

---

## What is OpenContext?

**OpenContext** is the agentic context runtime that sits underneath an agentic
application — and the substrate you build your own agent on top of.
It is not a UI, a chat surface, or a model provider —
it is the glue between the things that make an agent useful: durable
memory, retrieval, context correction, multi-platform connectivity,
scheduled awareness, and a deterministic loop engine, all behind one dependency.

→ Read [`docs/architecture.md`](./docs/architecture.md) for the full
data model, the lifecycle of a fact, and the transport surface map.

## Who is it for?

OpenContext fits teams who need to **engineer their context** — that is, teams whose day-to-day work runs straight into the problems OpenContext was built to solve. Each bullet spells out the pain and how OpenContext addresses it:

- **Software engineering teams.** Decisions scatter across GitHub PRs, Linear tickets, Slack threads, and Notion docs — across people, tools, and quarters. New hires ask *"why did we pick X?"* and no one can answer. OpenContext's temporal graph stores every fact with `valid_from / valid_until`, so *"what did we believe last quarter?"* is a real, citable query — not a guess.
- **Efficiency / productivity engineering teams.** The people building internal automation for the rest of the company. They don't want another SaaS — they want a runtime they can drop into a CLI, an MCP server, or a daemon. OpenContext is library-first, and the deterministic Loop engine only invokes the LLM when there is real work, so it does not become a token-burning always-on loop.
- **Office-assistant products.** Assistants that live inside Telegram, iMessage, WhatsApp, Lark/Feishu, and friends. Same agent code, same context across channels. `IntegrationRecord` hides credentials, rate-limits, and reconnect logic, while `platform + messageId` is the natural audit trail for personal and work data.
- **Financial trading teams.** Every order, rebalance, and risk decision needs to be traceable and auditable. The temporal graph plus append-only corrections mean *"what was the strategy in April?"* is a queryable fact, not a buried guess — and the trail lines up with MiFID II / SEC retention rules.
- **Legal, healthcare and other audited domains.** Law firms, hospitals, and similar teams where every judgement needs per-fact provenance, append-only corrections, and exportable compliance evidence.
- **Multi-agent and autonomous-workflow authors.** Need scheduled, deterministic wake-up instead of an LLM loop all the way down. `packages/loop` ships exactly that separation.

## Features

|     | Capability                                                                      | What it does                                                                                                                                                                                                                                                                                                                                                                                              |
| --- | ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🧠  | **[Temporal Context Graph](./docs/architecture.md#the-temporal-context-graph)** | A directed acyclic graph where every fact has `valid_from` / `valid_until`. Supersession, contradiction, and merge are first-class edges — corrections are append-only, not destructive.                                                                                                                                                                                                                |
| 🔌  | **[Platform Integration Mesh](./packages/integrations)**                        | One uniform `IntegrationRecord` shape across Gmail, Slack, Telegram, Linear, Jira, iMessage, Feishu, Weixin, … — credential rotation, rate-limit handling, and reconnect logic live behind the adapter.                                                                                                                                                                                                  |
| ⏰  | **[Deterministic Loop Engine](./packages/loop)**                                | A scheduler that wakes up, decides whether there is real work, and only then calls into the agent runtime. LLM calls are not the foundation — they are the last step.                                                                                                                                                                                                                                  |
| 🔍  | **[Retrieval Primitives](./packages/rag)**                                      | Chunking, embeddings, parsers (PDF/ZIP/text), sqlite-vec + pgvector + Chroma adapters. Mix backends without rewriting the recall pipeline.                                                                                                                                                                                                                                                              |
| 🤖  | **[Agent Runtime](./packages/ai)**                                              | AI SDK wrappers, sandbox providers (native / Claude / Vercel), MCP server, memory-consolidation job, image + audio generation.                                                                                                                                                                                                                                                                          |
| 🪶  | **[Library-First API](./packages/opencontext)**                                 | Install once with `pnpm add @melandlabs/opencontext` and get the contracts, memory store, retrieval primitives, loop engine, and agent runtime.                                                                                                                                                                                                          |
| 🛡️  | **[Audit + Encrypted Storage](./packages/audit)**                               | Structured audit logging to `~/.opencontext/logs/audit.jsonl`, Fernet symmetric encryption for secrets, URL allowlist/blocklist for outbound calls.             