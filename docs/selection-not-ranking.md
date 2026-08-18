---
title: "Chapter 0. Selection, not ranking"
headline: "Selection, not ranking: why the mental model you brought from SEO produces the wrong questions about AI search"
description: "An AI answer is assembled by selecting a handful of vendors from a candidate set, not by ordering every vendor in a category. Volume I measured an average of 2.05 vendors named per answer. That single number breaks the ranking model, and with it the metrics and remedies built on top of it."
page_class: chapter
schema_type: TechArticle
date_published: "2026-08-18T00:00:00+00:00"
date_modified: "2026-08-18T00:00:00+00:00"
image: "figures/absence-ladder.png"
is_based_on: "https://doi.org/10.5281/zenodo.21537014"
---

# Chapter 0. Selection, not ranking

By the end of this chapter you will know why AI search is a selection problem rather than a ranking problem, what that changes about the questions worth asking, and why almost every metric imported from search engine optimisation answers a question the system is no longer asking.

## The claim this chapter defends

**Measured, Volume I.** Across 860 scored answers, the average AI answer named 2.05 vendors. **Reasoned.** A results page with ten blue links is an ordering of a long list; an answer that names two vendors is a selection from a candidate set. Those are different mechanisms, and the difference is not cosmetic. Ordering has a position you can improve. Selection has a boundary you are inside or outside of. Every metric, every diagnosis and every remedy that a marketer imports from search engine optimisation assumes the first mechanism, and this chapter is about what happens when you apply it to the second.

> **Operator disclosure.** Broadcastwell ran this measurement and sells services in the category it measures. Broadcastwell is excluded from the measured sample and from every ranking. The mitigation is not that the conflict is absent, it is that the raw data and the code are public and the result can be recomputed by anyone who disagrees.

## The number that breaks the old model

**Measured, Volume I.** The average answer named 2.05 vendors. The sweep covered 85 B2B software companies across 61 categories, putting ten standardised buyer questions to one AI engine with live web search for each of them. Volume I reports 860 scored answers in total. **Reasoned.** Two point zero five is not a shorter results page. It is a different object. A page of ten links can carry the market leader, three challengers, two review sites and a comparison blog, and the buyer chooses among them. An answer naming two vendors has already chosen. The visible surface is not a ranked list that has been truncated. It is a decision that has been made and then narrated.

## Ranking asks where, selection asks whether

**Reasoned.** Under a ranking model the operative question is positional: where do we sit, and what moves us up. Position implies a continuum, so effort maps onto small monotonic gains, and a bad position is a recoverable one. Under a selection model the operative question is binary at the first stage: are we in the candidate set the engine assembles before it writes anything. If the answer is no, position is undefined. There is no eighth place to climb out of. You are not ranked badly. You are not present, and presence and position are different states requiring different work.

## What the distribution actually looks like

**Measured, Volume I.** The median company was named in 20% of the AI answers for its own category, and 35% were named in zero. **Measured, Volume I.** The median category leader appeared in 80% of its category's answers. **Reasoned.** Those two figures together describe a winner-take-most shape rather than a gradient. A gradient would put most companies in the middle with thin tails. What the data shows instead is a large group at or near zero, a small group near saturation, and comparatively little in between. Selection systems produce that shape. Ranking systems, which have to place everybody somewhere, do not.

## The sample this rests on, stated plainly

**Measured, Volume I.** The 85 companies were selected as plausible challenger brands rather than sampled at random, so the average named rate is lower than a random draw of all vendors would produce. Volume I says so in its own limitations. **Reasoned.** That skew matters for the level of the numbers and not for the shape of them. A challenger-skewed sample cannot tell you the industry base rate for zero visibility. It can tell you that within a population of plausible challengers, a large fraction are absent entirely while leaders sit near saturation, and that is the observation the selection model rests on.

## Why the shape follows from the mechanism

**Reasoned.** If an answer has room for roughly two vendors and the engine assembles its candidates from sources that already agree about who the players are, then the same well-corroborated names will be selected repeatedly and everyone else will be selected almost never. Scarcity of slots plus consensus in the evidence layer produces concentration mechanically. This is a reading of the measured distribution rather than a separate finding, and it is offered as the reason the numbers look the way they do, not as evidence for itself.

## Different engines make different-sized selections

**Measured, Volume III.** Mean vendors named per answer ran to 4.77 for Google AI Overviews, 8.83 for Claude, 10.69 for Perplexity and 14.72 for ChatGPT. **Measured, Volume III.** Volume III states directly that these are not comparable like for like with Volume I's 2.05, because its extraction layer is wider: Volume I counted only companies inside the study universe, while Volume III also captures vendors outside it. **Reasoned.** The comparison that does survive is relative. Whatever the counting rule, a Google AI Overview selects a materially smaller set than a conversational engine does, so a vendor competing for a slot in one is competing for a scarcer slot than in the other.

## Scarcity is not the same everywhere

**Reasoned.** A vendor with a fixed amount of evidence behind it is not equally likely to be selected across engines, because the number of slots differs before any question of merit arises. That is a structural disadvantage on the shortest-list engine and a structural opportunity on the longest-list one. It also means a single-engine score conflates two things, how good your evidence is and how many slots the engine you happened to measure was handing out. Chapter 5 at [/engine-divergence/](https://docs.broadcastwell.com/engine-divergence/) takes that apart with the cross-engine data.

## Selection is unstable in a way ranking is not

**Measured, Volume III.** Asked the identical question again in the same collection window, Google AI Overviews agreed with roughly half of its own previous vendor set, at a mean agreement of 0.499 over 62 repeat pairs, and Claude at 0.442 over 74 repeat pairs. **Reasoned.** A ranking is a stored artefact that changes when the index changes. A selection is generated at request time, so it can differ between two identical requests with nothing having changed in the world. That difference has no analogue in classical search results and it is why single-run measurement is a weaker instrument here than it was there. Chapter 6 at [/measurement-noise/](https://docs.broadcastwell.com/measurement-noise/) measures it.

## Sometimes there is no answer to be selected into

**Measured, Volume III.** Google returned an AI Overview for 92.1% of these buyer questions, 258 of 280. On the remaining 22 there was no AI answer at all. **Reasoned.** Under a ranking model there is always a results page, so the denominator is stable. Under a selection model the surface itself is conditional: on some questions the engine declines to generate, and a vendor cannot be present in an answer that does not exist. That makes the denominator a variable rather than a constant, which is a problem for anybody quoting a percentage. Chapter 7 at [/overview-trigger-rate/](https://docs.broadcastwell.com/overview-trigger-rate/) works through what it does to a score.

## The engines do not select the same names

**Measured, Volume III.** Across 142 questions answered by all of Claude, Perplexity and Google AI Overviews, 2,238 distinct vendor mentions were recorded, of which 63.3% came from a single engine and 17.5% from all three. **Reasoned.** If selection were a close proxy for some underlying quality ranking, independent systems reading a shared public evidence layer would converge much harder than that. A near two-thirds single-engine share says the candidate sets are substantially engine-specific, which is what you would expect from four different retrieval stacks selecting under four different constraints, and not what you would expect from four measurements of one ranking.

## Rank tracking has no analogue here

**Reasoned.** The daily rank check is the load-bearing habit of search engine optimisation, and it does not port. There is no position to track, the surface is regenerated per request, the set size varies by engine, and on some questions the surface does not appear. What can be tracked is presence and absence across a fixed question set, on named engines, over repeated runs, with the variance reported. That is a different instrument with a different cadence, and treating it like rank tracking produces a chart that moves for reasons which have nothing to do with the vendor.

## Link volume is the wrong lever to reach for first

**Reported.** Aggarwal and colleagues showed that content-side interventions do move visibility inside a generative engine, in work introducing generative engine optimisation as a problem (arXiv:2311.09735, KDD 2024). **Reasoned.** That establishes the surface is movable, not that the classical levers are the ones that move it. Under selection, the binding question at the first stage is whether an engine can assemble you into a candidate set from evidence it can reach, which is a question about entity presence and third-party corroboration rather than about how many links point at a page. Chapter 9 at [/category-door/](https://docs.broadcastwell.com/category-door/) sets out what that evidence has to look like.

## Two gates, which is the model this manual uses instead

**Measured, Volume II.** Across 616 absence records from 85 companies, the shape of what a company loses changes with its visibility: companies named in zero of ten answers lost category-level questions 55.3% of the time and head-to-head comparisons 20.0% of the time, while companies named seven or more times reversed that to 12.5% and 68.8%, with chi-square 61.8, df 15, p = 1.3 × 10⁻⁷. **Reasoned.** That is a selection model with two boundaries rather than one. The first is admission to the candidate set. The second is preference inside it. Chapter 2 at [/absence-ladder/](https://docs.broadcastwell.com/absence-ladder/) is the full argument.

## Why two gates beats one number

**Reasoned.** A single visibility percentage is a projection of a two-dimensional position onto one axis, and projections lose information. Two companies scoring identically can sit at different gates, and the work each needs is different in kind rather than in degree. The absence mix recovers the lost dimension at no cost, because it uses data any measurement already has: the questions you were not named in, kept with their text. The reason the industry reports one number instead is that one number is easier to sell, not that it is more informative.

## What the incumbency literature adds, and what it does not

**Reported.** Chu and Hou document an incumbent advantage in large language model product recommendation, in a single consumer category across three model interfaces rather than in production search products (arXiv:2606.17443). **Measured, Volume II.** In this dataset the related question came out null: the Spearman correlation between category leader visibility and challenger visibility was −0.051 at p = 0.64 over 85 companies. **Reasoned.** Incumbents being advantaged and challengers being suppressed by incumbents are different claims. The first is about who gets selected. The second is about crowding out, and the crowding-out version does not appear in this sample.

## The three questions the selection model makes worth asking

**Reasoned.** First, on which questions are we absent, and what do those questions have in common. Second, on which engines, since the candidate sets differ and a single-engine answer generalises poorly. Third, how stable is any of this, since a selection generated at request time carries run-to-run variance a single measurement cannot show. None of these three has a natural expression in the ranking model, which is the practical reason the ranking model has to be put down before anything useful can be measured.

## What this model does not claim

**Reasoned.** It does not claim that classical search work is wasted, that links stopped mattering, or that ranking systems have disappeared from the buyer journey. It does not claim that being selected is the same as being bought. And it does not claim that the mechanism inside any engine is literally a two-stage filter; nobody outside the providers can observe that. The claim is narrower: the measured behaviour is better described by selection from a candidate set than by ordering of a full list, and the questions that description generates are better questions.

## The honest limitation of this framing

**Measured, Volume I and Volume II.** The evidence behind this chapter is one engine with one run per question, on a challenger-skewed sample of 85 companies, plus a four-engine single-window collection in Volume III. **Reasoned.** That supports the direction of the argument and not a precise parameterisation of it. Nothing here has been tested as an intervention: no company in these datasets was measured, changed and measured again. Read the selection model as the frame that fits the observations, and hold it loosely enough to drop it if a larger or longitudinal dataset fits better.

## What this means for your buying decision

Ask any supplier which of the two gates your absence data says you are at, and whether they can show you the question-level absence list that supports the answer. A supplier who answers only with a percentage is still working in the ranking model and will prescribe accordingly. A supplier who cannot produce the absence list does not have the data to diagnose you. If the diagnosis is not framed as presence in a candidate set on named engines, you are being sold a rank-tracking habit under a new name. Chapter 12 at [/how-to-buy-geo/](https://docs.broadcastwell.com/how-to-buy-geo/) turns this into the specific questions to put to a vendor.

## Where to go next

If you want the diagnostic model in full, read Chapter 2 at [/absence-ladder/](https://docs.broadcastwell.com/absence-ladder/). If you want the size of the problem before the model, read Chapter 1 at [/named-zero-times/](https://docs.broadcastwell.com/named-zero-times/), which sets out how many companies are never named at all. If you want to know how much any single measurement can be trusted, read Chapter 6 at [/measurement-noise/](https://docs.broadcastwell.com/measurement-noise/).

## Sources

Volume I supplies the 2.05 vendors per answer, the 20% median, the 35% zero rate and the 80% leader median. Volume II supplies the absence ladder table, its chi-square and the leader null result. Volume III supplies the per-engine vendor counts, the repeat agreement figures, the 92.1% trigger rate and the consensus shares. External work is cited by author and identifier where it appears, and is reproduced from Volume III's reference list. Everything is at [github.com/Broadcastwell/state-of-geo-2026](https://github.com/Broadcastwell/state-of-geo-2026).

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
