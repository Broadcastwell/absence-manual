---
title: A small Google study does not give you a ranking recipe
description: The full Ziakis et al. correlation table, its three-query design and the limits of turning 45 selected
  results into a universal SEO checklist.
page_class: research
research_id: 16
research_group: source
lead: Ethan Brooks
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/sources/ziakis-2019/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://doi.org/10.3390/fi11020032
---

# A small Google study does not give you a ranking recipe

**The strongest average correlation was SSL at −0.3371 across three 15-result samples, not a ranking weight (Ziakis et al., 2019, Table 2).**

An average correlation of **−0.3371** for SSL certificates is the strongest reported relationship in this small observational study. That is an association within selected Google results, not an experimentally established instruction for changing a page’s rank. [Ziakis et al., 2019, Table 2, reprint PDF pp. 19 to 20, printed pp. 10 to 11](https://docs.broadcastwell.com/research/source-archives/ziakis-2019.pdf).

The distinction matters when a research table becomes an agency checklist. Security is worth maintaining for your visitors. The table does not tell you how many positions installing a certificate would gain, whether the certificate itself produced the association, or whether the relationship applies to software-buying questions today.

## What did the authors actually sample?

They collected the first **15 Google results** for each of three queries: “Hotel Athens,” “email marketing” and “casual shoes.” The searches took place on **1 April 2018 at 11:45 pm**, **12 April 2018 at 2:40 pm**, and **13 April 2018 at 4:00 pm**, respectively. This yields **45 selected result entries**, not 45 randomly sampled queries or a representative panel of all Google results. [§2, reprint PDF p. 13, printed p. 4].

The subject mix is useful context. Local hospitality, a marketing service and consumer footwear have different businesses, page types and competitive conditions. None is a controlled comparison of otherwise identical pages. The paper does not provide a probability-sampling frame from which to infer the prevalence of a relationship across the web.

The authors first reviewed literature and practitioner material to choose candidate factors. Their literature search covered ScienceDirect, Springer and IEEE Xplore during February and March 2018. They describe approximately **1,010 initial citations**, **125 articles after title and abstract screening**, and **23 articles used for the literature review**. Those are stages in selecting references, not additional observations supporting the correlation estimates. [§2].

The empirical and review components need separate labels. A factor can appear in the review because other authors discussed it without the present experiment demonstrating its causal importance. The conclusions refer to **24 SEO factors** discussed in the paper, while the empirical correlation table contains **21 measured rows**. We reproduce the table’s actual rows rather than expanding its sample to match that broader narrative count. [§5.1 and Table 2].

## How were the measurements transformed?

The study placed measurements on a **0 to 9 scale**, calculated Spearman rank correlations within each query sample, then averaged the three coefficients for each factor. Missing values were replaced with the average of the remaining normalized data. The authors say they consider this substitution not to affect the outcome. They do not report a sensitivity analysis demonstrating that assumption. [§2, PDF p. 13].

Spearman correlation describes whether two variables tend to order observations similarly. A negative coefficient can be consistent with stronger factor values occurring at numerically smaller, better positions. Its sign still depends on how a factor was coded. It is not a percentage contribution to Google’s algorithm.

Normalization, ties, missing-data substitution and the selected position range all affect what a coefficient means. Averaging three query-level coefficients is also different from fitting one relationship to a larger pooled sample. The table’s average should not be given the sampling interpretation of an independently estimated population coefficient with a published uncertainty interval.

The paper does not supply the raw page-level table here or confidence intervals for these coefficients. We therefore show reported values and their setting. We do not invent Wilson intervals for correlations: Wilson intervals describe binomial shares, not this statistic.

## What does the complete table show?

| Factor | Hotel Athens | Email marketing | Casual shoes | Reported average |
|---|---:|---:|---:|---:|
| Keyword in title tag | 0.0511 | 0.0000 | 0.2456 | 0.0989 |
| Keyword in H1/H2/H3 tag | -0.5404 | -0.2359 | 0.2107 | -0.1885 |
| Keyword density | -0.0677 | 0.3049 | -0.2364 | 0.0003 |
| Keyword in URL | -0.5890 | -0.1362 | -0.2443 | -0.3232 |
| Keyword in meta description tag | -0.0323 | -0.0691 | 0.1809 | 0.0265 |
| Alt text | 0.2270 | -0.1745 | 0.1237 | 0.0587 |
| Title length | 0.0631 | -0.3293 | 0.0000 | -0.0887 |
| URL length | 0.4373 | 0.4908 | -0.2716 | 0.2188 |
| Text to code ratio | -0.0094 | -0.2253 | 0.0619 | -0.0576 |
| Text length | -0.4582 | -0.2330 | -0.1727 | -0.2880 |
| Quantity of backlinks | -0.6771 | -0.2914 | 0.0686 | -0.3000 |
| 404 page | 0.1745 | 0.0000 | 0.2474 | 0.1406 |
| SSL certificate | -0.3928 | -0.3093 | -0.3093 | -0.3371 |
| Sitemap XML | -0.1260 | 0.2270 | 0.0000 | 0.0337 |
| Number of site pages | -0.5652 | 0.0229 | -0.1659 | -0.2361 |
| Domain age | -0.4779 | -0.1130 | -0.2535 | -0.2815 |
| Responsive layout | 0.2474 | 0.0908 | 0.0000 | 0.1127 |
| W3C validation | 0.3712 | 0.0619 | -0.3712 | 0.0206 |
| Bounce rate | -0.4942 | -0.0092 | 0.1605 | -0.1143 |
| Time on site | -0.5043 | -0.0092 | 0.3499 | -0.0545 |
| Loading time | -0.6444 | 0.4415 | 0.2623 | 0.0198 |

Source: Ziakis et al., **Table 2**, reprint PDF pp. **19 to 20**, printed pp. **10 to 11**. Each query column concerns 15 selected results. The last column transcribes the published average, including its rounding. [Download the table](https://docs.broadcastwell.com/research/data/ziakis-2019-correlations.csv).

The query columns are more informative than a list sorted by the final column. Loading time is negative for hotels and positive for the other queries. Backlink quantity is negative for hotels and email marketing but slightly positive for shoes. A near-zero average can conceal differences between queries; it does not prove a factor never matters.

Likewise, a factor shared by most selected results may have little variation left to correlate with position. That can happen even when it is useful for access, usability or eligibility. Observing only already prominent results restricts the comparison. It cannot establish how pages outside the selected range differ or why they were not included.

## Which claims are stronger than this design supports?

The table reports **−0.3000** for average backlink quantity and **0.0003** for average keyword density. These do not mean backlinks receive a negative algorithm weight or that density has been conclusively disproved as a factor in every setting. They describe this coding, these results and these queries. [Table 2].

The authors’ discussion sometimes uses stronger language, including saying that certain factors do not affect rank. That moves beyond what a small cross-sectional comparison can establish. A missing association may reflect selection, measurement, variation between topics or insufficient information. Demonstrating no meaningful causal effect would require a design and uncertainty analysis directed at that question.

The authors themselves supply a useful limit: “we cannot be sure whether they contribute.” They make that observation about factors with low correlation and high scores, noting that each keyword sample is restricted to 15 pages. That qualification belongs beside any use of the ranking-factor table. [§4.2, PDF p. 19].

Their discussion also distinguishes backlink quantity from quality. They measured quantity and state that they lacked the means to assess quality. A later summary claiming this study experimentally established the effect of high-quality backlinks would substitute a different variable for the one measured. [§4.3, PDF p. 21, printed p. 12].

## Can you turn the correlations into an implementation order?

Only with additional reasons beyond this paper. Fixing a broken page, protecting a visitor’s connection and making text readable can be justified by their direct consequences. The paper does not provide an estimate of the ranking return from each repair. Ordering a development backlog by the absolute value of these averages would imply a precision the research does not offer.

For a fictional B2B company, Cedarline Software, the decision should start with the failure being addressed. If its product documentation is unavailable over a secure connection, the repair has an observable access and security purpose. If its trial instructions are confusing, improved instructions have a usability purpose. Neither requires promising a particular search-position gain from this correlation table.

You can still evaluate whether the intended repair worked. Record the original condition, the change, the date and the outcome you can observe. Search inclusion, selected-query visibility, visits and trial completion are different outcomes. Choose the relevant one and retain its limits rather than combining them into a single unexplained success score.

## What transfers to AI answers?

The habit of identifying a measurement transfers. The coefficients do not automatically transfer. The 2018 study’s outcome is Google result position. A software vendor being named in a later AI answer is a different event, under a different set of questions and systems. A source URL being cited is different again.

An AI citation study can inspect observable page characteristics and compare the cited pages. Without suitable uncited controls or an intervention, it still cannot claim those characteristics caused citation. A common feature among cited pages may simply be common across the accessible web. Selection is the second thread connecting this old ranking study with current citation claims.

If you quote this paper, name the year, the three-query sample and the statistic. “SSL had the strongest average reported association in these samples” is supportable. “SSL is the top ranking factor” is a substantially broader claim. The complete table makes it possible to see that difference without relying on a promotional summary.

## What our own data shows

The September 2026 Absence Index contains **2,095 valid target observations** after five failed target observations are excluded from the 2,100 planned targets. Across the valid targets, **39 answers have no cited URL**, or **1.86%**, Wilson 95% interval **1.36% to 2.53%**. [Release 2026-09](https://doi.org/10.5281/zenodo.22907695); [citation answer bases](https://docs.broadcastwell.com/research/data/answer-citation-bases.csv), target/all row.

That observation concerns supplied citation lists. It is not evidence that any particular SEO factor produced or prevented citation, and an answer without a supplied citation is not necessarily an answer without sources. The base, the observable event and the missing information remain visible together. We have no controlled measurement of the ranking effect of changing SSL, backlinks or keyword density on this point.

## Sources

- Ziakis, C., Vlachopoulou, M., Kyrkoudis, T., & Karagkiozidou, M. (2019). Important factors for improving Google search rank. Future Internet, 11(2), 32. doi:10.3390/fi11020032 . [Accessible original](https://docs.broadcastwell.com/research/source-archives/ziakis-2019.pdf) Verified 30 October 2026.
- Broadcastwell. (2026). Absence Index, release 2026-09 [Data set]. Zenodo. Release JSON, answer JSONL and README. https://doi.org/10.5281/zenodo.22907695 Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *A small Google study does not give you a ranking recipe*. Broadcastwell. https://docs.broadcastwell.com/research/sources/ziakis-2019/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research16,
  author = {{Broadcastwell research team}},
  title = {A small Google study does not give you a ranking recipe},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/sources/ziakis-2019/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Ethan Brooks, management consultant.

Sources checked 30 October 2026. Independent check: pending. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the measurement chapter](https://docs.broadcastwell.com/measurement-noise/).
