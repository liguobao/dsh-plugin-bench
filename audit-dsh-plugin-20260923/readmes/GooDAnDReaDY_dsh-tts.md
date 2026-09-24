# 📦 @goodandready/dsh-tts

<div align="center">

<h3>Multi-Provider Text-to-Speech Voice Synthesis with Local Neural Engines, Sub-300ms Streaming, IT Dictionary & Messenger Integration for DeepSeek Harness</h3>

<p align="center">
  <a href="https://www.npmjs.com/package/@goodandready/dsh-tts"><img src="https://img.shields.io/npm/v/@goodandready/dsh-tts.svg?style=for-the-badge&color=6366f1&labelColor=1e1b4b" alt="npm version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-10b981.svg?style=for-the-badge&color=10b981&labelColor=064e3b" alt="license"></a>
  <a href="https://github.com/topics/dsh-plugin"><img src="https://img.shields.io/badge/DSH-Plugin-8b5cf6.svg?style=for-the-badge&labelColor=2e1065" alt="DSH Plugin"></a>
  <a href="https://nodejs.org"><img src="https://img.shields.io/badge/Node-20%2B-f59e0b.svg?style=for-the-badge&labelColor=451a03" alt="Node version"></a>
</p>

<p align="center">
  <a href="https://goodandready.app/"><img src="https://img.shields.io/badge/All_Author_Projects-goodandready.app-ff4500.svg?style=for-the-badge&logo=rocket&logoColor=white&labelColor=1a1a2e" alt="All Author Projects"></a>
</p>

<p align="center">
  <a href="README.md"><b>🇬🇧 English</b></a> •
  <a href="README.ru.md"><b>🇷🇺 Русский</b></a> •
  <a href="README.zh.md"><b>🇨🇳 中文说明</b></a>
</p>

<table align="center">
  <tr>
    <td align="center">
      ⭐ <strong>If you like this plugin, please star it on GitHub</strong> — it shows me that the plugin is useful to you and motivates me to keep developing it.
      <br><br>
      🐛 <strong>If you find a bug or would like to request a feature</strong>, open a GitHub issue in any language — I will review your proposal and implement useful suggestions in a future plugin version.
    </td>
  </tr>
</table>

</div>

---

## ⚡ Overview

**`dsh-tts`** provides robust, lifelike spoken voice synthesis for assistant replies in the **DeepSeek Harness** Web UI. When **Speak agent replies** is enabled, each finished assistant turn or real-time streaming chunk is synthesized on the host and streamed directly to the browser.

API keys never reach client browsers: synthesis is executed entirely on the host backend across **independent multi-provider fallback chains**, including local system engines (Edge TTS, Piper, eSpeak). Kokoro-82M and F5-TTS weights can be downloaded for future runtime support, but neural inference is **not bundled** in this package — those providers fail honestly and the chain continues.

```mermaid
graph LR
    subgraph Input [Assistant Message]
        Reply[💬 Agent Reply Text] --> Scrub[Smart Text Scrubbing & IT Dictionary]
    end

    subgraph Stream [Low-Latency Streaming]
        Scrub --> SSE[SSE /dsh-tts/stream]
        SSE --> Worklet[AudioWorklet PCM Processor]
    end

    subgraph Cache [Performance Layer]
        Scrub --> LRU{Disk LRU Cache}
        LRU -->|Cache Hit| Play[Immediate Audio Playback]
    end

    subgraph Fallback [TTS Provider Fallback Chain]
        LRU -->|Cache Miss| Chain{Active Chain}
        Chain -->|Offline| P1[Edge TTS / Piper / eSpeak]
        Chain -.->|Cloud Neural| P2[OpenAI / ElevenLabs / Google / Azure / Groq]
        Chain -.->|OpenAI-compatible| P3[SiliconFlow / DeepInfra / Fireworks / OpenRouter]
        Chain -.->|Other| P4[MiMo / MiniMax / Custom]
    end

    subgraph Output [Delivery & Integrations]
        P1 --> Store[Save to Cache]
        P2 --> Store
        P3 --> Store
        P4 --> Store
        Store --> Play
        Store --> Msg[Telegram / Discord via dsh-messenger-gateway]
    end

    style Input fill:#1e1e2e,stroke:#89b4fa,stroke-width:2px,color:#cdd6f4
    style Stream fill:#181825,stroke:#89dceb,stroke-width:2px,color:#cdd6f4
    style Cache fill:#181825,stroke:#cba6f7,stroke-width:2px,color:#cdd6f4
    style Fallback fill:#11111b,stroke:#a6e3a1,stroke-width:2px,color:#cdd6f4
    style Output fill:#181825,stroke:#f38ba8,stroke-width:2px,color:#cdd6f4
```

---

## 🚀 Key Features

### 1. 📴 Offline system engines + optional future neural runtimes
* **Edge TTS / Piper / eSpeak**: fully offline or free local/system synthesis without cloud API keys (Edge needs the `edge-tts` CLI).
* **Kokoro-82M / F5-TTS**: weight download and status UI only. **Neural inference is not bundled** in this package — those providers fail with a clear reason and the fallback chain continues. Do not enable them expecting speech until a supported runtime is wired.
* **ModelManager UI**: Direct manual installation in settings with real-time download progress bar, SHA-256 validation, and deletion. No silent or automatic multi-gigabyte downloads.

### 2. ⚡ Real-Time Streaming Audio (< 300 ms Latency)
* **AudioWorklet (`TTSWorklet`)**: High-performance Web Audio Worklet processor playing seamless Float32Array PCM chunks at 24 kHz without audible clicks or buffer underruns.
* **Server-Sent Events (SSE)**: Dedicated `/dsh-tts/stream` route delivering synthesized chunks to connected browsers instantly.

### 3. 🎙️ Voice Duplex & VAD Barge-In (with `@goodandready/dsh-voice`)
* **Full-Duplex Conversation**: Automatic voice reply synthesis upon completion of speech dictation.
* **VAD Barge-In**: Immediately mutes assistant speech playback when user voice activity is detected.
* **Installation Guard**: If `@goodandready/dsh-voice` is not present, settings controls are disabled with an explicit instruction banner (`dsh plugin --profile web add @goodandready/dsh-voice`).

### 4. 📚 Built-in IT Terminology Pronunciation Dictionary
* **Pre-configured Lexicon**: Correct phonetic pronunciation for common technical abbreviations and developer terms:
  - `SQL` $\rightarrow$ "сиквел"
  - `Nginx` $\rightarrow$ "энджинкс"
  - `Kubernetes` / `K8s` $\rightarrow$ "кубернетис"
  - `Docker` $\rightarrow$ "докер", `API` $\rightarrow$ "апи", `JSON` $\rightarrow$ "джейсон", `YAML` $\rightarrow$ "ямл"
  - `GUI`, `CLI`, `CI/CD`, `PR`, `Regex`, `OAuth`, `HTTP`, `HTTPS`, `CPU`, `GPU`, `RAM`
* **Interactive UI Editor**: Edit rules, preview phonetic substitutions with the **▶ Listen** button, and populate standard IT terms with one click.

### 5. 👥 Multi-Agent Personas & Subagent Voice Overrides
* Assign distinct voices, providers, models, and audio chimes to individual subagents (e.g. `coder`, `reviewer`, `planner`, `tester`).
* **Subagent Auto-Detection**: With `autoDetectSubagent` enabled, incoming turns automatically match subagents by message metadata (`subagent`, `agent`, `author`, `name`) and dynamically apply voice, rate, and SSML style presets.

### 6. 💾 Audio Clip Export & Speech History
* Export any spoken utterance directly to an audio file (`.wav` / `.mp3`) via `exportAudioClip(text)`.
* Instant download buttons (`⤓`) integrated directly into the input dock speaker control and recent utterances dropdown list.

### 7. 💬 Messenger Voice Notes Integration (with `@goodandready/dsh-messenger-gateway`)
* Generates voice audio for Telegram and Discord bot replies via `POST /dsh-tts/speak`.
* Protective dependency check with installation hint when gateway plugin is missing.

### 8. 🌐 Canonical English & Chinese Localization (EN + ZH)
* Complete built-in English (`en`) and Chinese (`zh`) UI and speech template dictionaries.
* Centralized Russian localization provided via `@goodandready/dsh-russian-lang` through Gitea issue tracking.
* Smart boundary tokenizer supporting CJK full-width punctuation (`。！？`), abbreviations, file extensions, and IP/version numbers.

---

## 🛠️ Complete Supported Providers Matrix (18 Backends)

| Provider Key | Service Backend | Default Model | Default Voice | Credential Ref | Features & Notes |
|---|---|---|---|---|---|
| `kokoro` | Local Kokoro-82M ONNX | `hexgrad/Kokoro-82M` | `af_bella` | *None* | Weights downloadable; **ONNX inference not bundled** — fails honestly |
| `f5` | Local F5-TTS GPU Daemon | `F5-TTS` | Default | *None* | Daemon ping only; **GPU inference not bundled** — fails honestly |
| `elevenlabs` | ElevenLabs API | `eleven_mul