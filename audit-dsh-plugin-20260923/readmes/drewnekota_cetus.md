<p align="center"><img src="docs/logo.png" width="120" alt="Cetus logo" /></p>

<h1 align="center">Cetus</h1>

<p align="center"><a href="https://cetus.run">Official website · cetus.run</a></p>

<p align="center"><strong>Turn your favorite agent runtime into an always-on desktop assistant.</strong></p>

<p align="center">Keep Codex, Claude Code, DeepSeek Harness, or the built-in runtime at the core. Cetus adds the desktop layer around it: summon it over any app, schedule work for later, and give it context from what has been on your screen.</p>

<p align="center"><strong>Quick Launcher</strong> · <strong>Automations</strong> · <strong>Global Quick Reply</strong> · <strong>Screen Context</strong></p>

<p align="center">
  <a href="https://github.com/drewnekota/cetus/releases/latest"><img alt="Download for macOS" src="https://img.shields.io/badge/Download_for_macOS-Apple_Silicon-111111?style=for-the-badge&logo=apple" /></a>
</p>

<p align="center">
  <a href="https://github.com/drewnekota/cetus/releases/latest"><img alt="Latest release" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdrewnekota%2Fcetus%2Fmain%2Fsrc-tauri%2Ftauri.conf.json&query=%24.version&prefix=v&label=release&color=blue" /></a>
  <a href="https://github.com/drewnekota/cetus/releases"><img alt="Downloads" src="https://img.shields.io/github/downloads/drewnekota/cetus/total" /></a>
  <a href="https://github.com/drewnekota/cetus/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/drewnekota/cetus/ci.yml" /></a>
  <a href="https://github.com/drewnekota/cetus/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/drewnekota/cetus" /></a>
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/github/license/drewnekota/cetus" /></a>
</p>

<p align="center"><strong>English</strong> · <a href="./README.zh-CN.md">简体中文</a></p>

<h2 align="center">Join the Cetus community</h2>

<p align="center">Scan with WeChat to join the group chat and share feedback.</p>

<p align="center"><img src="docs/cetus-community-wechat.jpg" width="360" alt="WeChat QR code for the Cetus community group" /></p>

![Cetus runtime picker — Claude Code, Codex, DeepSeek Harness, OpenCode, Grok Build, and Kimi CLI in one macOS app](docs/screenshot-runtime-picker.png)

![Cetus demo — launch an agent, schedule an automation, and switch runtimes](docs/cetus-demo.gif)

## Stay tuned

⭐️ Star Cetus to get notified about every new release, and to help more people find it.

<p align="center"><a href="https://github.com/drewnekota/cetus"><img src="docs/star-us.gif" width="720" alt="Star the Cetus repository on GitHub" /></a></p>

## Four things Cetus adds to your agent

### Quick Launcher — your agent, one hotkey away

Hold **both ⌘ keys** to summon your agent over any app. Cetus brings along the current screenshot, frontmost app, browser URL, and selected text as removable context chips, so you can ask in place instead of stopping to explain what you are looking at.

![Cetus quick launcher demo](docs/quick-launcher.gif)

### Automations — let it work while you are away

Turn any prompt into a one-off or recurring job (`at` / `every` / `cron` / `daily`). Each run keeps its chosen runtime and model settings, works in a fresh background conversation, and leaves the result ready for you to review.

![Cetus Automations demo](docs/automation.gif)

### Global Quick Reply — draft the answer without leaving the thread

Double-tap **right ⌥** on any conversation — a team channel, an email, a support console — and Cetus reads what is on screen, then streams a draft into an editable panel. It follows the language and register of the thread and answers what was actually asked, so a message with three open questions does not come back as "sounds good". Press **⏎** to drop it into the input you were already in, or **⇥** to redraft the same screen on another runtime.

![Cetus global quick reply demo](docs/quick-reply.gif)

### Screen Context — let it remember what you were doing

With screen context on, Cetus periodically captures frames, dedupes them, and OCRs them on-device with Apple Vision. Your agent can later recall what was on screen or search the history by text and app. Images and text stay on your Mac; capture is opt-in, with retention controls and an excluded-apps list.

![Cetus screen context settings](docs/screenshot-screen-history.png)

## Get started

The prebuilt app supports **Apple Silicon** and **macOS 13 or later**.

1. [Download the latest release](https://github.com/drewnekota/cetus/releases/latest).
2. Open the DMG and move Cetus to Applications.
3. Use the built-in Cetus runtime, or select an already installed and signed-in `claude`, `codex`, or `dsh` (DeepSeek Harness) CLI.
4. Choose a workspace and give the agent its first task.

Claude Code, Codex, and DeepSeek Harness reuse their existing CLI login — there is no second account to configure. Building from source is documented under [Development](#development).

> **Early release:** Cetus is under active development. Please [open an issue](https://github.com/drewnekota/cetus/issues) if something breaks or if a workflow is missing.

## Everything else

### Keep the runtime you already trust

Use the built-in pi runtime, **Claude Code**, **Codex**, or **DeepSeek Harness** with the models, tools, and login you already have. Cetus translates each runtime into the same desktop workflow while preserving conversation context and background terminals across replies.

Pick a **workspace**, choose a runtime, optionally attach files or a screenshot, and send. For parallel coding tasks, enable per-conversation git worktrees so each agent edits an isolated checkout.

![Cetus chat — What should we work on?](docs/screenshot-chat.png)

### Review background work in one place

Every conversation is a card tracked across **In progress · Needs review · Done**. Automations, long-running tasks, and parallel solutions all surface here instead of getting buried in terminal sessions.

![Cetus Kanban board](docs/screenshot-kanban.png)

### More ways to extend your runtime

- **Persistent memory** you and the agent both edit, injected into future turns
- **Parallel solutions**: fan one prompt into N candidate runs, then keep one and archive the rest
- **Per-conversation git worktrees** for isolated coding sessions
- **Visual quick reply** for drafting replies from the current screen without starting a full agent run
- **Cetus Remote**, an optional Tailscale-backed mobile companion for following runs and handling approvals
- **Voice dictation** and **meeting memory**, processed on-device
- **Computer and browser control**, with confirmation before consequential actions
- **30+ model providers**, including Anthropic, OpenAI, Google, Bedrock, Ollama, LM Studio, and OpenRouter

### Dictate from any app

Hold a hotkey from any app and talk — Cetus pops a floating equalizer HUD, transcribes on-device with Seed-ASR, and drops the cleaned-up text wherever your cursor is. The same stack as the in-app mic, but it follows you across the desktop.

![Cetus voice dictation HUD](docs/voice-hud.jpeg)

This photo was taken with a phone because the floating overlay does not show up in screenshots.

### Turn meetings into searchable context

Turn on **meeting memory** and Cetus quietly transcribes your calls into searchable notes — on-device, text only, no audio stored.

- **Auto-detect** — when another app grabs your mic (Zoom, Teams, FaceTime, Feishu…), Cetus starts a session and stops when the call ends. Nothing to press.
- **Manual** — global hotkey (default **⌘⇧M**) for in-person meetings that auto-detect can't pick up.
- **Both sides** — your mic is you; system audio is everyone else, captured separately so the transcript knows who said what (macOS 14.2+; falls back to mic-only below that).

Transcription is 100% on-device via Apple's Speech framework — streaming, punctuated, segm