---
title: "Chapter 8. What a valid measurement requires"
headline: "What a valid measurement requires: the criteria a buyer should demand before accepting an AI visibility number"
description: "Six requirements a visibility measurement has to meet before its number means anything: a fixed and published question bank, repeat runs, a named engine set, a deterministic scoring rule, stated denominators, and disclosed exclusions. Plus the failure modes that void a number entirely."
page_class: chapter
schema_type: TechArticle
date_published: "2026-08-18T00:00:00+00:00"
date_modified: "2026-08-18T00:00:00+00:00"
is_based_on: "https://doi.org/10.5281/zenodo.21789120"
---

# Chapter 8. What a valid measurement requires

By the end of this chapter you will have a list of requirements you can hold any supplier's visibility number against, and a shorter list of failure modes that make a number meaningless regardless of how it was produced. This chapter is written as criteria for a buyer, not as a procedure for an operator.

## The claim this chapter defends

**Reasoned.** A visibility number is only interpretable if six things are true of it: the question bank was fixed before collection and is published, each question was run more than once, the engine set is named, the scoring rule is deterministic and stated, the denominator is declared, and every exclusion is disclosed. **Measured, Volume III.** Each of those requirements exists because a published measurement demonstrated what goes wrong without it, and the failure modes at the end of this chapter are all observed rather than hypothetical.

> **Operator disclosure.** Broadcastwell ran this measurement and sells services in the category it measures. Broadcastwell is excluded from the measured sample and from every ranking. The mitigation is not that the conflict is absent, it is that the raw data and the code are public and the result can be recomputed by anyone who disagrees.

## Requirement one: the question bank is fixed before collection

**Measured, Volume III.** Of 280 questions, 276 came from the study's existing question bank and 4 from the published Volume I dataset. No question was regenerated. **Reasoned.** A bank that can be regenerated between measurements is a bank that can be tuned, deliberately or not, toward questions the subject happens to do well on. Fixing it in advance removes that degree of freedom. The test for a buyer is simple: ask whether the questions used this quarter are byte-identical to the questions used last quarter, and ask to see both.

## Requirement two: the bank is published in full

**Reasoned.** Publishing the bank is what makes a score checkable by somebody who did not run it. Without the question text, a reader cannot tell whether a high score reflects broad presence or a bank weighted toward definitional questions where almost everyone appears. It also prevents the quiet substitution of brand-name questions, which measure whether an engine knows a company exists rather than whether it competes. Appendix A at [/question-bank/](https://docs.broadcastwell.com/question-bank/) sets out the design rules at the level the source volumes publish them.

## Requirement three: the bank covers the shapes that matter

**Measured, Volume III.** Each category was required to carry at least one best-of, one alternatives, one comparison, one use-case and one pricing or evaluation question. 33 of 40 categories met that in full, and the 7 that did not are listed explicitly in the published sample manifest rather than quietly padded. **Reasoned.** Shape coverage matters because Chapter 2 at [/absence-ladder/](https://docs.broadcastwell.com/absence-ladder/) shows absence concentrating in different shapes at different visibility levels. A bank missing a shape cannot detect the gate that shape diagnoses.

## Why listing the seven gaps is the point

**Reasoned.** A study that declares 33 of 40 rather than reporting full coverage is telling you where its own instrument is incomplete. That disclosure costs nothing to make and is almost never made, which is why its presence is a useful signal about everything else in the report. When a supplier says their coverage is complete, ask which categories were short and what they did about it. Silence there usually means padding rather than perfection.

## Requirement four: every question is run more than once

**Measured, Volume III.** A stratified subsample of 25 questions, balanced across shapes, was run three times on all four engines, and an engine needed at least 12 repeat pairs before a verdict was asserted for it. **Measured, Volume III.** Within-engine agreement came out at 0.499 for Google AI Overviews over 62 repeat pairs and 0.442 for Claude over 74. **Reasoned.** Engines agree with roughly half of their own previous shortlist on a repeated identical question. One run therefore samples a distribution and reports a point, and the point is presented as though it were the distribution.

## How many repeats is enough

**Reasoned.** Three runs on a stratified subsample is the minimum this manual can point at a published precedent for, and it is a floor rather than a target. What matters more than the count is that the repeats exist, that they are run in the same window as the main collection, and that the variance they reveal is reported alongside the headline rather than in an appendix. A supplier who runs everything once and offers to run more for a fee has priced a correctness requirement as an upgrade.

**Reported.** Schulte, Bleeker and Kaufmann argue that a single visibility measurement is close to meaningless because the same query produces a distribution rather than a value, and that visibility should be measured repeatedly (arXiv:2604.07585).

## Requirement five: the engine set is named on the front page

**Measured, Volume III.** Of 32 measured companies tested on at least two engines, 14 were visible on some and invisible on others. **Reasoned.** For nearly half the sample the verdict depends on which engine was asked, so a report headed "AI search visibility" without an engine list is not describing a measurable quantity. The disclosure has to be prominent rather than a footnote, because a reader who takes the headline at face value will act on a claim the data does not support. Chapter 5 at [/engine-divergence/](https://docs.broadcastwell.com/engine-divergence/) has the underlying numbers.

## Requirement six: the scoring rule is deterministic and published

**Measured, Volume III.** Brand matching is word-boundary and case-sensitive when the brand is a single plain alphabetic word, so a company called Pitch does not match the ordinary verb, while a brand carrying a dot, digit, hyphen or space matches case-insensitively. Domain matching is at hostname level with multi-domain values split, so subdomains count and near-misses do not. **Reasoned.** Rules like these are boring and they are the difference between a score two people can reproduce and a score that depends on who ran it. Appendix C at [/scoring-spec/](https://docs.broadcastwell.com/scoring-spec/) reproduces the specification at the level the source publishes it.

## Where a language model may and may not be used in scoring

**Measured, Volume III.** The deterministic layer is authoritative for every company in the study universe. A second, model-based extraction layer exists only to catch vendors outside that universe, and any claim it makes about a universe company is discarded unless the deterministic layer also finds the string in the answer. **Reasoned.** That ordering is the safeguard: it means the model-based layer can widen coverage but cannot inflate or deflate a measured company's numbers in either direction. A supplier whose headline score depends on a model's judgement about whether you were mentioned has no such safeguard.

## Requirement seven: the denominator is declared

**Measured, Volume III.** Google returned an AI Overview on 258 of 280 questions. **Reasoned.** A score computed over answers that appeared is a different quantity from a score computed over questions asked, and the two differ by however many questions produced no answer. Any report should carry three counts, questions asked, answers returned and answers naming the subject, from which everything else can be derived. Chapter 7 at [/overview-trigger-rate/](https://docs.broadcastwell.com/overview-trigger-rate/) works through the size of the effect.

## Requirement eight: exclusions are disclosed and the raw rows retained

**Measured, Volume III.** Rows carrying a billing error were excluded from every denominator and retained in the raw data with an error status, so the exclusion is checkable. **Reasoned.** Every measurement drops something. The distinction between an honest measurement and a flattering one is whether the dropped rows are visible. Ask what was excluded, on what rule, and whether the excluded rows are still in the delivered data. A supplier who cannot answer has either not recorded exclusions or does not want them counted.

## Requirement nine: the operator's own position is declared

**Measured, Volume III.** The study that supplies most of this chapter carries an operator disclosure stating that the firm running the measurement sells services in the category it measures, that it is excluded from the sample and from every ranking, and that the mitigation is publication rather than the absence of the conflict. **Reasoned.** Every commercial visibility measurement has this conflict. The question is not whether it exists but whether it is stated and whether the data is open enough that a sceptic can recompute the result. A supplier who both measures you and sells you the remedy should say so on the first page.

## Failure mode zero: the number that has never been checked against itself

**Measured, Volume III.** The study reports its own repeat-run agreement rather than assuming stability, and reports it per engine rather than pooled. **Reasoned.** The cheapest possible integrity check on any measurement instrument is to point it at the same thing twice and see whether it agrees. A supplier who has never done that with their own tool does not know its precision, which means they cannot tell you whether a change between two reports is a change in your visibility or a change in nothing at all. Ask when they last measured their own repeatability and what the answer was.

## Failure mode one: the pooled mean with an unstated denominator

**Measured, Volume III.** Pooled across engines, within-engine agreement was 0.468 over 136 repeat pairs against between-engine 0.247 over 51 pairs, and 54.4% of those within-engine pairs came from one engine. **Reasoned.** A pooled figure is dominated by whichever engine contributed most, so it can report a separation that only one engine actually has. Volume III declines to headline it for that reason. When a supplier gives you one blended number across engines, ask how many observations each engine contributed.

## Failure mode two: the number with no date

**Reported.** Semrush reports that the share of commercial search results carrying an AI Overview grew 71 percent between November 2025 and April 2026, published 2 July 2026. **Reasoned.** The surfaces being measured are changing fast enough that a figure without a collection window cannot be compared with anything, including a later figure from the same supplier. A date is not metadata on a visibility score. It is part of the value.

## Failure mode three: the score that cannot be recomputed

**Reasoned.** If the question set, the raw answers and the scoring rule are not delivered with the number, nobody can check it, including the buyer paying for it. This is the requirement most commercial tools fail, and it is the one worth being least flexible about, because every other requirement in this chapter is unverifiable without it. A deliverable that consists of a dashboard and no underlying rows is a claim, not a measurement.

## What this chapter deliberately does not provide

**Reasoned.** This is a list of criteria for judging a measurement, not a procedure for producing one. The published protocol behind the three volumes is available in full in the source repository for anyone who wants to replicate it, and the appendices to this manual reproduce it at exactly the level the volumes already publish and no deeper. Nothing here describes how any commercial measurement is operated, and a reader looking for that will not find it in this manual.

## The honest limitation of these criteria

**Reasoned.** These requirements are drawn from what the three volumes did and from what went wrong when parts of it were missing. They are not validated against outcomes, because no dataset here links measurement quality to commercial results. A measurement can satisfy every requirement in this chapter and still be measuring something a buyer does not care about. What the criteria guarantee is that the number means what it says, which is a lower bar than being useful and a necessary one.

## What this means for your buying decision

Put the eight requirements to a supplier in writing before you sign, and treat any that cannot be answered in a sentence as a finding rather than a formality. The three that most often fail are repeat runs, the declared denominator, and delivery of the raw rows. If a supplier meets all eight, the number they give you may still be uninteresting, but it will at least be a number. Chapter 12 at [/how-to-buy-geo/](https://docs.broadcastwell.com/how-to-buy-geo/) turns this list into the specific questions to ask.

## Where to go next

Chapter 12 at [/how-to-buy-geo/](https://docs.broadcastwell.com/how-to-buy-geo/) is the buyer-side companion to this chapter. Appendix A at [/question-bank/](https://docs.broadcastwell.com/question-bank/), Appendix B at [/absence-rules/](https://docs.broadcastwell.com/absence-rules/) and Appendix C at [/scoring-spec/](https://docs.broadcastwell.com/scoring-spec/) reproduce the published protocol the requirements are drawn from. Chapter 6 at [/measurement-noise/](https://docs.broadcastwell.com/measurement-noise/) is the evidence behind the repeat-run requirement.

## Sources

The requirements in this chapter are drawn from the published methods and results of The 2026 State of GEO, Volume III: the fixed question bank and its provenance, the shape coverage requirement and the 33 of 40 disclosure, the repeat subsample and the 12-pair threshold, the within-engine agreement figures, the two-layer scoring rule and its precedence, the trigger rate and its denominators, and the exclusion policy for billing errors. The company-level 14 of 32 result is also Volume III. External work is cited by author and identifier and reproduced from Volume III's reference list. Everything is at [github.com/Broadcastwell/state-of-geo-2026](https://github.com/Broadcastwell/state-of-geo-2026).

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
