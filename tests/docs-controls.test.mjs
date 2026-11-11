// Chapter navigation on brand pages (STEP 3.3 B117, site tests D0071 and D0072). Imported by
// tests/brand-chrome.test.mjs, which tests/site-chrome.test.mjs runs on every pull request.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const read = p => readFileSync(new URL('../' + p, import.meta.url), 'utf8');

function simulate() {
  const handlers = {};
  const document = {
    activeElement: null,
    addEventListener(name, fn) { (handlers[name] ||= []).push(fn); },
  };
  function node(id) {
    const own = {};
    return { id, checked: false, attrs: {}, addEventListener(n, fn) { (own[n] ||= []).push(fn); },
      dispatchEvent(e) { for (const fn of own[e.type] || []) fn(e); }, setAttribute(n, v) { this.attrs[n] = v; },
      focus() { document.activeElement = this; } };
  }
  const drawer = node('__drawer'), button = node('chapters');
  const sections = [node('__nav_2'), node('__nav_3')];
  sections[1].checked = true;
  const navs = { '__nav_2_label': node('nav2'), '__nav_3_label': node('nav3') };
  document.getElementById = id => (id === '__drawer' ? drawer : null);
  document.querySelector = s => {
    if (s === '[data-manual-toggle="__drawer"]') return button;
    const m = s.match(/aria-labelledby="([^"]+)"/);
    return m ? navs[m[1]] || null : null;
  };
  document.querySelectorAll = s => (s === 'input.md-nav__toggle[id]' ? sections : []);
  vm.runInNewContext(read('docs/assets/brand/docs-controls.js'), { document, Event: class { constructor(type) { this.type = type; } } });
  const key = k => { for (const fn of handlers.keydown || []) fn({ key: k }); };
  return { document, drawer, button, sections, navs, key };
}

test('Escape closes the open chapter drawer and returns focus to the Chapters button', () => {
  const ui = simulate();
  let changes = 0;
  ui.drawer.addEventListener('change', () => { changes += 1; });
  ui.key('Escape');
  assert.equal(changes, 0, 'a closed drawer is left alone');
  ui.drawer.checked = true;
  ui.key('Enter');
  assert.equal(ui.drawer.checked, true);
  ui.key('Escape');
  assert.equal(ui.drawer.checked, false);
  assert.equal(changes, 1);
  assert.equal(ui.document.activeElement, ui.button);
});

test('each chapter-navigation section reports whether it is open', () => {
  const ui = simulate();
  assert.equal(ui.navs['__nav_2_label'].attrs['aria-expanded'], 'false');
  assert.equal(ui.navs['__nav_3_label'].attrs['aria-expanded'], 'true');
  ui.sections[0].checked = true;
  ui.sections[0].dispatchEvent({ type: 'change' });
  assert.equal(ui.navs['__nav_2_label'].attrs['aria-expanded'], 'true');
});

test('the brand frame loads the controls and hides the closed drawer from the keyboard', () => {
  const brand = read('overrides/brand.html');
  assert.match(brand, /assets\/brand\/docs-controls\.js' \| url \}\}" defer><\/script>/);
  const css = read('docs/assets/brand/docs.css');
  assert.ok(css.includes('.md-sidebar--primary { visibility: hidden;'));
  assert.ok(css.includes('[data-md-toggle="drawer"]:checked ~ .md-container .md-sidebar--primary { visibility: visible;'));
  const script = read('docs/assets/brand/docs-controls.js').replace(/\/\*[\s\S]*?\*\//g, '');
  assert.doesNotMatch(script, /localStorage|sessionStorage|cookie|fetch\(|XMLHttpRequest/);
});

// STEP 3.3 B126, art round 2 point 7: on wide screens the chapter list never shows half an item.
function column({ wide = true, top = 177, bottom = 500, links, active = null }) {
  const listeners = {};
  const frames = [];
  const col = {
    style: {},
    scrollTop: 400,
    getBoundingClientRect: () => ({ top, bottom }),
    querySelectorAll: s => (s === '.md-nav__link' ? links : []),
    addEventListener(n, fn) { (listeners[n] ||= []).push(fn); },
  };
  const document = {
    activeElement: active,
    addEventListener() {},
    getElementById: () => null,
    querySelector: s => (s === '.md-sidebar--primary .md-sidebar__scrollwrap' ? col : null),
    querySelectorAll: () => [],
  };
  const window = {
    matchMedia: q => ({ matches: q === '(min-width: 76.25em)' && wide }),
    requestAnimationFrame: fn => { frames.push(fn); return frames.length; },
    addEventListener(n, fn) { (listeners['window:' + n] ||= []).push(fn); },
  };
  vm.runInNewContext(read('docs/assets/brand/docs-controls.js'), { document, window, Event: class {} });
  const flush = () => { while (frames.length) frames.shift()(); };
  flush();
  return { col, listeners, flush };
}
const link = (top, height, visible = true) => ({
  getBoundingClientRect: () => ({ top, bottom: top + height, height }),
  checkVisibility: () => visible,
  contains(el) { return el === this; },
});

test('a chapter-list item either column edge would cut is hidden until it fits', () => {
  assert.equal(column({ links: [link(100, 50), link(200, 50), link(440, 50), link(490, 50), link(560, 50)] }).col.style.clipPath,
    'inset(0px 0 10px 0)');
  assert.equal(column({ links: [link(100, 50), link(150, 50), link(220, 50), link(560, 50)] }).col.style.clipPath,
    'inset(23px 0 0px 0)');
  assert.equal(column({ links: [link(160, 50), link(220, 50), link(470, 50)] }).col.style.clipPath, 'inset(33px 0 30px 0)');
});

test('collapsed sections, whole fits, narrow screens and a focused item are never clipped', () => {
  assert.equal(column({ links: [link(200, 50), link(470, 50, false), link(500, 50)] }).col.style.clipPath, '');
  assert.equal(column({ wide: false, links: [link(160, 50), link(480, 50)] }).col.style.clipPath, '');
  const focused = link(480, 50);
  assert.equal(column({ links: [link(200, 50), focused], active: focused }).col.style.clipPath, '');
});

test('on load an item cut at the top is brought into view, and scrolling trims again', () => {
  const links = [link(150, 50), link(480, 50)];
  const ui = column({ links });
  assert.equal(ui.col.style.clipPath, 'inset(23px 0 20px 0)');
  for (const fn of ui.listeners['window:load']) fn();
  ui.flush();
  assert.equal(ui.col.scrollTop, 373);
  links[0] = link(177, 50); links[1] = link(450, 50);
  for (const fn of ui.listeners.scroll) fn();
  ui.flush();
  assert.equal(ui.col.style.clipPath, '');
  assert.ok(ui.listeners['window:scroll'] && ui.listeners['window:resize'] && ui.listeners.focusin);
});
