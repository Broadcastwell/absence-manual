---
title: 'AI search glossary: what does each term mean?'
headline: 'AI search glossary: what does each term mean?'
description: Our AI search glossary defines 47 terms we use when we measure AI answers, from citation and named to base, Wilson interval and receipt, each with its source.
page_class: page
schema_type: Article
date_published: '2026-11-09T00:00:00+00:00'
date_modified: '2026-11-09T00:00:00+00:00'
template: business-hub.html
---

# AI search glossary: what does each term mean?

This AI search glossary gives one plain definition for each of 47 terms we use when we measure what AI answers say about companies, and every entry ends with the source that fixes its meaning. The most asked-for entry is [citation](#citation): a source an engine lists with its answer, which is a different event from the company being named.

Updated 9 November 2026.

Each term has its own anchor, so you can link straight to it, for example `https://docs.broadcastwell.com/ai-search-glossary/#citation`. Where a term has a longer research entry, we link it rather than repeat it. The Manual's own [Appendix D](glossary.md) keeps the vocabulary of the three State of GEO volumes; this page covers the words a buyer meets in our current reports, offers and Index releases.

## Answers and engines

### Answer engine {#answer-engine}

A product that replies to a typed question with written text rather than a list of links, often with sources attached. We measure five of them: ChatGPT, Claude, Perplexity, Google AI Overviews and Google AI Mode, and each receives identical wording. Source: [our method, v1.1](https://broadcastwell.com/methodology).

### AI Overview {#ai-overview}

The generated summary Google shows on some results pages, with links to supporting pages. Google says AI Overviews often do not trigger, and our captures agree: in the September 2026 Index, four target attempts were recorded with the reason "no AI Overview returned for this query". Source: [Google Search Central, AI features and your website](https://developers.google.com/search/docs/appearance/ai-features), last updated 10 December 2025; [our excluded answers table](research/data/excluded-answers.csv).

### AI Mode {#ai-mode}

Google's AI search mode for questions that need more exploration, reasoning or comparison, answered in its own view with links to supporting sites. Google says AI Mode and AI Overviews may use different techniques, so their responses and links vary; we read AI Mode in AI Mode itself and record it apart. Source: [our method, v1.1](https://broadcastwell.com/methodology); [Google Search Central](https://developers.google.com/search/docs/appearance/ai-features).

### Web search on {#web-search-on}

The capture setting in which an engine may read live web pages before it answers. Our rule for ChatGPT is that an answer given without live web search leaves the base, so it is neither a hit nor a miss. Source: [our method, v1.1](https://broadcastwell.com/methodology).

### Grounding {#grounding}

The pages and facts an engine retrieves and relies on while it writes a reply. Microsoft uses the phrase "grounding queries" for the searches behind citations in its own AI reporting. We record the visible result of grounding, the cited sources, never the hidden searches. Source: [Bing Webmaster Blog, Introducing AI Performance in Bing Webmaster Tools](https://blogs.bing.com/webmaster/2026/2/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview/), 10 February 2026.

### Query fan-out {#query-fan-out}

One question expanded into several related searches before the answer is assembled. Google describes AI Overviews and AI Mode as able to use it; no engine publishes the expansions for a given question. Our [research entry on query fan-out](research/glossary/query-fan-out/index.md) gives the dated operator description. Source: [Google Search Central](https://developers.google.com/search/docs/appearance/ai-features).

### Zero-click {#zero-click}

A visit that does not happen: the reader got what they needed from the answer and never opened a source. It is why answer measurement and visit measurement have to stay separate. Our [research entry on zero-click visibility](research/glossary/zero-click-visibility/index.md) sets out its sources and limits.

## What we count in an answer

### Named {#named}

The answer mentions the company as itself. We count it once per answer however many times it appears, and a longer word that merely contains the brand string does not count. Tone is not scored; a critical mention is still a mention. Source: [our method, v1.1](https://broadcastwell.com/methodology).

### Citation {#citation}

A citation is a source an engine attaches to its answer: a link or reference the reader can open to see where a statement came from. It records which page the engine pointed to, not whether the engine recommended anyone. In our counts a citation belongs to a company only when the listed source resolves to that company's own hostname or a confirmed alias, subdomains included; an uncited mention is never a citation. A company can be cited without being named, and named without being cited, which is why we report the two side by side and never add them. Sources: [our method, v1.1](https://broadcastwell.com/methodology); [our study of who AI engines cite](research/studies/who-ai-engines-cite/index.md).

### Own-domain citation {#own-domain-citation}

An answer with at least one listed source on the company's domain or a confirmed alias. The rate divides those answers by the same valid-answer base used for naming. Similar-looking domains are excluded. Source: [our method, v1.1](https://broadcastwell.com/methodology).

### Citation array {#citation-array}

The full list of sources saved with one answer, in the order the engine gave them. In the September 2026 Index the 2,095 valid target answers carried 18,893 citation entries. Source: [Study 2 data, answer citation bases](research/data/answer-citation-bases.csv).

### Zero-citation answer {#zero-citation-answer}

A valid answer whose citation array is empty. In September 2026, 39 of 2,095 target answers had none: 1.9 percent, Wilson 95 percent interval 1.4 to 2.5 percent. Source: [Study 2](research/studies/who-ai-engines-cite/index.md).

### Source class {#source-class}

The kind of site a cited host belongs to, such as vendor site, review platform, news or trade media, forum, video, directory or other. Each host's class comes with an evidence address, a rationale and the date it was checked. Source: [Study 2 host classes](research/data/host-classes-post-audit.csv).

### Recommendation position {#recommendation-position}

Where a company sits in a shortlist that has a visible order. We record it only when the answer gives a discernible order; the order of paragraphs is not a ranking. Source: [our method, v1.1](https://broadcastwell.com/methodology).

### Competitor named {#competitor-named}

A rival agreed with you before the run, counted under the same naming rule as your company. Source: [our method, v1.1](https://broadcastwell.com/methodology).

### Share of voice {#share-of-voice}

Answers naming the company divided by the mentions of the company and its recorded rivals across those answers, with each brand counted once per answer. It is a share of recorded mentions, not of answers or of every brand in a market. Source: [our method, v1.1](https://broadcastwell.com/methodology). A related vendor metric is described in our [research entry on Share of Model](research/glossary/share-of-model/index.md).

### Record accuracy {#record-accuracy}

How often classified statements about a company are correct, wrong or stale against dated evidence. Unverifiable is its own result, and a missing classification never implies zero errors. Source: [our method, v1.1](https://broadcastwell.com/methodology).

### Absence {#absence}

A valid answer to a buyer question that does not name the company. A failed or unavailable capture is not an absence, and a vendor that is not in a checked set has no measured absence at all. Source: [our free academic access terms](research/academic-access/index.md).

### Naming concentration {#naming-concentration}

The share of all checked-vendor mentions in a category taken by its three most-named vendors. In September 2026 CRM answers, three vendors held 319 of 476 checked-vendor naming occurrences: 67.0 percent, interval 62.7 to 71.1 percent. Source: [our concentration analysis](research/insights/one-channel-is-a-risk/index.md).

## Questions and panels

### Buyer question {#buyer-question}

A question worded the way a buyer researches a purchase, without your brand name in it. A full baseline uses 35 of them: 10 shortlist, 10 buyer-role, 10 use-case and 5 evaluation or pricing questions. Source: [our method, v1.1](https://broadcastwell.com/methodology); our free [ten-question buyer bank](question-bank.md).

### Branded question {#branded-question}

A question that includes the company's name. It measures what engines say about a company a buyer already knows, so we keep it in a separate set from discovery questions. Source: [our method, v1.1](https://broadcastwell.com/methodology).

### Question shape {#question-shape}

The pattern a question follows. The September 2026 Index tags every question with one of five: best option, specific workflow, top tools, alternative or buyer evaluation. Twelve of its 14 categories ask three best option, three alternative, three buyer evaluation and one specific workflow question. Source: [Index release 2026-09](https://doi.org/10.5281/zenodo.22907695).

### Frozen panel {#frozen-panel}

A question set whose wording is agreed before capture and then fixed. Changing one question opens a new baseline and ends the old comparison. Source: [our method, v1.1](https://broadcastwell.com/methodology).

### Baseline {#baseline}

The first dated measurement of a frozen panel, against which every later reading is compared under the same method version. Source: [our method, v1.1](https://broadcastwell.com/methodology).

### Checked set {#checked-set}

The vendors the Index looks for in each category, chosen by a written selection rule and dated directory captures. September 2026 checked 286 vendors across 14 categories. Source: [Index release 2026-09](https://doi.org/10.5281/zenodo.22907695).

### Control question {#control-question}

A question run outside the target panel to check the capture setup, for example ten control questions in two categories in September 2026. Its 150 answers never enter the target base. Source: <a href="https://index.broadcastwell.com/data/benchmark/README.md">Index benchmark README</a>.

## Runs, bases and uncertainty

### Scheduled run {#scheduled-run}

One planned asking of a question on an engine. We schedule three per question and engine, so 35 questions on five engines make 525 scheduled observations. Headline comparisons use scheduled runs only. Source: [our method, v1.1](https://broadcastwell.com/methodology).

### Adaptive run {#adaptive-run}

An extra run, at most two, given to a question and engine pair whose scheduled runs disagree. Adaptive answers are kept and reported apart; they never enlarge the panel. Source: [our method, v1.1](https://broadcastwell.com/methodology).

### Valid answer {#valid-answer}

A captured answer that can be scored: not empty, not an error and not a refusal. Only valid answers enter a numerator or a denominator. Source: [our method, v1.1](https://broadcastwell.com/methodology).

### Excluded answer {#excluded-answer}

An attempt removed from both the count and the base, listed with its engine, question and reason. September 2026 recorded five exclusions among 2,100 target attempts. Source: [our excluded answers table](research/data/excluded-answers.csv).

### Base {#base}

The number a rate is divided by, printed beside it. "15 of 29" tells you more than "52 percent", because the base shows how much evidence sits behind the share. Source: [our method, v1.1](https://broadcastwell.com/methodology).

### Wilson interval {#wilson-interval}

A 95 percent range for a proportion that behaves sensibly near zero and at small bases. We print it beside every headline proportion. When two companies' intervals overlap, no order between them is established. Source: [our method, v1.1](https://broadcastwell.com/methodology).

### Repeat disagreement {#repeat-disagreement}

A company named in one or two of three valid repeats of the same question on the same engine, rather than in none or all three. In September 2026 that held for 1,259 of 14,192 complete vendor and question cells: 8.9 percent, interval 8.4 to 9.4 percent. Source: [repeat disagreement data](research/data/repeat-disagreement.csv).

### Controlled lift {#controlled-lift}

The change on target questions minus the change on untouched control questions drawn from the same bank, each with its own interval. Lift is shown only when the lower bound is above zero and the targets rose. Source: [our method, addendum v1.2](https://broadcastwell.com/methodology).

### Method version {#method-version}

The written rules a measurement was taken under. A change to the questions, engines, collection or scoring opens a new version, and historical figures keep the version they were measured under. Current: v1.1. Source: [our method](https://broadcastwell.com/methodology).

## Records and releases

### Receipt {#receipt}

The saved record behind one counted answer: the question, engine product, time, full answer, cited sources and any exclusion reason. A count without its receipts cannot be checked. Our [receipt demonstration](resources/demos/receipt.md) walks through one. Source: [our method, v1.1](https://broadcastwell.com/methodology).

### Index release {#index-release}

A dated, citable publication of the Absence Index with its own version DOI. Release 2026-09 was published on 23 September 2026 as DOI 10.5281/zenodo.22907695. Source: [how to cite our research](cite.md).

### Erratum {#erratum}

A dated correction published beside the original record, which stays readable. Our errata table keeps the before and after wording. Source: [research errata, 3 November 2026](research/data/research-errata-2026-11-03.csv).

## Site signals

### llms.txt {#llms-txt}

A plain text file at the root of a website that lists the pages its owner wants language models to read first. In our method it is optional context, never a required fix, and publishing one does not establish indexing or citation. Source: [our method, v1.1](https://broadcastwell.com/methodology); our answer on [what an llms.txt file is](answers/fixes/what-is-an-llms-txt-file.md).

### Crawler policy {#crawler-policy}

The robots.txt rules that tell named crawlers what they may fetch. We read the applicable group and the longest matching rule, with Allow winning ties, and we record an access probe separately from any real crawler visit. Source: [our method, v1.1](https://broadcastwell.com/methodology); our [bot access guide](resources/bot-access.md).

### Google-Extended {#google-extended}

A robots.txt policy token Google offers for some uses of site content. It is not a fetcher and not the access decision for Google Search, which both Google answer products read through Googlebot. Source: [our method, v1.1](https://broadcastwell.com/methodology).

### Structured data {#structured-data}

Labels in a page's code, such as Organization, Product or Offer, that state facts in a form machines can read. Our [structured data playbook](research/playbooks/structured-data-for-b2b-software/index.md) covers what belongs on a software site.

### Information gain {#information-gain}

What a page adds beyond what a reader has already seen. The phrase comes from a Google patent; our [research entry on information gain](research/glossary/information-gain/index.md) and our [search patents analysis](search-patents.md) cover what a patent can and cannot show.

## The category

### GEO {#geo}

Generative engine optimization: work aimed at how generated answers describe and cite a company. Our [research entry on SEO, AEO and GEO](research/glossary/seo-aeo-geo/index.md) traces the terms.

### AEO {#aeo}

Answer engine optimization: work on how a page's content is presented as a direct answer. In practice the phrase overlaps with GEO; the research entry above separates the two by what each measures. Source: [our research entry](research/glossary/seo-aeo-geo/index.md).

### AI referral {#ai-referral}

A visit your analytics tool classifies as arriving from an AI assistant. Google Analytics 4's default channel group has an "AI Assistant" channel that excludes Google AI Overviews and AI Mode, which it counts as Organic Search. A referral is a visit record, not proof that an engine cited you. Source: [Google Analytics Help, Default channel group](https://support.google.com/analytics/answer/9756891), read 9 November 2026; our answer on [what a recorded AI referral establishes](answers/measurement/what-does-a-recorded-ai-referral-establish.md).

### Vendor Facts File {#vendor-facts-file}

A machine-readable file of a vendor's approved facts that assistants can read from a connector. Our [Vendor Facts standard](vendor-facts.md) defines the fields; the [business facts file guide](chatgpt-business-hub/business-facts-file.md) shows the version for a business site.

## Sources

- Broadcastwell, [measurement method v1.1 and addendum v1.2](https://broadcastwell.com/methodology), read 9 November 2026.
- Broadcastwell, [Absence Index release 2026-09](https://doi.org/10.5281/zenodo.22907695), published 23 September 2026, answers captured 22 and 23 September 2026.
- Broadcastwell, [Study 2: who appears in the sources of B2B software answers](research/studies/who-ai-engines-cite/index.md) and its [data tables](open-data.md), published 30 October 2026.
- Google Search Central, [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features), last updated 10 December 2025, read 9 November 2026.
- Google Analytics Help, [Default channel group](https://support.google.com/analytics/answer/9756891), read 9 November 2026 (no date shown).
- Microsoft Bing Webmaster Blog, [Introducing AI Performance in Bing Webmaster Tools Public Preview](https://blogs.bing.com/webmaster/2026/2/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview/), 10 February 2026.

Related: our [free course on reading AI answers](ai-visibility-course/index.md) uses these terms lesson by lesson, and our [chart library](chart-library.md) shows them in published figures.
