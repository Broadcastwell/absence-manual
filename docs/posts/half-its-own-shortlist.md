---
title: "Half its own shortlist"
headline: "Half its own shortlist: an AI engine asked the same question twice agrees with itself about half the time"
description: "Across 62 and 74 repeat pairs on a 25-question subsample, Google AI Overviews agreed with its own vendor shortlist at 0.499 and Claude at 0.442 when asked the identical question again. Every single-run visibility score carries that variance and cannot show it."
page_class: note
schema_type: TechArticle
date_published: "2026-08-18T00:00:00+00:00"
date_modified: "2026-08-18T00:00:00+00:00"
image: "figures/within-vs-between.png"
is_based_on: "https://doi.org/10.5281/zenodo.21789120"
---

# Half its own shortlist

## The finding

Asked the identical buyer question again inside the same collection window, Google AI Overviews agreed with roughly half of its own previous vendor shortlist, at a mean set agreement of 0.499 across 62 repeat pairs, and Claude at 0.442 across 74 repeat pairs, on a stratified subsample of 25 questions. Every single-run AI visibility number sold in this industry carries that variance and cannot show it. The same company measured twice can produce two different scores, and a single-run number cannot tell you how far apart the two could have been.

> **Operator disclosure.** Broadcastwell ran this measurement and sells services in the category it measures. Broadcastwell is excluded from the measured sample and from every ranking. The mitigation is not that the conflict is absent, it is that the raw data and the code are public and the result can be recomputed by anyone who disagrees.

## Why anyone measured this

These systems are not deterministic. Retrieval is live, ranking is probabilistic, and the answer is generated rather than looked up. Ask the same engine the same question twice and the shortlist moves.

That has a consequence for every cross-engine comparison ever published. Any measured difference between two engines contains an unknown amount of the same variation you would get by asking one engine twice. Unless the noise floor is measured on the same questions in the same window, a divergence headline is not interpretable at all. It is a number whose denominator has not been stated.

The 2026 State of GEO, Volume III, put 280 B2B software buyer questions across 40 categories to four production AI search engines in a single window, 05:28 to 16:29 UTC on 2026-08-04. A stratified subsample of 25 questions, balanced across question shapes, was run three times on all four engines specifically so the engine-to-engine difference could be read against each engine's own run-to-run noise.

## What went wrong, and why it is disclosed

Three of the four API accounts ran out of credit during collection. One was topped up and finished, two were not. The study as executed holds 18 ChatGPT, 280 Claude, 175 Perplexity and 280 Google AI Overviews answers, against 280 planned for each. Rows carrying a billing error are excluded from every denominator and retained in the raw data so the exclusion is checkable.

The two short engines were deliberately not refilled. A refill collected in a second window would make every cross-engine pair span two windows, so engine drift between windows would read as engine divergence and inflate the exact quantity the study was measuring. Staying short was the more honest option, and the four-engine intersection is reported at its true size of 18 questions rather than dressed up.

Only the two engines that completed contributed repeat pairs. ChatGPT and Perplexity contributed none and therefore get no verdict.

## The numbers

| Engine | Repeat pairs | Same engine, repeated | Different engines | Gap (95% CI) |
|-|-|-|-|-|
| Claude | 74 | 0.442 (0.389 to 0.494) | 0.277 (0.222 to 0.333), n = 37 | 0.165 (0.082 to 0.242) |
| Google AI Overviews | 62 | 0.499 (0.441 to 0.556) | 0.240 (0.186 to 0.295), n = 35 | 0.258 (0.178 to 0.338) |

The left-hand figure is the one that matters commercially. The best case here is an engine agreeing with itself on roughly half its own shortlist across runs of the identical question.

## The split, so this cannot be read as overclaiming

The gap between the two columns looks like clean evidence that engines genuinely differ. On one engine it is. On the other it is not, and reporting only the survivor would have been the easy mistake.

Engines name very different numbers of vendors per answer: 4.77 for Google AI Overviews, 8.83 for Claude, 10.69 for Perplexity, 14.72 for ChatGPT. Set overlap between two similar-length lists runs mechanically higher than between two lists of very different length. Same-engine repeat pairs are length-matched by construction. Different-engine pairs are not. So the comparison was rerun three more ways: restricted to the study universe, truncated to each answer's first five named vendors, and with the measure swapped for an overlap coefficient normalised by the smaller set.

On Google AI Overviews the gap survives all three, at 0.325, 0.167 and 0.193 respectively, all positive at 95%. On Claude it does not. The raw gap of 0.165 falls to 0.075, with an interval of −0.014 to 0.177, under truncation, and to 0.002, with an interval of −0.112 to 0.113, under the overlap coefficient. Both include zero.

On Claude, what looks like cross-engine divergence cannot be distinguished from the fact that the engines being compared name lists of different lengths.

## Why the pooled figure is not the headline

Pooled across engines, same-engine agreement is 0.468 (0.427 to 0.505) over 136 repeat pairs against different-engine agreement of 0.247 (0.201 to 0.298) over 51 pairs. That looks decisive and it is not, because 54.4% of those same-engine pairs are Claude. A pooled mean is dominated by whichever engine contributed the most pairs and can report a separation only one engine actually has. That is an unstated denominator, which is exactly the failure the study exists to name.

## What this means if someone sells you a score

Anyone selling a number described as "your AI search visibility" without naming the engine, the date and the question set is selling a number whose denominator is unstated.

Four questions settle it. Which engine produced this. On what date, in what window. What were the questions, in full text. How many runs did each question get, and if one, what is the run-to-run variance on those questions. A supplier doing the work properly answers all four in a sentence each. A supplier who cannot answer the fourth has sold you a point estimate from a distribution without telling you its width.

You can measure your own noise floor in an afternoon. Take five of your buyer questions, put each to the same engine three times on the same day, write down the vendors named each time, and compare the runs pairwise. That average is the number every other visibility figure you are shown should be read against.

## What this does not claim

It does not claim that variance makes measurement pointless. Variance is a property of the system that can be quantified and reported, and this study quantified it. It also says nothing about the run-to-run stability of ChatGPT or Perplexity, which contributed no repeat data. Everything here was collected in a single window on one day, on products under continuous change, Google AI Overviews is scraped rather than API-served, and the engines measured are production endpoints rather than the consumer applications people type into.

The full argument, the complete robustness table, the pooled figures and every limitation are in [Chapter 6 of The Absence Manual, Your Score Is Noisier Than Your Vendor Admits](../measurement-noise.md).

Source data: The 2026 State of GEO, Volume III, [10.5281/zenodo.21789120](https://doi.org/10.5281/zenodo.21789120). Data and code at [github.com/Broadcastwell/state-of-geo-2026](https://github.com/Broadcastwell/state-of-geo-2026).

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
