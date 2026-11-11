---
title: Connect published work to a fair recheck
headline: Connect published work to a fair recheck
description: Measurement / BW-RESOURCE-06
page_class: page
schema_type: Article
learning_resource: 'true'
hide:
- navigation
- toc
date_published: '2026-09-24T00:00:00+00:00'
date_modified: '2026-11-11T07:30:00Z'
---

# Connect published work to a fair recheck

<div class="bw-learning">
<nav class="bw-learning-nav" aria-label="Learning resources"><a href="/resources/">Resources</a><a href="/resources/playbooks/">Eight playbooks</a><a href="/resources/audit/sample/">Fictional Audit</a><a href="/resources/demos/recordings/">Recorded demos</a><a href="/resources/provenance/sources/">Sources</a></nav><article><p class="eyebrow">Measurement / BW-RESOURCE-06</p><figure><img width="800" height="450" class="visual" src="/assets/learning/visuals/fair-recheck.svg" alt="Preserve baseline receipts and methods, record the exact published change, then compare matching follow-up observations. Keep failed or changed-method observations separate and measure commercial signals from their own records."><figcaption>Preserve baseline receipts and methods, record the exact published change, then compare matching follow-up observations. Keep failed or changed-method observations separate and measure commercial signals from their own records.</figcaption></figure>
<p><strong>Version:</strong> bw-content-2026-09-24-v1 | <strong>Claim ID:</strong> BW-RESOURCE-06 | <strong>Prepared:</strong> 2026-09-24</p>
<p><strong>Decision:</strong> Compare observations without claiming causality or hiding no improvement.</p>
<p>Original Broadcastwell proposed operating method. Synthetic examples illustrate the method; they are not observed client outcomes.</p>
<h2>Record two events separately</h2>
<p>A page being published and an answer changing later are different events. Preserve the baseline receipts before work begins. Then keep the actual changed file, approved wording, route, timestamp and accessible publication evidence. A draft is not published work. A correction request being sent is not a third-party listing being updated.</p>
<h2>Choose comparable records</h2>
<p>Match question wording, method, interface, provider and locale where possible. Preserve both dates. If a surface or method changes, separate that observation or clearly limit the comparison. Do not assume a model label alone proves identical conditions; record the actual method details and known differences.</p>
<h2>Read a fictional no-improvement example</h2>
<p>In the included recheck fixture, DEMO-Q-002 has a reviewed absence at baseline and at follow-up on the same fictional local surface. The summary is “no observed mention improvement in the matched fixture.” A separate question has a failed follow-up and is excluded from mention comparison, with the failure retained. No sale, ranking movement or causal effect is represented.</p>
<h2>Avoid the attractive shortcuts</h2>
<p>Do not turn missing follow-up data into zero, remove an unfavorable run or count correlated repeats as independent buyers. Report what completed and what was actually reviewed. If the evidence is too small or changed to support a useful comparison, say that directly and decide whether another bounded investigation is justified.</p>
<h2>Use appropriate primary guidance</h2>
<p>For Google Search AI features, satisfying technical eligibility does not guarantee crawling, indexing or serving. That is a reason to keep implementation acceptance separate from appearance in an answer. It is not proof that a particular change worked or failed. <a href="https://developers.google.com/search/docs/appearance/ai-features">Google Search guidance, reviewed September 24, 2026</a>.</p>
<h2>Expect movement before you change anything</h2>
<p>Added 9 November 2026. Answers move between runs even when nothing on your site changes, so a re-check needs a baseline of repeats, not one answer. In the Absence Index release 2026-09, captured 22 to 23 September 2026, 1,259 of 14,192 checked vendor, question and engine cells were mixed: the vendor was named in one or two of three valid runs, not all three or none. That is 8.9 percent, with a Wilson 95 percent interval of 8.4 to 9.4 percent. <a href="/research/data/repeat-disagreement.csv">Repeat disagreement table</a>.</p>
<table>
<caption>Mixed cells by engine, release 2026-09, three valid runs per cell</caption>
<thead><tr><th scope="col">Engine</th><th scope="col">Mixed cells</th><th scope="col">Share</th><th scope="col">Wilson 95% interval</th></tr></thead>
<tbody>
<tr><td>ChatGPT</td><td>159 of 2,860</td><td>5.6%</td><td>4.8% to 6.5%</td></tr>
<tr><td>Claude</td><td>253 of 2,860</td><td>8.8%</td><td>7.9% to 9.9%</td></tr>
<tr><td>Perplexity</td><td>200 of 2,860</td><td>7.0%</td><td>6.1% to 8.0%</td></tr>
<tr><td>Google AI Overviews</td><td>302 of 2,752</td><td>11.0%</td><td>9.9% to 12.2%</td></tr>
<tr><td>Google AI Mode</td><td>345 of 2,860</td><td>12.1%</td><td>10.9% to 13.3%</td></tr>
</tbody>
</table>
<p>Seen from one run, the effect is larger. Our <a href="/assets/research/study3/Study3_Run_to_Run_Noise_2026-09.pdf">Study 3, Run-to-run noise</a>, published 26 September 2026, found that 22.2 percent of single-run vendor namings were not repeated by both other runs of the same question on the same engine, on a base of 8,055 namings. A re-check that compares one baseline answer with one follow-up answer can therefore show a change that three runs would not.</p>
<h2>A dated check before you compare</h2>
<p>Added 9 November 2026. Write these five lines down before the follow-up runs, and keep them with the baseline receipts:</p>
<ol>
<li>The exact questions, engines and country, copied from the baseline.</li>
<li>The number of runs per question and engine on each side; our method schedules three.</li>
<li>What counts as valid, failed and excluded, so a failed follow-up stays visible instead of becoming a miss.</li>
<li>The published change, with its route and timestamp, and any engine release between the two captures from our <a href="/model-releases/">model release tracker</a>.</li>
<li>The result you will accept as no improvement, stated before you see the follow-up.</li>
</ol>
<p>Lesson 5 of our <a href="/ai-visibility-course/lesson-5-recheck-fairly/">AI visibility course</a> works through the same comparison on fictional data, and session D of our <a href="/workshops/">client training path</a> turns this list into a team decision. Visit records belong in a separate column; our <a href="/ai-referral-analytics-template/">AI referral analytics template</a> keeps them apart from answer counts.</p>
<h2>Keep revenue in its own ledger</h2>
<p>A resource completion, qualified inquiry, held conversation, invoice and collected payment are distinct commercial signals. Exclude tests and preserve unknown attribution. A later payment may matter to the business without proving this page caused it. Use the recheck worksheet to recommend continuing, revising or stopping the hypothesis; include no-improvement evidence in that decision.</p>
<h2>Use the worksheet</h2>
<p><a href="/resources/worksheets/fair-recheck/">Editable worksheet</a> | <a href="/assets/learning/worksheets/fair-recheck.json">Blank JSON</a> | <a href="/resources/audit/recheck-receipts/">Worked example</a></p>
<p>Compare one matched pair, retain exclusions and decide whether the evidence supports continuing the work.</p>
<h2>Provenance</h2>
<p>This original method extends the supplied September 24 execution-pack draft and blueprint; no competitor writing or outcome is reused. Definitions and synthetic evidence: <a href="/resources/provenance/sources/">source ledger</a>. External technical statements, where present, have nearby primary-source links. Source freshness is limited to the stated review date.</p></article>
</div>
