---
title: Review-platform citations do not establish objective reviews
description: A checked table of B2B review-platform hosts beside two restaurant-review chapters. Review selection,
  citation and factual reliability require separate evidence.
page_class: research
research_id: 8
research_group: insight
lead: Priya Nair
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/insights/review-platforms-as-the-objective-source/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://doi.org/10.5281/zenodo.22907695
---

# Review-platform citations do not establish objective reviews

**G2 appears in 580/18,893 target citation entries: 3.1%, Wilson 95% interval 2.8% to 3.3% (Broadcastwell, 2026, Study 2).**

The exact host **g2.com** appears in **580 of 18,893 target citation entries**, **3.1%**, descriptive **95% Wilson interval 2.8% to 3.3%**, in the September software answers. The record establishes that references appeared. It does not establish that the underlying reviews were objective or that the engine judged them so. [Broadcastwell, Study 2, review-platform occurrences; release 2026-09](https://doi.org/10.5281/zenodo.22907695).

A useful warning comes from a restaurant-review project in Mexico City. Its researchers selected rating-platform material over social-media material and called the former “more objective.” That is the authors’ characterization of their selected corpus. It is not an independently validated property of every review site, and it should not be used as the voice of all AI answer systems. [Maldonado Castillo et al., 2024, chapter 90, §2, printed p. 841](https://doi.org/10.1007/978-3-031-51038-0_90).

## Two related chapters need to stay separate

The proceedings contain both a review-centralization chapter and a review-generation chapter. They share a research setting and several platform counts, but they do not make identical inclusion decisions. Combining their methods would create a project that neither chapter actually reports.

| Primary chapter | Reported review material | What the chapter permits us to say |
|---|---|---|
| Chapter 90, Centralization of Information to Understand the Consumer Within the Restaurant Sector | Yelp 7,160; Google Reviews 1,415; TripAdvisor 425; Instagram 1,029; Twitter 200 | Table 1 inventories retrieved material. The discussion excludes social-media reviews from the analysis because the authors considered them insufficiently informative or biased. |
| Chapter 96, Automatic Generation of Restaurant Reviews Using Natural Language Processing | Yelp 7,160; Google Reviews 1,415; TripAdvisor 425; Instagram 1,000 | The later system reports a 10,000-review labelled corpus and generates summaries from extracted aspects and opinions. It explicitly includes Instagram material in its reported corpus. |

Sources: [chapter 90, Table 1 and §2, printed pp. 840 to 841; PDF pp. 809 to 810](https://doi.org/10.1007/978-3-031-51038-0_90); [chapter 96, §§2.3 and 3, printed pp. 896 to 897; PDF pp. 860 to 861](https://doi.org/10.1007/978-3-031-51038-0_96). Collection is described as August 2022 to June 2023. These are corpus counts, not shares of all restaurant opinions; no population interval is claimed.

Chapter 90’s judgment about objectivity is qualitative. The authors discuss predominantly negative Twitter material and predominantly positive Instagram material, then prefer the rating platforms for their stated purpose. The chapter does not report a randomized test showing that a platform label makes a review accurate. A balanced-looking set of opinions could still omit relevant people or contain unreliable claims.

Chapter 96 describes a system that extracts aspects, opinions and sentiments before generating a composite review. It is a designed restaurant application. It is not an audit of ChatGPT, Claude, Perplexity or Google’s consumer answers. Explaining its operation cannot establish which sources those services call trustworthy.

## What appears in the B2B citation record?

| Exact host | Entries / all target entries | Share and descriptive 95% Wilson interval |
|---|---:|---|
| g2.com | 580 / 18893 | 3.1% (2.8% to 3.3%) |
| capterra.com | 478 / 18893 | 2.5% (2.3% to 2.8%) |
| getapp.com | 89 / 18893 | 0.5% (0.4% to 0.6%) |
| trustradius.com | 31 / 18893 | 0.2% (0.1% to 0.2%) |
| softwareadvice.com | 310 / 18893 | 1.6% (1.5% to 1.8%) |
| gartner.com | 73 / 18893 | 0.4% (0.3% to 0.5%) |

Source: [September citation arrays](https://doi.org/10.5281/zenodo.22907695); [host occurrence CSV](../../data/review-platform-occurrences.csv), primary variant, target scope, all engines and categories. Each row’s denominator is 18,893 URL occurrences, not 2,095 answers. Counts match the exact normalized hostname, so learn.g2.com is not included in g2.com. Gartner is shown as a separately requested host; its mixed research, advisory and review functions mean it is not a pure review-platform measure.

An answer can cite several of these hosts or repeat a host alongside a vendor. Adding the rows produces a selected-host occurrence count, not a percentage of answers that used reviews. The table also excludes other review services. It should not be labelled the total review-platform share, which depends on the broader classification and its uncertainty.

## Engine counts retain their own bases

| Engine | Citation-entry base | G2 | Capterra | GetApp | TrustRadius | Software Advice |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 1993 | 2 | 3 | 0 | 0 | 0 |
| Claude | 3975 | 96 | 151 | 30 | 1 | 64 |
| Google AI Mode | 1577 | 54 | 23 | 0 | 2 | 26 |
| Google AI Overviews | 3050 | 84 | 51 | 0 | 4 | 19 |
| Perplexity | 8298 | 344 | 250 | 59 | 24 | 201 |


The cells above are counts, with the citation-entry denominator at the left. The [complete downloadable table](../../data/review-platform-occurrences.csv) supplies each cell’s percentage and descriptive 95% Wilson interval, including zero-count intervals, as well as control, combined and category strata. Small cells and shared questions make these descriptions of the observed record, not a ranking of the services’ long-run preferences.

The count matrix helps you avoid a misleading comparison. An engine with many references can produce a larger host count without a larger share. Citation frequency also does not show whether a review influenced a particular sentence. The saved answer and the linked source need to be read together before claiming substantive use.

## A host’s purpose can change the class without changing the count

The registered study freezes a primary host-purpose table before class aggregation. A later audit found that several sites combine directories and reviews, while editorial subdomains should not automatically inherit a review-platform label. Both the original table and the dated corrections remain available.

This is why the exact-host count above is useful beside the class analysis. A reader can disagree about whether a multifunctional publisher belongs in review platform or directory without changing how often its hostname appeared. The uncertainty belongs in the classification, rather than being hidden behind an authoritative-looking combined percentage.

We also report a sensitivity that places ambiguous hosts in other. That deliberately sacrifices detail. It makes the unambiguous remainder easier to interpret, while acknowledging that some publishers really do serve several roles. There is no single natural label that removes the need to explain those choices.

## What would support a stronger objectivity claim?

You would need a defined outcome: accuracy of product facts, verified experience, completeness of criticism, resistance to manipulation or agreement with an external reference. Then you would need a sampling plan and a comparison that could fail. A platform’s own moderation description can explain its policy, but it cannot independently establish the policy’s success for every review.

The restaurant project shows the same distinction in miniature. Selecting sources that appear suited to a task is part of research design. Demonstrating that they are less biased requires evidence beyond the selection rationale. A generated summary does not settle that question merely by combining many reviews.

For your own software record, correct factual inaccuracies through a platform’s documented process and preserve the evidence for the correction. Do not infer that a paid profile, a large review count or a conspicuous badge guarantees an AI citation. Nothing in this table tests that intervention.

The remaining question is not whether review sites deserve one universal trust label. It is whether a particular source supports the specific claim the buyer is reading. That answer can differ within one platform, one category and even one cited page.

## What our own data shows

The frozen review-platform class contains **1,663/18,893 target citation occurrences, 8.8% (Wilson 95% interval 8.4% to 9.2%)**. The later host audit is reported separately. Our [September release](https://doi.org/10.5281/zenodo.22907695) contains the saved answers and explicit references underlying these counts. [OSF registration](https://doi.org/10.17605/OSF.IO/VCZKT) records the study question and analysis plan. The [CSV](../../data/review-platform-occurrences.csv) includes all engine/category scopes with bases and intervals; the [study](../../studies/who-ai-engines-cite/) discloses classification corrections and timing. We have no measurement here of whether a review was truthful, whether an engine considered it objective or whether a vendor’s listing caused inclusion.

## Sources

- Broadcastwell. (2026). Absence Index, release 2026-09 [Data set]. Zenodo. Release JSON, answer JSONL and README. https://doi.org/10.5281/zenodo.22907695 Verified 30 October 2026.
- Broadcastwell. (2026). Who do AI engines cite for B2B software questions? [Registration]. OSF. Registered 30 October 2026, 01:32:03 UTC. https://doi.org/10.17605/OSF.IO/VCZKT Verified 30 October 2026.
- Maldonado Castillo, I., Martínez Ortiz, F. Y., & Guzmán Flores, J. P. (2024). Centralization of information to understand the consumer within the restaurant sector. In Strategic innovative marketing and tourism (pp. 837 to 843). Table 1 and §2. https://doi.org/10.1007/978-3-031-51038-0_90 Verified 30 October 2026.
- Maldonado Castillo, I., Aguirre Miranda, I. A., & Olvera Mendoza, A. (2024). Automatic generation of restaurant reviews using natural language processing. In Strategic innovative marketing and tourism (pp. 893 to 901). §§2.3 and 3. https://doi.org/10.1007/978-3-031-51038-0_96 Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *Review-platform citations do not establish objective reviews*. Broadcastwell. https://docs.broadcastwell.com/research/insights/review-platforms-as-the-objective-source/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research8,
  author = {{Broadcastwell research team}},
  title = {Review-platform citations do not establish objective reviews},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/insights/review-platforms-as-the-objective-source/},
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
