// Writes the docs' header and footer partials in the brand system's markup (brief 8.7, 9.1, 9.2 and
// 11.1 step 5). Run after any change to the links below or to vendor/brand/:
//
//   node tools/brand_chrome.mjs
//
// Two variants are written, and mkdocs.yml extra.SHARED_NAV picks one at build time:
//   partials/brand/header-today.html, footer-today.html   today's links (the ones in
//       partials/site-header.html and partials/site-footer.html), drawn in the brand markup
//   partials/brand/header-shared.html, footer-shared.html  vendor/brand/nav.json, drawn by
//       vendor/brand/nav-render.mjs, the one renderer every surface uses
// tests/brand-chrome.test.mjs fails when a committed partial differs from this output.
// partials/site-header.html and partials/site-footer.html are not touched: the 45 registered
// field-study pages keep them byte for byte.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { renderNav, renderFooter } from '../vendor/brand/nav-render.mjs';
import { renderLegacyNav, renderLegacyFooter } from './legacy-chrome.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
export const OUT = 'overrides/partials/brand';
// One stylesheet for the brand pages: vendor/brand/tokens.css and vendor/brand/components.css byte
// for byte, then the docs' own layer (tools/brand-docs.css). One request instead of three; the
// font URLs in tokens.css stay relative to docs/assets/brand/, where the fonts are served.
export const STYLESHEET = 'docs/assets/brand/docs.css';
export const STYLE_PARTS = ['vendor/brand/tokens.css', 'vendor/brand/components.css', 'tools/brand-docs.css'];
export function stylesheet() {
  return Buffer.concat(STYLE_PARTS.flatMap((part, i) => [i ? Buffer.from([10]) : Buffer.alloc(0), readFileSync(join(root, part))]));
}

// Today's header and footer links on docs.broadcastwell.com, in their order today.
export const TODAY = {
  wordmark: { label: 'Broadcastwell', href: 'https://broadcastwell.com/' },
  items: [
    { label: 'Answer Operations', href: 'https://broadcastwell.com/' },
    { label: 'For agencies', href: 'https://broadcastwell.com/for-agencies' },
    { label: 'Answer Repair', href: 'https://broadcastwell.com/answer-repair' },
    { label: 'Pricing', href: 'https://broadcastwell.com/pricing' },
    { label: 'Research', href: 'https://broadcastwell.com/research' },
    { label: 'About', href: 'https://broadcastwell.com/about' }
  ],
  actions: [
    { label: 'Sign in', href: 'https://app.broadcastwell.com/signin', style: 'nav' },
    { label: 'Fix one answer, $490', href: 'https://broadcastwell.com/answer-repair', style: 'secondary' }
  ],
  menuLabel: 'Menu',
  footer: {
    before: ['<div class="bw-docs-disclosure"><p>Broadcastwell ran the measurement behind The Absence Manual and sells services in the category it measures. Broadcastwell is excluded from its own sample and from every ranking. The raw data and the analysis code are public.</p></div>'],
    // brand/ENTITY.md (brief 13.5): the brand line the other hosts' footers carry.
    brand_line: 'When you broadcast, broadcast well.',
    company: { name: 'Broadcastwell LLC', street: '517 E Kirkwood Ave', locality: 'Bloomington, IN 47408', country: 'United States', phone: '(812) 345 7272', phone_href: 'tel:+18123457272' },
    columns: [
      { title: 'Product', links: [
        { label: 'Answer Repair, $490', href: 'https://broadcastwell.com/answer-repair' },
        { label: 'Fix Sprint', href: 'https://broadcastwell.com/fix-sprint' },
        { label: 'The program', href: 'https://broadcastwell.com/pricing#program' },
        { label: 'For agencies', href: 'https://broadcastwell.com/for-agencies' },
        { label: 'Pricing', href: 'https://broadcastwell.com/pricing' },
        { label: 'PHP2Shell', href: 'https://broadcastwell.com/php2shell' },
        { label: 'The Change Desk', href: 'https://broadcastwell.com/change-desk' },
        { label: 'Connect an assistant', href: 'https://app.broadcastwell.com/connect' }
      ] },
      { title: 'Research', links: [
        { label: 'Absence Index', href: 'https://broadcastwell.com/absence-index' },
        { label: 'Public Fix', href: 'https://broadcastwell.com/public-fix' },
        { label: 'GEO Hub', href: 'https://broadcastwell.com/insights' },
        { label: 'Studies', href: 'https://broadcastwell.com/research' },
        { label: 'Methodology', href: 'https://broadcastwell.com/methodology' },
        { label: 'Data and citations', href: 'https://broadcastwell.com/data' }
      ] },
      { title: 'Free tools', links: [
        { label: 'Free 10-question check (one engine)', href: 'https://audit.broadcastwell.com/' },
        { label: 'llms.txt generator', href: 'https://app.broadcastwell.com/tools/llms-txt' },
        { label: 'Record check (free)', href: 'https://app.broadcastwell.com/tools/record-check' },
        { label: 'Agency comparisons', href: 'https://broadcastwell.com/best-geo-agencies' },
        { label: 'Sample, fictional company', href: 'https://app.broadcastwell.com/sample' },
        { label: 'Developers', href: 'https://broadcastwell.com/developers' }
      ] },
      { title: 'Company', links: [
        { label: 'About', href: 'https://broadcastwell.com/about' },
        { label: 'Company facts', href: 'https://broadcastwell.com/company-facts' },
        { label: 'Careers', href: 'https://broadcastwell.com/careers' },
        { label: 'Exchange', href: 'https://exchange.broadcastwell.com/' },
        { label: 'Partner Network', href: 'https://broadcastwell.com/partners' },
        { label: 'Security', href: 'https://broadcastwell.com/security' }
      ] },
      { title: 'Contact', links: [
        { label: 'hello@broadcastwell.com', href: 'mailto:hello@broadcastwell.com' },
        { label: 'Contact page', href: 'https://broadcastwell.com/contact' },
        { label: 'LinkedIn', href: 'https://www.linkedin.com/company/broadcastwell' },
        { label: 'Writing', href: 'https://broadcastwell.substack.com/' },
        { label: 'Sitemap', href: 'https://broadcastwell.com/sitemap' },
        { label: 'Questions and answers', href: 'https://broadcastwell.com/faq' }
      ] }
    ],
    notes: ['<p class="bw-docs-allowance"><strong>Free 10-question check (one engine):</strong> No email is needed; runs are limited per network and per day, and by the site&#39;s daily allowance.</p>'],
    legal: [
      { label: 'Privacy', href: 'https://broadcastwell.com/privacy' },
      { label: 'Terms', href: 'https://broadcastwell.com/terms' },
      { label: 'Cookies', href: 'https://broadcastwell.com/cookies' },
      { label: 'Procurement', href: 'https://broadcastwell.com/procurement' }
    ],
    copyright: 'Copyright 2026 Broadcastwell LLC.',
    // Today's dated line, unchanged: a library page shows its own date_modified; every other page
    // the reviewed date, which followup.html and business-hub.html replace as they do today.
    last: ['{% if page and (page.meta.get("library_cluster") or page.meta.get("library_hub")) %}{% set updated = page.meta.get("date_modified") | string %}{% set months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"] %}<p>Last updated <time datetime="{{ updated[:10] }}">{{ updated[8:10] | int }} {{ months[(updated[5:7] | int) - 1] }} {{ updated[:4] }}</time></p>{% else %}<p>Last updated <time datetime="2026-10-26">26 October 2026</time></p>{% endif %}']
  }
};

// Brand 3.0.2 (STEP 3.3 B117), drawn over the vendored 3.0.1 package, which stays byte for byte as
// synced: the footer legal row gains Procurement, after Integrity Standard (or last where that link is
// absent). Nothing else in the navigation changes. A package that already lists Procurement is returned
// unchanged, so vendoring 3.0.2 makes this a no-op. The wordmark's no-wrap rule is in tools/brand-docs.css.
export const PROCUREMENT = Object.freeze({ label: 'Procurement', href: 'https://broadcastwell.com/procurement' });
export function withBrand302(nav) {
  const legal = nav.footer.legal;
  if (legal.some(item => item.href === PROCUREMENT.href)) return nav;
  const after = legal.findIndex(item => item.label === 'Integrity Standard');
  const at = after < 0 ? legal.length : after + 1;
  return { ...nav, footer: { ...nav.footer, legal: [...legal.slice(0, at), { ...PROCUREMENT }, ...legal.slice(at)] } };
}

const BANNER = '{#- Generated by tools/brand_chrome.mjs from {source}. Do not edit; run node tools/brand_chrome.mjs. -#}\n';

export function partials() {
  const nav = withBrand302(JSON.parse(readFileSync(join(root, 'vendor/brand/nav.json'), 'utf8')));
  return {
    'header-today.html': BANNER.replace('{source}', 'its TODAY links') + renderLegacyNav(TODAY, { idPrefix: 'bw-nav' }) + '\n',
    'footer-today.html': BANNER.replace('{source}', 'its TODAY links') + renderLegacyFooter(TODAY, { idPrefix: 'bw-footer' }) + '\n',
    'header-shared.html': BANNER.replace('{source}', 'vendor/brand/nav.json') + renderNav(nav, { idPrefix: 'bw-nav' }) + '\n',
    'footer-shared.html': BANNER.replace('{source}', 'vendor/brand/nav.json') + renderFooter(nav, { idPrefix: 'bw-footer' }) + '\n'
  };
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  mkdirSync(join(root, OUT), { recursive: true });
  for (const [name, text] of Object.entries(partials())) writeFileSync(join(root, OUT, name), text);
  writeFileSync(join(root, STYLESHEET), stylesheet());
  console.log(`wrote ${Object.keys(partials()).length} partials to ${OUT} and ${STYLESHEET}`);
}
