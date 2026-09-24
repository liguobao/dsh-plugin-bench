# dsh-emacs — an Emacs client for DeepSeek Harness

**dsh-emacs** brings [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)
(`dsh`) into Emacs: streaming replies, tool calls, thinking blocks, slash
commands, file/session references, and model selection. It uses Emacs
built-ins (Emacs 27.1+) with no third-party dependencies.

![Chat buffer with streaming replies and tool calls](assets/chat.png)

> **0.4.1** targets the **dsh 0.1.5** wire protocol (server **0.1.5-rc.1 or
> newer**).

## Quick start

You need **Emacs 27.1+** and a provider/model configured in dsh to send
messages. dsh-emacs can install and start the dsh server for you; provider
credentials and model configuration remain in dsh. For an existing local or
remote server, set its address as described in [Server setup](#server-setup)
before connecting.

1. Clone the repository:

   ```sh
   git clone https://github.com/vritser/dsh-emacs.git ~/dsh-emacs
   ```

2. Add this to your Emacs configuration and evaluate it, or restart Emacs:

   ```emacs-lisp
   (add-to-list 'load-path (expand-file-name "~/dsh-emacs"))
   (require 'dsh-emacs)
   ```

3. Run `M-x dsh-emacs` to open the session list. If no local server is
   running, dsh-emacs starts one, offering to install the CLI if it is missing.
   On a fresh dsh setup, use `M-x dsh-emacs-open-web` to configure your
   provider and model before sending a message.
4. Press `c` in the session list to create a session. Use `C-c C-m` in the
   chat buffer to choose a model if needed.
5. Type after the `❯` prompt and press `C-c C-c` to send your first message.

For an optional `use-package` setup, see
[Example configuration](docs/customization.md#example-configuration).

## Using it

### Session list

`M-x dsh-emacs` opens your sessions, grouped by workspace. Press `c` to
create a session or `RET` to open one. See
[Session and workspace controls](docs/customization.md#session-and-workspace-controls)
for list management and navigation.

![Session list grouped by workspace](assets/sessions.png)

### Inside a chat buffer

| Key | What it does |
|---|---|
| `C-c C-c` | Send input or interrupt; see below |
| `C-c C-b` | Interrupt the running turn |
| `C-c C-q` | Manage the pending queue |
| `C-c C-g` | Open the goal-action prefix |
| `C-c C-m` | Switch model / reasoning effort |
| `C-c C-a` | Attach an image |
| `C-c C-s` / `C-c M-s` | Switch session in this workspace / across all |
| `C-c C-r` | Refresh |
| `C-c C-o` | Load older messages above the current transcript |
| `C-c C-w` | Copy (region → code block → message at point → last reply) |
| `C-c C-f` | Toggle mode-line stats |
| `C-c C-!` | Stop the tracked local shell process |
| `M-p` / `M-n` | Previous / next input |
| `C-/` / `C-_` / `C-x u` | Undo input editing; redo with `C-g C-/`, or `undo-redo` on Emacs 28+ (the transcript is never undone) |
| `TAB` | Complete a slash command |

**Sending during a running turn:** by default, `C-c C-c` queues a non-empty
message for the next turn. `C-u C-c C-c` steers the running turn instead;
`C-c C-c` with empty input interrupts it. Configure this with
`dsh-emacs-busy-enter-behavior`. The `C-c C-q` queue menu acts on the
highlighted item; `x` deletes all pending items.

Type **`@`** to choose file, directory or session references: `@src/` drills
into a directory and `@session-title` mentions another session. See
[@ references](docs/reference.md).

Type **`/`**, then press **`TAB`** to complete a slash command. Automatic
popups depend on your completion front-end and its settings: corfu/company
can provide them with auto completion enabled; stock completion,
vertico and icomplete require `TAB`. See
[Slash commands](docs/slash-commands.md#three-ways-to-run-a-command).

**`TAB`** completes a **local file path** once the token carries a separator:
`docs/rp`, `./src/`, `~/…` and `/abs/…` complete through the stock file-name
completer against the chat buffer's working directory — the session workspace
— with the same directory drill-down as `find-file`, the path suffix after
the cursor preserved, and the active completion styles (abbreviated
directories work with `partial-completion`). A leading `/name` is reserved
for slash commands even when their catalog is empty; type the next `/` or put
the path after prose to complete an absolute path. Completion reads the
machine Emacs runs on, like `!` shell lines — with a dsh server on another
host, use an `@` reference instead. A path with spaces is not handled in
plain text (the token ends at the space); quote it as an `@` reference.

**`TAB`** also completes an ordinary word from what is already in the buffer:
the draft above point and, within `dsh-emacs-word-completion-limit`
characters, the transcript above it — so a term from an earlier message or
tool result completes instead of being retyped. Words are runs of letters,
digits, `_` and `-`, so identifier-like terms such as `dsh-emacs-mode`
complete whole. Candidates appear nearest-first, and completion inside a
word includes the existing suffix. Slash commands and `@` references keep
their own completion even when their catalogs are empty.

The composer shows the current goal and the next pending message above `❯`.
Hover over the preview for its full text, or use `C-c C-q` to manage pending
messages. Goal shortcuts and inline controls are described in
[Goal actions](docs/customization.md#goal-actions).

Expanded file-edit cards show unchanged lines once as context, with red/green
rows and totals for the changes. See
[Tool cards](docs/ui-styling.md#tool-calls-dsh-web-style) for the display
rules, including the limit for very large replacements.

### Answering questions

Agent `ask` prompts are answered in one minibuffer read. The question text is
the prompt, the options are the completion candidates (each one carries its
description as an annotation), and the question detail shows in the echo area.

- Single choice: pick a candidate, `RET` accepts it. Empty input skips the
  question.
- Multiple choice: type the options comma-separated — `2,3` or `alpha,beta` —
  and `RET` submits them (`completing-read-multiple`, Emacs' standard
  comma-separated input path). An unambiguous prefix works too (`alph`), and
  an ambiguous one is left as your answer text rather than guessed.
- Anything that names no option is taken as your answer text, like at any
  Emacs completion prompt — there is no separate "type an answer" step, and
  a partly-matched answer is never silently trimmed.
- `C-c C-s` skips the question (empty input does the same); `C-g` abandons
  the whole group.

Nothing is toggled in place and the reader never reopens: one read per
question, so the menu cannot flicker or reorder.

```elisp
(setq dsh-emacs-question-help-display 'echo-area) ; default; nil hides the detail
```
Try `M-x dsh-emacs-question-preview` locally, without contacting a server.
See [Question prompts](docs/customization.md#ask-question-prompts) for details.

### Workspaces

Workspaces group sessions by project/directory.

New sessions use the current workspace when created from a workspace header,
its empty New Session row, or an existing chat. Without that context, a
**local server** can use the Emacs project of the current buffer's directory,
creating its workspace on first use. This detection is controlled by
`dsh-emacs-new-session-auto-project` and does not run for remote servers.
Otherwise the new session uses the current buffer's directory.

### Local shell commands

Enter `!git status` and press `C-c C-c` to run a command locally in the
session's workspace directory. Output appears in the transcript, including
while a model turn is running. `C-c C-!` stops the tracked shell process.

Shell output is not sent to the model or saved in server history; refreshing
the transcript removes it. With attachments, a leading `!` is caption text
sent to the model. See [Shell commands](docs/shell-commands.md) for multiline
scripts, shell selection and process handling.

### Models & pr