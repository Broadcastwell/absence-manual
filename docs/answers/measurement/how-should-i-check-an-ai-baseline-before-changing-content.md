---
title: How should I check an AI baseline before changing content?
headline: How should I check an AI baseline before changing content?
description: 'Fix the question set, retain answers and check repeat variation first: Claude’s mean shortlist agreement was 0.442 over 74 pairs on 4 August 2026.'
page_class: page
schema_type: Article
date_published: '2026-10-29T00:06:10+00:00'
date_modified: '2026-10-29T00:06:10+00:00'
hide:
- navigation
library_cluster: measurement
library_owner: Vikram Patel, AI Architect
library_subtopic: Baseline design
library_order: 80
demand_source: reddit
demand_evidence: LB-Q0520, private demand receipt dated 2026-10-28
also_asked_as:
- How should I check an AI baseline before changing content?
is_based_on: https://doi.org/10.5281/zenodo.21789120
evidence_kind: published-study
evidence_method_receipts:
- https://doi.org/10.5281/zenodo.21789120
---

# How should I check an AI baseline before changing content?

Before changing content, preserve the questions, engine, dates, valid-answer rules and original answers, then examine variation under those conditions. On 4 August 2026, Claude's mean vendor-set agreement was 0.442 across 74 repeat pairs in our study. A baseline that keeps only a single favourable screenshot cannot show how much the same question varied before the edit.

## What we measured

**Measured.** Volume III repeated a selected set of twenty-five questions three scheduled times within one collection window on 4 August 2026. The [published repeat method](https://doi.org/10.5281/zenodo.21789120) compares the vendor sets in usable repeat pairs using Jaccard agreement, the intersection divided by the union.

Claude supplied 74 pairs with mean agreement 0.442 and a published bootstrap 95% interval of 0.389 to 0.494. Google AI Overviews supplied 62 pairs, with mean 0.499 and interval 0.441 to 0.556. The 05:28 to 16:29 UTC window is a dated collection, rather than a claim that either engine has a fixed level of variation today.

**Reasoned.** These observations support checking the baseline's stability before interpreting later movement. They do not determine an optimal question count or establish that a particular content intervention will work. Three scheduled runs describe this study's design, not a universal sufficiency rule.

[Our answer-study method, v1.1.](https://broadcastwell.com/methodology)

## What this means for you

Write down the decision you want the baseline to inform. Keep category discovery questions separate from questions that already supply a brand name. If you retain paraphrases, label them as separate conditions rather than silently substituting them between dates.

Save the answer text and sources with every observation, including unusable captures and the reason for each exclusion. A name count should resolve back to the answer in which the name was matched.

Record the planned content change after preserving that baseline. When you measure again, retain the same conditions or disclose what changed. A different question set or engine configuration can produce a different result without demonstrating an effect from the page edit.

## Also asked as

How should I check an AI baseline before changing content?

## Related

- [Volume III repeat evidence](https://doi.org/10.5281/zenodo.21789120)
- [Measurement noise](https://docs.broadcastwell.com/measurement-noise/)
- [Choosing repeated runs](https://docs.broadcastwell.com/answers/measurement/how-many-repeated-runs-make-an-ai-visibility-rate-useful/)
- [Brand-name prompts and discovery](https://docs.broadcastwell.com/answers/geo-basics/do-brand-name-prompts-measure-discovery/)

## Next step

Save the complete result from [Free 10-question check (one engine)](https://audit.broadcastwell.com/) as one observation in your baseline, with the question and capture date intact. No email is needed; runs are limited per network and per day, and by the site's daily allowance.

When that baseline identifies a supported factual change, [Fix one answer, $490](https://broadcastwell.com/answer-repair) can define the page work separately from the later comparison. Preserve the original evidence before the work starts.

Prepared by the Broadcastwell team.

Page owner: Vikram Patel, AI Architect. Corrections: hello@broadcastwell.com
