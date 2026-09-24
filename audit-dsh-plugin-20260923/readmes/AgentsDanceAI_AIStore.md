<div align="center">

# AI Store

**Thirty-three open-source AI products behind one account—hosted, or pulled onto
your own machine with a single command.**

DeepSeek Harness, ComfyUI, Dify, OpenManus… each slot is its own workspace.
This repo is the layer behind them: accounts, a server-side model gateway,
metering and billing, teams, and the workspace orchestration—with the upstream
key never leaving the server.

[![CI](https://github.com/AgentsDanceAI/AIStore/actions/workflows/ci.yml/badge.svg)](https://github.com/AgentsDanceAI/AIStore/actions/workflows/ci.yml)
[![License: DSH Cloud Community 1.0](https://img.shields.io/badge/license-DSH%20Cloud%20Community%201.0-4c6ef5.svg)](LICENSE)
[![Security policy](https://img.shields.io/badge/security-private%20reporting-2f9e44.svg)](SECURITY.md)

Release: [`0.4.0`](release/release.json)

[中文](README.zh-CN.md) · [Architecture](docs/architecture.md) ·
[Self-host](docs/deploy.md) · [Editions](docs/editions.md) ·
[Security](SECURITY.md) · [Support](SUPPORT.md)

</div>

---

Boot the whole Community Edition locally with one command (Docker required):

```bash
npx --yes @agentsdanceai/dsh-cloud start
```

Put your model upstream key into `./dsh-cloud/.env` (`UPSTREAM_API_KEY=`), run
the same command again, and open <http://localhost:8787>. No Node? `uvx
dsh-cloud start` does the same from PyPI. Details: [Quick start](#quick-start).

## Choose your path

<!-- path:hosted -->

### Use AI Store Hosted

[AI Store Hosted](https://aistore.best/login?next=%2Fwork) is the managed
subscription service: no server installation, with model access, workspace
capacity, upgrades, monitoring, backups, and account support. Current plans are
paid once for the selected monthly or annual term and **do not renew automatically**.

**New accounts start with 500 free credits**, and the hosted gateway serves
**20 models** with no upstream key of your own.

[**Start on AI Store Hosted**](https://aistore.best/login?next=%2Fwork) ·
[Individual plans](https://aistore.best/pricing#plans) ·
[Team plans](https://aistore.best/pricing#team)

<!-- path:local -->

### Run the workspaces on your own machine

Keep the hosted account, gateway and billing—move the *containers* to your own
5090 box or Mac. A workspace that runs on your hardware costs you no machine
hours; model calls still go through the hosted gateway and are still billed in
credits.

```bash
python3 scripts/local/aistore-local.py login      # authorise this machine once
python3 scripts/local/aistore-local.py run codex  # pull, start, open localhost:8080
```

**Our servers never dial into your machine.** No tunnel, no public IP, no
inbound port. The runner authorises with a revocable device token (the same
RFC 8628 flow the desktop client uses); the agent inside the container calls
`aistore.best/llm/*` with it, so usage lands on your account exactly as it does
in the cloud.

Not every slot runs locally yet: `aistore-local.py list` prints the ones that do.
Multi-container stacks run too (Dify is ten containers, Hermes three): the main
container owns the network namespace and the rest join it with `--network
container:`, matching the pod semantics used in the cloud — so the upstream
configs that hard-code `127.0.0.1` hold as written. The four digital-human slots
stay hosted-only because they drive our GPU nodes.

That list and the start-up orchestration both come **from the server**
(`/api/local/catalog`, `/api/local/plan/<slot>`), so a new image tag or a new
slot needs no change here — the script is only an executor. The plan carries no
credentials: wherever a token belongs there is a placeholder, filled in locally
with the one on your machine.

Three things worth knowing before you start:

- **The images are large.** Measured: 0.6–1.9 GB per slot (the one Codex and
  Claude Code share is 1.17 GB, OpenManus is 1.93 GB); the Dify stack is about
  6 GB across its ten containers. They are pulled on demand and cached, but
  trying every slot costs twenty-odd GB. `docker system df` shows the usage,
  `docker image prune` reclaims what is unused.

- **The workspace images are `linux/amd64` only.** An x86 box (the 5090 case)
  runs them natively. On Apple Silicon `docker pull` **fails outright** (`no
  matching manifest for linux/arm64/v8`) — not "a bit slower": the runner falls
  back to `--platform linux/amd64` on its own and tells you it is emulating.
  Docker Desktop needs Rosetta / multi-arch support switched on.
- **Every image is public** (since 2026-09-10): the exact tag each slot
  references can be pulled anonymously, no ghcr login needed. A contract test
  pins this, so a new slot whose image was left private turns CI red.

<!-- path:selfhost -->

### Self-host Community Edition

Run the source-available Community Edition with your own domain, database, identity
providers, model upstream, storage, and operational controls. Docker Compose is
the canonical persistent path; Docker, npm/npx, and uv/uvx use the same versioned
stack contract.

[**Self-hosting guide**](docs/deploy.md) ·
[Configuration template](deploy/selfhost/.env.example) ·
[Security checklist](docs/security.md)

<!-- path:develop -->

### Develop and contribute

The public repository includes the FastAPI service, web console, gateway,
deployment definitions, desktop overlay, mobile shells, tests, and release
contracts.

[**Development setup**](#development) · [Contributing](CONTRIBUTING.md) ·
[Architecture](docs/architecture.md) · [Changelog](CHANGELOG.md)

## The thirty-three products

Every slot opens in the browser on the same account, the same credit balance
and the same server-side gateway — no per-product signup, no API keys of your
own. Twenty-five of them open as their own workspace container at
`/work?product_id=<id>`; the other eight live on the main site instead — the four
digital-human slots share GPU nodes, and the two decision models and the search /
recommendation slots call shared backends, so none of them runs a container per user.

Which slots are actually open depends on the deployment: a slot is live when its
image and domain are configured, and shows as *coming soon* until then. On the
hosted site the shelf grew from sixteen to thirty on 2026-09-22, so a batch of
the newer slots is still landing.

<!-- app-catalog:start -->
| Product | In one line | What you get |
| --- | --- | --- |
| **DeepSeek Harness**<br>`dsh` | DeepSeek general agent | The general agent: writes code, researches, runs commands, ships results. Our flagship. |
| **Agents Team**<br>`agents-team` | A crew of bots, in parallel | Hand one task to a room of bots: group them, they work in parallel and bring the results back together. |
| **ComfyUI**<br>`comfyui` | Node-graph controllable video & image | Node-graph canvas for image & video generation — Seedance, Wan and Qwen-Image ready to pick. |
| **Codex**<br>`codex` | OpenAI coding agent | OpenAI Codex in the browser: the same editor and terminal, driven by Codex — on your credits from the first minute. |
| **OpenClaw 2.0**<br>`openclaw` | The classic lobster, 2.0 | A self-hosted always-on personal agent: one gateway across Telegram, Discord, Slack and dozens more — it reads your files and gets things done. |
| **Claude Code**<br>`claude-code` | Anthropic coding agent | Claude Code in the browser: full VS Code plus an agent that reads your repo, edits code and runs tests — on your credits from the first minute. |
| **Hermes Agent**<br>`hermes` | Persistent memory, self-taught skills | Nous Research's always-on agent: persistent memory, and it writes each solved problem into a reusable skill — it gets better the longer it runs. |
| **AI 智慧搜索**<br>`/smart-search` · on the main site | Ask an index · recall then summarise | Ask a question against an index: pull the most relevant records first, then let the model answer and point at which record it came from. |
| **AI 智慧推荐**<br>`/smart-recommend` · on the main site | Feeds and related items | Give it a user profile for a feed, or an i