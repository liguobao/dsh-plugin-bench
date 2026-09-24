<p align="center">
  <img src="assets/branding/dsh-banner.png" alt="DSH IM Connect" width="100%">
</p>

<div align="center">

  # DSH IM Connect

  **Connect Feishu, Lark, DingTalk, WeCom, WeChat, QQ, and Telegram to local DeepSeek Harness**

  [简体中文](README.zh-CN.md) · [Changelog](CHANGELOG.md) · [Apache-2.0](LICENSE)

  [![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
  [![npm package](https://img.shields.io/npm/v/%40michengai%2Fdsh-im-connect.svg?label=npm%20package)](https://www.npmjs.com/package/@michengai/dsh-im-connect)
  [![npm downloads](https://img.shields.io/npm/dt/%40michengai%2Fdsh-im-connect.svg?label=npm%20downloads)](https://www.npmjs.com/package/@michengai/dsh-im-connect)
  [![DSH Web Plugin](https://img.shields.io/badge/DSH%20Web-Plugin-0f766e.svg)](https://github.com/MichengAI/dsh-im-connect)
  [![Node.js 22 or later](https://img.shields.io/badge/Node.js-22%20or%20later-339933.svg?logo=node.js&logoColor=white)](https://nodejs.org/)
  [![Channels](https://img.shields.io/badge/channels-7-238636.svg)](#-supported-channels)
</div>

> DSH IM Connect is a community-maintained DeepSeek Harness (DSH) plugin, not an official DeepSeek AI product.

## Features

Send tasks to your local DSH through your usual messenger, even when you are away from the computer. Receive replies, answer questions, and handle tool approvals in the same chat.

- **Connect familiar platforms**: DingTalk, Feishu, Lark, WeChat, WeCom, QQ, and Telegram.
- **Configure accounts separately**: each account has its own workspace, model, reasoning effort, permissions, and private-access mode.
- **Handle task interactions on your phone**: send work, read replies, and answer single- or multiple-choice questions. Approved users can approve or deny tools in private chats.
- **Keep chat records separate**: each IM chat has its own session under **Channels** in the web workspace.
- **Connect by QR code or credentials**: use the platform-specific setup in **Settings → IM Assistant**, then control message reception per account.
- **Control access**: groups trigger through mentions and private chats follow each account’s access settings, as detailed below.

## Who can drive the assistant

Inbound messages are identified before commands, tool approvals, or injection.

| Case | Behavior |
|---|---|
| Group without a mention of this bot | Ignored without a reply or pending approval request; mentioning someone else also does not trigger it |
| Group explicitly mentioning this bot | No binding. Anyone can send work |
| DM from the QR scanner | WeChat / Feishu / Lark / QQ scanners are allowlisted automatically |
| DM from anyone else | Appears on the settings pending list until approved |
| DM after QR binding that does not return user identity | DingTalk / WeCom QR setup returns bot credentials only, so the scanner still needs settings approval |
| DM after manual credentials | Telegram, and DingTalk / WeCom / QQ bound manually, require approval for every DM |
| DM without a userId | Denied |
| Tool approval | Only an allowlisted user in a DM can reply `Approve` / `Deny` (or `批准` / `拒绝`); group replies do not grant |
| Interactive choice | Reply with an option number or text in the originating IM conversation; separate multiple choices with commas or add a custom answer; only the initiating user can answer in a group |

WeChat is QR-only and DM-only, so the same WeChat account that scanned can talk immediately. A different WeChat account DMing the bot waits for settings approval.

## 📡 Supported channels

<p align="center">
  <code>🔔 DingTalk</code>&nbsp;
  <code>🐦 Feishu</code>&nbsp;
  <code>🌐 Lark</code>&nbsp;
  <code>💬 WeChat</code>&nbsp;
  <code>🏢 WeCom</code>&nbsp;
  <code>🐧 QQ</code>&nbsp;
  <code>✈️ Telegram</code>
</p>

| Channel | Status | How to connect | You need |
|---|---|---|---|
| 🔔 **DingTalk** | ✅ Ready | QR, or Client ID / Secret | DingTalk open-platform bot; replies prefer AI Card |
| 🐦 **Feishu** | ✅ Ready | QR only; creates the bot automatically | Feishu account |
| 🌐 **Lark** | ✅ Ready | QR only | Lark account |
| 💬 **WeChat** | ✅ Ready* | Official iLink QR | Dedicated account recommended; DM only |
| 🏢 **WeCom** | ✅ Ready | QR (recommended), or Bot ID / Secret | WeCom intelligent bot |
| 🐧 **QQ** | ✅ Ready | QR, or AppID / AppSecret | QQ Open Platform bot, not a personal QQ account |
| ✈️ **Telegram** | ✅ Ready | Bot Token only | `@BotFather`; do not enable Webhook on the same bot |

✅ Ready = text in and out works ｜ *WeChat = official iLink only, no reverse-engineered personal protocol ｜ Groups still require an @ mention

## Image input

Image input follows DSH Chat's model-capability and attachment rules rather than guessing vision support from model names:

The receive paths cover WeChat, WeCom, DingTalk, Feishu, Lark, QQ, and Telegram. See the [image-input verification guide](docs/image-input.md) for protocol forms and live checks.

- Use the model currently selected for the IM session, not just the global default.
- When the model declares `image` support, store images as standard DSH attachments and submit image content to the model. Session history keeps image references rather than only local-path text.
- When the model explicitly excludes image input, tell the sender to switch models instead of silently dropping the image. Missing capability metadata follows Chat's compatibility behavior and is not, by itself, a reason to reject an image.
- Channel download limits, host attachment size and format limits, DM access rules, and group mention requirements still apply.
- This is inbound image analysis, not a promise that every channel supports sending images from the bot or generating images.

## File input

WeChat, WeCom, DingTalk, Feishu, Lark, QQ and Telegram accept ordinary files through Chat’s upload service for the current session. Send PDFs, documents or spreadsheets for the assistant to process. Format support follows web Chat’s models, tools and file capabilities; uploading does not guarantee that every format can be understood directly.

- Requires the file-upload service in DSH `0.1.5-rc.1`, `0.1.5-rc.2`, `0.1.5-rc.3`, or `0.1.7-rc.1`. On `0.1.2-rc.1`, file input asks you to upgrade; existing text and image support is unchanged.
- Up to 4 ordinary files per message, totaling 20 MiB. Channel download limits also apply.
- Files become standard Chat attachments and are submitted with session-specific receipts, rather than local-path text.
- Private admission and group mention rules remain in force. File captions such as `/new` or “allow” are content, not commands or approval responses.
- Failed uploads do not submit partial text. Disabling or reloading an account prevents later submission to the old session. Generated files can be sent back after the reply.

## File delivery

WeChat, WeCom, DingTalk, Feishu, Lark, QQ, and Telegram can return files produced by the assistant. For example: “Create a PDF report and send me the file.”

- Files successfully created or edited with Chat's supported file tools are sent after the reply. On hosts with `present`, explicitly presented files are also sent, including existing files.
- File access follows Chat: files outside the workspace are allowed when the host can read them. The plugin does not extract arbitrary paths from reply text. Files created through shell commands need to be presented explicitly.
- Newer hosts use Chat's complete-file download service and its configured size limit. DSH `0.1.2-rc.1` uses the host filesystem with a 32 MiB limit. Directories and symbolic links are not sent; channel-specific file limits still apply.
- A failed transfer produces a message naming the file and does not stop the remaining files. Switching away from the session or stopping the account prevents pending delivery from continuing to a different target.
- Send `/export` as a standalone command to receive the current linked session’s Chat ZIP logs in this chat, without child se