"""Meaningful synthetic guard cases; none is an actual Root approval."""
from pathlib import Path
import copy,importlib.util,json,os,sys,tempfile,unittest
from unittest.mock import patch
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE/'tools'))
import library_owner_repair as p
import library_owner_repair_build as build
from library_owner_repair_consumers import (json_hash,validate_peer,repair_ledger,
    compose_effective_payload,validate_static_peer,validate_render_context,validate_actual_search)
from test_owner_repair_policy import page,edit


def quality():
 paths=['answers/x/p'+str(i)+'.md' for i in range(326)];frozen=set(paths[:45])
 rows={x:{'status':'DEFERRED_FIELD_TEST' if x in frozen else 'FAIL','passed':None if x in frozen else False} for x in paths}
 rows[paths[-1]]={'status':'PASS','passed':True}
 d={'analysis_completed':True,'baseline_exceptions':0,'pair_count':52975,'page_readiness':rows,'global_fatal_errors':[],'comparison_scopes':{n:{'pair_count':52975,'all_pairs_compared':True,'violations':[]} for n in ['literal','runtime']}}
 return d,frozen,paths


def current_fixture():
 meta={'title':'A current question','headline':'A current question','date_published':'2026-09-01T00:00:00+00:00','date_modified':'2026-11-03T17:00:00+00:00','description':'Before.'}
 body='# A current question\n\nSame measured opening.\n'
 old='---\n'+json.dumps(meta)+'\n---\n'+body
 before={'meta':meta,'body':body,'effective_full_source':old,'review_ids':{'source':'old-source','writing':'old-writing'}}
 newer=copy.deepcopy(meta);newer['description']='After.';newer['date_modified']='2026-11-03T18:00:00+00:00';full='---\n'+json.dumps(newer)+'\n---\n'+body
 def parse(text):h,b=text.split('\n---\n',1);return json.loads(h[4:]),b
 rawpin='a'*64;ledger=repair_ledger('answers/x/a.md',before,full,[],newer)
 record={'path':'answers/x/a.md','raw_canonical_source_sha256':rawpin,'before_effective_canonical_source_sha256':p.sha(old.encode()),'effective_full_source':full,'meta':newer,'body':body}
 store={};ids={'path':record['path']}
 for kind in ['source','writing']:
  d={'review_kind':kind,'approved':True,'current_full_file_actually_read':True,'scope':'owner-exact-repair-changes','policy':p.POLICY,'approved_exact_repair_changes':True,'preserved_facts':True,'repair_change_ledger_sha256':json_hash(ledger),'remaining_prior_S5_defects':['Existing footer needs S5 repair.'],'current_S5_pass':False,'path':record['path'],'canonical_source_sha256':rawpin,'before_effective_canonical_source_sha256':record['before_effective_canonical_source_sha256'],'effective_canonical_source_sha256':p.sha(full.encode()),'effective_body_sha256':p.sha(body.encode()),'effective_meta_sha256':json_hash(newer)}
  raw=json.dumps(d).encode();ids[kind]=p.sha(raw);store[p.sha(raw)]=raw
 return before,full,parse,record,ledger,store,ids


class IntegrationTests(unittest.TestCase):
 def test_scoped_current_dual_raw_and_effective_receipts_compose_without_article_pass(self):
  before,full,parse,r,l,store,ids=current_fixture()
  actual=compose_effective_payload(before,after_full=full,body_edits=[],expected_before_sha256=r['before_effective_canonical_source_sha256'],raw_source_sha256=r['raw_canonical_source_sha256'],review_ids=ids,receipt_store=store,source_parser=parse,allowed_metadata_fields={'description','date_modified'},actual_adoption_utc=r['meta']['date_modified'])
  self.assertEqual(full,actual['effective_full_source']);self.assertEqual(before['body'],actual['body']);self.assertNotIn('current_S5_pass',actual)
 def test_conflating_raw_and_effective_or_wrong_body_meta_path_ledger_rejects(self):
  _,_,_,r,l,store,ids=current_fixture();d=json.loads(store[ids['source']])
  for key,value in [('canonical_source_sha256',r['before_effective_canonical_source_sha256']),('before_effective_canonical_source_sha256',r['raw_canonical_source_sha256']),('effective_body_sha256','0'*64),('effective_meta_sha256','0'*64),('path','answers/x/other.md'),('repair_change_ledger_sha256','0'*64),('current_S5_pass',True),('current_full_file_actually_read',False)]:
   changed={**d,key:value};raw=json.dumps(changed).encode()
   with self.subTest(key=key),self.assertRaises(p.RepairError):validate_peer(raw,p.sha(raw),r,'source',json_hash(l))
 def test_missing_fresh_peer_never_uses_old_approval(self):
  before,full,parse,r,l,store,ids=current_fixture();del store[ids['source']]
  with self.assertRaises(p.RepairError):compose_effective_payload(before,after_full=full,body_edits=[],expected_before_sha256=r['before_effective_canonical_source_sha256'],raw_source_sha256=r['raw_canonical_source_sha256'],review_ids=ids,receipt_store=store,source_parser=parse,allowed_metadata_fields={'description','date_modified'},actual_adoption_utc=r['meta']['date_modified'])
 def test_date_published_or_date_only_churn_rejects(self):
  before,full,parse,r,l,store,ids=current_fixture()
  for revised in [full.replace('2026-09-01','2026-09-02'),full.replace('After.','Before.')]:
   with self.assertRaises(p.RepairError):compose_effective_payload(before,after_full=revised,body_edits=[],expected_before_sha256=r['before_effective_canonical_source_sha256'],raw_source_sha256=r['raw_canonical_source_sha256'],review_ids=ids,receipt_store=store,source_parser=parse,allowed_metadata_fields={'description','date_modified','date_published'},actual_adoption_utc=r['meta']['date_modified'])
 def test_real_whole_fail_is_retained_without_ordinary_s5_completion(self):
  before,frozen,_=quality();after=copy.deepcopy(before)
  result=p.validate_quality_transition(before,after,changed_content_paths=set(),frozen_paths=frozen)
  self.assertEqual(280,result['actual_current_FAIL_rows_retained']);self.assertFalse(result['S5_full_PASS_granted'])
 def test_prior_pass_regression_and_frozen_falsepass_reject(self):
  before,frozen,paths=quality()
  for path,row in [(paths[-1],{'passed':False,'status':'FAIL'}),(paths[0],{'passed':True,'status':'PASS'})]:
   after=copy.deepcopy(before);after['page_readiness'][path]=row
   with self.assertRaises(p.RepairError):p.validate_quality_transition(before,after,changed_content_paths=set(),frozen_paths=frozen)
 def test_each_scope_worsening_blocks_even_when_other_scope_already_worse(self):
  before,frozen,paths=quality();pair=paths[-3:-1]
  old={'kind':'six_word_similarity','key':'pair','pages':pair,'score_fraction':'1/4'}
  before['comparison_scopes']['runtime']['violations']=[old]
  after=copy.deepcopy(before);after['comparison_scopes']['literal']['violations']=[{**old,'score_fraction':'21/100'}]
  with self.assertRaises(p.RepairError):p.validate_quality_transition(before,after,changed_content_paths=set(),frozen_paths=frozen)
  after=copy.deepcopy(before);after['comparison_scopes']['runtime']['violations']=[{**old,'score_fraction':'26/100'}]
  with self.assertRaises(p.RepairError):p.validate_quality_transition(before,after,changed_content_paths=set(),frozen_paths=frozen)
 def test_wrong_paircount_globalfatal_or_baseline_exception_reject(self):
  before,frozen,_=quality()
  for key,value in [('pair_count',48205),('global_fatal_errors',['Missing actual source render']),('baseline_exceptions',1)]:
   after=copy.deepcopy(before);after[key]=value
   with self.assertRaises(p.RepairError):p.validate_quality_transition(before,after,changed_content_paths=set(),frozen_paths=frozen)
 def test_pagination_same_two_targets_pass_extra_text_or_href_reject(self):
  oldnav='<nav class="bw-document-pagination"><a href="/resources/audit/executive-template/" rel="prev">Previous: '+p.LABELS['resources/audit/executive-template/'][0]+'</a></nav>'
  newnav=oldnav.replace(p.LABELS['resources/audit/executive-template/'][0],p.LABELS['resources/audit/executive-template/'][1])
  old=page()+oldnav.encode();new=page(new=True)+newnav.encode()
  self.assertTrue(p.validate_navigation_only('resources/audit/recheck-receipts/index.html',old,new))
  for bad in [new.replace(b'rel="prev"',b'rel="next"'),new.replace(b'</nav>',b'Unapproved</nav>'),new.replace(b'/resources/audit/executive-template/',b'/another/',1)]:
   with self.assertRaises(p.RepairError):p.validate_navigation_only('resources/audit/recheck-receipts/index.html',old,bad)
 def test_css_tag_attribute_injection_rejects(self):
  old=page();new=page(new=True).replace(b'rel="stylesheet"',b'rel="stylesheet" media="all"')
  a,b=p.spans(old).styles[0],p.spans(new).styles[0]
  with self.assertRaises(p.RepairError):p.validate_navigation_only('a/index.html',old,new,old_css=old[a[0]:a[1]],new_css=new[b[0]:b[1]])
 def test_explicit_owner_dispatch_cannot_fall_back_or_share_active_environment(self):
  for env in [{},{'BW_OWNER_REPAIR_INPUTS':'missing','BW_OWNER_REPAIR_INPUTS_SHA256':'0'*64,'BW_LIBRARY_PUBLICATION_INPUTS':'ordinary'}]:
   with patch.dict(os.environ,env,clear=True),self.assertRaises(p.RepairError):build.from_environment({'docs_dir':'unused','site_dir':'unused'})
 def test_bound_relative_input_hash_and_namespace_are_checked(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);(root/'file.json').write_bytes(b'{}')
   self.assertEqual(b'{}',build.bound_file(root,{'path':'file.json','sha256':p.sha(b'{}')})[1])
   for row in [{'path':'../file.json','sha256':p.sha(b'{}')},{'path':'file.json','sha256':'0'*64},{'path':'C:/secret','sha256':'0'*64}]:
    with self.assertRaises(p.RepairError):build.bound_file(root,row)
 def test_old_pdf_paths_only_no_arbitrary_pdf_or_fabricated_northstar_path(self):
  self.assertNotIn('assets/samples/Northstar_synthetic_sample_retired_format.pdf',p.PDF_PATHS)
  self.assertNotIn('assets/samples/WhiteLabel_Sample_Category_Audit_v3.pdf',p.PDF_PATHS)
  self.assertIn('assets/samples/White_label_Category_Audit_sample.pdf',p.PDF_PATHS);self.assertIn('assets/samples/WhiteLabel_Sample_Category_Audit_v2.pdf',p.PDF_PATHS)
 def test_owner_stylesheet_hook_precedes_unchanged_freeze_and_final_capture(self):
  import library_owner_repair_freeze_styles_hook as hook
  self.assertEqual(-190,hook.on_post_build.mkdocs_priority)
  text=(HERE/'tools/library_owner_repair_hooks_candidate.py').read_text()
  self.assertIn('@event_priority(-300)\ndef on_post_build',text)
  self.assertNotIn('library_field_freeze_navigation',text)
 def test_static_source_comment_record_is_not_an_article_approval(self):
  before=b'/* old */a{color:blue}';after=b'/* new */a{color:blue}';ledger={'body_edits':[edit('/* old */','/* new */')]}
  d={'review_kind':'source','scope':'bounded-owner-policy-or-comment-inverse','policy':p.POLICY,'path':'assets/manual.css','raw_after_sha256':p.sha(after),'before_source_sha256':p.sha(before),'after_source_sha256':p.sha(after),'approved_exact_bounded_change':True,'exact_forward_reverse_replay':True,'body_edits':ledger['body_edits'],'ordinary_full_article_approval':False,'current_S5_pass':None};raw=json.dumps(d).encode()
  self.assertTrue(validate_static_peer(raw,p.sha(raw),path=d['path'],before=before,after=after,ledger=ledger,kind='source'))
  d['ordinary_full_article_approval']=True;raw=json.dumps(d).encode()
  with self.assertRaises(p.RepairError):validate_static_peer(raw,p.sha(raw),path=d['path'],before=before,after=after,ledger=ledger,kind='source')
 def test_actual_before_read_required_not_archive_only_or_wrong_production(self):
  from test_owner_repair_policy import fixture_plan
  plan,files,_,_=fixture_plan();plan.data['source_changes']={'docs/research/example/index.md':{}};plan.data['baseline_production_binding']={'fixture':'actual-binding'}
  files['research/example/index.html']=b'Existing public HTML'
  d={'approved':True,'reviewer':'root','review_kind':'root-current-owner-repair-before-read','policy':p.POLICY,'production_binding':plan.data['baseline_production_binding'],'sources':{'docs/research/example/index.md':{'public_path':'research/example/index.html','public_before_sha256':p.sha(b'Existing public HTML'),'actually_read':True,'javascript_off_or_raw_source_read':True,'recorded_utc':'2026-11-03T18:00:00Z'}}}
  raw=p.encoded(d);self.assertEqual(1,p.validate_before_read_receipt(raw,p.sha(raw),plan=plan,actual_prior_files=files)['actual_current_before_source_reads'])
  for mode in ['wrong-production','not-read','missing-source','wrong-public-sha']:
   bad=copy.deepcopy(d)
   if mode=='wrong-production':bad['production_binding']={}
   elif mode=='not-read':bad['sources']['docs/research/example/index.md']['actually_read']=False
   elif mode=='missing-source':bad['sources']={}
   else:bad['sources']['docs/research/example/index.md']['public_before_sha256']='0'*64
   raw=p.encoded(bad)
   with self.subTest(mode=mode),self.assertRaises(p.RepairError):p.validate_before_read_receipt(raw,p.sha(raw),plan=plan,actual_prior_files=files)
 def test_mkdocs_candidate_snapshot_waits_for_later_manual_pdf_build(self):
  import zipfile
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);site=root/'site';site.mkdir();work=root/'work';work.mkdir();archive=root/'prior.zip'
   with zipfile.ZipFile(archive,'w') as z:
    z.writestr('absence-manual.pdf',b'Existing PDF fixture');z.writestr('absence-manual-v1.0-2026-08-18.pdf',b'Existing PDF fixture');z.writestr('index.html',b'Existing HTML')
   session=build.OwnerRepairBuildSession.__new__(build.OwnerRepairBuildSession);session.site=site;session.work=work;session.archive=zipfile.ZipFile(archive)
   session.capture_candidate_observations()
   pending=json.loads((work/'pdf-observations.AWAITING_PDF_BUILD.json').read_bytes());self.assertFalse(pending['approval']);self.assertEqual(2,len(pending['paths']))
   self.assertTrue((work/'candidate-public-delta.NOT_APPROVED.json').exists());session.archive.close()


if __name__=='__main__':unittest.main()
