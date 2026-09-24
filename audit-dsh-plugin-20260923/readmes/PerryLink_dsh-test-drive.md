<div align="center">

# 🧪 dsh-test-drive
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-test-drive` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-test-drive)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-test-drive?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-test-drive?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-test-drive/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-test-drive)

**Isolated install-and-smoke test drives for DeepSeek Harness plugins.**

*Install, smoke, verify, and clean up in a throwaway profile — your real `~/.dsh` stays untouched.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-test-drive.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-test-drive/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-test-drive/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-test-drive?label=version)](https://github.com/PerryLink/dsh-test-drive/releases)
[![npm version](https://img.shields.io/npm/v/dsh-test-drive)](https://www.npmjs.com/package/dsh-test-drive)
[![npm downloads](https://img.shields.io/npm/dm/dsh-test-drive)](https://www.npmjs.com/package/dsh-test-drive)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Component | Version |
|---|---|
| DeepSeek Harness | **`dsh-v0.1.5-rc.2`** (GitHub tag, verified 2026-09-11: full gate chain + profile install smoke). npm dependency lines `0.1.2-rc.1` and `0.1.5-rc.2` (peer dependencies `>=0.1.2-rc.1 <0.2.0 || >=0.1.5-alpha.1 <0.2.0`) |
| Node.js | `^22.19.0 \|\| >=24.0.0` |
| Package manager | `pnpm@11.7.0` |
| Platform | Windows / macOS / Linux (host-only plugin) |
| External tools | `dsh` CLI on PATH (auto-detected, npm shims parsed), `pnpm` on PATH |

## What you get

- `test_drive` tool — one target through the complete pipeline: `dsh plugin add` → `--dump-config` patch check → headless boot smoke (FAILED-marker scan + optional one-shot task) → optional capability assertion → `dsh plugin remove` → quarantined cleanup. Returns the structured record synchronously, or `{ kind: 'background', jobId }` with `background: true`.
- `/testdrive` command — batch drive of a whitespace/comma-separated target list as a `drive-batch` background job over `ctx.jobs`, producing a matrix report (JSON + Markdown).
- `drive_report` tool — fetch any stored run (`tdr_...`), matrix (`tdm_...`), or the latest matrix; rendered as Markdown.
- Capability assertion — beyond "booted and exited": the optional `capability` stage drives one headless task that calls a named tool (or runs a `/command`) and verifies the durable session log recorded the invocation and the observed output contains `expect`. A clean boot is only a smoke test; `observed` proves a named capability really works.
- Structured results — every record carries the discriminator `schema: "dsh-test-drive/v1"` with first-class fields: `stages.install.status` (`pass`/`fail`), `stages.smoke.status` (`pass`/`fail`/`boot-ok`/`skipped`), `stages.capability.status` (`observed`/`invoked`/`not-registered`/`skipped`/`failed`), per-stage `durationMs`, sanitized `summary`/`outputTail`, and an overall `verdict` (`pass`/`fail`/`partial`/`unknown`). This is the machine-readable contract downstream scorers (dsh-score) consume.
- Safety by construction — every temp directory is created by this plugin under a dedicated `dsh-test-drive-` prefix, tracked in a live ownership registry, and removed only through a dry-run → quarantine-rename → delete ladder. The host profile is never read or written.

## Quick start

### Git channel

```sh
dsh plugin --profile web add github:PerryLink/dsh-test-drive#<commit-sha>
```

The first `add` fails because pnpm blocks the package's `prepare` build; copy the exact key pnpm printed into the profile's `pnpm-workspace.yaml` and re-run:

```yaml
allowBuilds:
  'dsh-test-drive': true
```

### npm channel

```sh
dsh plugin --profile web add dsh-test-drive
```

Prebuilt packages need no build allowance. Restart the profile, then use `test_drive` / `/testdrive` from a session.

## Install & uninstall

```sh
dsh plugin --profile web add dsh-test-drive     # install (npm) — or the git form above
dsh plugin --profile web remove dsh-test-drive  # uninstall
```

## Configuration

All keys are optional (defaults shown); invalid values fail loudly at load.

| Key | Default | Description |
|---|---|---|
| `profileName` | `headless` | Profile template initialized inside each throwaway DSH_HOME (base + headless bundles). |
| `dshBin` | `""` | Absolute dsh executable override; empty auto-detects `dsh` on PATH. |
| `headlessTask` | `"Reply with exactly: ok"` | One-shot task for the boot-smoke stage; empty skips the stage. |
| `forwardEnv` | `[]` | Environment VARIABLE NAMES (never values) forwarded into test-profile child processes. |
| `allowBuilds` | `true` | Allowlist a blocked git `prepare` build in the test profile and retry the install once. |
| `installTimeoutMs` | `600000` | `dsh plugin add` stage deadline. |
| `configTimeoutMs` | `60000` | `--dump-config` stage deadline. |
| `smokeTimeoutMs` | `300000` | Headless boot-smoke stage deadline. |
| `capabilityTimeoutMs` | `300000` | Capability-assertion task deadline. |
| `capability.enabled` | `false` | Run the capability-assertion stage (registered → invoked → observed). |
| `capability.kind` | `tool` | What to assert: `tool` or `command`. |
| `capability.name` | `""` | Tool or command name (no leading `/`). |
| `capability.args` | `""` | Invocation text: tool arguments (JSON-ish) or command words. |
| `capability.expect` | `""` | Literal expected in the observed output (case-insensitive substring). |
| `uninstallTimeoutMs` | `120000` | `dsh plugin remove` stage deadline. |
| `outputTailBytes` | `8000` | Cap on the sanitized output tail recorded per stage. |
| `keepTempDirs` | `false` | Keep temp dirs on failure for forensics (ownership is dropped; you clean up). |
| `maxBatchTargets` | `20` | `/testdrive` batch cap. |
| `batchConcurrency` | `1` | Batch concurrency (serial avoids pnpm-store contention). |

## Tools & surfaces

### `test_drive`

```
test_drive(target: string, headlessTask?: string, background?: boolean,
           capability?: { kind: 'tool' | 'command', name: string,
                          args: string, expect: string })
```

- `target` — git spec (`github:owner/repo#sha`, `git+https://...`), npm name, local path, or `.tgz` tarball.
- `capability` — assertion after the boot smoke: the agent calls `name` (tool) or runs `/name` (command) with `args`; the stage reads the durable session log and requires the observed output to contain `expect`. Needs `DEEPSEEK_API_KEY` (host env or `forwardEnv`); without it the stage is `skipped`, never failed.
- Returns the full structured record; see the sample below.
- `background: true` starts a `drive-batch` job and returns its id.

### `/testdrive <targets...>`

Starts one background batch job; progress streams through the job output, and the final line names the matrix id for `drive_report`.

### `drive_report(id?)`

Returns a run record (`tdr_...`), a matrix (`t