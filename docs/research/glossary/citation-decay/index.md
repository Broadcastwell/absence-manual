---
title: What is citation decay?
description: Citation decay is a decline in a defined page’s citation measure over comparable observations; a half-life
  requires an explicit baseline, threshold and time rule.
page_class: research
research_id: 36
research_group: glossary
lead: Lauren Chen
published: '2026-10-30T08:50:01Z'
updated: '2026-10-30T08:50:01Z'
next_review: '2027-01-30T08:50:01Z'
canonical: https://docs.broadcastwell.com/research/glossary/citation-decay/
sources_verified: true
schema_type: Article
date_published: '2026-10-30T08:50:01Z'
date_modified: '2026-10-30T08:50:01Z'
is_based_on: https://www.tryprofound.com/blog/citation-decay
defined_term: Citation decay
---

# What is citation decay?

**Citation decay is a decline in a defined page’s citation measure over comparable observations; a half-life requires an explicit baseline, threshold and time rule.**

An old page that is cited today has not necessarily decayed. A previously cited page missing from a later answer may reflect ordinary answer variation. The term becomes useful when it names a measured change through time under a stated observation design.

The practical reporting question belongs in the library’s [historical data and time-series guidance](/answers/measurement/which-ai-visibility-platforms-offer-historical-data-and-time-series-re/). Here we define the event that a time series would need to establish.

## Where does the current AI-search usage come from?

The earliest dated primary product explanation of the exact term we verified is Profound’s **29 September 2026** announcement by Joey Adelman and Matthew Huo. That is a bounded source finding, not a claim that no earlier author used the words in another field or on another site.

Profound defines a page’s citation share against all citations across the models it tracks, smoothed over a **two-week** window. Its half-life runs from the page’s peak to half that peak, with a requirement to remain at or below the threshold for **14 consecutive days**. These are Profound’s operational choices, not a universal definition imposed on other studies. [Adelman & Huo, 2026].

The product also excludes pages that do not meet its age, citation-count and peak-activity rules. Consequently, a summary for eligible pages should not be generalized to every published URL. The vendor’s concept is useful precisely because it says which curve and which threshold it means.

## Choose the quantity before fitting a curve

Absolute citation count, share of citations, proportion of answers citing a URL and proportion of questions ever citing it are different measures. A page can keep receiving the same number of citations while losing share because the rest of the observed citation pool grows.

Specify the URL identity rule. A changed tracking parameter should not necessarily start a new page history, while a substantially revised document at a stable address may need a version label. Explain whether redirects, canonical declarations or a manually maintained document identifier connect observations.

Define the observation window and treatment of missing collection. An unsuccessful capture is not an observed absence. A page that has not crossed the threshold by the last observation has an incomplete time-to-event record, not a measured infinite life or an invented future decay date.

## Why a missing citation is weak evidence by itself

Generated answers can differ under repeated questions. A before/after disappearance might therefore be a transient answer change rather than a durable loss. Repetitions help reveal that variation, while a stable comparison set helps separate page-specific changes from broader engine or collection changes.

Do not select a peak retrospectively and then describe every ordinary fluctuation below it as deterioration. State whether the peak is defined across the whole observed series, within a moving window or from an initial baseline. Different definitions can produce different half-lives from the same records.

Calendar age also differs from time since first observed citation. A document may have existed for years before entering the tracked question set. Without earlier observations, “first cited” means first seen by that collection, not necessarily the first citation anywhere.

## Can decay justify a content refresh?

A declining series can identify a page worth investigating. It does not establish that rewriting it will recover citations. Check whether the facts became stale, the question set changed, a competing source appeared, or the engine changed its source presentation.

If an intervention follows, record its date and preserve the earlier version. Report the outcome against an appropriate comparison design. A refresh recommendation and a demonstrated refresh effect are separate claims, and a decay estimate supplies only the former unless the later test supports more.

Joey Adelman and Matthew Huo write, “We track this on a rolling two-week average”. That smoothing choice is part of Profound’s published product definition, rather than a rule established for every citation dataset. [Adelman and Huo, 29 September 2026, “What Citation Decay shows”; verified 30 October 2026].

You can distinguish an ageing document from a measured decline in citation share.

## What our own data shows

We have no measurement on this point: citation decay. Study 3 is a registered protocol for release-to-release absence persistence and remains unrun until its comparability conditions are met. Vendor absence persistence is also a different event from a particular URL’s citation half-life.

Our repeated-question analysis observed **1,259 mixed-naming groups among 14,192 complete vendor-question-engine groups: 8.9%, Wilson 95% interval 8.4% to 9.4%**. Mixed means named in one or two of three valid repeats. These within-release groups do not measure elapsed-time decay. See [the measurement-noise finding](/research/insights/one-rank-number-is-a-fiction/) and the [Study 3 protocol](/research/studies/does-absence-persist/).

## Sources

- Adelman, J., & Huo, M. (2026, September 29). Introducing Citation Decay in Profound. Profound. Citation-share, smoothing, half-life and eligibility definitions. https://www.tryprofound.com/blog/citation-decay Verified 30 October 2026.
- Broadcastwell. (2026). Does absence persist from one release to the next? [Registration]. OSF. Registered 30 October 2026, 01:12:44 UTC. https://doi.org/10.17605/OSF.IO/MKJ9V Verified 30 October 2026.
- Broadcastwell. (2026). State of GEO, volume III [Data set and report]. Zenodo. README: repeated questions and same-vendor comparisons. https://doi.org/10.5281/zenodo.21789120 Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *What is citation decay?*. Broadcastwell. https://docs.broadcastwell.com/research/glossary/citation-decay/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research36,
  author = {{Broadcastwell research team}},
  title = {What is citation decay?},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/glossary/citation-decay/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Lauren Chen, AI architect and specialist.

Sources checked 30 October 2026. Independent check: 30 October 2026, Broadcastwell verification desk. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read about historical visibility data](https://docs.broadcastwell.com/answers/measurement/which-ai-visibility-platforms-offer-historical-data-and-time-series-re/).
