---
title: "Chapter 4. Who the engines actually cite"
headline: "Who the engines actually cite: the composition of the evidence layer behind AI answers"
description: "Among the 100 most-cited domains in Volume I, 77.4% of citations resolved to vendor-authored content. Community sources accounted for 0.0% of all 5,160 citations. The top 10 domains held only 12%, and 56% of cited domains appeared exactly once."
page_class: chapter
schema_type: TechArticle
date_published: "2026-08-18T00:00:00+00:00"
date_modified: "2026-08-18T00:00:00+00:00"
is_based_on: "https://doi.org/10.5281/zenodo.21537014"
---

# Chapter 4. Who the engines actually cite

By the end of this chapter you will know what kinds of source an AI engine reached for when it answered B2B software buying questions, how concentrated or fragmented that evidence layer is, and which of those figures carry which denominator, because two of the headline numbers in this chapter are computed on different bases and are routinely quoted as though they were not.

## The claim this chapter defends

**Measured, Volume I.** Among the 100 most-cited domains, 77.4% of citations resolved to vendor-authored content, 10.2% to review platforms, 6.5% to independent media and 5.9% to analyst firms. **Measured, Volume I.** Community sources, meaning Reddit, Quora and Stack Overflow, accounted for 0.0% of all 5,160 citations. **Reasoned.** The evidence an engine reached for was overwhelmingly published by vendors, and the places practitioners assume carry weight in software buying did not appear at all.

> **Operator disclosure.** Broadcastwell ran this measurement and sells services in the category it measures. Broadcastwell is excluded from the measured sample and from every ranking. The mitigation is not that the conflict is absent, it is that the raw data and the code are public and the result can be recomputed by anyone who disagrees.

## Two denominators, and why the difference matters

**Measured, Volume I.** The composition figures above are computed across the 100 most-cited domains, and those 100 domains account for 36% of all citations. The community figure is stated against the full corpus of 5,160 citations. **Reasoned.** So 77.4% vendor-authored is a statement about the head of the distribution, not about every citation the engine made. Quoting it as "77% of all AI citations are vendor content" overstates what was measured by attaching a corpus-wide denominator to a head-of-distribution figure. This manual states the base every time, and you should demand the same of anyone quoting it at you.

## What was counted

**Measured, Volume I.** Every cited URL across the sweep was logged, producing 5,160 traced source citations. The 100 most-cited domains were then classified by hand into vendor-authored, review platform, analyst, independent media, community, encyclopaedia and social categories. **Reasoned.** Hand classification of a hundred domains is tractable and auditable, and it is also the limiting factor on the resolution of this chapter. Nothing is known about the composition of the citations outside those 100 domains beyond the domains themselves, which are published.

## The head of the distribution, concretely

**Measured, Volume I.** The single most-cited domain was pipeline.zoominfo.com with 132 citations, classified vendor-authored. Second was gartner.com with 110, classified analyst. Fourth was g2.com with 57, classified review platform. **Reasoned.** The top of the list is not a list of publishers. It is mostly a list of software companies publishing about their own category, interleaved with the two or three third-party institutions that survive at that altitude. A vendor reading this list is looking at the pages that were doing the work of explaining its market to an engine.

## Below the top few, it is vendors all the way down

**Measured, Volume I.** Ranks three, five, six and seven of the most-cited domains were algolia.com with 69 citations, salesmotion.io with 50, guideflow.com with 47 and improvado.io with 46, all four classified vendor-authored. **Reasoned.** The pattern at the top is not a handful of vendor domains surrounded by publishers. It is a run of individual software companies, punctuated by one analyst domain and one review platform. If you are looking for the publications that explain your market to an engine, in this dataset they are largely your competitors' own pages.

## The most-named brand and the most-cited domain are different companies

**Measured, Volume I.** The most-named brand across the sweep was 6sense, with 123 mentions. The most-cited domain was pipeline.zoominfo.com, with 132 citations. **Reasoned.** The company whose material the engine leaned on hardest and the company the engine recommended most often were not the same company. That is the finding of Chapter 3 at [/cited-not-recommended/](https://docs.broadcastwell.com/cited-not-recommended/) visible at the very top of both distributions, and it is a useful corrective to the assumption that the way to be recommended is to become the most-quoted source in your category.

## What the taxonomy cannot separate

**Measured, Volume I.** Classification was assigned per domain, into vendor-authored, review platform, analyst, independent media, community, encyclopaedia and social. **Reasoned.** A per-domain label cannot distinguish a comparison page from a pricing page on the same vendor domain, nor an editorially independent article from sponsored placement on a media domain. It also forces single labels onto domains that do more than one thing. The consequence is that the composition figures are reliable about which organisation published a source and unreliable about what kind of content the source was, which is a real limit on how far they can be pushed.

## The evidence layer is fragmented, not concentrated

**Measured, Volume I.** The top 10 domains held only 12% of all citations, and 56% of cited domains appeared exactly once. **Reasoned.** That is a long tail, and it sits in tension with the concentration seen on the vendor-naming side, where a small set of names took a large share of the slots. Concentrated outputs assembled from a fragmented input layer is a specific structure: there is no small set of publications to be present in, because there is no small set of publications doing the work.

## How many distinct places the engine went

**Measured, Volume I dataset documentation.** The published dataset README records 1,753 unique domains cited across the sweep. This figure appears in the dataset documentation rather than in a paper body, and is labelled accordingly here. **Reasoned.** 1,753 distinct domains behind 5,160 citations is roughly three citations per domain on average, which is another way of saying the same thing the single-appearance share says: the engine went to a very large number of places, most of them once.

## What fragmentation rules out

**Reasoned.** It rules out a media-placement strategy as the primary route. If twelve percent of citations sit in ten domains, then winning a place in all ten would still leave the great majority of the evidence layer untouched. It also rules out the reverse assumption, that the tail is where the work is, since a single appearance in one of the many domains cited exactly once is worth very little on its own. What it points to instead is breadth of corroboration rather than placement in any particular outlet.

## The community result is the surprising one

**Measured, Volume I.** Community sources accounted for 0.0% of all 5,160 citations. **Reasoned.** Practitioner folklore holds that software buyers read Reddit threads and that engines therefore surface them. On these questions, on this engine, in this window, that did not happen once in five thousand one hundred and sixty citations. The honest reading is narrow: it is a fact about one engine's retrieval on B2B software buying questions in July 2026, and it says nothing about consumer categories or about other engines, one of which is measured differently in Chapter 5 at [/engine-divergence/](https://docs.broadcastwell.com/engine-divergence/).

## Why a zero is worth more attention than a small number

**Reasoned.** A category at two or three percent would be a minor contributor. A category at zero across the whole corpus is a structural absence, and structural absences are more informative than small positives because they cannot be explained by sampling noise in the same way. It also means any strategy premised on community presence feeding AI answers has no support in this dataset and needs its own evidence before anyone spends against it.

## Analyst and review presence, in proportion

**Measured, Volume I.** Within the top 100 domains, review platforms took 10.2% of citations and analyst firms 5.9%. **Reasoned.** Both are present and neither is dominant. That is a more useful reading than either the claim that review sites are the gatekeepers of AI answers or the claim that they no longer matter. They are one input among several, they punch above their number of domains because a single review platform can carry many citations, and a vendor absent from them is absent from roughly a tenth of the head of the evidence layer.

## What this implies about where evidence has to exist

**Reasoned.** If the head of the layer is mostly vendor-authored and the tail is enormous and thin, then the practical requirement is that material describing your category, and describing you as a member of it, exists in enough independent places that an engine assembling a candidate set encounters it more than once. That is a statement about corroboration rather than about volume, and the standards for it are the subject of Chapter 9 at [/category-door/](https://docs.broadcastwell.com/category-door/).

## Your own domain is a separate question

**Measured, Volume I.** Each answer was scored for whether the company's own domain appeared among cited sources, independently of whether the brand was named. **Reasoned.** So a vendor-authored citation share of 77.4% at the head of the distribution does not imply that your vendor-authored pages will be cited, still less that being cited will get you named. Chapter 3 at [/cited-not-recommended/](https://docs.broadcastwell.com/cited-not-recommended/) shows those two outcomes moving apart, including nine companies cited as a source while never being named at all.

## Limitation: the classification is by hand and by domain

**Measured, Volume I.** The type assignment was made by hand, at domain level, for the 100 most-cited domains only. **Reasoned.** Domain-level classification cannot distinguish an independent review published on a vendor's domain from a product page on the same domain, and hand assignment is a judgement that another analyst would make differently at the margins. The classification and the underlying counts are published, so anyone who disagrees with a call can reclassify and recompute rather than argue about it.

## Limitation: one engine, one run, one window

**Measured, Volume I.** All citations came from a single engine with live web search, one run per question, collected between 18 and 23 July 2026. **Reasoned.** Citation behaviour is a property of a retrieval stack, and retrieval stacks differ between products and change over time. Chapter 5 at [/engine-divergence/](https://docs.broadcastwell.com/engine-divergence/) reports the same composition question measured across four engines in August 2026 and finds the vendor-owned share varies widely between them, which is the correct caution to carry into any use of the figures in this chapter.

## Limitation: citation is not endorsement and not traffic

**Reasoned.** A cited URL is a URL the engine used while composing an answer. It is not a claim that the source was read favourably, that the buyer clicked it, or that it influenced the recommendation. Nothing in this dataset observes a buyer, and nothing in it observes the weight the engine placed on any individual source. Read the composition as a description of what the engine reached for, and not as a ranking of influence.

## The measurement standard this chapter implies

**Reasoned.** Any citation statistic offered to you should arrive with four things attached: the corpus size it was computed over, the subset it was computed on if that subset is not the whole corpus, the classification scheme and who applied it, and the collection window. Volume I publishes all four, which is why its figures can be quoted precisely and why the precision is worth insisting on. A citation composition chart with none of the four is a chart whose numbers cannot be checked or compared with anybody else's.

## Why comparing citation studies is harder than it looks

**Reasoned.** Two studies can report very different vendor-owned shares without either being wrong, because the share depends on which subset was classified, how the taxonomy draws its lines, which engine was measured and when. Chapter 5 at [/engine-divergence/](https://docs.broadcastwell.com/engine-divergence/) shows the same quantity varying substantially between four engines measured in a single window, which puts a floor under how much of the disagreement between published studies is real difference rather than methodological difference.

## What this chapter does not claim

**Reasoned.** It does not claim that vendor-authored content is the best evidence, that engines prefer it on quality grounds, or that publishing more of it will get you cited. It does not claim community sources are worthless, only that they did not appear here. And it does not claim these proportions hold outside US English B2B software buying questions on one engine in one week, because the sample cannot support that and Volume I says so.

## What this means for your buying decision

**Measured, Volume I, and reasoned from it.** Ask any supplier which denominator their citation statistics use, because head-of-distribution and whole-corpus figures differ substantially and are quoted interchangeably in this category. Ask whether their plan depends on placement in a small number of outlets, and if so, how that squares with the top ten domains holding 12% of citations. If a proposal leans on community presence as the route into AI answers, ask for the measurement that supports it. Chapter 12 at [/how-to-buy-geo/](https://docs.broadcastwell.com/how-to-buy-geo/) has the full list.

## Where to go next

**Reasoned.** Chapter 5 at [/engine-divergence/](https://docs.broadcastwell.com/engine-divergence/) splits citation composition by engine and shows how much it moves. Chapter 3 at [/cited-not-recommended/](https://docs.broadcastwell.com/cited-not-recommended/) explains why being in the evidence layer is not the same as being in the answer. Chapter 9 at [/category-door/](https://docs.broadcastwell.com/category-door/) turns the fragmentation finding into standards for what evidence about you has to look like.

## Sources

Every figure in this chapter comes from The 2026 State of GEO, Volume I: the 5,160 traced citations, the composition of the 100 most-cited domains and their 36% share of all citations, the 0.0% community share of the full corpus, the 12% held by the top ten domains, the 56% single-appearance share, and the individual domain rows quoted above. The 1,753 unique-domain count is taken from the published dataset README and labelled as such. The per-domain file is `cited_source_domains_top100.csv` at [github.com/Broadcastwell/state-of-geo-2026](https://github.com/Broadcastwell/state-of-geo-2026).

## About this manual

**Author.** Sairam Sivakumar, Broadcastwell.

**Operator disclosure.** Broadcastwell ran this measurement and sells services in the category it measures. Broadcastwell is excluded from the measured sample and from every ranking. The mitigation is not that the conflict is absent, it is that the raw data and the code are public and the result can be recomputed by anyone who disagrees.

**Self-audit, July 2026.** In the four-engine, five-run self-audit published alongside Volume II in July 2026, Broadcastwell was named in 0 of 200 answers and cited 0 times among 663 citations. That published figure stands with its date and is never replaced.

**Self-audit, 18 August 2026.** Re-measured on the same ten published questions across the same four engines, at one run per question rather than five, between 03:51 and 04:03 UTC on 18 August 2026: named in 1 of 40 answers, and cited once among 674 citations. The single naming and the single citation are the same answer, in which the engine quoted Broadcastwell's own published visibility page as a source. The two lines are not directly comparable, because one rests on five runs per question and the other on one.

**Not peer reviewed.** This is an independent industry study published as an open dataset with the analysis code that produced every figure in it. It has not been through academic peer review. Read it as measurement, and check the measurement. If you disagree with a number here, recompute it from the public data and publish what you get.

**Licence.** Prose and figures CC BY 4.0. Site code MIT.

**The three volumes.**

| Volume | What it covers | DOI |
|-|-|-|
| Volume I | 85 companies, 61 categories, 860 scored answers and 5,160 citations, one engine held constant. The dataset README additionally records 1,753 unique domains cited | [10.5281/zenodo.21537014](https://doi.org/10.5281/zenodo.21537014) |
| Volume II | The Absence Ladder. All 616 absence records classified by question shape | [10.5281/zenodo.21586091](https://doi.org/10.5281/zenodo.21586091) |
| Volume III | Cross-engine divergence. 280 questions, 40 categories, four engines, 853 answers | [10.5281/zenodo.21789120](https://doi.org/10.5281/zenodo.21789120) |

Data and analysis code for all three volumes: [github.com/Broadcastwell/state-of-geo-2026](https://github.com/Broadcastwell/state-of-geo-2026).

*Version 1.0, August 2026.*
