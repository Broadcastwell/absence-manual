---
title: Where can you download our open data and methods?
headline: Where can you download our open data and methods?
description: Our open data catalog lists 65 research tables and six Index release files with rows, columns, SHA-256, license and the method page that limits each one.
page_class: page
schema_type: Article
date_published: '2026-11-09T00:00:00+00:00'
date_modified: '2026-11-11T07:30:00Z'
template: business-hub.html
---

# Where can you download our open data and methods?

All of our open data downloads without a form, an account or a fee: 65 research tables on this site and six Absence Index release files, each listed below with its rows, columns, size, SHA-256 hash, license and the page that states its method and limits. Every count we publish traces back to one of these files.

Updated 11 November 2026.

Reuse is free under CC BY 4.0 with attribution to Broadcastwell, the terms set out on our [free academic access page](research/academic-access/index.md). Cite the release or report DOI when a result depends on a fixed version; our page on [how to cite our research](cite.md) gives the formats.

## How to check a download

The SHA-256 column holds the hash of the bytes we serve. Compute the hash of your copy and compare: `sha256sum vendor-pairs.csv` on Linux or macOS, `Get-FileHash vendor-pairs.csv -Algorithm SHA256` in Windows PowerShell. A match means you hold the same file we analyzed. Rows count data lines after the header, and JSON files show their records instead; a table with 0 rows ships its header so its columns are still documented. Hashes and counts were computed from the files on 9 November 2026.

Three limits travel with every file. The September 2026 archive holds 2,100 target attempts, of which 2,095 are valid answers; a failed capture is never a vendor absence. The August 2026 release kept aggregates only, so it cannot be expanded into answer rows or treated as a controlled comparison with September. And none of these tables measures clicks, revenue, product quality or future answers.

## Absence Index release files

Published on the Index site under the release's version DOI [10.5281/zenodo.22907695](https://doi.org/10.5281/zenodo.22907695), released 23 September 2026, answers captured 22 and 23 September 2026. The other 13 category tables sit beside the CRM table on the [Index downloads page](https://index.broadcastwell.com/downloads). Hashes are of the bytes served on 9 November 2026.

| File | What it holds | Rows | Columns | Size | SHA-256 | License | Method and limits |
| --- | --- | ---: | --- | ---: | --- | --- | --- |
| [release-2026-09.json](https://index.broadcastwell.com/data/release-2026-09.json) | The September 2026 release: categories, questions, checked vendors, named and cited counts with bases and intervals, exclusions and source captures | 14 categories | 9 keys | 1.1 MB | `e7829183f6785357787fcf85d3c27999403b0a329f349dad4c7343b11d23f142` | CC BY 4.0 | [Index method](https://index.broadcastwell.com/method) |
| [crm-2026-09.csv](https://index.broadcastwell.com/data/crm-2026-09.csv) | The CRM category: one row per checked vendor with counts, bases, intervals and per-engine figures | 10 | 27 | 9.2 KB | `56448ef384c7cbfaf05784cacf38d64815bf40a4923247aa4b5c49cecce5da8a` | CC BY 4.0 | [Index method](https://index.broadcastwell.com/method) |
| [benchmark/release-2026-09.jsonl](https://index.broadcastwell.com/data/benchmark/release-2026-09.jsonl) | One row per September target attempt, failures included: engine, repeat, capture time, named vendors in order and cited domains with class | 2,100 | 21 fields | 2.2 MB | `8777c45fa4d0695b2c4010cf88391b7a9903ce8d1d82cddbc9178d05fab3a125` | CC BY 4.0 | [Index method](https://index.broadcastwell.com/method) |
| [benchmark/schema.json](https://index.broadcastwell.com/data/benchmark/schema.json) | Field definitions for the attempt rows | one record | 6 keys | 2.3 KB | `661df3042b305a42b3fde31bc99279661a484a8bba7cedde7624373f85504ccd` | CC BY 4.0 | [Index method](https://index.broadcastwell.com/method) |
| <a href="https://index.broadcastwell.com/data/benchmark/README.md">benchmark/README.md</a> | Scope, file list, field notes, limits and citation for the long-format files | text | text | 2.9 KB | `696e3a0d85483f5e87c77d25a505cff1abae87aa7a37aa148a12a247160334d7` | CC BY 4.0 | [Index method](https://index.broadcastwell.com/method) |
| [benchmark/release-2026-08.1-aggregates.json](https://index.broadcastwell.com/data/benchmark/release-2026-08.1-aggregates.json) | The historical August 2026 aggregates with their erratum; attempt rows for August were not retained | 2 categories | 9 keys | 23.6 KB | `6d2c651844c7f6e4a885977290e9822f6c9e2994e8d554bd65c99bf60279cd67` | CC BY 4.0 | [Index method](https://index.broadcastwell.com/method) |

## Study 2: who appears in the sources of B2B software answers

Registered secondary analysis of the citation arrays in Index release 2026-09, registration [OSF VCZKT](https://doi.org/10.17605/OSF.IO/VCZKT); answers captured 22 and 23 September 2026. Method, corrections and limits are on the [Study 2 page](research/studies/who-ai-engines-cite/index.md).

| File | What it holds | Rows | Columns | Size | SHA-256 | License | Method and limits |
| --- | --- | ---: | --- | ---: | --- | --- | --- |
| [answer-citation-audit.csv](research/data/answer-citation-audit.csv) | One row per valid answer, target and control: engine, category, question, repeat, capture time, citation entries and a zero-citation flag | 2,245 | 10 | 280.0 KB | `870a01d49d90b3d146bf487b48171ff69663cfea3548e863cc7641db7fffded5` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [answer-citation-bases.csv](research/data/answer-citation-bases.csv) | Valid answers and zero-citation answers with intervals, plus citation entries, by scope, engine and category | 198 | 9 | 13.7 KB | `1908c8c14af91eb0d1d6bb2ac811ac075eacc62f71e550c7822277fe56a4b863` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [citation-occurrences.csv](research/data/citation-occurrences.csv) | Every citation entry: its answer, array position, original URL, host, source class and duplicate or ambiguity flags | 20,190 | 13 | 4.5 MB | `fbf0dda06220b5c414542cfc2f71a89471e3d84af9dffa0fc1d56ef0398921ac` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [citation-invalid.csv](research/data/citation-invalid.csv) | Citation entries rejected as unusable URLs; it holds its header and no rows | 0 | 13 | 136 bytes | `e9228d3f431c9d134516e02eaf9e1ef24eed0eff4c9f684781363093fbf6a26a` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [citation-class-shares.csv](research/data/citation-class-shares.csv) | Source-class shares of citation entries under the frozen classification, with Wilson intervals | 6,534 | 10 | 739.9 KB | `a516e444d93f486e03b62a809822ccf2db196df4dd1b7234578b23170853ffc5` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [citation-class-shares-post-audit.csv](research/data/citation-class-shares-post-audit.csv) | The same source-class shares after the dated host audit | 6,534 | 10 | 739.7 KB | `416363686d1733c2bcbe9f4469286c397fc83e2601dc9bc76fc1264e8a61dd65` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [citation-concentration.csv](research/data/citation-concentration.csv) | How much of each citation base the most-cited hosts take, with the tie rule and intervals | 792 | 13 | 143.4 KB | `e9d6b88dec45393202d508a7d7f312048856a629e2ee1319bafe2912e7f1b40a` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [cited-hosts.csv](research/data/cited-hosts.csv) | Every cited host ranked by citation entries, with share, interval, class and ambiguity | 51,234 | 13 | 6.2 MB | `65e2468d2edd34d10012622e16d9f74b0f6c75740a16576dbffcc6d3c80b7aee` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [top-twenty-hosts.csv](research/data/top-twenty-hosts.csv) | The twenty most-cited hosts in each cut, with share, interval and class | 7,870 | 13 | 1.0 MB | `716b3421d7771f9ed232dbb713c2072e6ab618e84a1f23c4f0d1b42b9812b023` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [host-classes.csv](research/data/host-classes.csv) | The frozen class of each cited host, with evidence address, rationale, check date and response fingerprint | 2,044 | 8 | 477.2 KB | `1c72328bbb09377f56a95884deef05b2d74b07ddfcbc0e623d38d15e072c6dfb` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [host-classes-post-audit.csv](research/data/host-classes-post-audit.csv) | Host classes after the dated audit | 2,044 | 8 | 477.1 KB | `3f53f95938ea3b45f24373ba7e73436fd8d0af7c5a9d83bb4091c6daf136154a` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [host-class-post-audit-changes.csv](research/data/host-class-post-audit-changes.csv) | The hosts whose class or ambiguity changed in the audit, and why | 13 | 8 | 3.2 KB | `adf32c8f3ae85e7a559fb13144498d1380eeb296b89032d00c6f579dec8214eb` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [review-platform-occurrences.csv](research/data/review-platform-occurrences.csv) | Citation entries pointing to review-platform hosts, by engine and category | 2,376 | 10 | 249.4 KB | `4355674e5b387757a9b8e3f8b453b741b99af39b76e108ac14ddcfd5d484e0c0` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [excluded-answers.csv](research/data/excluded-answers.csv) | The five excluded target attempts and the reason recorded for each | 5 | 9 | 1.0 KB | `9c3100824dcec90b651ce9574c1ba7f973d05ac3e93039794b89587d4dab4518` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [protocol-deviations.csv](research/data/protocol-deviations.csv) | Dated changes to the registered protocol and what stayed the same | 2 | 6 | 761 bytes | `3ee652424046d10d3eb0c633e6a7b6a5f373f5d982d901bd5bdd554feee840e2` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [repeat-disagreement.csv](research/data/repeat-disagreement.csv) | Vendor and question cells named in one or two of three valid repeats, by engine and category | 76 | 9 | 13.1 KB | `4baa3768bda1130a47fbaaa33c2abed0814bff0bf4f8d28db86b9fb8d20c0d7d` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [vendor-concentration.csv](research/data/vendor-concentration.csv) | The share of checked-vendor naming occurrences held by each category's three most-named vendors | 84 | 9 | 14.9 KB | `797dbd058ce01200a4f5d96e4dff16f3e398b0e5403fc1c99146677e97d25f8a` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [vendor-naming-citation.csv](research/data/vendor-naming-citation.csv) | Per category: vendor and answer pairs, named pairs and pairs that also cite the vendor's own domain, with intervals | 15 | 12 | 3.6 KB | `fed91f5317b7c4cc07dcd39469140231597b6246e9301fd690c2d1a965cb0cf1` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [vendor-pair-summary.csv](research/data/vendor-pair-summary.csv) | The same naming and own-domain citation measures split by engine | 90 | 12 | 11.1 KB | `f62cd7130797b6b9ac711576d024b769f961a2fa99beab0e1ef85e7e5d67be93` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [vendor-pairs.csv](research/data/vendor-pairs.csv) | One row per checked vendor and valid answer, with named and own-domain cited flags | 42,792 | 8 | 4.3 MB | `69b45b4ea2c2aa2ad62f5d5ac6f79316ca34b584f4adc7728ef770966c52aab8` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [vendor-pair-reconciliation.csv](research/data/vendor-pair-reconciliation.csv) | Reproduced named and cited counts beside the published release counts for every checked vendor | 286 | 8 | 20.5 KB | `691e85d27ba1d3a2fbf7607672b5113aca76318ddde8dfba2ee420f164d9988c` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [vendor-matching-dictionary.csv](research/data/vendor-matching-dictionary.csv) | The matching rules for each checked vendor: canonical domain, alias domains, product hosts and name aliases | 286 | 8 | 46.3 KB | `611d31d07e375ad44ac63cc924fb3f0c27dff08bcc2ea3240f9e749bbff8778b` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [vendor-presence.csv](research/data/vendor-presence.csv) | Each checked vendor's named count, valid base and interval, with its own-domain cited count | 286 | 13 | 46.3 KB | `f10ca6f1800471604fa7b8ea65b110b1cd94ea4af09054962e4e512fc2de7074` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [control-questions.json](research/data/control-questions.json) | The ten control questions with category and shape | 10 | 4 fields | 1.8 KB | `0c7ae041a984452b10ff9074deb7f502aa2c2b72f5a28fea581fae408be816cb` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |
| [study2-file-manifest.csv](research/data/study2-file-manifest.csv) | SHA-256 and role of every Study 2 file, for checking a download | 36 | 4 | 7.4 KB | `c70d4a381b3fa298774cfebdf95b6b89a397e9fe31e9ac04fd57224a11f6504c` | CC BY 4.0 | [Study 2](research/studies/who-ai-engines-cite/index.md) |

## Study 1: optimization signals on AI-cited pages

Registered analysis of the pages cited in the same September archive, fetched on 30 October 2026, registration [OSF DVYFU](https://doi.org/10.17605/OSF.IO/DVYFU). Method, rules and limits are on the [Study 1 page](research/studies/optimized-pages-in-ai-answers/index.md).

| File | What it holds | Rows | Columns | Size | SHA-256 | License | Method and limits |
| --- | --- | ---: | --- | ---: | --- | --- | --- |
| [study1-url-classifications.csv](research/data/study1-url-classifications.csv) | One row per cited URL: fetch outcome and page signals such as canonical, Open Graph, JSON-LD, robots and analytics | 6,271 | 32 | 3.6 MB | `2d9afc3cf8f55ad0f481c7718f8dffa923ba8cc49de0b7452e73057c8b523633` | CC BY 4.0 | [Study 1](research/studies/optimized-pages-in-ai-answers/index.md) |
| [study1-page-signals.jsonl](research/data/study1-page-signals.jsonl) | One record per fetch attempt: requested URL, robots state, outcome and whether HTML was fetched | 6,261 | 6 fields | 5.6 MB | `ad24aa966b860ee4c263b0ab2a08eb9427c31c0abd73098e4699e6f0439b4c91` | CC BY 4.0 | [Study 1](research/studies/optimized-pages-in-ai-answers/index.md) |
| [study1-citation-membership.csv](research/data/study1-citation-membership.csv) | Which URL sits at which position in each answer's citation array | 20,190 | 8 | 2.9 MB | `7e813c5f0aa5072705fd224d1a050b3e839b8af86c41276f72bd600b7132c7d6` | CC BY 4.0 | [Study 1](research/studies/optimized-pages-in-ai-answers/index.md) |
| [study1-citation-order.csv](research/data/study1-citation-order.csv) | Signal shares by position in the citation array, with bases and intervals | 3,750 | 13 | 627.6 KB | `4311ebf0ce82ec81352ffc1dc815fd0a8c8865571e43eebd0b3e8bf0dcddc68a` | CC BY 4.0 | [Study 1](research/studies/optimized-pages-in-ai-answers/index.md) |
| [study1-class-shares.csv](research/data/study1-class-shares.csv) | Shares of pages in each registered optimization class, with bases and intervals | 990 | 11 | 155.0 KB | `0f58daa31f775c686f9596e09122bce451454711e594e0a9aa8cff87eaebf9df` | CC BY 4.0 | [Study 1](research/studies/optimized-pages-in-ai-answers/index.md) |
| [study1-fetch-outcomes.csv](research/data/study1-fetch-outcomes.csv) | Fetch results for cited URLs by scope, engine and category, with bases | 1,191 | 11 | 153.4 KB | `9341ff3266845f21f17528964cf16bc36b9251b53421d313797ac210d6efb8be` | CC BY 4.0 | [Study 1](research/studies/optimized-pages-in-ai-answers/index.md) |
| [study1-schema-types.csv](research/data/study1-schema-types.csv) | Structured data types found on fetched pages, with bases and intervals | 11,775 | 11 | 1.8 MB | `3653ea1da9899d054cba40ae7778eea79bc5b4f4e515d652b705c122b6663bdf` | CC BY 4.0 | [Study 1](research/studies/optimized-pages-in-ai-answers/index.md) |
| [study1-llms-presence.csv](research/data/study1-llms-presence.csv) | How often a cited origin offered an llms.txt file, with bases and intervals | 1,188 | 11 | 190.7 KB | `53de0d17256d0cb74397c0556c75ff41ec5a3cc4bbdb5360fe360cac9e3bcffb` | CC BY 4.0 | [Study 1](research/studies/optimized-pages-in-ai-answers/index.md) |
| [study1-host-evidence.csv](research/data/study1-host-evidence.csv) | Per origin: whether robots.txt, sitemap.xml and llms.txt were found | 1,723 | 5 | 195.7 KB | `78d5da71ad4f4853d86603c436a74dc039f9b95217afe27a40d58c9a032ed578` | CC BY 4.0 | [Study 1](research/studies/optimized-pages-in-ai-answers/index.md) |
| [study1-wikipedia-shares.csv](research/data/study1-wikipedia-shares.csv) | Citations to Wikipedia and its sister projects, with bases and intervals | 396 | 11 | 52.9 KB | `ded8738061947acfb40125a3059d57b2ee220e118cdf97899a701fb4ed9b8196` | CC BY 4.0 | [Study 1](research/studies/optimized-pages-in-ai-answers/index.md) |
| [study1-news-hosts.csv](research/data/study1-news-hosts.csv) | Hosts classed as news, with evidence address and check date | 81 | 4 | 10.4 KB | `7eaf106a09229554581b4671720f656c3904620c80acb0f226d349baa809c82d` | CC BY 4.0 | [Study 1](research/studies/optimized-pages-in-ai-answers/index.md) |
| [study1-excluded-citations.csv](research/data/study1-excluded-citations.csv) | Citations excluded from Study 1; it holds its header and no rows | 0 | 8 | 84 bytes | `8912bf78b9779fe6d8c0f1b3d70b41653fba46b2e8c5a7e79c95a76be2434152` | CC BY 4.0 | [Study 1](research/studies/optimized-pages-in-ai-answers/index.md) |
| [page-signal-rules.json](research/data/page-signal-rules.json) | The page-signal rules frozen before collection | one record | 7 keys | 1.4 KB | `c5afcd6fd802c9cedd159f892c4754e795d26b366f2d514ee148bb822d4a0fcc` | CC BY 4.0 | [Study 1](research/studies/optimized-pages-in-ai-answers/index.md) |
| [study1-precollection-freeze.json](research/data/study1-precollection-freeze.json) | The record that the analysis files were frozen before collection began | one record | 5 keys | 724 bytes | `458805ef64751db13dff35d130dde3d8e816dc8efafbca03f4594299f86f0a7a` | CC BY 4.0 | [Study 1](research/studies/optimized-pages-in-ai-answers/index.md) |
| [study1-provenance.json](research/data/study1-provenance.json) | Collection and first-aggregation times and the hash of the original capture | one record | 21 keys | 2.7 KB | `1e58e37a103760cb881993dc9ca5ccd56c089ddd4973e2eb1d866646f16d0a0d` | CC BY 4.0 | [Study 1](research/studies/optimized-pages-in-ai-answers/index.md) |
| [registration_status.json](research/data/registration_status.json) | The registration record identifiers of Studies 1 to 3 | 3 studies | 1 key | 199 bytes | `f6ed451bb4f736c8a4dcdd402b394f36f062b27520da62c689dd7e974838fcbc` | CC BY 4.0 | [Study 1](research/studies/optimized-pages-in-ai-answers/index.md) |
| [study1-file-manifest.csv](research/data/study1-file-manifest.csv) | SHA-256, size and role of every Study 1 file | 24 | 5 | 5.3 KB | `9a6ceb1f6fb83f84a4b053f42d58950d1b61786393670770244ae3a161ab7e9a` | CC BY 4.0 | [Study 1](research/studies/optimized-pages-in-ai-answers/index.md) |

## Registered plans and the field test

Prospective designs whose outcomes are not yet computed. Their limits are on [the persistence plan](research/studies/does-absence-persist/index.md), registration OSF MKJ9V, and [the field test protocol](research/studies/evidence-refresh-field-test/index.md), registration OSF DMFPJ.

| File | What it holds | Rows | Columns | Size | SHA-256 | License | Method and limits |
| --- | --- | ---: | --- | ---: | --- | --- | --- |
| [dated-standings.csv](research/data/dated-standings.csv) | August and September 2026 named counts, bases and intervals for vendors in both releases, kept as separate dated observations | 20 | 12 | 1.4 KB | `addef6611bf9c92f2b5156d563ddabb3c28e22f78e2d68b8db5e50f92c84b756` | CC BY 4.0 | [Study 3 plan](research/studies/does-absence-persist/index.md) |
| [field-test-assignment.csv](research/data/field-test-assignment.csv) | The registered pages with their cluster, block, arm and impression stratum | 45 | 7 | 9.5 KB | `38611a5a0cbeeb971db889305c6215c643a5a60411a511b62481492fe03450a4` | CC BY 4.0 | [Field test](research/studies/evidence-refresh-field-test/index.md) |
| [field-test-interventions.json](research/data/field-test-interventions.json) | The frozen proposed edits for the field test and their placement rules | 30 edits | 4 keys | 43.4 KB | `62df4cb97e732307719e3f2fd46e4652955e421e77b2113cd08bbc868e70cfac` | CC BY 4.0 | [Field test](research/studies/evidence-refresh-field-test/index.md) |

## Evidence registry and literature records

Checks of claims and figures that circulate in the category, and the records of our literature search.

| File | What it holds | Rows | Columns | Size | SHA-256 | License | Method and limits |
| --- | --- | ---: | --- | ---: | --- | --- | --- |
| [claims.csv](research/data/claims.csv) | The GEO Claim Registry: each claim, its primary source and location, setting, verdict, check date and quotable correction | 83 | 10 | 64.7 KB | `513b9cdd0cf3acc35f12345fed55fa29d03b90e06eb2d3da7ecbe003b4269ad6` | CC BY 4.0 | [Claim Registry](research/claims/index.md) |
| [claims.json](research/data/claims.json) | The same registry as JSON, with its check date and license | 83 claims | 5 keys | 86.2 KB | `e9723bc469203ef2363e9cef3a2f219eb85ec727e730b315966b56e3324ee120` | CC BY 4.0 | [Claim Registry](research/claims/index.md) |
| [quotable-numbers.csv](research/data/quotable-numbers.csv) | Figures we consider safe to quote, each with full wording, primary source and limits | 16 | 6 | 5.5 KB | `f3bb29e0473413f1422ea9d47414fe93a0a3f0c163fae0fe52f4b32f3d5039f7` | CC BY 4.0 | [Quotable numbers](research/evidence/quotable-numbers/index.md) |
| [quotable-numbers-2026-11-03.csv](research/data/quotable-numbers-2026-11-03.csv) | The 3 November 2026 revision of that list | 15 | 6 | 4.9 KB | `81c2d04297b738c3c59bf22d086a693434c039a2171ef8379c48c5d983dccf97` | CC BY 4.0 | [Quotable numbers](research/evidence/quotable-numbers/index.md) |
| [research-errata-2026-11-03.csv](research/data/research-errata-2026-11-03.csv) | Dated errata with the wording before and after | 1 | 8 | 1.8 KB | `4122cb58ed8fb5a5e55d466a7c1bbefaa1208b1ad0f7357590e3836546c4b0c9` | CC BY 4.0 | [Unverified numbers](research/evidence/unverified-numbers/index.md) |
| [source-collection-inventory.csv](research/data/source-collection-inventory.csv) | The source documents we graded, with page counts and SHA-256 | 21 | 4 | 2.5 KB | `278c5262896a0d72893ea427eb2e2a6581b72e2fc0d33b41117d3a6990342df2` | CC BY 4.0 | [Graded sources](research/evidence/graded-sources/index.md) |
| [reading-list.csv](research/data/reading-list.csv) | A reading order for those documents, with priority pages and reading time | 21 | 6 | 5.4 KB | `65e81dd4102e9f3c2343913e23705fefd5d441c931f93bd2adc65327cc9adcbb` | CC BY 4.0 | [Reading list](research/sources/reading-list/index.md) |
| [literature-census-2026-10-30.csv](research/data/literature-census-2026-10-30.csv) | The papers screened for our GEO literature review, with decision and evidence | 61 | 13 | 42.3 KB | `9f508814db8ebcc112f85da15a451016eed648db4297d708099d574cd17e9887` | CC BY 4.0 | [GEO literature](research/insights/state-of-geo-research-2026/index.md) |
| [literature-search-log-2026-10-30.csv](research/data/literature-search-log-2026-10-30.csv) | The searches behind that census and what each service returned | 3 | 7 | 1.1 KB | `04d2b89694b63857a1bd29ec1768e8a6bdebc59686123e7efeccec392212d190` | CC BY 4.0 | [GEO literature](research/insights/state-of-geo-research-2026/index.md) |
| [target-question-inventory.csv](research/data/target-question-inventory.csv) | All September 2026 target questions with category and first word | 140 | 4 | 13.6 KB | `c8c15e992a3d32d0b875b16c2d9c4a53fea1b1248f44f744273b7b9505ff6ad4` | CC BY 4.0 | [Question playbook](research/playbooks/question-led-content/index.md) |
| [target-question-first-words.csv](research/data/target-question-first-words.csv) | How those questions begin, with counts and intervals | 5 | 7 | 583 bytes | `6b4b1ee8bb3a4723819f7d796f91a47bbb5787101f7ed82e69d45013fcac4d1c` | CC BY 4.0 | [Question playbook](research/playbooks/question-led-content/index.md) |
| [review-platform-snapshot.csv](research/data/review-platform-snapshot.csv) | The most-cited review platforms in one cut, with shares and intervals | 4 | 13 | 546 bytes | `2288c6c20642d94fdf6f8fbcf0757be975acef8b3d82159439d92218c6dfc715` | CC BY 4.0 | [Review platforms playbook](research/playbooks/review-platforms-for-b2b-software/index.md) |

## Reanalyses of published studies

Our recomputations of figures in other researchers' published work. Cite the original study as well as our table; each source review states what the original can and cannot show.

| File | What it holds | Rows | Columns | Size | SHA-256 | License | Method and limits |
| --- | --- | ---: | --- | ---: | --- | --- | --- |
| [rovira-workbook-reanalysis.csv](research/data/rovira-workbook-reanalysis.csv) | Our reanalysis of the Rovira and colleagues (2019) workbooks: query columns, positions and recomputed correlations | 9 | 11 | 1.7 KB | `e5e84410035f5f1823a16df2ba6dc07b66debf6f2b1f9335b48f2fbbfb0ee473` | CC BY 4.0 | [Rovira review](research/sources/rovira-2019/index.md) |
| [rovira-median-differences.csv](research/data/rovira-median-differences.csv) | Rows where a stored median differs from the recomputed 25-query median | 456 | 5 | 24.9 KB | `05dd0e35affaaed1a3cdd9389354eddc52eebf9425be49d8dac130ef049016ad` | CC BY 4.0 | [Rovira review](research/sources/rovira-2019/index.md) |
| [university-source-results.csv](research/data/university-source-results.csv) | The published ratings and ranks of the universities studied by Giannakoulopoulos and colleagues (2019) | 100 | 9 | 7.1 KB | `c929d70c15d09896cc8c269949c11d1578e39c0ffb80827ea6753bb14fbb7172` | CC BY 4.0 | [Giannakoulopoulos review](research/sources/giannakoulopoulos-2019/index.md) |
| [university-rank-reanalysis.csv](research/data/university-rank-reanalysis.csv) | Reported and recomputed Spearman correlations for that study | 3 | 7 | 600 bytes | `d1a7edd22751ea27455bce3cb576706b91d19b2ac1fb8d2d5378061045f9a940` | CC BY 4.0 | [Giannakoulopoulos review](research/sources/giannakoulopoulos-2019/index.md) |
| [news-commenting-2019.csv](research/data/news-commenting-2019.csv) | Commenting features reported by Karyotakis and colleagues (2019), with recomputed shares and intervals | 12 | 7 | 1.2 KB | `eb066b5c5550e423d868a69ebdcfa877c462f6c5ec51c9d8362ddae52ab1d337` | CC BY 4.0 | [Karyotakis review](research/sources/karyotakis-2019/index.md) |
| [ziakis-2019-correlations.csv](research/data/ziakis-2019-correlations.csv) | Correlations reported by Ziakis and colleagues (2019) for each ranking factor | 21 | 5 | 1.0 KB | `08827d58e729d4c9df3b347341bb2bd583a558a5eedbc7832fb58c0ad75f4ba1` | CC BY 4.0 | [Ziakis review](research/sources/ziakis-2019/index.md) |

## Operational log

A short request window from our own site, published as an observation rather than a study result. Its limits are on [the AI crawler log page](research/studies/ai-crawler-log/index.md).

| File | What it holds | Rows | Columns | Size | SHA-256 | License | Method and limits |
| --- | --- | ---: | --- | ---: | --- | --- | --- |
| [ai-crawler-log.csv](research/data/ai-crawler-log.csv) | The first AI crawler request window: recorded requests, matches to declared AI tokens, share and coverage | 1 | 13 | 605 bytes | `def944aa2c3085b70d303c9411b10ecab1c3e91b86cb5cac064117d62fc06f12` | CC BY 4.0 | [Crawler log](research/studies/ai-crawler-log/index.md) |
| [crawler-agent-definitions.csv](research/data/crawler-agent-definitions.csv) | The crawler tokens we match, with documented role, operator and documentation link | 11 | 6 | 1.7 KB | `680d333ec7bcb7b3eb6a84a10670384e8f0885677e2b388def0ae5f74e2388d6` | CC BY 4.0 | [Crawler log](research/studies/ai-crawler-log/index.md) |

## Corrections that travel with the data

Two dated notices from 3 November 2026 belong beside the report files: the [authorship correction](research/data/report-authorship-correction-2026-11-03.pdf) and the [interpretation notice](research/data/report-interpretation-notice-2026-11-03.pdf). Neither changes a data file. Figure-level corrections are in the errata table above, and each study page keeps its own correction history.

## What is not in this catalog

Client measurements are never here: client baselines, findings, question sets and outcomes need written approval before anything is published. Analysis programs and reproduction notes are published beside the tables and listed, with their hashes, in the [Study 1 manifest](research/data/study1-file-manifest.csv) and the [Study 2 manifest](research/data/study2-file-manifest.csv). Charts drawn from these tables are listed in our [chart library](chart-library.md), and the words in the column names are defined in our [AI search glossary](ai-search-glossary.md).

For an export that is not in the public package, such as a category cut or a question list, email index@broadcastwell.com.

## Sources

- Broadcastwell, [Absence Index release 2026-09](https://doi.org/10.5281/zenodo.22907695), published 23 September 2026.
- Broadcastwell, [AI search visibility: source evidence and two registered analyses](https://doi.org/10.5281/zenodo.23804758), research report, 2 November 2026.
- Broadcastwell, <a href="https://index.broadcastwell.com/data/benchmark/README.md">Index benchmark README</a>, read 9 November 2026.
- Broadcastwell, [free academic access and reuse terms](research/academic-access/index.md), 2 November 2026.
- OSF registrations [DVYFU](https://doi.org/10.17605/OSF.IO/DVYFU), [VCZKT](https://doi.org/10.17605/OSF.IO/VCZKT), [MKJ9V](https://doi.org/10.17605/OSF.IO/MKJ9V) and [DMFPJ](https://doi.org/10.17605/OSF.IO/DMFPJ).
- Row counts, column counts, sizes and SHA-256 hashes computed by us from the published bytes on 9 November 2026.

Related: our [measurement method](https://broadcastwell.com/methodology) defines how each count in these tables was taken.
