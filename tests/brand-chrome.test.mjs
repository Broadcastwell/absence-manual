// The docs on the brand system 3.0.0 (brief 8.7, 9.1, 9.2, 11.1). Imported by tests/site-chrome.test.mjs,
// which verify.yml runs on every pull request.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { FILES, SERVED, expectedHash, sha256 } from '../vendor/brand/sync.mjs';
import * as chrome from '../tools/brand_chrome.mjs';
import { partials, stylesheet, OUT, STYLESHEET, STYLE_PARTS, TODAY } from '../tools/brand_chrome.mjs';
import { renderNav, renderFooter } from '../vendor/brand/nav-render.mjs';
import './docs-controls.test.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const read = p => readFileSync(join(root, p), 'utf8');
const vendor = join(root, 'vendor', 'brand');
const version = JSON.parse(readFileSync(join(vendor, 'VERSION.json'), 'utf8'));
const vendored = JSON.parse(readFileSync(join(vendor, 'VENDORED.json'), 'utf8'));
const nav = JSON.parse(readFileSync(join(vendor, 'nav.json'), 'utf8'));
const links = html => [...html.matchAll(/<a\b[^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/g)].map(m => [m[2].replace(/<wbr\s*\/?>/g, '').replace(/<[^>]+>/g, '').replace(/&#39;/g, "'").replace(/&amp;/g, '&').trim(), m[1]]);

test('the vendored brand package names the version it was copied from', () => {
  assert.equal(vendored.version, version.version);
  assert.equal(vendored.built_at, version.built_at);
  assert.equal(version.version, '3.0.2');
});

// Brand 3.0.2 (STEP 3.3 B146) carries the two changes B117 drew over 3.0.1 by hand, so the docs draw the
// vendored files alone: Procurement in the shared footer's legal row, and a wordmark that never wraps.
test('brand 3.0.2 carries Procurement and the one-line wordmark itself, with no docs overlay', () => {
  const legal = nav.footer.legal.map(item => item.label);
  assert.equal(legal.indexOf('Procurement'), legal.indexOf('Integrity Standard') + 1);
  assert.equal(chrome.withBrand302, undefined, 'the B117 Procurement overlay is gone');
  assert.equal(chrome.PROCUREMENT, undefined);
  const logotype = read('vendor/brand/components.css').match(/^\.bw-logotype\{([^}]*)\}/m)[1];
  assert.match(logotype, /(^|;)white-space:nowrap(;|$)/);
  assert.match(logotype, /(^|;)flex-shrink:0(;|$)/);
  assert.doesNotMatch(read('tools/brand-docs.css'), /\.bw-logotype\s*\{[^}]*white-space/, 'the docs layer adds no wordmark override');
});

test('every vendored brand file is present and byte-identical to VERSION.json', () => {
  assert.deepEqual(Object.keys(vendored.files).sort(), Object.keys(FILES).sort());
  for (const [name, from] of Object.entries(FILES)) {
    const file = join(vendor, name);
    assert.ok(existsSync(file), `${name} is missing from vendor/brand`);
    assert.equal(vendored.files[name].from, from);
    assert.equal(sha256(file), expectedHash(version, from), `${name} differs from VERSION.json`);
  }
});

test('every served brand file equals its vendored copy', () => {
  for (const [served, name] of Object.entries(SERVED)) {
    assert.equal(sha256(join(root, served)), sha256(join(vendor, name)), `${served} drifted from vendor/brand/${name}`);
  }
});

test('the served brand stylesheet is tokens.css and components.css byte for byte, then the docs layer', () => {
  assert.deepEqual(STYLE_PARTS, ['vendor/brand/tokens.css', 'vendor/brand/components.css', 'tools/brand-docs.css']);
  const served = readFileSync(join(root, STYLESHEET));
  assert.ok(served.equals(stylesheet()), `${STYLESHEET} is stale; run node tools/brand_chrome.mjs`);
  const tokens = readFileSync(join(vendor, 'tokens.css'));
  const components = readFileSync(join(vendor, 'components.css'));
  assert.ok(served.subarray(0, tokens.length).equals(tokens));
  assert.ok(served.subarray(tokens.length + 1, tokens.length + 1 + components.length).equals(components));
  const layer = read('tools/brand-docs.css');
  assert.doesNotMatch(layer, /linear-gradient|radial-gradient|text-transform:\s*uppercase|letter-spacing:\s*0\.\d+em|#[0-9a-fA-F]{3,8}\b/, 'the docs layer uses tokens only, no gradient and no capitals');
  assert.doesNotMatch(layer, /\bInter\b|Roboto|Poppins|Playfair/, 'no face outside Geist and Newsreader');
});

// The token test of brief 8.7 (STEP 3.3 B146): the theme's em and rem spacing, the drawer backdrop, the resource
// headline and the one inline chart are set to brand tokens in the docs layer; the theme's files are not edited.
test('the docs layer puts the theme on the brand tokens', () => {
  const layer = read('tools/brand-docs.css');
  const token = layer.slice(layer.indexOf('/* ---------- the theme on the brand tokens'));
  assert.ok(token.length > 200, 'the token section is missing');
  for (const rule of [
    '.md-nav__link { margin-top: var(--bw-space-8); }',
    '.md-nav__item--section { margin: var(--bw-space-24) 0; }',
    ':where(.md-typeset) :where(p) { margin-block: var(--bw-space-24); }',
    '[dir=ltr] .md-typeset :is(ul, ol) { margin-left: var(--bw-space-8); }',
    '[dir=ltr] .md-typeset :is(ul, ol) li { margin-left: var(--bw-space-24); }',
    '[dir=ltr] .md-typeset .headerlink { margin-left: var(--bw-space-8); }',
    '.md-overlay { background-color: var(--bw-color-ink); }',
    '.md-content__inner:has(.bw-learning) > h1 { font-size: var(--bw-text-61); line-height: var(--bw-leading-61); }',
    '.md-typeset figure > svg text { font-size: var(--bw-text-13); }'
  ]) assert.ok(token.includes(rule), rule);
  // Every length and color in the section is a token: no px, em or rem value outside var(), and no color
  // literal. The chart footnote's move to the left edge is a position, not a design value.
  const values = token.replace(/\/\*[\s\S]*?\*\//g, '').replace(/@media[^{]*\{/g, '').replace(/\[[^\]]*\]/g, '');
  for (const [, property, value] of values.matchAll(/([a-z-]+)\s*:\s*([^;{}]+);/g)) {
    if (property === 'transform') continue;
    assert.doesNotMatch(value.replace(/var\([^)]*\)/g, ''), /\d(px|em|rem)\b|rgba?\(|#/, property + ': ' + value);
  }
});

test('the committed header and footer partials are the generator output', () => {
  for (const [name, text] of Object.entries(partials())) {
    assert.equal(read(`${OUT}/${name}`), text, `${OUT}/${name} is stale; run node tools/brand_chrome.mjs`);
  }
});

test("today's partials keep every link of today's header and footer, in order, in the brand markup", () => {
  const oldHeader = read('overrides/partials/site-header.html');
  const oldFooter = read('overrides/partials/site-footer.html');
  const header = read(`${OUT}/header-today.html`);
  const footer = read(`${OUT}/footer-today.html`);
  const desktop = header.slice(header.indexOf('<nav class="bw-site-nav__primary"'), header.indexOf('</nav>') + 6);
  const oldDesktop = oldHeader.match(/<nav class="bw-shared-nav"[^>]*>([\s\S]*?)<\/nav>/)[1];
  assert.deepEqual(links(desktop), links(oldDesktop));
  assert.match(header, /<a class="bw-site-nav__action" href="https:\/\/app\.broadcastwell\.com\/signin">Sign in<\/a>/);
  assert.match(header, /<a class="bw-button bw-button--secondary" href="https:\/\/broadcastwell\.com\/answer-repair">Fix one answer, \$490<\/a>/);
  for (const pair of links(oldHeader)) assert.ok(links(header).some(p => p[1] === pair[1]), `header lost ${pair[1]}`);
  const oldColumns = [...oldFooter.matchAll(/<h2 id="bw-footer-\d">([^<]+)<\/h2><\/summary><ul[^>]*>([\s\S]*?)<\/ul>/g)].map(m => [m[1], links(m[2])]);
  const newColumns = [...footer.matchAll(/<h2 class="bw-site-footer__title" id="bw-footer-\d">([^<]+)<\/h2><ul[^>]*>([\s\S]*?)<\/ul>/g)].map(m => [m[1], links(m[2])]);
  assert.equal(oldColumns.length, 5);
  assert.deepEqual(newColumns, oldColumns);
  for (const pair of links(oldFooter.replace(/\{%[\s\S]*?%\}|\{\{[\s\S]*?\}\}/g, ''))) assert.ok(links(footer).some(p => p[1] === pair[1]), `footer lost ${pair[1]}`);
  assert.match(footer, /Broadcastwell is excluded from its own sample and from every ranking/);
  assert.ok(footer.indexOf('excluded from its own sample') < footer.indexOf('bw-site-footer__columns'), 'the disclosure stays above the columns');
  assert.match(footer, /<time datetime="2026-10-26">26 October 2026<\/time>/, 'business-hub.html still finds the date it replaces');
  assert.match(footer, /<li><a href="https:\/\/www\.linkedin\.com\/company\/broadcastwell">LinkedIn<\/a><\/li><li><a href="https:\/\/broadcastwell\.substack\.com\/">Writing<\/a><\/li>/, 'followup.html still adds X and TikTok');
  assert.equal(TODAY.items.length, 6);
});

test('the shared partials are brand/nav.json through the one renderer, with no fifth variant', () => {
  const header = read(`${OUT}/header-shared.html`);
  const footer = read(`${OUT}/footer-shared.html`);
  assert.ok(header.endsWith(renderNav(nav, { idPrefix: 'bw-nav' }) + '\n'));
  // Brand 3.0.2: the vendored legal row lists Procurement after Integrity Standard (STEP 3.3 B146).
  assert.ok(footer.endsWith(renderFooter(nav, { idPrefix: 'bw-footer' }) + '\n'));
  assert.ok(footer.includes('<li><a href="https://broadcastwell.com/integrity">Integrity Standard</a></li><li><a href="https://broadcastwell.com/procurement">Procurement</a></li>'));
  assert.equal((footer.match(/>Procurement</g) || []).length, 1);
  const want = [nav.wordmark, ...nav.items.flatMap(i => i.menu ? i.menu : [i]), ...nav.actions].map(i => i.href);
  for (const href of want) assert.ok(header.includes(`href="${href}"`), `shared header lacks ${href}`);
  for (const column of nav.footer.columns) for (const item of column.links) assert.ok(footer.includes(`href="${item.href}"`), `shared footer lacks ${item.href}`);
  for (const name of ['header-today.html', 'header-shared.html']) {
    const text = read(`${OUT}/${name}`);
    assert.equal((text.match(/<header /g) || []).length, 1);
    assert.match(text, /^\{#-[^\n]*-#\}\n<a class="bw-skip" href="#main">Skip to content<\/a><header class="bw-site-nav" data-bw-nav>/);
    assert.doesNotMatch(text, /bw-shared-|style=|<script/);
  }
});

test('SHARED_NAV is one switch and the brand frame reads it for header, footer and search', () => {
  assert.match(read('mkdocs.yml'), /^  SHARED_NAV: (true|false)$/m);
  assert.equal((read('mkdocs.yml').match(/SHARED_NAV:/g) || []).length, 1);
  const frame = read('overrides/brand.html');
  assert.equal((frame.match(/\{%-? if config\.extra\.SHARED_NAV -?%\}/g) || []).length, 3);
  for (const name of ['header-shared', 'header-today', 'footer-shared', 'footer-today']) assert.ok(frame.includes(`partials/brand/${name}.html`), name);
  assert.equal((frame.match(/"material\/search" in config\.plugins and not config\.extra\.SHARED_NAV/g) || []).length, 2, 'the manual search panel and button are drawn only with the switch off');
  assert.match(read(`${OUT}/header-shared.html`), /href="https:\/\/app\.broadcastwell\.com\/search"/);
  assert.match(read('overrides/followup.html'), /^\{% extends "brand\.html" %\}/);
  assert.match(read('overrides/404.html'), /^\{% extends "brand\.html" %\}/);
  assert.match(read('overrides/main.html'), /^\{% extends "base\.html" %\}/);
});

test('the brand navigation script needs no storage, no request and no cookie', () => {
  const script = read('vendor/brand/nav.js');
  assert.doesNotMatch(script, /document\.cookie|localStorage|sessionStorage|fetch\(|XMLHttpRequest|sendBeacon/);
  assert.match(read('overrides/brand.html'), /assets\/brand\/nav\.js' \| url\) ~ '" defer><\/script>/);
});
