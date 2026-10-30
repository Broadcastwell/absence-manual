---
title: Why can a page rank in Google without being cited by ChatGPT or Perplexity?
headline: Why can a page rank in Google without being cited by ChatGPT or Perplexity?
description: Salesforce-domain URLs appeared in 19 ChatGPT and three Perplexity CRM answers. Compare those source selections with the services’ eligibility rules.
page_class: page
schema_type: Article
date_published: '2026-10-30T12:15:58+00:00'
date_modified: '2026-10-30T12:15:58+00:00'
hide:
- navigation
library_cluster: measurement
library_owner: Vikram Patel, AI Architect
library_subtopic: Google rank and answer-source selection
library_order: 331
demand_source: reddit
demand_evidence: LB-Q0503, private demand receipt dated 2026-10-28
also_asked_as:
- Why can a page rank in Google without being cited by ChatGPT or Perplexity?
- Why does a page rank well on Google but still never get cited by ChatGPT or Perplexity?
is_based_on: https://doi.org/10.5281/zenodo.22907695
---

# Why can a page rank in Google without being cited by ChatGPT or Perplexity?

Salesforce-domain URLs appeared in 19 of 30 ChatGPT CRM answers and 3 of 30 Perplexity CRM answers in our [Index capture of 22 September 2026](https://doi.org/10.5281/zenodo.22907695). That difference is a concrete source-selection result, not a Google rank comparison. A page's Google position does not establish that either service will select it as an answer citation.

## What we measured

**Measured.** We counted each original CRM answer at most once when its recorded citations contained a Salesforce-owned host, including help and training subdomains. The [Index release](https://doi.org/10.5281/zenodo.22907695) retained thirty answers per engine.

| Captured engine | Answers with a Salesforce-domain URL | Valid-answer base |
| --- | --- | --- |
| ChatGPT | 19 | 30 |
| Perplexity | 3 | 30 |

**Reported.** OpenAI's [search guide](https://help.openai.com/en/articles/9237897-searching-the-web-with-chatgpt), read on 29 October 2026, describes multiple ranking factors and says placement is not guaranteed. It also describes rewriting a user's question into targeted searches. Perplexity's [Pro Search guide](https://www.perplexity.ai/help-center/en/articles/10352903-what-is-pro-search), read the same day, describes multiple searches and source synthesis. Google's [AI-features guide](https://developers.google.com/search/docs/appearance/ai-features) likewise distinguishes eligibility from guaranteed indexing or serving.

**Reasoned.** Separate retrieval and source choices are consistent with different citation sets. Our panel did not record Google positions or diagnose a particular missing page's cause.

## What this means for you

The source paths differ. All three Perplexity citations in this cut come from the small-sales-team question and point to the same Salesforce small-business CRM blog URL. The ChatGPT set spans seven buyer questions. Its task-handoff answers include Salesforce Help and Trailhead paths, rather than that one blog page alone.

That distinction changes what you can inspect. A blog URL not selected for a handoff question is different from the entire Salesforce domain being absent. Our count groups the owned hosts into a domain-level observation; the retained paths preserve the more particular page and buyer context. Neither label is a Google-position field.

OpenAI also documents a separate access condition: OAI-SearchBot is its search crawler, while GPTBot concerns content that may be used for model training. The [crawler guide](https://developers.openai.com/api/docs/bots) lets a publisher separate those controls. A site that appears in Google's index still has that service-specific search-access question, and an allowed page still faces the source-selection process described by the search guide.

## Also asked as

Why can a page rank in Google without being cited by ChatGPT or Perplexity?

Why does a page rank well on Google but still never get cited by ChatGPT or Perplexity?

## Related

- [OpenAI search eligibility and sources](https://help.openai.com/en/articles/9237897-searching-the-web-with-chatgpt)
- [OpenAI crawler roles](https://developers.openai.com/api/docs/bots)
- [Perplexity Pro Search](https://www.perplexity.ai/help-center/en/articles/10352903-what-is-pro-search)
- [Google AI website eligibility](https://developers.google.com/search/docs/appearance/ai-features)
- [The CRM Index records](https://index.broadcastwell.com/questions/crm/)
- [The Manual on valid measurement](https://docs.broadcastwell.com/valid-measurement/)

## Next step

Use the [Free 10-question check (one engine)](https://audit.broadcastwell.com/) for a separate dated company-answer sample. No email is needed; runs are limited per network and per day, and by the site's daily allowance.

For one documented company-fact error, [Fix one answer, $490](https://broadcastwell.com/answer-repair). Keep the retained answer and its supporting public source with the correction.

[Every figure comes from the published method, v1.1.](https://broadcastwell.com/methodology)

Prepared by the Broadcastwell team.

Page owner: Vikram Patel, AI Architect. Corrections: hello@broadcastwell.com
