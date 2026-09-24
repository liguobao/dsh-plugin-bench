<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)"
            srcset="apps/client/assets/brand/source/cosyncing-lockup-stacked-reverse.svg">
    <img src="apps/client/assets/brand/source/cosyncing-lockup-stacked.svg"
         alt="cosyncing" width="280">
  </picture>
</p>





<p align="center"><b>From CLI to GUI, live and in sync</b></p>

<p align="center">
  <a href="https://cosyncing.com/#sync">
    <picture>
      <source media="(prefers-color-scheme: dark)"
              srcset="https://cosyncing.com/assets/sync/sync-demo-dark.gif">
      <img src="https://cosyncing.com/assets/sync/sync-demo-light.gif"
           alt="cosyncing app and agent CLI staying in sync through takeover and a permission request" width="830">
    </picture>
  </a>
</p>



<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)"
            srcset="apps/client/assets/brand/marketing/social-banner-1280x640.png">
    <img src="apps/client/assets/brand/marketing/social-banner-white-1280x640.png"
         alt="Code anywhere. Sync everywhere. Your agents keep working. You keep moving."
         width="830">
  </picture>
</p>

<p align="center">
  <a href="https://cosyncing.com/">Website</a> ·
  <a href="#install">Install</a> ·
  <a href="#client">Client</a> ·
  <a href="docs/README.md">Docs</a> ·
  <a href="docs/CONTRIBUTING.md">Contributing</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <a href="README.es.md">Español</a>
</p>

---

Synchronize and control your agents — from CLI to GUI, from desktop to phone. Pick up right where you left
off, anywhere. cosyncing keeps your coding agents in sync across your own network.

The broker runs on the machine where your agents work. It watches their sessions and serves
a client that shows each one — grouped by project, with its transcript, diffs, commands, and any
prompt waiting on you. Read a session, answer a prompt, or take over. No account to create, no
hosted service between the client and the broker.

## Supported agents

<p>
  <a href="https://www.claude.com/product/claude-code" title="Claude Code"><img src="docs/assets/agents/pills/claude.png" alt="Claude Code" height="34"></a>
  <a href="https://openai.com/codex/" title="Codex"><img src="docs/assets/agents/pills/codex.png" alt="Codex" height="34"></a>
  <a href="https://opencode.ai/" title="OpenCode"><img src="docs/assets/agents/pills/opencode.png" alt="OpenCode" height="34"></a>
  <a href="https://pi.dev/" title="Pi"><img src="docs/assets/agents/pills/pi.png" alt="Pi" height="34"></a>
  <a href="https://www.kimi.com/code" title="Kimi CLI"><img src="docs/assets/agents/pills/kimi.png" alt="Kimi CLI" height="34"></a>
  <a href="https://github.com/deepseek-ai/deepseek-harness" title="DeepSeek Harness"><img src="docs/assets/agents/pills/dsh.png" alt="DeepSeek Harness" height="34"></a>
  <a href="https://antigravity.google/" title="Antigravity"><img src="docs/assets/agents/pills/antigravity.png" alt="Antigravity" height="34"></a>
  <a href="https://github.com/can1357/oh-my-pi" title="omp (oh-my-pi)"><img src="docs/assets/agents/pills/omp.svg" alt="omp (oh-my-pi)" height="34"></a>
  <a href="https://reasonix.io/" title="Reasonix"><img src="docs/assets/agents/pills/reasonix.svg" alt="Reasonix" height="34"></a>
  <a href="https://grok.com/" title="Grok Build"><img src="docs/assets/agents/pills/grok.svg" alt="Grok Build" height="34"></a>
  <a href="https://cline.bot/" title="Cline"><img src="docs/assets/agents/pills/cline.svg" alt="Cline" height="34"></a>
  <a href="https://kilocode.ai/" title="Kilo Code"><img src="docs/assets/agents/pills/kilocode.svg" alt="Kilo Code" height="34"></a>
</p>

One protocol covers all twelve. Per-agent control differs, and Claude Code sessions open read-only
until you take over. See [supported-agent setup](docs/supported_agents/README.md) for versions and
installation, and [adapter support](docs/protocol/adapter-support.md) for the capability matrix.

Foreground clients can join the same broker-owned Codex, Pi, omp, or Reasonix Drive session without starting a
second native Resume. Claude Code keeps its Observe/Take-over flow on another client, while OpenCode
keeps its shared-live behavior. Background Observe connections stay read-only.

**Experimental:** Eight provisional adapters are available to source contributors.
[Kimi Code](docs/supported_agents/kimi.md) observes every session on a
`kimi web` server read-only, drives the ones cosyncing created — prompts, approvals, model selection —
and takes over the ones it did not, explicitly. [DeepSeek Harness](docs/supported_agents/dsh.md)
connects to a `dsh web` host and gives active foreground clients a shared transcript and control
surface, with model and reasoning-effort selection, permission presets, the host's own slash commands,
and image attachments. General file attachments are not supported — the host accepts image content
only — and background resident subscriptions and some message presentation remain follow-up work.
[Antigravity](docs/supported_agents/antigravity.md) reads the Antigravity CLI's own conversation
store — no server involved — replays every conversation read-only, and drives one through a
broker-owned `agy` child; two clients can share a Drive, and a write from a terminal hands the
session back. [omp](docs/supported_agents/omp.md) uses its own packaged bridge and native RPC
dialect for discovery, live sync, prompts, approvals, commands, models, file input, and session
creation. [Reasonix](docs/supported_agents/reasonix.md) observes its bounded local store and resumes
through a lazy broker-owned ACP child; joined clients share one writer, while terminal true sync and
file input remain unsupported. [Grok Build](docs/supported_agents/grok-build.md) observes its bounded
local store and, on 1.0.13 or newer, adds authenticated broker-owned ACP Create/Resume, prompts,
approvals, commands, and model/effort/mode controls. [Cline](docs/supported_agents/cline.md) keeps
bounded default-profile parent/subagent snapshots read-only, while app-created sessions use
an isolated broker-owned Hub for Create/Resume, prompts, Stop, approvals, create-time model/mode,
and shared Drive. Exact-id terminal handoff stays separate from that writer.
[Kilo Code](docs/supported_agents/kilocode.md) observes bounded local SQLite snapshots and, on 7.4.23
or newer, adds authenticated Create/Drive, approvals, model selection, and rename through a
broker-owned host on dedicated loopback port 4097. Terminal true sync remains unsupported for all
three.

None needs a rollout flag. Managed-host adapters need no terminal left open: an installed cosyncing
service starts a host when none is running, restarts one that crashes, and stops only the process it
started. A host you started yourself is never stopped, replaced, or reconfigured, and setup names
each managed runtime before you agree to it. Install DeepSeek Harness globally with
`npm install -g @deepseek-ai/dsh` —
cosyncing looks for `dsh` on your PATH, so an `npx`-only install can be talked to but never started or
version-checked. See [supported-agent setup](docs/supported_agents/README.md) for each runtime.

## Prerequisites

The server runs with [Bun](https://bun.sh) 1.3.8 or newer. The one-command installers acquire it
when needed; only the npm installation path requires Node.js/npm. The broker is local-only by
default. Cross-device use requires a proxy, tunnel, VPN,
mesh network, or another [operator-owned connectivity method](docs/connectivity/README.md).
For a simple private route, see [Tailscale Serve](docs/connectivity/tailscale-serve.md); for a
self-managed overlay, see [WireGuard or EasyTier](docs/connectivity/wireguard-easytier.md). After
`cosyncing setup`, you can also copy
`https://github.com/cosyncing/cosyncing/tree/main/docs/connectivity` to a coding agent and ask it to
configure your chosen method while keeping the broker bound to loop