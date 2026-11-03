"""Synthetic accepted45 fixtures only; no actual326 compile or approval."""
from pathlib import Path
import copy,gzip,json,sys,tempfile,unittest
from types import SimpleNamespace
from unittest.mock import patch
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE/'tools'))
import library_publication_field_freeze as field
from library_publication_eligibility import Finite45Eligibility,DEFERRED
from library_publication_overlay import PublicationOverlay,sha,OverlayError,QUALIFIER,run_current_rendered_quality
from library_publication_composition import ComposedPublicationOverlay
from library_publication_release import complete_current_analysis,make_compiled_state,state_fingerprint,incremental_release_gate,require_full_completion
from test_publication_overlay import q

class Fixture:
    def __init__(self,root,count=53):
        self.docs=Path(root)/'docs';self.docs.mkdir();self.records={};self.files={};rows=[];entries=[];self.notes={};self.order=[]
        for i in range(count):
            label=chr(97+i//26)+chr(97+i%26);path='answers/measurement/'+('frozen-' if i<45 else 'eligible-')+str(i)+'.md';title='Distinct'+label+'?';opening=' '.join('lex'+label+chr(97+j//26)+chr(97+j%26) for j in range(30))+'.'
            body='# '+title+'\n\n'+opening+'\n\n'+(QUALIFIER+'\n\n' if i>=45 else '')+'## Explanation\n\n'+('Other'+label+' ')*10+'\n'
            file=self.docs/path;file.parent.mkdir(parents=True,exist_ok=True);file.write_bytes(body.encode());meta={'title':title,'headline':title,'description':'Description'+label,'library_cluster':'measurement'}
            record={'path':path,'body':body,'meta':meta,'cluster':'measurement','review_ids':{'source':None if i<45 else 'source-ok','writing':None if i<45 else 'writing-ok'},'raw_canonical_source_sha256':sha(body.encode()),'effective_canonical_source_sha256':sha(body.encode()),'effective_body_sha256':sha(body.encode()),'effective_meta_sha256':sha(q.canonical_json(meta).encode()),'canonical_source_sha256':sha(body.encode()),'composition_origin':'exact-prior-effective-payload'}
            self.records[path]=record;self.order.append(path);self.notes[path]={'opening_shape':'shape'+str(i%8),'lead_figures':['figure'+label],'source_review_sha256':'source-ok','writing_review_sha256':'writing-ok'}
            html=path[:-3]+'/index.html';self.files[html]=('<article>Fixture '+label+'</article>').encode()
            if i<45:
                url='https://docs.broadcastwell.com/'+path[:-3]+'/';entry='<url><loc>'+url+'</loc><lastmod>2026-11-02</lastmod></url>'
                rows.append({'url':url,'source_path':path,'source_sha256':sha(body.encode()),'active_canonical_sha256':sha(body.encode()),'source_frozen':True,'prose_date_metadata_related_links_navigation_frozen':True,'served_html_path':html,'served_html_sha256':sha(self.files[html])});entries.append({'url':url,'exact_entry':entry,'sha256':sha(entry.encode())})
        hub=self.docs/'answers/measurement/index.md';hub.write_text('# Fixture hub\n\n'+'\n'.join('[Page]('+Path(p).name+')' for p in self.order),encoding='utf-8',newline='\n')
        assets=[]
        for i in range(5):path='assets/synthetic'+str(i)+'.css';self.files[path]=b'fixture';assets.append({'path':path,'sha256':sha(b'fixture')})
        xml=('<urlset>'+''.join(r['exact_entry'] for r in entries)+'</urlset>').encode();self.files['sitemap.xml']=xml;self.files['sitemap.xml.gz']=gzip.compress(xml,mtime=0)
        handoff=Path(root)/'handoff.md';handoff.write_bytes(b'Synthetic accepted45, no activation.');reg=Path(root)/'registry.json';reg.write_bytes(json.dumps({'fixture_only':True,'rows':rows,'presentation_asset_pins':assets,'frozen_sitemap_entries':entries,'frozen_sample_count':45,'activation_authorized':False,'experiment_edits_applied':0,'handoff_sha256':sha(handoff.read_bytes())}).encode())
        self.patcher=patch.object(field,'ROOT_REGISTRY_SHA256',sha(reg.read_bytes()));self.patcher.start();self.guard=field.FieldFreeze(reg,sha(reg.read_bytes()),handoff,sha(handoff.read_bytes()));self.scope=Finite45Eligibility(self.guard,self.docs,self.records)
        self.overlay=SimpleNamespace(records=self.records,docs=self.docs,q=q,s5_scope=self.scope,pending=[],deferred_s5_diagnostics={p:['Prior rule diagnostics deferred, not PASS'] for p in self.scope.frozen},mapping={'pages':{}},leaf_manifest={'pages':{p:{'canonical_source_sha256':r['raw_canonical_source_sha256']} for p,r in self.records.items()}},_merge_plan={},merge_statuses={})
        self.overlay._check_unchanged=lambda:self.scope.assert_current();self.overlay.metadata_consumer_errors=lambda:[];self.overlay._validate_related=lambda *a:None
        def receipt(digest,record,kind):
            if record['path'] in self.scope.frozen:raise AssertionError('Frozen article demanded fresh current receipt')
            return digest==kind+'-ok'
        self.overlay._article_receipt=receipt
        self.binding={'commit_sha':'a'*40,'deployment_id':'fixture-only','artifact_sha256':'b'*64,'served_receipt_sha256':'c'*64}
        self.artifacts={'/'+p[:-3]+'/':self.files[p[:-3]+'/index.html'] for p in self.records}
        self.state=make_compiled_state(self.overlay,built_route_artifacts=self.artifacts,redirects={},production_binding=self.binding);self.prior=copy.deepcopy(self.state);self.overlay.prior=self.prior
        self.refs={'records':[{'title':'Unusedreference'+str(i),'url':'https://example.test/'+str(i)} for i in range(140)]};self.refs_sha=sha(q.canonical_json(self.refs).encode())
    def close(self):self.patcher.stop()
    def analyze(self):
        with patch('library_publication_release.validate_current_annotations',return_value=(copy.deepcopy(self.notes),{})):
            return complete_current_analysis(self.overlay,self.state,current_annotations={'index_question_titles':self.refs},trusted_index_references_sha256=self.refs_sha)
    def gate(self,report):
        previous_report=copy.deepcopy(report);self.prior['current_quality_snapshot']=previous_report
        # Current and previous article/raw inventories are identical in this unit fixture.
        target=self.docs.parent/'prior.json';target.write_bytes((q.canonical_json(self.prior)+'\n').encode())
        return incremental_release_gate(previous_manifest_path=target,trusted_previous_sha256=sha(target.read_bytes()),actual_prior_production_binding=self.binding,candidate_state=self.state,actual_candidate_state=self.state,authorized_change_map={},full_current_report=report,q=q,s5_scope=self.scope)

class Finite45Tests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.f=Fixture(self.tmp.name);self.addCleanup(self.f.close)
    def test_eligible_completion_passes_without_frozen_false_PASS(self):
        self.f.scope.certify_artifacts(self.f.files);r=self.f.analyze();self.assertTrue(r['eligible_current_passed']);self.assertFalse(r['passed']);self.assertTrue(r['eligible_completion_passed']);self.assertEqual(45,r['s5_scope']['deferred_count']);self.assertEqual(8,r['s5_scope']['eligible_count'])
        for p in self.f.scope.frozen:self.assertEqual(DEFERRED,r['page_readiness'][p]['status']);self.assertIsNone(r['page_readiness'][p]['passed'])
        result=self.f.gate(r);self.assertFalse(result['full_current_passed']);self.assertTrue(result['final_completion_marker_allowed']);require_full_completion(result,s5_scope=self.f.scope)
    def test_eligible_missing_source_writing_or_layout_still_blocks(self):
        self.f.scope.certify_artifacts(self.f.files);p=next(iter(set(self.f.records)-self.f.scope.frozen));self.f.records[p]['review_ids']['source']='missing';r=self.f.analyze();self.assertFalse(r['eligible_current_passed']);self.assertFalse(self.f.gate(r)['final_completion_marker_allowed'])
        self.f.records[p]['review_ids']['source']='source-ok';self.f.overlay.pending=[p+': Layout read remains pending'];r=self.f.analyze();self.assertFalse(r['eligible_current_passed'])
    def test_preservation_is_required_for_every_release_not_just_final(self):
        r=self.f.analyze();self.assertTrue(r['eligible_current_passed']);self.assertFalse(r['eligible_completion_passed']);result=self.f.gate(r);self.assertFalse(result['incremental_release_passed']);self.assertFalse(result['final_completion_marker_allowed'])
    def test_frozen_false_PASS_or_eligible_deferral_is_rejected(self):
        self.f.scope.certify_artifacts(self.f.files);r=self.f.analyze();p=next(iter(self.f.scope.frozen));r['page_readiness'][p]['status']='PASS';r['page_readiness'][p]['passed']=True
        with self.assertRaisesRegex(OverlayError,'Frozen article cannot'):self.f.gate(r)
        r=self.f.analyze();p=next(iter(set(self.f.records)-self.f.scope.frozen));r['page_readiness'][p]['status']=DEFERRED;r['page_readiness'][p]['passed']=None
        with self.assertRaisesRegex(OverlayError,'Eligible article cannot'):self.f.gate(r)
    def test_frozen_only_quality_violation_defers_but_mixed_violation_fails_eligible(self):
        self.f.scope.certify_artifacts(self.f.files);frozen=list(self.f.scope.frozen);self.f.notes[frozen[1]]['lead_figures']=self.f.notes[frozen[0]]['lead_figures'];self.f.notes[frozen[2]]['lead_figures']=self.f.notes[frozen[0]]['lead_figures'];self.f.notes[frozen[3]]['lead_figures']=self.f.notes[frozen[0]]['lead_figures'];r=self.f.analyze();self.assertTrue(r['eligible_current_passed']);self.assertTrue(r['deferred_frozen_only_violations'])
        p=next(iter(set(self.f.records)-self.f.scope.frozen));self.f.notes[p]['lead_figures']=self.f.notes[frozen[0]]['lead_figures'];r=self.f.analyze();self.assertFalse(r['eligible_current_passed']);self.assertTrue(r['eligible_blocking_violations']);self.assertFalse(r['page_readiness'][p]['passed'])
    def test_wrong_source_off_registry_and_missing45th_fail(self):
        p=next(iter(self.f.scope.frozen));self.f.records[p]['raw_canonical_source_sha256']='0'*64
        with self.assertRaisesRegex(OverlayError,'accepted source/prior origin'):self.f.scope.validate_records(self.f.records)
        with self.assertRaisesRegex(OverlayError,'hides frozen'):self.f.scope.partition(set(self.f.records)-{p})
        with patch.object(field,'ROOT_REGISTRY_SHA256','0'*64):
            with self.assertRaisesRegex(OverlayError,'exact accepted Root'):Finite45Eligibility(self.f.guard,self.f.docs,self.f.records)
    def test_no_arbitrary_skiplist_and_no_sample_revision(self):
        self.f.overlay.s5_scope={'skip':list(self.f.scope.frozen)}
        with self.assertRaisesRegex(OverlayError,'skiplist'):self.f.analyze()
        with self.assertRaisesRegex(OverlayError,'active S5 revision'):self.f.scope.reject_active([next(iter(self.f.scope.frozen))])
    def test_frozen_output_mutation_invalidates_preservation(self):
        self.f.scope.certify_artifacts(self.f.files);bad=copy.deepcopy(self.f.files);path=self.f.scope.rows[next(iter(self.f.scope.frozen))]['served_html_path'];bad[path]+=b'changed'
        with self.assertRaisesRegex(OverlayError,'Frozen served HTML'):self.f.scope.certify_artifacts(bad)
        self.assertFalse(self.f.scope.preservation_passed)
    def test_composition_defers_only_its_explicit_frozen_S5_bucket(self):
        overlay=ComposedPublicationOverlay();overlay.s5_scope=self.f.scope;overlay.pending=[];overlay.deferred_s5_diagnostics={};p=next(iter(self.f.scope.frozen));e=next(iter(set(self.f.records)-self.f.scope.frozen));overlay._s5_issue(p,'Known current footer defect');overlay._s5_issue(e,'Layout pending')
        self.assertFalse(any(x.startswith(p+':') for x in overlay.pending));self.assertEqual([e+': Layout pending'],overlay.pending);self.assertIn(p,overlay.deferred_s5_diagnostics)
        self.f.overlay.pending=[p+': Frozen served content would change'];r=self.f.analyze();self.assertFalse(r['eligible_current_passed']);self.assertTrue(r['global_fatal_errors'])
    def test_default_scoped_quality_uses_same_gate_and_keeps_global_PASS_false(self):
        self.f.scope.certify_artifacts(self.f.files)
        with patch('library_publication_release.validate_current_annotations',return_value=(self.f.notes,{})):
            r=run_current_rendered_quality(self.f.overlay,current_annotations={'index_question_titles':self.f.refs},trusted_index_references_sha256=self.f.refs_sha)
        self.assertFalse(r['passed']);self.assertFalse(self.f.overlay._strict_current_passed);self.assertTrue(self.f.overlay._eligible_current_passed)
    def test_dynamic_300_and326_and_merge_counts_derive_from_actual_universe(self):
        with tempfile.TemporaryDirectory() as t:
            f=Fixture(t,count=326)
            try:
                original=list(f.records);d=f.scope.description(original[:300],original[:300]);self.assertEqual((255,45),(d['eligible_count'],d['deferred_count']))
                d=f.scope.description(original,original[:300]);self.assertEqual((300,255,326,281),(d['actual_published_article_count'],d['actual_published_eligible_count'],d['candidate_effective_article_count'],d['eligible_count']))
                self.assertEqual(280,f.scope.description(original[:-1],original[:300])['eligible_count'])
            finally:f.close()
    def test_hook_final_capture_follows_adopted_minus200_processor(self):
        source=(HERE/'tools/library_publication_hooks_candidate.py').read_text(encoding='utf-8');self.assertIn('@event_priority(-300)\ndef on_post_build',source)
    def test_bound_registry_cannot_be_mutated_into_a_general_skiplist(self):
        self.f.guard.data['rows'][0]['source_sha256']='0'*64
        with self.assertRaisesRegex(OverlayError,'data changed after binding'):self.f.scope.assert_current()
    def test_scoped_final_and_report_cannot_claim_global_PASS_or_wrong_count(self):
        self.f.scope.certify_artifacts(self.f.files);r=self.f.analyze();bad=copy.deepcopy(r);bad['s5_scope']['eligible_count']-=1
        with self.assertRaisesRegex(OverlayError,'off-registry'):self.f.gate(bad)
        bad=copy.deepcopy(r);bad['passed']=True
        with self.assertRaisesRegex(OverlayError,'global PASS'):self.f.gate(bad)
        result=self.f.gate(r)
        with self.assertRaisesRegex(OverlayError,'exact accepted finite45 authority'):require_full_completion(result)
    def test_default_publication_api_uses_explicit_eligible_completion_not_false_global_PASS(self):
        self.f.scope.certify_artifacts(self.f.files);r=self.f.analyze();self.assertTrue(r['eligible_completion_passed']);self.assertFalse(self.f.overlay._strict_current_passed)
        p=next(iter(set(self.f.records)-self.f.scope.frozen));record=self.f.records[p];record['post_finite94_body_sha256']=sha(record['body'].encode())
        self.assertEqual(record['body'],PublicationOverlay.transform_after_finite94(self.f.overlay,p,record['body']))
        self.f.overlay._eligible_current_passed=False
        with self.assertRaisesRegex(OverlayError,'Eligible current/frozen-preservation'):PublicationOverlay.transform_after_finite94(self.f.overlay,p,record['body'])

if __name__=='__main__':unittest.main()
