<div align="center">

# 🤖 dsh-local-ai
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-local-ai` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-local-ai)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-local-ai?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-local-ai?ref=badge)

**Local-model (Ollama) integration for DeepSeek Harness.**

*Discover, pull, remove, and inspect local models, route requests to them by task type or keyword with automatic fallback to the cloud, and get a one-shot status overview via `/ollama`.*

> **Official repository.** This is the only official repository of dsh-local-ai, maintained by PerryLink. Same-name repositories under other accounts are not affiliated.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-local-ai.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-local-ai/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-local-ai/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-local-ai?label=version)](https://github.com/PerryLink/dsh-local-ai/releases)
[![npm version](https://img.shields.io/npm/v/dsh-local-ai)](https://www.npmjs.com/package/dsh-local-ai)
[![npm downloads](https://img.shields.io/npm/dm/dsh-local-ai)](https://www.npmjs.com/package/dsh-local-ai)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.1` (verified 2026-09-18: dual typecheck rulers + 133 tests + self-contained/artifacts gates). The peer range admits every supported line: `>=0.1.2-rc.1 <0.2.0 \|\| >=0.1.5-alpha.1 <0.2.0 \|\| >=0.1.6-0 <0.2.0`; dev/test pins are `0.1.6-alpha.2`. |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Backend | [Ollama](https://ollama.com) (local HTTP API + CLI probe) |
| Model | Text-only route (`inputModalities: ['text']`); tool calls and tool results are supported |

## What you get

`dsh-local-ai` makes Ollama a first-class local provider in DeepSeek Harness:

- **Discovery & management** — `ollama_list` (installed models, running models, disk usage), `ollama_show` (parameter size, quantization, context length), `ollama_pull`, and `ollama_remove`.
- **Health check** — process liveness (via the `ollama` CLI) and API responsiveness (via `/api/version`), reported as two independent signals.
- **Official adapter** — the `ollama` provider route is registered through `ctx.llm.registerAdapter` (`LlmAdapter`), with configurable model mapping and temperature / max-tokens / stop translation.
- **OpenAI-compatible backends** — LM Studio, vLLM, and llama.cpp `--server` each register as their own `openai:<name>` provider through the same `LlmAdapter` seam, reusing one OpenAI `/v1/chat/completions` adapter (text-only route).
- **Local routing** — `model_route` rules route requests to a local model by task type (`purpose`), case-insensitive keyword, or `always`, with automatic fallback to the cloud when the local route fails before producing content.
- **`/ollama` command** — a one-shot status overview: models, disk usage, health, and suggestions.
- **Zero dependencies, HTTP first** — everything talks to Ollama's HTTP API (the CLI is used only for the process probe); no model files are bundled.

```text
request (loop)
   │ llm/stream waterfall
   ├─ rule matches? ──▶ route to ollama ──▶ Ollama /api/chat (NDJSON stream)
   │              └─▶ route to openai:<name> ─▶ /v1/chat/completions (SSE)
   │                        └─ fails first ─▶ fall back to cloud (next())
   └─ no match ──▶ cloud provider
tools ──▶ /api/tags · /api/ps · /api/show · /api/pull · /api/delete
health ──▶ /api/version (API) + ollama list (process)
```

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-local-ai#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-local-ai

# 2. configure routing in your profile patch (cordis.yml) and restart
dsh --profile web
```

Minimal routing configuration (the rule ships commented out in `cordis.patch.yml`):

```yaml
- insert:
    - id: dsh-local-ai
      name: dsh-local-ai
      config:
        route:
          - model: llama3.2
            keywords: ["confidential", "offline"]
```

Then verify the row mounts:

```sh
dsh --profile web --dump-config | grep -A2 'id: dsh-local-ai'
```

## Install & uninstall

- **git channel** (latest `main`): `dsh plugin --profile web add "github:PerryLink/dsh-local-ai#main"` — the `prepare` script builds with production dependencies only.
- **npm channel** (published releases): `dsh plugin --profile web add dsh-local-ai`.
- **tarball channel**: `pnpm pack` in this repo, then `dsh plugin --profile web add ./dsh-local-ai-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove dsh-local-ai` (or remove the row from the profile patch).

> If pnpm reports `ERR_PNPM_IGNORED_BUILDS` for this package, add `allowBuilds: { esbuild: true }` to your `pnpm-workspace.yaml` — the `dsh` CLI prints the exact snippet.

## Configuration

All tunables are Schemastery `Config` fields (changeable from cordis.yml). An id-targeted override replaces the whole row — restate every key you need. `cordis.patch.yml` documents each key inline.

| Key | Default | Meaning |
|---|---|---|
| `baseURL` | `http://127.0.0.1:11434` | Ollama HTTP API base URL; `/api/*` paths are appended |
| `requestTimeoutMs` | `30000` | Per-request HTTP timeout (milliseconds) |
| `graceMs` | `15000` | Subprocess terminate grace for the health-check CLI probe |
| `defaultContextWindow` | `8192` | Context capacity used when a model has no exact value |
| `maxTokens` | `4096` | Per-request output cap used when a model has no exact value |
| `temperature` | *(none)* | Default sampling temperature (0..2); omitted leaves the provider default |
| `vision` | `true` | Declare and serialize image support when the model reports vision; `false` keeps the route text-only |
| `visionCacheTtlMs` | `30000` | Milliseconds a `/api/show` capability probe stays cached (`0` disables caching; a pull or remove invalidates that model) |
| `models` | `[]` | Harness-visible → Ollama model mappings |
| `models[].name` | *(required)* | Harness-visible model name (`GenerateOptions.model`) |
| `models[].model` | `= name` | Ollama model id |
| `models[].contextWindow` | *(none)* | Per-model context capacity |
| `models[].maxTokens` | *(none)* | Per-model output cap |
| `models[].temperature` | *(none)* | Per-model sampling temperature |
| `backends` | `[]` | OpenAI-compatible local backends (LM Studio / vLLM / llama.cpp) |
| `backends[].name` | *(required)* | Backend name; registers provider id `openai:<name>` |
| `backends[].baseURL` | *(required)* | Backend base URL including `/v1`, e.g. `http://127.0.0.1:1234/v1` |
| `backends[].apiKey` | *(none)* | Optional bearer API key (most local servers leave it empty) |
| `backends[].models` | `[]` | Harness-visible → backend model mappings |
| `backends[].maxTokens` | `4096` | Per-backend output cap used when a model has no exact value |
| `backends[].temperature` | *(none)* | Per-backend sampling temperature |
| `route` | `[]` | Local-model routing rules (first match wins) |
| `route[].model` | *(required)* | Target local model name |
| `route[].provider` | `ollama` | Target provider id: `ollama` or `openai:<