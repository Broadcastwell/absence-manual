// The docs on the brand system 3.0.0 (brief 8.7, 9.1, 9.2, 11.1). Imported by tests/site-chrome.test.mjs,
// which verify.yml runs on every pull request.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { FILES, SERVED, expectedHash, sha256 } from '../vendor/brand/sync.mjs';
import { partials, stylesheet, OUT, STYLESHEET, STYLE_PARTS, TODAY } from '../tools/brand_chrome.mjs';
import { renderNav, renderFooter } from '../vendor/brand/nav-render.mjs';

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
  assert.equal(version.version, '3.0.0');
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
  assert.ok(footer.endsWith(renderFooter(nav, { idPrefix: 'bw-footer' }) + '\n'));
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

test('SHARED_NAV is one switch, off by default, and the brand frame reads it for header and footer', () => {
  assert.match(read('mkdocs.yml'), /^  SHARED_NAV: false$/m);
  assert.equal((read('mkdocs.yml').match(/SHARED_NAV:/g) || []).length, 1);
  const frame = read('overrides/brand.html');
  assert.equal((frame.match(/\{%-? if config\.extra\.SHARED_NAV -?%\}/g) || []).length, 3);
  for (const name of ['header-shared', 'header-today', 'footer-shared', 'footer-today']) assert.ok(frame.includes(`partials/brand/${name}.html`), name);
  assert.match(read('overrides/followup.html'), /^\{% extends "brand\.html" %\}/);
  assert.match(read('overrides/404.html'), /^\{% extends "brand\.html" %\}/);
  assert.match(read('overrides/main.html'), /^\{% extends "base\.html" %\}/);
});

test('the brand navigation script needs no storage, no request and no cookie', () => {
  const script = read('vendor/brand/nav.js');
  assert.doesNotMatch(script, /document\.cookie|localStorage|sessionStorage|fetch\(|XMLHttpRequest|sendBeacon/);
  assert.match(read('overrides/brand.html'), /assets\/brand\/nav\.js' \| url\) ~ '" defer><\/script>/);
});
