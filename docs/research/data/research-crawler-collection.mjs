// Public crawler study. No request body, query string, address or cookie is read.
export const agents = [
  ['GPTBot', true], ['OAI-SearchBot', true], ['ChatGPT-User', true],
  ['ClaudeBot', true], ['Claude-SearchBot', true], ['Claude-User', true],
  ['PerplexityBot', true], ['Perplexity-User', true],
  ['Googlebot', false], ['bingbot', false], ['Applebot', false]
];

export function claimedAgent(userAgent) {
  for (const [name, ai] of agents) {
    // Exact token boundaries avoid treating Applebot-Extended as Applebot.
    const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    if (new RegExp(`(?:^|[^A-Za-z0-9_-])${escaped}(?=$|[^A-Za-z0-9_-])`, 'i').test(userAgent))
      return { name, ai };
  }
  return null;
}

export function safeAgentText(value) {
  return String(value || '').replace(/[\r\n\x00-\x1f\x7f]/g, ' ')
    .replace(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/gi, '[email removed]')
    // URL's IPv6 parser validates full, compressed and IPv4-mapped literals.
    // This is local parsing only: no address lookup or network request occurs.
    .replace(/(?:[0-9a-f]{0,4}:){2,}[0-9a-f:.]*(?:%[A-Za-z0-9_.~-]+)?/gi, candidate => {
      const punctuation = candidate.match(/\.+$/)?.[0] || '';
      const literal = (punctuation ? candidate.slice(0, -punctuation.length) : candidate).replace(/%.*$/, '');
      try {
        new URL(`http://[${literal}]/`);
        return '[address removed]' + punctuation;
      } catch { return candidate; }
    })
    .replace(/\b(?:\d{1,3}\.){3}\d{1,3}\b/g, '[address removed]')
    .slice(0, 1024);
}

export function eligibleRecord(request, response, publicPaths, now = new Date()) {
  const url = new URL(request.url);
  if (url.hostname !== 'index.broadcastwell.com') return null;
  if (!['GET', 'HEAD'].includes(request.method)) return null;
  if (response.status !== 200 || !/text\/html/i.test(response.headers.get('content-type') || '')) return null;
  if (!publicPaths.has(url.pathname)) return null;
  const ua = safeAgentText(request.headers.get('user-agent'));
  return { timestamp: now.toISOString(), path: url.pathname, user_agent: ua,
    ai_match: Number(Boolean(claimedAgent(ua)?.ai)) };
}

export async function writeRecord(db, record) {
  const day = record.timestamp.slice(0, 10);
  // A daily observation ceiling keeps the collection bounded.
  // Saturation stays at 4,001, so subsequent batches cannot resume inserts.
  await db.batch([
    db.prepare(`INSERT INTO research_crawler_quota(day,n) VALUES(?,1)
      ON CONFLICT(day) DO UPDATE SET n=MIN(n+1,4001)`).bind(day),
    db.prepare(`INSERT INTO research_crawler_requests(timestamp,path,user_agent,ai_match)
      SELECT ?,?,?,? WHERE (SELECT n FROM research_crawler_quota WHERE day=?) <= 4000`)
      .bind(record.timestamp, record.path, record.user_agent, record.ai_match, day)
  ]);
}
