// Today's navigation and footer links, drawn in the brand system's markup (brief 11.1: through
// steps 2 to 8 each surface keeps the links it has today, in the new style, so no fifth variant
// appears). The markup and class names are the ones vendor/brand/nav-render.mjs writes, so the
// one stylesheet (vendor/brand/components.css) and the one script (vendor/brand/nav.js) serve
// both. The shared nav.json replaces this data when the surface's SHARED_NAV switch is on.
//
// data: {
//   wordmark: { label, href },
//   items: [{ label, href, menu?: [{ label, href }] }],
//   actions: [{ label, href, style: 'nav' | 'secondary' | 'primary', attrs?: { name: value } }],
//   menuLabel: 'Menu',
//   footer: { brand_line, company: { name, street, locality, country, phone, phone_href, email?, email_href? },
//             columns: [{ title, links: [{ label, href }] }], legal: [{ label, href }], copyright,
//             notes?: [html string],    // notes: trusted, pre-escaped paragraphs kept from today's footer
//             before?: [html string],   // trusted blocks placed above the footer columns (the docs' disclosure)
//             last?: [html string] }    // trusted blocks appended to the last row (the docs' dated line)
// Local copy of sa-sites/shared/legacy-chrome.mjs for the docs, with the before and last slots added.
// }
import { escapeHtml, normalizeUrl } from '../vendor/brand/nav-render.mjs';

const ICONS = {
  chevron: '<svg class="bw-icon" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M4 6l4 4 4-4"/></svg>',
  menu: '<svg class="bw-icon bw-icon--24" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
};

function current(href, page) {
  return page && href && !/#/.test(href) && normalizeUrl(href) === normalizeUrl(page) ? ' aria-current="page"' : '';
}
function attrs(extra) {
  return Object.entries(extra || {}).map(([k, v]) => v === true ? ` ${escapeHtml(k)}` : ` ${escapeHtml(k)}="${escapeHtml(v)}"`).join('');
}
function link(cls, item, page) {
  return `<a${cls ? ` class="${cls}"` : ''} href="${escapeHtml(item.href)}"${current(item.href, page)}${attrs(item.attrs)}>${escapeHtml(item.label)}</a>`;
}
function button(a, extra = '') {
  const cls = a.style === 'primary' ? 'bw-button bw-button--primary' : 'bw-button bw-button--secondary';
  return `<a class="${cls}${extra}" href="${escapeHtml(a.href)}"${attrs(a.attrs)}>${escapeHtml(a.label)}</a>`;
}

export function renderLegacyNav(data, { current: page = '', idPrefix = 'bw-nav', skipTarget = '#main', skipLabel = 'Skip to content' } = {}) {
  const prefix = String(idPrefix).replace(/[^A-Za-z0-9_-]/g, '');
  const navActions = data.actions.filter(a => a.style === 'nav');
  const buttons = data.actions.filter(a => a.style !== 'nav');
  const primary = buttons.find(a => a.style === 'primary');
  const desktop = data.items.map((item, i) => {
    if (!item.menu) return `<li>${link('bw-site-nav__trigger', item, page)}</li>`;
    const entries = item.menu.map(e => `<li>${link('bw-site-nav__link', e, page)}</li>`).join('');
    return `<li><details class="bw-site-nav__menu" data-bw-menu><summary class="bw-site-nav__trigger" id="${prefix}-menu-${i}">${escapeHtml(item.label)}${ICONS.chevron}</summary><ul class="bw-site-nav__panel" aria-labelledby="${prefix}-menu-${i}">${entries}</ul></details></li>`;
  }).join('');
  const phone = data.items.map(item => {
    if (!item.menu) return `<li>${link('bw-site-nav__link', item, page)}</li>`;
    return `<li><details class="bw-site-nav__group" data-bw-menu><summary>${escapeHtml(item.label)}${ICONS.chevron}</summary><ul>${item.menu.map(e => `<li>${link('bw-site-nav__link', e, page)}</li>`).join('')}</ul></details></li>`;
  }).join('');
  return [
    `<a class="bw-skip" href="${escapeHtml(skipTarget)}">${escapeHtml(skipLabel)}</a>`,
    `<header class="bw-site-nav" data-bw-nav>`,
    `<div class="bw-container bw-site-nav__bar">`,
    `<a class="bw-logotype" href="${escapeHtml(data.wordmark.href)}"${current(data.wordmark.href, page)}>${escapeHtml(data.wordmark.label)}</a>`,
    `<nav class="bw-site-nav__primary" aria-label="Main"><ul class="bw-site-nav__list">${desktop}</ul></nav>`,
    `<div class="bw-site-nav__actions">${navActions.map(a => link('bw-site-nav__action', a, page)).join('')}${buttons.map(a => button(a)).join('')}</div>`,
    primary ? button(primary, ' bw-site-nav__phone-start') : (buttons[0] ? button(buttons[0], ' bw-site-nav__phone-start') : ''),
    `<details class="bw-site-nav__phone" data-bw-phone-menu><summary class="bw-site-nav__menu-button">${ICONS.menu}<span>${escapeHtml(data.menuLabel || 'Menu')}</span></summary>`,
    `<div class="bw-site-nav__sheet"><nav aria-label="Main">`,
    buttons.length ? `<div class="bw-site-nav__doors">${buttons.map(a => button(a, ' bw-button--block')).join('')}</div>` : '',
    `<ul class="bw-site-nav__groups">${phone}</ul>`,
    navActions.length ? `<ul class="bw-site-nav__more">${navActions.map(a => `<li>${link('bw-site-nav__link', a, page)}</li>`).join('')}</ul>` : '',
    `</nav></div></details>`,
    `</div>`,
    `</header>`
  ].join('');
}

export function renderLegacyFooter(data, { current: page = '', idPrefix = 'bw-footer' } = {}) {
  const f = data.footer;
  const c = f.company;
  const prefix = String(idPrefix).replace(/[^A-Za-z0-9_-]/g, '');
  const columns = f.columns.map((column, i) => `<div><h2 class="bw-site-footer__title" id="${prefix}-${i}">${escapeHtml(column.title)}</h2><ul class="bw-site-footer__list" aria-labelledby="${prefix}-${i}">${column.links.map(item => `<li>${link('', item, page)}</li>`).join('')}</ul></div>`).join('');
  const contact = [`${escapeHtml(c.name)}, ${escapeHtml(c.street)}, ${escapeHtml(c.locality)}, ${escapeHtml(c.country)}`, c.phone ? `<a href="${escapeHtml(c.phone_href)}">${escapeHtml(c.phone)}</a>` : '', c.email ? `<a href="${escapeHtml(c.email_href)}">${escapeHtml(c.email)}</a>` : ''].filter(Boolean).join('<br>');
  return [
    `<footer class="bw-site-footer">`,
    `<div class="bw-container">`,
    (f.before || []).join(''),
    `<div class="bw-site-footer__top">`,
    `<div class="bw-site-footer__brand">`,
    `<a class="bw-logotype" href="${escapeHtml(data.wordmark.href)}">${escapeHtml(data.wordmark.label)}</a>`,
    f.brand_line ? `<p class="bw-site-footer__line">${escapeHtml(f.brand_line)}</p>` : '',
    `<address class="bw-site-footer__address">${contact}</address>`,
    `</div>`,
    `<nav class="bw-site-footer__columns" aria-label="Footer">${columns}</nav>`,
    `</div>`,
    (f.notes || []).join(''),
    `<div class="bw-site-footer__last"><ul class="bw-site-footer__legal" aria-label="Legal and site">${f.legal.map(item => `<li>${link('', item, page)}</li>`).join('')}</ul>${f.copyright ? `<p>${escapeHtml(f.copyright)}</p>` : ''}${(f.last || []).join('')}</div>`,
    `</div>`,
    `</footer>`
  ].join('');
}
