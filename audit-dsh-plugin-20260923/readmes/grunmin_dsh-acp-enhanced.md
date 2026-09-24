**[中文](README-zh.md) | English**

# dsh-acp-enhanced

An enhanced [Agent Client Protocol](https://agentclientprotocol.com) (ACP) server for
[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (dsh), built for ACP
editors like **Zed**. It is a drop-in replacement for the official `@deepseek-ai/dsh-acp`
bridge: the official bridge only streams plain text, this one exposes the Web GUI's
capabilities — streaming, telemetry, model/permission control, session management, MCP —
over the ACP wire.

## Features

### Output & telemetry

- **Block + reasoning streaming**: text blocks and the model's thinking arrive live
  (`agent_message_chunk` / `agent_thought_chunk`); cancelled/retried attempts never leak
  torn output. Set `streamDeltas: true` on the acp-enhanced row for token-level
  streaming instead — the reply renders while the model writes it, coalesced on a 75 ms
  timer; the trade-off is that a mid-block retry can no longer hide its abandoned
  partial text, so a visible `_[stream interrupted — retrying]_` marker separates the
  seam (off by default)
- **Full telemetry**: context usage ring plus cache hit rate / TPS / input-output-reasoning
  tokens / tool timing / turn counts (`usage_update._meta` carries the full breakdown)
- **Image support (multimodal)**: when the dsh composition mounts an attachment store
  (`dsh-attachment-local`, mounted by default in `dsh-base`), `promptCapabilities.image`
  is advertised and pasted/uploaded images are ingested into the harness's durable attachment
  store — a vision-capable model (e.g. `deepseek-v4-flash-vision-exp`) reads them natively,
  in wire order with surrounding text. Older stacks (no attachment store) automatically
  downgrade: image is not advertised and an image prompt is refused with a clear error.

### Model & permissions

- **Model switching**: live `provider/model` catalog dropdown (ACP grouped-select wire shape)
- **Reasoning effort**: `reasoning_effort` dropdown — only when the routed model exposes
  selectable efforts; each model remembers the effort it last used (persisted per profile),
  so switching back restores it, and a first-time model falls back to its own default — or
  its first offered effort — instead of an empty "unknown" selection
- **Permission presets**: read-only / workspace-write / full-access session modes
- **Approval**: native allow-once / reject-once prompts per tool call
- **Agent presets**: per-session model-facing composition (tools + prompt sections)
  from the dsh agent-presets roster. `standard` is the full coding agent (default),
  `minimal` (极简模式) is a bare shell + files editor with **no** subagent/web/todo/plan
  tools — nothing from the host layer leaks into a minimal agent; `code` and `cordis`
  ship alongside, and your own presets under `~/.dsh/.agent-presets` appear too.
  Choose via the `agent_preset` config option, the `/preset` command, or the
  `DSH_ACP_PRESET` env var (per-session default); switching is only allowed while the
  session is still blank (no turn has run), so history never straddles two tool sets.

### Zed deep integration

- **Tool cards**: one-line summary in the collapsed header — `Read <path>`, the
  model's own intent line for shell commands (`description`, Codex-style — the
  exact command stays one click away), `Search: <pattern>`, `Fetch: <url>`, etc.
  The card body follows the ACP best practice: file edits render as a real
  **diff**, **bash/pwsh commands as a real terminal card** (codex-acp wire
  shape: command line + output + exit pill inside a terminal panel — no more
  raw-JSON cards), other executors as a syntax-highlighted code block, and
  touched files as **clickable locations** that open the file — with `rawInput`
  / `rawOutput` kept one click away for transparency, plus per-kind icons and a
  proper in-progress → completed/failed status lifecycle
- **Zed files & terminal**: `zed_read_text_file` / `zed_write_text_file` / `zed_terminal`
  put file edits into Zed's "edited files" area (diff + accept/reject) and commands into a
  real Zed terminal
- **Native form questions**: `ask_user_question` → `elicitation/create` form, click an
  option — or type a custom answer when none of them fit: options render with their
  descriptions, each option-backed question gets a free-text "Custom answer" field, and a
  custom answer replaces the single selection / accompanies a multi-select (same semantics
  as dsh's native question card)
- **Plan panel**: plan mode toggle → "planning" status bar in Zed

### Sessions

- **Resume & archive**: `session/load` restores past threads (full replay); `session/list`
  lists the thread archive (titled, sorted by last activity); `session/close` drops the
  in-memory record so a later `session/load` resumes from the persisted log; live title
  updates. `session/delete` is deliberately **not** advertised — the harness declares no
  public persistence delete (see [Compatibility](#compatibility))
- **Multi-root workspaces**: `sessionCapabilities.additionalDirectories` is advertised,
  so Zed no longer shows "this agent doesn't currently support multi-root workspaces"
  and instead passes every workspace root on `session/new` / `session/load`. All roots
  are described to the model in the system prompt and reported on `session/list`; the
  sandbox keeps the primary `cwd` as its single writable root (see Known limitations)

### Commands

- **Slash commands**: typing `/` reveals the command list (`available_commands_update`):
  `/status` shows the route and telemetry, `/model` lists or switches the model, `/preset`
  lists or switches the agent preset (listings render as monospace code blocks — readable
  at a glance), everything else (`/compact` `/goal` `/permission` `/plan`…) runs straight
  through the harness command registry — all executed **without a model turn**. Every
  user-invocable skill is advertised as a command too, so `/ask-matt`, `/code-review`,
  `/tdd`, … reach the bridge instead of being rejected by the editor, and the skill's
  instructions are injected into the message (dsh-tool-skill-style user invocation).
  Images pasted next to a slash line ride along as command attachments (e.g. reference
  screenshots for a `/goal` objective), the same way the Web composer submits them

### MCP

- **MCP servers**: `session/new` `mcpServers` mount any MCP server (stdio + streamable
  HTTP); tools join as `mcp__<server>__<tool>`; a failing server never takes the session
  down

## Preview

After picking **dsh-acp-enhanced** in Zed's AI Agent panel:

<img src="assets/screenshots/approval-config-context.png" width="560">

<img src="assets/screenshots/tool-cards-elicitation.png" width="560">

## Quick start

**Requires `dsh ≥ 0.1.5-rc.2`** (`npm install -g @deepseek-ai/dsh@0.1.5-rc.2`); the bridge
targets one declared harness API line and does not probe older generations at runtime.

This package follows the official dsh plugin conventions (it declares `dsh.bundle`), so
installation matches any official bundle: **one command** — auto-initializes the profile,
installs the package, appends the bundle layer; no profile YAML to write.

### Install (2 steps)

**Step 1 — install** (from the npm registry; no source checkout needed):

```sh
dsh plugin --profile acp-enhanced add dsh-acp-enhanced
```

> When hacking on the code, use `link:` to a local checkout instead (live edits):
> `dsh plugin --profile acp-enhanced add "link:/absolute/path/to/dsh-acp-enhanced"`

**Step 2 — register in Zed** (under `agent_servers` in `~/.config/zed/settings.json`;
Zed spawns agents with a minimal PATH, so use the shipped launcher
`scripts/dsh-acp-zed.sh`, which locates `node`/`dsh` itself)

> **The launcher ships with the package.** Its absolute path depends on how you
> installed in Step 1:
> - **npm install (default)**: `$HOME/.dsh/profiles/acp-enhanced/node_modules/dsh-acp-enhanced/scripts/dsh-acp-zed.sh` — replace `$HOME` with your home directory (e.g. `/Users/you`); Zed does not expand `~` or env var