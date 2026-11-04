---
title: Does Anthropic crawl data from the web, and how can site owners block the crawler?
headline: Does Anthropic crawl data from the web, and how can site owners block the crawler?
description: Anthropic documents three separate web robots; Claude named Buildertrend in 21 of 30 construction answers captured on 22 September 2026.
page_class: page
schema_type: Article
date_published: '2026-10-29T15:18:56+00:00'
date_modified: "2026-11-04T01:03:17.612597+00:00"
hide:
- navigation
library_cluster: claude
library_owner: Vikram Patel, AI Architect
library_subtopic: Crawler controls
library_order: 160
demand_source: manual-faq
demand_evidence: LB-Q0275, private demand receipt dated 2026-10-28
also_asked_as:
- Does Anthropic crawl data from the web, and how can site owners block the crawler?
is_based_on: https://doi.org/10.5281/zenodo.22907695
---

# Does Anthropic crawl data from the web, and how can site owners block the crawler?

On 29 October 2026, Anthropic's published crawler guide describes separate robots for training collection, search and user-directed retrieval, with robots.txt controls for each. Choose the control that matches your purpose. In our construction capture dated 22 September 2026, Claude named Buildertrend in 21 of 30 valid answers.

Observed answers on stated dates, not a ranking.

In our [robots.txt](https://docs.broadcastwell.com/robots.txt) snapshot published on 3 November 2026, `ClaudeBot`, `Claude-SearchBot` and `Claude-User` each have their own `Allow: /` group. The identical path rule does not make the named purposes interchangeable. If a publisher chooses a different training policy, it must identify the corresponding group rather than treating this file as one company-wide permission. This is a reading of our declared policy, not an observed Anthropic request or a test of blocking.

## What we measured

**Reported.** [Anthropic's crawler guide](https://support.anthropic.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler), read on 29 October 2026, distinguishes ClaudeBot, Claude-SearchBot and Claude-User. It describes ClaudeBot as collecting material that could contribute to training, Claude-SearchBot as supporting search, and Claude-User as retrieving content at a user's direction. The guide gives robots.txt instructions for controlling each robot on the relevant site or subdomain.

**Measured.** Buildertrend's 21 naming appearances come from the Claude cells in the [September Index](https://doi.org/10.5281/zenodo.22907695): ten construction buyer questions, three runs per question, 30 retained Claude answers. Other engines have their own cells and are outside this figure.

The answer count does not measure the effect of blocking any of Anthropic's robots.

### One retained answer

In one retained [answer record](https://zenodo.org/records/22907695/files/answers-2026-09.jsonl?download=1), Claude answered the general contractor (GC) question “best construction software for a small GC that needs estimating and scheduling without Procore complexity” on 22 September 2026, run 1, with the fragment “Projul, JobTread, and Buildertrend”. This historical wording is an answer observation, not independent verification of the product claim or an explanation of the aggregate count.

## What this means for you

**Reasoned.** Pick the purpose first. If your decision concerns future training collection, read the ClaudeBot rule rather than treating Claude-SearchBot as another spelling of it. Anthropic gives the robots different jobs, so a single company-level instruction such as “block Claude” leaves the intended access unclear.

If you want company information available to user-directed retrieval, inspect the Claude-User instruction separately. The Buildertrend count describes answers observed in September; it is not a record of whether Claude-User requested Buildertrend's pages. Keep the access setting and the answer observation as separate items in your notes.

For server load, Anthropic also documents Crawl-delay separately from its full-site disallow example. Read the exact option before choosing between slowing a robot and excluding it. Apply the decision to the subdomain whose content you mean, as the published guide instructs.

## Also asked as

Does Anthropic crawl data from the web, and how can site owners block the crawler?

## Related





- [Anthropic robot purposes and controls](https://support.anthropic.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
- [Bot access in the Manual](../../resources/bot-access.md)
- [Claude construction observations](which-construction-software-does-claude-recommend.md)
- [The Manual on search retrieval and crawler roles](../../who-gets-cited.md)
- [More claude answers](https://docs.broadcastwell.com/answers/claude/)
- [Construction project management records in the Index](https://index.broadcastwell.com/categories/construction-project-management/)

## Next step

[Free 10-question check (one engine)](https://audit.broadcastwell.com/). No email is needed; runs are limited per network and per day, and by the site's daily allowance.

Claiming or correcting a vendor record is free and never depends on a purchase.

[Every figure comes from the published method, v1.1.](https://broadcastwell.com/methodology)

Answer Repair: [$490](https://broadcastwell.com/answer-repair).

Prepared by the Broadcastwell team.

Page owner: Vikram Patel, AI Architect. Corrections: hello@broadcastwell.com
