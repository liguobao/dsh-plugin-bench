<div align="center">
  <img src="build/icon.png" width="96" height="96" alt="DSH Desktop icon">
  <h1>DSH Desktop</h1>
  <p><strong>A compact, self-contained DeepSeek Harness desktop host with native iPhone and Android Remote companions.</strong></p>
  <p>
    <a href="#download">Download</a>
    · <a href="#highlights">Highlights</a>
    · <a href="#iphone-remote-testflight-beta">iPhone Remote</a>
    · <a href="#android-remote-github-release">Android Remote</a>
    · <a href="#development">Development</a>
    · <a href="CONTRIBUTING.md">Contributing</a>
  </p>
  <p>
    <strong>English</strong>
    · <a href="README.zh-CN.md">简体中文</a>
  </p>
  <p>
    <a href="https://github.com/chokwinlee/deepseek-harness-desktop/actions/workflows/ci.yml"><img src="https://github.com/chokwinlee/deepseek-harness-desktop/actions/workflows/ci.yml/badge.svg" alt="CI status"></a>
    <a href="https://github.com/chokwinlee/deepseek-harness-desktop/releases/latest"><img src="https://img.shields.io/github/v/release/chokwinlee/deepseek-harness-desktop" alt="Latest stable release"></a>
    <a href="LICENSE"><img src="https://img.shields.io/github/license/chokwinlee/deepseek-harness-desktop" alt="MIT License"></a>
  </p>
</div>

![DSH Desktop](docs/images/readme-hero-en.png)

*macOS DMGs around 100 MB, with the complete Harness runtime included.*

DSH Desktop runs the official [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) Web UI and runtime in a desktop window. The repository also contains DSH Remote native companions for continuing the computer's projects, sessions, and running tasks from iPhone and Android. This build is aligned with `@deepseek-ai/dsh@0.1.5-rc.2` and shows that bundled Harness version in the sidebar. The desktop app manages the local Harness process automatically, so users do not need to install Node.js or start `dsh web` themselves.

[Migration and rollback notes](docs/HARNESS_0.1.5_MIGRATION.md)


> [!IMPORTANT]
> This is an independent community project, not an official DeepSeek AI product. DeepSeek Harness is a developer preview and may introduce breaking changes.

## Highlights

- **Multimodal sessions** — paste or attach images and send them through the normal Harness conversation flow when the selected provider and model declare image input support. Image messages remain visible in session history.
- **Usage at a glance on macOS** — see today and seven-day token totals, estimated cost, active task count, and aggregate running throughput without leaving the current session.
- **Compact macOS package** — around 100 MB while bundling the complete Harness runtime, using Tauri and the system WKWebView instead of shipping Chromium.
- **Visible runtime alignment** — the sidebar identifies both the Desktop release and its bundled Harness version, such as `DSH Desktop v0.5.0 · Harness 0.1.5-rc.2`.
- **Ready to run** — includes everything needed to start Harness, with no separate Node.js installation or terminal command. The app starts and stops the local runtime automatically.
- **Native mobile Remote** — the SwiftUI iPhone client and Kotlin/Compose Android client pair on trusted Wi-Fi or the user's own Tailscale network, then browse projects, create sessions, steer tasks, handle approvals, send images, and follow subagents without moving execution off the computer.

Cost figures are estimates derived from local token logs and available public model prices. Unmatched models stay visibly unpriced rather than being counted as free.

## Multimodal and usage insights

![Multimodal session and usage insights](docs/images/readme-features-en.png)

*A real Harness rc.8 image-input session with live token and cost insights, using `google/gemini-2.5-flash-lite` through OpenRouter.*

The compact title-bar summary stays visible while you work. Open it for input, output, cache, cost, and live-throughput details. Usage is calculated locally from Harness session history, with estimated costs based on available public model prices.

## iPhone Remote (TestFlight beta)

> [!IMPORTANT]
> DSH Remote is available as a public iPhone beta. [Join with TestFlight](https://testflight.apple.com/join/7Ew6Yk9V).

<p align="center">
  <img src="docs/images/remote-home-en.png" width="30%" alt="DSH Remote same-Wi-Fi pairing in English">
  <img src="docs/images/remote-projects-en.png" width="30%" alt="DSH Remote projects and running sessions in English">
  <img src="docs/images/remote-conversation-en.png" width="30%" alt="DSH Remote approval handling in English">
</p>
<p align="center"><sub>Same-Wi-Fi pairing · Projects and running sessions · Approval handling</sub></p>

DSH Remote is a native SwiftUI companion for a DSH Desktop computer you own or manage. It does not run an agent, repository, terminal, or model provider on the phone. Work continues on the computer; the iPhone is a narrow control surface.

The iOS TestFlight beta follows the device's app-language setting and includes complete English and Simplified Chinese product copy, including setup, errors, notifications, approvals, models, Activity, and subagent flows.

- **Same Wi-Fi (recommended):** Desktop exposes an opt-in, authenticated LAN endpoint on a trusted private network. No Tailscale account is required.
- **Away from the local network:** both devices join the user's own tailnet, and Desktop configures a private Tailscale Serve HTTPS entry. Do not use Funnel.
- **No project-operated relay:** code, prompts, model credentials, tool execution, and session history remain on the user's computer.

### Install with TestFlight

1. Install Apple's [TestFlight app](https://apps.apple.com/app/testflight/id899247664) on an iPhone running iOS 17 or later.
2. Open the [DSH Remote public invitation](https://testflight.apple.com/join/7Ew6Yk9V), choose **View in TestFlight**, then accept and install the beta.
3. Install the current DSH Desktop release on the computer before pairing.

### Build from source with Xcode

Developers can also install the source on their own iPhone with Xcode:

1. Install Xcode 16 or later on a Mac and sign in under **Xcode → Settings → Accounts**.
2. Clone this repository and open `ios/DSHRemote/DSHRemote.xcodeproj`.
3. Select the `DSHRemote` target, choose your Team under **Signing & Capabilities**, and use a unique bundle identifier if automatic signing requests one.
4. Connect an iPhone running iOS 17 or later, select it as the run destination, and choose **Product → Run**.

A free Apple Account can use an Xcode Personal Team for personal on-device testing, but the app must be re-provisioned periodically. Downloading an unsigned or unrelated IPA from GitHub will not work.

### Pair and use Remote

1. Install and open the latest DSH Desktop build.
2. In Desktop, open **Settings → General → Mobile Remote → Connect phone**.
3. On the same trusted Wi-Fi, start local pairing and scan the QR code in DSH Remote.
4. For cellular or other remote networks, open the built-in Tailscale setup guide on Desktop or iPhone, enable anywhere access, and scan the HTTPS QR code.
5. Open a project, create or continue a session, and keep all execution on the computer.

See the [iOS TestFlight and source guide](ios/DSHRemote/README.md), [Chinese Tailscale setup guide](docs/TAILSCALE_REMOTE_SETUP.zh-CN.md), [privacy policy](docs/PRIVACY.md), [support notes](docs/SUPPORT.md), and [App Review notes](docs/APP_REVIEW_NOTES.md).

## Android Remote (GitHub release)

> [!IMPORTANT]
> [`v0.4.0`](https://github.com/chokwinlee/deepseek-harness-desktop/releases/tag/v0.4.0) is the first stable GitHub release with a signed Android APK. It requires Android 8.0 or later and the matching DSH Desktop build from that release. It is not yet available on Google Play.

<p align="center">
  <img src="docs/images/android-remote-home-en.png" width="42%" alt="DSH Remote Android onboarding in English">
  <img src="docs/images/android-remote-conversation-en.png" width="42%" alt="DSH Remote Android approval and conversation controls in E