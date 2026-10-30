---
title: Why nobody can give you a ranking recipe
description: An exploratory SEO study, an academic-search comparison and dated AI-answer evidence measure different
  things. None supplies a universal ranking formula.
page_class: research
research_id: 3
research_group: insight
lead: Priya Nair
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/insights/no-ranking-recipe/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://doi.org/10.3390/fi11020032
---

# Why nobody can give you a ranking recipe

**A correlation between a page feature and search position does not tell you what changing that feature will do.**

The strongest average association in Ziakis and colleagues' exploratory ranking table was SSL certification, with a Spearman coefficient of **−0.3371**. Their stated threshold for making stronger assumptions was an absolute coefficient above **0.5**. No factor's average cleared that threshold. [Ziakis et al., 2019, §2 and Table 2; collected April 2018](https://doi.org/10.3390/fi11020032).

We use that table as a worked example of weak evidence, graded C. It cannot establish a set of ranking factors or the effect of implementing them. You can accept HTTPS as sensible website practice without claiming that this study measured its causal ranking benefit.

The authors themselves write that “correlation does not mean always causation.” Their discussion nonetheless makes stronger recommendations than their averaged coefficients warrant. The gap between those parts of the paper is more informative than another ranked checklist of tactics. [Ziakis et al., §2, original article p. 5; reprint PDF p. 14](https://doi.org/10.3390/fi11020032).

## Three searches cannot expose a general formula

The researchers took the first **15 results** for each of **three queries**, producing **45 result URLs**: Hotel Athens, email marketing and casual shoes. These are identifiable search topics, with different businesses and competing pages. They were collected at separate times in April 2018. The paper measured **21 factors**, normalized their values and calculated rank correlations for each query before averaging the coefficients. [Ziakis et al., §2 and Table 2].

| Quantity in the exploratory table | Reported average | What it permits us to say |
|---|---:|---|
| SSL certificate versus numeric search position | −0.3371 | An observed association in these searches, below the paper's own stated bar |
| Quantity of backlinks versus position | −0.3000 | A modest average with substantial variation between queries |
| Text length versus position | −0.2880 | A sample relationship, with no identified optimum page length |
| Loading time versus position | 0.0198 | A near-zero average that does not establish that speed never matters |

Source: Ziakis et al., 2019, Table 2, original article pp. 10 to 11, reprint PDF pp. 19 to 20. These coefficients are not proportions; no numerator, denominator or Wilson interval applies to them. The sample and averaging procedure are their relevant boundaries.

Averaging can hide disagreement. In that table, the backlink coefficient is negative for Hotel Athens and slightly positive for casual shoes. The average does not tell a construction-software company how many links it needs or which link would change an answer. Nor does a near-zero average prove that an underlying feature has no effect under other conditions.

There is a further selection problem. These pages were already in the retrieved result set. A correlation among pages that appeared cannot explain all the pages that failed to appear. Visibility has several stages, and a study of the surviving results sees only part of the process.

## A much clearer association can still have a narrow meaning

Rovira and colleagues asked a more specific question: how closely does the relevance ordering of scholarly search results track the number of academic citations received? Their Table 2 contains large coefficients for some search systems. It also contains a much smaller Google Scholar coefficient for an unrestricted two-term search than for a title-restricted search. [Rovira et al., 2019, Table 2](https://doi.org/10.3390/fi11090202).

The detail that matters is their unit of analysis. The coefficients summarize **median citation counts at result positions**, across a selected set of scholarly searches. They are not the correlation across every individual result, and they do not describe the citation probability of a software vendor in a conversational answer.

The paper is useful because it records its conditions and compares alternative systems. It does not give a transferable instruction to manufacture citations or repeat title keywords. Academic citations are references received by scholarly works. Source links inside an AI answer are a different kind of citation, produced for a different purpose.

Even a strong relationship leaves the causal question open. Older documents have had more time to receive citations. Topics differ in their citation practices. Search systems may combine several signals that correlate with each other. Without a suitable intervention or identification strategy, a large coefficient cannot isolate the consequence of changing one feature.

## The answer can change with the engine

Our own published comparison gives another reason to resist a single recipe. In State of GEO, volume III, **14 of 32 companies** tested on multiple engines were visible on some and absent on others. That is a descriptive company-level comparison in the tested sample, not the probability that any company will have that pattern. [Broadcastwell, 2026, volume III README, headline findings](https://doi.org/10.5281/zenodo.21789120).

The same report also compared repeated answers within an engine with answers across engines. Its length controls changed the interpretation for Claude. A gap apparent in the unadjusted comparison did not remain distinguishable once answer-list length was accounted for. We retain that qualification rather than citing only the dramatic unadjusted result.

This is an awkward side thread for anyone selling a recipe. If one engine names longer lists, simple overlap can make it look more or less similar to another engine for mechanical reasons. The statistic has to answer the question you intended. Otherwise an apparent discovery about engine preferences may partly be a discovery about answer length.

## What a useful test would preserve

Suppose you revise a product explanation and later see a citation. The observation is worth saving. It does not establish that the revision caused the citation: the answer, source collection or engine behavior could have changed at the same time.

A more informative comparison would preserve the buyer question, product identity, engine, observation window and definition of success. It would retain answers that do not name the vendor, rather than selecting only the satisfying examples. It would distinguish naming from a link to the vendor's own domain and a link to a third party describing the vendor. These are outcome definitions a reader can inspect, not a claim to know the engine's private formula.

You also need a reason for the proposed edit. Correcting an inaccurate specification, clarifying who a product serves or making a source page readable has direct value to a buyer. Its usefulness does not depend on an unsupported promise about an algorithmic weight. A measurement can then ask whether the relevant answer changed under comparable conditions.

## A page can be better before a ranking claim exists

There is a practical distinction between a defect and an unproven tactic. A broken product link is observable. An undocumented promise that a particular page length wins AI citations is a hypothesis. Treating both as equally certain makes prioritization harder, not easier.

For a software team, the first question is often whether a buyer could verify the statement at all. Does the cited page state the product's scope? Is the date visible? Does the evidence support the exact sentence? A clear answer to those questions may justify an editorial change even when there is no measured visibility effect.

We still want explanatory research. Merely counting answers can leave mechanisms obscure, and an observational record cannot choose every next action. But the missing mechanism should remain an open question. The alternative is to attach an engine-shaped explanation to a change that happened once, then sell the explanation as if the counterfactual had been observed.

## What our own data shows

Volume III reports 14 of 32 companies visible on some tested engines and absent on others: 43.8%, descriptive 95% Wilson interval 28.2% to 60.7%. The base is companies tested on multiple engines, not answers or the software market. Source: [version DOI 10.5281/zenodo.21789120](https://doi.org/10.5281/zenodo.21789120), README headline findings. The deposited report's length-control qualification remains essential for interpreting its separate answer-overlap analysis.

## Sources

- Ziakis, C., Vlachopoulou, M., Kyrkoudis, T., & Karagkiozidou, M. (2019). Important factors for improving Google search rank. Future Internet, 11(2), 32. https://doi.org/10.3390/fi11020032 Verified 30 October 2026.
- Rovira, C., Codina, L., Guerrero-Solé, F., & Lopezosa, C. (2019). Ranking by relevance and citation counts, a comparative study: Google Scholar, Microsoft Academic, WoS and Scopus. Future Internet, 11(9), 202. https://doi.org/10.3390/fi11090202 Verified 30 October 2026.
- Broadcastwell. (2026). State of GEO, volume III [Data set and report]. Zenodo. README: repeated questions and same-vendor comparisons. https://doi.org/10.5281/zenodo.21789120 Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *Why nobody can give you a ranking recipe*. Broadcastwell. https://docs.broadcastwell.com/research/insights/no-ranking-recipe/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research3,
  author = {{Broadcastwell research team}},
  title = {Why nobody can give you a ranking recipe},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/insights/no-ranking-recipe/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Priya Nair, management consultant.

Sources checked 30 October 2026. This page has not been peer reviewed.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the engine comparison chapter](https://docs.broadcastwell.com/engine-divergence/).
