<p align="center">
  <img src="branding/app-icon.png" alt="DeepDeck app icon" width="96" height="96">
</p>

<h1 align="center">DeepDeck</h1>

<p align="center">
  Build and reuse WebMCP tools in a macOS desktop workspace for DeepSeek Harness.
</p>

<p align="center">
  <a href="https://github.com/jo32/DeepDeck/releases/latest"><strong>Download for Mac · Apple Silicon / Intel</strong></a> ·
  <a href="https://deepdeck.getmegaportal.com/">Website</a> ·
  <a href="#try-it">Try it</a> ·
  <a href="plugins/browser/README.md">Browser guide</a>
</p>

Describe a website task. DeepDeck's Agent can use the site's existing WebMCP tools, or explore its interface and build tools you can inspect and reuse later. Source and saved versions stay available for review, disabling, and rollback.

| Build tools for a website | Reuse them for a task |
| --- | --- |
| ![Builder reports creating and validating 23 tools for X](apps/web/public/webmcp/building-webmcp.png) | ![Use mode calls saved tools to prepare a Hello world draft without publishing](apps/web/public/webmcp/use-webmcp.png) |
| In this X example, Builder creates 23 tools for reading pages, searching, and editing drafts. | Switch to Use and ask for a Hello world draft. The example fills the draft without publishing it. |

Initial exploration and verification take time and tokens. Reuse benefits depend on the task and tool design; site changes can require revalidation. Measured savings are not yet established.

### Try it

1. [Download the latest release](https://github.com/jo32/DeepDeck/releases/latest), choose the DMG for your Mac, and open DeepDeck. Set up a model in Settings if you have not already configured Harness.
2. Open **Browser**, visit a site, and open **Site Agent → WebMCP** to inspect any tools the website provides.
3. If a needed tool is missing, switch to **Builder** and describe what it should do. Review the generated tools and validation results, then return to **Use** and ask for the task.

DeepDeck is a macOS desktop application. Install it from Releases; a generic `dsh plugin add` command does not install the desktop app or its native browser bridge. For development from source, see [First run](#first-run).

## Highlights

### Browser + WebMCP

**[Download the latest DeepDeck release](https://github.com/jo32/DeepDeck/releases/latest)** for Apple Silicon and Intel Macs.

**Let the Agent use a website, then keep what it learns as WebMCP tools.** You describe the goal. The Agent explores the real site, tries its workflows, checks the results, and saves the working operations as reusable tools. Building WebMCP is like preserving the Agent's experience of using the website, so future tasks can reuse it without a person writing step-by-step instructions.

That experience lives in inspectable, executable tools: how to search, read results, or edit and verify a draft. DeepDeck Browser supports both **reusing WebMCP tools that already exist** and **quickly building tools for websites that do not have them**, making existing products easier for agents to work with.

#### What is WebMCP?

[WebMCP](https://github.com/webmachinelearning/webmcp) is a proposed web API that lets websites expose JavaScript functions or HTML forms as tools with natural-language descriptions and structured input schemas. An agent can discover what a website does, supply the right arguments, and call its tools within the current page, sharing the user's browser context and visible interface. It complements backend MCP integrations.

#### WebMCP vs. ordinary computer use

Computer use operates a website through its interface: observe, locate controls, click or type, then observe again. WebMCP exposes named capabilities with descriptions and input schemas, so the model can call a tool and read its result. See the [WebMCP project's motivation and goals](https://github.com/webmachinelearning/webmcp#background-and-motivation).

| | Ordinary computer use | WebMCP |
| --- | --- | --- |
| Understanding | Infer functionality and state from screenshots or page structure. | Discover explicit tool names, descriptions, and parameters. |
| Execution | Locate and operate controls across multiple observation/action steps. | Supply arguments to a tool; it performs the corresponding operations and returns a result. |
| Reuse | Usually repeat the UI steps; reuse requires separately saving a script or workflow. | DeepDeck saves verified operations as tools that later tasks can reuse. |
| Time and tokens | Repeated page reads and model decisions add overhead. | For tasks covered by tools, fewer observation and interaction rounds can save time and tokens. |
| Best suited to | Exploring sites and handling interactions without existing tools. | Calling existing tools and reusing recurring website workflows. |

For example, **searching for a keyword and reading the results** with computer use typically means finding the search field, typing, submitting, reading the new page, and extracting results. With WebMCP, the Agent calls a search tool with the keyword and reads the result, using a separate results-reading tool if needed.

**DeepDeck combines both approaches.** The Agent explores and verifies a website through browser interaction, then saves working operations as WebMCP tools. Later tasks can reuse that experience, with browser interaction available for anything the tools do not cover. Initial tool building takes exploration and verification; savings depend on the website, tool design, and task, and site changes may require tool updates.

#### 1. Reuse existing WebMCP

Open a website, select **Site Agent → WebMCP**, and inspect the tools discovered under **Website**. In **Use** mode, describe your task and the Agent can call the available tools. The screenshot below shows DeepDeck discovering `search_openai` on openai.com.

![DeepDeck automatically discovers the search_openai tool under Website on openai.com](apps/web/public/webmcp/existing-webmcp.png)

#### 2. Quickly add WebMCP to an existing website

For a site without WebMCP, open **WebMCP Builder** or switch the Site Agent to **Builder**. Describe the capabilities you want, for example: “Build WebMCP tools for this site so I can search, read posts, and edit drafts.” You provide the goal; the Agent works out how to use the site. Builder explores its real controls, tries the relevant workflows, and turns verified operations into tools. This saves that experience in DeepDeck without needing to modify the website's source or deploy a separate MCP server.

![WebMCP Builder reports building and verifying tools for X](apps/web/public/webmcp/building-webmcp.png)

The X example produces **23 tools**, shown under **Built with DeepDeck**, including reading account state, posts, profiles, and search state. Website-provided tools and tools built with DeepDeck appear together, with their sources distinguished. Enabled tools are saved per website and load again when you return; source and saved versions remain available for inspection and rollback.

![The WebMCP tab lists 23 tools built with DeepDeck for X](apps/web/public/webmcp/built-webmcp.png)

Switch back to **Use** and ask for the task. In this example, “compose a hello world x post” calls WebMCP tools to prepare **Hello, world! 👋** as a draft. **The post is not published**; filling and submitting are separate actions. Use and Builder share the site's conversation, so you can build the missing capability and continue your work in place.

![The Site Agent calls WebMCP tools to compose a Hello world draft on X without publishing it](apps/web/public/webmcp/use-webmcp.png)

**Explore → use → verify → save → reuse.** The Agent's work on a website becomes a reusable capability for the next task, helping an existing product become easier to use through an agent while keeping its familiar web interface.

See the [Browser guide](plugins/browser/README.md) for details and the [website updates](https://deepdeck.getmegaportal.com/#updates) for feature announcem