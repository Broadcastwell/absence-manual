---
title: Quotable numbers, with their original boundaries
description: Source locations, counts, bases and limits for search and AI-answer figures that can be quoted without
  changing what was measured.
page_class: research
research_id: 46
research_group: evidence
lead: Vikram Patel
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/evidence/quotable-numbers/
sources_verified: true
schema_type: Article
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://doi.org/10.1145/3447535.3462479
research_dataset:
  name: Quotable search and AI-answer observations
  description: Source-bounded external findings and descriptive reanalyses of Absence Index release 2026-09. The
    linked CSVs specify their units, counts and bases.
  distribution:
  - name: Repeat disagreement
    contentUrl: https://docs.broadcastwell.com/research/data/repeat-disagreement.csv
    encodingFormat: text/csv
  - name: Vendor presence
    contentUrl: https://docs.broadcastwell.com/research/data/vendor-presence.csv
    encodingFormat: text/csv
---

# Quotable numbers, with their original boundaries

**Keep the population, date and metric in the same sentence as the number.**

The usable number is often less sweeping than the familiar headline. A source may establish a historical answer length, an experimental visibility score or a dated vendor-naming rate. Those are useful observations when their labels remain intact.

This ledger provides wording that can travel with a figure. It does not upgrade a paper's design or convert a reported association into an intervention effect. You can follow the source location to the original and use the linked data tables to inspect our descriptive reanalyses.

Rovira and colleagues called their proposed explanation for a change in scholarly search ordering “only an inference.” That short qualification belongs beside the result, not on a page the reader is unlikely to open. [Rovira et al., 2019, §4](https://doi.org/10.3390/fi11090202).

## External findings: use the complete wording

| Finding | Wording suitable for quotation | Location and limit |
|---|---|---|
| Observable optimization signals in a Google result sample | Lewandowski et al.'s 2021 paper classified 59.0% of 256,853 Google result URLs as definitely optimized, 29.0% as probably optimized and 12.0% in its combined negative group. | Figure 1, PDF p. 6, printed p. 17. Selected German-language query sample, not all Google results; classifications do not identify a causal optimization effect. Rounded shares do not supply recoverable integer numerators or count-based intervals. |
| Wikipedia result positions | Among the paper's 1,974 Wikipedia results, 27% appeared at position 1 and 79.3% in the top ten. | Lewandowski et al., §4.2, PDF p. 7, printed p. 18. The denominator is Wikipedia results. Do not describe this as Wikipedia's share of all first positions. Rounded shares; exact position counts and intervals are not reconstructed. |
| Scholarly relevance ordering | Rovira et al. report Google Scholar median-rank correlations of 0.968 and 0.721 for unrestricted one-term and two-term searches, and 0.990 and 0.994 with title restriction. | 2019, Table 2, reprint PDF p. 56. Correlation across position-wise median summaries from selected scholarly searches, not AI-answer citation probability. Coefficients are not proportions. |
| A temporary observed Web of Science ordering | The study reports a citation-like Web of Science ordering during 20 to 25 May 2019; Table 2 gives 0.907 for that collection and −0.075 for the other collection. | Rovira et al., Table 2 and §4. Operator testing is the authors' inference. The historical observation does not establish the present system's behavior. |
| Historical voice-answer length | Backlinko's 2018 study of 10,000 Google Home results reported an average spoken-answer length of 29 words. | Original study, answer-length section. Vendor study, historical system and selected sample. This is answer length, not query length or a universal content target; distribution-level uncertainty is unavailable. |
| GEO experiment | Aggarwal et al.'s 2024 Table 1 reports a best improvement of 41% in position-adjusted word-count visibility and 28% in subjective impression under its experimental conditions. | Author manuscript v3, Table 1. Relative improvement in specified metrics; neither number is a business's probability of being cited, traffic uplift or conversion gain. No binomial base applies to these metric improvements. |

The last row corrects the metric rather than validating a universal marketing promise. The abstract's “up to 40%” and the table's 41% summary have different presentation precision; retain the exact table location if using the latter. Do not combine them into an invented probability.

## September repeat disagreement

The following rates count complete vendor-question-engine groups. A group is mixed if the vendor was named in some, but not all, of its three valid target repeats. All intervals are descriptive 95% Wilson intervals; dependent observations prevent treating them as independent population trials.

| Engine | Mixed / eligible complete groups | Rate and interval |
|---|---:|---|
| ChatGPT | 159 / 2,860 | 5.6% (4.8% to 6.5%) |
| Claude | 253 / 2,860 | 8.8% (7.9% to 9.9%) |
| Perplexity | 200 / 2,860 | 7.0% (6.1% to 8.0%) |
| Google AI Overviews | 302 / 2,752 | 11.0% (9.9% to 12.2%) |
| Google AI Mode | 345 / 2,860 | 12.1% (10.9% to 13.3%) |
| Combined | 1,259 / 14,192 | 8.9% (8.4% to 9.4%) |

Primary: [September release DOI 10.5281/zenodo.22907695](https://doi.org/10.5281/zenodo.22907695), engine_presence counts. Reanalysis dated 30 October 2026. [CSV with category breakdowns](../../data/repeat-disagreement.csv). The 108 incomplete Google AI Overviews groups are omitted from this complete-repeat measure. Uniform absence counts as agreement, so the statistic is not an engine-quality score.

## Named examples from the vendor record

| Observation in release 2026-09 | Count / valid target answers | Percentage and descriptive 95% Wilson interval |
|---|---:|---|
| Microsoft Dynamics 365 named for CRM | 36 / 150 | 24.0% (17.9% to 31.4%) |
| Oracle OPERA Cloud named for hotel property management | 25 / 149 | 16.8% (11.6% to 23.6%) |
| GE HealthCare named for radiology and medical imaging | 24 / 150 | 16.0% (11.0% to 22.7%) |

Source: the same deposit, relevant category's vendor mention_rate fields. [Full checked-vendor CSV](../../data/vendor-presence.csv). Naming can include multiple vendors per answer. These figures describe the fixed questions and engines; they measure neither product quality nor commercial market share.

## The naming and own-source distinction

The September publisher aggregates contain **8,085 named vendor-answer pairs**, of which **2,608** carry a qualifying own-domain citation: **32.3%**, descriptive **95% Wilson interval 31.2% to 33.3%**. A pair combines one checked vendor and one eligible answer. Multiple pairs can arise from the same answer. [Derived counts and category table](../../data/vendor-naming-citation.csv).

These are summaries of the deposited publisher aggregates. The qualifying-name dictionary is not included in that deposit, so this table is not an independent reproduction of the individual citation verdicts. It does not mean that every remaining pair lacked a source of any kind; an answer can cite a third party.

## Choosing a number for your own page

Use the row whose outcome matches your sentence. A naming figure cannot support a statement about source ownership. A historical search-position figure cannot establish the behavior of every AI engine. A study's proposed mechanism should remain labelled as an explanation or inference unless the design tested it directly.

If you shorten a sentence, retain the unit before removing a qualification. The base often matters more than an extra decimal place. Our [unverified-number ledger](../unverified-numbers/) records examples where a plausible-looking number changed meaning in retelling, including objections we withdrew after reading the original.

The unresolved question is which future observations will remain comparable. The dated tables above are usable now; their presence here does not promise that a later release will produce the same counts.

## What our own data shows

[Download the complete repeat table](../../data/repeat-disagreement.csv), [vendor-presence table](../../data/vendor-presence.csv) and [naming/citation aggregate table](../../data/vendor-naming-citation.csv). All derive from [release 2026-09](https://doi.org/10.5281/zenodo.22907695). Counts and units appear above; Wilson intervals describe observed proportions without an independence claim. This ledger contains no Study 1 result.

## Sources

- Lewandowski, D., Sunkler, S., & Yagci, N. (2021). The influence of search engine optimization on Google's results. In WebSci '21 (pp. 12 to 20). ACM. https://doi.org/10.1145/3447535.3462479 Verified 30 October 2026.
- Rovira, C., Codina, L., Guerrero-Solé, F., & Lopezosa, C. (2019). Ranking by relevance and citation counts, a comparative study: Google Scholar, Microsoft Academic, WoS and Scopus. Future Internet, 11(9), 202. https://doi.org/10.3390/fi11090202 Verified 30 October 2026.
- Dean, B. (2018, February 28). We analyzed 10,000 Google Home results. Here's what we learned about voice search SEO. Backlinko. https://backlinko.com/voice-search-seo-study Verified 30 October 2026.
- Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A., Narasimhan, K., & Deshpande, A. (2024). GEO: Generative engine optimization. KDD 2024. https://doi.org/10.1145/3637528.3671900 . Author manuscript v3: https://arxiv.org/html/2311.09735v3 Verified 30 October 2026.
- Broadcastwell. (2026). Absence Index, release 2026-09 [Data set]. Zenodo. Release JSON, answer JSONL and README. https://doi.org/10.5281/zenodo.22907695 Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *Quotable numbers, with their original boundaries*. Broadcastwell. https://docs.broadcastwell.com/research/evidence/quotable-numbers/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research46,
  author = {{Broadcastwell research team}},
  title = {Quotable numbers, with their original boundaries},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/evidence/quotable-numbers/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Vikram Patel, AI architect and specialist.

Sources checked 30 October 2026. This page has not been peer reviewed.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the measurement chapter](https://docs.broadcastwell.com/measurement-noise/).
