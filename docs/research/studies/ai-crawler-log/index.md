---
title: The AI crawler log begins with a short observation window
description: A public server-side request log for the Index, with declared agent tokens, exact collection boundaries,
  privacy limits and an initial table. Requests do not prove citation.
page_class: research
research_id: 47
research_group: study
lead: Vikram Patel
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/studies/ai-crawler-log/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://developers.openai.com/api/docs/bots
research_dataset:
  name: Broadcastwell public Index crawler-request observations
  description: Dated aggregate requests to known public successful Index HTML routes, with declared agent-token
    definitions, own-check exclusions and coverage limits. User-agent identity is not authenticated.
  identifier: https://docs.broadcastwell.com/research/studies/ai-crawler-log/
  distribution:
  - name: Crawler-log snapshots
    contentUrl: https://docs.broadcastwell.com/research/data/ai-crawler-log.csv
    encodingFormat: text/csv
  - name: Agent definitions
    contentUrl: https://docs.broadcastwell.com/research/data/crawler-agent-definitions.csv
    encodingFormat: text/csv
---

# The AI crawler log begins with a short observation window

**The initial log has zero declared AI-token matches among 83 requests after our check is excluded (Broadcastwell, 30 October 2026, crawler-log snapshot).**

The first saved window contains **zero declared AI-agent token matches among 83 requests**, after excluding one named research check. Its descriptive **95% Wilson interval is 0.0% to 4.4%**. That short observation cannot establish that AI services never visit the site. [Broadcastwell public-request log, 30 October 2026, initial snapshot](../../data/ai-crawler-log.csv).

Collection was enabled on **30 October 2026 at 05:35:37 UTC**. The first stored observation is **05:35:44.478 UTC**; this initial table ends at the last stored observation, **05:38:00.771 UTC**. The window is deliberately printed with the count. It is not a complete day, a monthly total or a statement about all requests to Broadcastwell.

## What does the log cover?

The collection covers known public HTML routes on **index.broadcastwell.com**, for successful GET or HEAD responses only. It excludes unknown paths, form submissions, non-HTML assets and unsuccessful responses. The hostname and response rules also exclude preview deployments. The set of public routes is fixed from the published site’s HTML paths, rather than accepting arbitrary private-looking request paths.

The log does not cover docs.broadcastwell.com, app.broadcastwell.com, other company surfaces or activity that never reaches the observed routes. A service can use cached information, an outside index or a different public page without producing an event here. An unanswered or blocked request falls outside the successful-response record and must not be interpreted as a confirmed absence of crawling.

Only four observation fields are stored: timestamp, public path, sanitized user-agent string and a yes/no match to the declared AI-request tokens. Query strings, request bodies, cookies and addresses are not stored. The initial sanitizer removed email and IPv4 strings. A reserved-address test later showed that IPv6 strings were retained. A corrected sanitizer is supplied with the public collection instrument; the synthetic test does not establish that an actual visitor address was stored. The initial collection therefore cannot be described as guaranteeing removal of every address form. The public releases contain aggregates rather than raw visitor strings.

There is a **4,000-observation ceiling per UTC day**. A separate daily counter records whether that ceiling was reached. A capped day is incomplete and must be labelled as such in subsequent tables. The ceiling, missing coverage and logging failures cannot be converted into zero visits for the unobserved period. [Public collection instrument](../../data/research-crawler-collection.mjs), verified 30 October 2026. Its corrected sanitizer is distinguished from the initial production version.

## The first table is a starting record

| Window and scope | Stored requests | Our named checks excluded | Other-request base | Declared AI-token matches | Share and descriptive 95% Wilson interval |
|---|---:|---:|---:|---:|---|
| 30 October 2026, 05:35:44.478 to 05:38:00.771 UTC; observed public Index HTML routes | 84 | 1 | 83 | 0 | 0.0% (0.0% to 4.4%) |

Source: the live four-field observation table and a read-back aggregate query on **30 October 2026**. [Download the snapshot](../../data/ai-crawler-log.csv). The named research request verified that its query string did not enter the stored path and that its AI-match field remained false. It is excluded from the displayed other-request denominator.

The base includes other automated requests as well as any ordinary browser traffic meeting the rules. It is not a count of human visitors. Requests are dependent and the window is a cutoff record, so the Wilson interval is descriptive. Its upper bound is useful precisely because an observed zero in a small base does not mean a known zero in the wider world.

## Which agent strings are recognized?

| Request token | Documented role | In this log’s AI-match group? |
|---|---|---|
| GPTBot | Training-related crawl | yes |
| OAI-SearchBot | Search for ChatGPT | yes |
| ChatGPT-User | User-initiated retrieval, not automatic crawl | yes |
| ClaudeBot | Training-related crawl | yes |
| Claude-SearchBot | Search-related crawl | yes |
| Claude-User | User-initiated retrieval | yes |
| PerplexityBot | Search crawl | yes |
| Perplexity-User | User-initiated retrieval | yes |
| Googlebot | General Google Search crawl; not specific evidence of AI use | no |
| bingbot | General Bing crawl; not specific evidence of AI use | no |
| Applebot | Apple search-related crawl; AI use cannot be inferred per request | no |

Definitions personally checked **30 October 2026** against the operator pages in Sources. [Machine-readable agent table](../../data/crawler-agent-definitions.csv). Token matching uses boundaries, rather than accepting an arbitrary longer word containing a familiar bot name. The group is a declared measurement definition, not an exhaustive list of every present or future automated agent.

The yes/no field deliberately separates the listed AI-specific request tokens from general search crawlers. Googlebot and bingbot may support search products, but a request with either string does not establish that the page entered an AI answer. Apple likewise describes multiple uses for Applebot data. The operator’s broad product description does not reveal the purpose of a particular request.

## A request string is a claimed identity

User-agent strings can be copied. The operators publish verification guidance, including network information, but this collection does not retain addresses and therefore cannot authenticate each operator by network origin. We describe token matches as claimed identities, not verified visits by the named company.

A matching request also does not prove that the response was indexed, retained, used for training or cited. The server can observe a request and the response class; it cannot observe all later uses. You should resist replacing that modest observation with a stronger downstream event just because a recognizable agent name appears.

There is another distinction inside the operator lists. OpenAI states that ChatGPT-User is “not used for crawling the web in an automatic fashion.” It describes user-triggered actions separately from OAI-SearchBot and GPTBot. The log groups their AI-specific tokens for disclosure, while retaining the distinct definitions so a reader can separate retrieval from automatic crawling. [OpenAI crawler documentation, checked 30 October 2026].

## Data-use controls are not extra request agents

Google-Extended and Applebot-Extended should not be counted as ordinary HTTP crawler identities. They are controls over specified uses of content. Apple explicitly says its Extended control does not crawl pages. Google similarly distinguishes its Extended token from the crawler user agents that fetch pages. Counting a robots directive as a visit would manufacture an observation.

Operator rules also differ for user-triggered retrieval. Perplexity’s documentation distinguishes its search crawler from its user agent; OpenAI says robots rules may not apply to user-initiated actions. Anthropic documents its own named agents and site-owner controls. A generic sentence that all AI requests follow one identical policy would erase those differences. The operator references below preserve those individual rules and their verification dates.

## How should later tables be read?

Each update needs a defined UTC window, the last included observation, the eligible request base, agent counts and path counts, together with capped days and known gaps. Raw strings should be mapped to the dated operator definitions before aggregation. A changed token list needs a version note, so an apparent difference is not silently created by changing what counts.

The public path counts can identify frequently requested material, but they do not establish unique users or source influence. One automated requester can revisit a page. Different strings can belong to the same operator. A single request can be followed by many unseen uses or none at all.

The initial interval remains an historical snapshot rather than being overwritten with a later total. Subsequent CSV rows can extend the record with their own windows. The unresolved question is which parts of the public Index are repeatedly requested under identifiable agent strings once there is a longer, explicitly complete observation period.

## What our own data shows

After the named own check is excluded, the initial snapshot has **0 declared AI-token matches among 83 observations, 0.0% (Wilson 95% interval 0.0% to 4.4%)**. These are declared user-agent matches in that short covered window. The [initial observation CSV](../../data/ai-crawler-log.csv) is a direct aggregate from the public-request record, with one named own check excluded. The reference archive used for our answer studies is separately identified by [September release DOI](https://doi.org/10.5281/zenodo.22907695); it is not the source of crawler visits. We have no measurement here of whether any logged request caused an AI citation, a visit from a buyer or a commercial outcome.

## Sources

- OpenAI. (2026). Overview of OpenAI crawlers. OAI-SearchBot, GPTBot and ChatGPT-User definitions. https://developers.openai.com/api/docs/bots Verified 30 October 2026.
- Anthropic. (2026). Does Anthropic crawl data from the web, and how can site owners block the crawler? ClaudeBot, Claude-SearchBot and Claude-User definitions. https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler Verified 30 October 2026.
- Perplexity. (2026). Perplexity crawlers. PerplexityBot and Perplexity-User definitions and verification guidance. https://docs.perplexity.ai/docs/resources/perplexity-crawlers Verified 30 October 2026.
- Google Search Central. (2026). Google common crawlers. Googlebot and Google-Extended distinction. https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers Verified 30 October 2026.
- Microsoft Bing. (2026). Which crawlers does Bing use? Bingbot identities and verification. https://www.bing.com/webmasters/help/which-crawlers-does-bing-use-8c184ec0 Verified 30 October 2026.
- Apple. (2026, September 4). About Applebot. Applebot, Applebot-Extended and verification. https://support.apple.com/en-us/119829 Verified 30 October 2026.
- Broadcastwell. (2026). Public-request crawler study collection instrument. https://docs.broadcastwell.com/research/data/research-crawler-collection.mjs . Initial implementation and later sanitizer correction distinguished in the page text. Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *The AI crawler log begins with a short observation window*. Broadcastwell. https://docs.broadcastwell.com/research/studies/ai-crawler-log/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research47,
  author = {{Broadcastwell research team}},
  title = {The AI crawler log begins with a short observation window},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/studies/ai-crawler-log/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Vikram Patel, AI architect and specialist.

Sources checked 30 October 2026. Independent check: pending. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the measurement chapter](https://docs.broadcastwell.com/measurement-noise/).
