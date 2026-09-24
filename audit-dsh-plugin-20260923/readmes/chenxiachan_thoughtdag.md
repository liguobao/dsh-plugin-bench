<div align="center">

<img src="public/favicon.svg" width="72" alt="ThoughtDAG logo"/>

# ThoughtDAG

**Find the conversations. Decide what the model sees next.**

![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active_development-6B5CE7)

### [Download ↓](https://chenxiachan.github.io/thoughtdag/#download) · [Website](https://chenxiachan.github.io/thoughtdag/) · [Docs](https://chenxiachan.github.io/thoughtdag/docs/)

[中文](./README_ZH.md) · [DeepSeek Harness plugin](#new--deepseek-harness-available) · [Find past context](#new--pinpoint-the-context-you-need-across-agents) · [Visual app](#want-to-explore-and-shape-the-context-visually) · [How it differs](#how-thoughtdag-differs) · [Session Atlas](#-session-atlas-bring-agent-conversations-onto-the-canvas) · [Research](#-research-why-editable-context-matters) · [Documentation](https://chenxiachan.github.io/thoughtdag/docs/)

</div>

## New · DeepSeek Harness Available!

> ThoughtDAG runs as a view inside the DeepSeek Harness web UI: a 对话 | 思维图 switch above the chat. The canvas is where you decide what the harness sees next; the harness runs the turn.

```bash
dsh plugin --profile web add dsh-thoughtdag
dsh web
```

pnpm 11 holds back versions published within the last 24 hours by default, so on a release day the command above may still install the previous version. To get a release the day it ships, name it: `dsh plugin --profile web add dsh-thoughtdag@<version>`, with the version from the [latest release](https://github.com/chenxiachan/thoughtdag/releases/latest). The same command, with `@latest` or a version, updates an existing install.

- **Session Atlas sees all four agents.** The harness's own sessions sit beside Claude Code, Codex and Pi; open one as a graph and it follows the conversation live.
- **Ask from the canvas.** Pick one of the harness's models, or **DeepSeek Harness · Agent** to run the question as a real harness turn with tools. The answer streams back into the node, and the turn stays in the harness's session log.
- **The wires decide what the harness sees.** Materials, notes and nodes wired into a question arrive as its context; a follow-up at the tail of a mirrored session continues that session.

<img src="docs/harness-plugin-en.gif" alt="ThoughtDAG inside DeepSeek Harness: the 对话 | 思维图 switch above the chat, a question asked on the canvas and answered by a harness model, then a follow-up node growing the graph" width="100%"/>

The plugin bundles the canvas; no other ThoughtDAG install is needed. Requires Node 22.19+ and DeepSeek Harness 0.1.2-rc or later.

## New · Pinpoint the context you need across agents

> Start with a code file, an exact phrase, a URL, or a paper. ThoughtDAG searches your local agent conversations and takes you back to the matching turn.

Try it without installing anything:

```bash
npx thoughtdag why src/lib/api.ts
npx thoughtdag find "a phrase you remember"
```

For regular use, install the CLI and connect its read-only MCP tools:

```bash
npm install -g thoughtdag
thoughtdag setup mcp
```

Your agent can then call `why_check`, `why_file`, `find`, and `recall_turn` directly. Conversations from Claude Code, Codex, DeepSeek Harness, Pi, and ThoughtDAG canvases are indexed together on your machine; the desktop app is not required.

### What it can find

#### Which conversations changed or mentioned this code

```text
$ npx thoughtdag why src/lib/api.ts
why src/lib/api.ts · 12 turns in 6 sessions
claude-code  ✏️ edit  Q: Can the API detect vision support?
             Δ storedProviders → storedProviders, storedVision…
…
```

#### Which conversations discussed this concept

```text
$ npx thoughtdag find "context.committed" --in q
find "context.committed" · 21 turns in 12 sessions
claude-code  Q: …add context.committed to the event contract…
codex        Q: …context.committed is already half implemented…
…
```

#### Which conversations discussed this file, paper, or webpage

```text
$ npx thoughtdag find "arxiv" --in m
find "arxiv" · 1 turn in 1 canvas
thoughtdag   M: …collective intelligence, artificial life · arXiv:2606.26733…
```

Real local results, shortened to the most useful lines.

> **Give agents less irrelevant history. Reduce context-driven hallucinations and wasted tokens. Improve answer accuracy.** The query layer brings back only the matching history; the canvas lets you cut contaminated branches before they shape the next answer.

## Want to explore and shape the context visually?

The full desktop app adds Session Atlas, an editable context canvas, PDF and file readers, model and search connections, clipping, export, and handoff.

```bash
brew install --cask thoughtdag
```

Or use the [download page](https://chenxiachan.github.io/thoughtdag/#download) for macOS, Windows, and Linux.

<div align="center">

<img src="docs/hero-demo-en.gif" alt="ThoughtDAG hero demo: asking from a PDF passage, editing model context by removing an edge, zooming out into a thought map, exporting a backup, and turning scattered agent sessions into persistent project context with Session Atlas" width="100%"/>

<p align="center"><a href="https://www.youtube.com/watch?v=-8BqAyaoNXQ"><img src="https://img.youtube.com/vi/-8BqAyaoNXQ/maxresdefault.jpg" alt="YouTube thumbnail for the ThoughtDAG narrated tour" width="640" /></a></p>

**[▶ The 33-second narrated tour](https://www.youtube.com/watch?v=-8BqAyaoNXQ)**

</div>

## The one rule

> **Wires are the context.** What the model sees is exactly what wires into the node. Editing the graph edits the model's memory.

Many tools put conversations on a canvas. In ThoughtDAG, a wire is not decoration or an execution route. It determines what the model sees next.

## In action

One principle behind every gesture: **the human in the loop, the model on the wires**. No autonomous agent redraws your graph.

<table>
<tr>
<td width="45%"><img src="docs/illus/prune-en.svg" alt="Illustration: the research chain wired to a summary node, with the edge to a dinner node cut into a red dashed line"/></td>
<td width="55%">

### ✂️ Delete one edge, get a different answer

The model sees only what wires in. Delete the noise edge, ask again, and the same prompt returns a clean answer. **Reproduce it in chapter ③ of the example canvas.**

</td>
</tr>
</table>

<table>
<tr>
<td width="55%">

### 📖 Read a paper into a map

Select a passage, ask right there. The answer lands on the canvas with its page number, and the p.N chip jumps back to the page. **Finish the paper, and the map is drawn.**

</td>
<td width="45%"><img src="docs/illus/reading-en.svg" alt="Illustration: a passage selected on the original page, a purple ask bubble beside it, the paragraph tagged p.3"/></td>
</tr>
</table>

<table>
<tr>
<td width="45%"><img src="docs/illus/map-en.svg" alt="Illustration: three takeaway plaques with ruled-out, decided and pivoted badges, linked by dashed lines"/></td>
<td width="55%">

### 💎 Condense, zoom out, and export the shape

Merge nodes into a higher conclusion; weave highlights into cited prose. Zoom through full cards, takeaway plaques and an icon skeleton. Then export the current structure as a light or dark Thought Map.

</td>
</tr>
</table>

<table>
<tr>
<td width="55%">

### 🧭 Session Atlas: bring agent conversations onto the canvas

Bring work scattered across different agents into one editable context graph. Continue from any node, then bring the new work back to where the thought began.

*Currently supports local Claude Code, Codex, DeepSeek Harness, and Pi sessions, with more agent integrations in development. Source sessions remain read-only.*

</td>
<td width="45%"><img src="docs/illus/atlas-en.svg" alt="Illustration: local Codex and Claude Code sessions grouped by project, opened as a context graph, then continued in a fresh CLI session"/></td>
</tr>
</table>

## How ThoughtDAG differs

Many products use nodes and edges, but the graph does a different job in each category.

| 