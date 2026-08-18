---
title: "The Absence Manual"
headline: "The Absence Manual: a technical manual on AI search visibility for B2B software"
description: "A free, ungated technical manual on measuring and fixing AI search visibility, built entirely from three published open datasets with DOIs. One chapter per URL. No form, no login, no paywall."
schema_type: TechArticle
page_class: page
date_published: "2026-08-18T00:00:00+00:00"
date_modified: "2026-08-18T00:00:00+00:00"
image: "figures/absence-ladder.png"
is_based_on: "https://github.com/Broadcastwell/state-of-geo-2026"
---

# The Absence Manual

## What this is

The Absence Manual is a technical manual on AI search visibility for B2B software: how to measure how often an AI answer names your company, how to read what that measurement does and does not tell you, and what the evidence actually supports doing about it. Every finding in it is drawn from three already-published studies with DOIs, open data and open analysis code. It is free, ungated and permanently online. There is no form, no login, no paywall and no email field anywhere on this site, because an AI crawler issues a plain HTTP request and cannot fill in a form. A gated manual about citability would refute itself.

**Author.** Sairam Sivakumar, Broadcastwell.

> **Operator disclosure.** Broadcastwell ran this measurement and sells services in the category it measures. Broadcastwell is excluded from the measured sample and from every ranking. The mitigation is not that the conflict is absent, it is that the raw data and the code are public and the result can be recomputed by anyone who disagrees.

## What it is built from

| Volume | What it covers | DOI |
|-|-|-|
| Volume I | 85 B2B software companies, 61 categories, 860 scored answers, 5,160 traced citations across 1,753 unique domains, one engine held constant. See FLAGS.md on the question count | [10.5281/zenodo.21537014](https://doi.org/10.5281/zenodo.21537014) |
| Volume II | The Absence Ladder. All 616 absence records classified by question shape | [10.5281/zenodo.21586091](https://doi.org/10.5281/zenodo.21586091) |
| Volume III | Cross-engine divergence. 280 questions, 40 categories, four engines, 853 answers collected 05:28 to 16:29 UTC on 2026-08-04, with a 25-question repeat subsample run three times | [10.5281/zenodo.21789120](https://doi.org/10.5281/zenodo.21789120) |

All three are CC BY 4.0, with their data and analysis code at [github.com/Broadcastwell/state-of-geo-2026](https://github.com/Broadcastwell/state-of-geo-2026).

## How to read the evidence labels

Every substantive claim in this manual carries one of three labels, so you always know what kind of thing you are being told. This is the manual's central discipline and it is applied without exception.

**Measured.** The claim comes from one of the three volumes, and the volume is named in the same sentence or the label. You can recompute it from the published data.

**Reported.** The claim comes from a source outside this research programme, cited with its publisher and date. You should check it at the source.

**Reasoned.** The claim is an inference drawn from the measured or reported material above it. It is argument, not measurement, and it is marked so you can disagree with the reasoning without disputing the data.

A claim with no label is a defect. If you find one, it is a mistake and it will be corrected.

## How to read it

Every chapter has its own permanent URL and stands alone. Statistics carry their sample size in the sentence that states them. Limitations are stated in the body of the argument rather than collected at the end where they can be skipped. Where the evidence is strong the claim is unhedged, and where it is thin the chapter says so and names the base it rests on. Where a number is missing or two published sources disagree, the manual flags the gap rather than filling it with a plausible value.

## Chapters

| No. | Chapter | Status |
|-|-|-|
| 0 | [Selection, not ranking](selection-not-ranking.md) | Published |
| 1 | [One in three vendors is never named](named-zero-times.md) | Published |
| 2 | [The Absence Ladder](absence-ladder.md) | Published |
| 3 | [Cited is not recommended](cited-not-recommended.md) | Published |
| 4 | [Who the engines actually cite](who-gets-cited.md) | Published |
| 5 | [One engine is not four](engine-divergence.md) | Published |
| 6 | [Your score is noisier than your vendor admits](measurement-noise.md) | Published |
| 7 | [The AI Overview does not always appear](overview-trigger-rate.md) | Published |
| 8 | [What a valid measurement requires](valid-measurement.md) | Published |
| 9 | [Getting named at the category door](category-door.md) | Published |
| 10 | [Getting quoted at the comparison gate](comparison-gate.md) | Published |
| 11 | [How long this actually takes](how-long-it-takes.md) | Published |
| 12 | [How to buy GEO without getting sold a number](how-to-buy-geo.md) | Published |

## Appendices

| No. | Appendix | Status |
|-|-|-|
| A | The ten-question buyer bank | Forthcoming |
| B | Absence classification rules and precedence | Forthcoming |
| C | Scoring and matching specification | Forthcoming |
| D | Glossary | Forthcoming |
| E | References and self-audit disclosure | Forthcoming |

Chapters marked forthcoming have no URL yet. A slug published once is permanent: version numbers change, URLs never do. See the [changelog](https://github.com/Broadcastwell/absence-manual/blob/main/CHANGELOG.md).

## Notes

Short standalone pieces cut from the chapters, each linking back to its parent.

- [Same score, different problem](posts/same-score-different-problem.md), from Chapter 2.
- [Half its own shortlist](posts/half-its-own-shortlist.md), from Chapter 6.

## Licence and status

Prose and figures are published under CC BY 4.0. The site code is MIT. Nothing here has been through academic peer review: it is measurement published with the data and code that produced it, and the standing invitation is to recompute any figure you doubt from the public files and publish what you get. In the four-engine, five-run self-audit published alongside Volume II in July 2026, Broadcastwell was named in 0 of 200 answers and cited 0 times among 663 citations. Re-measured on the same ten questions and the same four engines on 18 August 2026, at one run per question rather than five, it was named in 1 of 40 answers and cited once among 674 citations. Both figures stand with their dates and neither replaces the other.

*Version 1.0, August 2026.*
