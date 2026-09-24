<p align="center">
 <img src="https://raw.githubusercontent.com/agentscope-ai/ReMe/main/docs/figure/reme_logo.png" alt="ReMe Logo" width="50%">
</p>

<p align="center">
  <a href="https://pypi.org/project/reme-ai/"><img src="https://img.shields.io/badge/python-3.11+-blue" alt="Python Version"></a>
  <a href="https://pypi.org/project/reme-ai/"><img src="https://img.shields.io/pypi/v/reme-ai.svg?logo=pypi" alt="PyPI Version"></a>
  <a href="https://pepy.tech/project/reme-ai/"><img src="https://img.shields.io/pypi/dm/reme-ai" alt="PyPI Downloads"></a>
  <a href="https://github.com/agentscope-ai/ReMe"><img src="https://img.shields.io/github/commit-activity/m/agentscope-ai/ReMe?style=flat-square" alt="GitHub commit activity"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-black" alt="License"></a>
  <a href="https://reme.agentscope.io"><img src="https://img.shields.io/badge/docs-ReMe-blue" alt="Documentation"></a>
  <a href="./README.md"><img src="https://img.shields.io/badge/English-Click-yellow" alt="English"></a>
  <a href="./README_ZH.md"><img src="https://img.shields.io/badge/简体中文-点击查看-orange" alt="简体中文"></a>
  <a href="https://github.com/agentscope-ai/ReMe"><img src="https://img.shields.io/github/stars/agentscope-ai/ReMe?style=social" alt="GitHub Stars"></a>
  <a href="https://deepwiki.com/agentscope-ai/ReMe"><img src="https://img.shields.io/badge/DeepWiki-Ask_Devin-navy.svg" alt="DeepWiki"></a>
</p>

<p align="center">
<a href="https://trendshift.io/repositories/20528" target="_blank"><img src="https://trendshift.io/api/badge/repositories/20528" alt="agentscope-ai%2FReMe | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
</p>

<p align="center">
  <strong>A local-first, self-evolving personal knowledge base for AI agents.</strong><br>
</p>

> Previous versions: [0.3.x](https://github.com/agentscope-ai/ReMe/tree/reme_v3) ·
> [0.2.x](https://github.com/agentscope-ai/ReMe/tree/v0.2.0.6) ·
> [MemoryScope](https://github.com/agentscope-ai/ReMe/tree/memoryscope_branch)

## ✨ Why ReMe?

🧠 ReMe turns conversations and resources into readable, editable, searchable, and interconnected Markdown memory. Agents
such as QwenPaw and DeepSeek Harness can share the same workspace to retrieve, maintain, and evolve knowledge, while
users retain control of the durable files.

- **Memory as File, File as Memory**: ReMe stores durable memory as ordinary Markdown with frontmatter and wikilinks.
  Users and agents can inspect, edit, move, sync, and back it up with familiar tools, while indexes and generated
  metadata remain rebuildable.
- **Self-evolving knowledge base**: ReMe progressively turns conversations and resources into daily notes and long-term
  knowledge, preserving sources while refining facts, preferences, procedures, and relationships over time.
- **Recall is precise and context-aware.** BM25, optional embeddings, and wikilink expansion retrieve relevant
  line-level passages and their relationships without loading the entire knowledge base into the agent context.
- **One memory workspace works across agents.** Personal assistants, coding agents, and other agent runtimes can share
  the same local workspace through native integrations, SKILL.md, CLI, HTTP, MCP, or Python APIs.

<p align="center">
  <img src="docs/figure/design-philosophy.svg" alt="ReMe Design Philosophy" width="92%">
</p>

## 📰 Latest Updates

- [2026.09] - **[ReMe Memory Tags](https://reme.agentscope.io/en/blog_20260920) published**: an introduction
  to file-native entity tags, rebuildable tag indexes, and tag-filtered memory search.
- [2026.09] - **[Hermes Agent memory provider](https://reme.agentscope.io/en/integrations/hermes) available**: choose HTTP or embedded
  mode for automatic recall before model calls and asynchronous `auto_memory` after completed turns. The integration
  supports Hermes Agent 0.21+ and includes profile-aware background work.
- [2026.09] - **[OpenClaw plugin](https://reme.agentscope.io/en/integrations/openclaw) released**: install it from
  [ClawHub](https://clawhub.ai/agentscope-ai/plugins/reme-openclaw-plugin) or
  [npm](https://www.npmjs.com/package/@agentscope-ai/reme-openclaw-plugin) to add native memory recall, automatic
  conversation capture, and scheduled consolidation to OpenClaw.
- [2026.09] - **[DeepSeek Harness plugin](https://reme.agentscope.io/en/integrations/dsh) released**: install it from
  [Awesome DSH Plugin](https://awesome-dsh-plugin.com/p/agentscope-ai/ReMe--integrations-dsh/) or
  [npm](https://www.npmjs.com/package/@agentscope-ai/reme-dsh-plugin) for long-term-memory guidance, `reme_search`,
  automatic memory, Auto Dream, and ReMe Status.
- [2026.08] - **ReMe blog published**: the [ReMe blog](https://reme.agentscope.io/en/reme-blog) introduces the
  local-first memory architecture, self-evolving workflows, hybrid search, proactive discovery, and benchmark results.
- [2026.08] - **New ReMe ecosystem plugins**: [Daily Paper](https://reme.agentscope.io/en/plugins/daily-paper)
  discovers and analyzes papers and generates file-native briefs, while
  [Auto Fin](https://reme.agentscope.io/en/plugins/auto-fin) researches the latest 24 hours of topic-related CLS news
  and builds traceable reports with local memory. Try them out.
- [2026.08] - **Plugin development support released**: use [Plugin Development](https://reme.agentscope.io/en/plugin_development) and
  [Plugin Management](https://reme.agentscope.io/en/plugin_management) to extend ReMe with Components, Steps, and Jobs. Contributions and
  new community plugins are welcome.
- [2026.08] - ReMe's [experience-driven enhancement method](https://reme.agentscope.io/en/benchmarks/toolmemory) for
  agent tool use is available on [arXiv:2608.03403](https://arxiv.org/abs/2608.03403).
- [2026.07] - Our
  paper [Remember Me, Refine Me: A Dynamic Procedural Memory Framework for Experience-Driven Agent Evolution](https://aclanthology.org/2026.findings-acl.829/)
  has been accepted to Findings of ACL 2026.

## 🚀 Quick Start

### Installation

ReMe requires Python 3.11+.

Install from pip:

```bash
pip install "reme-ai[core]"
```

Install from source:

```bash
git clone https://github.com/agentscope-ai/ReMe.git
cd ReMe
pip install -e reme_studio -e ".[core]"
cd reme_studio
npm ci
npm run build:static
cd ..
```

The static build requires Node.js 22.13 or newer and makes Studio available from the source tree.

### Environment Variables

Configure environment variables when you want LLM-powered memory evolution or embedding retrieval. Embeddings are
disabled by default, so the default setup does not start an embedding model or require an embedding API key.

```bash
cat > .env <<'EOF'
# Optional: used only after embedding components are explicitly enabled in the config.
# EMBEDDING_API_KEY=sk-xxx
# EMBEDDING_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# Required for auto_memory, auto_resource, auto_dream, and proactive refresh.
LLM_API_KEY=sk-xxx
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
EOF
```

Basic file operations, BM25 search, wikilink traversal, and reading proactive topics can run without LLM credentials.

> [!NOTE]
> To enable embedding-based semantic retrieval, uncomment `components.as_embedding` and
> `components.embedding_store` in [`reme/config/default.yaml`](reme/config/default.yaml), then change
> `components.file_store.default.embedding_store` from `""` to `default`. See the
> [memory search guide](https://reme.agentscope.io/en/memory_search) for details.

### Start the Service

```bash
reme start
```

The default service address is `127.0.0.1:2333`. If the port is occupied, specify another port:

```bash
reme start service.port=8181
# reme start workspace_dir=/tmp/reme-demo service.port=8181
```

```bash
reme version
reme health_check
reme help
curl -s http://127.0.0.1:2333/version -H 'Content-Type: application/json' -d '{}'
```

### 5-Minute Memory Demo

With the service running, wr