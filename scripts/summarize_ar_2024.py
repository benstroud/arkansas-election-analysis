"""Summarize Arkansas 2024 state legislative results by district (two-party D share).

Usage: python3 -I summarize_ar_2024.py <ar_2024_state_legislative.csv>
Aggregates from the mode-level rows the file carries. If a mode TOTAL row exists for a
candidate/precinct it is used alone; otherwise the individual mode rows are summed.
"""

import csv
import sys
from collections import defaultdict

path = sys.argv[1]
with open(path, newline="", encoding="utf-8") as fh:
    rows = list(csv.DictReader(fh))

modes = defaultdict(int)
parties = defaultdict(int)
for r in rows:
    modes[r["mode"]] += 1
    parties[(r["party_simplified"], r["party_detailed"])] += 1
print("modes:", dict(modes))
print("party_simplified/detailed:", dict(sorted(parties.items(), key=lambda kv: -kv[1])[:12]))

# Use TOTAL mode rows when present; they carry the full precinct total for that candidate.
has_total = any(r["mode"] == "TOTAL" for r in rows)
use = [r for r in rows if (r["mode"] == "TOTAL")] if has_total else rows
print(f"using {'TOTAL-mode rows' if has_total else 'all mode rows'}: {len(use)} of {len(rows)}")

res = defaultdict(lambda: defaultdict(int))
cands = defaultdict(set)
for r in use:
    chamber = "senate" if r["office"] == "STATE SENATE" else "house"
    dist = r["district"].lstrip("0") or "0"
    key = (chamber, dist)
    p = r["party_simplified"]
    res[key][p] += int(r["votes"])
    cands[key].add(r["candidate"])

out = []
for key, by in res.items():
    d = by.get("DEMOCRAT", 0)
    rr = by.get("REPUBLICAN", 0)
    tot = sum(by.values())
    two = d + rr
    out.append((key, (d / two * 100) if two else None, d, rr, tot, len(cands[key])))

for chamber in ("house", "senate"):
    rows_c = [x for x in out if x[0][0] == chamber]
    rows_c.sort(key=lambda x: (-(x[1] if x[1] is not None else -1), int(x[0][1]) if x[0][1].isdigit() else 0))
    print(f"\n{chamber.upper()}: {len(rows_c)} districts with 2024 races")
    for key, d2p, d, rr, tot, n in rows_c:
        s = f"{d2p:6.1f}" if d2p is not None else "   n/a"
        print(f"  {key[1]:>4}  D2P {s}  D {d:>7}  R {rr:>7}  total {tot:>7}  cands {n}")
