"""Exact source/template-derived slots on finite Owner content surfaces.

No template output is accepted by a caller digest. Each actual fragment is
recomputed from complete approved Markdown/meta and the pinned real templates.
The ordinary navigation-only validator is deliberately not modified.
"""
import hashlib,json,re
from pathlib import Path
from html.parser import HTMLParser
from types import SimpleNamespace
from urllib.parse import urljoin,urlsplit
from library_owner_repair import require

CATALOG_SHA256='14aae64a5e969184bcc638bba935b19a76b18b20cc173f345bb74840b46c36b6'
EXTENSIONS=['toc','tables','fenced_code','attr_list','md_in_html','def_list','footnotes','admonition']
TOC_CONFIG={'permalink':True,'toc_depth':3}

def _sha(raw):return hashlib.sha256(raw).hexdigest()

class _Elements(HTMLParser):
    def __init__(self,text,tag,predicate):
        super().__init__(convert_charrefs=False);self.text=text;self.tag=tag;self.predicate=predicate;self.stack=[];self.found=[];self.lines=[0]
        for line in text.splitlines(keepends=True):self.lines.append(self.lines[-1]+len(line))
        self.feed(text);self.close();require(not self.stack,'Unclosed exact template element')
    def _at(self):
        line,col=self.getpos();return self.lines[line-1]+col
    def handle_starttag(self,t,a):
        if t==self.tag:self.stack.append((self._at(),dict(a)))
    def handle_endtag(self,t):
        if t==self.tag:
            require(self.stack,'Unmatched exact template element');start,attrs=self.stack.pop();at=self._at()
            closing=re.match(r'</'+re.escape(t)+r'\s*>',self.text[at:],re.I);require(closing is not None,'Template closing tag malformed')
            if self.predicate(attrs):self.found.append((start,at+closing.end(),self.text[start:at+closing.end()]))
    def handle_startendtag(self,t,a):pass

def _elements(text,tag,predicate):return sorted(_Elements(text,tag,predicate).found)

def _environment(template_root):
    import jinja2,material,yaml
    catalog_path=Path(__file__).with_name('library_owner_repair_surface_templates.json')
    raw=catalog_path.read_bytes();require(_sha(raw)==CATALOG_SHA256,'Exact Owner surface template catalog differs')
    catalog=json.loads(raw);root=Path(template_root);theme=Path(material.__file__).parent/'templates'
    for path,expected in catalog['repository_templates'].items():
        require(_sha((root/path).read_bytes()) in expected['accepted_actual_raw_sha256'],'Actual Owner repository template differs: '+path)
    for path,expected in catalog['material_templates'].items():
        require(_sha((theme/path).read_bytes())==expected,'Actual installed Material template differs: '+path)
    config=yaml.safe_load((root/'mkdocs.yml').read_text(encoding='utf8'))
    require(config['site_name']=='The Absence Manual' and config['theme']['language']=='en','Actual title/language template configuration differs')
    require(config['markdown_extensions']==[{'toc':TOC_CONFIG},'tables','attr_list','md_in_html','def_list','footnotes','admonition'],'Actual Markdown TOC extension configuration differs')
    env=jinja2.Environment(loader=jinja2.FileSystemLoader([root/'overrides',theme]),auto_reload=False)
    for path,expected in catalog['repository_templates'].items():
        # Pin the exact existing Jinja loader input as well as known raw bytes;
        # this does not normalize any built output or comparator token.
        require(_sha(env.loader.get_source(env,path.removeprefix('overrides/'))[0].encode())==expected['actual_Jinja_source_sha256'],'Actual template engine input differs: '+path)
    for path,expected in catalog['material_templates'].items():
        require(_sha(env.loader.get_source(env,path)[0].encode())==expected,'Override shadows an exact pinned Material template: '+path)
    # The only template URL operation in these exact fragments is a TOC hash.
    def hash_url(value):
        require(isinstance(value,str) and value.startswith('#'),'Source skip URL is not an exact TOC hash')
        return value
    env.filters['url']=hash_url
    cfg={'theme':{'language':'en'},'mdx_configs':{'toc':TOC_CONFIG}}
    lang=env.get_template('partials/language.html').make_module({'config':cfg})
    return env,cfg,lang,catalog

def template_document_title(meta):
    # Exact overrides/main.html htmltitle expression; unlike social titles,
    # Jinja's striptags collapses the two legacy resource-title spaces.
    from markupsafe import Markup
    require(isinstance(meta.get('title'),str),'Source title missing')
    return str(Markup(meta['title']).striptags())+' | The Absence Manual'

def project_source_template_slots(path,record,raw,*,template_root):
    import markdown
    from mkdocs.structure.toc import get_toc
    env,cfg,lang,catalog=_environment(template_root)
    md=markdown.Markdown(extensions=EXTENSIONS,extension_configs={'toc':TOC_CONFIG});md.convert(record['body'])
    toc=get_toc(md.toc_tokens);page=SimpleNamespace(meta=record['meta'],toc=toc)
    context={'page':page,'config':cfg,'lang':lang}
    text=raw.decode();edits=[];markers=[]
    def add(start,end,old,new,kind):
        require(text[start:end]==old and new not in text,'Source-bound template slot is missing/ambiguous')
        edits.append((start,end,old,new));markers.append({'kind':kind,'old_sha256':_sha(old.encode()),'marker':new})
    expected=env.get_template('partials/toc.html').render(**context)
    expected_nav=_elements(expected,'nav',lambda a:'md-nav--secondary' in a.get('class','').split())
    require(len(expected_nav)==1,'Actual TOC template does not produce exactly one root')
    expected_nav=expected_nav[0][2]
    actual=_elements(text,'nav',lambda a:'md-nav--secondary' in a.get('class','').split())
    top=list(toc);visible=top[0].children if top and top[0].level==1 else top
    primary=_elements(text,'nav',lambda a:'md-nav--primary' in a.get('class','').split())
    require(len(primary)==1,'Actual current-page primary nav missing/repeated')
    route=path.removesuffix('index.md') if path.endswith('/index.md') or path=='index.md' else path.removesuffix('.md')+'/'
    current='https://docs.broadcastwell.com/'+route
    # Material nav-item.html integrates a TOC only when the current page is
    # actually a primary-nav member. The eleven Research leaves are not.
    def self_link(a):
        u=urlsplit(urljoin(current,a.get('href','')))
        return ('md-nav__link--active' in a.get('class','').split() and not u.fragment and not u.query
                and u.geturl()==current)
    members=_elements(primary[0][2],'a',self_link)
    require(len(members)<=1,'Repeated primary current-page membership')
    integrated=bool(members) and bool(visible)
    require(len(actual)==1+integrated and sum(primary[0][0]<a<b<primary[0][1] for a,b,_ in actual)==integrated,'Unexpected source TOC count/placement')
    for i,(a,b,fragment) in enumerate(actual):
        require(fragment==expected_nav,'Actual current-page TOC differs from complete source/pinned template: '+path)
        add(a,b,fragment,'<!--__EXACT_SOURCE_TOC_'+str(i)+'__-->','source-toc')
    base=env.loader.get_source(env,'base.html')[0]
    skip=re.search(r'{% if page\.toc \| first is defined %}(.*?){% endif %}',base,re.S)
    require(skip is not None,'Pinned Material skip expression missing')
    skip_expected=env.from_string('{% if page.toc | first is defined %}'+skip[1]+'{% endif %}').render(**context)
    expected_anchors=_elements(skip_expected,'a',lambda a:a.get('class')=='md-skip')
    actual_anchors=_elements(text,'a',lambda a:a.get('class')=='md-skip')
    require(len(actual_anchors)==len(expected_anchors)==bool(top),'Actual skip-link count differs from source TOC')
    if top:
        a,b,fragment=actual_anchors[0]
        require(fragment==expected_anchors[0][2],'Actual skip target/attributes/text differ from source/template')
        add(a,b,fragment,'<!--__EXACT_SOURCE_SKIP__-->','source-skip')
    # Compare the COMPLETE actual footer with the pinned real template before
    # projecting only its one metadata-derived time element. All surrounding
    # commercial, copyright, links, next-review and licence tokens remain.
    if record['meta'].get('page_class')=='research':
        main=env.loader.get_source(env,'main.html')[0]
        footerblock=main.split('{% block footer %}',1)[1]
        branch=re.search(r'{% if page and page\.meta\.get\("page_class"\) == "research" %}(.*?){% else %}',footerblock,re.S)
        require(branch is not None,'Pinned Research footer branch missing')
        footer_expected=env.from_string(branch[1]).render(**context)
    else:footer_expected=env.get_template('partials/site-footer.html').render(**context)
    ef=_elements(footer_expected,'footer',lambda a:'bw-footer' in a.get('class','').split())
    af=_elements(text,'footer',lambda a:'bw-footer' in a.get('class','').split())
    require(len(ef)==len(af)==1 and ef[0][2]==af[0][2],'Complete actual footer differs from exact Source metadata/pinned template')
    times=_elements(af[0][2],'time',lambda a:True)
    require(len(times)==1,'Exact current footer time missing/repeated')
    a,b,fragment=times[0];add(af[0][0]+a,af[0][0]+b,fragment,'<!--__EXACT_SOURCE_FOOTER_TIME__-->','source-footer-time')
    for (a,b,old,new),(c,d,_,_) in zip(sorted(edits),sorted(edits)[1:]):require(b<=c,'Source template slots overlap')
    projected=text
    for a,b,old,new in sorted(edits,reverse=True):projected=projected[:a]+new+projected[b:]
    reverse=projected
    for a,b,old,new in edits:
        require(reverse.count(new)==1,'Template inverse marker ambiguous');reverse=reverse.replace(new,old,1)
    require(reverse==text,'Exact template-slot inverse differs')
    return projected.encode(),{'source_path':path,'source_body_sha256':_sha(record['body'].encode()),
        'source_meta_sha256':_sha(json.dumps(record['meta'],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()),
        'template_catalog_sha256':CATALOG_SHA256,'slots':markers,'complete_footer_validated':True,'exact_forward_inverse':True}

def revalidate_bound_content_navigation(path,proof,before,after,*,source_note,template_root):
    """Final artifact gate re-derives the projection; no caller skip flag."""
    from library_related_chapter_links import source_body
    from library_owner_repair import validate_primary_labels
    require(isinstance(proof,dict) and set(proof)=={'before_full_source','after_full_source','before_html_sha256','after_html_sha256'},'Exact content-navigation source proof missing')
    require(proof['before_html_sha256']==_sha(before) and proof['after_html_sha256']==_sha(after),'Content-navigation actual HTML bytes differ')
    projected=[]
    for version,raw in [('before',before),('after',after)]:
        full=proof[version+'_full_source'];require(isinstance(full,str) and _sha(full.encode())==source_note[version+'_sha256'],'Content-navigation Root source pin differs')
        meta,body=source_body(full)
        value,_=project_source_template_slots(path,{'meta':meta,'body':body},raw,template_root=template_root)
        projected.append(value)
    route=path.removesuffix('index.md') if path.endswith('/index.md') or path=='index.md' else path.removesuffix('.md')+'/'
    validate_primary_labels(route+'index.html',*projected)
    return True
