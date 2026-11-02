---
title: A citation is an observed source choice, not a trust score
description: September citation hosts, source-class uncertainty and concentration across five engines. A citation
  records a source selection, without revealing an engine’s judgment.
page_class: research
research_id: 7
research_group: insight
lead: Priya Nair
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/insights/who-the-engines-trust/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://doi.org/10.5281/zenodo.22907695
---

# A citation is an observed source choice, not a trust score

**Ten hosts supplied 3,192/18,893 target citation entries: 16.9%, Wilson 95% interval 16.4% to 17.4% (Broadcastwell, 2026, Study 2).**

The leading ten hosts accounted for **3,192 of 18,893 target citation entries** in our September B2B-software answers: **16.9%**, descriptive **95% Wilson interval 16.4% to 17.4%**. Calling those hosts the sources the engines “trust” would add a mental state that the record does not measure. [Broadcastwell, Study 2, target concentration table; release 2026-09](https://doi.org/10.5281/zenodo.22907695).

The distinction changes the question you can answer. We can identify which hosts appeared in the saved citation arrays, how often they appeared and how concentrated those entries were. We cannot see every source considered, reconstruct the engine’s internal reasoning or establish that a cited page was correct. A displayed reference is evidence of a source choice in an answer, with its own opportunity for error.

## What exactly is being counted?

Study 2 uses the explicit citation arrays in the published September release. A citation entry is one recorded URL occurrence attached to an eligible answer. The primary denominator includes every such entry, including entries we cannot confidently classify. It does not turn an empty answer into a citation or an inaccessible publisher into a known source type.

There are **2,095 valid target answers**, containing **18,893 entries**. Separately, **150 control answers** contain **1,297 entries**. We keep those scopes separate because the control questions ask something different. The target sample includes **39 answers with empty citation arrays**, **1.9%**, descriptive **95% Wilson interval 1.4% to 2.5%**. Empty arrays remain in the answer-level base and contribute no URL to the citation-entry base. [September answer arrays; Study 2 answer-bases CSV, target and control rows].

Several links in one answer can point to the same publisher. Several answers can reuse one link. The table therefore describes citation occurrences, not unique readers, independent endorsements, unique documents or attributable visits. Its uncertainty intervals summarize observed proportions; shared questions and repeated answers prevent interpreting them as independent trials drawn from all buyer conversations.

## The source classes include a large unresolved remainder

Before aggregating class shares, we froze a host-purpose classification table. The table uses primary publisher descriptions where available and places unresolved or insufficiently specific hosts in other. A vendor class covers the checked vendor domains and documented aliases in the published matching dictionary; it is not a complete directory of every software supplier on the web.

| Frozen primary class | Entries / 18,893 target entries | Share and descriptive 95% Wilson interval |
|---|---:|---|
| Checked vendor site | 5,766 / 18,893 | 30.5% (29.9% to 31.2%) |
| Review platform | 1,663 / 18,893 | 8.8% (8.4% to 9.2%) |
| Wikipedia or sister project | 3 / 18,893 | 0.016% (0.005% to 0.047%) |
| Other, including unresolved purpose | 8,395 / 18,893 | 44.4% (43.7% to 45.1%) |

Source: [September version DOI](https://doi.org/10.5281/zenodo.22907695); [full class table](../../data/citation-class-shares.csv), all-array-entries variant, target scope, all engines and categories. The omitted classes remain in the denominator and in the download. These selected rows do not sum to the whole.

The large other group limits the interpretation. It includes blocked publishers, sites whose accessible descriptions do not establish the designated purpose and multifunctional sites that are difficult to place. Some are probably vendors outside the checked dictionary. The gap cuts both ways: calling every other entry a nonvendor would overstate the evidence, but so would calling the verified class a complete inventory of software vendors. Neither inference is supported.

After the first aggregation, a publisher-purpose audit identified five host-role corrections. We retained the frozen primary result and published a separately dated sensitivity table. Its review-platform result is **1,706/18,893**, **9.0%**, descriptive **95% Wilson interval 8.6% to 9.4%**. This correction followed aggregation. The correction log and ambiguity recoding accompany the full study. [Post-audit class table](../../data/citation-class-shares-post-audit.csv).

## Concentration depends on the engine’s citation base

| Engine | Top-ten host entries / all target citation entries | Share and descriptive 95% Wilson interval |
|---|---:|---|
| ChatGPT | 271 / 1,993 | 13.6% (12.2% to 15.2%) |
| Claude | 742 / 3,975 | 18.7% (17.5% to 19.9%) |
| Google AI Mode | 435 / 1,577 | 27.6% (25.4% to 29.8%) |
| Google AI Overviews | 822 / 3,050 | 27.0% (25.4% to 28.6%) |
| Perplexity | 1,532 / 8,298 | 18.5% (17.6% to 19.3%) |

Source: [Study 2 concentration CSV](../../data/citation-concentration.csv), target scope, all categories, primary occurrence variant. Each engine’s hosts are ranked separately, with alphabetical hostname ordering for ties. “Top ten” does not mean the same ten publishers across engines.

The overall table weights citation entries, so an engine that supplies more references contributes more to the combined result. It is not the average of five engine percentages. A different question, such as how often an answer cites any review platform, would require an answer-level denominator and would produce a different statistic.

Exact hostnames are the unit for concentration after lowercasing and removing a leading www. Subdomains remain distinct. That preserves what appeared in the saved record, but it can split one organization across several hosts. An organization-level consolidation would be a different analysis with additional ownership decisions. The present result should not be labelled a market-concentration index of corporate owners.

## Wikipedia’s older result answers a different question

Lewandowski, Sünkler and Yagci found **1,974 Wikipedia results** in their Google result sample. **27% of those Wikipedia results** were at position one and **79.3%** in the top ten. The denominator is Wikipedia’s own results. It is not the set of every first-position Google result. [Lewandowski et al., 2021, §5, PDF p. 7, printed p. 18](https://searchstudies.org/wp-content/uploads/2021/08/3447535.3462479.pdf).

That historical comparison concerns Google result positions for selected German-language queries. Our table concerns saved reference arrays for B2B-software answers. The small Wikipedia count in our sample cannot establish a loss of general authority, a change in Google’s behavior or a reduced role in model training. Those questions require other populations and measurements.

There is a useful older parallel in Goel and colleagues’ title, “ordinary people with extraordinary tastes.” Their long-tail research studies how popularity and diverse individual behavior coexist. But the familiar retelling about clicks should not be imported into our citation table: the relevant browsing concentration discussion measures pageviews. [Goel et al., 2010, §3.2](https://sites.santafe.edu/~aaronc/courses/7000/readings/Goel_Broder_Gabrilovich_Pang_10_AnatomyOfTheLongTail_OrdinaryPeopleWithExtraordinaryTastes.pdf). A pageview, a search click and a reference inside an answer are different events.

## What can you do with a citation map?

Start with the sources attached to the questions that matter to your buyers. Read the cited page, identify what claim it supports and check whether the answer represents it accurately. A recurring review site may warrant attention because it carries relevant evidence about your category. Its recurrence alone does not justify buying exposure or promising that a listing will cause inclusion.

The map is also useful for finding missing documentation. A vendor may be named without a qualifying own-domain reference. A third-party comparison may supply the facts instead. Neither observation tells you whether an engine ignored the vendor’s site, retrieved it without citing it or never encountered it.

The trade-off is practical. A conservative classification leaves a conspicuous unknown group, making the headline less tidy. It also leaves room for a reader to correct the classification without changing the underlying URL count. The open question is how much of that remainder a more complete, independently audited publisher inventory would resolve.

## What our own data shows

The target archive’s leading ten hosts supply **3,192/18,893 citation occurrences, 16.9% (Wilson 95% interval 16.4% to 17.4%)**. This measures concentration under the registered host rules. The tables above are a descriptive reanalysis of [Absence Index release 2026-09](https://doi.org/10.5281/zenodo.22907695), under [OSF registration vczkt](https://doi.org/10.17605/OSF.IO/VCZKT). Download the [host-purpose record](../../data/host-classes.csv), [class shares](../../data/citation-class-shares.csv), [post-audit sensitivity](../../data/citation-class-shares-post-audit.csv) and [concentration tables](../../data/citation-concentration.csv). The class corrections, timing deviation and complete method are stated on the [registered study page](../../studies/who-ai-engines-cite/). No table measures trust, truth, traffic or a causal effect of publishing.

## Sources

- Broadcastwell. (2026). Absence Index, release 2026-09 [Data set]. Zenodo. Release JSON, answer JSONL and README. https://doi.org/10.5281/zenodo.22907695 Verified 30 October 2026.
- Broadcastwell. (2026). Who do AI engines cite for B2B software questions? [Registration]. OSF. Registered 30 October 2026, 01:32:03 UTC. https://doi.org/10.17605/OSF.IO/VCZKT Verified 30 October 2026.
- Lewandowski, D., Sünkler, S., & Yagci, N. (2021). The influence of search engine optimization on Google's results: A multi-dimensional approach for detecting SEO. In WebSci '21 (pp. 12 to 20). ACM. doi:10.1145/3447535.3462479 . [Accessible original](https://searchstudies.org/wp-content/uploads/2021/08/3447535.3462479.pdf) Verified 30 October 2026.
- Goel, S., Broder, A., Gabrilovich, E., & Pang, B. (2010). Anatomy of the long tail: Ordinary people with extraordinary tastes. WSDM, pp. 201 to 210. §3.2, pageview distribution. https://doi.org/10.1145/1718487.1718513 . Author copy: https://sites.santafe.edu/~aaronc/courses/7000/readings/Goel_Broder_Gabrilovich_Pang_10_AnatomyOfTheLongTail_OrdinaryPeopleWithExtraordinaryTastes.pdf Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *A citation is an observed source choice, not a trust score*. Broadcastwell. https://docs.broadcastwell.com/research/insights/who-the-engines-trust/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research7,
  author = {{Broadcastwell research team}},
  title = {A citation is an observed source choice, not a trust score},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/insights/who-the-engines-trust/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Priya Nair, management consultant.

Sources checked 30 October 2026. Independent check: 30 October 2026, Broadcastwell verification desk. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the measurement chapter](https://docs.broadcastwell.com/measurement-noise/).
