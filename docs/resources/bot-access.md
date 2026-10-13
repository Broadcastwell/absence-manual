---
title: "Bot access per engine"
headline: "Bot access per engine: what the check can establish"
description: "How Broadcastwell checks robots rules, server responses and returned HTML, with separate policy notes and explicit limits."
page_class: note
schema_type: Article
date_published: "2026-10-13T00:00:00+00:00"
date_modified: "2026-10-13T00:00:00+00:00"
---

# Bot access per engine

The bot access check reports a state for ChatGPT, Claude, Perplexity, Google AI Overviews and Google AI Mode. It checks robots.txt, llms.txt, the homepage and up to two pages identified by the findings. No engine is asked a question.

## What the requests show

Requests use configured identities based on the providers' documented search and user fetcher tokens and examples, with the source date recorded. They come from our servers, not the providers' verified addresses. A firewall may therefore respond differently to a provider's own request.

Robots rules use the applicable groups and longest matching rule, with Allow winning a tie. Unknown or incomplete checks remain **Unknown**. An issue count of zero does not turn an Unknown result into Reachable.

Google AI Overviews and Google AI Mode use the Googlebot access result. `Google-Extended` is reported separately as a robots policy token; it is not an HTTP fetcher and does not decide the Google Search access result. Training crawler policies are also reported separately.

## What the HTML check cannot show

The main text check examines the returned HTML. Very little visible text together with signs of content loaded by scripts can be flagged for review. It is an HTML heuristic, not a browser render or proof of what a provider ultimately reads. Google rendering limits are noted rather than treated as the same finding for every engine.

Pages intentionally left out of this check, such as sign in, account and legal pages, are listed separately and excluded from the issue count. Reachability does not establish indexing, citation or inclusion.

## Reading a result

An existing stored check carries its date and is shown with the findings. Reading a findings page does not run a new check. A missing check is not evidence that the site is reachable.

The [Kalvenor bot access sample](https://app.broadcastwell.com/sample/bot-access) uses fictional **SAMPLE DATA**. It illustrates the states and policy notes; it is not a customer check or a visit by a provider's own crawler.

[Every figure comes from the published method, v1.1.](https://broadcastwell.com/methodology)
