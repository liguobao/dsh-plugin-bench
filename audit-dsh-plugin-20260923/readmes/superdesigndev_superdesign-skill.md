# Superdesign: UI, presentations, and graphics for coding agents

**Stop shipping AI-slop UI.** Coding agents write great code and mediocre interfaces: generic layouts, default shadcn everything, no taste. Superdesign is the skill that gives your agent design judgment, so the UI it ships actually looks considered.

Install it once and your agent (Claude Code, Cursor, Codex, and 70+ others) can find real design direction and generate + iterate high-quality UI, presentations, and graphics on an infinite canvas, all without leaving your terminal.

> Powered by [superdesign.dev](https://superdesign.dev), the AI product design agent.

[![Superdesign skill demo](https://i.ytimg.com/vi/AZYJWyWZ6pQ/maxresdefault.jpg)](https://youtu.be/AZYJWyWZ6pQ)

*▶ Watch the skill in action.*

---

## What is Superdesign?

**Superdesign is an AI product design agent.** It gives coding agents (Claude Code, Cursor, Codex, and 70+ others) real design judgment, so the UI they ship looks considered instead of generic.

- **What it does** — finds design direction, sets up design systems, approves presentation outlines, and generates + iterates high-quality UI, slide decks, and graphics on an infinite canvas.
- **Who it's for** — developers, indie hackers, and product/UI designers who want to go from idea to shippable UI fast without leaving their coding agent.
- **How it's different** — style-preset skills just swap in a theme or a component library. Superdesign designs *into* your existing design system: it reads your code for context, gathers real style references, and produces branchable drafts you refine.
- **Cross-session continuity** — after the first real-codebase design, the skill remembers the project, draft, extracted components, and budgeted source-context bundle so later unchanged iterations resume without repeating codebase discovery.
- **Two ways in** — this skill from any coding agent, or the web app at [superdesign.dev](https://superdesign.dev).

> **Not the legacy IDE extension.** The archived open-source `superdesigndev/superdesign` VS Code extension is an older, separate project. This skill and [superdesign.dev](https://superdesign.dev) are the current, maintained product.

---

## Install

**Any coding agent** — installs the skill for any of the [70+ supported coding agents](https://github.com/vercel-labs/skills#supported-agents):

```
npx skills add superdesigndev/superdesign-skill
```

**Claude Code** — install it as a plugin instead, so it stays namespaced and updates with `/plugin update`:

```
/plugin marketplace add superdesigndev/superdesign-skill
/plugin install superdesign@superdesign
```

The skill is then invoked as `/superdesign:superdesign`. (Do not also run `npx skills add` in Claude Code — that installs a second, unnamespaced copy of the same skill.)

Either way, install the CLI it drives:

```
npm install -g @superdesign/cli@latest
superdesign login
```

## Use it

Just talk to your agent:

```
/superdesign help me redesign this settings page so it doesn't look like default AI slop
```

```
/superdesign set up a design system from my current codebase
```

```
/superdesign improve the design of my dashboard
```

```
/superdesign create an 8-slide presentation about our product launch
```

The skill handles the rest: it reads your code for context, gathers real style references, and produces design drafts you can branch and refine.

---

# Core scenarios (what this skill handles)

1. **Design or improve UI** (feature/page/flow)
2. **Create a presentation** with an editable approved outline
3. **Create graphics** (posters, covers, social posts, and ads)
4. **Set or extract a design system**
5. **Generate supporting images or video**

## Tooling overview

### A) Inspiration & Style Tools (generic, always available)

Use these to discover style direction, references, and brand context. Browse the full [prompt library](https://superdesign.dev/library) in the web app, or query it from the CLI:

- **Search prompt library** (style/components/pages)

  ```bash
  superdesign search-prompts --query "<keyword>"
  superdesign search-prompts --tags "style"
  superdesign search-prompts --tags "style" --query "<style keyword>"
  ```

- **Get prompt details** — read the compact index first, then fetch the full body only for the slug(s) you pick

  ```bash
  superdesign get-prompts --slugs "<slug1,slug2,...>"          # index
  superdesign get-prompts --slugs "<slug>" --full             # full body of the chosen slug(s)
  ```

- **Extract a site's design DNA from a URL** (style guide, tokens, content, brand, clone)
  ```bash
  superdesign extract-website --url https://example.com --design-md
  ```

### B) Canvas Design Tools

Use design agent to generate high quality design drafts:
- Create project (optionally seed a baseline draft from an HTML template via `--template`)
- Create design draft
- Iterate design draft (replace / branch)
- Plan flow pages → execute flow pages
- Fetch specific design draft
- Create a presentation from an approved ordered slide outline
- Read stored presentation outline and preferences for safe iteration
- List reusable Project Brand Assets

---

## Overall SOP for designing features on top of existing app:
1. Investigate existing UI, workflow
2. Setup design system file if not exist yet
3. Requirements gathering: ask the user using the session's available user-input mechanism; if none is available, ask in chat (optionally use Inspiration tools when needed)
4. Ask user whether ready to design in superdesign OR implement UI directly
5. If yes to superdesign
  5.1 Create/update a pixel perfect html replica of current UI of page that we will design on top of in `.superdesign/replica_html_template/<name>.html` (html should only contain & reflect how UI look now, the actual design should be handled by superdesign agent)
  5.2 Create project with this replica html + design system guide
  5.3 Start desigining by iterating & branching design draft based on designDraft ID returned from project


## Always-on rules
- Design system should live at: `.superdesign/design-system.md`
- If `.superdesign/design-system.md` is missing, run **Design System Setup** first.
- Ask high-signal questions about constraints, taste, and tradeoffs using the session's available user-input mechanism; if none is available, ask in chat.
- Read each command's default output directly — it is agent-optimized (compact TOON plus `help[]` next-step hints). Add `--json` only when you genuinely need the full machine-readable payload, and `--full` only to expand truncated fields.

---

## replica_html_template rules (Canvas only)

The purpose of replica html template is creating a lightweight version of existing UI so design agent can iterate on top of it (Since superdesign doesn't have access to your codebase directly, this is important context)

Overall process for designing features on top of existing app:
1. Identify & understand existing UI of page related
2. Create/update a pixel perfect replica html in `.superdesign/replica_html_template/<name>.html` (Only replicate how UI look now, do NOT design)
  - If design task is redesign profile page, then replicate current profile page UI pixel perfectly
  - If design task is add new button to side panel, identify which page side panel is using, then replicate that page UI pixel perfectly

**replica_html_template = BEFORE state (what exists now).** It provides context for Superdesign agent.
Actual design will be done via superdesign agent, by passing the prompt

The replica_html_template must contain **ONLY UI that currently exists in the codebase**. 
- **DO NOT** design or improve anything in the replica_html_template
- **DO NOT** add placeholder sections like `<!-- NEW FEATURE - DESIGN THIS -->`
- **DO** create pixel-perfect replica of current UI state
- Save to: `.superdesign/replica_html_template/<name>.html`

### Naming & Reuse

**Naming convention** 
Name replica_html_template for reusability: Use the page route (e.g., `