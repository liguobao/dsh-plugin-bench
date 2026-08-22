# Classification reference: pitfalls and verdicts

Read this before correcting `digest.txt`. The machine pre-pass gets ~70% right;
the remaining 30% is where the evaluation earns its value.

## Known failure modes of the keyword pre-pass

1. **Category over-merge.** Generic words like "test", "verify", "build", "agent",
   "tool" pollute whole categories. Seen in production: "eng-quality" absorbed 253
   of 700 repos because "test" matched everything. If one category holds >20% of
   the corpus, the keywords are too broad — re-read those lines and reassign by
   what the project *actually is*.

2. **Tag-squatting: famous unrelated repos ride the topic for visibility.**
   Signals: repo created years before the ecosystem existed; star count wildly out
   of line with the topic's native distribution; README never mentions the
   platform except in a badge. Real cases (dsh-plugin, 2026-08): reactive-resume
   (41k), PicGo (27k), NocoBase (23.7k). Mark them `off-topic` and exclude from
   native rankings, but report their existence — star leaderboards mislead
   precisely because of them.

3. **Adapted-but-unrelated vs native.** Mature standalone projects that added a
   thin integration later ("X now works inside Y") are neither squatters nor
   native plugins. Count them separately: "adapted independents".

## Verdict rubric

- **productive**: solves a real recurring workflow (memory, security, CI, cost
  control, remote access, vertical domain work). Ask: would someone miss it?
- **productive-but-commoditized**: correct, useful, and the Nth near-identical
  copy (desktop shells, balance widgets, theme packs past the first few). Note
  the count — commoditization is itself an ecosystem finding.
- **toy / novelty**: pets, meme packs, skins, games, roleplay personas. Not
  worthless — cultural signal — but report separately from productivity claims.
- **off-topic / empty**: squatters, template stubs, AI-generated one-shots.

## Activity: why "pushed in last N days" lies

Frenzied young ecosystems show 30-40% "recent push" simply from launch noise.
The reliable signal is a **breaking-change release anchor**: find the newest
release of the core platform that broke plugin APIs, take its `published_at`,
and count repos with `pushed >= that timestamp`. Plugins that didn't adapt are
broken or abandoned — regardless of stars. High-star plugins failing this test
belong in an explicit "stalled despite stars" list; that list is usually the
most interesting finding in the report (real examples from the dsh audit:
a 12.3k-star memory layer and a 393-star remote plugin both failed the rc.1
anchor).

Fairness caveats to state in the report: (a) pure-skin plugins may not touch
broken APIs and need no update; (b) if the anchor release is <48h old, treat
"not adapted" as a risk indicator, not a death verdict.

## Scale sanity checks

- `one-shot ratio` (pushed only on creation day): in the dsh audit 48.3%.
  Above ~40% in a young ecosystem means the tail is mostly homework/launch
  churn — reading those READMEs has no marginal value; say so explicitly
  instead of pretending to have read everything.
- Star pyramid: if 0-4 star repos are >80% of the corpus, the "real" ecosystem
  is the intersection of (has meaningful stars) x (passed the anchor).
- Language mix tells you the plugin system's native language; outliers
  (a C++ framework tagged into a JS ecosystem) are usually tag-squatting.

## Report skeleton that worked

1. TL;DR numbers (total, real core size, anchor pass rate)
2. Method + honest boundaries (what was read fully vs metadata-only)
3. Growth curve + star pyramid
4. Anchor-based activity by star tier + stalled-despite-stars list
5. Category map (manually corrected), with head count per category
6. Productive / commoditized / toy / off-topic split
7. Best-in-class picks (native + anchor-passing + non-replaceable)
8. Deep-dive on any niche the user cares about (they often have a stake)
9. Risks + recommendations (users vs authors)
