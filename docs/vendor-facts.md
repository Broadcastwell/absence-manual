---
title: "Vendor Facts File v1"
headline: "Vendor Facts File v1: the facts a vendor states about itself"
description: "An open JSON schema for vendor facts, with a complete fictional example, validation instructions and CC BY 4.0 reuse. A facts file is not a ranking signal."
page_class: page
schema_type: Article
date_published: "2026-10-06T00:00:00+00:00"
date_modified: "2026-10-06T00:00:00+00:00"
---

# Vendor Facts File v1

One JSON document a vendor hosts at `https://<domain>/vendor-facts.json` so that any assistant, agent or crawler can read the facts the vendor itself states, with a date. It is not a ranking signal. It exists so an agent that asks "what does this cost" or "who is this for" can read the vendor's own answer instead of guessing.

## The rules

Every value must be readable on the vendor's own site. A vendor may host the file itself or publish it through Ask &lt;Vendor&gt;. No field is scored, ranked or weighted by Broadcastwell. The schema is CC BY 4.0 with attribution to Broadcastwell.

A facts file is a statement by the vendor, not a measurement by us. We recommend a facts file only when a recorded agent task shows a factual access problem it can address. It does not promise inclusion, position, leads or revenue.

The [canonical JSON Schema](https://app.broadcastwell.com/standard/vendor-facts.schema.json) uses JSON Schema 2020-12. The [standard and interactive validator](https://app.broadcastwell.com/standard/vendor-facts) are public. Reuse is under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

## Fields

All values are strings unless their type is stated below. Required fields are marked Yes.

| Field | Required | Meaning |
| --- | --- | --- |
| facts_version | Yes | Version string, currently "1". |
| updated | Yes | Real ISO calendar date, YYYY-MM-DD. |
| company | Yes | Legal or trading name. |
| domain | Yes | Canonical domain. |
| category | Yes | Category in the buyer's words. |
| one_sentence | Yes | What the product is. |
| for | Yes | Array of company sizes, roles or industries served. |
| not_for | No | Array describing unsuitable use cases. |
| pricing | Yes | Object containing public, url and plans. public is a boolean. Each plans entry contains name, price, billing and an includes array. |
| integrations | No | Array of objects containing name and url. |
| api_docs_url | No | Public API documentation URL. |
| compliance | No | Array containing name, status and url. status is stated, certified or in progress. Never list a certification the vendor does not state on its own site. |
| demo_url | Yes | Public empty demo path. |
| contact_url | Yes | Public contact path. |
| support_url | No | Public support URL. |
| status_url | No | Public status URL. |
| facts_url | Yes | This facts file's own URL. |
| index_record_url | No | The vendor's Absence Index record, if any. |

When pricing is not public, use public: false and an empty plans array. Do not infer a price or a certification. URLs use HTTPS.

## SAMPLE DATA: Kalvenor Systems

Kalvenor is fictional. Every example fact below is illustrative and describes no real company. Example domains do not represent a live vendor site.

```json
{
  "facts_version": "1",
  "updated": "2026-10-06",
  "company": "Kalvenor Systems (SAMPLE DATA)",
  "domain": "kalvenor.example",
  "category": "field service management software",
  "one_sentence": "SAMPLE DATA. Kalvenor is a fictional field service platform used only to illustrate this format.",
  "for": [
    "SAMPLE DATA: dispatch teams at fictional service companies"
  ],
  "not_for": [
    "SAMPLE DATA: organizations seeking a real vendor"
  ],
  "pricing": {
    "public": true,
    "url": "https://kalvenor.example/pricing",
    "plans": [
      {
        "name": "Illustrative plan",
        "price": "SAMPLE DATA: $99",
        "billing": "per month, fictional",
        "includes": [
          "Illustrative dispatch board"
        ]
      }
    ]
  },
  "integrations": [
    {
      "name": "SAMPLE DATA: illustrative calendar",
      "url": "https://kalvenor.example/integrations"
    }
  ],
  "api_docs_url": "https://kalvenor.example/docs/api",
  "compliance": [],
  "demo_url": "https://kalvenor.example/demo",
  "contact_url": "https://kalvenor.example/contact",
  "support_url": "https://kalvenor.example/support",
  "status_url": "https://kalvenor.example/status",
  "facts_url": "https://app.broadcastwell.com/vendors/kalvenor/facts.json"
}
```

## Validate and publish

Use the public validator at [Vendor Facts File v1](https://app.broadcastwell.com/standard/vendor-facts), or send a JSON document to `POST https://app.broadcastwell.com/api/v1/facts/validate`. It returns format errors and stores nothing. Format validation does not verify the truth of a claim.

A client may host its own copy at `https://<domain>/vendor-facts.json`. Ask &lt;Vendor&gt; reads that hosted copy when the client prefers and approves it. Alternatively, the approved file can be served at `https://app.broadcastwell.com/vendors/<slug>/facts.json`.

The read-only connector at `https://app.broadcastwell.com/mcp/vendor/<slug>` exposes six tools: get_company, get_pricing, get_fit, get_integrations, get_compliance and get_links. It answers from the approved file and has no write tool. The client may withdraw the approved facts. The separate account connector keeps its fifteen tools.

Try [Ask Kalvenor, the fictional sample](https://app.broadcastwell.com/connect#ask-a-vendor). Its six responses are marked SAMPLE DATA.
