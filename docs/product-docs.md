---
title: What does our product documentation cover?
headline: What does our product documentation cover?
description: Our product documentation covers eight free tasks, from the fictional sample to the Kalvenor connector, each with its limits and an expected output to check.
page_class: page
schema_type: Article
date_published: '2026-11-09T00:00:00+00:00'
date_modified: '2026-11-09T00:00:00+00:00'
template: business-hub.html
---

# What does our product documentation cover?

Our product documentation covers the eight things you can do with Broadcastwell without talking to us: read the fictional sample account, run the free 10-question check, build or validate an llms.txt file, validate a business facts file, connect an assistant to the fictional Kalvenor connector, set up an AI referral channel, look up a vendor in your browser and cite our data.

Updated 9 November 2026.

Each task below states what it does, its limits, one worked example on public or fictional data, and an expected output you can download and compare. Kalvenor Systems is a fictional company; every Kalvenor value is sample data, not a client result. Paid work is described on our [service model](service-model.md) page and is not needed for anything here.

## 1. Read the fictional sample account

**What it does.** [The fictional sample](https://app.broadcastwell.com/sample) shows a complete client account for Kalvenor Systems: 35 buyer questions in field service management software, five engines (ChatGPT, Claude, Perplexity, Google AI Overviews and Google AI Mode), three scheduled runs and a fourth run on some questions, with a receipt for every answer.

**Limits.** The figures demonstrate the format. They are not measurements of any real company.

**Worked example.** Open the CSV export and read its first row: question 1, "What is field service management software?", ChatGPT, run 1. Kalvenor is not named (`brand_named` is 0), Orbit Field is the checked competitor found, and two cited URLs are listed.

**Expected output.** The export has 549 answer rows over 35 questions; 133 rows name Kalvenor, and 7 rows record an engine error rather than a miss. Download [the CSV](https://app.broadcastwell.com/api/export/baseline-kalvenor-v11.csv) or [the JSON](https://app.broadcastwell.com/api/export/baseline-kalvenor-v11.json) and count them yourself.

## 2. Run the free 10-question check (one engine)

**What it does.** The [free check](https://audit.broadcastwell.com/) reads your homepage and up to two more public pages to propose your company name and category, then asks Claude ten buyer questions once each and shows each question as named or not named, with who is named instead and the sources cited.

**Limits.** One engine, one run, ten questions. No email is needed; runs are limited per network and per day, and by the site's daily allowance. Nothing runs until you confirm the category. One run is an observation, not a rate; our note on [measurement noise](measurement-noise.md) explains why.

**Worked example.** The fictional sample in task 1 is the five-engine, three-run version of the same per-question layout. Compare its question 1 rows across engines to see why a single engine and a single run cannot stand in for the full record.

**Expected output.** A score out of ten, the companies named instead, where the answers came from, and a question-by-question list. A saved result reports the count without the individual answers.

## 3. Build or validate an llms.txt file

**What it does.** The [llms.txt generator and validator](https://app.broadcastwell.com/tools/llms-txt) drafts a file from up to 40 public pages on one HTTPS site within eight seconds, following robots.txt, and validates a file you paste or one it fetches from `/llms.txt`. It also shows what robots.txt says to nine documented crawlers.

**Limits.** Same-site links are checked; external links and requests the time budget cannot finish are marked unverified. An llms.txt file is navigation guidance and does not make an assistant read, cite or name you. We do not save your website, company name, page content or result.

**Worked example.** Our own [llms.txt](https://docs.broadcastwell.com/llms.txt) for this site lists every guide with its title, address and one-line description, under a dated block of current prices and terms.

**Expected output.** A text file with a title line, a short summary and grouped link lists, served as `text/plain` from the root of your domain.

## 4. Validate a business facts file

**What it does.** Our [business facts file guide](chatgpt-business-hub/business-facts-file.md) defines a machine-readable file of your company, product, offer and contact facts, with a published schema.

**Limits.** A valid file proves its format and freshness dates, not that any engine reads it.

**Worked example.** Validate the fictional [Kalvenor business facts file](examples/kalvenor-business-facts.json) against [the schema](business-facts.schema.json) with any JSON Schema 2020-12 validator.

**Expected output.** No format errors. Every Kalvenor value carries a "SAMPLE DATA" label, and the file sets `"fictional": true`.

## 5. Connect an assistant to the fictional Kalvenor connector

**What it does.** The public connector at `https://app.broadcastwell.com/mcp/vendor/kalvenor` answers an assistant's questions about the fictional vendor from facts the vendor controls, in the format described by our [Vendor Facts File standard](vendor-facts.md).

**Limits.** Read-only sample data. It provides no ranking or measurement.

**Worked example.** We sent a `tools/list` request to the connector on 9 November 2026. It listed six read-only tools: `get_company`, `get_pricing`, `get_fit`, `get_integrations`, `get_compliance` and `get_links`, each described as "SAMPLE DATA. Fictional vendor."

**Expected output.** [The recorded response](assets/product-docs/kalvenor-connector-tools-list.json){: download="kalvenor-connector-tools-list.json" }, as JSON. Your client should list the same six names.

## 6. Set up an AI referral channel in GA4

**What it does.** One custom channel groups visits from six assistant hosts above Referral. Our [AI referral analytics template](ai-referral-analytics-template.md) documents it.

**Limits.** A visit without a referring address stays direct traffic. Google AI Overviews and AI Mode visits stay in Organic Search.

**Worked example and expected output.** The [thirteen test cases](assets/ai-referral/ai-referrals-test-cases.csv) list each source and whether the pattern matches it.

## 7. Look up a vendor from your browser

**What it does.** Our [AI Shortlist Check browser extension](browser-extension.md) shows the Index record for the software company whose site you are on.

**Limits.** Index release 2026-09 only; installed from its public source repository.

**Worked example and expected output.** On procore.com it shows Procore named in 109 of 150 valid answers, interval 65.0 to 79.2 percent, matching the release file.

## 8. Cite our data

**What it does.** Our [citation page](cite.md) gives every DOI-registered dataset and report in APA, Chicago, BibTeX and RIS.

**Limits.** Cite the DOI record, not a page title that may be shorter.

**Worked example and expected output.** The September Index cites as DOI 10.5281/zenodo.22907695. The [BibTeX file](assets/citations/broadcastwell-research.bib) holds the same record.

## Where the method lives

Every task above uses the measurement rules on our [method page](https://broadcastwell.com/methodology), version 1.1. Terms used on this page are defined in our [AI search glossary](ai-search-glossary.md).

## Sources

- Broadcastwell, [fictional sample account](https://app.broadcastwell.com/sample) and its CSV and JSON exports, read 9 November 2026.
- Broadcastwell, [Free 10-question check (one engine)](https://audit.broadcastwell.com/), read 9 November 2026.
- Broadcastwell, [llms.txt generator and validator](https://app.broadcastwell.com/tools/llms-txt), read 9 November 2026.
- Broadcastwell, fictional Kalvenor connector, `tools/list` response recorded 9 November 2026.
- Broadcastwell, [method v1.1](https://broadcastwell.com/methodology).
