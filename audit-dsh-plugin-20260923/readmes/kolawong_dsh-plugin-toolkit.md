<p align="center">
  <img src="docs/assets/hero.svg" alt="dsh-plugin-toolkit — small, runtime-toggleable quality-of-life optimizations for DeepSeek Harness" width="100%">
</p>

<p align="center">
  <b>English</b> · <a href="README_CN.md">简体中文</a>
</p>

Personal quality-of-life toolkit for [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness). Each optimization is too small to deserve its own vertical plugin, so they ship together as one entry in the Toolkit settings card: **Web settings → Plugins → DSH-Toolkit** expands a half-width sub-card grid (icon, title, short subtitle, on/off badge), and clicking a sub-card opens that optimization's dialog. The plugins page stays a compact launcher as the list grows.

Everything is wired through public extension surfaces — settings namespaces, the client module table, conversation slots, `llm/stream`, model discovery and `webServer` routes — so no dsh core package is patched and upstream one-click upgrades stay painless.

## Contents

- [At a glance](#at-a-glance)
- [Install](#install-web-profile)
- [Architecture](#architecture)
- [The settings card](#the-settings-card)
- [Optimizations](#optimizations)
  - [`workspacelessChat`](#workspacelesschat)
  - [`editLastMessage`](#editlastmessage)
  - [`viewActivity`](#viewactivity)
  - [`slashI18n`](#slashi18n)
  - [`changeReport`](#changereport)
  - [`opencodeSession`](#opencodesession)
  - [`modelCapability`](#modelcapability)
- [Configuration reference](#configuration-reference)
- [Development](#development)
- [Graduation rules](#graduation-rules)
- [Model experience](#model-experience)
- [License](#license)

## At a glance

| # | Optimization | What it does | Default | Half |
|---|---|---|---|---|
| 1 | [`workspacelessChat`](#workspacelesschat) | Keeps a no-project chat workspace and auto-connects it at cold start | on | client + host |
| 2 | [`editLastMessage`](#editlastmessage) | Edit-and-resend the last user message, rewinding the model context | on | client (host `session.rewrite` RPC) |
| 3 | [`viewActivity`](#viewactivity) | Sidebar activity icon: running-first, then Today / Yesterday / Weekday / Earlier | on | client |
| 4 | [`slashI18n`](#slashi18n) | Chinese descriptions for the `/` menu's commands and skills | on | client |
| 5 | [`changeReport`](#changereport) | Codex-style per-turn file-change card at the turn tail | on | client |
| 6 | [`opencodeSession`](#opencodesession) | Stable `x-opencode-session` header on OpenCode Go/Zen requests | on | host |
| 7 | [`modelCapability`](#modelcapability) | Keeps one llm-pi-ai route's model list, capacities and image support current | on | host + client |

## Install (web profile)

```sh
cd ~/.dsh/profiles/web
pnpm add file:/path/to/dsh-plugin-toolkit   # link:/path/to/dsh-plugin-toolkit while developing
# add "dsh-plugin-toolkit" to the dsh.profile.bundles list in package.json
systemctl restart deepseek-harness.service  # or your profile's restart path
```

Server-side changes (this package) need a profile restart; the client bundle re-syncs with `pnpm install` inside the profile followed by a browser hard refresh. Toggles, paths and model lists are settings-namespace values, so day-to-day edits apply live without a restart.

## Architecture

<p align="center">
  <img src="docs/assets/architecture.svg" alt="Architecture: the browser client half, the dsh host half, and the external OpenCode and models.dev services" width="100%">
</p>

The package is split into a browser half and a host half; both read the same `toolkit` settings namespace, and neither touches dsh source.

| Half | Files | Responsibility | Seams used |
|---|---|---|---|
| Client | `client.js` | Settings card, inline edit UI, sidebar re-sort, `/`-menu rewrite, change-report card, model-id pickers | Client module table, conversation node/turn-tail slots, `remote.*` namespace wraps, settings scope |
| Host | `index.js` | Settings schema and defaults, default chat workspace directory, OpenCode session-header stamping | `settings`, `llm/stream`, `globalThis.fetch` |
| Host | `model-sync.js` + `models-core.js` | Model discovery wrap, sync/listing routes, capacity and modality enrichment | `llm` model discovery, `webServer` routes, settings stores |

Design rules that hold across the package:

- **No core patches.** Every hook is a documented extension surface, so an upstream upgrade cannot conflict with the toolkit.
- **Dormant, not broken.** Missing a seam (older host, no `webServer`, no `session.rewrite`) disables just that optimization; the rest of the UI is untouched.
- **Live configuration.** Every toggle and field lives in the `toolkit` settings namespace and is re-read at use time.
- **Independent toggles.** Each optimization can be switched off from its sub-card and restores the stock behaviour verbatim.

## The settings card

<p align="center">
  <img src="docs/assets/settings-card.svg" alt="The DSH-Toolkit settings card with seven half-width optimization sub-cards, each with an icon, title, identifier and on badge" width="100%">
</p>

The card renders one sub-card per optimization with a live on/off badge and an **Enable all / Disable all** pair. Opening a sub-card shows that optimization's own description and fields (for example the chat directory, or the model-capability key and pickers).

## Optimizations

### `workspacelessChat`

Chat without picking a workspace first, like other agent harnesses' default-project behaviour. dsh's composer requires a blank session to belong to a workspace, so the optimization keeps a dedicated **no-project chat workspace** (「通用对话」) around: it is idempotently created with its friendly title whenever the optimization is enabled, so the option always shows in the sidebar and workspace picker — open it to chat without a project.

On top of that, when both baselines are ready, no session is selected, and the runtime's own startup policy has no recent workspace to connect (first run, no workspaces), the client also auto-connects a blank session in that workspace so the composer is live immediately.

<p align="center">
  <img src="docs/assets/flow-workspaceless-chat.svg" alt="Cold-start decision: the runtime's recent-workspace auto-connect wins; otherwise the toolkit ensures the chat workspace and auto-connects a blank session" width="100%">
</p>

The cold-start auto-connect failures retry at most 3 times (2 s apart) and then stay dormant until a list change re-triggers the check. The runtime's own recent-workspace auto-connect always wins; the auto-connect only fills the nothing-to-connect case, while the workspace itself exists unconditionally. The workspace is renamed to its friendly title only while it still carries the auto-derived basename (a title you set yourself is never overwritten).

| Config | Default | Meaning |
|---|---|---|
| `optimizations.workspacelessChat` | `true` | Toggle the no-project chat workspace + auto-connect. |
| `chatWorkspacePath` | `""` | Host directory for the default chat workspace; empty resolves to `<DSH_HOME>/chat`. The server creates the directory (live on settings edits, too). |
| `chatWorkspaceTitle` | `通用对话` | Display title of the no-project chat workspace. |

The card writes go through the `toolkit` settings namespace, so toggles and path edits apply live without a restart.

### `editLastMessage`

Retry a failed answer without copy-pasting and without polluting the model's context: the last user message's hover actions gain an **Edit** button. Clicking it opens an inline editor prefilled with that message; **Save & resend** rewrites the session in place — the edited message and everything after it are replaced (the model context truly rewinds, so the next request contains only the edited content), and a new turn answers the edited message.

<p align="center">
  <img src="docs/assets/flow-edit-resend.svg" alt="Before and after a rewrite: the old message and failed turn are erased from the transcript and from the derived model history" width="100%">
</p>

This