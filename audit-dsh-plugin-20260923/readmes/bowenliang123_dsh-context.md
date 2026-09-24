![Social preview](https://raw.githubusercontent.com/bowenliang123/dsh-context/main/docs/social-preview.png)

# dsh-context

[![npm version](https://img.shields.io/npm/v/dsh-context)](https://www.npmjs.com/package/dsh-context)
[![GitHub stars](https://img.shields.io/github/stars/bowenliang123/dsh-context?style=social)](https://github.com/bowenliang123/dsh-context)
[![dshfind](https://dshfind.com/api/badge/bowenliang123/dsh-context)](https://dshfind.com/en/plugins/bowenliang123/dsh-context?ref=badge)

**The best [DeepSeek Harness plugin](https://www.deepseek.com/harness/) for Agent's context insights and management.**

[`dsh-context`](https://www.npmjs.com/package/dsh-context) provides full context lifecycle management features.
- **Context Dashboard** — the cross-session overview above Settings on the sidebar foot: KPI band, activity heatmap, aggregate composition ring, and filterable session cards that jump straight into any session.
- **Context tab** — an UI context dashboard for DeepSeek Harness's context stats, composition, trend, events, and messages.
- **Context panel** — the same dashboard as a right-sidebar tab (dsh 0.1.5-rc.1+): pick **Context** on the sidebar's guide page and the panel opens beside the chat.
- **`/context` command** — the slash command shows the context model for current context composition and recent context evolution.

## Install / Update

Install [`dsh-context`](https://www.npmjs.com/package/dsh-context) plugin from [DeepSeek Harness](https://www.npmjs.com/package/@deepseek-ai/dsh):

```sh
dsh plugin --profile web add dsh-context
```

Or update the `dsh-context` plugin:

```sh
dsh plugin --profile web update dsh-context@latest
```

Then start the web UI with `dsh web`. No build step, no restart.

## Use it

Four surfaces, one story — what your agent is carrying, how it got there, and what it did with it:

| Where | What you get |
| --- | --- |
| **Context Dashboard** | Every session at a glance: usage, cost, cache hit, daily activity, and per-session context profiles — filtered by range, day, group, or search, one click to jump in. |
| **Context tab** | The full dashboard: stats, composition, per-request trend, events, file activity, and the agent network — in every session. |
| **`/context` command** | A centered modal with the same composition and context browser, without leaving the chat. |
| **Preferences card** | Per-user defaults: view placement, trend granularity & mode, File Activity sort, and more. |

## 🗂️ The Context Dashboard

Click **Context Dashboard / 上下文仪表盘** at the bottom-left of the sidebar, right above **Settings**:

![Context Dashboard](https://raw.githubusercontent.com/bowenliang123/dsh-context/main/docs/context-dashboard.png)

| Section | The question it answers |
| --- | --- |
| **KPI band** | How much am I using — sessions, billed tokens, estimated cost, and cache-hit rate over the picked range (7d / 30d / all). |
| **Activity heatmap** | When do I actually work — the last 8 weeks of daily billed tokens; click a day to filter the sessions that were active on it. |
| **Context Composition** | Where the context windows went, summed over the range's sessions. |
| **Session cards** | Each session's profile: composition ring, billed tokens, turns, cost, and its workspace-group / project breadcrumb — sorted by recency, tokens, or context size, searchable, grouped by workspace. A card click opens the session. |


## 📊 The Context tab

Open any session and click the **Context / 上下文** tab:

![Context panel overview](https://raw.githubusercontent.com/bowenliang123/dsh-context/main/docs/context-overview.png)

| Card | The question it answers |
| --- | --- |
| **Context Stats** | Turns, steps, human inputs, live tool calls, the session's cache-hit rate — plus a cost estimated from the models.dev list prices (hover the `?` for per-1M rates; DeepSeek peak/off-peak aware). |
| **Token Stats** | Where the billed tokens went — the same total as the chat stats line under the composer, split by composition (system, tools, messages…) with the provider-exact output closing the ring. |
| **Timing Stats** | How active time split across model calls, tool runs, and overhead. |
| **Current Context** | What's in the window *right now*. |
| **Context Trend** | Every request's size — and its story. |
| **Context Browser** | What any request was *actually* assembled from. |
| **Context Events** | When and why the window changed. |
| **File Activity** | What the agent *did* to your files. |
| **Agent Network** | The whole agent family, live. |

The headline occupancy and composition read the **same official token-meter projections as the chat composer's context ring** (`contextPressure` / `contextBreakdown`), so the figures always match what the ring tells you.

### Context Stats

#### Token Stats and Timing Stats
![Token_Stats_and_Timing_Stats](https://raw.githubusercontent.com/bowenliang123/dsh-context/main/docs/token-stats-and-timing-stats.png)

#### Context Stats
![Context_Stats](https://raw.githubusercontent.com/bowenliang123/dsh-context/main/docs/context-stats.png)


### 🧱 Current Context — what's in the context window now

![Current Context card](https://raw.githubusercontent.com/bowenliang123/dsh-context/main/docs/current-context.png)

A six-color stacked bar against the model's full window (hatching = free headroom): system prompt, tool schemas, user messages, injected context, assistant replies, tool results — each with its ≈token figure and share. When a conversation starts degrading, this is where you see *which part* is responsible.

### 📈 Context Trend — how the context grew and evolved by turn or steps

![Context Trend with the step brief](https://raw.githubusercontent.com/bowenliang123/dsh-context/main/docs/context-trend.png)

One stacked bar per model request — finer than per-message — so you watch the window grow turn by turn:

- **✨ Step brief** — three plain-language rows under the chart: **User** recalls the message that opened the turn, **In** lists what newly entered (usually the previous tool results), **Response** shows the reply and/or tools called. Click a row to open that exact message in the Context browser.
- **✂ marks the events** — compactions and prunes are pinned to the bar where they happened, so the drops explain themselves.
- **Read it your way** — **Step / Turn** granularity, **Total** (cumulative makeup) or **Delta** (each request's signed change), and sideways scrolling through the whole session. In Delta mode, growth piles up above the baseline and a compaction dives below it:

![Context Trend in Delta mode](https://raw.githubusercontent.com/bowenliang123/dsh-context/main/docs/history-delta.png)

- **Hover & pin** — scrub for an instant tooltip; click to pin the full breakdown, with provider-reported **Actual Prompt / Output / Cache** next to the estimates.
- **Live linkage** — hovering a bar previews that step's assembled context in the Context browser beside the chart; leaving the chart returns to your own pick.

### 🧭 Context Browser — open the box of any request

Pick **Live (next request)** or any retained step, and browse what that request was assembled from: seven collapsible categories expand into one row per element with its token price, and every element expands again into its **actual content** — the system prompt, each tool's JSON schema, message text, reasoning, tool arguments, and tool outputs. Skill content (the available-skills catalog, `/skill` invocations, and `skill`-tool loads) has its own **Skill Injections** category, so a stealthy skill's context footprint can't hide inside the injected-context and tool-result buckets.

- **Who provides each tool** — every tool-schema row carries a best-effort source chip: `tool-*` first-party packages, `dsh-*` capability packages, `mcp:<server>` proxies, or the exact plugin watched live from `tools.register()`. Sort by **size / name**, and filter every category by its own searchable fields:

![Tool schemas with source chips, filt