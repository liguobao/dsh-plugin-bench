# DSH Scholar

[简体中文](README.zh-CN.md) | **English**

DSH Scholar is an AI research workspace for computational research. It keeps project conversations, research materials, code and data, controlled experiment runs, evidence, and TeX manuscripts in one recoverable project. You can start from a new question or continue work that already exists elsewhere.

> DSH Scholar is still under active development. Use it for supervised computational-research workflows, review every approval and research claim, and keep independent backups of important source material and results.

![DSH Scholar standalone workspace in English](docs/assets/dsh-scholar-home-en.png)

## What it provides

- **Stage-aware research guidance**: Chat supports natural conversation, Grill Me intake, file upload, visual-model input, explicit slash commands, and an authoritative next-step prompt for the current research stage.
- **Governed research workflow**: Scope, Idea, Contract, Evidence, Direction, and Release decisions remain explicit, revision-bound, and auditable.
- **Controlled execution**: Runner Profiles describe local, local-Docker, or remote-SSH environments, including pinned container images and declared NVIDIA GPU capability.
- **Integrated workspace**: project-scoped Chat, editable files, session-bound Web terminals, run logs, artifacts, TeX source, compilation diagnostics, and PDF preview share the same context.
- **Traceable methodology**: Protocol revisions, run classifications, synthesis requests, assurance results, reviewer findings, knowledge-pack activation, and claim-to-evidence links are recorded as durable research state.
- **Visible collaboration**: Trajectory and Topology expose subagent parent-child relationships, status, follow-ups, and outputs.

## Intended use and boundaries

- DSH Scholar assists researchers; it does not assume responsibility for scientific judgment, approval, authorship, or publication.
- `gate-only` is the normal mode. Agents cannot impersonate a Human principal, fabricate accepted Evidence, or bypass a research Gate.
- `full-auto` means automatic approval only for the allowlisted Scope, Idea, Contract, and Budget Gates of an exact registered FixtureProfile. Its only canonical action executor is currently `survey_run`. Release, Direction, Intake, Evidence, and unsupported actions remain Human-controlled or are parked with a typed reason.
- A name-only `/new <name>` project always starts as `gate-only` and collects its Brief through Grill Me; it does not silently inherit `full-auto`.
- Formal experiments must bind immutable code and data snapshots, a frozen Protocol where required, and an explicit Runner Profile. Chat text, ordinary stdout, and Interactive Terminal output do not automatically become formal Evidence.
- Images sent to a visual model are untrusted, current-turn Chat context. They do not automatically become OCR output, Brief answers, Evidence, Claims, Gate decisions, or proof that a command ran.
- The product focuses on computational research such as machine learning, data science, and bioinformatics. It is not intended for clinical decisions, human studies, wet-lab work, or other high-risk research.

## Quick start

The local workspace requires Linux, Node.js 24, pnpm 11.20.0, and Docker Engine for controlled experiments, TeX compilation, and clean-room reproduction.

### 1. Install and build

```bash
pnpm install --frozen-lockfile
pnpm run build
```

### 2. Start the standalone workspace

```bash
bash scripts/start-standalone-ui.sh
```

Open <http://127.0.0.1:18610> and paste the token from:

```text
~/.dsh-scholar-standalone/research-ui-standalone/standalone-token
```

The standalone workspace and DSH use the same Research Kernel at `127.0.0.1:7412` and the same canonical project data directory at `~/.dsh/research-kernel`. Upgrading either surface must keep that directory unchanged so existing projects remain accessible. Browser tokens and display preferences live separately in the standalone BFF directory. Use `--no-token` only on an isolated, supervised, loopback-only development instance.

### 3. Configure an execution environment

Open **Settings → Execution environment** and select an explicit Runner Profile:

- local machine for trusted development and smoke checks;
- local Docker with a pinned image, optionally requiring the NVIDIA runtime and GPU capability;
- remote SSH with server-side endpoint, credential, known-hosts, and target-identity SecretRefs.

Formal Jobs do not execute until the selected profile and target pass readiness checks. A missing Runner, offline target, unavailable SecretRef, capability mismatch, or incomplete Contract/Protocol is shown as preparation or a blocker instead of being treated as ready. See the [runtime guide](docs/test-instance-plan.md) for target registration, target-scoped heartbeat credentials, Runner startup, ports, and security constraints.

### 4. Install the plugin in DSH

Install the current DSH prerelease through its moving `next` tag, then record the exact installed version:

```bash
npm install -g @deepseek-ai/dsh@next
npm ls -g @deepseek-ai/dsh --depth=0
```

The `@dsh-scholar/*` packages are not published yet. Build this repository and add its absolute path to DSH's `web` profile:

```bash
cd /absolute/path/to/dsh-scholar
pnpm install --frozen-lockfile
pnpm run build
dsh plugin --profile web add /absolute/path/to/dsh-scholar
dsh plugin --profile web why @dsh-scholar/research-plugin
dsh web
```

To update Scholar, rebuild this same checkout and add the same absolute path again. To uninstall it:

```bash
dsh plugin --profile web remove @dsh-scholar/research-plugin
```

The plugin adds Scholar tools, slash commands, Skills, settings, and a compact `dsh Scholar` tab. An unlinked DSH conversation can bind an existing project or create a name-only project. A linked conversation shows only its current stage, next action, and execution summary; use **Open in new page** or the configured shortcut for the complete workspace.

## Plugin configuration

Open **Settings → Plugin config → dsh Scholar** in DSH. Saved plugin changes take effect after the next DSH restart.

| Setting | Default | Meaning |
|---|---|---|
| Default governance mode | `gate-only` | Applies only when a fully configured project explicitly qualifies for that mode. Name-only creation remains `gate-only`. |
| Unattended runs | Off | Does not bypass Human Gates; an interaction requirement parks the project. |
| Standalone URL | `http://127.0.0.1:18610/` | Target for **Open in new page** and the shortcut. Only HTTPS or loopback HTTP is accepted. |
| Open-page shortcut | `Alt+Shift+S` | Can be disabled and does not fire while typing or using an IME. |

When `full-auto` is enabled for a valid fixture, Settings also reports worker state, restart-required state, the fixture-only boundary, and the latest park reason. Release remains Human-controlled. The Standalone URL cannot contain credentials, query parameters, or fragments. **Copy standalone access token** is available only from a loopback DSH instance after an explicit click; the page never displays the token and does not expose Kernel, Runner, Provider, or SSH secrets.

### Visual models in Chat

Scholar reads the live model catalog from DSH instead of guessing capability from a model name. Configure the actual DeepSeek-compatible image endpoint as an image-capable catalog entry in the DSH profile:

```yaml
- id: llm-deepseek
  name: '@deepseek-ai/dsh-llm-deepseek'
  config:
    models:
      - id: your-vision-model
        name: Your Vision Model
        inputModalities: [text, image]
```

Restart DSH, choose the model marked with `👁` in Scholar, attach or paste PNG, JPEG, WebP, or GIF images, then send a normal-language Chat message. The same upload may enter project Intake, but its visual bytes are consumed only by that successful free-conversation turn. A text-only or undeclared model is rejected before provider network I/O; Scholar never silently falls back