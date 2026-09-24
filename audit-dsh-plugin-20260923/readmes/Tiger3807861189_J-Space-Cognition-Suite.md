# J-Space Cognition Suite SV1

[Simplified Chinese](README.zh-CN.md)

[![Concept DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21971181.svg)](https://doi.org/10.5281/zenodo.21971181)

J-Space is an inference-time workspace and control suite for complex reasoning, repository
engineering, coordinated agents, and authorized security analysis. You install one skill,
load relevant modules, and keep long-task decisions connected to durable evidence.

Its thirteen modules share one premise and one routing entry. Standard-library Python
scripts persist state, reread actual source text, detect stale maps and evidence, and return
blocking results when a required condition is missing. The host supplies tools and agents.

## Quick start

You need a host that can load a local `SKILL.md` and retrieve its supporting files.
Python 3.10+ is needed for executable controllers and validation; low/medium can use the
documented prose fallback. No pip dependencies or background service are required.

1. Copy the complete [`j-space/`](j-space/) directory into your host's Skills directory.
   Obtain that directory from the host's own configuration; no universal location or
   invocation syntax applies to every host. Keep `SKILL.md`, `modules/`, `references/`,
   and `scripts/` together; avoid an extra nested `j-space/j-space/` directory.
   Copy `LICENSE` and `THIRD_PARTY_NOTICES.md` alongside the installed `SKILL.md` when
   distributing the standalone skill. Use an empty destination to avoid mixing installs.
2. Use Python 3.10 or later to verify the installed directory:

   ```text
   <python-command> <skill-root>/scripts/verify_suite.py
   ```

3. Reload the host if it discovers skills only at startup. Select `j-space` through its
   skill UI. Use `$j-space` or `/j-space` only if that host documents the syntax; otherwise
   ask it to read the installed `SKILL.md` explicitly. Confirm it can retrieve one routed
   module and execute the installed controller's `--help` if you need strict gates.
4. Give it the task and its acceptance conditions:

   ```text
   Use j-space to modify this repository. Inspect the existing contracts, maintain a
   source-backed map, delegate independent work where useful, and verify the final behavior.
   ```

Replace `<python-command>` with your available `python`, `python3`, or `py -3` command.
Resolve `<skill-root>` to the installed directory. Keep the task directory as the working
directory, or pass `--root TASK_DIRECTORY` before a controller subcommand.

For a path with spaces in Bash:

```bash
python3 "/path with spaces/j-space/scripts/control.py" --root "/task directory" status
```

For a quoted interpreter path in PowerShell:

```powershell
& "C:\Python313\python.exe" "C:\Skills\j-space\scripts\control.py" --root "D:\Task Directory" status
```

Run `status` after initializing the task. UTF-8 input supports English and Chinese task
content; use the language requested by the user for deliverables.
Run controllers in the target project's task directory, not the installed skill directory.
Installing the files does not automatically register hooks, launch agents, or grant tool access.

> **Intended use.** This suite is designed for real engineering and production-oriented
> projects with contracts, dependencies, verification, and recovery needs. It is not aimed
> at toy demonstrations such as “a pelican riding a bicycle.” Its suitability for serious
> work is a design focus, not a guarantee that any untested deployment is production-ready.

## Operating levels

| Level | Use | Control |
|---|---|---|
| `low` | A direct answer checkable at a glance | Fast pass; no persistent setup |
| `medium` | A bounded deliverable with a few dependent steps | Full pass; selective modules and delivery audit |
| `high` | Multi-file, multi-stage, or persistent work | Loop; shared state, source refresh, evidence checks |
| `xhigh` | Difficult integration or competing approaches that benefit from a team | Loop plus bounded agents, second consideration, and independent review |

`media` is an accepted alias for `medium`. Raise the level when the task's uncertainty or
dependencies require it. Use agents proactively when independent work justifies coordination.
When the host lacks agents, record the limitation and perform sequential checks.

## A short tutorial for all four levels

Select the skill first. In commands below, replace `<python-command>` and `<skill-root>`
with your installed interpreter and skill directory, quote paths containing spaces, and
work in the target task directory. The example artifact names refer to files you create
from actual work and checks; do not create empty or fabricated evidence just to pass a gate.

### low — a bounded check inside engineering work

Ask: “Use j-space at low to check whether this configuration change preserves the timeout
unit. State the conclusion and its evidence; do not expand the task.” Read the relevant
input, check the one constraint, and return the result. No state initialization is required.
Escalate if the check exposes cross-file dependencies or unresolved uncertainty.

### medium — a small deliverable with dependent steps

Ask: “Use j-space at medium to update this API example and verify its parameters against
the implementation. Keep a short record of the goal, uncertainty, and observed checks.”
Optionally use the lightweight ledger:

```text
<python-command> <skill-root>/scripts/jspace.py note --goal "API example matches implementation" --next "Inspect the endpoint"
<python-command> <skill-root>/scripts/jspace.py note --open "Does the example cover required inputs?" --settled-by "Inspect the endpoint and run the example"
<python-command> <skill-root>/scripts/jspace.py seam
```

Inspect and run the example, then record the actual outcome with
`note --check "Observed result" --by "manual inspection of each input and execution of the reported case" --close 1`.
Write `answer.md`, then run `jspace.py ship answer.md`. This audits text heuristically;
findings are advisory, while unreadable/oversized input is rejected. It does not prove the
API behavior. Do not maintain this ledger alongside the strict controller for the same task.

### high — repository work from inspection to delivery

Ask: “Use j-space at high to repair this repository issue. Preserve public contracts, keep
a source-backed map, run the relevant tests, and finish with evidence against each requirement.”
Follow the **Shared control** section to initialize, read sources, create/sync/view the map,
and pass the work gate. Perform the work; record real verification in `evidence/root.txt`
and a separate acceptance checklist in `evidence/completion.txt`. Keep `src/router.py` below
only if it is a material source dependency; substitute your actual sources and repeat `--source` as needed.

```text
<python-command> <skill-root>/scripts/control.py pulse --event checkpoint
<python-command> <skill-root>/scripts/control.py report --agent root --round 1 --summary "Observed repair and coverage" --evidence evidence/root.txt --completion evidence/completion.txt --source src/router.py --next "Deliver checked result"
<python-command> <skill-root>/scripts/control.py repo sync --map repo-map.json
<python-command> <skill-root>/scripts/control.py repo view --agent root
<python-command> <skill-root>/scripts/control.py repo check
<python-command> <skill-root>/scripts/control.py check --stage ship
```

Update the map's meaning before that final sync. Creating report/checklist files changes
the inventory too. Resolve open questions and security candidates before shipment. Exit 0
allows delivery; a nonzero result names an unmet condition. Repair that condition before
checking again; identical retries without changed evidence are not recovery.

### xhigh — actual independent work and integration

Ask: “Use j-space at xhigh for this integration. Assign an independent contract review to
a real child agent, request its second consideration, reproduce material findings, 