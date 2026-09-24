<div align="center">
  <img src="docs/assets/branding/miffan-icon.svg" alt="Miffan app icon" width="120" />
  <h1>Miffan</h1>
  <p>A native Android AI client that brings models, assistants, tools, and local or remote workspaces together.</p>

  <p>
    <a href="https://github.com/Ayuilos/Miffan/releases"><img alt="GitHub release" src="https://img.shields.io/github/v/release/Ayuilos/Miffan?display_name=tag&sort=semver" /></a>
    <img alt="Android 8.0+" src="https://img.shields.io/badge/Android-8.0%2B-3DDC84?logo=android&logoColor=white" />
    <a href="LICENSE"><img alt="License: AGPL-3.0" src="https://img.shields.io/badge/License-AGPL--3.0-blue" /></a>
  </p>

  <p>English · <a href="README_ZH_CN.md">简体中文</a> · <a href="README_ZH_TW.md">繁體中文</a></p>
</div>

Miffan is an open-source AI workspace designed for Android. Connect the model services you already use, give different assistants their own prompts, memories, tools, and personalities, and keep conversations and files organized in one native app.

Use an API key with OpenAI-compatible, Gemini, or Claude services, or sign in with an eligible ChatGPT subscription for Codex access. Miffan does not bundle a model or replace a provider account; availability and charges depend on the services you configure.

## What makes Miffan different

- **One home for different models.** Mix official APIs, compatible gateways, self-hosted endpoints, and a Codex subscription without rebuilding your workflow around one provider.
- **Assistants are real workspaces.** Each assistant can have isolated prompts, model parameters, memory, tools, MCP servers, Skills, visual identity, and conversation history.
- **The phone can do more than display chat.** Miffan can search the web, work with files, run a local Linux workspace, connect to remote servers over SSH, use device capabilities, and expose the same conversations through a browser.
- **A character system with purpose.** Choose customizable Miffan bowl characters or the blue whale girl, with expressions that respond to conversation state and time of day.

## Remote workspaces · new in 3.4

Connect your own server over SSH and let an assistant work in a chosen project directory. Keep local projects and remote machines in the same app, with clear identities and connection states.

- **Multiple hosts and projects.** Manage SSH hosts, credentials, and project directories, including machines on a Tailscale network your device has already joined.
- **Files and an interactive terminal.** Browse, preview, edit, import, and export remote files, or open a persistent terminal to run commands yourself. Returning from a file preview keeps your current directory.
- **AI that works where your files live.** Bind a workspace to an assistant and use file and shell tools there. AI shell permissions and execution confirmations are managed separately for local and remote targets.
- **SSH key management.** Generate or import keys, copy public keys, and view or export private keys, with optional passphrase encryption for backups.

Open **Workspaces → New → Remote** to choose a host and project directory, then bind the workspace in the assistant settings. The one-time introduction also links directly to workspace management.

<table>
  <tr>
    <td align="center" valign="top"><img src="docs/img/miffan-remote-workspaces.png" alt="Local and remote workspace list with search and connection status" width="260" /></td>
    <td align="center" valign="top"><img src="docs/img/miffan-remote-hosts.png" alt="SSH host management with authentication and connection status" width="260" /></td>
    <td align="center" valign="top"><img src="docs/img/miffan-workspace-introduction.png" alt="Remote workspace introduction with a direct entry to workspace management" width="300" /></td>
  </tr>
  <tr>
    <td align="center">Local and remote projects</td>
    <td align="center">SSH host management</td>
    <td align="center">Discover the new workspace</td>
  </tr>
</table>

Screenshots use demo hosts and projects; the displayed UI language is Simplified Chinese.

Remote workspaces currently support Linux/Unix SSH/SFTP hosts. Miffan uses an existing network connection and does not set up Tailscale or keep tasks running autonomously while the phone is offline. See the [remote workspace guide](docs/REMOTE_WORKSPACE.md) for setup and current limits.

## Meet the blue whale girl

<p align="center">
  <img src="docs/assets/branding/miffan-whale-girl.png" alt="The blue whale girl pointing forward from a smiling Miffan rice bowl, with rice grains on her cheeks" width="560" />
  <br /><em>Miffan and the blue whale girl · character illustration</em>
</p>

**蓝色大肥鱼** is a cheerful, rice-loving companion alongside the original Miffan bowl characters. Open **Settings → Appearance** to preview the collection and try it with a dedicated assistant.

- **An assistant of her own.** The first trial creates a separate whale-girl assistant and opens a new chat. Later trials reuse it and preserve your edits. Her name, personality prompt, model, and tools remain editable; existing assistants and conversations stay intact.
- **Expressions that follow the conversation.** She smiles, enjoys petting, looks proud, reacts to updates, eats while waiting, chews during text output, sways with spinning eyes during actual reasoning, and dozes with a breathing nose bubble. Native drawing keeps the background transparent and supports reduced motion.
- **A coordinated appearance.** Vivid blue hair, fins, and a bow come with light and dark palettes, onboarding previews, and startup artwork. The bowl and whale launcher icons can be selected independently. Restoring the previous palette keeps the dedicated assistant.
- **Easy to discover.** New installations can choose the collection during onboarding; existing users receive a one-time introduction on the chat home screen. You can also choose the whale avatar for an individual assistant.

## Screenshots

<table>
  <tr>
    <td align="center"><img src="docs/img/miffan-empty-chat.png" alt="Miffan mascot in an empty chat" width="280" /></td>
    <td align="center"><img src="docs/img/miffan-character-settings.png" alt="Miffan character customization" width="280" /></td>
    <td align="center"><img src="docs/img/miffan-tool-call.png" alt="Chat response with a local tool call" width="280" /></td>
  </tr>
  <tr>
    <td align="center">Living mascot</td>
    <td align="center">Character styles</td>
    <td align="center">Tool-aware chat</td>
  </tr>
</table>

### Selected-text translation

Select text in any Android app and choose **Miffan-Translate** from the text action menu (the label follows the app language). Miffan shows the translation in a compact floating window without taking you away from the current page.

<table>
  <tr>
    <td align="center"><img src="docs/img/miffan-selected-text-action.png" alt="Choosing Miffan-Translate from the Android text action menu" width="300" /></td>
    <td align="center"><img src="docs/img/miffan-selected-text-translation.png" alt="Translation result in the Miffan floating window" width="300" /></td>
  </tr>
  <tr>
    <td align="center">1. Select text and choose Miffan-Translate</td>
    <td align="center">2. Review or copy the translation</td>
  </tr>
</table>

## Features

### Models and providers

- OpenAI Chat Completions and Responses-compatible services, Google Gemini and Vertex AI, and Anthropic Claude-compatible services
- Browser-based OpenAI Codex sign-in using access included with eligible ChatGPT subscriptions
- Built-in presets for popular official services and gateways, plus fully custom providers, base URLs, models, request paths, headers, and body parameters
- Model discovery and configurable modality, reasoning, tool-use, context-window, and generation settings
- Authenticated HTTP/SOCKS5 proxy support, custom User-Agent, connection testing, and optional provider balance queries
- Chat, reasoning, tool calls, image generation, and multimodal input a