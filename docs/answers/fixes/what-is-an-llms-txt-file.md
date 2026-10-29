---
title: What is an llms.txt file?
headline: What is an llms.txt file?
description: The llms.txt v2 proposal describes a Markdown overview with links. Agent Gap reached 67 of 70 description endpoints without testing the file.
page_class: page
schema_type: Article
date_published: '2026-10-29T18:27:16+00:00'
date_modified: '2026-10-29T18:27:16+00:00'
hide:
- navigation
library_cluster: fixes
library_owner: Rohan Iyer, AI Engineer
library_subtopic: File definition and scope
library_order: 185
demand_source: google-autocomplete
demand_evidence: LB-Q0305, private demand receipt dated 2026-10-28
also_asked_as:
- What is an llms.txt file?
is_based_on: https://doi.org/10.5281/zenodo.23197560
evidence_kind: published-study
evidence_method_receipts:
- https://doi.org/10.5281/zenodo.23197560
---

# What is an llms.txt file?

The llms.txt v2 proposal defines a short Markdown overview with background and links to detailed content under its path. It gives you a way to describe a site's material to an assistant. Agent Gap separately recorded 67 of 70 initial description tasks reaching their public endpoint on 6 October 2026, without testing llms.txt. That distinction matters when someone presents a file as proof of usable product information.

## What we measured

**Reported.** The [proposal at llmstxt.org](https://llmstxt.org/), modified on 10 August 2026 and read on 29 October, describes files at a site's root or a subpath. Its specified format starts with a first-level project or site heading. A summary, explanatory text and second-level sections of links can follow. The document still describes a proposal.

**Measured.** The [Agent Gap protocol](https://doi.org/10.5281/zenodo.23197560) records 67 of the 70 initial description tasks reaching their public-website endpoint on 6 October. This result concerns the website task, without an llms.txt comparison or an engine-consumption observation.

The study cannot establish that adding the file makes an assistant use or cite your content.

## What this means for you

**Reasoned.** Define the covered path. Under the v2 proposal, a file at a documentation subpath describes that part of the site, while the root file can cover the wider site. Where several files apply, the proposal tells an agent to use the most specific one. A documentation-only overview should therefore identify that scope clearly.

The file's links do much of the work. V2 proposes links to clean Markdown versions of detailed pages, with standard link relations to help a client discover them. Its overview is meant to remain concise while the fuller material stays at those destinations. An extensive product claim in a summary still needs a working, relevant destination.

Keep access rules separate. The proposal describes llms.txt as context that complements robots.txt. It does not make an overview an instruction granting a crawler permission to fetch restricted content. The absence or presence of your file also does not settle whether the host returns the linked pages successfully.

If you publish a documentation overview, give its first heading the project's actual name and make the covered path explicit. Then check a linked Markdown page against its human-facing source for the same product fact and date. The overview and the detailed page are separate places where a stale term can survive.

## Also asked as

What is an llms.txt file?

## Related

- [The v2 proposal](https://llmstxt.org/)
- [The observed website tasks](https://doi.org/10.5281/zenodo.23197560)
- [Inspecting an existing file](how-should-i-check-an-llms-txt-file.md)

## Next step

Use [Free 10-question check (one engine)](https://audit.broadcastwell.com/) to inspect a defined set of buyer questions. No email is needed; runs are limited per network and per day, and by the site's daily allowance.

For one documented gap, [Fix one answer, $490](https://broadcastwell.com/answer-repair). Keep the question and source receipt with the requested change.

[Our answer-study method, v1.1.](https://broadcastwell.com/methodology)

Prepared by the Broadcastwell team.

Page owner: Rohan Iyer, AI Engineer. Corrections: hello@broadcastwell.com
