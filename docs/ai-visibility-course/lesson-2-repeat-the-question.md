---
title: 'Course lesson 2: why ask the same question three times?'
headline: 'Course lesson 2: why ask the same question three times?'
description: Lesson 2 of our free AI visibility course explains why we repeat each buyer question three times per engine and how to report a company named in only some runs.
page_class: page
schema_type: Article
date_published: '2026-11-09T00:00:00+00:00'
date_modified: '2026-11-09T00:00:00+00:00'
template: business-hub.html
---

# Course lesson 2: why ask the same question three times?

Lesson 2 of our AI visibility course: the same engine can return a different set of companies when you ask the same words again, so one run cannot tell a steady result from a passing one. In September 2026, 8.9 percent of vendor and question cells changed between three repeats on the same engine. Repeating the question shows which names hold.

Updated 9 November 2026.

Reading time: about 4 minutes. Lesson 2 of 5 in [the course](index.md). [Previous lesson](lesson-1-one-ai-answer.md).

## What the repeats showed

The September 2026 Index asked every target question three times on each engine. We then looked at every pairing of a checked vendor and a question on one engine where all three repeats were valid. A cell is "mixed" when the vendor was named in one or two of the three, rather than in none or all.

| Engine | Mixed cells / complete cells | Share | 95% Wilson interval |
| --- | ---: | ---: | --- |
| ChatGPT | 159 / 2,860 | 5.6% | 4.8% to 6.5% |
| Perplexity | 200 / 2,860 | 7.0% | 6.1% to 8.0% |
| Claude | 253 / 2,860 | 8.8% | 7.9% to 9.9% |
| Google AI Overviews | 302 / 2,752 | 11.0% | 9.9% to 12.2% |
| Google AI Mode | 345 / 2,860 | 12.1% | 10.9% to 13.3% |
| All five | 1,259 / 14,192 | 8.9% | 8.4% to 9.4% |

Most cells are stable, which is reassuring. But the cells that move are not spread evenly: Google AI Mode's mixed share is roughly twice ChatGPT's, and the two intervals do not overlap. A single run on the more variable engines is more likely to mislead.

Our method page puts the same point another way: in our September 2026 repeat-run study, 1,785 of 8,055 single-run vendor namings were not repeated in both other runs, 22.2 percent with an interval of 21.3 to 23.1 percent.

## How to report a partial result

Write the repeats as a count, never as yes or no.

- **Named in 3 of 3 valid repeats:** a steady result for that engine and wording on that date.
- **Named in 1 or 2 of 3:** a mixed result. Report it as such; do not round it up to "named" or down to "absent".
- **Named in 0 of 3:** absent from that question on that engine, on that date. Still not a statement about other engines or other wordings.

When a question and engine pair disagrees, our method allows up to two extra runs. Those [adaptive runs](../ai-search-glossary.md#adaptive-run) are kept and reported separately, and they never enlarge the scheduled base. Headline comparisons use the three scheduled runs only, so the panel stays the same size from one measurement to the next.

## Why three and not thirty

Repeats add dependence as well as evidence: answers on the same day from the same engine are not independent draws, so 30 repeats are not 30 times the evidence. Three scheduled runs separate steady results from passing ones while keeping every question on all five engines, ChatGPT, Claude, Perplexity, Google AI Overviews and Google AI Mode, in one panel. The trade-off is that a vendor named in 2 of 3 cannot be told apart from one named in 3 of 4 without more runs. Our Manual chapter on [how much a shortlist changes between repeats](../measurement-noise.md) covers the historical evidence on agreement.

## Exercise

A fictional company is checked on one question, three scheduled runs per engine. On one engine it appears in run 1 only. On a second engine it appears in all three runs. On a third engine run 2 failed with an error and runs 1 and 3 did not name it.

Write one line per engine using counts of valid repeats. For the third engine, decide what the base is before you write the count; lesson 3 checks your answer. Then say which engine's result you would trust least, and why.

## Sources

- Broadcastwell, [repeat disagreement table](../research/data/repeat-disagreement.csv), Absence Index release 2026-09, answers captured 22 and 23 September 2026, published with [Study 2](../research/studies/who-ai-engines-cite/index.md) on 30 October 2026.
- Broadcastwell, [measurement method v1.1](https://broadcastwell.com/methodology), repeated runs and adaptive runs, read 9 November 2026.

**Next lesson:** [Lesson 3: what is the base behind an AI visibility rate?](lesson-3-find-the-base.md)
