# 🎒 DSH Config Manager

**DeepSeek Harness Backup, Restore & Migration Plugin.**

Backup, restore, export, import, migrate and sync your complete DeepSeek Harness (DSH) configuration — settings, model providers, plugins, MCP servers, skills, agent presets and workspaces — and restore your whole environment on a new machine with one click.

- 🔄 **Backup & Restore** DeepSeek Harness configuration
- 📦 **Export / Import** complete DSH configuration
- 🚚 **Migrate** DSH to another machine
- ⏰ **Scheduled full backups** — automatic, on your own cadence (6h / 12h / 24h / 7d / custom weekly), secrets never included
- 🔌 Backup installed **plugins** and plugin configuration
- 🧩 Backup **MCP servers** and **Skills**
- 🔐 Encrypted backups with optional credentials
- ☁️ **Git / WebDAV** configuration sync
- 🛒 **Configuration market** — browse & one-click install shared configs
- ↩️ Automatic snapshot and rollback before restore

[English](README.md) · [简体中文](README.zh-CN.md)

---

## What is this? 🤔

DSH is your AI assistant workbench — it holds your settings: model configs, plugins, skills, workspaces…

**DSH Config Manager is its "moving service"**:

```
┌──────────────┐   ① one-click    ┌─────────────────┐   ② one-click    ┌──────────────┐
│  Machine A    │ ──── export ───► │ dsh-config.zip   │ ──── import ───► │  Machine B    │
│  my config    │                  │   (one file)     │                  │  all restored │
└──────────────┘                  └─────────────────┘                  └──────────────┘
```

> ⚠️ **Security first**: no secrets (API Key / Token / Password) are exported by default. See [Security](#-security).

---

## 🎯 Use Cases

### Backup DeepSeek Harness configuration

Create a portable backup of your DSH settings, model providers, plugins, MCP servers, skills, agent presets and workspace — one ZIP file, no secret values included by default. (DSH's own profiles — `$DSH_HOME/profiles/<name>`, i.e. which plugin stack to boot — are machine-local and are not migrated; the **Profiles** page can list/create/rename/delete them and record which one the next launch should use.)

### Restore DeepSeek Harness on another machine

Export your current DSH environment as a single ZIP and import it on a new Windows, macOS or Linux machine. One click brings back settings, plugins, MCP servers, skills and global instructions (AGENTS.md).

### Migrate DSH configuration to a new computer

Move your complete DeepSeek Harness setup without manually reinstalling plugins, MCP servers and skills. Dead absolute paths are detected and remapped automatically (batch prefix mapping supported).

### Sync DSH configuration across machines

Keep portable configuration synchronized between machines through a private Git repository or WebDAV — secrets do not sync by default (the payload is run through the SecretScanner); check "Export secrets" with an encryption password and `~/.dsh/.credentials.yaml` travels as scrypt + AES-256-GCM ciphertext inside the encrypted snapshot, so another machine can restore the credentials while the remote (Git host / WebDAV provider) only ever sees ciphertext.

### Schedule automatic full backups

Turn on scheduled backups (6h / 12h / 24h / 7d — or a **custom weekly weekday & time**) and DSH quietly keeps a fresh full backup of your configuration in the background — secrets are never included, so it stays safe on disk without a password. Consecutive failures are highlighted in red in the settings card.

### Discover & install configurations from the marketplace

Browse the built-in official market for ready-made configurations (model providers, plugins, MCP servers, skills, agent presets…), preview what would be imported (dry-run), and install with one click — supply-chain warnings are always shown and every section must be explicitly approved before anything is written.

---

## ✨ Highlights

| Icon | Feature | In one line |
|:---:|---|---|
| 🚀 | **One-click Export** | Package your recommended config into a ZIP |
| 📦 | **One-click Import** | Restore your environment on another machine |
| 👀 | **Preview before import** | Full preview first — **never touches your config silently** |
| ⚔️ | **Conflict handling** | Keep Current / Use Imported — you decide |
| 🗺️ | **Path auto-mapping** | Detects dead absolute paths and lets you remap them |
| 🔒 | **Secret safety** | API Keys are not exported by default — non-encrypted imports ask you to re-enter; encrypted backups restore them with the password |
| ↩️ | **Automatic rollback** | Failed import restores everything automatically |
| 📸 | **Snapshot restore** | Undo an import: whole-file restore + uninstall added plugins (CLI & GUI) |
| 🔄 | **Remote Sync** | Push/pull portable config via **Git private repo or WebDAV** (secrets do not sync by default; encrypted snapshots can optionally carry encrypted credentials) |
| ⏰ | **Scheduled backups** | Full backup on a fixed cadence (6h / 12h / 24h / 7d) — set-and-forget, secrets never included |
| 🛒 | **Config Marketplace** | Browse & one-click install community configs — supply-chain warnings + per-item content selection (change summary + in-place high-risk flags) |
| 🗂️ | **Profiles (DSH profiles)** | Manage `$DSH_HOME/profiles/<name>` directly: list / create from a shipped template / rename / hard delete / record which profile the next launch should use |
| 🌐 | **Bilingual UI** | Interface, reports and error details follow the DSH app language (中文 / English) |
| 🤖 | **Agent tools** | Backup / snapshot / restore / sync right from an agent session |

---

## 📸 Screenshots

| Export | Import Preview |
|:---:|:---:|
| ![One-click Export](assets/screenshot-export.png) | ![Import Preview](assets/screenshot-import-preview.png) |

| Snapshot Restore | Remote Sync |
|:---:|:---:|
| ![Snapshot Restore](assets/screenshot-snapshots.png) | ![Remote Sync](assets/screenshot-sync.png) |

| Configuration Market |
|:---:|
| ![Configuration Market](assets/screenshot-market.png) |

---

## 🔄 How it works?

### Export (pack it up)

```
Read your config → strip secrets (safe) → build manifest → compute checksums → pack into ZIP
```

### Import (restore the environment)

Every step confirms and backs up first — **it never modifies your config directly**:

```
Select ZIP → validate file → check integrity → check schema → compatibility check
    → scan contents → build import plan → preview & confirm
    → auto-backup current config → apply → validate → done
                      │
                      └─ failed midway? → automatically restored (rollback)
```

---

## 📥 Installation

It's a standard **DSH plugin** — two steps:

```bash
# ① Install the plugin
dsh plugin --profile web add dsh-config-manager@latest

# ② Restart DSH (a "Backup & Migration" entry appears in Settings)
```

> 💡 Just copy-paste the command: `@latest` ensures you get the newest build.
>
> 🐛 **`@latest` installed an old version?** That's pnpm 11's `minimumReleaseAge` supply-chain policy, not a cache issue: versions published less than ~30 days ago are excluded from resolution until whitelisted. Two fixes:
> - Install an exact version once (it auto-whitelists, then `@latest` works):
>   ```bash
>   dsh plugin --profile web add dsh-config-manager@0.1.8
>   ```
> - Or disable the age gate with a one-liner (adds `minimumReleaseAge: 0` at the top of the profile's `pnpm-workspace.yaml`):
>   ```powershell
>   $f = "$env:USERPROFILE\.dsh\profiles\web\pnpm-workspace.yaml"
>   $c = Get-Content $f -Raw
>   if ($c -notmatch '(?m)^minimumReleaseAge:') {
>     Set-Content -LiteralPath $f -Value ("minimumReleaseAge: 0`n" + $c) -Encoding utf8
>     Write-Output "Added minimumReleaseAge: 0"
>   } else {
>     Write-Output "Already present, nothing to do"
>   }
>   ```

---

## 🚀 Quick start (3-minute tour)

```
Machine A (export)
  1. Open DSH → Settings → "Backup & Migration"
  2. Click "Export Configuration" → choose "Quick Export"
  3. You get dsh-config-2026-08-14.zip (the report confirms no secrets inside)

Copy the