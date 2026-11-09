---
title: What belongs in a business facts file for ChatGPT?
headline: What belongs in a business facts file for ChatGPT?
description: A business facts file is a dated JSON statement of identity, contact details, priced offers and policies at /business-facts.json, built on Vendor Facts File v1.
page_class: page
schema_type: TechArticle
date_published: '2026-11-09T00:00:00+00:00'
date_modified: '2026-11-09T00:00:00+00:00'
template: business-hub.html
---

# What belongs in a business facts file for ChatGPT?

A business facts file is one JSON document at /business-facts.json on your own domain. It states your legal name, brand name, canonical domain, profiles, address, contact details, offers with prices, units and currency, and policies, plus who last reviewed it and when. It answers the reported ChatGPT Business Hub need to keep business information current, and it is a profile of our Vendor Facts File v1.

Updated 9 November 2026.

## How it relates to Vendor Facts File v1

[Vendor Facts File v1](../vendor-facts.md) tells an agent what a software vendor sells and who it is for. A business profile needs more: a legal identity, a postal address, prices a machine can read, and the policies a customer agrees to. This profile adds those fields and keeps the v1 rules as they are. Every value must be readable on your own site. The file is your statement, not our measurement, and no field is scored or ranked. Dates are ISO calendar dates and every URL uses HTTPS.

Four top-level names keep their v1 meaning: domain, category, one_sentence and facts_url. If you publish both files, vendor_facts_url points from this file to the other and the shared values must agree. Two files can drift apart, which is the cost of this design, so review them on the same day and keep last_reviewed equal to the v1 updated date.

## Required fields

| Field | Meaning |
| --- | --- |
| business_facts_version | "1". |
| profile_of | The Vendor Facts File v1 schema URL, https://app.broadcastwell.com/standard/vendor-facts.schema.json. |
| legal_name | The registered name, as it appears on your terms or invoices. |
| brand_name | The name customers see. |
| domain | Canonical domain, as in Vendor Facts File v1. |
| same_as | Array of HTTPS URLs for profiles you control on other sites, such as LinkedIn or GitHub. It may be empty. |
| address | Object with street_address, locality, postal_code and country, a two-letter ISO 3166-1 code. region is optional. |
| contact | Object with email and contact_url, and optionally phone in international format and other_emails, each with a purpose. |
| offers | Array of at least one offer, each with name, url and price. A published price has amount, a decimal string with no thousands separator, currency, an ISO 4217 code, and unit, such as once, a month or per client report. An unpublished price sets published to false and gives price_url, the page where a buyer asks. |
| policies | Array of at least one policy, each with name and an HTTPS url: terms, refunds, privacy, security. |
| last_reviewed | ISO date of the last full review. |
| reviewer | The person or team accountable for that review. |
| facts_url | This file's own URL, as in Vendor Facts File v1. |

## Optional fields

| Field | Meaning |
| --- | --- |
| category, one_sentence | As in Vendor Facts File v1. |
| products | Array of name, url and description for things you sell, as distinct from the offers that price them. |
| commerce_connection | Object with platform and store_url for the store you would connect to verify ownership. |
| vendor_facts_url | Your Vendor Facts File v1, if you publish one. |
| llms_txt_url | The llms.txt that links this file. |
| sample, fictional, label | Used together on any example file: true, true, and a label that starts with SAMPLE DATA. |

## Where it lives

Serve the file at https://&lt;domain&gt;/business-facts.json as application/json, and link it from your llms.txt with one line, for example `- [Business facts](https://example.com/business-facts.json): legal name, contact, offers and policies`. A subdomain you control is acceptable when the main site cannot serve a JSON file at its root, and facts_url then names that subdomain.

Our own file uses that allowance. It is served at https://docs.broadcastwell.com/business-facts.json and linked from https://docs.broadcastwell.com/llms.txt. Keep the same values in your [Organization](index.md#organization-data) and [Offer](index.md#product-data) structured data, so a reader who checks one finds the other in agreement.

## Validator rules

A file meets the standard when all twelve rules hold.

1. It parses as one UTF-8 JSON object with no repeated keys.
2. It validates against the JSON Schema below.
3. business_facts_version is "1" and profile_of names the Vendor Facts File v1 schema.
4. last_reviewed is a real calendar date and is not in the future.
5. Every URL starts with https://.
6. facts_url is on domain or one of its subdomains, at the path /business-facts.json.
7. No same_as entry is on domain itself; those links point to profiles elsewhere.
8. Every published price has an amount, a three-letter currency code and a unit. An unpublished price says published is false and carries no amount.
9. country is a two-letter code, and phone, when present, starts with a plus sign and a country code.
10. Offer names are unique within the file.
11. A file with sample set to true also sets fictional to true and has a label that starts with SAMPLE DATA.
12. A last_reviewed date more than 90 days old is reported as stale: the file still parses, but it no longer meets the freshness rule.

Passing these rules shows the file is well formed. It does not show that any statement in it is true, which is why the reviewer field is required.

## JSON Schema

The [schema](https://docs.broadcastwell.com/business-facts.schema.json) uses JSON Schema 2020-12 and is reusable under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) with attribution to Broadcastwell. Rules 4, 6, 7, 10, 11 and 12 compare values with each other or with the date, so they are checked outside the schema. Both examples below pass all twelve.

## Worked example: Broadcastwell

Our file states only facts printed on our public pages: our legal name, address and contact details, the six prices on our [pricing page](https://broadcastwell.com/pricing), our policy pages, and the profiles listed in the Organization structured data on broadcastwell.com. Download it at [business-facts.json](https://docs.broadcastwell.com/business-facts.json).

```json
{
  "business_facts_version": "1",
  "profile_of": "https://app.broadcastwell.com/standard/vendor-facts.schema.json",
  "legal_name": "Broadcastwell LLC",
  "brand_name": "Broadcastwell",
  "domain": "broadcastwell.com",
  "same_as": [
    "https://www.linkedin.com/company/broadcastwell",
    "https://github.com/Broadcastwell",
    "https://broadcastwell.substack.com/",
    "https://www.youtube.com/@Broadcastwell",
    "https://www.instagram.com/broadcastwell/"
  ],
  "address": {
    "street_address": "517 E Kirkwood Ave",
    "locality": "Bloomington",
    "region": "IN",
    "postal_code": "47408",
    "country": "US"
  },
  "contact": {
    "email": "hello@broadcastwell.com",
    "phone": "+1-812-345-7272",
    "contact_url": "https://broadcastwell.com/contact"
  },
  "offers": [
    {
      "name": "Answer Repair",
      "url": "https://broadcastwell.com/answer-repair",
      "price": {
        "published": true,
        "amount": "490",
        "currency": "USD",
        "unit": "once"
      }
    }
  ],
  "policies": [
    {
      "name": "Terms",
      "url": "https://broadcastwell.com/terms"
    }
  ],
  "llms_txt_url": "https://docs.broadcastwell.com/llms.txt",
  "last_reviewed": "2026-11-09",
  "reviewer": "Broadcastwell team",
  "facts_url": "https://docs.broadcastwell.com/business-facts.json"
}
```

The excerpt above shows one of our six offers and one of our five policies. The downloadable file carries all of them.

## Second example: Kalvenor, a fictional company

Kalvenor Systems is fictional, and its file says so in its own sample, fictional and label fields. It shows the branch our own file does not need: an offer whose price is not published, a product listed apart from its offer, and a commerce connection. Its domain, category and one_sentence match the [Kalvenor vendor facts file](https://app.broadcastwell.com/vendors/kalvenor/facts.json). Download it at [kalvenor-business-facts.json](https://docs.broadcastwell.com/examples/kalvenor-business-facts.json).

```json
"offers": [
  {
    "name": "SAMPLE DATA: Illustrative plan",
    "url": "https://kalvenor.example/pricing",
    "price": {
      "published": false,
      "price_url": "https://kalvenor.example/pricing"
    }
  }
]
```

## Related guides

- [How do you claim your business in ChatGPT?](index.md), our explainer and readiness checklist
- [What goes in a context pack for a business agent?](context-pack.md)
- [Is the ChatGPT Business Hub available yet?](watch.md)
- [How do you reconcile ChatGPT Hub counts with receipts?](reconciliation-report.md)

## Sources

- Broadcastwell, [Vendor Facts File v1 standard and JSON Schema](https://app.broadcastwell.com/standard/vendor-facts), published 6 October 2026.
- Broadcastwell, Organization structured data on [broadcastwell.com](https://broadcastwell.com/), read 9 November 2026 for the same_as list.
- JSON Schema, [Draft 2020-12](https://json-schema.org/draft/2020-12) specification.
- Barry Schwartz, [Search Engine Roundtable](https://www.seroundtable.com/chatgpt-tools-for-business-42476.html), 6 November 2026, for the reported "keep business information current" feature.
