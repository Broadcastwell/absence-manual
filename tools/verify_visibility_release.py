"""Check the complete published visibility scope against the reviewed decisions."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
import argparse, collections, hashlib, json, re
import xml.etree.ElementTree as ET
from library_publication_consumers import _HeadAndArticle
from library_visibility_release import require

BASE = 'https://docs.broadcastwell.com/'


class Page(_HeadAndArticle):
    def __init__(self):
        super().__init__()
        self.h1 = []; self.heading = False; self.links = []; self.article_links = []
        self.depth = 0; self.text = []; self.hidden = 0

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        a = dict(attrs)
        if tag in {'script', 'style'}: self.hidden += 1
        if tag == 'article': self.depth += 1
        if tag == 'h1': self.heading = True; self.h1.append('')
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
            if self.depth: self.article_links.append(a['href'])

    def handle_endtag(self, tag):
        super().handle_endtag(tag)
        if tag in {'script', 'style'}: self.hidden -= 1
        if tag == 'article': self.depth -= 1
        if tag == 'h1': self.heading = False

    def handle_data(self, data):
        super().handle_data(data)
        if self.heading: self.h1[-1] += data
        if not self.hidden: self.text.append(data)


def validate(site, decisions):
    site = Path(site)
    expected = {r['url']:r['meta'] for r in decisions['pages'].values()}
    for path,row in decisions['static_pages'].items():
        head = Page(); head.feed((site/path).read_text(encoding='utf8'))
        expected[row['url']] = {'title':head.title,'description':head.meta['description'][0]}
    require(len(expected) == 395, 'All 395 eligible pages are required')
    titles = []; descriptions = []; incoming = collections.Counter(); all_links = {}
    types = collections.Counter(); rows = []
    ns = {'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    xml = ET.fromstring((site/'sitemap.xml').read_bytes())
    entries = {r.findtext('s:loc',namespaces=ns):r.findtext('s:lastmod',namespaces=ns) for r in xml}
    require(len(entries) == 440, 'Current sitemap population differs')
    require(set(expected) <= set(entries), 'An eligible canonical page is absent from the sitemap')
    for url in entries:
        path = url.removeprefix(BASE) + 'index.html'
        page = Page(); raw = (site/path).read_bytes(); page.feed(raw.decode())
        links = {urljoin(url, href).split('#')[0].split('?')[0] for href in page.links}
        all_links[url] = links
        for target in links:
            if target != url and target in entries: incoming[target] += 1
        if url not in expected: continue
        meta = expected[url]
        require(page.title == meta['title'] and len(page.title) < 60 and page.title.endswith('?'), 'Question title differs: '+url)
        require([x.strip().rstrip('¶').strip() for x in page.h1] == [page.title], 'Visible H1 differs: '+url)
        require(page.canonical == [url], 'Canonical differs: '+url)
        desc = page.meta.get('description', [])
        require(desc == [meta['description']] and 150 <= len(desc[0]) <= 160, 'Description differs: '+url)
        for key in ['title','description','url','type','site_name','image','image:alt','image:type','image:width','image:height']:
            require(len(page.meta.get('og:'+key, [])) == 1 and page.meta['og:'+key][0], 'Open Graph field is missing: '+url+' '+key)
        require(page.meta['og:title'] == [page.title] and page.meta['og:description'] == desc and page.meta['og:url'] == [url], 'Social metadata differs: '+url)
        require(entries[url] == decisions['revision_utc'], 'Page revision and sitemap date differ: '+url)
        counts = collections.Counter(x.get('@type') for x in page.scripts)
        require(counts['BreadcrumbList'] == 1, 'Exactly one breadcrumb is required: '+url)
        require(counts['Dataset'] <= 1, 'Duplicate Dataset declarations: '+url)
        visible = ' '.join(' '.join(page.text).split())
        for schema in page.scripts:
            kind = schema.get('@type'); types[kind] += 1
            require(schema.get('@context') == 'https://schema.org', 'Structured data context differs')
            if kind == 'BreadcrumbList':
                items = schema['itemListElement']
                require([x['position'] for x in items] == list(range(1,len(items)+1)), 'Breadcrumb positions differ')
                require(items[-1]['item'] == url, 'Breadcrumb destination differs')
            if kind in {'Article','TechArticle'}:
                require(schema.get('author',{}).get('name') == 'Broadcastwell', 'Article author differs')
                require(schema.get('datePublished') and schema.get('dateModified') == decisions['revision_utc'], 'Article dates differ')
            if kind == 'FAQPage':
                for item in schema['mainEntity']:
                    require(' '.join(item['name'].split()) in visible, 'FAQ question is not visible: '+url)
                    require(' '.join(item['acceptedAnswer']['text'].split()) in visible, 'FAQ answer is not visible: '+url)
            if kind == 'Dataset':
                require(schema.get('name') and schema.get('description') and schema.get('url') == url and schema.get('distribution'), 'Dataset fields are incomplete')
                require(schema.get('creator',{}).get('name') == 'Broadcastwell', 'Dataset creator differs')
                require(schema.get('citation','').startswith('https://doi.org/') or schema.get('identifier') == url, 'Dataset needs its actual DOI or undeclared-DOI canonical identifier')
            require(kind in {'Organization','Article','TechArticle','BreadcrumbList','FAQPage','DefinedTerm','Dataset'}, 'An unreviewed schema type was introduced')
        if url.startswith(BASE+'answers/') and len(urlsplit(url).path.strip('/').split('/')) == 3:
            require(counts['Article'] == 1 and counts['TechArticle'] == 0, 'Answer needs Article schema: '+url)
            article = {urljoin(url,h).split('#')[0] for h in page.article_links}
            related = {x for x in article if x.startswith(BASE+'answers/') and len(urlsplit(x).path.strip('/').split('/')) == 3 and x != url}
            require(2 <= len(related) <= 4, 'Answer needs two to four related answers: '+url)
            hub = '/'.join(url.rstrip('/').split('/')[:-1])+'/'
            require(hub in article, 'Answer hub is missing: '+url)
            require('https://index.broadcastwell.com/method.html' in article, 'Index method is missing: '+url)
            require(any(x.startswith('https://index.broadcastwell.com/categories/') for x in article) or 'https://index.broadcastwell.com/' in article, 'Relevant category evidence is missing: '+url)
        titles.append(page.title); descriptions.append(desc[0])
        rows.append({'url':url,'sha256':hashlib.sha256(raw).hexdigest(),'schemas':dict(counts)})
    require(len(set(titles)) == len(titles), 'Duplicate current titles')
    require(len(set(descriptions)) == len(descriptions), 'Duplicate current descriptions')
    orphans=[u for u in expected if u != BASE and not incoming[u]]
    require(not orphans, 'Eligible pages are orphaned: '+', '.join(orphans))
    robots = (site/'robots.txt').read_text(encoding='utf8')
    for bot in ['Googlebot','Bingbot','GPTBot','OAI-SearchBot','ClaudeBot','PerplexityBot','Google-Extended']:
        require(re.search(r'User-agent: '+re.escape(bot)+r'\s+Allow: /', robots), 'Crawler is not allowed: '+bot)
    llms = (site/'llms.txt').read_text(encoding='utf8')
    for path,row in decisions['pages'].items():
        if path.startswith('research/') or (path.startswith('answers/') and path.endswith('/index.md')):
            require(row['url'] in llms, 'Key research page or hub missing from llms: '+path)
    return {'sitemap_urls':440,'eligible_pages':395,'frozen_exclusions':45,'types':dict(types),'pages':rows,'orphan_pages':0}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site',type=Path,default=Path('site'))
    parser.add_argument('--decisions',type=Path,default=Path('tools/library-visibility-20261105.json'))
    parser.add_argument('--out',type=Path,default=Path('visibility-release-check.json'))
    args=parser.parse_args()
    result=validate(args.site,json.loads(args.decisions.read_bytes()))
    args.out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:v for k,v in result.items() if k!='pages'}))
