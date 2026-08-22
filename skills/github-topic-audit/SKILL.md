---
name: github-topic-audit
description: >-
  Full-lifecycle audit of a GitHub topic ecosystem (plugin/platform ecosystems
  like "dsh-plugin", "claude-plugins", "vscode-extension", or any topic/keyword).
  Use whenever the user asks to evaluate, survey, count, or judge the health of
  a GitHub plugin/ecosystem landscape — how many repos, what categories, which
  are productive vs toys, how many are actively maintained, which broke on the
  latest breaking change, native plugins vs adapted products vs tag-squatters,
  or wants a written ecosystem report. Also use when the user questions the
  accuracy of an ecosystem assessment and wants it redone from raw GitHub data
  instead of directory-site summaries.
---

# GitHub Topic Ecosystem Audit

Evaluate a GitHub topic ecosystem from **primary API data**, never from
directory-site summaries (they lag, dedupe differently, and hide dead repos).
Field-tested on the DeepSeek Harness `dsh-plugin` topic (10,529 repos).

## The funnel

Work a shrinking funnel, and report the size of each stage. The funnel itself
is the headline finding ("10,529 tagged repos → 1,150 real plugins → 236
native-and-active worth tracking"):

```
full topic  →  enumerated  →  anchor-active  →  active × starred
           →  README-read set  →  native bucket  →  final watchlist
```

## Workflow

### 0. Scope the question

Clarify (or infer): which topic(s), what "counts" as a plugin, any niche the
user personally cares about (audit that niche separately and deeply — they
often own a plugin in it). If the user disputed a previous assessment, redo it
from raw data; that is what this skill is for.

### 1. Enumerate all repos (`scripts/fetch.py`)

```bash
python3 scripts/fetch.py <topic> --readme-top 700          # full, ~min for 10k repos
python3 scripts/fetch.py <topic> --quick --readme-top 100  # fast smoke pass
```

Requires authenticated `gh` CLI. Handles the traps that silently truncate
results:

- GitHub search caps **every query at 1000 results** regardless of pagination.
  The script slices star buckets, then recursively bisects any >1000 bucket by
  creation-date range. (Logic covered by an offline unit test:
  `python3 scripts/test_bisection.py` — no network, no rate limit.)
- README downloads parallelize x8 and skip existing files, so reruns are cheap.

If gh API calls start failing in long runs, you have hit GitHub's *secondary*
rate limit (not the 30/min primary one): stop, wait a few minutes, rerun —
the script resumes where it left off (jsonl dedupes, READMEs skip existing).

### 2. Find the activity anchor

Do NOT measure activity as "pushed in last N days" — launch-frenzied
ecosystems score 30-40% on that from noise alone. Instead:

```bash
gh api repos/<owner>/<core-repo>/releases --jq '.[] | [.tag_name, .published_at] | @tsv'
```

Pick the newest release with a **breaking change** (check release notes /
CHANGELOG; a 0.x minor bump usually means plugin-API break). Its
`published_at` is the anchor. If the user mentions a breaking change ("rc1
broke X"), use exactly that release.

### 3. Stats + first digest (`scripts/stats.py`)

```bash
python3 stats.py audit-<topic> --anchor-release owner/repo@<breaking-tag>
```

Writes `stats.txt` (star pyramid, language mix, one-shot ratio, anchor pass
rate by star tier, category × anchor cross-tab), `analysis.json`, and
`digest.txt` (one line per repo: stars / category / verdict / anchor-pass /
first README line).

### 4. Complete the active-set READMEs

The `--readme-top N` pass reads by stars and misses active 1-9★ repos.
After computing the anchor, download READMEs for **all repos with stars ≥ 1
AND pushed ≥ anchor** (reuse `fetch.py`'s download logic or the one-liner
pattern from the DSH audit), regenerate the digest over this set, and read
**every line**. This "active × starred" set is the ecosystem's real core —
in the DSH audit it was 1,150 of 9,393 and its structure differed sharply
from the star leaderboard.

### 5. Read the digest line by line (this is the actual evaluation)

Correct the machine's categories and verdicts as you go. Before starting,
read [references/classification.md](references/classification.md): it covers
pre-pass failure modes, the native/adapted/unrelated judgment, why the anchor
beats recency, and the consolidated report skeleton. Ambiguous line → open
that repo's README; reading the file beats guessing.

### 6. Split native / adapted / unrelated (`scripts/classify_native.py`)

```bash
python3 classify_native.py audit-<topic> --start 2026-02-01 \
    --kw dsh --kw deepseek-harness --anchor 2026-08-21T07:12:39Z \
    [--product-first product_first.txt]
```

Three rules in order: explicit PRODUCT_FIRST overrides (build this list by
manually reviewing the head of the corpus) → created before the ecosystem's
credible start date → platform-first linkage via keywords. Then **recompute
rankings and recommendations on the native bucket only** — the DSH audit
found 62 adapted repos holding 61% of all stars; the first native plugin sat
at leaderboard rank #12. `--start` estimation: earliest credible plugin
creation date (a self-described "first X plugin" repo is a good marker).

### 7. Compute funnel metrics + structural comparisons

- Funnel table: enumerated / anchor-active / active×starred / native×active.
- Star ≥ 10 universe split: active vs stalled (further split stalled into
  one-shot vs once-maintained), crossed with native bucket.
- "Stalled despite stars" list — separate *definitely stalled* (no push for
  days before anchor) from *borderline* (pushed hours before anchor).
- Category × anchor rates: the categories with the highest follow-up rates
  are where engineering discipline lives (DSH: memory 70% vs provider 32%).
- Tier structure shift: compare category shares in the high-star active set
  vs the 1-9★ active tail (DSH: infrastructure captures stars;
  micro-enhancements don't).

### 8. Deep-dive the user's niche

Enumerate the niche's repos specifically, fetch READMEs fully, and build a
comparison table — stars, anchor pass, technical approach, gaps. Rank by
anchor-pass + design, not stars alone. Disclose conflict of interest if the
user owns a plugin in the niche.

### 9. Write ONE consolidated report

Single document, skeleton in [references/classification.md](references/classification.md).
Non-negotiables:

- State the method **and its boundaries** honestly: N enumerated (X% of
  official count), M READMEs fully read, tail assessed by metadata only and
  why (one-shot ratio). Never imply coverage you didn't do.
- Lead with the funnel numbers; include the stalled-despite-stars list and
  the native-bucket recomputation; keep per-repo evidence in data files,
  referenced from the report.
- Numbers in tables, judgments in prose. Cite repo full names.

## Timing expectations

10k-repo topic: enumeration ~3-5 min (rate-limit sleeps), 700 READMEs ~2 min,
active-set completion ~2 min, digest review is the slow human-in-the-loop
step. Use `--quick` first to sanity-check the topic, then run full.
