# dsh-commandcode-provider

**English** | [简体中文](./README.zh-CN.md)

[![Awesome](https://awesome.re/badge.svg)](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin)
[![GitHub Repo stars](https://img.shields.io/github/stars/Mars-Sea/dsh-commandcode-provider?style=flat-square)](https://github.com/Mars-Sea/dsh-commandcode-provider/stargazers)
[![DeepSeek Harness](https://img.shields.io/badge/DeepSeek%20Harness-plugin-4D6BFE?style=flat-square)](https://github.com/deepseek-ai/deepseek-harness)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/Mars-Sea/dsh-commandcode-provider/pulls)
[![CI](https://github.com/Mars-Sea/dsh-commandcode-provider/actions/workflows/ci.yml/badge.svg)](https://github.com/Mars-Sea/dsh-commandcode-provider/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![npm](https://img.shields.io/badge/npm-@mars--sea%2Fdsh--commandcode--provider-blue.svg)](https://www.npmjs.com/package/@mars-sea/dsh-commandcode-provider)

Unofficial [DeepSeek Harness](https://deepseek-harness.github.io/deepseek-harness/) LLM provider plugin for **Command Code**, ported from [pi-commandcode-provider](https://github.com/patlux/pi-commandcode-provider) (MIT).

> This is a community integration. You need your own Command Code account and API key or subscription, and Command Code's terms apply. This project is not affiliated with Command Code, Inc.

## What you get

- **Plugin bundle** — install into any dsh profile with `dsh plugin add`; registers a `commandcode` provider route with a live model catalog.
- **Dedicated settings page** — API key, connection options, a live account-usage card, and a "Hide out-of-plan models" toggle.
- **Works in the terminal too** — the same install serves a [dsh-TUI](#terminal-ui-dsh-tui) profile, with its own **`/settings` → Command Code** page for the API key and the model controls.
- **Models-page key card** — the **Settings → Models → Command Code** card carries the key status, a paste field, and the sign-in button inline.
- **In-browser sign-in for keys** — start the official authorization flow (the same one `cmd login` runs) from the settings page; the approved key lands in the local credential service automatically. Manual paste remains the fallback.
- **Multi-account rotation** — when one account hits its usage limit, requests switch to the next account automatically. See [Account rotation](#account-rotation).
- **Flexible API key setup** — via the settings page, an environment variable, or the official CLI login file.
- **Model-picker annotations** — minimum plan, active deal or `FREE` badge, peak/off-peak state, image support, and context window; free models listed first.
- **Plan-aware picker** — models above your subscription tier are hidden by default (toggleable); an optional **Model allowlist** keeps only your favorites in the picker.
- **Reasoning-effort support** — models with selectable reasoning effort levels expose them in the picker.
- **Image input** — Vision-capable models accept images.
- **Plans & quota panel** — an optional Command Code card at the bottom of the sidebar (directly above Settings) shows the serving account's plan and its 5-hour and weekly windows; clicking it opens a dashboard with the billing period, both windows as progress bars with reset times, monthly credit consumption, and the purchased/free balances. The dashboard's **×** button hands the center column back to your conversation (the current session is untouched). **Off by default** — turn on *"Show the quota card in the sidebar"* under **Settings → Command Code → Advanced** to show it, and the same switch hides it again (a hidden card draws nothing at all and runs no background usage poll); the change lands as soon as you save. The panel follows your harness language (中文 / English) and needs dsh 0.1.5 (rc.1) or newer.
- **Session cost estimate** — published-rate estimates (`≈`) beside the composer token counter and in its usage dialog, using each request's model, request time and context tier from durable session history. Model switches and viewing the session later do not reprice earlier requests. Mixed-provider or unpriced usage shows a labeled subtotal (`≥`); missing history or wholly unpriceable usage stays hidden. These are estimates from the installed price snapshot, not provider invoices. Also English on every harness language.
- **Web search** — the dsh `web_search` tool is backed by the Command Code Provider API (`/alpha/web-search`) with the same key/endpoint as chat, so no separate search key or base URL is needed. See [Web search](#web-search).

See [Screenshots](#screenshots) below for what the UI looks like.

## Install

Pick the release line that matches your DeepSeek Harness version:

- **dsh 0.1.2-rc.1 or later** (the current 0.1.2 line — what `@latest` installs today):

  ```sh
  dsh plugin --profile web add @mars-sea/dsh-commandcode-provider@latest
  ```

- **Older dsh releases** (the 0.5.0 line and earlier, which use the rc-era Host/browser APIs) — the last plugin version supporting them is 0.9.1, installed by exact version. That line is no longer under active maintenance:

  ```sh
  dsh plugin --profile web add @mars-sea/dsh-commandcode-provider@0.9.1
  ```

> The `latest` tag points at the current 0.1.2-line plugin release. Users on the old 0.5.0-era Harness line must pin `@0.9.1` explicitly.

**pnpm 11 holds back new releases.** Its `minimumReleaseAge` defaults to 1440 minutes, so a version published less than a day ago is skipped and `@latest` resolves to the *previous* release — silently, with a success exit code. To install a release from the last 24 hours, name it exactly:

```sh
dsh plugin --profile web add @mars-sea/dsh-commandcode-provider@0.11.11
```

The same applies to every profile you install into, including the terminal UI below.

Fresh pnpm 10 marketplace generations are supported directly. Do not add a separate `@deepseek-ai/dsh-invariants` dependency; the plugin declares it as a Host peer so the active dsh profile remains the owner of Harness packages.

## Updating

Update with the same tag you installed with:

```sh
dsh plugin --profile web update @mars-sea/dsh-commandcode-provider@latest     # dsh 0.1.2-rc.1+
dsh plugin --profile web update @mars-sea/dsh-commandcode-provider@0.9.1      # older dsh (0.5.0 line, unmaintained)
```

Each profile updates separately — the terminal UI owns its own plugin list (see below):

```sh
dsh plugin --profile dsh-tui update @mars-sea/dsh-commandcode-provider@0.11.11
```

To move to a version published less than 24 hours ago, name it exactly as in Install above; pnpm 11's age gate resolves `@latest` to the previous release instead.

Then restart the web app.

## Getting an API key

The easiest path is the official CLI (Node.js 22+):

```sh
npm i -g command-code@latest
cmd login        # macOS/Linux; native Windows: cmdc login
```

Or skip the CLI: click **Sign in to Command Code** under **Settings → Command Code** — your browser opens the commandcode.ai authorization page (the same flow `cmd login` uses) and the key is stored in the local credential service when you approve. You can still create a key on the [Keys settings page](https://commandcode.ai/mars-sea/settings/keys) and paste it into **Settings → Command Code**, or `export COMMANDCODE_API_KEY="user_..."`.

> The sign-in flow needs the Host and your browser on the same machine (loopback callback). With a remote Host, paste the key manually; a literal composition-level `apiKey`, if set, still takes precedence over a signed-in credential.

## Verify it works

After restart, enter your API key in **Settings → Command Code** and save; **Settings → Models** shows a **Command Code** card, and the model picker lists the live catalog under **commandcode**. Send a message with a model your plan includes.

## Terminal UI (dsh-TUI)

The plugin also works under a t