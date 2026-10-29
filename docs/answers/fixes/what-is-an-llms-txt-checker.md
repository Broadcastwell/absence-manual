---
title: What is an llms.txt checker?
headline: What is an llms.txt checker?
description: An llms.txt checker tests stated file rules. Separate a valid structure or working link from a correct account of the destination and its pricing.
page_class: page
schema_type: Article
date_published: '2026-10-29T20:50:39+00:00'
date_modified: '2026-10-29T20:50:39+00:00'
hide:
- navigation
library_cluster: fixes
library_owner: Rohan Iyer, AI Engineer
library_subtopic: File-checker scope
library_order: 201
demand_source: google-autocomplete
demand_evidence: LB-Q0405, private demand receipt dated 2026-10-28
also_asked_as:
- What is an llms.txt checker?
is_based_on: https://doi.org/10.5281/zenodo.23197560
evidence_kind: published-study
evidence_method_receipts:
- https://doi.org/10.5281/zenodo.23197560
---

# What is an llms.txt checker?

An llms.txt checker is a program that checks a file against stated structure rules; some also inspect its links. A format pass cannot establish that the linked information was understood correctly. In our separate Agent Gap browser tasks on 6 October 2026, pricing results were correct in 67/70 initial sessions. You should keep a checker's file result distinct from that kind of content-correctness result; we did not test an llms.txt checker in the study.

## What we measured

**Reported.** The [llms.txt v2 proposal](https://llmstxt.org/), modified on 10 August 2026 and read on 29 October, describes a Markdown format that ordinary programs can parse. Its only required section is an H1 naming the project or site. An initial byte-order mark is optional. A summary blockquote, further non-heading material and H2 file-list sections follow the proposal's specified order when present.

Within a file list, each entry needs a Markdown hyperlink. The label can be followed by a colon and explanatory notes. The proposal also describes files at subpaths, where a file covers the URLs under its path. These are concrete rules a format check can address; a particular checker's documentation must state which it implements.

**Measured.** The [Agent Gap pricing-task method](https://doi.org/10.5281/zenodo.23197560) separately recorded correctness while the browser assistant examined public software websites. Among the 70 initial pricing tasks, 67 were correct, two incorrect and one unscored. Separate repeat sessions are outside that base. This is a content-result classification, not a Markdown-conformance count or a measurement of llms.txt use.

## What this means for you

**Reasoned.** Read the check's rule before interpreting its warning. Under the saved v2 proposal, an absent summary is different from an absent H1: only the latter omits the required section. A tool can prefer a summary, but that preference needs its own label. Calling both omissions a required-format failure would misstate the proposal.

Link syntax is a different check again. A recognisable Markdown link does not establish that its destination returns the intended document. A checker that also fetches the URL can report a response separately from its parsing result. Neither event establishes that a pricing description accurately captures the page's billing basis or qualifications.



The subpath rule also gives a reviewer a particular scope to inspect. For a file at /docs/llms.txt, the proposal describes the documentation path, rather than every page on the origin. Check that the tool's output identifies the actual file location before treating its result as a whole-site assessment. If a warning says the H1 is missing, attach the returned file and that rule to the correction task; a general visibility score cannot explain that specific parsing failure.

## Also asked as

What is an llms.txt checker?

## Related

- [The llms.txt v2 proposal](https://llmstxt.org/)
- [Agent Gap task classifications](https://doi.org/10.5281/zenodo.23197560)
- [Website browsing versus a connector](/answers/agents/how-does-an-ai-connector-differ-from-browsing-a-website/)
- [Checking llms.txt](how-should-i-check-an-llms-txt-file.md)

## Next step

Use [Free 10-question check (one engine)](https://audit.broadcastwell.com/) to inspect public buyer answers; its result is not an llms.txt format certificate. No email is needed; runs are limited per network and per day, and by the site's daily allowance.

For one documented gap, [Fix one answer, $490](https://broadcastwell.com/answer-repair). Keep the question and source receipt with the requested change.

[Our answer-study method, v1.1.](https://broadcastwell.com/methodology)

Prepared by the Broadcastwell team.

Page owner: Rohan Iyer, AI Engineer. Corrections: hello@broadcastwell.com
