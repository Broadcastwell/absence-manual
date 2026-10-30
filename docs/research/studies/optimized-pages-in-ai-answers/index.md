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

**Registration:** [OSF DVYFU](https://doi.org/10.17605/OSF.IO/DVYFU).

Comparison differences: **German Google queries collected in 2020 versus B2B software answers across five engines in September 2026; October page retrieval; static HTML, expanded signature rules and registered precedence; time to first byte instead of full page-loading time**. The earlier chart is contextual evidence, not a controlled baseline.

## Was the plan public before this analysis?

The existing OSF record reports registration at **2026-10-30T01:06:12.768170Z**. Its delayed approval was completed from the existing notice at approximately **05:31Z**, without a duplicate registration.

All three registrations were checked public and no longer archiving at approximately **05:32Z**. The collection rules, news list, instrument and source identities were frozen at **05:36:56.935712Z**; the first resource collection started at **05:37:03.800062Z**. A further all-three public check at **07:20:32 to 07:20:35Z** preceded the first aggregate analysis at **07:20:56.107845Z**.

[Provenance](../../data/study1-provenance.json) and [freeze receipt](../../data/study1-precollection-freeze.json) preserve chronology and fingerprints. Timestamps are not notarized; answers and aggregate counts predate registration.

Lewandowski and colleagues call pages “at least probably optimized” (2021, abstract, PDF p. 1); inferred labels are not causal.

## Registered protocol, unchanged

Quoted paragraphs reproduce the registered text unchanged. Unquoted section introductions guide reading; they are not part of the registration. [OSF DVYFU](https://doi.org/10.17605/OSF.IO/DVYFU).

### Question and design

> What share of URLs cited in the Absence Index release 2026-09 carry visible optimization signals, and how does that share differ by engine and software category? This is a descriptive secondary-data study, with no directional hypothesis and no causal test of whether a signal produces a citation.

### Source and prior knowledge

> Use the published answers-2026-09.jsonl and release-2026-09.json attached to version DOI 10.5281/zenodo.22907695, with their published checksums. These answers were already collected and made public before this registration. Published aggregate counts and the comparison paper have been read. No new study results, host classification totals or page-signal shares have been computed. All three research-section plans must be registered before analysis begins.

### Units and inclusion

The next section defines eligible units.

> Include every explicit citation URL in the archived answers. Retain engine, category, question, repeat, capture date and citation order for every occurrence. Deduplicate the analysis units by exact URL, preserving scheme, path, query and fragment in the unit identifier. Preserve a separate mapping to the requested resource URL. A URL contributes once to each engine or category stratum in which it occurs. Report target and control questions separately as well as the combined archive; do not treat a missing answer or an answer without a citation as a URL with no optimization. Retain excluded answer rows in a separate audit, but omit their citation URLs from the primary eligible-answer analysis unless the same URL also appears in an eligible answer. Give any all-record sensitivity analysis a separate label. Preserve extraction exclusions and reasons. Report any archival mismatch before continuing.

### Collection

> Retrieve each resource once and cache the result. Observe robots.txt and a maximum of one request per second per host, including redirects and host-root files. Use BroadcastwellResearchBot/1.0 (+https://docs.broadcastwell.com/research/). Do not fetch restricted client domains. Record requested and final URL, fetch date, status, content type, redirect chain and time to first byte. Record robots exclusions, blocked responses, 4xx, 5xx, timeout, non-HTML and other failures separately. A failed fetch is never evidence that a page is not optimized. Do not evade access controls. Keep raw HTML out of the public dataset.

### Signals and classification

> Record non-empty title and meta description; canonical link; Open Graph tags; viewport meta; JSON-LD or microdata and reported schema types; SEO plugin signatures, including Yoast, Rank Math, All in One SEO and SEOPress; analytics and advertising signatures; HTTPS; host-root robots.txt, sitemap and llms.txt; and time to first byte. Distinguish absent, present and unknown for host files. Publish exact signal rules and a host evidence table. Freeze any news-domain list and additional signature dictionary before aggregating outcomes; additions after inspecting results are exploratory and reported as deviations.
> Apply this precedence to successfully fetched HTML: (1) Wikipedia and sister projects: definitely not optimized, a stipulated class rather than a quality judgment; (2) an SEO plugin, structured data, a documented news-domain classification or an advertising signature: definitely optimized; (3) otherwise, a missing title or missing meta description: probably not optimized, overriding weak positive signals; (4) otherwise at least one weak signal: probably optimized. Weak signals are analytics, HTTPS, canonical, viewport, Open Graph, sitemap, explicit SEO hints in robots.txt, or time to first byte below three seconds. Any residual page is unclassified, not forced into a negative class. The time-to-first-byte threshold is our adaptation; Lewandowski et al. used page loading time below three seconds. A public rule table will distinguish this adaptation and the expanded structured-data rule from the paper's fitted decision tree.

### Statistics and finding rule

> For each class report numerator, eligible URL base, percentage and two-sided Wilson 95% interval overall, per engine and per category. Report unclassified and failed units with their own bases. Give citation-order results only when the archive provides order; do not infer answer rank from a host list. Separately report Wikipedia share, llms.txt presence and schema-type frequencies with explicit denominators and unknowns. Strata overlap and repeat answers are dependent; Wilson intervals describe uncertainty conditional on this archive and are not population confidence claims. No significance tests or claims of representativeness. A finding is a reproducible descriptive count or share supported by the released classification CSV, including a null or low observed share.

### Comparison and limits

> Compare only descriptively with Figure 1 of Lewandowski, Suenkler and Yagci (2021), DOI 10.1145/3447535.3462479: 59.0% definitely optimized, 29.0% probably optimized and 12.0% (probably) not optimized among 256,853 Google result URLs. State method differences first: German Google query sets in 2020 versus archived B2B software questions across five answer engines in September 2026; later fetch date; different signal and classification implementation. Cite the paper's chart rather than conflicting prose. Its 27% figure concerns the position of its Wikipedia results, not Wikipedia's share of all first-position results. A cited URL is not proof of the answer's source of truth, a fetched page may have changed since the answer, and this question set is not a representative sample of buyer searches. Publish code, classification CSVs, failures and deviations; do not claim control of AI answers.

**Comparison clarification:** the plan's phrase “conflicting prose” is retained as registered. The original paper's 48.4%, 27% and 31% concern news-content shares, not an alternative optimization-class split. They do not contradict Figure 1. The class results use that chart. [Lewandowski et al., §5, PDF p. 6, printed p. 17].

## Which records and implementation definitions produced the tables?

The eligible archive contains **20,190 citation occurrences** and **6,271 distinct exact URLs**, requested as **6,261 fragment-free resources**. The target scope contains **5,861 distinct URLs**. The [membership table](../../data/study1-citation-membership.csv) preserves each exact URL and its overlapping strata.

Apply the first matching rule to captured HTML:

| Order | First applicable condition | Class |
| --- | --- | --- |
| 1 | Wikipedia or listed sister project | definitely not optimized (stipulated) |
| 2 | Listed plugin, qualifying structured data, frozen news host or advertising signature | definitely optimized |
| 3 | Missing nonempty title or meta description; overrides weak signals | probably not optimized |
| 4 | Any registered weak signal | probably optimized |
| 5 | None of these | unclassified |

Failures are outside this classification. Qualifying structured data expands the strong rule to parseable nonempty JSON-LD or microdata. Time to first byte below three seconds replaces the paper’s full page-loading measure. This is fixed precedence, rather than the paper’s fitted decision tree. [Frozen instrument](../../data/collect_page_signals.py); [exact rules](../../data/page-signal-rules.json); [news list](../../data/study1-news-hosts.csv).

Presence does not prove consumption. Blocked or ambiguous root-file responses remain unknown.

## What is the target result?

| Registered class | Count / successful HTML base | Share (Wilson 95% interval) |
| --- | --- | --- |
| definitely optimized | 3,913 / 4,420 | 88.5% (87.6% to 89.4%) |
| probably optimized | 405 / 4,420 | 9.2% (8.3% to 10.0%) |
| probably not optimized | 100 / 4,420 | 2.3% (1.9% to 2.7%) |
| definitely not optimized | 2 / 4,420 | 0.045% (0.012% to 0.165%) |
| unclassified | 0 / 4,420 | 0.000% (0.000% to 0.087%) |

Source: [class-share table](../../data/study1-class-shares.csv), target/all/all; successful HTML base. Full CSV retains every class, engine, category, control and joint stratum. Failures are excluded.

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

Source: [retrieval outcomes](../../data/study1-fetch-outcomes.csv), target/all/all. All target URLs form each base. Failures limit observation; they do not establish absent signatures.

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

[All classes](../../data/study1-class-shares.csv) and [engine overview](../../insights/nearly-every-google-result-is-optimized/): successful-capture bases; overlapping categories.

## What about Wikipedia, root files and schema types?

Wikipedia or listed sister projects account for **2/5,861 target URLs: 0.034%, Wilson 95% interval 0.009% to 0.124%**. Among captured target HTML, the same count is **2/4,420: 0.045% (0.012% to 0.165%)**. These distinguish all cited units from successful captures. [Wikipedia table](../../data/study1-wikipedia-shares.csv).

For llms.txt, the unique final-origin result is:

| Root-file observation | Present / final-origin base | Share (Wilson 95% interval) |
| --- | --- | --- |
| llms.txt present | 774 / 1,600 | 48.4% (45.9% to 50.8%) |
| llms.txt absent | 741 / 1,600 | 46.3% (43.9% to 48.8%) |
| llms.txt unknown | 85 / 1,600 | 5.3% (4.3% to 6.5%) |

The [CSV](../../data/study1-llms-presence.csv) also gives URL-weighted counts. Neither view estimates web-wide adoption.

Leading declared types:

| Declared type | URLs / successful HTML base | Share (Wilson 95% interval) |
| --- | --- | --- |
| Organization | 2,959 / 4,420 | 66.9% (65.5% to 68.3%) |
| ListItem | 2,833 / 4,420 | 64.1% (62.7% to 65.5%) |
| BreadcrumbList | 2,718 / 4,420 | 61.5% (60.0% to 62.9%) |
| ImageObject | 2,614 / 4,420 | 59.1% (57.7% to 60.6%) |
| WebPage | 2,442 / 4,420 | 55.2% (53.8% to 56.7%) |
| Person | 2,248 / 4,420 | 50.9% (49.4% to 52.3%) |

[Full type table](../../data/study1-schema-types.csv): overlapping labels, normalized Schema.org prefixes, once per URL; empty declarations excluded.

## Can you reproduce the result?

[Instructions](../../data/study1-reproduction.txt) support recounts and rebuilds; the [manifest](../../data/study1-file-manifest.csv) distinguishes public bytes from original fingerprints.

The public projection omits response bodies, redirect metadata and free-text errors. One sensitive-query destination is blanked. Classifications and aggregate tables are unchanged; original metadata retains its fingerprint.

The [recount](../../data/reproduce_study1.py) checks **19,290 numeric rows, 198 strata and 1,723 host-evidence rows**. A full rebuild matched **47,474 rows across ten CSV files**, cell for cell. This is not peer review or independent approval.

The [order table](../../data/study1-citation-order.csv) gives citation positions, not vendor ranks. [Classifications](../../data/study1-url-classifications.csv) and [memberships](../../data/study1-citation-membership.csv) preserve units.

## Deviations and interpretation limits

Empty schema labels were removed after aggregation; scalar declarations remain and no URL class changed. Provenance preserves before/after fingerprints and rerun time; news and signature dictionaries were not expanded.

Static capture and selective missingness limit interpretation.

## What our own data shows

Source archive: [release 2026-09, DOI 10.5281/zenodo.22907695](https://doi.org/10.5281/zenodo.22907695).

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

Sources checked 30 October 2026. Independent check: 30 October 2026, Broadcastwell verification desk. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Check a proposed before-and-after claim](https://docs.broadcastwell.com/valid-measurement/).
