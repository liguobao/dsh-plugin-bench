<p align="center">
  <img src="docs/logo/logo.svg" width="160" height="160" alt="Mnemon Logo" />
</p>

<h1 align="center">Mnemon</h1>

<p align="center"><strong>English</strong> · <a href="docs/zh/README.md">中文</a></p>

<p align="center">
  <a href="https://www.npmjs.com/package/@mnemon-dev/mnemon"><img alt="npm version" src="https://img.shields.io/npm/v/@mnemon-dev/mnemon?label=npm" /></a>
  <a href="https://github.com/mnemon-dev/mnemon/releases/latest"><img alt="GitHub release" src="https://img.shields.io/github/v/release/mnemon-dev/mnemon" /></a>
  <a href="https://github.com/mnemon-dev/mnemon/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/mnemon-dev/mnemon?label=stars" /></a>
  <a href="https://go.dev/"><img alt="Go 1.24+" src="https://img.shields.io/badge/Go-1.24%2B-00ADD8?logo=go&amp;logoColor=white" /></a>
  <a href="https://github.com/mnemon-dev/mnemon/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/mnemon-dev/mnemon/actions/workflows/ci.yml/badge.svg" /></a>
  <a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-blue.svg" /></a>
</p>

<p align="center"><strong>LLM-supervised persistent memory for AI agents.</strong></p>

---

LLM agents forget everything between sessions. Context compaction drops critical decisions, cross-session knowledge vanishes, and long conversations push early information out of the window.

Mnemon gives your agent persistent, cross-session memory — a four-graph knowledge store with intent-aware recall, importance decay, and automatic deduplication. The `mnemon` memory path remains one local binary with zero API keys and one setup command.

Mnemon ships one executable with two separate surfaces. Memory stays at the
`mnemon` root; [Agency Preview](docs/AGENCY.md) lives at `mnemon agency ...` and adds
durable, project-local responsibility and effect admission to an existing Pi
agent. Agency does not replace Memory or the Agent Runtime.

> **Claude Max / Pro subscriber?** Mnemon works entirely through your existing subscription — no separate API key required. Your LLM subscription *is* the intelligence layer. Two commands and you're done.

### Why Mnemon?

Most memory tools embed their own LLM inside the pipeline. Mnemon takes a different approach: **your host LLM is the supervisor.** The binary handles deterministic computation (storage, graph indexing, search, decay); the LLM makes judgment calls (what to remember, how to link, when to forget). No middleman, no extra inference cost.

| Pattern | LLM Role | Representative |
|---|---|---|
| **LLM-Embedded** | Executor inside the pipeline | Mem0, Letta |
| **File Injection** | None — reads file at session start | Claude Code Memory |
| **MCP Server** | Tool provider via MCP protocol | claude-mem |
| **LLM-Supervised** | External supervisor of a standalone binary | **Mnemon** |

Mnemon also addresses a gap in the protocol stack. MCP standardizes how LLMs discover and invoke tools. ODBC/JDBC standardizes how applications access databases. But how LLMs interact with databases using memory semantics — this layer has no protocol. Mnemon's three primitives — `remember`, `link`, `recall` — form an intent-native protocol: command names map to the LLM's cognitive vocabulary (`remember` not INSERT, `recall` not SELECT), and output is structured JSON with signal transparency rather than raw database rows.

<p align="center">
  <img src="docs/diagrams/llm-supervised-concept.jpg" width="720" alt="LLM-Supervised Architecture — three patterns compared, with Mnemon hooks, protocol boundary, and deterministic memory engine" />
  <br />
  <sub>The LLM-Supervised pattern: hooks drive the lifecycle, the host LLM makes judgment calls, the binary handles deterministic computation.</sub>
</p>

Memory has a **compound interest effect** — the longer it accumulates, the greater its value. LLM engines iterate constantly, skill files cost nearly nothing to write, but memory is a private asset that grows with the user. It is the only component in the agent ecosystem worth deep investment.

<p align="center">
  <img src="docs/diagrams/10-knowledge-graph.jpg" width="720" alt="Knowledge Graph — 87 insights connected by temporal, entity, semantic, and causal edges" />
  <br />
  <sub>A real knowledge graph built by Mnemon — 87 insights, 2150 edges across four graph types.</sub>
</p>

See [Design & Architecture](docs/DESIGN.md) for details.

## Quick Start

### Install

**npm** (recommended; macOS / Linux / Windows, Node.js 22+):

```bash
npm install --global @mnemon-dev/mnemon
```

Upgrade the npm-managed CLI at any time:

```bash
mnemon update
```

The npm package installs the matching native Go executable for the host OS and
CPU. Mnemon's engine remains a single native binary; Node.js is used only by
the npm launcher and package manager.

**Alternative installers**:

```bash
brew install --cask mnemon-dev/tap/mnemon
go install github.com/mnemon-dev/mnemon@latest
```

Homebrew, `go install`, source builds, and other Node package managers must
continue to use their original installation method. To migrate one of these
installations, run the npm install command once and ensure the npm global bin
directory precedes the old executable on `PATH`; subsequent `mnemon update`
calls are npm-managed.

Windows supports the core Memory commands. Agency remains unavailable on
Windows until its local authority boundary has native Windows security.

**From source** (macOS / Linux):

```bash
git clone https://github.com/mnemon-dev/mnemon.git && cd mnemon
make install
```

**Verify installation**:

```bash
mnemon --version
mnemon agency --version
```

### Agency (Preview · Pi-first)

```bash
mnemon agency setup --runtime pi --project-root .
```

Set up each project once, then use Pi normally. Agency is available on macOS
and Linux and remains independent from Memory: `mnemon setup --target pi --yes`
enables Memory, while the command above enables Agency. See the
[Agency guide](docs/AGENCY.md) for its operating model, Preview compatibility
boundary, and optional peers.

### [Claude Code](https://github.com/anthropics/claude-code)

```bash
mnemon setup
```

`mnemon setup` auto-detects Claude Code, then interactively deploys skill, hooks, and behavioral guide. Start a new session — memory just works.

### [Codex](https://github.com/openai/codex)

```bash
mnemon setup --target codex --yes
```

One command deploys the mnemon skill, prompt files, and Codex lifecycle hooks
(`SessionStart`, `UserPromptSubmit`, `Stop`) in `.codex/hooks.json`.

### [Cursor](https://cursor.com/)

```bash
mnemon setup --target cursor --yes
```

One command deploys the mnemon skill, prompt files, and Cursor lifecycle hooks
to `.cursor/`. The integration primes new agent sessions with Mnemon guidance
and memory status, then nudges for durable-memory writeback after responses.

### [ZCode](https://zcode.z.ai/)

```bash
mnemon setup --target zcode --global --yes
```

ZCode installs the Mnemon skill under `~/.zcode/skills/` and registers
user-level lifecycle hooks in `~/.zcode/cli/config.json`. The hooks prime new
sessions, add recall guidance before model calls, and prompt for durable-memory
writeback at stop. Without `--global`, setup installs only the project skill;
ZCode currently ignores project-level hook configuration.

### [MiniMax Code](https://github.com/MiniMax-AI/minimax-code)

```bash
mnemon setup --target minimax-code --yes
```

One command deploys the Mnemon skill to
`.minimax/skills/mnemon/SKILL.md`. Add `--global` to use
`~/.minimax/skills/mnemon/SKILL.md` across projects. Current MiniMax Code
releases discover both roots natively. The integration is intentionally
skill-only: in MiniMax Code 3.0.65, the local Agent V2 path does not dispatch
the user-prompt lifecycle hook required for dependable automatic recall.

### [TRAE](https://www.trae.ai/) (TRAE Work)

```bash
mnemon setup --target trae --yes
```

One command deploys the mnemon skill, 