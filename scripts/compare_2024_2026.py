"""Build the Arkansas 2024 vs 2026 state legislative comparison table by district.

Inputs:
  2026 SOS CSV (county summary rows only; they reconcile with Total Votes)
  2024 MEDSL extract (data/derived/ar_2024_state_legislative.csv; modes summed)

Two-party share (D2P) = D / (D + R). A district is "contested" in a year when both a
Democratic and a Republican candidate appear. Swing = D2P 2026 - D2P 2024 (positive = toward D),
computed only when both years are contested.

Usage: python3 -I compare_2024_2026.py <sos_2026.csv> <ar_2024_state_legislative.csv> <out.csv>
"""

import csv
import re
import sys
from collections import defaultdict

sos_path, medsl_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

DIST_RE = re.compile(r"DIST(?:RICT)?\.?,?\s*0*(\d+)", re.I)
LEG_RE = re.compile(r"^State (Representative|Senator|Senate|House)\b", re.I)
PARTY_TOKENS = {"DEM": "DEM", "REP": "REP", "R": "REP", "LIB": "LIB", "IND": "IND"}


def is_county(r):
    return " - " not in r["Location Name"] and re.fullmatch(r"05\d{3}", r["Location ID"]) is not None


def party_2026(name):
    for tok in name.split():
        if tok.upper() in PARTY_TOKENS:
            return PARTY_TOKENS[tok.upper()]
    return "OTHER"


# results[(year, chamber, district, special)] = {"DEM": n, "REP": n, "OTHER": n}
results = defaultdict(lambda: defaultdict(int))
cands = defaultdict(lambda: defaultdict(set))

with open(sos_path, newline="", encoding="utf-8-sig") as fh:
    for r in csv.DictReader(fh):
        if not LEG_RE.match(r["Contest Name"]) or not is_county(r):
            continue
        name = r["Contest Name"]
        m = DIST_RE.search(name)
        if not m:
            continue
        chamber = "senate" if re.search(r"Senat", name, re.I) else "house"
        # The SOS file does not flag this race as special. Senator Ben Gilmore (R, SD 1) resigned
        # June 30, 2026, so the 2026 SD 1 race fills the vacancy (see README). Treat it as special.
        special = "Special" in name or (chamber == "senate" and int(m.group(1)) == 1)
        key = (2026, chamber, int(m.group(1)), special)
        p = party_2026(r["Candidate Name"])
        results[key][p] += int(r["Candidate Votes"])
        cands[key][p].add(r["Candidate ID"])

with open(medsl_path, newline="", encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        chamber = "senate" if r["office"] == "STATE SENATE" else "house"
        key = (2024, chamber, int(r["district"].lstrip("0") or "0"), False)
        p = {"DEMOCRAT": "DEM", "REPUBLICAN": "REP"}.get(r["party_simplified"], "OTHER")
        results[key][p] += int(r["votes"])
        cands[key][p].add(r["candidate"])


def summarize(key):
    d = results[key].get("DEM", 0)
    rr = results[key].get("REP", 0)
    has_d = len(cands[key].get("DEM", ())) > 0
    has_r = len(cands[key].get("REP", ())) > 0
    contested = has_d and has_r
    d2p = d / (d + rr) * 100 if contested else None
    return {"contested": contested, "d2p": d2p, "d": d, "r": rr, "has_d": has_d, "has_r": has_r}


# Universe of district keys, keyed by (chamber, district, special); 2024 has no specials.
universe = sorted({(k[1], k[2], k[3]) for k in results}, key=lambda x: (x[0], x[2], x[1] and 1))

rows = []
for chamber, dist, special in universe:
    k24 = (2024, chamber, dist, False)
    k26 = (2026, chamber, dist, special)
    s24 = summarize(k24) if (not special and any(results[k24].values())) else None
    s26 = summarize(k26) if any(results[k26].values()) else None
    in24 = s24 is not None
    in26 = s26 is not None
    if chamber == "senate":
        if special:
            cls = "2028 (2026 special for unexpired term; seat regular in 2028)"
        elif in24:
            cls = "2028 (2024 cycle)"
        elif in26:
            cls = "2030 (2026 cycle)"
        else:
            cls = "unknown"
    else:
        cls = "2028 (House, every 2 years)"
    swing = None
    if s24 and s26 and s24["contested"] and s26["contested"]:
        swing = s26["d2p"] - s24["d2p"]
    held26 = None
    if s26 and s26["contested"]:
        held26 = "D" if s26["d2p"] > 50 else "R"
    rows.append({
        "chamber": chamber,
        "district": dist,
        "special_2026": "Y" if special else "",
        "class": cls,
        "d2p_2024": None if not s24 or not s24["contested"] else round(s24["d2p"], 1),
        "d_votes_2024": s24["d"] if s24 else "",
        "r_votes_2024": s24["r"] if s24 else "",
        "contested_2024": "Y" if s24 and s24["contested"] else "N",
        "d2p_2026": None if not s26 or not s26["contested"] else round(s26["d2p"], 1),
        "d_votes_2026": s26["d"] if s26 else "",
        "r_votes_2026": s26["r"] if s26 else "",
        "contested_2026": "Y" if s26 and s26["contested"] else "N",
        "swing_2026_minus_2024": None if swing is None else round(swing, 1),
        "held_2026": held26 or "",
        "dem_cand_2026": "Y" if s26 and s26["has_d"] else "N",
        "rep_cand_2026": "Y" if s26 and s26["has_r"] else "N",
    })

fields = list(rows[0].keys())
with open(out_path, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

print(f"wrote {len(rows)} rows to {out_path}")
for chamber in ("house", "senate"):
    sub = [r for r in rows if r["chamber"] == chamber]
    both = [r for r in sub if r["contested_2024"] == "Y" and r["contested_2026"] == "Y"]
    print(f"{chamber}: districts {len(sub)}; contested 2024 {sum(r['contested_2024']=='Y' for r in sub)}; "
          f"contested 2026 {sum(r['contested_2026']=='Y' for r in sub)}; contested both {len(both)}; "
          f"R-held 2026 contested {sum(r['held_2026']=='R' for r in sub)}")
