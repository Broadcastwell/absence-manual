---
title: The university study compares academic standing with constructed website scores
description: A close reading of the 100-university study, its weighted technical scores, correlation table and deposited
  calculation discrepancies. Search position was not its outcome.
page_class: research
research_id: 14
research_group: source
lead: Arjun Mehta
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/sources/giannakoulopoulos-2019/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://doi.org/10.3390/fi11110242
---

# The university study compares academic standing with constructed website scores

**The 100-university study measures constructed website scores, not observed search rank; its printed SEO-rank sign does not reproduce (Giannakoulopoulos et al., 2019, Table 9).**

The study’s **100-university** comparison does not measure search results. It compares academic standing with researcher-constructed website-quality and SEO-performance rankings, and its printed SEO-rank sign fails to reproduce from the deposited data. [Giannakoulopoulos et al., 2019, abstract, §3 and Table 9](https://docs.broadcastwell.com/research/source-archives/giannakoulopoulos-2019.pdf); [original results workbook](https://doi.org/10.5281/zenodo.3484673).

That is a narrower and more interesting paper than a claim that prestige does not matter online. Andreas Giannakoulopoulos and colleagues ask whether academically prominent universities also have technically strong websites. They need a definition of website strength before calculating a relationship. Much of the paper is devoted to constructing that definition.

## Which universities and which outcomes?

The sample consists of the highest-ranked universities in the Academic Ranking of World Universities, commonly called the Shanghai ranking. The authors chose that academic comparison because it emphasizes research-related outputs. Their results workbook has one row for each included institution, with separate ratings and ranks for academic standing, website quality, SEO performance and the combined web measure. [Abstract and §§2 to 3; deposited Results Sheet1].

The publication date is **18 November 2019**, printed on the article’s opening page. It is a historical website assessment, not a fresh account of those institutions’ present websites. We have recalculated the deposited numbers; we have not rerun the original website tests, reconstructed changing tool versions or established a common present-day assessment date. [Original article opening page; supplied reprint PDF p. 24].

The distinction between a rating and a rank matters. The paper assigns numerical ratings on its defined scales, then orders institutions by those ratings. A relationship between two ranks is not the same statistic as a regression between the underlying ratings. Nor is either one an observation of where a page appeared for a search query.

## How was website quality constructed?

The quality measure combines structure, accessibility and performance. Structure includes HTML and CSS validation, mobile compatibility and a best-practices audit. Accessibility combines automated checks. Performance includes loading and resource-delivery measurements. The exact tests and scoring decisions are described in §3.1.

The final quality weights are **27 for structure, 40 for accessibility and 33 for performance**. These are researcher-chosen weights, not observed proportions of universities and not estimated ranking-factor effects. A binomial interval would be inappropriate for a chosen scoring parameter. [Table 5, reprint PDF p. 37, printed p. 28].

This construction gives a repeatable account of what the researchers valued, provided the same test outputs and scoring decisions are available. It also means another reasonable set of weights could produce another ordering. Accessibility has a particularly substantial role in the authors’ definition; that is a design judgment with a stated rationale, not a discovery about an engine’s private formula.

Some tests operate on the homepage, while other services inspect a broader set of site features or pages. The resulting composite therefore should not be described as a complete human assessment of every page in each university’s site. Automated checks can identify particular issues without measuring the entire usefulness of a website to its readers.

## What does SEO performance mean in this paper?

The SEO composite combines the historical outputs of Neil Patel’s SEO analyzer, SEO Site Checkup, WooRank and Google’s Lighthouse SEO audit. The paper assigns initial weights of **25, 30, 25 and 20**, respectively, and describes a rule that reduces the influence of unusually divergent ratings. [Tables 6 and 7, reprint PDF p. 38, printed p. 29].

These tools measure overlapping but different characteristics. The authors acknowledge that commercial tools do not disclose their complete methods and say that their outputs may be “questionable.” Combining them is the paper’s attempt to reduce dependence on one opaque score. It does not make the composite equivalent to observed search performance. [§3.2, reprint PDF p. 37].

The overall web rating then averages website quality and SEO performance. That creates a third constructed measure. Its relationship to the component measures is partly built into its definition, so it should not be presented as independent confirmation of every component’s validity. [§3.3].

If you are evaluating a software website, this is the question to keep asking: does an audit score measure the thing your decision needs? A technically accessible page can still be absent from a captured answer. A recognizable university can have technical defects. Neither statement identifies the cause of the other.

## Which correlations are reported, and which reproduce?

| Ranking compared with ARWU | Paper’s Table 9 | Recomputed from deposited ranks |
|---|---|---|
| Website quality | 0.35; nearby prose 0.355 | +0.35549 |
| SEO performance | -0.044 | +0.04382 |
| Overall web rating | 0.32 | +0.32013 |

Base: **100 institutions**. Source: [paper Table 9, reprint PDF p. 39, printed p. 30](https://docs.broadcastwell.com/research/source-archives/giannakoulopoulos-2019.pdf); [deposited Results Sheet1, rows 3 to 102](https://doi.org/10.5281/zenodo.3484673). [Reanalysis CSV](../../data/university-rank-reanalysis.csv). These are Spearman coefficients, not percentages, so no Wilson interval applies.

The website-quality row’s table and prose use different precision: the table prints 0.35 and the nearby text prints 0.355. That is different from the SEO row’s sign discrepancy. The SEO rank relationship from the deposited values is **+0.04382**, while the paper prints **−0.044**. The association is very weak under either version; the deposited ranks do not support repeating the printed sign as a reproduced result.

The paper labels its SEO significance value **0.333**, two-sided. A conventional two-sided t approximation for the deposited rank coefficient gives **p = 0.6651**. The printed value is roughly half that, but this alone does not establish why it occurred. We report the mismatch without claiming to know the authors’ calculation history. Both values leave the SEO association nonsignificant at conventional thresholds. [Table 9; deposited rank columns C and H].

## A regression detail also needs correction

The paper separately regresses website-quality rating on ARWU rating. The deposited data reproduce **R² = 0.07100**, a small share of variation in the defined score, with **F(1,98) = 7.4898**. The narrative prints **7.04**. The table’s slope test, **t = 2.737**, is compatible with an F value near the recomputed one when squared, rather than the printed narrative value. [Paper Tables 10 and 11 and adjoining prose, reprint PDF p. 40, printed p. 31; deposited rating columns B and D].

This is a numerical reproducibility issue. It does not make the design causal, whichever F value is used. Academic standing was not randomly assigned, and the study does not show that raising an academic rating would improve a website or that fixing a website would alter academic standing. The paper itself rejects a strong predictive interpretation of that model in its discussion.

The [public calculation](../../data/recompute_source_workbooks.py) and [100-row result transcription](../../data/university-source-results.csv) allow another reader to inspect this check. Original source workbooks remain the authority for the source values. Our recalculation is not an independent survey of the institutions.

## What can a B2B company take from the comparison?

A familiar organization name can make an omission surprising without measuring its probability. In our September radiology and medical-imaging answers, **GE HealthCare is named in 24/150 valid targets**, **16.0%**, descriptive **95% Wilson interval 11.0% to 22.7%**. That is a fixed question-and-engine observation, not a judgment of the company or its products. [Absence Index release 2026-09, category vendor table](https://doi.org/10.5281/zenodo.22907695).

The university study does not explain that vendor result. Its composite scores and its academic sample belong to another setting. The useful parallel is the refusal to substitute a broad reputation claim for the defined measurement in front of you.

We grade the paper B for this bounded use: a documented observational comparison with inspectable source data and explicit scoring decisions. The calculation discrepancies deserve correction, while the remaining design limits still apply after correction. The unresolved question is whether a particular technical change would alter real discovery under a controlled comparison; neither the university table nor the vendor example answers it.

## What our own data shows

Our external-source check uses the authors’ [deposited 2019 results](https://doi.org/10.5281/zenodo.3484673), with the [rank comparison](../../data/university-rank-reanalysis.csv), [100-row transcription](../../data/university-source-results.csv) and [offline calculations](../../data/recompute_source_workbooks.py) available. The separate GE HealthCare observation comes from [September release 2026-09](https://doi.org/10.5281/zenodo.22907695). The archive does not measure institutional prestige, general brand awareness or the causal effect of an audit score.

## Sources

- Giannakoulopoulos, A., Konstantinou, N., Koutsompolis, D., Pergantis, M., & Varlamis, I. (2019). Academic excellence, website quality, SEO performance: Is there a correlation? Future Internet, 11(11), 242. doi:10.3390/fi11110242 . [Accessible original](https://docs.broadcastwell.com/research/source-archives/giannakoulopoulos-2019.pdf). Methods §§3.1 to 3.3; Tables 7, 9, 10 and 11. Supplied reprint PDF pp. 38 to 40, printed pp. 29 to 31. Verified 30 October 2026.
- Giannakoulopoulos, A., Konstantinou, N., Koutsompolis, D., Pergantis, M., & Varlamis, I. (2019). Academic excellence, website quality, SEO performance: Deposited spreadsheets [Data set]. Zenodo. Results Sheet1 rows 3 to 102, rank columns C and G to I; rating columns B and D. https://doi.org/10.5281/zenodo.3484673 Verified 30 October 2026.
- Broadcastwell. (2026). Absence Index, release 2026-09 [Data set]. Zenodo. Release JSON, answer JSONL and README. https://doi.org/10.5281/zenodo.22907695 Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *The university study compares academic standing with constructed website scores*. Broadcastwell. https://docs.broadcastwell.com/research/sources/giannakoulopoulos-2019/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research14,
  author = {{Broadcastwell research team}},
  title = {The university study compares academic standing with constructed website scores},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/sources/giannakoulopoulos-2019/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Arjun Mehta, management consultant.

Sources checked 30 October 2026. Independent check: pending. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the measurement chapter](https://docs.broadcastwell.com/measurement-noise/).
