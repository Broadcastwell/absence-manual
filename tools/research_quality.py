"""Additional source, structure and cross-site similarity checks for research pages.

Existing manual and answer-library checks remain independent and unchanged.
"""
from pathlib import Path
import json, re, html
from html.parser import HTMLParser
import yaml
try:
    from tools.library_quality import words, sequences
except ModuleNotFoundError:
    from library_quality import words, sequences

FLOORS={'hub':(800,1400),'insight':(1400,2500),'source':(1400,2500),
        'study':(1400,2500),'playbook':(1200,2200),'glossary':(600,1100)}
ISO=re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|\+\d{2}:\d{2})$')

class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__();self.parts=[];self.hidden=0
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style','pre'):self.hidden+=1
    def handle_endtag(self,tag):
        if tag in ('script','style','pre'):self.hidden=max(0,self.hidden-1)
    def handle_data(self,data):
        if not self.hidden:self.parts.append(data)

def text_content(value):
    parser=VisibleText();parser.feed(value);return ' '.join(parser.parts)

def split(text):
    m=re.match(r'\A---\n(.*?)\n---\n(.*)',text,re.S)
    return (yaml.safe_load(m[1]) or {},m[2]) if m else ({},text)

def comparable(body):
    # Fixed reference, citation, attribution and next-step blocks carry no original argument.
    # The same exclusions apply to every candidate and every comparison page.
    body=re.split(r'(?m)^## (?:Sources|Cite this page|Continue)\s*$',body)[0]
    body=re.sub(r'(?s)```.*?```',' ',body)
    body=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',body)
    body=re.sub(r'<[^>]+>',' ',body)
    return body

def check_research(root):
    root=Path(root); docs=root/'docs'; errors=[]; pages={}; ids=[]
    for p in sorted(docs.rglob('*.md')):
        meta,body=split(p.read_text(encoding='utf-8-sig'))
        rel=p.relative_to(docs).as_posix()
        if meta.get('page_class')=='research':pages[rel]=(meta,body)
    if not pages:return errors
    other={}
    for p in docs.rglob('*.md'):
        rel=p.relative_to(docs).as_posix();meta,body=split(p.read_text(encoding='utf-8-sig'))
        other[rel]=sequences(words(comparable(body)),6)
    for rel,(meta,body) in pages.items():
        def need(ok,msg):
            if not ok:errors.append(rel+': '+msg)
        ids.append(meta.get('research_id'))
        for key in ('title','description','lead','canonical','research_group'):
            need(bool(meta.get(key)),key+' missing')
        for key in ('published','updated','next_review'):
            need(bool(ISO.fullmatch(str(meta.get(key,'')))),key+' must have full timestamp and timezone')
        need(meta.get('sources_verified') is True,'sources_verified must be true')
        expected='https://docs.broadcastwell.com/'+rel.removesuffix('index.md')
        need(meta.get('canonical')==expected,'canonical differs from permanent path')
        need(meta.get('published')==meta.get('date_published') and meta.get('updated')==meta.get('date_modified'),'legacy and research dates differ')
        group=meta.get('research_group'); visible=text_content(__import__('markdown').markdown(body,extensions=['tables']))
        wc=len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b",visible))
        if group in FLOORS:
            low,high=FLOORS[group];need(low<=wc<=high,f'visible article words {wc}, expected {low} to {high}')
        h1=re.findall(r'(?m)^# (.+)$',body);need(len(h1)==1,'one H1 required')
        heading=re.search(r'(?m)^# .+$',body)
        after=body[heading.end():].lstrip() if heading else ''
        quote=re.match(r'\*\*(.+?)\*\*',after)
        need(bool(quote) and len(quote[1].split())<=30,'bold opening quotation sentence must have at most 30 words')
        for block in ('What our own data shows','Sources','Cite this page','Continue'):
            need('## '+block in body,block+' missing')
        need('Prepared by the Broadcastwell research team. Lead: '+meta['lead'] in body,'lead byline missing')
        need('```bibtex' in body and meta['canonical'] in body,'APA and BibTeX citation missing')
        closing=body.split('## Continue')[-1];links=re.findall(r'\[[^\]]+\]\(([^)]+)\)',closing)
        need(len(links)==2 and links[0]=='https://audit.broadcastwell.com/' and links[1].startswith('https://docs.broadcastwell.com/'),'closing block needs only free check and relevant manual/library links')
        need(not re.search(r'\b(?:delve|tapestry|game.changer|unlock)\b',comparable(body),re.I),'prohibited prose wording')
        need(not re.search(r'\bour (?:workflow|pipeline)\b|\b(?:call counts|api keys|top.up)\b',comparable(body),re.I),'private production terminology requires removal')
        if group in ('insight','source','study','playbook'):need(meta.get('schema_type')=='TechArticle','TechArticle required')
        html_path=root/'site'/rel.replace('.md','.html')
        if html_path.exists():
            built=html_path.read_text(encoding='utf-8')
            schema=[]
            for item in re.findall(r'<script type="application/ld\+json">(.*?)</script>',built,re.S):
                try:schema.append(json.loads(item))
                except ValueError:need(False,'invalid JSON-LD')
            types={x.get('@type') for x in schema if isinstance(x,dict)}
            need('BreadcrumbList' in types and meta['schema_type'] in types,'article/breadcrumb schema missing')
            if meta.get('defined_term'):need('DefinedTerm' in types,'DefinedTerm schema missing')
            if meta.get('research_id') in (43,44,45,46):need('Dataset' in types,'Dataset schema missing')
            article=re.search(r'<article\b[^>]*>(.*?)</article>',built,re.S)
            if article:need('Answer Repair is $490' not in text_content(article[1]),'research has commercial closing block')
        own=other[rel]
        for target,six in other.items():
            if target==rel or not own or not six:continue
            shared=len(own & six);base=min(len(own),len(six))
            if shared*5>base:errors.append(f'{rel}: six-word similarity to {target} is {shared}/{base}, above 20%')
    if len(ids)!=len(set(ids)):errors.append('research IDs must be unique')
    return errors

if __name__=='__main__':
    import sys
    failures=check_research(Path(__file__).resolve().parents[1])
    print('\n'.join(failures) if failures else 'Research checks passed.')
    sys.exit(bool(failures))
