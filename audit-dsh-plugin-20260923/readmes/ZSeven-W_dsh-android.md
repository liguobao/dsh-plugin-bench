<p align="center">
  <img src="./docs/images/dsh-android-logo.png" alt="DSH Android" width="120" />
</p>

<h1 align="center">DSH Android</h1>

<p align="center">
  <strong>A live Android device inside a <a href="https://github.com/deepseek-ai/deepseek-harness">DeepSeek Harness</a> conversation — emulator or USB phone, driven entirely through adb.</strong><br />
  <sub>20 agent tools &bull; in-process live stream, no external helper &bull; three-button navigation panel &bull; Gradle build &amp; run &bull; Vision OCR</sub>
</p>

<p align="center">
  <sub>npm: <code>@zseven-w/dsh-android</code> &middot; Current plugin release: <code>0.1.0-rc.8</code> &middot; Tested with DSH <code>0.1.5-rc.1</code></sub>
</p>

<p align="center">
  <b>English</b> &middot; <a href="./README.zh.md">简体中文</a> &middot; <a href="./README.zh-TW.md">繁體中文</a> &middot; <a href="./README.ja.md">日本語</a> &middot; <a href="./README.ko.md">한국어</a> &middot; <a href="./README.fr.md">Français</a> &middot; <a href="./README.es.md">Español</a> &middot; <a href="./README.de.md">Deutsch</a> &middot; <a href="./README.pt.md">Português</a> &middot; <a href="./README.ru.md">Русский</a> &middot; <a href="./README.hi.md">हिन्दी</a> &middot; <a href="./README.tr.md">Türkçe</a> &middot; <a href="./README.th.md">ไทย</a> &middot; <a href="./README.vi.md">Tiếng Việt</a> &middot; <a href="./README.id.md">Bahasa Indonesia</a>
</p>

<br />

<p align="center">
  <img src="./docs/images/dsh-android-overview.png" alt="DSH Android — a live Android device inside the conversation" width="100%" />
</p>
<p align="center"><sub>An Android device streamed and controlled from inside a DSH conversation — the agent's tool call in the center, the live device panel on the right</sub></p>

## Why DSH Android

DSH Android gives the agent a real Android device inside the conversation — and gives you the pixels. The agent can start a stream on an emulator or a USB-connected phone, build and install a Gradle project, drive the UI by `resource-id`/text or by OCR, read logcat, and inspect processes and memory, while a live stream of the device renders in a persistent sidebar panel where you can tap, drag, rotate, and press Back / Home / Recents directly on the video. No image blocks and no screen-recording files: visual bytes reach the UI only through signed, expiring URLs served by the DSH webserver.

There is exactly one code path. `adb devices -l` reports a **serial**, and that serial is a device's only identity — `emulator-5554`, a USB serial, or an `ip:port` target all behave identically. The plugin is bound to no emulator product (AVD, Genymotion, WSA, a cloud device farm), and there is no simulator/real-device split to reason about.

| | |
| --- | --- |
| 📱 **Live device in the conversation** | A `multipart/x-mixed-replace` PNG stream produced **in-process** and served straight from the latest-frame buffer through signed `/_dsh/dsh-android/*` routes. |
| 🔌 **No external stream helper, no inner port** | One persistent `adb exec-out` child runs `while :; do screencap -p; done`; the host splits the concatenated PNGs into frames itself. There is no loopback stream server to proxy, no port range to manage, and nothing to adopt after an ungraceful exit. |
| 🧩 **One adb code path** | Emulators and phones are the same thing to adb and to this plugin. No `simctl`/WebDriverAgent dual stack, no build-and-trust dance before a physical device works. |
| 🛠️ **20 agent tools** | Devices, boot/shutdown, screenshot, interact, Gradle build &amp; run, app listing/launching, `uiautomator` UI tree + tap-by-element, list/feed row actions, Vision OCR find/tap/wait, logcat, processes, ANR/crash backtrace, meminfo, app info. |
| 👆 **Three-button navigation panel** | Tap and drag on the live video; a toolbar with **◁ Back · ○ Home · □ Recents** plus rotate, screenshot, and refresh; a device menu for the notification shade, quick settings, lock, wake, and the assistant. |
| 🖼️ **Native multimodal** | On an image-capable model every capture tool (screenshot, interact, tap_element, tap_text, tap_row) returns the screenshot ITSELF as an image block — the model sees the screen directly. OCR stays for pixel-precise text taps and text-only routes; text-only models keep the plain JSON summary. |
| 🔐 **Signed loopback-only routes** | Every route requires a loopback peer, a loopback `Host` (DNS rebinding rejected), and Fetch-Metadata/Origin checks — before any capability is consulted. HMAC-SHA256 capabilities expire within 10 minutes. |
| 🔍 **Semantic + visual automation** | `android_ui_tree` dumps the `uiautomator` hierarchy and `android_tap_element` taps by `resource-id`, text, or content-description; when the tree is empty or the text is baked into an image, `android_find_text` / `android_tap_text` OCR the screen instead of guessing coordinates. |

## Tools

All 20 tools are registered on every host and return plain JSON — visual bytes reach the UI only through `presentationMeta` + signed routes, never as image blocks. When adb cannot be resolved the tools stay registered and every call fails with an explanatory error naming the fix.

Coordinates are **normalized 0..1 of the streamed frame** everywhere. The frame follows the display rotation (a landscape app streams 2400×1080 on a 1080×2400 device) and `input tap` shares that same space, so no client-side rotation math exists anywhere in this plugin.

### Core tools

| Tool | What it does | Key parameters |
| --- | --- | --- |
| `android_devices` | List every device `adb devices -l` reports (serial, state, emulator/physical, model, Android version, API level, AVD name) plus the machine's AVD names under `avds`. Use it to discover the serial the other tools take. A failed enumeration throws instead of returning an empty list. | — |
| `android_boot` | Start the live stream. Pass an ONLINE serial to stream it immediately, or an AVD name to launch that emulator first and stream it once it finishes booting (minutes on a cold start). The stream stays alive for the conversation so the panel can show the device live. | `device` (required — a serial or an AVD name) |
| `android_shutdown` | Shut an emulator down (`adb emu kill`) and stop the stream when it targets that device. A physical device is refused with the reason: adb cannot power off a phone. | `device` |
| `android_screenshot` | Capture a PNG and return a small JSON summary (path, bytes, dimensions, device); the image renders in the card and the panel, never as an image block. | `device` (optional — streamed device, else the only online one) |
| `android_interact` | Interact with the streamed device: tap at normalized 0..1 coordinates, type text, press a navigation or hardware button (`back`, `home`, `recents`, `power`, `volume_up`, `volume_down`, `menu`, `enter`, `delete`), send a swipe gesture, or scroll. After the action settles (~300 ms) a fresh screenshot shows the effect. | `action` (required — `tap`/`type`/`button`/`gesture`/`scroll`), `x`/`y`, `text`, `name`, `json`, `device` |
| `android_list_apps` | List the packages installed on the device (`pm list packages`), with the version name from `dumpsys package` and a human label when one is resolvable — a third-party package name cannot be guessed, so list it or pass `name` to `android_launch_app`. | `device`, `query` (case-insensitive substring, CJK included), `include_system` (default false) |
| `android_launch_app` | Launch an installed app by `packageName`, or by `name` (a case-insensitive label substring resolved through the same listing). Exactly one of the two. `relaunch` force-stops the app first. | `packageName` or `name` (exactly one), `device`, `relaunch` |
| `android_build_run` | Build a Gradle project (`./gradlew assembleDebug`), install the resulting debug APK (`adb install -r`), and launch it. Takes minutes for a full build; on failure the result carries the tail of the Gradle error output. | `projectPath` (required), `device` |

### UI-tree and row tools (`uiautomator`)

| Tool | 