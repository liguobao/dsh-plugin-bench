<div align="center">

<img src="docs/assets/logo.svg" alt="local-shell-mcp logo" width="152">

# local-shell-mcp

**A ChatGPT-ready MCP control plane for shell, files, browser automation, file links, and remote machines.**

[![Docs](https://img.shields.io/badge/docs-fwerkor.github.io%2Flocal--shell--mcp-7c3aed?logo=materialformkdocs&logoColor=white)](https://fwerkor.github.io/local-shell-mcp/)
[![CI](https://github.com/fwerkor/local-shell-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/fwerkor/local-shell-mcp/actions/workflows/ci.yml)
[![dsh.so security](https://www.dsh.so/badge/local-shell-mcp.svg)](https://www.dsh.so/artifact/local-shell-mcp)
[![Release](https://img.shields.io/github/v/release/fwerkor/local-shell-mcp?sort=semver)](https://github.com/fwerkor/local-shell-mcp/releases)
[![Python](https://img.shields.io/badge/python-3.11%2B-3776ab?logo=python&logoColor=white)](https://github.com/fwerkor/local-shell-mcp)
[![Docker](https://img.shields.io/badge/docker-ready-2496ed?logo=docker&logoColor=white)](https://github.com/fwerkor/local-shell-mcp/pkgs/container/local-shell-mcp)
[![License](https://img.shields.io/github/license/fwerkor/local-shell-mcp)](LICENSE)

[Documentation](https://fwerkor.github.io/local-shell-mcp/) · [Quickstart](https://fwerkor.github.io/local-shell-mcp/getting-started/quickstart/) · [Runtime choices](https://fwerkor.github.io/local-shell-mcp/guides/deployment/) · [ChatGPT connector](https://fwerkor.github.io/local-shell-mcp/getting-started/chatgpt-connector/) · [DSH plugin](https://fwerkor.github.io/local-shell-mcp/clients/deepseek-harness/) · [Tools](https://fwerkor.github.io/local-shell-mcp/reference/tools/) · [Releases](https://github.com/fwerkor/local-shell-mcp/releases)

</div>

---

`local-shell-mcp` gives ChatGPT Developer Mode and other MCP clients controlled access to a real execution environment. It exposes a dedicated workspace with shell, persistent shell, filesystem, search, patch, Playwright, audit, durable logical sessions with optional Goal plans, public file links, and outbound remote-worker access. Git is handled through ordinary shell commands instead of a parallel wrapper API.

```text
Runtime: Docker / VS Code extension / binary / Python / stdio
  -> exposure: localhost, HTTPS proxy/tunnel, or stdio pipe
  -> client: ChatGPT or another MCP client
  -> controlled workspace at /workspace or configured root
  -> optional remote workers connected over outbound HTTP(S)
```

The intended safety boundary is the container or VM, not the host.

## Why use it

| Capability | What it enables |
|---|---|
| Real terminal access | Run tests, build projects, inspect logs, and debug with persistent shell sessions. |
| Workspace-aware file tools | Read, write, patch, search, and review files under a controlled root. |
| Git workflow support | Run the standard Git CLI through shell tools without a second, incomplete Git abstraction. |
| Browser automation | Extract page text, capture PNG/PDF evidence, or run a full Playwright script. |
| Remote workers | Control NAT, firewall, HPC, NPU, or lab machines that can only connect outward. |
| Agent Skills | Discover, load, and read reusable `SKILL.md` workflows through three fixed tools without changing the MCP tool list. |
| ChatGPT connector support | OAuth 2.1, `/mcp`, discovery controls, and ChatGPT-compatible tool schemas. |
| DeepSeek Harness plugin | Install this repository as a DSH bundle and expose the complete LSM tool surface, including remote workers. |
| ChatGPT Live Workspace | Render a native MCP App for real-time activity, terminal, files, diffs, jobs, remotes, audit, and direct human/agent collaboration inside ChatGPT. |
| Safer operations | Workspace scoping, shell timeouts, output limits, environment filtering, audit logs, and secret scanning. |

## Quick start

Install the official launcher or Python package when you want a host runtime:

```bash
npx local-shell-mcp --help
pipx install local-shell-mcp
lsm --help
```

The npm and Python distributions both expose `local-shell-mcp`; installed packages also expose `lsm` as the short command. The npm distribution is only a verified launcher for the matching standalone release binary, not a second server implementation.

Clone the repository and prepare configuration:

```bash
git clone https://github.com/fwerkor/local-shell-mcp.git
cd local-shell-mcp
cp .env.example .env
```

Set at least these values in `.env`:

```env
LOCAL_SHELL_MCP_PUBLIC_BASE_URL=https://your-public-host.example.com
LOCAL_SHELL_MCP_AUTH_MODE=oauth
LOCAL_SHELL_MCP_OAUTH_ADMIN_PIN=change-me-long-random-pin
LOCAL_SHELL_MCP_OAUTH_JWT_SECRET=change-me-64-hex-random-secret
CLOUDFLARE_TUNNEL_TOKEN=
```

Start the server:

```bash
mkdir -p workspaces/default
docker compose up -d
curl -i http://127.0.0.1:8765/healthz
```

Start the bundled Cloudflare Tunnel sidecar when you need public HTTPS access:

```bash
docker compose --profile tunnel up -d
```

The public MCP endpoint is:

```text
https://your-public-host.example.com/mcp
```

Full setup instructions are in the [documentation](https://fwerkor.github.io/local-shell-mcp/). Runtime choices are documented separately from client connections.

## Human interface

The service includes two compatible human interfaces backed by the same authenticated API and state:

- **Web UI** is a native browser dashboard for system health, machines, workloads, recent MCP activity, and alerts.
- **OpenTUI** is the full terminal-oriented interface with Dashboard, Files, Terminals, Remotes, and Audit screens. It remains available in the browser as a selectable console and as the native `local-shell-mcp tui` command.

Open the browser interface on the service origin:

```text
http://127.0.0.1:8765/ui
```

The OAuth screen lets you choose Web UI or OpenTUI before authorization. After login, switch modes at any time from the interface selector. Native Web UI routes use URL hashes such as `#/overview` and `#/console`, so a selected mode or page can be bookmarked. The OpenTUI console retains the existing authenticated xterm.js/PTY transport, mouse interaction, automatic resizing, reconnects, fullscreen mode, and mobile shortcut row.

Standalone release executables embed the native OpenTUI runtime, while Docker images provide it inside the image. Start the service, then launch it without a human login prompt:

```bash
local-shell-mcp tui
```

Files remains an LSM-native three-pane file manager inside OpenTUI for local and remote machines. It renders bounded PNG/JPEG/GIF/WebP thumbnails and provides consistent file operations through the shared service API. Manual actions entered through either human interface are excluded from the MCP audit log; Activity, Audit, and the terminal audit rail show model-originated MCP activity.

See the [human interface guide](https://fwerkor.github.io/local-shell-mcp/guides/human-interface/).

## ChatGPT setup

For full shell, filesystem, remote-worker, and Playwright tools, use ChatGPT Developer Mode or another full MCP client. ChatGPT is a client connection; choose and start a runtime first.

`session_manage` provides one durable logical task context for agent work. A Session is deliberately independent of machine and working directory: it stores the task objective, semantic progress reports, recent execution Activity, and an optional Plan. `session_id` is the only durable task identity. To continue work in another ChatGPT conversation, the user explicitly passes the existing `session_id`, and the new agent calls `session_manage(action="resume", session_id=...)`. Agents do not list or auto-select Sessions from other conversations. They should report the active `session_id` after start/resume, at meaningful progress checkpoints, and before ending a turn, while using `session_manage(action="report", session_id=...)` for semantic progress rather than copying every tool result into the summary. Ordinary tools receive the same task identity as `logical_session_id`.

When the client 