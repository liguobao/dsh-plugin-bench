<div align="center">

# dsh-mcp-panel
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-mcp-panel` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-mcp-panel)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-mcp-panel?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-mcp-panel?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-mcp-panel/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-mcp-panel)

**The MCP management console for the official DeepSeek Harness MCP client — add, edit, remove, and trial-call MCP servers from a settings page, with honest status, health diagnostics, and safe, reversible profile writes.**

*Official client = bridge, this plugin = console: read status through the `mcp/status` seam, write only append-only, approval-gated profile patches.*

> **Official repository.** This is the only official repository of dsh-mcp-panel, maintained by PerryLink. Same-name repositories under other accounts are not affiliated.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-mcp-panel.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-top-rated.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-mcp-panel/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-mcp-panel/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-mcp-panel?label=version)](https://github.com/PerryLink/dsh-mcp-panel/releases)
[![npm version](https://img.shields.io/npm/v/dsh-mcp-panel)](https://www.npmjs.com/package/dsh-mcp-panel)
[![npm downloads](https://img.shields.io/npm/dm/dsh-mcp-panel)](https://www.npmjs.com/package/dsh-mcp-panel)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (verified 2026-09-18): dual typecheck rulers green on the `0.1.6-alpha.2` dev/test face (this repo is the family's canary — no new errors surfaced), 174 tests, and the full gate chain (typecheck / typecheck:ci / test / build / verify / package). The `writePatch` re-verification assertion stands on this line. Previous baseline: `dsh-v0.1.7-alpha.1` (verified 2026-09-16). |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Platforms | Web GUI (dual-face: host + browser) |
| Model | Any (the panel is read-only; only `/mcp` output is model-readable) |

## What you get

`dsh-mcp-panel` is the experience layer on top of the official MCP client: a read-only runtime view plus safe, reversible profile writes.

- **`/mcp` command** — one row per server: transport, target, tool count, connection status (from the upstream seam; `unknown` when unobserved), last error, reconnect count — model-readable, session-log reconstructable, five output languages.
- **`/mcp <server> tools`** — model-visible `mcp__*` tool names and descriptions.
- **`/mcp <server> health`** — derived self-heal suggestions (ENOENT → missing dependency, ECONNREFUSED, timeouts, 401/403/404, DNS, rate limit, reconnect exhaustion…); exit code / stderr tail honestly labeled *pending upstream support* until the client exposes them.
- **`/mcp <server> disable` / `enable`** — turn one server row off or back on without editing the profile patch by hand.
- **`/mcp <server> probe`** — one Streamable HTTP connectivity probe for that server (background job).
- **`/mcp <server> call <tool> [json]`** — trial-call through the **official tool pipeline** (`ctx.tools.execute()`); pre-execute permission policy, approval, guards, and post-execute all apply.
- **Settings → Plugins → MCP tab** — status cards with badges, diagnostics, and probes, plus the server CRUD and the tool trial console.
- **Server CRUD** — add/edit/remove forms → `insert` for add and id-targeted overrides (`- id:` + `name:` + `disabled:`/`config:`) for edit/remove → clipboard copy or approval-gated write with automatic backups and loader re-verification.
- **Resources browse** — read-only resource listing, template listing, and URI reads through the official `list_mcp_resources` / `list_mcp_resource_templates` / `read_mcp_resource` tools (bridged by the shipped `@deepseek-ai/dsh-mcp-resources` service); results are shown in the tab only, never in model context.
- **Recommended directory** — a built-in community MCP server catalog (filesystem, git, github, fetch, playwright, …) served in the snapshot; `catalogEntries` appends/overrides entries, and `catalogToConfigInput` turns one into a one-click add.
- **Config import/export** — `exportConfigs()` serializes the server rows to a versioned JSON document (a `!!js` row exports as `null` with a reason), and `importPreview()` parses an export back into per-server `add` patch fragments for review.
- **Tool trial console** — server → `mcp__*` tool → JSON args → canonical JSON result + rendered content; capped by `trialMaxResultChars`; panel-only, never model context.

## Architecture: official client = bridge, this plugin = console

[`@deepseek-ai/dsh-mcp-client`](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/mcp/mcp-client) is the **only bridge**: one plugin instance per MCP server, configured as a hand-written `cordis.yml` row, connecting the transport, syncing tools, and registering `mcp__<server>__<tool>` names. This plugin never replaces it — it is the **experience layer on top**:

```text
                    ┌────────────────────────────────────────────┐
 profile            │  cordis.yml / cordis.patch.yml             │
 composition        │   - id: mcp-github                          │
 (one row per       │     name: '@deepseek-ai/dsh-mcp-client'     │
  server, hand-     │     config: { serverName, transport, … }    │
  written)          │   - id: mcp-panel                           │
                    │     name: dsh-mcp-panel   ◄── this plugin   │
                    └───────────────┬────────────────────────────┘
                                    │
        ┌───────────────────────────┴───────────────────────────┐
        │                                                        │
   ┌────▼──────────────┐        ┌───────────────────────────┐    │
   │ @deepseek-ai/dsh- │        │ dsh-mcp-panel (console)   │    │
   │ mcp-client        │        │                           │    │
   │ • transport       │        │ • /mcp command            │    │
   │ • tool sync       │        │ • Settings → Plugins →    │    │
   │ • mcp__* tools    │◄──────►│   MCP tab: CRUD, trial    │    │
   │ • mcp/status seam │ status │ • health diagnostics      │    │
   └───────────────────┘        │ • probes, capabilities    │    │
                                └───────────────────────────┘    │
```

The console **reads** the client through its proposed `mcp/status` observability seam (not yet shipped upstream; feature-detected) (event + `mcpStatus` query service), the tool registry, and the loader; it **writes** only the profile's patch layer — append-only, approval-gated, always backed up. Transport, OAuth, and protocol stay untouched.

## Console vs. hand-written cordis.yml

| | Hand-written cordis.yml | dsh-mcp-panel console |
|---|---|---|
| Add a server | Edit YAML, mind indent/quoting | Form → patch fragment → **copy** or **write** (approval + auto backup) |
| Edi