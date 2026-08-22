#!/usr/bin/env python3
"""Enumerate all repos for a GitHub topic + download top READMEs.

Defeats the search API 1000-result-per-query cap by slicing on star buckets,
then recursively bisecting any bucket that still exceeds the cap by creation
date range until every slice fits.

Usage:
  python3 fetch.py <topic> [--out DIR] [--readme-top N] [--quick]

Requires: gh CLI (authenticated). Rate limits: search ~30 req/min, so this
sleeps between search calls; a 10k-repo topic takes a few minutes.
"""
import argparse, base64, json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone

CAP = 1000  # GitHub search hard limit per query

def gh_api(path, retries=3):
    for i in range(retries):
        r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
        if r.returncode == 0:
            return json.loads(r.stdout)
        # rate limit / transient secondary rate limit -> back off
        time.sleep(10 * (i + 1))
    return None

def search(query, page):
    return gh_api(f"search/repositories?q={query}&per_page=100&page={page}")

def count(query):
    d = search(query, 1)
    return d.get("total_count", 0) if d else 0

def fetch_slice(query, label, out, seen, log):
    page, got = 1, 0
    while page <= 10:  # 10 pages x 100 = the 1000 cap
        d = search(query, page)
        if d is None:
            log(f"  WARN: failed slice {label} page {page}, skipping rest")
            break
        for it in d.get("items", []):
            fn = it["full_name"]
            if fn in seen:
                continue
            seen.add(fn)
            out.write(json.dumps({
                "repo": fn, "stars": it["stargazers_count"],
                "pushed": it["pushed_at"], "created": it["created_at"],
                "lang": it.get("language"), "archived": it["archived"],
                "desc": it.get("description"), "fork": it.get("fork"),
            }) + "\n")
            got += 1
        if len(d.get("items", [])) < 100:
            break
        page += 1
        time.sleep(1.5)
    time.sleep(1.5)
    return got

def fetch_bucket(topic, bucket, label, out, seen, log, quick):
    q = f"topic:{topic}+{bucket}"
    total = count(q)
    if total == 0:
        return
    if total <= CAP or quick:
        fetch_slice(q, label, out, seen, log)
        return
    # Over the cap: recursively bisect by creation-date range.
    log(f"  {label}: {total} > {CAP}, bisecting by created date")
    bisect_range(topic, bucket, date(2008, 1, 1),
                 datetime.now(timezone.utc).date() + timedelta(days=1),
                 label, out, seen, log, depth=0)

def bisect_range(topic, bucket, lo, hi, label, out, seen, log, depth):
    q = f"topic:{topic}+{bucket}+created:{lo.isoformat()}..{hi.isoformat()}"
    total = count(q)
    if total == 0:
        return
    if total <= CAP or depth > 9:
        fetch_slice(q, f"{label}[{lo}..{hi}]", out, seen, log)
        return
    mid = lo + (hi - lo) / 2
    bisect_range(topic, bucket, lo, mid, label, out, seen, log, depth + 1)
    bisect_range(topic, bucket, mid, hi, label, out, seen, log, depth + 1)

def download_readme(repo, outdir, max_bytes=8000):
    fn = repo.replace("/", "_")
    path = os.path.join(outdir, fn + ".md")
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return
    d = gh_api(f"repos/{repo}/readme")
    if not d or "content" not in d:
        open(path, "w").close()  # empty marker = no readme
        return
    try:
        txt = base64.b64decode(d["content"]).decode("utf-8", errors="ignore")
    except Exception:
        txt = ""
    with open(path, "w") as f:
        f.write(txt[:max_bytes])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("topic")
    ap.add_argument("--out", default=None, help="output dir (default: ./audit-<topic>)")
    ap.add_argument("--readme-top", type=int, default=700,
                    help="download READMEs for top N repos by stars (0 = skip)")
    ap.add_argument("--quick", action="store_true",
                    help="skip cap-busting bisection (only first 1000 per bucket)")
    args = ap.parse_args()

    outdir = args.out or f"audit-{args.topic}"
    os.makedirs(os.path.join(outdir, "readmes"), exist_ok=True)
    out = open(os.path.join(outdir, "repos.jsonl"), "w")

    def log(msg):
        print(msg, flush=True)

    log(f"== enumerating topic:{args.topic} (quick={args.quick})")
    seen = set()
    buckets = ["stars:>10000", "stars:1000..10000", "stars:500..999",
               "stars:200..499", "stars:100..199", "stars:50..99",
               "stars:20..49", "stars:10..19", "stars:5..9", "stars:1..4",
               "stars:0"]
    for b in buckets:
        fetch_bucket(args.topic, b, b, out, seen, log, args.quick)
        log(f"  cumulative unique: {len(seen)}")
    out.close()
    log(f"== metadata done: {len(seen)} repos -> {outdir}/repos.jsonl")

    if args.readme_top > 0:
        repos = sorted((json.loads(l) for l in open(outdir + "/repos.jsonl")),
                       key=lambda r: -r["stars"])[:args.readme_top]
        log(f"== downloading {len(repos)} READMEs (parallel x8)")
        rd = os.path.join(outdir, "readmes")
        with ThreadPoolExecutor(max_workers=8) as ex:
            list(ex.map(lambda r: download_readme(r["repo"], rd), repos))
        n = sum(1 for f in os.listdir(rd) if os.path.getsize(os.path.join(rd, f)) > 0)
        log(f"== READMEs: {n} non-empty -> {rd}")

if __name__ == "__main__":
    main()
