---
title: How do AI search crawlers differ from AI training crawlers?
headline: How do AI search crawlers differ from AI training crawlers?
description: Choose crawler access by purpose. Housecall Pro had 43 own-domain citations
  in 150 answers; those outputs do not reveal training access.
page_class: page
schema_type: Article
date_published: '2026-10-29T00:07:16+00:00'
date_modified: '2026-10-29T00:07:16+00:00'
hide:
- navigation
library_cluster: fixes
library_owner: Rohan Iyer, AI Engineer
library_subtopic: Crawler purposes
library_order: 76
demand_source: people-also-ask
demand_evidence: LB-Q0642, private demand receipt dated 2026-10-28
also_asked_as:
- What kinds of AI crawlers should a site owner distinguish?
is_based_on: https://doi.org/10.5281/zenodo.22907695
---

# How do AI search crawlers differ from AI training crawlers?

Search crawlers support finding web information, while training crawlers collect material for model development; some providers also distinguish a user-requested page visit. Choose access for each purpose separately. In answers captured on 22 September 2026, Housecall Pro's own domain was cited in 43 of 150 answers. That output count does not reveal which training crawler, if any, fetched its pages.

## What we measured

**Measured.** The [September Index method](https://doi.org/10.5281/zenodo.22907695) covered ten field service questions, three scheduled answers on ChatGPT, Claude, Perplexity, Google AI Overviews and Google AI Mode. Housecall Pro's own-domain citation rate was 28.7 percent, with a descriptive Wilson 95 percent interval of 22.0 to 36.4 percent. The event required its name and a supporting citation to its domain in the same answer. No crawler-request or training-use event was collected.

**Reported.** [Anthropic's bot guide](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler), read 28 October 2026, distinguishes ClaudeBot for potential training collection, Claude-SearchBot for search and Claude-User for user-directed access. These are provider-specific purposes, rather than three names for an identical request.

Google's [AI feature guidance](https://developers.google.com/search/docs/appearance/ai-features), read the same date, assigns Search crawl access to Googlebot. It points separately to Google-Extended for training and grounding in some other Google systems. Google Search's AI features therefore should not be treated as a training-only access decision.

[Every figure comes from the published method, v1.1.](https://broadcastwell.com/methodology)

## What this means for you

**Reasoned.** Write the policy you intend before selecting a bot token. A publisher might allow public research to be found in search while making a separate choice about model development. Record those choices in distinct rows so the delivered rules can be checked against them.

Keep a user-directed fetch separate too. It describes access initiated for a person's request, not a general promise that a page will appear in future search answers. Use the provider's current documentation to identify the purpose and supported control rather than guessing from a familiar name.

Then verify the right event. A served robots file demonstrates the instruction you published. A request log can show a recorded request under its identification rules. An answer citation shows a linked source at the time of that answer. None supplies all the other evidence.

When reporting to a buyer, leave the output count beside the output label. The 43 Housecall Pro observations should not become a training-access score or a claim that a particular permission caused citation.

- **For a site owner:** approve search, training and user-directed access as separate choices.
- **For a developer:** retain the documented purpose beside each configured token.

## Also asked as

What kinds of AI crawlers should a site owner distinguish?

## Related

- [Housecall Pro citation record](https://index.broadcastwell.com/vendors/housecall-pro/field-service-management/)
- [Broader bot-access guide](../../resources/bot-access.md)
- [Robots rules and access](how-should-i-use-robots-txt-to-control-ai-crawler-access.md)
- [Google Search control boundary](../google-ai/does-google-extended-control-ai-overview-or-ai-mode-visibility.md)

## Next step

Use the [Free 10-question check (one engine)](https://audit.broadcastwell.com/). No email is needed; runs are limited per network and per day, and by the site's daily allowance. Keep its source citation separate from your access-policy record.

For one factual error on an approved public source, [Fix one answer, $490](https://broadcastwell.com/answer-repair) addresses the page claim rather than a training-policy preference.

Claiming or correcting a vendor record is free and never depends on a purchase.

Prepared by the Broadcastwell team.

Page owner: Rohan Iyer, AI Engineer. Corrections: hello@broadcastwell.com
