<div align="center">

# 🛰️ dsh-lsp-actions
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-lsp-actions` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-lsp-actions)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-lsp-actions?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-lsp-actions?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-lsp-actions/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-lsp-actions)

**The LSP action surface for DeepSeek Harness — real language servers, real feedback, and the IDE integration backend for editors.**

*Diagnostics, formatting, completion, code actions, symbols, signature help, inlay hints, and rename for your agent's editor loop — plus the stable editor action protocol (`lsp.actions.*`) that lets any editor consume them directly.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-lsp-actions.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-top-rated.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-lsp-actions/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-lsp-actions/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-lsp-actions?label=version)](https://github.com/PerryLink/dsh-lsp-actions/releases)
[![npm version](https://img.shields.io/npm/v/dsh-lsp-actions)](https://www.npmjs.com/package/dsh-lsp-actions)
[![npm downloads](https://img.shields.io/npm/dm/dsh-lsp-actions)](https://www.npmjs.com/package/dsh-lsp-actions)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (compat declared for `>=0.1.2-rc.1 <0.2.0 \|\| >=0.1.5-alpha.1 <0.2.0 \|\| >=0.1.6-0 <0.2.0 \|\| >=0.1.7-0 <0.2.0`); the plugin writes no session events itself - the host records the standard tool/call + tool/result events. The released seam still carries only the four legacy operations, so the plugin keeps its own client and records that vintage on the first action call. Verified 2026-09-18 (dual typecheck rulers + full test suite + self-contained/artifacts gates). |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Platforms | All (pure host; subprocess + filesystem, no network) |
| Model | Any (tools are model-agnostic; the plugin never calls a model) |

## What you get

`dsh-lsp-actions` mounts as a single host row (`id: lsp-actions`, `name: dsh-lsp-actions`, `inject: [tools, fs, subprocess]`). The official DeepSeek Harness `ctx.lsp` seam covers **navigation** (go-to-definition, references, implementation, hover); this plugin completes the **action surface** — the feedback loop an agent needs while it writes and fixes code:

1. **Eight `lsp_*` tools** — diagnostics, formatting, completion, code actions, symbols, signature help, inlay hints, and rename, all served by the same language servers your IDE uses.
2. **Editor action protocol v1** — a stable JSON-RPC surface (`lsp.actions.list` / `lsp.actions.run` / `lsp.events`) that lets any editor (VS Code first) consume those capabilities directly.
3. **Real-server verification** — a real `typescript-language-server` run is part of the test suite (self-contained, CI on Node 22/24 across Linux, Windows, and macOS), not just mocks.

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-lsp-actions#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-lsp-actions

# 2. restart and verify the row
dsh --profile web --dump-config | grep -A3 'id: lsp-actions'
```

## Install & uninstall

- **git channel** (latest `main`): `dsh plugin --profile web add "github:PerryLink/dsh-lsp-actions#main"` — the `prepare` script builds (`tsc --noEmitOnError && node scripts/fix-dts.mjs`).
- **npm channel** (published releases): `dsh plugin --profile web add dsh-lsp-actions`.
- **tarball channel**: `pnpm pack` in this repo, then `dsh plugin --profile web add ./dsh-lsp-actions-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove dsh-lsp-actions` (or remove the row from the profile patch).

## Configuration

All tunables are Schemastery `Config` fields (changeable from cordis.yml). An id-targeted override replaces the whole row — restate every key you need. `cordis.patch.yml` documents each key inline.

| Key | Default | Meaning |
|---|---|---|
| `servers` | `{}` | Named language servers; an empty table activates no servers |
| `editor.enabled` | `false` | Serve the editor action protocol over JSON-RPC stdio (headless backend only) |
| `editor.requestTimeoutMs` | `60000` | Per-run timeout budget (ms) for the editor protocol |
| `editor.diagnosticsCacheMaxFiles` | `64` | Bounded LRU diagnostics-cache size (files) |
| `maxDiagnostics` | `200` | Diagnostics cap per result |
| `maxCompletionItems` | `20` | Completion-items cap per result |
| `maxCodeActions` | `50` | Code-actions cap per result |
| `maxSymbols` | `100` | Symbol-results cap |
| `maxSignatures` | `10` | Signature-help cap |
| `maxInlayHints` | `200` | Inlay-hints cap |
| `maxResultChars` | `16000` | Rendered-result cap (chars) |
| `maxDocumentBytes` | `4000000` | Document-read cap (bytes) |
| `timeoutMs` | `60000` | Per-call timeout, enforced by the official timeout policy |

Each `servers` entry is an `LspServerEntry`: `command` (executable resolved on PATH at load) and `extensionToLanguage` (`".ts"` → `typescript`) are required; optional `fileGlobs`, `projectMarkers`, `args`, `env`, `initializationOptions`, `configuration`, `formattingOptions`, `maxMessageBytes`, `maxStderrBytes`, `killGraceMs`, `shutdownTimeoutMs`, `diagnosticsSettleMs`, `diagnosticsDebounceMs`, and `idleTimeoutMs` (`0` = keep the server process alive) tune the built-in stdio client.

Routing is deterministic and configuration-driven. Every file takes the first match from: **(1)** a server entry whose `fileGlobs` match the path; **(2)** the nearest ancestor directory — walking up to the workspace root — that holds a project config file listed in some entry's `projectMarkers`, matched against the entries that also map the file's extension; **(3)** the entry whose `extensionToLanguage` maps the file's extension, in config order. A workspace holding `apps/node-app/{package.json,tsconfig.json,src/main.ts}` and `apps/deno-app/{deno.json,src/main.ts}` therefore serves each `main.ts` from its own project's server, with no path rule to maintain and nothing to change when a project is added, renamed, or moved:

```yaml
servers:
  typescript:
    command: typescript-language-server
    args: ["--stdio"]
    extensionToLanguage: { ".ts": typescript, ".tsx": typescriptreact }
    projectMarkers: ["package.json", "tsconfig.json"]
  deno:
    command: deno
    args: ["lsp"]
    extensionToLanguage: { ".ts": typescript, ".tsx": typescriptreact }
    projectMarkers: ["deno.json", "deno.jsonc"]
```

A project marker only decides among servers that already map the file's extension (it never widens an entry's file types); the walk never leaves the workspace root, and a project config in one directory never applies to a sibling directory. Step **(1)** outranks a project marker: an entry whose `fileGlobs` match the path still wins, so drop projec