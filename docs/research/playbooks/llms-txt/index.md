---
title: What is llms.txt, and what can it actually do?
description: A dated guide to the revised proposal, a small example and the difference between publishing a file,
  an audit reading it and an engine using it.
page_class: research
research_id: 27
research_group: playbook
lead: Rohan Iyer
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/playbooks/llms-txt/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://developers.google.com/search/updates
---

# What is llms.txt, and what can it actually do?

**Google’s June 2026 guidance says llms.txt does not affect Search visibility or rankings; the proposal serves other possible uses (Google, 2026).**

Google’s **15 June 2026** documentation update says llms.txt files are not needed for Google Search and do not positively or negatively affect visibility or rankings. It also says maintaining them for other services is fine. That is narrower than saying that no software reads them. [Google Search Central, documentation updates](https://developers.google.com/search/updates).

The proposal itself has changed. Jeremy Howard’s current **v2**, modified **10 August 2026**, describes a concise Markdown guide that helps agents find information on a website. Read that revision before repeating instructions based on the initial proposal. The file is an emerging convention, not a rule that obliges every answer engine to read or obey it. [Howard, The /llms.txt file, v2](https://llmstxt.org/).

## Which kind of adoption can you verify?

Separate publication, retrieval, documented use and measured effect. A live file proves that its publisher serves a file. An HTTP request shows that a requester asked for it. A documented audit shows that a particular product checks it. None of those observations alone shows a resulting citation gain.

There is a concrete example of a reader: Chrome’s Lighthouse documentation describes its llms.txt audit. The audit flags a server error while retrieving the file; a missing file returning 404 is marked not applicable because the file is optional. This is evidence about that audit’s behaviour, not a Google Search ranking requirement. [Chrome for Developers, llms.txt audit, updated 5 May 2026](https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt).

The opened [FastHTML documentation file](https://www.fastht.ml/docs/llms.txt) is another inspectable publishing example. Its existence does not tell us which answer engines used it in a particular response. The proposal’s adoption examples should be read as named examples, rather than a census of all consumer behaviour.

## Choose a scope you can keep accurate

Under v2 a file can sit at the origin root or under a path. It covers URLs beneath that path, with a more specific applicable file taking precedence in the proposed convention. This makes a documentation section possible without requiring control over an entire shared hostname. [Howard, v2, proposal and format sections].

Decide what belongs in the guide before adding links. For a software documentation section, that may be the overview, terminology, supported versions and the pages people need to complete a task. For a research collection, it may be the methods, datasets, releases and correction policy. A short description of purpose can prevent the link list from becoming a second, less reliable sitemap.

Do not paste every page’s full text into the index because there is no immediate file-size error. The proposal’s intended reading path keeps the overview small and places detail behind links. A file that no one can review comfortably is also difficult to maintain responsibly.

## Write the smallest useful guide

The v2 format requires an H1 naming the site or project. It can then include a summary blockquote, explanatory text without intervening headings, and H2 sections containing linked file lists. An Optional section conventionally marks secondary material. The following is an **illustrative subset**, not a claim that the live Broadcastwell file consists only of these lines:

```markdown
# Broadcastwell research

> Dated evidence about software vendors named in AI answers.

The release identifier and capture date belong with each observation.

## Primary records

- [September Index](https://doi.org/10.5281/zenodo.22907695): Versioned data and method.
- [Research evidence standard](https://docs.broadcastwell.com/research/standard/): How claims are assessed.

## Optional

- [Absence Manual](https://docs.broadcastwell.com/): Longer explanations and references.
```

For a new file, prefer links whose labels say what a reader will find. Keep identity, scope and evidence limits visible. Do not use the file to insert instructions telling a third party to ignore its own safeguards, hide contrary evidence or favour your product irrespective of the question.

V2 also proposes clean Markdown versions of content pages and link relations identifying the alternate representation and the relevant guide. If you offer such links, verify that they resolve to the promised content. A renamed HTML response is not automatically a clean Markdown representation. [Howard, v2, proposal section].

## Inspect the file that is actually being served

Request the live URL and check its status, content type and text. A search engine’s cached extract can be older than the response a visitor receives. Compare the visible company description, dates and linked destinations with current public pages, then repair stale wording through the normal publishing process.

Our direct read of [docs.broadcastwell.com/llms.txt](https://docs.broadcastwell.com/llms.txt) on **30 October 2026** returned the current company description and dated terms. A search-cache version presented an older description. We therefore use the direct response as the worked publishing example. This is a content-consistency observation, not evidence that an AI answer consumed either version.

After a revision, read the file again from its public URL. Follow a sample of important links and any Markdown alternates you added. Check whether the file is still within the scope its path implies. If an item is a historical release, identify it as such rather than silently changing its label to “latest.”

## Keep discovery separate from permission

The proposal is intended to coexist with robots.txt, sitemaps and structured data. Those files do different jobs. A curated reading guide is not an access-control system, a complete crawl inventory or an authorization to reuse copyrighted material. Publishing a link cannot grant rights that the publisher does not hold. [Howard, v2, existing standards].

Keep private material out of every public representation. A file can reveal a link even if that link is absent from the human navigation. Check the full text, not merely the first screen. Where a document needs authentication, publishing an explanatory public page is a different choice from exposing the document itself.

## What would show that it helped?

Define the outcome before interpreting logs. A fetch of llms.txt, retrieval of a linked document, a source citation and a buyer visit are distinct events. A convincing effect claim would need a suitable comparison and a way to distinguish the file change from other changes to the site or engine. This guide supplies no such experiment.

For operational monitoring, report the observation you actually have: the requested path, period covered, stated requester identity and whether that identity was verified. Avoid saying that “AI reads our file” when the record only contains a matching user-agent string. The [crawler-log study](https://docs.broadcastwell.com/research/studies/ai-crawler-log/) explains that boundary.

Maintain llms.txt if it gives a useful, accurate route into your public material. Describe its intended use plainly. A current guide can be worthwhile without attaching an unsupported visibility promise to it.

## What our own data shows

We have no measurement on this point: whether serving our llms.txt changes citation or naming. Broadcastwell serves a public llms.txt file, which was opened directly for this guide. We have no measurement showing that the file increased our citations, naming rate or buyer visits. Presence and effect remain separate questions.

The initial crawler-log record covers selected public Index HTML routes. It is not a log of all requests to the documentation host or a proof of llms.txt consumption.

## Sources

- Google Search Central. (2026, June 15). Clarifying guidance on llms.txt files. Latest documentation updates. https://developers.google.com/search/updates Verified 30 October 2026.
- Howard, J. (2026, August 10). The /llms.txt file, v2. Proposal first published 3 September 2024. https://llmstxt.org/ Verified 30 October 2026.
- Chrome for Developers. (2026, May 5). llms.txt. Lighthouse agentic-browsing audit documentation. https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt Verified 30 October 2026.
- FastHTML. (2026). Documentation llms.txt [Live text file]. https://www.fastht.ml/docs/llms.txt Verified 30 October 2026.
- Broadcastwell. (2026). llms.txt [Live text file]. Direct response opened 30 October 2026; search-cache copy differed. https://docs.broadcastwell.com/llms.txt Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *What is llms.txt, and what can it actually do?*. Broadcastwell. https://docs.broadcastwell.com/research/playbooks/llms-txt/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research27,
  author = {{Broadcastwell research team}},
  title = {What is llms.txt, and what can it actually do?},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/playbooks/llms-txt/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Rohan Iyer, AI engineer.

Sources checked 30 October 2026. Independent check: pending. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the vendor-facts chapter](https://docs.broadcastwell.com/vendor-facts/).
