# dsh-status-rotator

> Replaces the DSH Web status line (`Deep diving...`) with your own phrase bank: **1092 phrases, 12 theme packs, typewriter + day/night rainbow gradient + danmaku**.

**English** | [中文](./README_ZH.md) · [Quick start](#quick-start) · [Features](#feature-overview) · [Configuration](#configuration) · [Changelog](./CHANGELOG.md)

[![npm version](https://img.shields.io/npm/v/dsh-status-rotator?color=4a6cf7)](https://www.npmjs.com/package/dsh-status-rotator)
[![npm downloads](https://img.shields.io/npm/dt/dsh-status-rotator?color=4a6cf7)](https://www.npmjs.com/package/dsh-status-rotator)
[![GitHub stars](https://img.shields.io/github/stars/01Virex/dsh-status-rotator?color=4a6cf7)](https://github.com/01Virex/dsh-status-rotator)
[![license](https://img.shields.io/github/license/01Virex/dsh-status-rotator)](LICENSE)
[![status](https://img.shields.io/badge/status-stable-2ecc71)](https://www.npmjs.com/package/dsh-status-rotator)

## Quick start

```bash
dsh plugin --profile web add dsh-status-rotator   # 1. install (the package ships its own bundle manifest)
dsh web                                            # 2. restart once, first install only
```

3. Open **Settings → Status Texts** (bottom left): toggle theme packs, edit phrases, tune the gradient and danmaku — every change saves and applies live, no refresh.

A [DeepSeek Harness (dsh)](https://github.com/deepseek-ai/deepseek-harness) client plugin that replaces the hardcoded `Deep diving...` / `深度求索中...` status line in the Web UI's turn footer with your own phrase bank: phase-aware switching, typewriter output, timed rotation, weighted random picking, template placeholders with live values, an animated rainbow gradient with separate day/night palettes, video-site-style danmaku, and a real-time engine that feeds the phrases and the browser tab title. The elapsed-time clock of the UI is left untouched.

> **Status line as of dsh 0.1.7**: the host moved the running status into the turn's fold header `button[data-turn-process]` (`Deep diving for 12s` / `深度求索中，用时12秒`, long gone from the viewport in a long turn). The plugin moves the status line **back to the old position** — just above the input box, below the conversation, left-aligned with the message column (mirroring dsh ≤0.1.6's `.turnStatus`: 26px tall, built-in shimmer, clock 13px + 8px gap), pinned with the composer so it stays visible; the header copy is hidden to avoid duplicates and the host's own `Took 12s` / `Worked` returns once the turn ends. Duration and phase are still read from the header label text (React rewrites it wholesale every second — the plugin never writes into it), and the screen-reader announcement span is left alone. On 0.1.6 and older the `role="status"` status line already sits in that position and behaves as before.

## Feature Overview

**Core**

- **Status swapping** — the `Deep diving...` label (or the `Deep diving for 12s` running label since 0.1.7) is replaced by your phrases, rotated every `intervalMs`, typed out character by character (`typeSpeedMs`, `0` disables the typewriter);
- **Phase-aware** — separate phrase sets for `thinking` / `running` / `long`; `thinking` covers the first 15 seconds of a turn, then the phase follows the elapsed time, without waiting for the rotation interval;
- **Weighted random** — any phrase may carry a weight; picking follows the weights (`weightedRandom: false` falls back to fully uniform);
- **Zero-intrusion targeting** — locates the status label by `role="status"` + `aria-live="polite"` on older hosts and by `button[data-turn-process]` on 0.1.7+; there the plugin only inserts its own line inside the composer seat, hides the header copy, and reads the header label text for the duration — chat-history code snippets, other aria-live regions and the host clock are never touched.

**Content**

- **Phrase bank separated from code** — all phrases live in JSON files; editing them needs zero code and no restart;
- **Modular phrase packs** — phrases are grouped into named packs (`packs[]` + `enabledPacks[]`) that merge into the effective bank with text-dedup; the settings page toggles packs and edits each one independently;
- **Template placeholders** — `{elapsed}`, `{phase}`, `{phaseLabel}`, `{locale}`, `{date}`, `{time}`, plus live-engine values `{model}`, `{provider}`, `{tps}`, `{pending}`, `{tools}`, `{running}`;
- **Multilingual** — phrases switch live between Chinese and English following Settings → Language; unknown languages fall back to Chinese;
- **Community phrase bot** — a GitHub-issue form with an automatic validator and auto-PR (see [Contributing Phrases](#contributing-phrases-via-github-issues)).

**Visuals**

- **Rainbow gradient** — text rendered with an animated gradient; separate day (light) / night (dark) palettes that follow the interface theme (or force one with `mode`); colors and speed configurable, one switch to turn off;
- **Danmaku** — every phrase can also fly across the page as bullet-screen comments; random size, per-bullet random rainbow colors, adjustable opacity and z-index.

**Live**

- **Real-time status engine** — subscribes to the dsh session snapshot (session list, conversation snapshot, model RPC) with a DOM clock fallback — one source feeding phrases and the tab title;
- **Browser tab title** — rotates `document.title` through your templates, restores the original title when idle (configurable);
- **Presets & scheduling** — multiple named phrase banks with their own config, switched from the settings page or automatically by time-of-day / weekday rules.

**Workflow**

- **Auto-loading** — the node half registers an HTTP route to serve `config.json`; no localStorage or deployment needed;
- **Hot reload** — while the page stays open the config is re-read periodically and immediately when you switch back to the tab;
- **Persistent storage** — saved edits are written into the official dsh settings store (`$DSH_HOME/settings.yaml`), surviving plugin upgrades;
- **Settings page** — a "Status Texts" page in DSH's Settings with visual editing for the Chinese/English × three-phase phrase banks; saves take effect immediately.

## Installation

Two ways to install: the recommended `dsh plugin add` command, or the manual copy. Either way, restart `dsh web` once after the first install.

### Option A: `dsh plugin add` (recommended)

The plugin's `package.json` declares a `dsh.bundle.patch` manifest, so it is recognized automatically after install — no extra flags needed. The command syntax is `dsh plugin --profile <name> add <package>` (e.g. `--profile web`):

- **From npm** (easiest): `dsh plugin --profile web add dsh-status-rotator` ← always installs the latest release
- **From a clone**: `dsh plugin --profile web add ./dsh-status-rotator`
- **From a release package**: download `dsh-status-rotator-<version>.zip` from the Release page (it contains a ready-to-use plugin directory with `config.json` — **not** an npm tarball), unzip it, then `dsh plugin --profile web add /path/to/dsh-status-rotator`.

### Option B: manual install

1. Put this project directory under your profile's node_modules (default `C:\Users\<you>\.dsh\profiles\node_modules\dsh-status-rotator\`);
2. Insert the following into the profile's `cordis.patch.yml`:

   ```yaml
   - insert:
       - id: status-rotator
         name: dsh-status-rotator
   ```

3. Run `node gen-config.cjs` to initialize the local `config.json` (copied from `config.example.json`);
4. Restart `dsh web` and hard-refresh the browser with Ctrl+F5.

### First run

On first start the plugin serves, in order: your **saved settings** (`$DSH_HOME/settings.yaml`, namespace `status-rotator`) merged over the `config.json` sitting next to the package — or over `config.example.json` when that file is absent, which is the case for npm installs (all 1092 default phrases live inside it — see [Phrase Bank](#phrase-bank)) — plus two bank layers on top: an **auto-updated bank** pulled from upstream every 6 hours (see [Auto-