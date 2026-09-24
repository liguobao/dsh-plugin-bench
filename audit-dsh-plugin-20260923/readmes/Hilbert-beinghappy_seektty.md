> **Development branch:** this checkout adapts SeekTTY to official dsh `0.1.5-rc.1` only. It is not the published `seektty@1.2.5` artifact. The release installation commands below describe the previous release; use a locally packed candidate for this branch. Interface differences, migration decisions, and completed/pending checks are recorded in [the adaptation document](docs/dsh-0.1.5-rc.1-adaptation.md).

<div align="center">

<img src="assets/seektty-logo.png" alt="SeekTTY logo" width="200">

<h1>SeekTTY</h1>

<p>A terminal workspace for DeepSeek Harness.</p>

<p>
  <a href="https://github.com/Hilbert-beinghappy/seektty/releases"><img src="https://img.shields.io/badge/Version-1.2.5-orange" alt="Version 1.2.5"></a>
  <img src="https://img.shields.io/badge/DeepSeek%20Harness-0.1.1--rc.2-5B5BD6" alt="DeepSeek Harness 0.1.1-rc.2">
  <img src="https://img.shields.io/badge/Node-%5E22.19.0%20%7C%7C%20%3E%3D24-339933?logo=nodedotjs&logoColor=white" alt="Node.js 22.19 or newer">
  <a href="https://github.com/Hilbert-beinghappy/seektty/actions"><img src="https://github.com/Hilbert-beinghappy/seektty/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow" alt="MIT License"></a>
</p>

<p>
  <a href="#overview">Overview</a>
  ·
  <a href="#quick-start">Quick start</a>
  ·
  <a href="#clarify-and-plan">Clarify and Plan</a>
  ·
  <a href="#features">Features</a>
  ·
  <a href="#compatibility-and-verification">Compatibility</a>
</p>

<p>English · <a href="README.zh.md">中文</a></p>

</div>

---

## Overview

Run `deepseek` from a project directory to use the native Agent, Session, model, permission, Settings, Profile, plugin, and persistence services of [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) in one terminal workspace. SeekTTY is the terminal surface; Harness remains the owner of runtime state.

Models, Providers, Agent Presets, permissions, commands, tools, Settings, Skills, MCP servers, and marketplace sources are discovered from the running Harness. Capabilities added by upstream or third-party Bundles therefore appear without being hard-coded into SeekTTY.

For requirements that still need definition, the optional [Clarify Host plugin](https://github.com/Hilbert-beinghappy/dsh-plugin-clarify) adds a guided `/clarify` workflow. It asks focused questions, updates a reviewable Draft after each answer, and returns the accepted Draft to the composer. Harness-native `/plan` can then turn the submitted requirement into an implementation plan.

## Quick start

Install SeekTTY on the tested official DeepSeek Harness `0.1.1-rc.2`:

```sh
pnpm add --global --config.enable-global-virtual-store=false @deepseek-ai/dsh@0.1.1-rc.2

dsh plugin --profile tui add --config.enable-global-virtual-store=false seektty@1.2.5

dsh --profile tui
```

These commands install the prebuilt Bundle through native `dsh plugin` reconciliation. The per-command pnpm option avoids the pnpm 11 Global Virtual Store layout that the Cordis loader in the currently tested dsh releases cannot reliably load. SeekTTY never changes global pnpm configuration. Clarify and Auxiliary Runtime are optional, not default dependencies; their historical joint acceptance is listed under [Compatibility](#compatibility-and-verification).

The exact `seektty@1.2.5` npm package and the GitHub Release tarball are built from the same reviewed package inputs. The [1.2.5 owner review and release checklist](docs/release-v1.2.5-verification.md) records the publication and verification procedure.

### Bare `deepseek` launcher

After installing `dsh`, install the same SeekTTY release globally and pin Profile reconciliation to its exact npm version:

```sh
pnpm add --global --config.enable-global-virtual-store=false seektty@1.2.5
export SEEKTTY_SPEC=seektty@1.2.5
deepseek
```

PowerShell uses the same exact npm spec:

```powershell
pnpm add --global --config.enable-global-virtual-store=false 'seektty@1.2.5'
$env:SEEKTTY_SPEC='seektty@1.2.5'
deepseek
```

`deepseek` requires `dsh` on `PATH`, or `DSH_BIN` pointing to its executable. Common launch forms include:

```sh
deepseek "check this project"
deepseek --cwd ../project
deepseek --resume
deepseek --resume <sessionId>
deepseek --profile team-tui
deepseek --version
deepseek --update
```

`deepseek --update` is self-first: it checks SeekTTY before dsh, installs at most one compatible component per run, and never installs an untested gap or future Host. `DSH_BIN`, local installs, and `SEEKTTY_SPEC` overrides are left unchanged. Update failures do not block startup. Set `SEEKTTY_UPDATE=check` for a post-session notice or `SEEKTTY_UPDATE=0` to disable checks.

SeekTTY `1.2.5` brings a Fastfetch-style welcome page, terminal-integrated backgrounds, VS Code-grade TextMate highlighting, more reliable transcript and selection controls, and pnpm 11 installation compatibility to official Harness `0.1.1-rc.2`. No Settings or Session migration is required.

### What's new in 1.2.5

- Empty sessions open with a responsive DeepSeek pixel-whale welcome page and Profile runtime facts. `/welcome` configures custom rows, optional safe/trusted Fastfetch information, built-in/file/local-Fastfetch logos, mixed ordering, live preview, refresh, and reset without writing welcome content into Session history.
- The canvas can inherit terminal transparency, blur, and background images through `theme`, `terminal`, and backward-compatible `explicit` background modes. Overlay, panel, and ordinary code surfaces now follow the same inherited-background policy; contrast adaptation and terminal-color restoration keep text readable and terminal state recoverable.
- Imported VS Code `tokenColors` are authoritative, built-in themes include detailed TextMate rules, and legacy themes receive a compatible fine-grained fallback. Highlighting is language-grammar aware while intentionally remaining visual rather than LSP-semantic.
- Live and completed Thinking blocks can be folded without streaming reopening them; transcript hit rows are aligned, and collapsed tool cards now hide both parameters and results.
- Permission switching validates native Harness results and refreshes authoritative state. Model, reasoning effort, and Agent mode have independent click targets and selectors; `/effort` provides the keyboard path.
- Wide overlays use available space for full option descriptions while preserving search, selection, scroll position, and pointer geometry across resize. Hover styling and transparent surfaces are consistent across nested controls.
- Launcher provisioning, compatible updates, and TUI plugin mutations disable pnpm 11 Global Virtual Store per command. Known `store/v11/links` loader failures receive precise, credential-redacted recovery without changing global pnpm configuration or bypassing native Profile reconciliation.

See the bilingual [release notes](docs/release-v1.2.5.md) for changes and the [owner review checklist](docs/release-v1.2.5-verification.md) for verification limits and the publication procedure.

## Interface

| DeepSeek light | DeepSeek dark |
| --- | --- |
| ![SeekTTY DeepSeek light start screen](assets/seektty-tui.png) | ![SeekTTY DeepSeek dark start screen](assets/seektty-tui-dark.png) |

| TypeScript in the light interface | Tools, file reads, and Diff in the dark interface |
| --- | --- |
| ![SeekTTY light TypeScript syntax highlighting](assets/seektty-code-light.png) | ![SeekTTY dark tool and Diff syntax highlighting](assets/seektty-code-dark.png) |

Full mode uses a fixed alternate-screen viewport and keeps the composer and status at the bottom. Its mouse support browses history, selects text, and clicks existing controls inside SeekTTY. F3 or `/mouse native` switches while idle to terminal-native mode: SeekTTY leaves the alternate screen, writes the complete loaded conversation to ordinary terminal scrollback, disables mouse reporting, and lets the terminal or tmux own scrolling, sear