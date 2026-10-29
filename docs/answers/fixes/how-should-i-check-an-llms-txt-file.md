---
title: How should I check an llms.txt file?
headline: How should I check an llms.txt file?
description: 'Check the served file and its destinations separately: Agent Gap found
  all 70 pricing pages but reached 52 task endpoints.'
page_class: page
schema_type: Article
date_published: '2026-10-28T23:31:03+00:00'
date_modified: '2026-10-28T23:31:03+00:00'
hide:
- navigation
library_cluster: fixes
library_owner: Rohan Iyer, AI Engineer
library_subtopic: File validation
library_order: 72
demand_source: google-autocomplete
demand_evidence: LB-Q0639, private demand receipt dated 2026-10-28
also_asked_as:
- How should I check an llms.txt file?
is_based_on: https://doi.org/10.5281/zenodo.23197560
evidence_kind: published-study
evidence_method_receipts:
- https://doi.org/10.5281/zenodo.23197560
---

# How should I check an llms.txt file?

Check the served file's content, structure and destinations separately from any claim about AI use. Agent Gap found pricing pages for all 70 selected vendors on 6 October 2026, but only 52 pricing tasks reached their endpoint. Those were browser tasks, not llms.txt checker results; a reachable URL alone did not describe the complete outcome.

## What we measured

**Measured.** The [Agent Gap pricing-task method](https://doi.org/10.5281/zenodo.23197560) used the ChatGPT Work browser interface. Among 70 initial pricing sessions, 67 results were correct, two incorrect and one unscored; endpoint reach was a separate field with 52 reached. The collection does not reveal whether a crawler read a special text file or why an individual path stopped.

**Reported.** The [llms.txt v2 proposal](https://llmstxt.org/), read 28 October 2026, gives a Markdown structure with a project H1 and optional grouped links. A format check can assess that structure without establishing adoption by an engine.

## What this means for you

**Reasoned.** Open the public file address first. Confirm that the response is the intended text, not an error page, login screen or unrelated redirect. Record the final URL and read date so that a later reviewer can identify the version you checked.

Next, inspect the text. Check the site name, description, headings and link syntax. Follow the links instead of stopping after a parser accepts them. A destination may return successfully yet describe an old product, a different plan or a historical study. Compare each changed label with the page it promises to explain.

Keep separate outcomes in the receipt: the file was retrieved, the syntax was checked, the destinations resolved and the descriptions matched. Mark an unresolved destination as unresolved. A green checker badge should say which of these checks it actually performed.

After a deployment, compare the served version with the approved output and recheck the changed links. This catches a delivery problem that a local validation cannot see. Checking these static facts requires no new model call; any later claim about use, citation or recommendation needs its own observation and method.

- **For a site owner:** inspect the final served URL and its actual content.
- **For a developer:** report individual failures instead of hiding them in one score.
- **For an agency:** deliver the checked version and the list of unresolved items.

## Also asked as

How should I check an llms.txt file?

## Related

- [Agent Gap's pricing-path evidence](https://broadcastwell.com/research/agent-gap)
- [Source-checking standard](../../ai-source-standard.md)
- [Generate from page records](how-can-i-generate-llms-txt-from-existing-pages.md)
- [What publication proves](what-does-publishing-llms-txt-prove-about-ai-visibility.md)

## Next step

Use the [Free 10-question check (one engine)](https://audit.broadcastwell.com/). No email is needed; runs are limited per network and per day, and by the site's daily allowance. Retain its cited source and observation date when deciding which description to inspect.

If the check identifies one source page with an approved factual correction, [Fix one answer, $490](https://broadcastwell.com/answer-repair).

[Our answer-study method, v1.1.](https://broadcastwell.com/methodology)

Prepared by the Broadcastwell team.

Page owner: Rohan Iyer, AI Engineer. Corrections: hello@broadcastwell.com
