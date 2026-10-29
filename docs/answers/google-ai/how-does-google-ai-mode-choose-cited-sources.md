---
title: How does Google AI Mode choose cited sources?
headline: How does Google AI Mode choose cited sources?
description: Google reports related-search and eligibility mechanisms, not a complete selection formula. Procore’s 3 of 3 AI Mode mentions measure naming only.
page_class: page
schema_type: Article
date_published: '2026-10-28T23:21:51+00:00'
date_modified: '2026-10-28T23:21:51+00:00'
hide:
- navigation
library_cluster: google-ai
library_owner: Vikram Patel, AI Architect
library_subtopic: Source selection
library_order: 60
demand_source: google-autocomplete
demand_evidence: LB-Q0282, private demand receipt dated 2026-10-28
also_asked_as:
- How does Google AI Mode choose cited sources?
is_based_on: https://doi.org/10.5281/zenodo.22907695
---

# How does Google AI Mode choose cited sources?

Google describes related searches and supporting-page eligibility, but its public guidance does not give a complete formula for which source AI Mode will cite. Our own example is narrower: AI Mode named Procore in 3 of 3 answers to one construction-software question on 22 September 2026. That naming result cannot reveal which sources the system selected or why.

## What we measured

**Reported.** Google's [AI-feature documentation](https://developers.google.com/search/docs/appearance/ai-features), read on 28 October 2026, says AI Mode may issue related searches across subtopics and data sources while developing a response. Supporting pages must be indexed and eligible for a Google Search snippet. The guide also says that meeting requirements does not guarantee crawling, indexing or serving.

**Measured.** The [September release](https://doi.org/10.5281/zenodo.22907695) captured three scheduled AI Mode answers for the small-residential-builder construction question. All three named Procore, yielding a descriptive 95% Wilson interval of 43.9% to 100.0%. The recorded engine-by-question result is a name count. It is not an engine-specific own-domain citation count or an observation of Google's internal selection process.

**Reasoned.** An answer's visible links can show which destinations were attached to that captured response. They do not expose every page considered, a ranking weight or a causal path from a website edit to a citation. Google's reported mechanisms and our observed answers must retain those separate roles.

[Every figure comes from the published method, v1.1.](https://broadcastwell.com/methodology)

## What this means for you

If you want to understand a citation, begin with the captured answer and its exact links. Read the destination and identify the passage that supports the associated claim. A name appearing elsewhere in the answer is a separate observation.

Check ordinary Search eligibility before seeking an undocumented AI-specific trick. Google's guide says that no special AI text file or schema is required for these features; it does not promise selection after any one technical change.

Keep an honest gap in your report when source-selection evidence is unavailable. A naming table can answer “was this product named?” without answering “why was this page cited?”

## Also asked as

How does Google AI Mode choose cited sources?

## Related

- [Procore naming record](https://index.broadcastwell.com/vendors/procore/construction-project-management/)
- [Sources and their limits](https://docs.broadcastwell.com/who-gets-cited/)
- [Reading a cited domain](https://docs.broadcastwell.com/answers/geo-basics/what-can-a-cited-domain-tell-me-about-an-ai-source/)
- [Own-domain citation counting](https://docs.broadcastwell.com/answers/measurement/what-counts-as-an-own-domain-citation-in-an-ai-answer/)

## Next step

In [Free 10-question check (one engine)](https://audit.broadcastwell.com/), open the actual source link before inferring how a name reached the answer. No email is needed; runs are limited per network and per day, and by the site's daily allowance.

Choose [Fix one answer, $490](https://broadcastwell.com/answer-repair) for a specific supported factual correction. A proposed secret source-selection formula is not evidence for that work.

Claiming or correcting a vendor record is free and never depends on a purchase.

Prepared by the Broadcastwell team.

Page owner: Vikram Patel, AI Architect. Corrections: hello@broadcastwell.com
