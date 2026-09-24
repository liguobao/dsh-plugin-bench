<!-- Brand assets: placeholder art in THIS repo's assets/, referenced by
     repo-relative path so the rendered README always shows what is on the
     default branch.

     Previously these were jsDelivr URLs pinned to a commit SHA. That made
     the page a snapshot of a commit rather than of the branch: editing an
     SVG changed nothing until someone also rewrote the @<sha>, and twice
     nobody did (#412, then #415 — whose hero recolour merged and then sat
     unrendered behind a stale pin).

     Relative paths remove that failure mode: replace the SVG file CONTENTS
     (same filenames), commit, done. There is no second step to forget.

     If a mark ever needs to be pinned deliberately — quoting old artwork,
     or a link that must survive a rename — pin that ONE url and say why
     here. Do not reintroduce a blanket pin. -->

<div align="right">
  <a href="#"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/OpenCues_logo-dark.svg"><img width="180" alt="OpenCues" src="assets/OpenCues_logo-light.svg"></picture></a>
</div>

<br><br>

<div align="center">
  <a href="#"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/Hero-dark.svg"><img width="600" alt="OpenCues" src="assets/Hero-light.svg"></picture></a>
</div>

<br><br>

#

<p align="left"><a href="#"><img width="120" alt="Associations:" src="assets/associations.svg"></a><a href="https://www.reddit.com/user/inventor_black/" target="_blank" rel="noopener noreferrer"><img width="257" alt="Mod of r/ClaudeAI" src="assets/mod.svg"></a><img width="24" alt="" src="assets/spacer.svg"><a href="https://luma.com/OpenSourceIRL" target="_blank" rel="noopener noreferrer"><img width="161" alt="OpenSourceIRL" src="assets/open-source-irl.svg"></a><img width="24" alt="" src="assets/spacer.svg"><a href="https://wilfred.md" target="_blank" rel="noopener noreferrer"><img width="211" alt="Anthropic Ambassador" src="assets/anthropic-ambassador.svg"></a><img width="24" alt="" src="assets/spacer.svg"><a href="https://wilfred.md" target="_blank" rel="noopener noreferrer"><img width="207" alt="Cerebras Ambassador" src="assets/cerebras-ambassador.svg"></a></p>

<br><br><br>

<!-- npm badge — hidden until announce; uncomment to show:
[![npm](https://img.shields.io/npm/v/opencues)](https://npmjs.com/package/opencues) -->

**Turn any text field into a two-way LLM channel.** It reads what you write and fills what you ask: catching a slip as you type, or answering the moment you end a line with `_`. A drop-in for Claude Code, OpenCode, Gemini CLI, your shell, and Chrome. Model-agnostic, output you review before it sends, an open standard with no chat window.

The model comes to your cursor, both ways. **Cues** react to what you've already written and surface a fix or a sharper line inline, unprompted. **Blanks** act on demand: end a line with `_` and the model fills in the rest. No chat window, no copy-paste, no context switch.

<!-- Slot 1, the hero. ONE span asked four times - a brief written, rewritten
     in place, grown, then translated - and every answer walkable back through
     `_`. Then a fresh line the runtime WIPES rather than fills, because the
     buffer holds nothing but the question.

     Every answer is the product's own, captured through the runtime's own
     fused transform-blank prompt at the product's settings (cerebras
     gemma-4-31b, temperature 0, seed 42) and pinned by a capture file, so
     the film fails its gate if the values ever stop being what the product
     says: opencues-web `artifact-kit/layouts/solo/captures/`.

     Cut from two `layouts/solo` configs joined at the step level
     (`solo/join-readme-hero.py`), not hand-authored: a bare terminal block
     on transparency, no catalog wrapper and no frame, so it sits on
     whichever ground GitHub renders the README in. The earlier
     `films/readme-hero-live.py` cut of this is deprecated - it hand-wrote
     its states, which is the one thing that system exists to prevent.

     Every answer GLIMMERS in - the 140ms blink then the 70ms churn easing
     0.45 to 0.15, glimmer-render.ts's own recipe at the product's default
     900ms - because since v0.7.8 that is how a substitution lands on every
     host, and a film whose answer hard-cuts is showing something the
     product no longer does. Derived, not opted into: the kit emits it on
     every blank `resolved` (opencues-web artifact-kit, derive.py `_glim`). -->
<img width="100%" alt="One prompt improved, rewritten as a senior engineer would, grown with a security paragraph, translated to Japanese - then an ffmpeg command answered on a fresh line" src="assets/readme-1-hero.webp">

OpenCues is platform, model, and provider agnostic, engineered from the ground up to enable native inline AI.

| You type | You get |
|---|---|
| i keep having to approve every single git command | ↳ 💡 Tired of approving? /permissions allow rules like Bash(git *), or Shift+Tab to auto mode |
| ok this is a mess, let's start over on the auth stuff | ↳ 💡 Starting over? /clear wipes the conversation, CLAUDE.md stays |
| let's ship it Thursday the 19th | ↳ ⚠ the 19th is a Friday |
| we should probably go ahead and refactor this | ↳ we should refactor this |
| hey can u send me that report when u get a sec make this formal _ | Could you please send me that report at your earliest convenience? |
| hello world translate to japanese _ | こんにちは世界 |
| draft an email to my landlord asking for a rent reduction _ | (the email, written) |
| ffmpeg command to convert a video to web-ready mp4 _ | ffmpeg -i input.mov -vcodec libx264 -crf 23 -pix_fmt yuv420p -acodec aac output.mp4 |

Rows with `_` are **blanks**: you ask, the model fills in. Rows without are **cues**: the model speaks up on what you wrote, no prompt. A 💡 cue knows the situation you are in and `_` makes the draft the command.

#

<p align="left"><a href="LICENSE"><img width="216" alt="Apache-2.0 License" src="assets/license.svg"></a><a href="spec/README.md"><img width="157" alt="Open Standard" src="assets/Ownership-05.svg"></a><img width="24" alt="" src="assets/spacer.svg"><a href="spec/blank-spec.md"><img width="121" alt="Blanks.md" src="assets/Ownership-06.svg"></a><img width="24" alt="" src="assets/spacer.svg"><a href="spec/cue-spec.md"><img width="112" alt="Cues.md" src="assets/Ownership-07.svg"></a></p>

<br><br><br><br>

# Quickstart

```bash
npm install -g opencues              # needs Node 22+ and git
opencues set-key cerebras csk-...    # cerebras.ai — free tier, lowest latency
opencues install claude-code         # or: opencode | gemini-cli | chrome | shell | dsh
claude-cues                          # launch — native `claude` is untouched
```

Full walkthrough, prerequisites, and per-host detail: [`docs/install.md`](docs/install.md). `opencues doctor` diagnoses anything that looks wrong.

<!-- Slot 2, the cues half. Nothing is pressed to make these appear.
     film29. -->
<img width="100%" alt="A Claude Code tip that knows the situation you are in, underscore makes the draft the command; then Slack catching a date that does not exist" src="assets/readme-2-cues.webp">

#

<p align="left"><a href="docs/guides/cli-reference.md#the-5-youll-actually-use"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/opencues-cli-dark.svg"><img width="178" alt="OpenCues CLI" src="assets/opencues-cli-light.svg"></picture></a><a href="docs/features/README.md"><img width="109" alt="Features" src="assets/features.svg"></a></p>

<br><br><br><br>

# Integrations

| Host | Status | Install |
|---|---|---|
| Claude Code | Available | `opencues install claude-code` |
| OpenCode | Available | `opencues install opencode` |
| Gemini CLI | Beta | `opencues install gemini-cli` |
| Chrome | Beta | `opencues install chrome` |
| Shell | Beta | `opencues install shell` |
| DeepSeek Harness | Beta | `dsh plugin --profile web add @opencues/dsh` |

Each pins its own upstream fork and never touches your native host i