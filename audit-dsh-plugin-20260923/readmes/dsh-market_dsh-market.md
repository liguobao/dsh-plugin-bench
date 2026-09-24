<p align="center">
  <img src="assets/logo.svg" width="96" alt="dsh-market logo">
</p>

# dsh-market

English | [中文](README.zh.md)

[![npm](https://img.shields.io/npm/v/dshmarket)](https://www.npmjs.com/package/dshmarket)
[![stars](https://img.shields.io/github/stars/dsh-market/dsh-market?style=flat)](https://github.com/dsh-market/dsh-market)

The plugin market inside DeepSeek Harness. Open Settings → **Plugin Market** → browse, search, one-click install.

![dsh-market](assets/demo-en.png)

One-click themes: install, switch live, no restart.

## Install

```sh
dsh plugin --profile web add dshmarket
```

Restart `dsh web`, then open **Settings → Plugin Market**.

**Requires dsh web 0.1.0-rc.6 or newer.** On an older host the market
disables itself and says so in the browser console rather than rendering
against primitives that are not there — if the Plugin Market entry never
appears, that is usually why. Worth checking when a desktop build bundles
its own dsh: it may be older than the one `npm` would give you (#139).

## What you get

- **Browse & search** the full community catalog (2300+ plugins, growing daily) — category filters, star counts, top/new sorting, bilingual descriptions that follow your UI language
- **Host-aware discovery** — cards show the DSH requirement declared by `engines.dsh` or lockstep `@deepseek-ai/dsh-*` peers; an opt-in filter hides only confirmed mismatches with the running host. Undeclared, malformed, unavailable, and GitHub-only entries remain visible rather than being guessed incompatible
- **Screenshots** — AppStore-style screenshots, auto-carousel when there's more than one, click to preview full-size: author-curated shots show right on the card (zero extra requests); plugins without curated shots fall back to automatic README extraction once you open the install dialog. Images load from GitHub hosting only
- **Comments** — every card opens the plugin's discussion thread in place. It is the same thread its pages on [dshmarket.com](https://dshmarket.com) and the [catalog](https://awesome-dsh-plugin.com) show, so a plugin has one conversation rather than three. Backed by GitHub Discussions through giscus: it loads when you open it, needs a GitHub account only to post, and the note above it says plainly that opening it contacts giscus.app and GitHub. On local dsh web, reading stays embedded while a dedicated GitHub action opens the exact discussion in a new tab for sign-in and posting, so the cross-site return never carries or depends on the host session
- **Favorites** — bookmark plugins and themes from Discover or the Themes tab; a dedicated Favorites tab lists them with search, sort, and install actions. Bookmarks persist in the profile's market state (`state.json`); entries that leave the catalog can be cleared in one click
- **Themes** — a dedicated tab for community themes and skins: install → active immediately, switch with one click (themes are mutually exclusive, your choice survives restarts), uninstall to revert
- **One-click install** — confirm the source, watch live progress; most plugins go live after a page refresh, no restart
- **Backup & restore** — export your profile's plugin list and configuration as readable JSON, import it on another machine, store it on WebDAV with daily auto-backup, or sync through a private GitHub Gist; restores **merge** (plugins installed after the backup are kept), validate before writing, and roll back on failure
- **Updates** — per-plugin update checks (npm version or pinned commit vs HEAD), one-click update, or update everything at once; the market updates itself the same way
- **Resilient GitHub routes** — in the China download region, Git refs, README content, and avatars each keep their own fallback order. The market remembers the last working route, switches only after transport/HTTP/payload validation fails, and rejects proxy error pages disguised as HTTP 200. If every built-in route fails, **Settings → Plugins → Plugin configuration → GitHub acceleration** accepts one persistent custom HTTPS prefix; `DSHM_GITHUB_PROXY` remains the operator-owned override
- **Public update API** — plugin-owned settings pages can use the versioned, capability-gated [update API v1](UPDATE-API-V1.md) (beta) instead of copying package-manager logic or depending on private Market UI responses
- **Uninstall** — two-step confirm; plugins installed this session are removed live
- **Hot disable / enable** — toggles write `- id: …` + `disabled: true|false` into the profile's `cordis.patch.yml` (the official patch layer, mechanism ported from [dsh-plugin-hub](https://github.com/Noob-stupid/dsh-plugin-hub)): DSH's HMR re-composes within ~1s, no restart, and the loader re-applies the choice on every boot; hand-edited patch rows show as badges, host-infrastructure plugins are protected from toggling, and a malformed patch file is never made worse
- **Restart when needed** — changes that cannot hot-load show a one-click restart beside the pending-change banner; the action is restricted to same-origin loopback requests
- **Recovery when a restart does not come back** — DSH's boot is all-or-nothing: one plugin that cannot load stops the whole process, and the market's own UI dies with the host it was serving from. Now that failure prompt offers **Adjust plugins**: the ones DSH blamed are marked red and left unticked, you choose what should be enabled at the next start, the choice is written through the same `cordis.patch.yml` rows the market's own toggles use (plus `dsh.profile.bundles` for a disable-carrier), and the boot is retried. It is served by the detached restart helper on the same address the page was already polling, so it works even though the host is gone — and opening the URL fresh renders a standalone version of the same page. When DSH starts normally, none of it appears
- **Zero jargon** — if a component is missing (pnpm), the market detects it and offers a one-click automatic setup
- **Log export** — one click produces a sanitized plain-text log for bug reports (home paths and credential shapes are masked; nothing is ever sent anywhere). The market's version sits next to the page heading, so a screenshot of a problem already carries it
- **Settings card** — on dsh 0.1.0-rc.7 and newer the market manages *itself* from **Settings → Plugins → Plugin configuration**, next to every other plugin: see the running version, pick a **release channel** (stable, or beta to try builds still being verified — the market only, never your other plugins; a third *dev* channel appears once developer mode is switched on, and carries builds published straight off a branch), update, or remove the market — with an opt-in cleanup that also drops the disable rows it wrote, so plugins it switched off start running again rather than staying off with no UI left to switch them back on
- **Diagnostics** — the plugin load order and conflict surface, one page: bundle stack with official/community badges, duplicate loader entries, dependency version mismatches, multi-version core packages, overrides and invalid config entries. Plain-language terms, problem blocks highlighted, everything collapsible

- **Load order** — drag community bundles into the order you want, or take the suggested one derived from the plugins' own before/after rules. Nothing is written until a trial composition passes, and the panel tells you what the new order would change (overrides, invalid or duplicate entries) before you apply it
- **AI fix** — one click copies a diagnostics-driven fix prompt (errors/warnings/order conflicts + conservative scope instructions) to the clipboard; you paste it into a new conversation and decide whether to send. The prompt first asks the agent to detect whether it is itself the harness running this profile — if so it hard-forbids mutating the live composition, upgrading/restarting the harness or core packages, or reinstalling deps, and instead has it write an idempotent `apply` script plus a `rollback` script, h