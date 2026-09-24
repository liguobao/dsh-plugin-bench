<div align="center">

<p align="center">
  <img src="https://raw.githubusercontent.com/A3Boy/dsh-web-tools/main/assets/logo.png" alt="dsh-web-tools" width="160" />
</p>

# dsh-web-tools

Empower DeepSeek Harness with unified search and deep content extraction across the open web and social platforms.

**Native-Capability Adaptation Across 8 Web Providers · SearchHints Semantic Compilation · Multi-Source Resilience · Xiaohongshu & Twitter / X Retrieval**

<p align="center">
  <a href="https://github.com/A3Boy/dsh-web-tools/stargazers">
    <img src="https://img.shields.io/github/stars/A3Boy/dsh-web-tools?style=flat-square&label=Stars" alt="GitHub Stars" />
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-2ea44f?style=flat-square" alt="MIT License" />
  </a>
  <a href="https://github.com/deepseek-ai/deepseek-harness">
    <img src="https://img.shields.io/badge/DeepSeek%20Harness-Web%20Runtime-4D6BFE?style=flat-square" alt="DeepSeek Harness" />
  </a>
  <img src="https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
</p>

**English** | [简体中文](README.zh-CN.md)

</div>

## What problem does it solve?

When web access depends on a single provider, exhausted quota, rate limits, or timeouts can interrupt retrieval. Wrapping multiple APIs with a naive proxy often flattens them to a lowest common denominator, failing to leverage each provider's specialized search modes, categories, freshness, domain rules, and extraction capabilities.

dsh-web-tools connects Exa, Tavily, Firecrawl, Parallel, Brave, You.com, Jina, SearXNG, Xiaohongshu, and Twitter / X to DSH’s standard `web_search` / `web_fetch` interface.

While keeping the tool interface unified, dsh-web-tools normalizes search intents through SearchHints and compiles queries into native provider-specific parameters. This leverages each engine's native categories, freshness filters, domain policies, regional targeting, and content extraction, while maximizing uptime through multi-key allocation, automated failover, and dedicated browser profiles.

---

**Key Highlights**:

- **Native-Capability Adaptation Across 8 Web Providers**: Keeps the standard `web_search` / `web_fetch` contracts while compiling unified search intent into provider-specific native parameters instead of reducing every backend to the same lowest-common-denominator feature set.
- **SearchHints → Provider-Specific Parameter Compilation**: Normalizes technical, research, news, date, region, and domain constraints from queries, compiling them into provider-native parameters through deterministic code without additional LLM latency.
- **Xiaohongshu & Twitter / X Platform Sources**: Both platforms support signed-in native search, detail extraction, and returned comments or replies through dedicated local browser profiles.
- **Multi-Source Scheduling & Resilience**: Features multi-API-key pooling, 401 failover, 429 cooldown windows, configurable Ordered / Round-Robin / Random routing, and failover chains.
- **Native DSH Tool Integration**: Plugs directly into standard `web_search` / `web_fetch` without requiring new tool declarations, and includes a session-level "Search Mode" toggle.

```text
                         DSH Agent
                            │
                 web_search / web_fetch
                            │
                            ▼
                       SearchHints
            topic / freshness / domains
               locale / cleanQuery ...
                            │
                 Provider-specific
                    compilation
                            │
      ┌────────┬─────────┬───────────┬──────────┐
      │  Exa   │ Tavily  │ Firecrawl │ Parallel │ ...
      │        │         │           │          │
      │category│ topic   │ github    │objective │
      │ date   │ chunks  │ research  │ policy   │
      │domains │ time    │ tbs       │ queries  │
      └────────┴─────────┴───────────┴──────────┘

```

<p align="center">
  <img src="https://raw.githubusercontent.com/A3Boy/dsh-web-tools/main/assets/searchOrderAndRouting.png" width="900" alt="dsh-web-tools search strategy and multi-provider routing" />
</p>

## Native-Capability Adaptation Across 8 Web Providers

The tool interface and search semantics are unified for the DSH agent, but underlying provider capabilities are not.

dsh-web-tools expresses query intent through SearchHints and crafts dedicated requests for each provider, rather than compressing all backends into a single set of lowest-common-denominator parameters.

For example, when searching for "AI coding references from the past week":

* **Exa**: Maps category filters, ISO date ranges, and domain constraints;
* **Firecrawl**: Maps technical queries to the native `github` category, research queries to `research`, and applies `tbs` freshness filters;
* **Parallel**: Deconstructs the query into `objective`, clean `search_queries`, and `source_policy`;
* **Brave Search**: Maps freshness, country, and language parameters with priority LLM Context endpoint;
* **You.com**: Leverages `boost_domains` for soft domain preference.

All adaptations run through deterministic code without invoking an extra LLM call.

* **Exa**: Category mapping (`publication` / `news` / `financial report`), ISO-8601 date ranges, and domain constraints.
* **Firecrawl**: Maps coding and technical queries to the `github` category, academic queries to `research`, and supports `tbs`, domain constraints, and clean Markdown extraction.
* **Parallel**: Dual-layer semantics (`objective` soft-steering + clean `search_queries`) and `source_policy` domain/freshness filters.
* **Tavily**: Supports `basic` / `advanced` / `fast` / `ultra-fast` search depths; `basic`, `advanced`, and `fast` support `chunks_per_source`, with native `news` / `finance` topics, date ranges, country, and domain constraints.
* **Brave Search**: LLM Context endpoint with `pd/pw/pm/py` freshness filters, country, and search language.
* **You.com**: Native **`boost_domains`** soft-weighting, freshness presets, and geo/language targeting.
* **Jina**: Query noise reduction and ReaderLM-v2 high-precision markdown extraction.
* **SearXNG**: Self-hosted metasearch with `categories` (it/science/news) and `time_range`.
* **Native & Generic Page Extraction (`web_fetch`)**: Automatically routes to provider-native scraping backends (Exa `/contents`, Tavily `/extract`, Firecrawl `/scrape`, Parallel `/v1/extract`, You.com `/v1/contents`, Jina Reader) when available; seamlessly falls back to the **built-in generic HTTP fetcher** (powered by local Defuddle Markdown parsing with SSRF/DNS protection) for SearXNG-only / Brave-only setups or when native extractors fail.

---

## Social Platform Sources

Unlike general search engines, the plugin connects directly to native social platform sessions:

* **Native Isolated Browser Architecture**:
  * Directly controls local Edge / Chrome instances using dedicated profiles over CDP.
  * **0 browser extensions and 0 Playwright / Chromium bundles**. Cookies remain managed by the dedicated browser profile and are not written to plugin configuration, logs, or relays; the browser still sends them to the platform during normal authenticated requests.

* **Xiaohongshu**:
  * **Note Detail & Comment Fetch (`web_fetch`)**: Uses the dedicated browser profile to extract structured `__INITIAL_STATE__` data with DOM fallback while preserving signed `xsec_token` URLs. When the page loads comment data, top-level comments and returned nested replies are extracted individually.
  * **Native Search Discovery (`web_search`)**: Uses the signed-in browser and the real search controls on `/explore`, entering only the cleaned topic query rather than platform names or `site:` operators. It distinguishes login walls, security verification, and a genuinely signed-out session. Operators can temporarily disable this path with `XHS_NATIVE_SEARCH=0` while diagnos