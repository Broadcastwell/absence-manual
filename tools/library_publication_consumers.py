"""Visible effective consumers and exact derived-output checks, private proposal.

All functions operate on bytes/records supplied by the owning build. They never
write a source file, contact a service or accept a caller's claimed fingerprint
as proof that a generator consumed effective metadata.
"""
from __future__ import annotations
import copy
import gzip
import io
from html import escape,unescape
from html.parser import HTMLParser
import json
from pathlib import PurePosixPath
import re
from urllib.parse import urljoin,urlsplit,urlunsplit
import xml.etree.ElementTree as ET

from library_publication_overlay import require,sha,canonical
from library_publication_release import route_for,DERIVED_ROUTES

SITE='https://docs.broadcastwell.com'
SITEMAP_NS='http://www.sitemaps.org/schemas/sitemap/0.9'
URL_FRAGMENT=re.compile(rb'<url\b[^>]*>.*?</url>',re.S)
LIBRARY_HUB=re.compile(r'answers/(?:[a-z0-9-]+/)?index\.md')


def public_route(path):
    return '/'+path.removesuffix('index.md') if LIBRARY_HUB.fullmatch(path) else route_for(path)


class _RenderSignature(HTMLParser):
    def __init__(self,base,source=False):super().__init__(convert_charrefs=True);self.base=base;self.source=source;self.tokens=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='table' and 'tabindex' in attrs:
            require(attrs.pop('tabindex')=='0','Unexpected table accessibility mutation')
        if tag=='a' and 'headerlink' in attrs.get('class','').split():
            if 'aria-hidden' in attrs:require(attrs.pop('aria-hidden')=='true','Unexpected heading accessibility mutation')
            if 'tabindex' in attrs:require(attrs.pop('tabindex')=='-1','Unexpected heading focus mutation')
        for field in ['href','src']:
            if field not in attrs:continue
            joined=urljoin(self.base,attrs[field]);p=urlsplit(joined)
            if self.source and field=='href' and p.netloc=='docs.broadcastwell.com' and p.path.endswith('.md'):
                path=p.path.removesuffix('index.md') if p.path.endswith('/index.md') else p.path.removesuffix('.md')+'/'
                joined=urlunsplit((p.scheme,p.netloc,path,p.query,p.fragment))
            attrs[field]=joined
        self.tokens.append(('start',tag,tuple(sorted(attrs.items()))))
    def handle_endtag(self,tag):self.tokens.append(('end',tag))
    def handle_data(self,data):
        text=' '.join(data.split())
        if text:self.tokens.append(('text',text))


def require_source_render_context(path,body,html):
    import markdown
    expected=markdown.markdown(body,extensions=['toc','tables','attr_list','md_in_html','def_list','footnotes','admonition'],extension_configs={'toc':{'permalink':True,'toc_depth':3}})
    source=_RenderSignature(SITE+'/'+path,True);source.feed(expected)
    actual=_RenderSignature(SITE+public_route(path));actual.feed(html)
    require(source.tokens==actual.tokens,'Actual renderer output differs from the complete effective Markdown')


class EffectiveRegistry:
    def __init__(self,overlay):
        overlay._check_unchanged()
        self.overlay=overlay
        self.records=copy.deepcopy(overlay.records)
        self.fingerprint=sha(overlay.q.canonical_json({path:{'meta':r['meta'],'body_sha256':sha(r['body'].encode()),'effective_canonical_sha256':r['effective_canonical_source_sha256']} for path,r in sorted(self.records.items())}).encode())
        self.receipts={}
        self.hubs={}

    def assert_current(self):
        self.overlay._check_unchanged()
        current=sha(self.overlay.q.canonical_json({path:{'meta':r['meta'],'body_sha256':sha(r['body'].encode()),'effective_canonical_sha256':r['effective_canonical_source_sha256']} for path,r in sorted(self.overlay.records.items())}).encode())
        require(current==self.fingerprint,'Effective registry changed during consumer generation')

    def receipt(self,name,*,consumed_paths,outputs,proof):
        self.assert_current()
        require(name in {'page-head-and-structured-data','library-hubs','llms','search','sitemap'},'Unknown effective consumer')
        paths=set(consumed_paths)
        require(paths==set(self.records),'Consumer did not inspect the full effective leaf registry')
        require(isinstance(outputs,dict) and outputs and all(isinstance(v,bytes) for v in outputs.values()),'Actual consumer output bytes required')
        result={'consumer':name,'registry_sha256':self.fingerprint,'effective_paths':sorted(paths),
            'output_sha256':{k:sha(v) for k,v in sorted(outputs.items())},'proof':copy.deepcopy(proof)}
        self.receipts[name]=result
        return result


class _HeadAndArticle(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.title='';self.in_title=False;self.meta={};self.canonical=[];self.scripts=[];self.in_json=False;self.json=''
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='title':self.in_title=True
        if tag=='meta':
            key=a.get('name') or a.get('property')
            if key:self.meta.setdefault(key,[]).append(a.get('content'))
        if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
        if tag=='script' and a.get('type')=='application/ld+json':self.in_json=True;self.json=''
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
        if tag=='script' and self.in_json:self.scripts.append(json.loads(self.json));self.in_json=False
    def handle_data(self,data):
        if self.in_title:self.title+=data
        if self.in_json:self.json+=data


def validate_page_contexts(registry,*,contexts,site_name='The Absence Manual'):
    """Inspect actual renderer inputs and complete final HTML for every article."""
    registry.assert_current();require(set(contexts)==set(registry.records)|set(registry.hubs),'Actual effective page context coverage differs')
    outputs={}
    footer=re.compile(r'\s*<hr>\s*<p class="manual-footer-version">Broadcastwell answer library\. Prose and figures CC BY 4\.0\. Site code MIT\. <a href="https://docs\.broadcastwell\.com/answers/">Read the library</a>\.</p>\s*\Z')
    for path,record in {**registry.records,**registry.hubs}.items():
        context=contexts[path];meta=record['meta']
        require(context['markdown']==record['body'] and context['meta']==meta,'Renderer did not consume the effective body/metadata')
        require_source_render_context(path,record['body'],context['html'])
        raw=context['rendered_html'];require(isinstance(raw,bytes),'Actual final HTML bytes required')
        html=raw.decode('utf-8');head=_HeadAndArticle();head.feed(html)
        url=SITE+public_route(path)
        require(head.title==str(meta['title'])+' | '+site_name and head.canonical==[url],'Public title/canonical is not effective metadata')
        expected={'description':meta['description'],'og:title':meta['title'],'og:description':meta['description'],'og:url':url,'twitter:title':meta['title'],'twitter:description':meta['description']}
        require(all(head.meta.get(key)==[value] for key,value in expected.items()),'Public social/description metadata is stale or repeated')
        article=[x for x in head.scripts if x.get('@type')=='Article']
        require(len(article)==1,'Exactly one effective Article object required')
        for key,value in {'headline':meta['headline'],'name':meta['headline'],'description':meta['description'],'datePublished':meta['date_published'],'dateModified':meta['date_modified'],'url':url,'isBasedOn':meta.get('is_based_on','')}.items():
            require(article[0].get(key)==value,'Structured Article consumes stale metadata: '+key)
        crumbs=[x for x in head.scripts if x.get('@type')=='BreadcrumbList'];require(len(crumbs)==1 and crumbs[0]['itemListElement'][-1]['name']==meta['title'],'Breadcrumb title is stale')
        rendered_article=re.findall(r'<article\b[^>]*>(.*?)</article>',html,re.S);require(len(rendered_article)==1,'Actual article wrapper differs')
        m=footer.search(rendered_article[0]);require(m is not None,'Exact library footer boundary is missing')
        require(rendered_article[0][:m.start()].strip()==context['html'].strip(),'Final visible article differs from the actual pinned renderer output')
        outputs[public_route(path)]=raw
    return registry.receipt('page-head-and-structured-data',consumed_paths=registry.records,outputs=outputs,proof={'renderer_markdown_and_metadata_exact':True,'whole_visible_article_matches_renderer_HTML':True,'head_social_Article_breadcrumb_fields_exact':True})


def leaf_path(href,source_path):
    joined=urljoin(SITE+'/'+source_path,href)
    parsed=urlsplit(joined)
    if parsed.netloc!='docs.broadcastwell.com':return None
    path=parsed.path.strip('/')
    if path.endswith('.md'):return path
    if re.fullmatch(r'answers/[a-z0-9-]+/[a-z0-9-]+',path):return path+'.md'
    return None


def render_hub_body(registry,*,path,body,raw_leaf_metadata,merged_sources=()):
    """Change only actual answer title/description blocks and exact count text.

    Research links, surrounding paragraphs, group order and unrelated bytes are
    retained. A subtopic regrouping is an explicit separately reviewed hub edit,
    not an automatic consequence of a metadata spelling correction.
    """
    require(bool(LIBRARY_HUB.fullmatch(path)),'Only a library hub may consume these blocks')
    root=path=='answers/index.md';merged=set(merged_sources)
    link=re.compile(r'(?m)^(?P<bullet>- )?\[(?P<title>[^\]\n]+)\]\((?P<href>[^\s)]+)\)(?P<inline>[^\n]*)\n')
    replacements=[];listed=[];source_listed=[]
    for m in link.finditer(body):
        rel=leaf_path(m['href'],path)
        if rel is None or rel not in raw_leaf_metadata:continue
        source_listed.append(rel);raw=raw_leaf_metadata[rel]
        require(m['title']==str(raw['title']),'Hub title is not its exact current source metadata')
        start,end=m.span();inline=m['inline'];old_desc=''
        if root:
            require(inline.startswith(' '),'Featured answer must retain an inline description')
            old_desc=inline[1:]
        else:
            following=re.match(r'\n(?P<description>[^\n]+)\n',body[end:])
            require(following is not None,'Cluster hub lacks the exact answer-description paragraph')
            old_desc=following['description'];end+=following.end()
        require(' '.join(old_desc.split())==' '.join(str(raw['description']).split()),'Hub excerpt differs from the source metadata; needs an explicit hub patch')
        if rel in merged:
            require(rel not in registry.records,'Merged hub row still exists as an effective article')
            replacements.append((start,end,''));continue
        require(rel in registry.records,'Hub names an unregistered effective leaf')
        effective=registry.records[rel]['meta'];listed.append(rel)
        if effective.get('library_subtopic')!=raw.get('library_subtopic'):
            require(False,'Subtopic change needs a separately reviewed exact hub group patch')
        if effective['title']==raw['title'] and effective['description']==raw['description']:continue
        label=str(effective['title']);description=str(effective['description'])
        require('\n' not in label and '\n' not in description and '[' not in label and ']' not in label,'Effective hub label/description needs an explicit safe Markdown representation')
        new=(m['bullet'] or '')+'['+label+']('+m['href']+')'
        new+=(' '+description+'\n') if root else ('\n\n'+description+'\n')
        replacements.append((start,end,new))
    if not root:
        cluster=PurePosixPath(path).parent.name
        expected={p for p,r in registry.records.items() if r['cluster']==cluster}
        require(len(listed)==len(set(listed)) and set(listed)==expected,'Cluster hub hides or duplicates an effective leaf')
    for start,end,new in reversed(replacements):body=body[:start]+new+body[end:]
    if merged:
        # Empty subtopic headings only; no nonempty paragraph or research block is removed.
        body=re.sub(r'(?m)^## (?!Browse|Start|Next)[^\n]+\n(?:[ \t]*\n)+(?=## |\[Browse all answer clusters\])','',body)
    count=len(registry.records) if root else len(listed)
    phrase=re.compile(r'\bThese \d+ (pages|answers)\b')
    if phrase.search(body):body=phrase.sub(lambda m:'These '+str(count)+' '+m[1],body,count=1)
    return body


def generate_effective_hubs(registry,*,hub_sources,raw_leaf_metadata,approved_hub_changes,merged_sources=()):
    """Return served hub bodies/meta; source bytes are never written."""
    registry.assert_current();require('answers/index.md' in hub_sources,'Library root hub is missing')
    expected={'answers/'+r['cluster']+'/index.md' for r in registry.records.values()}|{'answers/index.md'}
    require(set(hub_sources)==expected,'Hub registry lacks an effective cluster')
    result={};outputs={}
    for path,source in sorted(hub_sources.items()):
        old_body=source['body'];old_meta=source['meta'];meta=copy.deepcopy(old_meta)
        body=render_hub_body(registry,path=path,body=old_body,raw_leaf_metadata=raw_leaf_metadata,merged_sources=merged_sources)
        if path=='answers/index.md' and set(merged_sources):
            description=re.sub(r'^\d+(?= answers\b)',str(len(registry.records)),str(meta['description']),count=1)
            meta['description']=description
        if body!=old_body or meta!=old_meta:
            change=approved_hub_changes.get(path)
            require(change and change.get('approved') is True and change.get('before_canonical_sha256')==source['canonical_sha256']
                and change.get('after_body_sha256')==sha(body.encode()),'Changed effective hub lacks its exact reviewed generated-body binding')
            allowed=change.get('metadata_delta',{})
            require(set(allowed)<={'title','headline','description','date_modified'},'Protected hub metadata cannot change')
            for field,item in allowed.items():
                require(item.get('old')==old_meta.get(field),'Effective hub metadata old value differs')
                meta[field]=item['new']
            require('date_modified' in allowed,'Changed hub needs an explicit approved modification time')
            require(re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})',str(meta['date_modified'])),'Hub modification time is not explicit ISO')
            if path=='answers/index.md' and set(merged_sources):require(meta['description'].startswith(str(len(registry.records))+' answers'),'Root hub metadata still has a stale article count')
        result[path]={'body':body,'meta':meta}
        outputs['/'+path.removesuffix('index.md')]=body.encode()
    registry.receipt('library-hubs',consumed_paths=registry.records,outputs=outputs,proof={'actual_title_description_blocks_consume_effective_metadata':True,'all_clusters_cover_exact_effective_leaves':True,'surrounding_research_and_nonanswer_bytes_preserved':True,'modified_hubs_independently_pinned':True})
    registry.hubs=copy.deepcopy(result)
    return result


def generate_answers_section(registry,*,hub_metadata,page_url):
    """Same visible format as the source generator, using effective metadata."""
    registry.assert_current();entries=[]
    require(hub_metadata=={p:r['meta'] for p,r in registry.hubs.items()} and hub_metadata,'llms did not consume the actual effective hub metadata')
    for path,meta in hub_metadata.items():
        require(LIBRARY_HUB.fullmatch(path),'Nonlibrary metadata supplied as a hub')
        relative=PurePosixPath(path)
        order=(0 if len(relative.parts)==2 else 1,int(meta.get('library_order',999999)),path)
        entries.append((order,meta,relative))
    for path,record in registry.records.items():
        meta=record['meta'];entries.append(((2,int(meta.get('library_order',999999)),path),meta,PurePosixPath(path)))
    lines=['## Answers','']
    for _,meta,path in sorted(entries,key=lambda x:x[0]):
        title=' '.join(str(meta['title']).split()).replace('[','').replace(']','')
        description=' '.join(str(meta['description']).split())
        lines.append('- ['+title+']('+page_url(path)+'): '+description)
    return '\n'.join(lines)+'\n'


def generate_effective_llms(registry,*,original,hub_metadata,source_generator):
    section=generate_answers_section(registry,hub_metadata=hub_metadata,page_url=source_generator.page_url)
    result=source_generator.regenerate(original,section)
    require(source_generator.regenerate(original,section)==result,'Effective llms generator is nondeterministic')
    # Reversing only the exact Answers span proves prices/research/client bytes outside it survived.
    headings=list(source_generator.ANSWERS_HEADING.finditer(original))
    require(len(headings)==1,'Existing llms Answers section requires an exact source boundary')
    h=headings[0];following=re.search(rb'(?m)^## ',original[h.end():]);right=h.end()+following.start() if following else len(original)
    start=h.start();oldsection=original[start:right]
    replacement=section.encode()+ (b'\n' if following else b'')
    require(result[:start]==original[:start] and result[start+len(replacement):]==original[right:],'llms generation changed bytes outside Answers')
    registry.receipt('llms',consumed_paths=registry.records,outputs={'/llms.txt':result},proof={'answers_section_sha256':sha(section.encode()),'non_Answers_bytes_exact':True,'hub_paths':sorted(hub_metadata)})
    return result


def _sitemap_rows(raw):
    require(b'<!DOCTYPE' not in raw and b'<!ENTITY' not in raw,'Sitemap must not contain a DTD/entity declaration')
    root=ET.fromstring(raw);require(root.tag=='{'+SITEMAP_NS+'}urlset','Unexpected sitemap root/namespace')
    fragments=list(URL_FRAGMENT.finditer(raw));children=list(root)
    require(len(fragments)==len(children),'Sitemap URL fragments differ from XML rows')
    result=[];seen=set()
    for child,m in zip(children,fragments):
        require(child.tag=='{'+SITEMAP_NS+'}url','Unexpected sitemap child')
        loc=child.find('{'+SITEMAP_NS+'}loc');lastmod=child.find('{'+SITEMAP_NS+'}lastmod')
        require(loc is not None and loc.text and loc.text not in seen,'Missing/duplicate sitemap location')
        require(urlsplit(loc.text).netloc=='docs.broadcastwell.com','Unexpected sitemap host')
        require(lastmod is not None and lastmod.text,'Sitemap lastmod is missing')
        seen.add(loc.text);result.append({'url':loc.text,'lastmod':lastmod.text,'raw':m.group(),'start':m.start(),'end':m.end()})
    return result


def generate_effective_sitemaps(registry,*,prior_xml,hub_metadata,merged_sources=(),field_freeze=None,publication_dates=None):
    """Keep every nonlibrary URL element byte exact; use approved effective dates."""
    registry.assert_current()
    require(hub_metadata=={p:r['meta'] for p,r in registry.hubs.items()} and hub_metadata,'Sitemap did not consume the actual effective hub metadata')
    desired={SITE+route_for(path):r['meta']['date_modified'] for path,r in registry.records.items()}
    for path,meta in hub_metadata.items():
        require(LIBRARY_HUB.fullmatch(path),'Unexpected sitemap hub')
        desired[SITE+'/'+path.removesuffix('index.md')]=meta['date_modified']
    for url,stamp in list(desired.items()):
        require(isinstance(stamp,str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})',stamp),'Sitemap requires exact approved ISO date_modified')
        desired[url]=stamp[:10]
    if publication_dates is not None:
        from library_publication_sitemap_dates import BoundPublicationDates
        require(isinstance(publication_dates,BoundPublicationDates),'Arbitrary sitemap-date preservation map is forbidden')
        desired=publication_dates.expected(registry,prior_xml)
    if field_freeze is not None:
        field_freeze.check_sitemap(prior_xml)
        require(set(field_freeze.sitemap_dates())<=set(desired),'A frozen sitemap leaf was removed')
        desired.update(field_freeze.sitemap_dates())
    rows=_sitemap_rows(prior_xml);result=prior_xml;seen=set();merged={SITE+route_for(path) for path in merged_sources}
    for row in reversed(rows):
        if not urlsplit(row['url']).path.startswith('/answers/'):continue
        if row['url'] in merged:
            result=result[:row['start']]+result[row['end']:];continue
        require(row['url'] in desired,'Prior sitemap library route missing without reviewed301')
        replacement=re.sub(rb'(<lastmod>).*?(</lastmod>)',lambda m:m[1]+desired[row['url']].encode()+m[2],row['raw'],count=1,flags=re.S)
        result=result[:row['start']]+replacement+result[row['end']:];seen.add(row['url'])
    additions=[]
    for url in sorted(set(desired)-seen):
        additions.append(('    <url>\n         <loc>'+escape(url,quote=False)+'</loc>\n         <lastmod>'+desired[url]+'</lastmod>\n    </url>\n').encode())
    require(result.count(b'</urlset>')==1,'Sitemap closing boundary differs')
    if additions:result=result.replace(b'</urlset>',b''.join(additions)+b'</urlset>',1)
    validate_effective_sitemap(registry,prior_xml=prior_xml,candidate_xml=result,hub_metadata=hub_metadata,merged_sources=merged_sources,field_freeze=field_freeze,publication_dates=publication_dates)
    buffer=io.BytesIO()
    with gzip.GzipFile(fileobj=buffer,filename='',mode='wb',compresslevel=9,mtime=0) as stream:
        stream.write(result)
    compressed=buffer.getvalue()
    registry.receipt('sitemap',consumed_paths=registry.records,outputs={'/sitemap.xml':result,'/sitemap.xml.gz':compressed},proof={'nonlibrary_URL_elements_byte_exact':True,'leaf_lastmod':'exact unchanged prior publication-lastmod, otherwise actual reviewed modified date; frozen entries exact' if publication_dates is not None else 'effective approved date_modified except exact accepted field-freeze entries; no article rule PASS exemption','publication_lastmod_audit':publication_dates.audit() if publication_dates is not None else None,'field_freeze_preserved_urls':sorted(field_freeze.sitemap_dates()) if field_freeze is not None else [],'gzip_mtime':0})
    return result,compressed


def validate_effective_sitemap(registry,*,prior_xml,candidate_xml,hub_metadata,merged_sources=(),field_freeze=None,publication_dates=None):
    old=_sitemap_rows(prior_xml);new=_sitemap_rows(candidate_xml)
    old_non={r['url']:r['raw'] for r in old if not urlsplit(r['url']).path.startswith('/answers/')}
    new_non={r['url']:r['raw'] for r in new if not urlsplit(r['url']).path.startswith('/answers/')}
    require(old_non==new_non,'A nonlibrary sitemap URL element changed')
    expected={SITE+route_for(path):r['meta']['date_modified'][:10] for path,r in registry.records.items()}
    expected.update({SITE+'/'+path.removesuffix('index.md'):meta['date_modified'][:10] for path,meta in hub_metadata.items()})
    if publication_dates is not None:
        from library_publication_sitemap_dates import BoundPublicationDates
        require(isinstance(publication_dates,BoundPublicationDates),'Arbitrary sitemap-date preservation map is forbidden')
        expected=publication_dates.expected(registry,prior_xml)
    if field_freeze is not None:
        field_freeze.check_sitemap(prior_xml);field_freeze.check_sitemap(candidate_xml)
        require(set(field_freeze.sitemap_dates())<=set(expected),'A frozen sitemap leaf was removed')
        expected.update(field_freeze.sitemap_dates())
    actual={r['url']:r['lastmod'] for r in new if urlsplit(r['url']).path.startswith('/answers/')}
    require(actual==expected,'Sitemap hides/adds an effective route or uses stale metadata dates')
    require(not {SITE+route_for(path) for path in merged_sources}&set(actual),'Merged301 source remains in sitemap')


def validate_effective_search(registry,*,prior_bytes,candidate_bytes,actual_page_contexts,merged_sources=()):
    registry.assert_current();old=json.loads(prior_bytes);new=json.loads(candidate_bytes)
    require(set(old)==set(new) and {k:v for k,v in old.items() if k!='docs'}=={k:v for k,v in new.items() if k!='docs'},'Search configuration/non-document fields changed')
    def library(row):return row.get('location','').lstrip('/').startswith('answers/')
    require([r for r in old['docs'] if not library(r)]==[r for r in new['docs'] if not library(r)],'Nonlibrary search rows changed')
    expected_contexts=set(registry.records)|set(registry.hubs)
    require(set(actual_page_contexts)==expected_contexts,'Search actual page-context coverage differs')
    # The installed pinned Material producer consumes these verified contexts;
    # an arbitrary caller-provided expected-doc list is not an approval path.
    from material.plugins.search.plugin import SearchIndex
    from types import SimpleNamespace
    generated=SearchIndex(**new['config'])
    for path,context in actual_page_contexts.items():
        expected=registry.records[path] if path in registry.records else registry.hubs[path]
        require(context['markdown']==expected['body'] and context['meta']==expected['meta'],'Search renderer context has stale body/metadata')
        require_source_render_context(path,expected['body'],context['html'])
        url=path.removesuffix('index.md') if path.endswith('/index.md') else path.removesuffix('.md')+'/'
        page=SimpleNamespace(meta=expected['meta'],title=expected['meta']['title'],content=context['html'],toc=context['toc'],url=url)
        generated.add_entry_from_context(page)
    expected_library_entries=generated.entries
    actual=[r for r in new['docs'] if library(r)]
    require(actual==expected_library_entries,'Built search entries differ from actual effective page contexts')
    roots={r['location'].split('#')[0].strip('/') for r in actual}
    require({path.removesuffix('.md') for path in registry.records}<=roots,'Search hides an effective article')
    require(not {path.removesuffix('.md') for path in merged_sources}&roots,'Merged301 source remains in search')
    registry.receipt('search',consumed_paths=registry.records,outputs={'/search/search_index.json':candidate_bytes},proof={'nonlibrary_rows_exact':True,'library_rows_equal_actual_effective_page_contexts':True})


def compare_complete_artifacts(*,prior_files,candidate_files,changed_article_paths,changed_hub_paths,validated_derived_routes,merged_sources,expected_redirect_bytes,private_sidecars,reviewed_generated_pdf_changes=None,expected_canonical_stub_bytes=None):
    """Every byte difference must belong to an exact reviewed surface."""
    article_artifacts={p.removesuffix('.md')+'/index.html' for p in changed_article_paths}
    hub_artifacts={p.removesuffix('index.md')+'index.html' for p in changed_hub_paths}
    derived={r.lstrip('/') for r in validated_derived_routes}
    require(set(validated_derived_routes)<=DERIVED_ROUTES,'Unknown derived exclusion')
    removed={p.removesuffix('.md')+'/index.html' for p in merged_sources}
    allowed=article_artifacts|hub_artifacts|derived|removed
    from library_publication_generated_pdf import ReviewedPdfChanges
    pdfs=set()
    if reviewed_generated_pdf_changes is not None:
        require(isinstance(reviewed_generated_pdf_changes,ReviewedPdfChanges),'Generated PDF exception is not a computed Root review proof')
        reviewed_generated_pdf_changes.validate_artifacts(prior_files,candidate_files)
        pdfs=set(reviewed_generated_pdf_changes.rows);allowed|=pdfs
    require(set(private_sidecars)<= {'relaunch-build-provenance.json','library-release-proof.json','library-effective-payload.json','library-compiled-state.json'},'Unknown private sidecar exclusion')
    changes={p for p in set(prior_files)|set(candidate_files) if prior_files.get(p)!=candidate_files.get(p)}
    if expected_redirect_bytes is not None:
        require(candidate_files.get('_redirects')==expected_redirect_bytes,'Redirect artifact differs from exact append-only301 proof')
        allowed.add('_redirects')
    require(changes<=allowed|set(private_sidecars),'Unrelated/nonlibrary artifact bytes changed: '+', '.join(sorted(changes-allowed-set(private_sidecars))))
    if expected_canonical_stub_bytes is not None:
        require(set(expected_canonical_stub_bytes)==removed,'Canonical stub artifact map hides/invents a source')
        for source in removed:require(isinstance(expected_canonical_stub_bytes[source],bytes) and candidate_files.get(source)==expected_canonical_stub_bytes[source],'Actual canonical stub bytes differ')
    else:
        for source in removed:require(source not in candidate_files,'Merged source HTML still exists')
    return {'changed_artifact_paths':sorted(changes),'nonlibrary_artifacts_byte_exact':not bool(pdfs),'other_nonlibrary_artifacts_byte_exact':True,'reviewed_generated_pdf_artifacts':sorted(pdfs),'derived_artifacts_explicit':sorted(derived),'private_sidecars_not_public_routes':sorted(private_sidecars)}
