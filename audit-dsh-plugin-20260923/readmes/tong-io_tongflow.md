<div align="center">
  <img src="public/logo.svg" alt="TongFlow" width="320" />

  <h1>TongFlow: The Open-Source Modality-First GenAI Platform</h1>
  <p>
    <a href="https://github.com/tong-io/tongflow/stargazers"><img src="https://img.shields.io/github/stars/tong-io/tongflow?style=flat&logo=github" alt="GitHub stars" /></a>
    <a href="https://github.com/tong-io/tongflow/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-AGPL--3.0-blue.svg" alt="License" /></a>
    <a href="https://github.com/tong-io/tongflow/actions/workflows/ci.yml"><img src="https://github.com/tong-io/tongflow/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
    <a href="https://pypi.org/project/tongflow/"><img src="https://img.shields.io/pypi/v/tongflow?logo=pypi&logoColor=white&label=Python%20SDK" alt="PyPI" /></a>
    <a href="https://discord.gg/K7V8az94Zf"><img src="https://img.shields.io/badge/Discord-join-5865F2?logo=discord&logoColor=white" alt="Discord" /></a>
    <a href="https://github.com/tong-io/tongflow/releases"><img src="https://img.shields.io/github/v/release/tong-io/tongflow?logo=github" alt="Latest Release" /></a>
  </p>
  <p>
    <video src="https://github.com/user-attachments/assets/407a7e7b-2d44-4c90-8016-33d0a9f5e7d5"></video>
  <p>
  <p>
    <strong>English</strong> · <a href="docs/README_ZH.md">简体中文</a> · <a href="docs/README_JA.md">日本語</a>
  </p>
</div>

**Different modalities. One workflow.**

Text, images, audio, video and 3D are your materials. Decide how they transform and combine, then choose the model behind each step. Every result is material you can use again.

Open-source core · Your models · Self-hostable · [tongflow.com](https://www.tongflow.com) · [Open the canvas](https://app.tongflow.com)

## Sponsors

<table>
  <tr>
    <td width="190" align="center">
      <a href="https://metaso.cn/minimax-h3/?s=TongFlow" target="_blank" rel="noopener noreferrer"><img src="docs/assets/sponsor-metaso.png" width="163" alt="Metaso / 秘塔科技"></a>
    </td>
    <td>
      <strong>MiniMax H3 video generation API — Metaso (秘塔科技)</strong> Metaso runs MiniMax H3 video generation at <strong>¥0.09/second for 768P and ¥0.15/second for 2K</strong>. Native 2K, synced audio and picture, an <strong>OpenAI-compatible</strong> API, and <strong>ComfyUI</strong> support — no GPU to deploy yourself. 🎁 Sign up through the <a href="https://metaso.cn/minimax-h3/?s=TongFlow" target="_blank" rel="noopener noreferrer">TongFlow link</a> to claim bonus credits and a partner discount.
    </td>
  </tr>
  <tr>
    <td width="190" align="center">
      <a href="https://www.infistar.cc/register?aff=Y8S76PTA&amp;ref_source=link" target="_blank" rel="noopener noreferrer"><img src="docs/assets/sponsor-infistar.png" width="96" alt="Infistar / 无限星河AI"></a>
    </td>
    <td>
      <strong>One key for the whole canvas — Infistar (无限星河AI)</strong> An OpenAI-compatible gateway: one key and one balance cover the canvas's text, image, video and transcription nodes — GPT-6, Claude Opus 5, Gemini 3 Pro, Grok and DeepSeek alongside the broadest Chinese lineup (Qwen, GLM, Doubao, MiniMax, Kimi, StepFun), plus GPT Image 2.5, Seedream 5 and Qwen-Image for stills and Wan / Seedance for video. <strong>Images from ¥0.06 each.</strong> Use it through the <a href="https://github.com/tong-io/tongflow-router-infistar">tongflow-router-infistar</a> plugin. 🎁 Sign up through the <a href="https://www.infistar.cc/register?aff=Y8S76PTA&amp;ref_source=link" target="_blank" rel="noopener noreferrer">TongFlow link</a> for $5 of trial credit.
    </td>
  </tr>
</table>

## Demo Examples

| Workflow | Result |
| :--: | :--: |
| **Basic** — Type text (Add), generate images (Transform), then blend them into one (Combine).<br/><img src="https://file.tongflow.com/public/demos/basic.png" width="620" alt="workflow" /> | <img src="https://file.tongflow.com/public/demos/basic_result.png" width="200" alt="result" /> |
| **Intermediate** — (Add topic → write script → generate speech) + (character description → generate image) → lip-synced video = talking-head avatar.<br/><img src="https://file.tongflow.com/public/demos/digitalhuman.png" width="620" alt="workflow" /> | <video src="https://github.com/user-attachments/assets/a803394d-0ccf-4023-9b06-5c1581345758" width="200"></video> |
| **Advanced** — Generate lyrics + song + characters + scenes + storyboard → produce a music video.<br/><img src="https://file.tongflow.com/public/demos/mv.png" width="620" alt="workflow" /> | <video src="https://github.com/user-attachments/assets/2bc71e3c-3ed6-48b2-81e7-82ad5976d801" width="200"></video> |

Every output stays on the canvas as a material: branch from a generated image, feed a transcript into the next step, or swap the model behind one node and keep the rest of the workflow.

## How To Start

There are three ways to use TongFlow, all sharing the same open-source core: **TongFlow Cloud** (the desktop app or [app.tongflow.com](https://app.tongflow.com) in a browser), **self-host** ([from source](#run-from-source) or [with Docker](#run-with-docker)), or **build with an agent** (the [`tongflow` npm package](packages/tongflow/README.md) or the [dsh plugin](#use-it-inside-an-agent-dsh-plugin)).

The TongFlow **desktop app** is a lightweight (~10 MB) shell around the cloud studio at **[app.tongflow.com](https://app.tongflow.com)** — install it, sign in, and start creating. The cloud studio also runs in any modern browser.

### Step 1 — Install the desktop app

Download the installer for your platform, install it, and open it.

- **macOS (Universal — Apple Silicon & Intel):** [TongFlow-mac-universal.dmg](https://github.com/tong-io/tongflow/releases/latest/download/TongFlow-mac-universal.dmg)
- **Windows:** [TongFlow-win-x64.msi](https://github.com/tong-io/tongflow/releases/latest/download/TongFlow-win-x64.msi)

All builds are on the [Releases](https://github.com/tong-io/tongflow/releases/latest) page.

> **macOS:** the builds are not yet notarized with Apple, so Gatekeeper will block the first launch ("TongFlow is damaged and can't be opened"). After moving the app to Applications, clear the quarantine flag once and it opens normally:
>
> ```bash
> xattr -cr /Applications/TongFlow.app
> ```
>
> Download from this page directly — installers passed through chat apps (e.g. WeChat) may be renamed or re-flagged.

### Step 2 — Sign in and create

Sign in with Google or WeChat and start creating — the cloud studio manages plugins and execution for you.

> **Prefer a fully local, account-free TongFlow?** That's what self-hosting is for — see [Run from source](#run-from-source) or [Run with Docker](#run-with-docker), then follow [Self-host setup](#self-host-setup-plugins--credentials). (The desktop app up to v0.1.13 bundled this local runtime; those installers remain on the [Releases](https://github.com/tong-io/tongflow/releases) page.)

## Modality-First

A modality is a form of information: text, image, audio, video, 3D, document, URL. TongFlow makes these the building blocks of a workflow. Decide what you want to do with them, then choose the model for the job. Every step is three separate decisions:

| | Question | Examples |
| :-- | :-- | :-- |
| **Material** | What do you have? | A document, a photo, a recording, an idea. |
| **Capability** | What could it become? | Understand, generate, transform, combine or split. |
| **Implementation** | What should run it? | A compatible plugin and the model it provides. |

- **Every result is a new beginning.** Materials have their own nodes. An uploaded image and a generated image can both feed the next compatible operation. Branch out from a result instead of starting over.
- **Choose a capability, then a model.** A workflow records what a step does separately from the plugin that runs it. Switch compatible implementations while keeping the surrounding structure.
- **Four operations.** Add, transform, combine, split & batch. Understanding, generating and processing fit into the same syste