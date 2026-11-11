---
title: What goes in a context pack for a business agent?
headline: What goes in a context pack for a business agent?
description: A context pack holds buyer questions, approved answers, policies and facts a business agent may use, each answer with its source, owner, review date and expiry.
page_class: page
schema_type: TechArticle
date_published: '2026-11-09T00:00:00+00:00'
date_modified: '2026-11-11T07:30:00Z'
template: business-hub.html
---

# What goes in a context pack for a business agent?

A context pack is one reviewed JSON document holding the questions buyers ask, the answers your business approves, your policies and your key facts. Every answer carries its source page, an owner, a review date and an expiry date. The reported ChatGPT Business Hub includes a business agent that answers customer questions with context the business controls, and this pack is a format for that context.

Updated 11 November 2026.

## Why one reviewed document

An agent answering for your business can only be as current as what it is given, and that includes last quarter's price. Keeping every approved answer in one file, each tied to the public page it came from, makes the review a single job: open the pack, open each source, confirm they still agree, move the dates. The cost is discipline. A pack nobody reviews goes stale on a schedule you can read in its own expiry fields, which is better than a stale answer nobody can date.

## The six groups

Answers sit in the same six groups our read-only vendor connector serves: company, pricing, fit, integrations, compliance and links. The [fictional Kalvenor connector](https://app.broadcastwell.com/mcp/vendor/kalvenor) (Sample data, fictional company) answers from those groups today. One approved pack can feed a connector now and give you reviewed text to enter wherever OpenAI's business agent takes its context, if OpenAI publishes how it does.

| Group | What belongs in it |
| --- | --- |
| company | What the business is and does, in its own words. |
| pricing | Prices with their units, credits and refund terms. |
| fit | Who the offer is for, who it is not for, and what it does not promise. |
| integrations | What connects to what, as the business states it. |
| compliance | Certifications claimed, certifications not claimed, data handling. |
| links | Where the method, demo, contact and policy pages are. |

## Pack fields

| Field | Required | Meaning |
| --- | --- | --- |
| context_pack_version | Yes | "1". |
| business | Yes | Legal name of the business. |
| domain | Yes | Canonical domain. |
| owner | Yes | The person or team who approves answers. |
| facts_url | Yes | The business facts file this pack agrees with. |
| rules | Yes | One sentence on where answers come from and what happens at expiry. |
| facts | Yes | Short approved statements, each with source_url. |
| policies | Yes | Name and HTTPS URL of each policy an answer may cite. |
| groups | Yes | The six groups above, each an array of answers. |
| sample, fictional, label | On examples | true, true, and a label that starts with SAMPLE DATA. |

## Answer fields

| Field | Required | Meaning |
| --- | --- | --- |
| id | Yes | Stable identifier, unique within the pack. |
| question | Yes | The buyer's question in the buyer's words. |
| answer | Yes | The approved answer, using only what the source page says. |
| source_url | Yes | The public HTTPS page the answer comes from. |
| reviewed | Yes | ISO date the owner last confirmed answer and source agree. |
| expires | Yes | ISO date after which the answer is withheld until reviewed again. |
| owner | No | Overrides the pack owner for one answer. |

## Review rules

1. Every answer comes from its source page as that page reads on the reviewed date. Nothing is added from memory, a sales call or a draft.
2. Pricing answers expire 30 days after review and all others after 90 days, because prices change most often.
3. An expired answer is withheld, not served with a warning.
4. A price appears with its unit or billing period, as the source page states it.
5. Compliance answers state what the business claims and what it does not. A certification the business does not state on its own site is never listed.
6. No answer carries instructions to the agent or to a model, hidden text or a ranking claim.

## Our own pack

Our [Broadcastwell context pack](https://docs.broadcastwell.com/context-pack/broadcastwell.json) holds 14 buyer questions, each answered only from what one of our public pages said when we read it on the pack's reviewed date. These are the questions and the pages they come from.

| Group | Buyer question | Source page |
| --- | --- | --- |
| company | What does Broadcastwell do? | [FAQ](https://broadcastwell.com/faq) |
| company | Which AI engines do you measure? | [Methodology](https://broadcastwell.com/methodology) |
| pricing | What does Answer Repair cost? | [Answer Repair](https://broadcastwell.com/answer-repair) |
| pricing | Can we check one buyer question before buying a repair? | [Pricing](https://broadcastwell.com/pricing) |
| pricing | What does the Fix Sprint cost? | [Fix Sprint](https://broadcastwell.com/fix-sprint) |
| pricing | What do Care and Program cost? | [Pricing](https://broadcastwell.com/pricing) |
| fit | Do you work with agencies? | [For agencies](https://broadcastwell.com/for-agencies) |
| fit | Can you guarantee that ChatGPT will name us? | [FAQ](https://broadcastwell.com/faq) |
| fit | Is this just SEO? | [FAQ](https://broadcastwell.com/faq) |
| integrations | Does the Fix Sprint connect to our analytics? | [Fix Sprint](https://broadcastwell.com/fix-sprint) |
| compliance | Do you hold SOC 2 or ISO 27001 certification? | [Security](https://broadcastwell.com/security) |
| compliance | What information should we not send you? | [Security](https://broadcastwell.com/security) |
| compliance | Can we ask you to delete our project information? | [Security](https://broadcastwell.com/security) |
| links | Where is your measurement method published? | [Methodology](https://broadcastwell.com/methodology) |

## Fictional example: Kalvenor

The [Kalvenor context pack](https://docs.broadcastwell.com/context-pack/kalvenor.json) is fictional and labeled SAMPLE DATA in its own fields and in every answer. It has one answer in each group and shows how a pack handles a business with no public price: the pricing answer sends the buyer to the pricing page instead of quoting a number.

## Related guides

- [How do you claim your business in ChatGPT?](index.md), our explainer and readiness checklist
- [What belongs in a business facts file for ChatGPT?](business-facts-file.md)
- [Is the ChatGPT Business Hub available yet?](watch.md)
- [How do you reconcile ChatGPT Hub counts with receipts?](reconciliation-report.md)

## Sources

- Juozas Kaziukėnas, [LinkedIn post](https://www.linkedin.com/posts/juozas_chatgpt-is-building-an-analytics-tool-to-share-7524436371613118464-E3Zf/), 6 November 2026, for the reported business agent.
- Broadcastwell, [Ask Kalvenor, the fictional sample connector](https://app.broadcastwell.com/connect#ask-a-vendor), with six read-only groups.
- Broadcastwell public pages used by our pack: [pricing](https://broadcastwell.com/pricing), [FAQ](https://broadcastwell.com/faq), [Answer Repair](https://broadcastwell.com/answer-repair), [Fix Sprint](https://broadcastwell.com/fix-sprint), [for agencies](https://broadcastwell.com/for-agencies), [security](https://broadcastwell.com/security) and [methodology](https://broadcastwell.com/methodology).
