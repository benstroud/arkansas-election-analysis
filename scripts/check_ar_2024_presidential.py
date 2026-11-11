"""Check Arkansas 2024 presidential totals in the MEDSL national precinct file.

Compares our sums against the vote-aggregation table in the MEDSL dataset README
(precinct-dataset and county-dataset columns). Also tests whether the PROVISIONAL
mode is double-counted by comparing sums with and without it.

Input: the MEDSL per-state 2024 Arkansas file (2024-ar-precinct-general.tab, tab-delimited,
office "US PRESIDENT"), Harvard Dataverse doi:10.7910/DVN/NYTPDU, file ID 13731179.

Usage: python3 -I check_ar_2024_presidential.py <2024-ar-precinct-general.tab> [delimiter]
Streams the file; does not load it into memory.
"""

import csv
import sys
from collections import defaultdict

src = sys.argv[1]
delim = sys.argv[2] if len(sys.argv) > 2 else "\t"

# From the MEDSL README, Arkansas vote aggregation check (precinct dataset, county dataset).
README_REF = {
    "DONALD J TRUMP": (759132, 759241),
    "KAMALA D HARRIS": (396824, 396905),
    "CHASE OLIVER": (5716, 5715),
    "JILL STEIN": (4273, 4275),
    "PETER SONSKI": (2141, 2141),
    "MICHAEL WOOD": (1144, 1144),
}

by_cand_mode = defaultdict(lambda: defaultdict(int))
modes_seen = defaultdict(int)
rows_seen = 0

with open(src, newline="", encoding="utf-8") as fh:
    for r in csv.DictReader(fh, delimiter=delim):
        if r["state"] != "ARKANSAS" or r["year"] != "2024" or r["stage"] != "GEN":
            continue
        if r["office"] not in ("PRESIDENT", "US PRESIDENT"):
            continue
        rows_seen += 1
        modes_seen[r["mode"]] += 1
        by_cand_mode[r["candidate"]][r["mode"]] += int(r["votes"])

print(f"Arkansas 2024 presidential rows: {rows_seen}")
print(f"modes: {dict(modes_seen)}")
print(f"{'candidate':<18}{'all modes':>12}{'no PROV':>12}{'README prec':>13}{'README cnty':>13}{'diff vs prec':>14}")
for cand, (prec, cnty) in README_REF.items():
    modes = by_cand_mode.get(cand, {})
    total = sum(modes.values())
    no_prov = total - modes.get("PROVISIONAL", 0)
    print(f"{cand:<18}{total:>12,}{no_prov:>12,}{prec:>13,}{cnty:>13,}{total - prec:>14,}")

unknown = [c for c in by_cand_mode if c not in README_REF]
print("candidates in file but not in README table:", {c: sum(by_cand_mode[c].values()) for c in unknown})
