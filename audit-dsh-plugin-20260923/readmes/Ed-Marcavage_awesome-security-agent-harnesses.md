# Awesome Security Agent Harnesses [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> AI agents for pentesting, code audit, fuzzing, vulnerability discovery, and reverse engineering — harnesses, sandboxes, security MCP servers, benchmarks, and evals.

Please read the [contribution guidelines](contributing.md) before opening a pull request.

## Contents

- [What Is a Security Agent Harness](#what-is-a-security-agent-harness)
- [Code Audit Harnesses](#code-audit-harnesses)
- [Pentesting Agents](#pentesting-agents)
- [Fuzzing and Vulnerability Discovery](#fuzzing-and-vulnerability-discovery)
- [DARPA AIxCC Cyber Reasoning Systems](#darpa-aixcc-cyber-reasoning-systems)
- [Agent Tooling and Integrations](#agent-tooling-and-integrations)
- [Agent Sandboxes](#agent-sandboxes)
- [Benchmarks and Evals](#benchmarks-and-evals)
- [Readings](#readings)

## What Is a Security Agent Harness

A security agent harness is everything wrapped around the model: the sandbox it runs in, the analysis tools it can call, the prompts and skills that encode a methodology, and the evals you use to check it. Most of the engineering lives here rather than in the model — or as Cloudflare put it after scaling one across its own fleet, the harness is the bit that lasts.

Agents are good at producing plausible findings and bad at telling which ones are real. An agent will edit the source so its own exploit works, then report the bug it just created. So the metric that matters is not recall, which nobody can measure without already knowing every bug in a codebase, but how few unconfirmed findings reach a human: Cloudflare's pipeline cut 20,799 raw candidates down to 12,057 that survived validation, then folded away another 5,442 as duplicates. A harness that can reproduce a crash, replay an input, or re-run a static analyzer is how you throw out the bad ones before a human ever sees them.

Entries tagged `SKILL.md` are skill packs rather than runnable harnesses: methodology encoded as [Agent Skills](https://agentskills.io) that a general coding agent like Claude Code executes. They live in the section matching what they do.

## Code Audit Harnesses

Harnesses that run coding agents against source code: discovery, triage, validation, and patching.

- [Anthropic Defending Code Reference Harness](https://github.com/anthropics/defending-code-reference-harness) - Reference implementation for autonomous vulnerability discovery and remediation with Claude, with skills for threat modeling, scanning, triage, and patching.
- [audit](https://github.com/evilsocket/audit) - Eight-stage discovery agent built on the Claude Code SDK, combining many narrow agents, deliberate disagreement between them, and an explicit reachability gate.
- [Capital One VulnHunter](https://github.com/capitalone/VulnHunter) - Agentic security tool applying proactive, attacker-first analysis directly to source code.
- [Clearwing](https://github.com/Lazarus-AI/clearwing) - Autonomous source-code hunter that ranks files, fans out specialist agents, and treats sanitizer crashes as ground truth, with a separate network-pentest mode.
- [Cloudflare Security Audit](https://github.com/cloudflare/security-audit-skill) - Six-phase audit skill: parallel hunting agents attack the codebase from different angles, separate agents try to disprove each finding, and fresh agents verify the schema-validated `findings.json` against source. `SKILL.md`.
- [Google Mantis](https://github.com/google/mantis) - Modular, stack-agnostic toolkit of security review skills for coding agents to find, reproduce, and patch vulnerabilities, with gVisor-sandboxed reproducers and an explicit false-positive filter rule.
- [Krait](https://github.com/ZealynxSecurity/krait) - Claude Code audit methodology for Solidity with 101 heuristics, 26 analysis modules, and 8 kill gates that try to disprove every finding, measured blind on 50 Code4rena contests at 100% precision on the v8 baseline.
- [Open Kritt](https://github.com/Kritt-ai/open-kritt) - Self-hosted orchestrator that runs agents to find and validate vulnerabilities, export canonical findings, and rank severity, with bug-bounty payouts credited to its Blockian researcher identity.
- [OpenAI Codex Security](https://github.com/openai/codex-security) - CLI and TypeScript SDK for finding, validating, and fixing security vulnerabilities with Codex.
- [OpenHack](https://github.com/openhackai/OpenHack) - Multi-agent scanner running recon, specialist hunts, independent validation, and sandbox and browser verification, using only open-source models.
- [RAPTOR](https://github.com/gadievron/raptor) - Autonomous research framework chaining static analysis, binary analysis, vulnerability validation, exploit generation, and patch writing over a codebase or binary. `SKILL.md`.
- [Trail of Bits Skills](https://github.com/trailofbits/skills) - Skills for security research, vulnerability detection, and audit workflows, distilled from the firm's audit practice. `SKILL.md`.
- [Vercel Labs Deepsec](https://github.com/vercel-labs/deepsec) - Security harness for finding vulnerabilities in a codebase using coding agents.
- [Visa Vulnerability Agentic Harness](https://github.com/visa/visa-vulnerability-agentic-harness) - Agentic SAST pipeline for autonomous vulnerability discovery, remediation, and validation, emitting Markdown and SARIF reports.

## Pentesting Agents

Agents that attack running applications and infrastructure: reconnaissance, exploitation, and proof of impact.

- [AIDA](https://github.com/Vasco0x4/AIDA) - Model-agnostic pentesting agent that reasons over a defined scope, executes in an isolated container, and keeps persistent assessment state across sessions.
- [AWE](https://github.com/stuxlabs/AWE) - Research framework pairing a lightweight orchestration layer with memory-augmented, vulnerability-specific agent pipelines, evaluated on the XBOW benchmark.
- [BlacksmithAI](https://github.com/yohannesgk/blacksmith) - Multi-agent pentesting framework that walks a target from reconnaissance through post-exploitation inside a Docker image preloaded with standard security tooling, driven from either a web UI or a CLI.
- [BreachWeave](https://github.com/m-sec-org/BreachWeave) - Multi-role pentest harness where a Manager schedules and reclaims Solvers that exploit in parallel while a bystander Observer watches for drift and holds the termination decision, built on the Pi SDK; placed first of 613 teams in both the online and offline rounds of the second Tencent Cloud AI pentest challenge.
- [BugTraceAI](https://github.com/BugTraceAI/BugTraceAI) - Multi-agent platform for authorized web application security testing with independent validation, evidence capture, and reporting.
- [CAI](https://github.com/aliasrobotics/cai) - Alias Robotics' framework for building cybersecurity agents, with tool and workflow primitives for offensive testing.
- [Cairn](https://github.com/oritera/Cairn) - Pentesting as state-space search: Claude Code, Codex, or Pi workers with no fixed roles coordinate only through a blackboard of facts, intents, and hints, and solved all 54 problems at the Tencent Cloud AI pentest challenge, the only team to clear the board.
- [CHYing-agent](https://github.com/yhy0/CHYing-agent) - Human-AI teaming pentester with an orchestrator coordinating command-execution, browser, C2, and reverse-engineering subagents over Kali, rebuilt on the Claude Code Python SDK; the ninth-place finisher in the first Tencent Cloud AI pentest challenge.
- [CyberStrike](https://github.com/CyberStrikeus/CyberStrike) - Offensive-security harness coordinating autonomous agents over signed attack skills, built-in tools, and MCP integrations, mapped to MITRE ATT&CK and OWASP WSTG.
- [hackingBuddyGPT](https://github.com/ipa-lab/hackingBuddyGPT) - TU Wien research framework for writing LLM pentesting agents in roughly 50 lines of code, released alongside reusable Linux privilege-escalation benchmarks and open-access evaluations.
- 