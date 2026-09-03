#!/usr/bin/env python3
"""Offline unit test for fetch.py's cap-busting bisection (no network).

Builds a synthetic universe of 4,684 repos in one star bucket, including more
than 1,000 created on the same day, mocks the search layer, and verifies
bisect_range captures every repo despite the 1000-result query cap.
Run: python3 test_bisection.py
"""
import io, json, sys
from datetime import datetime, timedelta, timezone
import fetch

UNIVERSE = {}  # repo -> creation timestamp
d = datetime(2026, 8, 15, tzinfo=timezone.utc)
for i in range(4684):
    # 1,500 repos land on the first day; timestamp bisection must split them.
    UNIVERSE[f"test/repo-{i:05d}"] = d + timedelta(seconds=i * 37 % (7 * 86400))

def fake_search(query, page):
    # parse "topic:t+stars:0+created:A..B"
    created = [p for p in query.split("+") if p.startswith("created:")]
    lo, hi = created[0][8:].split("..")
    lo = datetime.fromisoformat(lo.replace("Z", "+00:00"))
    hi = datetime.fromisoformat(hi.replace("Z", "+00:00"))
    hits = sorted(r for r, cd in UNIVERSE.items() if lo <= cd < hi)
    start = (page - 1) * 100
    items = [{
        "full_name": r, "stargazers_count": 0,
        "pushed_at": UNIVERSE[r].isoformat().replace("+00:00", "Z"),
        "created_at": UNIVERSE[r].isoformat().replace("+00:00", "Z"),
        "language": None, "archived": False, "description": None, "fork": False,
    } for r in hits[start:start + 100]]
    return {"total_count": len(hits), "items": items}

fetch.search = fake_search
fetch.time.sleep = lambda s: None  # no waiting in tests

seen, out = set(), io.StringIO()
calls = []
orig_search = fetch.search
def counting_search(q, p):
    calls.append((q, p))
    return orig_search(q, p)
fetch.search = counting_search

fetch.bisect_range("t", "stars:0", d, d + timedelta(days=7),
                   "test", out, seen, lambda m: None, 0)

captured = {json.loads(l)["repo"] for l in out.getvalue().splitlines()}
assert captured == set(UNIVERSE), (
    f"FAIL: captured {len(captured)} of {len(UNIVERSE)}; "
    f"missing {len(set(UNIVERSE) - captured)}")
big = [q for q, p in calls if "+created:" not in q]
print(f"PASS: bisection captured all {len(UNIVERSE)} repos across "
      f"{len(set(q for q, _ in calls))} slice queries "
      f"(cap={fetch.CAP}, universe={len(UNIVERSE)})")
