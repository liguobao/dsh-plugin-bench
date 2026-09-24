<p align="center">
  <img src="assets/branding/dsh-banner-en.webp" alt="DSH Archive Manager" width="100%">
</p>

<div align="center">

  # DSH Archive Manager

  **Safely manage archived sessions in DeepSeek Harness**

  [简体中文](README.zh-CN.md) · [Changelog](CHANGELOG.md) · [Apache-2.0](LICENSE)

  [![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
  [![npm package](https://img.shields.io/npm/v/%40michengai%2Fdsh-archive-manager.svg?label=npm%20package)](https://www.npmjs.com/package/@michengai/dsh-archive-manager)
  [![npm downloads](https://img.shields.io/npm/dt/%40michengai%2Fdsh-archive-manager.svg?label=npm%20downloads)](https://www.npmjs.com/package/@michengai/dsh-archive-manager)
  [![DSH Web Plugin](https://img.shields.io/badge/DSH%20Web-Plugin-0f766e.svg)](https://github.com/MichengAI/dsh-archive-manager)
  [![DSH supported through 0.1.7-rc.1](https://img.shields.io/badge/DSH-up%20to%200.1.7--rc.1-2563eb.svg)](#prerequisites)
</div>

> DSH Archive Manager is a community-maintained DeepSeek Harness (DSH) plugin, not an official DeepSeek AI product.

## What you can do

Put inactive conversations away and find them again when needed, keeping everyday task lists tidy.

- **Archive conversations**: put away one chat or all unarchived chats in a workspace.
- **Find past work**: search titles and content, combine project/favorites/date filters, and sort by time, title, or turns.
- **Restore tasks**: restore one chat, selected chats, or a project group; select all filtered results for bulk actions.
- **Clean up records**: permanently delete unwanted archives after confirmation, track batch progress, and retry remaining items.
- **Organize important chats**: save favorites and preview idle cleanup while protecting favorites and active work.
- **Inspect and troubleshoot**: preview without restoring, copy IDs/paths, diagnose errors, and repair supported legacy logs.

> This README describes 1.0.0. See the [changelog](CHANGELOG.md) for the complete feature list and upgrade boundaries.

## Session diagnosis and repair

The archive page collects read failures, including archived IDs with missing summaries. Expand **Diagnosis and repair**, choose **Diagnose session**, then **Confirm repair** only when eligible. Repair converts supported legacy automation message sources while retaining the original log, conversation text, and automation attribution. Sessions must be archived and closed in every DSH process. Missing files, permission failures, and unsupported corruption are reported; messages are never truncated or deleted to force recovery. Eligibility is verified from artifacts and the host format, not solely from error wording.

## Search and preview

- Archived and Unarchived share title/content search, project, favorites, updated-date filters, and creation-time sorting. Star or unstar conversations on either tab.
- Choose **Titles and content** to search user and assistant text; the default remains titles only. Date filters include the entire local end date and combine with project and favorites.
- Matches show snippets and highlights. On Archived, click a snippet or **More → Quick preview** to inspect context without restoring. On Unarchived, a snippet opens the full conversation.
- Preview renders Markdown tables, quotes, and code blocks with role labels; switch to source text for highlights. It shows up to eight recent messages, or context around the first match. Each message is limited to 2,000 UTF-16 code units without splitting Unicode characters.
- Search accepts up to 200 query characters and reads batches of at most 20 sessions, sequentially within each batch. Tools, attachments, reasoning, system messages, and plugin injections are excluded. Read failures remain visible and can be retried. Stored text is not the model's current context.
- There is no persistent full-text index. Large or long conversations can be slow; narrow project, dates, or favorites first. No session-count or latency guarantee has been established. Changing filters prevents later batches and stale results, but cannot interrupt the batch already reading.

## Turn counts and location

- Both tabs show user submission counts, including image submissions; assistant replies, tool calls, and injected messages do not count as turns.
- Sort by most or fewest turns; unknown counts remain last. Failed details can be retried.
- **More** provides separate ID/path copying. Official JSONL storage returns the session directory; other backends use a valid host-provided path. Clipboard operations require browser permission and HTTPS or localhost; failures are reported.
- Details are read in batches of up to 20 without activating or restoring sessions. Counts include inherited user messages, have no persistent index, and may take time for long logs.

## Screenshots

Search, favorite, preview, restore, and clean up in **Settings → Archived sessions → Archived**:

![Archived: shared search filters, favorites, and restore](assets/screenshots/archived-sessions.webp)

Switch to **Unarchived** for the same filters, idle cleanup previews, and project-wide archiving:

![Unarchived: idle cleanup and project archiving](assets/screenshots/unarchived-sessions.webp)

> Screenshots show the pre-release development build labeled 0.1.44; this release is 1.0.0. The sidebar belongs to the installed UI plugin and does not represent new sidebar features in this release.

## Prerequisites

- A working [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) Web installation with `dsh` available in your terminal.
- Supported DSH versions: `0.1.0-rc.8`, `0.1.1-rc.2`, `0.1.2-rc.1`, `0.1.5-rc.1`, `0.1.5-rc.2`, and `0.1.7-rc.1`. Other versions are not currently supported.
- Node.js matching `^22.19.0 || >=24.0.0`. Source installation also requires pnpm.

## Installation

Examples use the `web` profile. Replace it with the profile you actually use.

### Ask an agent to install it

Send this prompt to an agent that can run terminal commands on your computer:

```text
Install the latest @michengai/dsh-archive-manager into my local DSH web profile using the official npm registry. Check the plugin configuration afterward, then explain how to reload DSH and open archived session management.
```

### Install manually

Run in PowerShell:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

dsh plugin --profile web add @michengai/dsh-archive-manager@latest --registry=https://registry.npmjs.org/
```

Restart DSH Web, then hard-refresh your browser with `Ctrl+Shift+R`. Open **Settings → Archived sessions** to get started.

## Usage

| Goal | Action |
| --- | --- |
| Archive one chat | Open its sidebar menu and choose **Archive session** |
| Archive a workspace | Open the workspace menu and choose the option to archive its chats |
| Find an archive | Open **Settings → Archived sessions**, then choose title/content search or filter by project, favorites, and dates |
| Change the order | Sort by update time, creation time, title, or most/fewest turns |
| Restore one chat | Click the restore icon, or choose **More → Restore and open** |
| Archive a project or ungrouped chats | On **Unarchived**, open the group’s **…** menu and confirm archiving all chats in that group, regardless of search filters |
| Favorite a chat | Click its right-side star; use the favorites dropdown to filter |
| Preview archived content | Click a match snippet or **More → Quick preview** |
| Clean up idle chats | On Unarchived, set idle days, preview candidates, and confirm |
| Locate a session | Copy its ID or path from More |
| Handle read errors | Expand diagnosis, diagnose first, and confirm repair when eligible |
| Archive across projects | Switch to **Unarchived**, select sessions across projects, then click **Archive** and confirm |
| Restore or delete in bulk | Select chats and use the bulk actions, or use the project menu; the