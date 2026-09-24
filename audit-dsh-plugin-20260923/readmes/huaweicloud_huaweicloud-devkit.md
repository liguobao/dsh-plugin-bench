# HuaweiCloud DevKit

[![Discussions](https://img.shields.io/badge/Discussions-Join%20the%20discussion-blue)](https://github.com/huaweicloud/huaweicloud-devkit/discussions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![CI](https://github.com/huaweicloud/huaweicloud-devkit/actions/workflows/ci.yml/badge.svg)](https://github.com/huaweicloud/huaweicloud-devkit/actions/workflows/ci.yml)
[![npm version](https://img.shields.io/npm/v/huaweicloud-devkit)](https://www.npmjs.com/package/huaweicloud-devkit)
[![Beta](https://img.shields.io/badge/beta-v1.1.6-orange)](https://github.com/huaweicloud/huaweicloud-devkit)

**[中文](README.zh-CN.md) | English**

Help AI coding agents use Huawei Cloud safely and accurately — a single integration that gives agents cloud knowledge, CLI tooling, and safety guardrails.

Supports OpenCode, Codex, CodeArts Agent, WorkBuddy, DeepSeek Harness (DSH), OfficeAce, Hermes, OpenClaw, and AtomCode.

## Prerequisites

- Node.js >= 22

> **China mainland users**: If you experience slow downloads or connection issues with the default npm registry, configure the Huawei Cloud npm mirror:
>
> ```bash
> npm config set registry https://mirrors.huaweicloud.com/repository/npm/
> ```
>
> Restore the default registry: `npm config delete registry`
>
> **Mirror lag**: npm mirrors (npmmirror, mirrors.huaweicloud.com) may lag behind the official registry for hours after a new release. If install fails with `ETARGET` or you get an older version, install via the official registry instead:
>
> ```bash
> npx --yes --registry=https://registry.npmjs.org huaweicloud-devkit install --target <target>
> ```

## Quick Start

> If `--target` is omitted, the installer auto-detects agents on your machine:
>
> - **None detected**: interactive terminals ask what you want (install to one
>   explicit target / install to all / wire up a generic MCP agent);
>   non-interactive shells error out with the supported target list.
> - **One detected**: installs directly to it.
> - **Multiple detected**: interactive terminals show a multi-select chooser;
>   non-interactive shells error and point at `--target <agent>` / `--target all`.
>   For a one-shot full setup, run `npx --yes huaweicloud-devkit install --target all`
>   (Codex is skipped when its CLI is missing).

The commands below are global (they act on every agent):

```bash
npx --yes huaweicloud-devkit version  # print CLI version and installed plugin versions per agent
npx --yes huaweicloud-devkit uninstall --target all --clean-global  # also remove KooCLI + OBS config
```

### OpenCode

```bash
npx --yes huaweicloud-devkit install --target opencode
```

**Restart the session** after installation.

```bash
npx --yes huaweicloud-devkit doctor --target opencode
npx --yes huaweicloud-devkit status --target opencode
npx --yes huaweicloud-devkit update --target opencode
npx --yes huaweicloud-devkit uninstall --target opencode
rm -rf ~/.npm/_npx/  # Linux/macOS; Windows: rmdir /s /q %LOCALAPPDATA%\npm-cache\_npx
```

### Codex

```bash
npx --yes huaweicloud-devkit install --target codex
```

**Restart the Codex session** after installation.

```bash
codex plugin list  # verify huaweicloud-devkit@huaweicloud-devkit is installed and enabled
npx --yes huaweicloud-devkit doctor --target codex
npx --yes huaweicloud-devkit status --target codex
npx --yes huaweicloud-devkit update --target codex
npx --yes huaweicloud-devkit uninstall --target codex
```

Then mention `@huaweicloud-devkit` in Codex or describe your Huawei Cloud task directly.

> **Requires Codex CLI** — the `codex` command must be in PATH. If Codex is installed via WindowsApps (Microsoft Store), use `--target codex-desktop` instead. Run `codex --version` to verify CLI availability.

### Codex Desktop

Use this target when the Codex CLI is unavailable or when Codex is installed through WindowsApps on Windows.

```bash
npx --yes huaweicloud-devkit install --target codex-desktop
```

**Restart the Codex Desktop session** after installation.

```bash
npx --yes huaweicloud-devkit doctor --target codex-desktop
npx --yes huaweicloud-devkit status --target codex-desktop
npx --yes huaweicloud-devkit update --target codex-desktop
npx --yes huaweicloud-devkit uninstall --target codex-desktop
```

Then mention `@huaweicloud-devkit` in a new Codex Desktop task or describe your Huawei Cloud task directly.

### CodeArts Agent

```bash
npx --yes huaweicloud-devkit install --target codearts
```

**Restart the session** after installation.

```bash
npx --yes huaweicloud-devkit doctor --target codearts
npx --yes huaweicloud-devkit status --target codearts
npx --yes huaweicloud-devkit update --target codearts
npx --yes huaweicloud-devkit uninstall --target codearts
```

> **Sandbox mode**: CodeArts defaults to sandbox mode which blocks KooCLI. `install-hcloud` detects this and shows how to resolve it — install KooCLI outside the sandbox terminal, or disable sandbox mode in CodeArts settings (Settings → Chats → Agents Terminal Command Running Mode → Auto Running).

### CodeArts Work

```bash
npx --yes huaweicloud-devkit install --target codearts-work
```

**Restart the session** after installation.

```bash
npx --yes huaweicloud-devkit doctor --target codearts-work
npx --yes huaweicloud-devkit status --target codearts-work
npx --yes huaweicloud-devkit update --target codearts-work
npx --yes huaweicloud-devkit uninstall --target codearts-work
```

> **CodeArts Work** (CodeArts Space, appId: `com.codearts.work`) uses user-level config at `%USERPROFILE%\.codeartswork\`. No project-level `.codeartswork` directory is created.

### WorkBuddy

```bash
npx --yes huaweicloud-devkit install --target workbuddy
```

**Restart the session** after installation.

```bash
npx --yes huaweicloud-devkit doctor --target workbuddy
npx --yes huaweicloud-devkit status --target workbuddy
npx --yes huaweicloud-devkit update --target workbuddy
npx --yes huaweicloud-devkit uninstall --target workbuddy
```

### DeepSeek Harness (DSH)

```bash
npx --yes huaweicloud-devkit install --target dsh
```

**Restart the DSH session** after installation.

```bash
npx --yes huaweicloud-devkit doctor --target dsh
npx --yes huaweicloud-devkit status --target dsh
npx --yes huaweicloud-devkit update --target dsh
npx --yes huaweicloud-devkit uninstall --target dsh
```

> DSH V1 reuses the existing MCP server through `@deepseek-ai/dsh-mcp-client`. If the installer reports that the client is not detected, run: `npx @deepseek-ai/dsh plugin --profile web add @deepseek-ai/dsh-mcp-client`.

### OfficeAce

```bash
npx --yes huaweicloud-devkit install --target officeace
```

**Restart OfficeAce** after installation.

```bash
npx --yes huaweicloud-devkit doctor --target officeace
npx --yes huaweicloud-devkit status --target officeace
npx --yes huaweicloud-devkit update --target officeace
npx --yes huaweicloud-devkit uninstall --target officeace
```

### Hermes

```bash
npx --yes huaweicloud-devkit install --target hermes
```

**Restart the Hermes session** after installation.

```bash
npx --yes huaweicloud-devkit doctor --target hermes
npx --yes huaweicloud-devkit status --target hermes
npx --yes huaweicloud-devkit update --target hermes
npx --yes huaweicloud-devkit uninstall --target hermes
```

> **Uninstall notes**: On Linux, run `rm -rf ~/.npm/_npx/* && npm cache clean --force` after uninstall to ensure a clean slate. On Windows, close all Hermes sessions first to release file locks, then after uninstall check `%LOCALAPPDATA%\hermes\config.yaml` for YAML corruption and manually remove `%LOCALAPPDATA%\hermes\huaweicloud-plugins` if any files remain.
> **Safety hooks**: The installer configures Hermes shell hooks (`config.yaml` → `hooks.pre_tool_call`) to intercept unsafe terminal commands such as credential file reads, environment variable dumps, and unapproved `hcloud` write operations. Hermes shows a consent prompt the first time; approve it or set `hooks_auto_accept: true` in `config.yaml` to