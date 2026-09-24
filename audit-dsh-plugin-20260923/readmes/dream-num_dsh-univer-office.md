![Univer × DeepSeek](docs/assets/readme/univer-deepseek-banner.png)

# DSH × Univer Office

> Give DeepSeek Harness a real office environment.
>
> Univer Office Plugin brings spreadsheets, docs, slides, canvases, relational tables, and more into one runtime — with connected data, validation, versioned changes, and isolated worktrees for multi-agent collaboration.

English · [简体中文](README.zh-CN.md)

[![npm](https://img.shields.io/npm/v/dsh-univer-office)](https://www.npmjs.com/package/dsh-univer-office)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D22.19-339933?logo=node.js&logoColor=white)](package.json)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

`dsh-univer-office` is the Univer office plugin for DeepSeek Harness (DSH). Tell the agent what you need and it can create or edit spreadsheets, documents, presentations, multidimensional tables, and canvases, or work with existing Excel, Word, and PowerPoint files. Every change is verified and stays in the conversation for you to preview, approve, or discard.

After installation, describe the result you want in natural language. The agent handles creation, editing, and verification while you follow the work live and review the result in the conversation. Deliver spreadsheets as Excel (`.xlsx`), documents as Word (`.docx`), and presentations as PowerPoint (`.pptx`) files when needed.

## See it in action

[![Play the DSH × Univer Office demo](docs/assets/readme/nike-presentation-demo.png)](https://www.youtube.com/watch?v=k-2zW_CMiew)


The agent created this spreadsheet from a natural-language request, then added conditional formatting and a chart in the same conversation. The result can be previewed, revised, merged into the current version, or discarded in place.

![Reviewing a spreadsheet with conditional formatting and a chart in DSH](docs/assets/readme/chart-and-formatting.png)

> **Deliver a standard Excel file:** after review, ask the agent to export the spreadsheet as `.xlsx` so it can be opened and edited in Excel, WPS Office, and other compatible office applications.

<details>
<summary>See the complete workflow from request to review</summary>

### 1. Describe the task in natural language

![Asking the agent to create a class score sheet](docs/assets/readme/spreadsheet-request.png)

### 2. Follow the result live while the agent works

![A live spreadsheet window while the agent works](docs/assets/readme/live-worktree.png)

### 3. Approve or discard the changes in the conversation

![The spreadsheet review card after the task completes](docs/assets/readme/review-result.png)

</details>

### Generate a presentation from one request

Give the agent a topic, audience, page count, content outline, and visual direction. It can build the complete presentation, verify content and layout page by page, and leave the result in the conversation for review.

![Reviewing a bubble sort teaching presentation in DSH](docs/assets/readme/presentation-review.png)

> **Deliver a standard PowerPoint file:** after review, ask the agent to export the presentation as `.pptx` so it can be presented and edited in PowerPoint, WPS Office, and other compatible office applications.

<details>
<summary>See the presentation workflow from request to finished deck</summary>

#### 1. Specify the topic, audience, and page requirements

![Asking the agent to create a bubble sort teaching presentation](docs/assets/readme/presentation-request.png)

#### 2. Follow and verify the pages while the agent works

![A live presentation window while the agent works](docs/assets/readme/presentation-live.png)

</details>

## What can it do?

- **Analyze and build spreadsheets** — read or create Excel data, clean fields, write formulas, apply formatting and validation, create tables, charts, pivots, filters, sparklines, conditional formatting, and images, then export the result as `.xlsx`, `.csv`, or `.tsv`.
- **Write and lay out documents** — create paragraphs, rich text, lists, tasks, tables, images, charts, headers, footers, pagination, and page layouts.
- **Create and revise presentations** — generate a deck from an outline, redesign selected pages, edit text, shapes, images, tables, charts, and transitions, then detect off-page, overflowing, and overlapping text.
- **Build lightweight databases** — create Base tables, fields, records, and views with formula fields, filters, sorting, grouping, and Sheet-backed references.
- **Draw editable canvases** — create shapes, text, connectors, images, native charts, and diagrams, with connector and layout analysis.
- **Compose several content types** — one `.univer` file can contain Sheets, Docs, Slides, Bases, and Boards. Formulas and embedded content can reference other content in the same file.
- **Work with Office files** — import `.xlsx`, `.csv`, `.tsv`, `.docx`, and `.pptx`, then export the edited content in the matching format.
- **Review agent changes safely** — every write starts in an isolated draft. Watch changes live, then approve or discard them instead of letting the agent overwrite the current version.
- **Compare worktree changes semantically** — switch a draft or submitted worktree from View to Compare to inspect Sheet, Doc, Slide, Base, or Board changes side by side against a pinned trunk version or another active worktree.

### Example requests

```text
Create a simple payroll spreadsheet with employee, base salary, bonus, deduction, gross pay, and net pay columns. Calculate the totals automatically.

Create a six-slide lesson deck about bubble sort. Explain the concept, each comparison pass, pseudocode, and complexity, and check every page for layout problems.

Create a formal weekly project report with an executive summary, this week's progress, a risk table, next week's plan, headers, and footers, then export it as docx.

Create a customer-tracking Base with company, contact, stage, expected value, and next action fields, plus a view grouped by stage.

Create a sales Sheet and a summary Slide in the same .univer file, with the Slide chart reading the Sheet data.
```

## Capabilities

| Content | Create and edit | Verify and review | Import | Export |
| --- | --- | --- | --- | --- |
| Sheet | Cells, formulas, styles, tables, charts, pivots, filters, validation, images, and more | Structured range inspection, recalculation, screenshots, PDF printing, live preview | `.xlsx` `.csv` `.tsv` | `.xlsx` `.csv` `.tsv` |
| Doc | Paragraphs, rich text, lists, tasks, tables, images, charts, headers, footers, pagination | Document readback, page screenshots, PDF printing, live preview | `.docx` | `.docx` |
| Slide | Pages, text, shapes, images, tables, charts, SVG layouts, transitions | Structure inspection, layout lint, screenshots, PDF printing, live preview | `.pptx` | `.pptx` |
| Base | Tables, fields, records, views, formulas, filters, sorting, grouping | Structured data checks, workbench screenshot, live preview | — | `.xlsx` `.csv` `.tsv` |
| Board | Shapes, text, connectors, images, native charts, routing | Element analysis, screenshots, PDF printing, live preview | — | — |

Every content type supports isolated draft editing, side-by-side semantic comparison, review, revision, approval, and discarding. Base and Board support structural verification; Board file export is not yet supported.

## Get started in 3 minutes

### 1. Install the plugin

Supported DSH versions are `0.1.5-rc.1`, `0.1.6-alpha.1`, and their later `0.1.x` releases (`^0.1.5-rc.1 || ^0.1.6-alpha.1`).

If DSH is running, first press **Ctrl+C** in the terminal that started it. You can run the installation command while DSH is running, but the current DSH process will not load the new plugin automatically.

Install the plugin from npm:

```sh
dsh plugin --profile web add dsh-univer-office
```

Restart DSH after installation:

```sh
dsh web
```

After DSH starts successfully, refresh the existing DeepSeek Harness browser page with **Cmd+R / Ctrl+R**.

### 2. Describe what you ne