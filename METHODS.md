# Methods and definitions

This file explains how the results are computed and what the terms mean. For how to run the code, see [README.md](README.md). For sources and the step-by-step log, see [PROVENANCE.md](PROVENANCE.md).

## Definitions

- **Two-party share (D2P).** Democratic votes divided by Democratic plus Republican votes in a race, as a percentage. Libertarian, independent, and write-in votes are excluded from the calculation but included in the totals shown. D2P above 50 means the Democrat led the two-party vote.
- **Contested.** A race in a given year where both a Democratic and a Republican candidate appeared. Races without both are not contested for this analysis, so they have no D2P.
- **Swing.** 2026 D2P minus 2024 D2P for the same district. Positive means a shift toward Democrats. Swing is only computed when both years are contested.
- **Latest result.** The 2026 result when the seat was contested that year, otherwise the 2024 result.
- **Republican-held.** The latest result is below 50% D2P. This is a proxy for who won the seat in the latest contested race, not confirmed incumbency.
- **2028 class.** The seats up for election in 2028. The House is elected every two years, so all 100 House seats are on the 2028 ballot. For the Senate, the 2028 class is the 18 seats contested in 2024, including District 1. See the caveat on the Senate class below.
- **Target.** A 2028-class seat that is Republican-held by the latest result and has a contested result. Targets are ranked by latest D2P, highest (closest to 50%) first.
- **Special.** A race to fill a vacancy, not a regular election. The 2026 District 1 Senate race is a special election. Its result is shown in its own row.

## Pipeline

1. **Extract** the Arkansas 2024 state legislative rows from the MEDSL state precinct file (`scripts/extract_ar_2024_legislative.py`).
2. **Summarize** 2024 results by district (`scripts/summarize_ar_2024.py`). Optional.
3. **Compare** 2024 and 2026 by district, using county summary rows for 2026 and all vote modes for 2024 (`scripts/compare_2024_2026.py`).
4. **Rank** Republican-held 2028-class seats (`scripts/rank_2028_targets.py`).
5. **Validate** the source data (`scripts/review_sos_2026.py`, `scripts/check_ar_2024_presidential.py`).

## Data choices

- **2026 results** come from the Secretary of State's county summary rows, which reconcile exactly with the total votes reported for each contest. Precinct rows are not used for totals, because precinct IDs repeat across counties.
- **2024 results** come from the MEDSL state file. Votes are summed across all modes (absentee, early, election day, and provisional). The presidential check confirms that including provisional votes matches the MEDSL precinct totals.
- **Maps** are not used. Results are joined to districts by district number, which both sources carry directly. The Census TIGER files are downloaded but are not needed for the rankings.
- **Districts** use the maps drawn after the 2020 census, which were used in 2022, 2024, and 2026. The next redistricting follows the 2030 census, so the 2028 districts should match.

## Caveats

- **Unofficial results.** The 2026 file was last updated 11/10/2026 and is marked "Unofficial." Certified numbers may differ.
- **Different election types.** 2024 was a presidential year and 2026 a midterm. Turnout differs, so the swing mixes changes in opinion with changes in who voted.
- **Incumbency and candidates are not included.** Retirements, open seats, incumbency, and 2028 candidates are not in the data. Twenty-seven of the 44 targets had no Democratic candidate on the 2026 ballot.
- **Uncontested races are excluded.** Seats with only one major-party candidate in a year have no D2P for that year. A Democrat unopposed in 2026 is excluded from the target list.
- **Ranking is not a forecast.** It sorts seats by how close they were in the latest contested race. It does not model 2028 turnout, candidates, or the national environment.

## Senate class (unresolved)

The 2028 Senate class is inferred from the 2024 contests, not yet confirmed against an official source. Arkansas Senate seats serve four-year terms, and the 2026 file shows 17 regular Senate contests plus the District 1 special. A news report says 17 seats were up in 2026, which is consistent with this inference. The official roster at senate.arkansas.gov should confirm the term-end years for each seat.
