<div align="center">

<img src="docs/assets/stratagate-avatar.png" alt="StrataGate Agent Memory banner" width="100%" />

# StrataGate

### Recent conversations stay detailed. Older memories grow more concise.

StrataGate gradually condenses an AI agent's short-term memory as the conversation progresses, with original details available to expand when needed. Important information becomes Events and a knowledge graph, preserving historical changes and current state for future sessions.

[![CI](https://github.com/diqierjia/StrataGate-AgentMemory/actions/workflows/ci.yml/badge.svg)](https://github.com/diqierjia/StrataGate-AgentMemory/actions/workflows/ci.yml)
[![npm version](https://img.shields.io/npm/v/stratagate-dsh.svg)](https://www.npmjs.com/package/stratagate-dsh)
[![npm downloads](https://img.shields.io/npm/dt/stratagate-dsh.svg)](https://www.npmjs.com/package/stratagate-dsh)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6.svg)](https://www.typescriptlang.org/)
[![Awesome DSH Plugin](https://awesome-dsh-plugin.com/badge.svg)](https://awesome-dsh-plugin.com)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

[中文说明](README.zh-CN.md) · [DeepSeek Harness guide](docs/DSH.md) · [Architecture](docs/ARCHITECTURE.md) · [Full evaluation](docs/EVALUATION.md)

<strong>Current public result:</strong> on LoCoMo `conv-26`, StrataGate averaged <strong>80.46%</strong> across 10 independent Judge runs, versus <strong>63.22%</strong> for Mem0 base. [See the scope and protocol](#experimental-results).

</div>

> **In plain words:** StrataGate keeps recent conversations detailed and gradually condenses older ones as the conversation progresses. Important information becomes Events and a knowledge graph for future sessions. Original records remain available to expand and verify when needed.

## Why StrataGate?

1. **Short-term memory: details fade as the conversation progresses and expand when needed.**

   (1) **Recent history stays detailed; older history becomes concise.** Each conversation block has six views, L0–L5, with different levels of detail. As more conversation accumulates, older memories gradually shift from full dialogue to key facts, short summaries, and title indexes, reducing the context occupied by history. → [Layered memory](#layered-memory)

   (2) **Views shrink while original records remain.** Complete L5 source messages and tool records are preserved. When details need checking, the agent can expand a memory to recover the original wording and context. → [Layered memory](#layered-memory)

2. **Long-term memory: an event timeline preserves history, while a knowledge graph organizes current state.**

   (1) **Events record what happened.** Important decisions, preferences, plans, and changes are extracted from conversations as Events. Each retains its source and distinguishes when something was mentioned from when it happened, so future sessions can retrieve and trace it. → [Event cards](#event-cards)

   (2) **The knowledge graph represents current state.** Historical Events provide the basis for current information and relationships about people, projects, organizations, tools, and places. New Events can supplement or supersede an earlier state while historical Events and their sources remain preserved. → [Current-state graph](#current-state-graph)

   (3) **Long-term weights decay too.** As conversations progress, memories that have not been adopted gradually lose weight, affecting their priority during retrieval and automatic recall. Their sources remain available for verification even after their weights decay. → [Weights and adoption-based reinforcement](#use-only-reinforcement)

   (4) **Bring memories from other AIs.** Imported content can become traceable Events and update the knowledge graph while the original imported text remains preserved. → [External memory import](#external-memory-import)

3. **Evidence gate: check whether retrieved evidence is sufficient before answering.**

   A relevant search result may still be insufficient to answer the question. The agent assesses the evidence and, when needed, searches again, expands Events, or checks the original messages. If it still cannot confirm the answer, it states the uncertainty. → [Evidence gate](#evidence-gate)

4. **Reinforce only memories actually used.**

   Search hits and automatic context injection do not trigger reinforcement. Only evidence recorded as actually used in the final answer increases the adoption count and resets the decay anchor. More adoptions mean slower future decay, preventing a memory from reinforcing itself merely because it is frequently retrieved. → [Use-only reinforcement](#use-only-reinforcement)

Get started: → [Quick start](#quick-start-deepseek-harness)

## Choose your path

| Path | Best for | Start here |
| --- | --- | --- |
| **DeepSeek Harness plugin** | Users who want automatic, local-first memory with a visual Memory UI | [Install `stratagate-dsh`](#quick-start-deepseek-harness) |
| **Core TypeScript library** | Developers building a custom agent or memory integration | [Library entry points](#code-entry-points) |

<a id="quick-start-deepseek-harness"></a>

## Quick start: DeepSeek Harness

If DeepSeek Harness is already installed, add StrataGate to the profile you use:

```bash
dsh plugin --profile web add stratagate-dsh
```

Restart that profile, then keep using DSH normally. StrataGate will capture completed main-agent turns, build searchable memory in the background, and expose its Memory UI under **DSH Settings → StrataGate-AgentMemory**.

By default, the database is stored at:

```text
DSH_HOME/stratagate/memory.db
```

Removing the plugin does not delete the database. For screenshots, configuration, memory tools, and the exact automatic-capture rules, see the [DeepSeek Harness plugin guide](docs/DSH.md).

## The problem behind the design

As conversations accumulate, an AI agent has to fit the current task, earlier discussions, and lasting information into a limited context window.

Recent discussions often need their full detail. Older conversations can remain as concise summaries and expand when needed. Meanwhile, user preferences, project decisions, and task plans change, making it necessary to distinguish historical records from current state. StrataGate addresses these needs by managing short-term views, long-term updates, retrieval assessment, and usage feedback separately.

| Common problem | How StrataGate handles it |
| --- | --- |
| Conversations keep growing, and historical details continue to occupy context | Store each conversation block as L0–L5 views; as more conversation accumulates, older content defaults to a more concise view and expands when needed |
| Important information is scattered across conversations, and old decisions can be confused with current state | Extract Events with sources and timestamps, preserve history in an event timeline, and organize current state in a knowledge graph |
| Search finds related content but misses details needed to answer | Assess the evidence through the evidence gate; search again, expand memories, or inspect the source when necessary |
| A memory keeps gaining weight merely because it is frequently retrieved | Separate retrieval from adoption: long-term weights decay as conversations progress, and only memories recorded as actually used receive reinforcement |

Short-term decay gradually reduces the detail that older conversations contribute to current context. Long-term memory and its weighting mechanism help the agent recall information that remains useful in future sessions. Both retain sources so condensed information can still be traced and checked.

<a id="how-stratagate-works"></a>

## How it works

![Figure 1: StrataGate workflow—memory formation, automatic activation, active retrieval, and evidence assessment](d