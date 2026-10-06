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

- Prices, the only ones allowed (Sairam's ruling of 5 Oct 2026, section 0): $490 Category Audit; $2,900 Fix Sprint (by conversation); $13,500 program per 90 days, billed $4,500 monthly (by conversation); agency wholesale $1,000 per client per month for the first client, then $490; $190 Index Brief; $490 white-label Category Audit; $490 Second Opinion; $1,960 Portfolio Scan. The AI Visibility Diagnostic is retired and the AI Fact Check is not for sale: neither is shown as an offer. The one credit line is "The $490 credits once against the $2,900 Fix Sprint within 30 days of delivery, so the Sprint is $2,410."
- Five engines, always by name: ChatGPT, Claude, Perplexity, Google AI Overviews and Google AI Mode. "Free 10-question check (one engine)", never "free audit".
- Never in Broadcastwell's own words: em dashes, double hyphens, "founder-led", "early-stage", "startup", "studio", "boutique", "solo", "$1,500", "four engines", "120 observed answers", "free audit", "against the first month", "three month minimum", any model string, workflow ids, any guaranteed placement, any traffic or revenue result for a client. The team sentence is "Broadcastwell is a team of consultants and engineers. Sairam Sivakumar, Founder, is accountable for every order."
- Quoted evidence stays verbatim: an engine's answer, a cited title, a seller's price or product name in a study. The rules govern Broadcastwell's own text around it.

## Files that are rendered elsewhere

- The sample findings PDFs in `docs/assets/samples/` are rendered by the delivery tools (FINISH `render_findings_v2.py` plus `render_local.mjs`). Before replacing one, open it and scan its text for mis-encoded sequences (for example the three characters that a wrong encoding makes of an ellipsis or a middle dot). On 28 Sep 2026 all three samples carried them and were re-printed; see CHANGELOG.
