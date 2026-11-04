"""Exact one-release owner repair policy; ordinary S5 gates are not modified.

These pure checks do not grant authority from a filename or a claimed flag.
Root's bound source plan and independent actual artifact/PDF reviews are separate.
No renderer, browser, network call or public sidecar writer lives here.
"""
from __future__ import annotations
import copy, hashlib, json, posixpath, re
from html import escape
from html.parser import HTMLParser
from pathlib import PurePosixPath, PureWindowsPath
from urllib.parse import urljoin, urlsplit

POLICY='OWNER_RISK_VERIFY_REPAIR_2026_11_03_V1'
AUTHORITY_SHA256='e9e33b6921d4eb0b78550f556b314cab937509c6c120f74261d59c9073cf2e88'
REGISTRY_SHA256='c346b0f6a7997449f4eccbaf662b53f7ae25ba21a57341f786dc7d673db1798c'
HANDOFF_SHA256='3f09732e9a23c36ea0852fa6dcec96c0c1c9f0c1cb55d2f4af722072ac17eb1b'
NAV_MAP_SHA256='e8d4688604fdcb57e38944ce6937ce7fa788da73ec96b77902042990f8806f4c'
OLD_CSS='assets/stylesheets/combined-102e6961704e82a1.css'
OLD_CSS_SHA256='102e6961704e82a1ba00e7fa7980462b0020768c9f6e6684ca439c8a683a6c69'
SITE='https://docs.broadcastwell.com/'
LABELS={
 'resources/audit/executive-template/':('Category Audit ,  executive delivery template','Executive delivery template (retired Category Audit format, kept for reference)'),
 'resources/audit/sample/':('Synthetic Category Audit ,  Northstar Lab','Synthetic audit example, Northstar Lab (retired Category Audit format)')}
CSS_SOURCES=frozenset({'docs/assets/manual.css','docs/assets/learning.css'})
MANUAL_PDFS=frozenset({'absence-manual.pdf','absence-manual-v1.0-2026-08-18.pdf'})
SAMPLE_PDFS=frozenset({'assets/samples/Kalvenor_Sample_Category_Audit.pdf',
 'assets/samples/FieldEdge_Category_Audit_v2.pdf',
 'assets/samples/Category_Audit_sample_Kalvenor_fictional.pdf',
 'assets/samples/Category_Audit_sample_FieldEdge_rehearsal.pdf',
 'assets/samples/WhiteLabel_Sample_Category_Audit_v2.pdf',
 'assets/samples/White_label_Category_Audit_sample.pdf'})
PDF_PATHS=MANUAL_PDFS|SAMPLE_PDFS
DERIVED=frozenset({'llms.txt','search/search_index.json','sitemap.xml','sitemap.xml.gz'})
SOURCE_CLASSES=frozenset({'resource_retitle','manual_offer_or_rates','answer_rates_label',
 'answer_metadata','appendix_seo','rule4_fact','rule4_record_reading','specific_precision','css_comment','repository_rule','sample_pdf','legal_video'})
ARTIFACT_CLASSES=frozenset({'navigation_only','source_content','source_metadata','generated_hub',
 'derived','css_source','css_bundle','manual_pdf','sample_pdf'})
_TOKEN=object()

class RepairError(ValueError):pass
def require(ok,message):
    if not ok:raise RepairError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def encoded(value):return (json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'))+'\n').encode()
def digest(value):return sha(encoded(value))
def json_unique(raw):
    def pairs(items):
        d={}
        for k,v in items:
            require(k not in d,'Duplicate JSON key: '+k);d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs)

def validate_authority_receipt(raw,expected_sha256,*,local_pdf=None):
    require(sha(raw)==expected_sha256,'Root authority read receipt hash differs')
    d=json_unique(raw)
    fields={'schema_version','reviewer','review_kind','policy','authority_pdf_sha256','pages_actually_read','actual_full_read_complete','local_hash_verified','recorded_utc'}
    require(set(d)==fields,'Authority receipt contains missing/private/unapproved fields')
    require(d['schema_version']==1 and d['reviewer']=='root' and d['review_kind']=='owner-brief-local-full-read' and d['policy']==POLICY,'Actual Root authority read missing')
    require(d['authority_pdf_sha256']==AUTHORITY_SHA256 and type(d['pages_actually_read']) is int and d['pages_actually_read']==5 and d['actual_full_read_complete'] is True and d['local_hash_verified'] is True,'Full five-page Root read/local hash verification missing')
    require(bool(re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00',str(d['recorded_utc']))),'Authority read timestamp malformed')
    if local_pdf is not None:require(sha(local_pdf)==AUTHORITY_SHA256,'Supplied local authority PDF changed')
    return d


def validate_before_read_receipt(raw,expected_sha256,*,plan,actual_prior_files):
    require(sha(raw)==expected_sha256,'Root current before-read receipt bytes differ')
    d=json_unique(raw)
    require(d.get('approved') is True and d.get('reviewer')=='root' and d.get('review_kind')=='root-current-owner-repair-before-read' and d.get('policy')==POLICY and d.get('production_binding')==plan.data['baseline_production_binding'],'Actual current Root before-read binding missing')
    expected={s for s in plan.data['source_changes'] if s.startswith('docs/')}
    require(set(d.get('sources',{}))==expected,'Current before-read source coverage differs')
    for source,row in d['sources'].items():
        rel=source[5:];public=(rel.removesuffix('index.md') if rel.endswith('index.md') else rel.removesuffix('.md')+'/')+'index.html' if rel.endswith('.md') else rel
        require(row.get('public_path')==public and public in actual_prior_files and row.get('public_before_sha256')==sha(actual_prior_files[public]),'Before read does not bind the actual prior public source/page')
        require(row.get('actually_read') is True and row.get('javascript_off_or_raw_source_read') is True and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|\+00:00)',str(row.get('recorded_utc'))),'Actual current before read incomplete')
    return {'actual_current_before_source_reads':len(expected),'production_binding':d['production_binding']}
def safe_path(value):
    require(isinstance(value,str) and value and '\\' not in value,'Repair path must be a POSIX relative path')
    p=PurePosixPath(value);w=PureWindowsPath(value)
    require(not p.is_absolute() and not w.is_absolute() and not w.drive and '..' not in p.parts and p.as_posix()==value,'Repair path escapes its namespace')
    require(not value.startswith(('.git/','file:','http:','https:')),'Private/protocol path is not a public artifact')
    return value

def exact_edits(before,edits):
    """Literal source/line edits with an exact reverse proof, never broad replace."""
    require(isinstance(before,bytes) and isinstance(edits,list),'Exact edits need bytes/list')
    result=before
    for e in edits:
        require(set(e)=={'old','new','old_sha256','new_sha256'},'Literal edit fields differ')
        old,new=e['old'].encode(),e['new'].encode()
        require(old and old!=new and sha(old)==e['old_sha256'] and sha(new)==e['new_sha256'],'Literal edit span hash differs')
        require(result.count(old)==1,'Literal old span missing or repeated')
        result=result.replace(old,new,1)
    reverse=result
    for e in reversed(edits):
        old,new=e['old'].encode(),e['new'].encode()
        require(reverse.count(new)==1,'Literal new span is ambiguous for inverse proof')
        reverse=reverse.replace(new,old,1)
    require(reverse==before,'Literal edits do not reconstruct exact prior bytes')
    return result

def css_comment_only(before,after):
    strip=lambda b:re.sub(rb'/\*.*?\*/',b'',b,flags=re.S)
    require(before!=after and strip(before)==strip(after),'CSS repair changes a rule rather than comment text only')

def freeze_exact(candidate,pins):
    for path,expected in pins.items():
        safe_path(path);require(path in candidate and sha(candidate[path])==expected,'Frozen public bytes changed: '+path)

class TagSpans(HTMLParser):
    def __init__(self,raw):
        super().__init__(convert_charrefs=False);self.text=raw.decode();self.lines=[0];self.styles=[];self.primary=[];self.navdepth=0;self.navstart=None
        for line in self.text.splitlines(keepends=True):self.lines.append(self.lines[-1]+len(line))
    def absolute_offset(self):
        line,column=self.getpos();return self.lines[line-1]+column
    def byte(self,n):return len(self.text[:n].encode())
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='link' and a.get('rel')=='stylesheet':
            start=self.absolute_offset();self.styles.append((self.byte(start),self.byte(start+len(self.get_starttag_text())),a.get('href')))
        if tag=='nav':
            if self.navdepth:self.navdepth+=1
            elif 'md-nav--primary' in a.get('class','').split():self.navdepth=1;self.navstart=self.absolute_offset()
    def handle_endtag(self,tag):
        if tag=='nav' and self.navdepth:
            self.navdepth-=1
            if not self.navdepth:
                start=self.absolute_offset();m=re.match(r'</nav\s*>',self.text[start:],re.I);require(m is not None,'Malformed nav closing tag')
                self.primary.append((self.byte(self.navstart),self.byte(start+m.end())))
def spans(raw):
    p=TagSpans(raw);p.feed(p.text);p.close();require(p.navdepth==0,'Unclosed primary navigation');return p
def resolve_artifact(page,href):
    u=urlsplit(urljoin(SITE+safe_path(page),str(href)))
    require(u.scheme=='https' and u.netloc=='docs.broadcastwell.com' and not u.query and not u.fragment,'Stylesheet URL is not a local fixed artifact')
    return safe_path(u.path.lstrip('/'))

def restore_frozen_stylesheet(*,page,before,candidate,new_bundle_path,new_bundle_bytes,baseline_files):
    """Return bytes only; the original45 whole-HTML guard must still run next."""
    require(OLD_CSS in baseline_files and sha(baseline_files[OLD_CSS])==OLD_CSS_SHA256,'Frozen prior stylesheet bytes differ')
    safe_path(new_bundle_path)
    require(new_bundle_path=='assets/stylesheets/combined-'+sha(new_bundle_bytes)[:16]+'.css','New bundle path is not its exact generated content hash')
    a,b=spans(before),spans(candidate)
    old=[x for x in a.styles if resolve_artifact(page,x[2])==OLD_CSS]
    require(len(a.styles)==len(b.styles)==1 and len(old)==1,'Frozen page needs exactly its original combined stylesheet')
    x,y,href=b.styles[0]
    require(resolve_artifact(page,href) in {OLD_CSS,new_bundle_path},'Frozen stylesheet has an unrelated target')
    original=before[old[0][0]:old[0][1]];current=candidate[x:y]
    # Only the href may differ. Attribute/order/tag changes remain rejected.
    oldhref=old[0][2].encode();newhref=href.encode()
    require(current.replace(newhref,oldhref,1)==original and current.count(newhref)==1,'Frozen stylesheet tag differs beyond exact href')
    return candidate[:x]+original+candidate[y:]

class NavLabels(HTMLParser):
    def __init__(self,fragment,page):
        super().__init__(convert_charrefs=False);self.fragment=fragment.decode();self.page=page;self.tokens=[];self.anchor=None;self.changed=[]
    def handle_starttag(self,t,a):
        if t=='a':self.anchor=urlsplit(urljoin(SITE+self.page,dict(a).get('href',''))).path.lstrip('/')
        self.tokens.append(('start',self.get_starttag_text()))
    def handle_endtag(self,t):
        self.tokens.append(('end',t))
        if t=='a':self.anchor=None
    def handle_startendtag(self,t,a):self.tokens.append(('void',self.get_starttag_text()))
    def handle_entityref(self,n):self.tokens.append(('entity',n))
    def handle_charref(self,n):self.tokens.append(('charref',n))
    def handle_comment(self,v):self.tokens.append(('comment',v))
    def handle_data(self,v):
        self.tokens.append(('data',v,self.anchor))

def validate_primary_labels(page,before,after):
    """Parse the whole actual primary nav; permit just the two exact labels."""
    old,new=spans(before),spans(after);require(len(old.primary)==len(new.primary)==1,'Expected one actual primary navigation')
    oa,ob=old.primary[0];na,nb=new.primary[0]
    a,b=NavLabels(before[oa:ob],page),NavLabels(after[na:nb],page);a.feed(a.fragment);b.feed(b.fragment);a.close();b.close()
    require(len(a.tokens)==len(b.tokens),'Navigation structure changed')
    changes=[];expected=before[oa:ob]
    for x,y in zip(a.tokens,b.tokens):
        if x==y:continue
        require(x[0]==y[0]=='data' and x[2]==y[2] and x[2] in LABELS,'Navigation changed outside the two authorized labels')
        oldlabel,newlabel=LABELS[x[2]]
        require(x[1].strip()==oldlabel and y[1].strip()==newlabel,'Navigation label is not the exact owner literal')
        require(re.match(r'^\s*',x[1]).group()==re.match(r'^\s*',y[1]).group() and re.search(r'\s*$',x[1]).group()==re.search(r'\s*$',y[1]).group(),'Navigation label whitespace/layout changed')
        require(expected.count(x[1].encode())==1,'Owner label text node repeated')
        expected=expected.replace(x[1].encode(),y[1].encode(),1)
        changes.append(x[2])
    require(sorted(changes)==sorted(LABELS),'Both and only both resource labels must change once')
    require(expected==after[na:nb],'Navigation has an unapproved byte difference')
    return (oa,ob),(na,nb)

def validate_navigation_only(page,before,after,*,old_css=None,new_css=None):
    """Two text nodes at the same hrefs; everything else is exact bytes."""
    (oa,ob),(na,nb)=validate_primary_labels(page,before,after)
    left=before[:oa]+b'__EXACT_PRIMARY_NAV__'+before[ob:];right=after[:na]+b'__EXACT_PRIMARY_NAV__'+after[nb:]
    # The actual Manual template also prints Previous/Next labels. Only
    # matching links to the same two resources inside the unique parsed
    # bw-document-pagination nav may change. No article text is masked.
    left,right=validate_pagination_labels(page,left,right)
    if old_css is not None or new_css is not None:
        require(old_css and new_css,'Both exact stylesheet tags are required')
        require(left.count(old_css)==right.count(new_css)==1,'Actual stylesheet tag missing/repeated')
        a,b=spans(old_css),spans(new_css)
        require(len(a.styles)==len(b.styles)==1,'Exact stylesheet tags required')
        require(new_css.count(b.styles[0][2].encode())==1 and new_css.replace(b.styles[0][2].encode(),a.styles[0][2].encode(),1)==old_css,'Stylesheet changed beyond href')
        left=left.replace(old_css,b'__EXACT_STYLESHEET__',1);right=right.replace(new_css,b'__EXACT_STYLESHEET__',1)
    require(left==right,'Navigation-only page changed outside primary nav/approved stylesheet')
    return {'path':page,'only_two_owner_labels':True,'outside_fragments_byte_exact':True}


def validate_pagination_labels(page,before,after):
    pattern=rb'<nav\b[^>]*class="bw-document-pagination"[^>]*>.*?</nav>'
    aa=list(re.finditer(pattern,before,re.S));bb=list(re.finditer(pattern,after,re.S))
    require(len(aa)==len(bb) and len(aa)<=1,'Document pagination structure changed')
    if not aa:return before,after
    a,b=aa[0],bb[0];x,y=NavLabels(a[0],page),NavLabels(b[0],page)
    x.feed(x.fragment);y.feed(y.fragment);x.close();y.close()
    require(len(x.tokens)==len(y.tokens),'Document pagination structure changed')
    expected=a[0]
    for old,new in zip(x.tokens,y.tokens):
        if old==new:continue
        require(old[0]==new[0]=='data' and old[2]==new[2] and old[2] in LABELS,'Pagination changed outside the two resource labels')
        prefix='Previous: ' if old[1].startswith('Previous: ') else 'Next: ' if old[1].startswith('Next: ') else None
        require(prefix and old[1]==prefix+LABELS[old[2]][0] and new[1]==prefix+LABELS[old[2]][1],'Pagination label is not exact owner literal')
        require(expected.count(old[1].encode())==1,'Pagination label repeated')
        expected=expected.replace(old[1].encode(),new[1].encode(),1)
    require(expected==b[0],'Pagination has an unapproved byte change')
    return before[:a.start()]+b'__EXACT_PAGINATION__'+before[a.end():],after[:b.start()]+b'__EXACT_PAGINATION__'+after[b.end():]

def navigation_repair_universe(prior,frozen_html):
    found=set()
    for page,raw in prior.items():
        if not page.endswith('.html') or page in frozen_html:continue
        parsed=spans(raw)
        if not parsed.primary:continue
        require(len(parsed.primary)==1,'Actual prior page has repeated primary navigation')
        a,b=parsed.primary[0];n=NavLabels(raw[a:b],page);n.feed(n.fragment);n.close()
        seen={t[2] for t in n.tokens if t[0]=='data' and t[2] in LABELS and t[1].strip()==LABELS[t[2]][0]}
        require(seen==set(LABELS),'Actual prior primary nav has unexpected/missing retired labels')
        found.add(page)
    return found

def validate_source_class(path,row,*,answer_paths,research_paths,bank_ids,frozen_sources):
    safe_path(path);require(path.removeprefix('docs/') not in frozen_sources,'Frozen source repair is forbidden')
    kind=row.get('class');require(kind in SOURCE_CLASSES,'Unknown source repair class')
    if kind=='resource_retitle':require(path in {'docs/resources/audit/executive-template.md','docs/resources/audit/sample.md'},'Unlisted resource title')
    elif kind=='manual_offer_or_rates':require(path in {'docs/why-does-chatgpt-not-mention-us.md','docs/resources/three-rates.md'},'Unlisted Manual/rates source')
    elif kind=='answer_rates_label':require(bank_ids.get(path.removeprefix('docs/'))=='LB-Q0531','Rates label is not Q0531')
    elif kind=='answer_metadata':require(bank_ids.get(path.removeprefix('docs/')) in {'LB-Q0623','LB-Q0299','LB-Q0641'},'Description fix is not one of three eligible records')
    elif kind=='appendix_seo':require(path=='docs/absence-rules.md','SEO title repair is only exact Appendix B')
    elif kind=='legal_video':require(path=='docs/answers/chatgpt/which-legal-practice-software-does-chatgpt-recommend.md' and bank_ids.get(path[5:])=='LB-Q0591','Legal media repair is not the exact reviewed unfrozen leaf')
    elif kind=='rule4_fact':require(path.removeprefix('docs/') in answer_paths|research_paths,'Rule4 source is outside actual answer/Research universe')
    elif kind in {'rule4_record_reading','specific_precision'}:
        from library_owner_repair_required28 import validate_named_case
        rel=path.removeprefix('docs/')
        require(path.startswith('docs/') and rel in answer_paths|research_paths,'Finite28 source is outside actual universe')
        validate_named_case(rel,kind,bank_ids)
    elif kind=='css_comment':require(path in CSS_SOURCES,'Unlisted CSS source')
    elif kind=='repository_rule':require(path=='CLAUDE.md','Only exact CLAUDE line is authorized')
    elif kind=='sample_pdf':require(path.removeprefix('docs/') in SAMPLE_PDFS,'Unlisted sample PDF')

def validate_quality_transition(before,after,*,changed_content_paths,frozen_paths,post_s5_binding=None):
    """Keep honest FAIL rows; no prior PASS or comparison-scope regression."""
    count=326
    if post_s5_binding is not None:
        from library_owner_repair_post_s5 import PostS5Binding
        require(isinstance(post_s5_binding,PostS5Binding),'Arbitrary post-S5 count is forbidden');post_s5_binding.check()
        require(set(before['page_readiness'])==post_s5_binding.pages,'Post-S5 quality universe differs');count=307
    pairs=count*(count-1)//2
    require(after.get('analysis_completed') is True and after.get('baseline_exceptions')==0,'Whole current analysis/zero exceptions missing')
    require(after.get('pair_count')==pairs and len(after.get('page_readiness',{}))==count,'Owner repair must keep all actual326 articles')
    require(set(before['page_readiness'])==set(after['page_readiness']),'Owner repair changes the article universe')
    require(before.get('analysis_completed') is True and before.get('baseline_exceptions')==0 and before.get('pair_count')==pairs,'Actual prior whole326 zero-exception report missing')
    require(len(frozen_paths)==45 and frozen_paths<=set(after['page_readiness']),'Exactly accepted45 deferred rows required')
    for p in frozen_paths:
        require(after['page_readiness'][p].get('status')=='DEFERRED_FIELD_TEST' and after['page_readiness'][p].get('passed') in {False,None},'Frozen row cannot become current PASS')
    errors=[]
    for p,row in before['page_readiness'].items():
        if row.get('passed') is True and after['page_readiness'][p].get('passed') is not True:errors.append('Prior PASS regressed: '+p)
    from library_publication_release import _violation_worsened
    for name in ['literal','runtime']:
        a,b=before['comparison_scopes'][name],after['comparison_scopes'][name]
        require(a.get('all_pairs_compared') is True and a.get('pair_count')==pairs,'Actual prior both-scope proof missing')
        require(b.get('all_pairs_compared') is True and b.get('pair_count')==pairs,'Both actual326 comparison scopes required')
        old={r['key']:r for r in a['violations']}
        for r in b['violations']:
            require(set(r['pages'])<=set(after['page_readiness']),'Unknown comparison page')
            if set(r['pages'])<=frozen_paths:continue
            if _violation_worsened(r,old.get(r['key'])):errors.append({'scope':name,'new_or_worse':r})
    require(not after.get('global_fatal_errors'),'Whole current analysis has a fatal error')
    require(not errors,'Owner repair worsens current quality: '+str(errors))
    return {'both_scope_nonregression':True,'prior_PASS_regressions':0,
            'changed_content_paths':sorted(changed_content_paths),'actual_current_FAIL_rows_retained':sum(r.get('status')=='FAIL' for r in after['page_readiness'].values()),'S5_full_PASS_granted':False}

def freeze_xml_exact(raw,rows):
    require(b'<!DOCTYPE' not in raw and b'<!ENTITY' not in raw,'Sitemap declaration forbidden')
    fragments=re.findall(rb'<url\b[^>]*>.*?</url>',raw,re.S)
    for row in rows:
        needle=('<loc>'+row['url']+'</loc>').encode()
        found=[f for f in fragments if needle in f]
        require(len(found)==1 and found[0]==row['exact_entry'].encode() and sha(found[0])==row['sha256'],'Frozen sitemap entry differs')

class OwnerRepairPlan:
    """A sealed exact Root plan, not a general nonlibrary/over50 whitelist."""
    def __init__(self,data,freeze_data,token):
        require(token is _TOKEN,'Owner repair requires a bound policy plan')
        self.data=copy.deepcopy(data);self.freeze_data=copy.deepcopy(freeze_data);self._seal=digest([self.data,self.freeze_data])
    @classmethod
    def bind(cls,raw,expected_sha256,*,authority_read_receipt,registry_bytes,handoff_bytes,nav_map_bytes,actual_prior_binding,actual_answer_paths,actual_research_paths,bank_ids,local_authority_pdf=None,post_s5_binding=None):
        require(sha(raw)==expected_sha256,'Root repair plan hash differs')
        d=json_unique(raw);require(d.get('schema_version')==1 and d.get('kind')==POLICY,'Unknown owner repair dispatch')
        require(d.get('approved') is True and d.get('review_kind')=='root-exact-owner-repair-source-plan' and d.get('Root_actual_source_review_complete') is True,'Exact Root source-plan review missing')
        require(d.get('authority_pdf_sha256')==AUTHORITY_SHA256,'Wrong owner brief authority')
        validate_authority_receipt(authority_read_receipt,d.get('authority_read_receipt_sha256'),local_pdf=local_authority_pdf)
        require(sha(registry_bytes)==d.get('freeze_registry_sha256')==REGISTRY_SHA256 and sha(handoff_bytes)==d.get('freeze_handoff_sha256')==HANDOFF_SHA256,'Wrong accepted45 authority')
        require(sha(nav_map_bytes)==d.get('freeze_nav_map_sha256')==NAV_MAP_SHA256,'Wrong unchanged frozen nav map')
        require(d.get('baseline_production_binding')==actual_prior_binding,'Repair plan is not bound to actual current production')
        count=326
        if post_s5_binding is not None:
            from library_owner_repair_post_s5 import PostS5Binding
            require(isinstance(post_s5_binding,PostS5Binding),'Post-S5 plan binding is not trusted');post_s5_binding.check()
            require(set(actual_answer_paths)==post_s5_binding.pages and d.get('post_s5_context_sha256')==digest(post_s5_binding.data),'Owner plan/post-S5 context differs')
            require(d.get('Source_rule4_relevance_inventory_complete') is True,'Current Rule4 inventory is incomplete')
            count=307
        require(d.get('article_count')==count and d.get('retirements')==[] and d.get('new_articles')==[],'Owner repair cannot activate parked retirements or change article count')
        require(isinstance(d.get('source_changes'),dict) and isinstance(d.get('artifact_scope'),dict),'Finite source/artifact maps missing')
        if any(r.get('class') in {'rule4_record_reading','specific_precision'} for r in d['source_changes'].values()):
            from library_owner_repair_required28 import validate_complete_required_scope
            validate_complete_required_scope(d)
        nav=json.loads(nav_map_bytes);frozen=set(nav['pages']);protected={r['served_html_path'] for r in nav['pages'].values()}|{r['path'] for r in nav['presentation_asset_pins']}
        require(len(frozen)==45 and len(protected)==50,'Accepted freeze coverage differs')
        require(len(actual_answer_paths)==count and set(bank_ids)==set(actual_answer_paths),'Actual production326 identity coverage required')
        for p,row in d['source_changes'].items():
            validate_source_class(p,row,answer_paths=set(actual_answer_paths),research_paths=set(actual_research_paths),bank_ids=bank_ids,frozen_sources=frozen)
            require(re.fullmatch('[0-9a-f]{64}',str(row.get('before_sha256'))) and re.fullmatch('[0-9a-f]{64}',str(row.get('after_sha256'))),'Source before/after SHA malformed')
        require(not set(d['artifact_scope'])&protected,'Owner artifact map includes frozen bytes')
        for p,row in d['artifact_scope'].items():
            safe_path(p);require(row.get('class') in ARTIFACT_CLASSES,'Unknown public repair class')
            require(re.fullmatch('[0-9a-f]{64}',str(row.get('before_sha256'))) or row.get('before_sha256') is None,'Before artifact SHA malformed')
            if row['class']=='navigation_only':require(p.endswith('.html'),'Navigation repair must name actual HTML')
            if row['class'] in {'source_content','source_metadata'}:
                require(row.get('source_path') in d['source_changes'],'Changed HTML lacks its exact source repair')
            if row['class']=='generated_hub':
                require(row.get('source_path') in d.get('generated_hubs',{}) and re.fullmatch(r'docs/answers/(?:[a-z-]+/)?index\.md',row['source_path']),'Generated hub lacks finite Root metadata/body approval')
            if row['class']=='derived':require(p in DERIVED,'Unknown derived repair artifact')
            if row['class']=='manual_pdf':require(p in MANUAL_PDFS,'Unlisted Manual PDF repair')
            if row['class']=='sample_pdf':require(p in SAMPLE_PDFS,'Unlisted sample PDF repair')
            if row['class']=='css_source':require('docs/'+p in CSS_SOURCES,'Unlisted raw CSS repair')
            if row['class']=='css_bundle':require(bool(re.fullmatch(r'assets/stylesheets/combined-[0-9a-f]{16}\.css',p)) and p!=OLD_CSS,'Unknown/new frozen stylesheet repair')
        require(all(not p.startswith('file:') for p in d['artifact_scope']),'File protocol is forbidden')
        return cls(d,nav,_TOKEN)
    def assert_current(self):require(digest([self.data,self.freeze_data])==self._seal,'Bound owner repair plan changed')

def validate_artifact_delta(plan,*,prior,candidate,pdf_reviews=None,navigation_proofs=None,content_proofs=None,derived_proofs=None):
    require(isinstance(plan,OwnerRepairPlan),'Arbitrary owner artifact map is forbidden');plan.assert_current()
    frozen_pins={r['served_html_path']:r['served_html_sha256'] for r in plan.freeze_data['pages'].values()}
    frozen_pins.update({r['path']:r['sha256'] for r in plan.freeze_data['presentation_asset_pins']})
    freeze_exact(candidate,frozen_pins);scope=plan.data['artifact_scope']
    require('sitemap.xml' in candidate and 'sitemap.xml.gz' in candidate,'Exact frozen XML/gzip are required')
    freeze_xml_exact(candidate['sitemap.xml'],plan.freeze_data['frozen_sitemap_entries'])
    import gzip
    require(gzip.decompress(candidate['sitemap.xml.gz'])==candidate['sitemap.xml'],'Actual gzip does not match checked XML')
    changes={p for p in set(prior)|set(candidate) if prior.get(p)!=candidate.get(p)}
    require(changes==set(scope),'Actual owner artifact delta differs from the exact Root scope')
    nav_universe=navigation_repair_universe(prior,{r['served_html_path'] for r in plan.freeze_data['pages'].values()})
    require(nav_universe<=changes,'Owner repair omitted an unfrozen actual navigation page')
    pdf_reviews=pdf_reviews or {};navigation_proofs=navigation_proofs or {};content_proofs=content_proofs or {};derived_proofs=derived_proofs or {}
    for page in sorted(nav_universe):
        row=scope[page]
        if row['class'] in {'source_content','source_metadata'}:
            # Recompute exact Source/template projections from Root-bound full
            # files and these actual HTML bytes; never trust a skip flag.
            from pathlib import Path
            from library_owner_repair_surface import revalidate_bound_content_navigation
            proof=content_proofs.get(page,{})
            require(proof.get('source_path')==row['source_path'],'Content navigation has the wrong Root source path')
            revalidate_bound_content_navigation(row['source_path'].removeprefix('docs/'),proof.get('source_navigation'),
                prior[page],candidate[page],source_note=plan.data['source_changes'][row['source_path']],template_root=Path(__file__).resolve().parents[1])
        else:validate_primary_labels(page,prior[page],candidate[page])
    for p in sorted(changes):
        r=scope[p];require(p in candidate,'Unreviewed public removal/404 is forbidden')
        require((sha(prior[p]) if p in prior else None)==r['before_sha256'],'Actual before public bytes differ')
        require(sha(candidate[p])==r.get('after_sha256'),'Exact Root after artifact bytes missing or differ')
        if r['class']=='navigation_only':require(navigation_proofs.get(p)=={'path':p,'only_two_owner_labels':True,'outside_fragments_byte_exact':True},'Actual finite navigation proof missing')
        if r['class'] in {'source_content','source_metadata','generated_hub'}:require(content_proofs.get(p,{}).get('after_sha256')==sha(candidate[p]) and content_proofs[p].get('source_path')==r['source_path'],'Actual bound source/render proof missing')
        if r['class']=='derived':require(derived_proofs.get(p,{}).get('after_sha256')==sha(candidate[p]) and derived_proofs[p].get('exact_inverse_or_actual_contexts') is True,'Actual finite derived-consumer proof missing')
        if p.endswith('.pdf'):require(p in pdf_reviews and pdf_reviews[p].get('actual_Root_visual_review_complete') is True and pdf_reviews[p].get('after_sha256')==sha(candidate[p]),'Actual exact named PDF visual/CI review missing')
    return {'kind':POLICY,'actual_changed_artifact_paths':sorted(changes),'actual_changed_artifact_count':len(changes),'ordinary_S5_cap_changed':False,'frozen_bytes_exact':True,'S5_completion_granted':False}
