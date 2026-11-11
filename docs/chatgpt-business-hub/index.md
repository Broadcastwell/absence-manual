---
title: How do you claim your business in ChatGPT?
headline: How do you claim your business in ChatGPT?
description: 'Reported on 6 November 2026 and unreleased on 8 November 2026: what the ChatGPT Business Hub shows, how ownership may be verified, and the checks to make first.'
page_class: page
schema_type: Article
date_published: '2026-11-09T00:00:00+00:00'
date_modified: '2026-11-11T07:30:00Z'
template: business-hub.html
faq:
- question: Can you claim your business in ChatGPT today?
  answer: No. The tool was reported on 6 November 2026 and was still unreleased when we checked on 8 November 2026, with no OpenAI launch page or verification method. Our watch page records each check and its date.
- question: When will the ChatGPT Business Hub launch?
  answer: OpenAI has published no date, and we do not forecast one. The reports say its first steps were seen as early as August 2026 and describe the feature as a work in progress.
- question: How will a business verify ownership?
  answer: OpenAI has not said. The report gives connecting a Shopify store as an example, and domain control is the other route we expect because search webmaster tools commonly use it. Both are expectations, not published requirements.
- question: Will the Hub show which prompts mention your business?
  answer: Not according to the 6 November 2026 reports. They describe daily impressions and clicks with no prompt data, no user data and no competitor benchmark or ranking. Prompt measurement shows which buyer questions name you and who is named instead.
- question: Do you need llms.txt or a business facts file to appear in ChatGPT?
  answer: Neither is a published requirement. Both put your current facts in one dated place that an agent, or a person checking a claim, can read. We treat them as readiness work, not as a ranking signal.
- question: Is readiness sold separately?
  answer: Yes. The ChatGPT Business Hub Readiness Setup is sold on its own at $1,820 once. Readiness is also part of the Fix Sprint, Care and Program, as our offer section on this page lists.
---

# How do you claim your business in ChatGPT?

You cannot claim your business in ChatGPT yet. The ChatGPT Business Hub was reported on 6 November 2026 and was still unreleased when we checked on 8 November 2026, with no OpenAI launch page and no verification method. The reports compare it to a ChatGPT Search Console or ChatGPT webmaster tools: a place where a verified business sees how often it appears in answers and keeps its information current. You can prepare for it now.

Updated 11 November 2026.

## What was reported on 6 November 2026

Two sources describe the tool, both published on 6 November 2026. Juozas Kaziukėnas wrote on LinkedIn that ChatGPT is building an analytics tool for businesses, shared a screenshot of a banner reading "Claim your business in ChatGPT", and said he had seen its first steps as early as August 2026. Barry Schwartz reported the post the same day on Search Engine Roundtable. Both describe the tool as part of a larger Business Hub feature, available to businesses that have verified their ownership, with connecting a Shopify store given as the example.

Nothing in either source comes from OpenAI. We treat every detail below as reported, and we will correct this page when OpenAI publishes its own description.

## What the tool will show, and what it will not

The report lists four things the tool shows and four it does not.

| What | Per the 6 November 2026 report |
| --- | --- |
| Impressions: how often the business appears in ChatGPT answers, counted daily and shown as a chart | Shown |
| Clicks from those answers to the business website, counted daily | Shown |
| A place to add products and keep business information current | Shown |
| A business agent that answers customer questions with context the business controls | Shown |
| The prompts behind an impression or a click | Not shown |
| Data about the people who asked | Not shown |
| A competitor benchmark or ranking | Not shown |
| Why a count rose or fell | Not shown |

## Expected verification routes

OpenAI has not published how a business proves ownership. We expect two routes and label both as expected until OpenAI says otherwise.

| Route | Status | Basis |
| --- | --- | --- |
| Commerce connection: connecting the store you sell from | Expected | The report gives connecting a Shopify store as its example |
| Domain control: proving you control the website's domain, for example with a DNS record or a file at the site root | Expected | Common practice for search webmaster tools |

The ChatGPT Business Hub is not ChatGPT Business, which is OpenAI's subscription plan, and it is not ChatGPT Enterprise or ChatGPT ads.

## How to get your business listed in ChatGPT: the readiness checklist

No checklist makes ChatGPT name a business, and none of these ten items is a published OpenAI requirement. They cover what the report says the Hub asks for, which is verified ownership, current business information and products, plus what crawlers and agents read today. Our free check links each of its results to the matching item below.

### Ownership verification {#ownership-verification}

Know who controls your domain's DNS and its web root, and who holds the owner login for any store. Write down the legal name and the domain you would verify, then confirm the same pair appears on your site, in your structured data and in your main directory listings.

### Organization structured data {#organization-data}

Your home page carries Organization JSON-LD with legal name, brand name, URL, logo, address, telephone, email and sameAs links to the profiles you control. Every value matches what the page shows and what your business facts file states.

### Product and Offer structured data {#product-data}

Each product or service page carries Product and Offer markup with the price, the currency and the unit or billing period a buyer sees on that page. When a price is not public, leave it out of the markup rather than estimating one.

### llms.txt {#llms-txt}

A short llms.txt at your site root lists your key pages and links your business facts file. Neither report says the Hub reads llms.txt, and Google says its AI search features need no special text file, as our answer on [what Google's guidance says about llms.txt](../answers/fixes/what-does-google-s-guidance-say-about-llms-txt.md) records. We still include it, because it gives any agent a dated map of your facts at little cost.

### Crawler policy {#crawler-policy}

Your robots.txt allows OAI-SearchBot, the crawler [OpenAI documents](https://developers.openai.com/api/docs/bots) for ChatGPT search results. GPTBot, its training crawler, is a separate setting, so decide it on its own terms. Our answer on [whether allowing GPTBot makes a site appear in ChatGPT search](../answers/chatgpt/does-allowing-gptbot-make-a-site-appear-in-chatgpt-search.md) explains the difference.

### Sitemap {#sitemap}

An XML sitemap lists every canonical page you want found, each with a truthful lastmod date, and your robots.txt points to it. Product, pricing, contact and policy pages belong in it.

### Name consistency {#name-consistency}

Use one legal name, one brand spelling, one address format and one phone number across your site, structured data, store, directories and social profiles. If a claim compares your store or your domain with your business name, there is then nothing to reconcile.

### Commerce connection {#commerce-connection}

If you sell through a store platform, confirm who holds its owner account, that the store name and domain match your business name, and that the products and prices in the store match your site. This is the route the report names. If you have no store, domain control is the route to prepare.

### Business facts file {#business-facts-file}

Publish a business facts file at /business-facts.json: a dated JSON statement of your identity, contact details, offers with prices, and policies. Our [business facts file standard](business-facts-file.md) gives the fields, a validator rule list, a JSON Schema and two examples.

### Context pack {#context-pack}

Write down the questions buyers ask and the answers you approve, each with its source page, owner, review date and expiry. The report's phrase for the business agent is "context you control", and our [context pack format](context-pack.md) is a way to have that context reviewed before anyone asks for it.

## What our ChatGPT Business Hub Readiness work includes {#readiness-offer}

1. Ownership verification readiness: domain control confirmed; business identity consistent across the site, structured data and directories; a commerce connection checked where a store exists.
2. Business information pack: Organization, Product and Offer structured data on your site; a business facts file at /business-facts.json linked from llms.txt; products, prices and contact facts current.
3. Business-agent context pack: the questions buyers ask, the approved answers, policies and facts in one reviewed document you control, in the format our connectors already serve.
4. Mention and click baseline: our dated measurement of how your business is named today on ChatGPT, Claude, Perplexity, Google AI Overviews and Google AI Mode, with receipts, so the Hub's first-party numbers can be reconciled later. It uses the measurement runs included in your purchase.
5. Launch-day claim: we watch for availability and claim your business on the day OpenAI opens the tool to it.
6. Reconciliation report: Hub counts beside our receipts, every month.

On 9 November 2026 we checked the 40 companies in our competitor review; 0 of them published a readiness program for this tool.

Parts 1 to 4 are included in the [Fix Sprint](https://broadcastwell.com/fix-sprint) ($3,900 once). Parts 1 to 6 are included in Care ($490 a month) and Program ($5,500 a month), both described on our [pricing page](https://broadcastwell.com/pricing). We also offer the [ChatGPT Business Hub Readiness Setup](https://app.broadcastwell.com/offers/chatgpt-business-hub-readiness-setup) on its own at $1,820 once, for a business that wants to prepare without buying the Fix Sprint, Care or Program.

<a id="clients"></a>
Our current clients Vantaa Tax, Neurvalis and Valren Atelier are enrolled in this program; their readiness work is under way, and we claim each of them on the first day OpenAI opens the tool to them.

## Why measure prompts too

As reported, the Hub counts impressions and clicks inside ChatGPT. It will not show which prompts produced them, who ChatGPT recommended instead of you, what other engines say, or why a count moved. That is the part our measurement covers. We ask fixed buyer questions on ChatGPT, Claude, Perplexity, Google AI Overviews and Google AI Mode, record who is named instead of you, keep the receipt for every answer and publish our [method](https://broadcastwell.com/methodology).

The trade-off runs both ways. Our panel samples the questions agreed with you, while the Hub, as reported, counts appearances across ChatGPT conversations. Neither replaces the other, so our [reconciliation report](reconciliation-report.md) puts the two records side by side and explains each difference.

The business agent in the report is close to the vendor-controlled answer connectors we have published since October 2026: the [fictional Kalvenor connector](https://app.broadcastwell.com/mcp/vendor/kalvenor) (Sample data, fictional company) and the [Vendor Facts File standard](https://app.broadcastwell.com/standard/vendor-facts) it answers from.

## Check your site for free

Our [ChatGPT Business Hub readiness check](https://app.broadcastwell.com/tools/chatgpt-business-hub-readiness) is free. It checks your public site against the ten items above and links each result to its section on this page. For availability, our [watch page](watch.md) lists what we check and the latest result.

## Questions

### Can you claim your business in ChatGPT today?

No. The tool was reported on 6 November 2026 and was still unreleased when we checked on 8 November 2026, with no OpenAI launch page or verification method. Our [watch page](watch.md) records each check and its date.

### When will the ChatGPT Business Hub launch?

OpenAI has published no date, and we do not forecast one. The reports say its first steps were seen as early as August 2026 and describe the feature as a work in progress.

### How will a business verify ownership?

OpenAI has not said. The report gives connecting a Shopify store as an example, and domain control is the other route we expect because search webmaster tools commonly use it. Both are expectations, not published requirements.

### Will the Hub show which prompts mention your business?

Not according to the 6 November 2026 reports. They describe daily impressions and clicks with no prompt data, no user data and no competitor benchmark or ranking. Prompt measurement shows which buyer questions name you and who is named instead.

### Do you need llms.txt or a business facts file to appear in ChatGPT?

Neither is a published requirement. Both put your current facts in one dated place that an agent, or a person checking a claim, can read. We treat them as readiness work, not as a ranking signal.

### Is readiness sold separately?

Yes. The [ChatGPT Business Hub Readiness Setup](https://app.broadcastwell.com/offers/chatgpt-business-hub-readiness-setup) is sold on its own at $1,820 once. Readiness is also part of the Fix Sprint, Care and Program, as our offer section on this page lists.

## Related guides

- [What belongs in a business facts file for ChatGPT?](business-facts-file.md)
- [What goes in a context pack for a business agent?](context-pack.md)
- [Is the ChatGPT Business Hub available yet?](watch.md)
- [How do you reconcile ChatGPT Hub counts with receipts?](reconciliation-report.md)
- [Why does ChatGPT not mention us?](../why-does-chatgpt-not-mention-us.md)
- [What belongs in a public vendor facts file?](../vendor-facts.md)

## Sources

- Barry Schwartz, [OpenAI Working On ChatGPT Tools For Business For Analytics & Citations](https://www.seroundtable.com/chatgpt-tools-for-business-42476.html), Search Engine Roundtable, 6 November 2026.
- Juozas Kaziukėnas, [LinkedIn post on ChatGPT's business analytics tool](https://www.linkedin.com/posts/juozas_chatgpt-is-building-an-analytics-tool-to-share-7524436371613118464-E3Zf/), 6 November 2026.
- OpenAI, [Overview of OpenAI crawlers](https://developers.openai.com/api/docs/bots), developer documentation.
- Broadcastwell, [Method v1.1](https://broadcastwell.com/methodology), first published 25 August 2026.
