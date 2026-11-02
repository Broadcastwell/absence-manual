---
title: 'Rovira and colleagues: citations, search restrictions and a spreadsheet discrepancy'
description: The 2019 comparison of scholarly search systems, all nine reported correlations, the median-by-position
  method and a reproducible range omission in one deposited workbook.
page_class: research
research_id: 13
research_group: source
lead: Arjun Mehta
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/sources/rovira-2019/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://doi.org/10.3390/fi11090202
---

# Rovira and colleagues: citations, search restrictions and a spreadsheet discrepancy

**Rovira’s two-term Google Scholar correlations are 0.721 unrestricted and 0.994 title-restricted; they compare aggregated ranks (2019, Table 2).**

Restricting the search to titles changes the comparison substantially. Rovira and colleagues report Google Scholar coefficients of 0.721 for unrestricted two-term searches and 0.994 for title-restricted two-term searches. Neither coefficient is a probability that a paper will be cited. [Rovira et al., 2019, Table 2](https://docs.broadcastwell.com/research/source-archives/rovira-2019.pdf).

The distinction matters. Here, citations are references already received by scholarly documents, while the observed visibility outcome is their relevance ordering in academic search systems. Neither measure records a software vendor's appearance in an AI-generated answer.

There is also a reproducibility detail worth keeping in view from the start. One deposited spreadsheet calculates its medians from fewer query columns than the method describes. The broad association survives the correction, but the precise reported coefficient changes at the published rounding level. A useful paper can have a specific, inspectable calculation defect.

## The searches were broad by design

The researchers compared Google Scholar, Microsoft Academic, Scopus and Web of Science during 10 to 30 May 2019. They selected common academic terms and search suggestions that produced many results. The collections used sets of 25 searches with up to 1,000 results per search. Some configurations used one search term, others two, and the available search restrictions differed across systems. [§3, reprint PDF pp. 54 to 55].

This is not a study of 25,000 independent query formulations per system. The detailed method describes 25 searches and their result items. Its isolated phrase “25,000 searches” conflicts with that account. We use the detailed units so that result items do not become an inflated query count. [§3].

The selection also favors broad, result-rich scholarly queries. That makes it practical to compare deep result lists, but it leaves a question about narrow searches with few results. The authors expressly call for future confirmation of the ranking behavior in that setting. A procurement question about a specific integration is not represented merely because both tasks use a search box. [§5, PDF p. 63].

## What was correlated?

For each search, the authors made a second ordering based on the number of academic citations the documents had received. They compared that ordering with the system's native relevance order. To summarize the selected searches, they calculated the median citation-based rank at each native result position and then calculated a Spearman rank correlation for those median summaries. [§3, PDF p. 55].

That aggregation is the crucial qualification. The headline coefficient is not the typical correlation for a single query and not a fit to every individual result as an independent observation. Taking a median at each position reduces the variation among the query-specific rankings before the final comparison.

You can imagine the issue without inventing a new empirical result. Several searches may disagree about which documents belong near the top while their position-wise medians still form a smooth increasing sequence. A high correlation in the summary says something about that summary. To answer a question about a particular search, you would also inspect the individual-search distributions and their restrictions.

## All nine configurations belong in the table

| System and configuration | Table 2 Spearman coefficient | What must stay attached |
| --- | ---: | --- |
| Google Scholar, one term, unrestricted | 0.968 | Median-by-position summary; historical collection |
| Google Scholar, two terms, unrestricted | 0.721 | The lowest reported Google Scholar configuration |
| Google Scholar, one term, title restricted | 0.990 | Workbook range omission discussed below |
| Google Scholar, two terms, title restricted | 0.994 | All returned titles satisfy the search restriction |
| Microsoft Academic, one term | 0.907 | Title, abstract and keyword search scope |
| Microsoft Academic, two terms | 0.937 | Same bibliographic-field scope |
| Scopus, two terms | −0.107 | Near-zero negative association in this collection |
| Web of Science, first collection | −0.075 | Separate observed relevance ordering |
| Web of Science, second collection | 0.907 | Citation-like ordering during part of the collection window |

Source: Rovira et al., Table 2, reprint PDF p. 56, verified 30 October 2026. These are correlations, not shares; Wilson intervals do not apply. We reproduce reported values here and distinguish the affected configuration from the recomputation below.

A shorthand range of 0.968 to 0.994 for all Google Scholar configurations would omit the 0.721 result. Likewise, a list containing only the high coefficients would conceal the Scopus and first Web of Science observations. The full table makes the differences between configurations visible.

The paper interprets the title-restriction comparison as evidence that title terms and citations both matter in scholarly relevance ordering. That interpretation is plausible within the design, but it is not an intervention estimating what happens when an author adds a particular keyword to a title. Search restriction changes which records are eligible for the comparison. [§4].

## The deposited formula leaves out two columns

We downloaded the original workbooks from the authors' Zenodo dataset and matched the publisher's checksums. We read the original stored formulas and cached values without saving or recalculating the workbooks. [Rovira et al., deposited data, version DOI 10.5281/zenodo.3381151](https://doi.org/10.5281/zenodo.3381151).

In `GS-1-word-title-restriction.xlsx`, sheet `Full 1`, cell B2 contains `MEDIAN(C2:Y2)`. That range spans 23 query columns. The query headers continue through Z1, theory, and AA1, variable. Both columns sit outside the median formula. The same omission continues through the 1,000 stored median cells B2:B1001.

| Check on that workbook | Stored 23-column calculation | Recalculation using all 25 query columns |
| --- | ---: | ---: |
| Median at result position one, row 2 | 10 | 14 |
| Spearman correlation across 1,000 positions | 0.9903496178 | 0.9910214634 |
| Coefficient rounded to three decimals | 0.990 | 0.991 |

Across the 1,000 positions, 456 medians differ. This is a count of changed summary cells, not a proportion of searches producing a different answer. Blank query-result cells remain blank and are omitted from each median as in the spreadsheet's numeric median calculation; they are never replaced with zero. [Original workbook cells B2:B1001 and C2:AA1001; Broadcastwell source-data reanalysis, checked 30 October 2026].

The other eight configurations reproduce their Table 2 coefficients at three decimal places when we use all available numeric values across their 25 query columns. The correction therefore concerns one calculation range, not a rejection of every result in the article. We do not infer intent or the cause of the omitted columns.

The [reanalysis table](/research/data/rovira-workbook-reanalysis.csv), [differing median cells](/research/data/rovira-median-differences.csv) and [reproduction code](/research/data/recompute_source_workbooks.py) retain the source filenames, hashes, formulas and separate cached and reconstructed values. The original deposits remain the authority for the underlying observations.

## A changing order is not a confirmed test

The Web of Science observations deserve their dates. The article reports an unexpectedly citation-like ranking during 20 to 25 May 2019. It proposes that the service might have been testing a change, while explicitly describing that explanation as “only an inference.” [§4, PDF p. 60].

We can cite the observed difference. We cannot turn the proposed explanation into a statement from the operator, an announced experiment or a permanent description of the service. The ordering could have several explanations that this design does not isolate. Even the system name needs historical framing: a 2019 service comparison is not a verified inventory of today's available products.

This is the second thread running through the paper. The title restriction, the date and the aggregation method all change what a reported coefficient means. A number taken out of that setting becomes much easier to repeat and much harder to defend.

## How should a B2B marketer use this research?

If you publish research, the paper supports taking scholarly discovery seriously as a distinct setting with its own metadata and citation history. It does not support copying a coefficient into an AI-visibility forecast. A well-cited academic article, a product documentation page and a vendor review can enter different systems through different processes.

For a company measuring AI answers, the useful habit is to preserve the configuration before comparing outputs. Record the exact questions, engines, eligible answers and naming rules. If those differ between releases, describe two dated observations first. A common vendor name does not make the research design common.

There remains an appealing unanswered question: under a stable configuration, does a vendor's low observed presence persist? This article cannot answer it. Its citations and search ranks belong to scholarly documents in a historical collection. The question needs its own longitudinal vendor-answer data, a defined matched cohort and a waiting rule that does not disappear when the early tables look interesting.

## What our own data shows

Our corrected August and September Index releases share CRM and project-management vendor identities, but differ in engine coverage, control scope and valid-answer bases. For example, Microsoft Dynamics 365 is named in 23 of 117 valid August CRM answers, 19.7% (Wilson 95% interval 13.5% to 27.8%), and separately in 36 of 150 September answers, 24.0% (17.9% to 31.4%). These are dated observations under different configurations, not an estimated change or a persistence result. [August version](https://doi.org/10.5281/zenodo.22721962); [September version](https://doi.org/10.5281/zenodo.22907695); [registered waiting rule](https://doi.org/10.17605/OSF.IO/MKJ9V).

## Sources

- Rovira, C., Codina, L., Guerrero-Solé, F., & Lopezosa, C. (2019). Ranking by relevance and citation counts, a comparative study: Google Scholar, Microsoft Academic, WoS and Scopus. Future Internet, 11(9), 202. doi:10.3390/fi11090202 . [Accessible original](https://docs.broadcastwell.com/research/source-archives/rovira-2019.pdf) Verified 30 October 2026.
- Rovira, C., Codina, L., Guerrero-Solé, F., & Lopezosa, C. (2019). Ranking by relevance and citation counts: Deposited search-result workbooks [Data set]. Zenodo. https://doi.org/10.5281/zenodo.3381151 . Nine original XLSX files, read without saving or recalculating. Verified 30 October 2026.
- Broadcastwell. (2026). Absence Index, release 2026-08.1 [Data set]. Zenodo. Release files and README. https://doi.org/10.5281/zenodo.22721962 Verified 30 October 2026.
- Broadcastwell. (2026). Absence Index, release 2026-09 [Data set]. Zenodo. Release JSON, answer JSONL and README. https://doi.org/10.5281/zenodo.22907695 Verified 30 October 2026.
- Broadcastwell. (2026). Does absence persist from one release to the next? [Registration]. OSF. Registered 30 October 2026, 01:12:44 UTC. https://doi.org/10.17605/OSF.IO/MKJ9V Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *Rovira and colleagues: citations, search restrictions and a spreadsheet discrepancy*. Broadcastwell. https://docs.broadcastwell.com/research/sources/rovira-2019/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research13,
  author = {{Broadcastwell research team}},
  title = {Rovira and colleagues: citations, search restrictions and a spreadsheet discrepancy},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/sources/rovira-2019/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Arjun Mehta, management consultant.

Sources checked 30 October 2026. Independent check: 30 October 2026, Broadcastwell verification desk. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the measurement chapter](https://docs.broadcastwell.com/measurement-noise/).
