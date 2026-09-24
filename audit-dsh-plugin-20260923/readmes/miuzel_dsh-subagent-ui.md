# DSH Subagent Workspace UI

A Web client plugin that adds a **子代理管理** button to the conversation-header action row. It opens a searchable panel for the subagents currently discovered by the DSH client runtime.

## Features

- Compact title-bar trigger shows the active-child count and animated activity dot without opening the panel.
- Defaults to the main session's current workspace and current session, even when the user is viewing a child session.
- Workspace and session selectors support current workspace, all workspaces, named workspaces, current session, and named sessions.
- Sort by recent activity, name, or type; recently running children remain near the top after they finish.
- Group by session, workspace, category, type, or no grouping. Session headers show the workspace and parent session name.
- Browser-local classification tabs support custom regular expressions. Built-ins include all, other, review, test, implementation, and planning.
- One-shot children carry a compact `⚡ 一次性` badge; continuable children remain visually uncluttered.
- Show each child's current **type and model provider/id** (`provider/model`, plus the reasoning effort when the host publishes one) from the host's public projections only — no new RPC, no model-switch UI. See [Type and model](#type-and-model-read-only-projections).
- Show each child's usage inline, computed with the host's own definitions: `↑ 131.3k (未缓存 39.1k) / ↓ 12.7k · 命中 70% · 104 tps · 3 轮 · 9 步` (English UI: `miss` / `Hit` / `rnds` / `stps`). The `↑` figure is the **billed input** (`uncachedInputTokens + cacheReadTokens + cacheWriteTokens`) and that billed input alone is the cache-hit denominator — exactly what DSH's own composer footer does, so the plugin and the host agree instead of disagreeing by six points. `tps` is `decodeTokens / (decodeMs / 1000)` from the same public `sessionStats` projection. Hovering the row or the floating panel reveals the complete breakdown — total, every bucket, the share, the speed, and the session's LLM / tool / TTFT timings — in the native `title` tooltip.
- Archive state is local and never deletes a DSH session. Single-row archive actions and a batch mode support shift-selection, select-all, time-based selection (up to 1,000 rows), batch archive, restore, and archive-all.
- Load catalogs in pages of 40 with an independent wheel-scroll container; batch time selection expands loading up to 1,000 children.
- Batch mode changes cards into selection targets and hides individual archive/restore actions. The highlighted 完成 button exits batch mode.
- Open a loaded child at its exact `{ parentSessionId, childSessionId, mode }` address. In normal mode the whole card opens the child; archive controls do not.
- Every row also carries a dedicated **open in the sidebar** button (`◫`) that opens the child as a right-sidebar tab, so the main conversation stays where it is. The button stops propagation (it never triggers the row's default navigation and never toggles batch selection), and it is rendered only when the runtime exposes the sidebar capability: without `ctx.sidebarRight` plus a type that claims the address, the button is hidden entirely; for a single row whose subagent address cannot be resolved it stays visible but disabled with a readable reason. The same button is on the active-subagent floating panel.
- Show session IDs beside names, compact metadata, token totals, and creation time in the relative-time tooltip.
- Active children are grouped at the top in a collapsible section. When the runtime exposes conversation snapshots, the panel shows the latest two lines of live output, recent tool calls, context injection, command status, and a gray final snapshot after completion.

## Screenshot guide

Both screenshots were taken on the `1.7.0-dev` line (commit `79d9d0f`) against a real dsh **0.1.6-alpha.2** instance in its dark theme. The session had four background subagents at once — three still running and one already finished — so every row could be shown with its real type, model and usage figures. The pair below is the English UI; the Chinese UI pair is in [`README.zh.md`](README.zh.md).

![Subagent manager panel (English UI)](docs/images/screenshot-1.en.png)

![Active subagent floating panel (English UI)](docs/images/screenshot-2.en.png)

1. **Header** — panel title, `Current session n · Current workspace n · Active n`, the show-active-float toggle, and the close action.
2. **Search and scope row** — ordinary name/title/workspace search, with `id: xxx` reserved for Session ID search; workspace, session, sorting, and grouping selectors stay on one compact row.
3. **Classification row** — built-in and custom categories with live counts, custom-category creation and deletion inside the same tab frame.
4. **Filter row** — hide one-shot, hide long-inactive, subagent background colour (light/dark), and reset filters.
5. **Summary row** — `Showing n/m`, show details, show hidden, and the batch-mode entry.
6. **Active subagents group** — pinned to the top and collapsible, with `Pause all`; each row carries the activity dot, the name, the Session ID, the relative activity time, and the `◫` open-in-the-sidebar, `⏸ Pause`, `⊘ Hide` and `🗑 Delete` actions.
7. **Detail block** — `Type: … · Model: …` straight from the host's read-only projections, then the official usage line `↑ billed (miss …) / ↓ output · Hit n% · n tps · n rnds · n stps`; a running child also shows its latest live-output lines, while a finished child keeps its final snapshot.
8. **Floating panel** — the running children of the current session in a compact always-on-top card, each with its live output, usage line and stop button; it appears whenever at least one child is running and the manager panel is closed.

## Install in the Web profile

From this directory:

```bash
dsh plugin --profile web add file:.
```

The bundle includes [`cordis.patch.yml`](cordis.patch.yml), which inserts the manager and shadows exactly one stock slot: `conversation.session.header.lineage` is claimed by a `priority: -1` title-only shadow so DSH's stock `ui-subagent` lineage dropdown stays invisible while this package is installed. The stock `ui-subagent` plugin itself is **left enabled** — this package no longer disables it wholesale, because the sidebar tab it provides is the navigation target of the new "open in the sidebar" button. The shadow renders the session title instead of an empty entry, so the subagent session header keeps its title. Removing the package removes this bundle layer, and the host's `ui-subagent` setting is untouched, so your own configuration is restored as it was. Restart the existing `dsh web` process, then refresh `http://127.0.0.1:3080` after the plugin is available.

If you previously disabled `ui-subagent` manually in `$DSH_HOME/profiles/web/cordis.patch.yml`, you can keep that stanza: it is user-owned and intentionally preserved. The plugin no longer needs (or writes) such a stanza.

## Runtime data boundary

The public DSH Web session store exposes subagent summaries that have been discovered in the current browser runtime. It deliberately does not expose a global historical subagent index or a mode for every unvisited child. Therefore this first plugin version manages the discovered catalog; rows whose type is not yet loaded remain visible and searchable and fall back to DSH's retained session navigation. Exact catalog navigation is used automatically as soon as DSH supplies the address and mode.

A full persistent workspace-wide archive view requires a host-side catalog RPC (or an upstream DSH API) that enumerates every child address and its mode. The public `SessionSummary` does not expose the original prompt, so prompts are neither queried nor displayed; **type and model** come from the public projections documented in [Type and model](#type-and-model-read-only-projections). Live output and tool/context activity are read from the bound session automatically: on dsh **0.1.2-alpha.2** they are