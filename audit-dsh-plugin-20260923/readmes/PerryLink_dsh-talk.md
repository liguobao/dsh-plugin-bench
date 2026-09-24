<div align="center">

# 🎙️ dsh-talk
- **1024 store channel**: `npm i -g dsh1024` once, then `dsh1024 plugin --profile web add dsh-talk` (counts toward the [deepseek1024.com](https://deepseek1024.com) install ranking).
[![Gitee](https://img.shields.io/badge/Gitee-mirror-c71d23?logo=gitee)](https://gitee.com/perrylink/dsh-talk)
[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-talk?metric=downloads)](https://dshfind.com/plugins/PerryLink/dsh-talk?ref=badge)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-talk/badge)](https://api.securityscorecards.dev/projects/github.com/PerryLink/dsh-talk)

**Voice-first session loop for DeepSeek Harness: talk to it, hear it answer.**

*Press the mic, speak, and the reply is spoken back — with speak-to-interrupt.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![DSH plugin](https://img.shields.io/badge/dsh--plugin-✅-green)](https://github.com/topics/dsh-plugin)
[![dsh-doctor](https://raw.githubusercontent.com/PerryLink/dsh-plugin-doctor/main/badges/PerryLink__dsh-talk.svg)](https://github.com/PerryLink/dsh-plugin-doctor#verified-徽章)
[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-top-rated.svg)](https://dsh.market/)
[![Node](https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-brightgreen.svg)](#)
[![CI](https://img.shields.io/github/actions/workflow/status/PerryLink/dsh-talk/ci.yml?branch=main&label=CI)](https://github.com/PerryLink/dsh-talk/actions)
[![Version](https://img.shields.io/github/v/tag/PerryLink/dsh-talk?label=version)](https://github.com/PerryLink/dsh-talk/releases)
[![npm version](https://img.shields.io/npm/v/dsh-talk)](https://www.npmjs.com/package/dsh-talk)
[![npm downloads](https://img.shields.io/npm/dm/dsh-talk)](https://www.npmjs.com/package/dsh-talk)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

</div>

---

## Compatibility

| Surface | Status |
|---|---|
| Harness | DeepSeek Harness `dsh-v0.1.7-alpha.2` (adapted 2026-09-18: third peer clause + `engines.dsh` + `manifestVersion: 1`, and the monthly Compat workflow anchored to that line); full gate chain green on 2026-09-18 (dual typecheck rulers, 86 tests, build, self-contained, artifacts, pack). npm dev/test line `0.1.7-alpha.2`, peers `>=0.1.2-rc.1 <0.2.0 || >=0.1.5-alpha.1 <0.2.0 || >=0.1.6-0 <0.2.0 || >=0.1.7-0 <0.2.0`. |
| Node | `^22.19.0 \|\| >=24.0.0` |
| Browser | Web Speech + MediaRecorder (Chrome/Edge best); host transcription/TTS engines for the rest |

## What you get

`dsh-talk` closes the voice loop in both directions:

- **`speak` tool** — the agent speaks its replies aloud. TTS engines: the browser voice, `edge-tts` (network neural voices), or `piper` (local). Audio plays in the browser; on hosts that can carry it, the session log records the sanitized utterance (see Security boundaries).
- **Composer mic button** — press it, speak, and the transcription lands in the input box (or submits directly). STT engines: the browser's Web Speech (interim results included), a FunASR HTTP server, or local `whisper.cpp`.
- **Speak-to-interrupt** — starting to talk stops whatever is playing (client → host over the `talk` Remote namespace).
- **Event announcements** — turn completion, pending approvals (waterfall-safe: never blocks the gate), and errors, with a mute switch and configurable phrases.
- **Settings tab** — engine/language selects and announcement switches, saved as append-only profile-patch operations with backups.

```text
browser                                host
  🎙 press ──▶ interrupt ─────────────────▶ talk/interrupt
  record (MediaRecorder / Web Speech)
  transcribe (browser) or talk/transcribe ─▶ FunASR / whisper.cpp
  setDraft(text) or submit()  ◀── talk:speech projection ── speak tool / announcements
  ▶ play audio (talk/audio or speechSynthesis)
```

## Quick start

```sh
# 1. install the bundle into your profile
dsh plugin --profile web add "github:PerryLink/dsh-talk#main"

# or from npm (published releases)
dsh plugin --profile web add dsh-talk

# 2. restart and verify the row
dsh --profile web --dump-config | grep -A2 'id: talk'
```

Then press the microphone next to the composer and talk; ask the agent to `speak` its reply:

```
> Say "hello" with the speak tool.
```

## Install & uninstall

- **git channel** (latest `main`): `dsh plugin --profile web add "github:PerryLink/dsh-talk#main"` — the `prepare` script builds with production dependencies only.
- **npm channel** (published releases): `dsh plugin --profile web add dsh-talk`.
- **tarball channel**: `pnpm pack` in this repo, then `dsh plugin --profile web add ./dsh-talk-<version>.tgz`.
- **uninstall**: `dsh plugin --profile web remove dsh-talk` (or remove the row from the profile patch).

> If pnpm reports `ERR_PNPM_IGNORED_BUILDS` for this package (esbuild's harmless platform-binary validation), add `allowBuilds: { esbuild: true }` to your `pnpm-workspace.yaml` — the `dsh` CLI prints the exact snippet.

## Configuration

All tunables are Schemastery `Config` fields (changeable from cordis.yml). `cordis.patch.yml` documents each key inline.

| Key | Default | Meaning |
|---|---|---|
| `record.enabled` | `true` | Show the composer mic button |
| `record.hotkey` | *(none)* | Optional toggle hotkey, e.g. `"alt+r"` |
| `record.maxSeconds` | `60` | Recording cap in seconds (1..600) |
| `record.autoSubmit` | `false` | Submit the transcription as a user message (false = fill the draft) |
| `record.vad.enabled` / `silenceMs` / `energyThreshold` | `true` / `1500` / `0.01` | Voice-activity detection: silence auto-ends the recording (degrades when `AudioContext` is absent) |
| `stt.engine` | `auto` | `auto` / `web` / `funasr` / `whisper`; auto prefers a configured local engine, then Web Speech |
| `stt.language` | `auto` | BCP-47 language or `auto` |
| `stt.interim` | `true` | Show interim transcriptions (Web Speech) |
| `stt.silenceFinaliseMs` | `4000` | Stop continuous Web Speech recognition after this many milliseconds without speech (500..15000) |
| `stt.funasr.url` | *(none)* | FunASR inference endpoint; required when the engine is `funasr` |
| `stt.whisper.modelPath` | *(none)* | whisper.cpp model; required when the engine is `whisper` |
| `tts.engine` | `auto` | `auto` / `browser` / `edge-tts` / `piper`; auto prefers piper, then edge-tts, then the browser voice |
| `tts.rate` | `0` | Rate offset in percent (-50..50) for edge-tts/piper |
| `tts.fallbackToBrowser` | `true` | Fall back to the browser voice when a local engine fails |
| `tts.browser.voiceName` | *(none)* | Preferred browser voice name; an unknown name uses the platform default |
| `tts.browser.rate` | `1` | Browser SpeechSynthesis rate (0.1..10) |
| `tts.browser.pitch` | `1` | Browser SpeechSynthesis pitch (0..2) |
| `tts.piper.modelPath` | *(none)* | piper voice model; required when the engine is `piper` |
| `announce.enabled` | `true` | Master switch for event announcements |
| `announce.onTurnEnd` / `onApproval` / `onError` | `true` | Which events are spoken |
| `announce.messages.*` | *"Turn complete." etc.* | Spoken phrases |
| `interrupt` | `true` | Talking stops current playback |
| `maxSpeakChars` | `20000` | Cap on the speak tool's text length (1..100000) |
| `maxAudioCacheBytes` | `8388608` | In-memory synthesized-audio cache cap (1 MiB..64 MiB) |

`stt.silenceFinaliseMs` and `record.vad.silenceMs` are separate mechanisms: the first finalises the Web Speech transcript when continuous recognition hears no speech, the second is the MediaRecorder energy-based detector that ends the recording (and submits it when `record.autoSubmit` is on). They run in different pipelines and share no state.

## Tools & surfaces

| Surface | Kind | Notes |
|---|---|---|
| `speak` | tool | Speaks text aloud (browser/edge-tts/piper); per-call engine/voice overrides; canonical JSON outcome |
| 