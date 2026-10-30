---
title: One rank number was already a fiction in 2009
description: Repeated September answers disagree about vendor naming. A dated practitioner warning helps explain
  why a single rank needs its observation conditions.
page_class: research
research_id: 4
research_group: insight
lead: Priya Nair
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/insights/one-rank-number-is-a-fiction/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://doi.org/10.5281/zenodo.22907695
---

# One rank number was already a fiction in 2009

**Mixed naming occurred in 1,259/14,192 complete repeat groups: 8.9%, Wilson 95% interval 8.4% to 9.4% (Broadcastwell, 2026, September engine_presence counts).**

The September answers disagreed about vendor naming in **1,259 of 14,192 complete vendor-question-engine groups**. Each group contains the same vendor, one fixed question and one engine, observed in three valid repeats: **8.9%**, descriptive **95% Wilson interval 8.4% to 9.4%**. [September release](https://doi.org/10.5281/zenodo.22907695), engine_presence fields; [derived table](../../data/repeat-disagreement.csv).

That is not a share of answers, and it is not a universal error rate. It is a precise reason to hesitate before treating a single answer as a settled position. A group is mixed when the vendor is named in some repeats and absent in others. Uniform presence and uniform absence both count as agreement.

Jill Whalen had a related objection long before modern AI answers. Asked about ranking measurement in the second edition of Jerri Ledford's SEO Bible, she called it “an impossible measurement” and pointed to personalization and geography. Those words are practitioner testimony from **2009**, not an experimental estimate of today's answer variability. [Ledford, printed p. 448; PDF p. 470].

## What did the old warning anticipate?

Whalen was talking about search positions presented to different users. Our table concerns repeated vendor naming in captured answers. We do not merge the two into one historical data series. The connection is conceptual: a position needs the conditions under which it was observed.

You can see the problem without a dashboard. A buyer asks for a shortlist. One answer names a vendor, another does not. If you save only the answer that happens to be visible when a report is prepared, the report omits a material part of the record. A confident label can conceal the fact that another valid answer gave a different inclusion decision.

The reverse is just as important. A vendor missing from a single answer has not been proven undiscoverable. That observation may be a real instance of absence, yet an incomplete description of the vendor's presence across questions and repeats. Both the positive and the negative example need their base.

## How much do repeat-disagreement rates differ by engine?

| Engine | Mixed complete groups / eligible complete groups | Mixed share | Descriptive 95% Wilson interval | Incomplete groups left out |
|---|---:|---:|---|---:|
| ChatGPT | 159 / 2,860 | 5.6% | 4.8% to 6.5% | 0 |
| Claude | 253 / 2,860 | 8.8% | 7.9% to 9.9% | 0 |
| Perplexity | 200 / 2,860 | 7.0% | 6.1% to 8.0% | 0 |
| Google AI Overviews | 302 / 2,752 | 11.0% | 9.9% to 12.2% | 108 |
| Google AI Mode | 345 / 2,860 | 12.1% | 10.9% to 13.3% | 0 |
| Combined | 1,259 / 14,192 | 8.9% | 8.4% to 9.4% | 108 |

Source: Broadcastwell, Absence Index release 2026-09, deposited release JSON, engine_presence entries, reanalysis dated 30 October 2026. A complete group has three valid target repeats. The intervals are descriptive: groups share questions, vendors and answers, so they are not independent trials. The table does not establish a statistically tested ranking of engine stability.

The capture archive contains **2,250 observations**, but that is not this table's denominator. That archive includes target and control captures. The public target base excludes **five unusable target observations**, leaving **2,095 valid target answers**; the complete-repeat table additionally excludes any affected vendor-question-engine group. [Release README and excluded_answer_uids].

Those distinctions matter. Dividing mixed groups by total captures would combine different units. Counting an unusable observation as a vendor absence would manufacture a negative verdict. Keeping an incomplete group while pretending it had all repeats would make engines with missing answers incomparable on this particular statistic.

## Agreement includes persistent absence

A low mixed share can sound reassuring. It can also occur when a vendor is absent from every repeat. The table measures disagreement, not the desirability or accuracy of the answer. An engine can be consistent and consistently omit a relevant vendor.

That is why the companion vendor-presence table retains counts and eligible answer bases. It answers how often a vendor was named. The disagreement table asks whether that naming decision differed within a repeated question. Neither tells us whether the recommendation met the buyer's needs.

There is a second asymmetry. A group named in one repeat and a group named in two repeats are both mixed here. That is intentional for the binary disagreement question. If you want the intensity of presence, use the underlying counts rather than treating this one statistic as a complete account.

## Keep the observation attached to the claim

A usable visibility statement identifies the question, engine, date, vendor definition and eligible base. It also distinguishes a product mention from a qualifying citation to the vendor's own domain. A report that silently alternates between those outcomes can appear to show a change that is really a definition change.

For a decision about a particular buyer question, retain the answer itself and the sources it presents. Aggregate presence can identify where to look. It cannot replace reading a source to determine whether the product's stated scope or factual details are correct.

This makes repeated observation useful even when no marketing action has been taken. You need some idea of ordinary variation before interpreting a later difference as an effect. A before-and-after anecdote with no repeat baseline can mistake the answer's variability for the impact of an edit.

## What does a more honest label require?

“Present in this captured answer” is less satisfying than a permanent rank. It is also easier to defend. A business still needs a summary, so the practical answer is a layered record: an understandable headline linked to counts, uncertainty and examples that retain their observation conditions.

You may prefer to inspect a narrow set of high-value buyer questions rather than summarize many unrelated questions. That choice can be reasonable, but the resulting sample describes that decision set. It should not be advertised as a share of the entire market's conversations.

The historical Whalen interview makes another uncomfortable point: a metric can be easy to collect and still be a poor proxy for the outcome a business wants. We do not have a measured relationship here between mixed naming groups and sales, qualified leads or customer understanding. Those outcomes require their own evidence. Repetition improves the description of answers; it does not turn that description into revenue attribution.

There is another choice hidden inside a summary. Equal weight for each checked vendor-question group answers a different question from equal weight for each category. Categories contain different checked sets. A pooled figure should retain its actual weighting rather than be described as the experience of a typical category or a typical buyer. The engine and category rows remain available for that reason.

For the next report, the open question is how much of the same pattern persists under a comparable later release. The registered persistence study specifies the conditions for that analysis. Until those observations exist, the table above remains a dated account of September repeats, including the groups where nothing changed at all.

## What our own data shows

The combined mixed share is 1,259 / 14,192 complete vendor-question-engine groups, 8.9% (descriptive 95% Wilson interval 8.4% to 9.4%). [Download the counts and engine/category breakdown](../../data/repeat-disagreement.csv). Primary observations: [Absence Index release 2026-09, DOI 10.5281/zenodo.22907695](https://doi.org/10.5281/zenodo.22907695). This reanalysis uses the deposited repeat counts, not a fresh scoring of each answer; it makes no claim about factual accuracy or commercial effect.

## Sources

- Broadcastwell. (2026). Absence Index, release 2026-09 [Data set]. Zenodo. Release JSON, answer JSONL and README. https://doi.org/10.5281/zenodo.22907695 Verified 30 October 2026.
- Ledford, J. L. (2009). SEO: Search engine optimization bible (2nd ed.). Wiley. Jill Whalen interview, printed pp. 447 to 449 (PDF pp. 469 to 471). ISBN 978-0-470-45264-6. https://books.google.com/books?vid=ISBN9780470452646 Verified 30 October 2026.
- Broadcastwell. (2026). Does absence persist from one release to the next? [Registration]. OSF. Registered 30 October 2026, 01:12:44 UTC. https://doi.org/10.17605/OSF.IO/MKJ9V Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *One rank number was already a fiction in 2009*. Broadcastwell. https://docs.broadcastwell.com/research/insights/one-rank-number-is-a-fiction/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research4,
  author = {{Broadcastwell research team}},
  title = {One rank number was already a fiction in 2009},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/insights/one-rank-number-is-a-fiction/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Priya Nair, management consultant.

Sources checked 30 October 2026. Independent check: 30 October 2026. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the measurement chapter](https://docs.broadcastwell.com/measurement-noise/).
