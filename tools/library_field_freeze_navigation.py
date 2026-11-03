"""Finite registered45-page retention; no whole-page overwrite or source edit."""
from __future__ import annotations
import gzip,hashlib,io,json,re
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET

REGISTRY_SHA256='c346b0f6a7997449f4eccbaf662b53f7ae25ba21a57341f786dc7d673db1798c'
PAGINATION_PATH='answers/geo-basics/does-ai-search-replace-seo.md'
def digest(raw):return hashlib.sha256(raw).hexdigest()
def require(ok,message):
    if not ok:raise ValueError(message)

class PrimaryNavigation(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=False);self.text=text;self.offsets=[0];self.spans=[];self.start=None;self.depth=0
        for line in text.splitlines(keepends=True):self.offsets.append(self.offsets[-1]+len(line))
    def absolute_offset(self):
        line,column=self.getpos();return self.offsets[line-1]+column
    def handle_starttag(self,tag,attrs):
        if tag!='nav':return
        if self.depth:self.depth+=1;return
        if 'md-nav--primary' in dict(attrs).get('class','').split():
            require(not self.spans,'Repeated primary navigation boundary');self.start=self.absolute_offset();self.depth=1
    def handle_endtag(self,tag):
        if tag!='nav' or not self.depth:return
        self.depth-=1
        if not self.depth:
            start=self.absolute_offset();m=re.match(r'</nav\s*>',self.text[start:],re.I);require(m is not None,'Malformed primary navigation end')
            self.spans.append((self.start,start+m.end()));self.start=None

def primary_navigation_span(raw):
    text=raw.decode('utf-8');p=PrimaryNavigation(text);p.feed(text);p.close()
    require(len(p.spans)==1 and p.depth==0,'Exactly one complete parsed primary navigation is required')
    a,b=p.spans[0];return len(text[:a].encode()),len(text[:b].encode())

class Pagination(PrimaryNavigation):
    def __init__(self,text):super().__init__(text);self.in_head=False;self.head=[];self.links=[];self.anchor=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='head':self.in_head=True
        if tag=='link' and self.in_head and 'next' in a.get('rel','').split():
            start=self.absolute_offset();self.head.append((start,start+len(self.get_starttag_text())))
        if tag=='a' and 'next' in a.get('rel','').split():
            require(self.anchor is None,'Nested next pagination anchor');self.anchor=self.absolute_offset()
    def handle_endtag(self,tag):
        if tag=='head':self.in_head=False
        if tag=='a' and self.anchor is not None:
            start=self.absolute_offset();m=re.match(r'</a\s*>',self.text[start:],re.I);require(m is not None,'Malformed next pagination end');self.links.append((self.anchor,start+m.end()));self.anchor=None

def pagination_spans(raw):
    text=raw.decode('utf-8');p=Pagination(text);p.feed(text);p.close()
    require(len(p.head)==len(p.links)==1 and p.anchor is None,'Exact one head-next and one bottom-next fragment required')
    return {name:(len(text[:a].encode()),len(text[:b].encode())) for name,(a,b) in [('head_next',p.head[0]),('bottom_next',p.links[0])]}

def retain_primary_navigation(raw,row):
    a,b=primary_navigation_span(raw);fragment=row['primary_navigation'].encode()
    require(digest(fragment)==row['primary_navigation_sha256'],'Pinned historical primary navigation changed')
    result=raw[:a]+fragment+raw[b:];supplement=[]
    if row.get('pagination'):
        require(row.get('source_path')==PAGINATION_PATH and row.get('root_pagination_approval',{}).get('approved') is True,'Only exact Root-reviewed Q0311 pagination may be retained')
        spans=pagination_spans(result);replacements=[]
        require(set(row['pagination'])=={'head_next','bottom_next'},'Unexpected extra frozen pagination fragment')
        for name,note in row['pagination'].items():
            start,end=spans[name];new=note['fragment'].encode();require(digest(new)==note['sha256'] and row['root_pagination_approval']['fragment_sha256'][name]==digest(new),'Root-reviewed pagination fragment changed')
            replacements.append((start,end,new));supplement.append({'fragment':name,'before_sha256':digest(result[start:end]),'after_sha256':digest(new)})
        for start,end,new in sorted(replacements,reverse=True):result=result[:start]+new+result[end:]
    require(digest(result)==row['served_html_sha256'],'Frozen page differs outside the exact primary navigation; separate review required')
    return result,{'before_sha256':digest(raw),'after_sha256':digest(result),'primary_fragment_before_sha256':digest(raw[a:b]),'primary_fragment_after_sha256':digest(fragment),'additional_Root_reviewed_Q0311_fragments':supplement,'whole_page_overwrite':False,'every_other_byte_retained':True}

def sitemap_spans(raw):
    result={}
    for m in re.finditer(rb'<url\b[^>]*>.*?</url>',raw,re.S):
        e=ET.fromstring(m.group());url=next((x.text for x in e if x.tag.rsplit('}',1)[-1]=='loc'),None)
        require(url and url not in result,'Missing/repeated sitemap URL');result[url]=(m.start(),m.end(),m.group())
    return result

def retain_sitemap_entries(raw,rows):
    spans=sitemap_spans(raw);replacements=[]
    for row in rows:
        require(row['url'] in spans,'Frozen sitemap URL missing')
        a,b,old=spans[row['url']];new=row['exact_entry'].encode();require(digest(new)==row['sha256'],'Pinned frozen sitemap fragment changed');replacements.append((a,b,new))
    for a,b,new in sorted(replacements,reverse=True):raw=raw[:a]+new+raw[b:]
    for row in rows:require(sitemap_spans(raw)[row['url']][2]==row['exact_entry'].encode(),'Frozen exact sitemap entry was not retained')
    return raw

class FrozenNavigation:
    def __init__(self,docs_dir,map_path,expected_sha256):
        self.docs=Path(docs_dir).resolve();self.map_path=Path(map_path).resolve();raw=self.map_path.read_bytes()
        require(digest(raw)==expected_sha256,'Finite frozen navigation map bytes changed');d=json.loads(raw)
        require(d.get('schema_version')==1 and d.get('approved') is True and d.get('root_registry_sha256')==REGISTRY_SHA256,'Finite frozen navigation map requires explicit Root adoption')
        require(len(d['pages'])==45 and len(d['presentation_asset_pins'])==5 and len(d['frozen_sitemap_entries'])==45,'Finite frozen navigation coverage differs')
        self.data=d;self.map_sha256=expected_sha256;self.source_stamps={}
        for rel,row in d['pages'].items():
            require(rel.startswith('answers/') and rel.endswith('.md') and '..' not in Path(rel).parts,'Unexpected frozen source path')
            p=self.docs/rel;source=p.read_bytes();require(digest(source.decode('utf-8').replace('\r\n','\n').encode())==row['source_canonical_sha256'],'Frozen canonical source/date/metadata changed')
            self.source_stamps[rel]=digest(source)
            if row.get('pagination'):require(rel==PAGINATION_PATH and row['root_pagination_approval'].get('approved') is True,'Unapproved or generic pagination retention is forbidden')
    def check_sources(self):
        require(digest(self.map_path.read_bytes())==self.map_sha256,'Frozen navigation map changed during build')
        require(all(digest((self.docs/p).read_bytes())==h for p,h in self.source_stamps.items()),'Frozen source bytes changed during build')
    def post_build(self,site_dir):
        self.check_sources();site=Path(site_dir).resolve();report={'pages':{},'production_exact_bytes':True,'activation_authorized':False}
        require(site!=self.docs and not site.is_relative_to(self.docs) and not self.docs.is_relative_to(site),'Frozen retention output must be the separate built site')
        require((site/'sitemap.xml.gz').is_file(),'Built compressed sitemap missing before retention')
        # Compute and validate every output before the first output write.
        pending={}
        for rel,row in self.data['pages'].items():
            path=row['served_html_path'];raw=(site/path).read_bytes();new,receipt=retain_primary_navigation(raw,row);pending[path]=new;report['pages'][rel]=receipt
        for row in self.data['presentation_asset_pins']:require(digest((site/row['path']).read_bytes())==row['sha256'],'Frozen shared presentation asset differs')
        xml=(site/'sitemap.xml').read_bytes();new_xml=retain_sitemap_entries(xml,self.data['frozen_sitemap_entries']);pending['sitemap.xml']=new_xml
        stream=io.BytesIO()
        with gzip.GzipFile(fileobj=stream,filename='',mode='wb',compresslevel=9,mtime=0) as gz:gz.write(new_xml)
        pending['sitemap.xml.gz']=stream.getvalue();self.check_sources()
        for path,new in pending.items():
            target=site/path
            if target.read_bytes()!=new:target.write_bytes(new)
        self.verify_site(site);report['sitemap_before_sha256']=digest(xml);report['sitemap_after_sha256']=digest(new_xml)
        return report
    def verify_site(self,site_dir):
        self.check_sources();site=Path(site_dir)
        for row in self.data['pages'].values():require(digest((site/row['served_html_path']).read_bytes())==row['served_html_sha256'],'Final frozen HTML is not byte-exact')
        for row in self.data['presentation_asset_pins']:require(digest((site/row['path']).read_bytes())==row['sha256'],'Final frozen asset is not byte-exact')
        xml=(site/'sitemap.xml').read_bytes();spans=sitemap_spans(xml)
        for row in self.data['frozen_sitemap_entries']:require(row['url'] in spans and spans[row['url']][2]==row['exact_entry'].encode(),'Final frozen sitemap fragment changed')
        require(gzip.decompress((site/'sitemap.xml.gz').read_bytes())==xml,'Final gzip differs from frozen-checked XML')
