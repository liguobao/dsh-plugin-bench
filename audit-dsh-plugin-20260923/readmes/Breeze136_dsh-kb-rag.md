# kb-rag — Local literature RAG with passage-level provenance

[![npm version](https://img.shields.io/npm/v/dsh-kb-rag)](https://www.npmjs.com/package/dsh-kb-rag)
[![npm downloads](https://img.shields.io/npm/dm/dsh-kb-rag)](https://www.npmjs.com/package/dsh-kb-rag)
[![GitHub release](https://img.shields.io/github/v/release/Breeze136/dsh-kb-rag)](https://github.com/Breeze136/dsh-kb-rag/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Awesome DSH Plugin](https://beancookie.github.io/awesome-dsh-plugin/badge.svg)](https://beancookie.github.io/awesome-dsh-plugin)
[![dsh.so security](https://www.dsh.so/badges/kb-rag.svg)](https://www.dsh.so/artifact/kb-rag/)

**English** | [Chinese](./README_CN.md)

kb-rag is a local literature knowledge base for DSH (DeepSeek Harness) and any MCP-capable agent. It indexes PDFs and Zotero libraries into a single SQLite file, then answers questions with passages rather than paraphrases: every result carries its section, physical PDF page, and a clickable DOI — and every in-text citation in the retrieved passage can be traced back to the referenced work, including whether that work is already in your library.

> The npm package [`dsh-kb-rag`](https://www.npmjs.com/package/dsh-kb-rag) is published from [`npm-package/`](./npm-package) in this repository. It is not affiliated with other repositories that share the name `dsh-kb-rag`.

Indexing, embedding, and reranking all run locally. There is no API cost and no upload.

<p align="center">
  <a href="#quick-start"><strong>Quick Start</strong></a> ·
  <a href="#three-deployment-shapes"><strong>Deployment shapes</strong></a> ·
  <a href="#tool-reference"><strong>Tool reference</strong></a> ·
  <a href="#documentation"><strong>Documentation</strong></a> ·
  <a href="#measured-performance"><strong>Measured performance</strong></a>
</p>

## What the output looks like

A single `kb_rag` call returns evidence in this form. The tool renders its interface in Chinese today, so the block below is that output translated; the in-library marker it prints appears here as `[in-library]`:

```text
**Knowledge base sources Top-2**
deep · reranked with BAAI/bge-reranker-base · cache hit

1. [Chemical vapour deposition of graphene on copper substrates](https://doi.org/10.5555/12345678) — Author A; Author B · 2024 · Carbon · Results · p.4
> graphene domains nucleate on the copper surface and coalesce into a continuous film ... at a growth rate of ~2 um/min
citations from this evidence ([in-library] = already held, searchable)
  · [Ref 4] Author C, et al. Carbon 48, 1234 (2010)
    [in-library] [Nucleation and growth of graphene on transition metals](https://doi.org/10.5555/12345684) (Author C · 2010 · Carbon) (this evidence's Ref 4) · [open in Zotero](zotero://open-pdf/library/items/EXAMPLEKEY1)
  · 3 further citations collapsed (Ref 6-8); use the numbers to fetch them

**Related work**
- [A Practical Guide to Raman Spectroscopy of Graphene] — Author G et al. · 2020 (same author, related topic)
```

The full walkthrough, including the agent's answer and the follow-up that resolves a page number, is in [`docs/OUTPUT-FORMAT.md`](docs/OUTPUT-FORMAT.md). The example uses neutral placeholder data: authors, journals, and DOIs are fictional.

## Positioning

Retrieval is table stakes; the question is how far a result sits from the original evidence. kb-rag returns a **location** rather than a summary: section, physical PDF page, clickable DOI, and the citation chain behind the passage.

Three deliberate trade-offs define the project:

- **Local first, zero upload.** Embedding and reranking run on local bge models. The entire index is one `kb.sqlite` file that can be copied or archived.
- **Vertical, not general purpose.** Section-aware chunking (abstract and methods weighted), native Zotero migration, and DOI citation conventions. It is built for papers, not for arbitrary document management.
- **Stated limits.** Scanned PDFs without a text layer are skipped, figure captions are indexed as text rather than images, and cross-language retrieval is weak. These are documented under [Known limitations](#known-limitations) instead of being promised as forthcoming.

> [!IMPORTANT]
> **Scope and expectations.** Retrieval quality is bounded by the library itself: the tool cannot answer from documents it does not hold, and it cannot read a scanned page that has no text layer. Three behaviours are worth knowing in advance:
>
> - **First use is slow.** The embedding model (~95 MB) and the reranker (~1.1 GB) are downloaded on first use, and the first query waits roughly ten seconds for them to load. The resident daemon then keeps them in memory and subsequent queries are sub-second.
> - **Anchors are ingest-time data.** Page anchors and superscript citation markers are produced when a document is parsed. Libraries indexed before v1.6 keep working, but those fields stay empty until the documents are re-ingested with `force`.
> - **Bulk ingestion is asynchronous.** Above `KB_ASYNC_THRESHOLD` (default 25) pending files, `kb_ingest` forks the batch as a background job and returns a `job_id` immediately instead of blocking the session — in both deployment shapes, so a host-side call timeout cannot interrupt the work. Poll the job with `kb_status` until it reports `done`.

## Three deployment shapes

One engine (`kb_engine.py`), one data format, three entry points:

| Shape | Entry point | Tool set |
|---|---|---|
| **DSH plugin** (primary) | `plugin/` — conversational use inside a DSH session | 10 tools, adding `kb_scope` (query scope and strict mode, a DSH session concept) and `kb_status` (background job polling) |
| **MCP server** | `mcp-server/server.py` — stdio, for Claude Desktop, Cherry Studio, Kimi, DeepSeek, Cursor, and similar | 9 tools; `kb_status` exists in both shapes, so only `kb_scope` remains DSH-specific |
| **npm package** | `dsh-kb-rag` — declares `dsh.bundle`, so `dsh plugin add` installs and activates in one step | Same as the DSH plugin |

## Quick Start

### 1. Requirements

Python 3.9 or newer. Node and pnpm are checked by the installer, which installs pnpm if it is missing. DSH users operate inside a DSH profile; MCP users need only Python.

<details>
<summary><strong>Windows</strong> — non-ASCII usernames are handled from v1.6.3</summary>

Windows PowerShell 5.1 defaults its pipe encoding to ASCII, which turned non-ASCII usernames in the temp path into `?` and made the engine smoke test fail with `WinError 123`. From v1.6.3 the installer forces UTF-8 pipe encoding at the top of the script. Details: [`docs/install-winerror123-fix.md`](docs/install-winerror123-fix.md).
</details>

<details>
<summary><strong>Restricted networks</strong> — model downloads fall back to a mirror</summary>

Both the installer and the engine retry through `hf-mirror.com` when a direct download fails (`_apply_hf_mirror` patches the `huggingface_hub` constants, since setting the environment variable after import has no effect). To pin it manually: `HF_ENDPOINT=https://hf-mirror.com`.
</details>

### 2. Install

> **On Windows and would rather not touch a command line?** Use the companion
> one-click installer: download the zip from the
> [dsh-oneclick release page](https://github.com/Breeze136/dsh-oneclick/releases/latest),
> unzip it **completely**, then double-click `install.cmd`. It fills in a missing
> Node.js (no administrator rights), the official DSH CLI and a desktop shortcut, and
> asks once whether you want this knowledge base — press Enter and Python, the engine
> dependencies and the ~1.2 GB of retrieval models are installed too. Running it again
> updates. It is a third-party helper, not published by DeepSeek: it installs the
> official packages through their official channels.

**Option A — one command (recommended if you have a terminal)**

```bash
npx dsh-kb-rag-install
```

The installer runs the whole chain: Python dependencies, engine smoke test, Node/pnpm che