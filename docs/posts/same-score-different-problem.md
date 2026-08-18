---
title: "Same score, different problem"
headline: "Same score, different problem: why two companies both scoring 2 of 10 in AI answers need opposite work"
description: "Across 616 absence records from 85 B2B software companies, companies named in zero of ten AI answers lose category-level questions 55.3% of the time, while companies named in seven or more lose head-to-head comparisons 68.8% of the time. A single visibility percentage cannot tell you which you are."
schema_type: TechArticle
date_published: "2026-08-18"
date_modified: "2026-08-18"
image: "figures/absence-ladder.png"
is_based_on: "https://doi.org/10.5281/zenodo.21586091"
---

# Same score, different problem

## The finding

Across 616 recorded absences from 85 B2B software companies in 60 categories, what a company loses to an AI answer changes shape as its visibility rises: companies named in zero of ten answers lose category-level questions 55.3% of the time, while companies named in seven or more of ten lose head-to-head comparisons 68.8% of the time. The pattern holds across all four visibility tiers at chi-square 61.8, df 15, p = 1.3 × 10⁻⁷. Two companies can hold the identical visibility score and be at opposite ends of what they need to do next.

> **Operator disclosure.** Broadcastwell ran this measurement and sells services in the category it measures. Broadcastwell is excluded from the measured sample and from every ranking. The mitigation is not that the conflict is absent, it is that the raw data and the code are public and the result can be recomputed by anyone who disagrees.

## Two companies, one number

A visibility score of 2 out of 10 tells you that eight answers went by without you. It does not tell you what those eight answers were about.

Picture two companies that both score 2. The first is losing every best-of shortlist in its category. When a buyer asks an AI engine who the players are, the answer lists four vendors and this company is not one of them. It is not being rejected. It is not being considered.

The second company appears on those shortlists. It shows up when the buyer asks who exists. What it loses is the eight questions of the form "this company versus that one," where a buyer has already narrowed to two names and wants a verdict. It is in the set and losing inside it.

Those are different problems. They have different fixes, different content requirements and different costs. The single percentage hides the difference completely.

## Inverting the measurement

The usual approach counts the answers where a company appeared. The 2026 State of GEO, Volume II, did the opposite: it kept the full text of every buyer question where the company was not named, and asked what those questions had in common.

The method was 85 B2B software companies across 60 categories, ten buyer questions each, put to one AI engine with live web search, one run per question. Every question where the company was not named was retained with its verbatim text. That produced 616 absence records, and completeness was validated rather than assumed: for all 85 companies, the absence count equals ten minus the visibility score, with zero mismatches.

Each absence question was then assigned one shape by regular-expression rules applied in fixed precedence, so a question containing both "best" and "vs" counts as a comparison rather than a shortlist. The rules and their order are published, so the classification is reproducible by anyone who wants to check it. 2.8% of records fell to a residual "other" category.

## The ladder

| Visibility | Companies | Absences | Category-level | Head-to-head |
|-|-|-|-|-|
| Named 0 of 10 | 30 | 300 | **55.3%** | 20.0% |
| Named 1 to 3 | 25 | 199 | 48.2% | 24.6% |
| Named 4 to 6 | 21 | 101 | 20.8% | 41.6% |
| Named 7 to 10 | 8 | 16 | 12.5% | **68.8%** |

Category-level means best-of shortlists plus alternatives-to-incumbent queries.

Read the two right-hand columns downward. They move in opposite directions, monotonically, across every tier. That is the shape of a sequential process rather than a single wall.

Two things about the bottom row should travel with it wherever it is quoted. Nine companies scored 7 or above, but one of them scored 10 of 10 and therefore produced no absence records at all, so the top tier rests on the remaining 8 companies and their 16 records. Company counts across the four tiers sum to 84 here and to 85 in the sample, for that reason. The 68.8% figure is the most quotable number in the study and it sits on the smallest base in it.

The relationship survives that small base being removed. Visibility against absence-is-comparison runs at r = 0.234, p = 4.1 × 10⁻⁹ across all 616 records, and excluding the top tier entirely it still holds at r = 0.184, p = 5.9 × 10⁻⁶, n = 600.

## Two gates

A company named zero times is failing at the category door. The engine does not consider it a member of the set when a buyer asks who the players are. More than half of its losses are questions that never mention a competitor by name.

A company named seven or more times has cleared that door. It is a recognised member of the category, and what it loses is the second gate: direct comparison against a specific named rival.

The middle tiers sit exactly where you would expect if those two gates are sequential rather than simultaneous.

## What to do with this

The work implied by each stage is different. A company at the category door needs entity presence and inclusion in the third-party sources engines consult when assembling a set. Its problem is membership. A company at the comparison gate needs comparison content a model can quote against a specific named competitor. Its problem is preference.

Prescribing the second to a company stuck at the first is a common and expensive mistake, and a single visibility percentage cannot tell you which one you are.

The diagnostic costs nothing. Write down the ten questions a real buyer in your category would type. Put each to an AI engine with web search on. Record only whether you were named. Keep the full text of the questions where you were not. Sort those by shape, collapse best-of and alternatives into one category-level bucket, keep head-to-head comparison separate, and count. Whichever bucket dominates tells you which gate you are at.

## What this does not prove

The ladder describes where a company sits, not why it got there. Nothing in the dataset is an intervention study: no company was measured, changed and measured again. The sample is challenger-skewed by construction, so the 35% zero-visibility rate is a property of this sample and not of B2B software generally. All answers came from one engine, one run per question, and run-to-run variance was not measured here, so treat the direction of the finding as the result rather than the decimal.

The full argument, the six shape rules with examples, the complete statistics and every limitation are in [Chapter 2 of The Absence Manual, The Absence Ladder](../absence-ladder.md).

Source data: The 2026 State of GEO, Volume II, [10.5281/zenodo.21586091](https://doi.org/10.5281/zenodo.21586091). Data and code at [github.com/Broadcastwell/state-of-geo-2026](https://github.com/Broadcastwell/state-of-geo-2026).

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
| Volume I | 85 companies, 61 categories, 860 scored answers, 5,160 citations across 1,753 domains, one engine held constant | [10.5281/zenodo.21537014](https://doi.org/10.5281/zenodo.21537014) |
| Volume II | The Absence Ladder. All 616 absence records classified by question shape | [10.5281/zenodo.21586091](https://doi.org/10.5281/zenodo.21586091) |
| Volume III | Cross-engine divergence. 280 questions, 40 categories, four engines, 853 answers | [10.5281/zenodo.21789120](https://doi.org/10.5281/zenodo.21789120) |

Data and analysis code for all three volumes: [github.com/Broadcastwell/state-of-geo-2026](https://github.com/Broadcastwell/state-of-geo-2026).

*Version 1.0, August 2026.*
