#!/usr/bin/env python3
"""Distribution-channel check: GitHub releases vs npm, per repo.

Answers a question star counts cannot: can this plugin actually be installed,
and does anyone install it through official channels? Two channels matter in
most plugin ecosystems: the package registry (here npm; `plugin add` usually
resolves npm names) and GitHub Releases (needed for anything shipping
binaries — desktop clients, apps).

Per repo it records:
  releases        count of releases (capped at 10 latest)
  rel_downloads   sum of asset download_count across those releases
  latest_release  latest published_at
  npm_name        "name" from the repo's package.json (None if absent)
  npm_exists      published on the npm registry?
  npm_weekly      downloads in the last week (npm downloads API)

Key lessons encoded (from the DSH audit):
  - Sum across ALL repos is misleading: a handful of pre-existing adapted
    products (tag-squatters on the download side too) hold most release
    downloads. ALWAYS recompute the summary on the native bucket when one
    exists (native_plugins.jsonl).
  - The two dead zones worth reporting: repos with a package.json name but
    never published ("cannot be installed"), and releases with zero asset
    downloads. Median npm weekly of 0 means the community installs via
    `github:owner/repo` directly — npm counts only measure the head.
  - Low-star/high-install repos exist in the tail; check the download
    leaderboard for repos missing from your curated lists.

Usage:
  python3 check_dist.py <audit-dir> [--repos FILE] [--min-stars N] [--native-file FILE]

  --repos        jsonl file with {"repo": ...} per line, or json list of names.
                 Default: repos.jsonl in audit-dir, filtered by --min-stars.
  --native-file  native bucket list (e.g. native_plugins.jsonl). If given,
                 prints the native-only summary alongside the full one.

Requires: gh CLI (core API), network access to registry.npmjs.org /
api.npmjs.org (unauthenticated). Resumable: appends to dist_check.jsonl,
skips repos already present.
"""
import argparse, base64, json, os, subprocess, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

def gh(path):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if r.returncode in (0, 404):
        return (r.returncode, r.stdout)
    return None

def npm_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "dist-check"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"_status": e.code}
    except Exception:
        return {"_status": -1}

def check(repo):
    rel = gh(f"repos/{repo}/releases?per_page=10")
    n_rel, dl, latest = 0, 0, None
    if rel and rel[0] == 0:
        try:
            for r in json.loads(rel[1]):
                n_rel += 1
                for a in r.get("assets", []):
                    dl += a.get("download_count", 0)
                t = r.get("published_at")
                if t and (latest is None or t > latest):
                    latest = t
        except Exception:
            pass
    pkg = gh(f"repos/{repo}/contents/package.json")
    npm_name, npm_exists, npm_wk = None, False, None
    if pkg and pkg[0] == 0:
        try:
            p = json.loads(base64.b64decode(json.loads(pkg[1])["content"]).decode("utf-8", "ignore"))
            npm_name = p.get("name")
        except Exception:
            pass
    if npm_name:
        from urllib.parse import quote
        q = quote(npm_name, safe="")
        reg = npm_json(f"https://registry.npmjs.org/{q}")
        if isinstance(reg, dict) and "_status" not in reg:
            npm_exists = True
            d = npm_json(f"https://api.npmjs.org/downloads/point/last-week/{q}")
            if isinstance(d, dict) and "downloads" in d:
                npm_wk = d["downloads"]
    row = {"repo": repo, "releases": n_rel, "rel_downloads": dl,
           "latest_release": latest, "npm_name": npm_name,
           "npm_exists": npm_exists, "npm_weekly": npm_wk}
    with open(OUT, "a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row

def summarize(rows, label, native=None):
    rows = [r for r in rows if native is None or r["repo"] in native]
    if not rows:
        return
    N = len(rows)
    rel = [r for r in rows if r["releases"] > 0]
    pkg = [r for r in rows if r["npm_name"]]
    pub = [r for r in pkg if r["npm_exists"]]
    dl = sorted((r["rel_downloads"] for r in rel), reverse=True)
    wk = sorted((r["npm_weekly"] or 0 for r in pub), reverse=True)
    print(f"\n== {label} (n={N})")
    print(f"releases: {len(rel)} ({len(rel)/N*100:.0f}%) | total asset dl {sum(dl):,} "
          f"| zero-dl releases {sum(1 for r in rel if r['rel_downloads']==0)}")
    print(f"package.json: {len(pkg)} | published npm: {len(pub)} "
          f"({len(pub)/len(pkg)*100:.0f}% of those with a name; "
          f"{len(pkg)-len(pub)} named-but-never-published)")
    print(f"npm weekly total {sum(wk):,} | median {wk[len(wk)//2] if wk else 0} "
          f"| <10/wk: {sum(1 for d in wk if d < 10)}")
    print("top release dl:")
    for r in sorted(rows, key=lambda r: -r["rel_downloads"])[:5]:
        print(f"  {r['rel_downloads']:>8,}  {r['repo']}")
    print("top npm weekly:")
    for r in sorted([r for r in rows if r["npm_weekly"]], key=lambda r: -r["npm_weekly"])[:5]:
        print(f"  {r['npm_weekly']:>8,}  {r['npm_name']}  ({r['repo']})")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("audit_dir")
    ap.add_argument("--repos", default=None)
    ap.add_argument("--min-stars", type=int, default=1)
    ap.add_argument("--native-file", default=None)
    args = ap.parse_args()

    OUT = os.path.join(args.audit_dir, "dist_check.jsonl")
    if args.repos and os.path.exists(args.repos):
        content = open(args.repos).read().strip()
        if content.startswith("["):
            todo = json.loads(content)
            todo = [x["repo"] if isinstance(x, dict) else x for x in todo]
        else:
            todo = [json.loads(l)["repo"] for l in open(args.repos)]
    else:
        todo = [json.loads(l)["repo"] for l in open(os.path.join(args.audit_dir, "repos.jsonl"))
                if json.loads(l)["stars"] >= args.min_stars]
    requested = set(todo)

    done = set()
    if os.path.exists(OUT):
        for l in open(OUT):
            try:
                done.add(json.loads(l)["repo"])
            except Exception:
                pass
    todo = [r for r in todo if r not in done]
    print(f"checking {len(todo)} repos ({len(done)} already done)", flush=True)

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=8) as ex:
        for i, _ in enumerate(ex.map(check, todo)):
            if (i + 1) % 100 == 0:
                print(f"{i+1}/{len(todo)} {time.time()-t0:.0f}s", flush=True)

    # A resumable cache can contain repositories from an older requested set.
    # Keep those rows cached, but exclude them from the current summary.
    rows = [json.loads(l) for l in open(OUT) if json.loads(l)["repo"] in requested]
    summarize(rows, "ALL repos")
    if args.native_file and os.path.exists(args.native_file):
        native = {json.loads(l)["repo"] for l in open(args.native_file)}
        summarize(rows, "NATIVE bucket only", native=native)
        print("\nnote: if the native file only covers a star threshold, "
              "low-star/high-install repos in the tail are not in it — "
              "scan the ALL leaderboard for repos missing from the native set.")
