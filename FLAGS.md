# Open flags on version 1.0

Every statistic in this manual traces to a published figure in one of the three
State of GEO volumes or their released datasets. Where a number is missing, or
two published sources disagree, the gap is recorded here rather than filled with
a plausible value, and nothing on this list has been silently reconciled. A
human should resolve each of these before any figure on the list is promoted.

## FLAG 1. The Volume II DOI. RESOLVED, 18 August 2026

**Status.** Resolved in favour of what the manual already published. Nothing was
changed in any page.

**What Zenodo says.** Queried directly against the Zenodo record API on
18 August 2026. Every one of these records reports the same `conceptrecid`,
21537013, which is what makes `10.5281/zenodo.21537013` the concept DOI for the
series rather than a version of it.

| Record | Zenodo `doi` | Zenodo `version` | `conceptrecid` | Is the concept record |
|-|-|-|-|-|
| 21537013 | resolves to the latest version, currently 3.0 | 3.0 | 21537013 | yes |
| 21537014 | 10.5281/zenodo.21537014 | v1.0 | 21537013 | no |
| 21586091 | 10.5281/zenodo.21586091 | v2.0 | 21537013 | no |
| 21789120 | 10.5281/zenodo.21789120 | v3.0 | 21537013 | no |

Zenodo gives publication dates of 2026-07-24 for v1.0, 2026-07-26 for v2.0 and
2026-08-04 for v3.0.

**Conclusion.** `10.5281/zenodo.21586091` is the version DOI for Volume II, which
is what the manual cites. `10.5281/zenodo.21537013` is the concept DOI covering
all versions and is not a volume, which is why the source project's own
verification rule forbids citing it in place of a version DOI. The manual cites
it nowhere.

**Scope checked.** The Volume II DOI appears in six files: the volume table in
`docs/index.md`, the repeated "About this manual" block in the four chapter and
note pages, and the publisher `sameAs` list in `overrides/main.html`. The
repeated block itself appears in exactly four files, which matches what Run 1
reported. All six carry the correct identifier and none was edited.

## FLAG 2. Volume III answer counts do not reconcile

**Where.** The Volume III row of the volume table, and the section "What went
wrong during collection, stated plainly" in Chapter 6 and in the note cut from
it.

**The disagreement.** Volume III states that all 853 collected answers are
released. It separately states the study holds 18 ChatGPT, 280 Claude, 175
Perplexity and 280 Google AI Overviews answers, which sums to 753. Its own
results table then gives answered counts of 18, 280, 157 and 258, which sums to
713, the difference being 18 rows carrying an API error on Perplexity and 22
questions on which Google returned no AI Overview. A fourth figure, 808, appears
as the count of answers the second extraction layer covered.

**What was published, and why.** Chapter 6 quotes the 18 / 280 / 175 / 280
holdings and, three sections later, the 258 of 280 and 92.1% AI Overview figures.
Both are Volume III's own numbers on Volume III's own denominators, and the
chapter makes no claim about how they relate. The repeat runs of the
25-question stability subsample are the obvious candidate for the difference
between 853 and the rest, but Volume III does not say so and this manual does
not say so on its behalf.

## FLAG 3. Volume I answer count against its own question count

**Where.** The Volume I row of the volume table on the landing page.

**The disagreement.** Volume I reports 85 companies, ten standardised buyer
questions each, and 860 scored AI answers. 85 times 10 is 850. Volume II's
completeness check, which passed for all 85 companies with zero mismatches,
uses absence count equals ten minus the visibility score, which implies ten
scored answers per company and 850 in total.

**What was published, and why.** The landing page carries Volume I's own figure
of 860 scored answers and does not restate the ten-questions-each figure in the
same sentence, so the manual is not asserting a product that does not hold.
Chapter 2 states its own base as 616 absence records out of 85 companies, which
is unaffected either way.

## FLAG 4. Volume III's stated collection duration

**Where.** Chapter 6 and the note cut from it, in the method section and in the
limitations.

**The disagreement.** Volume III describes its collection window as 05:28 to
16:29 UTC on 2026-08-04 and calls it a window of about four hours. Those
timestamps are about eleven hours apart.

**What was published, and why.** The manual quotes the timestamps, which are
unambiguous, and does not repeat the duration. Confirm which is correct.

## FLAG 5. The date on the published self-audit

**Where.** The "About this manual" block on every page.

**What is needed.** A published date for the four-engine, five-run self-audit.

**The gap.** The operator disclosure sentence in Volume III says the self-audit
was published alongside Volume 2 and gives no month. July 2026 is taken from the
Volume II citation metadata in the released dataset, which gives a release date
of 24 July 2026. It is inferred from a published file rather than quoted from a
paper.

## FLAG 6. The unique-domain count

**Where.** The Volume I row of the volume table on the landing page.

**The gap.** 5,160 citations is stated in the Volume II paper body. 1,753 unique
cited domains appears in the Volume I dataset README rather than in a paper
body. Both are published in the open release. If the manual is ever held to
paper-body sourcing only, that figure is the one that does not qualify.

## FLAG 7. The August 2026 re-measure is one run, not five

**Where.** The "About this manual" block on every page, second self-audit line.

**The gap.** The published figure of 0 of 200 answers and 0 of 663 citations
comes from a four-engine, five-run structure. The re-measure of 18 August 2026
used the same ten published questions and the same four engines but one run per
question, giving 40 answers, because the existing measurement is capped at forty
calls and lifting that cap would have meant altering it. The two lines are
therefore not directly comparable and both are published with their dates and
their run structure stated.
