#!/usr/bin/env python3
"""Split README-read repos into native / adapted / unrelated buckets.

Generalized from the DSH audit: an ecosystem's star leaderboard is usually
dominated by pre-existing products that merely added the topic tag. Rankings
and recommendations must be computed on the *native* bucket only.

Rules (in order):
  1. PRODUCT_FIRST override list -> adapted (manual judgment, head of corpus)
  2. created < ecosystem start date -> adapted (cannot have been built for a
     platform that did not exist yet; also catches old repos renamed to
     squat the topic — always check created date on suspiciously high stars)
  3. platform-first linkage (name contains platform keyword, or desc/README
     leads with the platform) -> native; else -> unrelated

Usage:
  python3 classify_native.py <audit-dir> --start 2026-02-01 \
      --kw dsh --kw deepseek-harness [--anchor ISO] [--product-first file.txt]

Reads  <audit-dir>/repos.jsonl + analysis.json
Writes <audit-dir>/native_plugins.jsonl (native only, star-desc)
"""
import argparse, json, os
from collections import Counter
from datetime import datetime

def load_product_first(path):
    if not path or not os.path.exists(path):
        return set()
    return {l.strip() for l in open(path) if l.strip() and not l.startswith("#")}

def linked(repo, desc, first, kws):
    name = repo.lower()
    text = (desc + " " + first).lower()
    return any(k.lower() in name for k in kws) or any(k.lower() in text for k in kws)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audit_dir")
    ap.add_argument("--start", required=True, help="ecosystem credible start date YYYY-MM-DD")
    ap.add_argument("--kw", action="append", required=True,
                    help="platform keyword (name or text linkage); repeatable")
    ap.add_argument("--anchor", default=None, help="breaking-change ISO ts for rc-adapted flag")
    ap.add_argument("--product-first", default=None, help="file of repo full_names counted as adapted")
    ap.add_argument("--exclude", action="append", default=[],
                    help="repo to drop entirely (e.g. the core platform repo); repeatable")
    ap.add_argument("--previous", default=None,
                    help="previous classification.jsonl used as carry-forward evidence")
    ap.add_argument("--supplement-active-high", action="store_true",
                    help="metadata-classify missing star>=10 or anchor-active starred repos")
    args = ap.parse_args()

    pf = load_product_first(args.product_first)
    meta = {}
    with open(os.path.join(args.audit_dir, "repos.jsonl")) as f:
        for line in f:
            r = json.loads(line)
            meta.setdefault(r["repo"], r)
    analysis = json.load(open(os.path.join(args.audit_dir, "analysis.json")))
    analysis = [e for e in analysis if e["repo"] not in set(args.exclude)]

    rows = []
    for e in analysis:
        m = meta.get(e["repo"], {})
        created = (m.get("created") or "")[:10]
        repo = e["repo"]
        if repo in pf:
            cls = "adapted"
        elif created < args.start:
            cls = "adapted"
        else:
            cls = "native" if linked(repo, m.get("desc") or "", e.get("first") or "", args.kw) else "unrelated"
        rows.append({"repo": repo, "stars": e["stars"], "cat": e["cat"],
                     "verdict": e.get("verdict"), "created": created,
                     "desc": (m.get("desc") or "")[:200], "cls": cls,
                     "classification_source": "current-readme"})

    by_repo = {row["repo"]: row for row in rows}
    if args.previous and os.path.exists(args.previous):
        with open(args.previous) as f:
            for line in f:
                previous = json.loads(line)
                repo = previous["repo"]
                if repo in by_repo or repo not in meta or repo in set(args.exclude):
                    continue
                m = meta[repo]
                row = dict(previous)
                row.update({
                    "stars": m.get("stars", 0),
                    "created": (m.get("created") or "")[:10],
                    "desc": (m.get("desc") or "")[:200],
                    "classification_source": "previous-carry-forward",
                })
                rows.append(row)
                by_repo[repo] = row

    if args.supplement_active_high:
        if not args.anchor:
            ap.error("--supplement-active-high requires --anchor")
        for repo, m in meta.items():
            if repo in by_repo or repo in set(args.exclude):
                continue
            if m.get("stars", 0) < 10 and not (
                m.get("stars", 0) >= 1 and m.get("pushed", "") >= args.anchor
            ):
                continue
            created = (m.get("created") or "")[:10]
            if repo in pf:
                cls = "adapted"
            elif created < args.start:
                cls = "adapted"
            else:
                cls = "native" if linked(
                    repo, m.get("desc") or "", "", args.kw
                ) else "unrelated"
            row = {
                "repo": repo,
                "stars": m.get("stars", 0),
                "cat": "unclassified",
                "verdict": None,
                "created": created,
                "desc": (m.get("desc") or "")[:200],
                "cls": cls,
                "classification_source": "metadata-only",
            }
            rows.append(row)
            by_repo[repo] = row

    native = sorted((r for r in rows if r["cls"] == "native"), key=lambda x: -x["stars"])
    all_out = os.path.join(args.audit_dir, "classification.jsonl")
    with open(all_out, "w") as f:
        for r in sorted(rows, key=lambda x: -x["stars"]):
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    out = os.path.join(args.audit_dir, "native_plugins.jsonl")
    with open(out, "w") as f:
        for r in native:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    counts = Counter(r["cls"] for r in rows)
    stars = {c: sum(r["stars"] for r in rows if r["cls"] == c) for c in counts}
    total = sum(stars.values()) or 1
    for c in ("native", "adapted", "unrelated"):
        print(f"{c:10s} {counts[c]:4d} repos  {stars[c]:>7}* ({stars[c]*100//total}%)")
    # how deep into the star leaderboard before the first native repo?
    board = sorted(rows, key=lambda r: -r["stars"])
    first_native = next((i for i, r in enumerate(board) if r["cls"] == "native"), -1)
    print(f"first native on star leaderboard: rank #{first_native + 1}")
    print(f"wrote {all_out} ({len(rows)} classified)")
    print(f"wrote {out} ({len(native)} native)")
    if args.anchor:
        a = sum(1 for r in native if meta.get(r["repo"], {}).get("pushed", "") >= args.anchor)
        print(f"native anchor-follow-up: {a}/{len(native)}")

if __name__ == "__main__":
    main()
