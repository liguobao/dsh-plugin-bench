<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/banner-dark.svg">
    <img src="docs/banner.svg" alt="dsh-auto-continue" width="720">
  </picture>
</p>

<h1 align="center">dsh-auto-continue</h1>

<p align="center">
  <em>DSH Web UI plugin — when a request is interrupted by a network error or any other non-human cause, it automatically sends “Continue” for you.</em>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/dsh-client-auto-continue"><img src="https://img.shields.io/npm/v/dsh-client-auto-continue?logo=npm&label=npm" alt="npm version"></a>
  <a href="https://www.npmjs.com/package/dsh-client-auto-continue"><img src="https://img.shields.io/npm/dm/dsh-client-auto-continue?label=downloads" alt="npm downloads"></a>
  <a href="https://github.com/HsiangNianian/dsh-auto-continue/stargazers"><img src="https://img.shields.io/github/stars/HsiangNianian/dsh-auto-continue?logo=github&label=Stars" alt="GitHub stars"></a>
  <a href="https://github.com/HsiangNianian/dsh-auto-continue/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-65a30d?style=flat" alt="MIT license"></a>
  <br>
  <a href="https://awesome-dsh-plugin.com"><img src="https://awesome-dsh-plugin.com/badge.svg" alt="awesome · DSH plugin"></a>
  <a href="https://www.dsh.so/artifact/dsh-auto-continue/"><img src="https://www.dsh.so/badge/install/dsh-auto-continue.svg" alt="dsh.so install"></a>
  <br>
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=fff" alt="TypeScript">
  <img src="https://img.shields.io/badge/esbuild-FFCF00?style=flat&logo=esbuild&logoColor=000" alt="esbuild">
  <img src="https://img.shields.io/badge/GUI--configurable-0ea5e9?style=flat" alt="GUI configurable">
</p>

<p align="center">
  <b>English</b> · <a href="README.zh.md">中文</a>
</p>

---

## What It Does

For [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (`dsh web`): whenever a request in the web GUI gets interrupted by a **non-human cause**, the plugin simulates the user typing **“Continue”** and sends it, so the agent keeps working without manual intervention. The message enters the session log exactly like a manual prompt — the model sees it, and the interrupted work resumes. Since 0.8.0 the engine runs **inside the host process** (single instance), so it keeps watching even with every browser tab closed, and multiple open tabs can never double-send.

![demo](docs/demo.svg)

**Smart recovery** (all configurable):

- **Error classification** — transient failures (network / timeout / 5xx / 429…) are auto-resumed; permanent ones are **skipped** and notified, because retrying them never helps. A failure counts as permanent when its HTTP status is 401/403 or its code/message matches auth, credential/API-key, balance/quota, unknown-model, or context-length/overflow keywords. Provider-specific exceptions can be opted into with literal custom retryable patterns; turn classification off to resume everything
- **Adaptive backoff** — consecutive failures wait longer each time (cooldown × factor: 20s → 40s → 80s…), capped at the max backoff, instead of hammering a broken upstream
- **English / Chinese localization** — the settings card, built-in resume / guard / loop text, and browser notifications follow DSH's active UI language (initially selected from the browser language). Only `en` and `zh` are supported; other languages fall back to Chinese. Switching languages updates built-in defaults without overwriting custom text
- **Templated continue text** — `continueText` supports `{code}` `{message}` `{status}` `{tool}` `{turn}` `{errorCount}` `{sessionTitle}` `{elapsed}` placeholders, so the resume message can carry the failure context ("Continue ({tool} failed: {code})"); a **separate template** fires on `max-tokens` (e.g. "Continue the output without repeating anything already generated")
- **Idempotency guard** — before resuming, the plugin inspects the last tool call: if its result is unconfirmed (the turn died mid-tool, e.g. a `git push` that may have gone through), the resume message tells the model to check state first and not to rerun; if the tool is confirmed done, it says so and asks not to repeat it; a failed tool gets no guard (retrying it is the point). Both guard texts are configurable (`{tool}` / `{result}` placeholders)
- **Pause** — a global **Pause auto-continue** toggle in the settings card stops everything (live + scan) instantly; per-session pauses (e.g. via a notification button) suspend only one session until they expire. The **Resume now** notification button is the one explicit exception: pressing it is the user asking for exactly one send, pause or not
- **Notification buttons** — notifications carry **Resume now** (send immediately, ignoring cooldown, the consecutive cap and any pause) and **Pause this session 1h** actions
- **Loop guard** — watches **running** turns too. Four signals trip the guard, which cancels the turn and restarts it with a configurable loop text ("stop repeating, try another way"): the model repeating the **exact same message** several times (any length — e.g. "Let me test variants of the regex…" ×7), repeated near-duplicate paragraphs **inside one streamed assistant message**, many short messages inside a short time window with no tool call in between (the "Let me read…" spin), or the same tool called repeatedly with the **same arguments and the same results** (a changed argument or result counts as progress). The cancel carries an internal marker so it is never confused with a user stop — the restart only happens for guard-initiated cancels. Thresholds, the time window and the loop text are configurable
- **Stats panel** — the settings card shows today's auto-continue count, recoveries, failures, permanent skips, give-ups and loop breaks, broken down by error code, with a one-click reset
- **Browser notifications** — optional alerts when auto-continue fires, gives up, or hits a permanent error; the browser asks for permission on first use, and nothing is shown again after a denial

It watches the live event streams and reacts to:

| Event | Meaning |
| --- | --- |
| `turn/end` → `error` | Turn failed (model / network / timeout, …) |
| `turn/end` → `interrupted` | Crash-orphaned turn left behind by a host restart (recovered by the startup scan) |
| `turn/end` → `max-tokens` | Output token ceiling reached |
| `host/agent-error` | Agent failure with no turn position (only network/timeout-class messages auto-resume) |

**Never auto-continues:** user-aborted turns (`aborted`) or policy rejections (`blocked`); live `interrupted` turn-ends too — that marker is only written by crash repair when the host reloads, so orphaned turns are recovered by the startup scan, not the live path; sessions the host already resumed itself; running sessions; subagent sessions; anything inside the cooldown / consecutive-cap windows (configurable in the settings card, below). If an interrupted session already has queued turns, the continuation runs first and the existing turns retain their order behind it.

---

## How It Works

The host-side engine subscribes to the session event firehose inside the dsh host process — exactly one engine, regardless of how many tabs are open (the duplicate-send class of bugs cannot exist by construction). On an interruption it waits a **grace period** (default 3 s) — if the host starts a new turn by itself (`turn/start`), the auto-continue is cancelled — then sends the configured text through the agent registry (`agent.followup`, the same queue the Send button uses). When that queue already contains turns, the engine promotes only its newly inserted continuation before the host wakes the agent; it does not remove or reorder the queued user turns.

On host boot it also scans the live sessions: a session whose last turn ended with a non-human reason **within the scan window** (default 15 minutes), with no later `turn/start` or user