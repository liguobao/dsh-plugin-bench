# 🎨 dsh-genui

<div align="center">

**English** · [简体中文](./README.zh-CN.md)

<br>

[**Open the live product site**](https://omdsh-dev.github.io/dsh-genui/) · [**Watch the real demo**](#watch-the-real-interface) · [**Install in DSH**](#quick-start)

</div>

> Give the model's answers a face — the text is still there, and an interactive UI is already live.
>
> 🔌 Ecosystem: the repo carries the `#dsh` · `#dsh-plugin` topics — welcome to be listed by @dsh-plugin.

`dsh-genui` turns a model reply into a **safe, interactive DSH surface**. Ask “how are this month’s orders doing?” and the answer can include a sortable data panel, a native video, a draggable plot, a local quiz, or a persistent session panel — without replacing the surrounding text.

## Start with the evidence

| If you want to… | Go straight to… | What you can verify |
|---|---|---|
| See the complete DSH flow first | [40-second real walkthrough](#40-second-walkthrough) | Components are rendered inside a real DSH conversation. |
| Inspect concrete UI outputs | [Three real outputs](#three-real-outputs-inside-a-dsh-reply) | Monitoring, function plots, and composable layout primitives. |
| Try it in your own DSH | [Quick start](#quick-start) | A public npm install, a prompt to run, and an activation check. |
| Learn the JSON language | [Component syntax](./SKILL.md) | The supported, guarded `dsh-ui` component specification. |

## Watch the real interface

> **No concept mockups.** The recording and images in this section are captured from `dsh-genui` rendering in the DSH interface. Use them to see the actual visual language before installing.

### 40-second walkthrough

<div align="center">

https://github.com/user-attachments/assets/f5db33ec-7471-4d4a-a85b-79c9962ab4ef

</div>

<p align="center">
  <a href="./assets/demo.mp4"><img src="./assets/demo-thumb.png" width="92%" alt="Preview of the complete dsh-genui walkthrough video"></a>
  <br><em>Click the preview to download the original MP4 if the GitHub player is unavailable.</em>
</p>

The walkthrough moves from an answer-embedded panel through forms, plotting, Mermaid, and 3D-oriented components. The player does **not** auto-play. If it does not load, use the [original MP4](./assets/demo.mp4); the four-step prompt sequence is documented in [demo-prompts.md](./demo-prompts.md).

### Three real outputs inside a DSH reply

#### 1. A monitoring panel is an answer, not a separate dashboard

<p align="center">
  <img src="./assets/showcase-panel.png" width="92%" alt="Real dsh-genui monitoring panel rendered inside a DSH conversation">
  <br><em>Real output: refresh/reset controls, time-range selection, statistics, charts, and a service table live inside the assistant reply.</em>
</p>

#### 2. A function plot redraws locally as its parameters change

<p align="center">
  <img src="./assets/showcase-plot.png" width="76%" alt="Real dsh-genui function plot with draggable parameter sliders">
  <br><em>Real output: `plot` renders curves while sliders, reset, and animation controls update the graph locally.</em>
</p>

#### 3. Layout primitives compose into structured work surfaces

<p align="center">
  <img src="./assets/showcase.png" width="76%" alt="Real dsh-genui layout and card component composition">
  <br><em>Real output: typography, grid, card, and row/column primitives combine into a hierarchy the model can describe declaratively.</em>
</p>

---

## ⚠️ Read this first: dual-channel rendering (no host source patch required)

The plugin ships **two rendering channels** and picks one automatically after the host activates its browser module:

- **Registry channel**: when the host exposes the `fence-registry` extension point (newer dsh builds), fences register through the host's streaming render pipeline and behave seamlessly with the host;
- **DOM channel**: when the host lacks that extension point (including supported stock DSH builds), the plugin observes the session DOM and mounts its own render tree. Since 0.7.2 it **supports streaming rendering**: components appear as the model writes them — the first finished component shows up immediately, no need to wait for the whole reply. Since 0.8.3 fence discovery is **multi-surface**: it matches the stock `md-code-block` surface, the deepsuite-style `.code-block` / `.code-block-small` surfaces some host builds render instead, and — as a structural backstop — any element whose banner labels it `dsh-ui` and contains a `<pre>` body. If your dsh build renders fences with a different class name, they still render (and a one-time console warning tells you the host DOM drifted).
- **DSH 0.1.7 generic code banner**: when the host's final DOM omits fenced-code language metadata, dsh-genui reads the current assistant's original Markdown from the public ChatSnapshot and only takes over `dsh-ui` fences. The DOM identifies the mount location. If source data is temporarily unavailable, a settled assistant CodeBlock can use the strict canonical GenUI validation as a final fallback.

Whichever channel is active, components, interactions, panels, and persistence behave identically.

CI's packed host smoke installs the generated npm tarball in a real DSH host and verifies host startup and rendering. Source-backed fence routing is covered by integration tests; the smoke does not claim to validate a real model response. Real-model E2E requires configured model credentials.

The repository ships both renderer channels, the host plugin, and the built browser bundle. The host still owns **client activation** and must provide the `slots` and `sessions` services. A downloaded `client.js` or a ModuleLoader cache entry proves only that bytes arrived — successful activation always prints `[genui] client active; fence-channel=registry|dom`. If that line is absent, fix package/profile identity or host activation first; DOM attributes such as `data-streaming` and `data-chat-anchor-key` are optional fallbacks, not installation prerequisites.

---

## ✨ Before vs. after

| Plain answer | With dsh-genui |
|---|---|
| "Revenue this month: ¥128,430, +12.4% MoM — watch the conversion rate." | One line of analysis + three stat cards (revenue / orders / conversion), a trend chart, and a progress bar rendered right beside it |
| Want to see more? Type another question. | The panel already has "Refresh" / "Switch view" buttons — click, and the model updates the data |

## 🚀 Quick start

Prerequisites — all required:

1. **dsh `^0.1.2-rc.1 || ^0.1.5-alpha.1 || ^0.1.6-alpha.1 || ^0.1.7-alpha.1`** (verified host tags: `dsh-v0.1.2-rc.1`, `dsh-v0.1.7-alpha.1`, and `dsh-v0.1.7-alpha.2`; users on DSH `<=0.1.1-rc.x` should use dsh-genui `0.9.8`)
2. **`pnpm` on your PATH**: the `dsh plugin` command depends on it. If missing: `corepack enable` (or `npm i -g pnpm`), then **open a new terminal** and confirm `pnpm -v` prints a version

Install and activate in DSH (one command, all dependencies included):

```sh
# Public npm package (works without an npm account)
dsh plugin --profile web add @changfenhuang/dsh-genui
```

To add it only as a Node dependency in an existing project:

```sh
npm install @changfenhuang/dsh-genui
```

> `npm install` only adds the dependency; it does not register the plugin with DSH. Use `dsh plugin add` above when installing it into DSH.

> ⚠️ **Don't use `link:` on a freshly cloned directory** — `link:` does not install the plugin's dependencies (mermaid / three / react), so the renderer will break. Use the npm command above for normal installation; reserve `link:` for local development iteration (see below).

### Migrating from the old `@omdsh-dev` package name

If you installed from `github:omdsh-dev/dsh-genui` before v0.9.2, pnpm may keep the dependency under the old `@omdsh-dev/dsh-genui` key even though the repository now declares `@changfenhuang/dsh-genui`. The loader resolves plugins from the profile's dependency keys, so a later reinstall can then fail with `Cannot find package '@changfenhuang/dsh-genui'`. Re-add the 