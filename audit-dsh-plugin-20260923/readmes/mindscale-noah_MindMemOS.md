<p align="center">
  <img src="./assets/mindmemos-readme-hero.png" alt="MindMemOS Memory For AI Agents">
</p>

<p align="center">
  <a href="https://mindmemos.cn">
    <img src="https://img.shields.io/badge/Website-mindmemos.cn-0A66C2?labelColor=gray&logo=googlechrome&logoColor=white" alt="MindMemOS Website">
  </a>
  <a href="https://mindmemos.cn/#/api-docs">
    <img src="https://img.shields.io/badge/FastAPI-Docs-009688?labelColor=gray&logo=fastapi&logoColor=white" alt="MindMemOS FastAPI Docs">
  </a>
  <a href="https://pypi.org/project/mindmemos-sdk/">
    <img src="https://img.shields.io/pypi/v/mindmemos-sdk?color=%2334D058&label=pypi%20sdk&labelColor=gray&logo=pypi&logoColor=white" alt="MindMemOS SDK PyPI version">
  </a>
  <a href="https://www.npmjs.com/package/@mindmemos/openclaw-plugin">
    <img src="https://img.shields.io/npm/v/%40mindmemos%2Fopenclaw-plugin?label=npm%20plugin&labelColor=gray&logo=npm&logoColor=white" alt="MindMemOS OpenClaw Plugin npm version">
  </a>
  <a href="https://www.npmjs.com/package/@mindmemos/deepseek-harness-plugin">
    <img src="https://img.shields.io/npm/v/%40mindmemos%2Fdeepseek-harness-plugin?label=dsh%20plugin&labelColor=gray&logo=npm&logoColor=white" alt="MindMemOS DeepSeek Harness Plugin npm version">
  </a>
  <a href="https://arxiv.org/abs/2608.12428">
    <img src="https://img.shields.io/badge/arXiv-2608.12428-B31B1B?labelColor=gray&logo=arxiv&logoColor=white" alt="MindMemOS arXiv paper">
  </a>
  <a href="#license">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg?labelColor=gray" alt="MIT License">
  </a>
</p>

<p align="center">
  <strong><a href="README_ZH.md">简体中文</a></strong>
  &nbsp;&nbsp;│&nbsp;&nbsp;
  <strong><a href="https://mindmemos.cn">Website</a></strong>
  &nbsp;&nbsp;│&nbsp;&nbsp;
  <strong><a href="https://mindmemos.cn/#/api-docs">API Docs</a></strong>
  &nbsp;&nbsp;│&nbsp;&nbsp;
  <strong><a href="https://pypi.org/project/mindmemos-sdk/">PYPI SDK</a></strong>
  &nbsp;&nbsp;│&nbsp;&nbsp;
  <strong><a href="docs/deploy/instruction.md">Deployment Guide</a></strong>
</p>

<p align="center">
  Accurately remember user and task context and reuse it across agents; evolve memory through ongoing interactions, automatically distill Skills, and connect with file-based knowledge systems so experience truly becomes capability.
</p>

> ⭐ **Star us on GitHub to automatically upgrade to a Pro quota membership.**

## 📰 News

- **2026-08-18**: We released the [DeepSeek Harness Plugin](https://www.npmjs.com/package/@mindmemos/deepseek-harness-plugin), letting DeepSeek Harness (dsh) agents automatically recall and write MindMemOS memories.
- **2026-08-14**: We released the [MindMemOS 1.0 technical report](https://arxiv.org/abs/2608.12428), *MindMemOS: A Portable and Self-Evolving Memory Operating Layer for AI Agents*.
- **2026-07-17**: MindMemOS integrated with [LLM4AD_NEXT](https://github.com/Optima-CityU/LLM4AD_Next), providing searchable long-term memory for algorithm design tasks and enabling the accumulation and reuse of cross-task experience, domain knowledge, and constraints.
- **2026-06-30**: MindMemOS was officially released!

## 🌟 Core Features

- **Portable across agents**: Persist user profiles, preferences, project facts, tool experience, and skill candidates as reusable assets, allowing OpenClaw, Hermes, Claude Code, OpenHands, and other agents to share or transfer the same long-term memory.
- **Self-evolving memory system**: Continuously improve memory quality through schema learning, dreaming, and feedback by automatically learning frequent memory patterns, consolidating memories offline, and using interaction corrections to optimize add/search workflows.
- **Memory and Skills integration**: Experience memories can be distilled into skill candidates, while skill execution results, failure traces, and user feedback flow back into the memory system to drive continuous skill evolution.
- **Plugin integrations**: Connect MindMemOS to different agents and workflows through plugins that retrieve and inject relevant memories before interactions and automatically write conversations back afterward. The [OpenClaw Plugin](https://www.npmjs.com/package/@mindmemos/openclaw-plugin) and [DeepSeek Harness Plugin](https://www.npmjs.com/package/@mindmemos/deepseek-harness-plugin) are currently available, with more integrations in progress.

<p align="center">
  <img src="./assets/mindmemos-benchmark-overview.png" alt="MindMemOS benchmark results overview">
</p>

## 🚀 Quick Start

MindMemOS offers **two deployment modes** (official cloud service, local self-hosting) and **three access methods** (HTTP API, Python SDK / CLI, agent plugin). Any combination works — server and client speak the same protocol:

| Access Method | Use Case | Cloud base_url | Local base_url |
| :--- | :--- | :--- | :--- |
| [HTTP API](https://mindmemos.cn/api-docs) | Call directly from business apps | `https://mindmemos.cn` | `http://127.0.0.1:8000` |
| [Python SDK / CLI](https://pypi.org/project/mindmemos-sdk/) | Integrate into business apps | `https://mindmemos.cn` | `http://127.0.0.1:8000` |
| [OpenClaw Plugin](https://www.npmjs.com/package/@mindmemos/openclaw-plugin) | Agent auto-recalls / writes memory | `https://mindmemos.cn` | `http://127.0.0.1:8000` |
| [DeepSeek Harness Plugin](https://www.npmjs.com/package/@mindmemos/deepseek-harness-plugin) | Agent auto-recalls / writes memory (dsh) | `https://mindmemos.cn` | `http://127.0.0.1:8000` |

To try it without deploying, use the official cloud service (request an API key on the [website](https://mindmemos.cn)); for on-premises or offline use, start with Local Deployment below.

### 1. Local Deployment

MindMemOS uses `uv` to manage dependencies and run local commands. For detailed configuration instructions, see [docs/deploy/instruction.md](docs/deploy/instruction.md).

#### 1.1 Prepare Configuration Files

```bash
cp .env.example .env
cp config/mindmemos/dev.example.yaml config/mindmemos/dev.yaml
```

Before startup, configure at least the following three model routers in `config/mindmemos/dev.yaml`:

- `chat_model_router`: supports memory extraction, Skill evolution, and other generation tasks.
- `embed_model_router`: generates semantic embeddings; make sure its dimensions match the Qdrant dimension configuration.
- `rerank_model_router`: optional; reranks memory retrieval results.

The schema memory-extraction flow is versioned: `algo_config.add.schema.version` defaults to `v2` (rule-based graph fusion) and can be pinned to `v1` (develop-compatible flow) per project. Storage is compatible in both directions; see the deployment guide for binding and effective timing.

Configure an API key and its bound `project_id` in `config/mindmemos/api_keys.yaml`.

#### 1.2 Start the Service

Start the local service:

```bash
make dev
```

`make dev` starts the full Docker dependency stack before starting FastAPI.

To start only core dependencies:

```bash
make dev-core          # Qdrant + Neo4j + Kafka
make db-observability  # Qdrant + Neo4j + Kafka + ClickHouse + OTel + Grafana
```

The default local service port is 8000:

```text
FastAPI:   http://127.0.0.1:8000
```

Stop the local service:

```bash
make dev-down
```

### 2. Access Methods

Cloud and local self-hosting use the same access protocol. Local keys come from `config/mindmemos/api_keys.yaml`; cloud keys are obtained from the [website](https://mindmemos.cn).

#### 2.1 HTTP API

HTTP is the base access method — the SDK and plugins also talk HTTP underneath. Once the service is up, first use curl to verify the endpoints work, then wire up your business logic. Define the address and key before calling (pick local or cloud):

```bash
export BASE_URL=http://127.0.0.1:8000   # Local self-host; change to https://mindmemos.cn for cloud
export API_KEY=dev-api-key-001          # Local example key; use a website-issued key for cloud
```

Add a memory:

```bash
curl -sS -X POST "$BASE_URL/v1/memory/add" \
  -H "Authorizat