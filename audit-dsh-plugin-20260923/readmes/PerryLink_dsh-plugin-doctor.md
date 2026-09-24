# dsh-plugin-doctor

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![npm version](https://img.shields.io/npm/v/%40perrylink%2Fdsh-plugin-doctor)](https://www.npmjs.com/package/@perrylink/dsh-plugin-doctor)
[![npm downloads](https://img.shields.io/npm/dm/%40perrylink%2Fdsh-plugin-doctor)](https://www.npmjs.com/package/@perrylink/dsh-plugin-doctor)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-plugin-doctor/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-plugin-doctor/actions)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-plugin-doctor?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-plugin-doctor?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-plugin-doctor/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-plugin-doctor)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

An all-in-one "integrity + runtime health" checker for dsh plugins. Zero dependencies (it uses
only what Node ≥22 ships), and one run covers four layers at once:
**static package-structure checks (R) → Cordis contract scan (K) → dynamic sandbox smoke (D) → ecosystem directory-listing validation (CC)**.
Every criterion traces back to three first-hand research tracks dated 2026-09-07: the deepseek-harness
docs and source, the cordiverse/cordis source contracts, and an inventory of every distribution
channel in the workspace (full text in `SURVEY.md`).

## Installation (DSH bundle)

`dsh-plugin-doctor` declares `dsh.bundle.patch` → `cordis.patch.yml` in package.json, so it can also be installed as a DeepSeek Harness bundle:

```powershell
# git channel (latest main)
dsh plugin --profile web add "github:PerryLink/dsh-plugin-doctor#main"

# npm channel (released version; always use the scoped full name -- the bare name dsh-plugin-doctor is a different project)
dsh plugin --profile web add @perrylink/dsh-plugin-doctor
```

The inserted line loads this package under the standard Cordis plugin contract: the host half is a plain ESM module exporting `apply(ctx)` (declaring `inject` for the services it needs). The package ships no browser UI, so there is no `dsh.client` declaration.

```js
// bundle entry (host half) -- the export contract the patch line loads
export function apply(ctx) {
  // registers the /doctor command and the plugin_doctor read-only check tool
}
```

Uninstall: `dsh plugin --profile web remove @perrylink/dsh-plugin-doctor` (or delete that line from the profile patch). The CLI usage below is unaffected.

## Usage

```powershell
node doctor.mjs --repo <插件仓路径>            # 全量（含动态冒烟，需网络 + pnpm）
node doctor.mjs --repo <路径> --no-smoke       # 仅静态 + 清单
node doctor.mjs --repo <路径> --dsh 0.1.7-alpha.1 # 冒烟宿主版本（默认 npm latest 已发布线）
node doctor.mjs --repo <路径> --only R,K       # 只跑静态两层（推荐用 ASCII 别名）
node doctor.mjs --repo <路径> --json report.json
node doctor.mjs --repo <路径> --json -         # JSON 写 stdout（此时抑制人类可读报告）
node doctor.mjs --repo <路径> --format check --json -   # 生态三值契约视图（PASS/WARN/FAIL + 0/1/2）
node doctor.mjs --repo <路径> --workspace <工作区根>   # 指定兄弟仓所在工作区（CC 组核对用）
node doctor.mjs --repo <路径> --allow-degraded # 显式接受「整组未真跑」（默认 exit 6）
node doctor.mjs --purge <隔离目录>              # 清理本工具产生的隔离目录（仅 doctor-quarantine-*）
```

### Target shapes and coverage (new in 0.2.0)

`--repo` may be a **source tree** or an **installed package directory / unpacked tarball artifact** (the latter is common at `node_modules/<pkg>`). The criteria change with the shape:

| Shape | K group (Cordis contract) | Notes |
|---|---|---|
| Source tree with `src/` | scans `src/**` plus root-level JS (`mode: src`) | complete |
| **No `src/`, `main` points at `lib/`** | **fallback scan of `lib/**` (`mode: lib-fallback`)** | fixed in 0.2.0: the old implementation keyed on "no build script", but published packages **keep** their build script → the fallback never fired, all nine K checks were skipped, and it still exited 0 (false green) |
| Neither `src/` nor `lib/` | all nine skipped (`mode: none`) | **the whole group never really ran → exit code 6**, no more false green |

Coverage is written to `coverage.K` in the JSON (`{filesInspected, mode}`) and summarised in `groups.K`.

### `--only` groups and ASCII aliases

| Alias | Full group name | Contents |
|---|---|---|
| `R` | static · package structure | R0–R8 |
| `K` | static · Cordis contract scan | K1–K9 |
| `D` | dynamic · sandbox smoke | D0–D3, D9 |
| `CC` | ecosystem · directory listings | CC1–CC5 |

Aliases are case-insensitive, and the Chinese full names still work. **Use the aliases in workflows**: if an editor or script round-trips a Chinese group name through the wrong encoding, `--only` matches no group at all.

### Exit-code contract

| Code | Meaning | Introduced |
|---|---|---|
| `0` | no fail/error (warn/skip allowed), and every requested group really ran | 0.1.x |
| `1` | fail/error present (a plugin defect) | 0.1.x |
| `2` | usage error, unknown group, **unknown option** | 0.1.x |
| `3` | infrastructure error (missing npm/pnpm and the like) | **0.2.0** |
| `4` | unsupported host version (the host itself failed to install; **not** a plugin verdict) | **0.2.0** |
| `5` | unstable result (a step timed out or was killed by a signal) | **0.2.0** |
| `6` | **degraded**: a requested group never really ran (e.g. no source files to scan) | **0.2.0** |

**Guarding against silent passes** (two layers):

1. If even one group name in `--only` fails to match → immediately `2`. Versions 0.1.4 and earlier would "check nothing + exit 0" when a group name was mangled, which once turned the CI gates of 35 repos into false green (measured 2026-09-09: `checks_run=0`, `exit=0`).
2. From 0.2.0: **a requested group whose checks all skipped → `6`**. The old implementation only covered "not a single check ran", not "it ran but everything skipped" — the latter let "K group with zero coverage" count as a pass. To accept that explicitly, use `--allow-degraded` (exit code drops to 0, but `degraded` stays non-empty in the JSON).

> ⚠️ The existing gates in 41 family repos **do not read the exit code** (their workflows use `set +e` / `out="$(…)"` / `set -e`) and only parse the `R0 ` / `K1 ` prefixes on stdout and `results[].name` in the JSON. So 0.2.0's new exit codes **change nothing for those pipelines**; they serve interactive use and future integrators.

- The smoke run keeps its temporary `DSH_HOME`/`DSH_AGENTS_HOME` inside a self-made `%TEMP%` sandbox (prefix `doctor-`, which **does not overlap** the host-protected `%TEMP%\dsh-*` template) and never touches the real `~/.dsh` (red line 3).
- `dsh plugin add` is always passed `--ignore-scripts`: the tested package's install/prepare scripts never execute on the host. A pnpm ignored-builds block is classified as `environment` (it counts neither as a pass nor as a plugin defect).
- Every step's subprocess stdout/stderr is written to `%TEMP%\doctor-run-*\logs\`; at the end the run **quarantines instead of deleting** (renames to `%TEMP%\doctor-quarantine-*`), prints that path in the report tail, and leaves removal to `--purge` after a human confirms (red line 4, the three-stage rule).
- Absolute paths seen at runtime are placeholder-ised to `<path>` before they reach the JSON or the rendered text, so a report can be committed into someone else's repo without tripping its path-leak gate.

## Name collisions (important)

This repository is **`@perrylink/dsh-plugin-doctor`**, and it is **not the same project** as other same-named tools in the ecosystem:

- The bare npm name `dsh-plugin-doctor` belongs to **Xrainsmile/DSH-Plugin-Doctor** (a different project, 0.1.1). So **never run `npx dsh-plugin-doctor`** — that executes someone else's package; always use the scoped full name `@perry