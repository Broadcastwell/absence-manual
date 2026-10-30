---
title: GEO papers ask different questions about visibility
description: A dated, bounded literature search separates verified empirical citation studies, preprints, surveys
  and editorial defects. Search scope and access limits are published.
page_class: research
research_id: 11
research_group: insight
lead: Priya Nair
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/insights/state-of-geo-research-2026/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://arxiv.org/html/2311.09735v3
---

# GEO papers ask different questions about visibility

**Our bounded 30 October 2026 search verifies seven peer-reviewed empirical source-visibility studies; this is a documented minimum, not the size of the field.**

We verified **seven peer-reviewed empirical studies of source citation or source visibility** in a bounded search completed **30 October 2026**. The exact-phrase arXiv search displayed **61 unique records**. Those are different counts: a search hit is not automatically an eligible study, and our verified minimum is not a census of the whole field. [Dated search log](../../data/literature-search-log-2026-10-30.csv); [record decisions and primary links](../../data/literature-census-2026-10-30.csv).

That result makes a blanket description of GEO research as empty or fake untenable. It also leaves a more useful problem. Controlled citation experiments, observational audits of deployed services, conceptual frameworks and commercial case reports answer different questions. You cannot combine their headlines as though each measured the effect of publishing a page on the same live engine.

## What did we search?

| Service | Query and scope | What was actually inspected |
|---|---|---|
| arXiv | Exact phrase “generative engine optimization,” all fields, no start-date filter, announcement date descending | All 61 displayed records and expanded abstracts, with identifiers deduplicated; primary follow-up for counted studies |
| Google Scholar | The same exact phrase, default article search, any time, default relevance order | First ten displayed records for discovery; the approximate search total is not used as a study count |
| Scopus | Intended document query TITLE-ABS-KEY("generative engine optimization") | Current Preview offered author/source access and institutional sign-in. No document search was executed; no zero-result conclusion is reported |

Source: service pages personally opened on **30 October 2026**, with exact URLs and access outcomes in the [search log](../../data/literature-search-log-2026-10-30.csv). The corrected arXiv query uses quotation marks; an earlier broad search returned stemmed, largely unrelated results and is not included in the record count.

These boundaries matter. We did not screen every Scholar result, search every synonym or obtain a full Scopus export. Papers using only “answer engine optimization,” “generative search,” source attribution or another vocabulary may be absent. New versions and later indexing can also change discovery. The published count is a minimum verified from this search, without a field-wide completeness claim.

## What qualifies for the verified minimum?

A counted record needs an opened primary paper reporting empirical measurements of source citation or visibility in generated answers, an identifiable method and result, and a verified conference publication record or proceedings version. A preprint’s self-description alone does not certify peer review. We count a work once, linking its preprint and proceedings version rather than treating them as independent studies.

Here, data-carrying means the paper reports empirical observations or experiments with methods and results. It does **not** mean that every raw observation is openly downloadable or that we reproduced the experiment. Artifact availability receives a separate field in the CSV. This distinction is particularly consequential when an otherwise useful paper supplies code without its local evaluation data.

| Counted work | Primary publication | Empirical object and boundary |
|---|---|---|
| Aggarwal and colleagues, GEO | KDD 2024, DOI 10.1145/3637528.3671900 | Citation-based visibility in a supplied-source benchmark; not a general live-web discovery experiment |
| Zhou and colleagues, IF-GEO | Findings of ACL 2026, DOI 10.18653/v1/2026.findings-acl.1373 | Multi-query document revisions and citation-based visibility/stability; author code says local datasets are not distributed there |
| Kim and colleagues, SAGEO Arena | KDD 2026, DOI 10.1145/3770855.3818146 | A controlled pipeline that separately evaluates retrieval, reranking and generated citations; not an audit of every commercial engine |
| Wu and colleagues, MAGEO | Findings of ACL 2026, pp. 43305 to 43315 | Revision evaluation with visibility and attribution-fidelity outcomes; the inspected repository emphasizes core code |
| Grossman and colleagues, How Generative AI Disrupts Search | SIGIR 2026, DOI 10.1145/3805712.3809667 | Observed source differences across search and answer services; associations do not isolate a causal publishing tactic |
| Vishwakarma and colleagues, What Gets Cited | SIGIR 2026, DOI 10.1145/3805712.3808445 | Controlled competition between injected source candidates, measuring the first citation marker |
| Sourirajan and colleagues, Beyond the Vacuum | EMNLP 2026, pp. 11852 to 11871 | Competitor-aware rewriting on fixed and augmented benchmark corpora, using citation-based impression measures |

Primary locations: the full references below link the opened papers; the [census CSV](../../data/literature-census-2026-10-30.csv) records publication evidence, design, screen level and artifact limits. This table certifies the inclusion basis, not the quality of every result or an independently reproduced effect size.

Other records are not silently labelled nonempirical. The CSV distinguishes conceptual and adjacent work from candidates whose peer-reviewed publication and qualifying outcome were not jointly certified in this bounded audit. Some candidates may qualify after further primary verification. Treating the minimum as the maximum would reverse the meaning of the count.

## Why do the experiments disagree about what visibility means?

In the first GEO paper, source material is already supplied to the generator. SAGEO Arena instead includes retrieval and reranking before citation. What Gets Cited restricts the candidate competition and measures the first reference marker. Beyond the Vacuum changes the competitive environment. Those are substantive design differences, not merely alternative names for a universal ranking score.

The title “Beyond the Vacuum” captures one of the unresolved issues: a page’s apparent gain can depend on what competing documents look like. A result under a controlled source set may remain useful, while saying little about whether a new website enters a commercial engine’s retrieval set. [Sourirajan et al., 2026, §§5 to 6].

For your decision, ask where the intervention begins and where the outcome ends. Does the study change the source before retrieval, after retrieval or inside a supplied context? Does it count references, cited words, source fidelity or visits? A board presentation that calls all of these “AI visibility uplift” loses the comparison before any statistical question arises.

## An older review is not the current citation-study count

Ziakis and Vlachopoulou’s AI-and-SEO chapter reports an initial **33 Scopus articles**, an expanded pool of **73**, **44** after title/abstract screening and a final **28** articles. Its search concerns artificial intelligence and search-engine optimization, with grey literature and snowballing added. [Ziakis and Vlachopoulou, 2024, §2, printed p. 392; PDF p. 395](https://doi.org/10.1007/978-3-031-51038-0_43).

The chapter’s sequence is its own review history. It is not our count of empirical AI-answer citation studies in October 2026. Nor should the initial and expanded pools be casually added without reconstructing the authors’ selection record. A useful taxonomy can organize a topic without establishing the causal effect of every practice it describes.

## Editorial defects deserve precise descriptions

The supplied IJRPR paper contains the phrase “next point same instructions” on printed page **4132**, PDF page **4**. That is a visible editorial defect. It does not prove who wrote the preceding text, whether software was used or whether the authors fabricated a dataset. [Singh and Kesarwani, 2025, supplied original].

The LPU course text also contains wording about a September 2021 knowledge cutoff in its Core Web Vitals discussion, PDF page **146**. That dates the wording’s frame and raises an editorial question. It is not a validated authorship detector. Historical teaching material needs current operator verification before its advice is presented as current policy. [LPU, DEMKT806, Unit 11.5].

Our [unverified-number ledger](../../evidence/unverified-numbers/) records claims for which the primary support was missing, the unit had changed or the inference exceeded the design. Each objection belongs to the particular sentence and source. Finding one defective line does not estimate the prevalence of unreliable research across GEO publishing.

## What should the next search preserve?

The dated files preserve exact queries, the screened set, duplicate handling, inclusion decisions and access limits. A later update can add records and correct publication status without disguising what the earlier search actually covered. Expanded vocabulary would improve recall but also increase irrelevant material requiring screening.

There is a trade-off between a rapidly updated discovery list and a deeply verified evidence review. This page gives a bounded discovery record with a conservative verified minimum. The unresolved work is the size and strength of the qualifying literature beyond those boundaries, especially studies that connect citation outcomes to durable discovery and actual buyer behavior.

## What our own data shows

Our contribution here is the [dated literature record](../../data/literature-census-2026-10-30.csv) and [query/access log](../../data/literature-search-log-2026-10-30.csv): 61 arXiv abstract-screen records, seven primary-verified empirical peer-reviewed works, and an explicit incomplete-coverage boundary. These are bibliographic tallies, not random-sample proportions, so no Wilson estimate of a field prevalence is made. Our own [September answer archive](https://doi.org/10.5281/zenodo.22907695) remains a separate measured record; it does not certify the outside papers or establish a publishing tactic’s causal effect.

## Sources

- Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A., Narasimhan, K., & Deshpande, A. (2024). GEO: Generative engine optimization. KDD 2024. doi:10.1145/3637528.3671900 . [Accessible original](https://arxiv.org/html/2311.09735v3) . Author manuscript v3: https://arxiv.org/html/2311.09735v3 Verified 30 October 2026.
- Zhou, H., Chen, J., Chen, X., Bao, J., Chen, Z., & Liao, Y. (2026). IF-GEO: Conflict-aware instruction fusion for multi-query generative engine optimization. Findings of ACL 2026, pp. 27576 to 27590. §§5 to 6, Tables 1 to 3. https://doi.org/10.18653/v1/2026.findings-acl.1373 . Code: https://github.com/yangjizc/IF-GEO Verified 30 October 2026.
- Kim, S., Jeong, W., Kim, S., Lee, S., & Lee, D. (2026). SAGEO Arena: A realistic environment for evaluating search-augmented generative engine optimization. KDD 2026. §§3 to 5. https://doi.org/10.1145/3770855.3818146 . Author version: https://arxiv.org/html/2602.12187v2 . Software artifact: https://doi.org/10.5281/zenodo.20423532 Verified 30 October 2026.
- Wu, B., Mao, F., Lin, J., Yang, C., Lu, J., Guo, Y., Zhang, S., Wu, Y., Huang, Y., & Li, F. (2026). From experience to skill: Multi-agent generative engine optimization via reusable strategy learning. Findings of ACL 2026, pp. 43305 to 43315. §§4 to 5. https://aclanthology.org/2026.findings-acl.2149/ . Author code: https://github.com/Wu-beining/MAGEO Verified 30 October 2026.
- Grossman, R., Liu, S., Chen, M. K., Smith, M., Borcea, C., & Chen, Y. (2026). How generative AI disrupts search: An empirical study of Google Search, Gemini, and AI Overviews. SIGIR 2026, pp. 448 to 459. §§3 to 4. https://doi.org/10.1145/3805712.3809667 . Author copy: https://web.njit.edu/~borcea/papers/acm-sigir26.pdf Verified 30 October 2026.
- Vishwakarma, R., Kumar, S., & Jamidar, R. (2026). What gets cited: Competitive GEO in AI answer engines. SIGIR 2026. §§2 to 3. https://doi.org/10.1145/3805712.3808445 . Author copy: https://arxiv.org/pdf/2605.25517 Verified 30 October 2026.
- Sourirajan, V., Zhang, Y., Kumar, H., Wadhwa, S., Patel, M., & Iranitalab, A. (2026). Beyond the vacuum: Combinatorial strategy selection for competitor-aware generative engine optimization. EMNLP 2026, pp. 11852 to 11871. §§5 to 6. https://aclanthology.org/2026.emnlp-main.516/ Verified 30 October 2026.
- Ziakis, C., & Vlachopoulou, M. (2024). Artificial intelligence’s revolutionary role in search engine optimization. In Strategic innovative marketing and tourism (pp. 391 to 399). §2, printed p. 392. https://doi.org/10.1007/978-3-031-51038-0_43 Verified 30 October 2026.
- Dogra, R. (n.d.). Search engine optimization (L. Jasrai, Ed.; cover course code DEOPR806). Lovely Professional University. Supplied file DEMKT806_SEARCH_ENGINE_OPTIMIZATION.pdf. Unit 11.5, PDF p. 146, cutoff wording; cover editor and publication-page credits differ. https://ebooks.lpude.in/new-scheme/management/mba/sem_3-4/DEMKT806_SEARCH_ENGINE_OPTIMIZATION.pdf Verified 30 October 2026.
- Singh, S., & Kesarwani, H. (2025). Study on search engine optimization (SEO) vs. paid advertising: Which strategy yields better ROI? International Journal of Research Publication and Reviews, 6(4), 4129 to 4135. Supplied IJRPR41950.pdf, printed p. 4132, PDF p. 4. https://ijrpr.com/uploads/V6ISSUE4/IJRPR41950.pdf Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *GEO papers ask different questions about visibility*. Broadcastwell. https://docs.broadcastwell.com/research/insights/state-of-geo-research-2026/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research11,
  author = {{Broadcastwell research team}},
  title = {GEO papers ask different questions about visibility},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/insights/state-of-geo-research-2026/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Priya Nair, management consultant.

Sources checked 30 October 2026. Independent check: pending. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the measurement chapter](https://docs.broadcastwell.com/measurement-noise/).
