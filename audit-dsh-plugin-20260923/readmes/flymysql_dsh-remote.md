**English** · [中文](./README.zh.md)

---

# dsh-remote

[![npm version](https://img.shields.io/npm/v/dsh-remote)](https://www.npmjs.com/package/dsh-remote)
[![downloads](https://img.shields.io/npm/dw/dsh-remote)](https://www.npmjs.com/package/dsh-remote)
[![downloads](https://img.shields.io/npm/dm/dsh-remote)](https://www.npmjs.com/package/dsh-remote)
[![license](https://img.shields.io/github/license/flymysql/dsh-remote)](LICENSE)
[![dsh-plugin](https://img.shields.io/badge/topic-dsh--plugin-7a3ef3)](https://github.com/topics/dsh-plugin)

Maintained by [@flymysql](https://github.com/flymysql) · [Blog](https://gitpull.cn) · [Discussions](https://github.com/flymysql/dsh-remote/discussions) · [Issues](https://github.com/flymysql/dsh-remote/issues) · [中文说明](./README.zh.md)

![dsh-remote — make any SSH machine a real DSH workspace](docs/cover.png)

**Remote-work assistant for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (DSH).**

Manage several SSH machines, then pick a **remote workspace** (or a **local** one) and let the agent operate right there without leaving the harness — listing files, reading code, running builds & commands over the remote host, and keeping that remote directory mirrored into a real local workspace object.

The harness Web UI intentionally binds `127.0.0.1` (the CLI rejects `--host 0.0.0.0` for safety). This plugin goes the other way: **you connect out** to the machines you maintain, pick a workspace, and work in it through the normal DSH workspace + agent fs flows — no changes to `dsh-workspace` or the harness core.

## Screen previews

Settings → **远程工作区** — a multi-machine SSH registry (add / edit / delete / set-current, password stored locally):

<img src="docs/ui-settings-panel.png" alt="dsh-remote settings — multi-machine registry (light theme, host scrubbed)" width="720"/>

The native **"Add workspace" / "Select workspace"** flow — a centered modal, two tabs, opens on **本机 (local)**; switch to **远程 (remote)**:

- **远程** — a **machine `<select>`**, a path field that **auto-prefills `/` and live-completes** directories (picking one immediately reveals its next level, OS/VSCode-style), plus a **浏览…** floating browser that fills the field without committing — you review, edit, then **设为远程工作区**.

Real capture (host scrubbed to a placeholder):

<img src="docs/ui-picker-panel.png" alt="dsh-remote workspace picker — real dialog; 本机 (local) tab; 远程 machine select + prefilled root path + autocomplete" width="720"/>

---

## Features

- **Multi-machine SSH** — save any number of hosts (`host`/`port`/`user` + **private key** or **password**). Passwords are stored locally and never shown back in the UI. Switch with one click in Settings. Per-machine **passphrase / host-key mode / SSH agent / keyboard-interactive (OTP) / proxy jump (bastion)** and an **optional OS-keychain password** (`加密保存密码` — macOS Keychain / Windows DPAPI / Linux secret-tool).
- **`~/.ssh/config` aliases (resolved live, never copied)** — a machine can be saved as just a **Host alias** (`useSshConfig`): hostname/user/port/key/jump host are read from `~/.ssh/config` **at every connect**, so editing that file takes effect immediately and there is nothing to re-import; the registry stores **no copy** of those values (the key stays a path reference, its content is never read). Full OpenSSH semantics: multi-alias `Host a b`, `*`/`?` wildcards, `!` negation, `Include` (globbed, relative to `~/.ssh`), trailing-`\` continuations and ssh_config(5)'s *first-obtained-value-wins*. In Settings, **Import from ~/.ssh/config** saves an alias in one click (or **Copy fields** materialises a normal machine), the alias list and machine rows show **alias → what it actually resolves to**, and anything the plugin cannot honour (`ProxyJump` with several hops, `ProxyCommand`) is surfaced as a warning instead of silently degrading.
- **Two-tab workspace picker** (fills the native "Add workspace" flow):
  - **本机 / Local** — opens the **native OS folder chooser** over the host (macOS `osascript` / Linux `zenity`→`kdialog` / **Windows `FolderBrowserDialog`**), or lets you type a local path → adopted directly as a normal DSH local workspace.
  - **远程 / Remote** — the picker is a **centered modal**. Pick a **machine** → on Windows hosts the root shows a **"This PC" drive view** (`C:\`, `D:\`, `E:\`… instead of the Git Bash MSYS root) and the path field live **autocompletes** directories (accepts `C:\Users\…` or `/c/Users/…` — Windows paths are rewritten to the Git Bash form underneath); selecting a directory immediately lists its next level. A **浏览…** floating browser (Windows-aware breadcrumb `此电脑 / C:\ / Users / dev`, drive rows, size + mtime, dirs first, follows symlinks) fills the field without committing; the **回上一级** button works at any depth (even when the browser was opened at the path bar's value). **最近 workspaces** quick-pick, **`~` 主目录** shortcut and **新建目录** are one click away. On confirm it creates a **real local mirror** under `$DSH_HOME/remote-workspaces/<host>-<user>-<port>/<base>` that passes `fs.realpath` → the harness adopts it as a real workspace while dsh-remote keeps it synced over SFTP.
- **Git Bash default terminal (Windows remotes)** — the remote platform is auto-detected (`cmd /c ver`, plus an `uname -s` MINGW/MSYS probe as fallback); on Windows the plugin locates Git Bash (`config.shell` can pin a path or `native` disables wrapping) and pipes every command to `bash -s` over the exec channel, so quoting/backslash escaping is never an issue regardless of the SSH default shell. `rw_exec` runs with a Git Bash cwd (`/c/Users/…` form). `/dsh-remote/status`, `rw_info` and the 测试连接 button report the detected platform + shell.
- **Windows path auto-conversion** — typing `C:\Users\dev\project` (or `C:/…`, `/c/…`, `/C:/…`) is normalized underneath to the Git Bash form `/c/Users/dev/project` for shell commands, while workspaces are stored and shown Windows-style (`C:\Users\dev\project`). All model tools accept and report both forms; SFTP access uses the Win32-OpenSSH `/D:/…` form (see `toSftpPath`).
- **Remote `@` completion (issue #39)** — in a remote session `@` lists the **remote** tree (read live over SFTP, not the local mirror): directories drill down, a slash-free query fuzzy-matches the whole tree, and candidates are **workspace-relative paths** (`@src/main.c`) exactly like a local session. The `rw_*` tools accept those relative paths and resolve them against the remote workspace root. The index is bounded (entries/directories/deadline + cache + failure breaker) and **falls back to the local mirror when the host is unreachable** — never a silent empty list. Local sessions are untouched.
- **Bidirectional SFTP sync, conflict-aware** — `rw_sync` (remote → mirror) and `rw_push` (mirror → remote) are **three-way** (remote vs local vs last-synced snapshot): files changed on both sides are **reported as conflicts and never silently overwritten** (`force=true` overrides). Defaults are **depth 8 / 2000 files**; hitting a cap is reported as **`TRUNCATED`**. Both support **dry-run**, **background tasks**, and honor **gitignore-style ignore rules**.
- **Model tools** — 20 tools, all Windows/POSIX portable via SFTP: `rw_info`, `rw_connect` (with `save`), `rw_pick_workspace`, `rw_list_dir` (size+mtime), `rw_stat`, `rw_read_file` (encoding-aware: utf-8/gbk), `rw_write_file`, **`rw_edit`** (literal replace + mtime optimistic lock), `rw_append`, `rw_mkdir`, `rw_remove` (recursive, bounded), `rw_move`, `rw_exec` (pty/env), **`rw_search`** (SFTP tree walk — works on Windows too, honors ignore rules, context lines), `rw_download`/`rw_upload` (streaming fastGet/fastPut + size caps), **`rw_forward`** (SSH tunnels), `rw_sync`, `rw_push`, `rw_disconnect`.
- **Port forwarding panel** — create/start/stop/remove **local** (`127.0.0.1:port → remote`) and **reverse** (`remote → local`) tunnels in the Settings page or via `rw_forward`; definitions persist, auto-restart on reconnect