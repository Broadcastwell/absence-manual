---
title: What is entity confidence, and is it a Google metric?
description: Entity confidence is a publisher-defined assessment of how clearly a system identifies and describes
  an entity; it is not a standardized Google search metric.
page_class: research
research_id: 39
research_group: glossary
lead: Maya Thompson
published: '2026-10-30T08:50:01Z'
updated: '2026-10-30T08:50:01Z'
next_review: '2027-01-30T08:50:01Z'
canonical: https://docs.broadcastwell.com/research/glossary/entity-confidence/
sources_verified: true
schema_type: Article
date_published: '2026-10-30T08:50:01Z'
date_modified: '2026-10-30T08:50:01Z'
is_based_on: https://fireflyweblabs.com/ai-visibility-framework/entity-confidence-why-ai-trusts-some-businesses-and-not-others/
defined_term: Entity confidence
---

# What is entity confidence, and is it a Google metric?

**Entity confidence is a publisher-defined assessment of how clearly a system identifies and describes an entity; it is not a standardized Google search metric.**

Treat the label as a request for a definition. A consultant might use it for consistent company facts, an identity-matching system for a match probability, and a vendor for a weighted audit score. Those meanings cannot be exchanged without examining their evidence and calculation.

The library explains [what counts as a brand mention](/answers/measurement/what-counts-as-a-brand-mention-in-an-ai-answer/). This entry concerns the additional certainty claim sometimes attached to recognition or accurate description.

## A vendor framework with a limited date

Firefly Web Labs displays **2025** on its Entity Confidence framework page, without a day or month. It is the earliest dated AI-visibility framework use we verified for this entry. We cannot establish a sole inventor or a precise first-publication day from that page.

Firefly organizes the idea around identifiability, consistency, corroboration, specificity and stability. Its FAQ acknowledges that the concept is not a single published score inside AI systems. The page also retains an unfilled research placeholder for a proposed relationship with citation frequency. That placeholder is a reason to withhold the proposed empirical conclusion. [Firefly Web Labs, displayed 2025, definition, FAQ and research placeholder].

The framework can suggest questions for an audit. It does not, by itself, demonstrate a universal internal threshold shared by different engines or prove that the proposed properties combine mathematically in the way its narrative suggests.

## What does Google actually document?

Google’s Knowledge Graph Search API documentation defines **resultScore** as an indicator of how well an entity matched the request constraints. That is the documented meaning of that field. It is not described there as the probability that Google trusts the company, a general recommendation score or a Search ranking weight. [Google, entities.search, response fields].

This distinction is narrower and more defensible than claiming to know that Google has no internal measures of certainty. We do not have access to every internal system. What we can say is that the opened operator documentation does not establish the marketing label Entity Confidence as a standardized public Google metric.

If a report presents such a score, ask who produces it. An externally constructed rubric can be legitimate as a rubric, provided its inputs and limits are disclosed. It should not acquire operator authority through a label or a graph styled to resemble a search-engine dashboard.

## How could an outside assessment be tested?

Start with observable tasks. Can the answer distinguish the intended company from a similarly named one? Does it correctly state the product category? Does it attach the right official domain? Preserve the question, answer, time and reference facts used to judge correctness.

Report those outcomes separately before combining them. A well-known name can be recognized and still be described inaccurately. A correct description can appear without a recommendation. An omission cannot reveal how certain the system felt about an entity it never named.

A calibrated probability would need repeated outcomes and an explicit validation design. If items assigned a given probability are not checked against known outcomes, the number may be an audit rating rather than measured confidence. Name it accordingly and disclose any weighting chosen by the assessor.

## What helps a B2B reader interpret the term?

Prefer a documented identity record over a promise to increase an invisible score. Keep legal and product names distinguishable, show which domain represents the product, date material facts and correct contradictions you can substantiate. These actions make verification easier for people as well as automated readers.

Do not infer that absence proves identity confusion. A question can exclude a product for legitimate scope reasons, retrieval may fail, or the answer may vary. Investigate those possibilities using the actual answer record rather than selecting the vendor framework’s preferred explanation in advance.

## What our own data shows

Our published method uses explicit **name and domain matching rules**. These produce observed matching events; they are not confidence scores inside an engine. Study 2’s **8,085 named pairs among 42,792 eligible vendor-answer pairs** are counted under those rules, not graded on a hidden certainty scale.

The [public matching dictionary and method](/research/studies/who-ai-engines-cite/) let a reader inspect what qualified as a naming or own-domain-citation event. We have not measured Entity Confidence or validated a vendor’s composite confidence score.

## Sources

- Firefly Web Labs. (2025, as displayed; no day or month supplied). Entity confidence: Why AI trusts some businesses and not others. AI Visibility Framework. Definition, FAQ and unfilled research placeholder, checked 30 October 2026. https://fireflyweblabs.com/ai-visibility-framework/entity-confidence-why-ai-trusts-some-businesses-and-not-others/ Verified 30 October 2026.
- Google. (n.d.). Method entities.search. Knowledge Graph Search API. Response fields: resultScore. Checked 30 October 2026. https://developers.google.com/knowledge-graph/reference/rest/v1/ Verified 30 October 2026.
- Broadcastwell. (2026). Absence Index, release 2026-09 [Data set]. Zenodo. Release JSON, answer JSONL and README. https://doi.org/10.5281/zenodo.22907695 Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *What is entity confidence, and is it a Google metric?*. Broadcastwell. https://docs.broadcastwell.com/research/glossary/entity-confidence/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research39,
  author = {{Broadcastwell research team}},
  title = {What is entity confidence, and is it a Google metric?},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/glossary/entity-confidence/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Maya Thompson, AI architect and specialist.

Sources checked 30 October 2026. Independent check: pending. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Understand brand-mention matching](https://docs.broadcastwell.com/answers/measurement/what-counts-as-a-brand-mention-in-an-ai-answer/).
