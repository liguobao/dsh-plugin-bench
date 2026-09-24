<p align="center">
  <img src="docs/logo.svg" alt="DeepSeek Harness Remote" width="600">
</p>

<p align="center">
  <strong>English</strong>
  &nbsp;·&nbsp;
  <a href="README.zh.md">中文</a>
  &nbsp;·&nbsp;
  <a href="docs/README.md">Documentation</a>
  &nbsp;·&nbsp;
  <a href="apps/server/README.md">Self-hosting</a>
  &nbsp;·&nbsp;
  <strong>Download:</strong>
  <a href="https://github.com/liguobao/dsh-desktop/releases/latest">Windows</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/liguobao/dsh-desktop/releases/latest">macOS</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/liguobao/dsh-desktop/releases/latest">Linux</a>
  &nbsp;·&nbsp;
  <a href="https://dsh.r2049.cn/app">Web</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/liguobao/ds-harness-remote/releases/latest">Android</a>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/ds-harness-remote">npm</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/liguobao/ds-harness-remote">GitHub</a>
  &nbsp;·&nbsp;
  <a href="https://dshfind.com/zh/plugins/liguobao/ds-harness-remote?ref=badge"><img src="https://dshfind.com/api/badge/liguobao/ds-harness-remote?metric=downloads&amp;lang=zh" alt="dshfind downloads" width="137" height="20" align="absmiddle"></a>
</p>

## Connect once. Ready whenever you are.

Continue using your DeepSeek Harness instance from a phone, computer, or browser.

Return to the same Harness session from whichever device is with you. Harness keeps running on your work computer, with the same workspaces, tools, and project setup. Remote is simply another window into that environment.

## Features

- Continue active sessions and review their latest progress from another device
- Send new instructions, change direction, and use image prompts with supported Harness versions from `dsh-v0.1.1-rc.2` through `dsh-v0.1.6-alpha.1`
- Answer questions and permission requests from clients with live conversation controls
- Open workspaces from another authorized computer on the same account
- Reuse the native Harness interface instead of maintaining a separate desktop conversation UI
- Preview remote files between two Harness installations with the optional `dsh-file-viewer` plugin
- Run a terminal-only [dsh-TUI](https://github.com/ccch1mneyyy/dsh-TUI) profile as a Host and authorize it with a GitHub or Zhihu QR code
- The Harness Host does not need a public listening port. Connect securely from anywhere with internet access over a bidirectional end-to-end encrypted channel

## Install

### Path A: DSH Desktop

Install [DSH Desktop](https://github.com/liguobao/dsh-desktop) on Windows, macOS, or
Linux. Remote is included and enabled by default, so no separate plugin installation is required.

### Path B: Automated installation

macOS / Linux:

```sh
curl -fsSL https://dsh.r2049.cn/app/install.sh | bash
```

Windows PowerShell (Run as administrator):

```powershell
irm https://dsh.r2049.cn/app/install.ps1 | iex
```

Follow [Quick start](#quick-start) to sign in. See the [installation guide](docs/installation.md) for configuration, service management, and uninstallation.

### Path C: Existing DSH installation

Add the exact package version through DSH's plugin manager for the `web` profile:

```sh
dsh plugin --profile web add -w ds-harness-remote@0.4.17
```

`-w` targets the profile's own workspace root. It is required on pnpm below 11, which
otherwise refuses the add with `ERR_PNPM_ADDING_TO_ROOT`.

Restart Harness after installation.

Do not install this package directly with npm. Only `dsh plugin` updates the selected profile and
adds the bundle's configuration layer.

### Path D: dsh-TUI Host

For terminal Host setup with [dsh-TUI](https://github.com/ccch1mneyyy/dsh-TUI), see the
[dsh-TUI Remote guide](docs/dsh-tui.md).

## Quick start

1. Open **Remote** from the Harness sidebar.
2. Sign in with a GitHub or Zhihu QR code, or use your account and password. New password accounts can register through [Remote Web](https://dsh.r2049.cn/app/register); the site shows the current invitation requirements.
3. Enable remote control for the current computer.
4. On another device, open DSH Desktop, Remote Web, or the Android client and sign in to the same account.
5. Select the online Host, then choose an existing workspace or browse remote directories to open one.

The public service uses the hosted Remote relay. For a minimal single-account deployment,
see the [self-hosted Server](apps/server/README.md); its Web page shows device status only.

## Authorization recovery and multiple instances

Each running Host needs its own device identity. Profiles sharing the same `DSH_HOME`
share Remote credentials; use a separate `DSH_HOME` and authorize each instance if
both must stay online. When another connection replaces this Host (`CONNECTION_REPLACED`),
automatic reconnect stops to prevent the two instances from repeatedly disconnecting each other.

Expired credentials refresh under a cross-process lock. If the Server rejects a
handshake, the Host can refresh and retry it once. If refresh is rejected, use
`/remote login [github|zhihu]` or authorize the Host again in Remote settings.
The log marks refresh failures with `phase: credential_refresh` without exposing credentials.

`SERVER_CREDENTIALS_BUSY` means another process holds the refresh lock. After an
abnormal exit, stop **all** instances sharing that `DSH_HOME`, remove only the
`server-credentials.json.refresh-lock` directory beside the affected credentials
under `remote/servers/<serverHash>/<role>/`, then authorize again and restart.
Locks are never taken over based on age: a suspended process could still use the old token.

## Screenshots

### Desktop

Enable **Allow control of this device** in Remote settings to make the current computer
available as a Host.

On another computer, select an online Host and open one of its workspaces.

<p align="center">
  <img src="docs/images/host-list.png" alt="Remote workspace picker listing online Hosts" width="900">
</p>

The workspace opens in the native Harness interface, with the active Host and encrypted
connection status shown in the header.

<p align="center">
  <img src="docs/images/remote.png" alt="A Harness conversation running through an encrypted remote connection" width="900">
</p>

### Android

Download the latest Android APK from [GitHub Releases](https://github.com/liguobao/ds-harness-remote/releases/latest).

Sign in to the Android client with your existing account, select an available computer,
open a workspace, and continue the conversation with text or image prompts. The conversation
toolbar also lets you switch the active model and choose any reasoning effort declared by it.

Harness conversations open **Files** (workspace folders and paged read-only UTF-8 previews) and **Terminal** from the conversation title bar. These require the native APIs in DSH `0.1.6-alpha.2` or later and an updated Remote Host plugin. Enable **Remote terminal** in the Host's local Remote settings before opening a shell. The Terminal panel lists the terminals owned by this device and creates a new one only when you tap ＋ in its title bar; opening the panel never creates a terminal. Android restores terminals from the Host snapshot; it never replays input after disconnect. In Files, Back returns from a file to its directory and closes the tool only at the workspace root; refresh also sits in the title bar. These tools are not exposed for CodeX conversations.

The permission selector supports both older inline options and the separate `permissionPresets/catalog` used by newer DSH 0.1.6 builds. Update the Host Remote plugin too; unsupported Hosts show an actionable error instead of fabricated permission options.

Android Files also previews PNG/JPEG/GIF/WebP images and PDF documents, plus DOC/DOCX/XLS/XLSX/PPT/PPTX when the Host provides `officeToPdf`. Binary previews are limited to 8 MiB (Office sources: 50 MiB). PDF rendering is bundled locally, with no CDN, external viewer, or file export. Unknown binary type