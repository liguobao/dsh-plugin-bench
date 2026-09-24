<h1 align="center">DeepSeek Flow</h1>

<p align="center"><strong>See the workflow. Keep Markdown portable. Review only real canvas edits.</strong></p>

<p align="center">A visual, Markdown-first workflow editor built for the DeepSeek Harness Web UI.</p>

<p align="center"><a href="https://deepseekflow.kanghelyu.org/">🌐 Official website — deepseekflow.kanghelyu.org</a></p>

<p align="center">
  <a href="https://www.npmjs.com/package/deepseek-flow"><img alt="npm version" src="https://img.shields.io/npm/v/deepseek-flow?style=flat-square&amp;logo=npm&amp;logoColor=white&amp;color=CB3837"></a>
  <a href="https://github.com/kanghelyu/dsh-deepseek-flow/releases"><img alt="GitHub release" src="https://img.shields.io/github/v/release/kanghelyu/dsh-deepseek-flow?style=flat-square&amp;logo=github&amp;label=release"></a>
  <a href="https://github.com/deepseek-ai/deepseek-harness"><img alt="DeepSeek Harness Web plugin" src="https://img.shields.io/badge/DeepSeek_Harness-Web_Plugin-4F46E5?style=flat-square"></a>
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/license-MIT-0EA5E9?style=flat-square"></a>
</p>

<p align="center"><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a></p>

DeepSeek Flow turns a `WORKFLOW.md` and its step-level `STEP.md` files into an editable diagram inside DeepSeek Harness. The bundled Skill lets the current Session create and maintain workflows through tools, while the diagram and Markdown remain synchronized and portable.

It is intentionally an editor—not a workflow runtime. DeepSeek Flow helps you design, inspect, and improve a workflow; execution remains in the current Session.

<p align="center">
  <img src="docs/images/engdark.png" width="49%" alt="DeepSeek Flow in dark mode">
  <img src="docs/images/englight.png" width="49%" alt="DeepSeek Flow in light mode">
</p>

## What it gives you

- **Markdown as the source of truth** — one master `WORKFLOW.md`, plus one `STEP.md` workspace for each step.
- **A real visual editor** — create, move, connect, reconnect, label, and delete nodes and arrows.
- **Two-way synchronization** — edits made on the canvas and in the Markdown editor are written back to the workflow files.
- **Source-aware topology transactions** — human canvas edits receive a full current-Session review; topology produced by direct Session file edits can use an invisible deterministic finalize path instead of being sent back to the same Session.
- **Executable gate semantics** — the exported contract includes formulas, operands, predicates, and deterministic Boolean results without running Agent steps.
- **Per-session isolation** — each Harness session keeps its own workflows, with optional shared templates; the canvas toolbar can delete the current workflow or shared template behind a guarded confirm (managed workspaces move to a trash area and can be recovered).
- **Comfortable large-flow navigation** — collapsible and resizable side panels, pan and zoom, fit-to-view, animated node focus, and independent scrolling regions; node drags commit once on pointer release and background sync polls lightweight revisions, so large graphs stay smooth.
- **Native theme support** — the interface follows Harness light and dark themes and the active WebUI language.
- **Manual AI assistance** — run logic validation, optimize one document with review, or optimize the complete workflow.
- **Background AI jobs** — switching documents, views, or sessions does not interrupt accepted jobs; document proposals are restored when you return.
- **Persistent results and drafts** — logic-validation findings, AI proposals, and unapplied canvas drafts are persisted to disk: view switches, session switches, and `dsh web` restarts lose nothing; they are cleared only by an explicit discard or a successful commit. Markdown edits inside the 650 ms autosave window are flushed immediately when you leave the view.
- **I/O and memory safeguards** — unchanged documents are never rewritten (autosaves no longer grind the SSD), assist history and drafts live in separate files, result polling uses single-key queries with failure and duration caps, every background poll is cancellable with no leaks, and subagents get a 10-minute default timeout.
- **A bundled Agent Skill** — installs with the plugin, documents every workflow tool, and includes executable IF/ELSE and Boolean-gate examples.

## Quick start

Install from GitHub into the Web profile:

```bash
dsh plugin --profile web add "github:kanghelyu/dsh-deepseek-flow#main"
```

Restart `dsh web`, open a session, and select the **DeepSeek Flow** tab.

To confirm that the plugin is mounted:

```bash
dsh web --dump-config | grep deepseek-flow
```

## Your first workflow

1. In a Session, ask the Agent to **build a workflow** or **import a workflow**. The bundled `deepseek-flow` Skill guides it to `flow_create` or `flow_put`.
2. Open **DeepSeek Flow**. The plugin scaffolds a master document, step documents, and their visual layout.
3. Ask the Session Agent to change the workflow files, or select a document and edit its Markdown directly.
4. Direct Session/file-driven topology updates are finalized without another main-Session review. The Agent should call `flow_finalize_canvas`; if it forgets, Studio falls back to detecting that no canvas edit event occurred and presses the same invisible finalize action automatically.
5. When **you** add, remove, rename, or connect boxes on the canvas, click **Apply changes**. DeepSeek Flow validates the graph, asks the current Session Agent to review it, validates again, and atomically saves a new revision.
6. Return to the Session when you want the Agent to execute the workflow.

A typical workflow directory looks like this:

```text
my-workflow/
├── WORKFLOW.md
├── 01-input/
│   └── STEP.md
├── 02-research/
│   └── STEP.md
├── 03-quality-check/
│   └── STEP.md
└── 04-output/
    └── STEP.md
```

## Agent tools

| Tool | Purpose |
| --- | --- |
| `flow_create` | Create a documented linear or branched workflow and save it in the current Session. |
| `flow_list` / `flow_read` | Discover workflows and read the master document, step documents, revision, graph, and logic contract. Both also return the session's `activeFlowId`, plus a one-shot `activeFlowNotice` after the user switches the active workflow in Studio — the agent should then run the switched workflow and ignore earlier instructions about other workflows; without a notice, keep the conversation seamless. |
| `flow_put` | Import or atomically update a complete flow definition. A successful call is already persisted. |
| `flow_evaluate` | Evaluate Boolean gates from upstream values without running Agent steps. |
| `flow_finalize_canvas` | After direct file edits, queue Studio's invisible deterministic finalize action and skip a redundant main-Session review. |
| `flow_delete` | Delete a Session flow or shared template; managed workspaces are moved to trash. |

The Skill is registered reactively when the Harness `skills` service becomes available. Its `SKILL.md` contains real Markdown after frontmatter, so filesystem and runtime providers never return an empty instruction body.

## Active workflow & cross-session switching

The Studio toolbar's workflow dropdown lists **every historical workflow**, grouped by origin: current session first, other sessions next, shared templates last. Switching to another session's workflow imports an independent copy of its document workspace into the current session — external custom `docRoot`s are referenced, never copied. Shared templates are also copied into the current session's own managed workspace on switch, so edits never pollute the shared original.

Each session persists an `activeFlowId` (the workflow last used in Studio) inside `sessions/<id>.json`. Reopening Studio auto-selects it, and because both the pointer and the history listing (`dflow/allFlows`) are read straight from disk, the dropdown stays fully populated after a `dsh web` restart o