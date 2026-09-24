<p align="center">
  <img src="assets/banner.png" alt="mnemosyne OS" width="100%">
</p>

# mnemosyne OS

<p align="center">
  <a href="https://pypi.org/project/mnemosyne-os/">PyPI</a> ·
  <a href="https://github.com/FrankHu-HK/mnemosyne">GitHub</a> ·
  <a href="README_CN.md">中文</a>
</p>

<p align="center">
  <a href="https://pypi.org/project/mnemosyne-os/"><img src="https://img.shields.io/badge/PyPI-mnemosyne--os-blue?style=for-the-badge" alt="PyPI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+"></a>
  <a href="#-mcp-server"><img src="https://img.shields.io/badge/MCP-31%20Tools-00ADD8?style=for-the-badge" alt="Model Context Protocol"></a>
  <a href="#quick-start"><img src="https://img.shields.io/badge/dependencies-0-brightgreen?style=for-the-badge" alt="Zero dependencies"></a>
  <a href="https://pepy.tech/projects/mnemosyne-os"><img src="https://img.shields.io/pepy/dt/mnemosyne-os?style=for-the-badge" alt="Downloads"></a>
  <a href="https://x.com/mnemosyne_oos"><img src="https://img.shields.io/badge/X-@mnemosyne_oos-black?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
</p>

<p align="center">
  <a href="README_TW.md"><img src="https://img.shields.io/badge/Lang-繁體中文-red?style=for-the-badge" alt="繁體中文"></a>
  <a href="README.es.md"><img src="https://img.shields.io/badge/Lang-Español-orange?style=for-the-badge" alt="Español"></a>
  <a href="README.ru.md"><img src="https://img.shields.io/badge/Lang-Русский-blue?style=for-the-badge" alt="Русский"></a>
  <a href="README.de.md"><img src="https://img.shields.io/badge/Lang-Deutsch-lightgrey?style=for-the-badge" alt="Deutsch"></a>
  <a href="README.th.md"><img src="https://img.shields.io/badge/Lang-ไทย-blue?style=for-the-badge" alt="ไทย"></a>
  <a href="README.ko.md"><img src="https://img.shields.io/badge/Lang-한국어-green?style=for-the-badge" alt="한국어"></a>
  <a href="README.ja.md"><img src="https://img.shields.io/badge/Lang-日本語-red?style=for-the-badge" alt="日本語"></a>
</p>

**Mnemosyne OS 8.0.0** — a zero-dependency, local-first AI memory system. Graph
memory, multimodal ingestion, reranking, temporal reasoning, a hash-chained audit
ledger, lossless compression, and 31 MCP tools.

> The only AI memory engine whose **core genuinely carries zero third-party
> dependencies** — no vector database, no LLM runtime, no cloud account.
> `install_requires` is an empty list. It runs on a laptop, a server, or
> serverless infrastructure alike.

Use it as a **Python library**, a **CLI**, an **HTTP API**, or an **MCP server**.

---

## 🚀 Quick start

### Install

```bash
pip install mnemosyne-os          # core: zero third-party dependencies
```

### Remember and recall without configuring anything

```python
from mnemosyne import Memory

m = Memory()                       # built-in embedder + rule-based extractor
m.add("I prefer dark mode and use vim keybindings. My name is Alice.",
      user_id="alice")

for hit in m.search("what does alice prefer", filters={"user_id": "alice"})["results"]:
    print(f"{hit['score']:.3f}  {hit['memory']}")
```

Offline, no API key, no model download, no database to install — which is what
makes the next section possible.

### Attach real models only once recall needs to be stronger

```python
from mnemosyne import Memory

m = Memory.from_config({
    "llm":          {"provider": "openai", "config": {"model": "gpt-4o-mini"}},
    "embedder":     {"provider": "openai", "config": {"model": "text-embedding-3-small"}},
    "vector_store": {"provider": "qdrant", "config": {"url": "http://localhost:6333"}},
    "reranker":     {"provider": "cohere", "config": {"api_key": "..."}},
    "graph_store":  {"provider": "builtin"},
})
```

Every component is independently optional. When a provider cannot be built it
falls back to the built-in equivalent and **says so** — nothing degrades silently:

```python
m.describe()["degraded"]
# {'llm': {'requested': 'openai', 'used': 'rules', 'reason': 'no API key configured',
#          'hint': 'Set MNEMOSYNE_LLM_OPENAI_API_KEY ...'}}
```

### Or drive it from the command line

```bash
mnemosyne init
mnemosyne add "I prefer dark mode and vim keybindings" --user-id alice
mnemosyne search "what does alice prefer" --user-id alice
mnemosyne list  --user-id alice
mnemosyne event --limit 10
mnemosyne --agent search "preferences" --user-id alice   # JSON envelope for tool loops
```

### Or expose it over MCP

```json
{
  "mcpServers": {
    "mnemosyne": {
      "command": "python",
      "args": ["-m", "mnemosyne.webui.mcp_server",
               "--brain-dir", "./mem", "--namespace", "default"],
      "env": { "MNEMOSYNE_MCP_TOKEN": "<random 32+ chars>" }
    }
  }
}
```

### Or serve it over HTTP

```bash
mnemosyne-web --port 9090          # console and REST share one port
curl -X POST http://127.0.0.1:8788/v3/memories/add/ \
  -H "Authorization: Bearer $MNEMOSYNE_API_KEY" -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"I moved to Berlin in 2023."}],"user_id":"alice"}'
```

---

## 📊 Benchmarks

Measured with the harness shipped in this repository. Reproduce with
`scripts/verify_recall_quality.py` and `scripts/verify_precision_recall.py`.

| Benchmark | Score | What it measures |
| --- | --- | --- |
| LongMemEval | **96.2** | long-horizon conversational recall |
| LoCoMo | **94.8** | multi-session dialogue memory |
| BEAM (1M) | **68.5** | recall under a 1M-token context budget |
| BEAM (10M) | **53.9** | recall under a 10M-token context budget |

Scores are out of 100.

---

## 🧩 Capabilities

<table>
<tr><td><b>Memory API</b></td><td><code>Memory</code> / <code>AsyncMemory</code> / <code>MemoryClient</code> with a complete method surface: <code>add</code> <code>get</code> <code>get_all</code> <code>search</code> <code>update</code> <code>delete</code> <code>delete_all</code> <code>history</code> <code>reset</code> <code>close</code> <code>from_config</code>.</td></tr>
<tr><td><b>Four-dimensional scoping</b></td><td><code>user_id</code> / <code>agent_id</code> / <code>run_id</code> / <code>app_id</code> — enforced by <b>physical isolation</b>: one SQLite file per scope, rather than shared rows with a filter applied.</td></tr>
<tr><td><b>Filter language</b></td><td><code>eq</code> <code>ne</code> <code>gt</code> <code>gte</code> <code>lt</code> <code>lte</code> <code>in</code> <code>nin</code> <code>contains</code> <code>icontains</code> <code>wildcard</code>, with arbitrarily nested <code>AND</code>/<code>OR</code>/<code>NOT</code>.</td></tr>
<tr><td><b>Single-pass ADD-only extraction</b></td><td>One model call per write; memories accumulate and are never overwritten. Because nothing is rewritten, a bad extraction only introduces noise — it can never destroy a real fact.</td></tr>
<tr><td><b>Graph memory, always on</b></td><td>Entity linking and multi-hop traversal live in the same SQLite file. No external graph database required.</td></tr>
<tr><td><b>Multimodal ingestion</b></td><td>Accepts the OpenAI, Anthropic and Gemini image content shapes (plus audio). With a vision model configured it stores a description; without one it stores the reference — nothing is dropped.</td></tr>
<tr><td><b>Multi-signal retrieval</b></td><td>Semantic + BM25 keyword + entity graph + temporal + tag, fused with calibrated relevance floors and a lexical fallback.</td></tr>
<tr><td><b>Temporal reasoning</b></td><td>Observation dates, relative-time resolution, expiry semantics, and per-entity version chains.</td></tr>
<tr><td><b>Tiered memory</b></td><td>Hot / warm / cold tiers with forgetfulness economics: low-value memories are demoted and compressed, never silently deleted.</td></tr>
<tr><td><b>Lossless compression (AIC)</b></td><td>Compresses a memory into <i>pointer + structured facts + content ato