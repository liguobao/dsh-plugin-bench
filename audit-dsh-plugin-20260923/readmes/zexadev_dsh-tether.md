<h1 align="center">DSH Tether</h1>

<p align="center">
  <strong>DSH in your pocket: connect to your machine when you have one, run it on the phone when you don't.</strong><br>
  Remote: across networks, peer to peer, no server to set up, no shared Wi-Fi — if hole-punching fails it falls back to a relay that sees only ciphertext.<br>
  Local (Android): the DeepSeek Harness runs on the phone itself — install and go, no Termux, no commands.
</p>

<p align="center"><sub>An independent community project. Not affiliated with, partnered with, authorised by, or endorsed by DeepSeek.<br>No DeepSeek employee or upstream DeepSeek Harness team member is involved in this repository.<br><a href="README.zh.md">中文</a> · English</sub></p>

<p align="center">
  <img src="assets/banner.jpg" alt="Phone tethered directly to a dev machine" width="100%">
</p>

<p align="center">
  <a href="../../releases/latest"><img src="https://img.shields.io/github/v/release/zexadev/dsh-tether?style=flat&label=release&color=4D6BFE" alt="Latest release"></a>
  <a href="../../releases"><img src="https://img.shields.io/github/downloads/zexadev/dsh-tether/total?style=flat&label=downloads&color=4D6BFE" alt="Downloads"></a>
  <a href="../../stargazers"><img src="https://img.shields.io/github/stars/zexadev/dsh-tether?style=flat&label=%E2%98%85&color=08C" alt="Stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2EA44F?style=flat" alt="MIT"></a>
  <img src="https://img.shields.io/badge/dsh-0.1.0--rc.7%20%7C%20rc.8%20%7C%200.1.2%20%7C%200.1.5-4D6BFE?style=flat" alt="dsh 0.1.0-rc.7 | rc.8 | 0.1.2 | 0.1.5">
  <img src="https://img.shields.io/badge/Android-4493F8?style=flat" alt="Android">
  <img src="https://img.shields.io/badge/iOS-beta-8E8E93?style=flat" alt="iOS beta">
  <a href="https://www.dsh.so/artifact/dsh-tether"><img src="https://www.dsh.so/badge/dsh-tether.svg" alt="dsh.so security scan"></a>
  <a href="https://www.dsh.so/artifact/dsh-tether"><img src="https://www.dsh.so/badge/install/dsh-tether.svg" alt="dsh.so install check"></a>
</p>

<p align="center">
  <img src="assets/phone-cellular.png" width="240" alt="A DSH session on the phone">
  <img src="assets/phone-sidebar-drawer.png" width="240" alt="The sidebar as an overlay drawer">
  <img src="assets/phone-settings.png" width="240" alt="Settings laid out for a phone">
</p>

DSH Tether carries the [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) web interface to your phone over a direct peer-to-peer connection. The agent keeps running on the machine your code lives on, and the phone gets DSH's own full interface — conversations, tool calls, approvals and settings, not a reimplementation of them. Pair once with a 6-digit code; after that the two ends find each other whatever network they are on.

When there is no machine around, the same app can run DSH on the phone itself (Android) — see [Local mode](#local-mode-no-machine-needed-android).

## The case it solves

**You are not on your machine's network, and you do not want a server in the middle.**

Reaching your own dev machine from a phone usually asks for one of two things: both ends on the same LAN, or a relay you deploy, configure and trust. This asks for neither. The two ends hole-punch to each other through [iroh](https://www.iroh.computer/), and once they do, nothing passes through a third party; the fallback relay only ever carries ciphertext it cannot read.

If you only use your phone on the same Wi-Fi as your machine, you don't need any of this — a LAN setup is simpler.

### Compared with ds-harness-remote

The project most often compared with this one is [liguobao/ds-harness-remote](https://github.com/liguobao/ds-harness-remote). Going by both READMEs:

| | DSH Tether | ds-harness-remote |
| --- | --- | --- |
| Connection | Direct first (iroh hole-punching), relay only as fallback and it sees ciphertext only; no account, no server to run | Sign in to its service, then LAN → P2P → TURN → Relay in turn; a self-hosted relay is supported |
| No machine around | Android local mode: DSH runs on the phone | — |
| Clients | Android, iOS (beta) | PC, Android, Web; no native iOS app |
| License | MIT | No license file in the repository |

## Download and install

| Where | Download | How |
| --- | --- | --- |
| Machine | — | `dsh plugin --profile web add dsh-plugin-tether` |
| Phone | `dsh-tether-<version>-arm64.apk` from the [Release](../../releases/latest) | Signed — install it directly; local mode included |
| Phone (iOS) | `dsh-tether-<version>-ios-unsigned.ipa` from the [Release](../../releases/latest) | **Beta**, unsigned — sign it yourself |

The plugin carries a small Rust sidecar that owns the iroh connection, shipped as one package per platform; installing pulls only the one matching your system, with nothing to choose.

The phone build is split by CPU architecture. **Any Android phone from the last decade takes `arm64`**; `arm` is for 32-bit legacy devices, and `x86` / `x86_64` are for emulators and ChromeOS. Picking the wrong one simply gets refused at install time. Only the `arm64` build carries the local-mode runtime; the other three have no such entry.

The iOS build is **beta**: this project has no Mac, so the package is only ever built in CI and has never run on a real device. You sign it yourself with AltStore, Sideloadly or similar (a free Apple ID expires after 7 days). Please open an issue if you hit anything.

You can also build the sidecar from source (needs Rust):

```sh
git clone https://github.com/zexadev/dsh-tether && cd dsh-tether
cargo build --release -p tether-host
dsh plugin --profile web add .
```

## Pair

Start `dsh web` as you normally would, then click **Connect phone** at the bottom of the sidebar. You get one line to copy:

On the phone, open DSH Tether → **Add computer** → paste that whole line → name the computer → connect.

From then on the app connects by itself when you open it.

## Local mode: no machine needed (Android)

Open the app → **Hosts** in the top bar → **Run on this phone**. The first start unpacks the runtime first (about 9 seconds measured); after that the DSH interface appears in about 2 seconds. Enter an API key in Settings and start talking.

- **Install and go**: no Termux, no terminal, no commands, no root. Node 24 and the full dependency tree of dsh `0.1.5-rc.2` ship inside the APK and unpack offline on first start; after that only model API calls need the network.
- **No pairing**: dsh is on this phone, there is no remote end. Sessions, settings and workspaces live only on the phone and are entirely separate from what you see when connected to a machine; switching back and forth touches neither.
- **Stays up**: while running there is a persistent notification (a foreground service), so backgrounding or locking the screen does not get the process reclaimed. If the process is killed anyway, the next launch restarts it; sessions are already on disk.
- **Versioned with the app**: the bundled dsh upgrades with the app; currently `0.1.5-rc.2`.
- Only the `arm64` APK carries local mode; iOS forbids child processes, so the iOS build has no such entry.
- The phone has no bash and no full coreutils, so shell-dependent tools are incomplete; chat and file read/write are unaffected.

The Termux route still works if you prefer it: install dsh and this plugin inside Termux (it picks the `android-arm64` sidecar package automatically), then pair to it in remote mode — the phone is just another "machine". There is no guided setup for that path; it simply keeps working.

## Features

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>Direct across networks</h3>
      <p>The two ends hole-punch to each other through iroh, and once connected nothing passes through a third party. Phone on 4G/5G and machine on home broadband works — no public IP, no tunnel service, no relay of your own. Only a failed hole-punch falls back to a relay, which carries ciphertext it cannot read.</p>
    <