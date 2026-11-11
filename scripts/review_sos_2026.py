"""Review the Arkansas SOS 2026 general election CSV and tabulate legislative races.

Aggregates from county summary rows (which reconcile to Total Votes). Precinct
Location IDs repeat across counties, so precinct rows are not used for totals.

Usage: python3 -I review_sos_2026.py <path-to-csv>
"""

import csv
import re
import sys
from collections import defaultdict

path = sys.argv[1]
with open(path, newline="", encoding="utf-8-sig") as fh:
    rows = list(csv.DictReader(fh))

LEG_RE = re.compile(r"^State (Representative|Senator|Senate|House)\b", re.I)
DIST_RE = re.compile(r"DIST(?:RICT)?\.?,?\s*0*(\d+)", re.I)
PARTY_TOKENS = {"DEM": "DEM", "REP": "REP", "R": "REP", "LIB": "LIB", "IND": "IND", "GRN": "GRN"}


def is_county(r):
    """County summary rows: 05xxx FIPS id and no ' - ' in the location name."""
    return " - " not in r["Location Name"] and re.fullmatch(r"05\d{3}", r["Location ID"]) is not None


def chamber_of(name):
    return "senate" if re.search(r"Senat", name, re.I) else "house"


def party_of(name):
    for tok in name.split():
        if tok.upper() in PARTY_TOKENS:
            return PARTY_TOKENS[tok.upper()]
    return "OTHER"


leg = [r for r in rows if LEG_RE.match(r["Contest Name"])]
county = [r for r in leg if is_county(r)]

print(f"rows: {len(rows)}; legislative rows: {len(leg)}; legislative county rows: {len(county)}")
print(f"not fully reported (county rows): {sum(1 for r in county if r['Precincts Reporting'] != r['Total Precincts'] or r['Precincts Partially Reporting'] != '0')}")
print(f"absentee+early+election-day != candidate votes: {sum(1 for r in leg if int(r['Absentee']) + int(r['Early Voting']) + int(r['Election Day']) != int(r['Candidate Votes']))}")

# County totals vs Total Votes
s = defaultdict(int)
t = {}
for r in county:
    k = (r["Contest Name"], r["Location ID"])
    s[k] += int(r["Candidate Votes"])
    t[k] = int(r["Total Votes"])
print(f"county contest pairs where sum(candidates) != Total Votes: {sum(1 for k in s if s[k] != t[k])} of {len(s)}")

# Candidate party-token audit
tok_counts = defaultdict(int)
for r in leg:
    for tok in r["Candidate Name"].split():
        if tok.upper() in PARTY_TOKENS:
            tok_counts[tok] += 1
            break
    else:
        tok_counts["(none)"] += 1
print("party tokens in candidate names:", dict(tok_counts))

# Build district results keyed by (chamber, district number, special flag)
res = defaultdict(lambda: defaultdict(int))
cands = defaultdict(set)
labels = {}
for r in county:
    name = r["Contest Name"]
    m = DIST_RE.search(name)
    if not m:
        print("could not parse district from:", name)
        continue
    key = (chamber_of(name), int(m.group(1)), "Special" in name)
    labels[key] = name
    res[key][party_of(r["Candidate Name"])] += int(r["Candidate Votes"])
    cands[key].add(r["Candidate ID"])


def table(chamber):
    keys = [k for k in res if k[0] == chamber]
    out = []
    for key in keys:
        d = res[key]["DEM"]
        rr = res[key]["REP"]
        tot = sum(res[key].values())
        two = d + rr
        d2p = d / two * 100 if two else None
        flags = []
        if d == 0:
            flags.append("NO_DEM")
        if rr == 0:
            flags.append("NO_REP")
        if len(cands[key]) == 1:
            flags.append("UNOPPOSED")
        out.append((key, d2p, d, rr, tot, len(cands[key]), flags))
    out.sort(key=lambda x: (-(x[1] if x[1] is not None else -1), x[0][1]))
    print(f"\n=== STATE {chamber.upper()} (sorted by D two-party share) ===")
    print(f"{'district':<14}{'D2P%':>7}{'D%':>7}{'R%':>7}{'Oth%':>7}{'cands':>6}  flags")
    for key, d2p, d, rr, tot, n, flags in out:
        label = f"{key[1]:>3}{' special' if key[2] else ''}"
        pct = lambda v: f"{v / tot * 100:6.1f}" if tot else "   n/a"
        d2p_s = f"{d2p:7.1f}" if d2p is not None else "    n/a"
        print(f"{label:<14}{d2p_s}{pct(d)}{pct(rr)}{pct(tot - d - rr)}{n:6d}  {','.join(flags)}")
    return out


house_out = table("house")
senate_out = table("senate")

print("\nSummary:")
for label, out in [("house", house_out), ("senate", senate_out)]:
    print(
        f"  {label}: districts {len(out)}, no D candidate {sum('NO_DEM' in x[6] for x in out)}, "
        f"no R candidate {sum('NO_REP' in x[6] for x in out)}, unopposed {sum('UNOPPOSED' in x[6] for x in out)}, "
        f"both parties and D2P 40-60%: {sum(1 for x in out if x[1] is not None and 40 <= x[1] <= 60 and not x[6])}"
    )
