<div align="center">

# 🖱️ dsh-click
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-click` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-click)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-click?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-click?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-click/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-click)

**Cross-platform native desktop control for DeepSeek Harness — Windows first.**

*Look at the screen, then act — every click gated, every action audited.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-click.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-click/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-click/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-click?label=version)](https://github.com/PerryLink/dsh-click/releases)
[![npm version](https://img.shields.io/npm/v/dsh-click)](https://www.npmjs.com/package/dsh-click)
[![npm downloads](https://img.shields.io/npm/dm/dsh-click)](https://www.npmjs.com/package/dsh-click)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (GitHub tag, verified 2026-09-11). Verified 2026-09-11 against the dsh-v0.1.7-alpha.1 master checkout (full gate chain + profile install smoke). |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Platforms | **Windows first** (UIAutomation + Win32 input, via a bundled PowerShell helper); macOS/Linux backends are reserved and fail closed with a clear reason |
| Model | Text-only models fully supported (`screen_read` returns structured text); vision models additionally get `screen_shot` images |

## What you get

`dsh-click` gives the harness a complete observe → act loop over native desktop applications:

- **`screen_shot`** — screenshot of a window (or the primary screen), downscaled to a configurable bound. With a vision-capable model the result carries the image; otherwise a text description keeps text-only models working.
- **`screen_read`** — the structured observation: the window's accessibility tree (element ids, types, names, rectangles, supported patterns) plus pixel-location hints with colors — plain text, no image model required.
- **`click` / `type` / `scroll` / `key`** — window-scoped actions addressed by element id or coordinates. Delivery prefers UIA invoke, falls back to posted window messages — and **never steals foreground focus**.
- **`app_list` / `app_launch`** — enumerate running applications and their windows; launch one by name or path.

Every mutating action crosses one safety boundary:

1. **Freshness** — the action must cite a `basedOn` observation; the window is re-captured right before acting and the action is refused if the screen changed (pixel-hash check + max-age bound).
2. **Approval** — `ctx.approval` gates every action by default; window-title/executable regexes can allowlist specific windows (still audited).
3. **Process identity** — the owning process's pid and executable path are verified before **and** after the act; a change refuses the outcome loudly.
4. **Audit** — observations and actions land in the session log as `dsh-click/observed` / `dsh-click/action` events (sanitized, log-only).

```text
model                           harness
  │ screen_read ──▶ observationId (+ elements, pixels)         ← structured text
  │ click {basedOn, target} ──▶ freshness check ──▶ approval ──▶ helper (UIA)
  │                             pixel hash changed? ── refuse + re-observe
  │                             pid/exe changed after act? ── PROCESS_CHANGED
  │ ◀── canonical JSON + audit events (dsh-click/action)
```

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-click#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-click

# 2. restart and verify the row
dsh --profile web --dump-config | grep -A2 'id: dsh-click'
```

Then ask the agent to look at a window and act — the approval prompt appears for every mutating action:

```
> Open Notepad, type "hello", then read back what is on screen.
```

## Install & uninstall

- **git channel** (latest `main`): `dsh plugin --profile web add "github:PerryLink/dsh-click#main"` — the `prepare` script builds with production dependencies only.
- **npm channel** (published releases): `dsh plugin --profile web add dsh-click`.
- **tarball channel**: `pnpm pack` in this repo, then `dsh plugin --profile web add ./dsh-click-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove dsh-click` (or remove the row from the profile patch).

> If pnpm reports `ERR_PNPM_IGNORED_BUILDS` for this package (esbuild's harmless platform-binary validation), add `allowBuilds: { esbuild: true }` to your `pnpm-workspace.yaml` — the `dsh` CLI prints the exact snippet.

## Configuration

All tunables are Schemastery `Config` fields (changeable from cordis.yml). An id-targeted override replaces the whole row — restate every key you need. `cordis.patch.yml` documents each key inline.

| Key | Default | Meaning |
|---|---|---|
| `requireApproval` | `true` | Gate every mutating action behind approval; observers never ask |
| `autoApproveWindows` | `[]` | Window-title/executable regexes that skip the approval ask (still freshness-checked and audited) |
| `auditSessionEvents` | `true` | Append `dsh-click/observed` / `dsh-click/action` session audit events. The adaptive gate already skips the append on envelope-less hosts (rc.6–rc.8, 0.1.1-rc.2, and 0.1.2-rc.1, which fails closed on unknown types at read); set `false` to stop audit appends entirely 0.1.2-rc.1 (adapted 2026-09-02): the session envelope keeps its ignorable field for stored-log read compatibility only - Session.append still cannot stamp it, so audit-gate behavior is unchanged. |
| `focusFallback` | `never` | Whether an action may bring the target window to the foreground as a last resort (`never` / `allow`) |
| `imageMode` | `auto` | `screen_shot` rendering: `auto` (image when the model accepts images, text otherwise) or `text` |
| `helperTimeoutMs` | `30000` | Per-helper-call timeout in ms (1..300000) |
| `maxHelperOutputBytes` | `25165824` | Cap on one helper response in bytes (1024..67108864) |
| `maxScreenshotSide` | `2560` | Longest screenshot side in pixels (320..7680); larger captures are downscaled |
| `staleCheckPixels` | `true` | Compare a fresh pixel hash before every action and refuse on change |
| `maxObservationAgeMs` | `30000` | Maximum age in ms of an observation an action may cite (1000..600000) |
| `maxCachedObservations` | `8` | LRU cap on cached observations (1..64) |
| `maxElements` | `500` | Cap on accessibility elements per `screen_read` (1..2000) |
| `maxTreeDepth` | `32` | Maximum accessibility tree-walk depth (1..64) |
| `maxTextLength` | `200` | Truncation length for sanitized model-visible strings (16..10000) |
| `rollbackEnabled` | `true` | Back up and restore control text when `type` fails |
| `ocr.enabled` / `command` / `language` | `true` / `tesseract`