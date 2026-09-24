<p align="center">
  <img src="site/public/mem9-wordmark-square.svg" alt="mem9" width="180" />
</p>
<p align="center">
  <strong>Persistent Memory for AI Agents.</strong><br/>
  Your agents forget everything between sessions. mem9 fixes that with persistent memory across sessions and machines, shared memory for multi-agent workflows, and hybrid recall with a visual dashboard.
</p>

<p align="center">
  For OpenClaw and ClawHub installs, start here: <a href="https://mem9.ai/openclaw-memory">mem9.ai/openclaw-memory</a>
  <br/>
  Hermes Agent, Claude Code, OpenCode, Codex, DeepSeek Harness, and Dify guides are below.
</p>

<p align="center">
  <a href="https://tidbcloud.com"><img src="https://img.shields.io/badge/Powered%20by-TiDB%20Cloud%20Starter-E60C0C?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIj48cGF0aCBkPSJNMTEuOTk4NCAxLjk5OTAyTDMuNzE4NzUgNy40OTkwMkwzLjcxODc1IDE3TDExLjk5NjQgMjIuNUwyMC4yODE0IDE3VjcuNDk5MDJMMTEuOTk4NCAxLjk5OTAyWiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=" alt="Powered by TiDB Cloud Starter"></a>
  <a href="https://goreportcard.com/report/github.com/mem9-ai/mem9/server"><img src="https://goreportcard.com/badge/github.com/mem9-ai/mem9/server" alt="Go Report Card"></a>
  <a href="https://github.com/mem9-ai/mem9/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License"></a>
  <a href="https://github.com/mem9-ai/mem9"><img src="https://img.shields.io/github/stars/mem9-ai/mem9?style=social" alt="Stars"></a>
</p>

---

## Quick Start

1. Choose your mem9 endpoint.

   - Hosted API: `https://api.mem9.ai`
   - Self-hosted: apply the matching control-plane schema, then start `mnemo-server`:

     ```bash
     cd server
     MNEMO_DSN="user:pass@tcp(host:4000)/mnemos?parseTime=true" go run ./cmd/mnemo-server
     ```

     See [Self-Hosting](#self-hosting) for backend-specific setup details, and [API Reference](#api-reference) for provisioning.

2. Pick your integration guide.

   - [OpenClaw / ClawHub](https://mem9.ai/openclaw-memory)
   - [Hermes Agent](https://github.com/mem9-ai/mem9-hermes-plugin#readme)
   - [Claude Code](claude-plugin/README.md)
   - [OpenCode](opencode-plugin/README.md)
   - [Codex](codex-plugin/README.md)
   - [DeepSeek Harness](dsh-plugin/README.md)
   - [Dify](https://github.com/mem9-ai/mem9-dify-plugin#readme)
   - [Any HTTP client / custom runtime](#api-reference)

3. Set your credentials.

   ```bash
   # Hosted API
   export MEM9_API_URL="https://api.mem9.ai"
   export MEM9_API_KEY="<mem9-api-key>"

   # Self-hosted
   export MEM9_API_URL="http://localhost:8080"
   export MEM9_API_KEY="<mem9-api-key>"
   ```

   For self-hosted deployments, use your server URL and the mem9 API key returned or configured by your provisioning flow.

## Why mem9

mem9 gives coding agents one shared memory layer instead of separate local notebooks and one-off prompt files.

| What mem9 gives you | Why it matters |
|---|---|
| Persistent memory across sessions and machines | Your context survives restarts, laptop switches, and long-running projects |
| Shared memory across agents and workflow platforms | OpenClaw, Hermes Agent, Claude Code, OpenCode, Codex, DeepSeek Harness, Dify apps, and custom clients can recall the same facts |
| Stateless integrations | Runtime plugins stay thin because storage, search, ingest, and policy live in the server |
| Hybrid recall and a visual dashboard | Semantic search, keyword search, and inspection workflows stay in one system |

## Supported Platforms and Agent Runtimes

| Platform | Integration shape | Install / docs |
|---|---|---|
| OpenClaw | `kind: "memory"` plugin for server-backed shared memory | [OpenClaw / ClawHub install guide](https://mem9.ai/openclaw-memory) |
| Hermes Agent | Memory provider plugin with setup and activation flow | [mem9-hermes-plugin README](https://github.com/mem9-ai/mem9-hermes-plugin#readme) |
| Claude Code | Marketplace plugin with hooks and skills | [`claude-plugin/README.md`](claude-plugin/README.md) |
| OpenCode | Plugin SDK integration loaded from `opencode.json` | [`opencode-plugin/README.md`](opencode-plugin/README.md) |
| Codex | Marketplace plugin with managed hooks and project overrides | [`codex-plugin/README.md`](codex-plugin/README.md) |
| DeepSeek Harness | Native DSH/Cordis bundle with recall, smart ingest, and memory tools | [`dsh-plugin/README.md`](dsh-plugin/README.md) |
| Dify | Tool plugin for Dify Agent apps and Workflow apps, with single-space and multi-space authorization | [mem9-dify-plugin README](https://github.com/mem9-ai/mem9-dify-plugin#readme) |
| Any HTTP client / custom runtime | Direct REST API integration | [API Reference](#api-reference) |

All supported runtimes and platform integrations expose the same core memory flow: store, search, get, update, and delete against the mem9 server API.

## Why the Hosted API

The hosted mem9 API is the fastest way to put persistent memory behind an agent fleet while keeping the option to self-host later.

| Hosted API capability | Why teams start here |
|---|---|
| Hosted mem9 API with instant space provisioning | You can install an agent integration first and skip standing up infrastructure on day one |
| Shared memory across runtimes and platforms | One space can serve OpenClaw, Hermes Agent, Claude Code, OpenCode, Codex, DeepSeek Harness, Dify apps, and custom clients together |
| Managed search and storage | Hybrid recall works out of the box without a separate vector stack or sync layer |
| TiDB Cloud Starter foundation | The hosted path benefits from instant provisioning, native vector search, full-text search, server-side auto-embedding, hybrid search, and MySQL-compatible operational semantics |
| Same API contract as self-hosted mem9 | Moving to your own deployment is a base-URL and credential change, not a plugin rewrite |
| Visual dashboard and product onboarding | Teams can inspect and manage memory without building internal tooling first |

Under the hood, the hosted mem9 API runs the same mem9 server model surfaced in this repository, with TiDB Cloud Starter providing managed provisioning, native vector search, full-text search, server-side auto-embedding, hybrid search, and MySQL-compatible storage semantics.

## API Reference

Set `X-Mnemo-Agent-Id` on authenticated memory, import, and session-message requests when you want the server to distinguish which runtime or agent instance is writing and recalling memories inside the same mem9 space. This works on both the tenant-path `v1alpha1` routes and the `v1alpha2` API-key routes.

### Provisioning

Use this endpoint when you want mem9 to auto-provision a new TiDB-backed space.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/v1alpha1/mem9s` | TiDB auto-provision endpoint when a provisioner is configured. TiDB Zero enables this path by default on `tidb`; TiDB Cloud Pool uses `MNEMO_TIDB_ZERO_ENABLED=false` with `MNEMO_TIDBCLOUD_API_KEY` and `MNEMO_TIDBCLOUD_API_SECRET`. Manual-bootstrap deployments use pre-existing tenants instead of this path. Returns `{ "id" }`. Accepts optional `utm_*` query params for attribution logging |

Prefer `v1alpha2` for all new integrations. It uses `X-API-Key` and is the primary API surface for current runtimes.

### Preferred API (`v1alpha2`)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/v1alpha2/mem9s/memories` | Preferred unified write endpoint. Requires `X-API-Key` header |
| `GET` | `/v1alpha2/mem9s/memories` | Preferred search endpoint. Requires `X-API-Key` header |
| `GET` | `/v1alpha2/mem9s/memories/{id}` | Preferred get-by-id endpoint. Requires `X-API-Key` header |
| `PUT` | `/v1alpha2/mem9s/memories/{id}` | Preferred update endpoint. Requires `X-API-Key` header |
| `DELETE` | `/v1alpha2/mem9s/memories/{id}` | Preferred delete endpoint. Requires `X-API-Key` header |
| `GET/POST` 