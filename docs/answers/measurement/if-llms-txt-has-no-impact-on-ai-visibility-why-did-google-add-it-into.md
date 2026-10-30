---
title: What does Lighthouse’s llms.txt audit check?
headline: What does Lighthouse’s llms.txt audit check?
description: Lighthouse documents a file-retrieval audit. Our zero cited-file count measures a separate event, rather than a visibility effect.
page_class: page
schema_type: Article
date_published: '2026-10-30T06:43:02+00:00'
date_modified: '2026-10-30T06:43:02+00:00'
hide:
- navigation
library_cluster: measurement
library_owner: Vikram Patel, AI Architect
library_subtopic: Lighthouse file retrieval and citation records
library_order: 305
demand_source: reddit
demand_evidence: LB-Q0462, private demand receipt dated 2026-10-28
also_asked_as:
- If llms.txt has no impact on AI visibility, why did Google add it into Lighthouse audits?
is_based_on: https://doi.org/10.5281/zenodo.23271935
evidence_kind: published-study
evidence_method_receipts:
- https://doi.org/10.5281/zenodo.23271935
---



# What does Lighthouse’s llms.txt audit check?

An optional file-retrieval check is what Google documents for llms.txt under [Lighthouse’s Agentic browsing audits](https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt). Our [Study 7 records](https://doi.org/10.5281/zenodo.23271935) contain no recorded cited URL ending in llms.txt among 2,093 included software answers; their capture dates were 22 and 23 September 2026. That zero counts cited filenames; it does not measure whether an agent retrieved the file.

## What we measured

**Reported.** Chrome for Developers places the audit under Agentic browsing, then Discoverability. The page, last updated on 5 May 2026 and read on 30 October, describes llms.txt as an emerging convention for a machine-readable website summary. It says Lighthouse flags a server error while retrieving the file. A missing file returning 404 is Not Applicable because providing one is optional.

**Measured.** Our [published Study 7 data and method](https://doi.org/10.5281/zenodo.23271935) retain 2,093 included software-answer records across fourteen categories. We checked the final filename in each stored cited URL’s path, excluding query strings and fragments. No path ended in llms.txt. Thirty-eight included records have an empty cited-URL list. This is an observation about the released URL field, rather than a test of file ingestion, Lighthouse behavior or a visibility effect.

**Reasoned.** A retrieval audit and a cited-URL count can both concern llms.txt while recording different events. The documented Lighthouse check therefore does not settle the question’s premise that the file has no impact on AI visibility.

## What this means for you

Read the audit category. The official navigation separates Agentic browsing audits from SEO audits. Under Discoverability, the llms.txt entry addresses a summary file and its retrieval response. If an audit report flags that entry, inspect the recorded response condition before describing it as a Search eligibility failure or a change in an answer engine’s source selection.

Keep 404 and server errors distinct. In this documented audit, the absence of an optional file receives N/A, while a server error during retrieval is flagged. That difference matters when you write a maintenance ticket: creating a file and correcting a failing request are different tasks. The published page asks for a concise Markdown summary with the site’s purpose and key links when you provide the file.

## Also asked as

If llms.txt has no impact on AI visibility, why did Google add it into Lighthouse audits?

## Related

- [Lighthouse’s documented llms.txt audit](https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt)
- [Study 7 method and released records](https://doi.org/10.5281/zenodo.23271935)
- [What Google says about llms.txt](https://docs.broadcastwell.com/answers/fixes/what-does-google-s-guidance-say-about-llms-txt/)
- [The Manual on valid measurement](https://docs.broadcastwell.com/valid-measurement/)

## Next step

Use the [Free 10-question check (one engine)](https://audit.broadcastwell.com/) for a separate dated answer sample. No email is needed; runs are limited per network and per day, and by the site's daily allowance.

For one sourced company-fact error, [Fix one answer, $490](https://broadcastwell.com/answer-repair). Keep the answer and the supporting public record together.

[Our answer-study method, v1.1.](https://broadcastwell.com/methodology)

Prepared by the Broadcastwell team.

Page owner: Vikram Patel, AI Architect. Corrections: hello@broadcastwell.com
