---
title: "Appendix B. Absence classification rules and precedence"
headline: "Absence classification rules and precedence: the six question shapes, their regular-expression rules and the fixed order in which they are applied"
description: "The complete classification scheme behind the absence ladder, reproduced as published in Volume II: six question shapes, the rule that assigns each, the precedence order, worked examples, and the residual category."
page_class: appendix
schema_type: TechArticle
date_published: "2026-08-18T00:00:00+00:00"
date_modified: "2026-08-18T00:00:00+00:00"
is_based_on: "https://doi.org/10.5281/zenodo.21586091"
---

# Appendix B. Absence classification rules and precedence

Reference material for Chapter 2 at [/absence-ladder/](https://docs.broadcastwell.com/absence-ladder/), Chapter 9 at [/category-door/](https://docs.broadcastwell.com/category-door/) and Chapter 10 at [/comparison-gate/](https://docs.broadcastwell.com/comparison-gate/). Reproduced as published in Volume II.

## What is being classified

**Measured, Volume II.** For every question where the company was not named, the full question text was retained. That produced 616 absence records across 85 companies in 60 categories. Each record was then assigned exactly one shape.

## How completeness was validated

**Measured, Volume II.** For all 85 companies, the absence count equals ten minus the visibility score, with zero mismatches. **Reasoned.** That check is what makes the denominator of every percentage in the ladder the complete set of losses rather than a convenience subset, and it is the single cheapest integrity check available on an absence dataset.

## The six shapes and their rules

**Measured, Volume II.** Each absence question was assigned one shape by regular-expression rules applied in fixed precedence.

| Shape | Rule | Example |
|-|-|-|
| Head-to-head comparison | contains "vs", "versus", or "comparison" | "Whitespace vs Artificial Labs: which is better?" |
| Alternatives-to-incumbent | contains "alternative" | "What are the best Sequel alternatives?" |
| Best-of shortlist | contains "best" or "top N" | "What is the best resource management software?" |
| Evaluation criteria | evaluate, choose, select, criteria, pricing model | "How should I compare pricing models when switching?" |
| Use case or problem | opens "how can/do/does" or contains "use case" | "How can this software reduce manual data entry?" |
| Definitional | opens "what is/are" without "best" | "What is reinsurance placement software?" |

## The precedence order

**Measured, Volume II.** The rules are applied in the order shown, top to bottom. A question containing both "best" and "vs" is counted as a comparison, not a shortlist. **Reasoned.** Precedence is what makes the scheme deterministic. Without a stated order, the same question can land in two shapes depending on implementation, and two people classifying the same absence list will not agree.

## The residual category

**Measured, Volume II.** 2.8% of records fell to *other*, meaning they matched none of the six rules. **Reasoned.** A published residual is a useful signal about a taxonomy. A scheme with no residual has usually forced every case into a bucket, and a scheme with a large one is not describing its material. 2.8% is small enough to be ignorable and non-zero, which is what an honest rule set looks like.

## The collapsed buckets used in the ladder

**Measured, Volume II.** Category-level means best-of shortlists plus alternatives-to-incumbent queries, combined. Head-to-head comparison is reported on its own. **Reasoned.** The collapse is what turns six shapes into a two-gate diagnostic. Best-of and alternatives-to-incumbent both ask who belongs in a set without adjudicating between two named vendors, which is why they group. Comparison is separated because it tests preference rather than membership.

## The visibility tiers

**Measured, Volume II.** Records were grouped by the subject company's visibility score into four tiers: named 0 of 10, named 1 to 3, named 4 to 6, and named 7 to 10, carrying 300, 199, 101 and 16 absence records respectively across 30, 25, 21 and 8 companies. **Measured, Volume II.** Nine companies scored 7 or above but one scored 10 of 10 and produced no absence records, so the top tier rests on 8 companies, and company counts sum to 84 in the tier table against 85 in the sample.

## The stated limitation of the scheme

**Measured, Volume II.** Question shapes were assigned by regular expression, not human annotation, and Volume II publishes the rules and their precedence so anyone can reclassify and check. **Reasoned.** A human annotator would classify some questions differently, most plausibly at the boundary between the evaluation-criteria and use-case rules, which both key on how a question opens. **Reasoned.** The trade is accuracy for reproducibility, and it is the right trade for a published dataset because the rules and the 616 classified questions are both published. Anyone who disagrees with a rule can reclassify the whole set and recompute the table rather than argue about individual calls.

## How to apply this to your own absence list

**Reasoned.** Take the questions you were not named in, keep the full text, and apply the six rules in the order given: comparison first, then alternatives, then best-of, then evaluation, then use case, then definitional. Anything matching none of them is other. Then collapse best-of and alternatives into a single category-level bucket and keep comparison separate. Those two counts are the diagnostic described in Chapter 2 at [/absence-ladder/](https://docs.broadcastwell.com/absence-ladder/).

## Sources

The classification scheme, its precedence, the worked examples, the residual share, the tier definitions and their record counts, the completeness validation and the stated limitation are all from The 2026 State of GEO, Volume II. The 616 classified questions are published with their verbatim text, assigned shape and visibility tier in `absence_questions_classified.csv`, and the aggregate table in `absence_shape_by_tier.csv`, at [github.com/Broadcastwell/state-of-geo-2026](https://github.com/Broadcastwell/state-of-geo-2026).

## About this manual

**Author.** Sairam Sivakumar, Broadcastwell.

**Operator disclosure.** Broadcastwell ran this measurement and sells services in the category it measures. Broadcastwell is excluded from the measured sample and from every ranking. The mitigation is not that the conflict is absent, it is that the raw data and the code are public and the result can be recomputed by anyone who disagrees.

**Self-audit, July 2026.** In the four-engine, five-run self-audit published alongside Volume II in July 2026, Broadcastwell was named in 0 of 200 answers and cited 0 times among 663 citations. That published figure stands with its date and is never replaced.

**Self-audit, 18 August 2026.** Re-measured on the same ten published questions across the same four engines, at one run per question rather than five, between 03:51 and 04:03 UTC on 18 August 2026: named in 1 of 40 answers, and cited once among 674 citations. The single naming and the single citation are the same answer, in which the engine quoted Broadcastwell's own published visibility page as a source. The two lines are not directly comparable, because one rests on five runs per question and the other on one.

**Not peer reviewed.** This is an independent industry study published as an open dataset with the analysis code that produced every figure in it. It has not been through academic peer review. Read it as measurement, and check the measurement. If you disagree with a number here, recompute it from the public data and publish what you get.

**Licence.** Prose and figures CC BY 4.0. Site code MIT.

**The three volumes.**

| Volume | What it covers | DOI |
|-|-|-|
| Volume I | 85 companies, 61 categories, 860 scored answers and 5,160 citations, one engine held constant. The dataset README additionally records 1,753 unique domains cited | [10.5281/zenodo.21537014](https://doi.org/10.5281/zenodo.21537014) |
| Volume II | The Absence Ladder. All 616 absence records classified by question shape | [10.5281/zenodo.21586091](https://doi.org/10.5281/zenodo.21586091) |
| Volume III | Cross-engine divergence. 280 questions, 40 categories, four engines, 853 answers | [10.5281/zenodo.21789120](https://doi.org/10.5281/zenodo.21789120) |

Data and analysis code for all three volumes: [github.com/Broadcastwell/state-of-geo-2026](https://github.com/Broadcastwell/state-of-geo-2026).

*Version 1.0, August 2026.*
