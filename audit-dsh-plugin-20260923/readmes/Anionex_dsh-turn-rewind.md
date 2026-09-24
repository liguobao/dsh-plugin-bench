# DSH Turn Rewind

[![X (Twitter)](https://img.shields.io/badge/-@anion__ex-000000?style=flat-square&logo=x&logoColor=white)](https://x.com/anion_ex)

[中文说明](README.zh.md)

Message-anchored project-file recovery for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness), with an option to restart from the restored request.

**Turn Rewind** is the user-facing feature, repository, and Profile Bundle name. **Change Ledger** is the durable restore engine underneath it: the `ctx.changeLedger` service, on-disk format, and storage path keep that name because they describe the reusable snapshot and recovery layer rather than the Web action alone.

Change Ledger gives a DSH session an explicit safety boundary around workspace mutations:

```text
create restore point
        ↓
agent / user / external tools modify the worktree
        ↓
preview exact path-level drift
        ↓
review a full or selective restore plan
        ↓
press the final restore button in the rewind dialog
        ↓
create rescue point → restore → verify
```

It never commits, stashes, resets, switches branches, edits the Git index, or decides automatically that a change should be reverted.

## What's new

Most recent work first:

- **File rewind works in ordinary directories (0.3.0)** — when the working directory is not a Git repository it is snapshotted as an ordinary directory (`.git` and `node_modules` excluded by default, plus an optional `.dsh-rewindignore`), so messages-only rewind is no longer the only option.
- **The fastest path is now the default (0.3.8)** — the new `auto` mode uses Git-native checkpoints in a Git worktree (reusing the repository object database, so committed content is never stored twice) and the plugin's own store for ordinary directories.
- **Unchanged files are no longer re-read (0.3.5)** — each workspace keeps a persistent path identity cache; a measured 20 000-file / 351 MB workspace dropped from 237 s to about 7 s per capture.
- **One oversized file no longer discards a whole checkpoint (0.3.3)** — it is skipped and reported while the rest is still captured, and a restore never touches a path its checkpoint did not record, so a file that was too large then and small now is never deleted.
- **Checkpoint budget 5 s → 60 s, parallel capture (0.3.4)** — a 5-second budget in a large directory could only ever report a skip.
- **Rewind button and messages-only fixes (0.2.2 / 0.2.3)** — adapted to the DSH 0.1.2-alpha client hooks and restored the messages-only mode that the Host rejected.
- **Settings card matches the official cards (0.3.6 / 0.3.7)** — one collapsed row that expands, consistent with every other plugin card.

## Preview

Rewind appears as an icon-only third action under each user message, after its timestamp and native Copy action:

![Turn Rewind action under a user message](docs/assets/turn-rewind-action.png)

Opening it shows the affected files and offers three choices: restore the files and restart from before that message, restore only the files, or rewind only the messages and leave the files untouched:

![Turn Rewind review dialog](docs/assets/turn-rewind-dialog.png)

## Why it has a Change Ledger engine

A diff button can show current changes, but it does not own a durable restore lifecycle. Change Ledger owns:

- content-addressed restore-point manifests;
- Git worktree, HEAD, branch, and in-progress-operation fences;
- stale-plan detection between review and mutation;
- exact two-step confirmation plus DSH human approval;
- automatic pre-restore rescue points;
- post-restore hash verification;
- rollback after a failed restore;
- startup reconciliation of interrupted restore journals;
- a public `ctx.changeLedger` service that other plugins can consume.

The durable format is documented in [docs/FORMAT.md](docs/FORMAT.md). The security and failure model is documented in [SECURITY.md](SECURITY.md).

## Safety contract

- **Explicit only:** nothing is restored automatically — every restore starts from the user pressing the final button in the Web dialog, or from an explicit call through the service API.
- **Read before write:** the dialog preview generates an expiring, session-bound plan from the current tree and changes no files.
- **Human gate:** the dialog's reviewed impact plus the final restore button is the human decision; direct mutation requests without a live session-bound plan pair fail closed.
- **Rescue before mutation:** every restore captures the current eligible tree as a durable rescue point before changing a path.
- **No silent omission:** unsupported submodules, sparse checkouts, oversized files, aggregate limits, and unsupported file types fail point creation.
- **No path escape:** every durable path is canonical and workspace-relative; restore refuses symlink parents and non-empty directory replacement.
- **No stale overwrite:** selected paths and the reviewed HEAD/branch/operation fence are checked again at apply time. Any relevant post-review change invalidates the plan.
- **No Git control-plane mutation:** the index, branch, HEAD, stash, and commits remain untouched.

## Scope

Two workspace kinds are supported and selected from the Session's own directory:

**Normal Git worktree**

- tracked files, including currently missing tracked paths;
- untracked files not excluded by `.gitignore` or other standard Git excludes;
- regular files, binary or text;
- symbolic links;
- executable and other portable permission bits.

**Ordinary directory (the Session directory is not a Git repository)**

- every regular file and symbolic link below it; links are captured as links and never followed;
- `.git` and `node_modules` are excluded by default;
- an optional `.dsh-rewindignore` in the directory root adds `.gitignore`-style rules; the built-in exclusions are applied last and cannot be re-included;
- snapshot content is stored in the plugin's own content-addressed storage instead of the Git object database;
- running `git init` inside the directory changes the workspace mode, so earlier restore points stop applying (`WORKSPACE_MODE_CHANGED`) and a new message must create a new one.

The following are rejected or deliberately outside the snapshot:

- sparse checkouts;
- submodule gitlinks (create a restore point inside each submodule instead);
- ignored files and files excluded by `.dsh-rewindignore`;
- special files, sockets, devices, and named pipes;
- extended attributes, ACLs, ownership, timestamps, and hard-link topology;
- the Git index and repository metadata.

If an ignored or otherwise unmanaged file occupies a path that restoration would replace, the restore fails rather than deleting it.

## Install

Build the checked-out plugin, then add it to each DSH profile that should expose the service:

```sh
pnpm install --frozen-lockfile
pnpm run check

dsh plugin --profile web add @anionex/dsh-turn-rewind
dsh plugin --profile headless add @anionex/dsh-turn-rewind

dsh --profile web --dump-config | grep turn-rewind
```

Restart a running profile after changing its bundle list.

The package is a DSH Profile Bundle. `package.json` declares `dsh.bundle.patch`, and `cordis.patch.yml` mounts `@anionex/dsh-turn-rewind` without a DSH core patch.

When the profile also provides the DSH Agent service, the plugin captures a hidden checkpoint in the first `agent/pre-step` waterfall before the Agent processes the opening user message. Capture failures are reported but do not reject the user's turn; the corresponding message simply has no usable rewind point. In Web profiles, the same-origin `/turn-rewind` endpoint resolves the selected `user/message` sequence, exposes a paged file preview, mints a short-lived session-bound restore plan, and delegates child creation to DSH's official Host create/fork lifecycle. It never restores files automatically.

## User flow

In the Web profile, each direct user message gains a compact, icon-only **Rewind** action after its timestamp and native Copy control. The tooltip reads “Return to 