---
title: What do search patents say about AI answers?
headline: What do search patents say about AI answers?
description: We read nine public search patents and applications on 9 November 2026, eight from Google and one from Microsoft, and set out what each shows and cannot.
page_class: page
schema_type: Article
date_published: '2026-11-09T00:00:00+00:00'
date_modified: '2026-11-09T00:00:00+00:00'
template: business-hub.html
---

# What do search patents say about AI answers?

Nine public search patents and applications, read on Google Patents on 9 November 2026, describe generated summaries tied to their source documents, machine-written query variants, search that keeps a chat's state, retrieval trained on synthetic queries, scoring by information gain and checking quoted text against its source. Eight belong to Google and one to Microsoft. None of them proves that a feature runs in a live product.

Updated 9 November 2026.

A patent record tells you what a company asked to protect and when. It does not tell you what ships, to which users, for which queries, or in what form. We treat every record below as a description of an idea with dates attached, and we keep our own measurement of real answers separate from it.

## The nine records

| Record | Title as filed | Assignee | Priority date | Filed | Published or granted | Type |
| --- | --- | --- | --- | --- | --- | --- |
| [US11354342B2](https://patents.google.com/patent/US11354342B2/en) | Contextual estimation of link information gain | Google LLC | 18 Oct 2018 | 18 Oct 2018 | Granted 7 Jun 2022 | Granted patent |
| [US11663201B2](https://patents.google.com/patent/US11663201B2/en) | Generating query variants using a trained generative model | Google LLC | 29 Apr 2017 | 27 Apr 2018 | Granted 30 May 2023 | Granted patent |
| [US12579133B2](https://patents.google.com/patent/US12579133B2/en) | Generating query variants using a trained generative model | Google LLC | 29 Apr 2017 | 12 May 2023 | Granted 17 Mar 2026 | Granted patent |
| [US11769017B1](https://patents.google.com/patent/US11769017B1/en) | Generative summaries for search results | Google LLC | 30 Dec 2022 | 20 Mar 2023 | Granted 26 Sep 2023 | Granted patent |
| [US11886828B1](https://patents.google.com/patent/US11886828B1/en) | Generative summaries for search results | Google LLC | 30 Dec 2022 | 22 Aug 2023 | Granted 30 Jan 2024 | Granted patent |
| [US20250005303A1](https://patents.google.com/patent/US20250005303A1/en) | Generative summaries for search results | Google LLC | 30 Dec 2022 | 10 Sep 2024 | Published 2 Jan 2025 | Application, not granted as of 9 November 2026 |
| [US20240289407A1](https://patents.google.com/patent/US20240289407A1/en) | Search with stateful chat | Google LLC | 28 Feb 2023 | 27 Feb 2024 | Published 29 Aug 2024 | Application, not granted as of 9 November 2026 |
| [WO2024064249A1](https://patents.google.com/patent/WO2024064249A1/en) | Systems and methods for prompt-based query generation for diverse retrieval | Google LLC | 21 Sep 2022 | 21 Sep 2023 (international) | Published 28 Mar 2024 | International application; Google Patents shows it as ceased |
| [US20240296295A1](https://patents.google.com/patent/US20240296295A1/en) | Attribution verification for answers and summaries generated from large language models (llms) | Microsoft Technology Licensing LLC | 3 Mar 2023 | 3 Mar 2023 | Published 5 Sep 2024 | Application, not granted as of 9 November 2026 |

Dates and assignees are as each record showed them on 9 November 2026. Google Patents labels its legal status lines as assumptions rather than legal conclusions, so we print the record type and leave expiry estimates out.

## Generated summaries that point back to their sources

Three Google records share one title and one priority date, 30 December 2022: US11769017B1, US11886828B1 and the later application US20250005303A1. Their shared description covers a language model writing a natural-language summary of the documents returned for a query, drawing on content tied to related, recent or implied queries to reduce inaccuracy. Portions of the summary are linked to the documents that support them, and the summary can be revised when the user opens one of those documents.

**What it supports:** a written design in which a generated answer carries links to supporting pages. **What it does not support:** a claim that a given Google AI Overview was produced this way, or any statement about how often a particular page is linked. Our own count of what actually gets linked is an observation: in the September 2026 Index, Google AI Overviews returned 3,050 citation entries across 415 valid target answers. Those counts come from captured answers, not from the patent.

## Query variants written by a model

US11663201B2 and its continuation US12579133B2 describe a trained generative model that writes variants of a submitted query at run time, using the query's words and optional facts about the user or task, including for rare queries. Responses to the variants can feed the result for the original query, and a separate control model can decide how many variants to generate.

The idea predates the generative answer products by years: the priority date is 29 April 2017. Our [research entry on query fan-out](research/glossary/query-fan-out/index.md) covers Google's own 2025 description of related searches behind AI Mode. Neither source gives a publisher the variants for a particular question, which is why we hold the buyer's question wording fixed and report what the engine returned for it.

## Search that keeps the state of a chat

US20240289407A1 describes a "generative companion" that carries a user's state across chat-style search turns. It uses that state to write synthetic queries, choose search results, classify the query and pick which downstream generative models render the response.

**Reasoned:** if earlier turns can shape later results, a measurement of one typed question does not show what an engine returns after a longer conversation. That limit applies to every single-question measurement, ours included, and it is one reason we print the capture date and engine product beside each answer.

## Retrieval trained on synthetic queries

WO2024064249A1 describes prompting a large language model with a few task examples so that it writes synthetic query and document pairs from a corpus, then training a retrieval model on those pairs to predict relevant documents. Google Patents shows this international application as ceased; the record still documents the approach and its dates.

**Reasoned:** a retrieval system tuned this way learns from questions a model wrote, not only from questions people typed. That is a reason to describe a product in the plain words buyers use for their problem, which our free [ten-question buyer bank](question-bank.md) is built around.

## Information gain

US11354342B2 scores documents a user has not yet been shown by how much new information each adds beyond the documents already presented by an automated assistant or search interface, and uses those scores to order or present them. The scores may come from a machine learning model working on semantic representations of the documents.

Our [research entry on information gain](research/glossary/information-gain/index.md) records how the phrase moved from this patent into vendor blogs. **What it supports:** a published design that rewards addition over repetition. **What it does not support:** a ranking factor, a score you can read, or proof that any engine applies it today.

## Checking quoted text against the source

Microsoft's application US20240296295A1 describes asking a language model to return verbatim quotes with source identifiers from a supplied document, parsing those quotes out of the output and string-matching each one against the source. Each quote is then labeled verified, partially verified or unverified.

**Reasoned:** the problem it addresses is real. A citation in an answer can point to a page that does not say what the answer says. Our guide to [checking whether an AI citation supports its claim](answers/measurement/how-can-i-check-whether-an-ai-citation-supports-its-claim.md) covers how a buyer can test that by hand.

## What a buyer can and cannot conclude

1. **A patent is not a launch.** None of the nine records establishes that a feature is deployed, where, or for whom. Product behavior is evidence only when it is observed and dated.
2. **Four dates mean four different things.** Priority, filing, publication and grant are separate events. US11663201B2 claims priority from 29 April 2017 but was granted on 30 May 2023; quoting only one date misstates the record.
3. **An application can still change.** Four of the nine are applications: three US applications not granted as of 9 November 2026, whose claims may be narrowed or refused, and one international application shown as ceased.
4. **Status lines are estimates.** Google Patents describes its legal status as an assumption, so a "granted" or "ceased" label is a starting point for checking, not a legal opinion.
5. **Nothing here is a recipe.** No record names a page feature that guarantees a citation. Our note on [why no study can give a ranking recipe](research/insights/no-ranking-recipe/index.md) makes the same point from published research.

## How this connects to what we measure

We measure answers, not intentions. The patents describe linked summaries, expanded queries and stateful sessions; our method fixes the buyer question, records the five engines ChatGPT, Claude, Perplexity, Google AI Overviews and Google AI Mode separately, and keeps every cited source with its receipt. Our chapter on [how far the engines diverge](engine-divergence.md) shows why one engine's behavior does not transfer to another, and our [glossary](ai-search-glossary.md) defines each counted event.

## Sources

Each record was read on Google Patents on 9 November 2026:

- [US11354342B2](https://patents.google.com/patent/US11354342B2/en), Google LLC, inventors include Victor Carbune and Pedro Gonnet Anders.
- [US11663201B2](https://patents.google.com/patent/US11663201B2/en), Google LLC, inventors include Jyrki Alakuijala, Christian Buck and Jannis Bulian.
- [US12579133B2](https://patents.google.com/patent/US12579133B2/en), Google LLC, same inventors as US11663201B2.
- [US11769017B1](https://patents.google.com/patent/US11769017B1/en), Google LLC, inventors include Matthew K. Gray, John Blitzer and Corinn Herrick.
- [US11886828B1](https://patents.google.com/patent/US11886828B1/en), Google LLC, same inventors as US11769017B1.
- [US20250005303A1](https://patents.google.com/patent/US20250005303A1/en), Google LLC, same inventors as US11769017B1.
- [US20240289407A1](https://patents.google.com/patent/US20240289407A1/en), Google LLC, inventors include Mahsan Rofouei, Anand Shukla and Qing Wei.
- [WO2024064249A1](https://patents.google.com/patent/WO2024064249A1/en), Google LLC, inventors include Zhuyun Dai, Yuzhe Zhao and Ji Ma.
- [US20240296295A1](https://patents.google.com/patent/US20240296295A1/en), Microsoft Technology Licensing LLC, inventors include James Simon Russell, Mary Sugino David Pasch and Jingtian Jiang.
- Broadcastwell, [Study 2 answer citation bases](research/data/answer-citation-bases.csv), Absence Index release 2026-09, answers captured 22 and 23 September 2026.

Related: our [open data catalog](open-data.md) lists the tables behind every count we cite.
