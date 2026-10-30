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

## What has to match before we join releases?

The registered plan requires matching category definitions, target question text and type, engine set, scheduled repeats, vendor matching rules and eligible-answer rules. Controls stay outside vendor standings. Capture dates and differences in valid bases remain visible. A third release by itself does not authorize a transition estimate. [Registered plan, Waiting and comparability rule].

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

If the configuration differs or cannot be verified, the protocol says not to join those releases into a transition estimate. A changed comparability rule would require a registered amendment before use. Choosing a subset after seeing an attractive result would answer a different question from the one registered here.

## The cohort and the bands are fixed in advance

The primary unit is a vendor-category pair in the intersection of the vendor universes in the two eligible releases. Canonical domains and documented identity mappings establish the join. An undocumented fuzzy name match does not. Additions, removals, renames and unmatched records will be published separately. [Registered plan, Units and cohort].

The low band means a vendor is named in **a quarter or fewer** of the valid target answers for its category. The high band means naming in **three quarters or more**. These are operational thresholds chosen in the registration, not natural boundaries between successful and unsuccessful businesses. We will use unrounded counts and integer cross-products to determine membership. A rounded display percentage must not push a vendor across a threshold. [Definitions].

A zero valid base means missing evidence. It does not mean zero presence. The middle band remains in the transition table, and missing observations remain visible. This avoids an appealing but incomplete comparison that selects only the most extreme vendors and forgets the rest of the cohort.

The principal table pools the configured engines within each eligible release. Secondary engine-specific tables will appear only when that engine's configuration is unchanged. The registered plan includes the full eligible matched cohort rather than recruiting a new sample of companies.

## What will the persistence estimate mean?

For the low band, the numerator will be the number of eligible vendor-category pairs that are low at the first release and still low at the next. The denominator will be all eligible low-band pairs at the first release. The high-band estimate uses the corresponding high-band cohort. Each will include its exact count, base, proportion and two-sided Wilson 95% interval. [Registered plan, Primary statistics].

The full low, middle and high transition table will accompany these conditional shares, together with missing records. Category-specific tables and a pooled matched-cohort table will be reported. Repeated answers and categories are not interchangeable independent draws from all buyer behavior. The intervals describe the observed archive under these rules, with that dependence and the fixed question bank left explicit.

No p-value threshold or minimum directional effect is required for publication. If the eligible data show little persistence, that is still a result. If there is no eligible pair, the protocol remains waiting. The registered wording is direct: “do not manufacture a result.” [Finding rule and interpretation].

You will be able to inspect the input versions, identity join, exclusions and calculation tables. The study will not turn a threshold crossing into proof that a marketing action worked. It records an observed sequence, with external product changes, publisher changes and engine changes still possible.

## The current standings are two observations

The table below contains the shared historical vendors with the release configuration shown above it. It is deliberately presented without a change column, arrows or a trend score. Different valid bases and engine coverage prevent an interpretation of these columns as an estimated improvement, deterioration or persistence probability.

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

Results will be added only after the third-release and same-configuration conditions hold. The update will identify the version DOIs, capture windows, matched vendors, exclusions, transition counts and descriptive intervals. Any amendment or deviation will be dated and explained beside the affected table. Until then, the empty result is an unavailable estimate, not a measured zero.

The registration originally included an all-three-studies-before-analysis timing clause. A later timing ruling authorized the already registered Study 2 to proceed while Study 1 waits. That departure is recorded with Study 2; it supplies no permission to compute Study 3 persistence early. The waiting and comparability rules on this page still govern this study.

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

Sources checked 30 October 2026. Independent check: pending. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the measurement chapter](https://docs.broadcastwell.com/measurement-noise/).
