
![preview](docs/preview.png)

> **Requires DeepSeek Harness ≥ 0.1.5 (compatibility update)**
>
> This plugin line is adapted for **DeepSeek Harness 0.1.5+**, which ships the official right sidebar (`ui-sidebar-right`). Workbench panels (Git, Usage, terminal, browser, control plane, and more) dock into that host sidebar instead of only using the plugin’s own chrome.
>
> On older harness versions you may still see an **update available** notice, but **install is refused** so your environment is not broken. Upgrade DeepSeek Harness to **0.1.5 or newer** first, then install or upgrade this plugin.

A workbench plugin for the [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) Web UI. After Workbench is opened in Conversation, chat stays on the left. Two columns appear on the right: the editor (**Agent Control Plane**, syntax highlighting, and **smart terminal**) and the side dock for files, Git, the **Usage** panel, and the **Ultra Slash** panel.

Look for these first:

- **Usage** — official API balance, this-machine observed spend, this-session tokens and context. Pin it above the left **Settings** button so you can see spend while chatting.
- **Agent Control Plane** — the editor’s first tab by default. Two pages: **Execution trajectory** (timeline fishbone of user → LLM → tools → agent reply, with expandable I/O) and **Capabilities** (current-session agent model, tools, prompt sections, and session knobs). Toggle visibility in Settings.
- **Ultra Slash** — slash commands that inject guidance **without stopping the current turn**. Manage them in the right dock; send them from the bottom group of the chat `/` menu.
- **Canvas** — live React previews for product prototypes, dashboards, and custom visuals. Agent-written files live under `.canvas/*.canvas.tsx` in the workspace (not in IDE config folders). After a write, the workbench **auto-opens** the file in **preview**; switch to edit or split like Markdown. Send `/canvas <topic>` to steer the model without interrupting the turn.
- **Smart terminal** — a local PTY in the editor. Real shell lines (including pasted `$ ls`) run as-is. Natural language is translated by **AI command assist** (<kbd>Alt</kbd>+<kbd>I</kbd> or the ✨ button) and typed into the **current** terminal. Notes are never executed. A blacklist blocks destructive commands the assistant would otherwise type. <kbd>Alt</kbd>+<kbd>J</kbd> opens another terminal tab.
- **Add to chat** — hand the model anything without copying and pasting. Drag a file from the tree (or a DevTools network request) into the chat box; right-click terminal output to add the selection or recent output (with its pwd/shell context); or tap the **point-and-pick** button in the embedded browser and click a page element. Each lands as a reference chip in the input and rides along with your next message.
- **AI commit messages** — in the right-dock **Source Control** tab, generate a message from staged changes; the text streams into the commit box. The template is editable.

- **Notification sounds** — when a session finishes while you are away or is waiting on you (approval, plan confirmation, question), the workbench plays a chime. Pick one of 5 built-in Web Audio sounds or upload your own audio (mp3, ogg, wav, webm, m4a, flac, up to 50 MB); a loop reminder keeps replaying it every N seconds (default 10) until the item is handled. The master switch, sound picker, and loop interval live in the workbench **Settings** panel.

## Contents

- [Interface](#interface)
- [Core capabilities](#core-capabilities)
- [Feature list](#feature-list)
- [Agent Control Plane](#agent-control-plane)
- [Usage panel](#usage-panel)
- [Ultra Slash](#ultra-slash)
- [Canvas](#canvas)
- [Smart terminal](#smart-terminal)
- [Workspace terminal](#workspace-terminal)
- [AI command assist](#ai-command-assist)
- [Capability matrix](#capability-matrix)
- [Release](#release)
- [Installation](#installation)
- [Upgrade](#upgrade)
- [License](#license)

## Interface

The workbench uses a three-column layout. Conversation stays on the left. The two columns on the right are the capability area: editor (**Agent Control Plane**, syntax highlighting, smart terminal) in the center; file tree, Git, Usage, and Ultra Slash on the far right. The right dock tabs are **Files**, **Source Control**, **Usage**, and **Ultra Slash**. The editor’s first tab is **Control Plane** by default.

### DeepSeek-Harness >= V0.1.5

![screen_8](docs/img/screen_shot_8.png)

### Previous Version

![screen_0](docs/img/screen_shot_0.png)
![screen_1](docs/img/screen_shot_1.png)
![screen_2](docs/img/screen_shot_2.png)
![screen_3](docs/img/screen_shot_3.png)
![screen_4](docs/img/screen_shot_4.png)
![screen_5](docs/img/screen_shot_5.png)
![screen_6](docs/img/screen_shot_6.png)
![screen_7](docs/img/screen_shot_7.png)


## Core capabilities

1. **Workbench layout.** Three columns: Conversation on the left, editor and terminal in the center, files / Git / Usage / Ultra Slash on the right. A new session opens the workbench immediately. By default the editor is collapsed, the files sidebar is open, and usage is pinned above Settings. Columns can be resized, collapsed to icon rails, and restored. Collapse, the side-dock tab, and the usage pin are remembered globally across reload and new sessions.
2. **Smart terminal.** A local PTY. Real shell lines (including pasted `$ ls`) go straight to the terminal; natural language is translated and typed into the **current** shell. Notes are non-executable. A configurable blacklist blocks destructive commands the assistant would otherwise type.
3. **Agent Control Plane.** First editor tab (on by default; toggle in Settings). **Execution trajectory** shows a threaded feed with a left rail for each LLM round, tool call, and agent reply (expand for full I/O). **Capabilities** lists the current session agent’s model, tools, prompt sections, sub-agents, and session knobs you can adjust online.
4. **Workspace editor.** CodeMirror 6 with syntax highlighting, Plain / Emacs / Vim keymaps, Markdown edit / preview / split, **Canvas edit / preview / split** (React render of `.canvas/*.canvas.tsx`), image and spreadsheet previews, Git diffs, tabs, breadcrumbs, save and dirty-close guards.
5. **Files.** Tree browse, filter, hidden files, `.gitignore` marks, new / rename / delete, and open in a local editor (Cursor, VS Code, and others).
6. **Git.** Status, stage, commit (including streamed AI messages), fetch / pull / push with safety checks, branches, merge, restore, commit graph, `git init`, and model-facing `git_*` tools.
7. **Usage panel.** Official API balance, this-machine observed spend, this-session tokens and context. Open the right-dock **Usage** tab, or pin the panel above the left **Settings** button (including the collapsed icon rail). The status bar always shows the balance next to **Feedback**.
8. **Ultra Slash panel.** Slash commands that inject guidance into the next model step **without interrupting the current turn**. Open the right-dock **Ultra Slash** tab to manage them; type `/` in chat and pick from the bottom Ultra Slash group. Built-in: `/steer`, `/new`, `/skill`, `/docs`, `/canvas`. Custom `/name` shortcuts are stored on this machine and shared by every session.
9. **Status bar.** Open-file tabs, balance, Feedback, version / upgrade, workspace path, branch, dirty count, editor mode.
10. **Maintenance & privacy.** In-UI upgrade checker, Chinese / English UI, and redaction of tokens in paths and errors.

## Feature list

### Workbench

- Three-column layout: Conversation | editor + terminal | files / Git / Usage / Ultra Slash
- Right-dock tabs: **Files**, **Source Control**, **Usage**, **Ultra Slash**
- Opens as soon as you create a session; no first message required
- Header **Workbench** button shows or hides the whole workbench
- Drag column widths; double-click a sash to reset; widths are remembered
- Collapse Conversation, editor, or the right dock into a narrow icon rail

### 