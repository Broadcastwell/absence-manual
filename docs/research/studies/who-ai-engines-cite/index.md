---
title: Who appears in the sources of B2B software answers?
description: 'Registered descriptive analysis of September citation arrays: source classes, concentration, empty
  answers and vendor naming with own-domain citation. Corrections and code included.'
page_class: research
research_id: 44
research_group: study
lead: Ananya Rao
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/studies/who-ai-engines-cite/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://doi.org/10.5281/zenodo.22907695
research_dataset:
  name: B2B software answer citation classes and concentration
  description: Registered secondary analysis of explicit citation arrays in Absence Index release 2026-09, including
    frozen and post-audit classifications, scopes, counts, bases and descriptive intervals.
  identifier: https://doi.org/10.17605/OSF.IO/VCZKT
  distribution:
  - name: Citation classes
    contentUrl: https://docs.broadcastwell.com/research/data/citation-class-shares.csv
    encodingFormat: text/csv
  - name: Reproducibility manifest
    contentUrl: https://docs.broadcastwell.com/research/data/study2-file-manifest.csv
    encodingFormat: text/csv
---

# Who appears in the sources of B2B software answers?

**Thirty-nine of 2,095 target answers had empty citation arrays: 1.9%, Wilson 95% interval 1.4% to 2.5% (Broadcastwell, 2026, Study 2).**

A citation describes a source choice. It does not establish trust or causation. Rovira and colleagues call their own explanation for a historical search-order change "only an inference" (2019, §4); the same restraint belongs beside an observed distribution. [Rovira et al., 2019, §4](../../source-archives/rovira-2019.pdf).

## Registration and analysis history

[OSF registration vczkt](https://doi.org/10.17605/OSF.IO/VCZKT) records the plan, with platform timestamp **30 October 2026, 01:32:03 UTC**. The archive and its aggregate figures were already known; this is secondary analysis, not a preregistered collection of unseen answers.

The plan originally required all three research-section registrations before analysis. A prospective timing amendment, recorded **30 October at 03:36:50 UTC**, permitted this completed registration to proceed while Study 1 awaited approval. No class rules, units or planned statistics changed in that amendment. The [deviation record](../../data/protocol-deviations.csv) preserves it. Study 1 subsequently became public; that does not retroactively erase the timing change.

Host classes were frozen at **04:41:53 UTC**, before class-share aggregation. A later audit found classification errors. We preserve the frozen primary result and show the corrected sensitivity separately below. There is no directional hypothesis, no significance test and no claim of a representative sample of all software buying.

## Registered protocol, unchanged

This is the unchanged registered plan. Its timing clause is superseded only by the amendment above; the prior-knowledge statements describe registration time. [OSF VCZKT](https://doi.org/10.17605/OSF.IO/VCZKT).

### Question and design

> Which classes of sources do five AI answer engines cite for B2B software questions, and how concentrated are those citations? This is a descriptive secondary-data study, not an experiment, a test of source truth or a causal test of citation preference. There is no directional hypothesis.

### Source and analysis timing

> Use answers-2026-09.jsonl, release-2026-09.json and control-questions.json from the published Absence Index release 2026-09, version DOI 10.5281/zenodo.22907695. Check the published checksums. The archive was already public and its published aggregate figures are known. New host-class shares, concentration results and vendor-pair results have not been computed. Analysis begins only after all three research-section Study Plans have been registered.

### Units and eligibility

> A citation occurrence is an explicit URL entry in the archived cited_urls array, linked to its engine, category, question, repeat and capture date. Preserve each array entry and its order, including duplicate entries if present; flag duplicates and provide a sensitivity table with at most one exact URL per answer. Do not extract extra URLs from answer prose and silently count them as returned citations. Quarantine excluded answer rows with their recorded reasons; do not include them in the primary eligible-answer analysis. Show target and control questions separately and give a combined eligible-archive summary. Preserve valid answers with zero citations in an answer-level denominator, but they contribute zero occurrences to a citation-occurrence denominator. Retain malformed or non-HTTP URLs as unclassified audit rows rather than inventing a host.

### Host classification

> Lowercase the parsed hostname, remove an initial www., preserve other subdomains, and keep the original URL. Assign each host one class and publish the host-to-class table, evidence URL, rationale, verification date and any ambiguity. Freeze the table before aggregating class shares. Use these classes: vendor site; review platform; Wikipedia or sister project; news or trade media; agency, consultancy or blog; directory or listicle site; forum; video; government or standards body; other. A vendor is a domain in the release's canonical domain list or a documented software vendor in that category. The review-platform list initially includes g2.com, capterra.com, getapp.com, trustradius.com, softwareadvice.com and Gartner Peer Insights; any additions require public evidence. For a multifunction host such as Gartner, document which service the citation paths identify and apply one disclosed primary-role classification at host level, with an ambiguity flag. Wikipedia and sister-project domains form their own class. Reddit, Quora and Stack Exchange are forums; video-service hosts are video. Government and standards-body status requires an official source. News, agency/blog and directory classifications require visible publisher or site-purpose evidence; a list-format article does not automatically turn a software vendor into a directory. Unknown or conflicting cases remain other with an uncertainty flag. Do not classify a host solely from the wording of the AI answer. Never fetch restricted client domains. Any after-aggregation changes are deviations and receive a sensitivity analysis.

### Statistics and finding rule

> Report the numerator, citation-occurrence base, share and two-sided Wilson 95% interval for each class overall, by engine and by category. Report top twenty cited hosts overall and per engine, with counts and shares. Compute the share held by the ten highest-frequency hosts and by the highest-frequency ceiling(0.01 times H) hosts, where H is the number of distinct classified hosts with at least one eligible occurrence; use at least one host and break count ties alphabetically. State this rank-cut rule and the denominator. Publish a deduplicated-per-answer sensitivity table so repeated array entries cannot silently drive concentration. Strata and repeats are dependent; Wilson intervals are descriptive conditional on this archive and are not representative population estimates. No significance tests. A finding is any reproducible count, distribution or concentration statistic, including little concentration or no material class difference.

### Vendor naming and citation

> Use the release's published universe, aliases, qualifiers and matching rules. On valid target vendor-answer pairs within the vendor's category, record qualifying naming and qualifying own-domain citation separately. A citation is qualifying only when the answer names the vendor under the published matching rule and cites a canonical, alias or product host documented in the release. Report own-domain cited pairs and named-without-own-domain-citation pairs, with their bases, overall and by engine and category. Do not treat a third-party review page as a vendor's own-domain citation. Do not add private matching rules. Separately report the named-and-cited share among named pairs and the named-without-own-citation share among all eligible vendor-answer pairs; label denominators visibly.

### Comparisons, limits and outputs

> A comparison with Goel et al. (2010), Anatomy of the Long Tail, DOI 10.1145/1718487.1718513, is a parallel about concentration, not an equivalence between search clicks and AI citations. Verify any numerical comparator in the original before publication. Host class is a judgment and can be disputed using the published table. An engine-returned citation is not proof that its page supports the answer or caused the vendor to be selected. The Google AI Overviews and AI Mode citations are the citations returned on the archived capture dates. The question set is not representative of all software buying. Publish code, extraction and host-class CSVs, exact bases, zero-citation and exclusion audits, and all deviations. Do not claim to control or guarantee AI answers.

## Which answers enter the analysis?

Inputs are the release’s answer JSONL, release JSON and control-question file, under version DOI **10.5281/zenodo.22907695**. Published checksums were matched before analysis. The archive has **2,250 observations**: **2,100 targets** and **150 controls**. Five excluded target observations remain in the exclusion audit, leaving **2,095 eligible targets** and all **150 controls**. [Release README, files and exclusion fields].

The primary target analysis contains **18,893 explicit citation-array entries**. Controls contribute **1,297**, making **20,190 eligible entries** in the combined archive. We neither infer extra references from prose nor treat an empty array as an unoptimized page. [Extraction CSV and answer-bases CSV].

| Engine | Valid target answers | Empty arrays / valid answers | Empty-array share and descriptive 95% Wilson interval | Citation entries |
|---|---:|---:|---|---:|
| ChatGPT | 420 | 0 / 420 | 0.0% (0.0% to 0.9%) | 1993 |
| Claude | 420 | 0 / 420 | 0.0% (0.0% to 0.9%) | 3975 |
| Google AI Mode | 420 | 29 / 420 | 6.9% (4.9% to 9.7%) | 1577 |
| Google AI Overviews | 415 | 10 / 415 | 2.4% (1.3% to 4.4%) | 3050 |
| Perplexity | 420 | 0 / 420 | 0.0% (0.0% to 0.9%) | 8298 |

Source: [answer-bases CSV](../../data/answer-citation-bases.csv), target scope and all categories. The controls are separate in that file: **12/150** control answers have empty arrays, **8.0%**, descriptive **95% Wilson interval 4.6% to 13.5%**. They are not mixed into the target table.

## What did the extraction audit find?

There were no within-answer exact URL duplicates, so the registered deduplicated sensitivity gives the same occurrence totals. No malformed or non-HTTP entries were found. The empty invalid-entry audit remains available. [Citation-occurrences and invalid-entry CSVs].

The public host table supplies each host's class, evidence URL, rationale, verification date and ambiguity. Copied publisher excerpts are omitted; response fingerprints retain their identity. This conservative inventory does not make other equivalent to nonvendor or claim a complete census of software publishers.

## What did the frozen primary classification produce?

![Other accounts for 44.4% of target citation entries, exceeding the checked-vendor class at 30.5%.](../../data/citation-classes.svg)

| Primary class | Citation entries / 18,893 | Share and descriptive 95% Wilson interval |
|---|---:|---|
| vendor site | 5,766 / 18,893 | 30.5% (29.9% to 31.2%) |
| review platform | 1,663 / 18,893 | 8.8% (8.4% to 9.2%) |
| Wikipedia or sister project | 3 / 18,893 | 0.016% (0.005% to 0.047%) |
| news or trade media | 663 / 18,893 | 3.5% (3.3% to 3.8%) |
| agency, consultancy or blog | 389 / 18,893 | 2.1% (1.9% to 2.3%) |
| directory or listicle site | 1,108 / 18,893 | 5.9% (5.5% to 6.2%) |
| forum | 473 / 18,893 | 2.5% (2.3% to 2.7%) |
| video | 369 / 18,893 | 2.0% (1.8% to 2.2%) |
| government or standards body | 64 / 18,893 | 0.3% (0.3% to 0.4%) |
| other | 8,395 / 18,893 | 44.4% (43.7% to 45.1%) |
| unclassified URL entry | 0 / 18,893 | 0.000% (0.000% to 0.020%) |


Source: [primary class-share CSV](../../data/citation-class-shares.csv), all-array-entries variant, target scope, all engines and categories. The complete download includes **engine, category and joint strata**, plus separate control and combined results, each with its count, base and interval. Other remains the largest class.

## What changed after the publisher-purpose audit?

The post-audit table changes five host roles: SourceForge, SoftwareReviews and Crozdesk move from directory to review platform; learn.g2.com moves from review platform to agency/consultancy/blog; solutions.trustradius.com moves from review platform to other. Multifunctional roles retain ambiguity flags. Eight additional directory/review descriptions receive ambiguity flags without a primary-role change. [Dated host-class correction CSV].

In that sensitivity, review-platform entries are **1,706/18,893**, **9.0%**, descriptive **95% Wilson interval 8.6% to 9.4%**, compared with the frozen **1,663/18,893**, **8.8%**, interval **8.4% to 9.2%**. The underlying citation entries do not change. [Post-audit shares](../../data/citation-class-shares-post-audit.csv).

Both versions also recode flagged hosts to other as an ambiguity sensitivity. The after-aggregation corrections remain exploratory; neither version creates a universal trust hierarchy.

## How concentrated are the hosts?

The target record contains **1,896 distinct normalized hosts**. Its leading ten supply **3,192/18,893 entries**, **16.9%**, descriptive **95% Wilson interval 16.4% to 17.4%**. The highest-frequency ceiling of one percent is **19 hosts**, supplying **4,107/18,893**, **21.7%**, interval **21.2% to 22.3%**. Host-count ties are broken alphabetically. [Concentration CSV, target/all/all rows].

The [top-twenty table](../../data/top-twenty-hosts.csv) reports overall and engine-specific hosts with counts and shares. G2’s exact host is the overall leading host, with **580/18,893**, **3.1%**, interval **2.8% to 3.3%**. The [source-choice insight](../../insights/who-the-engines-trust/) discusses the engine-specific concentration table; these counts do not measure clicks or unique users.

## Naming a vendor is different from citing its own site

Using the September matching definition and its accompanying public dictionary projection, we reproduced all **286 vendor records** across **42,792 eligible vendor-answer pairs**. Every named count, qualifying own-domain cited count and valid base reconciles with the deposited release. Plain-word names retain the published qualifier and boundary rules rather than accepting every substring.

Of **8,085 named pairs**, **2,608** have a qualifying own-domain citation: **32.3%**, descriptive **95% Wilson interval 31.2% to 33.3%**. Separately, **5,477/42,792 eligible pairs** are named without an own-domain citation: **12.8%**, interval **12.5% to 13.1%**. Those are deliberately different denominators. A third-party review reference does not count as the vendor’s own source. [Vendor-pair summary and reconciliation CSVs].

A pair without a qualifying own-domain citation may still have a third-party source. The table supplies the narrower event, with engine and category breakdowns available.

## Can you reproduce the tables?

The release deposit supplies the immutable answers and question files. The [public reproduction package](../../data/study2-reproduction.txt) supplies the matching function and a field-limited dictionary CSV. [Download the extraction](../../data/citation-occurrences.csv), [answer audit](../../data/answer-citation-audit.csv), [exclusions](../../data/excluded-answers.csv), [host classes](../../data/host-classes.csv), [pair observations](../../data/vendor-pairs.csv) and [pair summaries](../../data/vendor-pair-summary.csv). The [file manifest](../../data/study2-file-manifest.csv) records hashes and roles.

The public analysis accepts explicit input paths and an expected classification-file hash. The public host CSV is a projection of the frozen table with copied publisher prose removed; class and ambiguity values are identical. Its hash differs from the original frozen evidence file, and the manifest preserves both identities. [Citation analysis](../../data/analyze_citations.py); [pair reproduction](../../data/reproduce_vendor_pairs.mjs).

Classification coverage remains unresolved. Further publisher evidence could clarify some other entries, but a later fetch cannot recover each cited page exactly as it was when the answer was captured.

## What our own data shows

This study reanalyses [release 2026-09](https://doi.org/10.5281/zenodo.22907695), following the [registered plan](https://doi.org/10.17605/OSF.IO/VCZKT) with disclosed timing and classification deviations. It measures **20,190 eligible citation entries**, including controls, and **18,893 target entries**. Complete class, engine, category, concentration and vendor-pair outputs are linked above. The source-purpose judgments are contestable; counts do not measure trust or a causal ranking mechanism.

## Sources

- Rovira, C., Codina, L., Guerrero-Solé, F., & Lopezosa, C. (2019). Ranking by relevance and citation counts, a comparative study: Google Scholar, Microsoft Academic, WoS and Scopus. Future Internet, 11(9), 202. §4, reprint PDF p. 60. doi:10.3390/fi11090202 . [Accessible original](../../source-archives/rovira-2019.pdf) Verified 30 October 2026.
- Broadcastwell. (2026). Absence Index, release 2026-09 [Data set]. Zenodo. Release JSON, answer JSONL and README. https://doi.org/10.5281/zenodo.22907695 Verified 30 October 2026.
- Broadcastwell. (2026). Who do AI engines cite for B2B software questions? [Registration]. OSF. Registered 30 October 2026, 01:32:03 UTC. https://doi.org/10.17605/OSF.IO/VCZKT Verified 30 October 2026.
- Broadcastwell. (2026). September matching definition and dictionary projection [Study instruments]. https://docs.broadcastwell.com/research/data/study2-reproduction.txt . The public package supplies the required function and dictionary fields. Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *Who appears in the sources of B2B software answers?*. Broadcastwell. https://docs.broadcastwell.com/research/studies/who-ai-engines-cite/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research44,
  author = {{Broadcastwell research team}},
  title = {Who appears in the sources of B2B software answers?},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/studies/who-ai-engines-cite/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Ananya Rao, AI engineer.

Sources checked 30 October 2026. Independent check: 30 October 2026, Broadcastwell verification desk. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the measurement chapter](https://docs.broadcastwell.com/measurement-noise/).
