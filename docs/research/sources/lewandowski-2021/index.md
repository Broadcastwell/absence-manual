---
title: 'Lewandowski, Sünkler and Yagci: detecting optimization in Google results'
description: 'A close reading of the 2021 WebSci study: its classifier, Google samples, Wikipedia denominator, useful
  findings and limits for AI-answer comparisons.'
page_class: research
research_id: 12
research_group: source
lead: Arjun Mehta
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/sources/lewandowski-2021/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://doi.org/10.1145/3447535.3462479
---

# Lewandowski, Sünkler and Yagci: detecting optimization in Google results

**Among 256,853 Google result URLs, the study identified optimization signals rather than causal benefits (Lewandowski et al., 2021, Figure 1).**

The paper's central result concerns what a searcher could encounter: optimization signals were common across the Google results the researchers could retrieve. It did not measure the extra traffic or ranking benefit a business would get from installing a plugin. [Lewandowski, Sünkler and Yagci, 2021, abstract and §§3 to 6](https://searchstudies.org/wp-content/uploads/2021/08/3447535.3462479.pdf).

That distinction matters if you are reading the paper to decide what to change on a software website. A feature can be widespread among returned pages without being sufficient to get your page returned. The study observes the selected results. It does not include a randomized comparison of otherwise identical pages with and without each feature.

The Wikipedia result makes the point unusually clear. Wikipedia was deliberately put on the classifier's list of sites treated as definitely not optimized. Yet many of its returned results appeared near the top. The classification is an operational definition chosen by the researchers, not a judgment that Wikipedia cannot be discoverable. [Table 1 and §5, original printed pp. 16 to 18].

## What was actually sampled?

The authors assembled German Google query sets with different subject matter. The Trends collection used queries gathered during March to June and November to December 2020. The coronavirus set concerned the pandemic; the radical-right set came from work with a regional media-regulation authority. These were purposeful collections, not a probability sample of everything people asked Google. [Table 2, original p. 17].

| Collection | Queries in Table 2's query column | Retrieved result URLs |
| --- | ---: | ---: |
| Google Trends | 1,563 | 207,522 |
| Radical-right topics | 80 | 12,673 |
| Coronavirus | 271 | 36,658 |
| Total | 1,914 | 256,853 |

Source: Lewandowski et al., Table 2, PDF p. 6, printed p. 17; verified 30 October 2026. The three result counts sum to the reported total. These are result records from the study, not the number of websites on the web or the number of people exposed to them.

There is a wording discrepancy within Table 2. Its coronavirus description says 482 queries, while its query-count column says 271. The latter reconciles with the paper's total of 1,914. We preserve that distinction rather than quietly repairing the original. The raw reason for the difference is not established in the paper. [Table 2 and abstract].

The authors also used a separate development dataset of 281,848 documents when evaluating the classifier. That is not another way to express the 256,853-result analysis sample. Substituting the larger development count into the results denominator would combine different stages of the research. [§3, PDF p. 4, printed p. 15].

## The classes contain judgments

The method combines recognizable tools, manually maintained website lists and observable page or site features. Its categories are more specific than the everyday phrase “does SEO.” A news host could receive a definite classification through the maintained list, while HTTPS could support a probable classification. Missing basic metadata had its own place in the rule order. [§3 and Table 1].

| Rule-based class | Examples in the published rule table | Interpretation limit |
| --- | --- | --- |
| Definitely optimized | SEO tools, known SEO customers, listed news sites, sites with ads, microdata or schema.org | Some are host-list judgments; a signal is not proof of a successful intervention. |
| Probably optimized | HTTPS, canonical links, viewport, Open Graph, listed shops, fast page loading | Common technical practices can serve purposes besides search optimization. |
| Probably not optimized | Missing title or description under the stated precedence | Absence of a tag does not establish why a page ranks where it does. |
| Definitely not optimized | The maintained negative list, represented by Wikipedia | This is a classification decision, not an experiment withholding SEO from Wikipedia. |

Source: Table 1, PDF p. 5, printed p. 16. The complete original table distinguishes the rule-based approach from the features retained in the decision tree. Microdata/schema.org appears in the rule table but has a dash in the decision-tree-use column. It is inaccurate to say every listed rule feature was retained by that fitted tree.

There is another small but consequential detail. The speed feature is a website loading time below three seconds, not time to first byte. Replacing one with the other in a later study changes the measurement. A comparison can still be useful, but it needs to disclose the substitution rather than claim to have reproduced the original classifier. [Table 1].

## The headline split is a classified share

Figure 1 reports the following rounded overall distribution. The last row combines the negative categories in the figure. It should not be retold as a direct measurement of deliberate optimization spending or of the share of search success caused by SEO.

| Figure 1 category | Reported overall share | Denominator and precision |
| --- | ---: | --- |
| Definitely optimized | 59.0% | 256,853 result URLs; published rounded share |
| Probably optimized | 29.0% | Same result base; published rounded share |
| Negative categories together | 12.0% | Same result base; published rounded share |

Source: Figure 1, PDF p. 6, printed p. 17, visually checked against the original. The paper does not provide exact cell counts for these rounded overall percentages. We do not manufacture numerators or Wilson intervals by multiplying rounded percentages by the total. Those would look more precise than the available source.

The nearby prose also gives 48.4%, 27% and 31% for news content in the Trends, radical-right and coronavirus datasets. These are news-content shares. They are not the probably-optimized values from Figure 1, so they do not establish a prose-versus-figure contradiction about that class. [§5, paragraph beneath Figure 1].

## Wikipedia's denominator travels with the number

The original reports 1,974 Wikipedia results. Of those Wikipedia results, 27% were at position one and 79.3% were within the first ten positions. It does not say Wikipedia held 27% of all first positions. [§5, PDF p. 7, printed p. 18].

You can check the difference with a question: among which records was the percentage calculated? Here the answer is Wikipedia's own returned results. The rounded percentages do not reveal exact integer counts at each position, so we retain the reported precision and do not add an invented interval.

We also withhold the prose's overall 0.7% Wikipedia share as a clean, reconciled statistic. Dividing the printed 1,974 by the overall 256,853 gives about 0.769%, which rounds to 0.8% at one decimal place. The underlying data might explain the mismatch, but the article alone does not. Quoting 0.7% without this qualification would hide a real unresolved arithmetic discrepancy. [§5 and Figure 1].

## High prevalence persists beyond the first positions

The positional analysis runs through position 130 because the number of available results falls sharply farther down. The authors did not find vast differences in optimization prevalence across positions. They nevertheless describe somewhat higher optimization probability near the top, with topic-specific differences. A summary saying the curves are perfectly flat would overstate their conclusion. [Figures 2 to 4 and §§5 to 6].

The changing number of available records also matters. Back positions are not simply the same complete query sample observed at a different rank. You cannot treat a thin tail of available results as though every query contributed every position. Nor can you infer the composition of results Google did not expose to the collection. [Figure 2 and §5].

The paper's most useful limiting phrase is “not based on a representative sample of queries.” It also limits the analysis to Google and excludes off-site factors such as backlinks. Those are substantive limits on generalization, even though the result sample is large. [§6, original p. 18].

## What carries over to AI-answer research?

A B2B team can borrow the discipline of defining observable signals before counting them. It can also publish failures separately and explain which rules classify a whole host rather than an individual page. Those are research-design choices that make a later comparison inspectable.

The outcome itself changes. A Google result position is not a citation occurrence in an AI answer. A returned citation does not prove that its page supplied the disputed sentence, and a vendor can be named while a third-party page is cited. Our comparison therefore needs separate units for cited URLs, answer occurrences and vendor-answer pairs. The paper supplies no conversion between them.

Even a future finding that most cited pages carry technical optimization signals would leave the intervention question open. The uncited eligible pages, their content and their retrieval opportunities would also matter. We do not turn the presence of a tag among selected pages into a promise that adding that tag will make an engine cite your company.

## What our own data shows

The September 2026 release contains 2,095 valid target answers after five target exclusions, with controls kept separate. Its explicit citation arrays contain 18,893 target citation occurrences in our registered Study 2 reanalysis. Those are answer-linked URL entries, not Google ranked-result records. [Broadcastwell, release 2026-09, README and answer JSONL](https://doi.org/10.5281/zenodo.22907695); [Study 2 registration](https://doi.org/10.17605/OSF.IO/VCZKT). This review uses Study 2’s citation counts for its own-data comparison. Study 1’s separate page-signal analysis is not reported as a result on this review page.

## Sources

- Lewandowski, D., Sünkler, S., & Yagci, N. (2021). The influence of search engine optimization on Google's results. In WebSci '21 (pp. 12 to 20). ACM. doi:10.1145/3447535.3462479 . [Accessible original](https://searchstudies.org/wp-content/uploads/2021/08/3447535.3462479.pdf) Verified 30 October 2026.
- Broadcastwell. (2026). Absence Index, release 2026-09 [Data set]. Zenodo. Release JSON, answer JSONL and README. https://doi.org/10.5281/zenodo.22907695 Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *Lewandowski, Sünkler and Yagci: detecting optimization in Google results*. Broadcastwell. https://docs.broadcastwell.com/research/sources/lewandowski-2021/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research12,
  author = {{Broadcastwell research team}},
  title = {Lewandowski, Sünkler and Yagci: detecting optimization in Google results},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/sources/lewandowski-2021/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Arjun Mehta, management consultant.

Sources checked 30 October 2026. Independent check: pending. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the measurement chapter](https://docs.broadcastwell.com/measurement-noise/).
