<div align="center" id="readme-top">

![EverOS banner](https://github.com/user-attachments/assets/806e9d7f-c861-4b89-9141-11e38f8753e3)

<p align="center">
  <a href="https://x.com/evermind"><img src="https://img.shields.io/badge/EverMind-000000?labelColor=gray&style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
  <a href="https://huggingface.co/EverMind-AI"><img src="https://img.shields.io/badge/🤗_HuggingFace-EverMind-F5C842?labelColor=gray&style=for-the-badge" alt="HuggingFace"></a>
  <a href="https://discord.gg/gYep5nQRZJ"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fdiscord.com%2Fapi%2Fv10%2Finvites%2FgYep5nQRZJ%3Fwith_counts%3Dtrue&query=%24.approximate_presence_count&suffix=%20online&label=Discord&color=404EED&labelColor=gray&style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://github.com/EverMind-AI/EverOS/discussions/67"><img src="https://img.shields.io/badge/WeCom-EverMind_社区-07C160?labelColor=gray&style=for-the-badge&logo=wechat&logoColor=white" alt="WeChat"></a>
</p>

[Website](https://evermind.ai) · [Documentation](https://docs.evermind.ai) · [Blog](https://evermind.ai/blogs) · [中文](README.zh-CN.md)

</div>


<br>

<details>
  <summary><kbd>Table of Contents</kbd></summary>

<br>

- [Why EverOS](#why-ever-os)
- [Ecosystem Integrations](#ecosystem-integrations)
- [Quick Start](#quick-start)
- [Use Cases](#use-cases)
- [Documentation](#documentation)
- [EverMind Ecosystem](#evermind-ecosystem)
- [Contributing](#contributing)

<br>

</details>


## Why EverOS

EverOS is a Python library and local-first memory runtime for agents and
makers. It gives one portable memory layer across coding assistants, apps,
devices, and workflows from day one. It stores conversations, files, and agent
trajectories as readable Markdown, then syncs local SQLite and LanceDB indexes
for fast retrieval and self-evolving reuse.

<table>
<tr>
<th width="28%">Title</th>
<th width="36%">EverOS</th>
<th width="36%">Other Agent Memory Libraries</th>
</tr>
<tr>
<td><strong>Markdown source of truth</strong></td>
<td>✅ Canonical <code>.md</code> files that are readable, editable, diffable, and Git-versioned</td>
<td>❌ Usually API, vector, graph, dashboard, or database state</td>
</tr>
<tr>
<td><strong>Direct file editing</strong></td>
<td>✅ Edit <code>.md</code> files; cascade watcher syncs</td>
<td>❌ Usually SDK, API, dashboard, or backend update paths</td>
</tr>
<tr>
<td><strong>Local three-part stack</strong></td>
<td>✅ Markdown + SQLite + LanceDB; no MongoDB, Elasticsearch, or Redis required</td>
<td>❌ Often depends on managed services, vector DBs, graph DBs, or server stacks</td>
</tr>
<tr>
<td><strong>User + agent tracks</strong></td>
<td>✅ User <code>episodes/profile</code> and agent <code>cases/skills</code> are separate first-class surfaces</td>
<td>❌ Usually centered on chat history, profiles, entities, facts, or retrieval records</td>
</tr>
<tr>
<td><strong>Orthogonal retrieval</strong></td>
<td>✅ Search by <code>user_id</code>, <code>agent_id</code>, <code>app_id</code>, <code>project_id</code>, and <code>session_id</code></td>
<td>❌ Usually app, namespace, tenant, thread, or graph scoped</td>
</tr>
<tr>
<td><strong>Knowledge Wiki</strong></td>
<td>✅ Editable, source-backed Markdown knowledge pages with taxonomy, CRUD APIs, and topic search</td>
<td>❌ Usually separate from memory, trapped in a dashboard, or not tied back to source files</td>
</tr>
<tr>
<td><strong>Reflection</strong></td>
<td>✅ Offline memory evolution that merges episode clusters and refines profiles and skills between sessions</td>
<td>❌ Usually retrieval-only memory with little background consolidation or long-horizon improvement</td>
</tr>
</table>

<br>

## Ecosystem Integrations

EverOS adds durable memory to the agent and workflow platforms below—and comes
built into Raven. Choose an integration to open its setup guide.

<table width="100%">
<tr>
<td width="400" align="center"><a href="https://github.com/EverMind-AI/plugins/tree/main/dsh"><img src="https://avatars.githubusercontent.com/u/148330874?s=200&amp;v=4" alt="DeepSeek Harness" width="72"><br><strong>DeepSeek Harness</strong></a></td>
<td width="400" align="center"><a href="https://github.com/EverMind-AI/plugins/tree/main/hermes"><img src="https://github.com/user-attachments/assets/477eebc4-e615-4425-921e-368d7667e491" alt="Hermes" width="72"><br><strong>Hermes</strong></a></td>
<td width="400" align="center"><a href="https://github.com/EverMind-AI/plugins/tree/main/openclaw"><img src="https://github.com/user-attachments/assets/01d948fe-1e2b-48e8-9b32-b8057cb3f336" alt="OpenClaw" width="72"><br><strong>OpenClaw</strong></a></td>
<td width="400" align="center"><a href="https://github.com/EverMind-AI/Raven"><img src="https://github.com/user-attachments/assets/27e1ea63-69d4-48b3-a884-7f0355926907" alt="Raven" width="72"><br><strong>Raven</strong></a></td>
<td width="400" align="center"><a href="https://github.com/EverMind-AI/plugins#plugins"><img src="https://raw.githubusercontent.com/langgenius/dify/280f81757d5fdea9c2dd804483c7f70c2e95cd9a/web/public/logo/logo-site.png" alt="Dify" width="112"><br><strong>Dify</strong></a></td>
</tr>
</table>

<br>

## Quick Start

> One OpenRouter API key is enough to start EverOS, write durable memories,
> and retrieve them with keyword search.

### Prerequisites

- Python 3.12+
- One [OpenRouter API key](https://openrouter.ai/keys)

### 1. Install

```bash
uv pip install everos
# or: pip install everos
```

### 2. Try the standalone demo — no key required

No API key or server setup required—run one command to quickly experience how
EverOS stores and recalls memory:

```bash
# If you installed EverOS as a package:
everos demo

# If you cloned or forked this repository and have not activated .venv:
uv run everos demo
```

Enter something EverOS should remember, then ask a related question to watch
the memory move through ingest -> extract -> index -> recall.

<https://github.com/user-attachments/assets/98cb8e1e-2ca8-4504-b0a6-0b9a040a0a5c>

### 3. Initialize and add your OpenRouter key

```bash
everos init
```

This creates `~/.everos/everos.toml` and `~/.everos/ome.toml`. Open
`~/.everos/everos.toml`; the generated model and OpenRouter URL are already
correct, so replace only the empty `api_key`:

```toml
[llm]
model = "openai/gpt-4.1-mini"
api_key = "<OPENROUTER_API_KEY>"
base_url = "https://openrouter.ai/api/v1"
```

This is the smallest Tier 1 setup: memory add, flush, Markdown persistence,
cascade indexing, and keyword search.

Use `everos init --root <path>` if you want a different memory root. Pass the
same `--root <path>` to subsequent commands.

### 4. Start EverOS

```bash
everos server start
```

Keep the server running, then open a second terminal and check it:

```bash
curl http://127.0.0.1:8000/health
```

Look for `"status":"ok"`. With this one-key setup, `capabilities.llm` is
`true`; embedding and rerank remain `false` until you configure them.

### 5. Add and retrieve your first memory

> [!NOTE]
> Business endpoints live under `/api/v2`. The older `/api/v1` prefix still
> resolves to the same handlers so existing integrations keep working, but it
> is a legacy alias that may be removed in a future major release — write new
> code against `/api/v2`.

Add a tiny conversation:

```bash
TS=$(($(date +%s)*1000))

curl -X POST http://127.0.0.1:8000/api/v2/memory/add \
  -H 'Content-Type: application/json' \
  -d "{
    \"session_id\": \"demo-001\",
    \"app_id\": \"default\",
    \"project_id\": \"default\",
    \"messages\": [
      {\"sender_id\": \"alice\", \"role\": \"user\", \"timestamp\": $TS, \"content\": \"I love climbing in Yosemite every spring.\"},
      {\"sender_id\": \"alice\", \"role\": \"user\", \"timestamp\": $((TS+10000)), \"content\": \"My favorite coffee shop is Blue Bottle in SOMA.\"}
    ]
  }"
```

Flush the memory at the end of the session:

```bash
curl -X POST http://127.0.0.1:8000/api/v2/memory