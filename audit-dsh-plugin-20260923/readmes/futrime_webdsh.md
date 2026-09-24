# webdsh

[![webdsh — DeepSeek Harness in a browser tab, with no server and no install](https://capsule-render.vercel.app/api?type=rect&height=180&color=0:0d1117,55:15407e,100:2f81f7&text=webdsh&fontSize=68&fontColor=ffffff&fontAlignY=45&desc=DeepSeek+Harness+in+a+browser+tab+%C2%B7+no+server+%C2%B7+no+install&descSize=19&descAlignY=70)](https://dsh.zjzh.me/)

> DeepSeek Harness in a browser tab — the real agent, real Node, no server to run.

[![Live](https://img.shields.io/badge/live-dsh.zjzh.me-2ea44f)](https://dsh.zjzh.me/)
[![Deploy](https://github.com/futrime/webdsh/actions/workflows/pages.yml/badge.svg)](https://github.com/futrime/webdsh/actions/workflows/pages.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (`dsh`) is an
agent harness where everything is a plugin. `dsh web` runs a Node host and serves
a browser client to it. **webdsh is that, as static files** — the host runs inside
the page, and the agent's commands run in [WebContainers](https://webcontainers.io):
Node itself, in the tab.

- ⚡ **Nothing to run.** No server, no install, no local Node — the harness boots in the page.
- 🌍 **The container is online too.** The page's CORS policy is preloaded into every Node process it starts, so `fetch` inside the container retries a refused host through the proxy on its own — `http://example.com` answers there now, and it did not before.
- 🖥️ **Real Node, real Python.** `npm install` and `pip install` both work, and the terminal and the agent share one container.
- 💾 **Or a whole PC.** Settings → Machine swaps the container for [v86](https://github.com/copy/v86) and offers **128 machines** — the whole of v86's catalog, from a 512-byte bootsector game to Windows 2000, **127 of them booting with nothing to set up** — emulated x86, on its own screen, with the tool set that machine actually has.
- 🧭 **Or a browser.** The third machine is real tabs of the real web, and the assistant drives them three ways: the page structure (a labelled tree with a handle on everything clickable), the pixels, or JavaScript in the page itself. Multi-tab, with its own cookies and per-site storage that persist — and each tab is sandboxed into an opaque origin, so a page cannot reach this harness, its storage, or your keys. That is the browser's own rule, not a promise this build makes: every escape route comes back `SecurityError`, and `npm run test:browser` checks it.
- 🤖 **And it can be programmed.** One action per turn is the wrong shape for a table with twenty rows in it, so the browser machine also takes *programs*: `browser_task` runs `getByRole('button', {name: 'Save'}).click()`, retrying `expect`, frames, popups, dialogs, downloads and uploads in a named task space that keeps its pages, its variables and its login state between calls — with receipts, so a run that was interrupted halfway through a form can be asked what happened instead of repeated. The model's own code runs in an opaque origin of its own, holding nothing of this page: the same boundary that keeps a browsed site out keeps the script the model wrote out too.
- 🌐 **The PC is online.** A WISP relay by default, so the guest gets real TCP — `https://`, package managers, `ssh` — and without one the page itself is the router: it answers the guest's DHCP, DNS and pings and carries HTTP as browser `fetch`, through the same CORS policy the rest of the app uses. `wget http://example.com` works on an emulated Buildroot either way; the same URL from the container answers `fetch failed`.
- 👁️ **It can see.** Attach an image and the model reads it: oriented, capped and re-encoded to the route's budget by the browser's own decoder, with the source's EXIF and colour profile stripped on the way. A model you add yourself is asked what it accepts, so a vision model on your own gateway arrives with its eyes open rather than registered as text-only.
- 🧩 **Real plugins.** Install from npm, a tarball, GitHub, or a path — from the browser.
- 📦 **Real dsh.** The published `@deepseek-ai/*` packages, unmodified: 120 of 135 rows compose exactly as `dsh web` composes them.
- 🔒 **Yours.** Files, sessions and keys live in your browser's storage. Nothing is uploaded.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background

Nothing here is a fork of dsh. The agent loop, tool registry, model adapters and
the entire web client come from npm at install time; the only modification is a
`cordis.patch.yml` layer — the mechanism dsh documents for exactly this.

What this repository adds is the platform underneath: a synchronous POSIX
filesystem mirrored to IndexedDB (`src/vfs`), `node:*` implemented over it
(`src/node`), the runtimes a session can run on — WebContainers and an
emulated x86 PC (`src/runtime`), and a browser built out of sandboxed frames
(`src/browser`) — an in-page virtual server for `/api`, the CORS policy every
outbound request goes through and the network the emulated machine is given
(`src/net`), and the plugins this build ships (`packages/`).

Six composition rows are swapped, each because the shipped one names something a
page cannot have — or, in the shell's case, cannot honestly describe. Four more
are reconfigured rather than replaced, including the one that decides whether
this deployment can open a path at all. `npx tsx scripts/alignment.ts` prints
the whole difference.

## Install

Nothing to install — [open the page](https://dsh.zjzh.me/). To run it yourself:

```sh
npm ci
npm run build        # → dist/
node scripts/serve.mjs 4173
```

Node 22 or newer. `dist/` is plain static files with relative URLs, so it works
at a domain root, a project path, or a local directory.

## Usage

Open the page, choose a workspace, start talking. 42 models across six routes
are registered up front, so it answers before it asks you for anything.

Three things live in the sidebar:

- **Files** — the workspace, as the agent and the terminal see it. Drop files
  in; take a file, a directory or a tick-box selection back out. Click a path
  the assistant mentions to open it here.
- **Machine** — `` Ctrl+` ``. What this session runs on: a terminal for the Node
  container, the live screen for an emulated PC, the tab strip and address bar
  for the browser. Click the screen and the machine gets your keyboard and
  mouse; Escape gives them back. The browser's tabs are the same tabs the
  assistant is driving, not a second copy of them — what it clicks, you watch.
- **Settings** — which machine, which models, which CORS proxy, which plugins.

Both panels dock beside the conversation on a wide window and along the bottom
on a narrow one, and take width from it rather than covering it.

**Machines.** Settings → Machine offers three kinds: the Node container, a
**browser**, and **128** emulated PCs — the whole of [v86's
catalog](https://copy.sh/v86/), **127 of which boot with nothing to set up**.
The choice applies on the next load, because it decides which tools the
assistant gets: `jsh`, Node and Python in the container; `browser_navigate`,
`browser_snapshot`, `browser_click`, `browser_screenshot`, `browser_eval` and
the rest on the browser; `sh` or `dos` plus `vm_screenshot`, `vm_key`,
`vm_type`, `vm_mouse` and friends on a guest, whose disk shares nothing with
your workspace. A guest is offered the tools that
currently work on it and not the ones that would come back empty — no
`vm_screen` on a desktop with no text, no `vm_mouse` at a prompt that never
turned a mouse on. The one that is left, Arch, wants a host for its 9p tree —
open one from your computer and it stays in your browser, or point the setting
at a host that serves them. `npm run v86:catalog` prints the difference against
upstream; `npm run v86:boot -- --bundled --as-shipped` re-boots all 127. The
disks come from v86's own `copy/images`