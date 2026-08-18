---
title: "Appendix D. Glossary"
headline: "Glossary: every term this manual uses in a specific sense, with one definition each"
description: "Definitions for the terms used in a specific technical sense across The Absence Manual, including the evidence levels, the two gates, the agreement measures, the denominator vocabulary and the scoring layers."
page_class: appendix
schema_type: TechArticle
date_published: "2026-08-18T00:00:00+00:00"
date_modified: "2026-08-18T00:00:00+00:00"
is_based_on: "https://github.com/Broadcastwell/state-of-geo-2026"
---

# Appendix D. Glossary

One definition per term. Where a term comes from a source volume the volume is named in the entry, which stands in place of an evidence label: a definition is a statement about usage rather than a claim about the world, so the three-level scheme used everywhere else in this manual does not apply here. Where a term is this manual's own coinage that is stated explicitly.

## The evidence levels

**Measured.** A claim taken from one of the three State of GEO volumes, with the volume named, recomputable from the published data.

**Reported.** A claim taken from a source outside this research programme, cited with its publisher or authors and a date or identifier.

**Reasoned.** An inference drawn from measured or reported material. Argument rather than measurement, marked so it can be disputed without disputing the data. This three-level scheme is this manual's own convention.

## The unit of analysis

**Answer.** One response from one engine to one question on one run. The unit everything else is counted over.

**Named.** Volume I and II. A binary outcome recording that the subject company's brand string appeared in the answer text under the matching rules in Appendix C at [/scoring-spec/](https://docs.broadcastwell.com/scoring-spec/).

**Cited.** Volume I and II. A separate binary outcome recording that the subject company's own domain appeared among the sources the engine cited for that answer.

**Absence record.** Volume II. One question on which the subject company was not named, retained with its full question text.

**Absence list.** This manual's term for the set of a company's own absence records.

## The model

**Selection, not ranking.** This manual's framing, Chapter 0 at [/selection-not-ranking/](https://docs.broadcastwell.com/selection-not-ranking/). The observation that an AI answer is assembled by choosing a small number of vendors from a candidate set rather than by ordering a full list.

**Candidate set.** The group of vendors an engine assembles before writing an answer. Not directly observable from outside; inferred from which vendors appear.

**Category door.** This manual's term for the first gate: whether an engine treats a company as a member of its category at all.

**Comparison gate.** This manual's term for the second gate: whether an engine prefers a company over a specific named rival.

**Absence ladder.** Volume II. The finding that the mix of question shapes a company loses shifts systematically as its visibility rises.

**Visibility tier.** Volume II. One of four bands grouping companies by score: named 0 of 10, 1 to 3, 4 to 6, and 7 to 10.

## Question vocabulary

**Question bank.** The fixed set of buyer questions a measurement is computed over. See Appendix A at [/question-bank/](https://docs.broadcastwell.com/question-bank/).

**Question shape.** Volume II. One of six categories a question is assigned to by rule: head-to-head comparison, alternatives-to-incumbent, best-of shortlist, evaluation criteria, use case or problem, definitional.

**Precedence.** Volume II. The fixed order in which shape rules are applied, so a question matching two rules lands deterministically in one shape.

**Category-level.** Volume II. Best-of shortlist plus alternatives-to-incumbent, collapsed into one bucket because both ask who belongs in a set rather than adjudicating between two named vendors.

## Agreement and variance

**Jaccard similarity.** Volume III. The size of the intersection of two vendor sets divided by the size of their union. 1.0 means identical shortlists.

**Overlap coefficient.** Volume III. An agreement measure normalised by the smaller of the two sets, used as a length control because it cannot be depressed by one side simply being longer.

**Repeat pair.** Volume III. Two runs of the same question on the same engine, compared with each other.

**Within-engine agreement.** Volume III. Mean agreement across repeat pairs on one engine. The engine's agreement with itself.

**Between-engine agreement.** Volume III. Mean agreement between one engine and the others on the same questions.

**Noise floor.** This manual's term for an engine's within-engine agreement, used as the threshold any claimed difference has to exceed to be interpretable.

**Fleiss kappa.** Volume III. A chance-corrected agreement statistic treating engines as raters making a binary mention decision.

**Bootstrap.** Volume III. Resampling used to produce confidence intervals, run at 2000 replicates with a fixed seed so the intervals reproduce exactly.

## Denominator vocabulary

**Trigger rate.** Volume III. The share of questions on which an engine returned a generated answer at all.

**No AI Overview.** Volume III. A recorded status meaning Google returned no AI Overview for that question, kept distinct from an error because it is a result about the engine.

**Answer rate.** Volume III. Answers returned divided by questions attempted, per engine.

**Unstated denominator.** This manual's term for a reported percentage whose base has not been declared.

## Scoring vocabulary

**Study universe.** Volume III. The set of companies, domains, competitors and aliases the deterministic matching layer knows about.

**Layer 1.** Volume III. The deterministic matching layer, authoritative for every company in the study universe.

**Layer 2.** Volume III. A language-model extraction layer that may only add vendors from outside the study universe and can never override Layer 1 about a universe company.

**Vendor-authored.** Volume I. A citation classification for a source published on a software vendor's own domain.

**Evidence layer.** This manual's term for the set of sources engines cite when composing answers about a category.

## Sample vocabulary

**Challenger-skewed.** Volume I and II. A sample selected as plausible non-leaders in categories with an identifiable incumbent, which lowers average named rates relative to a random draw of all vendors.

**Category leader.** Volume II. The brand scoring highest in a category's sweep. Leaders enter the data through mentions rather than through selection.

**Winner-take-most.** Volume I. The observed shape in which a small group of names is selected repeatedly while a large group is selected almost never.

**Collection window.** The period during which answers were gathered. Part of the value of any figure, not metadata on it.

## Disclosure vocabulary

**Operator disclosure.** The statement, carried on every page of this manual, that the firm running the measurement sells services in the category it measures, is excluded from the sample and from every ranking, and publishes the raw data and code so the result can be recomputed.

**Self-audit.** A measurement the operator runs against itself on its own published question set, reported with its date and run structure. Both self-audit figures appear in the block at the foot of every page and in Appendix E at [/references/](https://docs.broadcastwell.com/references/).

**Concept DOI.** A Zenodo identifier covering all versions of a record, which resolves to the latest. Not a version and not cited in place of one.

**Version DOI.** A Zenodo identifier for one specific published version. The three volumes are cited by version DOI throughout.

## Sources

Terms attributed to a volume are used in the sense that volume defines. Terms marked as this manual's own are conventions adopted here for clarity and carry no external authority. The underlying data and code are at [github.com/Broadcastwell/state-of-geo-2026](https://github.com/Broadcastwell/state-of-geo-2026).

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
