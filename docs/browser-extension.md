---
title: What does our AI Shortlist Check browser extension do?
headline: What does our AI Shortlist Check browser extension do?
description: Our free Chrome browser extension shows the Absence Index record of the software site you are on, with bases and intervals, using one permission only.
page_class: page
schema_type: Article
date_published: '2026-11-09T00:00:00+00:00'
date_modified: '2026-11-09T00:00:00+00:00'
template: business-hub.html
---

# What does our AI Shortlist Check browser extension do?

Our free AI Shortlist Check browser extension for Chrome shows how often ChatGPT, Claude, Perplexity, Google AI Overviews and Google AI Mode named the software company whose website you are viewing, from the Absence Index release 2026-09. It covers 286 vendors in 14 categories, prints every figure with its base and interval, and asks for one permission only.

Updated 9 November 2026.

You install it from its public source repository, because it is not listed in the Chrome Web Store as of 9 November 2026. The five steps are below.

## What it shows

Click the toolbar icon on a software company's site. If the company is one of the 286 vendors in the [September Index](https://doi.org/10.5281/zenodo.22907695), you see:

- how many of up to 150 valid answers named it, with the base and the Wilson 95 percent interval as the Index publishes them;
- how often its own domain was cited in those answers;
- which vendors were named most in its category.

If the company is not in the Index, one click opens the [Free 10-question check (one engine)](https://audit.broadcastwell.com/) for that site. You can also search all 286 vendors from any page.

**Worked example.** On procore.com the extension reads the Index record for Procore in construction project management software: named in 109 of 150 valid answers, 72.7 percent, interval 65.0 to 79.2 percent; own domain cited in 30 of 150, 20.0 percent, interval 14.4 to 27.1 percent. You can check both figures against the [release file](https://index.broadcastwell.com/data/release-2026-09.json) and the category record on the Index. These are observed answers on stated dates, not a ranking and not a judgment of product quality.

## What it can and cannot see

| Question | Answer |
| --- | --- |
| Permissions | One: `activeTab`. It reads the address of the current tab only when you click its icon. |
| Page content and history | Not read. It matches the hostname on your device against vendor records bundled in the extension. |
| Data sent anywhere | None in the background. No analytics, no cookies, no remote code, no background or content script. |
| Links it opens | The free-check link can carry the hostname you selected, to prefill the check. Index and method links carry the label `utm_source=chrome_extension`, which holds no personal identifier. The checkout link carries no label. |
| Chrome version | 123 or later, per its manifest |

These answers restate the extension's [privacy section](https://broadcastwell.com/privacy), updated 27 October 2026, and its source code, which anyone can read.

## How to install it from source

1. Download the repository from [github.com/Broadcastwell/ai-shortlist-check](https://github.com/Broadcastwell/ai-shortlist-check) (Code, then Download ZIP) and unzip it.
2. In Chrome, open the Extensions page by typing `chrome://extensions` in a new tab.
3. Turn on Developer mode with the switch on that page.
4. Click Load unpacked and choose the unzipped folder.
5. Pin AI Shortlist Check to the toolbar from the extensions menu.

These steps follow Chrome's own guide to loading an unpacked extension. You can remove the extension at any time from the same Extensions page.

## Where the numbers come from

The extension ships the Index release 2026-09, released 23 September 2026, with answers captured 22 to 23 September 2026 under method v1.1: 14 categories, 286 vendors, 2,095 valid target answers, ten buyer questions per category, three scheduled runs and five engines. The release files it was built from are kept in the repository with their SHA-256 hashes, and its build stops if any figure differs from the release JSON or a category CSV, or if a recomputed Wilson interval disagrees. Our [open data catalog](open-data.md) lists the same release files.

A company missing from the bundled list is not a measured absence: it was simply not in the September checked set. A checked vendor named in none of its answers is a different finding, the one our chapter on vendors [named zero times](named-zero-times.md) measures.

## License and source

Code: MIT. Data: CC BY 4.0 with attribution to Broadcastwell, DOI 10.5281/zenodo.22907695. Our [citation page](cite.md) gives the citation in four formats.

## Sources

- Broadcastwell, [AI Shortlist Check repository](https://github.com/Broadcastwell/ai-shortlist-check), version 1.0.0, read 9 November 2026: README, manifest and bundled data file.
- Broadcastwell, [Privacy notice, AI Shortlist Check extension privacy](https://broadcastwell.com/privacy), section updated 27 October 2026, read 9 November 2026.
- Broadcastwell, Absence Index release 2026-09, [release file](https://index.broadcastwell.com/data/release-2026-09.json), DOI [10.5281/zenodo.22907695](https://doi.org/10.5281/zenodo.22907695).
- Chrome for Developers, [Hello World extension, "Load an unpacked extension"](https://developer.chrome.com/docs/extensions/get-started/tutorial/hello-world), last updated 4 October 2022, read 9 November 2026.

Related: our [product documentation](product-docs.md) and our [AI search glossary](ai-search-glossary.md).
