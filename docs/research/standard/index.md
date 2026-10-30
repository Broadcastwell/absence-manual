---
title: The Broadcastwell evidence standard
description: How we distinguish measurements, reported associations, historical advice and unsupported claims in
  search and AI visibility research.
page_class: research
research_id: 24
research_group: evidence
lead: Vikram Patel
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/standard/
sources_verified: true
schema_type: Article
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
---

# The Broadcastwell evidence standard

**A figure is ready to quote only when its source, unit, denominator and limits can travel with it.**

A precise number can still answer the wrong question. A survey about perceived search performance cannot establish a change in observed search positions, however carefully its statistical model is reported.

This standard governs the claims in this research section. It asks what a source permits us to say, rather than whether we agree with its conclusion. You should be able to take a sentence from a page, follow its reference and find the same quantity in the original. The qualifying words belong to the claim. They are not optional material for a footnote.

Google's current content guidance asks, “Does the content provide original information, reporting, research, or analysis?” That is a useful editorial question. It is not an experimental result about the ranking benefit of publishing research. Guidance and measurement enter the ledger in different columns. [Google Search Central, content and quality questions](https://developers.google.com/search/docs/fundamentals/creating-helpful-content).

## Start with the object being counted

An answer, a vendor named in an answer and a link attached to that answer are different objects. An answer may name several vendors and cite several pages. A host can appear repeatedly. Counting those occurrences gives a different quantity from counting answers that cite the host at least once.

Before accepting a rate, write its numerator and denominator in ordinary language. “Among captured target answers” is a narrower population than “among all buyers.” “Among named vendor-answer pairs” differs from “among all checked vendor-answer pairs.” If the distinction changes the interpretation, it belongs beside the percentage.

The same discipline applies to an external paper. Lewandowski and colleagues report where Wikipedia's own results appeared. Their first-position percentage does not describe Wikipedia's share of every first-position slot. Reversing the conditioning group produces a different statement, even when the printed percentage remains unchanged. [Lewandowski et al., 2021, §4.2](https://doi.org/10.1145/3447535.3462479).

## The grades and the permissions they carry

| Grade | What earns it | What we permit on a page |
|---|---|---|
| A | Strong empirical design for the particular question, transparent methods, an appropriate sample and a checkable scholarly record | Report the measured result with its original scope and location. A large observational sample still does not establish causation. |
| B | Useful evidence with a material boundary, or an authoritative primary statement of policy or historical practice | Put the boundary beside the claim. A search operator's guide establishes what the operator said, rather than the size of an effect. |
| C | Untraceable inputs, serious inconsistencies, unsupported inference, a small exploratory exercise or a conceptual account presented as evidence | Discuss the defect or vocabulary. Do not turn its headline figures into advice or performance claims. |
| D | Material outside the question being answered | Leave it out of the substantive argument. Identify a relevant chapter separately if a large collection contains one. |

A grade attaches to a use. A practitioner interview may be valuable historical testimony and weak quantitative evidence. A collection can contain an excellent empirical article beside an exploratory one. We grade those articles separately. A publisher's reputation is part of the context, never a substitute for reading the design.

## Read five parts of the evidence

**Sample.** Who or what entered the study? Was selection random, systematic, convenient or unexplained? What geography, language, question set and collection period were covered? A study of university websites can inform a question about university websites without representing software procurement.

**Measurement.** What was observed directly? A ranking, a questionnaire response, a crawler request and an evaluator's judgment have different error sources. An indicator bearing a familiar label does not automatically measure the thing a marketer wants. A composite website score is not a search position.

**Comparison.** What makes the result interpretable? A correlation describes co-variation. A before-and-after comparison needs a stable definition and comparable conditions. A causal claim needs a design that can separate the proposed cause from plausible alternatives. We do not infer that design from confident verbs in an abstract.

**Access.** Can a reader inspect the observations or at least the exact table? A DOI identifies a record; it does not certify a method. An accessible repository improves auditability, but missing labels or an absent scoring dictionary can still prevent full reproduction. We state the remaining gap.

**Consistency.** Do the method, tables, figures and discussion agree? If they differ, we preserve the disagreement and identify the version and locations. We do not average conflicting numbers, silently choose the convenient one or manufacture a count from a rounded percentage.

## Counts first, uncertainty next

For our derived proportions we show the observed count and eligible base, followed by the percentage and a descriptive Wilson interval at the stated confidence level. The interval summarizes binomial variation around that proportion. Repeated answers, related vendors and shared questions create dependence, so an interval is not a population guarantee or a significance test between engines.

When an outside source reports only a rounded share, its original integer numerator may be unavailable. We keep the source's rounding and say that a count-based interval cannot be reconstructed reliably. Multiplying a rounded percentage by a total does not recover the missing observations.

A zero also needs context. No citation in the captured answers is an observed absence within that sample. A failed fetch is missing evidence about the page. A query for which an engine returned no usable answer is not a negative verdict about every vendor. These cases must remain distinguishable in both tables and prose.

## The quiet problem of revised records

An updated article may retain its publication year while changing its data definition. We identify the version used. We also distinguish a protocol, a completed analysis and a later correction. Registration records decisions made before an analysis; it does not validate the eventual conclusion.

The same applies to this section. A correction should tell you which claim changed, why and which source now supports the wording. Moving an unsupported statistic to a different page does not repair it. If the source cannot be reached or the underlying study cannot be identified, its status remains unresolved.

## Try the standard on a vendor presentation

Take the sentence making the largest promise. Ask for the original report, then find the exact outcome in its table or methods. Replace promotional terms with the actual unit. If “visibility” means a weighted share of words in an experimental answer, write that. Do not translate it into visits, revenue or probability of being cited.

Next ask which businesses and questions were observed. An average across topics may hide large differences between topics. Check whether the claimed improvement is relative or expressed in percentage points. Ask whether the comparison held the observation conditions constant. A result can survive all these questions and still be useful only as a reason to test locally.

There is a cost to this standard: some memorable figures disappear, and some pages have to admit that no measurement exists. There is also a cost to pretending those gaps are settled. If a small, well-documented study gives a more relevant answer than a large but indirect one, the page should explain that choice instead of treating sample size as a ranking of truth.

## What our own data shows

We have no measurement on this point: no experiment establishes that this editorial grading system improves search ranking or AI citation. The [September Index deposit](https://doi.org/10.5281/zenodo.22907695) supplies the observations used elsewhere in this section; it is an observational release, not an evaluation of this standard.

## Sources

- Google Search Central. (2026). Creating helpful, reliable, people-first content. https://developers.google.com/search/docs/fundamentals/creating-helpful-content Verified 30 October 2026.
- Lewandowski, D., Sunkler, S., & Yagci, N. (2021). The influence of search engine optimization on Google's results. In WebSci '21 (pp. 12 to 20). ACM. https://doi.org/10.1145/3447535.3462479 Verified 30 October 2026.
- Broadcastwell. (2026). Absence Index, release 2026-09 [Data set]. Zenodo. Release JSON, answer JSONL and README. https://doi.org/10.5281/zenodo.22907695 Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *The Broadcastwell evidence standard*. Broadcastwell. https://docs.broadcastwell.com/research/standard/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research24,
  author = {{Broadcastwell research team}},
  title = {The Broadcastwell evidence standard},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/standard/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Vikram Patel, AI architect and specialist.

Sources checked 30 October 2026. This page has not been peer reviewed.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the measurement chapter](https://docs.broadcastwell.com/measurement-noise/).
