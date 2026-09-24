<div align="center">

# ⏱️ dsh-automation

### *Run coding tasks on schedule. Manage them from Web or Agent.*

[![DeepSeek Harness](https://img.shields.io/badge/DeepSeek%20Harness-plugin-4D6BFE)](https://github.com/deepseek-ai)
[![Version](https://img.shields.io/badge/version-0.1.7-4D6BFE)](package.json)
[![Node.js](https://img.shields.io/badge/Node.js-22.19%2B-4D6BFE)](package.json)
[![License: MIT](https://img.shields.io/badge/license-MIT-4D6BFE)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/titanwings/dsh-automation?style=social)](https://github.com/titanwings/dsh-automation/stargazers)

<br>

<table>
<tr><td align="left">

🕒 &nbsp;Need recurring or one-shot coding work to run later without relying on an old chat?<br>
🧭 &nbsp;Need each unattended run to stay inside an explicit workspace and permission boundary?<br>
🧾 &nbsp;Need to inspect what ran, which revision it used, and how it ended?

</td></tr>
</table>

### ✨ dsh-automation turns all three requirements into one workflow.

Create and manage schedules from DSH Web or any eligible root Agent. Every
dispatched occurrence starts in a fresh root Agent and Session, then leaves an
auditable record.

**Self-contained task + schedule + permission boundary → fresh root Agent + fresh Session + durable run history**

<br>

[Why automation](#why-automation) · [Features](#features) · [Install](#install) · [Quick start](#quick-start) · [Safety](#a-schedule-is-not-permission) · [Technical details](#technical-details)

**English** · [简体中文](README.zh-CN.md)

<br>

![dsh-automation — Schedule. Run. Remember.](docs/social-preview.png)

</div>

---

![Automation dashboard showing workspace rules, next runs, and recent outcomes](docs/01-dashboard-en.png)

<a id="why-automation"></a>

## 🎯 Why automation

DSH Core Schedule is the right tool for reminders in the current conversation: “come back to this Session in ten minutes.” `dsh-automation` handles a different job: “run this complete task independently every weekday and leave me a result I can inspect.”

| | DSH Core Schedule | dsh-automation |
| --- | --- | --- |
| Execution context | Returns to the same live Agent | Starts a fresh root Agent and Session |
| Input | A follow-up inside existing context | A saved, self-contained task |
| Scope | Current Session Log | One canonical DSH workspace |
| History | Conversation events | Definition revisions and durable run records |
| Best for | Reminders and same-chat follow-ups | Repeated or one-shot standalone coding work |

If a task depends on unstated chat history, needs an interactive approval halfway through, or should react to a file, HTTP, or process condition rather than time, it is not a good automation yet.

---

<a id="features"></a>

## ✨ Features

### 🕹️ One control plane, two ways in

- **DSH Web:** open **Automations** from the sidebar or the conversation tab to create a rule, pause or resume it, run it now, delete it, and inspect recent runs. On the blank New Session screen, the sidebar shortcut tells you to start a conversation instead of failing silently.
- **Any eligible root Agent:** ask in natural language. Six scoped tools let the Agent manage automations only for its exact workspace.

There is no separate bot, daemon UI, or third-party scheduler to operate.

### 📅 Schedules people can read

Create a one-shot, fixed-interval, daily, or weekly rule. Daily and weekly schedules use an IANA time zone; the friendly form is normalized into a validated RFC 5545 RRULE for persistence and inspection.

![Create form with schedule, time zone, and permission boundary](docs/02-create-en.png)

### 🧠 A model target for each automation

The Web form can follow the live global model or pin one provider/model pair. A pinned model can use its own default reasoning effort or one of the opaque effort values advertised by that exact model. The card shows the saved target, and each run keeps the same target in its immutable snapshot.

Agent tools expose the same fields. Omitting all model fields on create preserves the existing behavior of capturing the creating Session's complete selection; explicitly setting `provider` and `model` to `null` follows the live global selection at run time. On update, omitted fields stay unchanged, `null` clears a pin, and changing the route without an effort resets to the new model's default.

### 🧼 A clean execution boundary every time

Each dispatched occurrence receives:

- a new Session ID and fresh root Agent;
- the saved prompt, not the source conversation history;
- the captured workspace, cwd, Agent preset, permission preset, and a durable model target that either follows the live global selection or pins one model and optional reasoning effort;
- an explicit `automation` message source containing the automation ID, run ID, and scheduled time;
- a terminal result derived from the actual DSH turn end, not merely “message delivered.”

### 🧾 History that explains failure as well as success

Runs progress through `queued`, `running`, and a terminal state such as `succeeded`, `failed`, `skipped`, or `cancelled`. Each record keeps its definition revision, prompt and target snapshot, scheduled time, result Session ID, bounded summary, and structured error.

![Run history with a completed run, an interrupted failure, summaries, and result Session links](docs/03-run-history-en.png)

Updating a definition increments its revision, so each retained run still identifies what it executed. Deleting the definition does not immediately erase those run records. Retention removes only the oldest terminal records; queued and running records are never pruned.

Set `archiveRunSessions: true` in the Cordis plugin config to archive completed, failed, cancelled, and other terminal run Sessions from the ordinary DSH conversation list. Their logs are not deleted: the Automations run history keeps the Session ID, summary, and error as an auditable inbox. Current Harness releases do not expose an unarchive API, so an archived result is labeled instead of offering a broken Session-open action. The default is `false` and preserves ordinary Session navigation.

---

<a id="install"></a>

## ⚡ Install

Install the GitHub bundle into the DSH Web profile, then restart `dsh web`:

```bash
dsh plugin --profile web add github:titanwings/dsh-automation#v0.1.7
```

The version tag keeps the install reproducible; a reviewed commit SHA is equally valid. If you run DSH from its source checkout, use `pnpm dsh` in place of `dsh`.

<details>
<summary><strong>Install from a local checkout</strong></summary>

<br>

Node.js 22.19 or newer is required.

```bash
git clone https://github.com/titanwings/dsh-automation.git
cd dsh-automation
pnpm install
pnpm check

cd /path/to/deepseek-harness
pnpm dsh plugin --profile web add /absolute/path/to/dsh-automation
```

The repository ships its built Host and Web bundles. Git installation runs no
package build script and needs no `allowBuilds` entry.

</details>

---

<a id="quick-start"></a>

## 🚀 Quick start

### 🖥️ From DSH Web

1. Open a Session attached to the workspace you want to automate.
2. Open **Automations** from the sidebar, or select it next to Chat and Trajectory. If the New Session screen is still blank, start the conversation first.
3. Enter a self-contained task, schedule, IANA time zone, model target, and permission boundary.
4. Use **Run now** once before relying on the schedule; inspect the resulting Session and run record.

### 💬 Ask an Agent

Once installed, eligible root Agents receive the management tools. For example:

```text
Create a read-only automation called "Weekday regression triage" for this workspace.
Run it Monday through Friday at 09:30 in Asia/Shanghai. Inspect the latest local test
evidence, identify regressions, and return a short report. Do not modify files.
```

| Tool | Purpose |
| --- | --- |
| `automation_create` | Create a workspace-bound standalone rule, optionally with a pinned model and reasoning effort. |
| `automatio