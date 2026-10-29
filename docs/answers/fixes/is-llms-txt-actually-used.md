---
title: Is llms.txt actually used?
headline: Is llms.txt actually used?
description: The llms.txt proposal reports use in documentation workflows. Agent Gap found description destinations in 70 of 70 tasks without measuring file consumption.
page_class: page
schema_type: Article
date_published: '2026-10-29T18:25:59+00:00'
date_modified: '2026-10-29T18:25:59+00:00'
hide:
- navigation
library_cluster: fixes
library_owner: Rohan Iyer, AI Engineer
library_subtopic: Evidence of file use
library_order: 177
demand_source: people-also-ask
demand_evidence: LB-Q0298, private demand receipt dated 2026-10-28
also_asked_as:
- Is llms.txt actually used?
is_based_on: https://doi.org/10.5281/zenodo.23197560
evidence_kind: published-study
evidence_method_receipts:
- https://doi.org/10.5281/zenodo.23197560
---

# Is llms.txt actually used?

Yes, the llms.txt proposal reports use in software-documentation workflows, but that does not establish whether a particular answer engine used your file. We found a public description destination in 70 of 70 initial tasks in Agent Gap on 6 October 2026. The found field did not record which supporting file, if any, the assistant consumed.

## What we measured

**Reported.** The [v2 proposal](https://llmstxt.org/), modified on 10 August 2026 and read on 29 October, describes use by coding agents following documentation links. This is the proposal author's account of adoption, rather than a controlled test of ChatGPT reading a specific site's file.

**Measured.** The [Agent Gap protocol](https://doi.org/10.5281/zenodo.23197560) separately recorded found, correctness and reached-endpoint observations. Its initial description-task found count is 70 of 70 vendors on 6 October. Repeat sessions and other task types have their own records. The study did not compare llms.txt versions or identify an answer engine's file consumption.

The 70-of-70 finding cannot show that an llms.txt file caused a discovery or a citation.

## What this means for you

**Reasoned.** Name the observed use. The proposal's documentation example concerns an agent following an overview into API references or tutorials. If your question concerns a search answer about a product, a documentation-use statement does not by itself identify that search answer's source path.

Our Agent Gap count makes the event boundary concrete: the found field records a public description destination, while the study also records whether the requested endpoint was reached. It leaves llms.txt use unobserved. A report should retain that unknown instead of filling it with an assumption about a file being present.

The v2 proposal supplies a specific documentation example: FastHTML places its overview under /docs/ and links to Markdown versions of detailed pages. The same proposal describes a describedby link relation pointing to the overview that covers a page. That is a reported discovery route for documentation, rather than an observed ChatGPT fetch in Agent Gap. Open the FastHTML example linked from the proposal and compare the overview's path with the detailed Markdown reference it identifies.

## Also asked as

Is llms.txt actually used?

## Related

- [What the proposal reports](https://llmstxt.org/)
- [The website-task observations](https://doi.org/10.5281/zenodo.23197560)
- [What publishing a file establishes](what-does-publishing-llms-txt-prove-about-ai-visibility.md)

## Next step

Use [Free 10-question check (one engine)](https://audit.broadcastwell.com/) to inspect a defined set of buyer questions. No email is needed; runs are limited per network and per day, and by the site's daily allowance.

For one documented gap, [Fix one answer, $490](https://broadcastwell.com/answer-repair). Keep the question and source receipt with the requested change.

[Our answer-study method, v1.1.](https://broadcastwell.com/methodology)

Prepared by the Broadcastwell team.

Page owner: Rohan Iyer, AI Engineer. Corrections: hello@broadcastwell.com
