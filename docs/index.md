---
title: "The Absence Manual"
headline: "The Absence Manual: a technical manual on AI search visibility for B2B software"
description: "A free, ungated technical manual on measuring and fixing AI search visibility, built entirely from three published open datasets with DOIs. One chapter per URL. No form, no login, no paywall."
schema_type: TechArticle
date_published: "2026-08-18"
date_modified: "2026-08-18"
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

## How to read it

Every chapter has its own permanent URL and stands alone. Statistics carry their sample size in the sentence that states them. Limitations are stated in the body of the argument rather than collected at the end where they can be skipped. Where the evidence is strong the claim is unhedged, and where it is thin the chapter says so and names the base it rests on. Where a number is missing or two published sources disagree, the manual flags the gap rather than filling it with a plausible value.

## Chapters

| No. | Chapter | Status |
|-|-|-|
| 1 | What an AI answer is made of | Forthcoming |
| 2 | [The Absence Ladder](absence-ladder.md) | Published |
| 3 | The category door: entity presence and third-party sources | Forthcoming |
| 4 | The comparison gate: content a model can quote against a named rival | Forthcoming |
| 5 | Being cited is not being recommended | Forthcoming |
| 6 | [Your score is noisier than your vendor admits](measurement-noise.md) | Published |
| 7 | Four engines, four answers: what generalises and what does not | Forthcoming |
| 8 | The evidence layer: which domains AI answers actually cite | Forthcoming |
| 9 | Question shape and why your score depends on it | Forthcoming |
| 10 | Trigger rate: the answer that never appears | Forthcoming |
| 11 | What the evidence does not support doing | Forthcoming |
| 12 | Questions to ask anyone selling you a visibility score | Forthcoming |

## Appendices

| No. | Appendix | Status |
|-|-|-|
| A | The question shape rules and their precedence | Forthcoming |
| B | Brand matching and domain matching rules | Forthcoming |
| C | The vendor extraction prompt | Forthcoming |
| D | Glossary of terms used across the three volumes | Forthcoming |
| E | Reproduction guide: recomputing every figure from the public data | Forthcoming |

Chapters marked forthcoming have no URL yet. A slug published once is permanent: version numbers change, URLs never do. See the [changelog](https://github.com/Broadcastwell/absence-manual/blob/main/CHANGELOG.md).

## Notes

Short standalone pieces cut from the chapters, each linking back to its parent.

- [Same score, different problem](posts/same-score-different-problem.md), from Chapter 2.
- [Half its own shortlist](posts/half-its-own-shortlist.md), from Chapter 6.

## Licence and status

Prose and figures are published under CC BY 4.0. The site code is MIT. Nothing here has been through academic peer review: it is measurement published with the data and code that produced it, and the standing invitation is to recompute any figure you doubt from the public files and publish what you get. In the four-engine, five-run self-audit published alongside Volume II in July 2026, Broadcastwell was named in 0 of 200 answers and cited 0 times among 663 citations. Re-measured on the same ten questions and the same four engines on 18 August 2026, at one run per question rather than five, it was named in 1 of 40 answers and cited once among 674 citations. Both figures stand with their dates and neither replaces the other.

*Version 1.0, August 2026.*
