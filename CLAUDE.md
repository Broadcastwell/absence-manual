# CLAUDE.md: rules for every session in absence-manual (docs.broadcastwell.com)

These rules come from the owner's standing brief (ZENITH, 28 Sep 2026). They override defaults. If a task conflicts with them, stop and say so.

## Money and secrets

- $0 new spend. No purchase, trial, upgrade, plan change, credit top-up, new paid API key, domain, seat or subscription. Free open-source packages are not spend. Anything that asks for a card goes to the owner with the exact cost.
- Never read, print, copy, rotate or create a secret, and never open a `.dev.vars` or token file.

## Lanes

- This repository is The Absence Manual and its public assets (research PDFs and charts, sample findings packs, llms.txt). The site (broadcastwell.com, Framer), the app, bw-index-site, n8n, mailboxes and Stripe are other lanes.
- URLs never change. A published file name keeps resolving; a renamed file is added beside the old name, never moved.

## Build and deploy

- GitHub Pages builds `main` (`.github/workflows/deploy.yml`: `mkdocs build`, `python tools/build_pdf.py`, `python tools/verify_build.py`). Every other branch runs the same build as `Verify manual pull request`. There is no preview URL; the verify run and its `manual-site-preview` artifact are the preview.
- Merges to `main` go through a reviewed pull request by the owner.
- `tools/verify_build.py` fails on a direct checkout address, a mailto buy button, retired offer wording, or an llms.txt without its dated "Current prices and terms" block. Keep it passing; never weaken it.

## Copy rules (every string a reader can see, including llms.txt, PDFs and chart text)

- Prices and offers (Sairam's ruling, 5 November 2026): Answer Repair $490 once; Agency Deadline Audit $490 per client report; Fix Sprint $3,900 ($3,410 after the $490 credit); Care $490 a month; Program $5,500 a month; 150-page build $6,000 plus $250 a page; one live buyer question $19 once. $19 once, credited in full against Answer Repair within 30 days of payment for the same account, so the repair then costs $471. One buyer question of your choosing: five engines (ChatGPT, Claude, Perplexity, Google AI Overviews and Google AI Mode), three repeats and 15 planned answers with receipts, delivered within 24 hours of payment. If we do not deliver within 24 hours of payment, we refund the $19 in full. Anything not listed is retired and cannot be bought. Offer links go to https://broadcastwell.com/answer-repair.
- Five engines, always by name: ChatGPT, Claude, Perplexity, Google AI Overviews and Google AI Mode. "Free 10-question check (one engine)", never "free audit".
- Never in Broadcastwell's own words: em dashes, double hyphens, "founder-led", "early-stage", "startup", "studio", "boutique", "solo", "$1,500", "four engines", "120 observed answers", "free audit", "against the first month", "three month minimum", any model string, workflow ids, any guaranteed placement, any traffic or revenue result for a client. The team sentence is "Broadcastwell is a team of consultants and engineers. Sairam Sivakumar, Founder, is accountable for every order."
- Quoted evidence stays verbatim: an engine's answer, a cited title, a seller's price or product name in a study. The rules govern Broadcastwell's own text around it.

## Files that are rendered elsewhere

- The sample findings PDFs in `docs/assets/samples/` are rendered by the delivery tools (FINISH `render_findings_v2.py` plus `render_local.mjs`). Before replacing one, open it and scan its text for mis-encoded sequences (for example the three characters that a wrong encoding makes of an ellipsis or a middle dot). On 28 Sep 2026 all three samples carried them and were re-printed; see CHANGELOG.
