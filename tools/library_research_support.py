"""Library-owned finite Research support. No output changes while absent.

The two existing Dataset entries are the only allowed no-lastmod rows. The
shared caller must bind the Library-reviewed module/policy before executing
Research's check_sources; this module never invokes its postbuild writer.
"""
from pathlib import Path
import copy,gzip,hashlib,io,json,re,runpy
import xml.etree.ElementTree as ET

POLICY='LIBRARY_FINITE_RESEARCH_SUPPORT_V2'
MODULE='docs/research/data/research_release_gate.py'
TEXT_POLICY='docs/research/data/research-release-policy.json'
PLAN='tools/library-research-support.json'
PIN='tools/library-research-support.sha256'
URLS=('https://docs.broadcastwell.com/assets/research/change-desk/2026-10-26/connectwise-statements-ai/',
      'https://docs.broadcastwell.com/assets/research/change-desk/2026-10-26/software-transaction-state/')
_TOKEN=object()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def qsha(v):return sha(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
def entry(url):return ('  <url>\n    <loc>'+url+'</loc>\n  </url>\n').encode()
def dataset_path(url):return url.removeprefix('https://docs.broadcastwell.com/')+'index.html'

def _file(root,rel):
    require(not Path(rel).is_absolute() and '..' not in Path(rel).parts,'Research support path escape')
    p=Path(root).absolute()
    require('..' not in p.parts,'Research support root traversal')
    require(not any(a.is_symlink() or getattr(a,'is_junction',lambda:False)() for a in [p,*p.parents]),
        'Research support root/parent symlink or junction')
    for part in Path(rel).parts:
        p=p/part;require(not p.is_symlink() and not getattr(p,'is_junction',lambda:False)(),'Research support input symlink')
    require(p.is_file(),'Research support input is missing: '+rel)
    return p

class ResearchSupport:
    def __init__(self,root,plan,token):
        require(token is _TOKEN,'Research support needs an actual Library binding')
        self.root=Path(root).resolve();self.plan=copy.deepcopy(plan);self._seal=(str(self.root),qsha(plan))
        self._plan_raw=_file(self.root,PLAN).read_bytes();self._pin_raw=_file(self.root,PIN).read_bytes()
    def assert_current(self):
        require(self._seal==(str(self.root),qsha(self.plan)),'Research support binding mutated')
        require(_file(self.root,PLAN).read_bytes()==self._plan_raw and _file(self.root,PIN).read_bytes()==self._pin_raw,
            'Committed Library Research support plan/pin changed after binding')
        require(sha(_file(self.root,MODULE).read_bytes())==self.plan['module_sha256']
            and sha(_file(self.root,TEXT_POLICY).read_bytes())==self.plan['policy_sha256'],
            'Research module/policy bytes changed after Library review')
        for url,digest in self.plan['dataset_HTML_sha256'].items():
            require(sha(_file(self.root,'docs/'+dataset_path(url)).read_bytes())==digest,
                'Existing Dataset source bytes changed')

def optional_support(root):
    root=Path(root);present=[(root/p).exists() for p in [MODULE,TEXT_POLICY]]
    if not any(present):return None
    require(all(present),'Partial Research module/policy presence is forbidden')
    raw=_file(root,PLAN).read_bytes();pin=_file(root,PIN).read_text(encoding='ascii').strip()
    require(re.fullmatch('[0-9a-f]{64}',pin) and sha(raw)==pin,'Library Research support plan is missing/changed')
    d=json.loads(raw)
    base={'schema_version','policy','approved','review_kind','Root_actual_module_and_policy_read',
        'module_sha256','policy_sha256','dataset_HTML_sha256'}
    require(set(d) in [base,base|{'release_inputs','staged_file_sha256'}],'Research support plan schema differs')
    require(d['schema_version']==1 and d['policy']==POLICY and d['approved'] is True
        and d['review_kind']=='library-root-reviewed-finite-research-support'
        and d['Root_actual_module_and_policy_read'] is True,'Actual Library module/policy review is missing')
    require(set(d['dataset_HTML_sha256'])==set(URLS),'Only exact two existing Dataset URLs supported')
    require(all(re.fullmatch('[0-9a-f]{64}',str(v)) for v in [d['module_sha256'],d['policy_sha256'],*d['dataset_HTML_sha256'].values()]),'Research support pin malformed')
    if 'release_inputs' in d:
        ref=d['release_inputs']
        require(isinstance(ref,dict) and set(ref)=={'path','sha256'}
            and ref['path']=='.library-research-work/inputs.json'
            and re.fullmatch('[0-9a-f]{64}',str(ref['sha256'])),
            'Research release input must be exact ignored Library staging namespace')
        files=d['staged_file_sha256']
        require(isinstance(files,dict) and files.get(ref['path'])==ref['sha256'] and files
            and all(isinstance(p,str) and p.startswith('.library-research-work/')
                and '..' not in Path(p).parts and '\\' not in p and ':' not in p
                and p!='.library-research-work/candidate.gitLF.zip'
                and re.fullmatch('[0-9a-f]{64}',str(v)) for p,v in files.items()),
            'Research staged file namespace/pins differ')
    result=ResearchSupport(root,d,_TOKEN);result.assert_current();return result

def check_optional_sources(root):
    support=optional_support(root)
    if support is None:return []
    support.assert_current()
    namespace=runpy.run_path(str(_file(support.root,MODULE)),run_name='_Library_reviewed_Research_source_gate')
    checker=namespace.get('check_sources')
    require(callable(checker),'Reviewed Research source checker is absent')
    errors=checker(support.root)
    require(isinstance(errors,list) and all(isinstance(e,str) for e in errors),'Research checker returned an uncontrolled result')
    support.assert_current();return errors

def allow_no_lastmod(support,url,fragment):
    require(isinstance(support,ResearchSupport),'No-lastmod needs the exact Library Research binding')
    support.assert_current()
    require(url in URLS and fragment==entry(url).strip(),
        'Unknown or nonexact no-lastmod Dataset element')
    return True

def transform_datasets(xml,compressed,*,support,static_dataset_files):
    if support is None:return xml,compressed
    require(isinstance(support,ResearchSupport),'Arbitrary Research support flag forbidden')
    support.assert_current();require(gzip.decompress(compressed)==xml,'XML/gzip disagree')
    require(set(static_dataset_files)==set(URLS),'Exact two Dataset HTML byte proofs required')
    for url,raw in static_dataset_files.items():
        require(sha(raw)==support.plan['dataset_HTML_sha256'][url],'Actual Dataset output bytes differ')
    require(b'<!DOCTYPE' not in xml and b'<!ENTITY' not in xml,'Unsafe sitemap declaration')
    root=ET.fromstring(xml);require(root.tag=='{http://www.sitemaps.org/schemas/sitemap/0.9}urlset','Wrong sitemap namespace')
    old=[r.findtext('{*}loc') for r in root];require(len(old)==len(set(old)),'Duplicate sitemap URL')
    result=xml
    for url in URLS:
        if url in old:
            require(result.count(entry(url))==1,'Existing Dataset row differs')
        else:
            require(result.count(b'</urlset>')==1,'Unexpected sitemap close')
            result=result.replace(b'</urlset>',entry(url)+b'</urlset>',1)
    validate_dataset_inverse(xml,result,support=support)
    if result==xml:return xml,compressed
    b=io.BytesIO()
    with gzip.GzipFile(fileobj=b,filename='',mode='wb',compresslevel=9,mtime=0) as z:z.write(result)
    return result,b.getvalue()

def validate_dataset_inverse(before,after,*,support):
    require(isinstance(support,ResearchSupport),'Dataset inverse lacks actual binding');support.assert_current()
    old=[r.findtext('{*}loc') for r in ET.fromstring(before)]
    new=[r.findtext('{*}loc') for r in ET.fromstring(after)]
    require(len(new)==len(set(new)) and set(new)==set(old)|set(URLS),'Dataset URL scope differs')
    remaining=after
    for url in URLS:
        require(after.count(entry(url))==1,'Dataset element is not exact')
        if url not in old:remaining=remaining.replace(entry(url),b'',1)
    require(remaining==before,'Sitemap bytes changed outside the exact two insertions')
    return True
