<h1 align="center">dsh-hashline-edittool</h1>

<p align="center">
  <img src="docs/images/cards.png" alt="hashline cards: read / edit / grep / LSP / settings" width="760">
</p>

<p align="center">
  <strong>Line-anchored editing for DeepSeek Harness<br>
  Every line gets a variable-length content anchor — no line numbers, no echoing old code, fewer tokens, more context for real work.</strong>
</p>

<p align="center">
  <strong>English</strong> ·
  <a href="README.zh.md">简体中文</a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#the-anchor-contract">The Anchor Contract</a> •
  <a href="#tools">Tools</a> •
  <a href="#settings">Settings</a> •
  <a href="#error-codes">Error Codes</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#acknowledgments">Acknowledgments</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/DeepSeek_Harness-Plugin-blueviolet.svg" alt="DeepSeek Harness Plugin">
  <img src="https://img.shields.io/npm/v/dsh-hashline-edittool" alt="npm version">
  <img src="https://img.shields.io/github/stars/hyperion2144/dsh-hashline-edittool?style=social" alt="GitHub Stars">
</p>

---

## What it is

A [DeepSeek Harness](https://github.com/deepseek-ai) plugin that replaces the built-in
`read` / `edit` / `grep` tools with **hash-anchored** versions and adds `undo_last_edit`,
`ast_grep`, `ast_edit`, and an `lsp` tool on top:

- **Every line carries a content anchor** — a variable-length Base62 marker (2 characters
  covers the first 3,844 lines; the encoding grows only as the file demands). The model
  edits by marker, so it never echoes the code it is replacing.
- **Edits are verified against what the model actually saw.** Each resolved range is checked
  against the *served* mirror (anchor + content). A line that changed under the agent is
  rejected with `[E_STALE]` — and the rejection echoes the current lines **with fresh,
  immediately usable anchors** (reject-and-serve).
- **One call = one atomic batch.** All anchors in one `edit` resolve against the original
  snapshot; any failure rejects the whole call and writes nothing. Multi-file batches are
  grouped per file, each file all-or-nothing, partial success reported.
- **Everything is a card.** The bundled client plugin renders read / diff / grep / undo /
  write / structural / LSP cards in the dsh web UI from structured `presentationMeta` —
  the model text and the UI never have to agree by string parsing.

Ships as one npm package (`dsh-hashline-edittool`): host plugin + web card plugin + prompt
sections, mounted by a single bundle patch.

## Highlights

**Self-rendering cards.** The bundled client plugin ships its own React components —
`HashlineReadRow`, `HashlineEditRow`, `HashlineGrepRow` (file tabs + match highlighting),
`HashlineUndoRow`, `HashlineWriteRow`, `HashlineAstGrepRow`, `HashlineAstEditRow`,
`HashlineLspRow` — registered straight into the dsh web UI's slots. Every card renders
from the tool's structured `presentationMeta`, with anchor gutters, diff rows, and
highlight spans drawn natively. No generic tool-output cards, no string parsing, no
upstream web changes.

**Dynamic-length anchors.** Anchors are not fixed-width hashes. Allocation is
shortest-first: 2 characters cover the first 3,844 lines, and a new layer grows only when
the file demands it (up to 62⁸ lines — practically unbounded). All-digit encodings are
skipped so a marker can never be confused with a line number, collisions are probed and
resolved at allocation time, and surviving lines keep their anchors across edits within
the session.

**AST + LSP, two semantic backends.** `ast_grep` / `ast_edit` answer "where does the
syntax match" through a sandboxed tree-sitter worker, with a curated grammar catalog
(SHA-256-pinned downloads, install/uninstall routes) and folded editable outlines for
long files. The `lsp` tool answers "what does this symbol mean" through a real language
server per language — started on demand, shared with dsh's own `lsp` service — and falls
back to a heuristic backend when none can be had. Both serve their rows, so structural and
semantic results are directly editable.

**Diagnostics on write.** After an edit/write lands, the plugin baselines the language server with the pre-write text, pulls diagnostics, and delivers them per written file — an inline, severity-tinted capsule under the card within a short window, with bounded async delivery at the model's next natural step, riding both the JSON envelope and the text channel. One switch (`lsp.auto_diagnostics`) turns it off.

**A settings panel rendered by the plugin itself.** The bundled `HashlineSettingsCard` is
a full settings UI in the web: separator, output format, context lines,
require_line_content, the AST master switch plus per-language toggles, named LSP servers,
auto-diagnostics. Edit, commit, done — no YAML editing required.

**Hot switching, everywhere.** A committed settings change takes effect on the **next
tool call** — output format, separator, context lines, AST/LSP toggles (verified live:
flipping `output_format` mid-session immediately changes what the model receives). And the
switch with the biggest blast radius is handled too: flipping `require_line_content`
disposes and re-registers the `edit` tool's schema, so the model's very next step sees the
new `{ anchor, line }` parameter set — no restart anywhere.

## Quick Start

```sh
npx @deepseek-ai/dsh plugin --profile web add github:hyperion2144/dsh-hashline-edittool   # from github
npx @deepseek-ai/dsh plugin --profile web add dsh-hashline-edittool                       # from npm
npx @deepseek-ai/dsh plugin --profile web add /path/to/dsh-hashline-edittool              # local checkout
```

The profile's next session runs with the hashline tools installed. Verify the layer is active:

```sh
dsh --profile <name> --dump-config   # shows a "# == dsh-hashline-edittool" layer
```

| Requirement | |
| --- | --- |
| Node | `^22.19.0 \|\| >=24.0.0` (dsh's requirement; the store uses `node:sqlite`) |
| Profile | a dsh profile (`dsh plugin` initializes one on first use) |
| Backends | sandboxed / remote filesystems supported (writes go through `ctx.fs`) |

## The Anchor Contract

### Markers

- An anchor is a variable-length Base62 marker, **unique per line** (identical content
  lines get *distinct* anchors — the anchor is a row identity, not a content hash you can
  guess). Digits-only encodings are skipped, so a marker is never all digits.
- A marker is written `<anchor>` or `<anchor>:<line>`; `line` is a **positional hint only**
  — the anchor is authoritative, and a disagreeing hint is a warning
  (`[E_LINE_HINT]`), not an error. The legacy `<line>:<anchor>` order is still accepted.
- `read` output opens with an `ANCHOR:FILELINE` header separating the marker column from
  verbatim content, using the configured separator (`|` in the examples below):

```text
ANCHOR:FILELINE
G8:1|// UI demo file
ur:2|export const APP = "hashline";
D0:4|export function greet(name: string): string {
```

### Served-state verification (reject-and-serve)

A row becomes **served** when a tool result shows it to the model (`read`, `grep`, edit
diffs, structural results, LSP rows). `edit` verifies each resolved range against that
mirror before writing:

- anchor unknown or row never served → `[E_RANGE_UNSERVED]` / `[E_RANGE_UNVERIFIED]`;
- served content differs from disk → `[E_STALE]` / `[E_RANGE_STALE]`;
- every rejection **echoes the current lines as served rows with fresh anchors**, so the
  fix is: take the marker from the echo and resubmit. Served rows are also emitted as
  `fs/observed`, so they can be written with immediately.

There is no `Shift:` block — after an edit, take anchors from the diff rows the response
just gave you, or re-read.

### Batch semantics

- `edits[]` apply **in order against one snapshot**; overlapping ranges are
  `[E_BATCH_CONF