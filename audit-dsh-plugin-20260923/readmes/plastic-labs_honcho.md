<!-- markdownlint-disable MD033 -->
<div align="center">
  <a href="https://app.honcho.dev" target="_blank">
    <img src="assets/honcho.svg" alt="Honcho" width="400">
  </a>
</div>
<!-- markdownlint-enable MD033 -->

---

![Static Badge](https://img.shields.io/badge/Server-3.2.1-blue)
[![PyPI version](https://img.shields.io/pypi/v/honcho-ai.svg)](https://pypi.org/project/honcho-ai/)
[![NPM version](https://img.shields.io/npm/v/@honcho-ai/sdk.svg)](https://npmjs.org/package/@honcho-ai/sdk)
[![CLI](https://img.shields.io/pypi/v/honcho-cli.svg?label=honcho-cli)](https://pypi.org/project/honcho-cli/)
[![Discord](https://img.shields.io/discord/1016845111637839922?style=flat&logo=discord&logoColor=23ffffff&label=Plastic%20Labs&labelColor=235865F2)](https://discord.gg/honcho)

**Honcho is memory infrastructure for building stateful agents that understand changing people, agents, groups, projects, and ideas over time.**

Store messages and events, let Honcho reason in the background, then query peer representations, session context, search results, or natural-language insights from any model or framework. Use it managed at [api.honcho.dev](https://api.honcho.dev), run a local stack with [`honcho start`](#cli), or self-host the FastAPI server yourself.

Using Honcho as your memory system will earn your agents higher retention, more trust, and help you build data moats to out-compete incumbents.

> Honcho has defined the Pareto Frontier of Agent Memory. Watch the [video](https://x.com/honchodotdev/status/2002090546521911703?s=20), check out our [evals page](https://honcho.dev/evals/), and read the [blog post](https://blog.plasticlabs.ai/research/Benchmarking-Honcho) for more detail.

## Contents

- [Start Here](#start-here)
- [Why Honcho](#why-honcho)
- [The Honcho Loop](#the-honcho-loop)
- [Quickstart](#quickstart)
- [What Honcho Gives You](#what-honcho-gives-you)
- [Integrations](#integrations)
- [CLI](#cli)
- [Core Concepts](#core-concepts)
- [Benchmarks & Evals](#benchmarks--evals)
- [Self-hosting](#self-hosting)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [SDKs](#sdks)
- [Learn More](#learn-more)
- [Contributing](#contributing)
- [License](#license)

The Honcho project is split between several repositories, with this one hosting the core service logic — implemented as a FastAPI server. Client SDKs for Python and TypeScript live in the [`sdks/`](./sdks) directory. The [`honcho-cli`](./honcho-cli) package lives here too.

## Start Here

| I want to...                           | Path                                                       | Get started                   |
| -------------------------------------- | ---------------------------------------------------------- | ----------------------------- |
| Give my coding agent persistent memory | Claude Code, OpenCode, OpenClaw, Hermes, or any MCP client | [Integrations](#integrations) |
| Add memory to my product               | Python or TypeScript SDK                                   | [Quickstart](#quickstart)     |
| Run Honcho locally                     | Install CLI, then `honcho start --setup`                   | [CLI](#cli)                   |
| Inspect a deployment                   | `honcho workspace inspect`, `honcho doctor`                | [CLI](#cli)                   |
| Self-host from source                  | Docker Compose or local development                        | [Self-hosting](#self-hosting) |

## Why Honcho

| Capability              | What it means                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------ |
| Reasoning-first memory  | Extracts conclusions from conversations and events, not just matching chunks.        |
| Peer-centric model      | Tracks users, agents, groups, projects, and ideas as entities that change over time. |
| Multi-peer perspective  | Models what one peer knows about another when configured.                            |
| Managed or self-hosted  | Use `api.honcho.dev`, `honcho start` locally, or run the FastAPI server yourself.    |
| Agent-tool integrations | MCP, Claude Code, OpenCode, OpenClaw, Hermes, Cursor-compatible clients.             |

## The Honcho Loop

1. **Store** conversations, events, documents, or tool traces as messages on a session.
2. **Reason** — Honcho processes the queue in the background and updates peer representations.
3. **Query** — ask Honcho for context, search results, peer representations, or a natural-language answer.
4. **Inject** — drop the result into any LLM call or agent framework.

Concretely: workspaces hold peers, peers participate in sessions, messages live on sessions, and Honcho builds a per-peer representation that you query through the [Chat Endpoint](https://honcho.dev/docs/v3/documentation/features/chat) or directly.

## Quickstart

Get an API key at [app.honcho.dev](https://app.honcho.dev) — when you sign up you'll be prompted to join an organization, which gets its own dedicated Honcho instance and $100 free credits. Or install the CLI and run [`honcho start --setup`](#cli), then point the SDK at `http://localhost:8000`.

### Python

```bash
pip install honcho-ai
# or: uv add honcho-ai
# or: poetry add honcho-ai
```

```python
import os
from honcho import Honcho

# Managed service uses api.honcho.dev by default. For self-hosted, pass
# base_url="http://localhost:8000" or set HONCHO_URL.
honcho = Honcho(
    workspace_id="my-app-testing",
    api_key=os.environ["HONCHO_API_KEY"],
)

# 1. Store: peers and messages on a session
alice = honcho.peer("alice")
tutor = honcho.peer("tutor")
session = honcho.session("session-1")
session.add_messages([
    alice.message("Hey there — can you help me with my math homework?"),
    tutor.message("Absolutely. Send me your first problem!"),
])

# 2. Reason: happens asynchronously in the background.

# 3. Query: ask Honcho what it knows, or pull prompt-ready context.
answer = alice.chat("What learning styles does the user respond to best?")
context = session.context(summary=True, tokens=10_000)

# 4. Inject: hand the context to your model of choice.
from openai import OpenAI
client = OpenAI()
completion = client.chat.completions.create(
    model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
    messages=context.to_openai(assistant=tutor),
)
```

### TypeScript

```bash
npm install @honcho-ai/sdk
# or: bun add @honcho-ai/sdk
```

```typescript
import { Honcho } from "@honcho-ai/sdk";
import OpenAI from "openai";

const honcho = new Honcho({
  workspaceId: "my-app-testing",
  apiKey: process.env.HONCHO_API_KEY,
});

const alice = await honcho.peer("alice");
const tutor = await honcho.peer("tutor");
const session = await honcho.session("session-1");
await session.addMessages([
  alice.message("Hey there — can you help me with my math homework?"),
  tutor.message("Absolutely. Send me your first problem!"),
]);

const answer = await alice.chat(
  "What learning styles does the user respond to best?",
);
const context = await session.context({ summary: true, tokens: 10_000 });

const openai = new OpenAI();
const completion = await openai.chat.completions.create({
  model: process.env.OPENAI_MODEL ?? "gpt-4o-mini",
  messages: context.toOpenAI({ assistant: tutor }),
});
```

> **Note:** background reasoning is asynchronous. Newly-added messages may take a moment to be reflected in chat/representation responses; for low-latency reads, use the [`representation`](https://honcho.dev/docs/v3/documentation/features/representation) endpoint.

## What Honcho Gives You

| Need                               | API                                                             |
| ---------------------------------- | --------------------------------------------------------------- |
| Save interaction history           | `session.add_messages(...)`                                     |
| Ask what Honcho knows about a peer | `peer.chat(...)`