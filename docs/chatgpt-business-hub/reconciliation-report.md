---
title: How do you reconcile ChatGPT Hub counts with receipts?
headline: How do you reconcile ChatGPT Hub counts with receipts?
description: Our monthly format sets ChatGPT Business Hub impressions and clicks beside our answer receipts, gives each gap a reason code and states what is never inferred.
page_class: page
schema_type: TechArticle
date_published: '2026-11-09T00:00:00+00:00'
date_modified: '2026-11-11T07:30:00Z'
template: business-hub.html
---

# How do you reconcile ChatGPT Hub counts with receipts?

Put the month's ChatGPT Business Hub impressions and clicks beside our receipts for the same month, give every difference one reason code, and leave unstated anything neither record shows. The format below is filled with a fictional Kalvenor sample (Sample data, fictional company) for October 2026. Its Hub numbers are illustrative and fictional, because the Hub was unreleased when we wrote it.

Updated 11 November 2026.

## What each record counts

The two records measure different things, and the report never merges them.

| | Hub, as reported on 6 November 2026 | Our receipts |
| --- | --- | --- |
| Engines | ChatGPT | ChatGPT, Claude, Perplexity, Google AI Overviews and Google AI Mode |
| Unit | Daily impressions and clicks | One answer to one fixed buyer question on one run |
| Questions | Every conversation that showed the business, prompts not shown | The agreed buyer questions, each named |
| Competitors | Not shown | Who is named instead, with counts |
| Evidence | First-party counts | The full answer, cited URLs and capture date for every count |

## The monthly table

SAMPLE DATA. Kalvenor Systems is fictional. The Hub column is illustrative and fictional, and the receipt counts are a fictional sample of our format, not a measurement.

| Line, October 2026 | Hub, ChatGPT | Our receipts, ChatGPT | Reason code |
| --- | --- | --- | --- |
| Appearances | 1,240 impressions | Named in 9 of 29 valid answers | SCOPE |
| Visits and sources | 37 clicks | Cited in 4 of 29 valid answers | DEFINITION |
| Questions behind the count | Not shown | 10 buyer questions, each with receipts | NOT_SHOWN |
| Who is named instead | Not shown | Rival A (fictional) in 17 of 29 valid answers | NOT_SHOWN |
| Capture dates | Every day of the month | Scheduled runs on 6, 13 and 20 October | TIMING |

Claude, Perplexity, Google AI Overviews and Google AI Mode have receipts and no Hub counterpart, so their lines carry the reason code ENGINE.

| Engine, October 2026 | Planned | Valid | Named | Cited | Rival A named |
| --- | --- | --- | --- | --- | --- |
| ChatGPT | 30 | 29 | 9 of 29 | 4 of 29 | 17 of 29 |
| Claude | 30 | 30 | 7 of 30 | 3 of 30 | 15 of 30 |
| Perplexity | 30 | 30 | 11 of 30 | 6 of 30 | 14 of 30 |
| Google AI Overviews | 30 | 26 | 5 of 26 | 3 of 26 | 12 of 26 |
| Google AI Mode | 30 | 30 | 8 of 30 | 5 of 30 | 16 of 30 |

Planned answers are 10 buyer questions times 3 scheduled runs per engine. The ChatGPT exclusion is an answer that did not search the live web; the four Google AI Overviews exclusions are questions where no AI Overview was returned. Excluded answers leave both the count and its base, as our [method](https://broadcastwell.com/methodology) requires.

[Download the sample as CSV](https://docs.broadcastwell.com/examples/kalvenor-reconciliation-2026-10.csv). Every row repeats the SAMPLE DATA label and the fictional company name.

## How differences are explained

Each difference between the two records gets exactly one reason code and one sentence.

| Code | Meaning |
| --- | --- |
| SCOPE | The Hub counts every conversation; our receipts count a fixed set of buyer questions. The bases differ. |
| DEFINITION | A click is a visit; a citation is a source listed in an answer. A naming is not an impression. |
| NOT_SHOWN | The Hub does not show this line, so only the receipts carry it. |
| TIMING | The Hub counts daily; our receipts come from scheduled capture dates. |
| ENGINE | The line comes from an engine the Hub does not cover. |

When a month's figures move in opposite directions, for example Hub impressions up and our named count down, the report says so and names the likely codes. It does not pick a winner. If no code explains a gap, the line reads "unexplained" and stays in the report.

## What is never inferred

- No rate is computed from Hub counts over our answer base, or from our counts over Hub impressions.
- No prompt is inferred from a Hub count, and no Hub count is estimated for a competitor.
- No click is read as a lead, and no impression as a recommendation.
- No causal claim links a page change to a Hub count. A change on our side is reported only under the controlled-lift rules in our method.
- A missing month or a missing engine is missing, never zero.

## Related guides

- [How do you claim your business in ChatGPT?](index.md), our explainer and readiness checklist
- [What belongs in a business facts file for ChatGPT?](business-facts-file.md)
- [What goes in a context pack for a business agent?](context-pack.md)
- [Is the ChatGPT Business Hub available yet?](watch.md)

## Sources

- Barry Schwartz, [Search Engine Roundtable](https://www.seroundtable.com/chatgpt-tools-for-business-42476.html), and Juozas Kaziukėnas, [LinkedIn](https://www.linkedin.com/posts/juozas_chatgpt-is-building-an-analytics-tool-to-share-7524436371613118464-E3Zf/), both 6 November 2026, for the Hub's reported impressions and clicks and what it does not show.
- Broadcastwell, [Method v1.1](https://broadcastwell.com/methodology), for exclusions, bases and controlled lift.
