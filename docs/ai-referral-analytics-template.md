---
title: How do you track AI referral traffic in analytics?
headline: How do you track AI referral traffic in analytics?
description: Our AI referral analytics template for GA4, documented with its exact pattern, test cases and limits, and how Google files AI Overviews and AI Mode visits.
page_class: page
schema_type: Article
date_published: '2026-11-09T00:00:00+00:00'
date_modified: '2026-11-11T07:30:00Z'
template: business-hub.html
---

# How do you track AI referral traffic in analytics?

Track AI referral traffic with one custom channel in Google Analytics 4 that matches the assistants' own web addresses, placed above Referral. Our free [GA4 AI-referral channel template](https://app.broadcastwell.com/tools/ai-referral-channel) gives that channel; this page documents it with downloads, test cases and the limits Google states. Google AI Overviews and AI Mode visits stay in Organic Search, where GA4 files them.

Updated 11 November 2026.

A referral record tells you that your analytics classified a visit by its source. It does not tell you which question the visitor asked, what the answer said about you or whether a sale followed. Our answer on [what a recorded AI referral establishes](answers/measurement/what-does-a-recorded-ai-referral-establish.md) keeps those events apart, and the template is built the same way.

## What GA4 and Search Console already do

| Where the visit starts | Where it lands by default | What the provider says |
| --- | --- | --- |
| ChatGPT, Microsoft Copilot and the other assistants Google lists | GA4 default channel "AI Assistant" | Google's default channel page names ChatGPT, Deepseek, Copilot, Grok and Google's own assistant as example sources; the full list is not on that page |
| Claude, Perplexity | Not named on that page | Our template names both, so they are counted on purpose rather than by an unpublished list |
| Google AI Overviews and Google AI Mode | GA4 "Organic Search" | Google's default channel page says the AI Assistant channel excludes them and Organic Search includes them |
| Google AI Overviews and Google AI Mode, in Search Console | Performance report, "Web" search type | Google Search Central says these features are part of overall search traffic; page last updated 10 December 2025 |
| Microsoft Copilot and Bing AI summaries, in Bing Webmaster Tools | AI Performance report | Bing's post of 10 February 2026 describes citation counts and grounding queries, not visits |

Keep the Google rows inside search. A visit from an AI Overview arrives through Google Search, and a hostname alone cannot separate it from a classic result, so the template leaves ordinary Google referrals out.

## The template

In GA4, open Admin, then Data display, then Channel groups, and make a copy of your existing group. You need the Editor role or above on the property. Add one channel:

| Setting | Value |
| --- | --- |
| Channel name | AI referrals |
| Field | Source |
| Condition | matches regex |
| Value | The pattern below, on one line |
| Position | Above Referral. GA4 places a visit in the first channel whose definition it matches. |

    ^(.*\.)?(chatgpt\.com|chat\.openai\.com|claude\.ai|perplexity\.ai|copilot\.microsoft\.com|copilot\.cloud\.microsoft)$

Coverage as of 2 November 2026 is six hosts: chatgpt.com, chat.openai.com, claude.ai, perplexity.ai, copilot.microsoft.com and copilot.cloud.microsoft, plus any subdomain of them, such as www.perplexity.ai. It is a conservative list of identifiable referral hosts, not a list of the engines we measure. Google's own assistant is not in it; Google names that assistant among its AI Assistant examples, and your copied rules below the new channel still apply to it.

The pattern is anchored at both ends, so a host that only contains one of these names, such as `chatgpt.com.example`, stays in Referral.

### Why we do not copy Google's example pattern

Google's custom channel page offers an example pattern that begins `^.*ai|` and continues with broad terms such as `.*gpt.*` and `.*google.*bard.*`. The first part matches any source containing the letters "ai". In our test cases it catches a newsletter tagged `email`, the host `mail.example.com` and `chatgpt.com.example`, none of which came from an assistant. Our pattern names exact hosts instead. The cost is upkeep: when an assistant changes its address, the pattern needs a new entry, as Google's own note on that page says.

### Limits to know before you start

- A standard GA4 property allows two custom channel groups besides the predefined one, and a 360 property allows five. Each group holds up to 50 channels.
- Custom channel groups apply to your reports retroactively, so past visits are regrouped as well.
- A visit carries an assistant's host as its source only when a referring address reaches your site. A copied link, an app that opens a browser or a privacy setting can leave the visit as direct traffic, and no channel rule recovers it.

## Downloads and the expected output

- [Channel settings, CSV](assets/ai-referral/ai-referrals-channel-group.csv){: download="ai-referrals-channel-group.csv" }
- [The pattern on one line, text](assets/ai-referral/ai-referrals-source-regex.txt){: download="ai-referrals-source-regex.txt" }
- [Thirteen test cases with the expected result, CSV](assets/ai-referral/ai-referrals-test-cases.csv){: download="ai-referrals-test-cases.csv" }

The test file is the expected output. Put each source through the pattern as a full match and you should get its `matches_pattern` value: the six listed hosts and www.perplexity.ai match; `gemini.google.com`, `google`, `email`, `mail.example.com`, `chatgpt.com.example` and the fictional `kalvenor.example` do not. Our test suite runs the same check on every build of this site, so the page and the files cannot drift apart.

## How to read the channel once it fills

Report the channel as sessions with an identified AI source, beside the dated answers that named or cited you. Our [three measured rates](resources/three-rates.md) define what each answer count means, and our note on [Search Console query evidence](answers/measurement/what-can-search-console-show-about-ai-visibility-queries.md) covers what Google's report can and cannot show. A rise after a page change is a reason to look at the answers again, not proof that the change caused it; our guide to a [fair re-check](resources/guides/fair-recheck.md) sets out the comparison. Keep answers to a "How did you hear about us?" field in their own column too.

When we measure answers for you, the capture covers ChatGPT, Claude, Perplexity, Google AI Overviews and Google AI Mode, and the visit record stays yours. A [Fix Sprint](https://broadcastwell.com/fix-sprint) agrees one primary test before payment, and buyer-task completion is one of the three it can use. The full ladder is on our [service model](service-model.md) page.

## Sources

- Broadcastwell, [Free GA4 AI-referral channel template](https://app.broadcastwell.com/tools/ai-referral-channel), updated 2 November 2026, read 9 November 2026.
- Google Analytics Help, [Default channel group](https://support.google.com/analytics/answer/9756891), AI Assistant and Organic Search channel descriptions and rules, read 9 November 2026 (no date shown on the page).
- Google Analytics Help, [Custom channel groups](https://support.google.com/analytics/answer/13051316), "Example: AI assistants", per-property limits and channel order, read 9 November 2026 (no date shown on the page).
- Google Search Central, [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features), last updated 10 December 2025, read 9 November 2026.
- Bing Webmaster Blog, [Introducing AI Performance in Bing Webmaster Tools Public Preview](https://blogs.bing.com/webmaster/2026/2/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview/), 10 February 2026, read 9 November 2026.

Related: our [AI search glossary](ai-search-glossary.md), our [operating framework](operating-framework.md) and the [completed-case format](cases/format.md), which keeps commercial fields apart from answer counts.
