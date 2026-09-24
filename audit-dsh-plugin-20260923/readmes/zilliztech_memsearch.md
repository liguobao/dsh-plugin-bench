<h1 align="center">
  <img src="assets/logo-icon.jpg" alt="" width="100" valign="middle">
  &nbsp;
  memsearch
</h1>

<p align="center">
  <strong>Cross-platform semantic memory for AI coding agents.</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/memsearch/"><img src="https://img.shields.io/pypi/v/memsearch?style=flat-square&color=blue" alt="PyPI"></a>
  <a href="https://zilliztech.github.io/memsearch/platforms/claude-code/"><img src="https://img.shields.io/badge/Claude_Code-plugin-c97539?style=flat-square&logo=claude&logoColor=white" alt="Claude Code"></a>
  <a href="https://zilliztech.github.io/memsearch/platforms/codex/"><img src="https://img.shields.io/badge/Codex-plugin-ff6b35?style=flat-square" alt="Codex"></a>
  <a href="https://zilliztech.github.io/memsearch/platforms/dsh/"><img src="https://img.shields.io/badge/DeepSeek_Harness-plugin-4d6bfe?style=flat-square" alt="DeepSeek Harness"></a>
  <a href="https://zilliztech.github.io/memsearch/platforms/openclaw/"><img src="https://img.shields.io/badge/OpenClaw-plugin-4a9eff?style=flat-square" alt="OpenClaw"></a>
  <a href="https://zilliztech.github.io/memsearch/platforms/opencode/"><img src="https://img.shields.io/badge/OpenCode-plugin-22c55e?style=flat-square" alt="OpenCode"></a>
  <a href="https://pypi.org/project/memsearch/"><img src="https://img.shields.io/badge/python-%3E%3D3.10-blue?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/zilliztech/memsearch/blob/main/LICENSE"><img src="https://img.shields.io/github/license/zilliztech/memsearch?style=flat-square" alt="License"></a>
  <a href="https://github.com/zilliztech/memsearch/actions/workflows/test.yml"><img src="https://img.shields.io/github/actions/workflow/status/zilliztech/memsearch/test.yml?branch=main&style=flat-square" alt="Tests"></a>
  <a href="https://zilliztech.github.io/memsearch/"><img src="https://img.shields.io/badge/docs-memsearch-blue?style=flat-square" alt="Docs"></a>
  <a href="https://github.com/zilliztech/memsearch/stargazers"><img src="https://img.shields.io/github/stars/zilliztech/memsearch?style=flat-square" alt="Stars"></a>
  <a href="https://discord.com/invite/FG6hMJStWu"><img src="https://img.shields.io/badge/Discord-chat-7289da?style=flat-square&logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://x.com/zilliz_universe"><img src="https://img.shields.io/badge/follow-%40zilliz__universe-000000?style=flat-square&logo=x&logoColor=white" alt="X (Twitter)"></a>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/427b7152-bc16-408c-a8b0-59a2b05fd1e0" alt="memsearch demo" width="800">
</p>

## 📰 What's New

- **Optional Jev reranking** — rerank memory search results with Jev through the TypeSafe API, with no local model download. See [configuration](docs/home/configuration.md#optional-remote-reranking) and the [Chinese/English evaluation](evaluation/reranking-evaluation.md).

- **DeepSeek Harness support** — MemSearch now brings automatic capture, pre-step memory injection, native skill-based recall, background maintenance, and a read-only memory browser to [DeepSeek Harness (DSH)](https://zilliztech.github.io/memsearch/platforms/dsh/).
- **Skills from memory** — MemSearch now distills the workflows you repeat into reusable, installable agent skills (a third "procedural memory" layer) and keeps them up to date in the background. See [Skills from Memory](#skills-from-memory).
- **Advanced memory maintenance** — optional background tasks keep durable `PROJECT.md` and `USER.md` notes current across sessions. See [Advanced Memory Maintenance](#advanced-memory-maintenance).

---

### Why memsearch?

- 🌐 **All Platforms, One Memory** — memories flow across [Claude Code](plugins/claude-code/README.md), [Codex](plugins/codex/README.md), [DeepSeek Harness](plugins/dsh/README.md), [OpenClaw](plugins/openclaw/README.md), and [OpenCode](plugins/opencode/README.md). A conversation in one agent becomes searchable context in all others — no extra setup
- 👥 **For Agent Users**, install a plugin and get persistent memory with zero effort; **for Agent Developers**, use the full [CLI](https://zilliztech.github.io/memsearch/cli/) and [Python API](https://zilliztech.github.io/memsearch/python-api/) to build memory and harness engineering into your own agents
- 📄 **Markdown is the source of truth** — inspired by [OpenClaw](https://github.com/openclaw/openclaw). Your memories are just `.md` files — human-readable, editable, version-controllable. Milvus is a "shadow index": a derived, rebuildable cache
- 🔍 **Progressive retrieval, hybrid search, smart dedup, live sync** — 3-layer recall (search → expand → transcript); dense vector + BM25 sparse + RRF reranking; SHA-256 content hashing skips unchanged content; file watcher auto-indexes in real time

---

## 🧑‍💻 For Agent Users

Pick your platform, install the plugin, and you're done. Each plugin captures conversations automatically and provides semantic recall with zero configuration.

<details open>
<summary><h3>For Claude Code Users</h3></summary>

```bash
# Install
/plugin marketplace add zilliztech/memsearch
/plugin install memsearch
# Restart Claude Code to activate the plugin
```

After restarting, just chat with Claude Code as usual. The plugin captures every conversation turn automatically.

**Verify it's working** — after a few conversations, check your memory files:

```bash
ls .memsearch/memory/          # you should see daily .md files
cat .memsearch/memory/$(date +%Y-%m-%d).md
```

**Recall memories** — two ways to trigger:

```
/memory-recall what did we discuss about Redis?
```
Or just ask naturally — Claude auto-invokes the skill when it senses the question needs history:
```
We discussed Redis caching before, what was the TTL we chose?
```

> 📖 [Claude Code Plugin docs](https://zilliztech.github.io/memsearch/platforms/claude-code/) · [Troubleshooting](https://zilliztech.github.io/memsearch/platforms/claude-code/troubleshooting/)

</details>

<details open>
<summary><h3>For Codex Users</h3></summary>

```bash
# Install
git clone --depth 1 https://github.com/zilliztech/memsearch.git
bash memsearch/plugins/codex/scripts/install.sh
codex --yolo  # needed for ONNX model network access
```

After installing, chat as usual. Hooks capture and summarize each turn.

**Verify it's working:**

```bash
ls .memsearch/memory/
```

**Recall memories** — use the skill:

```
$memory-recall what did we discuss about deployment?
```

> 📖 [Codex Plugin docs](https://zilliztech.github.io/memsearch/platforms/codex/)

</details>

<details open>
<summary><h3>For DeepSeek Harness Users</h3></summary>

```bash
# Install the published plugin into your DSH profile
uv tool install "memsearch[onnx]"
dsh plugin --profile web add @zilliz/memsearch-dsh
# Restart that DSH profile, or start a new session
```

After installing, use DSH normally. Completed turns are captured automatically, and relevant memories are injected before the first model step only when they are useful.

**Verify it's working:**

```bash
ls .memsearch/memory/
```

**Recall memories** — ask naturally or tell DSH to use the registered `memory-recall` skill:

```
Use memory-recall to find what we decided about the deployment architecture.
```

The web profile also adds a compact MemSearch dock where you can review skill candidates and browse supported files under `.memsearch/` without editing them.

> 📖 [DeepSeek Harness Plugin docs](https://zilliztech.github.io/memsearch/platforms/dsh/)

</details>

<details>
<summary><h3>For OpenClaw Users</h3></summary>

```bash
# Install from ClawHub
openclaw plugins install --force clawhub:memsearch
openclaw config set plugins.entries.memsearch.hooks.allowConversationAccess true
openclaw config set plugins.entries.memsearch.hooks.allowPromptInjection true
openclaw gateway restart
```

After installing, chat in TUI as usual. The plugin captures each turn automatically.

**Verify it's working** — m