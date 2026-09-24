<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/vshulcz/deja-vu/main/assets/logo-dark.svg">
    <img src="https://raw.githubusercontent.com/vshulcz/deja-vu/main/assets/logo.svg" width="330" alt="deja-vu">
  </picture>
</p>

<p align="center"><b>The one memory your coding agents share, built from the history already on your disk.</b></p>

<p align="center">Your agent is about to re-debug something you fixed in March — in a different agent.
deja indexes the sessions Claude Code, Codex, Cursor and every other agent on this machine
already wrote to disk, and hands the right one back in whichever agent asks.</p>

<p align="center"><img src="https://raw.githubusercontent.com/vshulcz/deja-vu/main/assets/demo.gif" width="720" alt="The same question put to the same agent twice: without memory it has no record of it, with deja it answers with the decision from eight months earlier"></p>

<p align="center"><sub><em>Nobody searched anything — the agent called deja itself. Two genuine runs, a real model and a real tool call, against a synthetic corpus: nobody's history is published.</em></sub></p>

<p align="center"><b>deja starts full: the history 34 agents already wrote, searchable while it indexes, with no model and no capture step.</b></p>

<p align="center">And nobody has to ask for it: recall arrives at session start, on every prompt,
before a file is edited or a command runs, and after one fails. Keys and tokens are stripped as
the index is built; <a href="docs/SECURITY-MODEL.md">the security model</a> says what that catches
and what it cannot.</p>

<p align="center">
<b>88.1% hit@1</b> on LongMemEval-S (470-question cleaned set) &middot; <b>70.5% retrieval hit@1</b> on LoCoMo &middot; <b>millisecond</b> lookups over gigabytes of history<br>
<sub>Both harnesses ship in this repo and run on the public datasets in minutes &middot;
<a href="https://vshulcz.github.io/deja-vu/guide/benchmarks.html">check the numbers yourself</a></sub>
</p>

<p align="center">
  <a href="https://github.com/vshulcz/deja-vu/actions/workflows/ci.yml"><img src="https://github.com/vshulcz/deja-vu/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/vshulcz/deja-vu/releases"><img src="https://img.shields.io/github/v/release/vshulcz/deja-vu" alt="Release"></a>
  <a href="https://mcptoplist.com/server/io.github.vshulcz%2Fdeja-vu"><img src="https://mcptoplist.com/badge/io.github.vshulcz%2Fdeja-vu.svg" alt="MCP Toplist"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
</p>

<p align="center">English | <a href="README.zh.md">中文</a> | <a href="README.ja.md">日本語</a></p>

<p align="center"><a href="https://vshulcz.github.io/deja-vu/">Docs</a> &middot; <a href="https://vshulcz.github.io/deja-vu/guide/benchmarks.html">Benchmarks</a> &middot; <a href="https://vshulcz.github.io/deja-vu/guide/compare.html">How it compares</a> &middot; <a href="docs/INTEGRATING.md">Building it into your tool</a></p>
<p align="center"><sub>Found it useful? <a href="https://github.com/vshulcz/deja-vu">Star deja-vu on GitHub</a>.</sub></p>

## Install

```sh
curl -fsSL https://raw.githubusercontent.com/vshulcz/deja-vu/main/install.sh | sh
deja install --auto
```

<p align="center"><img src="https://raw.githubusercontent.com/vshulcz/deja-vu/main/assets/banner.png" width="700" alt="What deja prints after the first index: the mark, the agents it found, and a query taken from your own history"></p>

Ten seconds to install, about ten to index, and it is useful. The second command wires MCP
recall into every agent it finds, turns on session-start recall where the agent supports
it, and builds the first index so the next session does not pay for it.

Start a new agent session and ask it something you worked on months ago:

> have we dealt with jwt refresh rotation before? check your memory

It does not have to be asked, either — with auto-recall the agent already knows what you
solved in that project when the session opens.

<details>
<summary>Other ways to install, and what to do if you want less than all of it</summary>

`brew install deja-vu`, `go install github.com/vshulcz/deja-vu/cmd/deja@latest`,
or `npx @vshulcz/deja-vu "query"` to try it without installing anything. Desktop apps that
take MCP servers as bundles can open the `.mcpb` from the
[latest release](https://github.com/vshulcz/deja-vu/releases/latest); it carries the binary.

Claude Code, Codex, Cursor, Qwen, OpenClaw and Copilot can take the same plugin bundle from
their own marketplaces instead:

```sh
claude plugin marketplace add vshulcz/deja-vu && claude plugin install deja-vu@deja-vu
```

On Windows the install script exits with `unsupported OS` — it is a shell script. Use
Scoop instead, from the main bucket every Scoop install already has:

```powershell
scoop install deja-vu
```

Or take `deja-vu_<version>_windows_amd64.zip` from the
[latest release](https://github.com/vshulcz/deja-vu/releases/latest) and put `deja.exe` on
your `PATH`, e.g. in `%USERPROFILE%\.local\bin`.

The binary alone is a complete install for searching: index, search, `show`, `ctx`, `blame`,
`--json` and redaction need nothing else. `deja install` is what wires MCP into your agents
and turns on session-start recall — worth having, and optional. On a binary-only setup
`deja doctor` reports every MCP target as `not-wired`, which is that setup working as
intended. `deja warmup` also leaves a skill at `~/.agents/skills/deja-search/SKILL.md`
that teaches an agent the CLI contract — `deja search --json`, `ctx`, `blame`, how to read
`tier` and `total` — so it knows history is searchable without MCP. The copy in the repo is
[`skills/deja-search/SKILL.md`](skills/deja-search/SKILL.md).

`deja install --all` is `--auto` without the session-start recall: agents answer from memory
when they decide to call it, rather than starting each session with it. The
[agent setup guide](https://vshulcz.github.io/deja-vu/guide/agents.html) covers what each
harness supports, aider's read-only context file, and the Windows `cmd /c deja mcp` wrapper.

</details>

<details>
<summary>What gets written into each agent's own guidance file</summary>

Install also writes user-level guidance for the harnesses it detects: Claude Code, Codex, opencode, Gemini CLI, Antigravity, Qwen, Kimi Code, pi, Senpi, Copilot, VS Code Copilot Chat, Cursor, Goose, OpenClaw, Hermes, Roo Code, omp, Amp, prime-agent, DeepSeek Harness, Continue, Crush and Zed each get it in their own guidance file (or under the configured `XDG_CONFIG_HOME`). Re-run rewrites deja's skill or marked block without changing surrounding user content. Use `deja install --all --no-guidance` to opt out; Grok Build gets the shared skill in `~/.agents/skills`, which is what it reads; the `~/.grok/GROK.md` written beside it is for the unrelated community CLI that shares that directory. Cursor has no user-level instructions file, so it gets the shared skill in `~/.agents/skills` — one of the four places Cursor reads skills from — read only when something looks relevant rather than every session.

</details>

## What you get

**Solve it in Codex. Claude remembers.** Thirty-four coding agents write every conversation
to local files, and deja turns those files into one memory layer all of them read.

| | |
| --- | --- |
| **Retroactive search** | `deja "connection pool exhausted"` over gigabytes, including everything from before you installed deja. Natural-language questions fall back to a relevance tier. Time is a hint, not a filter. |
| **Cross-agent recall** | The MCP `deja` tool in `recall` mode answers *"we fixed this three weeks ago"* in whichever agent asks, whoever solved it originally. |
| **It survives compaction** | Measured over 43 compactions: the summary keeps 77% of the decisions and 0.2% of the commands you ran. deja hands back the other 99.8% — and on Claude Code and Codex it captures the ta