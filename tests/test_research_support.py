"""Synthetic future Research fixtures; no actual307/Owner/Research execution."""
from pathlib import Path
import ast,copy,gzip,hashlib,io,json,os,re,stat,sys,tempfile,unittest,zipfile
from unittest.mock import patch
H=Path(__file__).resolve().parents[1];T=H/'tools'
FIXTURES=H/'tests/fixtures/owner_required28'
OWNER11_FIXTURES=H/'tests/fixtures/research_owner11'
sys.path.insert(0,str(T))
from datetime import datetime,timezone
import library_research_owner_preservation as owner11
import library_research_support as support
import library_research_release as release
from library_research_source_archive import archive_files,bind_source_archives,CONTROLS
from library_research_consumers import generate_research_sitemaps,validate_research_sitemaps,validate_research_search,research_url
from library_research_render import validate_research_contexts
from library_publication_consumers import _sitemap_rows
import library_related_chapter_links as finite
from library_build_dispatch import from_environment

j=lambda v:json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def zipped(files):
 b=io.BytesIO()
 with zipfile.ZipFile(b,'w') as z:
  for p,raw in sorted(files.items()):z.writestr(p,raw)
 return b.getvalue()
def write(root,files):
 for p,raw in files.items():
  target=root/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)


class Fixture:
 def __init__(self,root,protected):
  self.root=root;self.catalog=release.paths();self.before={};self.after={};self.prior_public=dict(protected)
  self.records={};self.contexts={}
  self.event=datetime.now(timezone.utc).isoformat();self.day=self.event[:10]
  self.owner_catalog=owner11.catalog()
  data=(OWNER11_FIXTURES/'fixture_index.json').read_bytes()
  assert support.sha(data)=='bfe7fa171329549a126dcbc95992c20718583f3ae67f108316806b55a40286bd'
  self.owner_index=json.loads(data)['sources'];self.owner_lineage_files={};self.owner_refs={};self.owner_dates={}
  for p in self.catalog['source_paths']:
   if p.endswith('.md'):
    meta={'title':'Synthetic Research fixture','headline':'Synthetic Research fixture','description':'Synthetic fixture only.',
      'page_class':'research','schema_type':'Article','date_published':'2026-11-01T12:00:00+00:00','date_modified':'2026-11-02T12:00:00+00:00'}
    body='# Synthetic Research fixture\n\nExact fixture evidence.\n\n## What our own data shows\n\nFour of ten fixture records.\n\n## Sources\n\n[Fixture source](https://example.org/source).\n'
    import yaml
    def full(m):return ('---\n'+yaml.safe_dump(m,sort_keys=False)+'---\n\n'+body).encode()
    path=p.removeprefix('docs/')
    if path in self.owner_index:
     row=self.owner_index[path];spec=self.owner_catalog['sources'][path]
     value=(OWNER11_FIXTURES/row['expected_before_file']['path']).read_bytes()
     assert support.sha(value)==row['expected_before_file']['sha256']
     self.before[p]=value;meta,body=finite.source_body(value.decode())
     edits=owner11._expected_presentation(spec,self.event);self.owner_dates[path]=edits
     for edit in edits:body=body.replace(edit['old'],edit['new'],1)
     for key in ['updated','date_modified']:meta[key]=self.event
     self.after[p]=full(meta)
     refs={'source_id':spec['id']}
     for key,masterkey in [('scoped_Source','current_scoped_Source_receipt'),('Source_evidence','current_fact_or_precision_Source_evidence'),('repair_ledger','original_Root_repair_change_ledger')]:
      ref=row[masterkey];value=(OWNER11_FIXTURES/ref['path']).read_bytes();assert support.sha(value)==ref['sha256']
      rel='.library-research-work/source-lineage/'+spec['id']+'/'+key+'.json'
      self.owner_lineage_files[rel]=value;refs[key]={'path':rel,'sha256':ref['sha256']}
     self.owner_refs[path]=refs
    else:
     self.before[p]=full(meta);meta['date_modified']=self.event;self.after[p]=full(meta)
    self.records[path]=dict(meta=copy.deepcopy(meta),body=body,effective_full_source=self.after[p].decode())
    self.prior_public[p.removeprefix('docs/').removesuffix('index.md')+'index.html']=b'old synthetic HTML'
   else:self.before[p]=b'old fixture';self.after[p]=b'new fixture'
  self.after[support.MODULE]=b'def check_sources(root):\n    return []\n'
  self.after[support.TEXT_POLICY]=b'{"synthetic_fixture":true}'
  for p,raw in protected.items():self.before['docs/'+p]=raw;self.after['docs/'+p]=raw
  for url in support.URLS:
   p='docs/'+support.dataset_path(url);self.before[p]=self.after[p]=b'<html>Synthetic existing Dataset fixture</html>'
  self.before['CLAUDE.md']=self.after['CLAUDE.md']=b'Unrelated source must stay exact.'
  self.plan_support={'schema_version':1,'policy':support.POLICY,'approved':True,
   'review_kind':'library-root-reviewed-finite-research-support','Root_actual_module_and_policy_read':True,
   'module_sha256':support.sha(self.after[support.MODULE]),'policy_sha256':support.sha(self.after[support.TEXT_POLICY]),
   'dataset_HTML_sha256':{u:support.sha(self.after['docs/'+support.dataset_path(u)]) for u in support.URLS}}
  raw=j(self.plan_support);self.after[support.PLAN]=raw;self.after[support.PIN]=support.sha(raw).encode()
  self.prior_zip=zipped(self.before);self.candidate_zip=zipped(self.after);write(root,self.after)
  self.support=support.optional_support(root)
  pages={f'answers/fixture/p{i}.md':{} for i in range(307)}
  ready={p:{'status':'DEFERRED_FIELD_TEST','passed':None} if i<45 else {'status':'PASS' if i<89 else 'FAIL','passed':i<89} for i,p in enumerate(pages)}
  self.quality={'analysis_completed':True,'baseline_exceptions':0,'passed':False,'global_fatal_errors':[],
   'page_readiness':ready,'comparison_scopes':{n:{'all_pairs_compared':True,'pair_count':46971,'violations':[{'fixture':'unchanged violation'}]} for n in ['literal','runtime']}}
  self.binding={'commit_sha':'a'*40,'deployment_id':'FIXTURE','artifact_sha256':'b'*64,'served_receipt_sha256':'c'*64}
  self.payload={'pages':pages};self.state={'production_binding':self.binding,'current_quality_snapshot':self.quality,
   'merged_sources':{f'answers/retired/p{i}.md':{'fixture':i} for i in range(19)},
   'raw_source_pins':{f'answers/raw/p{i}.md':'d'*64 for i in range(326)}}
  self.producer={'approved':True,'review_kind':'prior-production-effective-payload','actual_served_readback':True,
   'source_render_equality_passed':True,'hub_source_render_equality_passed':True,'production_binding':self.binding,
   'mechanical_proof':{'exact_Git_archive':{'sha256':support.sha(self.prior_zip)}}}
  self.plan={'schema_version':1,'policy':release.POLICY,'approved':True,
   'review_kind':'library-root-reviewed-finite-research-release','Root_actual_source_review_complete':True,
   'production_receipt_sha256':support.sha(j(self.producer)),'production_binding':self.binding,
   'candidate_source_inventory_sha256':support.qsha({p:support.sha(r) for p,r in sorted(self.after.items()) if p not in CONTROLS}),
   'current_payload_object_sha256':support.qsha(self.payload),'inherited_dispositions_sha256':support.qsha(self.state['merged_sources']),
   'source_files':{p:{'before_sha256':support.sha(self.before[p]),'after_sha256':support.sha(self.after[p])} for p in self.catalog['source_paths']},
   'Library_owned_activation_before_pins':{p:None for p in CONTROLS},
   'full_source_reviews':{'docs/'+p:{'approved':True,'current_full_file_actually_read':True,'review_kind':'reviewed-current-research-source',
    'scope':'Research-release-current-source-reading','path':'docs/'+p,'reviewer':'Synthetic fixture reader',
    'actual_read_scope':'Synthetic fixture bytes only; no project approval.',
    'before_canonical_source_sha256':support.sha(self.before['docs/'+p]),
    'after_canonical_source_sha256':support.sha(r['effective_full_source'].encode()),'after_body_sha256':support.sha(r['body'].encode()),'after_metadata_sha256':support.qsha(r['meta'])} for p,r in self.records.items()},
   'Owner11_required_Source_manifest_sha256':self.owner_catalog['Source_required_manifest_sha256'],
   'Owner11_preserved_claim_spans':{p:[{k:r[k] for k in ['id','text','sha256']} for r in self.owner_catalog['sources'][p]['required_spans']] for p in self.catalog['Owner11_rebased_claim_sources']},
   'Owner11_Source_lineage':self.owner_refs,'Owner11_actual_Research_adoption_utc':self.event,
   'Owner11_presentation_date_edits':self.owner_dates,
   'artifact_changes':{},'artifact_review':{'approved':False},'notice_PDF_review':{'approved':False}}
  self.refresh_synthetic_evidence()
 def refresh_synthetic_evidence(self):
  files=dict(self.owner_lineage_files)
  for i,(path,review) in enumerate(self.plan['full_source_reviews'].items()):
   body={k:v for k,v in review.items() if k!='evidence_receipt'};raw=j(body)
   name=f'.library-research-work/readings/{i:02}.json';files[name]=raw
   review['evidence_receipt']={'path':name,'sha256':support.sha(raw)}
  self.plan['source_read_evidence_map_sha256']=support.qsha(self.plan['full_source_reviews'])
  data=j(self.plan);files['.library-research-work/inputs.json']=data
  d={k:v for k,v in self.plan_support.items() if k not in {'release_inputs','staged_file_sha256'}}
  d['release_inputs']={'path':'.library-research-work/inputs.json','sha256':support.sha(data)}
  d['staged_file_sha256']={p:support.sha(raw) for p,raw in files.items()}
  self.plan_support=d;raw=j(d);self.after[support.PLAN]=raw;self.after[support.PIN]=support.sha(raw).encode()
  write(self.root,{**files,support.PLAN:raw,support.PIN:self.after[support.PIN]})
  self.candidate_zip=zipped(self.after);self.support=support.optional_support(self.root)
 def bind(self):
  return release.bind_release(self.root,j(self.plan),support.sha(j(self.plan)),support=self.support,actual_prior_binding=self.binding,
   prior_source_archive_raw=self.prior_zip,candidate_source_archive_raw=self.candidate_zip,
   prior_public_files=self.prior_public,current_payload=self.payload,prior_state=self.state,producer_raw=j(self.producer))
 def sitemap(self):
  rows=['  <url>\n    <loc>'+research_url('docs/'+p)+'</loc>\n    <lastmod>2026-11-02</lastmod>\n  </url>\n' for p in self.records]
  rows+=['  <url>\n    <loc>https://docs.broadcastwell.com/answers/frozen/example/</loc>\n    <lastmod>2026-10-29</lastmod>\n  </url>\n']
  return ('<?xml version="1.0"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(rows)+'</urlset>').encode()
 def rendered_contexts(self):
  # Execute only the actual existing pure content-hook function, not its
  # build/session module. No mock or fabricated renderer receipt is used.
  original=T/'hooks.py'
  tree=ast.parse(original.read_text(encoding='utf-8'))
  function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='on_page_content')
  namespace={'re':re,'PERMALINK':re.compile(r'<a class="headerlink"(?![^>]*aria-hidden)'),
   'REPLACEMENT':'<a class="headerlink" aria-hidden="true" tabindex="-1"'}
  exec(compile(ast.Module(body=[function],type_ignores=[]),str(original),'exec'),namespace)
  from types import SimpleNamespace
  from html import escape
  import markdown
  from mkdocs.structure.toc import get_toc
  result={}
  for path,r in self.records.items():
   md=markdown.Markdown(extensions=['toc','tables','attr_list','md_in_html','def_list','footnotes','admonition'],extension_configs={'toc':{'permalink':True,'toc_depth':3}})
   actual=namespace['on_page_content'](md.convert(r['body']),SimpleNamespace(meta=r['meta']))
   meta=r['meta'];url=research_url('docs/'+path)
   head='<title>'+escape(meta['title'])+' | The Absence Manual</title><link rel="canonical" href="'+url+'">'
   for key,val in {'description':meta['description'],'og:title':meta['title'],'og:description':meta['description'],'og:url':url,'twitter:title':meta['title'],'twitter:description':meta['description']}.items():
    head+='<meta name="'+key+'" content="'+escape(val,quote=True)+'">'
   head+='<script type="application/ld+json">'+json.dumps({'@type':'Article','headline':meta.get('headline',meta['title']),'name':meta.get('headline',meta['title']),
    'description':meta['description'],'datePublished':meta['date_published'],'dateModified':meta['date_modified'],'url':url})+'</script>'
   footer='<hr><p class="manual-footer-version">Broadcastwell research. Sources and dates are stated on each page. Prose and derived tables CC BY 4.0, site code MIT. External sources retain their own licenses. Not peer reviewed. <a href="/research/standard/">Evidence standard</a>.</p>'
   result[path]={'markdown':r['body'],'meta':meta,'html':actual,'toc':get_toc(md.toc_tokens),
    'rendered_html':('<html><head>'+head+'</head><body><article>'+actual+footer+'</article></body></html>').encode()}
  return result


class ResearchSupportTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cat=release.paths()
  cls.protected={p:(H/'docs'/p).read_bytes() for p in cat['immutable_science_and_registered_downloads']}
  assert all(support.sha(raw)==cat['immutable_science_and_registered_downloads'][p] for p,raw in cls.protected.items())
 def setUp(self):self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
 def tearDown(self):self.temp.cleanup()
 def fixture(self):return Fixture(self.root,self.protected)
 def test_absent_module_is_no_output_change(self):
  self.assertIsNone(support.optional_support(self.root));self.assertEqual([],support.check_optional_sources(self.root))
  xml=b'<urlset/>';gz=gzip.compress(xml);self.assertEqual((xml,gz),support.transform_datasets(xml,gz,support=None,static_dataset_files={}))
 def test_partial_module_missing_plan_unapproved_or_tampered_plan_reject(self):
  write(self.root,{support.MODULE:b'def check_sources(root):return []'})
  with self.assertRaises(ValueError):support.optional_support(self.root)
  f=self.fixture()
  for change in ['unapproved','hash','module']:
   with self.subTest(change=change):
    files=copy.deepcopy(f.after)
    if change=='module':files[support.MODULE]+=b'# changed'
    else:
     d=copy.deepcopy(f.plan_support)
     if change=='unapproved':d['approved']=False
     files[support.PLAN]=j(d)+(b' ' if change=='hash' else b'')
     if change=='unapproved':files[support.PIN]=support.sha(files[support.PLAN]).encode()
    write(self.root,files)
    with self.assertRaises(ValueError):support.optional_support(self.root)
    write(self.root,f.after)
 def test_exact60_source_reviews_archive_and_preserved_science_bind(self):
  f=self.fixture();p=f.bind();self.assertEqual(53,len(p.research_records));self.assertEqual({'sources'},set(p.proofs))
  self.assertEqual([],support.check_optional_sources(self.root))
 def test_source_archive_wrong_prior_omission_unrelated_change_and_working_bytes_reject(self):
  f=self.fixture()
  for mode in ['prior','omit','unrelated','working']:
   with self.subTest(mode=mode):
    old=f.prior_zip;new=f.candidate_zip
    if mode=='prior':f.prior_zip=zipped({'forged':b'not actual prior'})
    elif mode in ['omit','unrelated']:
     files=copy.deepcopy(f.after)
     if mode=='omit':files.pop('CLAUDE.md')
     else:files['CLAUDE.md']+=b' bad'
     f.candidate_zip=zipped(files)
    else:(self.root/'CLAUDE.md').write_bytes(b'working tamper')
    with self.assertRaises(ValueError):f.bind()
    f.prior_zip=old;f.candidate_zip=new;write(self.root,f.after)
 def test_coherent_out_of_scope_source_change_rejects_even_with_rebound_inventory(self):
  f=self.fixture();f.after['CLAUDE.md']+=b'bad';write(self.root,f.after);f.candidate_zip=zipped(f.after)
  f.plan['candidate_source_inventory_sha256']=support.qsha({p:support.sha(r) for p,r in sorted(f.after.items()) if p not in CONTROLS})
  f.refresh_synthetic_evidence()
  with self.assertRaises(ValueError):f.bind()
 def test_missing_wrong_review_or_Owner_span_or_science_rejects(self):
  f=self.fixture();original=copy.deepcopy(f.plan)
  for mode in ['missing','wrongbody','unread','Owner','science']:
   with self.subTest(mode=mode):
    f.plan=copy.deepcopy(original);key=next(iter(f.plan['full_source_reviews']))
    if mode=='missing':f.plan['full_source_reviews'].pop(key)
    elif mode=='wrongbody':f.plan['full_source_reviews'][key]['after_body_sha256']='0'*64
    elif mode=='unread':f.plan['full_source_reviews'][key]['current_full_file_actually_read']=False
    elif mode=='Owner':next(iter(f.plan['Owner11_preserved_claim_spans'].values()))[0]['text']='Missing scientific qualification'
    else:f.prior_public[next(iter(self.protected))]=b'bad'
    f.refresh_synthetic_evidence()
    with self.assertRaises(ValueError):f.bind()
    f.prior_public=dict(self.protected)
 def test_actual_read_evidence_missing_fake_unapproved_wrong_reviewer_scope_or_before_reject(self):
  f=self.fixture();original=copy.deepcopy(f.plan)
  for mode in ['missing','fakebytes','unapproved','reviewer','scope','before']:
   f.plan=copy.deepcopy(original);key=next(iter(f.plan['full_source_reviews']));row=f.plan['full_source_reviews'][key]
   if mode=='unapproved':row['approved']=False
   elif mode=='reviewer':row['reviewer']=''
   elif mode=='scope':row['scope']='ordinary-Source-kind-waiver'
   elif mode=='before':row['before_canonical_source_sha256']='0'*64
   f.refresh_synthetic_evidence();path=self.root/row['evidence_receipt']['path']
   if mode=='missing':path.unlink()
   elif mode=='fakebytes':path.write_bytes(b'{"approved":true,"forged":true}')
   with self.subTest(mode=mode),self.assertRaises((ValueError,OSError)):f.bind()
 def test_both_XML_generator_and_independent_expected_enforce_only53dates_twoDatasets(self):
  f=self.fixture();p=f.bind();before=f.sitemap();datasets={u:f.after['docs/'+support.dataset_path(u)] for u in support.URLS}
  after,gz=generate_research_sitemaps(before,gzip.compress(before),permit=p,static_dataset_files=datasets)
  self.assertTrue(validate_research_sitemaps(before,after,gz,permit=p));self.assertEqual(53,after.count(('<lastmod>'+f.day+'</lastmod>').encode()))
  self.assertIn(b'<lastmod>2026-10-29</lastmod>',after)
  with self.assertRaises(ValueError):_sitemap_rows(after)
  self.assertEqual(56,len(_sitemap_rows(after,p.support)))
  for mode in ['frozen','unknown','wrongdate','datasetdate','missing','gzip']:
   bad=after
   if mode=='frozen':bad=bad.replace(b'2026-10-29',f.day.encode())
   elif mode=='unknown':bad=bad.replace(b'</urlset>',b'<url><loc>https://docs.broadcastwell.com/unlisted/</loc><lastmod>2026-11-03</lastmod></url></urlset>')
   elif mode=='wrongdate':bad=bad.replace(f.day.encode(),b'2026-11-02',1)
   elif mode=='datasetdate':bad=bad.replace(support.entry(support.URLS[0]),support.entry(support.URLS[0]).replace(b'</url>',b'<lastmod>2026-11-03</lastmod></url>'))
   elif mode=='missing':bad=bad.replace(support.entry(support.URLS[0]),b'')
   with self.subTest(mode=mode),self.assertRaises((ValueError,OSError)):validate_research_sitemaps(before,bad,b'bad' if mode=='gzip' else gzip.compress(bad),permit=p)
 def test_no_lastmod_unsupported_URL_or_arbitrary_flag_reject(self):
  f=self.fixture()
  for url in ['https://docs.broadcastwell.com/answers/frozen/example/','https://docs.broadcastwell.com/research/unlisted/']:
   xml=b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+support.entry(url)+b'</urlset>'
   with self.subTest(url=url),self.assertRaises(ValueError):_sitemap_rows(xml,f.support)
  with self.assertRaises(ValueError):support.allow_no_lastmod(True,support.URLS[0],support.entry(support.URLS[0]).strip())
 def test_support_or_bound_records_mutation_reject(self):
  f=self.fixture();p=f.bind();next(iter(p.research_records.values()))['body']+=' tamper'
  with self.assertRaises(ValueError):p.check()
  (self.root/support.PIN).write_bytes(b'0'*64)
  with self.assertRaises(ValueError):f.support.assert_current()
 def test_quality_each_scope_priorPASS_and_global_errors_remain_strict(self):
  f=self.fixture();self.assertTrue(release.validate_quality_identity(f.quality,copy.deepcopy(f.quality)))
  for mode in ['literal','runtime','PASS','global']:
   after=copy.deepcopy(f.quality)
   if mode in ['literal','runtime']:after['comparison_scopes'][mode]['violations'].append({'new':'violation'})
   elif mode=='PASS':next(r for r in after['page_readiness'].values() if r['status']=='PASS')['status']='FAIL'
   else:after['global_fatal_errors'].append('new error')
   with self.subTest(mode=mode),self.assertRaises(ValueError):release.validate_quality_identity(f.quality,after)
 def test_missing_proof_closure_or_pending_ArtifactPDF_review_cannot_finish(self):
  f=self.fixture();p=f.bind()
  with self.assertRaises(ValueError):p.finish()
  for k in ['render','sitemap','search','library_consumers','quality','freeze','stubs','PDF','whole_public_delta']:
   p._record_proof(k,{'fixture':True},release._PROOF_TOKEN)
  with self.assertRaises(ValueError):p.finish()
 def test_actual_Markdown_and_existing_hook_full53render_and_head_controls(self):
  f=self.fixture();p=f.bind();contexts=f.rendered_contexts()
  self.assertTrue(validate_research_contexts(p,contexts));first=next(path for path in contexts if path not in f.owner_index)
  for mode in ['number','missing','title','JSONLD','footer']:
   bad=copy.deepcopy(contexts)
   if mode=='missing':bad.pop(first)
   elif mode=='number':
    bad[first]['html']=bad[first]['html'].replace('Four of ten','Nine of ten')
    bad[first]['rendered_html']=bad[first]['rendered_html'].replace(b'Four of ten',b'Nine of ten')
   elif mode=='title':bad[first]['rendered_html']=bad[first]['rendered_html'].replace(b'<title>Synthetic',b'<title>Wrong')
   elif mode=='JSONLD':bad[first]['rendered_html']=bad[first]['rendered_html'].replace(('"dateModified": "'+f.day).encode(),b'"dateModified": "2026-11-02')
   else:bad[first]['rendered_html']=bad[first]['rendered_html'].replace(b'Not peer reviewed.',b'Peer reviewed.')
   with self.subTest(mode=mode),self.assertRaises(ValueError):validate_research_contexts(p,bad)
 def test_actual_Material_search_exact53_and_every_unselected_row_preserved(self):
  f=self.fixture();p=f.bind();contexts=f.rendered_contexts()
  from material.plugins.search.plugin import SearchIndex
  from types import SimpleNamespace
  config={'lang':['en'],'separator':r'[\s\-]+','pipeline':['stopWordFilter']}
  index=SearchIndex(**config)
  for path,c in contexts.items():index.add_entry_from_context(SimpleNamespace(meta=c['meta'],title=c['meta']['title'],content=c['html'],toc=c['toc'],url=research_url('docs/'+path).removeprefix('https://docs.broadcastwell.com/')))
  outside={'location':'answers/unchanged/','title':'Actual unchanged fixture row','text':'Preserved.'}
  before={'config':config,'docs':[outside]+[{**r,'text':'Old fixture text'} for r in index.entries]}
  after={'config':config,'docs':[outside]+index.entries}
  self.assertTrue(validate_research_search(j(before),j(after),permit=p,contexts=contexts))
  for mode in ['library','oldresearch','extra','config','stalecontext']:
   bad=copy.deepcopy(after);ctx=copy.deepcopy(contexts)
   if mode=='library':bad['docs'][0]['text']='Changed Library row'
   elif mode=='oldresearch':bad['docs'][1]['text']='Stale source text'
   elif mode=='extra':bad['docs'].append({'location':'research/unlisted/','title':'Unlisted','text':'Unlisted'})
   elif mode=='config':bad['config']['lang']=['de']
   else:next(iter(ctx.values()))['meta']['description']='Stale metadata'
   with self.subTest(mode=mode),self.assertRaises(ValueError):validate_research_search(j(before),j(bad),permit=p,contexts=ctx)
 def test_whole_public_delta_rejects_unlisted_frozen_scientific_stub_and_price_files(self):
  f=self.fixture();p=f.bind();prior=copy.deepcopy(f.prior_public);candidate=copy.deepcopy(prior)
  library={f'answers/fixture/p{i}/index.html' for i in range(319)}
  for path in library:prior[path]=candidate[path]=b'unchanged Library fixture'
  frozen={path:support.sha(prior[path]) for path in sorted(library)[:45]}
  for i in range(5):
   path=f'assets/frozen-{i}.css';prior[path]=candidate[path]=b'unchanged asset';frozen[path]=support.sha(prior[path])
  stubs={f'answers/retired/p{i}/index.html':b'exact current stub fixture' for i in range(19)}
  prior.update(stubs);candidate.update(stubs)
  changed=next(iter(f.catalog['article_artifact_paths']));candidate[changed]=b'new fixture HTML'
  p.data['artifact_changes']={changed:{'before_sha256':support.sha(prior[changed]),'after_sha256':support.sha(candidate[changed])}}
  # Rebind the synthetic plan after declaring its exact candidate bytes.
  f.plan['artifact_changes']=p.data['artifact_changes'];f.refresh_synthetic_evidence();p=f.bind()
  args=dict(frozen_pins=frozen,exact_stub_bytes=stubs,library_artifact_paths=library,protected_scientific_pins=f.catalog['immutable_science_and_registered_downloads'])
  self.assertEqual(1,p.verify_public_delta(prior,candidate,**args)['actual_changed_artifact_count'])
  for mode in ['unlisted','frozen','scientific','stub','pricing','omit']:
   bad=dict(candidate)
   if mode=='unlisted':bad['research/unlisted/index.html']=b'unlisted'
   elif mode=='frozen':bad[next(iter(frozen))]=b'tampered'
   elif mode=='scientific':bad[next(iter(self.protected))]=b'tampered'
   elif mode=='stub':bad[next(iter(stubs))]=b'tampered'
   elif mode=='pricing':bad['pricing/index.html']=b'new price page'
   else:bad.pop(next(iter(library)))
   with self.subTest(mode=mode),self.assertRaises(ValueError):p.verify_public_delta(prior,bad,**args)
 def test_untrusted_public_proof_dict_and_internal_mutation_cannot_grant_permit(self):
  f=self.fixture();p=f.bind();p.proofs.update({k:{'forged':True} for k in ['render','sitemap','search','library_consumers','quality','freeze','stubs','PDF','whole_public_delta']})
  self.assertEqual({'sources'},set(p.proofs))
  with self.assertRaises(ValueError):p._record_proof('render',{'forged':True},object())
  p._proofs['render']={'forged':True}
  with self.assertRaises(ValueError):p.check()
 def test_final_stub_dispatch_rejects_partial_unknown_and_mixed_Research_inputs(self):
  from library_publication_verify_stubs import reviewed_stub_pages
  for env in [{'BW_RESEARCH_RELEASE_INPUTS':'x'},{'BW_RESEARCH_RELEASE_UNKNOWN':''},
   {'BW_RESEARCH_RELEASE_INPUTS':'x','BW_RESEARCH_RELEASE_INPUTS_SHA256':'a'*64,'BW_OWNER_REPAIR_INPUTS':'x'}]:
   with self.subTest(env=env),self.assertRaises(ValueError):reviewed_stub_pages(self.root,self.root/'site',environment=env)
 def test_all_new_modules_parse_and_ordinary_release_cap_file_is_untouched(self):
  names=['library_build_dispatch.py', 'library_inherited_presentation.py', 'library_publication_build.py', 'library_publication_consumers.py', 'library_publication_sitemap_dates.py', 'library_publication_verify_stubs.py', 'library_research_build.py', 'library_research_consumers.py', 'library_research_freeze_styles_hook.py', 'library_research_hooks_candidate.py', 'library_research_owner_preservation.py', 'library_research_release.py', 'library_research_render.py', 'library_research_source_archive.py', 'library_research_stage.py', 'library_research_support.py', 'verify_build.py']
  for name in names:ast.parse((T/name).read_text(encoding='utf-8'))
  self.assertNotIn('library_publication_release.py',names)
  # Git LF code identity; only the two verified raw checkout forms are accepted.
  release_raw=(T/'library_publication_release.py').read_bytes()
  self.assertIn(support.sha(release_raw),{'71a538a7a2fcd9312a522efffb05b4124cdada8a8a0f72c8ba881826e71672e6','5580daee9fef55111572afe6c735ed1025db71eb7d0df3ab8803f8acc3427339'})
  self.assertEqual('5580daee9fef55111572afe6c735ed1025db71eb7d0df3ab8803f8acc3427339',support.sha(release_raw.replace(b'\r\n',b'\n')))
  self.assertFalse((H/'ACTUAL_OUTPUTS').exists())
 def staged_fixture(self,approved=True):
  root=self.root/'namespace/checkout/repo';root.mkdir(parents=True)
  f=Fixture(self.root/'separate-source-fixture',self.protected);write(root,f.after);bundle=self.root/'bundle'
  registry=T/'library-publication/inputs/field-registry.json'
  handoff=T/'library-publication/inputs/field-handoff.md'
  rows={'field_freeze_registry':{'path':'registry.json','sha256':support.sha(registry.read_bytes())},
   'field_freeze_handoff':{'path':'handoff.md','sha256':support.sha(handoff.read_bytes())}}
  base=j({'files':rows,'receipt_files':[]})
  config=j({'schema_version':1,'policy':release.POLICY,'approved':approved,'review_kind':'library-root-reviewed-finite-research-release',
   'portable_files':{'base_inputs':{'path':'base.json','sha256':support.sha(base)}}})
  files={'.library-research-work/inputs.json':config,'.library-research-work/base.json':base,
   '.library-research-work/registry.json':registry.read_bytes(),'.library-research-work/handoff.md':handoff.read_bytes()}
  d=copy.deepcopy(f.plan_support);d['release_inputs']={'path':'.library-research-work/inputs.json','sha256':support.sha(config)}
  d['staged_file_sha256']={p:support.sha(raw) for p,raw in files.items()}
  raw=j(d);write(root,{support.PLAN:raw,support.PIN:support.sha(raw).encode()});write(bundle,files)
  return root,bundle,files
 def test_stage_exact_reviewed_work_files_only_and_matching_targets_untouched(self):
  from library_research_stage import stage
  root,bundle,files=self.staged_fixture();before={p.relative_to(root).as_posix():p.read_bytes() for p in (root/'docs').rglob('*') if p.is_file()}
  result=stage(root,bundle);self.assertEqual(0,result['manuscripts_changed'])
  self.assertEqual(before,{p.relative_to(root).as_posix():p.read_bytes() for p in (root/'docs').rglob('*') if p.is_file()})
  stamps={p:(root/p).stat().st_mtime_ns for p in files};stage(root,bundle)
  self.assertEqual(stamps,{p:(root/p).stat().st_mtime_ns for p in files})
  self.assertEqual('EXISTING_MATCHING_UNTOUCHED',stage(root,bundle)['accepted45_handoff_bridge']['status'])
 def test_stage_unapproved_source_plan_rejects_before_any_copy(self):
  from library_research_stage import stage
  root,bundle,files=self.staged_fixture(approved=False)
  with self.assertRaises(ValueError):stage(root,bundle)
  self.assertFalse((root/'.library-research-work').exists())
 def test_stage_changed_bundle_or_conflicting_existing_file_rejects(self):
  from library_research_stage import stage
  root,bundle,files=self.staged_fixture();p=next(iter(files));(bundle/p).write_bytes(b'changed')
  with self.assertRaises(ValueError):stage(root,bundle)
  self.assertFalse((root/'.library-research-work').exists());(bundle/p).write_bytes(files[p])
  write(root,{p:b'conflicting'})
  with self.assertRaises(ValueError):stage(root,bundle)
  self.assertEqual(b'conflicting',(root/p).read_bytes())
 def test_pending_Research_session_cannot_load_without_committed_exact_inputs(self):
  from library_research_build import ResearchBuildSession
  f=self.fixture()
  with self.assertRaises(ValueError):ResearchBuildSession.load(self.root/'docs',self.root/'unreviewed.json','a'*64,self.root/'work')
 def test_inherited_Appendix_real_Page_keeps_old_nav_current_title_and_original_File(self):
  from library_inherited_presentation import retain_appendix_from_actual_prior,OLD,NEW
  from mkdocs.structure.files import File
  from mkdocs.structure.pages import Page
  from mkdocs.config.defaults import MkDocsConfig
  from types import SimpleNamespace
  docs=self.root/'docs';docs.mkdir();source='---\ntitle: '+NEW+'\nheadline: '+OLD+'\n---\n\n# '+OLD+'\n\nUnchanged classification text.\n'
  (docs/'absence-rules.md').write_text(source,encoding='utf-8')
  html=('<title>'+NEW+' | The Absence Manual</title><link rel="canonical" href="https://docs.broadcastwell.com/absence-rules/"><nav class="md-nav--primary"><a href="/absence-rules/">'+OLD+'</a></nav>').encode()
  archive=zipfile.ZipFile(io.BytesIO(zipped({'absence-rules/index.html':html})))
  config=MkDocsConfig();config.load_dict({'site_name':'The Absence Manual','docs_dir':str(docs),'site_dir':str(self.root/'site')})
  file=File('absence-rules.md',str(docs),str(self.root/'site'),True);page=Page(OLD,file,config);file.page=page
  otherfile=File('other.md',str(docs),str(self.root/'site'),True);other=Page('Other',otherfile,config);otherfile.page=other;other.next_page=page
  nav=SimpleNamespace(items=[page],pages=[page],homepage=page)
  s=SimpleNamespace(docs=docs,archive=archive,overlay=SimpleNamespace(finite=finite))
  _,proof=retain_appendix_from_actual_prior(nav,[file,otherfile],s)
  self.assertIs(file.page,page);self.assertEqual(NEW,page.title);self.assertEqual(OLD,nav.pages[0].title)
  self.assertIs(other.next_page,nav.pages[0]);self.assertEqual(page,nav.pages[0]);self.assertEqual(nav.pages[0],page)
  self.assertFalse(proof['new_repair_or_approval'])
  archive.close()
 def test_inherited_Appendix_wrong_actual_prior_label_or_title_rejects(self):
  from library_inherited_presentation import retain_appendix_from_actual_prior,OLD,NEW
  from types import SimpleNamespace
  docs=self.root/'docs';docs.mkdir();(docs/'absence-rules.md').write_text('---\ntitle: '+NEW+'\nheadline: '+OLD+'\n---\n\n# '+OLD+'\n',encoding='utf-8')
  for label in ['Unreviewed title',NEW]:
   raw=('<title>'+NEW+' | The Absence Manual</title><link rel="canonical" href="https://docs.broadcastwell.com/absence-rules/"><nav class="md-nav--primary"><a href="/absence-rules/">'+label+'</a></nav>').encode()
   with zipfile.ZipFile(io.BytesIO(zipped({'absence-rules/index.html':raw}))) as z:
    with self.subTest(label=label),self.assertRaises(ValueError):retain_appendix_from_actual_prior(SimpleNamespace(),[],SimpleNamespace(docs=docs,archive=z,overlay=SimpleNamespace(finite=finite)))
 def test_inherited_styles_only_exact_current_prior_bundle_and45_tags(self):
  from library_inherited_presentation import retain_frozen_stylesheets_from_actual_prior
  from library_owner_repair import OLD_CSS
  from library_publication_build import BuildSession
  from library_publication_field_freeze import FieldFreeze
  from types import SimpleNamespace
  old=(H/'tests/fixtures/owner-repair/frozen-pr91-combined.css').read_bytes()
  new=b'/* Synthetic inherited current bundle */ body{color:black}'
  current='assets/stylesheets/combined-'+support.sha(new)[:16]+'.css';files={OLD_CSS:old,current:new};rows=[]
  for i in range(45):
   p=f'answers/frozen/p{i}/index.html';raw=('<link rel="stylesheet" href="/'+OLD_CSS+'"><article>Exact frozen fixture.</article>').encode()
   files[p]=raw;rows.append({'source_path':f'answers/frozen/p{i}.md','served_html_path':p,'served_html_sha256':support.sha(raw)})
  site=self.root/'site';write(site,{p:raw.replace(('/'+OLD_CSS).encode(),('/'+current).encode()) if p.endswith('.html') else raw for p,raw in files.items() if p!=OLD_CSS})
  session=BuildSession();session.archive=zipfile.ZipFile(io.BytesIO(zipped(files)));session.overlay=SimpleNamespace(_check_unchanged=lambda:None)
  session.freeze=SimpleNamespace(assert_current=lambda:None,data={'rows':rows,'presentation_asset_pins':[]},check_sitemap=lambda raw:None)
  result=retain_frozen_stylesheets_from_actual_prior(session,site)
  self.assertTrue(result['exact45_inherited_stylesheet_fragments_only']);self.assertTrue(all((site/r['served_html_path']).read_bytes()==files[r['served_html_path']] for r in rows))
  bad=site/rows[0]['served_html_path'];bad.write_bytes(bad.read_bytes().replace(b'Exact frozen fixture.',b'TAMPERED.'))
  retain_frozen_stylesheets_from_actual_prior(session,site)
  self.assertIn(b'TAMPERED.',bad.read_bytes())  # No whole-HTML overwrite hides it.
  with self.assertRaises(ValueError):FieldFreeze.check_files(session.freeze,{p.relative_to(site).as_posix():p.read_bytes() for p in site.rglob('*') if p.is_file()})
  (site/current).write_bytes(b'Unreviewed new style')
  with self.assertRaises(ValueError):retain_frozen_stylesheets_from_actual_prior(session,site)
  session.archive.close()
 def test_no_input_or_partial_unknown_or_mixed_environment_never_falls_back(self):
  cases=[{}, {'BW_RESEARCH_RELEASE_INPUTS':'x'}, {'BW_RESEARCH_RELEASE_EXTRA':''},
   {'BW_RESEARCH_RELEASE_INPUTS':'x','BW_RESEARCH_RELEASE_INPUTS_SHA256':'a'*64,'BW_LIBRARY_PUBLICATION_INPUTS':'x'}]
  for env in cases:
   with self.subTest(env=env),patch.dict(os.environ,env,clear=True),self.assertRaises(ValueError):from_environment({'docs_dir':str(self.root/'docs'),'site_dir':str(self.root/'site')})
 def test_archive_traversal_duplicate_symlink_reject(self):
  for mode in ['escape','duplicate','symlink']:
   b=io.BytesIO()
   with zipfile.ZipFile(b,'w') as z:
    if mode=='escape':z.writestr('../outside',b'bad')
    elif mode=='duplicate':z.writestr('same',b'1');z.writestr('same',b'2')
    else:
     item=zipfile.ZipInfo('link');item.external_attr=(stat.S_IFLNK|0o777)<<16;z.writestr(item,b'target')
   with self.subTest(mode=mode),self.assertRaises(ValueError):archive_files(b.getvalue())

if __name__=='__main__':unittest.main(verbosity=2)
