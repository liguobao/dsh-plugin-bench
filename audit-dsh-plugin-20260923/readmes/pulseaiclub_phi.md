<p align="center">
  <img src="assets/pixel-text-PHI.png" alt="phi" width="220" style="image-rendering: pixelated; image-rendering: crisp-edges;">
</p>

<p align="center">
  <a href="https://discord.gg/UnyHB3tvRk"><img alt="Discord" src="https://img.shields.io/badge/discord-community-5865F2?style=flat-square&logo=discord&logoColor=white" /></a>
  <a href="README.zh-CN.md"><img alt="中文" src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87-58A6FF?style=flat&colorA=222222&colorB=58A6FF" /></a>
  <a href="https://github.com/pulseaiclub/phi/blob/main/LICENSE"><img src="https://img.shields.io/github/license/pulseaiclub/phi?style=flat&colorA=222222&colorB=58A6FF" alt="License"></a>
  <a href="https://github.com/pulseaiclub/phi/actions"><img src="https://img.shields.io/github/actions/workflow/status/pulseaiclub/phi/ci.yml?style=flat&colorA=222222&colorB=3FB950" alt="CI"></a>
  <a href="https://go.dev"><img src="https://img.shields.io/badge/Go-1.26-00ADD8?style=flat&colorA=222222&logo=go&logoColor=white" alt="Go"></a>
  <a href="https://github.com/pulseaiclub/phi/releases"><img src="https://img.shields.io/github/v/release/pulseaiclub/phi?style=flat&colorA=222222&colorB=8957E5" alt="Release"></a>
</p>

A lean, high-performance terminal coding agent harness in Go — a sibling to Pi.

**Docs:** [pulseaiclub.github.io](https://pulseaiclub.github.io/)

- **Fast and small** — ~15 MB release binary, ~21 MB idle RSS, ~31 ms to first frame; no Node / Electron / Python runtime
- **Sub-agents** — spawn isolated jobs and watch the full run unfold in the TUI / job logs, without stuffing every turn into the parent context
- **Hashline edits** — edit by whole-file `@file path#TAG` plus line `LINE#HASH` anchors (same idea as [oh-my-pi](https://github.com/can1357/oh-my-pi)): the model points at anchors instead of rewriting whole files; stale tags/hashes are rejected so over-edits and silent corruption stop here
- **Permission gate** — Gate / Ask before destructive tools fire; safety is not optional when an agent can touch your tree
- **MCP without context death** — configure as many MCP servers as you want; their tool schemas **never** enter the model prompt. The system prompt lists **server names** only (like the Skills catalog); the agent uses three meta-tools (`mcp_list` / `mcp_inspect` / `mcp_call`) to discover and call on demand. Same Gate / Ask / Hooks path as built-in tools. See [MCP](#mcp)
- **Extensions (Go or Rust)** — native binaries speak the **PXB** binary protocol over stdin/stdout; official author SDKs for Go ([`ext/go`](ext/go)) and Rust ([`ext/rust`](ext/rust)): LLM tools, slash commands, event intercepts, confirm dialogs — no reflection; JSON at the SDK edges via `serde_json`. See [Extensions](#extensions)
- **In-TUI diff review** — `/diff` opens a full-screen git review (working tree / staged / HEAD): syntax-highlighted hunks, line notes, then `a` sends notes to the agent. See [Diff review](#diff-review)
- **Any model** — OpenAI-compatible, Anthropic, or Gemini via an explicit `api` field; built-in presets fill endpoint, context window, and capabilities for known model names (GPT, DeepSeek, Gemini, Kimi, GLM). See [Supported models](doc/models.md)

![phi welcome](assets/phi.png)

![phi TUI](assets/image.png)

![phi diff review](assets/diff.png)

- [Docs](https://pulseaiclub.github.io/docs/getting-started/)
- [Quick start](#quick-start)
- [Footprint](#footprint)
- [Configuration](#configuration)
- [Interactive mode](#interactive-mode)
- [Diff review](#diff-review)
- [Code viewer](#code-viewer)
- [Commands](#commands)
- [Sessions](#sessions)
- [Headless mode](#headless-mode)
- [Skills](#skills)
- [Permissions](#permissions)
- [Extensions](#extensions)
- [MCP](#mcp)
- [Tools](#tools)
- [Project layout](doc/project-layout.md)

## Quick start

Install the latest release (macOS / Linux):

```sh
curl -fsSL https://raw.githubusercontent.com/pulseaiclub/phi/main/scripts/install.sh | bash
```

Windows (PowerShell 5.1+):

```powershell
irm https://raw.githubusercontent.com/pulseaiclub/phi/main/scripts/install.ps1 | iex
```

First launch needs a model. Open the config editor (creates `~/.phi` layout
and writes `~/.phi/config.yaml`):

```sh
phi config
```

Or set env vars for a one-off run:

```sh
export PHI_MODEL=gpt-4o
export PHI_API_KEY=sk-...
```

Then start the TUI:

```sh
phi
```

Or build from source (Go 1.26.3+, see `go.mod`):

```sh
make build          # produces ./phi
make install        # build and install into $GOBIN
```

On first start, phi automatically creates `~/.phi/{bin,skills,hooks,session}`. Search
tools (`fd`, `rg`) download into `~/.phi/bin` in the background when missing.

The TUI gives the model four core tools — `read`, `write`, `edit`, and
`bash` — plus `grep`, `find`, and `ls`. The model uses these to
fulfill your requests. External HTTP fetch is available via MCP when configured.

## Footprint

Lean is not enough — phi is built to feel instant and stay cheap under load.
phi numbers are a stripped release build (`CGO_ENABLED=0`, `-ldflags="-s -w"`)
on macOS arm64. Other harnesses use published Linux PSS / interactive PTY
figures.

### Time to first frame

<p align="center">
  <img src="assets/perf-first-frame.png" alt="Time to first frame: phi 0.031s vs other terminal harnesses" width="900">
</p>

### Idle RAM · 1 session

<p align="center">
  <img src="assets/perf-ram-1.png" alt="Idle RAM, 1 session: phi 21.2 MB vs other terminal harnesses" width="900">
</p>

### Idle RAM · 10 sessions

<p align="center">
  <img src="assets/perf-ram-10.png" alt="Idle RAM, 10 sessions: phi 221 MB vs other terminal harnesses" width="900">
</p>

| Metric | phi |
| --- | ---: |
| Release binary | **~15 MB** |
| Idle RSS (1 session) | **~21 MB** |
| 10 idle sessions (total RSS) | **~221 MB** |
| Time to first frame | **~31 ms** (26–49 ms) |
| Cold `go build` (empty `GOCACHE`) | **~5.5 s** |
| Warm rebuild | **~0.7 s** |
| Go source (excl. tests) | **~22k LOC** / 107 files |
| Go packages | **32** |
| Direct module deps | **6** (15 modules total) |
| Linked runtimes | system libs only (no Node / Electron / Python) |

## Configuration

phi reads `~/.phi/config.yaml` (standard YAML). Environment variables
override it for one-off runs. `phi config` opens an HTML editor for the same
file in your browser.

![phi config](assets/config.png)

```yaml
# ~/.phi/config.yaml
models:
  - name: gpt-4o
    api: OpenAI             # OpenAI | OpenAIResponses | Anthropic | Gemini (empty → OpenAI-compatible)
    api_key: sk-...         # or set PHI_API_KEY
    base_url: https://api.openai.com/v1   # default; PHI_BASE_URL overrides
    context_window: 128000  # optional
    default: true           # the model used at startup; first entry wins if absent
  - name: claude-sonnet-4-20250514
    api: Anthropic          # required — no name/URL guessing
    api_key: sk-ant-...
    base_url: https://api.anthropic.com
    context_window: 200000
  - name: deepseek-flash    # built-in preset: base_url / context / thinking filled in
    api_key: sk-...
  - name: gemini-2.5-flash  # built-in preset (api: Gemini)
    api_key: ...
    think_level: high       # optional: off | minimal | low | medium | high | …

skill_path: ~/.phi/skills # where SKILL.md files are loaded from

agents:
  enabled: true           # default; set false to disable agent_* sub-agent tools
  models:                 # optional per-role defaults; omit → inherit parent model
    explore: cheap-model
    review: strong-model
    worker: coding-model

permissions:
  mode: interactive       # interactive | readonly | autopilot | headless-strict
  bash:
    default: ask          # ask | allow | deny
    allow:
      - "go test ./..."
    deny:
      - "rm -rf *"
```

Built-in presets and thinking wire formats: [doc/models.md](doc/models.md).

### Recommended model: DeepSeek Flash

phi + DeepSeek Flash — the best pairing: grounded, low hallucination, cache hit rates near 100%.

Use the built-in preset (only `name` + `api_key` requi