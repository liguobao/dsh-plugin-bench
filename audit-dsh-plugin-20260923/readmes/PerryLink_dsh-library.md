<div align="center">

# 📚 dsh-library
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-library` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-library)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-library?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-library?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-library/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-library)

**Local document knowledge base for DeepSeek Harness.**

*Import, retrieve, verify — hybrid search with citations your agent can check.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-library.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-library/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-library/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-library?label=version)](https://github.com/PerryLink/dsh-library/releases)
[![npm version](https://img.shields.io/npm/v/dsh-library)](https://www.npmjs.com/package/dsh-library)
[![npm downloads](https://img.shields.io/npm/dm/dsh-library)](https://www.npmjs.com/package/dsh-library)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (verified 2026-09-18: dual typecheck rulers + 89 tests + self-contained/artifacts gates; peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.1.5-alpha.1 <0.2.0 \|\| >=0.1.6-0 <0.2.0 \|\| >=0.1.7-0 <0.2.0`). Home of the family's only exercised alpha.2 host smoke (2026-09-11). |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Storage | Any storage-domain backend (JSON or SQLite); the index lives in the host's storage domain |
| Models | None required — the built-in embedder is deterministic hashing (zero downloads) |

## What you get

`dsh-library` turns local md/txt documents into a queryable knowledge base with a quality pipeline your agent can trust:

- **`library_add` / `library_remove` / `library_list`** — import a document by path (chunked and embedded), remove one with **purge verification** (signatures of the removed content are probed against the remaining index and any residue is reported), and list document metadata.
- **`library_search`** — hybrid semantic + keyword ranking, maximal-marginal-relevance diversity re-rank, relevance filtering, and **lost-in-the-middle avoidance** (strongest chunks pinned to head and tail). With `inject: true` the result page is injected into the calling agent; every hit carries a `[n]` source marker and the injection is reconstructable from the `library/inject` session event (host-gated; see Permissions & data).
- **`library_cite_check`** — verify the `[n]` citations in an answer against the search result page with a fuzzy token match AND a semantic similarity check.
- **`library_diagnose`** — chunk-size histogram, near-duplicate chunk pairs, a self-retrieval probe, and the middle-penalty signal.
- **`/library`** — one-line index summaries per library.

```text
document ── library_add ─▶ chunk (sliding window) ─▶ embed (hash / external cmd)
                                  │
                        storage domain (documents / chunks / purges)
                                  │
query ── library_search ─▶ hybrid score ─▶ MMR re-rank ─▶ relevance filter
                                  │                    ─▶ lost-in-middle order
                                  ▼
                    result page with [n] markers ── inject: true ─▶ agent + library/inject event (host-gated)
```

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-library#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-library

# 2. restart and verify the row
dsh --profile web --dump-config | grep -A2 'id: dsh-library'
```

Then ask the agent to import and use a document:

```
> Add ./docs/spec.md to library docs, then answer: what does the spec say about retries? Cite [n] markers.
```

## Install & uninstall

- **git channel** (latest `main`): `dsh plugin --profile web add "github:PerryLink/dsh-library#main"` — the `prepare` script builds with production dependencies only.
- **npm channel** (published releases): `dsh plugin --profile web add dsh-library`.
- **tarball channel**: `pnpm pack` in this repo, then `dsh plugin --profile web add ./dsh-library-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove dsh-library` (or remove the row from the profile patch).

> If pnpm reports `ERR_PNPM_IGNORED_BUILDS` for this package (esbuild's harmless platform-binary validation), add `allowBuilds: { esbuild: true }` to your `pnpm-workspace.yaml` — the `dsh` CLI prints the exact snippet.

## Configuration

All tunables are Schemastery `Config` fields (changeable from cordis.yml). An id-targeted override replaces the whole row — restate every key you need. `cordis.patch.yml` documents each key inline.

| Key | Default | Meaning |
|---|---|---|
| `chunkSize` | `900` | Sliding-window chunk size in characters (≤ 4000) |
| `chunkOverlap` | `120` | Overlap between consecutive windows; must be smaller than `chunkSize` |
| `maxFileBytes` | `5242880` | Files larger than this are rejected on `library_add` |
| `embedding.dims` | `256` | Hash-embedding dimensionality (≥ 8) |
| `embedding.provider` | `hash` | Embedder backend: `hash` (built-in, zero downloads), `command` (external subprocess, requires `embedding.command`), or `ollama` (local Ollama, probed and degraded to `hash` when unreachable) |
| `embedding.command` | `''` | Optional external embedder command (space-separated argv, no shell) over `ctx.subprocess`; setting it selects the `command` provider |
| `embedding.ollamaUrl` / `ollamaModel` | `http://127.0.0.1:11434` / `nomic-embed-text` | Local Ollama endpoint + model for the `ollama` provider (zero cloud) |
| `embedding.timeoutMs` / `graceMs` / `maxOutputBytes` / `maxBatchItems` | `30000` / `1000` / `1048576` / `64` | Embedder subprocess budget |
| `search.topK` | `8` | Results returned after the full pipeline |
| `search.hybridWeight` | `0.6` | 0 = keyword-only, 1 = semantic-only |
| `search.minRelevance` | `0.15` | Chunks below this relevance threshold are filtered out |
| `search.diversityLambda` | `0.5` | MMR trade-off: 1 = pure relevance, 0 = pure diversity |
| `search.lostMiddleHead` / `lostMiddleTail` | `1` / `1` | Strongest chunks pinned to head / tail |
| `search.maxResultChars` | `16000` | Character budget of the model-facing result page |
| `injection.enabled` / `maxChars` | `true` / `12000` | `library_search` inject behavior and budget |
| `citation.windowChars` / `minScore` / `minSemantic` | `150` / `40` / `0.1` | `library_cite_check` thresholds |
| `purge.signatureLength` / `maxProbes` | `4` / `24` | Purge verification signatures and probe budget |
| `diagnose.maxDuplicatePairs` / `sampleCap` / `positionBins` | `24` / `200` / `5` | `library_diagnose` budget caps |

## Tools & surfaces

| Tool | Notes |
|---|---|
| `library_add` | `{ path, library, name? }` → document id; file read through the harness filesystem service |
| `library_remove` | `{ library, documentId 