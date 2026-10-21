---
title: Bot access and AI search visibility
headline: Bot access, search eligibility and cited sources
description: Understand the difference between permission to crawl, search inclusion
  and an observed citation, using current primary documentation.
page_class: note
schema_type: Article
date_published: '2026-10-13T00:00:00+00:00'
date_modified: '2026-10-20T00:00:00+00:00'
faq:
- question: Does Anthropic crawl data from the web, and how can site owners block
    the crawler?
  answer: Yes. Anthropic documents ClaudeBot for potential training-data collection,
    Claude-SearchBot for search and Claude-User for user-directed page access. Its
    bots honour robots.txt signals. Site owners should decide on these purposes separately
    and review the current official documentation. A decision about one purpose should
    not be treated as evidence about every other purpose.
- question: Does allowing GPTBot make a site appear in ChatGPT search?
  answer: No. OpenAI distinguishes GPTBot, associated with training, from OAI-SearchBot,
    associated with search. Their permissions are independent. Allowing training collection
    is not a prerequisite or a guarantee for search inclusion. Check the search-specific
    access policy and the sources in actual search answers.
- question: Does Google-Extended control AI Overviews or AI Mode visibility?
  answer: No. Google documents Google-Extended separately from Google Search. It does
    not control Search inclusion or ranking, including the AI search features. Search
    eligibility depends on the relevant Google Search requirements. Keep a training-policy
    decision separate from the question of whether a page can appear as a supporting
    link.
---

# Bot access and AI search visibility

Permission to read a page, inclusion in a search index, retrieval for a question and appearance as a citation are different events. A successful page request establishes access for that request. It does not establish the later events.

## What the requests show

A dated access observation can show that a page was returned under the conditions tested. Read the URL, date and scope with the result. A public educational page should be readable without exposing private customer material. Access decisions should follow the site owner's policy for each purpose.

## What the HTML check cannot show

An accessible page is not guaranteed to be indexed, retrieved, cited or recommended. A training crawler and a search crawler can have different purposes. Read the search product's current documentation rather than treating all AI-related requests as one system.

## Reading a result

Record the access finding separately from actual answer observations. If an answer cites your domain, inspect the linked page and the passage supporting the claim. If it does not, check search eligibility and the relevance of the page without assuming that access alone decides the outcome.

## Does Anthropic crawl data from the web, and how can site owners block the crawler?

Yes. Anthropic documents ClaudeBot for potential training-data collection, Claude-SearchBot for search and Claude-User for user-directed page access. Its bots honour robots.txt signals. Site owners should decide on these purposes separately and review the current official documentation. A decision about one purpose should not be treated as evidence about every other purpose.

## Does allowing GPTBot make a site appear in ChatGPT search?

No. OpenAI distinguishes GPTBot, associated with training, from OAI-SearchBot, associated with search. Their permissions are independent. Allowing training collection is not a prerequisite or a guarantee for search inclusion. Check the search-specific access policy and the sources in actual search answers.

## Does Google-Extended control AI Overviews or AI Mode visibility?

No. Google documents Google-Extended separately from Google Search. It does not control Search inclusion or ranking, including the AI search features. Search eligibility depends on the relevant Google Search requirements. Keep a training-policy decision separate from the question of whether a page can appear as a supporting link.

## Primary sources

- [OpenAI's crawler purposes](https://developers.openai.com/api/docs/bots)
- [Anthropic's crawler purposes and owner choices](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
- [Google's crawler documentation](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers)
- [Google's AI feature eligibility guidance](https://developers.google.com/search/docs/appearance/ai-features)

Sources reviewed 20 October 2026. Read the [GEO Hub](https://broadcastwell.com/insights), [AI source chapter](../who-gets-cited.md) and [answer-reading guide](guides/read-an-answer.md) next.
