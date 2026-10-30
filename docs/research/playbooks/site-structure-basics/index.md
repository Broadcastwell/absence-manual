---
title: Which site-structure basics still matter?
description: Use clear permanent URLs, consistent canonical signals, navigable breadcrumbs, real error responses
  and descriptive text links, checked against current Google documentation.
page_class: research
research_id: 33
research_group: playbook
lead: Ananya Rao
published: '2026-10-30T03:55:00Z'
updated: '2026-10-30T03:55:00Z'
next_review: '2027-01-30T03:55:00Z'
canonical: https://docs.broadcastwell.com/research/playbooks/site-structure-basics/
sources_verified: true
schema_type: TechArticle
date_published: '2026-10-30T03:55:00Z'
date_modified: '2026-10-30T03:55:00Z'
is_based_on: https://developers.google.com/crawling/docs/troubleshooting/http-status-codes
---

# Which site-structure basics still matter?

**A page that says “not found” while returning HTTP 200 can be treated as a soft 404 (Google Crawling Infrastructure, 2026).**

A **200 response is not proof of a useful page or indexing**. Google’s current status-code documentation explains that content suggesting an error or empty page can be classified as a soft 404 even when the server returns success. A visible apology alone does not make a missing-page response technically correct. [Google Crawling Infrastructure, HTTP status codes](https://developers.google.com/crawling/docs/troubleshooting/http-status-codes).

Site structure gives a reader stable destinations and an intelligible route among them. It also gives crawlers addresses they can request. The checks below are practical ways to preserve those properties. They do not establish that a particular URL pattern causes a higher AI citation rate.

## Give each substantive page a preferred address

Decide which URL represents the page and use it consistently in internal links, the sitemap and relevant metadata. Keep tracking parameters out of the address you present as the permanent reference when those parameters do not change the content. A citation should continue to identify the same page after a campaign ends.

Google’s current canonical guidance distinguishes redirects, canonical annotations and sitemap signals. These communicate a preference while Google still makes its own selection. Do not promise that a tag forces a particular outcome. [Google Search Central, canonical URL guidance].

“One page, one preferred URL” is a useful publishing rule, rather than a claim that all alternate representations are forbidden. Language versions, downloads and genuine product variants can require distinct addresses. Explain the relationship instead of redirecting every alternative to an unrelated homepage.

The 2010 guide already advised concentrating on one URL when the same content was accessible through multiple addresses. Its historical recommendation belongs beside current canonical guidance, not in place of it. [Google, 2010, PDF p. 9].

## Make the address recognizable when copied

Use a readable path that describes the page’s subject. Avoid meaningless identifiers where a useful descriptive slug is practical, and avoid placing essential identity only in a long query string. A reader who receives a shortened display of a URL should still have a reasonable clue about its destination.

Google’s current URL guide recommends hyphens to separate words and explains that case differences can identify different URLs. It also recommends reducing unnecessary parameters and avoiding fragment-driven content changes. These are specific crawlability and clarity points; they do not establish a maximum SEO-friendly title length. [URL structure best practices].

Test the actual address in the places people use it: a document reference, a phone message and a search-result preview. “Truncation-safe” here means our editorial preference for recognizable, stable paths, not an operator-defined metric or a promise that every interface will show the same number of characters.

## Use breadcrumbs that match the page’s place

Show the route from a broader topic to the current page when that route helps the visitor. For this research section, a source review belongs under the research and sources context, while a study has its own study identity. Avoid breadcrumbs that point to unrelated product categories simply to insert desired words.

The 2010 guide describes breadcrumbs as a way to navigate back toward a more general section. Google’s current structured-data guide separately describes BreadcrumbList for a page’s navigational context. Keep the visible links and encoded representation consistent. [Google, 2010, PDF p. 10; Google Search Central, Breadcrumb structured data].

Follow the links after publication. A syntactically valid breadcrumb with a missing parent destination still disappoints a reader. An accurate navigational trail is useful even when no special search display appears.

## Return a real error for a missing page

A missing page should have an appropriate not-found response and a helpful explanation. Offer useful navigation without pretending that the requested content exists. A redirect is appropriate when there is a genuine replacement, rather than as a way to send every obsolete URL to the homepage.

Google distinguishes not-found responses from server failures and rate-limit signals. Its documentation says success responses can be considered for processing, while indexing remains unguaranteed. Use the status that describes the actual condition instead of choosing one solely because a dashboard shows fewer errors. [Google Crawling Infrastructure, HTTP status codes].

For a practical check, request a known page, an intentionally nonexistent path and any moved page. Inspect both the response code and the visible content. A custom error design can be pleasant to use while still returning the correct status.

## Make links work as links

Google’s link guide says crawlable anchors generally need an HTML a element with an href. A script event on a styled span is a different object. Where interactive navigation is needed, preserve a sensible ordinary link destination as well. [Google Search Central, Link best practices].

Check important routes without depending on a search form or a hidden menu. A visitor should be able to move from the section hub to an individual page and then to its evidence. Give the site a clear hierarchy.

The historical guide’s recommendation for mostly text navigation remains a useful principle, even though its examples name older technologies. Read it as a reason to provide usable links, then verify behaviour in the current site. [Google, 2010, PDF p. 12].

## Write anchors that identify the destination

Prefer a phrase such as “September citation-class table” when that is what the link opens. A page filled with repeated “click here” labels makes it difficult to understand destinations out of context. Google’s current guide recommends descriptive, reasonably concise anchor text relevant to both pages. [Link best practices, anchor text].

Do not fill every anchor with a long string of targeted terms. A useful link label sets an expectation for a human reader. The sentence around it can supply additional context when the destination is a dataset, historical source or download rather than another article.

For images used as links, provide text that explains the destination through the appropriate accessible representation. A decorative graphic should not become the only intelligible way to navigate to a substantive page.

## Check the whole route after an edit

| Check | What success establishes | What it does not establish |
|---|---|---|
| Preferred URL and response | The intended public page can be reached | Search indexing or canonical selection by an engine. |
| Canonical annotation | The page communicates its preferred identity | A binding instruction to every search system. |
| Breadcrumb and topic links | Readers can move through the published hierarchy | A quantified ranking advantage from that hierarchy. |
| Missing-path response | Absent content is represented honestly | A cure for unrelated discovery or quality problems. |
| Descriptive anchors | A reader can anticipate linked material | That the destination’s claim is factually correct. |

Run these checks on the deployed pages after a navigation change, as well as on a local preview. A broken link can survive a successful build. Keep any observed indexing state separate from these technical and editorial checks.

Google’s link guidance says, “Good anchor text is descriptive, reasonably concise”. The surrounding explanation also asks that the wording fit both the current page and the linked destination. [Google Search Central, Link best practices, “Write good anchor text”; verified 30 October 2026].

## What our own data shows

We have no measurement on this point: the causal citation effect of these site-structure changes. The Index’s archived answers can identify which URLs were visibly cited on stated dates. They do not expose every retrieval step or establish that a breadcrumb, slug or response code caused selection.

We have no controlled measurement of the citation effect of these site-structure changes. Their immediate purpose is to keep public pages reachable, understandable and accurately identified.

## Sources

- Google Crawling Infrastructure. (2026). How HTTP status codes affect Google’s crawlers. https://developers.google.com/crawling/docs/troubleshooting/http-status-codes Verified 30 October 2026.
- Google Search Central. (2026). URL structure best practices for Google Search. Updated word-separation guidance announced 23 October 2026. https://developers.google.com/search/docs/crawling-indexing/url-structure Verified 30 October 2026.
- Google Search Central. (2026). Link best practices for Google. Crawlable anchors and descriptive link text. https://developers.google.com/search/docs/crawling-indexing/links-crawlable Verified 30 October 2026.
- Google Search Central. (2026). How to specify a canonical URL with rel="canonical" and other methods. https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls Verified 30 October 2026.
- Google Search Central. (2026). Breadcrumb structured data. https://developers.google.com/search/docs/appearance/structured-data/breadcrumb Verified 30 October 2026.
- Google. (2010). Search engine optimization starter guide. Improving site structure, PDF pp. 8 to 12; content and anchor text, pp. 14 to 17. https://static.googleusercontent.com/media/www.google.com/en//webmasters/docs/search-engine-optimization-starter-guide.pdf Verified 30 October 2026.

## Cite this page

Broadcastwell research team. (2026, October 30). *Which site-structure basics still matter?*. Broadcastwell. https://docs.broadcastwell.com/research/playbooks/site-structure-basics/ Published 30 October 2026; updated 30 October 2026.

```bibtex
@online{broadcastwell2026research33,
  author = {{Broadcastwell research team}},
  title = {Which site-structure basics still matter?},
  year = {2026},
  date = {2026-10-30},
  url = {https://docs.broadcastwell.com/research/playbooks/site-structure-basics/},
  urldate = {2026-10-30},
  note = {Published 2026-10-30; updated 2026-10-30}
}
```

Prepared by the Broadcastwell research team. Lead: Ananya Rao, AI engineer.

Sources checked 30 October 2026. Independent check: 30 October 2026, Broadcastwell verification desk. This page has not been peer reviewed.

Last updated: 30 October 2026. Next review: 30 January 2027.

## Continue

- [Run a free visibility check](https://audit.broadcastwell.com/).
- [Read the valid-measurement chapter](https://docs.broadcastwell.com/valid-measurement/).
