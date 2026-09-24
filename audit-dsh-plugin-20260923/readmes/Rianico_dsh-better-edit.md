<p align="center">
  <img src="assets/logo.svg" alt="dsh-better-edit" width="200">
</p>

<h1 align="center">dsh-better-edit</h1>
<p align="center">
  <strong>A better edit tool for DeepSeek Harness<br>
  Position-free hashes — one read, many edits, fewer tokens, more room for real work.</strong>
</p>
<p align="center">
  <strong>English</strong> ·
  <a href="README.zh.md">简体中文</a>
</p>

<p align="center">
  <a href="#why-you-need-this"><img src="https://img.shields.io/badge/why-hashline-blue?style=flat" alt="why hashline"></a>
  <a href="#quick-start"><img src="https://img.shields.io/badge/quick_start-30s-brightgreen?style=flat" alt="quick start 30s"></a>
  <a href="#benchmark"><img src="https://img.shields.io/badge/correctness-23%2F23-success?style=flat" alt="23/23 battery"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#why-hashline">Why Hashline</a> •
  <a href="#tools">Tools</a> •
  <a href="#benchmark">Benchmark</a> •
  <a href="#how-anchors-work">How Anchors Work</a> •
  <a href="#development">Development</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.7.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/DeepSeek_Harness-Plugin-blueviolet.svg" alt="DeepSeek Harness Plugin">
  <img src="https://img.shields.io/npm/v/dsh-better-edit" alt="npm version">
  <img src="https://img.shields.io/npm/dm/dsh-better-edit" alt="npm downloads">
  <img src="https://img.shields.io/github/stars/Rianico/dsh-better-edit?style=social" alt="GitHub Stars">
</p>

<p align="center">
  <img src="assets/banner.svg" alt="file.ts → read → hashed lines → edit by hash → diff" width="900">
</p>

---

> _"The harness — not the model — is the bottleneck."_ — Can Bölük, [_The Harness Problem_](https://stencil.so/blog/the-harness-problem)

> **This is the harness fix.** Hashes replace line numbers — edits above don't shift anchors below. One `read` serves many `edit`s; drift outside your range passes with a notice, true conflicts retry with fresh anchors — no full `read` needed.

> **3 calls vs 6 · -55.8% tokens · 23/23 correctness.** Same external-drift refactor, same file (single stochastic run; [method](https://github.com/Rianico/pi-better-edit/blob/main/benchmarks/results/2026-08-17-practical-token-benchmark.md)). Payload numbers are deterministic — see [Benchmark](#benchmark).

## Why you need this

**If you've watched `line 47 → 74` corrupt a file after an insert — this is for you.**

| Before: `str_replace` / line numbers               | After: hashline `edit`                                                                                                                  |
| -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Re-types old code (~5-6× billed)                   | Two `3-char` hashes, old text never echoed                                                                                              |
| One insert shifts every number → silent wrong line | Content addresses — edits above don't move anchors below                                                                                |
| No check against what was shown                    | Every line verified; `[E_STALE_RANGE]`/`[E_UNSERVED_RANGE]` reject before write, then **reject-and-serve** returns fresh `HASH│content` |

> [!TIP]
> **Shining points — honest:**
>
> - **Position-free.** `read 1..5` → `insert @0` → `edit 10..12` still lands at `10..12`. Anchors are `canon(line)` hashes, not positions (ADR-0013). Exterior drift is a notice, not a re-read.
> - **Fewer round-trips.** Single-session `1 read → N edits` — no ritual re-reads. Multi-session exterior `A:10..12 / B:20..30` also passes; only overlapping `A∩B≠∅` retries once via `servedRows` (no full `read`). Harness `9/9` green.
> - **Fewer tokens.** Compact payload `{path, edits:[[from,to,text]]}` + never echoing `old_string`; diff/echo/rejection rows count as serves. Envelope `-40%` pinned 12-edit corpus, session `-55.8%` on external-drift.
> - **Concurrent-safe, not silent.** `retired anchor` per `(session,path)` epoch blocks re-bound `S@3→@3`; `retired` + `canon` + `hash` + `changed∩[L,R]` makes `pos-free` single-thread and `strict` only on true overlap. One retry vs silent wrong-line.

Not for one-line touch-ups (near parity) or new files (`write`). Pays off in long sessions and structural edits.

## Quick Start — install to verified edit in 30s

### Install (pick one)

```sh
npx @deepseek-ai/dsh plugin --profile web add github:Rianico/dsh-better-edit   # from github
npx @deepseek-ai/dsh plugin --profile web add dsh-better-edit                 # from npm
npx @deepseek-ai/dsh plugin --profile web add /path/to/dsh-better-edit       # local
```

No config. Next session runs with hashline tools. Verify:

```sh
dsh --profile <name> --dump-config   # shows "# == dsh-better-edit" layer
```

| Requirement |                                          |
| ----------- | ---------------------------------------- |
| Node        | `^22.19.0 \|\| >=24.0.0`                 |
| Profile     | `dsh` profile (`dsh plugin` creates one) |
| Backends    | sandboxed / remote `ctx.fs`              |

### See it work

`read` serves `HASH│content` — the hash _is_ the address:

```text
ve7│function hello() {
szJ│  console.log("world");
kQm│}
```

`edit` by hashes — always lands where you meant:

```json
{ "path": "src/main.ts", "edits": [["szJ", "szJ", "  console.log('hi');"]] }
```

Returns a diff with fresh anchors — next edit needs no `read`:

```text
- szJ │   console.log("world");
+ a3m │   console.log('hi');
  kQm │ }
```

**Position-free in one line:** `read 1..5` → `insert @0` → `edit 10..12` still verifies `10..12` (`resist` mode). **Multi-session honesty:** `A:10..12+1` shifts `B:20..30→21..31` → `B` passes (drift notice); `B:12..13` overlapping `A` → `E_STALE_RANGE` + fresh rows, one retry.

Batch atomically — one `edit`, up to 32 same-file ranges:

```json
{
  "path": "src/main.ts",
  "edits": [
    ["a1b", "a1b", "new line 1\n"],
    ["c3d", "c3d", "new line 2"]
  ]
}
```

One fails → none write (`[E_BATCH_ABORT]`).

> [!TIP]
> **Want proof before you install?** Upstream [23/23 battery](https://github.com/Rianico/pi-better-edit/blob/main/benchmarks/README.md) runs no LLM — stale edits are rejected every run. Same algorithm.

### Configuration

Tenancy and prompt guidance declare once, read at `agent/created`, no code change.

**Store** central by default `$DSH_HOME/plugins/dsh-better-edit/runtime/<name>-<hash8>/` (`ls`-readable + `.wsPath` sidecar). DBs are disposable caches — `rm -rf runtime/<name>-<hash8>/` is safe, rebuilt on next `read`.

```yaml
# $DSH_HOME/plugins/dsh-better-edit/config.yaml
storeDir: central # central | workspace | /abs
autoGitignore: false
undo_ttl_s: 604800 # 7d, -1 forever
storeMaxAgeS: 2592000 # 30d janitor
storeMaxTotalBytes: 524288000 # 500 MB LRU
```

Env overrides yaml (`DSH_BETTER_EDIT_STORE_DIR`, `DSH_BETTER_EDIT_AUTO_GITIGNORE`).

**Guidance per preset** — `tool:read` / `tool:edit` / `tool:undo_last_edit` are plain markdown per preset at `$DSH_HOME/plugins/dsh-better-edit/<preset>/<section>.md` (orders `130/131/133`). Delete or empty a file → default re-seeds at next boot; keep a `---` fence to blank on purpose.

## Why Hashline

**Verified against what was served.** Every resolved line checked against `read`/diff/rejection rows. Stale or unseen → `[E_STALE_RANGE]`/`[E_UNSERVED_RANGE]` + fresh `HASH│content`, retry needs no `read`. Session-scoped — sub-agent serves never validate main edits.

**Content-addressed.** `canon(line)` strips ASCII whitespace, `xxh32 → 62³=238,328` anchors. Re-inserting identical text keeps its hash; `prettier`/`eslint --fix` between edits doesn't invalidate. Unique by bitset probing — `}`/`impo