<h1 align="center">DSH Update Status</h1>

<p align="center">A read-only version badge and release-channel guide for the DeepSeek Harness Web sidebar.</p>

<p align="center">
  <a href="https://www.npmjs.com/package/dsh-update-status"><img src="https://img.shields.io/npm/v/dsh-update-status?label=npm&color=CB3837" alt="npm version"></a>
  <a href="https://github.com/idoall/dsh-update-status/actions/workflows/ci.yml"><img src="https://github.com/idoall/dsh-update-status/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-0F172A" alt="MIT"></a>
</p>

<p align="center">English | <a href="README.zh.md">中文</a></p>

<p align="center">
  <a href="#features">Features</a> ·
  <a href="#install">Install</a> ·
  <a href="#usage">Usage</a> ·
  <a href="#release-channels">Release channels</a> ·
  <a href="#lan--non-loopback-pages">LAN pages</a> ·
  <a href="#compatibility">Compatibility</a> ·
  <a href="#configuration">Configuration</a> ·
  <a href="#troubleshooting">Troubleshooting</a> ·
  <a href="#security-boundary">Security</a> ·
  <a href="#uninstall">Uninstall</a> ·
  <a href="docs/RELEASING.md">Release guide</a>
</p>

> DSH Update Status is a community plugin for DeepSeek Harness. It does not modify DSH core and it never installs, restarts, rolls back, downloads, or replaces DSH files.

It shadows only the expanded sidebar brand name with `DeepSeek` plus a compact version chip that fits the 24px brand row, leaving the official fish mark untouched. A green dot next to the version means there is nothing to do, and a breathing amber dot means a newer release is available. Tap the chip to inspect npm release channels, compatibility status, and a copy-only command for the selected channel.

<p align="center">
  <img src="./assets/update-panel.png" width="400" alt="DSH Update Status panel: cache duration, the running 0.1.7-rc.1 on the latest channel, a next row that does not match the followed channel, compatibility labels, and a copy-only upgrade command">
</p>

## Features

- **Visible version status** — shows the running DSH version in the expanded sidebar and a fallback action in the collapsed rail.
- **Quiet update signal** — a pending update never repaints the version chip. Only an amber dot with a soft halo next to the version breathes (scale + glow; the animation is disabled under `prefers-reduced-motion`), so a new release reads as one small light instead of a recoloured brand row.
- **Three dot states, one glance** — with nothing to do the dot beside the version is a plain **green circle** (the theme's success colour, not the text colour, so a dark shell no longer paints a dot that reads as "off"). While a check is running it is the neutral grey pulse; a pending update is the amber halo. Only the update state animates or glows, and only a failed status read repaints the chip, in red.
- **Neutral chip surface** — the chip is a grey second-level surface in both themes (`#f1f3f5` light / `#353638` dark) with the theme's normal label colour, so the dark shell gets a dark grey chip with white text rather than a white pill that hides the amber halo.
- **Light, dark, or system — followed automatically** — every colour the plugin renders is a DSH semantic token, so the chip, the dot, its halo, the footer ring and the panel all resolve through whatever appearance DSH is using. Set DSH to light, to dark, or to system and the plugin switches with the shell: no plugin-side theme setting, no media query to keep in sync. Hover lifts the chip in both directions (darkened in light mode, lightened in dark mode) by mixing the theme's label colour into the surface.
- **Stable and preview discovery** — reads npm dist-tags `latest`, `next`, and `alpha` in one registry request; `latest` is the default.
- **Useful choices only** — de-duplicates rows by version, keeps `latest` and the channel you follow, and never hides the channel that matches the release you are running.
- **In-panel channel selection** — select a meaningful stable, candidate, or preview release directly in the panel; the preference is stored by the DSH Host.
- **Compatibility labels** — explicitly verified versions are marked verified; unknown preview compatibility is marked unverified rather than claimed safe.
- **Copy-only guidance** — generates an installation-kind-aware `@latest`, `@next`, or `@alpha` command but never executes it.
- **Cache without polling** — one Host check on mount, a configurable 30–1,440 minute cache, single-flight registry access, and no frontend polling. Only the Check for updates button bypasses the cache.
- **Mobile-safe panel** — uses a modal browser top layer so the scrollable, safe-area-aware bottom sheet stays above the DSH drawer.

## Install

Requirements:

- DeepSeek Harness with the Web profile
- Node.js 20 or newer
- Verified DSH releases: `0.1.7-rc.1` (latest RC) and `0.1.7-alpha.2`

With an installed `dsh` command:

```sh
dsh plugin --profile web add dsh-update-status@latest
```

From a DeepSeek Harness source checkout:

```sh
corepack enable
pnpm install
pnpm dsh plugin --profile web add dsh-update-status@latest
```

Restart the existing DSH process after installation, then refresh its Web GUI. Do not start a second Web server for this plugin.

Local development link:

```sh
pnpm install --frozen-lockfile
pnpm run build
dsh plugin --profile web add "link:$(pwd)"
```

## Usage

1. Open the DSH sidebar drawer. The official fish remains in place; the name row shows `DeepSeek` plus the current version badge.
2. Tap the badge. The update panel opens without triggering the parent New Session action.
3. Review the offered channels. Rows are de-duplicated by version, `latest` and the channel you follow are always listed, and the channel matching the release you are running stays selectable.
4. Select `alpha` or another channel to follow it. The choice is stored by the DSH Host and only affects future checks; an unverified preview stays clearly marked.
5. Copy the generated command and run it yourself in a terminal on the computer hosting DSH.
6. Restart DSH yourself after the package-manager command completes.

Example commands generated for a global install:

```sh
npm install -g @deepseek-ai/dsh@latest
npm install -g @deepseek-ai/dsh@next
npm install -g @deepseek-ai/dsh@alpha
```

The plugin displays one command that matches the detected installation kind and selected channel. It does not run these commands.

### What the dot means

The dot beside the version carries the whole status, and only the update state animates:

| Dot | State | Meaning |
| --- | --- | --- |
| green circle | up to date | The followed channel points at the running release. The chip keeps its normal fill. |
| grey pulse | checking | A status read is in flight (first mount, a channel change, or **Check for updates**). |
| amber dot with a halo | update | The followed channel points at a newer release. Copy the command, run it yourself, restart DSH. |
| chip turns red | failed read | The plugin could not determine the state: the registry read failed, the channel is unpublished, or the versions are not SemVer-comparable. An *unverified* release is not this case — it is an advisory shown only in the panel. |

<p align="center">
  <img src="./assets/sidebar-chip.png" width="300" alt="The version chip in a light shell (grey chip, dark text) and a dark shell (dark grey chip, white text), each showing the green up-to-date dot">
</p>

The chip itself is a neutral second-level surface — grey in both themes, with the theme's own label colour — so the amber halo always reads against it, and it never changes colour to announce an update.

## Release channels

| Channel | Purpose | Compatibility treatment |
| --- | --- | --- |
| `latest` | Default stable/candidate recommended by the DSH npm package | Verified only when explicitly declared by this plugin |
| `next` | Candidate release when it differs meaningfully from the running/stable releas