"""Finite owner-repair source/consumer deltas with exact inverse proofs."""
from __future__ import annotations
import copy,gzip,io,json,re
import xml.etree.ElementTree as ET
from html import escape
from html.parser import HTMLParser
from library_owner_repair import require,sha,encoded,digest,exact_edits,SITE,DERIVED,POLICY

def json_hash(value):return sha(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())

def validate_peer(raw,expected_sha256,record,kind,ledger_sha256,*,prior_S5_pass=False):
    require(sha(raw)==expected_sha256,'Current peer receipt bytes differ')
    d=json.loads(raw)
    require(d.get('approved') is True and d.get('current_full_file_actually_read') is True and d.get('review_kind')==kind and d.get('scope')=='owner-exact-repair-changes' and d.get('policy')==POLICY,'Actual scoped repair peer missing')
    require(d.get('approved_exact_repair_changes') is True and d.get('preserved_facts') is True and d.get('repair_change_ledger_sha256')==ledger_sha256,'Exact repair changes/fact preservation review missing')
    require(isinstance(d.get('remaining_prior_S5_defects'),list),'Explicit remaining prior S5 defects required')
    if prior_S5_pass:
        from library_owner_repair_post_s5 import LEGAL
        from library_owner_repair_required28 import ANTHROPIC
        require(record['path'] in {LEGAL,ANTHROPIC} and d.get('current_S5_pass') is None
            and d.get('ordinary_full_article_approval') is False and not d['remaining_prior_S5_defects'],
            'Exact Legal/Q0275 scoped peer cannot grant ordinary PASS or hide a known defect')
    elif record['path'].startswith('answers/'):
        require(d.get('current_S5_pass') is False and d['remaining_prior_S5_defects'],'Scoped answer peer cannot grant ordinary S5 PASS or hide remaining defects')
    else:require(d.get('current_S5_pass') is None,'Nonlibrary repair is not an S5 article PASS')
    require(d.get('path')==record['path'] and d.get('canonical_source_sha256')==record['raw_canonical_source_sha256'] and d.get('before_effective_canonical_source_sha256')==record['before_effective_canonical_source_sha256'],'Current peer raw/before-effective source/path binding differs')
    require(d.get('effective_canonical_source_sha256')==sha(record['effective_full_source'].encode()) and d.get('effective_body_sha256')==sha(record['body'].encode()) and d.get('effective_meta_sha256')==json_hash(record['meta']),'Current peer full/body/metadata binding differs')
    return True

def repair_ledger(path,before,after_full,body_edits,after_meta):
    return {'path':path,'before_effective_canonical_sha256':sha(before['effective_full_source'].encode()),
      'after_effective_canonical_sha256':sha(after_full.encode()),'body_edits':copy.deepcopy(body_edits),
      'metadata_delta':{k:{'old':before['meta'].get(k),'new':after_meta.get(k)} for k in sorted(set(before['meta'])|set(after_meta)) if before['meta'].get(k)!=after_meta.get(k)}}


def validate_static_peer(raw,expected_sha256,*,path,before,after,ledger,kind):
    require(sha(raw)==expected_sha256,'Bound static peer bytes differ')
    d=json.loads(raw)
    require(d.get('review_kind')==kind and d.get('policy')==POLICY and d.get('path')==path and d.get('raw_after_sha256')==sha(after),'Static peer exact identity differs')
    if kind=='source':
        require(d.get('scope')=='bounded-owner-policy-or-comment-inverse' and d.get('approved_exact_bounded_change') is True and d.get('exact_forward_reverse_replay') is True,'Source bounded policy/comment inverse missing')
        require(d.get('before_source_sha256')==sha(before) and d.get('after_source_sha256')==sha(after) and d.get('body_edits')==ledger['body_edits'],'Source static literal inverse differs')
        require(d.get('ordinary_full_article_approval') is False and d.get('current_S5_pass') is None,'Source static proof cannot grant article PASS')
    else:
        require(d.get('scope')=='owner-exact-repair-changes' and d.get('approved') is True and d.get('approved_exact_repair_changes') is True and d.get('repair_change_ledger_sha256')==json_hash(ledger),'Writing static policy/comment inverse missing')
        require(d.get('current_S5_pass') is None,'Writing static proof cannot grant article PASS')
    return True

def validate_fact_bindings(bindings,*,published_records,after_body,allowed_public_urls):
    """Match actual published cuts; a qualitative reading is not numeric1."""
    from urllib.parse import urlsplit
    require(isinstance(bindings,list) and bindings,'Rule4 requires exact published fact bindings')
    keys={'observation_id','published_record_sha256','source_url','count','base','unit','observed_at','quote','body_span'}
    for b in bindings:
        require(set(b)==keys and b['observation_id'] in published_records,'Missing/unlisted fact identity')
        r=published_records[b['observation_id']]
        require(json_hash(r)==b['published_record_sha256'],'Published fact record hash differs')
        require(r.get('source_kind') in {'index-release','published-study','claim-registry'} and r.get('numeric_cut') is True,'Unsupported source kind or invented numeric qualitative cut')
        u=urlsplit(r.get('source_url',''));require(u.scheme=='https' and r.get('source_url') in allowed_public_urls,'Fact source is not an exact finite approved public URL')
        require(all(b[k]==r.get(k) for k in ['source_url','count','base','unit','observed_at']),'Fact count/base/date/unit changed from the published record')
        require(type(b['count']) is int and type(b['base']) is int and 0<=b['count']<=b['base'] and b['base']>0,'Published count/base malformed')
        require(isinstance(b['quote'],str) and b['quote'] and b['quote'] in r.get('public_text',''),'Exact published quote missing')
        require(isinstance(b['body_span'],str) and b['body_span'] and b['body_span'] in after_body,'Fact is absent from the actual after body')
    return {'published_fact_bindings':len(bindings),'all_exact':True,'numeric_identities_invented':False}

def compose_effective_payload(before,*,after_full,body_edits,expected_before_sha256,raw_source_sha256,review_ids,receipt_store,source_parser,allowed_metadata_fields,actual_adoption_utc,prior_S5_pass=False,ordinary_review_ids=None):
    """Patch actual production effective text, never wholesale raw proposal text."""
    require(sha(before['effective_full_source'].encode())==expected_before_sha256,'Before is not the actual prior effective payload')
    meta,body=source_parser(after_full)
    require(exact_edits(before['body'].encode(),body_edits).decode()==body,'After body is not the exact literal composition')
    require(meta.get('date_published')==before['meta'].get('date_published'),'Published date is immutable')
    changed={k for k in set(meta)|set(before['meta']) if meta.get(k)!=before['meta'].get(k)}
    require(changed<=set(allowed_metadata_fields),'Protected metadata changed')
    changed_content=body!=before['body'] or any(meta.get(k)!=before['meta'].get(k) for k in changed-{'date_modified'})
    require(changed_content,'A repair must not create date-only source churn')
    require(meta.get('date_modified')==actual_adoption_utc and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00',actual_adoption_utc),'Actual Root adoption UTC binding missing')
    require(after_full.endswith(body),'Exact after full/body boundary differs')
    result=copy.deepcopy(before);result.update(meta=meta,body=body,effective_head=after_full[:-len(body)] if body else after_full,effective_full_source=after_full,review_ids=copy.deepcopy(review_ids))
    require(isinstance(raw_source_sha256,str) and re.fullmatch('[0-9a-f]{64}',raw_source_sha256),'Protected raw source pin missing')
    record={'path':review_ids.get('path'),'raw_canonical_source_sha256':raw_source_sha256,'before_effective_canonical_source_sha256':expected_before_sha256,'effective_full_source':after_full,'meta':meta,'body':body}
    require(isinstance(record['path'],str),'Current review path missing')
    ledger=repair_ledger(record['path'],before,after_full,body_edits,meta)
    for kind in ['source','writing']:
        key=review_ids.get(kind);require(key in receipt_store,'Fresh complete '+kind+' receipt missing')
        validate_peer(receipt_store[key],key,record,kind,json_hash(ledger),prior_S5_pass=prior_S5_pass)
    if prior_S5_pass:
        require(isinstance(ordinary_review_ids,dict) and set(ordinary_review_ids)=={'source','writing'}
            and all(ordinary_review_ids[k]!=review_ids[k] for k in ordinary_review_ids),'Separate ordinary Legal peers required')
        result['review_ids']=copy.deepcopy(ordinary_review_ids)
    result['review_ids'].pop('path',None)
    return result

def apply_llms_lines(before,edits,*,allowed_urls,expected_metadata=None):
    """All unlisted bytes including Research/prices stay exact."""
    literal=[];seen=set()
    line=re.compile(r'^- \[([^\]]+)\]\((https://docs\.broadcastwell\.com/[^\s)]+)\): (.+)$')
    for e in edits:
        a,b=line.fullmatch(e['old']),line.fullmatch(e['new'])
        require(a is not None and b is not None and a[2]==b[2] in allowed_urls,'llms repair URL/prefix malformed or unlisted')
        require(a[2] not in seen,'Repeated llms repair URL');seen.add(a[2])
        require(e.get('change_title') is True or a[1]==b[1],'llms metadata repair changes its title prefix')
        if expected_metadata is not None:
            require(b[2] in expected_metadata and b[1]==expected_metadata[b[2]]['title'] and b[3]==expected_metadata[b[2]]['description'],'Actual llms line differs from exact reviewed metadata')
        literal.append({k:e[k] for k in ['old','new','old_sha256','new_sha256']})
    after=exact_edits(before,literal)
    return after,{'after_sha256':sha(after),'exact_inverse_or_actual_contexts':True,'edited_urls':sorted(seen)}

def xml_rows(raw):
    require(b'<!DOCTYPE' not in raw and b'<!ENTITY' not in raw,'Sitemap entity/DTD forbidden')
    root=ET.fromstring(raw);require(root.tag=='{http://www.sitemaps.org/schemas/sitemap/0.9}urlset','Sitemap namespace differs')
    fragments=list(re.finditer(rb'<url\b[^>]*>.*?</url>',raw,re.S));require(len(fragments)==len(root),'Sitemap fragment/element coverage differs')
    out={}
    for item,frag in zip(root,fragments):
        loc=item.find('{*}loc');last=item.find('{*}lastmod');require(loc is not None and last is not None and loc.text not in out,'Sitemap location/date missing or duplicate')
        require(str(loc.text).startswith(SITE),'Unexpected sitemap host')
        out[loc.text]={'raw':frag.group(),'start':frag.start(),'end':frag.end(),'lastmod':last.text}
    return out

def apply_nonlibrary_sitemap_dates(before,dates,*,approved_source_metadata,frozen_urls):
    """No new/removal/URL edit; only approved nonlibrary publication dates."""
    rows=xml_rows(before);replacements=[]
    for url,date in dates.items():
        require(url in rows and not url.startswith(SITE+'answers/') and url not in frozen_urls,'Nonlibrary date map has unknown/library/frozen URL')
        require(url in approved_source_metadata and date==approved_source_metadata[url]['date_modified'][:10],'Sitemap date is not actual approved metadata')
        raw=rows[url]['raw'];new=re.sub(rb'(<lastmod>).*?(</lastmod>)',lambda m:m[1]+date.encode()+m[2],raw,count=1,flags=re.S)
        replacements.append((rows[url]['start'],rows[url]['end'],new))
    after=before
    for a,b,new in sorted(replacements,reverse=True):after=after[:a]+new+after[b:]
    actual=xml_rows(after);require(set(actual)==set(rows),'Sitemap added/removed a URL')
    for url,row in rows.items():
        if url not in dates:require(actual[url]['raw']==row['raw'],'Unlisted sitemap URL element changed')
        else:require(actual[url]['lastmod']==dates[url],'Approved sitemap date was not rendered')
    reverse=after
    # Reconstruct using the full exact prior elements, not a text exclusion.
    spans=xml_rows(after)
    for url in sorted(dates,key=lambda u:spans[u]['start'],reverse=True):
        a,b=spans[url]['start'],spans[url]['end'];reverse=reverse[:a]+rows[url]['raw']+reverse[b:]
    require(reverse==before,'Nonlibrary sitemap inverse differs')
    buffer=io.BytesIO()
    with gzip.GzipFile(fileobj=buffer,filename='',mode='wb',compresslevel=9,mtime=0) as stream:stream.write(after)
    compressed=buffer.getvalue()
    proof={'after_sha256':sha(after),'exact_inverse_or_actual_contexts':True,'edited_urls':sorted(dates)}
    return after,compressed,proof,{'after_sha256':sha(compressed),'exact_inverse_or_actual_contexts':True,'gzip_matches_xml':True}

def public_url(path):
    return path.removesuffix('index.md') if path.endswith('index.md') else path.removesuffix('.md')+'/'


def require_exact_repair_render(path,body,html,meta):
    """Same owning signature, with explicit nonlibrary URL resolution.

    The ordinary helper's answer-only public_route is deliberately untouched.
    No caller text exclusion, source fact stripping or rendered-body waiver.
    """
    import markdown
    from types import SimpleNamespace
    from library_publication_hooks_candidate import on_page_content
    from library_owner_repair import safe_path
    from library_publication_consumers import _RenderSignature
    safe_path(path);require(path.endswith('.md'),'Repair render source must be Markdown')
    # MkDocs adds fenced_code to its default toc/tables extension set before
    # applying this repository's exact additional extensions.
    expected=markdown.markdown(body,extensions=['toc','tables','fenced_code','attr_list','md_in_html','def_list','footnotes','admonition'],extension_configs={'toc':{'permalink':True,'toc_depth':3}})
    expected=on_page_content(expected,page=SimpleNamespace(meta=meta))
    source=_RenderSignature(SITE+path,True);source.feed(expected)
    actual=_RenderSignature(SITE+public_url(path));actual.feed(html)
    require(source.tokens==actual.tokens,'Actual owner renderer differs from complete approved Markdown')

def validate_actual_search(before,after,*,changed_contexts,expected_records):
    """Compute actual installed Material entries from exact validated contexts."""
    from material.plugins.search.plugin import SearchIndex
    from types import SimpleNamespace
    old,new=json.loads(before),json.loads(after)
    require(set(old)==set(new) and {k:v for k,v in old.items() if k!='docs'}=={k:v for k,v in new.items() if k!='docs'},'Search configuration/non-doc data changed')
    require(set(changed_contexts)==set(expected_records),'Changed search context coverage differs')
    roots={public_url(p) for p in expected_records}
    root=lambda r:r.get('location','').split('#')[0]
    require([r for r in old['docs'] if root(r) not in roots]==[r for r in new['docs'] if root(r) not in roots],'Unlisted search row changed')
    for path,context in changed_contexts.items():
        expected=expected_records[path]
        require(context['markdown']==expected['body'] and context['meta']==expected['meta'],'Search context has stale effective body/meta')
        require_exact_repair_render(path,expected['body'],context['html'],expected['meta'])
        generated=SearchIndex(**new['config']);p=SimpleNamespace(meta=expected['meta'],title=expected['meta']['title'],content=context['html'],toc=context['toc'],url=public_url(path));generated.add_entry_from_context(p)
        actual=[r for r in new['docs'] if root(r)==public_url(path)]
        require(actual==generated.entries,'Actual search rows differ from actual reviewed render context: '+path)
    return {'after_sha256':sha(after),'exact_inverse_or_actual_contexts':True,'changed_source_paths':sorted(expected_records)}

def validate_render_context(path,record,context,rendered):
    require(context['markdown']==record['body'] and context['meta']==record['meta'],'Actual repair source/render context differs')
    require_exact_repair_render(path,record['body'],context['html'],record['meta'])
    require(context['rendered_html'].encode()==rendered,'Final repair HTML differs after capture')
    class Head(HTMLParser):
        def __init__(self):super().__init__();self.in_title=False;self.title='';self.canonical=[];self.meta={}
        def handle_starttag(self,t,a):
            a=dict(a)
            if t=='title':self.in_title=True
            if t=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
            if t=='meta':self.meta.setdefault(a.get('name') or a.get('property'),[]).append(a.get('content'))
        def handle_endtag(self,t):
            if t=='title':self.in_title=False
        def handle_data(self,d):
            if self.in_title:self.title+=d
    h=Head();h.feed(rendered.decode());title=record['meta']['title'];description=record['meta']['description']
    require(h.title==title+' | The Absence Manual','Actual repair document title stale')
    require(h.canonical==[SITE+public_url(path)],'Actual repair canonical differs')
    for field in ['og:title','twitter:title']:require(h.meta.get(field)==[title],'Actual repair social title stale')
    for field in ['description','og:description','twitter:description']:require(h.meta.get(field)==[description],'Actual repair description stale')
    return {'source_path':'docs/'+path,'after_sha256':sha(rendered),'source_render_exact':True}


def validate_content_surface(path,before_record,after_record,context,before,after):
    """Source content/head deltas do not license unrelated page chrome changes.

    Exact Source render + unchanged template suffix; outside that article the
    complete parsed token stream must match, apart from approved metadata,
    the two resource labels, and the combined stylesheet's href.
    """
    from library_owner_repair import validate_primary_labels,validate_pagination_labels,spans,LABELS
    raw_pair=[]
    for record,raw,version in [(before_record,before,'before'),(after_record,after,'after')]:
        text=raw.decode();matches=list(re.finditer(r'<article\b[^>]*>(.*?)</article>',text,re.S))
        require(len(matches)==1,'Actual content surface requires one article')
        match=matches[0];inner=match[1]
        marker='<p class="bw-editorial-byline">'
        if marker in inner:
            require(inner.count(marker)==1,'Editorial suffix is ambiguous');split=inner.index(marker)
        else:
            footer=re.search(r'\s*<hr>\s*<p class="manual-footer-version">.*?</p>\s*\Z',inner,re.S)
            require(footer is not None,'Exact existing template footer boundary missing');split=footer.start()
        content=inner[:split].strip();tail=inner[split:]
        require_exact_repair_render(path,record['body'],content,record['meta'])
        if version=='after':require(content==context['html'].strip(),'Final visible content differs from actual renderer context')
        raw_pair.append((text[:match.start(1)]+'__EXACT_SOURCE_CONTENT__'+tail+text[match.end(1):]).encode())
    # Both labels must still be exactly the two owner literals. The token
    # validator below retains all other nav content and structure.
    validate_primary_labels(public_url(path)+'index.html',before,after)
    class Surface(HTMLParser):
        def __init__(self,raw,meta,version):
            super().__init__(convert_charrefs=True);self.tokens=[];self.meta=meta;self.version=version;self.json_mode=False;self.json_text='';self.feed(raw.decode());self.close()
        def handle_starttag(self,t,a):
            attrs=[];d=dict(a)
            for k,v in a:
                if t=='meta' and k=='content':
                    key=d.get('name') or d.get('property')
                    field='title' if key in {'og:title','twitter:title'} else 'description' if key in {'description','og:description','twitter:description'} else None
                    if field:require(v==self.meta[field],'Metadata slot differs from exact Source metadata');v='__EXACT_'+field+'__'
                if t=='link' and d.get('rel')=='stylesheet' and k=='href':
                    require(re.search(r'combined-[0-9a-f]{16}\.css$',str(v)) is not None,'Unrelated stylesheet target');v='__EXACT_COMBINED_CSS__'
                attrs.append((k,v))
            self.tokens.append(('start',t,attrs))
            if t=='script' and d.get('type')=='application/ld+json':self.json_mode=True;self.json_text=''
        def handle_endtag(self,t):
            if t=='script' and self.json_mode:
                obj=json.loads(self.json_text)
                if obj.get('@type')==self.meta.get('schema_type','Article'):
                    for k,field in [('name','headline'),('headline','headline'),('description','description'),('datePublished','date_published'),('dateModified','date_modified')]:
                        require(obj.get(k)==self.meta[field],'Structured repair metadata is stale: '+k);obj[k]='__EXACT_'+field+'__'
                if obj.get('@type')=='BreadcrumbList':
                    require(obj['itemListElement'][-1]['name']==self.meta['title'],'Structured breadcrumb is stale');obj['itemListElement'][-1]['name']='__EXACT_title__'
                if obj.get('@type')=='Dataset':
                    require(obj.get('datePublished')==self.meta.get('published') and obj.get('dateModified')==self.meta.get('updated'),'Structured Research dataset dates are stale')
                    obj['dateModified']='__EXACT_updated__'
                self.tokens.append(('json',obj));self.json_mode=False
            self.tokens.append(('end',t))
        def handle_startendtag(self,t,a):self.handle_starttag(t,a)
        def handle_comment(self,d):self.tokens.append(('comment',d))
        def handle_decl(self,d):self.tokens.append(('decl',d))
        def handle_data(self,d):
            if self.json_mode:self.json_text+=d;return
            if d==self.meta['title'] or d==self.meta['title']+' | The Absence Manual':d=d.replace(self.meta['title'],'__EXACT_title__',1)
            for old,new in LABELS.values():
                label=old if self.version=='before' else new
                # Only isolated navigation label nodes (not arbitrary prose).
                if d.strip()==label:d=d.replace(label,'__EXACT_RESOURCE_'+old+'__')
                for prefix in ['Previous: ','Next: ']:
                    if d==prefix+label:d=prefix+'__EXACT_RESOURCE_'+old+'__'
            self.tokens.append(('data',d))
    a=Surface(raw_pair[0],before_record['meta'],'before');b=Surface(raw_pair[1],after_record['meta'],'after')
    require(a.tokens==b.tokens,'Content repair changes unrelated head/script/chrome/footer tokens')
    return {'source_path':'docs/'+path,'after_sha256':sha(after),'source_render_exact':True,'outside_approved_content_metadata_navigation_tokens_exact':True}
