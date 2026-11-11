# 2024 Precinct-level Election Returns

This is the MIT Election Data + Science Lab repository for precinct-level election returns from the 2024 General Election in the United States. If you notice any issues in our results, please contact us through Harvard Dataverse or, even better, [create an issue in our Github repository](https://github.com/MEDSL/2024-elections-official). **We ask that you triple check that potential issues exist in the repository's data and are not an artifact of the user's wrangling.**

## Contributors

These data are the culmination of a multi-year effort by a team of MEDSL research staff as well as MIT graduate and undergraduate students. We thank the following people for their contributions to the 2024 release: Charles Stewart III, Samuel Baltz, Zayne Sember, Honor Durham, Sina Shaikh, Ning Soong, Zachary Djanogly Garai, Mason Reece, Garima Rastogi, Caitlin Donovan, Elaine Zhao, Kevin Acevedo. We also thank Arianna Conte, Claire DeSoi, Jason Rhode, and Rachel Wright for their support as MEDSL staff.

## Usage
### Methods and accuracy
For any questions about how we clean and quality assure these data, and how accurate they are, please consult this paper, which answers those questions for our 2016, 2018, and 2020 precinct data efforts: https://www.nature.com/articles/s41597-022-01745-0.

For more of our election return data, visit [our website](https://electionlab.mit.edu/data) or the [Harvard Dataverse](https://dataverse.harvard.edu/dataverse/medsl_election_returns).

**We strongly encourage a careful reading of the below and our codebook before you begin working with the data.**

### Warnings
* In general, users need to exercise real caution when computing descriptive statistics. Please make sure you understand exactly which rows belong in the computation you're performing. Here are two of the most common issues:
   * Sometimes the way that states report data generates fictitious zero-vote rows, where a candidate is recorded as getting no votes in a precinct where they did not actually appear on the ballot. It is not generally possible to ensure that all real zero-vote totals are recorded while no fictitious zero-vote totals are recorded. This could affect, for example, measures of central tendency.
   * We typically retain exactly the modes that states report. This can lead to double-counting if users do not select the correct modes, for example if modes are split apart *and* a mode value of `TOTAL` is included. Users should make sure that any analysis includes votes of each mode once.
* While we attempt to verify every value of every variable, `magnitude` values in particular may be approximate for local-level offices. Please double-check these values before relying on them. We are also still working to make sure that the `NONPARTISAN` value of the party fields is propagated correctly to local offices.
* `mode` values typically retain the state's original classification. These original data sources may not identify modes in a way that is consistent across jurisdictions, and one jurisdiction may report more granularly or more accurately than another. For example, `UOCAVA` ballots may be classed as `ABSENTEE` without any means to disaggregate them.
* In some small jurisdictions in California, Kansas, Nevada, and New Mexico, vote counts are not published due to privacy concerns. In these cases `votes = "*"`.

## State-specific information

Provided below for each state are the source(s) of the raw data, state-specific notes and warnings, and the results of a vote aggregation check for presidential and senate candidates comparing statewide votes derived from these precinct-level data to two reference datasets from MEDSL: [county-level presidential returns](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ) and [county-level senate returns](https://github.com/MEDSL/2024-elections-official/blob/main/2024-senate-county.csv). 

**Note: These aggregation checks are representative of the data as it stands upon the initial release and may not be reflective as we improve the data over time.**


### Alabama
*[Source](https://www.sos.alabama.gov/alabama-votes/voter/election-data)*  

Alabama gives voters an option to check one box to cast a straight ticket ballot (e.g. vote for all Republican candidates). We denote this as `office = "STRAIGHT PARTY"`.

#### Vote Aggregation Check

| Candidate       | Precinct dataset | County dataset | Difference |
| --------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP  | 1,462,616        | 1,462,616      | 0          |
| KAMALA D HARRIS | 772,412          | 772,412        | 0          |
| CHASE OLIVER    | 4,930            | 4,930          | 0          |
| JILL STEIN      | 4,319            | 4,319          | 0          |

---
### Alaska
*[Source](https://www.elections.alaska.gov/election-results/e/?id=24genr)*

#### Vote Aggregation Check

| Candidate        | Precinct dataset | County dataset | Difference |
| ---------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP   | 184,458          | 184,458        | 0          |
| KAMALA D HARRIS  | 140,026          | 140,026        | 0          |
| CHASE OLIVER     | 3,040            | 3,040          | 0          |
| JILL STEIN       | 2,342            | 2,342          | 0          |
| CORNEL WEST      | 1,127            | 1,127          | 0          |
| PETER SONSKI     | 702              | 702            | 0          |
| ROBERT F KENNEDY | 5,670            | 5,670          | 0          |

---
### Arizona
*[Source](https://github.com/openelections/openelections-data-az/tree/master/2024/General)*  

`STATE HOUSE` races in Pima County are missing values for `district` due to limitations of the source data.

#### Vote Aggregation Check

| Candidate              | Precinct dataset | County dataset | Difference    |
| ---------------------- | ---------------- | -------------- | ------------- |
| DONALD J TRUMP         | 1,769,393        | 1,770,242      | −849 (0.048%) |
| KAMALA D HARRIS        | 1,582,676        | 1,582,860      | −184 (0.012%) |
| RUBEN GALLEGO (Senate) | 1,676,123        | 1,676,335      | −212 (0.013%) |
| KARI LAKE (Senate)     | 1,594,959        | 1,595,761      | −802 (0.050%) |
| CHASE OLIVER           | 17,896           | 17,898         | −2            |
| JILL STEIN             | 18,280           | 18,319         | −39           |

All gaps <0.05% of total, likely due to late ballots / provisional canvassing.

---
### Arkansas
*[Source](https://results.enr.clarityelections.com/AR/122502/web.345435/#/reporting)*

#### Vote Aggregation Check

| Candidate       | Precinct dataset | County dataset | Difference    |
| --------------- | ---------------- | -------------- | ------------- |
| DONALD J TRUMP  | 759,132          | 759,241        | −109 (0.014%) |
| KAMALA D HARRIS | 396,824          | 396,905        | −81 (0.020%)  |
| CHASE OLIVER    | 5,716            | 5,715          | +1            |
| JILL STEIN      | 4,273            | 4,275          | −2            |
| PETER SONSKI    | 2,141            | 2,141          | 0             |
| MICHAEL WOOD    | 1,144            | 1,144          | 0             |

---
### California
*[Source](https://statewidedatabase.org/election.html)*  


With regards to `precinct` codes:

`precinct` ending in `"A"`
- These are thought to denote absentee ballots.

From the Statewide Database's FAQ we have: 

> There are two rows for each precinct in the SVPREC files: one with a number and one with the same number plus "A" (e.g., 202 and 202A). To determine total vote for a candidate, for example, should I add the numbers in the rows corresponding to 202 and 202A?

> Yes. The A denotes the absentee ballots that were cast in that precinct.

`precinct` ending in `"AA"`
- These are thought to denote all-absentee jurisdictions because the "AA" (All-Absentee) designation is a legal status defined under California Elections Code §3005.

`precinct` ending in `"B"` or `"C"`
- We believe these denote later supplemental batches of votes that are provisionals or VBM dropped off on Election Day.

Upon reaching out to [Statewide Database](https://statewidedatabase.org/), we were told that these suffixes on precinct names are determined jurisdiction by jurisdiction and are not necessarily standardized across states. Our vote aggregation checks are consistent with the above but users should be cautious when using these data and assuming anything about the mode of voting.

#### Vote Aggregation Check

| Candidate              | Precinct dataset | County dataset | Difference     |
| ---------------------- | ---------------- | -------------- | -------------- |
| DONALD J TRUMP         | 6,071,718        | 6,081,697      | −9,979 (0.16%) |
| KAMALA D HARRIS        | 9,269,414        | 9,276,179      | −6,765 (0.07%) |
| JILL STEIN             | 167,675          | 167,814        | −139           |
| CHASE OLIVER           | 66,592           | 66,662         | −70            |
| ADAM B SCHIFF (Senate) | 9,029,588        | 9,036,252      | −6,664 (0.07%) |
| STEVE GARVEY (Senate)  | 6,302,653        | 6,312,594      | −9,941 (0.16%) |

Gaps are attributable to 187,233 suppressed (`*`) precinct rows whose actual vote totals appear in county aggregates.


---
### Colorado
*[Source](https://www.sos.state.co.us/pubs/elections/resultsData.html)*

#### Vote Aggregation Check

| Candidate       | Precinct dataset | County dataset | Difference |
| --------------- | ---------------- | -------------- | ---------- |
| KAMALA D HARRIS | 1,728,159        | 1,728,159      | 0          |
| DONALD J TRUMP  | 1,377,441        | 1,377,441      | 0          |
| CHASE OLIVER    | 21,439           | 21,439         | 0          |

---
### Connecticut
*[Source](https://ctemspublic.tgstg.net/#/home)*

#### Vote Aggregation Check

CT reports disaggregated modes (MACHINE COUNT, ABSENTEE, EARLY VOTES, SDR, UNKNOWN) plus a TOTAL summary row. Vote check performed against TOTAL mode only.

| Candidate                     | Precinct dataset | County dataset | Difference |
| ----------------------------- | ---------------- | -------------- | ---------- |
| KAMALA D HARRIS               | 992,053          | 992,053        | 0          |
| DONALD J TRUMP                | 736,918          | 736,918        | 0          |
| CHRISTOPHER S MURPHY (Senate) | 1,000,695        | 1,000,695      | 0          |
| MATTHEW M COREY (Senate)      | 678,256          | 678,256        | 0          |

---
### Delaware
*[Source](https://elections.delaware.gov/results/html/index.shtml?electionId=GE2024)*

#### Vote Aggregation Check

Vote check performed against TOTAL mode only (DE reports TOTAL + IN-PERSON + ABSENTEE + EARLY).

| Candidate                     | Precinct dataset | County dataset | Difference |
| ----------------------------- | ---------------- | -------------- | ---------- |
| KAMALA D HARRIS               | 289,758          | 289,758        | 0          |
| DONALD J TRUMP                | 214,351          | 214,351        | 0          |
| LISA BLUNT ROCHESTER (Senate) | 283,298          | 283,298        | 0          |
| ERIC HANSEN (Senate)          | 197,753          | 197,753        | 0          |

---
### District of Columbia
*[Source](https://electionresults.dcboe.org/election_results/2024-General-Election)*

#### Vote Aggregation Check

| Candidate         | Precinct dataset | County dataset | Difference |
| ----------------- | ---------------- | -------------- | ---------- |
| KAMALA D HARRIS   | 294,185          | 294,185        | 0          |
| DONALD J TRUMP    | 21,076           | 21,076         | 0          |
| WRITE-IN + others | 10,608           | 10,618 (OTHER) | -10        |

---
### Florida
*[Source](https://dos.fl.gov/elections/data-statistics/elections-data/precinct-level-election-results/)*

#### Vote Aggregation Check

| Candidate                       | Precinct dataset | County dataset | Difference |
| ------------------------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP                  | 6,110,126        | 6,110,125      | +1         |
| KAMALA D HARRIS                 | 4,683,038        | 4,683,038      | 0          |
| RICK SCOTT (Senate)             | 5,977,707        | 5,977,706      | +1         |
| DEBBIE MUCARSEL-POWELL (Senate) | 4,603,077        | 4,603,077      | 0          |

---
### Georgia
*[Source (precinct data)](https://results.sos.ga.gov/results/public/Georgia/elections/2024NovGen)* 
*[Source (office crosswalk)](https://results.sos.ga.gov/results/public/Georgia/elections/2024NovGen/reports)*

#### Vote Aggregation Check

| Candidate       | Precinct dataset | County dataset | Difference    |
| --------------- | ---------------- | -------------- | ------------- |
| DONALD J TRUMP  | 2,663,110        | 2,663,117      | −7 (<0.001%)  |
| KAMALA D HARRIS | 2,548,006        | 2,548,017      | −11 (<0.001%) |
| CHASE OLIVER    | 20,684           | 20,684         | 0             |

---
### Hawaii
*[Source (precinct data)](https://elections.hawaii.gov/election-results/)*  
*[Source (precinct-to-county crosswalk)](https://elections.hawaii.gov/resources/districts-and-precincts/)*

#### Vote Aggregation Check

HI has no TOTAL mode row; MAIL IN + ELECTION DAY summed = certified total.

| Candidate               | Precinct dataset | County dataset | Difference |
| ----------------------- | ---------------- | -------------- | ---------- |
| KAMALA D HARRIS         | 313,044          | 313,044        | 0          |
| DONALD J TRUMP          | 193,661          | 193,661        | 0          |
| MAZIE K HIRONO (Senate) | 324,194          | 324,194        | 0          |
| BOB MCDERMOTT (Senate)  | 160,075          | 160,075        | 0          |

---
### Idaho
*[Source](https://voteidaho.gov/election-results/)*

#### Vote Aggregation Check

| Candidate       | Precinct dataset | County dataset | Difference |
| --------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP  | 605,246          | 605,246        | 0          |
| KAMALA D HARRIS | 274,972          | 274,972        | 0          |

---
### Illinois
*[Source](https://www.elections.il.gov/electionoperations/ElectionVoteTotalsPrecinct.aspx?ID=rfZ%2buidMSDY%3d)*

#### Vote Aggregation Check

| Candidate       | Precinct dataset | County dataset | Difference |
| --------------- | ---------------- | -------------- | ---------- |
| KAMALA D HARRIS | 3,062,863        | 3,062,863      | 0          |
| DONALD J TRUMP  | 2,449,079        | 2,449,079      | 0          |

---
### Indiana
*[Source (official state data)](https://enr.indianavoters.in.gov/site/index.html)*  
*[Source (supplemental OpenElections data)](https://github.com/openelections/openelections-data-in/tree/master/2024/counties)*  

**Warning:** Major caveats apply to Indiana’s data completeness and accuracy. Senate and Governor totals are overreported because some county sources appear to fold straight-party votes into candidate totals, and some counties reuse the same precinct label for distinct ballot batches so precinct names are not always unique identifiers.

#### Vote Aggregation Check

| Candidate               | Precinct dataset | County dataset | Difference       |
| ----------------------- | ---------------- | -------------- | ---------------- |
| DONALD J TRUMP          | 1,807,658        | 1,808,892      | −1,234 (−0.07%)  |
| KAMALA D HARRIS         | 1,223,828        | 1,220,554      | +3,274 (+0.27%)  |
| JIM BANKS (Senate)      | 1,746,481        | 1,659,416      | +87,065 (+5.25%) |
| VALERIE MCCRAY (Senate) | 1,152,859        | 1,097,061      | +55,798 (+5.09%) |

*Deduplication method: use TOTAL mode per county where available; otherwise sum all modes.*

---
### Iowa
*[Source](https://sos.iowa.gov/elections/results/precinctvotetotals2024general.html)*

#### Vote Aggregation Check

IA has `ELECTION DAY` and `ABSENTEE` modes; no TOTAL row. Summing both modes gives the certified total.

| Candidate       | Precinct dataset | County dataset | Difference |
| --------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP  | 927,019          | 927,019        | 0          |
| KAMALA D HARRIS | 707,278          | 707,278        | 0          |

---
### Kansas
*[Source](https://sos.ks.gov/elections/election-results.html)*

#### Vote Aggregation Check

| Candidate       | Precinct dataset | County dataset | Difference   |
| --------------- | ---------------- | -------------- | ------------ |
| DONALD J TRUMP  | 758,775          | 758,802        | −27 (0.004%) |
| KAMALA D HARRIS | 544,836          | 544,853        | −17 (0.003%) |

---
### Kentucky
*[Source](https://elect.ky.gov/results/2020-2029/Pages/2024.aspx)*

#### Vote Aggregation Check

| Candidate       | Precinct dataset | County dataset | Difference |
| --------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP  | 1,337,491        | 1,337,494      | −3         |
| KAMALA D HARRIS | 704,043          | 704,043        | 0          |

---
### Louisiana
*[Source](https://voterportal.sos.la.gov/static/2024-11-05)*  

Louisiana reports early voting only at the parish level, as such early votes are NOT included in the precinct data.

#### Vote Aggregation Check

| Candidate       | Precinct dataset | County dataset | Difference |
| --------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP  | 617,868          | 1,208,505      | −590,637   |
| KAMALA D HARRIS | 400,437          | 766,870        | −366,433   |

**Known data limitation:** LA's precinct file contains only Election Day (in-person) votes. Early voting (~590K Trump, ~366K Harris) is excluded from the source data. This is a known incompleteness in the LA precinct dataset — it is not an error in our processing. The reference data TOTAL includes all voting modes (EARLY VOTING + PROVISIONAL + ELECTION DAY).

---
### Maine
*[Source](https://www.maine.gov/sos/cec/elec/results/results24.html)*  


For some observations, `jurisdiction_fips` was unable to be determined. 

Maine precinct totals are first-round counts and will not match final certified presidential/Senate totals because of ranked-choice redistribution.

State House district 021 is missing candidate Marianna Reeves because she is absent from the raw data.

#### Vote Aggregation Check

| Candidate                | Precinct dataset | County dataset | Difference    |
| ------------------------ | ---------------- | -------------- | ------------- |
| DONALD J TRUMP           | 376,991          | 376,991        | 0             |
| KAMALA D HARRIS          | 410,492          | 430,342        | −19,850 (RCV) |
| ANGUS S KING JR (Senate) | 424,490          | 427,570        | −3,080 (RCV)  |
| DEMI KOUZOUNAS (Senate)  | 283,638          | 284,434        | −796 (RCV)    |

Harris and King gaps are RCV redistribution artifacts; reference data includes final RCV tally; precinct data shows first-round counts.

---
### Maryland
*[Source](https://www.elections.maryland.gov/elections/2024/index.html)*

#### Vote Aggregation Check

| Candidate                  | Precinct dataset | County dataset | Difference |
| -------------------------- | ---------------- | -------------- | ---------- |
| KAMALA D HARRIS            | 1,902,577        | 1,902,577      | 0          |
| DONALD J TRUMP             | 1,035,550        | 1,035,550      | 0          |
| ANGELA ALSOBROOKS (Senate) | 1,650,912        | 1,650,912      | 0          |
| LARRY HOGAN (Senate)       | 1,294,344        | 1,294,344      | 0          |

---
### Massachusetts
*[Source](https://electionstats.state.ma.us/elections/search/year_from:2024/year_to:2024/stage:General)*

#### Vote Aggregation Check

| Candidate                     | Precinct dataset | County dataset | Difference |
| ----------------------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP                | 1,251,303        | 1,251,303      | 0          |
| KAMALA D HARRIS               | 2,126,518        | 2,126,518      | 0          |
| ELIZABETH ANN WARREN (Senate) | 2,041,668        | 2,041,668      | 0          |
| JOHN DEATON (Senate)          | 1,365,440        | 1,365,440      | 0          |

---
### Michigan
*[Source](https://mielections.us/election/results/)*  

There are several cases of negative vote values that appear to be county-level correction artifacts, these were retained as reported.

#### Vote Aggregation Check

| Candidate               | Precinct dataset | County dataset | Difference |
| ----------------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP          | 2,816,636        | 2,816,636      | 0          |
| KAMALA D HARRIS         | 2,736,533        | 2,736,533      | 0          |
| ELISSA SLOTKIN (Senate) | 2,712,686        | 2,712,686      | 0          |
| MIKE ROGERS (Senate)    | 2,693,680        | 2,693,680      | 0          |

---
### Minnesota
*[Source](https://electionresults.sos.mn.gov/Select/MediaFiles/Index?ersElectionId=170)*

#### Vote Aggregation Check

| Candidate              | Precinct dataset | County dataset | Difference |
| ---------------------- | ---------------- | -------------- | ---------- |
| KAMALA D HARRIS        | 1,656,979        | 1,656,979      | 0          |
| DONALD J TRUMP         | 1,519,032        | 1,519,032      | 0          |
| AMY KLOBUCHAR (Senate) | 1,792,441        | 1,792,441      | 0          |
| ROYCE WHITE (Senate)   | 1,291,712        | 1,291,712      | 0          |

---
### Mississippi
*[Source](https://sos.ms.gov/elections/electionresults_aspx/elections_results_2024_county.aspx)*

#### Vote Aggregation Check

| Candidate               | Precinct dataset | County dataset | Difference |
| ----------------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP          | 747,744          | 747,744        | 0          |
| KAMALA D HARRIS         | 466,667          | 466,668        | −1         |
| ROGER F WICKER (Senate) | 763,420          | 761,934        | +1,486     |
| TY PINKINS (Senate)     | 451,980          | 450,749        | +1,231     |

---
### Missouri
*[Source](https://enr.sos.mo.gov/)*  

Kansas City rows use synthetic county_fips = 36000 as a cross-county placeholder because Kansas City spans multiple counties.

#### Vote Aggregation Check

| Candidate            | Precinct dataset | County dataset | Difference |
| -------------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP       | 1,751,986        | 1,751,986      | 0          |
| KAMALA D HARRIS      | 1,200,599        | 1,200,599      | 0          |
| JOSH HAWLEY (Senate) | 1,651,907        | 1,651,907      | 0          |
| LUCAS KUNCE (Senate) | 1,243,728        | 1,243,728      | 0          |

---
### Montana
*[Source](https://electionresults.mt.gov/ResultsSW.aspx)*

#### Vote Aggregation Check

| Candidate           | Precinct dataset | County dataset | Difference   |
| ------------------- | ---------------- | -------------- | ------------ |
| DONALD J TRUMP      | 352,001          | 352,079        | −78 (<0.03%) |
| KAMALA D HARRIS     | 231,856          | 231,906        | −50 (<0.03%) |
| TIM SHEEHY (Senate) | 319,618          | 319,682        | −64 (<0.02%) |
| JON TESTER (Senate) | 276,252          | 276,305        | −53 (<0.02%) |

---
### Nebraska
*[Source](https://electionresults.nebraska.gov/default.aspx)*

#### Vote Aggregation Check

| Candidate                             | Precinct dataset | County dataset | Difference |
| ------------------------------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP                        | 564,816          | 564,816        | 0          |
| KAMALA D HARRIS                       | 369,995          | 369,995        | 0          |
| DEB FISCHER (Senate regular)          | 499,124          | 499,124        | 0          |
| DAN OSBORN (Senate regular)           | 436,493          | 436,493        | 0          |
| PETE RICKETTS (Senate 2-yr special)   | 585,103          | 585,103        | 0          |
| PRESTON LOVE JR (Senate 2-yr special) | 349,902          | 349,902        | 0          |

NE had two senate races: regular (US SENATE: Fischer vs Osborn) and special (US SENATE - 2 YEAR TERM: Ricketts vs Love).

---
### Nevada
*[Source (results)](https://www.nvsos.gov/electionresults/)*  
*[Source (parties)](https://www.nvsos.gov/sos/elections/election-information/2024-election-information)*

#### Vote Aggregation Check

| Candidate               | Precinct dataset | County dataset | Difference    |
| ----------------------- | ---------------- | -------------- | ------------- |
| DONALD J TRUMP          | 750,963          | 751,205        | −242 (<0.04%) |
| KAMALA D HARRIS         | 705,057          | 705,197        | −140 (<0.02%) |
| JACKY S. ROSEN (Senate) | 700,976          | 701,105        | −129 (<0.02%) |
| SAM BROWN (Senate)      | 676,852          | 677,046        | −194 (<0.03%) |

Gaps attributable to `*` suppressed vote rows.

---
### New Hampshire
*[Source](https://www.sos.nh.gov/2024-general-election-results)*

#### Vote Aggregation Check

| Candidate       | Precinct dataset | County dataset | Difference |
| --------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP  | 395,523          | 395,523        | 0          |
| KAMALA D HARRIS | 418,488          | 418,488        | 0          |

---
### New Jersey
*Source:* NJ's data is collected from a number of locations, including:
- https://www.nj.gov/state/elections/election-night-results.shtml
- https://github.com/openelections/openelections-data-nj/tree/master/2024
- https://www.co.hunterdon.nj.us/DocumentCenter/View/15968/G2024-Official-Elections-Results-PDF 
- https://sussexcountyclerk.org/wp-content/uploads/2025/01/OFFICIAL-Precinct-Rpt-suppressed-11-25-Amended-web.pdf
- https://www.warrencountyvotes.com/home/showpublisheddocument/11384
- https://www.camdencounty.com/wp-content/elections/general2024/2024_General_Election_Canvasser.pdf
- https://www.bergencountyclerk.gov/_Content/pdf/ElectionResult/2024%20General%20District%20Report(2).pdf
- https://www.livevoterturnout.com/ENR/salemnjenr/7/en/Index_7.html
- https://gloucestercountynj.gov/1252/Previous-Election-Results


In 2024 NJ reported its data at the election district level but also included totals at the municipal level. For instance, an observation with `precinct = "Cliffside Park"` provides the total votes across "Cliffside Park 01", "Cliffside Park 02", etc. Care should be taken to not double count votes by including both the municipal totals and election district vote counts. Bergen and Gloucester `TOTAL` rows appear to double-count, while Burlington, Cumberland, Essex, and Mercer are missing `TOTAL rows`, so statewide sums using `TOTAL` or all modes require caution

#### Vote Aggregation Check

NJ has a complex multi-mode structure. 13 counties have TOTAL mode rows (county-level aggregates); 8 counties have only precinct-level rows (no TOTAL). The source data has known quality issues:
- Bergen and Gloucester TOTAL mode rows appear to double-count (2× expected).
- Burlington, Cumberland, Essex, Mercer have no TOTAL mode rows (missing from source).

**Presidential totals (all modes summed):**

| Candidate       | Precinct dataset | County dataset | Difference                                                 |
| --------------- | ---------------- | -------------- | ---------------------------------------------------------- |
| DONALD J TRUMP  | 2,468,310        | 1,968,215      | +500,095 (known over-count: double-counting in TOTAL mode) |
| KAMALA D HARRIS | 2,733,394        | 2,220,713      | +512,681 (known over-count: same)                          |

These discrepancies are a **known source data quality issue** — not a processing error. The source data double-counts TOTAL mode for Bergen/Gloucester and is missing TOTAL mode for Burlington/Essex/Mercer/Cumberland.

**Senate totals:**

| Candidate              | Precinct dataset | County dataset | Difference                            |
| ---------------------- | ---------------- | -------------- | ------------------------------------- |
| ANDY KIM (Senate)      | 2,580,816        | 2,161,491      | +419,325 (same double-counting issue) |
| CURTIS BASHAW (Senate) | 2,142,658        | 1,773,589      | +369,069 (same)                       |

---
### New Mexico
*[Source](https://electionresults.sos.nm.gov/)*

#### Vote Aggregation Check

| Candidate                      | Precinct dataset | County dataset | Difference   |
| ------------------------------ | ---------------- | -------------- | ------------ |
| DONALD J TRUMP                 | 423,381          | 423,391        | −10 (<0.01%) |
| KAMALA D HARRIS                | 478,755          | 478,802        | −47 (<0.01%) |
| MARTIN HEINRICH (Senate)       | 497,290          | 497,333        | −43 (<0.01%) |
| NELLA LOUISE DOMENICI (Senate) | 405,970          | 405,978        | −8 (<0.01%)  |

---
### New York
*Source:* Most counties' data were drawn from [OpenElections](https://github.com/openelections/openelections-sources-ny/tree/master/2024/general), NYC data drawn from [here](https://www.vote.nyc/page/election-results-summary). Nassau County data were generously provided by the Nassau County Board of Elections upon request. Orange County results for non-presidential races were generously provided by the Orange County Board of Elections.


New York is one of the most challenging states to gather and standardize precinct-level returns for due to data availability, formatting, and complexity. Considerable care should be taken when using these data and users should take note of the following:

* Party fusion: New York uses a party fusion system where candidates appear on multiple party lines. Most counties report vote totals for each party line separately, in these cases we preserve this in our data, for instance having a row for `candidate = "KAMALA D HARRIS" where `party_detailed = "WORKING FAMILIES"` and another where `party_detailed = "DEMOCRAT"`, in both cases `party_simplified = "DEMOCRACT"`. Some counties do not disaggregate by fusion party line in which case we report a single vote total for the candidate.
* Negative undervotes: There are two cases of undervotes being reported as `-2` in the raw Albany County data. We reached out to the Albany County Board of Elections who explained this as a system-balancing mechanism used when recorded votes slightly exceed the total ballots cast (e.g., due to voters sending in an absentee ballot after voting in person or by affidavit). This adjustment does not meaningfully impact vote totals and so is kept as it is reported in the raw data.
* Jefferson and Dutchess County have minor vote shortfalls/missing precincts due to "protected precincts" where data is suppressed for privacy.
* Herkimer County is missing results for `office = "State Proposal One"` in the raw data from the county.

#### Vote Aggregation Check

NY has 58 counties with direct total rows and 4 counties (CATTARAUGUS, CLINTON, OTSEGO, SCHENECTADY) without direct total rows. The comparison uses total votes across all reported county rows.

| Candidate                     | Precinct dataset | County dataset | Difference      |
| ----------------------------- | ---------------- | -------------- | --------------- |
| DONALD J TRUMP                | 3,579,349        | 3,578,899      | +450 (<0.01%)   |
| KAMALA D HARRIS               | 4,619,339        | 4,619,195      | +144 (<0.01%)   |
| KIRSTEN E GILLIBRAND (Senate) | 4,710,459        | 4,711,669      | −1,210 (<0.03%) |
| MICHAEL D SAPRAICONE (Senate) | 3,244,407        | 3,246,690      | −2,283 (<0.07%) |

---
### North Carolina
*[Source](https://www.ncsbe.gov/results-data/election-results/historical-election-results-data)*

#### Vote Aggregation Check

NC has 4 modes (no TOTAL). All modes summed.

| Candidate       | Precinct dataset | County dataset | Difference    |
| --------------- | ---------------- | -------------- | ------------- |
| DONALD J TRUMP  | 2,898,099        | 2,898,423      | −324 (<0.01%) |
| KAMALA D HARRIS | 2,714,494        | 2,715,375      | −881 (<0.03%) |

---
### North Dakota
*[Source](https://results.sos.nd.gov/ResultsExport.aspx?)*

#### Vote Aggregation Check

| Candidate                     | Precinct dataset | County dataset | Difference |
| ----------------------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP                | 246,505          | 246,505        | 0          |
| KAMALA D HARRIS               | 112,327          | 112,327        | 0          |
| KEVIN CRAMER (Senate)         | 241,569          | 241,569        | 0          |
| KATRINA CHRISTIANSEN (Senate) | 121,602          | 121,602        | 0          |

---
### Ohio
*[Source](https://www.ohiosos.gov/elections/election-results-and-data/2024-official-election-results/)*

#### Vote Aggregation Check

| Candidate              | Precinct dataset | County dataset | Difference |
| ---------------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP         | 3,180,116        | 3,180,116      | 0          |
| KAMALA D HARRIS        | 2,533,699        | 2,533,699      | 0          |
| BERNIE MORENO (Senate) | 2,857,383        | 2,857,383      | 0          |
| SHERROD BROWN (Senate) | 2,650,949        | 2,650,949      | 0          |

---
### Oklahoma
*[Source](https://results.okelections.gov/OKER/?elecDate=20241105)*

#### Vote Aggregation Check

| Candidate       | Precinct dataset | County dataset | Difference |
| --------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP  | 1,036,213        | 1,036,213      | 0          |
| KAMALA D HARRIS | 499,599          | 499,599        | 0          |

---
### Oregon
*Source:* [Open Elections](https://github.com/openelections/openelections-sources-or/tree/master/2024/general) and county websites

#### Vote Aggregation Check

| Candidate       | Precinct dataset | County dataset | Difference    |
| --------------- | ---------------- | -------------- | ------------- |
| DONALD J TRUMP  | 919,841          | 919,480        | +361 (<0.04%) |
| KAMALA D HARRIS | 1,240,316        | 1,240,600      | −284 (<0.02%) |

---
### Pennsylvania
*[Source](https://www.pa.gov/agencies/dos/resources/voting-and-elections-resources/voting-and-election-statistics/bulk-election-data.html#accordion-b33bb36a11-item-d105bc02cf)*

#### Vote Aggregation Check

| Candidate                  | Precinct dataset | County dataset | Difference      |
| -------------------------- | ---------------- | -------------- | --------------- |
| DONALD J TRUMP             | 3,543,041        | 3,543,308      | −267 (<0.01%)   |
| KAMALA D HARRIS            | 3,420,865        | 3,423,042      | −2,177 (<0.06%) |
| DAVID H MCCORMICK (Senate) | 3,399,054        | 3,399,295      | −241 (<0.01%)   |
| ROBERT P CASEY (Senate)    | 3,382,144        | 3,384,180      | −2,036 (<0.06%) |

---
### Rhode Island
*[Source](https://elections.ri.gov/elections/previous-election-results)*

#### Vote Aggregation Check

| Candidate                   | Precinct dataset | County dataset | Difference     |
| --------------------------- | ---------------- | -------------- | -------------- |
| DONALD J TRUMP              | 214,406          | 214,291        | +115 (<0.05%)  |
| KAMALA D HARRIS             | 285,156          | 283,750        | +1,406 (<0.5%) |
| SHELDON WHITEHOUSE (Senate) | 294,665          | 294,665        | 0              |
| PATRICIA MORGAN (Senate)    | 196,039          | 196,039        | 0              |

---
### South Carolina
*[Source](https://www.enr-scvotes.org/SC/122436/web.345435/#/access-to-races)*

#### Vote Aggregation Check

| Candidate       | Precinct dataset | County dataset | Difference |
| --------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP  | 1,483,747        | 1,483,747      | 0          |
| KAMALA D HARRIS | 1,028,452        | 1,028,452      | 0          |

---
### South Dakota
*[Source (official results)](https://electionresults.sd.gov/Default.aspx)*  
*[Source (candidate party labels)](https://vip.sdsos.gov/candidatelist.aspx?eid=684)*

#### Vote Aggregation Check

| Candidate       | Precinct dataset | County dataset | Difference |
| --------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP  | 272,081          | 272,081        | 0          |
| KAMALA D HARRIS | 146,859          | 146,859        | 0          |

---
### Tennessee
*[Source](https://sos.tn.gov/elections/results)*

#### Vote Aggregation Check

| Candidate                 | Precinct dataset | County dataset | Difference |
| ------------------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP            | 1,966,865        | 1,966,865      | 0          |
| KAMALA D HARRIS           | 1,056,265        | 1,056,265      | 0          |
| MARSHA BLACKBURN (Senate) | 1,918,743        | 1,918,743      | 0          |
| GLORIA JOHNSON (Senate)   | 1,027,461        | 1,027,461      | 0          |

---
### Texas
*[Source](https://data.capitol.texas.gov/topic/elections)*

#### Vote Aggregation Check

| Candidate             | Precinct dataset | County dataset | Difference    |
| --------------------- | ---------------- | -------------- | ------------- |
| DONALD J TRUMP        | 6,393,403        | 6,393,597      | −194 (<0.01%) |
| KAMALA D HARRIS       | 4,835,134        | 4,835,250      | −116 (<0.01%) |
| TED CRUZ (Senate)     | 5,990,637        | 5,990,741      | −104 (<0.01%) |
| COLIN ALLRED (Senate) | 5,031,142        | 5,031,249      | −107 (<0.01%) |

---
### Utah
*[Source](https://electionresults.utah.gov/results/public/utah/elections/general11052024)*

#### Vote Aggregation Check

| Candidate                | Precinct dataset | County dataset | Difference    |
| ------------------------ | ---------------- | -------------- | ------------- |
| DONALD J TRUMP           | 883,417          | 883,818        | −401 (<0.05%) |
| KAMALA D HARRIS          | 562,382          | 562,566        | −184 (<0.03%) |
| JOHN CURTIS (Senate)     | 914,298          | 914,700        | −402 (<0.05%) |
| CAROLINE GLEICH (Senate) | 464,368          | 464,515        | −147 (<0.03%) |

Small gaps attributable to canvassing noise.

---
### Vermont
*[Source](https://electionarchive.vermont.gov/elections/search/date:2024-11-05)*

#### Vote Aggregation Check

| Candidate               | Precinct dataset | County dataset | Difference |
| ----------------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP          | 119,395          | *              | -          |
| KAMALA D HARRIS         | 235,791          | *              | —          |
| BERNIE SANDERS (Senate) | 229,429          | 229,429        | 0          |
| GERALD MALLOY (Senate)  | 116,512          | 116,512        | 0          |

*County-level presidential data for VT is incomplete (missing several counties); our data matches official VT Secretary of State results (~119K Trump, ~235K Harris).

---
### Virginia
*[Source](https://enr.elections.virginia.gov/results/public/Virginia/elections/2024NovemberGeneral)*

#### Vote Aggregation Check

| Candidate                | Precinct dataset | County dataset | Difference |
| ------------------------ | ---------------- | -------------- | ---------- |
| DONALD J TRUMP           | 2,075,085        | 2,075,085      | 0          |
| KAMALA D HARRIS          | 2,335,395        | 2,335,395      | 0          |
| TIMOTHY M KAINE (Senate) | 2,417,115        | 2,417,115      | 0          |
| HUNG CAO (Senate)        | 2,019,911        | 2,019,911      | 0          |

---
### Washington
*[Source](https://results.vote.wa.gov/results/20241105/export.html)*

#### Vote Aggregation Check

| Candidate               | Precinct dataset | County dataset | Difference      |
| ----------------------- | ---------------- | -------------- | --------------- |
| DONALD J TRUMP          | 1,528,208        | 1,530,923      | −2,715 (<0.18%) |
| KAMALA D HARRIS         | 2,243,401        | 2,245,849      | −2,448 (<0.11%) |
| MARIA CANTWELL (Senate) | 2,251,055        | 2,252,577      | −1,522 (<0.07%) |
| DR RAUL GARCIA (Senate) | 1,547,135        | 1,549,187      | −2,052 (<0.13%) |

---
### West Virginia
*[Source](https://results.enr.clarityelections.com/WV/122766/web.345435/#/summary)*

#### Vote Aggregation Check

| Candidate              | Precinct dataset | County dataset | Difference |
| ---------------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP         | 533,556          | 533,556        | 0          |
| KAMALA D HARRIS        | 214,309          | 214,309        | 0          |
| JIM JUSTICE (Senate)   | 514,079          | 514,079        | 0          |
| GLENN ELLIOTT (Senate) | 207,548          | 207,548        | 0          |

---
### Wisconsin
*[Source](https://elections.wi.gov/elections/election-results#accordion-11951)*  

`VILLAGE OF LISBON` rows are missing jurisdiction_name and jurisdiction_fips in the source data and could not be resolved cleanly.

#### Vote Aggregation Check

| Candidate              | Precinct dataset | County dataset | Difference |
| ---------------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP         | 1,697,626        | 1,697,626      | 0          |
| KAMALA D HARRIS        | 1,668,229        | 1,668,229      | 0          |
| TAMMY BALDWIN (Senate) | 1,672,777        | 1,672,777      | 0          |
| ERIC HOVDE (Senate)    | 1,643,996        | 1,643,996      | 0          |

---
### Wyoming  
*[Source](https://sos.wyo.gov/Elections/Docs/2024/2024GeneralResults.aspx)*  


#### Vote Aggregation Check

| Candidate               | Precinct dataset | County dataset | Difference |
| ----------------------- | ---------------- | -------------- | ---------- |
| DONALD J TRUMP          | 192,633          | 192,633        | 0          |
| KAMALA D HARRIS         | 69,527           | 69,527         | 0          |
| JOHN BARRASSO (Senate)  | 198,418          | 198,418        | 0          |
| SCOTT D MORROW (Senate) | 63,727           | 63,727         | 0          |

---
