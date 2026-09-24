<p align="center">
  <img src="docs/assets/dsh-switchboard-gui.png" alt="DSH Switchboard showing a local Profile health check, pending Bundle plan, Bundle inventory, and recent activity" width="920">
</p>

<h1 align="center">DSH Toolbox</h1>

<p align="center">
  A local-first toolbox for DeepSeek Harness.<br>
  Product research, context switching, plugin preflight, and compatibility monitoring in one safety-focused visual control panel.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/DSH-0.1.1--rc.2-0b6ff4?style=flat-square" alt="DSH 0.1.1-rc.2">
  <img src="https://img.shields.io/badge/Node.js-22.19%2B-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node.js 22.19+">
  <img src="https://img.shields.io/badge/local--first-SQLite-168f91?style=flat-square&logo=sqlite&logoColor=white" alt="Local-first SQLite">
  <img src="https://img.shields.io/badge/license-noncommercial-d63d4b?style=flat-square" alt="Noncommercial license">
  <a href="https://github.com/HiWhaleW/dsh-toolbox/actions/workflows/ci.yml"><img src="https://github.com/HiWhaleW/dsh-toolbox/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
</p>

<p align="center">
  <a href="https://dsh-toolbox.lisongyang0130.chatgpt.site"><strong>Live interactive demo</strong></a>
  ·
  <a href="#five-minute-installation"><strong>Five-minute installation</strong></a>
  ·
  <a href="https://github.com/HiWhaleW/dsh-toolbox/issues"><strong>Report an issue</strong></a>
</p>

> [!NOTE]
> The online version is a safe demo: health checks, Bundle toggles, change plans, activity, and rollback are simulated in the current browser's memory and reset on refresh. It never connects to a visitor's computer or reads DSH Profiles, API credentials, or SQLite data. Install the local version to connect to a real DSH workflow.

> [!IMPORTANT]
> **Experimental MVP · Noncommercial use only.** DeepSeek Harness remains in Developer Preview, and upgrades may affect Profile Bundle compatibility. This project is independently developed and is not affiliated with or endorsed by DeepSeek.

## What is DSH Toolbox?

DSH Toolbox is a DeepSeek Harness companion for individual, local-first workflows. Four plugins run as native DSH Profile Bundles. DSH Switchboard runs outside the active Harness process to inspect Profiles, run health checks, preview Bundle changes, create backups, and roll changes back safely.

There are no accounts, hosted backends, behavioral analytics, telemetry, background registry checks, or automatic upgrades by default. Real runtime data stays in local SQLite. Profile changes always begin with a plan, require user confirmation before writing, and leave an auditable transaction record.

## Five components

| Component | Everyday use | Tools |
| --- | --- | ---: |
| [`@dsh-toolbox/product-research-workbench`](packages/product-research-workbench) | Import URL or text evidence, organize findings, evaluate opportunities, back up projects, and generate Markdown/HTML reports. | 12 |
| [`@dsh-toolbox/context-switchboard`](packages/context-switchboard) | Route tasks into bounded contexts, activate native runtime context, and support rollback. | 10 |
| [`@dsh-toolbox/plugin-preflight`](packages/plugin-preflight) | Inspect local Bundles before installation for package semantics, capabilities, policy, SBOM data, and fingerprints. | 2 |
| [`@dsh-toolbox/compatibility-radar`](packages/compatibility-radar) | Discover Bundles, compare them with a target runtime, save and compare snapshots, and generate upgrade reports. | 7 |
| [`@dsh-toolbox/dsh-switchboard`](packages/dsh-switchboard) | Discover DSH Profiles, inspect Bundles, plan and validate changes, create backups and reports, and roll back safely. | CLI / control plane |

The first four components are independently installable DSH Profile Bundles. The fifth is the unified local control plane. Product Research Workbench and related reports support Markdown and HTML output, while runtime data is stored in SQLite by default.

## Online demo vs. local installation

| Capability | Online demo | Local installation |
| --- | --- | --- |
| Explore four views and a fixed activity sidebar | Available | Available |
| Switch Profiles, filter activity, and review Bundle plans | Simulated in browser memory | Connected to real local data |
| Run `dsh --dump-config` health checks | Simulated success result | Real command execution |
| Write Profiles, create backups, roll back, and generate reports | No writes; resets on refresh | Real execution after plan confirmation |
| Data destination | Current browser memory | SQLite and private directories on the user's computer |

## Requirements

- Node.js `^22.19.0 || >=24.0.0` (`node:sqlite` is built in)
- npm, for packing the local bundles
- `@deepseek-ai/dsh@0.1.1-rc.2`
- A local DSH profile you are allowed to modify

Read-only Switchboard inspection works without the DSH CLI on `PATH`. Applying or rolling back a change requires the CLI by default because a successful `dsh --profile <name> --dump-config` is the runtime safety gate.

The tested runtime combination is:

| Component | Tested version |
| --- | --- |
| DeepSeek Harness | `0.1.1-rc.2` |
| DSH Tools | `0.1.1-rc.2` |
| Cordis | `4.0.1` |
| Node.js | `24.x` and the declared `22.19+` range |

CI runs the full check and package dry-run matrix on Ubuntu with Node.js `22.19.0` and `24.x`. A separate `windows-latest` job verifies that Switchboard can detect and execute npm-installed `dsh.cmd` shims without enabling shell execution.

Install the pinned DSH CLI if it is not already available:

```sh
npm install --global @deepseek-ai/dsh@0.1.1-rc.2
dsh --version
```

## Five-minute installation

Clone the source, create the four npm tarballs, and install them into one DSH profile:

```sh
git clone https://github.com/HiWhaleW/dsh-toolbox.git
cd dsh-toolbox

mkdir -p dist
npm pack --workspace @dsh-toolbox/product-research-workbench --pack-destination dist
npm pack --workspace @dsh-toolbox/context-switchboard --pack-destination dist
npm pack --workspace @dsh-toolbox/plugin-preflight --pack-destination dist
npm pack --workspace @dsh-toolbox/compatibility-radar --pack-destination dist

dsh plugin --profile toolbox add ./dist/dsh-toolbox-product-research-workbench-0.2.1.tgz
dsh plugin --profile toolbox add ./dist/dsh-toolbox-context-switchboard-0.2.1.tgz
dsh plugin --profile toolbox add ./dist/dsh-toolbox-plugin-preflight-0.2.1.tgz
dsh plugin --profile toolbox add ./dist/dsh-toolbox-compatibility-radar-0.2.1.tgz

dsh --profile toolbox --dump-config
```

The final command should show all four bundle layers. Start DSH with the same profile:

```sh
dsh --profile toolbox
```

You may install only the tarballs you need. Packing does not execute plugin code and does not require repository dependencies to be installed. Direct checkout-path installation is also possible after `npm install` at the repository root, but tarballs match npm packaging semantics and are the validated portable flow.

Each package pins the small DSH tool-definition runtime needed for reliable out-of-tree installation. There are no install lifecycle scripts.

### Open the DSH Switchboard GUI

DSH Switchboard is a local settings app for DeepSeek Harness. It shows which Profiles and Profile Bundles are installed, checks whether a Profile can start, previews every change, and keeps a backup so the change can be rolled back safely.

The navigation opens four working views in the center panel:

- **DSH Profiles** — inspect a Profile, run its DSH health check, review installed Bundles, and plan enable/disable changes.
- **Plugins** — view the Bundle inventory and its compatibility status.
- **Activity** — inspect local plans, validations, applied changes, and rollbacks.
- **Settings** — review the detected DSH runtime and local data locations.

Recent activity remains visible on the right while you move between views. Long lists scroll inside their own panels, so the overall application frame stays fixed and readable.