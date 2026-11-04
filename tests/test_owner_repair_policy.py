"""Synthetic unit fixtures. Approved flags below are not actual Root receipts."""
from pathlib import Path
from copy import deepcopy
import gzip,json,sys,unittest
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE/'tools'))
import library_owner_repair as p
from library_owner_repair_consumers import json_hash,apply_llms_lines,apply_nonlibrary_sitemap_dates,validate_peer,validate_fact_bindings,repair_ledger,compose_effective_payload

def edit(a,b):return {'old':a,'new':b,'old_sha256':p.sha(a.encode()),'new_sha256':p.sha(b.encode())}
def page(body='Preserved content',new=False,style=None):
 labels=p.LABELS
 nav='<nav class="md-nav md-nav--primary">'+''.join('<a href="/'+u+'"><span>\n    '+t[int(new)]+'\n  </span></a>' for u,t in labels.items())+'</nav>'
 style=style or '/'+p.OLD_CSS
 return ('<html><head><link rel="stylesheet" href="'+style+'"></head><body>'+nav+'<article>'+body+'</article></body></html>').encode()

def fixture_plan():
 prior={'answers/test/index.html':page()};rows={};xml=[]
 for i in range(45):
  name='answers/frozen'+str(i)+'/index.html';raw=('Frozen '+str(i)).encode();prior[name]=raw;url=p.SITE+'answers/frozen'+str(i)+'/'
  entry='<url><loc>'+url+'</loc><lastmod>2026-11-02</lastmod></url>';xml.append(entry)
  rows[str(i)+'.md']={'served_html_path':name,'served_html_sha256':p.sha(raw)}
 assets=[]
 for i in range(5):
  name='assets/frozen'+str(i)+'.js';raw=('asset'+str(i)).encode();prior[name]=raw;assets.append({'path':name,'sha256':p.sha(raw)})
 x=('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(xml)+'</urlset>').encode();prior['sitemap.xml']=x;prior['sitemap.xml.gz']=gzip.compress(x,mtime=0)
 freeze={'pages':rows,'presentation_asset_pins':assets,'frozen_sitemap_entries':[{'url':p.SITE+'answers/frozen'+str(i)+'/','exact_entry':x,'sha256':p.sha(x.encode())} for i,x in enumerate(xml)]}
 candidate=deepcopy(prior);candidate['answers/test/index.html']=page(new=True)
 scope={'answers/test/index.html':{'class':'navigation_only','before_sha256':p.sha(prior['answers/test/index.html']),'after_sha256':p.sha(candidate['answers/test/index.html'])}}
 # Internal constructor exercises pure delta checks only; bind authority is tested separately.
 plan=p.OwnerRepairPlan({'artifact_scope':scope},freeze,p._TOKEN)
 proof={'answers/test/index.html':p.validate_navigation_only('answers/test/index.html',prior['answers/test/index.html'],candidate['answers/test/index.html'])}
 return plan,prior,candidate,proof

class PolicyTests(unittest.TestCase):
 def test_two_exact_labels_pass_without_other_bytes_changed(self):
  self.assertTrue(p.validate_navigation_only('answers/test/index.html',page(),page(new=True))['outside_fragments_byte_exact'])
 def test_nav_only_rejects_changed_article(self):
  with self.assertRaisesRegex(p.RepairError,'outside primary'):p.validate_navigation_only('answers/test/index.html',page(),page('Changed body',True))
 def test_nav_rejects_an_extra_link(self):
  new=page(new=True).replace(b'</nav>',b'<a href="/extra/">Extra</a></nav>')
  with self.assertRaises(p.RepairError):p.validate_navigation_only('answers/test/index.html',page(),new)
 def test_nav_rejects_semantically_equal_unapproved_closing_tag_bytes(self):
  new=page(new=True).replace(b'</a>',b'</A >',1)
  with self.assertRaises(p.RepairError):p.validate_navigation_only('answers/test/index.html',page(),new)
 def test_nav_rejects_wrong_new_label(self):
  new=page(new=True).replace(p.LABELS['resources/audit/sample/'][1].encode(),b'Any retired format')
  with self.assertRaises(p.RepairError):p.validate_navigation_only('answers/test/index.html',page(),new)
 def test_css_comment_only_passes_and_rule_change_rejects(self):
  p.css_comment_only(b'/* old */a{color:blue}',b'/* new */a{color:blue}')
  with self.assertRaises(p.RepairError):p.css_comment_only(b'/* old */a{color:blue}',b'/* new */a{color:red}')
 def test_literal_edit_exact_inverse_and_ambiguous_rejection(self):
  self.assertEqual(b'before new after',p.exact_edits(b'before old after',[edit('old','new')]))
  with self.assertRaises(p.RepairError):p.exact_edits(b'old old',[edit('old','new')])
 def test_wrong_literal_span_hash_rejects(self):
  e=edit('old','new');e['old_sha256']='0'*64
  with self.assertRaises(p.RepairError):p.exact_edits(b'old',[e])
 def test_authority_receipt_no_raw_pdf_needed_but_actual_read_required(self):
  d={'schema_version':1,'reviewer':'root','review_kind':'owner-brief-local-full-read','policy':p.POLICY,'authority_pdf_sha256':p.AUTHORITY_SHA256,'pages_actually_read':5,'actual_full_read_complete':True,'local_hash_verified':True,'recorded_utc':'2026-11-03T17:00:00+00:00'}
  raw=p.encoded(d);self.assertEqual(d,p.validate_authority_receipt(raw,p.sha(raw)))
  d['actual_full_read_complete']=False;raw=p.encoded(d)
  with self.assertRaises(p.RepairError):p.validate_authority_receipt(raw,p.sha(raw))
 def test_authority_wrong_hash_private_field_and_changed_local_pdf_reject(self):
  d={'schema_version':1,'reviewer':'root','review_kind':'owner-brief-local-full-read','policy':p.POLICY,'authority_pdf_sha256':p.AUTHORITY_SHA256,'pages_actually_read':5,'actual_full_read_complete':True,'local_hash_verified':True,'recorded_utc':'2026-11-03T17:00:00+00:00'}
  raw=p.encoded(d)
  with self.assertRaises(p.RepairError):p.validate_authority_receipt(raw,'0'*64)
  with self.assertRaises(p.RepairError):p.validate_authority_receipt(raw,p.sha(raw),local_pdf=b'Changed local PDF')
  d['private_brief_text']='not allowed';raw=p.encoded(d)
  with self.assertRaises(p.RepairError):p.validate_authority_receipt(raw,p.sha(raw))
 def test_duplicate_json_keys_reject(self):
  with self.assertRaises(p.RepairError):p.json_unique(b'{"approved":false,"approved":true}')
 def test_frozen_source_any_class_rejects(self):
  with self.assertRaises(p.RepairError):p.validate_source_class('docs/answers/x/frozen.md',{'class':'rule4_fact'},answer_paths={'answers/x/frozen.md'},research_paths=set(),bank_ids={},frozen_sources={'answers/x/frozen.md'})
 def test_unlisted_research_and_wrong_metadata_record_reject(self):
  for path,row in [('docs/research/new.md',{'class':'rule4_fact'}),('docs/answers/a/other.md',{'class':'answer_metadata'})]:
   with self.assertRaises(p.RepairError):p.validate_source_class(path,row,answer_paths=set(),research_paths=set(),bank_ids={},frozen_sources=set())
 def test_exact_artifact_delta_passes_but_grants_no_s5_completion(self):
  plan,a,b,proof=fixture_plan();r=p.validate_artifact_delta(plan,prior=a,candidate=b,navigation_proofs=proof)
  self.assertEqual(1,r['actual_changed_artifact_count']);self.assertFalse(r['S5_completion_granted']);self.assertFalse(r['ordinary_S5_cap_changed'])
 def test_extra_nonlibrary_artifact_hidden_delta_rejects(self):
  plan,a,b,proof=fixture_plan();b['research/unlisted/index.html']=b'Changed'
  with self.assertRaises(p.RepairError):p.validate_artifact_delta(plan,prior=a,candidate=b,navigation_proofs=proof)
 def test_one_byte_frozen_html_asset_and_xml_reject(self):
  for path in ['answers/frozen0/index.html','assets/frozen0.js','sitemap.xml']:
   plan,a,b,proof=fixture_plan();b[path]+=b'x'
   with self.assertRaises(p.RepairError):p.validate_artifact_delta(plan,prior=a,candidate=b,navigation_proofs=proof)
 def test_mutated_bound_plan_rejects(self):
  plan,a,b,proof=fixture_plan();plan.data['artifact_scope'].clear()
  with self.assertRaises(p.RepairError):p.validate_artifact_delta(plan,prior=a,candidate=b,navigation_proofs=proof)
 def test_omitted_unfrozen_navigation_page_rejects(self):
  plan,a,b,proof=fixture_plan();a['another/index.html']=page();b['another/index.html']=page()
  with self.assertRaisesRegex(p.RepairError,'omitted'):p.validate_artifact_delta(plan,prior=a,candidate=b,navigation_proofs=proof)
 def test_false_navigation_proof_and_wrong_after_hash_reject(self):
  plan,a,b,proof=fixture_plan()
  with self.assertRaises(p.RepairError):p.validate_artifact_delta(plan,prior=a,candidate=b,navigation_proofs={})
  b['answers/test/index.html']+=b'x'
  with self.assertRaises(p.RepairError):p.validate_artifact_delta(plan,prior=a,candidate=b,navigation_proofs=proof)
 def test_ordinary_s5_still_rejects_cap51(self):
  from library_publication_release import incremental_release_gate
  with self.assertRaisesRegex(ValueError,'cap cannot exceed50'):
   incremental_release_gate(previous_manifest_path='unused',trusted_previous_sha256='',actual_prior_production_binding={},candidate_state={},actual_candidate_state={},authorized_change_map={},full_current_report={},q=None,maximum_changed_routes=51)
 def test_frozen_old_style_fixture_hash_and_finite_href_restore(self):
  oldcss=(HERE/'tests/fixtures/owner-repair/frozen-pr91-combined.css').read_bytes();self.assertEqual(p.OLD_CSS_SHA256,p.sha(oldcss));newcss=b'new compiled css';newpath='assets/stylesheets/combined-'+p.sha(newcss)[:16]+'.css';old=page();new=page(new=True,style='/'+newpath)
  out=p.restore_frozen_stylesheet(page='answers/test/index.html',before=old,candidate=new,new_bundle_path=newpath,new_bundle_bytes=newcss,baseline_files={p.OLD_CSS:oldcss})
  self.assertEqual(page(new=True),out)
 def test_frozen_style_unrelated_tag_or_wrong_old_asset_rejects(self):
  oldcss=(HERE/'tests/fixtures/owner-repair/frozen-pr91-combined.css').read_bytes();newcss=b'new';path='assets/stylesheets/combined-'+p.sha(newcss)[:16]+'.css'
  for raw,base in [(page(new=True,style='/'+path).replace(b'rel="stylesheet"',b'rel="stylesheet" media="all"'),oldcss),(page(new=True,style='/'+path),b'wrong')]:
   with self.assertRaises(p.RepairError):p.restore_frozen_stylesheet(page='answers/test/index.html',before=page(),candidate=raw,new_bundle_path=path,new_bundle_bytes=newcss,baseline_files={p.OLD_CSS:base})

class ConsumerTests(unittest.TestCase):
 def test_llms_finite_lines_preserve_all_other_bytes(self):
  a='- [Title](https://docs.broadcastwell.com/a/): Old description.';b='- [Title](https://docs.broadcastwell.com/a/): New description.';raw=('## Prices\nKeep exact.\n'+a+'\n## Research\nKeep exact too.\n').encode()
  after,proof=apply_llms_lines(raw,[edit(a,b)],allowed_urls={'https://docs.broadcastwell.com/a/'})
  self.assertEqual(raw.replace(a.encode(),b.encode()),after);self.assertTrue(proof['exact_inverse_or_actual_contexts'])
 def test_llms_wrong_url_or_changed_title_without_explicit_retitle_rejects(self):
  a='- [Title](https://docs.broadcastwell.com/a/): Old.'
  for b in ['- [Title](https://docs.broadcastwell.com/b/): New.','- [Other](https://docs.broadcastwell.com/a/): New.']:
   with self.assertRaises(p.RepairError):apply_llms_lines((a+'\n').encode(),[edit(a,b)],allowed_urls={'https://docs.broadcastwell.com/a/'})
 def test_xml_one_approved_date_inverse_and_gzip(self):
  url=p.SITE+'research/example/';old=('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+url+'</loc><lastmod>2026-11-02</lastmod></url></urlset>').encode()
  new,gz,proof,_=apply_nonlibrary_sitemap_dates(old,{url:'2026-11-03'},approved_source_metadata={url:{'date_modified':'2026-11-03T17:00:00+00:00'}},frozen_urls=set())
  self.assertEqual(old.replace(b'2026-11-02',b'2026-11-03'),new);self.assertEqual(new,gzip.decompress(gz));self.assertTrue(proof['exact_inverse_or_actual_contexts'])
 def test_xml_unknown_frozen_and_stale_date_rejects(self):
  url=p.SITE+'research/example/';old=('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+url+'</loc><lastmod>2026-11-02</lastmod></url></urlset>').encode()
  for dates,frozen in [({p.SITE+'research/other/':'2026-11-03'},set()),({url:'2026-11-03'},{url}),({url:'2026-11-01'},set())]:
   with self.assertRaises(p.RepairError):apply_nonlibrary_sitemap_dates(old,dates,approved_source_metadata={url:{'date_modified':'2026-11-03T17:00:00+00:00'}},frozen_urls=frozen)
 def fact(self):
  r={'source_kind':'published-study','numeric_cut':True,'source_url':'https://doi.org/10.5281/zenodo.12345','count':4,'base':30,'unit':'answers','observed_at':'2026-09-22','public_text':'Four of30 answers named the vendor.'}
  b={'observation_id':'actual-cut','published_record_sha256':json_hash(r),**{k:r[k] for k in ['source_url','count','base','unit','observed_at']},'quote':'Four of30 answers named the vendor.','body_span':'We observed4 of30 answers on22September2026.'};return r,b
 def test_exact_published_fact_binding_passes(self):
  r,b=self.fact();self.assertTrue(validate_fact_bindings([b],published_records={'actual-cut':r},after_body=b['body_span'],allowed_public_urls={r['source_url']})['all_exact'])
 def test_wrong_fact_hash_count_base_date_or_body_rejects(self):
  r,b=self.fact()
  for k,v in [('published_record_sha256','0'*64),('count',1),('base',150),('observed_at','2026-09-23'),('body_span','Not in actual body')]:
   bad=deepcopy(b);bad[k]=v
   with self.assertRaises(p.RepairError):validate_fact_bindings([bad],published_records={'actual-cut':r},after_body=b['body_span'],allowed_public_urls={r['source_url']})
 def test_qualitative_numeric1_and_unsupported_kind_reject(self):
  r,b=self.fact()
  for field,value in [('numeric_cut',False),('source_kind','private-watch')]:
   bad=deepcopy(r);bad[field]=value;binding=deepcopy(b);binding['published_record_sha256']=json_hash(bad)
   with self.assertRaises(p.RepairError):validate_fact_bindings([binding],published_records={'actual-cut':bad},after_body=b['body_span'],allowed_public_urls={r['source_url']})

if __name__=='__main__':unittest.main()
