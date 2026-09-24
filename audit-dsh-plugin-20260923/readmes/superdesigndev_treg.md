# Treg (OpenRouter for Tools)

![treg — the tool catalog for your agent](docs/assets/treg-hero.png)

**OpenRouter, but for agent tools instead of models.** Point an agent at one base URL with one token
and it can do the job: **3,000+ catalogued endpoints across 60+ providers** — SEO and backlinks,
social and trends, people and company enrichment, ads, scraping, image and video generation —
**priced per call, from a cent**,
with no provider signup. Plus your own team's keys, skills and CLIs, callable by every teammate's
agent without the credential ever leaving the server.

**Ask for the task, not the tool.** You do not need to know which vendor sells backlink data, or to
hold an account with them. Search for what you want to do, read the price, call it.

Built for the Superdesign team, live at [treg.to](https://treg.to) — anyone can self-host.

## Why it exists

The tools an agent needs for real work sit behind subscriptions nobody buys for a single run —
Semrush $139/mo, Moz $99/mo, Crunchbase $99/mo, Apollo $59/seat — behind signup walls, or behind no
public API at all (invite-only, partner-only, app-review-only). treg carries those accounts and
bills fractions of a cent per call.

## Two kinds of tool, one token

- **The catalog** — external endpoints treg can serve with its own key or through a verified public
  route that needs no provider key. Own-key calls use the team's prepaid balance; anonymous calls
  are free. No account with the provider is needed. New verified accounts receive **$1.00 free**
  once, when they create an eligible team.
- **Your own tools** — anything a teammate registered: a paid API account, an OAuth connection, a
  vendor CLI, a `SKILL.md`. **Your own key always wins over treg's, and those calls are never
  metered.**

The vocabulary for the second half:

- **tool** = something the registry calls for you with the org's credential. Two kinds:
  - **endpoint** — an upstream `base_url` + credential **bindings** (each binding injects one
  secret into the request; a request can carry several, e.g. an OAuth bearer *and* a
  `developer-token` header).
  - **CLI** — a vendor binary (`stripe`, `gh`, `vercel`, ...) run with the credential injected.
- **skill / bundle** = a recipe (`SKILL.md`) + its secrets + its tool(s), registered together.

**The one rule:** the proxy **relays, never models** the upstream, and **injects auth server-side**
— so it survives upstream API changes and callers never hold keys.

---

# Part 1 · Using the registry

Visit [**treg.to**](https://treg.to) (hosted on Render) — the dashboard,
sign-in, and every URL below live there.

## Quickstart

Same flow as the dashboard's **Getting started** guide:

```bash
# 1. install the CLI — also points it at the registry
curl -fsSL https://treg.to/install.sh | sh

# 2. sign in (GitHub default · --email for a one-time code · --token for agents/CI)
treg login

# 3. do something useful immediately — no key, nothing registered
treg catalog search "backlinks for a domain"     # find a tool by what it DOES
treg call tikhub.tiktok.user.profile --query uniqueId=tiktok
treg balance                                     # exactly what that cost

# (or `treg onboard` for the guided walkthrough)
```

Fish Audio provides S2.1 Pro speech, public-voice discovery, and private voice cloning.
Speech is binary stdout, so redirect it to a file. A discovered voice's `_id` or a team voice id is
the TTS `reference_id`; voices created on treg's Fish account are durable team resources:

```bash
treg call fishaudio.tts.s2-1-pro --method POST --header model=s2.1-pro \
  --data '{"text":"Hello from treg","format":"mp3"}' > speech.mp3
treg call fishaudio.voices.discover --query self=false --query licensed=false --query language=en
treg resources list --provider fishaudio --kind voice
```

With your own Fish key, requests remain an unrestricted, unmetered upstream relay and Fish owns the
account boundary.

Catalog tool inputs are described by `treg catalog get <id>`. Tools marked `strict_query` reject undeclared or repeated query parameters, unsupported values and request bodies.

Your token identifies you on every call (`X-Treg-Token` header) and is the same for all tools.
Discover what your team has shared: `treg tool ls` · check credential health: `treg health`.

### Or install it as a Claude Code plugin

```
/plugin marketplace add superdesigndev/treg
/plugin install treg@treg
```

Installs with no token and no configuration. The skill loads as `treg:treg` and, on its first run,
walks your agent through the rest — the CLI, sign-in, then `treg mcp install` — so you end up with
the command line **and** treg's tools. Other agents: `npx skills add superdesigndev/treg -s treg`
(the `-s` matters — without it you also get this repo's internal dev skills).
See [docs/CLAUDE-PLUGIN.md](docs/CLAUDE-PLUGIN.md). MiniMax Code / MiniMax Agent users: the same
skill ships via the MiniMax Plugin Marketplace ([docs/MINIMAX-PLUGIN.md](docs/MINIMAX-PLUGIN.md)).

### Claude.ai connector

The Claude Connectors Directory surface is `https://treg.to/mcp/v2/`. It exposes only curated
catalog endpoints and separates read calls from write calls so Claude receives accurate safety
signals. The existing `/mcp/` surface remains available for catalog endpoints, team-owned tools,
and imported skills. See the [MCP and OAuth architecture](docs/context/architecture/mcp-oauth.md)
for the boundary and implementation, and the
[submission runbook](docs/CLAUDE-CONNECTOR-SUBMISSION.md) for release gates.

## Call a tool you don't have a key for

The catalog is grouped by what endpoints **do**: keyword and rank tracking, backlinks and authority,
AI visibility, trending and discovery, publishing to socials, people and company enrichment, ads
management and creative, measurement.

```bash
treg catalog                                    # every platform, busiest first
treg catalog search "find a work email"         # by the job, not the vendor
treg catalog get hunter.people.email.find       # params, PRICE, example response
treg call hunter.people.email.find --query domain=reddit.com --query full_name="Alexis Ohanian"
```

**How a catalogued call is served** — the credential ladder, in order:

1. your team registered its own tool for that provider → that tool, that key;
2. your team stored a secret for the provider → injected through a virtual tool;
3. neither, and the endpoint has a verified public route → **no provider key**, free;
4. otherwise → **treg's own key**, billed to the team's prepaid balance.

The anonymous price assumes the caller does not send a provider credential header. The faithful
relay preserves caller headers, so a caller-supplied provider key can use that key's credits.
Your own credential always beats treg's, so connecting a key you already pay for makes those calls
free of the balance rather than duplicating them. An endpoint treg has no published price for is
**refused**, not served free — you are told to connect your own key instead. Where several providers
serve one capability, `treg catalog search` shows them side by side with prices; **choosing is
yours** — treg does not silently pick or fail over between providers for you. (When treg's own
account for a provider is out it may serve the *same* endpoint through a treg-owned relay account,
disclosed on the response; a team can opt out.) The exception you opt into: `treg.<capability>` routed endpoints, where treg picks the provider for you and names it.

```bash
treg balance          # credit left, calls in flight, recent spend
treg topup            # add funds, or set up automatic top-ups
```

Out of balance is an HTTP **402** carrying `balance_micro`, `estimated_cost_micro` and a `topup_url`,
so an agent can act on it without reading prose.

**Enrich Arena** lives at `/enrich-arena`, outside the dashboard. Compare enrichment answers with each vendor’s cost and speed,
vote for the best answer in one click, or watch a sequential waterfall. Browsing is
public