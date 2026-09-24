# AgentShim

English | [简体中文](README.zh-CN.md)

AgentShim gives coding agents a small, focused set of tools for working with source code. Codex and Cursor connect to its local stdio MCP server; DSH uses the native adapter in this repository. The server treats the directory you start it in as the repository root and provides first-class Windows x86-64 support with compatibility releases for Linux and macOS.

## Why use it

- **Predictable file access.** `read`, `grep`, and `glob` use unrestricted scope by default for compatibility; opt into `--read-scope normal` when repository/skill/plugin boundaries are required. This read scope does not constrain spawned processes.
- **Managed long-running Bash.** `run_program` takes one executable and literal arguments. `bash` handles POSIX composition and can detach work under an instance-bound `job_id`; `bash_status` reports lifecycle, primary exit status, and a bounded log tail, while `bash` can terminate the complete owned tree.
- **Cross-platform.** Full support for Windows x86-64, with compatibility release assets for Linux x86-64, Linux ARM64, and macOS Apple Silicon.
- **Reads structured documents.** `read` returns PDF page text or rendered images and Markdown for DOCX, XLSX, PPTX, DOC, XLS, and PPT, with continuation cursors for long documents.

## Tools

| Tool | Description |
| --- | --- |
| `read` | Read source files with line numbers. Supports UTF-8, BOM-detected UTF-16, WHATWG encoding labels, PDFs, and six Office formats. |
| `grep` | Search file contents with Rust regex or literal strings. |
| `glob` | Find files. Gitignored files are included by default; `.git` and common large directories stay excluded. |
| `run_program` | Run one program with a literal argument list, without a shell. |
| `bash` | Run a POSIX bash command line and return merged stdout and stderr. |
| `bash_status` | Inspect one detached Bash job and its bounded log tail. |

## Install

**Windows (PowerShell):**

```powershell
irm https://github.com/possible055/agentshim/releases/latest/download/install.ps1 | iex
```

Installs to `%LOCALAPPDATA%\agentshim\bin\agentshim.exe` (e.g. `C:\Users\<user>\AppData\Local\agentshim\bin\agentshim.exe`).

**Linux / macOS:**

```sh
curl -fsSL https://github.com/possible055/agentshim/releases/latest/download/install.sh | sh
```

Installs to `${XDG_DATA_HOME:-$HOME/.local/share}/agentshim/bin/agentshim` (e.g. `~/.local/share/agentshim/bin/agentshim`).

Re-run the same command to update. Install a specific version with `-Version` (PowerShell) or `--version` (sh).

**Build from source** (requires Rust 1.88):

```console
cargo build --release --locked
```

The binary is at `target/release/agentshim` (Linux and macOS) or `target/release/agentshim.exe` (Windows).

An existing `codexshim` installation is not removed or overwritten. After installing AgentShim, update each client to the new executable and MCP server name, verify the six tools, and then remove the old installation if it is no longer needed.

## Configure Codex

Copy the matching example into `~/.codex/config.toml` (user-level) or a project's `.codex/config.toml`, then replace `command` with the absolute path to your `agentshim` binary:

- [Windows example](config/codex.windows.toml.example)
- [Linux example](config/codex.linux.toml.example)
- [macOS example](config/codex.macos.toml.example)

```toml
[mcp_servers.agentshim]
required = true
command = "/absolute/path/to/agentshim"
args = ["serve", "--client-profile", "codex"]
# Unrestricted mode (default) allows any absolute read/grep/glob path. To
# restrict to repository and Codex skill/plugin paths, use:
# args = ["serve", "--client-profile", "codex", "--read-scope", "normal"]
supports_parallel_tool_calls = true
tool_timeout_sec = 600
enabled_tools = ["read", "grep", "glob", "run_program", "bash", "bash_status"]
default_tools_approval_mode = "approve"
env = { CODEX_MCP_PROTOCOL_VERSION = "2026-07-28" }

[features]
mcp_2026_07_28 = true
```

## Configure Cursor

Copy the [Cursor example](config/cursor.mcp.json.example) to `~/.cursor/mcp.json`, replace `command` with the absolute path to the binary, and restart Cursor:

```json
{
  "mcpServers": {
    "agentshim": {
      "type": "stdio",
      "command": "/absolute/path/to/agentshim",
      "args": ["serve", "--client-profile", "cursor"]
    }
  }
}
```

On Windows, JSON paths must escape each backslash.

## Configure DSH

Install the native adapter and its exact optional platform package into your target DSH profile (e.g. `web` for Web UI, `headless` for CLI):

```sh
dsh plugin --profile web add dsh-agentshim
dsh web --dump-config
```

DSH loads `agentshim-core` through the platform addon in-process; it does not start the MCP server or require an installed `agentshim` executable. Unsupported platforms, missing packages, and native API mismatches fail plugin activation. See the [DSH adapter guide](adapters/dsh/README.md) for configuration, capture retention, sandbox approval behavior, and removal.

## Options

### `--client-profile`

Selects the aggregate burst policy. These layers are separate limits, not a single cap:

| Layer | Value | Meaning |
| --- | ---: | --- |
| Codex per-item truncation | 10,000 tokens or bytes | Client history cap after `Wall time:` / `Output:` |
| Server content ceiling | 9,872 | 10,000 minus 128 wrapper tokens |
| Per-call ceiling | 8,192 | Both profiles; a single page cannot exceed this currently |
| Burst aggregate | profile default | Remaining budget split across in-flight calls |

| Value | Per-call token ceiling | Default burst tokens |
| --- | ---: | ---: |
| `codex` (default) | 8,192 | 16,384 |
| `cursor` | 8,192 | 32,768 |

`AGENTSHIM_IDLE_TIMEOUT` enables idle shutdown for the `codex` profile. The `cursor` profile always disables the watchdog, but setting an invalid value still fails startup.

### `--read-scope`

Controls which paths `read`, `grep`, and `glob` may access outside the repository:

| Value | Behavior |
| --- | --- |
| `unrestricted` (default) | Any absolute path readable by the server user. |
| `normal` | Repository paths plus Codex skill/plugin directories. Credentials and history under `.codex` stay inaccessible. |

```toml
args = ["serve", "--read-scope", "normal"]
```

`--read-scope` only bounds `read`, `grep`, and `glob`. MCP process tools deliberately remain unrestricted and inherit the filesystem access of the server user; agentshim does not add a process sandbox.

The DSH adapter uses the official DSH `ctx.sandbox` and `ctx.sandboxPolicy` services when they are composed. It passes the prepared, exact argv through that service and never substitutes a second sandbox provider or silently retries an unconfined command after confinement fails.

The versioned cross-adapter contract is [`contracts/tool-contract-v1.json`](contracts/tool-contract-v1.json). The generator also checks in the MCP JSON-Schema projection and DSH parameter/output projection under [`contracts/generated/`](contracts/generated/). Validate every projection with `python3 scripts/generate-contracts.py --check`. MCP keeps legacy error classes in `error.code`; classes with a v1 mapping are normalized in `error.canonicalCode`, while unmapped legacy classes retain their class name.

### Long-running work

`bash` accepts `detach` with a `log_path` inside the repository. Output goes to that file and the call returns an opaque instance-bound `job_id`, plus the diagnostic pid and log path:

```json
{ "command": "cargo test > /dev/null; echo EXIT=$?", "detach": true, "log_path": "local/test.log" }
```

Use `bash_status` for an immediate state/exit snapshot and a bounded tail (`tail_bytes: 0` returns metadata only):

```json
{ "job_id": "bash-550e8400-e29b-41d4-a716-446655440000", "tail_bytes": 8192 }
```

Terminate the complete server-owned tree through `bash` itself:

```json
{ "action": "terminate", "job_id": "bash-550e8400-e29b-41d4-a716-446655440000" }
```

Up to 16 detached trees may be active. `timeout_ms` is measured f