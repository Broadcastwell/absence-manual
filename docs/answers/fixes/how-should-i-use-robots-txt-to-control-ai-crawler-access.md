---
title: How should I use robots.txt to control AI crawler access?
headline: How should I use robots.txt to control AI crawler access?
description: Choose crawler rules by provider and purpose; Agent Gap's 210 public
  website tasks did not test robots.txt compliance.
page_class: page
schema_type: Article
date_published: '2026-10-28T23:31:03+00:00'
date_modified: '2026-10-28T23:31:03+00:00'
hide:
- navigation
library_cluster: fixes
library_owner: Rohan Iyer, AI Engineer
library_subtopic: Crawler access controls
library_order: 75
demand_source: people-also-ask
demand_evidence: LB-Q0641, private demand receipt dated 2026-10-28
also_asked_as:
- How do robots.txt rules affect AI crawler access?
is_based_on: https://doi.org/10.5281/zenodo.23197560
evidence_kind: published-study
evidence_method_receipts:
- https://doi.org/10.5281/zenodo.23197560
---

# How should I use robots.txt to control AI crawler access?

Choose robots.txt rules for the particular crawler, purpose and URL path you intend to control. Agent Gap found pages in all 210 initial website tasks on 6 October 2026, but its 163 reached endpoints were task outcomes, not a test of robots.txt compliance. Access instructions and a successful assistant task need different evidence.

## What we measured

**Measured.** The [Agent Gap task method](https://doi.org/10.5281/zenodo.23197560) used the ChatGPT Work browser interface across 70 software vendors and three public website tasks. It recorded 206 correct results, three incorrect and one unscored across 210 initial sessions. Thirty repeat sessions were separate. The study did not compare crawler policies, authenticate bot identities or test whether a rules change caused an answer to cite a page.

**Reported.** Google's [AI feature guidance](https://developers.google.com/search/docs/appearance/ai-features), read 28 October 2026, identifies Googlebot rules as the crawl control for Search, including its AI features. Google-Extended governs different uses, including training and grounding in other Google products. Google's [robots.txt introduction](https://developers.google.com/search/docs/crawling-indexing/robots/intro), read the same date, explains that crawler instructions depend on crawler cooperation and do not secure private content.

## What this means for you

**Reasoned.** First write the access decision in plain language. You may want a public source available to search while choosing a different policy for another use. An undifferentiated instruction to block AI cannot express those separate decisions reliably.

Identify the provider's documented crawler token and the exact paths affected. Review the existing rules before adding a new group; a broad rule may cover more public content than the page you had in mind. Test representative allowed and disallowed URLs against the intended rule interpretation, then inspect the actual served robots.txt file.

Keep hosting and access controls in the same review. A page permitted by robots.txt can still be unavailable because of its server or delivery settings. A disallow instruction is also different from a request to remove a URL from search results. Use the provider's documented indexing or snippet controls for that separate goal.

Preserve a dated before-and-after rule record and the reason for the change. Verification should show which published rule applies to which URL. It cannot certify that every crawler obeyed it, that an assistant completed a task or that a future answer will include your company.

- **For a site owner:** separate search access from other provider uses.
- **For a developer:** test the named token and affected paths before changing the served file.
- **For an agency:** report policy delivery separately from observed requests or answers.

## Also asked as

How do robots.txt rules affect AI crawler access?

## Related

- [Agent Gap's task boundaries](https://broadcastwell.com/research/agent-gap)
- [Broader bot-access guide](../../resources/bot-access.md)
- [Google's crawl controls](https://developers.google.com/search/docs/appearance/ai-features)
- [Special-file requirement question](is-llms-txt-required-for-ai-search-visibility.md)

## Next step

Use the [Free 10-question check (one engine)](https://audit.broadcastwell.com/). No email is needed; runs are limited per network and per day, and by the site's daily allowance. Keep any answer observation separate from your crawler-policy receipt.

When a public source needs one approved factual clarification, [Fix one answer, $490](https://broadcastwell.com/answer-repair).

[Our answer-study method, v1.1.](https://broadcastwell.com/methodology)

Prepared by the Broadcastwell team.

Page owner: Rohan Iyer, AI Engineer. Corrections: hello@broadcastwell.com
