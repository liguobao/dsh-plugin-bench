# dsh-plugin-subscriptions [![Awesome DSH Plugin](https://awesome-dsh-plugin.com/badge.svg)](https://awesome-dsh-plugin.com)

English | [中文](README.zh.md)

Use your **ChatGPT (Codex)**, **Claude**, **Grok (X Premium)**, **GitHub Copilot**, and **Google Antigravity** subscriptions as LLM providers in [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) — no API keys. Codex, Grok, and Antigravity log in via OAuth in the dsh web UI (Settings → Subscriptions), while Copilot uses the GitHub OAuth device flow; Claude imports credentials from an existing Claude Code session when there is one (macOS Keychain or `~/.claude/.credentials.json`) and otherwise falls back to the same browser OAuth flow, so the Claude Code CLI is not required. Tokens live at `~/.dsh/plugins/subscriptions/auth.json` (mode 0600) and refresh automatically.

## Demo

Settings → **Subscriptions**: per-provider login/logout, no API keys. Claude imports credentials from Claude Code when available and otherwise uses OAuth, as Codex and Grok always do (settings screenshots use demo accounts and catalog data):

![Subscriptions settings page](https://raw.githubusercontent.com/V1ki/dsh-plugin-subscriptions/main/docs/images/subscriptions.png)

Configure visibility, default reasoning effort, and context together in **Edit model list**, with shared Save and Cancel actions:

![Model settings](https://raw.githubusercontent.com/V1ki/dsh-plugin-subscriptions/main/docs/images/model-settings.png)

Configure image generation, video generation, and X search per provider. Tool switches apply only to sessions created after saving:

![Provider tools](https://raw.githubusercontent.com/V1ki/dsh-plugin-subscriptions/main/docs/images/provider-tools.png)

Logged-in providers join the session model picker with their live model catalogs:

![Model picker with subscription models](https://raw.githubusercontent.com/V1ki/dsh-plugin-subscriptions/main/docs/images/model-picker.png)

Models that advertise reasoning levels get an **Effort** selector in the same menu — Codex models, Grok 4.6 / 4.5, and Copilot's reasoning models (levels and defaults come from each provider's live catalog, not a hardcoded list; Copilot's `capabilities.supports.reasoning_effort` array is sent as `reasoning_effort` on chat completions and `reasoning.effort` on the Responses wire). Models listing both Copilot endpoints (gpt-5.4, gpt-5-mini) normally speak chat completions but reroute to `/responses` when a request combines function tools with an effort — Copilot rejects that combination on the chat wire:

![Reasoning effort selector](https://raw.githubusercontent.com/V1ki/dsh-plugin-subscriptions/main/docs/images/model-effort.png)

Codex models whose catalog advertises the fast tier (the codex CLI's fast mode) get a **Speed** toggle in the composer's tool row, next to the model selector — Standard or Fast (`service_tier: priority`), per session. The `/fast` slash command offers the same choice as a popup; it errors with an explanation when the current model has no fast tier.

![Speed toggle with the Standard/Fast menu open](https://raw.githubusercontent.com/V1ki/dsh-plugin-subscriptions/main/docs/images/speed-toggle.png)

The composer's stats row gains a **subscription usage** pill showing the remaining rate-limit window for the provider of the session's current model (Codex when a GPT model is selected, Grok for a Grok model, and so on). Click it to expand every logged-in provider and account — the default account is starred, and the current provider is listed first:

![Subscription usage pill expanded to show every provider and account](https://raw.githubusercontent.com/V1ki/dsh-plugin-subscriptions/main/docs/images/usage-badge.png)

The `image_generate` tool renders its result inline in the conversation:

![image_generate renders the image inline](https://raw.githubusercontent.com/V1ki/dsh-plugin-subscriptions/main/docs/images/image-generate-inline.png)

Its `provider` parameter picks the image backend — the same prompt through GPT (`gpt-image-2`, top) and Grok (`grok-imagine-image-2.0`, bottom):

![image_generate with provider gpt vs grok](https://raw.githubusercontent.com/V1ki/dsh-plugin-subscriptions/main/docs/images/image-generate-providers.png)

The `video_generate` tool plays the generated clip inline:

![video_generate plays the clip inline](https://raw.githubusercontent.com/V1ki/dsh-plugin-subscriptions/main/docs/images/video-generate-inline.png)

## Providers

| Route    | Subscription      | Models |
|----------|-------------------|--------|
| `codex`  | ChatGPT Plus/Pro  | live catalog from `chatgpt.com/backend-api/codex/models` |
| `claude` | Claude Pro/Max    | all models available in your subscription (Opus, Sonnet, Haiku, Fable — static catalog, updated with the plugin) |
| `grok`   | X Premium (xAI)   | live catalog from `api.x.ai/v1/models` (chat models only); reasoning efforts from the Grok CLI catalog (`cli-chat-proxy.grok.com/v1/models`) |
| `copilot` | GitHub Copilot   | live catalog from `api.githubcopilot.com/models` (chat models on both wires, with per-model vision flags and reasoning efforts); login uses the OAuth device flow (enter the shown code at `github.com/login/device`) |
| `antigravity` | Google Antigravity | live catalog from Antigravity `v1internal:fetchAvailableModels`; requests use `generateContent` / `streamGenerateContent` with text, image, streaming reasoning, and tool-call conversion |

Only logged-in providers appear in the session model picker; the lists above refresh on login/logout. Vision-capable models declare `['text', 'image']` input modalities, and image content is translated to each provider's wire format.

Logged-in cards also show **subscription usage** — per rate-limit window (5-hour session, weekly, and per-model weekly where the plan has one) with the used percentage, a progress bar, and the reset time, plus a Refresh button. Codex usage comes from `chatgpt.com/backend-api/wham/usage` (also reports the plan), Claude usage from `api.anthropic.com/api/oauth/usage`, and Grok usage from the Grok Build CLI proxy's `cli-chat-proxy.grok.com/v1/billing` (the source of the CLI's `/usage` panel; reports the shared weekly pool and the subscription tier). Antigravity reports plan, credits, and per-model quotas from `loadCodeAssist` and `fetchAvailableModels` when those fields are present. Copilot exposes no usage endpoint, so its card shows no usage section.

Also included, registered when the matching provider is enabled:

- **`web_search`** provider (Codex) — uses Codex's hosted web search through DSH's native tool and citation UI. It follows the default Codex account and the plugin's proxy configuration. It registers as one candidate behind the host's `web` seam and does not claim it: with no other search provider mounted DSH auto-selects it, and alongside another one you pick the winner with the host's own `web.searchProvider` setting. Turning **Web search** off under Codex's **Provider tools** withdraws this provider, leaving the host's `web_search` tool to whatever else is registered.
- **`x_search`** tool (Grok) — xAI's hosted X search, returning `{ answer, citations }`.
- **`image_generate`** tool (ChatGPT or Grok) — `gpt-image-2` via the Codex backend, or `grok-imagine-image-2.0` via `api.x.ai/v1/images/generations`. The `provider` argument picks the preferred provider (`gpt`, the default, or `grok`); when the preferred one is logged out the other serves as fallback. Images are saved under `~/.dsh/plugins/subscriptions/images/` and the paths returned. The `size`/`quality` arguments map onto Grok's `aspect_ratio`/`quality` on the Grok path.
- **`video_generate`** tool (Grok) — `grok-imagine-video-1.5` via `api.x.ai/v1/videos` (async submit + poll); MP4s are saved under `~/.dsh/plugins/subscriptions/videos/`, the path returned, and the clip plays inline in the conversation. Supports duration (1–15 s), aspect ratio, resolution, and image-to-video via `image_url`.

`image_gen