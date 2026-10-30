---
title: How can server logs show whether AI crawlers request llms.txt?
headline: How can server logs show whether AI crawlers request llms.txt?
description: A server request needs a path, time, status and a defensible crawler identity. Our zero llms.txt citations in 2,093 answers measure a different event.
page_class: page
schema_type: Article
date_published: '2026-10-30T12:15:58+00:00'
date_modified: '2026-10-30T12:51:00+00:00'
hide:
- navigation
library_cluster: measurement
library_owner: Vikram Patel, AI Architect
library_subtopic: Observed crawler requests to llms.txt
library_order: 334
demand_source: reddit
demand_evidence: LB-Q0504, private demand receipt dated 2026-10-28
also_asked_as:
- How can server logs show whether AI crawlers request llms.txt?
- llms.txt adoption vs actual crawler behavior, anyone tracked GPTBot/ClaudeBot hits against a llms.txt file directly?
is_based_on: https://doi.org/10.5281/zenodo.23271935
evidence_kind: published-study
evidence_method_receipts:
- https://doi.org/10.5281/zenodo.23271935
---

# How can server logs show whether AI crawlers request llms.txt?

Read the request path in your server or CDN log to establish a request for llms.txt; a crawler name on its own is insufficient. Our [Study 7 capture of 22 to 23 September 2026](https://doi.org/10.5281/zenodo.23271935) contains 0 recorded llms.txt citation URLs among 2,093 eligible answers. That is an answer-source result, so it cannot substitute for a request log.

## What we measured

**Measured.** The [method and records for The AI written RFP](https://doi.org/10.5281/zenodo.23271935) retain 2,093 included answers across fourteen software categories. We checked their recorded cited-URL paths for the filename llms.txt after separating the query string. None matched. Thirty-eight included records have empty cited-URL lists. Team review: in progress. This dataset contains answer citations, not a record of HTTP requests to anyone's llms.txt file.

**Reported.** OpenAI's [crawler documentation](https://developers.openai.com/api/docs/bots), read on 29 October 2026, separates OAI-SearchBot, GPTBot and ChatGPT-User, with published IP-range links. It says a robots.txt request may carry an extra robots.txt marker in the user-agent string. Anthropic's [crawler guide](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler), read the same day, separates ClaudeBot, Claude-SearchBot and Claude-User. The [llms.txt v2 proposal](https://llmstxt.org/), modified on 10 August 2026, describes a curated file and linked Markdown resources.

**Reasoned.** File publication, a request, a returned response and an answer citation are distinct observations. A request record addresses the first access event, without proving how the content was used afterward.

## What this means for you

Keep the requested path. OpenAI's documented robots.txt user-agent marker explains a concrete trap: a crawler-looking log line can concern robots.txt rather than llms.txt. The method, request target, timestamp and response status keep that event identifiable. A file requested under /docs/llms.txt is also a different target from the site's root /llms.txt.

Keep the crawler's role too. OAI-SearchBot is for search; GPTBot concerns material that may contribute to training. OpenAI says those controls are independent and a crawl may serve both permitted uses. The displayed user-agent should therefore be assessed alongside the documented IP ranges and the request's actual source, rather than relabeling every OpenAI request as ChatGPT search.

Anthropic's names make a similar distinction: ClaudeBot concerns potential training material, Claude-SearchBot search indexing and Claude-User user-directed retrieval. A log summary that merges those names would hide the purpose specified by the provider. The llms.txt proposal, meanwhile, permits files at a root or subpath and describes links to detail pages; each requested resource retains its own URL in an access record.

## Also asked as

How can server logs show whether AI crawlers request llms.txt?

llms.txt adoption vs actual crawler behavior, anyone tracked GPTBot/ClaudeBot hits against a llms.txt file directly?

## Related

- [OpenAI crawler identities and IP ranges](https://developers.openai.com/api/docs/bots)
- [Anthropic crawler roles](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
- [The llms.txt v2 proposal](https://llmstxt.org/)
- [The AI written RFP data and method](https://doi.org/10.5281/zenodo.23271935)
- [The Manual on request, citation and referral events](https://docs.broadcastwell.com/ai-source-standard/)
- [The Manual on valid measurement](https://docs.broadcastwell.com/valid-measurement/)

## Next step

Use the [Free 10-question check (one engine)](https://audit.broadcastwell.com/) for a separate dated company-answer sample. No email is needed; runs are limited per network and per day, and by the site's daily allowance.

For one documented company-fact error, [Fix one answer, $490](https://broadcastwell.com/answer-repair). Keep the retained answer and its supporting public source with the correction.

[Our answer-study method, v1.1.](https://broadcastwell.com/methodology)

Prepared by the Broadcastwell team.

Page owner: Vikram Patel, AI Architect. Corrections: hello@broadcastwell.com
