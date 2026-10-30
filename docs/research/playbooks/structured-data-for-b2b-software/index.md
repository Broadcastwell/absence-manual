---
title: Which structured data belongs on a B2B software site?
description: Choose markup by the visible entity and current consumer requirements. FAQPage remains a vocabulary
  type, but Google retired FAQ rich results in May 2026.
page_class: research
research_id: 26
research_group: playbook
lead: Rohan Iyer
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/playbooks/structured-data-for-b2b-software/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://developers.google.com/search/updates
---

# Which structured data belongs on a B2B software site?

**Google stopped showing FAQ rich results from 7 May 2026; FAQPage remains a Schema.org type (Google, 2026; Schema.org, 2026).**

Google gives **7 May 2026** for the end of FAQ rich-result display; its later documentation update explains why the former FAQ feature page was removed. A Schema.org type can remain meaningful even after a search feature stops using it in that way. [Google Search Central, May 8 and June 15 changelog entries](https://developers.google.com/search/updates); [Schema.org, FAQPage](https://schema.org/FAQPage).

For a B2B software site, start with what the page actually describes. An organization, a software application, a product offer, a dataset and a navigation trail are different things. Marking all of them on every page makes the representation less useful. Choose the type and properties that match the visible material, then check the requirements of the service you hope will consume them.

## Match the entity before choosing properties

| Visible subject | Appropriate starting point | What to establish first |
|---|---|---|
| The company itself | Organization | Consistent name, official site and an identity that the page supports. |
| A particular software application | SoftwareApplication, or an appropriate subtype | The application’s own name and factual capabilities; distinguish the app from its publisher. |
| A product or commercial offer | Product and, where appropriate, Offer | What is actually offered, the current terms and whether the chosen Google feature supports that content. |
| A page of published questions and answers | FAQPage | The questions and answers are really on the page; do not promise a retired Google rich result. |
| A published research dataset | Dataset, with DataDownload for its files | Name, description, creator, identifier, license, access and distribution details. |
| The route through a site | BreadcrumbList | A real, ordered navigation trail with resolvable destinations. |

The table is a planning aid. That vocabulary does not confer Google eligibility. The broad Schema.org vocabulary and Google’s supported feature requirements are separate references.

## Give the organization a stable identity

Google’s Organization documentation explains that organization markup can help it understand administrative details and distinguish similarly named entities. Use an official name and website that agree with the company’s visible facts. A stable identifier can connect references to the same organization across pages. [Google Search Central, Organization structured data].

Avoid making a department, a product and the legal company share a name merely for convenience. Describe their actual relationship. Link to a profile as an identity reference only when it identifies the same entity. A page that mentions the company is not automatically an equivalent identity page.

Do not add an award, partner status, address or service area because another site with a similar name has one. Evidence still comes before markup. If a fact cannot be supported in ordinary prose, encoding it out of sight does not make it safer to assert.

## Separate an application from a price claim

SoftwareApplication describes software. Google’s current software-app rich-result requirements include a name, an offer price and a rating or review, with further rules for those properties. An application description that is valid in the vocabulary may therefore remain ineligible for that specific search appearance. [Google Search Central, Software app structured data, required properties].

Do not invent a zero price for a product that requires a commercial agreement. Likewise, do not make up a star rating to satisfy a required field. If the real offer lacks the data needed for a feature, leave the feature unclaimed. The application can still have an accurate page.

When prices or plans change, review both the visible page and the embedded data. An old number can survive in a template after the public table has changed. Inspect the rendered page rather than assuming that a successful content edit updated every representation.

## Describe a dataset so a reader can obtain it

A dataset landing page should identify the collection before it lists files. State what the rows represent, who created the data, which version is being described and what license permits reuse. Link the actual download separately from the explanation of the method. Google’s Dataset guide recommends identifiers such as DOIs and describes distribution metadata. [Google Search Central, Dataset structured data].

Here is an invented illustration of a small research release. This example reports no measurement:

```json
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "Example invoice-format observations",
  "description": "Illustrative metadata only; not an actual dataset.",
  "creator": {"@type": "Organization", "name": "Example Research"},
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "distribution": {
    "@type": "DataDownload",
    "encodingFormat": "text/csv",
    "contentUrl": "https://example.org/data/invoice-formats.csv"
  }
}
```

A real release needs a real destination and a license the publisher is entitled to grant. A DOI identifies the deposited object; it does not certify the analysis or establish peer review. Keep a version-specific identifier distinct from an identifier that resolves to the record family.

## Use FAQPage for the content it actually represents

The continuing Schema.org definition covers a webpage presenting frequently asked questions. That does not authorize hidden questions inserted purely to target searches. Keep the answers useful and consistent with the visible page. If visitors can submit multiple competing answers, inspect the distinction from QAPage before choosing a type. [Schema.org, FAQPage and its linked QAPage definition].

For Google Search, the current retirement notice supersedes older advice about eligibility for particular kinds of sites. Do not promise FAQ enhancements on a software pricing page, and do not claim that removing the enhancement means all question-led writing has lost its purpose. A question can help a buyer even when no special visual result is offered.

## Validate three different things

First, parse the rendered JSON. A missing comma, invalid escape or truncated script can prevent a consumer from reading it. Test the deployed page, since a source file and the final response can differ.

Second, check vocabulary types and property domains with the Schema.org validator. An output with no syntax error can still put a real property on the wrong kind of object. Resolve warnings on their merits rather than treating them as proof that the content is false.

Third, check the current Google guide and Rich Results Test for a supported feature. A general vocabulary validation is not a Google eligibility decision. Even eligibility does not guarantee display. If a public test is unavailable, record that limitation; do not relabel a local check as a successful public test. [Google Search Central, Introduction to structured data].

## Check consistency after publication

Compare the page title, entity names, dates, download links and current offers with the rendered markup. Follow the breadcrumbs. Check the canonical destination and any version identifier. Where several pages refer to the same dataset or company, inconsistent identifiers deserve investigation.

Lewandowski’s historical classifier counted observable optimization signals. Detecting structured data in that design is not evidence that the markup was accurate, eligible for a rich result or responsible for the page’s position. The later registered signal study likewise concerns presence, with its own rules. Use those observations to describe the page, while keeping validation and causal claims separate.

Google defines structured data as “a standardized format for providing information about a page”. The definition explains machine-readable description, without establishing that any particular feature will appear. [Google Search Central, Introduction to structured data markup in Google Search, opening paragraph; verified 30 October 2026].

## What our own data shows

We have no measurement on this point: the causal effect of adding a particular structured-data type on AI citation. Our registered page-signal study includes JSON-LD and microdata as observable signals. Its structured-data presence test does not certify a page’s factual content or search-feature eligibility. Invalid JSON-LD is separately recorded.

The Index’s dated citation arrays do not supply a controlled test of adding markup. We have no measurement establishing that a particular type increases a software vendor’s chance of citation.

## Sources

- Google Search Central. (2026). Latest documentation updates. FAQ deprecation, May 8; documentation removal, June 15. https://developers.google.com/search/updates Verified 30 October 2026.
- Schema.org. (2026). FAQPage. Type definition, not a promise of a Google feature. https://schema.org/FAQPage Verified 30 October 2026.
- Google Search Central. (2026). Organization structured data. https://developers.google.com/search/docs/appearance/structured-data/organization Verified 30 October 2026.
- Google Search Central. (2026). Software app structured data. https://developers.google.com/search/docs/appearance/structured-data/software-app Verified 30 October 2026.
- Google Search Central. (2026). Dataset structured data. https://developers.google.com/search/docs/appearance/structured-data/dataset Verified 30 October 2026.
- Google Search Central. (2026). Introduction to structured data markup in Google Search. https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data Verified 30 October 2026.
- Lewandowski, D., Sünkler, S., & Yagci, N. (2021). The influence of search engine optimization on Google's results: A multi-dimensional approach for detecting SEO. WebSci 2021, 12 to 20. doi:10.1145/3447535.3462479 . Accessible author original: https://searchstudies.org/wp-content/uploads/2021/08/3447535.3462479.pdf Verified 30 October 2026.
- Broadcastwell. (2026). Do AI engines cite optimized pages? [Registered study plan]. OSF. Platform registration timestamp 30 October 2026, 01:06:12 UTC. https://doi.org/10.17605/OSF.IO/DVYFU Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *Which structured data belongs on a B2B software site?*. Broadcastwell. https://docs.broadcastwell.com/research/playbooks/structured-data-for-b2b-software/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research26,
  author = {{Broadcastwell research team}},
  title = {Which structured data belongs on a B2B software site?},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/playbooks/structured-data-for-b2b-software/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Rohan Iyer, AI engineer.

Sources checked 30 October 2026. Independent check: 30 October 2026, Broadcastwell verification desk. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the answer-page chapter](https://docs.broadcastwell.com/vendor-facts/).
