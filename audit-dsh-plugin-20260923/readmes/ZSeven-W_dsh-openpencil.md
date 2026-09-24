<p align="center">
  <img src="./docs/images/dsh-openpencil-logo.png" alt="DSH OpenPencil" width="120" />
</p>

<h1 align="center">DSH OpenPencil</h1>

<p align="center">
  <strong>The DeepSeek Harness plugin for OpenPencil — preview, inspect, and edit real <code>.op</code> documents inside a conversation.</strong><br />
  <sub>Exact Multi-Frame Previews &bull; Interactive Canvas &bull; Managed Editor &bull; Agent-Native Design Tools</sub>
</p>

<p align="center">
  <sub>npm: <a href="https://www.npmjs.com/package/@zseven-w/dsh-openpencil"><code>@zseven-w/dsh-openpencil</code></a> · Current plugin release: <code>0.1.0-rc.7</code> · Tested through DSH <code>0.1.1-rc.2</code></sub>
</p>

<p align="center">
  <a href="./README.md"><b>English</b></a> · <a href="./README.zh.md">简体中文</a> · <a href="./README.zh-TW.md">繁體中文</a> · <a href="./README.ja.md">日本語</a> · <a href="./README.ko.md">한국어</a> · <a href="./README.fr.md">Français</a> · <a href="./README.es.md">Español</a> · <a href="./README.de.md">Deutsch</a> · <a href="./README.pt.md">Português</a> · <a href="./README.ru.md">Русский</a> · <a href="./README.hi.md">हिन्दी</a> · <a href="./README.tr.md">Türkçe</a> · <a href="./README.th.md">ไทย</a> · <a href="./README.vi.md">Tiếng Việt</a> · <a href="./README.id.md">Bahasa Indonesia</a>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/@zseven-w/dsh-openpencil"><img src="https://img.shields.io/npm/v/%40zseven-w%2Fdsh-openpencil?style=flat&color=cfb537" alt="npm" /></a>
  <a href="https://github.com/ZSeven-W/dsh-openpencil/actions/workflows/check.yml"><img src="https://img.shields.io/github/actions/workflow/status/ZSeven-W/dsh-openpencil/check.yml?label=CI" alt="CI" /></a>
  <a href="https://github.com/ZSeven-W/dsh-openpencil/stargazers"><img src="https://img.shields.io/github/stars/ZSeven-W/dsh-openpencil?style=flat&color=cfb537" alt="Stars" /></a>
  <a href="https://github.com/ZSeven-W/dsh-openpencil/blob/main/LICENSE"><img src="https://img.shields.io/github/license/ZSeven-W/dsh-openpencil?color=64748b" alt="License" /></a>
  <a href="https://discord.gg/h9Fmyy6pVh"><img src="https://img.shields.io/badge/Discord-Join%20chat-5865F2?logo=discord&logoColor=white" alt="Discord" /></a>
</p>

<br />

<p align="center">
  <img src="./docs/images/dsh-openpencil-overview.png" alt="DSH OpenPencil — multi-frame preview and sidebar editor" width="100%" />
</p>
<p align="center"><sub>Exact multi-frame <code>.op</code> previews with an interactive canvas and the managed editor workbench</sub></p>

## Why DSH OpenPencil

DSH OpenPencil connects [DeepSeek Harness](https://github.com/deepseek-ai/DSH) with [OpenPencil](https://github.com/ZSeven-W/openpencil) so an Agent drives a real, editable, interactive design canvas instead of returning a generated image.

<table>
<tr>
<td width="50%">

### 🖼️ Exact Multi-Frame Previews

The installed OpenPencil headless exporter renders design-faithful previews: the first top-level frame as a large replay-safe PNG, plus a horizontally scrollable thumbnail rail, click-to-select, and previous/next navigation for multi-frame documents.

</td>
<td width="50%">

### 🗺️ Interactive Canvas

"Open interactive canvas" lazily mounts the read-only OpenPencil Web SDK with pan, zoom, and fit — inspect any page, nested node, or inactive page without leaving the conversation.

</td>
</tr>
<tr>
<td width="50%">

### ✏️ Managed Editor

With `editable: true`, the edit action opens the managed OpenPencil editor — selection, layers, properties, drawing tools, undo/redo, and explicit save semantics — in a resizable right-hand workbench with a full-screen option.

</td>
<td width="50%">

### 🤖 Agent-Native Design Tools

Five direct-canvas tools plus six `openpencil_pipeline_*` tools let the Agent create, inspect, refine, publish, modify, and read a real canvas through managed OpenPencil runtimes.

</td>
</tr>
<tr>
<td width="50%">

### 🔐 Capability-Gated Grants

Image and document grants are signed, hash-bound capabilities. Browser metadata never exposes an arbitrary host path, and signed preview/editor capabilities never enter the canonical tool result or model context.

</td>
<td width="50%">

### ⚡ Transactional Safety

A full-pipeline document stays in a private unpublished draft until every native and DSH quality gate passes. Publication never overwrites an existing path, and aborts or failed batches leave no empty target behind.

</td>
</tr>
<tr>
<td width="50%">

### 🌍 Follows DSH Look & Feel

The tool card and managed editor follow DSH's Chinese/English locale and light/dark theme without reloading the editing session.

</td>
<td width="50%">

### 🎯 One Complete Workflow

"Requirement → private draft → semantic batches → live user previews → deterministic structure/layout/quality validation → exact-PNG-integrity atomic publish" — one complete loop inside DSH.

</td>
</tr>
</table>

## Install into DSH

DSH is a separate package. Install it once if you do not already have it:

```sh
npm install -g @deepseek-ai/dsh@latest
```

Then add the plugin to a profile and start the web app:

```sh
dsh plugin --profile web add @zseven-w/dsh-openpencil@next
dsh web
```

The plugin is still on a prerelease line, so install it from the npm `next` tag. The npm `latest` tag currently points to the older `0.1.0-rc.1` package.

For local development, build the checkout, link its absolute path into the Web profile, and then restart DSH:

```sh
pnpm run build
dsh plugin --profile web add link:/absolute/path/to/dsh-openpencil
dsh web
```

The `link:` dependency exposes subsequent rebuilds from this checkout, but DSH must be fully restarted after replacing the profile dependency because the shipped Web profile does not hot-reload host bundles by default.

Prefer not to install DSH globally? Run the same two steps through `pnpm dlx`:

```sh
pnpm dlx --package=@deepseek-ai/dsh@latest dsh plugin --profile web add @zseven-w/dsh-openpencil@next
pnpm dlx --package=@deepseek-ai/dsh@latest dsh web
```

> The OpenPencil plugin is public and requires no npm token. If the DSH prerelease itself requires registry authentication, keep that credential in a user-level or temporary npm config outside the checkout. This repository intentionally contains no registry credentials.

## Design Tools

| Tool | What it does |
| --- | --- |
| `openpencil_new` | Compatible fast path for simple jobs: runs one transactional QuickJS `batch_design` script, publishes with create-if-absent semantics, and returns an editable presentation. Prefer the full pipeline below for production design. |
| `openpencil_pipeline_begin` | Starts an owner-scoped private draft, internally seeds its only root, returns `rootNodeId`, `continuationStyle`, and the compact runtime-matched canvas/build contract, then immediately opens the same live draft in the sidebar; the target `.op` remains unpublished. |
| `openpencil_pipeline_context` | Loads one bounded guideline, style, theme, or UI-kit detail that is genuinely missing from the begin contract; it is not a startup-context refresh loop. |
| `openpencil_pipeline_batch` | Runs at most two direct native `I(...)`/`K(...)` generation scripts: the bounded first-visible-viewport script returned by begin's `next`, then one script for every remaining region. Before exposing the second preview, an authored-structure gate rejects empty category/product helpers, atomically restores the first-batch snapshot, and permits one corrected second script without consuming the two-script budget. Each successful transaction attempts an exact user-facing PNG and must be followed immediately, without narration, by its returned `next`. A third generation script is rejected; only the complete repair gate returned by finish may authorize one bounded `U(...)` QuickJS repair script. |
| `openpencil_pipeline_inspect` | Provides manual diagnostics only when the user explicitly requests them; ordinary generation never uses it as a preview or model-inspection step. |
| `openpencil_pipeli