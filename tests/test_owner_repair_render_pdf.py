"""Synthetic approvals test the contract; no actual visual read is claimed."""
from pathlib import Path
import copy,json,sys,unittest
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE/'tools'))
import library_owner_repair as p
from library_owner_repair_consumers import validate_render_context,validate_actual_search,validate_content_surface
from library_owner_repair_pdf import capture_pdf_observation,validate_owner_pdf_review,inspect_pdf


class RenderTests(unittest.TestCase):
 def fixture(self):
  import markdown
  path='research/example/index.md';body='# Exact title\n\nThe public record has4 of30 answers on22September2026.\n'
  meta={'title':'Exact title','description':'Exact approved description.','page_class':'research'};html=markdown.markdown(body,extensions=['toc','tables','attr_list','md_in_html','def_list','footnotes','admonition'],extension_configs={'toc':{'permalink':True,'toc_depth':3}})
  from library_publication_hooks_candidate import on_page_content
  from types import SimpleNamespace
  html=on_page_content(html,page=SimpleNamespace(meta=meta))
  head='<head><title>Exact title | The Absence Manual</title><link rel="canonical" href="https://docs.broadcastwell.com/research/example/">'+''.join('<meta '+('property' if k.startswith('og:') else 'name')+'="'+k+'" content="'+v+'">' for k,v in [('og:title',meta['title']),('twitter:title',meta['title']),('description',meta['description']),('og:description',meta['description']),('twitter:description',meta['description'])])+'</head>'
  rendered=('<html>'+head+'<article>'+html+'</article></html>').encode();record={'body':body,'meta':meta};context={'markdown':body,'meta':meta,'html':html,'toc':[],'rendered_html':rendered.decode()}
  return path,record,context,rendered
 def test_actual_markdown_context_head_and_source_proof(self):
  path,r,c,raw=self.fixture();self.assertTrue(validate_render_context(path,r,c,raw)['source_render_exact'])
 def test_wrong_body_head_canonical_description_and_late_mutation_reject(self):
  path,r,c,raw=self.fixture()
  for bad in [raw.replace(b'Exact title |',b'Stale title |'),raw.replace(b'/research/example/',b'/research/other/'),raw.replace(b'Exact approved description.',b'Stale description.')]:
   changed={**c,'rendered_html':bad.decode()}
   with self.assertRaises(ValueError):validate_render_context(path,r,changed,bad)
  with self.assertRaises(ValueError):validate_render_context(path,r,c,raw+b'late mutation')
  changed={**c,'html':c['html'].replace('4 of30','5 of30')}
  with self.assertRaises(ValueError):validate_render_context(path,r,changed,raw)
 def search(self):
  from material.plugins.search.plugin import SearchIndex
  from types import SimpleNamespace
  path,r,c,_=self.fixture();idx=SearchIndex(lang=['en'],separator=r'[\s\-]+');idx.add_entry_from_context(SimpleNamespace(meta=r['meta'],title=r['meta']['title'],content=c['html'],toc=[],url='research/example/'))
  config={'lang':['en'],'separator':r'[\s\-]+'};old={'config':config,'docs':[{'location':'other/','title':'Keep','text':'Exact unrelated row'}]};new={**old,'docs':old['docs']+idx.entries}
  return path,r,c,old,new
 def test_actual_material_search_entries_derive_from_effective_context(self):
  path,r,c,a,b=self.search();result=validate_actual_search(json.dumps(a).encode(),json.dumps(b).encode(),changed_contexts={path:c},expected_records={path:r});self.assertTrue(result['exact_inverse_or_actual_contexts'])
 def test_unlisted_search_row_or_stale_effective_title_reject(self):
  path,r,c,a,b=self.search()
  for bad in [copy.deepcopy(b),copy.deepcopy(b)]:
   if bad==b:bad['docs'][0]['text']='Unlisted changed text'
   with self.assertRaises(ValueError):validate_actual_search(json.dumps(a).encode(),json.dumps(bad).encode(),changed_contexts={path:c},expected_records={path:r})
  bad=copy.deepcopy(b);bad['docs'][1]['title']='Stale title'
  with self.assertRaises(ValueError):validate_actual_search(json.dumps(a).encode(),json.dumps(bad).encode(),changed_contexts={path:c},expected_records={path:r})


class SurfaceTests(unittest.TestCase):
 def fixture(self):
  import markdown
  from types import SimpleNamespace
  from library_publication_hooks_candidate import on_page_content
  from test_owner_repair_policy import page
  meta={'title':'Specific current question','headline':'Specific current question','description':'Old bounded description.','date_published':'2026-09-01T00:00:00+00:00','date_modified':'2026-11-02T00:00:00+00:00','page_class':'research','schema_type':'TechArticle'}
  newer={**meta,'description':'New bounded description.','date_modified':'2026-11-03T18:00:00+00:00'}
  before={'meta':meta,'body':'# Specific current question\n\nThe count is4 of30.\n'};after={'meta':newer,'body':'# Specific current question\n\nThe count is4 of30, with the exact unit clarified.\n'}
  def render(r,new):
   html=on_page_content(markdown.markdown(r['body'],extensions=['toc','tables','fenced_code','attr_list','md_in_html','def_list','footnotes','admonition'],extension_configs={'toc':{'permalink':True,'toc_depth':3}}),page=SimpleNamespace(meta=r['meta']))
   obj={'@type':'TechArticle',**{k:r['meta'][v] for k,v in [('name','headline'),('headline','headline'),('description','description'),('datePublished','date_published'),('dateModified','date_modified')]},'author':{'name':'Keep exact'}}
   raw=page(body=html+'\n<hr>\n<p class="manual-footer-version">Existing exact footer.</p>',new=new)
   raw=raw.replace(b'</head>',('<script type="application/ld+json">'+json.dumps(obj)+'</script></head>').encode())
   return html,raw
  _,a=render(before,False);html,b=render(after,True)
  return before,after,{'html':html},a,b
 def test_finite_content_metadata_navigation_preserve_every_other_token(self):
  a,b,c,old,new=self.fixture();self.assertTrue(validate_content_surface('research/example/index.md',a,b,c,old,new)['outside_approved_content_metadata_navigation_tokens_exact'])
 def test_extra_script_footer_or_structured_author_change_reject(self):
  a,b,c,old,new=self.fixture()
  for bad in [new.replace(b'</body>',b'<script>unapproved()</script></body>'),new.replace(b'Existing exact footer.',b'Changed unrelated footer.'),new.replace(b'Keep exact',b'Changed author')]:
   with self.assertRaises(ValueError):validate_content_surface('research/example/index.md',a,b,c,old,bad)
 def test_stale_structured_date_or_dropped_fact_reject(self):
  a,b,c,old,new=self.fixture()
  for bad in [new.replace(b'2026-11-03T18:00:00+00:00',b'2026-11-02T00:00:00+00:00'),new.replace(b'4 of30',b'5 of30')]:
   with self.assertRaises(ValueError):validate_content_surface('research/example/index.md',a,b,c,old,bad)


class PdfTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  import library_publication_build
  repo=Path(library_publication_build.__file__).resolve().parent.parent
  cls.path='assets/samples/Kalvenor_Sample_Category_Audit.pdf'
  cls.old=(repo/'docs'/cls.path).read_bytes();cls.new=cls.old+b'\n'
  # Existing published PDF bytes only; no test creates or edits a PDF file.
  cls.ci={'runner_os':'Linux','source_head':'a'*40,'checkout_commit':'b'*40,'source_tree':'c'*40,'repository':'fixture/repo','workflow_ref':'fixture/repo/.github/workflows/verify.yml@refs/pull/1/merge','run_id':'1','run_attempt':'1'}
 def fixture(self):
  before={'docs/'+self.path:p.sha(self.old)};after={'docs/'+self.path:p.sha(self.new)}
  obs=capture_pdf_observation(self.path,self.old,self.new,prior_artifact_sha256='d'*64,before_inputs=before,after_inputs=after,actual_ci=self.ci)
  frames={(v,i):('SYNTHETIC-RASTER-FIXTURE-'+v+str(i)).encode() for v in ['before','after'] for i in range(1,obs[v]['page_count']+1)}
  visual={'approved':True,'reviewer':'root','review_kind':'actual-owner-repair-full-pdf-visual-read','path':self.path,'before_pdf_sha256':p.sha(self.old),'after_pdf_sha256':p.sha(self.new),'frames':[{'version':v,'page':i,'actually_viewed':True,'layout_readable':True,'no_clipping_overlap_missing_glyphs':True,'render_sha256':p.sha(raw)} for (v,i),raw in frames.items()],'all_original_figures_quotes_dates_preserved_or_exact_source_approved':True}
  full=p.digest({'before':obs['before'],'after':obs['after']});source={'approved':True,'review_kind':'source-exact-owner-repair-pdf-text','policy':p.POLICY,'path':self.path,'before_pdf_sha256':p.sha(self.old),'after_pdf_sha256':p.sha(self.new),'full_text_and_geometry_sha256':full,'after_consumed_inputs_sha256':p.digest(after),'all_original_figures_quotes_dates_preserved_or_exact_source_approved':True}
  source_raw=p.encoded(source);visual_raw=p.encoded(visual)
  review={'approved':True,'reviewer':'root','review_kind':'root-owner-repair-pdf','policy':p.POLICY,'path':self.path,'before_sha256':p.sha(self.old),'after_sha256':p.sha(self.new),'prior_artifact_sha256':'d'*64,'observation_sha256':p.digest(obs),'after_consumed_inputs_sha256':p.digest(after),'before_consumed_inputs_sha256':p.digest(before),'full_text_and_geometry_sha256':full,'all_text_changes_source_reviewed':True,'source_review_receipt_sha256':p.sha(source_raw),'visual_receipt_sha256':p.sha(visual_raw),'first_linux_artifact_id':'1','first_linux_artifact_sha256':'e'*64}
  return dict(path=self.path,old=self.old,new=self.new,review_raw=p.encoded(review),review_sha256=p.sha(p.encoded(review)),observation=obs,visual_raw=visual_raw,visual_sha256=p.sha(visual_raw),rendered_frames=frames,before_inputs=before,after_inputs=after,prior_artifact_sha256='d'*64,source_change_pins={'docs/'+self.path:{'before_sha256':p.sha(self.old),'after_sha256':p.sha(self.new)}},approved_code_pins={},current_ci=self.ci,source_review_raw=source_raw,source_review_sha256=p.sha(source_raw))
 def test_full_existing_pdf_text_geometry_and_exact_receipt_fixture(self):
  kw=self.fixture();self.assertGreater(kw['observation']['after']['page_count'],1);r=validate_owner_pdf_review(**kw);self.assertTrue(r['actual_Root_visual_review_complete']);self.assertFalse(r['http301_verified'])
 def test_pdf_observation_cache_cannot_be_mutated_by_a_caller(self):
  first=inspect_pdf(self.old);count=first['page_count'];first['pages'].clear();first['page_count']=1
  second=inspect_pdf(self.old);self.assertEqual(count,second['page_count']);self.assertEqual(count,len(second['pages']))
 def test_original_known_defect_needs_honest_inventory_not_a_false_clean_flag(self):
  kw=self.fixture();v=json.loads(kw['visual_raw']);before=next(r for r in v['frames'] if r['version']=='before' and r['page']==1)
  before.update(layout_readable=False,no_clipping_overlap_missing_glyphs=False,preexisting_defects=[{'id':'known-label-touch','description':'Specific original label touches adjacent count.','rectangle':[1,1,8,8]}])
  def update():
   kw['visual_raw']=p.encoded(v);kw['visual_sha256']=p.sha(kw['visual_raw']);r=json.loads(kw['review_raw']);r['visual_receipt_sha256']=kw['visual_sha256'];kw['review_raw']=p.encoded(r);kw['review_sha256']=p.sha(kw['review_raw'])
  update();result=validate_owner_pdf_review(**kw);self.assertTrue(result['all_after_pages_layout_clear']);self.assertEqual('known-label-touch',result['before_layout_defect_inventory'][0]['defects'][0]['id']);self.assertFalse(result['global_layout_PASS_inferred_from_preservation'])
  before['no_clipping_overlap_missing_glyphs']=True;update()
  with self.assertRaises(ValueError):validate_owner_pdf_review(**kw)
 def test_unlisted_pdf_missing_visual_page_wrong_raster_and_wrong_source_reject(self):
  original=self.fixture()
  for key,value in [('path','another.pdf'),('source_review_raw',b'{}'),('new',self.new+b'changed')]:
   kw=copy.deepcopy(original);kw[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):validate_owner_pdf_review(**kw)
  for mode in ['missing-page','wrong-raster','not-actually-read']:
   kw=copy.deepcopy(original);v=json.loads(kw['visual_raw'])
   if mode=='missing-page':v['frames'].pop()
   elif mode=='wrong-raster':kw['rendered_frames'][('after',1)]=b'different raster'
   else:v['frames'][0]['actually_viewed']=False
   kw['visual_raw']=p.encoded(v);kw['visual_sha256']=p.sha(kw['visual_raw']);r=json.loads(kw['review_raw']);r['visual_receipt_sha256']=kw['visual_sha256'];kw['review_raw']=p.encoded(r);kw['review_sha256']=p.sha(kw['review_raw'])
   with self.subTest(mode=mode),self.assertRaises(ValueError):validate_owner_pdf_review(**kw)
 def test_unsupported_generator_change_wrong_linux_binding_or_fake_source_review_reject(self):
  original=self.fixture()
  for mode in ['generator','windows','source-false']:
   kw=copy.deepcopy(original)
   if mode=='generator':kw['after_inputs']['tools/unreviewed.py']='f'*64
   elif mode=='windows':kw['current_ci']['runner_os']='Windows'
   else:
    s=json.loads(kw['source_review_raw']);s['approved']=False;kw['source_review_raw']=p.encoded(s);kw['source_review_sha256']=p.sha(kw['source_review_raw']);r=json.loads(kw['review_raw']);r['source_review_receipt_sha256']=kw['source_review_sha256'];kw['review_raw']=p.encoded(r);kw['review_sha256']=p.sha(kw['review_raw'])
   with self.subTest(mode=mode),self.assertRaises(ValueError):validate_owner_pdf_review(**kw)


if __name__=='__main__':unittest.main()
