# API Relay Audit

<p align="center">
  Local security audit for AI API relays and LLM proxies.
</p>

<p align="center">
  <a href="https://toby-bridges.github.io/api-relay-audit/"><img alt="GitHub Pages" src="https://img.shields.io/badge/GitHub%20Pages-Live%20Site-0a7f5a?style=for-the-badge"></a>
  <a href="#chinese-readme"><img alt="README 中文" src="https://img.shields.io/badge/README-%E4%B8%AD%E6%96%87-111111?style=for-the-badge"></a>
  <a href="https://x.com/li9292"><img alt="X @li9292" src="https://img.shields.io/badge/X-%40li9292-111111?style=for-the-badge"></a>
  <a href="https://github.com/toby-bridges"><img alt="GitHub toby-bridges" src="https://img.shields.io/badge/GitHub-toby--bridges-24292f?style=for-the-badge"></a>
</p>

<p align="center">
  <a href="#deepseek-harness-dsh-plugin"><strong>DSH Plugin</strong></a>
</p>

## Your Agent Is Mine: what you can test locally

[*Your Agent Is Mine*](https://arxiv.org/abs/2604.08407) documents malicious API
relays injecting payloads and exfiltrating credentials.
[Anthropic's September 10, 2026 report](https://www.anthropic.com/threat-intelligence-report-september-2026)
describes fraudulent Claude resellers swapping models and harvesting credentials
through their client tooling. In his
[September 11 disclosure](https://x.com/shoucccc/status/2098169782541631871),
co-author Chaofan Shou reports buying router data containing users' credentials.

API Relay Audit is an independent, local security audit tool for AI API relays
and LLM proxies, informed by the paper. The current release checks observable
relay behavior and generates a Markdown report covering:

- **Prompt and context signals:** hidden prompt injection, instruction override,
  and context truncation.
- **Response integrity:** changes to pinned package-command text, error-response
  leakage, and SSE stream anomalies.
- **Reviewable findings:** per-step evidence and `LOW / MEDIUM / HIGH` summaries;
  inconclusive probes remain visible.

**See the output:** [example report (synthetic fixture)](./docs/examples/sanitized-audit-report.md)
· **Try it:** [run a local audit](#quick-start)
· [Coverage and limits](#what-it-does-not-claim)

The standalone script uses Python's standard library plus `curl`. Your API key
is sent only to the relay URL you choose.

<p align="center">
  <img alt="API Relay Audit - local AI API relay security audit with separate query families for relay audit, prompt injection audit, model substitution signals, and Web3 relay audit." src="./assets/readme-banner.png">
</p>

## Quick Start

```bash
AUDIT_SCRIPT_REF=v2.4.0
curl -fsSL "https://raw.githubusercontent.com/toby-bridges/api-relay-audit/${AUDIT_SCRIPT_REF}/audit.py" -o audit.py

python audit.py --key <YOUR_KEY> --url <BASE_URL> --output report.md

# Web3 / wallet users
python audit.py --key <YOUR_KEY> --url <BASE_URL> --profile web3 --output report.md
```

See a public-safe fixture report: [sanitized audit report](./docs/examples/sanitized-audit-report.md).
Use `master` as `AUDIT_SCRIPT_REF` only when intentionally testing unreleased changes.

> If API Relay Audit helps you evaluate a relay before sending real traffic, [star the repository](https://github.com/toby-bridges/api-relay-audit) to follow new detector coverage and release-tested updates.

## When to Use It

- You use a third-party AI API relay, mirror, gateway, or LLM proxy.
- You want to check whether a Claude-compatible or OpenAI-compatible proxy injects prompts, swaps models, truncates context, or rewrites tool output.
- You are testing relay behavior before production traffic, coding-agent automation, package-install suggestions, or wallet-related actions.
- You need a local, repeatable audit report instead of a web tool that asks for your API key.

## What It Does Not Claim

- It does not certify that a relay is safe.
- It does not replace manual security review or operational monitoring.
- It does not treat `inconclusive` as `clean`; blocked probes and ambiguous responses stay visible in the report.

## Query Family Boundaries

| Query family | User intent | Profile / steps | Evidence boundary |
|---|---|---|---|
| API relay audit | Audit a third-party relay, mirror, gateway, LLM proxy, or resale API before trusting traffic. | `general` by default; `full` for every probe | Produces a local report, not a safety certificate. |
| Prompt injection audit | Detect hidden prompt injection, prompt leakage, instruction override, and extraction behavior. | `general`; Steps 3-6 | Records prompt evidence without publishing private prompts or secrets. |
| Model substitution signals | Collect model identity, stream, latency, and upstream channel signals. | `general`; Steps 5, 10, 13, 14 | Self-ID, latency, and channel fingerprints are signals, not standalone proof of provider substitution. |
| Web3 relay audit | Check wallet-sensitive relay behavior before agent workflows touch signing or transactions. | `web3` or `full`; Step 11 | Profile-gated; general relay audits do not imply wallet safety. |

The canonical contract lives in [docs/query-families.md](./docs/query-families.md). README headings, Pages cards, issue templates, and skill descriptions should preserve these boundaries instead of flattening them into one slogan.

## Coverage

API Relay Audit checks whether a relay modifies the request or response path between you and the model:

- Prompt safety: token injection, prompt extraction, instruction override, jailbreak resistance
- Relay integrity: context truncation, tool-call substitution, error leakage, stream integrity
- Model identity: non-Claude identity leaks, model substitution signals, Claude/OpenAI-compatible relay behavior
- Web3 wallet safety: transfer guidance, signed-transaction refusal, private-key refusal

## Audit LLM Proxies Locally

The project has two distribution modes:

- `audit.py`: zero-dependency standalone script for quick local audits
- `api_relay_audit/` plus `scripts/`: modular development version with tests

Runtime profiles:

- `general`: default AI API relay and LLM proxy checks
- `web3`: wallet-safety probes for Web3 agent flows
- `full`: general plus Web3 checks

## DeepSeek Harness DSH Plugin

The repository is also an installable `dsh-api-relay-audit` bundle for
[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) Web and
community TUI surfaces that use the official `@deepseek-ai/dsh-commands`
registry. Pin an immutable commit or release tag:

```bash
DSH_PLUGIN_REF=v2.4.0
dsh plugin --profile web add "github:toby-bridges/api-relay-audit#${DSH_PLUGIN_REF}"

# dsh-cc-tui and other compatible profile-based clients
dsh plugin --profile cc-tui add "github:toby-bridges/api-relay-audit#${DSH_PLUGIN_REF}"
```

The command reuses the current DSH provider's `baseURL`, model, and credential
reference. The credential stays in DSH Credentials and is delivered to the
local audit process through an environment variable, never through command
arguments or the session log:

```text
/relay-audit
/relay-audit --connectivity
/relay-audit --profile web3 --fast-context
/relay-audit --url <URL> --model <claude-model> --credential-ref <DSH_CREDENTIAL_REF>
```

No arguments preserves the existing full-audit default and may consume
metered tokens. Use `--connectivity` for a lower-cost check. This distribution
does not add a new model baseline: the selected route must identify as Claude,
although the relay API itself may be Anthropic-compatible or OpenAI-compatible.
Independent wrappers without DSH profiles and the DSH command registry are not
compatible with this bundle. See [agent distribution notes](./docs/skill-distribution.md).
The exact v2.4.0 installation, runtime, and secret-scan results are recorded in
[the DSH distribution verification](./docs/distribution-verification-v2.4.0.md).

## Retained Agent Skill Files

The repository retains its existing OpenClaw and Hermes skill files for direct
users and downstream compatibility. They are not current registry distribution
targets; ac