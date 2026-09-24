<p align="center">
  <picture>
    <img src="./docs/images/logo.png" alt="WeKnora Logo" height="120"/>
  </picture>
</p>

<p align="center">
  <picture>
    <a href="https://trendshift.io/repositories/15289" target="_blank">
      <img src="https://trendshift.io/api/badge/repositories/15289" alt="Tencent/WeKnora | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/>
    </a>
  </picture>
</p>
<p align="center">
    <a href="https://weknora.weixin.qq.com" target="_blank">
        <img alt="Official Website" src="https://img.shields.io/badge/Official Website-WeKnora-4e6b99">
    </a>
    <a href="https://chatbot.weixin.qq.com" target="_blank">
        <img alt="WeChat Dialog Open Platform" src="https://img.shields.io/badge/WeChat Dialog Open Platform-5ac725">
    </a>
    <a href="https://chromewebstore.google.com/detail/jpemjbopikggjlmikmclgbmkhhopjdgd" target="_blank">
        <img alt="Chrome Extension" src="https://img.shields.io/badge/Chrome Extension-WeKnora-4285F4">
    </a>
    <a href="https://clawhub.ai/lyingbug/weknora" target="_blank">
        <img alt="ClawHub Skill" src="https://img.shields.io/badge/ClawHub Skill-WeKnora-ff6b35">
    </a>
    <a href="https://www.npmjs.com/package/@wxg-prc-cpg/dsh-weknora" target="_blank">
        <img alt="npm @wxg-prc-cpg/dsh-weknora" src="https://img.shields.io/npm/v/@wxg-prc-cpg/dsh-weknora?label=dsh-weknora">
    </a>
    <a href="https://github.com/Tencent/WeKnora/blob/main/LICENSE">
        <img src="https://img.shields.io/badge/License-MIT-ffffff?labelColor=d4eaf7&color=2e6cc4" alt="License">
    </a>
    <a href="./CHANGELOG.md">
        <img alt="Version" src="https://img.shields.io/badge/version-0.8.0-2e6cc4?labelColor=d4eaf7">
    </a>
</p>

<p align="center">
| <b>English</b> | <a href="./README_CN.md"><b>简体中文</b></a> | <a href="./README_JA.md"><b>日本語</b></a> | <a href="./README_KO.md"><b>한국어</b></a> |
</p>

<p align="center">
  <h4 align="center">

  [Overview](#-overview) • [Architecture](#-architecture) • [Key Features](#-key-features) • [Getting Started](#-getting-started) • [API Reference](#-api-reference) • [Developer Guide](#-developer-guide)
  
  </h4>
</p>

# 💡 WeKnora — Turn Documents into Living Knowledge with RAG, Agents and Auto-Wiki

## 📌 Overview

[**WeKnora**](https://weknora.weixin.qq.com) is an open-source, LLM-powered knowledge framework built for enterprise-grade document understanding, semantic retrieval, and autonomous reasoning.

https://github.com/user-attachments/assets/19b28ce2-a62f-4f54-b289-c983576259bc

*2:25 · 1080p · English narration & captions.*

It is organized around three core capabilities: **RAG-based Quick Q&A** for everyday lookups, a **ReAct Agent** that autonomously orchestrates retrieval, MCP tools, a **tenant skill catalog**, session-persistent **Docker / E2B / Cube sandboxes** and web search to handle complex multi-step tasks, and a brand-new **Wiki Mode** in which agents distill raw documents into a self-maintaining, interlinked markdown knowledge base with an interactive knowledge graph, complete with manual editing, revision history and one-click rollback. **Cross-session long-term memory** remembers who you are and what you keep asking about. Knowledge curation is equally hands-on: a **tree-structured folder view** preserves the directory layout of uploads, and **chunk editing with revision history** lets retrieval chunks be edited, diffed and reverted like documents. Combined with multi-source ingestion (Feishu wiki / Feishu Drive / GitLab / Tencent IMA / Notion / Yuque / DingTalk Docs / RSS, and growing), **website embed widgets** for publishing agents to external sites, **scoped API keys with a principal model** for programmatic integrations, **multi-instance storage backends** per workspace for flexible data placement, 20+ LLM provider integrations (including LiteLLM), full Langfuse observability plus a **runtime task-queue dashboard with worker-pool governance**, **enterprise-ready multi-workspace RBAC** (4-tier role matrix + per-resource ownership + per-workspace audit log), and a fully self-hostable modular architecture, WeKnora turns scattered documents into a queryable, reasoning-capable, continuously evolving knowledge asset.

The framework supports auto-syncing knowledge from Feishu, GitLab, Tencent IMA, Notion, and Yuque (more data sources coming soon), handles 10+ document formats including PDF, Word, images, Excel and XMind, and can serve Q&A directly through IM channels like WeCom, Feishu, Slack, and Telegram. It is compatible with major LLM providers including OpenAI, DeepSeek, Qwen (Alibaba Cloud), Zhipu, Hunyuan, Gemini, MiniMax, NVIDIA, LiteLLM, and Ollama. Office files can be parsed in-process with **anydoc**. Its fully modular design allows swapping LLMs, vector databases, and storage backends, with support for local and private cloud deployment ensuring complete data sovereignty. WeKnora also integrates with **Langfuse** for comprehensive observability into agent reasoning, token usage, and pipeline tracing.


## ✨ Latest Updates

- **v0.8.0** — **Skill sandbox runtime** (session-persistent Docker / E2B / Cube backends with per-tenant network policy; Local host-process backend removed; Docker opt-in); **tenant skill catalog** (install from ClawHub / SkillHub / git / zip, per-sandbox snapshots, live progress, file browse/edit, personal and workspace env vars); **cross-session long-term memory** (profile / preference / fact / task / interest, auto-extract with confirm, `search_memory`); **in-process anydoc office parser**; official **DeepSeek Harness plugin** `@wxg-prc-cpg/dsh-weknora`; GitLab and Tencent IMA data sources; LiteLLM; Exa and Metaso web search; XMind parsing; chat artifacts, question outline and timestamps; context compaction and provider prompt-cache markers. Plus OIDC JWKS verification, optional complex passwords, document auto-tagging, and broad sandbox/security hardening. See [`CHANGELOG.md`](./CHANGELOG.md).
- **v0.7.2** — Launched the **official product documentation site** (VitePress; six sections, ~50 pages covering ~360 API endpoints and ~150 environment variables, with standalone Docker/Nginx deployment, quickstart sample data and a local MCP demo); **knowledge base folder tree** (upload paths stored as first-class data, browse/rename/re-file documents like a file manager); **chunk editing with revision history** (edit retrieval chunks in the UI, per-version diff and rollback, automatic reindexing, plus custom document metadata); **Wiki page revision history** (snapshots + line-level diff + one-click rollback + in-browser manual editing); **directly loadable file URLs** via `resource_urls=public` / `RESOURCE_URL_MODE` (third-party apps render images and files without a second authenticated proxy call); **Feishu Drive data source** and docx sync through the blocks API; batch document tagging; **MCP Server 1.1.x** (migrated to the mcp 2.x high-level API, official PyPI package `tencent-weknora-mcp`, new `create_knowledge_from_text` and `list_shared_knowledge_bases` for 29 tools total); AWS S3 default credential chain (IAM Role / IRSA); local HTML upload parsing; QQBot markdown replies; new PR CI checks for app / frontend / docreader / mcp-server. Plus large-scale router and `modelcontext` refactors, rerank and chunking quality work, and broad stability fixes. See [`CHANGELOG.md`](./CHANGELOG.md).
- **v0.7.1** — New **Yunzhijia (云之家) IM integration** (WebSocket + image messages + markdown replies); **Volcengine rerank** provider (with request batching) and **Zhipu AI web search** provider; **platform-scoped API keys** for control-plane automation (tenant management, system settings, runtime queues, audit logs); **per-KB activity audit trail**; FAQ management enhancements (filtering, tagging, export, import tracking); **Langfuse OTLP/OTel tracing** migration with W3C traceparent propagation; chat header actions with one-click **Markdown export** and wiki tool results in the references