# DSH Taskboard

English | [简体中文](README.zh.md)

Native, local project task management for DeepSeek Harness. SQLite is the sole task authority. Harness Agent Sessions, Goals, Workspaces, tools, permissions, and the Web Client remain the execution and conversation owners.

This README is written so a human **or another coding agent** can install the plugin into a live Harness profile, verify it, and start using it without guessing.

**Package:** `@shengsheng/dsh-taskboard`  
**Repository:** https://github.com/shengsheng90/DSH-taskboard  
**License:** Apache-2.0  
**Compatible Host:** DeepSeek Harness `0.1.6-alpha.1`

![Native Taskboard board, task detail, and workflow views](docs/assets/taskboard-demo.gif)

If you are an installing agent, jump to [Install into DeepSeek Harness](#install-into-deepseek-harness) and follow every step in order. Do **not** add this Git repository as a raw plugin source: `lib/` is gitignored, so a git install has no compiled Host/Client bundle.

## What you get

After a successful install, Harness gains:

- A **Taskboard** sidebar button and a native overlay page (not an iframe, not a second chat runtime)
- Local SQLite projects, tasks, comments, relations, attachments, workflows, and automation
- Stable readable keys such as `DSH-42` plus opaque ids and optimistic versions
- Seven statuses: `backlog` → `todo` → `in_progress` → `in_review` → `done`, plus `blocked` and `canceled`
- In-process Agent tools `taskboard_*` (no accept / no generic status mutation)
- Headless JSON CLI `dsh-taskboard`
- Packaged Skill `manage-taskboard`

Agents can submit verified work to `in_review`. Only an authenticated human UI or CLI operation can accept it as `done`.

Further design docs: [Architecture](docs/architecture.md), [Security and recovery](docs/security.md), [CLI reference](docs/cli.md), [Acceptance audit](docs/acceptance-audit.md). Attribution shipped to package consumers is in `THIRD_PARTY_NOTICES.md`.

## Requirements

| Requirement | Value |
|---|---|
| Node.js | `^22.19.0` or `>=24.0.0` (24 recommended; built-in `node:sqlite`) |
| pnpm | `11` (`packageManager` is `pnpm@11.15.1`) |
| DeepSeek Harness | `0.1.6-alpha.1` checkout or installation, **web** profile |
| Network | only needed to clone this repo and install Node dependencies |
| Permissions | write access to `$DSH_HOME` (default `~/.dsh`) and the ability to restart the Harness process |

Confirm the toolchain before installing:

```sh
node -v    # v22.19+ or v24+
pnpm -v    # 11.x
```

## Install into DeepSeek Harness

Use these constants. Read live values from disk; do not invent a different package name.

| Name | Value |
|---|---|
| Package name | `@shengsheng/dsh-taskboard` |
| Default profile | `web` |
| Default Web port | `3080` (detect; do not assume) |
| Profile directory | `$DSH_HOME/profiles/<profile>` , usually `~/.dsh/profiles/web` |
| Packed tarball name | `shengsheng-dsh-taskboard-<version>.tgz` |

`<version>` is whatever this repo's `package.json` currently declares — read it there rather than copying a number out of this document. After `pnpm pack`, use the tarball that was actually written.

A longer copy-paste prompt for a Harness-side agent is in [docs/install-plugin-prompt.zh.md](docs/install-plugin-prompt.zh.md). The steps below are the normative English procedure.

### 1. Detect the running Harness

Find the Web listener and its working directory:

```sh
PORT=3080
lsof -iTCP:"$PORT" -sTCP:LISTEN
# then, with the listener PID:
lsof -p <PID> -a -d cwd
```

If nothing is listening on `3080`, search other common ports or ask the operator for the URL they use (`http://127.0.0.1:<port>`).

Decide how to invoke the `dsh` CLI:

- If the Harness cwd is a source checkout (repo root has `pnpm-workspace.yaml` and `package.json` contains a `"dsh"` script), run every later command from that checkout root as `pnpm dsh ...`.
- Else if `command -v dsh` succeeds, use `dsh ...` directly.

In the commands below, `dsh` means whichever of those two forms you just chose. First use of a profile may initialize it and install `@deepseek-ai/dsh-base`.

### 2. Build a packed plugin (required)

`lib/` is not in git. Always build, then pack. Installing the raw git tree or an unbuilt working copy will produce a package without Host/Client output.

```sh
git clone https://github.com/shengsheng90/DSH-taskboard.git
cd DSH-taskboard
pnpm install
pnpm build
pnpm pack
```

Expected artifacts:

- `lib/index.js`, `lib/cli.js`, `lib/client.js` (and sibling declarations)
- `shengsheng-dsh-taskboard-<version>.tgz` in the repo root

Record the absolute tarball path. Example:

```text
/absolute/path/to/DSH-taskboard/shengsheng-dsh-taskboard-<version>.tgz
```

If this repository is already cloned and dependencies are installed, `pnpm build && pnpm pack` is enough. Optional local checks: `pnpm typecheck`, `pnpm test`, `pnpm example`.

### 3. Add the plugin to the profile

The profile directory is a pnpm workspace root (`packages: [.]`). The `-w` / workspace-root flag is **mandatory**. Without it, pnpm fails with `ERR_PNPM_ADDING_TO_ROOT`.

```sh
dsh plugin --profile web add -w /absolute/path/to/shengsheng-dsh-taskboard-<version>.tgz
```

Prefer the packed tarball over the source directory. A source-directory add can miss `lib/` if the tree was not built.

This command may rewrite the profile `package.json`, lockfile, and `node_modules`. That is expected.

Install succeeded only when **all** of the following are true:

1. `$DSH_HOME/profiles/web/package.json` `dependencies` contains `@shengsheng/dsh-taskboard`.
2. The same file's `dsh.profile.bundles` lists `@shengsheng/dsh-taskboard` **after** `@deepseek-ai/dsh-base`.
3. `$DSH_HOME/profiles/web/node_modules/@shengsheng/dsh-taskboard/` exists and contains `lib/` plus `cordis.patch.yml`.

If the CLI warns `declares no dsh.bundle`, the package is missing `"dsh": { "bundle": { "patch": "./cordis.patch.yml" } }` in `package.json`. This repository already declares that; rebuild and reinstall rather than editing the installed copy by hand.

### 4. Verify composition (does not start the server)

```sh
dsh --profile web --dump-config
```

Pass when the dump ends with a `# == @shengsheng/dsh-taskboard` layer and the `taskboard` plugin config (`databasePath`, `attachmentRoot`, worker limits, and the other keys listed in [Configuration](#configuration)).

`--dump-config` idempotently rewrites the profile-root `cordis.yml`. If a sandbox returns `EPERM` while writing `~/.dsh`, ask the operator for full filesystem permission and retry. That rewrite is expected, not a failure.

### 5. Smoke-test module resolution

```sh
cd ~/.dsh/profiles/web && node --input-type=module -e \
  "import('@shengsheng/dsh-taskboard').then(m=>console.log('OK', m.name, typeof m.apply)).catch(e=>{console.error(e.message);process.exit(1)})"
```

Pass: `OK taskboard function`.

Fail is usually a missing peer (`@deepseek-ai/*` or `react`). Those resolve through the install-fallback links under `~/.dsh/profiles/node_modules`, which Harness heals on boot. Re-run step 4, then retry this import.

### 6. See whether the running process already loaded the plugin

Plugin composition and client-module scanning happen **only at boot**. Installing into the profile does not hot-load the UI.

```sh
curl -s http://127.0.0.1:3080/ | grep -c '@shengsheng/dsh-taskboard'
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:3080/plugins/@shengsheng/dsh-taskboard/client.js
```

- Manifest count `> 0` **and** bundle HTTP `200` → already active; skip the restart and go to [Confirm activation](#7-confirm-activation).
- Otherwise restart Harness.

### 7. Restart Harness

Restart stops the process that hosts the current session. Session data lives in `$DSH_HOME/sessions` and is not deleted; in-flight Agent turns are interrupted. Tell the operator before restarting.

From a Harness source checkout, a typical restart is:

```sh
# stop the current listener
OLD_PID=$(lsof -tiTCP:3080 -sTCP:LISTEN | head -1)
