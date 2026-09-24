# Sealos Skills

<!-- README-I18N:START -->

**English** | [简体中文](./readmes/README.zh-CN.md) | [繁體中文](./readmes/README.zh-TW.md) | [日本語](./readmes/README.ja.md) | [한국어](./readmes/README.ko.md) | [Español](./readmes/README.es.md) | [Français](./readmes/README.fr.md) | [Deutsch](./readmes/README.de.md) | [Português (Brasil)](./readmes/README.pt-BR.md) | [Русский](./readmes/README.ru.md) | [العربية](./readmes/README.ar.md) | [हिन्दी](./readmes/README.hi.md) | [Bahasa Indonesia](./readmes/README.id.md)

<!-- README-I18N:END -->

Deploy projects to [Sealos Cloud](https://sealos.io) from your AI agent.

Sealos Skills is a plugin-first skill pack centered on Sealos Cloud development and deployment. It helps an AI agent inspect a project, prepare missing deployment artifacts, connect Sealos Cloud databases and object storage for development, build or reuse a container image, ship the app to Sealos Cloud, and view deployed resources in a local read-only canvas.

The recommended Codex path is native Codex plugin installation. Cross-host plugin installs, `skills.sh`, and context-only extension hosts such as Gemini CLI and Qwen Code use the same root `skills/**` source.

## Quick Start

### Recommended: install in Codex

Add this repository as a Codex marketplace, then install the Sealos plugin:

```bash
codex plugin marketplace add labring/sealos-skills
codex plugin add sealos@sealos
```

One Sealos plugin installs the deploy, database, S3, canvas, app-builder, and supporting cloud-native skills from root `skills/**`: `sealos-deploy`, `sealos-database`, `sealos-s3`, `sealos-canvas`, `sealos-app-builder`, `cloud-native-readiness`, `dockerfile-skill`, and `docker-to-sealos`.

For compatibility and local Codex testing, install the same plugin with:

```bash
npx plugins add https://github.com/labring/sealos-skills --target codex
```

After installation in Codex, use the plugin from Codex:

- **Codex CLI:** type `$sealos`
- **Codex App:** click the **+** button in the lower-left corner of the chat input, choose **Plugins**, then choose **Sealos**

![Select the Sealos plugin in Codex App](./assets/codex-sealos.png)

Codex examples:

```text
$sealos deploy this repo to Sealos Cloud
$sealos deploy /path/to/project
$sealos deploy https://github.com/labring-sigs/kite
$sealos create a cloud Postgres database for this repo and wire DATABASE_URL
$sealos create private S3 object storage for uploads and wire env vars
```

### Install in Claude Code

Add this repository as a Claude Code marketplace, then install the Sealos plugin:

```bash
claude plugin marketplace add labring/sealos-skills
claude plugin install sealos@sealos
```

For compatibility with cross-host plugin installers, install the same plugin with:

```bash
npx plugins add https://github.com/labring/sealos-skills --target claude-code
```

If you only use one detected agent tool on the machine, you can let `plugins` choose the target:

```bash
npx plugins add https://github.com/labring/sealos-skills
```

After installation in Claude Code, use `/sealos`:

```text
/sealos deploy this repo to Sealos Cloud
/sealos deploy /path/to/project
/sealos deploy https://github.com/labring-sigs/kite
/sealos create a cloud Postgres database for this repo and wire DATABASE_URL
/sealos create private S3 object storage for uploads and wire env vars
```

### Test in Qoder

Build the Qoder plugin package from the repository root:

```bash
python3 scripts/package-qoder-plugin.py
```

Import `dist/sealos-1.2.5.zip` into Qoder. The package exposes the same eight root-level skills as the Codex plugin and provides `/sealos` as its command entry point.

Qoder examples:

```text
/sealos deploy this repo to Sealos Cloud
/sealos create a cloud Postgres database for this repo and wire DATABASE_URL
/sealos create private S3 object storage for uploads and wire env vars
/sealos show the resources created by the last deployment
```

### Install in DeepSeek Harness

This repository is a dsh profile bundle over the same root `skills/**` source. After `npx @deepseek-ai/dsh web` works, install it into the same `web` profile (`pnpm` must be on `PATH`):

```sh
npx @deepseek-ai/dsh plugin --profile web add github:labring/sealos-skills
npx @deepseek-ai/dsh web
```

A local checkout:

```sh
npx @deepseek-ai/dsh plugin --profile web add /path/to/sealos-skills
```

The eight root skills appear in the session skill catalog. Ask the agent to deploy to Sealos Cloud; it loads `sealos-deploy` (and sibling skills as needed) through the `skill` tool, then runs `kubectl` / `sealos-cli` through bash.

The default bash sandbox blocks writes outside the workspace. Login writes `~/.sealos/kubeconfig`, so those commands need `sandbox_permissions: danger-full-access`.

### Other supported AI tools

| Tool | Install | Usage |
| --- | --- | --- |
| Codex CLI / Codex App | `codex plugin marketplace add labring/sealos-skills` then `codex plugin add sealos@sealos` | `$sealos` in Codex CLI, or **+** → **Plugins** → **Sealos** in Codex App |
| Claude Code | `claude plugin marketplace add labring/sealos-skills` then `claude plugin install sealos@sealos` | `/sealos` |
| Claude Code compatibility path | `npx plugins add https://github.com/labring/sealos-skills --target claude-code` | `/sealos` |
| Qoder | Build with `python3 scripts/package-qoder-plugin.py`, then import the ZIP | `/sealos` or automatic skill selection |
| DeepSeek Harness | `npx @deepseek-ai/dsh plugin --profile web add github:labring/sealos-skills` | Ask the agent to use Sealos skills; there is no `/sealos` slash command |
| OpenClaw / ClawHub | `clawhub install labring/sealos-skills` | Host command exposure depends on the ClawHub runtime |
| CodeBuddy | `/plugin marketplace add labring/sealos-skills` | Host command exposure depends on the CodeBuddy runtime |
| Gemini CLI | `gemini extensions install https://github.com/labring/sealos-skills` | Context-only extension; ask Gemini to use Sealos Skills |
| Qwen Code | `qwen extensions install https://github.com/labring/sealos-skills` | Context-only extension; ask Qwen to use Sealos Skills |
| Amp / Kimi / generic repo importers | Import `https://github.com/labring/sealos-skills.git` | Host-dependent |

Gemini CLI and Qwen Code manifests provide repository context through `CLAUDE.md`; they do not claim slash-command support.

### Alternative: install as a `skills.sh` skill pack

If your agent uses `skills.sh` directly, install the same skills pack with:

```bash
npx skills add labring/sealos-skills
```

Then run the deploy skill directly:

```text
/sealos-deploy
/sealos-deploy /path/to/project
/sealos-deploy https://github.com/labring-sigs/kite
/sealos-database create a cloud Postgres database for this repo and wire DATABASE_URL
/sealos-s3 create private object storage for uploads and wire env vars
```

After a project has been deployed and `.sealos/state.json` contains verified `last_deploy` runtime evidence, use the `sealos-canvas` skill through your installed plugin entry point for a local read-only view. Canvas stays plugin-pack mediated because it consumes verified deployment state.

`/sealos-deploy`, `/sealos-database`, and `/sealos-s3` are direct `skills.sh` skill entries. Plugin usage should go through `$sealos` in Codex or `/sealos` in Claude Code.

## Why Use the Plugin

Prefer the plugin install for Codex, Claude Code, and Qoder because it:

- installs all Sealos skills as one managed package
- exposes the same skills across supported agent tools
- keeps the plugin metadata, logo, prompts, commands, and capabilities together
- avoids maintaining a separate packaged copy of the skills

## Plugin Distribution

The Codex integration follows [OpenAI's Codex plugin build guide](https://developers.openai.com/codex/plugins/build):

- `.codex-plugin/plugin.json` contains plugin identity, discovery metadata, interface copy, default prompts, brand metadata, and asset paths relative to the repository root.
- `.agents/plugins/marketplace.json` registers this repo-local