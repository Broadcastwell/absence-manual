---
title: What do AI crawlers do, and how can site owners control access?
headline: What do AI crawlers do, and how can site owners control access?
description: Search, training and user retrieval use different bot controls. Agent Gap reached 67 of 70 description-task endpoints, without measuring any crawler rule.
page_class: page
schema_type: Article
date_published: '2026-10-29T16:17:31+00:00'
date_modified: '2026-10-29T16:17:31+00:00'
hide:
- navigation
library_cluster: fixes
library_owner: Rohan Iyer, AI Engineer
library_subtopic: Crawler controls
library_order: 166
demand_source: google-autocomplete
demand_evidence: LB-Q0132, private demand receipt dated 2026-10-28
also_asked_as:
- What do AI crawlers do, and how can site owners control access?
is_based_on: https://doi.org/10.5281/zenodo.23197560
evidence_kind: published-study
evidence_method_receipts:
- https://doi.org/10.5281/zenodo.23197560
---

# What do AI crawlers do, and how can site owners control access?

On our 29 October 2026 read, OpenAI and Anthropic document different web robots for search, training and user-directed retrieval. Choose the rule for the job you mean to permit or block. Our Agent Gap study reached the endpoint in 67 of 70 initial description tasks on 6 October 2026; those website tasks did not identify a crawler or test the effect of a robots rule.

## What we measured

**Reported.** OpenAI's [bot documentation](https://developers.openai.com/api/docs/bots) separates OAI-SearchBot for search from GPTBot for training. It describes ChatGPT-User as acting on user requests; that agent is separate from automatic search crawling. [Anthropic's crawler article](https://support.anthropic.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler) distinguishes ClaudeBot, Claude-SearchBot and Claude-User, with their own purposes and robots.txt instructions. Both sources were read on 29 October 2026.

**Measured.** The [Agent Gap protocol](https://doi.org/10.5281/zenodo.23197560) records the 67 reached endpoints within its initial Describe task for 70 software vendors. The task concerned the vendor's public website. It did not classify requests as OAI-SearchBot, GPTBot or any Anthropic robot.

The endpoint count cannot establish whether a particular crawler was allowed or blocked.

## What this means for you

**Reasoned.** Name the robot in the decision. A rule about GPTBot concerns OpenAI's training crawler; the same provider documents OAI-SearchBot for search. A site owner who intends to restrict training while allowing search needs to inspect those distinct rules, rather than treating the company name as one access setting.

Anthropic makes another distinction useful for a site owner: Claude-User serves user-directed retrieval, while Claude-SearchBot supports search. Its guide places controls in robots.txt for the site or subdomain concerned. If your product documentation lives on a separate subdomain from your homepage, check the instructions at that address too.

For OpenAI search eligibility, the [search help article](https://help.openai.com/en/articles/9237897-searching-the-web-with-chatgpt) also asks publishers to allow traffic from the published searchbot IP addresses at the host. A robots permission and a host restriction are separate checks. Do not change one and report that both were verified.

Keep the task receipt separate. In Agent Gap, reaching a description-task endpoint is the reported event, so its 67 successes cannot be relabelled successful crawler visits. A missing company name in a later AI answer would likewise require its own answer record; it would not identify which robot requested a page.

For an agency managing a documentation subdomain, write down the exact intended purpose beside the bot rule and the address inspected. That makes the Claude-User or OAI-SearchBot choice clear to the person maintaining that specific host.

## Also asked as

What do AI crawlers do, and how can site owners control access?

## Related

- [OpenAI bot purposes](https://developers.openai.com/api/docs/bots)
- [Anthropic web robots](https://support.anthropic.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
- [Agent Gap study](https://doi.org/10.5281/zenodo.23197560)

## Next step

Use [Free 10-question check (one engine)](https://audit.broadcastwell.com/) to inspect a defined set of buyer questions. No email is needed; runs are limited per network and per day, and by the site's daily allowance.

For one documented gap, [Fix one answer, $490](https://broadcastwell.com/answer-repair). Keep the question and source receipt with the requested change.

[Our answer-study method, v1.1.](https://broadcastwell.com/methodology)

Prepared by the Broadcastwell team.

Page owner: Rohan Iyer, AI Engineer. Corrections: hello@broadcastwell.com
