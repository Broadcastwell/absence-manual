"""Synthetic fixtures only; no real307 producer or approval is created."""
import copy,json,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import library_owner_repair as p
import library_owner_repair_post_s5 as x
from library_owner_repair_consumers import json_hash,validate_peer
from library_publication_canonical_stub import POLICY,STATUS,OWNER_QUOTE_SHA256,render_canonical_stub,stub_artifact_path
from library_publication_release import route_for
from library_publication_overlay import PublicationOverlay

def raw(d):return json.dumps(d,sort_keys=True,separators=(',',':')).encode()

def fixture():
    paths=['answers/x/p'+str(i)+'.md' for i in range(306)]+[x.LEGAL]
    retired=['answers/x/retired'+str(i)+'.md' for i in range(19)]
    frozen=set(paths[:45]);rows={path:{'status':'DEFERRED_FIELD_TEST' if path in frozen else 'FAIL','passed':None if path in frozen else False} for path in paths}
    rows[x.LEGAL]={'status':'PASS','passed':True}
    quality={'analysis_completed':True,'baseline_exceptions':0,'pair_count':46971,'page_readiness':rows,'global_fatal_errors':[],
      'comparison_scopes':{k:{'all_pairs_compared':True,'pair_count':46971,'violations':[]} for k in ['literal','runtime']}}
    stubs={};decisions={};files={}
    for source in retired:
        row={'policy':POLICY,'status':STATUS,'article_pass':False,'owner_quote_sha256':OWNER_QUOTE_SHA256,
             'source_canonical_sha256':'a'*64,'target_path':paths[-1],'target_title':'Current fixture question','meta_refresh_seconds':None}
        row['stub_html_sha256']=p.sha(render_canonical_stub(source,row))
        d={**row,'approved':True,'review_kind':'reviewed-source-fit-canonical-stub','source_fit_status':STATUS,'source_path':source}
        key=p.sha(raw(d));decisions[key]=d;row['decision_receipt_sha256']=key;stubs[source]=row
        files[stub_artifact_path(source)]=render_canonical_stub(source,row)
    files[stub_artifact_path(paths[-1])]=('<html><link rel="canonical" href="https://docs.broadcastwell.com'+route_for(paths[-1])+'"></html>').encode()
    binding={'commit_sha':'1'*40,'deployment_id':'fixture-only','artifact_sha256':'2'*64,'served_receipt_sha256':'3'*64}
    prior={'production_binding':binding,'merged_sources':stubs,'raw_source_pins':{k:'a'*64 for k in paths+retired},'current_quality_snapshot':quality}
    payload={'pages':{k:{} for k in paths}};leaves={'pages':{k:{} for k in paths+retired}};merges={'merges':{}}
    inputs={k:{'sha256':p.sha(k.encode())} for k in ['prior_state','prior_payload','prior_hub_payload','current_leaf_manifest','merges']}
    producer=raw({'approved':True,'review_kind':'prior-production-effective-payload','actual_served_readback':True,'source_render_equality_passed':True,'hub_source_render_equality_passed':True,'production_binding':binding,'payload_bundle_sha256':inputs['prior_payload']['sha256'],'hub_payload_bundle_sha256':inputs['prior_hub_payload']['sha256']})
    context={'schema_version':1,'approved':True,'reviewer':'root','review_kind':'root-exact-post-small-S5-owner-context','article_count':307,'raw_article_count':326,'inherited_stub_count':19,'production_receipt_sha256':p.sha(producer),'production_binding':binding,'input_sha256':{k:v['sha256'] for k,v in inputs.items()},'inherited_dispositions_sha256':json_hash(stubs)}
    context['input_object_sha256']={k:json_hash(value) for k,value in [('prior_state',prior),('prior_payload',payload),('current_leaf_manifest',leaves),('merges',merges)]}
    values=dict(producer_raw=producer,prior=prior,payload=payload,leaves=leaves,new_merges=merges,input_files=inputs,actual_binding=binding)
    overlay=SimpleNamespace(records=payload['pages'],merge_statuses=stubs,_check_unchanged=lambda:None,_load_receipt=lambda key:decisions.get(key))
    return context,values,overlay,files,frozen,decisions

def bind(context,values):return x.bind_post_s5(raw(context),p.sha(raw(context)),**values)

class PostS5ContractTests(unittest.TestCase):
    def test_exact_future_fixture_binds307_326_19_without_actual_claim(self):
        c,v,o,f,_,_=fixture();b=bind(c,v)
        self.assertEqual(307,len(b.pages));self.assertEqual(19,len(b.stubs))
        r=x.validate_inherited_closure(o,b,f);self.assertIsNone(r['actual_http_status_observed']);self.assertFalse(r['HTTP301_claim'])
    def test_wrong_counts_never_use_actual326_or308_as307(self):
        for field,value in [('article_count',326),('article_count',308),('raw_article_count',307),('inherited_stub_count',18)]:
            c,v,*_=fixture();c[field]=value
            with self.subTest(field=field,value=value),self.assertRaises(p.RepairError):bind(c,v)
    def test_unapproved_partial_or_false_context_rejects(self):
        for field,value in [('approved',False),('reviewer','source'),('schema_version',2),('review_kind','generic')]:
            c,v,*_=fixture();c[field]=value
            with self.subTest(field=field),self.assertRaises(p.RepairError):bind(c,v)
    def test_context_hash_must_match_actual_bytes(self):
        c,v,*_=fixture()
        with self.assertRaises(p.RepairError):x.bind_post_s5(raw(c),'0'*64,**v)
    def test_real_producer_fields_must_each_be_approved(self):
        for key in ['approved','actual_served_readback','source_render_equality_passed','hub_source_render_equality_passed']:
            c,v,*_=fixture();d=json.loads(v['producer_raw']);d[key]=False;v['producer_raw']=raw(d);c['production_receipt_sha256']=p.sha(v['producer_raw'])
            with self.subTest(key=key),self.assertRaises(p.RepairError):bind(c,v)
    def test_producer_or_binding_or_any_input_hash_mismatch_rejects(self):
        c,v,*_=fixture();c['production_receipt_sha256']='0'*64
        with self.assertRaises(p.RepairError):bind(c,v)
        for key in list(c['input_sha256']):
            c,v,*_=fixture();c['input_sha256'][key]='0'*64
            with self.subTest(key=key),self.assertRaises(p.RepairError):bind(c,v)
        c,v,*_=fixture();v['actual_binding']={**v['actual_binding'],'deployment_id':'other'}
        with self.assertRaises(p.RepairError):bind(c,v)
    def test_raw_or_effective_omission_and_new_merge_reject(self):
        for name in ['payload','leaves']:
            c,v,*_=fixture();v[name]['pages'].pop(next(iter(v[name]['pages'])))
            with self.subTest(name=name),self.assertRaises(p.RepairError):bind(c,v)
        c,v,*_=fixture();v['new_merges']={'merges':{'answers/x/new.md':{}}}
        with self.assertRaises(p.RepairError):bind(c,v)
    def test_whole_prior_both_scopes_and_frozen_falsepass_reject(self):
        for scope in ['literal','runtime']:
            c,v,*_=fixture();v['prior']['current_quality_snapshot']['comparison_scopes'][scope]['pair_count']=52975
            with self.subTest(scope=scope),self.assertRaises(p.RepairError):bind(c,v)
        c,v,_,_,f,_=fixture();v['prior']['current_quality_snapshot']['page_readiness'][next(iter(f))]['passed']=True
        with self.assertRaises(p.RepairError):bind(c,v)
    def test_sealed_binding_detects_mutation(self):
        c,v,*_=fixture();b=bind(c,v);b.stubs.clear()
        with self.assertRaises(p.RepairError):b.check()
    def test_coherently_tampered_object_with_old_file_hash_rejects(self):
        c,v,*_=fixture();v['prior']['raw_source_pins'][next(iter(v['prior']['raw_source_pins']))]='0'*64
        with self.assertRaisesRegex(p.RepairError,'bound input object'):bind(c,v)
    def test_missing_semantic_object_pin_rejects(self):
        c,v,*_=fixture();del c['input_object_sha256']['prior_payload']
        with self.assertRaisesRegex(p.RepairError,'bound input object'):bind(c,v)
    def test_original_inherited_receipt_closure_missing_or_unapproved_rejects(self):
        for missing in [True,False]:
            c,v,o,f,_,d=fixture();b=bind(c,v);key=next(iter(d))
            if missing:d.pop(key)
            else:d[key]['approved']=False
            with self.subTest(missing=missing),self.assertRaises(p.RepairError):x.validate_inherited_closure(o,b,f)
    def test_tampered_stub_or_target_reroute_or_chain_rejects(self):
        c,v,o,f,_,_=fixture();b=bind(c,v);f[next(k for k in f if 'retired' in k)]+=b' '
        with self.assertRaises(ValueError):x.validate_inherited_closure(o,b,f)
        c,v,o,f,_,_=fixture();b=bind(c,v);f[stub_artifact_path(x.LEGAL)]=b'<link rel="canonical" href="https://other.example/">'
        with self.assertRaises(p.RepairError):x.validate_inherited_closure(o,b,f)
    def test_old_target_fullhash_is_not_falsely_required_after_valid_revision(self):
        c,v,o,f,_,d=fixture();b=bind(c,v)
        for decision in d.values():decision['target_effective_canonical_sha256']='0'*64
        self.assertEqual(19,x.validate_inherited_closure(o,b,f)['inherited_stubs'])
    def test_post_quality_retains_real_fail_and_all_prior_pass(self):
        c,v,_,_,f,_=fixture();b=bind(c,v);before=v['prior']['current_quality_snapshot'];after=copy.deepcopy(before)
        out=x.validate_post_quality(before,after,changed_content_paths={x.LEGAL},frozen_paths=f,binding=b)
        self.assertEqual(261,out['actual_current_FAIL_rows_retained']);self.assertFalse(out['S5_full_PASS_granted'])
    def test_post_quality_regression_and_new_literal_only_violation_reject(self):
        c,v,_,_,f,_=fixture();b=bind(c,v);before=v['prior']['current_quality_snapshot'];after=copy.deepcopy(before);after['page_readiness'][x.LEGAL]={'status':'FAIL','passed':False}
        with self.assertRaises(p.RepairError):x.validate_post_quality(before,after,changed_content_paths={x.LEGAL},frozen_paths=f,binding=b)
        after=copy.deepcopy(before);after['comparison_scopes']['literal']['violations']=[{'key':'new','kind':'six_word_similarity','pages':list(b.pages-f)[:2],'score_fraction':'21/100'}]
        with self.assertRaises(p.RepairError):x.validate_post_quality(before,after,changed_content_paths=set(),frozen_paths=f,binding=b)
    def test_arbitrary307_count_without_bound_context_rejects(self):
        c,v,_,_,f,_=fixture();r=v['prior']['current_quality_snapshot']
        with self.assertRaises(p.RepairError):p.validate_quality_transition(r,r,changed_content_paths=set(),frozen_paths=f)


class LegalPeerTests(unittest.TestCase):
    def fixture(self):
        r={'path':x.LEGAL,'raw_canonical_source_sha256':'a'*64,'effective_canonical_source_sha256':'b'*64,'effective_full_source':'full','body':'body','meta':{},'before_effective_canonical_source_sha256':'c'*64}
        store={};ids={}
        for kind in ['source','writing']:
            d={'approved':True,'actual_full_read_complete':True,'review_kind':kind,'scope':'full-effective-article','path':x.LEGAL,'canonical_source_sha256':'a'*64,'effective_canonical_source_sha256':'b'*64}
            key=p.sha(raw(d));store[key]=d;ids[kind]=key
        overlay=SimpleNamespace(_load_receipt=lambda key:store.get(key))
        overlay._article_receipt=lambda key,record,kind:PublicationOverlay._article_receipt(overlay,key,record,kind)
        r['review_ids']=ids
        return r,overlay,store,ids
    def test_real_owning_article_receipt_requires_separate_full_legal_peers(self):
        r,o,_,ids=self.fixture();self.assertTrue(x.validate_legal_ordinary(o,r,ids,{'passed':True,'status':'PASS'}))
    def test_scoped_receipts_cannot_replace_ordinary_or_use_wrong_body_full_pin(self):
        for field,value in [('scope','owner-exact-repair-changes'),('effective_canonical_source_sha256','0'*64),('path','answers/x/other.md'),('actual_full_read_complete',False)]:
            r,o,store,ids=self.fixture();store[ids['source']][field]=value
            with self.subTest(field=field),self.assertRaises(p.RepairError):x.validate_legal_ordinary(o,r,ids,{'passed':True,'status':'PASS'})
    def test_no_generic_priorpass_or_false_priorpass_allowance(self):
        r,o,_,ids=self.fixture()
        with self.assertRaises(p.RepairError):x.validate_legal_ordinary(o,r,ids,{'passed':False,'status':'FAIL'})
        r['path']='answers/x/other.md'
        with self.assertRaises(p.RepairError):x.validate_legal_ordinary(o,r,ids,{'passed':True,'status':'PASS'})
    def test_legal_scoped_currentpass_null_is_not_ordinary_pass(self):
        r,_,_,_=self.fixture();d={'approved':True,'current_full_file_actually_read':True,'review_kind':'source','scope':'owner-exact-repair-changes','policy':p.POLICY,'approved_exact_repair_changes':True,'preserved_facts':True,'repair_change_ledger_sha256':'d'*64,'remaining_prior_S5_defects':[],'current_S5_pass':None,'ordinary_full_article_approval':False,'path':x.LEGAL,'canonical_source_sha256':r['raw_canonical_source_sha256'],'before_effective_canonical_source_sha256':r['before_effective_canonical_source_sha256'],'effective_canonical_source_sha256':p.sha(b'full'),'effective_body_sha256':p.sha(b'body'),'effective_meta_sha256':json_hash({})}
        self.assertTrue(validate_peer(raw(d),p.sha(raw(d)),r,'source','d'*64,prior_S5_pass=True))
        for field,value in [('current_S5_pass',True),('ordinary_full_article_approval',True),('remaining_prior_S5_defects',['A known failure'])]:
            bad={**d,field:value}
            with self.subTest(field=field),self.assertRaises(p.RepairError):validate_peer(raw(bad),p.sha(raw(bad)),r,'source','d'*64,prior_S5_pass=True)


class FiniteTrimTests(unittest.TestCase):
    def test_actual_production_constants_bind_exact_root_v7_scope(self):
        self.assertEqual('6ee84ad5db688ee2664b27d724d8d8e58cb26b5e379fa7bfeb08a620dd160db9',x.TRIM_SHA)
        self.assertEqual('d2474b7a10aacc6fd398d04af6d73626a972e01ddbba1c3ab0954b25631994dc',x.CUMULATIVE_SHA)
    def fixture(self):
        oldbody='A old.\n\nB old.\n\nC old.\n\nD old.';body=oldbody.replace('old.','new.')
        meta={'date_modified':'2026-11-03T21:07:36+00:00','updated':'2026-11-03T21:07:36+00:00'};oldmeta={k:'2026-11-03T17:50:50+00:00' for k in meta}
        full=json.dumps(meta)+'\n'+body;oldfull=json.dumps(oldmeta)+'\n'+oldbody
        edits=[{'old':a+' old.','new':a+' new.','old_sha256':p.sha((a+' old.').encode()),'new_sha256':p.sha((a+' new.').encode())} for a in 'ABCD']
        ledger={'path':x.INFO,'before_effective_canonical_sha256':p.sha(oldfull.encode()),'after_effective_canonical_sha256':p.sha(full.encode()),'body_edits':edits,'metadata_delta':{k:{'old':oldmeta[k],'new':meta[k]} for k in meta}}
        cumulative={**ledger,'synthetic_cumulative':True};r={'path':x.INFO,'body':body,'meta':meta,'effective_full_source':full}
        def parse(t):a,b=t.split('\n',1);return json.loads(a),b
        return r,raw(ledger),raw(cumulative),oldfull,parse
    def test_four_literal_forward_inverse_fixture(self):
        r,t,c,old,parse=self.fixture()
        with patch.multiple(x,TRIM_SHA=p.sha(t),CUMULATIVE_SHA=p.sha(c),INFO_AFTER=p.sha(r['effective_full_source'].encode())):
            self.assertTrue(x.validate_info_trim(r,trim_raw=t,cumulative_raw=c,pretrim_full=old,source_parser=parse,actual_ledger_raw=c)['four_spans_inverse_exact'])
    def test_wrong_ledger_source_body_or_general_prose_rejects(self):
        r,t,c,old,parse=self.fixture()
        with self.assertRaises(p.RepairError):x.validate_info_trim(r,trim_raw=t,cumulative_raw=c,pretrim_full=old,source_parser=parse,actual_ledger_raw=c)
        with patch.multiple(x,TRIM_SHA=p.sha(t),CUMULATIVE_SHA=p.sha(c),INFO_AFTER=p.sha(r['effective_full_source'].encode())):
            for kwargs in [dict(trim_raw=t+b' '),dict(pretrim_full=old+' '),dict(actual_ledger_raw=t)]:
                args=dict(trim_raw=t,cumulative_raw=c,pretrim_full=old,source_parser=parse,actual_ledger_raw=c);args.update(kwargs)
                with self.subTest(kwargs=list(kwargs)),self.assertRaises(p.RepairError):x.validate_info_trim(r,**args)
            r['body']+=' unreviewed prose'
            with self.assertRaises(p.RepairError):x.validate_info_trim(r,trim_raw=t,cumulative_raw=c,pretrim_full=old,source_parser=parse,actual_ledger_raw=c)


if __name__=='__main__':unittest.main()
