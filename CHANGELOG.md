# Changelog

Version numbers change. URLs never do. A chapter slug published once is
permanent.

## Offer and phone update, 26 September 2026

- The header button and the next step under every chapter now go to the $490
  Category Audit at https://broadcastwell.com/buy/audit. The hold notice and
  both "check availability" email buttons are gone. The AI Visibility
  Diagnostic shows one Paused state until the next Audit delivery.
- llms.txt opens with a dated "Current prices and terms (26 Sep 2026)" block,
  gives the /buy address instead of any checkout address, states the current
  Index release and DOI, and uses the one team sentence.
- The front page offer section and the buyer page carry the same state and the
  one line on the API, webhooks and connector already public on /developers.
- Phones: the reading column gets a 16 px gutter on each side below 720 px, and
  a wide table scrolls inside its own box instead of running off the page.
- The build now fails on a direct checkout address, a mailto used as a buy
  button, the retired availability wording, or an llms.txt without the dated
  block.

## Version 1.0, 18 August 2026

The complete manual. Thirteen chapters, five appendices, one buyer page, one
landing page and two standalone notes, all published at
docs.broadcastwell.com and all free and ungated.

- Chapters 0 to 12, each at its own permanent slug, drawn from The 2026 State
  of GEO, Volumes I, II and III.
- Appendices A to E: the ten-question buyer bank, the absence classification
  rules and their precedence, the scoring and matching specification, the
  glossary, and the references with the self-audit disclosure.
- A buyer page at /for-buyers/ in plain language, and two standalone notes cut
  from Chapters 2 and 6.
- Every substantive claim carries an evidence level: measured with the volume
  named, reported with the external source named, or reasoned. The buyer page
  is the one deliberate exception and carries none.
- Eight figures, each copied unmodified from the source repository, each with
  alt text that states the finding rather than the chart type.
- The whole manual is also published as one ungated PDF, generated from the
  same markdown in the same build so the two cannot drift.
- Open flags are recorded in FLAGS.md where a published source is missing a
  figure or two published sources disagree. None was reconciled.
- The build fails if the manual stops being ungated, crawlable or extractable
  without JavaScript, if a chapter falls under its word floor, if a figure
  ships without alt text, or if the PDF is missing or has fallen behind the
  pages.
