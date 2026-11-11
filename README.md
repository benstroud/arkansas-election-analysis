# Arkansas Legislative Analysis: 2028 Democratic Targets

This project identifies Arkansas House and Senate seats that Democrats could plausibly flip in 2028. It compares the 2024 and 2026 general elections district by district and ranks the Republican-held seats on the 2028 ballot by how close the latest contest was.

**Status:** Results use the Secretary of State's 2026 election-night file, marked "Unofficial," last updated 11/10/2026. They may change once certified. This is a ranking of how close seats were, not a forecast.

## Results

Targets are Republican-held seats on the 2028 ballot, ranked by Democratic two-party share in the latest contested race. Closer to 50% is listed first. The full list is in `data/derived/ar_2028_target_ranking.csv`.

**Top House targets**

| District | Dem share | Latest race | Notes |
|---|---|---|---|
| House 81 | 49.5% | 2026 | 2024: 39.8% |
| House 14 | 48.2% | 2026 | 2024: 34.8% |
| House 34 | 48.0% | 2026 | 2024: 38.0% |
| House 50 | 43.4% | 2026 | 2024: 36.0% |
| House 16 | 41.7% | 2026 | No 2024 contest |
| House 36 | 41.1% | 2026 | 2024: 32.1% |
| House 8 (special) | 40.3% | 2026 special | Regular 2026 seat uncontested |
| House 53 | 39.0% | 2026 | 2024: 26.6% |

**Top Senate targets** (2028 class)

| Seat | Dem share | Latest race | Notes |
|---|---|---|---|
| Senate 17 | 41.8% | 2024 | No 2026 contest |
| Senate 20 | 39.1% | 2024 | No 2026 contest |
| Senate 34 | 36.1% | 2024 | No 2026 contest |
| Senate 1 | 31.6% | 2026 special | Vacancy from Gilmore's resignation |

**What the numbers show**

- In the 25 House districts contested by both parties in 2024 and 2026, Democrats gained in every one. The mean gain was 9.2 points.
- A uniform shift is consistent with a statewide change in the national environment. Targets are most useful when ranked by how close they already were, not by how much they moved.
- Of the 44 targets, 27 had no Democratic candidate on the 2026 ballot. Those seats need a candidate before they can flip.

These results omit incumbency, retirements, open seats, and 2028 candidates, none of which are known yet. See [METHODS.md](METHODS.md) for definitions and caveats.

## Reproducing the results

Requirements: Python 3. The scripts use only the standard library.

Raw inputs:
- `data/raw/sos/sos_2026_general_and_judicial_runoff.csv` is tracked.
- `data/raw/medsl2024/STATE_precinct_general.csv` is **not tracked** because it is 1.2 GB. Download it from Harvard Dataverse, file ID 13730906 (`https://dataverse.harvard.edu/api/access/datafile/13730906`), and save it at that path. Its SHA-256 is recorded in [PROVENANCE.md](PROVENANCE.md).

Run from the project root:

```sh
# 1. Extract Arkansas 2024 state legislative rows from the MEDSL file
python3 scripts/extract_ar_2024_legislative.py data/raw/medsl2024/STATE_precinct_general.csv data/derived/ar_2024_state_legislative.csv

# 2. Compare 2024 and 2026 by district
python3 scripts/compare_2024_2026.py data/raw/sos/sos_2026_general_and_judicial_runoff.csv data/derived/ar_2024_state_legislative.csv data/derived/ar_2024_vs_2026_by_district.csv

# 3. Rank 2028 targets
python3 scripts/rank_2028_targets.py data/derived/ar_2024_vs_2026_by_district.csv data/derived/ar_2028_target_ranking.csv
```

Optional checks and summaries:

```sh
python3 scripts/review_sos_2026.py data/raw/sos/sos_2026_general_and_judicial_runoff.csv
python3 scripts/summarize_ar_2024.py data/derived/ar_2024_state_legislative.csv
python3 scripts/check_ar_2024_presidential.py data/raw/medsl2024_by_state/2024-ar-precinct-general.tab
```

The derived files in `data/derived/` are already committed, so you can read the results without rerunning anything.

## Files

| File | What it is |
|---|---|
| `data/derived/ar_2028_target_ranking.csv` | The ranked target list. Start here. |
| `data/derived/ar_2024_vs_2026_by_district.csv` | Every House district and Senate seat, with 2024 and 2026 Democratic share, swing, and flags. |
| `data/derived/ar_2024_state_legislative.csv` | Arkansas 2024 House and Senate rows from MEDSL. |
| `METHODS.md` | Definitions, pipeline, and caveats. |
| `PROVENANCE.md` | Sources, checksums, and a dated log of steps. |

## Open items

- [ ] Confirm the 2028 Senate class against official term-end years at senate.arkansas.gov. The current list is inferred from the 2024 contests.
- [ ] Confirm the 2026 results are certified, then re-download the file, update its checksum, and rerun the pipeline.
- [ ] Confirm the District 1 special election result and its term.
- [ ] Add incumbency and open-seat status once they settle (most will not be known until 2027–2028).
- [ ] Add 2028 candidate data for the targets, after filing opens.
- [ ] Add a script that downloads and checksums the MEDSL file, so the 1.2 GB step is not manual.
