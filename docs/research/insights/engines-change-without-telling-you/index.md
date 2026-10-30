---
title: Search ordering needs a date and a configuration
description: A 2019 Web of Science observation and two dated Index releases explain why comparison conditions must
  precede claims of change.
page_class: research
research_id: 6
research_group: insight
lead: Priya Nair
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/insights/engines-change-without-telling-you/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://doi.org/10.3390/fi11090202
---

# Search ordering needs a date and a configuration

**August covered four engines; September covered five. These are dated standings, not a controlled trend (Broadcastwell, 2026, release READMEs).**

Web of Science produced an unexpectedly citation-like ordering during **20 to 25 May 2019**, according to Rovira and colleagues. Their explanation that the service was testing a different relevance order was an inference, not an operator-confirmed experiment. [Rovira et al., 2019, §4](https://doi.org/10.3390/fi11090202).

Our August and September Index tables illustrate a related comparison problem. The August observation used **four engines**; September used **five**, adding Google AI Mode. Both used fixed category questions and repeated observations, but the pooled configurations differ. We state that before placing their standings side by side.

You can read both records as dated observations. You cannot attribute their differences to a vendor's actions, an engine update or a visibility trend from these tables alone. There is no matched counterfactual identifying any of those causes.

## A live service departed from its documented order

Rovira and colleagues compared scholarly results with an ordering based on academic citation counts. They collected up to **1,000 results per search**, using sets of **25 search terms**, and summarized the citation-based ranks at each result position using medians. Their Table 2 reports a Spearman coefficient of **−0.075** for one Web of Science collection and **0.907** for the other. [Rovira et al., §3 and Table 2].

These are correlations for the median-based summary, not the proportion of individual results sorted correctly. They do not establish the precise contents of a private ranking algorithm. The researchers' observed order was more consistent with citation sorting during the identified period than with the service's documented relevance criteria.

The authors describe their testing explanation as “only an inference.” That wording is central to the claim. It prevents the observed difference from being retold as a confirmed disclosure by Web of Science. [Rovira et al., §4, original article p. 12; reprint PDF p. 60].

The historical service comparison also contains a trap for contemporary advice. Microsoft Academic is among the systems in the paper. A result from that historical comparison should not become an instruction to optimize for a service without checking its present status. A paper's date belongs to the finding as much as its coefficient does.

## Configuration before the standings

| Observation | August release 2026-08.1 | September release 2026-09 |
|---|---|---|
| Engines | ChatGPT, Claude, Perplexity, Google AI Overviews | Those engines plus Google AI Mode |
| Target questions | 10 per category | 10 per category |
| Scheduled repeats | 3 | 3 |
| CRM eligible target answers | 117 | 150 |
| Project-management eligible target answers | 120 | 150 |
| Scope of the table below | CRM and project management | The same named categories, within a broader release |

Sources: [August deposit](https://doi.org/10.5281/zenodo.22721962), corrected README and release JSON; [September deposit](https://doi.org/10.5281/zenodo.22907695), README and release JSON. Excluded answers reduce the eligible base. They are not vendor misses. The comparison uses vendor naming, preserving the outcome label across these displayed columns.

## Selected CRM observations

Each cell contains named count / valid target base, percentage and descriptive 95% Wilson interval. These are snapshots with shared questions and dependent answers, not independent market estimates.

| Checked vendor | August 2026-08.1 | September 2026-09 |
|---|---|---|
| Salesforce Sales Cloud | 78 / 117, 66.7% (57.7% to 74.6%) | 109 / 150, 72.7% (65.0% to 79.2%) |
| HubSpot CRM | 77 / 117, 65.8% (56.8% to 73.8%) | 113 / 150, 75.3% (67.9% to 81.5%) |
| Zoho CRM | 63 / 117, 53.8% (44.8% to 62.6%) | 73 / 150, 48.7% (40.8% to 56.6%) |
| Microsoft Dynamics 365 | 23 / 117, 19.7% (13.5% to 27.8%) | 36 / 150, 24.0% (17.9% to 31.4%) |
| Nimble | 0 / 117, 0.0% (0.0% to 3.2%) | 0 / 150, 0.0% (0.0% to 2.5%) |

The interval beside a zero is worth retaining. No naming in the captured sample is an observation, while permanent invisibility is a much broader claim. A larger eligible base can alter the interval even when the observed count stays at zero.

## Selected project-management observations

| Checked vendor | August 2026-08.1 | September 2026-09 |
|---|---|---|
| Jira | 32 / 120, 26.7% (19.6% to 35.2%) | 63 / 150, 42.0% (34.4% to 50.0%) |
| Asana | 62 / 120, 51.7% (42.8% to 60.4%) | 97 / 150, 64.7% (56.7% to 71.9%) |
| monday.com | 71 / 120, 59.2% (50.2% to 67.5%) | 26 / 150, 17.3% (12.1% to 24.2%) |
| Wrike | 49 / 120, 40.8% (32.5% to 49.8%) | 54 / 150, 36.0% (28.8% to 43.9%) |
| Notion | 1 / 120, 0.8% (0.1% to 4.6%) | 6 / 150, 4.0% (1.8% to 8.5%) |

Source for both tables: the corresponding vendor mention_rate fields in the versioned deposits. [Download the complete side-by-side table](../../data/dated-standings.csv), including every checked vendor common to these categories. No movement labels or inferred causal explanation are attached to it.

## The tempting story is not the observed result

The table for monday.com is especially likely to attract a narrative. The counts are visibly different. But the question we can answer here is what was recorded under each configuration. The table cannot separate engine composition, ordinary answer variation, source changes and vendor activity.

An engine could also change without issuing a public notice. That possibility is a reason to retain observation dates; it is not evidence that a specific hidden update occurred between these releases. Invoking an unseen update whenever a result differs would make the explanation impossible to test.

The Web of Science paper helps because its authors kept both the empirical observation and the uncertainty of their explanation. The relevant analogy is their restraint. Scholarly citation sorting in a historical database is not the same outcome as software naming in a present-day answer.

## What would permit a persistence statement?

Our registered persistence plan requires an additional eligible release and a comparable consecutive-release pair. It specifies the common vendor set and valid-answer bases before calculating transition rates. The current two-release display cannot substitute for those conditions. [OSF registration](https://doi.org/10.17605/OSF.IO/MKJ9V).

Even a comparable pair would describe persistence within its chosen questions and checked vendors. It would not prove why a vendor remained absent or present. Causal attribution to an intervention would require another design and another evidentiary claim.

For your own reporting, keep a definition table next to the chart. Identify engine set, buyer questions, repeats, exclusions, product identity and outcome. A naming measure should not quietly become a citation measure halfway through the series. If a condition changes, retain the old observation and label the new one.

This creates an inconvenience for a headline: a side-by-side table can remain informative without yielding a movement claim. A company can still inspect the specific answers and supporting sources. The unresolved question is which comparable future observations will permit a transition analysis, and what that analysis will leave unexplained.

## What our own data shows

The [complete dated-standings CSV](../../data/dated-standings.csv) places the deposited August and September naming counts side by side. Primary version DOIs: [10.5281/zenodo.22721962](https://doi.org/10.5281/zenodo.22721962) and [10.5281/zenodo.22907695](https://doi.org/10.5281/zenodo.22907695). Configurations differ. We have no measurement on this point: these observations do not establish comparable-release persistence or an effect of a particular engine update.

## Sources

- Rovira, C., Codina, L., Guerrero-Solé, F., & Lopezosa, C. (2019). Ranking by relevance and citation counts, a comparative study: Google Scholar, Microsoft Academic, WoS and Scopus. Future Internet, 11(9), 202. https://doi.org/10.3390/fi11090202 Verified 30 October 2026.
- Broadcastwell. (2026). Absence Index, release 2026-08.1 [Data set]. Zenodo. Release files and README. https://doi.org/10.5281/zenodo.22721962 Verified 30 October 2026.
- Broadcastwell. (2026). Absence Index, release 2026-09 [Data set]. Zenodo. Release JSON, answer JSONL and README. https://doi.org/10.5281/zenodo.22907695 Verified 30 October 2026.
- Broadcastwell. (2026). Does absence persist from one release to the next? [Registration]. OSF. Registered 30 October 2026, 01:12:44 UTC. https://doi.org/10.17605/OSF.IO/MKJ9V Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *Search ordering needs a date and a configuration*. Broadcastwell. https://docs.broadcastwell.com/research/insights/engines-change-without-telling-you/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research6,
  author = {{Broadcastwell research team}},
  title = {Search ordering needs a date and a configuration},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/insights/engines-change-without-telling-you/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Priya Nair, management consultant.

Sources checked 30 October 2026. This page has not been peer reviewed.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the measurement chapter](https://docs.broadcastwell.com/measurement-noise/).
