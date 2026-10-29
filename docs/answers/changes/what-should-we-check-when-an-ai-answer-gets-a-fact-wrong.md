---
title: What should we check when an AI answer gets a fact wrong?
headline: What should we check when an AI answer gets a fact wrong?
description: Check the exact claim, dated vendor evidence and review state. Procore had two wrong classifications among 57 extracted statements in Wrong About You.
page_class: page
schema_type: Article
date_published: '2026-10-29T16:17:32+00:00'
date_modified: '2026-10-29T16:17:32+00:00'
hide:
- navigation
library_cluster: changes
library_owner: Marcus Reed, AI Specialist
library_subtopic: Checking disputed facts
library_order: 169
demand_source: reddit
demand_evidence: LB-Q0467, private demand receipt dated 2026-10-28
also_asked_as:
- What should we check when an AI answer gets a fact wrong?
is_based_on: https://doi.org/10.5281/zenodo.23270124
evidence_kind: published-study
evidence_method_receipts:
- https://doi.org/10.5281/zenodo.23270124
---

# What should we check when an AI answer gets a fact wrong?

If you have an AI answer with a disputed fact, check the exact statement against the vendor's dated evidence before deciding what needs correction. Wrong About You classified 2 of Procore's 57 extracted statements as wrong: the underlying answers were captured on 22 September 2026 and the vendor's pages read on 8 October. Both flagged records still show team review in progress; they are evidence to inspect, not a claim that a correction has already been completed.

## What we measured

**Measured.** The [Wrong About You classification method](https://doi.org/10.5281/zenodo.23270124) records 57 Procore statements: 38 true, two wrong, none stale and 17 unverifiable. These are extracted statements, not the 109 answers that named Procore. The two wrong statements each appeared in one of three runs of the small-general-contractor comparison question.

One Claude record asserted that Procore had no pricing page. The saved vendor page contradicts that assertion. One Google AI Overview record described per-user pricing; the saved Procore source says adding users does not incur a charge. Each flag retains its question, engine, run, answer date, vendor proof and actual review state.

The classifications do not prove that either answer is still being shown or that a proposed repair will change it.

## What this means for you

**Reasoned.** Separate the two pricing questions. A page explaining how pricing is determined can exist without publishing a fixed rate card. The Claude flag concerns the existence of a pricing page, so a correction should preserve that distinction rather than inventing a public fixed price.

For the Overview flag, read the vendor passage about adding users. It addresses the per-user assertion in that record. Do not expand that passage into an unsupported statement about every component of a Procore contract; the checked evidence settles the particular claim, not the whole commercial agreement.

Keep unverifiable separate. Procore's 17 unverifiable statements did not become wrong merely because the saved vendor pages failed to settle them. Likewise, the zero stale statements in this vendor cut cannot establish that no product fact has changed since the capture.

The Claude pricing-page flag records Projul's Procore-versus-Buildertrend comparison as a cited page carrying the disputed statement. That gives the reviewer a named page to inspect alongside Procore's saved pricing page. The study's causing-page label does not prove that Claude read the Projul page as the cause of its answer.

For an agency handling either flag, include the in-progress team-review status in the handover. A published classification, a reviewed correction request and a changed served answer are separate records. The two Procore flags are not marked as completed repairs in this source.

## Also asked as

What should we check when an AI answer gets a fact wrong?

## Related

- [Wrong About You data](https://doi.org/10.5281/zenodo.23270124)
- [Procore dated record](https://index.broadcastwell.com/vendors/procore/construction-project-management/)
- [Our factual-accuracy study](../../research/study6-wrong-about-you.md)

## Next step

Use [Free 10-question check (one engine)](https://audit.broadcastwell.com/) to inspect a defined set of buyer questions. No email is needed; runs are limited per network and per day, and by the site's daily allowance.

For one documented gap, [Fix one answer, $490](https://broadcastwell.com/answer-repair). Keep the question and source receipt with the requested change.

Claiming or correcting a vendor record is free and never depends on a purchase.

[Our answer-study method, v1.1.](https://broadcastwell.com/methodology)

Prepared by the Broadcastwell team.

Page owner: Marcus Reed, AI Specialist. Corrections: hello@broadcastwell.com
