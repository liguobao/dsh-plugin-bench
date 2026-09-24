<h1 align="center"><img src="https://raw.githubusercontent.com/lcestou/dsh-oh-my-claude/main/docs/media/spark.svg" alt="" width="22" height="22"> Oh My Claude</h1>

<p align="center">
  English | <a href="README.zh.md">中文</a>
</p>

<p align="center">
  <strong>Claude Code, native inside dsh</strong>
</p>

<p align="center">
  <em>Drive your logged-in Claude Code CLI as a first-class dsh provider: no API key, no extra services, no runtime dependencies.</em>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/dsh-oh-my-claude"><img src="https://img.shields.io/npm/v/dsh-oh-my-claude?style=flat&color=cb3837&logo=npm" alt="npm version" /></a>
  <img src="https://img.shields.io/badge/host-dsh-6c5ce7?style=flat" alt="dsh" />
  <img src="https://img.shields.io/badge/drives-Claude%20Code%20CLI-d97757?style=flat" alt="Claude Code CLI" />
  <img src="https://img.shields.io/badge/language-TypeScript-3178c6?style=flat&logo=typescript" alt="TypeScript" />
  <img src="https://img.shields.io/badge/build-Bun-f472b6?style=flat&logo=bun" alt="Bun" />
  <img src="https://img.shields.io/badge/runtime%20deps-zero-45cfa0?style=flat" alt="Zero runtime dependencies" />
</p>

<p align="center">
  <sub>Built with AI assistance, and open to more. Contributions from AI coding agents are welcome; start with <a href="https://github.com/lcestou/dsh-oh-my-claude/blob/main/CONTRIBUTING.md">CONTRIBUTING.md</a>.</sub>
</p>

---

Claude Code CLI as an LLM provider for [dsh](https://github.com/deepseek-ai/dsh). Every request drives `claude -p` with stream-json in and out, so it uses whatever login, hooks, CLAUDE.md files, MCP servers and rate limits Claude Code already has. No API key needed. The plugin speaks the CLI's own protocol (the one the Agent SDK wraps) directly, so it has no runtime dependencies.

## Tour

<p><img src="https://raw.githubusercontent.com/lcestou/dsh-oh-my-claude/main/docs/media/shield-menu.png" width="640" alt="dsh's access shield in a Claude session: Plan, Ask, Accept edits, Auto, Don't ask and Bypass rows with dsh's own icons"></p>

The shield is dsh's own control. In a Claude session its rows become Claude's six permission modes, each labelled with the dsh access level it sets underneath.

<p><img src="https://raw.githubusercontent.com/lcestou/dsh-oh-my-claude/main/docs/media/panel-tabs.gif" width="640" alt="the Oh My Claude panel switching between its Memory, Rewind, Changes and Asides tabs"></p>

One `✻` button beside the composer opens the whole plugin: Memory, Instructions, Skills, Rewind, Changes, MCP, Asides, Diagnostics, Tasks and Tune, plus a Restore tab while the session is still blank.

<p><img src="https://raw.githubusercontent.com/lcestou/dsh-oh-my-claude/main/docs/media/panel-changes.png" width="640" alt="the Changes tab listing the working tree diff with per-file line counts"> <img src="https://raw.githubusercontent.com/lcestou/dsh-oh-my-claude/main/docs/media/panel-asides.png" width="640" alt="the Asides tab with a side question expanded above the tab strip"> <img src="https://raw.githubusercontent.com/lcestou/dsh-oh-my-claude/main/docs/media/panel-mcp.png" width="640" alt="the MCP tab's add-server form, filled with a server name, command and argument list"></p>

<p><img src="https://raw.githubusercontent.com/lcestou/dsh-oh-my-claude/main/docs/media/cost-row.png" width="640" alt="dsh's footer stats row ending with the Claude session cost and cached token count"></p>

Cost and cached token count, two figures dsh cannot compute, join dsh's footer stats row. The pill turns orange once a session passes the spend line you set. The dollar figures are what the turns would cost at API rates; on a Claude subscription you are not billed them.

<p><img src="https://raw.githubusercontent.com/lcestou/dsh-oh-my-claude/main/docs/media/context-usage.png" width="300" alt="dsh's context ring popover with Claude plan windows and the CLI's own context breakdown"> <img src="https://raw.githubusercontent.com/lcestou/dsh-oh-my-claude/main/docs/media/phone-panel.png" width="300" alt="the panel as a phone sheet above the composer"></p>

Plan usage and the CLI's own context breakdown live in dsh's context ring popover. On a phone the panel becomes a sheet.

<p><img src="https://raw.githubusercontent.com/lcestou/dsh-oh-my-claude/main/docs/media/add-workspace.png" width="640" alt="dsh's Select Workspace Directory dialog with a box dropdown in its footer listing This box and an ssh box"></p>

Once an SSH box is saved, dsh's own Add workspace dialog gains a box dropdown: a folder on that box becomes a workspace here, and the session in it runs Claude Code there.

<sub>Shots by <code>tools/playwright/tour.ts</code>.</sub>

## Install

You need the Claude Code CLI on `PATH` and logged in (`claude --version` works, `claude` opens without asking you to sign in), and dsh 0.1.5-rc.1 or newer. Nothing else: no API key, no Node build step.

```sh
dsh plugin --profile web add dsh-oh-my-claude                        # from npm
dsh plugin --profile web add github:lcestou/dsh-oh-my-claude         # or straight from the repository
systemctl --user restart dsh-web.service   # or restart `dsh web` however you run it
```

The package declares a dsh bundle, so `dsh plugin add` registers it in the profile by itself. After the restart, "Oh My Claude" appears in the model picker with the models your login can use. Pick one and chat.

The plugin speaks English and Chinese and follows dsh's own language setting (Settings → General → Language), switching as soon as you change it.

If the picker lists it as `Oh My Claude (not logged in)`, run `claude auth login` in a terminal on the box that runs dsh, or press Log in under Settings → Oh My Claude → Boxes.

**DSH Desktop** (macOS and Windows) installs and updates plugins from its own Plugins page, not the `dsh plugin` command: add `dsh-oh-my-claude` there and restart when it asks. The plugin looks for `claude` in the usual install folders, since an app started from the Dock does not see your shell's PATH. On Windows it runs Claude as a plain child of dsh, so restarting the app ends a running turn, and the parts that need a Unix shell (Log in from Settings, SSH boxes) are not available. The server half has been run under Electron on Linux the way Desktop runs it; a real Mac or Windows install has not been tried yet.

When a newer version is on npm, an orange pill with the version number appears in Settings and on the panel's Runtime line; a click copies the update command. Details, and the one repair a dsh upgrade can call for, are under [Plugin updates](https://github.com/lcestou/dsh-oh-my-claude/blob/main/docs/how-it-works.md#plugin-updates).

Optional, in `~/.dsh/settings.yaml`:

```yaml
agent-default-model:            # make Claude Code the default for new sessions
  provider: claude-code
  model: claude-fable-5-1
subagent-model-selection:       # let dsh subagents run on Claude Code too
  enabled: true
  allowedModels:
    - provider: claude-code
      model: claude-haiku-4-5
```

Working on the plugin itself? Start at [docs/developing.md](https://github.com/lcestou/dsh-oh-my-claude/blob/main/docs/developing.md).

## Compatibility

dsh ships prereleases only and moves client APIs between them, so every release of the plugin records the dsh line it was written for and the dsh it was driven on. "Runs on" is the range the code carries branches for; "tested on" is the dsh installed on the box when the release was cut. The update pill reads the floor off the registry and never offers a release to a box whose dsh is below it.

| Plugin | Runs on dsh | Tested on dsh | npm tag |
| --- | --- | --- | --- |
| next (main, unreleased) | 0.1.5-rc.1 through 0.1.7-alpha.2 | 0.1.7-alpha.2 | none yet |
| 1.3.1 | 0.1.5-rc.1 through 0.1.6-alpha.2 | 0.1.6-alpha.2 | `latest`, `dsh-0.1.6` |
| 1.2.1 | 0.1.5-rc.1 through 0.1.6-alpha.2 | 0.1.6-alpha.2 | `dsh-0.1.5` |

## What you get

1. Any Claude model your login can use, in dsh's own picker. [Models](h