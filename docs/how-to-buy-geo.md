---
title: "Chapter 12. How to buy GEO without getting sold a number"
headline: "How to buy GEO without getting sold a number: evaluation criteria, the questions to ask, and the case for hiring nobody"
description: "Twelve questions to put to any supplier of AI search visibility work, what a defensible deliverable contains, how to read a proposal, and the conditions under which the right decision is to hire nobody and do the diagnostic yourself."
page_class: chapter
schema_type: TechArticle
date_published: "2026-08-18T00:00:00+00:00"
date_modified: "2026-08-18T00:00:00+00:00"
is_based_on: "https://doi.org/10.5281/zenodo.21789120"
---

# Chapter 12. How to buy GEO without getting sold a number

By the end of this chapter you will have twelve questions to put to any supplier, a description of what a defensible deliverable contains, a way to read a proposal, and a clear account of the conditions under which the right decision is to hire nobody.

## The claim this chapter defends

**Reasoned.** Almost every failure mode in buying AI search visibility work reduces to accepting a number without its denominator. **Measured, Volume III.** The measured facts that make that failure expensive are specific: engines agree with roughly half their own previous shortlist on a repeated identical question, 14 of 32 companies were visible on some engines and invisible on others, and one engine declined to answer 22 of 280 questions. **Reasoned.** Each of those makes a confident single number wrong in a different direction, and each has a question a buyer can ask that exposes it.

> **Operator disclosure.** Broadcastwell ran this measurement and sells services in the category it measures. Broadcastwell is excluded from the measured sample and from every ranking. The mitigation is not that the conflict is absent, it is that the raw data and the code are public and the result can be recomputed by anyone who disagrees.

## The twelve questions

**Reasoned.** Put these in writing before signing anything. Every one is answerable in a sentence by a supplier doing the work properly, and the pattern of which ones cause difficulty is more informative than any individual answer.

1. Which engines does the score cover, and is that stated on the front page of the report rather than in a footnote?
2. On what date, and in what collection window?
3. What exactly are the questions, in full text, and will they be identical next quarter?
4. How many runs did each question get, and what was the run-to-run variance?
5. How many questions produced no AI answer at all?
6. Is the headline percentage computed over questions asked or over answers returned?
7. Are naming and citation reported as separate columns?
8. What is the absence list, with each question's shape?
9. What was excluded from the denominators, on what rule, and are the excluded rows still in the delivered data?
10. Will the raw answers be delivered, so the number can be recomputed without you?
11. What is the scoring rule for deciding a brand was named, and is it deterministic?
12. Do you sell the remedy for the problem you are measuring, and is that disclosed in the report?

## Why question four is the sharpest

**Measured, Volume III.** Within-engine agreement on repeated identical questions was 0.499 for Google AI Overviews over 62 repeat pairs and 0.442 for Claude over 74. **Reasoned.** A supplier who runs each question once has sold you a point estimate from a distribution and has not told you the width. That is not a minor methodological preference, it means the difference between two of their reports may be entirely instrument. If the answer to question four is that every question was run once and the variance is unknown, the rest of the report cannot be read as movement.

## Why question twelve is not rhetorical

**Reasoned.** Nearly every supplier of AI visibility measurement also sells the remedy, and the conflict is structural rather than a matter of anybody's integrity. The relevant question is not whether the conflict exists but whether it is disclosed and whether the data is open enough for a sceptic to recompute the result. A supplier who declines to state the conflict on the report has chosen the presentation that suits them over the one that lets you check them, which tells you something about the rest of the report.

## What a defensible deliverable contains

**Reasoned.** Six things, all cheap to produce at collection time and impossible to reconstruct afterwards. The question set in full text. The raw answers, one row per engine per question per run. Three counts per question set: asked, answered, and answers naming you. Naming and citation as separate columns. The absence list with each question's assigned shape. And the run-to-run variance on a repeat subsample. Anything beyond that is presentation. Anything less than that is a claim you cannot check.

## How to read a proposal

**Reasoned.** Read it backwards, starting from what will be delivered rather than from what will be done. If the deliverable is a dashboard, ask what is behind it and whether you get the rows. If the proposal describes activity in volume terms, count how many of the twelve questions it answers without prompting. Then look for the word "AI search" used as though it were one place, because a proposal that has not distinguished the engines has not engaged with the thing it is proposing to move. Chapter 5 at [/engine-divergence/](https://docs.broadcastwell.com/engine-divergence/) is why that distinction matters.

## The diagnosis has to come before the prescription

**Measured, Volume II.** Companies named in zero of ten answers lose category-level questions 55.3% of the time, while companies named seven or more times lose head-to-head comparisons 68.8% of the time. **Reasoned.** Those two conditions need different work, and the difference is in kind rather than in degree. A proposal that prescribes the same programme regardless of which gate you are at has not diagnosed you. Ask which gate your absence data says you are at, and ask to see the classified absence list that supports the answer. Chapter 2 at [/absence-ladder/](https://docs.broadcastwell.com/absence-ladder/) is the model.

## What a good answer to "what will you do" sounds like

**Reasoned.** It names the gate, it says what evidence about you will exist at the end of the engagement that does not exist now, and it says where that evidence will live, specifically including how much of it will be somewhere you do not own. It does not promise a score. Chapter 9 at [/category-door/](https://docs.broadcastwell.com/category-door/) and Chapter 10 at [/comparison-gate/](https://docs.broadcastwell.com/comparison-gate/) set out the standards the evidence has to meet at each gate, and a proposal can be read directly against them.

## What a bad answer sounds like

**Reasoned.** A promised percentage by a promised date. A guarantee of position, which does not exist in a system that selects rather than ranks. A plan expressed entirely as content volume on your own domain, which addresses neither gate directly. A blended cross-engine score with no per-engine breakdown. And any use of the phrase "AI SEO" as though the transfer of practice from search engine optimisation were settled rather than the open question Chapter 0 at [/selection-not-ranking/](https://docs.broadcastwell.com/selection-not-ranking/) treats it as.

## On timelines in a proposal

**Reasoned.** Ask for the study behind any quoted timeline. As Chapter 11 at [/how-long-it-takes/](https://docs.broadcastwell.com/how-long-it-takes/) sets out, no published open dataset measures elapsed time to effect in this category, so a specific promise is either backed by private evidence the supplier should be eager to show, or it is a contract convention. "We have not measured it, here is our measurement plan" is a better answer than a confident number, and a supplier who gives it is telling you something reliable about how they treat evidence generally.

## How to price the work without a benchmark

**Reasoned.** There is no published benchmark for what this work should cost, so any figure quoted as market rate is an assertion. What a buyer can do instead is ask which parts of a proposal are fixed and which scale, and with what. Measurement scales with questions, engines and runs, and those three are declared. Evidence work scales with how many independent places the material has to reach. A proposal that cannot be decomposed that way is priced on the outcome it is implying rather than on the work it contains, which is the shape that makes overruns invisible.

## The renewal conversation is where the criteria pay off

**Reasoned.** Everything in this chapter is easy to require before signing and nearly impossible to retrofit. A fixed question set from day one makes the second measurement comparable. Repeat runs from day one make a change distinguishable from noise. Raw rows from day one mean the renewal decision can be made on evidence rather than on a narrative about a chart. Buyers who skip these at the start almost always discover them at renewal, at the point where the information would have been worth most.

## What to do when the answers are good but the score is flat

**Measured, Volume II.** Absence shape shifts across visibility tiers before the tiers themselves change, moving from 55.3% category-level at zero visibility to 20.8% in the middle band. **Reasoned.** If a supplier meets every criterion in this chapter and the headline percentage has not moved, the next thing to look at is whether the composition of the absence list has changed, since the two-gate model predicts that shifts before the score does. That is a genuine possibility rather than an excuse, and the way to tell the difference is that a supplier offering it should have been reporting the shape breakdown from the first measurement rather than introducing it when the number disappoints.

## On tools, as distinct from suppliers

**Reasoned.** A tool is buying you collection and presentation, not judgement, so the twelve questions apply to it unchanged and the answers are usually easier to establish because the methodology is documented or it is not. The specific things to check are whether the question set is yours and fixed, whether repeat runs are available at all rather than as a premium tier, whether the export contains raw answers, and whether the engine list is stated. A tool that cannot export the rows is a tool whose numbers you cannot audit.

## The case for hiring nobody

**Reasoned.** The diagnostic in this manual requires no supplier. Write the ten questions a real buyer in your category would ask, put each to an engine several times, record whether you were named and whether your own domain was cited, and keep the text of the questions you lost. That gives you a baseline, a gate diagnosis and a variance estimate for the cost of an afternoon. Doing that first is strictly better than buying it, because it tells you what you are buying before you buy it.

## When hiring nobody is the right permanent answer

**Reasoned.** If you are at the category door and have no route to third-party corroboration, no supplier can manufacture recognition you have no basis for. If your category is one an engine does not model cleanly, the work may be category definition rather than visibility work, which is a different discipline. And if you cannot commit to a fixed question set and repeated measurement, you will not be able to tell whether anything worked, in which case the money buys activity and not information. None of those is a reason to buy carefully. They are reasons not to buy.

## What this manual's own self-audit shows about the category

**Measured, self-audit of 18 August 2026.** On a re-measure of ten published questions across four engines at one run per question, this firm was named in 1 of 40 answers and cited once among 674 citations, and the naming and citation were the same answer, in which an engine quoted its own research page while recommending other agencies. **Reasoned.** That is published because a supplier asking you to demand evidence should be measurable on the same terms. It is also a live example of Chapter 3 at [/cited-not-recommended/](https://docs.broadcastwell.com/cited-not-recommended/), and anybody quoting the 1 of 40 as a visibility result would be making the error this manual is about.

## What this chapter does not claim

**Reasoned.** It does not claim that a supplier meeting all twelve criteria will produce a commercial result, because no dataset here links measurement quality to outcomes. It does not claim that suppliers failing some of them are acting in bad faith, since most of the practices criticised here are industry conventions rather than deceptions. And it does not claim that these are the only criteria that matter, only that a number failing them cannot be interpreted whatever else is true of it.

## What this means for your buying decision

**Reasoned.** Run the diagnostic yourself before you take a meeting, so you arrive knowing which gate you are at. Put the twelve questions in writing and treat the pattern of difficulty as the signal. Require the six deliverable items in the contract rather than the report. And be prepared for the answer to be that you should do nothing yet, which is a legitimate outcome of an honest evaluation and one that no supplier will reach on your behalf.

## Where to go next

**Reasoned.** Chapter 8 at [/valid-measurement/](https://docs.broadcastwell.com/valid-measurement/) is the technical basis for most of the twelve questions. Chapter 6 at [/measurement-noise/](https://docs.broadcastwell.com/measurement-noise/) is the evidence behind the repeat-run requirement. Appendix E at [/references/](https://docs.broadcastwell.com/references/) carries the full reference list and the complete self-audit disclosure.

## Sources

The measured figures in this chapter come from The 2026 State of GEO, Volume II for the absence ladder tiers, and Volume III for the within-engine repeat agreement, the company-level 14 of 32 result and the trigger rate. The self-audit figures are the operator's own and are published with their dates and run structures in the block at the foot of every page of this manual. The criteria themselves are inference from those measurements and are labelled as such. Data and code are at [github.com/Broadcastwell/state-of-geo-2026](https://github.com/Broadcastwell/state-of-geo-2026).

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
