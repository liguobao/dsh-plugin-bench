# Classification reference: pitfalls, judgments, and the report skeleton

Read this before correcting `digest.txt`. The machine pre-pass gets ~70% right;
the remaining 30% is where the evaluation earns its value.

## Known failure modes of the keyword pre-pass

1. **Category over-merge.** Generic words like "test", "verify", "build",
   "agent", "tool" pollute whole categories. Seen in production:
   "eng-quality" absorbed 253 of 700 repos because "test" matched everything.
   If one category holds >20% of the corpus, the keywords are too broad —
   re-read those lines and reassign by what the project *actually is*.

2. **Substring bugs in name rules.** Watch for platform keywords appearing
   inside unrelated words: in the DSH audit, the regex `see` matched
   "deep**see**k" and silently dumped desktop clients into the vision bucket.
   Word-bound your patterns; spot-check the largest output bucket before
   trusting any rule set.

3. **Tag-squatting: famous unrelated repos ride the topic for visibility.**
   Signals: repo created years before the ecosystem existed; star count wildly
   out of line with the topic's native distribution; README never mentions the
   platform except in a badge. Real cases (dsh-plugin, 2026-08):
   reactive-resume (41k), PicGo (27k), NocoBase (23.7k). Mark them
   `unrelated` and exclude from rankings. **Variant:** squatters *inside* a
   legitimate category — an "awesome-<topic>" list created years before the
   platform existed is an old repo renamed to farm the trend; always check
   `created` against the ecosystem start date for suspiciously high stars.

4. **Adapted independents vs native.** Mature standalone projects that added a
   thin integration later ("X now works inside Y") are neither squatters nor
   native plugins. They often hold most of the stars (DSH: 62 adapted repos,
   61% of stars; first native at rank #12) — counting them in plugin rankings
   torments every recommendation. Use `scripts/classify_native.py`:
   PRODUCT_FIRST overrides (build by manually reviewing the corpus head) →
   created-before-ecosystem-start → platform-first keyword linkage.
   Boundary cases exist (a generic protocol whose npm package is
   platform-branded); when in doubt, document the call.
   **Adapted ≠ worthless** — they may be usable as external infrastructure;
   they just shouldn't appear in "plugins of this platform" rankings, because
   their fate is not decided by this ecosystem.

## Verdict rubric

- **productive**: solves a real recurring workflow (memory, security, CI,
  cost control, remote access, vertical domain work). Ask: would someone
  miss it?
- **productive-but-commoditized**: correct, useful, and the Nth near-identical
  copy (desktop shells, balance widgets, theme packs past the first few).
  Count them — commoditization is itself an ecosystem finding, and the Nth
  duplicate marks where NOT to invest.
- **toy / novelty**: pets, meme packs, skins, games, roleplay personas.
  Not worthless — cultural signal and retention glue (in the DSH audit every
  toy survived the breaking change) — but report separately from
  productivity claims.
- **off-topic / empty**: squatters, template stubs, AI-generated one-shots.

## Activity: why "pushed in last N days" lies

Frenzied young ecosystems show 30-40% "recent push" simply from launch noise.
The reliable signal is a **breaking-change release anchor**: find the newest
release of the core platform that broke plugin APIs, take its `published_at`,
and count repos with `pushed >= that timestamp`. Plugins that didn't adapt are
broken or abandoned — regardless of stars.

Fairness caveats to state in the report: (a) pure-skin plugins may not touch
broken APIs and need no update; (b) if the anchor release is <48h old, treat
"not adapted" as a risk indicator, not a death verdict — split the
stalled-despite-stars list into *definitely stalled* (no push for days before
the anchor) and *borderline* (pushed hours before it).

## Scale sanity checks

- `one-shot ratio` (pushed only on creation day): above ~40% in a young
  ecosystem means the tail is homework/launch churn — reading those READMEs
  has no marginal value; say so explicitly instead of pretending coverage.
- Star pyramid: if 0-4★ repos are >80% of the corpus, the "real" ecosystem is
  the intersection of (has meaningful stars) × (passed the anchor).
- Language mix outliers (a C++ framework tagged into a JS ecosystem) are
  usually tag-squatting.

## Structural comparisons worth computing

- **Category × anchor rates**: highest follow-up = engineering discipline
  (DSH: memory 70%, market/curation 62% at the top; provider/subscription 32%
  at the bottom). This is a quality signal star counts cannot give.
- **Tier shift**: category shares in high-star active set vs 1-9★ active tail.
  DSH: infrastructure (markets, desktop clients) captures stars;
  micro-enhancements (UI tweaks) dominate the tail by count but not by
  recognition.
- **Author concentration**: count repos per owner in the active set — a single
  author with 20+ active repos ("workshop" pattern) is a finding; official-org
  follow-up discipline vs community average is another.

## Consolidated report skeleton (single document)

1. Header: method + coverage + anchor definition + data-file pointers
2. Special declaration: how adapted/squatter repos were excluded
3. TL;DR: funnel numbers, headline judgments (6 items max)
4. Method table with honest limitation column
5. Scale & growth (creation curve, star pyramid, languages, one-shot ratio)
6. Anchor activity by star tier + active×starred intersection table
7. Star ≥ N analysis universe: active/stalled split, native cross, stalled-
   despite-stars list (definite vs borderline)
8. Native/adapted/unrelated three-bucket table + exclusion groups
9. Category panorama: full-count table on the active set + native product-
   line detail; tier-shift observation
10. Niche deep-dive (if user has a stake): comparison table + disclosure
11. Productive/commoditized/toy/off-topic split
12. Top-N native picks (native + anchor-passing + irreplaceable; note
    honorables and explicit "out on activity" warnings)
13. Findings from the line-by-line read (workshop authors, official-org
    discipline, emerging sub-categories, dead-end routes)
14. Risks & recommendations (users vs authors), keyed to unfilled gaps
15. Appendix: data files, reproduction commands, license note for snapshots

Keep ONE document; fold earlier partial reports into it rather than linking
sibling versions.
