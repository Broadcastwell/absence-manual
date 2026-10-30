---
title: Which optimization signals appear on AI-cited pages?
description: Registered descriptive Study 1 of later static-page captures for archived September AI citations, with
  public classifications, overlapping strata, retrieval failures, intervals and reproducible files.
page_class: research
research_id: 43
research_group: study
lead: Ananya Rao
published: '2026-10-30T08:50:01Z'
updated: '2026-10-30T08:50:01Z'
next_review: '2027-01-30T08:50:01Z'
canonical: https://docs.broadcastwell.com/research/studies/optimized-pages-in-ai-answers/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T08:50:01Z'
date_modified: '2026-10-30T08:50:01Z'
is_based_on: https://doi.org/10.17605/OSF.IO/DVYFU
research_dataset:
  name: Observed optimization signals on archived AI-cited pages
  description: Registered Study 1 scalar observations, exact-URL classifications, citation memberships and descriptive
    tables. No raw response bodies.
  distribution:
  - name: Exact URL classifications
    contentUrl: https://docs.broadcastwell.com/research/data/study1-url-classifications.csv
    encodingFormat: text/csv
  - name: Reproduction manifest
    contentUrl: https://docs.broadcastwell.com/research/data/study1-file-manifest.csv
    encodingFormat: text/csv
---

# Which optimization signals appear on AI-cited pages?

**Study 1 classifies 3,913 of 4,420 captured target URLs as definitely optimized: 88.5%, Wilson 95% interval 87.6% to 89.4% (registered rules; October 2026 capture).**

**Registration:** [OSF DVYFU](https://doi.org/10.17605/OSF.IO/DVYFU). This is a descriptive secondary-data study with no directional hypothesis or causal test. Its question is which visible page signals occur among URLs already cited in the published September answer archive.

Before comparing it with Lewandowski and colleagues, retain the design differences: **German Google queries collected in 2020 versus B2B software answers across five engines in September 2026; October page retrieval; static HTML, expanded signature rules and registered precedence; time to first byte instead of full page-loading time**. The earlier chart is contextual evidence, not a controlled baseline.

## Was the plan public before this analysis?

The existing OSF record reports registration at **2026-10-30T01:06:12.768170Z**. Its delayed approval was completed from the existing notice at approximately **05:31Z**, without a duplicate registration. Registration timestamp, approval action and public availability are distinct events.

All three registrations were checked public and no longer archiving at approximately **05:32Z**. The collection rules, news list, instrument and source identities were frozen at **05:36:56.935712Z**; the first resource collection started at **05:37:03.800062Z**. A further all-three public check at **07:20:32 to 07:20:35Z** preceded the first aggregate analysis at **07:20:56.107845Z**.

The [provenance record](../../data/study1-provenance.json) and [frozen receipt](../../data/study1-precollection-freeze.json) preserve this recorded chronology and the file fingerprints. These are research records, not independently notarized timestamps. The original answers and published aggregate counts were already available before registration; we do not describe them as previously unseen data.

## What were the source records and units?

The source is version DOI [10.5281/zenodo.22907695](https://doi.org/10.5281/zenodo.22907695), using its answer JSONL, release JSON and control-question identities. Every explicit citation in eligible answers contributes an occurrence record with engine, category, question, repeat, capture date and saved array position.

The eligible archive contains **20,190 citation occurrences** and **6,271 distinct exact URLs**, requested as **6,261 fragment-free resources**. The target scope has **5,861 distinct URLs**. Exact scheme, path, query and fragment remain part of URL identity; a shared requested resource does not erase a distinct cited identifier.

A URL contributes once to each engine/category stratum in which it occurs. Strata overlap. Target and control questions are identified from the released inputs, not inferred from an identifier prefix. Excluded answers do not contribute primary citation units; the extraction-exclusion table contains no citation rows in this archive. An answer without a source is not a URL without optimization.

## What did collection preserve?

The research instrument requested each resource once, reused cached responses and observed robots policies and per-host delays. It did not bypass restrictions. Complete successful HTML is required for a page classification. Other states remain separately tabulated.

The capture records nonempty title and description, canonical, Open Graph, viewport, JSON-LD or microdata and declared types, four listed plugin families, the listed analytics and advertising signatures, HTTPS, host-root files and time to first byte. [Exact instrument](../../data/collect_page_signals.py); [frozen signature dictionary](../../data/page-signal-rules.json); [news list](../../data/study1-news-hosts.csv).

The root-file rule is deliberately limited. A sitemap marker is not full XML validation. A nonempty text llms.txt response is recorded as present, without establishing conformance to every specification, consumption by an engine or an effect on citations. Blocked or ambiguous host-file responses remain unknown.

## Which classification takes precedence?

For captured HTML, apply the following order without fitting it to these outcomes:

1. Wikipedia and the listed sister projects: definitely not optimized, by stipulation.
2. A listed plugin, qualifying structured data, frozen news-host indicator or listed advertising signature: definitely optimized.
3. Otherwise a missing nonempty title or description: probably not optimized, overriding weak signals.
4. Otherwise any registered weak signal: probably optimized.
5. Otherwise: unclassified.

Weak signals include the listed analytics markers, HTTPS, canonical, viewport, Open Graph, qualifying sitemap or robots hints, and time to first byte below three seconds. Qualifying JSON-LD means a parseable nonempty object or list, not validation of its truth or every Schema.org requirement. [Registered plan](../../data/study1-registered-plan.txt).

## What is the target result?

| Registered class | Count / successful HTML base | Share (Wilson 95% interval) |
| --- | --- | --- |
| definitely optimized | 3,913 / 4,420 | 88.5% (87.6% to 89.4%) |
| probably optimized | 405 / 4,420 | 9.2% (8.3% to 10.0%) |
| probably not optimized | 100 / 4,420 | 2.3% (1.9% to 2.7%) |
| definitely not optimized | 2 / 4,420 | 0.045% (0.012% to 0.165%) |
| unclassified | 0 / 4,420 | 0.000% (0.000% to 0.087%) |

Source: [class-share table](../../data/study1-class-shares.csv), target/all/all. The base is successful complete HTML, including unclassified pages. The complete CSV reports every class overall, per engine, per category and jointly, with control and combined scopes separately. It does not put failed retrievals into the negative classes.

## How much of the target archive was observable?

| Retrieval outcome | Count / all target URLs | Share (Wilson 95% interval) |
| --- | --- | --- |
| HTTP 5xx | 3 / 5,861 | 0.051% (0.017% to 0.150%) |
| blocked HTTP 403 | 636 / 5,861 | 10.9% (10.1% to 11.7%) |
| blocked HTTP 429 | 34 / 5,861 | 0.6% (0.4% to 0.8%) |
| non-HTML response | 43 / 5,861 | 0.7% (0.5% to 1.0%) |
| other HTTP 4xx | 68 / 5,861 | 1.2% (0.9% to 1.5%) |
| other HTTP response | 14 / 5,861 | 0.2% (0.1% to 0.4%) |
| oversized | 5 / 5,861 | 0.085% (0.036% to 0.200%) |
| restricted_or_nonpublic_destination | 8 / 5,861 | 0.1% (0.1% to 0.3%) |
| robots_disallowed | 247 / 5,861 | 4.2% (3.7% to 4.8%) |
| robots_unavailable | 355 / 5,861 | 6.1% (5.5% to 6.7%) |
| successful HTML | 4,420 / 5,861 | 75.4% (74.3% to 76.5%) |
| timeout | 28 / 5,861 | 0.5% (0.3% to 0.7%) |

Source: [retrieval-outcome table](../../data/study1-fetch-outcomes.csv), target/all/all. Each row uses all target URLs as its base. These failures are substantive limits on the captured-page result, not evidence that the excluded pages lacked signatures.

## How do category strata compare?

| Software category | Definitely optimized / successful HTML URLs | Share (Wilson 95% interval) |
| --- | --- | --- |
| construction project management | 321 / 355 | 90.4% (86.9% to 93.1%) |
| crm | 392 / 441 | 88.9% (85.6% to 91.5%) |
| dealership management systems | 246 / 274 | 89.8% (85.6% to 92.8%) |
| dental practice management | 218 / 249 | 87.6% (82.9% to 91.1%) |
| field service management | 344 / 356 | 96.6% (94.2% to 98.1%) |
| hotel property management | 208 / 240 | 86.7% (81.8% to 90.4%) |
| insurance agency management | 249 / 296 | 84.1% (79.5% to 87.8%) |
| legal practice management | 265 / 286 | 92.7% (89.0% to 95.1%) |
| loan origination software | 283 / 312 | 90.7% (87.0% to 93.5%) |
| project_management | 336 / 374 | 89.8% (86.4% to 92.5%) |
| radiology medical imaging | 281 / 338 | 83.1% (78.8% to 86.8%) |
| residential property management | 307 / 341 | 90.0% (86.4% to 92.8%) |
| transportation management systems | 290 / 344 | 84.3% (80.1% to 87.8%) |
| veterinary practice management | 181 / 225 | 80.4% (74.8% to 85.1%) |

These rows show the definite class as a compact category comparison. [Every class and interval](../../data/study1-class-shares.csv) and the [per-engine overview](../../insights/nearly-every-google-result-is-optimized/) retain their own successful-capture bases. No pooled category average is substituted for a URL-level result.

## What about Wikipedia, root files and schema types?

Wikipedia or listed sister projects account for **2/5,861 target URLs: 0.034%, Wilson 95% interval 0.009% to 0.124%**. Among captured target HTML, the same count is **2/4,420: 0.045% (0.012% to 0.165%)**. These distinguish all cited units from successful captures. [Wikipedia table](../../data/study1-wikipedia-shares.csv).

For llms.txt, the unique final-origin result is:

| Root-file observation | Present / final-origin base | Share (Wilson 95% interval) |
| --- | --- | --- |
| llms.txt present | 774 / 1,600 | 48.4% (45.9% to 50.8%) |
| llms.txt absent | 741 / 1,600 | 46.3% (43.9% to 48.8%) |
| llms.txt unknown | 85 / 1,600 | 5.3% (4.3% to 6.5%) |

The [download](../../data/study1-llms-presence.csv) also supplies a distinct-URL-weighted view, repeating each cached host result across its cited URLs. Do not confuse those denominators. Presence is conditional on origins associated with successfully captured HTML and is not measured adoption across the web.

The leading declared schema types among captured target URLs are:

| Declared type | URLs / successful HTML base | Share (Wilson 95% interval) |
| --- | --- | --- |
| Organization | 2,959 / 4,420 | 66.9% (65.5% to 68.3%) |
| ListItem | 2,833 / 4,420 | 64.1% (62.7% to 65.5%) |
| BreadcrumbList | 2,718 / 4,420 | 61.5% (60.0% to 62.9%) |
| ImageObject | 2,614 / 4,420 | 59.1% (57.7% to 60.6%) |
| WebPage | 2,442 / 4,420 | 55.2% (53.8% to 56.7%) |
| Person | 2,248 / 4,420 | 50.9% (49.4% to 52.3%) |

Types can co-occur, so this is not a partition. The [complete type table](../../data/study1-schema-types.csv) normalizes the HTTP/HTTPS Schema.org prefixes and counts a type once per URL. An empty declared string is not a type.

## Can the published files reproduce the result?

The [package instructions](../../data/study1-reproduction.txt) support an offline recount from scalar classifications and citation memberships, plus a full rebuild from the public captured-signal projection and deposited answer inputs. The [manifest](../../data/study1-file-manifest.csv) records public hashes and distinct original-file fingerprints where line endings or projection differ.

The public projection omits fetched response bodies, redirect metadata and free-text errors. A generic timeout marker preserves that outcome. Two failed final destinations with sensitive query-key names are blanked under the public URL policy. Those removals leave classifications and substantive aggregate tables unchanged; the original metadata capture retains its own fingerprint.

The [recount program](../../data/reproduce_study1.py) checks **19,290 numeric table rows across 198 strata**, along with **1,723 host-evidence rows**. A separate full rebuild matched **47,474 data rows across ten CSV files**, cell for cell. These are writer reproduction checks, not peer review or independent approval.

The [citation-order table](../../data/study1-citation-order.csv) gives both occurrence-weighted and distinct-URL-at-position summaries. Saved citation-array position is not vendor recommendation rank. The [URL classifications](../../data/study1-url-classifications.csv) and [membership mapping](../../data/study1-citation-membership.csv) expose the counted units.

## Deviations and interpretation limits

After the first aggregation, empty schema-type declarations were removed from the type-frequency labels. Their original scalar declarations remain in the data, and no URL classification changed. The provenance file records the before/after schema-table fingerprints and rerun time. No news-domain or signature dictionary was expanded after aggregation.

The original ACM Figure 1 reports **59.0%, 29.0% and 12.0%** in its combined classes. Our broader signature rule and different population preclude treating the difference as a trend or intervention effect. The original’s loading-time feature is not our time-to-first-byte measure.

Pages can change after citation. Static capture misses rendered-only features, signatures are incomplete and missingness can be selective. Shared URLs and repeated questions create dependencies. Wilson intervals describe proportions conditional on this convenience archive; no significance tests, buyer-population estimates or causal citation claims follow.

## What our own data shows

Across target and control scopes together, **4,750/6,271 distinct URLs** produced successful complete HTML. The target class result is **3,913/4,420 definitely optimized, 88.5% (Wilson 95% interval 87.6% to 89.4%)**. Its separate target retrieval success is **4,420/5,861, 75.4% (74.3% to 76.5%)**.

These are measurements of later captured signatures on previously cited pages. We have no measurement of whether installing those signatures caused an answer engine to cite a page.

## Sources

- Broadcastwell. (2026). Study 1 plan: Do AI engines cite optimized pages? [Registration]. OSF. Registered 30 October 2026, 01:06:12 UTC; public approval completed before this study’s collection and aggregation. https://doi.org/10.17605/OSF.IO/DVYFU Verified 30 October 2026.
- Broadcastwell. (2026). Absence Index, release 2026-09 [Data set]. Zenodo. Release JSON, answer JSONL and README. https://doi.org/10.5281/zenodo.22907695 Verified 30 October 2026.
- Lewandowski, D., Sünkler, S., & Yagci, N. (2021). The influence of search engine optimization on Google’s results: A multi-dimensional approach for detecting SEO. WebSci 2021 (pp. 12 to 20). ACM. Figure 1, printed p. 17 (PDF p. 6); feature and classification method, §§3 to 4. doi:10.1145/3447535.3462479 . Accessible author original: https://searchstudies.org/wp-content/uploads/2021/08/3447535.3462479.pdf Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *Which optimization signals appear on AI-cited pages?*. Broadcastwell. https://docs.broadcastwell.com/research/studies/optimized-pages-in-ai-answers/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research43,
  author = {{Broadcastwell research team}},
  title = {Which optimization signals appear on AI-cited pages?},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/studies/optimized-pages-in-ai-answers/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Ananya Rao, AI engineer.

Sources checked 30 October 2026. Independent check: pending. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Check a proposed before-and-after claim](https://docs.broadcastwell.com/valid-measurement/).
