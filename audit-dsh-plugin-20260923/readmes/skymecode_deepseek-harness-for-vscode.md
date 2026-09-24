# DeepSeek Harness for VS Code

**English** | [简体中文](README.zh-CN.md)

A native VS Code coding-agent extension powered by [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness). Install the platform-specific VSIX and start working—there is no upstream repository to clone, no Node/npm setup, and no local Harness deployment to manage.

> This is the community-maintained `0.6.1-dev` release. DeepSeek Harness is currently a Developer Preview, and this extension pins the official `@deepseek-ai/dsh@0.1.7-alpha.1` package (Typert Remote protocol).

> **Runtime upgrade:** Harness now uses session format V4. Supported older logs are migrated on resume into a new generation while their original files are preserved. Old runtimes cannot read the new V4 generation; back up `~/.dsh/vscode/harness-home` before upgrading, and do not downgrade an active profile. Third-party plugins using the removed `ctx.agent` or runtime `Inbox` APIs need their own compatibility updates. The extension keeps its native VS Code interface rather than embedding the official Web UI.

Startup uses the official runtime package resolver. Only a recognized legacy module conflict triggers one bounded backup-and-repair attempt; ordinary profile packages are no longer moved on every startup or installation.

## Runtime update policy

The bundled DeepSeek Harness runtime is upgraded selectively, not automatically with every upstream release. We review the actual changes—relevant features, bug and security fixes, and breaking changes—and adopt an update after compatibility adaptation and regression testing, with particular attention to Windows, macOS, Linux, existing conversation history, and plugins. The 0.1.7 native capability gap is tracked in [the upgrade audit](docs/DSH_0_1_7_NATIVE_GAP_ANALYSIS.zh-CN.md).

Stability and the upgrade experience for existing users take priority over always bundling the newest version. Releases that still need validation or introduce compatibility risks may be deferred; an extension update may also keep the current pinned runtime. The bundled version and any upgrade caveats are documented in this README and the [changelog](CHANGELOG.md).

## Features

- **Native VS Code workbench** — all interaction happens in the sidebar; the local Harness Gateway exposes only the loopback API transport, while the official WebUI is neither served nor embedded.
- **Shared local history** — the bundled runtime and an independently installed official DSH can read the same saved conversations. Installing the official CLI is optional; credentials and plugin profiles stay separate.
- **Detachable workbench** — open the same synchronized conversation UI in an editor-area panel and move it to another VS Code window when more space is needed.
- **Complete session workflow** — persistent history, create, switch, rename, fork, resume, archive/restore, export, and import sessions (official DSH ZIP, ChatGPT export ZIP, and other agent transcripts via `dsh-chat-import`); changing the DSH mode opens a fresh session in the new mode and carries the previous context as a hidden digest attached to your next message.
- **Streaming Markdown** — headings, lists, tables, code blocks, copy controls, safe external links, and clickable workspace file references.
- **Stable incremental rendering** — streamed updates preserve disclosure state and the reader's scroll position.
- **Progressive reasoning timeline** — nodes appear as thinking steps arrive, connecting only existing steps within the same turn. Completed turns retain their timeline inside the expandable process section.
- **Session titles** — automatic titles and manual renames are owned by the official session service.
- **Per-turn file changes** — official snapshots and historical diffs include shell-driven edits. Old or unavailable snapshots fall back to labeled tool statistics; current workspace changes never stand in for a historical diff.
- **Compact completed turns** — reasoning, tool calls and interim updates fold into a duration row; the final answer and file changes remain visible.
- **Reader-friendly streaming** — while a turn streams you can scroll up through earlier messages freely; auto-follow yields to your scroll and only resumes at the very bottom. The finished conclusion is set off by a divider between the thinking and the final answer (or above the message when there is no thinking).
- **DeepSeek Harness-native reasoning** — thinking is presented in a native reasoning block that opens as deltas stream, follows the newest content, and collapses to a summary row once the block completes.
- **Editor context** — selected code appears as a removable context card; type `@` to fuzzy-search and attach workspace files without leaving the composer.
- **Slash commands** — use official Harness commands plus `/model`, `/reasoning`, and `/preset` extension commands.
- **Harness-native capabilities** — reasoning, tool calls, approvals, structured questions, Todos, Skills, Goals, Plan mode, and background jobs.
- **Model and agent controls** — official catalogs provide model capabilities and reasoning choices; new sessions default to `deepseek-flash`. The PTC preset uses `ptc`; legacy `code` sessions keep a compatible preset.
- **Token usage** — see current input and output token counts in the composer.
- **Native DSH plugin center** — search a curated catalog, filter by category, inspect installed plugins, or install an npm/GitHub/local/tarball package.
- **Automatic localization** — follows the VS Code display language with English and Simplified Chinese support.
- **Zero-deployment runtime** — official `dsh`, pnpm, and standalone Node 22.22.3 are bundled in each platform VSIX and managed by the extension.

Open the workbench with `Ctrl+Alt+H` on Windows/Linux or `Cmd+Alt+H` on macOS.

## Interface preview

Screenshots use the **0.5.9** workbench UI with a demonstration conversation and no private account data. This README shows the English interface; the [Chinese README](README.zh-CN.md#界面预览) shows the localized interface. Select an image to view it at full resolution.

<table>
  <tr>
    <td align="center" width="58%">
      <a href="docs/images/workbench-preview.png">
        <img src="docs/images/workbench-preview.png" alt="DeepSeek Harness 0.5.9: single-row header, collapsed turn process, final answer and edited files" width="460">
      </a>
    </td>
    <td align="center" width="42%">
      <a href="docs/images/model-and-effort.png">
        <img src="docs/images/model-and-effort.png" alt="DeepSeek Harness 0.5.9: Flash and Pro model selection, four DSH modes and reasoning effort slider" width="300">
      </a>
    </td>
  </tr>
  <tr>
    <td align="center"><sub>0.5.9 workbench — compact turn process, final answer and per-turn file changes</sub></td>
    <td align="center"><sub>Flash / Pro, four DSH modes and the effort slider</sub></td>
  </tr>
</table>

## Installation

1. Download the VSIX matching your platform from [Releases](https://github.com/skymecode/deepseek-harness-for-vscode/releases).
2. Open the VS Code Extensions view (`Cmd/Ctrl+Shift+X`).
3. Select `...` → **Install from VSIX...** and choose the downloaded file.
4. Reload the VS Code window when prompted.

For example, an Apple Silicon Mac requires the `darwin-arm64` package.

## Quick start

1. Open the project you want to work on.
2. Select the **DeepSeek Harness** icon in the Activity Bar.
3. Open **Connection settings** and configure DeepSeek Official or add a relay source. You can also run `DeepSeek Harness: Set API Key` for the official source.
4. Describe your task in the composer and send it.

No Harness install or start command is required.

## Shared history with official DSH

The extension still ships and starts its own tested Harness/Node runtime. A separately installed CLI is **not required** and is not substituted automatically. On the same machine and OS user account, both backends use the official history location by default:

| Platfo