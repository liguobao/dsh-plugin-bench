# Zat-DSH Engine

> The visual plugin marketplace for DeepSeek Harness. Browse, search, install, update and uninstall community plugins — Wallpaper Engine style.

[English](#zat-dsh-engine) · [中文说明](README.zh.md)

Zat-DSH Engine adds a **Plugin Market** tab to **Settings → Plugins** in the DeepSeek Harness web GUI. It lists the entire `dsh-plugin` topic community from GitHub, shows bilingual intros, and installs plugins with one click.

## Features

- **Full community catalog** — live GitHub search of the `dsh-plugin` topic (1700+ repositories, growing daily)
- **AI plugin finder** — in any conversation just say what you need (e.g. "find me a plugin that lets the model see images") and the AI searches the market, recommends candidates, and reports each one's **pre-install health + security scan** (✅/⚠️/❌) — problems are reported honestly, nothing is blindly recommended
- **12 categories** — Theme, Tools, Browser, Skills, Vision, Network, Agents, Data, Hardware, Design, Security…
- **Live search** — type to filter, no Enter key needed; clearing the box returns to the full list
- **Bilingual intros** — 999 pre-translated Chinese intros bundled; new plugins keep their English intro (on-the-fly model translation is removed — with peak/off-peak pricing, mass-translating on store open could burn your balance); English UI shows the original GitHub description
- **Install / Update / Uninstall** — one click, powered by the official `dsh plugin` profile mechanism (`pnpm` under the hood)
- **Monorepo-aware install** — repositories that bundle several plugins install correctly: a single-plugin repo installs silently, multi-plugin repos offer a plain-language picker
- **Installed detection** — marks plugins you already have, with version comparison and an **update badge** when a newer version is released
- **Cross-platform** — full Windows and Linux support (PowerShell / sh, curl / wget, system-proxy aware)
- **Network auto-adaptation** — inherits your VPN/system proxy for fetching and installing; if GitHub is unreachable, requests automatically fall back to `gh-proxy.com` and recover. **Works without a VPN**: proxy → direct → mirror → built-in fetch fallback
- **One-click enable/disable** — toggle plugins right on the card (official core and the market itself are protected)
- **Pre-install conflict gate + 🩺 health check** — blocking two marketplaces at once, official-package hijack, duplicate patch rows / registered names; one-click health report on conflicts and dependency issues
- **Pre-install health + security scan** — every candidate is checked before install (entry files, build artifacts, dependency style, network destinations, OS support); the security scan catches obfuscation/credential theft/exfiltration but only warns (no false positives); objective issues (missing entries, unsupported OS) are blocked
- **One-click check + repair** — detects network/pnpm/entry/OS/past-error problems in one click, auto-fixes what it can (installs pnpm, enables plugins, fills deps), and explains the rest
- **Safe by default** — install/uninstall/toggle roll back automatically on failure; a last-known-good backup restores a broken profile with one command
- **Live progress bar** — install/update/uninstall show a bar right on the card (percent + live counts); progress survives leaving and re-entering the market
- **One-click star** — reuses your local git credentials to star repos; badge color legend, auto-fading notices
- **Self-update** — a button appears beside the title when a newer version of the marketplace itself is available

## Installation

> ⚠️ **Install it with the command below — do NOT hand-edit any patch file.**
> Letting an AI "install" this project by pasting the repo URL and manually editing `cordis.patch.yml` breaks dsh: the market's own `plugin-market` row is auto-mounted by dsh from the bundled patch, and writing it by hand into two places (`app.asar.unpacked/cordis.patch.yml` and `~/.dsh/profiles/<profile>/cordis.patch.yml`) duplicates the id and makes dsh fail to start. If dsh already won't start, delete the hand-written `plugin-market` row from your profile's `cordis.patch.yml` and reinstall with the command below.

### From GitHub (recommended, after release)

```sh
dsh plugin --profile web add github:mishibeikejie/zat-dsh-engine
```

### From China without a VPN (via the domestic mirror, verified)

```sh
dsh plugin --profile web add https://gh-proxy.com/https://github.com/mishibeikejie/zat-dsh-engine.git
```

Either command installs the same plugin. Once installed, the market's own search and install paths carry the mirror fallback, so networking is handled for you.

### From a local checkout

```sh
git clone https://github.com/mishibeikejie/zat-dsh-engine.git
dsh plugin --profile web add ./zat-dsh-engine
```

### From npm (if published later)

```sh
dsh plugin --profile web add zat-dsh-engine
```

Replace `web` with your profile name if you use a different one (`headless` etc.).

> Requirements: a working dsh installation, `pnpm` and `curl` on PATH, and a profile that has been initialized (`dsh plugin --profile web add` creates it on first use).

## Usage

1. Restart dsh after installing.
2. Open the web GUI → **Settings → Plugins**.
3. Click the **🛒 Plugin Market** tab on the right of the plugin list.
4. Browse, search, filter by category or install state, and click **Install** on any card.
5. Restart dsh to activate installed plugins.

## Update

```sh
dsh plugin --profile web add github:mishibeikejie/zat-dsh-engine
```

Re-running `add` updates to the latest commit. The marketplace also detects its own updates and shows an **Update** button beside the title.

## Uninstall

```sh
dsh plugin --profile web remove zat-dsh-engine
```

## FAQ

**The market shows at most 1000 plugins in the All view.** GitHub's search API caps any query at 1000 results. Search and category filters reach every plugin regardless.

**Why do some plugins have no Chinese intro?** 999 Chinese intros ship with the plugin. Plugins released after the snapshot keep their English description — live on-the-fly translation is removed, because with DeepSeek's peak/off-peak pricing, opening the store used to batch-translate every uncached plugin with your current model and burn your balance during peak hours.

**Is the mirror safe?** The mirror is only used when a direct GitHub request fails, and only for public repository metadata.

**dsh won't start after installing a plugin — how do I recover?** After every successful install/uninstall/toggle, the market backs up the last known-good state into the `zat-backup/` folder inside your profile directory. Restore it by copying the three files back over the profile directory.

In the commands below, `web` is your profile name: **everyone using the web GUI has the profile `web`** (unless you started dsh with a custom name — if unsure, open the market and look at the "Profile:" line in the footer; use whatever it says):

```sh
# Windows (PowerShell)
Copy-Item "$HOME\.dsh\profiles\web\zat-backup\*" "$HOME\.dsh\profiles\web\" -Force

# macOS / Linux
cp ~/.dsh/profiles/web/zat-backup/* ~/.dsh/profiles/web/
```

Then start dsh again. This restores the state right after the last successful operation, so the plugin that broke startup is removed from the enabled list and the profile boots normally.

**Can I install two marketplace plugins at once?** No — the install gate blocks it: two market/manager plugins register the same settings pages and services, which can take dsh down. Uninstall the current one first if you want to switch.

## Permissions & trust (security-review perspective)

This marketplace is at heart a **package manager**, and that job itself requires strong capabilities. A security review will always see the behaviors below — here is what each one is for and where its boundaries are:

- **Running shell commands**: install/update/uninstall means running pnpm. The market only runs the pnpm/curl/wget/powershell commands it assembl