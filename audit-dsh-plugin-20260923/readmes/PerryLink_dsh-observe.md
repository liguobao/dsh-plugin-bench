<div align="center">

# 📊 dsh-observe
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-observe` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-observe)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-observe?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-observe?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-observe/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-observe)

**OpenTelemetry and Langfuse observability exporter for DeepSeek Harness.**

*Turn session events into OTLP traces and Langfuse observations — sanitized, buffered, off by default.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-observe.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-observe/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-observe/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-observe?label=version)](https://github.com/PerryLink/dsh-observe/releases)
[![npm version](https://img.shields.io/npm/v/dsh-observe)](https://www.npmjs.com/package/dsh-observe)
[![npm downloads](https://img.shields.io/npm/dm/dsh-observe)](https://www.npmjs.com/package/dsh-observe)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (adapted 2026-09-22): session format V4 represents a tool result as a first-class `role: 'tool'` message carrying top-level `toolCallId` + `content` + optional `isError` — the V3 `tool-result` content block is gone from the host's `ContentBlockMap`, and this plugin reads only the V4 shape (a pre-upgrade V3 log still projects through a read-only compatibility path). Session format V3's other traits carry over: the assistant stream is embedded in `assistant/message` / `assistant/attempt`, and the system prompt is surface node 0 (`system/message`); the plugin consumes only the live event stream and never reads session log files. The peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.1.5-alpha.1 <0.2.0 \|\| >=0.1.6-0 <0.2.0 \|\| >=0.1.7-0 <0.2.0` keeps every published line installable (full local gate chain; the compat workflow covers the profile install smoke). |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Backends | OpenTelemetry OTLP/HTTP (traces + metrics, JSON encoding) and Langfuse (LLM observability) — either or both |
| Model | Model-agnostic: it exports the session/event stream; no model calls are made |

## What you get

`dsh-observe` turns the harness's `session/event` stream into standard observability protocols:

- **Spans** — turn, step, tool-call (duration, status, retry derivation), and LLM generation spans, linked into per-turn traces with deterministic ids.
- **Metrics** — per-provider/model token counters, USD cost counters (configurable pricing table), and the optional context-pressure gauge from `ctx.tokenMeter`.
- **Sanitized capture** — prompt and completion bodies are redacted (structural key names + built-in secret patterns + your patterns) and truncated before anything is queued or sent.
- **Reliability** — async batching (size- and timer-triggered), a bounded durable offline buffer (storage-domain) with oldest-first eviction, and deterministic exponential-backoff retries; undeliverable batches survive restarts.
- **Runtime kill switch** — the optional Typert remote (`observe/status`, `observe/setEnabled`) lets a settings page stop and resume exporting without unmounting.
- **Off by default** — `enabled: true` plus at least one backend is an explicit opt-in; nothing is captured or exported otherwise.

```text
session/event stream
   │ collector (turn/step/tool/llm spans, metrics)
   │ sanitize (keys, secrets, budgets)
   ├──▶ pipeline "otlp"  ── queue ── flush ──▶ OTLP /v1/traces + /v1/metrics
   │         └─ retry/backoff ─┐
   ├──▶ pipeline "langfuse" ── queue ── flush ──▶ Langfuse ingestion
   │         └─ retry/backoff ─┤
   └────────── durable spool (offline buffer, bounded) ◀┘
```

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-observe#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-observe

# 2. configure a backend in your profile patch (cordis.yml) and restart
dsh --profile web
```

Minimal OTLP configuration (the row ships commented out in `cordis.patch.yml`):

```yaml
- insert:
    - id: dsh-observe
      name: dsh-observe
      config:
        enabled: true
        otlp:
          endpoint: http://localhost:4318
```

Then verify the row mounts:

```sh
dsh --profile web --dump-config | grep -A2 'id: dsh-observe'
```

## Install & uninstall

- **git channel** (latest `main`): `dsh plugin --profile web add "github:PerryLink/dsh-observe#main"` — the `prepare` script builds with production dependencies only.
- **npm channel** (published releases): `dsh plugin --profile web add dsh-observe`.
- **tarball channel**: `pnpm pack` in this repo, then `dsh plugin --profile web add ./dsh-observe-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove dsh-observe` (or remove the row from the profile patch).

> If pnpm reports `ERR_PNPM_IGNORED_BUILDS` for this package (esbuild's harmless platform-binary validation), add `allowBuilds: { esbuild: true }` to your `pnpm-workspace.yaml` — the `dsh` CLI prints the exact snippet.

## Configuration

All tunables are Schemastery `Config` fields (changeable from cordis.yml). An id-targeted override replaces the whole row — restate every key you need. `cordis.patch.yml` documents each key inline.

| Key | Default | Meaning |
|---|---|---|
| `enabled` | `false` | Master switch; `true` plus at least one backend is the explicit opt-in |
| `otlp` | `null` | OTLP backend config, or `null` to disable it |
| `otlp.endpoint` | *(required)* | OTLP base URL; `/v1/traces` and `/v1/metrics` are appended |
| `otlp.serviceName` | `deepseek-harness` | `service.name` resource attribute |
| `otlp.serviceVersion` | *(none)* | `service.version` resource attribute |
| `otlp.headers` | `{}` | Extra headers merged into every export request |
| `otlp.timeoutMs` | `10000` | Per-request timeout |
| `langfuse` | `null` | Langfuse backend config, or `null` to disable it |
| `langfuse.baseUrl` | `https://cloud.langfuse.com` | Langfuse base URL |
| `langfuse.publicKey` | *(required)* | Project public key |
| `langfuse.secretKey` | *(required)* | Project secret key |
| `langfuse.release` | *(none)* | Release tag stamped onto traces |
| `langfuse.traceName` | `session {session} turn {turn}` | Trace-name template; `{session}`/`{turn}` interpolate per trace |
| `langfuse.tags` | `[]` | Static tags stamped onto every trace |
| `langfuse.timeoutMs` | `10000` | Per-request timeout |
| `capture.turns` | `true` | Turn lifecycle spans |
| `capture.steps` | `true` | Step lifecycle spans |
| `capture.tools` | `true` | Tool-call spans with sanitized arguments/results |
| `capture.llm` | `true` | LLM generation spans |
| `llm.prompt` | `true` | Capture the sanitized request prompt (`false` = sizes only) |
| `llm.completion` | `true` | Capture the sanitized completion (`false` = sizes only) |
| `metadata.se