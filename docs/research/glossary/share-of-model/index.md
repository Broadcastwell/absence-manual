---
title: What does Share of Model measure?
description: Share of Model is a brand’s share of category-brand mentions in a specified set of AI answers; the
  question set and counting rules define the result.
page_class: research
research_id: 35
research_group: glossary
lead: Lauren Chen
published: '2026-10-30T08:50:01Z'
updated: '2026-10-30T08:50:01Z'
next_review: '2027-01-30T08:50:01Z'
canonical: https://docs.broadcastwell.com/research/glossary/share-of-model/
sources_verified: true
schema_type: Article
date_published: '2026-10-30T08:50:01Z'
date_modified: '2026-10-30T08:50:01Z'
is_based_on: https://marketing.org.nz/resource-hub/share-of-model-a-new-metric-for-marketing-strategies
defined_term: Share of Model
---

# What does Share of Model measure?

**Share of Model is a brand’s share of category-brand mentions in a specified set of AI answers; the question set and counting rules define the result.**

The capitalized name can refer to a product as well as a marketing measure. Ask for the calculation before comparing two dashboards. A count of answers naming a company and a share of all brand mentions answer different questions, even when both carry the same label.

For practical reporting decisions, use the library’s [client AI visibility report guidance](/answers/measurement/what-should-a-client-ai-visibility-report-contain/). This definition concerns the denominator behind the term.

## Which early uses can we verify?

Peter Mangin’s Marketing Association article is dated **20 March 2024** and uses Share of Model for how language models perceive a brand relative to competitors. That is the earliest dated article using the phrase that we verified for this entry. It does not establish who first spoke or coined it. [Mangin, 2024].

Tom Roach’s **11 July 2024** Marketing Week column makes the category-mention ratio explicit. Roach attributes an early discussion to Jellyfish colleague Jack Smyth. The live article header confirms the author and date; the primary publisher’s indexed article text supplies that definition. We do not turn the attribution into an independently established invention claim. [Roach, 2024].

Vendor use continues. Jellyfish’s **25 June 2026** product announcement calls its platform Share of Model and describes creator-content analysis. A platform name does not make every metric in that platform the same quantity as the category-mention ratio. [Jellyfish, 2026].

## Write out the denominator

A reproducible category-mention share divides mentions assigned to the focal brand by all eligible category-brand mentions in the same observations. State whether a brand can count repeatedly within an answer or only once. Identify how aliases, subsidiaries, ambiguous ordinary words and product names are treated.

An answer-level naming rate instead divides eligible answers naming that brand by all eligible answers. Several competing brands can appear in an answer, so their naming rates need not sum to a complete partition. Category-mention shares can form a partition only when the same exhaustive, mutually exclusive brand-assignment rules apply to the numerator and denominator.

Neither quantity is a direct view into everything a model learned. The observed answers are responses to a chosen set of questions under particular conditions. A company can appear because of information retrieved during that interaction, information already represented in the system, or a mixture the answer itself does not reveal.

## Make comparisons that survive a question change

Keep the category boundary fixed. Adding obscure competitors to the dictionary can change the denominator without changing the focal company’s answers. Adding questions about that company’s strongest use case can change the result without any change to its public presence.

Preserve the original answer records and the release’s question texts. Report engine, observation dates, language, repetitions, exclusions and the rule for an empty answer. Compare like configurations separately before presenting a combined result. A weighted aggregate needs its weights disclosed; it is not automatically the unweighted average of the individual engine shares.

A negative recommendation still contains a mention. Report the naming event separately from whether the answer presents the product favorably or actually recommends it. Likewise, a linked source is a citation event, not another spelling of a brand mention.

## What should a software company request?

Request the counted observations behind a material movement, not just a percentage change. Check which questions changed, which competitors entered the calculation, and whether the engine configuration stayed comparable. A larger proportion of a shrinking mention pool can coexist with fewer absolute mentions.

Use the result to describe exposure within the observed category questions. Connecting it to commercial outcomes requires additional evidence about people, visits and purchases. The measure itself does not establish market share, customer preference or revenue attributable to AI answers.

## What our own data shows

The Absence Index calls its answer-level outcome **naming rate**, with the eligible answer base stated in the release. Study 2 separately reports vendor-answer pairs, own-domain citations and named-without-own-citation events. Those measures retain their own names; we do not relabel them Share of Model.

For example, the registered citation analysis finds **2,608 own-domain citation events among 8,085 named vendor-answer pairs: 32.3%, Wilson 95% interval 31.2% to 33.3%**. This is conditional citation coverage among named pairs, not a category-mention share. The [Study 2 table and public reproduction files](/research/studies/who-ai-engines-cite/) supply the exact units and underlying counts.

## Sources

- Mangin, P. (2024, March 20). Share of Model: A new metric for marketing strategies. Marketing Association. Dated author article, definition and limitations. https://marketing.org.nz/resource-hub/share-of-model-a-new-metric-for-marketing-strategies Verified 30 October 2026.
- Roach, T. (2024, July 11). Share of model is the new marketing measure for the AI era. Marketing Week. Author definition of category-mention share; full primary search-index text and live article header checked. https://www.marketingweek.com/tom-roach-share-of-model-ai-era/ Verified 30 October 2026.
- Jellyfish. (2026, June 25). Jellyfish expands Share of Model with Creator Intelligence updates to reveal which creators influence AI models & more. Product announcement. https://www.jellyfish.com/en-us/news/creator-intelligence-updates/ Verified 30 October 2026.
- Broadcastwell. (2026). Absence Index, release 2026-09 [Data set]. Zenodo. Release JSON, answer JSONL and README. https://doi.org/10.5281/zenodo.22907695 Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *What does Share of Model measure?*. Broadcastwell. https://docs.broadcastwell.com/research/glossary/share-of-model/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research35,
  author = {{Broadcastwell research team}},
  title = {What does Share of Model measure?},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/glossary/share-of-model/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Lauren Chen, AI architect and specialist.

Sources checked 30 October 2026. Independent check: pending. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Build a client visibility report](https://docs.broadcastwell.com/answers/measurement/what-should-a-client-ai-visibility-report-contain/).
