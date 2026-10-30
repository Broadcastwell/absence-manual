---
title: Does a crawler request count as a buyer visit?
headline: Does a crawler request count as a buyer visit?
description: A crawler request records machine access. It does not identify a buyer, a purchase or a completed customer journey.
page_class: page
schema_type: Article
date_published: '2026-10-30T04:24:00+00:00'
date_modified: '2026-10-30T04:24:00+00:00'
hide:
- navigation
library_cluster: fixes
library_owner: Rohan Iyer, AI Engineer
library_subtopic: Machine requests and buyer evidence
library_order: 293
demand_source: manual-faq
demand_evidence: LB-Q0273, private demand receipt dated 2026-10-28
also_asked_as:
- Does a crawler request count as a buyer visit?
is_based_on: https://doi.org/10.5281/zenodo.23197560
evidence_kind: published-study
evidence_method_receipts:
- https://doi.org/10.5281/zenodo.23197560
---

# Does a crawler request count as a buyer visit?

No. A crawler request is evidence of a machine request, not an identified buyer visit. Our [Agent Gap study](https://doi.org/10.5281/zenodo.23197560) labeled 70 of 70 initial demo-path responses correct on 6 October 2026, yet correctness described the assigned task response rather than a customer arriving or placing an order.

## What we measured

**Measured.** The [Agent Gap method](https://doi.org/10.5281/zenodo.23197560) separates whether a response is correct from whether the assistant reaches its destination. For S3, seventy initial responses were labeled correct, while forty-four reached the public demo-path endpoint. These fields were not purchase or website-conversion measurements.

**Reported.** OpenAI's [crawler documentation](https://developers.openai.com/api/docs/bots), read on 29 October 2026, assigns different roles to OAI-SearchBot, GPTBot and ChatGPT-User. Anthropic's [robot guide](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler) separately distinguishes ClaudeBot, Claude-SearchBot and Claude-User.

**Reasoned.** Those role definitions describe how content may be retrieved. They do not identify the commercial intent of a person behind a request, and the Agent Gap task labels do not supply missing buyer identities.

## What this means for you

Read the agent name. OpenAI describes OAI-SearchBot as its Search crawler and GPTBot as collecting material that may be used for model training. A Search-crawler request and a training-crawler request therefore should not be merged into one count of people considering your software.

User-directed retrieval is another defined role. OpenAI says ChatGPT-User may visit a page for certain user actions and is not its automatic Search crawler. Anthropic similarly describes Claude-User as responding to user requests. Even this closer connection to a user action does not disclose whether that user is a buyer, researcher or existing customer.

The Procore S3 record in Agent Gap makes the task boundary visible. Its initial session is marked found, correct and reached, with an endpoint time on 6 October 2026. Those three fields describe the assistant's public demo-path task. They are different from an order identifier, a submitted customer request or a paid transaction, none of which was the task's recorded outcome.

## Also asked as

Does a crawler request count as a buyer visit?

## Related

- [OpenAI’s crawler roles](https://developers.openai.com/api/docs/bots)
- [Anthropic’s robot roles](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
- [Agent Gap tasks and fields](https://doi.org/10.5281/zenodo.23197560)
- [Public browsing versus a connection](https://docs.broadcastwell.com/answers/agents/how-does-an-ai-connector-differ-from-browsing-a-website/)

## Next step

To examine public answer wording rather than server traffic, use the [Free 10-question check (one engine)](https://audit.broadcastwell.com/). No email is needed; runs are limited per network and per day, and by the site's daily allowance.

For one sourced factual error, [Fix one answer, $490](https://broadcastwell.com/answer-repair). Retain the answer and the document that supports the correction.

[Our answer-study method, v1.1.](https://broadcastwell.com/methodology)

Prepared by the Broadcastwell team.

Page owner: Rohan Iyer, AI Engineer. Corrections: hello@broadcastwell.com
