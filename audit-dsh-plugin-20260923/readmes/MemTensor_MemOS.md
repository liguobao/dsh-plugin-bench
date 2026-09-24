<div align="center">
  <h1 align="center">
    <a href="https://memos.openmem.net/">
      <img src="https://statics.memtensor.com.cn/logo/memos_color_m.png" alt="MemOS Logo" width="48"/>
    </a>&nbsp;
    MemOS 2.0&ensp;Stardust（星尘）
  </h1>

  <p align="center">
    <a href="https://memos-docs.openmem.net/home/overview/"><img src="https://img.shields.io/badge/Docs-Get--Start-002FA7?labelColor=gray&style=for-the-badge&logo=googledocs&logoColor=white" alt="Docs"></a>
    <a href="https://arxiv.org/abs/2507.03724"><img src="https://img.shields.io/badge/ArXiv-2507.03724-B31B1B?labelColor=gray&style=for-the-badge&logo=arxiv&logoColor=white" alt="ArXiv"></a>
    <a href="https://x.com/MemOS_dev"><img src="https://img.shields.io/badge/Follow-MemOS-000000?labelColor=gray&style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
    <a href="https://discord.gg/Txbx3gebZR"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fdiscord.com%2Fapi%2Fv10%2Finvites%2FTxbx3gebZR%3Fwith_counts%3Dtrue&query=%24.approximate_presence_count&suffix=%20online&label=Discord&color=404EED&labelColor=gray&style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
    <br>
    <a href="https://github.com/IAAR-Shanghai/Awesome-AI-Memory"><img src="https://img.shields.io/badge/Resources-Awesome--AI--Memory-8A2BE2?labelColor=gray&style=for-the-badge&logo=awesomelists&logoColor=white" alt="Resources"></a>
  </p>

  <p align="center">
    <strong>Give your Agent persistent memory and the ability to grow.</strong><br/>
  </p>

  <p align="center">
    <strong>English</strong> | <a href="README_ZH.md">中文</a>
  </p>
</div>


<div align="center">
  <img width="1660" alt="MemOS agent ecosystem: OpenClaw, Hermes, and DeepSeek Harness" src="./assets/readme/memos-agent-ecosystem.png" />
</div>

> [!TIP]
> **New: Connect MemOS to DeepSeek Harness (`dsh`)**
>
> Add automatic recall, background capture, hybrid retrieval, and a local Memory Viewer to DeepSeek Harness—powered by the same MemOS core used across agent ecosystems.
>
> **[Get started →](#memos-plugin)**

---

## 👾 MemOS: Memory Operating System for LLM & AI Agents

**MemOS** is a Memory Operating System for LLMs and AI agents that unifies **store / retrieve / manage** for long-term memory, enabling **context-aware and personalized** interactions with **KB**, **multi-modal**, **tool memory**, and **enterprise-grade** optimizations built in.

### Key Features

- **Unified Memory API**: A single API to add, retrieve, edit, and delete memory—structured as a graph, inspectable and editable by design, not a black-box embedding store.
- **Multi-Modal Memory**: Natively supports text, images, tool traces, and personas, retrieved and reasoned together in one memory system.
- **Multi-Cube Knowledge Base Management**: Manage multiple knowledge bases as composable memory cubes, enabling isolation, controlled sharing, and dynamic composition across users, projects, and agents.
- **Asynchronous Ingestion via MemScheduler**: Run memory operations asynchronously with millisecond-level latency for production stability under high concurrency.
- **Memory Feedback & Correction**: Refine memory with natural-language feedback—correcting, supplementing, or replacing existing memories over time.


### News

- **2026-08-17** · 🐋 **MemOS Connects with DeepSeek Harness**
  MemOS now brings persistent memory to **DeepSeek Harness** through both local and cloud plugins. DSH can automatically recall relevant context before a task and retain new experience after a successful turn, without modifying its core.

- **2026-07-02** · 🏆 **MemOS Advances Agent and User Memory Benchmarks**
  With MemOS, **OpenClaw** improves average task completion from **36.63% to 50.87%** across five agent tasks. MemOS also achieves **88.83 on LoCoMo** and **89.20 on LongMemEval**, and leads in **OmniMemEval**, a unified evaluation of 14 commercial memory products across ten datasets.

- **2026-05-09** · 🧠 **memos-local-plugin 2.0**
  Official local memory plugin for **Hermes Agent** and **OpenClaw**. One core powers self-evolving memory across L1 traces, L2 policies, L3 world models, and crystallized Skills, with local-first storage and feedback-driven retrieval.

- **2026-04-10** · 👧🏻 **MemOS Hermes Agent Local Plugin**
  Official Hermes Agent memory plugins launched: Hybrid retrieval (FTS5 + vector), smart dedup, tiered skill evolution, multi-agent collaboration. 100% local, zero cloud dependency.

- **2026-03-08** · 🦞 **MemOS OpenClaw Plugin — Cloud & Local**
  Official OpenClaw memory plugins launched. **Cloud Plugin**: hosted memory service with 72% lower token usage and multi-agent memory sharing ([MemOS-Cloud-OpenClaw-Plugin](https://github.com/MemTensor/MemOS-Cloud-OpenClaw-Plugin)). **Local Plugin** (`v1.0.0`): 100% on-device memory with persistent SQLite, hybrid search (FTS5 + vector), task summarization & skill evolution, multi-agent collaboration, and a full Memory Viewer dashboard.

## 📊 Performance

MemOS leads across multiple benchmarks — evaluated against mainstream commercial memory products across 5 user memory and 5 agent memory tasks.


| Benchmark       | Score |
| --------------- | ----- |
| LoCoMo          | 88.83 |
| LongMemEval     | 89.20 |
| PersonaMem v2   | 40.58 |
| HaluMem         | 80.91 |
| BEAM-10M        | 56.75 |
| GDPVal          | 62.07 |
| LiveCodeBench   | 64.96 |
| OmniMath        | 61.00 |
| SWE-Bench       | 38.46 |
| BrowseComp-Plus | 23.85 |


Evaluated via OmniMemEval — [https://github.com/MemTensor/OmniMemEval](https://github.com/MemTensor/OmniMemEval).

## 🎯 What MemOS Is For

MemOS gives AI agents long-term memory. Common uses:

- AI assistants with consistent, context-rich conversations
- Customer support that recalls past tickets and user history
- Personalized agents that adapt to individual preferences
- Multi-agent collaboration with shared or isolated memory

## 🚀 Quick Start

MemOS is built around four entry points. Pick the one that matches your scenario.


|              | Cloud API               | Self-Host          | MemOS Cloud Plugin       | Local Plugin                                     |
| ------------ | ----------------------- | ------------------ | ------------------------ | ------------------------------------------------ |
| Best for     | Your app, fully managed | Teams on own infra | OpenClaw users, zero ops | DeepSeek Harness, Hermes, or OpenClaw; on-device |
| Setup        | Get an API key          | docker compose up  | openclaw plugins install | npm install + agent-specific setup               |
| Infra needed | None (hosted)           | Neo4j + Qdrant     | None (uses MemOS Cloud)  | None (local SQLite)                              |
| Data lives   | MemOS Cloud             | Your servers       | MemOS Cloud              | Your machine                                     |

### ☁️ Use the Cloud API (Hosted)

You want to add memory to your app through a fully managed service — no infrastructure to run.

**1. Get an API key:**

- Sign up on the [MemOS dashboard](https://memos-dashboard.openmem.net/cn/quickstart/?source=landing).
- Go to **API Keys** and copy your key (starts with `mpg-`). Keep it server-side.

**2. Add and search memories:**

```python
import requests

API_KEY = "mpg-..."                  # keep this server-side
base = "https://memos.memtensor.cn/api/openmem/v1"
headers = {"Authorization": f"Token {API_KEY}", "Content-Type": "application/json"}

# 1. Add a memory
requests.post(f"{base}/add/message", headers=headers, json={
    "user_id": "alice",
    "conversation_id": "conv_001",
    "messages": [{"role": "user", "content": "I like strawberry"}],
})

# 2. Search memories
res = requests.post(f"{base}/search/memory", headers=headers, json={
    "query": "What do I like?",
    "user_id": "alice",
})
print(res.json())
```

**Next steps:**

- [MemOS Cloud Getting Started](https://memos-docs.openmem.net/memos_cloud/quick_start/) — connect to MemOS Cloud and enable memory i