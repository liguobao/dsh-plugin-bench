<p align="center">
  <img src="docs/images/banner.jpg" alt="DSH Mobile — the DeepSeek Harness in your pocket" width="100%">
</p>

<h1 align="center">DSH Mobile — DeepSeek Harness Remote</h1>

<p align="center">
  An open-source Android companion that puts your <b>DeepSeek Harness</b> in your pocket.<br>
  Drive sessions, review plans and goals, answer approvals and questions, and get notified
  when the harness finishes — from your phone, over your network or a relay.
</p>

<p align="center">
  <a href="https://dshm.zyphite.com"><img alt="Website" src="https://img.shields.io/badge/website-dshm.zyphite.com-4176E6?style=flat-square"></a>
  <a href="https://github.com/sorsama/deepseek-harness-mobile/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/release/sorsama/deepseek-harness-mobile?style=flat-square"></a>
  <a href="https://github.com/sorsama/deepseek-harness-mobile/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/sorsama/deepseek-harness-mobile/ci.yml?branch=main&style=flat-square"></a>
  <img alt="Android 8.0+" src="https://img.shields.io/badge/Android-8.0%2B-3DDC84?style=flat-square">
  <a href="LICENSE"><img alt="MIT" src="https://img.shields.io/badge/license-MIT-blue?style=flat-square"></a>
</p>

<p align="center">
  <b>English</b> ·
  <a href="README.zh-CN.md">中文</a> ·
  <a href="README.hi.md">हिन्दी</a> ·
  <a href="README.es.md">Español</a> ·
  <a href="README.fr.md">Français</a> ·
  <a href="README.th.md">ไทย</a>
</p>

DSH Mobile is an **unofficial companion app** for the
[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (MIT). It mirrors the web GUI
feature for feature and uses the harness's own visual language. Android only, Kotlin + Jetpack
Compose.

Its companion on the other end is
[**dsh-relay**](https://github.com/sorsama/deepseek-harness-relay), a harness plugin that adds the
authentication layer the harness says it lacks, so this app can reach a harness with a real
credential and a pinned key instead of an open port. See
[Relay](https://github.com/sorsama/deepseek-harness-mobile/wiki/Relay).

**[dshm.zyphite.com](https://dshm.zyphite.com)** is the project site: what the app is, what it looks
like, and how to get it running, on one page.

The [**wiki**](https://github.com/sorsama/deepseek-harness-mobile/wiki) is the user-facing guide:
[getting started](https://github.com/sorsama/deepseek-harness-mobile/wiki/Getting-Started),
[connecting](https://github.com/sorsama/deepseek-harness-mobile/wiki/Connecting),
[troubleshooting](https://github.com/sorsama/deepseek-harness-mobile/wiki/Troubleshooting),
a [feature tour](https://github.com/sorsama/deepseek-harness-mobile/wiki/Feature-Tour) and an
[FAQ](https://github.com/sorsama/deepseek-harness-mobile/wiki/FAQ).

---

## Screenshots

| Connect | Chat | Trajectory |
|:--:|:--:|:--:|
| <img src="docs/images/home.png" width="240" alt="Connect screen: recent harnesses with live reachability, discovery, manual entry and auto-connect toggles"> | <img src="docs/images/chat.png" width="240" alt="Chat: streamed turns with per-tool icons, tool cards, goal dock and composer"> | <img src="docs/images/trajectory.png" width="240" alt="Trajectory: a per-turn ledger with usage totals"> |
| Recent harnesses with live reachability, LAN discovery, manual `host:port`, auto-connect. | Streamed turns, a glyph per tool, expandable tool cards, permission picker. | The same session as a per-turn ledger with usage totals. |

| Session details | Subagents |
|:--:|:--:|
| <img src="docs/images/session-info.png" width="240" alt="Details panel: context breakdown, goal, plan mode, jobs, queue, subagents, host information"> | <img src="docs/images/subagent.png" width="240" alt="Subagent catalog with continuable children"> |
| Context breakdown, goal, plan mode, background jobs, queued turns, host info, session-log export. | The subagent catalog — open a child's transcript, follow up, or interrupt it. |

## Features

- Connecting — finds a harness on your Wi-Fi with an active subnet scan and a readiness
  handshake, remembers hosts and probes them for liveness on the way in, takes a manual
  `host:port`, handles loopback for same-device setups, and auto-connects when you tell it to
  (last used, LAN, or same device).
- Navigation — the drawers work like Discord's: swipe right from the left edge for the
  workspace-grouped chat list, swipe left to close it, swipe left from the right edge for the
  session details panel.
- Chat — streamed turns with reasoning disclosure, markdown, terminal/diff/read/search/web tool
  cards, a queue dock where you can edit, remove or steer a queued turn, history paging, and
  multi-photo and file attachments. Drafts are kept per host and session.
- Workspace panels — tabbed text, Markdown, image, PDF and isolated HTML previews; native
  terminal controls with a bundled xterm renderer; archived-session restore in Settings.
- Message feedback — confirmed ratings and retraction, with version-conflict handling.
- Slash commands and skills — the composer checks a `/` line against the session's own command
  catalog and runs it through the harness's command gateway. Anything the catalog does not claim
  is sent as a prompt, which is how skills get invoked.
- Everything the GUI does — goals (phases, rounds, pause/resume/edit), plan mode and plan review,
  permission approvals, user questions, todo dock, subagents (catalog, follow-ups, interrupt),
  background jobs, workflow runs, skills, model selection, agent presets, session search,
  trajectory ledger, session export, message feedback.
- Notifications — turn complete, goal complete or blocked, review or question waiting for you.
  A foreground service keeps the connection alive in the background.
- Harness look — the exact DeepSeek Harness design tokens (colors, type, radii, disclosure rows,
  shimmer, ink buttons), with light, dark and system themes.
- 11 languages — English, 中文, हिन्दी, Español, Français, العربية, বাংলা, Português, Русский,
  اردو, ไทย (RTL aware).

## Requirements

- Android 8.0+ (minSdk 26).
- A running [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)
  at `0.1.6-alpha.1` plus master commit
  `0d1f50007f9bca3f52b06e1c3074fa14d5fb0720` for DSH Mobile `0.11.0`.
  See [compatibility](docs/COMPATIBILITY.md) and [validation results](docs/VALIDATION-0.11.0.md).

## Quick start

1. Install the latest APK from
   [Releases](https://github.com/sorsama/deepseek-harness-mobile/releases/latest).
2. Open the app and choose how to connect. Relay and local network are two different setups, not
   two settings of one, so pick the one that matches what you installed on the computer. The last
   two entries below are ways of running local-network mode.

   **Relay** — encrypted, authenticated, and works from outside your Wi-Fi.
   Install [`dsh-relay`](https://github.com/sorsama/deepseek-harness-relay) into
   the harness web profile:

   ```sh
   dsh plugin --profile web add dsh-relay
   dsh web
   ```

   Open the printed URL **on that computer**, set a password, then open
   `/relay/pair`. In the app: **Relay → Pair a relay**, scan the QR. Once every
   client you use has paired, turn off the relay's `compat.addressGrants`;
   nothing here needs it.

   **Local network** — apply the one-file LAN patch in
   [`harness/README.md`](harness/README.md), restart `dsh web`, then tap
   **Scan network**. The harness signs each device in once: paste the link it
   prints at startup when the app asks. That link authenticates the phone, but
   it does not encrypt the connection and it does not stop anyone already on the
   network from reaching the port, so use it only on networks you trust.

   **Behind your own HTTPS reverse proxy** — paste the `https://` address into
   local-network mode. The proxy can forward to loopback, so the harness needs
   no patch, but it encrypts the link without authenticating anyone. See
   [`harness/