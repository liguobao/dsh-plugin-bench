# smartmoney-cub-harness

<img src="assets/smartmoney-cub-mark.png" alt="SmartMoney-Cub" width="72" height="72" align="right" />

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-pytest-informational)](tests/)
[![Read-only](https://img.shields.io/badge/mode-read--only-brightgreen)](docs/safety.md)
[![No financial advice](https://img.shields.io/badge/no-financial%20advice-critical)](docs/safety.md)
[![Human-in-the-loop](https://img.shields.io/badge/human--in--the--loop-required-blueviolet)](docs/harness-contract.md)
[![Agent-ready](https://img.shields.io/badge/agent--ready-offline%20artifacts-success)](docs/agent-integration.md)
[![Official API gateway](https://img.shields.io/badge/official%20API%20gateway-alphatech.net.cn-C96F4A)](https://alphatech.net.cn/)

[![SmartMoney-Cub official API gateway](assets/smartmoney-cub-alphatech-banner.png)](https://alphatech.net.cn/)

![SmartMoney-Cub bilingual cover](assets/smartmoney-cub-harness-cover.png)

`smartmoney-cub-harness` is a **local-first, agent-agnostic trading journal and review harness**: read-only over markets and execution, writable over your own journal. It turns an external caller's offline run into portable, reviewable artifacts without taking trading authority.

External Agent or CLI caller → Run Envelope → frozen Benchmark/Evidence Pack → deterministic replay → explicit human promotion gate.

![Finance-JEV Benchmark Hero](assets/benchmark/benchmark-hero-1200x630.png)

### Jev Reasoning Layer & Four-Track Financial Benchmark

SmartMoney-Cub supports Jev ([TypeSafe](https://typesafe.ai/) | [OpenRouter](https://openrouter.ai/typesafe/jev)) as an optional typed-judgment layer with two pluggable backends: TypeSafe direct and OpenRouter. Jev evaluates only structured `noul`, `choice`, and `score` judgments, while all arithmetic, date comparisons, and strict temporal boundary validation (`available_at <= decision_time`) remain enforced in deterministic Python code.

The repository ships `finance-jev-v1`, a frozen offline evaluation suite containing 240 cases across four tracks (`trading-review`, `financial-filings`, `industry-events`, `macro-policy`). Following full answerability auditing and the elimination of input label leakage, cases present realistic evidence narratives (post-trade logs, disclosure excerpts, wire dispatches, central bank communiques) evaluated against strictly typed questions without answer leakage. In the published reference run ([assets/benchmark/run.json](assets/benchmark/run.json)), the deterministic rule baseline achieves **83.33%** overall accuracy (95% Wilson confidence interval [80.92%, 85.49%]) and a macro F1 of **0.7792** across all 240 cases (1,020 evaluated items). The live TypeSafe Jev backend (`typesafe_direct`, evaluated against the real API resolving to model `jev-1.13.0`) achieves **78.43%** overall accuracy (95% Wilson confidence interval [75.80%, 80.85%]) and a macro F1 of **0.7319** with a median latency of 1034 ms and superior probabilistic calibration (ECE of 0.1464 vs 0.1667). On `financial-filings`, Jev achieves **77.00%** accuracy (F1: 0.6990) outperforming the baseline (73.33%), while achieving **93.33%** accuracy (F1: 0.9215) on `industry-events` and **74.44%** (F1: 0.7148) on `macro-policy`. These figures reflect empirical performance on this frozen toy suite and do not imply generalization to production market regimes. The OpenRouter backend (`openrouter_jev`) remains reported as `not_run` due to unconfigured credentials.

`READ_ONLY_NO_ORDER_NO_CANCEL_NO_TRADE`

### 30-Second Quickstart

```bash
# 1. Install harness and dev dependencies
pip install -e ".[dev]"

# 2. Verify environment and strict read-only safety boundary
smcub doctor

# 3. Shortest review loop (capture offline toy run & replay)
smcub capture-run --mode after-close --preset toy --sandbox --decision-time "2026-06-01T15:31:00+08:00"
smcub replay-evidence-pack tmp/sandbox/20260601/*-after-close
```


It has **no embedded LLM** in its core, **no broker connection**, and
**no automatic trading**: the control plane runs entirely offline. The review assistant
is a separate, opt-in surface that calls the provider you configure and sends only
redacted structured fields. The project does not place, cancel, or execute trades;
select stocks; mutate accounts; run a background autonomous trading Agent; or
automatically mutate core rules.

[简体中文](README.zh-CN.md)

## Official API Gateway

[alphatech.net.cn](https://alphatech.net.cn/) is this project's own hosted gateway for OpenAI-compatible model access. Point a provider at its endpoint when you prefer a managed relay over configuring an upstream yourself:

```text
https://alphatech.net.cn/v1
```

The gateway is optional. The core harness runs fully offline and read-only, and it works with any provider you configure yourself; using the gateway grants no trading authority and does not change the execution ban. Provider and custom-gateway settings are documented in [docs/review-agent.md](docs/review-agent.md).

## Bilingual System Flow

![SmartMoney-Cub bilingual system flow](assets/smartmoney-cub-system-flow-bilingual.png)

Read-only inputs feed the SmartMoney-Cub control plane. Optional, user-selected open-source tools are kept outside the trusted core and enter only as review evidence. The control plane freezes manifests and evidence packs, and delayed D1/D3 outcomes flow through deterministic replay, evaluation, memory, challenger rules, and an explicit human promotion gate before any rule candidate can return to the next plan.

See [docs/architecture.md](docs/architecture.md) for the text and Mermaid representation of the same flow.

## Toy/offline control-plane workflow

Install the package, then capture one deterministic toy run with external-Agent metadata:

```bash
git clone https://github.com/myc0576/SmartMoney-Cub.git
cd SmartMoney-Cub
python -m pip install -e ".[dev]"
smcub capture-run --mode after-close --preset toy --sandbox --decision-time "2026-06-01T15:31:00+08:00" --agent-name "toy-doc-agent" --agent-version "1.0" --agent-interface "cli"
smcub validate-envelope tmp/sandbox/20260601/20260601_153100-after-close/run_envelope.json
smcub build-outcome tmp/sandbox/20260601/20260601_153100-after-close --horizon d1 --price-source smartmoney_cub_harness:data/sample_prices.json
smcub build-evidence-pack tmp/toy-evidence-pack --sample tmp/sandbox/20260601/20260601_153100-after-close --rule-candidate examples/toy_strategy/sample_rule_candidate.json --horizon d1
smcub replay-evidence-pack tmp/toy-evidence-pack
```

Run this sequence in a clean checkout; if you reuse the fixed decision time, `capture-run` adds a numeric suffix to avoid overwriting the earlier run. All inputs are toy/offline. The machine contracts are [Run Envelope](schemas/run-envelope.schema.json) and [Evidence Pack](schemas/evidence-pack.schema.json).

The workflow states are review states, never trading actions: a Run Envelope is `completed`, `pending_review`, or `blocked`; an Evidence Pack is `challenger`, `ready_for_review`, `pending_review`, or `blocked`; a replay report is `verified`, `pending_review`, or `blocked`. Only `action_label` describes a recorded observation such as `SILENT` or `ALERT`.

Run Envelope permissions are a **declarative, unverified policy record** (`enforcement: declarative`, `verified: false`), not a subprocess sandbox or proof that an external command obeyed the policy. The CLI's `--sandbox` flag only selects the disposable `tmp/sandbox` output namespace; it does not isolate the process. Run untrusted commands inside an OS/container sandbox. `evidence_pack.sha256` seals the exact pack manifest for local tamper detection; it is not an authenticated signature. Replay rejects a missing, malformed, mismatched, or structurally invalid seal/manifest as `pending_review`.

Optional ecosystem in