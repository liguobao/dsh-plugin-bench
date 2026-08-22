---
name: github-topic-audit
description: >-
  Full-lifecycle audit of a GitHub topic ecosystem (plugin/platform ecosystems
  like "dsh-plugin", "claude-plugins", "vscode-extension", or any topic/keyword).
  Use whenever the user asks to evaluate, survey, count, or judge the health of
  a GitHub plugin/ecosystem landscape — how many repos, what categories, which
  are productive vs toys, how many are actively maintained, which broke on the
  latest breaking change, or wants a written ecosystem report. Also use when the
  user questions the accuracy of an ecosystem assessment and wants it redone
  from raw GitHub data instead of directory-site summaries.
---

# GitHub Topic Ecosystem Audit

Evaluate a GitHub topic ecosystem from **primary API data**, never from
directory-site summaries (they lag, dedupe differently, and hide dead repos).
Field-tested on the DeepSeek Harness `dsh-plugin` topic (10,529 repos).

## Workflow

### 0. Scope the question

Clarify with the user (or infer): which topic(s), what "counts" as a plugin,
and any niche they personally care about — audit that niche separately and
deeply. If the user disputed a previous assessment, redo it from raw data;
that is what this skill is for.

### 1. Enumerate all repos (`scripts/fetch.py`)

```bash
python3 scripts/fetch.py <topic> --readme-top 700          # full, ~min for 10k repos
python3 scripts/fetch.py <topic> --quick --readme-top 100  # fast smoke pass
```

Requires authenticated `gh` CLI. Handles the two traps that silently truncate
results:

- GitHub search caps **every query at 1000 results** regardless of pagination.
  The script slices star buckets, then recursively bisects any >1000 bucket by
  creation-date range. (Logic covered by an offline unit test:
  `python3 scripts/test_bisection.py` — no network, no rate limit.)
- README downloads parallelize x8 and skip already-downloaded files, so reruns
  are cheap.

If gh API calls start failing in long runs, you have hit GitHub's *secondary*
rate limit (not the 30/min primary one): stop, wait a few minutes, rerun —
the script resumes where it left off (jsonl dedupes, READMEs skip existing).

Output: `audit-<topic>/repos.jsonl` (full metadata) + `readmes/` (top N by
stars, first 8KB each). Compare the enumerated count against
`gh api "search/repositories?q=topic:<topic>&per_page=1" --jq .total_count`;
report the coverage gap (usually same-day creations).

### 2. Find the activity anchor

Do NOT measure activity as "pushed in last N days" — launch-frenzied
ecosystems score 30-40% on that from noise alone. Instead:

```bash
gh api repos/<owner>/<core-repo>/releases --jq '.[] | [.tag_name, .published_at] | @tsv'
```

Pick the newest release with a **breaking change** (check release notes /
CHANGELOG; a version-number jump like 0.1.0 → 0.1.1 in 0.x semver usually means
plugin-API break). Its `published_at` is the anchor. If the user mentions a
breaking change ("rc1 broke X"), use exactly that release.

### 3. Compute stats + pre-classification (`scripts/stats.py`)

```bash
python3 stats.py audit-<topic> --anchor-release owner/repo@<breaking-tag>
# or: --anchor 2026-08-21T07:12:39Z
```

Writes `stats.txt` (star pyramid, language mix, one-shot ratio, anchor pass
rate by star tier), `analysis.json`, and `digest.txt` — one line per repo with
stars / category / verdict / anchor-pass / first README line.

### 4. Read the digest line by line (this is the actual evaluation)

Read `digest.txt` **completely** — star order — and correct the machine's
categories and verdicts as you go. Before starting, read
[references/classification.md](references/classification.md): it documents the
pre-pass failure modes (category over-merge, tag-squatting by famous unrelated
repos, adapted-vs-native), the verdict rubric, why the anchor beats recency,
and the report skeleton. If a line is ambiguous, open that repo's README in
`readmes/` — reading the actual file beats guessing from one line.

Judge each repo: productive / productive-but-commoditized / toy / off-topic.
Note head-counts per category; commoditization clusters (5th+ duplicate) are a
finding, not filler.

### 5. Deep-dive the user's niche

If the user cares about a niche (they often own a plugin in it): enumerate that
niche's repos specifically (`gh api search/repositories?q=<niche>-terms`),
fetch those READMEs fully, and build a comparison table — stars, anchor pass,
technical approach, gaps. Rank by anchor-pass + design, not stars alone.

### 6. Write the report

Follow the skeleton in `references/classification.md`. Non-negotiables:

- State the method **and its boundaries** honestly: N repos enumerated (X% of
  official count), M READMEs fully read, tail assessed by metadata only and
  why (one-shot ratio). Never imply full coverage you didn't do.
- Include the "stalled despite stars" list — repos failing the anchor despite
  high stars. Usually the most valuable finding.
- Numbers in tables, judgments in prose. Cite repo full names.

## Timing expectations

10k-repo topic: enumeration ~3-5 min (rate-limit sleeps), 700 READMEs ~2 min,
digest review is the slow human-in-the-loop step. Use `--quick` first to
sanity-check the topic, then run full.
