---
title: 'Course lesson 3: what is the base behind a rate?'
headline: 'Course lesson 3: what is the base behind a rate?'
description: Lesson 3 of our free AI visibility course finds the base behind a visibility rate, takes failed answers out of both sides and reads the interval it supports.
page_class: page
schema_type: Article
date_published: '2026-11-09T00:00:00+00:00'
date_modified: '2026-11-09T00:00:00+00:00'
template: business-hub.html
---

# Course lesson 3: what is the base behind a rate?

Lesson 3 of our AI visibility course: the base is the number of valid answers a rate is divided by, and it decides how much the rate can be trusted. Failed, empty and refused answers leave both the count and the base. A rate printed without its base, or without the interval that base supports, cannot be checked.

Updated 9 November 2026.

Reading time: about 4 minutes. Lesson 3 of 5 in [the course](index.md). [Previous lesson](lesson-2-repeat-the-question.md).

## From planned answers to the base

Every measurement starts with planned answers and ends with a smaller number you can score. In the September 2026 Absence Index the steps were:

| Step | Count |
| --- | ---: |
| Target questions | 140 |
| Planned attempts: each question on ChatGPT, Claude, Perplexity, Google AI Overviews and Google AI Mode, three runs each | 2,100 |
| Attempts excluded, each with its recorded reason | 5 |
| Valid answers, the base | 2,095 |

All five exclusions were Google AI Overviews attempts: four where no AI Overview appeared and one where Google returned no valid results. So Google AI Overviews has a base of 415 valid target answers, while ChatGPT, Claude, Perplexity and Google AI Mode have 420 each. A rate for that engine divides by 415, not by 420, and the five missing answers are not counted as misses.

That last rule matters. If a failed capture were scored as "not named", every company in that category would look a little more absent than it was. Our [excluded answers table](../research/data/excluded-answers.csv) lists each one by engine, category, question and repeat.

## Reading a rate with its interval

Take the fictional Kalvenor sample, a made-up company we publish to show the format. Its fictional baseline planned 525 answers, excluded 7 and scored 518.

| Fictional sample | Count and base | Rate | 95% Wilson interval |
| --- | --- | ---: | --- |
| Kalvenor named, all engines | 125 of 518 | 24.1% | 20.6% to 28.0% |
| Kalvenor's own pages cited | 66 of 518 | 12.7% | 10.1% to 15.9% |
| Kalvenor named, ChatGPT, baseline run of 12 July 2026 | 15 of 29 | 51.7% | 34.4% to 68.6% |

The ChatGPT rate looks twice as good as the overall rate. Its interval is also more than four times as wide, because 29 answers carry far less evidence than 518. Read the interval as the range of rates the data is consistent with: for ChatGPT, anything from about a third to about two thirds.

The same arithmetic explains why a count of 2 of 3 is not "67 percent". Its interval runs from 20.8 to 93.9 percent, which says almost nothing. That is why small bases are best reported as counts.

## Three habits

1. **Ask for the base before the rate.** "52 percent" invites a conclusion; "15 of 29" shows you how much evidence there is.
2. **Check the exclusions.** A base that silently shrinks, or a failure scored as a miss, changes the answer without anyone saying so.
3. **Compare intervals, not points.** When two intervals overlap, no difference between the two rates is established.

The three rates we report, named, cited and share of voice, each have their own base; our page on [how naming, citation and share of voice differ](../resources/three-rates.md) sets them side by side. The Manual's chapter on [interpretable measurement](../valid-measurement.md) gives the longer argument.

## Exercise

Return to the third engine from lesson 2: run 2 failed and runs 1 and 3 did not name the fictional company. Write its result as a count and base. (It is 0 of 2 valid repeats, not 0 of 3.)

Then, for the fictional Kalvenor sample, write one sentence a manager could read in five seconds that keeps both the ChatGPT count and its base, without the percentage. Compare it with the sentence "Kalvenor wins 52 percent on ChatGPT" and note what the second sentence hides.

## Sources

- Broadcastwell, <a href="https://index.broadcastwell.com/data/benchmark/README.md">Absence Index benchmark README</a>, September 2026 attempts, valid answers and exclusions, read 9 November 2026.
- Broadcastwell, [answer citation bases](../research/data/answer-citation-bases.csv), valid target answers by engine, published 30 October 2026.
- Broadcastwell, [measurement method v1.1](https://broadcastwell.com/methodology), scoring rules and uncertainty, read 9 November 2026.
- Broadcastwell, [fictional Kalvenor sample](https://app.broadcastwell.com/sample), values as shown on our [completed-case format](../cases/format.md) page; Wilson intervals recomputed by us.

**Next lesson:** [Lesson 4: which sources do AI answers cite?](lesson-4-read-the-sources.md)
