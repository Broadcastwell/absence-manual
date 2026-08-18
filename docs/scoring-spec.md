---
title: "Appendix C. Scoring and matching specification"
headline: "Scoring and matching specification: the deterministic rules that decide whether a brand was named and whether a domain was cited"
description: "The two-layer extraction design, the text normalisation applied before matching, the word-boundary and case-sensitivity rules for brand names, hostname-level domain matching, the citation classification scheme and the completeness rules, as published in Volume III."
page_class: appendix
schema_type: TechArticle
date_published: "2026-08-18T00:00:00+00:00"
date_modified: "2026-08-18T00:00:00+00:00"
is_based_on: "https://doi.org/10.5281/zenodo.21789120"
---

# Appendix C. Scoring and matching specification

Reference material for Chapter 8 at [/valid-measurement/](https://docs.broadcastwell.com/valid-measurement/). Reproduced at exactly the level Volume III publishes it and no deeper.

## Why the rules matter more than they look

**Reasoned.** A visibility score is the output of a decision procedure applied to answer text. If that procedure is a judgement call, the score depends on who ran it. If it is a stated rule, two independent parties get the same number from the same answers. Everything in this appendix exists to make the second true.

## Two layers, with a strict ordering

**Measured, Volume III.** Layer 1 is deterministic and authoritative for every company in the study universe. Layer 2 is a language-model extractor that exists to catch vendors outside that universe, and it may only add out-of-universe names. Any Layer 2 claim about a universe company is discarded unless Layer 1 also finds the string in the answer.

**Reasoned.** That ordering is the safeguard. It means the model-based layer can widen coverage but cannot inflate or deflate a measured company's numbers in either direction, so every universe-only statistic in the study is independent of it.

## Text normalisation, applied before any matching

**Measured, Volume III.** Answer text is normalised for non-breaking and thin spaces, curly quotes and the dash family, then whitespace-collapsed. **Reasoned.** Without normalisation, a brand rendered with a typographic apostrophe fails to match the same brand rendered with a straight one, and the failure is silent. Normalisation is unglamorous and it is where a large share of avoidable scoring errors live.

## Brand matching

**Measured, Volume III.** Brand matching is word-boundary. It is case-sensitive when the brand is a single plain alphabetic word, so a company called Pitch does not match the ordinary verb. A brand carrying a dot, digit, hyphen or space matches case-insensitively.

**Reasoned.** The asymmetry is deliberate. Single common words carry a high false-positive risk and need the extra constraint of case. Names containing punctuation or digits are unlikely to appear by accident, so the constraint can be relaxed without cost. Volume III states these are Volume I's rules, unchanged, which is what makes the two volumes comparable.

## Domain matching

**Measured, Volume III.** Domain matching is at hostname level, with multi-domain values split on pipes and commas, so subdomains count and near-misses do not. **Reasoned.** Hostname level means a citation of a subdomain counts as a citation of the company, which is correct because companies publish across subdomains. It also means a domain that merely contains the company name as a substring does not count, which prevents a class of false positive that would otherwise inflate citation counts.

## Citation classification

**Measured, Volume III.** Every cited URL is reduced to a hostname and classified as vendor-owned, review platform, editorial, analyst, community or other, reusing Volume I's classification so the vendor-authored figure from that volume is comparable per engine. **Measured, Volume I.** In Volume I the same scheme carried the additional labels encyclopaedia and social, and the 100 most-cited domains were classified by hand.

**Reasoned.** Reusing a classification across volumes is what allows a like-for-like comparison. Changing a taxonomy between studies while keeping the same headline metric is a common and quiet way to make two incomparable numbers look like a trend.

## The two scored outcomes

**Measured, Volume I.** Each answer was scored on two independent binary outcomes: whether the company's brand was named, and whether its own domain was cited as a source. Every cited URL was logged. **Reasoned.** Keeping these separate is what makes Chapter 3 at [/cited-not-recommended/](https://docs.broadcastwell.com/cited-not-recommended/) possible. A measurement that blends them into one visibility figure cannot recover the distinction later.

## Completeness and exclusion rules

**Measured, Volume III.** The primary sample is the set of questions where every engine in the relevant set returned a usable answer, and pairwise metrics additionally use every question both engines in that pair answered, which is why pair sample sizes differ and are reported. Attrition is reported per engine rather than absorbed.

**Measured, Volume III.** A Google query that returns no AI Overview is recorded with its own status rather than as an error, because Google declining to generate is a result about the engine. Rows carrying a billing error are excluded from every denominator and retained in the raw data with an error status, so the exclusion is checkable.

## Repeat handling

**Measured, Volume III.** A repeat pair whose two runs used different model strings measures a model change rather than run-to-run noise and is excluded by construction. Volume III reports that no pair triggered that rule. **Measured, Volume III.** An engine needs at least 12 repeat pairs before a verdict is asserted for it.

## Reproducibility

**Measured, Volume III.** The bootstrap uses 2000 replicates with a fixed seed, so the published confidence intervals reproduce exactly, and figures are generated from the computed results file rather than typed, so a caption cannot drift from the dataset. **Reasoned.** A fixed seed is the difference between an interval a reader can verify and one they have to trust.

## What is deliberately not in this appendix

**Reasoned.** This reproduces the scoring and matching specification at the level the source volumes publish it. It does not describe how any commercial measurement is operated, scheduled or delivered, and nothing here constitutes an operable procedure for running a sweep.

## Sources

The two-layer design, normalisation, brand and domain matching rules, citation classification, completeness and exclusion rules, repeat handling and bootstrap settings are from The 2026 State of GEO, Volume III, sections 3.4 to 3.6 and 7. The two scored outcomes and the hand classification of the top 100 domains are Volume I. The extractor prompt and the analysis scripts are published in full at [github.com/Broadcastwell/state-of-geo-2026](https://github.com/Broadcastwell/state-of-geo-2026) under `volume-iii/analysis/`.

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
