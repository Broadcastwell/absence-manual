---
title: Does low presence persist? The registered study is waiting for comparable releases
description: Study 3 protocol, OSF registration, fixed thresholds and comparability rules. August and September
  standings are separate dated observations; no persistence result is available.
page_class: research
research_id: 45
research_group: study
lead: Ananya Rao
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/studies/does-absence-persist/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://doi.org/10.17605/OSF.IO/MKJ9V
research_dataset:
  name: Registered protocol for persistence of vendor presence
  description: Protocol and separately dated historical standings. No persistence outcomes have been computed.
  identifier: https://doi.org/10.17605/OSF.IO/MKJ9V
  distribution:
  - name: Dated historical standings
    contentUrl: https://docs.broadcastwell.com/research/data/dated-standings.csv
    encodingFormat: text/csv
---

# Does low presence persist? The registered study is waiting for comparable releases

**Study 3 requires a third release and a comparable consecutive pair before estimating persistence (Broadcastwell, 2026, OSF MKJ9V).**

There is no persistence estimate yet. Study 3 is registered, and its waiting rule requires both a third Absence Index release and a consecutive pair with the same published configuration. The existing August and September observations do not meet that comparability rule. [Broadcastwell, Study 3 registration](https://doi.org/10.17605/OSF.IO/MKJ9V).

Registration DOI: **10.17605/OSF.IO/MKJ9V**. OSF recorded registration on **30 October 2026 at 01:12:44 UTC**. This page publishes the protocol and historical context. It does not announce a transition finding or predict which vendors will remain absent. [OSF registration record, checked 30 October 2026].

A company can be missing from many measured answers on one date without being permanently invisible. It might appear under another question, in another engine or after a refresh. The question here is narrower: when a vendor has low measured presence in an eligible release, how often does that same vendor-category observation remain in the low band in the next comparable release?

## Registered protocol, unchanged

The text below is the registered plan, including the prior-knowledge and timing statements as recorded then. The separately disclosed Study 2 timing amendment does not relax this protocol's waiting or comparability conditions. [OSF MKJ9V](https://doi.org/10.17605/OSF.IO/MKJ9V).

### Question and status

> For vendors measured in consecutive, comparable Absence Index releases, what share of those named in a quarter or fewer of eligible answers remain in that band in the next release? What share of those named in three quarters or more remain in that band? This is a registered protocol for future descriptive analysis. No persistence result is being computed now.

### Sources and prior knowledge

> The historical comparison sources are the corrected August 2026 archive, version DOI 10.5281/zenodo.22721962, and the September 2026 release, version DOI 10.5281/zenodo.22907695. The Index concept DOI is 10.5281/zenodo.22150321. Record the exact version DOI, published method and checksums for any future release used. The existing releases and published summaries are known; this is not a claim of complete blinding. None of the new research-section study outcomes have been computed. All three plans must be registered before analysis begins.

### Waiting and comparability rule

> Do not compute persistence until a third Index release exists. A third release alone is insufficient: there must also be a consecutive pair with the same published configuration. Require matching category scope and definition, target question text and type, engine set, scheduled repeat count, vendor matching rules and eligible-answer rules. Exclude controls from standings. Document capture dates, exclusions and any differences in valid bases. If the published configurations differ or cannot be verified, do not join them into a transition estimate. Register an amendment before using a changed rule. The August and September configurations differ, so show their CRM and project-management standings only as two separately dated observations, with a configuration table placed first. Do not use those two releases to claim improvement, deterioration, momentum or persistence.

### Units and cohort

> The primary transition unit is a vendor-category pair in the intersection of the vendor universes measured in both eligible releases. Identify vendors by published canonical-domain and documented identity mappings, not by an undocumented fuzzy name join. Publish additions, removals, renames and unmatched records separately. The principal analysis pools the configured engines within each release; report per-engine transitions as secondary descriptive strata when they are comparable. No sampling or recruitment is planned: include the full eligible matched cohort, with exact inclusion and exclusion counts.

### Definitions

> Use unrounded named counts and valid target-answer bases from each release. A low-presence observation has named_count divided by valid_base less than or equal to 0.25. A high-presence observation has that ratio greater than or equal to 0.75. A zero valid base is missing, never zero presence. Use integer cross-products for band membership so rounding does not move a vendor across a boundary. Keep the middle band and all missing observations visible. Vendor presence is an observed naming rate, not product quality, market share, a purchase recommendation or a universal engine ranking.

### Primary statistics

> For each comparable release pair, count vendors in the low band at N and count how many of them are still in the low band at N+1. Report the numerator, eligible low-band base, conditional proportion and a two-sided Wilson 95% interval. Repeat for the high band. Show the full transition table among low, middle and high bands, plus missing records, so band selection cannot hide other outcomes. Give each category separately and a pooled matched-cohort table; state that categories and engines are not interchangeable independent samples. Provide per-engine tables only when that engine's configuration is unchanged. Publish calculations, input version references and join/exclusion CSVs. There is no p-value threshold, directional hypothesis or minimum effect required for publication.

### Finding rule and interpretation

> A finding is a reproducible descriptive transition proportion from an eligible pair, whether persistence is high, low or indeterminate. If there is no eligible pair, the finding is that the protocol remains waiting; do not manufacture a result. Compare cautiously with the rich-get-richer discussion in Lewandowski, Suenkler and Yagci (2021), DOI 10.1145/3447535.3462479. That discussion concerns Google search results and possible selection feedback; it is not proof of an AI-answer mechanism. Persistent absence cannot establish its cause, and a threshold transition is not proof of a durable change in buyer exposure.

### Limits and reporting

> A fixed question bank is not representative of all buyer questions. Repeated answers may be dependent, observations change with refreshes, and surviving matched vendors are a selected cohort. Wilson intervals summarize the observed archive and are not a guarantee about future answers. Different release dates can include external product or publisher changes that this design does not isolate. Report every protocol deviation with its timing and reason. Publish the registration URL and timestamp on the study page now; add results only after the waiting and comparability conditions are satisfied. Do not claim control or ownership of AI answers.

## Which configurations produced the dated observations?

The configuration table comes before the standings because matching question text cannot cancel a different engine set or missing evidence about other collection conditions.

| Configuration | Corrected August release 2026-08.1 | September release 2026-09 |
| --- | --- | --- |
| Version DOI | 10.5281/zenodo.22721962 | 10.5281/zenodo.22907695 |
| Published release date in JSON | 28 August 2026 | 23 September 2026 |
| Category scope | CRM and project management | Fourteen software categories, including those two |
| Engines | ChatGPT, Claude, Perplexity, Google AI Overviews | Those four plus Google AI Mode |
| Target questions and scheduled repeats | Ten questions per category, three repeats per engine | Ten questions per category, three repeats per engine |
| Shared CRM and project-management question text | Ten exact text matches in each shared category against September | The same ten texts in each shared category |
| Shared-category valid target bases | CRM 117; project management 120 | CRM 150; project management 150 |
| Controls | None in these historical standings | Additional control questions for CRM and construction project management; excluded from standings |
| Naming evidence | Published aggregate verdicts; answer text not retained in this deposit | Archived answer text and cited URL arrays, with published matching rules |

Sources: the two versioned release JSONs and READMEs, verified 30 October 2026. The shared question wording was compared directly, not assumed from the category label. Matching wording does not cancel the different engine set or answer-evidence scope.

## The current standings are two observations

The table below contains the shared historical vendors with the release configuration shown above it. There is no change column. Different valid bases and engine coverage prevent an interpretation of these columns as an estimated improvement, deterioration or persistence probability.

| Category and vendor | August 2026.1, named/base, share [Wilson 95% interval] | September 2026, named/base, share [Wilson 95% interval] |
| --- | --- | --- |
| CRM: Salesforce Sales Cloud | 78/117, 66.7% [57.7% to 74.6%] | 109/150, 72.7% [65.0% to 79.2%] |
| CRM: HubSpot CRM | 77/117, 65.8% [56.8% to 73.8%] | 113/150, 75.3% [67.9% to 81.5%] |
| CRM: Pipedrive | 63/117, 53.8% [44.8% to 62.6%] | 97/150, 64.7% [56.7% to 71.9%] |
| CRM: Zoho CRM | 63/117, 53.8% [44.8% to 62.6%] | 73/150, 48.7% [40.8% to 56.6%] |
| CRM: Nimble | 0/117, 0.0% [0.0% to 3.2%] | 0/150, 0.0% [0.0% to 2.5%] |
| CRM: Microsoft Dynamics 365 | 23/117, 19.7% [13.5% to 27.8%] | 36/150, 24.0% [17.9% to 31.4%] |
| CRM: Freshsales | 15/117, 12.8% [7.9% to 20.1%] | 22/150, 14.7% [9.9% to 21.2%] |
| CRM: Copper | 1/117, 0.9% [0.2% to 4.7%] | 4/150, 2.7% [1.0% to 6.7%] |
| CRM: Insightly | 3/117, 2.6% [0.9% to 7.3%] | 10/150, 6.7% [3.7% to 11.8%] |
| CRM: Close | 5/117, 4.3% [1.8% to 9.6%] | 12/150, 8.0% [4.6% to 13.5%] |
| Project management: Jira | 32/120, 26.7% [19.6% to 35.2%] | 63/150, 42.0% [34.4% to 50.0%] |
| Project management: Asana | 62/120, 51.7% [42.8% to 60.4%] | 97/150, 64.7% [56.7% to 71.9%] |
| Project management: Smartsheet | 40/120, 33.3% [25.5% to 42.2%] | 54/150, 36.0% [28.8% to 43.9%] |
| Project management: monday.com | 71/120, 59.2% [50.2% to 67.5%] | 26/150, 17.3% [12.1% to 24.2%] |
| Project management: ClickUp | 56/120, 46.7% [38.0% to 55.6%] | 80/150, 53.3% [45.4% to 61.1%] |
| Project management: Notion | 1/120, 0.8% [0.1% to 4.6%] | 6/150, 4.0% [1.8% to 8.5%] |
| Project management: Airtable | 8/120, 6.7% [3.4% to 12.6%] | 13/150, 8.7% [5.1% to 14.3%] |
| Project management: Wrike | 49/120, 40.8% [32.5% to 49.8%] | 54/150, 36.0% [28.8% to 43.9%] |
| Project management: Basecamp | 6/120, 5.0% [2.3% to 10.5%] | 18/150, 12.0% [7.7% to 18.2%] |
| Project management: Trello | 18/120, 15.0% [9.7% to 22.5%] | 32/150, 21.3% [15.5% to 28.6%] |


Sources: corrected August and September release JSON vendor counts; Wilson intervals reproduced from the stated numerator and valid base. Verified 30 October 2026. The [dated standings CSV](/research/data/dated-standings.csv) retains each count and interval separately. The [offline calculation](/research/data/dated_standings.py) reproduces the published named counts and Wilson intervals without computing transitions. The August correction concerns qualifying own-domain citation fields; it does not turn the retained named counts into a fresh re-score of missing answer text.

This side-by-side has a practical use even while the study waits. It lets you identify what was measured and locate a vendor's dated record without pretending the two designs were interchangeable. A buyer evaluating project-management software and a marketer evaluating a campaign need different conclusions from the same table. This table provides neither a product-quality verdict nor a campaign-effect estimate.

## Why discuss rich-get-richer effects at all?

Lewandowski, Sünkler and Yagci discuss a possible feedback mechanism in Google search: already visible optimized material may receive interactions that reinforce visibility. Their discussion says that such behavior “may lead to a rich-get-richer effect.” It is a proposed mechanism, not proof that low-presence software vendors are trapped in AI answers. [Lewandowski et al., 2021, §6, original p. 19](https://searchstudies.org/wp-content/uploads/2021/08/3447535.3462479.pdf).

Study 3 can describe persistence if its conditions are met. It cannot identify that mechanism from transitions alone. Persistent low presence could reflect a fixed question bank, product fit, source availability, engine behavior or other factors not isolated by this design. A stable high band would have similarly limited causal meaning.

There is a trade-off in waiting. We give up the convenience of an immediate longitudinal headline. In return, the future reader can distinguish a predeclared comparison from one chosen because the first pair happened to look persuasive. The historical releases and their published summaries were already known when the plan was registered, so this is not a claim of complete blinding.

## What will change on this page next?

The result remains unavailable. Once an eligible pair exists, the update will identify its version DOIs and capture windows, the matched cohort and exclusions, and each transition count with its descriptive interval. Any amendment or deviation belongs beside the affected table, with a date and an explanation; an unavailable estimate must never be displayed as zero.

The Study 2 timing departure remains separately recorded. It authorized that already registered secondary analysis while Study 1 awaited approval, without permitting an early persistence estimate here or changing the comparability conditions quoted above.

## What our own data shows

We have no measurement on this point: release-to-release absence persistence under the registered comparability conditions. The existing September archive measures 286 vendors across fourteen categories, with 2,095 valid target answers after five target exclusions. The table above shows only the shared historical CRM and project-management vendors and their own category bases. We have no measurement on the persistence question yet. The protocol is a commitment to a future eligible comparison, not a claim that either low or high presence already persists.

## Sources

- Broadcastwell. (2026). Does absence persist from one release to the next? [Registration]. OSF. Registered 30 October 2026, 01:12:44 UTC. https://doi.org/10.17605/OSF.IO/MKJ9V Verified 30 October 2026.
- Broadcastwell. (2026). Absence Index, release 2026-08.1 [Data set]. Zenodo. Release files and README. https://doi.org/10.5281/zenodo.22721962 Verified 30 October 2026.
- Broadcastwell. (2026). Absence Index, release 2026-09 [Data set]. Zenodo. Release JSON, answer JSONL and README. https://doi.org/10.5281/zenodo.22907695 Verified 30 October 2026.
- Lewandowski, D., Sünkler, S., & Yagci, N. (2021). The influence of search engine optimization on Google's results. In WebSci '21 (pp. 12 to 20). ACM. doi:10.1145/3447535.3462479 . [Accessible original](https://searchstudies.org/wp-content/uploads/2021/08/3447535.3462479.pdf) Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *Does low presence persist? The registered study is waiting for comparable releases*. Broadcastwell. https://docs.broadcastwell.com/research/studies/does-absence-persist/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research45,
  author = {{Broadcastwell research team}},
  title = {Does low presence persist? The registered study is waiting for comparable releases},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/studies/does-absence-persist/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Ananya Rao, AI engineer.

Sources checked 30 October 2026. Independent check: 30 October 2026, Broadcastwell verification desk. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the measurement chapter](https://docs.broadcastwell.com/measurement-noise/).
