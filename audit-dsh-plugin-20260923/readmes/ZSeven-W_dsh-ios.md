<p align="center">
  <img src="./docs/images/dsh-ios-logo.png" alt="DSH iOS" width="120" />
</p>

<h1 align="center">DSH iOS Simulator</h1>

<p align="center">
  <strong>A live, interactive iOS Simulator inside a <a href="https://github.com/deepseek-ai/deepseek-harness">DeepSeek Harness</a> conversation — plus your real iPhone over USB.</strong><br />
  <sub>22 agent tools &bull; live MJPEG sidebar panel &bull; simulator &amp; real iPhone over USB &bull; list/feed row actions &bull; SwiftUI preview hot reload</sub>
</p>

<p align="center">
  <sub>npm: <code>@zseven-w/dsh-ios</code> &middot; Current plugin release: <code>0.1.0-rc.10</code> &middot; Tested with DSH <code>0.1.5-rc.1</code></sub>
</p>

<p align="center">
  <b>English</b> &middot; <a href="./README.zh.md">简体中文</a> &middot; <a href="./README.zh-TW.md">繁體中文</a> &middot; <a href="./README.ja.md">日本語</a> &middot; <a href="./README.ko.md">한국어</a> &middot; <a href="./README.fr.md">Français</a> &middot; <a href="./README.es.md">Español</a> &middot; <a href="./README.de.md">Deutsch</a> &middot; <a href="./README.pt.md">Português</a> &middot; <a href="./README.ru.md">Русский</a> &middot; <a href="./README.hi.md">हिन्दी</a> &middot; <a href="./README.tr.md">Türkçe</a> &middot; <a href="./README.th.md">ไทย</a> &middot; <a href="./README.vi.md">Tiếng Việt</a> &middot; <a href="./README.id.md">Bahasa Indonesia</a>
</p>

<p align="center">
  <sub>npm: <code>@zseven-w/dsh-ios</code> &middot; Current plugin release: <code>0.1.0-rc.10</code> &middot; Tested with DSH <code>0.1.5-rc.1</code></sub>
</p>

<br />

<p align="center">
  <img src="./docs/images/dsh-ios-overview.png" alt="DSH iOS Simulator — a real iPhone inside the conversation" width="100%" />
</p>
<p align="center"><sub>A real iPhone driven from inside a DSH conversation — the agent's tool calls on the left, the live device panel on the right</sub></p>

## Why DSH iOS Simulator

DSH iOS Simulator gives the agent a real iOS Simulator inside the conversation — and gives you the pixels. The agent can boot a device, build and run an Xcode project or Swift package, drive the UI by accessibility identity or by OCR text, read unified logs, and inspect processes, backtraces, and leaks, while a live stream of the device renders in a persistent sidebar panel where you can tap, drag, rotate, and press Home directly on the video. The same verbs also work on a real iPhone connected over USB: the plugin builds and launches WebDriverAgent on the phone, tunnels its control and screen ports over loopback, and streams the device into the same panel, cards, and tools. No image blocks, no screen-recording files: visual bytes reach the UI only through signed, expiring URLs served by the DSH webserver.

| | |
| --- | --- |
| 🖥️ **Live simulator in the conversation** | A serve-sim MJPEG stream of the booted device, proxied through signed `/_dsh/dsh-ios/*` routes into a persistent right-side panel — the browser never touches serve-sim's port. |
| 📱 **Real iPhone over USB** | `ios_real_start_wda` builds and launches WebDriverAgent on a connected phone and tunnels its control (REST) and screen (MJPEG) ports over loopback; the same panel, tools, cards, and status capsule then drive the phone. The device must be unlocked, and every real-account tap is gated by the plugin's identify-before-tap rules. |
| 🛠️ **22 agent tools** | Devices, boot/shutdown, screenshot, interact, build &amp; run, unified logs, AXe-backed UI tree + tap-by-element, list/feed row actions, Vision OCR find/tap, SwiftUI preview hot reload, processes, backtrace, leaks, app info. |
| 👆 **Interactive panel** | Tap and drag on the live video; Home / rotate / screenshot / refresh icon toolbar with hover tooltips; size modes (适应 · 50–125% · S/M/L); frame styles (无框 / 边框 / 真机框); drag-resize up to 960 px with double-click reset; landscape auto-widen. |
| 🧾 **List &amp; feed rows** | `ios_sim_ui_rows` turns deep accessibility snapshots into indexed rows with labels and generically parsed counters; `ios_sim_tap_row` taps inside a row at relative coordinates and verifies the action by the counter's expected ±1 change — the only reliable confirmation a list app offers. |
| 🔐 **Loopback-only transport** | serve-sim binds 127.0.0.1 in a dedicated port range; every route requires a loopback peer, a loopback `Host`, and Fetch-Metadata/Origin checks; HMAC capabilities expire within 10 minutes. The WebDriverAgent control/MJPEG tunnels on a real device are loopback usbmux forwards under the same fence. |
| ⚡ **SwiftUI preview hot reload** | `ios_sim_preview` generates a disposable host app outside your package, builds your previews as a dylib, and hot-swaps edits into the running simulator without relaunching (~2–5 s). |
| 🧭 **Semantic UI automation** | `ios_sim_ui_tree` dumps the accessibility tree (AXe-backed) and `ios_sim_tap_element` taps by label or identifier; `ios_sim_find_text` OCRs the screen when the tree is empty or degenerate, and `ios_sim_tap_text` taps the matched text — identity- and text-based taps instead of guessed coordinates. |

## Tools

All 22 tools are registered on every host and return plain JSON — visual bytes reach the UI only through `presentationMeta` + signed routes, never as image blocks. Simulator udids route through simctl/serve-sim; physical-device udids route through WebDriverAgent automatically. On non-macOS hosts (or when serve-sim is unresolvable) the tools stay registered but fail with an explanatory error; the one exception is `ios_sim_preview` `status`, which truthfully reports `{ running: false }` on any host.

### Core simulator tools

| Tool | What it does | Key parameters |
| --- | --- | --- |
| `ios_sim_devices` | List the iOS Simulator devices available on this Mac (udid, name, runtime, state) and which are booted, plus any USB-connected physical iPhones under `realDevices` (udid, name, osVersion, model, state, developerMode). Use it to discover the udid or name to pass to the other tools. | — |
| `ios_sim_boot` | Boot a device and start its live serve-sim stream; the stream stays alive for the conversation so the panel can show the simulator live. | `udid` (required — udid or device name) |
| `ios_sim_shutdown` | Shut a device down; stops the stream when it targets that device. | `udid` (required) |
| `ios_sim_screenshot` | Capture a PNG and return a small JSON summary (path, bytes, dimensions, device); the image renders in the card/panel, never as an image block. Works on the streamed simulator and on a USB-connected phone via WebDriverAgent. | `udid` (optional — streamed device, else first booted) |
| `ios_sim_interact` | Interact with the streamed device — simulator or USB-connected phone: tap at normalized 0..1 coordinates, type text (US keyboard on a simulator), press a hardware button (`home`, `lock`, `volumeUp`…), scroll, or send a touch gesture; after the action settles (~300 ms) a fresh screenshot shows the effect. | `action` (required — `tap`/`type`/`button`/`gesture`/`scroll`), `x`/`y`, `text`, `name`, `json` |
| `ios_sim_list_apps` | List the apps INSTALLED on a booted simulator or a connected phone (bundle id, display name, version, system flag) — a third-party bundle id cannot be guessed, so list it or pass `name` to `ios_sim_launch_app`. A FAILED listing throws (e.g. "the device is not reachable by CoreDevice") instead of returning an empty list, so `count: 0` always means the device really has no matching app. | `udid` (optional), `query` (case-insensitive substring over display name AND bundle id, CJK included), `include_system` (default false) |
| `ios_sim_launch_app` | Launch an installed app on a booted simulator or a connected phone — by `bundleId`, or by `name` (a case-insensitive display-name substring resolved through the same listing, CJK included). Exactly one of the two; a launch failure and an ambiguous name both come back with what to do next (`ios_sim_build_run` is for building one from source). | `bundleId` or `name` (exactly one), `udid`, `