---
title: "AI Source Standard v1"
headline: "AI Source Standard v1: record AI-assisted buyers at the source"
description: "The open specification for optional AI source fields, CRM properties, analytics classes and dated aggregate reporting. CC BY 4.0."
page_class: page
schema_type: Article
date_published: "2026-10-07T00:00:00+00:00"
date_modified: "2026-10-07T00:00:00+00:00"
---

# AI Source Standard v1

Published release v1.0: [DOI 10.5281/zenodo.23225776](https://doi.org/10.5281/zenodo.23225776). [Release source and templates](https://github.com/Broadcastwell/ai-source-standard/tree/v1.0).

Version 1.0. Specification date: 7 October 2026. Copyright 2026 Broadcastwell LLC. [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), attribution to Broadcastwell. Adopt it without asking. This specification and its templates are free.

GA4, Google Tag Manager and Salesforce recipes: **documentation checked; live installation not tested.** Broadcastwell's reference stack uses Framer analytics and HubSpot. Each installation needs its own verification record; local fixture checks do not establish live platform import acceptance.

A small, open specification for recording where AI-assisted buyers came from, in the systems a company already runs. One source field, an optional question, two CRM properties, analytics definitions and a classification of referrers and parameters. Buyers may arrive with no referrer. A visibility score cannot show what reached a company's pipeline. This standard adds no identity field, cookie or Broadcastwell tracking service. Free text can contain personal information and needs the controls below.

## 1. Form fields

Place these fields after the visitor's message or request details and before Submit. Neither is required. Do not select a source by default. A blank means not supplied, not Other. Preserve this exact order and spelling:

1. ChatGPT
2. Claude
3. Perplexity
4. Google AI Overviews or AI Mode
5. Microsoft Copilot
6. Google search
7. LinkedIn
8. A colleague or partner
9. An event
10. Other

The first five are the AI options. The field name is `ai_source`, label `How did you hear about us?`, single select. Values equal the option labels. Do not add Gemini to this v1 list: use Other for a source without its own option. This is separate from the analytics classification, which can recognize gemini.google.com.

The follow-up is `ai_question_asked`, label `What did you ask it?`, multi-line text, optional, maximum 2,000 characters. Display it when an AI option is selected. Where conditional fields are unavailable, show it with `Only if an AI assistant sent you.` Do not turn a referrer or query parameter into a self-reported answer. Do not prefill either field. Clear the question if the visitor changes to a non-AI option. Raw questions stay in the company's own intake and CRM; no raw question goes to analytics.

## 2. CRM properties and mapping

<table><thead><tr><th>Internal name</th><th>Label</th><th>Type</th><th>Group</th></tr></thead><tbody><tr><td>ai_source</td><td>AI source</td><td>Dropdown select, exact ten options above</td><td>Contact information</td></tr><tr><td>ai_question_asked</td><td>AI question asked</td><td>Multi-line text</td><td>Contact information</td></tr></tbody></table>

Description for ai_source: `AI Source Standard v1. Self-reported by the contact on a form. Never edited by hand.`

Description for ai_question_asked: `AI Source Standard v1. The question the contact says they asked an AI assistant, as submitted. De-identified before any report.`

The form's existing mapping writes these two values on a successful submission. Do not manually set them, infer a source or overwrite the CRM's Original Traffic Source. A missing answer does not overwrite a previous non-empty self-report. Retain dated form submissions in the CRM so a later answer does not erase period evidence. Deduplicate within each reporting period using the CRM's own stable contact identifier. Export only aggregates and reviewed questions.

HubSpot's minimum implementation is the two properties and form mapping. Optional contact workflow: `AI Source Standard v1: record AI source`. Trigger on the installed form submission with ai_source known. One action creates a contact note: `AI Source Standard v1: ai_source = <value>, recorded <date>`. Insert actual property and date tokens, not those literal placeholders. Re-enrolment off; do not enrol existing contacts. No email, task, owner, list or other action. This note records the first qualifying enrolment; it is not a complete history of subsequent submissions. If the plan has no suitable workflow, keep the minimum implementation and record the omitted note workflow. Do not upgrade.

The JSON templates are separate valid POST bodies for HubSpot's Properties API, not a claimed bulk import screen. Use the existing authorized integration or the settings UI. No new credential is required by this standard. Salesforce equivalents are Lead fields `AI_Source__c` (Picklist) and `AI_Question_Asked__c` (Long Text Area). Keep generated Web-to-Lead field IDs local to that organization. Map to corresponding Contact fields on conversion if the client already authorizes them. No opportunity amount is inferred from a source field.

## 3. Browser referrer and parameter classes

These rules classify what was received, not who sent a visitor. Referrers may be absent, truncated or forged; parameters may be copied or user supplied. A host must be an exact match or a subdomain on a dot boundary. Reject suffix lookalikes, user-info URLs and non-HTTP protocols. Keep observed referrer class, parameter class and self-report separate.

<table><thead><tr><th>Candidate class</th><th>Received host</th><th>Outbound parameter guarantee</th><th>Evidence status on 7 October 2026</th></tr></thead><tbody><tr><td>ChatGPT</td><td>chatgpt.com; chat.openai.com retained for legacy configuration</td><td>utm_source=chatgpt.com</td><td>OpenAI documents this parameter. It does not guarantee a referrer on every click. Legacy host is a configuration candidate.</td></tr><tr><td>Claude</td><td>claude.ai</td><td>Not stated by the platform</td><td>Configuration candidate; no click-through observation in this run</td></tr><tr><td>Perplexity</td><td>perplexity.ai</td><td>Not stated by the platform</td><td>Configuration candidate; no click-through observation in this run</td></tr><tr><td>Gemini</td><td>gemini.google.com</td><td>Not stated by the platform</td><td>Configuration candidate; no click-through observation in this run</td></tr><tr><td>Microsoft Copilot</td><td>copilot.microsoft.com</td><td>Not stated by the platform</td><td>Configuration candidate; bing.com alone is ambiguous and excluded</td></tr><tr><td>Google AI Overviews or AI Mode</td><td>No distinct referrer class</td><td>No unique attribution parameter established here</td><td>Google search referrers cannot separate these clicks. Record the visitor's optional self-report.</td></tr></tbody></table>

Primary parameter source: [OpenAI publishers FAQ](https://help.openai.com/en/articles/12627856-publishers-and-developers-faq), read 7 October 2026. The sources in the table are candidate matching rules unless explicitly documented above. No automated AI-product use or human click-through observation was made in this run. A client verification record adds observed host, parameter, date and test session reference; it does not convert an observation into a platform guarantee.

Google AI Overviews and AI Mode traffic is not separable by browser referrer and is recorded here only through the self-reported field. Google separately provides [Search Console reports for generative AI features](https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports). Search Console visibility is not a session-level CRM attribution record. Sources read 7 October 2026: that announcement, [AI features guidance](https://developers.google.com/search/docs/appearance/ai-features), and [GA4 default channels](https://support.google.com/analytics/answer/9756891?hl=en).

## 4. Analytics

Name the reporting channel `AI referred`. Use session scope. Count a session once, with an eligible received source from section 3. The GA4 recipe creates a custom channel group and puts the exact AI source rule above the broad Referral rule. Keep the original default group. Create per-source session segments using the same exact boundaries. Report sessions, source, date range and property timezone. An exploration uses Session source / medium as rows and Sessions as its metric, with the AI segment applied. Export a summary with filters and export date.

GA4 may use a campaign label ahead of a referrer. Its AI Assistant default channel is useful but has its own platform definition, which excludes Google AI Overviews and AI Mode. Do not silently mix that total with this versioned custom definition. Where source provenance is unavailable, label the number `session source class; referrer versus parameter not distinguishable in this export`. Never call a page view or unique visitor a session. If the existing platform cannot supply session totals, report its actual metric separately and print sessions as not measured.

A cookie-free helper recipe in a client's existing tag manager can calculate the received host and ChatGPT parameter classes and fill a hidden technical field `ai_referrer_class`. It never writes ai_source, never persists data, never sends a request and never forwards the free-text question to analytics. The client owns the configuration. Broadcastwell hosts no tracking script or endpoint for it. Review imported tags in an unpublished workspace before the client's own administrator publishes. A client without a tag manager uses the existing analytics source export; installing a new manager is not required.

Sources read 7 October 2026: [GA4 custom channel groups](https://support.google.com/analytics/answer/13051316?hl=en), [traffic-source processing](https://support.google.com/analytics/answer/11242841?hl=en), [segments](https://support.google.com/analytics/answer/9304353?hl=en), [Tag Manager variables](https://support.google.com/tagmanager/answer/7683362?hl=en), [custom variables](https://support.google.com/tagmanager/answer/7182738?hl=en), [container import](https://support.google.com/tagmanager/answer/6106997?hl=en-GB).

## 5. Server user agents

User-agent strings identify a declared purpose, not a human session or a verified identity. Keep these requests outside AI-referred human-session totals. Verify vendor-published IP information or signatures where available; otherwise label them declared only. Do not treat a crawler visit as a buyer or an organic mention.

1. OpenAI: OAI-SearchBot is a search crawler; GPTBot is a training crawler; ChatGPT-User is a user-triggered fetch. A signed ChatGPT cloud-browser request is a separate agent-browsing class. [Bots documentation](https://developers.openai.com/api/docs/bots) and [signed browser guidance](https://help.openai.com/en/articles/11845367-chatgpt-works-cloud-browser-allowlisting).
2. Anthropic: Claude-SearchBot is search; ClaudeBot is training; Claude-User is user-triggered retrieval. These do not establish the identity of a Chrome extension request. [Crawler guidance](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler).
3. Perplexity: PerplexityBot is search; Perplexity-User is a user-triggered request. Neither alone proves a Comet browser session. [Crawler guidance](https://docs.perplexity.ai/docs/resources/perplexity-crawlers).
4. Google: Googlebot is search crawling; Google-Agent is a documented user-triggered fetcher. Google-Extended is a robots control token, not a separate HTTP user agent. [Fetcher guidance](https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers).

All sources read 7 October 2026. See the existing [agent traffic guide](https://app.broadcastwell.com/tools/agent-traffic) for the dated operational checks. No agent query is required to install this standard.

## 6. Reporting definitions

An AI-referred session is a session in section 4's class, labelled by received source class and date. An AI-sourced lead is a distinct lead whose submitted ai_source is one of the first five options, labelled self-reported. Count leads with a qualifying submission in the period once; exclude test submissions and report the total lead base using the same period and identity rule. A blank is not zero.

An AI-sourced opportunity is a distinct CRM opportunity with a documented association to an AI-sourced lead. Deduplicate each opportunity once even if it has several qualifying contacts. State the association rule, pipeline, currency and date basis. For this implementation, opportunities created within the period form the cohort; pipeline amount is the CRM-recorded open amount for that cohort at export, and won amount is the CRM-recorded won amount for that cohort at export. Include the total opportunity base for the same cohort. Do not sum currencies or silently mix creation-date cohorts with close-date totals. These are recorded amounts, not incremental revenue. Missing association or amount data is not measured, with a reason.

## 7. De-identification and privacy

Before a question is stored outside the company's own CRM or intake, a person removes names, email addresses, phone numbers and company names, replacing necessary entities with neutral descriptions such as `[vendor]` or `[buyer]`. Drop any question that cannot be de-identified confidently. Do not upload raw CRM exports or contact identifiers to Broadcastwell. Review at most the questions needed for the report. Application validation rejects obvious identifiers and known account/company tokens; it cannot identify every name, so a named human review remains mandatory.

Privacy sentence: `Our forms ask, optionally, how you heard about us and what you asked an AI assistant before visiting; we store the answer with your enquiry, remove names and contact details from the question before it is used in reporting, and set no additional cookie for this.`

Reports use counts, amounts and reviewed questions only. Read permission is optional and revocable. Revoking it stops permission-based imports and hides that source from the account projection; a client may instead provide a reviewed aggregate export. Credentials remain with the client. Do not put raw questions in URLs, browser analytics, source labels or receipt filenames.

## 8. The Proof Page and Report

Four lines, each with source and date:

1. Measured presence: named count, base, named rate and 95 percent interval from the latest released Category Audit or applicable Absence Index record. State method version and run or release reference.
2. AI-referred demand: analytics sessions by source class and leads by self-reported AI option, with separate totals, periods and source dates. Questions are reviewed and de-identified.
3. AI-sourced pipeline: CRM-recorded opportunities, open pipeline and won amounts for the stated cohort and currency. No forecast or weighting.
4. Lift: the existing published controlled-lift computation, only with a shipped fix, locked target/control assignment and eligible follow-up. Otherwise `no fix window yet`. Never infer this verdict from correlated presence and pipeline totals.

Every unavailable source says `not measured` and why. Page one of the Proof Report adds the period table, buyer questions and next step. Its appendix gives the analytics and CRM export summaries, filters, timezone and dates, and a released re-measure link where one exists. Priya Nair, Management Consultant, reviews before release. Fictional examples display SAMPLE DATA on every view.

The Proof Page shows what analytics, forms and CRM recorded beside measured presence on stated dates. A buyer may read an AI answer and type the address, arriving as direct traffic. A referrer can be stripped. A self-report is what the person chose. An amount is what the CRM holds. Presence and pipeline moving together is an association; the only causal statement is the controlled-lift verdict under its published rule. The page promises no leads, revenue or position.

## 9. Version and adoption

Do not change the option list without a version note. Changes to values, inclusion rules, period bases or privacy rules require a new version and a migration note; never rewrite past reports. Corrections retain a dated changelog. Preserve the standard version in every template, installation record and report. A DOI identifies the published release; an unreleased working copy must not invent one.

## Templates and downloads

Use the [version 1.0 downloads](https://app.broadcastwell.com/standard/ai-source#downloads) for the complete specification, HubSpot property JSON and field table, platform recipes, local classifier, Tag Manager container recipe, optional HTML fields and privacy sentence. Preserve existing platform settings and verify the actual installation before publishing it. The files are free under CC BY 4.0 with attribution to Broadcastwell.

Platform recipes can be documentation-checked without a live installation. An installation record must state which systems were actually applied, who verified them, evidence dates, omitted features and pending human click-through checks. Do not describe a recipe as live merely because its JSON parses. The free standard is independent of buying Proof Setup.
