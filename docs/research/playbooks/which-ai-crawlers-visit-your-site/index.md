---
title: How can you see which AI crawlers visit your site?
description: Use dated request records and operator documentation to distinguish search crawlers, training crawlers,
  user fetchers and robots controls that never appear as separate user agents.
page_class: research
research_id: 28
research_group: playbook
lead: Daniel Kim
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/playbooks/which-ai-crawlers-visit-your-site/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://developers.openai.com/api/docs/bots
---

# How can you see which AI crawlers visit your site?

**Google-Extended and Applebot-Extended are robots controls, not separate HTTP user agents to count in logs (Google and Apple operator documentation, 2026).**

**Google-Extended** and **Applebot-Extended** belong in a crawl-policy discussion, but looking for those exact names as separate HTTP requesters is the wrong log test. Their operators describe them as controls over specified uses of crawled content. Count the requester that actually appears in a request, then interpret its role using current operator documentation. [Google common crawlers; Apple, About Applebot, verified 30 October 2026].

An agent name is also a claim made by a request. It can be copied. A useful report distinguishes a declared token match from an authenticated operator identity, and it distinguishes both from evidence that a page was cited in an answer.

## Which names should you recognize?

The following roles were checked against the linked operators’ documentation on **30 October 2026**. Names are tokens rather than fixed complete strings; version numbers and surrounding browser text can change.

| Token or control | Documented role | Interpretation for your record |
|---|---|---|
| GPTBot | OpenAI training-related crawling | A request is not a ChatGPT search citation. |
| OAI-SearchBot | Search discovery for ChatGPT | Treat it separately from the training crawler. |
| ChatGPT-User | Certain user-initiated actions | It is not an automatic web crawl or the control for Search opt-outs. |
| ClaudeBot | Anthropic training-related collection | Distinguish it from search and user requests. |
| Claude-SearchBot | Search-related collection | A search role still does not prove later citation. |
| Claude-User | Retrieval at a Claude user’s direction | Record the requested page and successful response separately. |
| PerplexityBot | Search discovery, not foundation-model training | Apply the operator’s published verification guidance. |
| Perplexity-User | Retrieval supporting a user action | The operator says these user fetches generally ignore robots.txt. |
| Googlebot | General Google Search crawling | A visit does not identify an AI Overview or AI Mode use. |
| bingbot | Bing crawling | Verify identity before attributing traffic to Microsoft. |
| Applebot | Apple search-related collection | A request alone does not identify a particular downstream AI use. |
| Google-Extended | Robots token for specified training and grounding uses | Not a separate HTTP user-agent stream. |
| Applebot-Extended | Robots control for specified generative-AI use | Not a separate crawler to count beside Applebot. |

Operator references: [OpenAI](https://developers.openai.com/api/docs/bots), [Anthropic](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler), [Perplexity](https://docs.perplexity.ai/docs/resources/perplexity-crawlers), [Google](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers), [Bing](https://www.bing.com/webmasters/help/which-crawlers-does-bing-use-8c184ec0) and [Apple](https://support.apple.com/en-us/119829).

## Find the observation source before interpreting a zero

Check which host serves the page and which request records are available for it. Page views are not request records. A CDN total may combine humans, assets and crawlers without exposing individual user agents. Identify the actual fields and period before deciding what the report can answer.

If you have no requester-level record, say that coverage is unavailable. Do not turn a missing report into “no AI visits.” A site can also be served from several hosts or a cached copy; observing one host does not cover the others.

For a narrow study, retain only fields needed for the question and publish aggregates. Query strings, cookies, bodies and visitor addresses are unnecessary for a simple count of declared agents on public pages. User-agent values themselves are untrusted strings and can contain unexpected information, so review and sanitize them before retaining or sharing them.

## Verify identity when attribution matters

Some operators publish address ranges or DNS verification procedures. Follow the operator’s current instructions rather than trusting a familiar substring. If your retained data cannot perform that verification, label the result as a declared token match. Do not retrospectively call it authenticated.

Google’s documentation explicitly warns that HTTP user-agent strings can be spoofed. Bing likewise publishes identification guidance. Verification is about who sent the request; it still does not reveal which answer, user or commercial outcome resulted from that request. [Google common crawlers; Bing crawler documentation].

Avoid testing a report by pretending to be the operator you are trying to count. Use a clearly identified research check and exclude it from the substantive observations. Preserve that exclusion in the published denominator so that a later reader can reproduce the total.

## Choose robots rules by the intended use

OpenAI documents separate settings for OAI-SearchBot and GPTBot. A site can allow search-related collection while restricting training-related collection. ChatGPT-User has a different user-request role, and OpenAI says robots rules may not apply to those actions. [OpenAI, Overview of OpenAI crawlers].

Anthropic documents separate training, search and user agents and says its bots honor robots directives. It also describes support for Crawl-delay. Perplexity separates its search bot from its user fetcher. Those operator-specific statements matter; a single rule copied for every service can create an unintended policy. [Anthropic; Perplexity operator pages].

For Google Search AI features, Googlebot and the documented Search preview controls are relevant. Google-Extended addresses other specified uses; it is not a substitute for the Search control. Read the product scope before changing a rule. [Google Search Central, AI features and your website].

Robots rules communicate crawl preferences to cooperating requesters. They are not authentication or a secure way to hide private information. Keep confidential material behind appropriate access controls and avoid making a public link inventory of it.

## Group visits without hiding gaps

A weekly table should identify its timezone, first and last observation, covered hosts and paths, success-status rules and excluded checks. Count requests consistently, and state whether repeated requests to one page remain separate events. No unique-reader count follows.

If a quota, outage or deployment change interrupts collection, mark the affected period as incomplete. Separate incomplete periods from complete periods with zero recorded matches. The distinction is essential when someone later plots a trend.

Page-level tables help answer which public resources were requested. They do not establish which source the answer system ultimately relied on. A crawler may revisit a page that is never cited, while an answer may use previously cached material without a fresh visit during your observation window.

## Compare logs with answer receipts cautiously

An answer receipt can show a particular visible citation on a stated date. A request log can show that a matching requester reached a particular path. Connecting those records causally requires evidence beyond their proximity in time. Do not infer an engine’s source-selection process from a coincident visit.

Our [public crawler-log study](https://docs.broadcastwell.com/research/studies/ai-crawler-log/) begins with an explicitly short window and restricted route coverage. Its downloadable table states those boundaries. It is a starting observation, not a benchmark for how often every B2B site should be crawled.

OpenAI’s operator documentation says, “Each setting is independent of the others”. A permission for search and a permission for model training therefore need separate interpretation when reading the declared request tokens. [OpenAI, Overview of OpenAI crawlers, opening explanation; verified 30 October 2026].

## Recorded operational snapshot

The first Index log snapshot records zero declared AI-token matches among 83 other requests after one named check is excluded. Its descriptive Wilson 95% interval is 0.0% to 4.4%, for that short covered window only. [Initial operational snapshot, 30 October 2026](https://docs.broadcastwell.com/research/data/ai-crawler-log.csv). This operational log is separate from the registered answer-archive studies. It does not authenticate requester identity or cover the documentation host.

## What our own data shows

We have no measurement on this point: whether a recorded crawler visit leads to a later citation or sale. The operational request counts above do not measure that relationship.

## Sources

- Broadcastwell. (2026, October 30). AI crawler operational log: initial snapshot [Data set]. Index-host covered HTML requests, 05:35:44.478 to 05:38:00.771840 UTC; named check excluded. https://docs.broadcastwell.com/research/data/ai-crawler-log.csv Verified 30 October 2026.
- OpenAI. (2026). Overview of OpenAI crawlers. Search, training and user-request roles. https://developers.openai.com/api/docs/bots Verified 30 October 2026.
- Anthropic. (2026, April 7). Does Anthropic crawl data from the web, and how can site owners block the crawler? https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler Verified 30 October 2026.
- Perplexity. (2026). Perplexity crawlers. Search and user-request roles. https://docs.perplexity.ai/docs/resources/perplexity-crawlers Verified 30 October 2026.
- Google Crawling Infrastructure. (2026). List of Google’s common crawlers. Googlebot and Google-Extended controls. https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers Verified 30 October 2026.
- Microsoft Bing. (2026). Which crawlers does Bing use? https://www.bing.com/webmasters/help/which-crawlers-does-bing-use-8c184ec0 Verified 30 October 2026.
- Apple. (2026, September 4). About Applebot. Opened in the operator page earlier on 30 October 2026; a later automated request was rate limited. https://support.apple.com/en-us/119829 Verified 30 October 2026.
- Google Search Central. (2026). AI features and your website. https://developers.google.com/search/docs/appearance/ai-features Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *How can you see which AI crawlers visit your site?*. Broadcastwell. https://docs.broadcastwell.com/research/playbooks/which-ai-crawlers-visit-your-site/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research28,
  author = {{Broadcastwell research team}},
  title = {How can you see which AI crawlers visit your site?},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/playbooks/which-ai-crawlers-visit-your-site/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Daniel Kim, AI engineer.

Sources checked 30 October 2026. Independent check: 30 October 2026, Broadcastwell verification desk. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read why citation and recommendation differ](https://docs.broadcastwell.com/cited-not-recommended/).
