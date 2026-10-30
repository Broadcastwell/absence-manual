// Published September name/domain matching definition. Pure, offline study instrument.
import {isIP} from "node:net";
const fail=message=>{throw new Error(message);};
const requireThat=(condition,message)=>{if(!condition)fail(message);};
const nonempty=value=>typeof value==="string"&&value.trim().length>0;
export function publicHost(value) {
  return typeof value === 'string' && value.length <= 253 && !isIP(value) &&
    /^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$/.test(value) &&
    !/(?:^|\.)(?:localhost|local|internal|invalid|test|onion)$/.test(value);
}
function citedHost(raw) {
  requireThat(nonempty(raw), 'cited_urls must contain strings');
  let u; try { u = new URL(raw); } catch { fail('Invalid cited URL: ' + raw); }
  requireThat(['https:', 'http:'].includes(u.protocol) && !u.username && !u.password && !u.port, 'Unsupported cited URL');
  return publicHost(u.hostname) ? u.hostname.replace(/^www\./, '') : null;
}
const hostWithin = (host, domain) => host === domain || host?.endsWith('.' + domain);
const regexEscape = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
function exactMatches(text, name) {
  const re = new RegExp('(?<![\\p{L}\\p{N}_])' + regexEscape(name) + '(?![\\p{L}\\p{N}_])', 'giu');
  return [...text.matchAll(re)];
}
export function matchVendor(v, text, citedUrls) {
  const hosts = [...new Set(citedUrls.map(citedHost).filter(Boolean))];
  const supported = hosts.filter(h => [v.canonical_domain, ...v.alias_domains, ...v.product_hosts].some(d => hostWithin(h, d)));
  const matches = [...new Set([v.name, ...v.name_aliases])].flatMap(n => exactMatches(text, n));
  const canonicalCited = hosts.some(h => hostWithin(h, v.canonical_domain));
  const named = matches.some(m => {
    if (!v.plain_word || canonicalCited) return true;
    // Qualifier within five whitespace-separated tokens of this exact match, same sentence.
    const before = text.slice(0, m.index).split(/[.!?;\n]/).at(-1).trim().split(/\s+/).slice(-5).join(' ');
    const after = text.slice(m.index + m[0].length).split(/[.!?;\n]/)[0].trim().split(/\s+/).slice(0, 5).join(' ');
    return v.qualifiers.some(q => exactMatches(before, q).length || exactMatches(after, q).length);
  });
  return {named, cited: named && supported.length > 0, cited_domains: named ? supported.sort() : [],
    citation_without_mention: !named && supported.length > 0};
}

