"""Synthetic owner-policy tests; no real approval, route or network request."""
import copy,json,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from library_publication_overlay import PublicationOverlay,OverlayError,sha
from library_publication_release import route_for,make_compiled_state,state_fingerprint
from library_publication_canonical_stub import *
from test_publication_overlay import q,encoded
from test_publication_release import StateFixture
from library_publication_consumers import compare_complete_artifacts


class StubFixture:
    def __init__(self,directory):
        self.docs=Path(directory);self.source='answers/measurement/old.md';self.target='answers/measurement/new.md'
        p=self.docs/self.source;p.parent.mkdir(parents=True);p.write_text('A dated source observation.\n',encoding='utf-8')
        self.base=PublicationOverlay();self.base.docs=self.docs;self.base.q=q;self.base.pending=[];self.base.metadata_consumers={};self.base.receipt_store={}
        full='# New question?\n\nA dated source observation.\n\nOld question?\n'
        self.record={'path':self.target,'raw_canonical_source_sha256':'b'*64,'effective_canonical_source_sha256':sha(full.encode()),'body':full,'meta':{'title':'New question?','also_asked_as':['Old question?']},'review_ids':{}}
        for kind in ['source','writing']:
            r={'fixture_only':True,'approved':True,'actual_full_read_complete':True,'review_kind':kind,'scope':'full-effective-article','path':self.target,'canonical_source_sha256':'b'*64,'effective_canonical_source_sha256':sha(full.encode())};self.record['review_ids'][kind]=self.store(r)
        self.base.records={self.source:{'raw_canonical_source_sha256':'a'*64},self.target:self.record}
        span='A dated source observation.'
        facts=[{'id':'synthetic-fact','source_span':span,'target_span':span,'source_span_sha256':sha(span.encode()),'target_span_sha256':sha(span.encode())}]
        self.row={'target_path':self.target,'source_canonical_sha256':'a'*64,'target_canonical_sha256':'b'*64,'target_effective_canonical_sha256':sha(full.encode()),'preserved_fact_bindings':facts,'required_fact_ids':['synthetic-fact'],'required_aliases':['Old question?'],'meta_refresh_seconds':None}
        disposition={'target_path':self.target,'target_title':'New question?','policy':POLICY,'owner_quote_sha256':OWNER_QUOTE_SHA256,'meta_refresh_seconds':None}
        self.decision={'fixture_only':True,'approved':True,'review_kind':'reviewed-source-fit-canonical-stub','source_path':self.source,'target_path':self.target,'source_fit_status':STATUS,'source_canonical_sha256':'a'*64,'target_effective_canonical_sha256':sha(full.encode()),'owner_quote_sha256':OWNER_QUOTE_SHA256,'required_fact_ids':['synthetic-fact'],'preserved_fact_bindings_sha256':sha(q.canonical_json(facts).encode()),'required_aliases':['Old question?'],'meta_refresh_seconds':None,'stub_html_sha256':sha(render_canonical_stub(self.source,disposition))}
        self.plan={'schema_version':1,'approved':True,'routing_policy':POLICY,'owner_quote':OWNER_QUOTE,'owner_quote_sha256':OWNER_QUOTE_SHA256,'merges':{self.source:self.row}}
    def store(self,r):
        raw=encoded(r);h=sha(raw);self.base.receipt_store[h]=raw;return h
    def apply(self):
        self.row['decision_receipt_sha256']=self.store(self.decision);p=self.docs/'plan.json';p.write_bytes(encoded(self.plan))
        return apply_reviewed_canonical_stubs(self.base,p,sha(p.read_bytes()),hub_orders={'measurement':[self.target]})


class CanonicalStubTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.fx=StubFixture(self.tmp.name)
    def test_default_visible_link_canonical_no_javascript_no_refresh_no_301(self):
        overlay=self.fx.apply();row=overlay.merge_statuses[self.fx.source];raw=render_canonical_stub(self.fx.source,row)
        proof=validate_canonical_stub_bytes(self.fx.source,row,raw)
        self.assertIn(b'<link rel="canonical" href="https://docs.broadcastwell.com/answers/measurement/new/">',raw)
        self.assertIn(b'<a href="https://docs.broadcastwell.com/answers/measurement/new/">New question?</a>',raw)
        self.assertNotIn(b'<script',raw);self.assertNotIn(b'refresh',raw);self.assertIsNone(proof['http_status_observed']);self.assertFalse(proof['live_http_301_verified'])
        self.assertNotIn(self.fx.source,overlay.records);self.assertFalse(row['article_pass']);self.assertEqual(STATUS,row['status']);self.assertTrue((self.fx.docs/self.fx.source).exists())
    def test_owner_quote_and_policy_cannot_be_substituted(self):
        self.fx.plan['owner_quote']='A fabricated broader permission.'
        with self.assertRaisesRegex(OverlayError,'owner policy'):self.fx.apply()
    def test_frozen_source_or_target_cannot_be_selected(self):
        for path in [self.fx.source,self.fx.target]:
            self.fx.base.s5_scope=SimpleNamespace(frozen={path})
            with self.subTest(path=path),self.assertRaisesRegex(OverlayError,'Frozen'):self.fx.apply()
    def test_missing_fact_or_alias_is_not_a_content_preserving_merge(self):
        self.fx.record['body']='# New question?\nOld question?\n'
        with self.assertRaisesRegex(OverlayError,'source fact'):self.fx.apply()
        self.fx.record['body']='# New question?\nA dated source observation.\n'
        with self.assertRaisesRegex(OverlayError,'aliases missing'):self.fx.apply()
    def test_target_requires_actual_current_full_body_review(self):
        self.fx.record['review_ids']['writing']=None
        with self.assertRaisesRegex(OverlayError,'current writing approval'):self.fx.apply()
    def test_meta_refresh_not_added_without_exact_decision_binding(self):
        self.fx.row['meta_refresh_seconds']=0
        with self.assertRaisesRegex(OverlayError,'decision missing or stale'):self.fx.apply()
    def test_target_body_and_stub_bytes_cannot_change_after_decision(self):
        self.fx.row['target_effective_canonical_sha256']='d'*64
        with self.assertRaisesRegex(OverlayError,'body pins differ'):self.fx.apply()
        self.fx.row['target_effective_canonical_sha256']=self.fx.record['effective_canonical_source_sha256'];self.fx.decision['stub_html_sha256']='e'*64
        with self.assertRaisesRegex(OverlayError,'exact generated bytes'):self.fx.apply()
    def test_stub_source_cannot_chain_to_retired_target(self):
        self.fx.base.merge_statuses={'answers/measurement/prior.md':{'target_path':self.fx.source}}
        with self.assertRaisesRegex(OverlayError,'chain/cycle'):self.fx.apply()
    def test_existing_rules_preserved_and_overlap_rejected(self):
        overlay=self.fx.apply();existing=b'/old /new 301\n'
        self.assertEqual(existing,validate_existing_routing(existing,overlay.merge_statuses))
        with self.assertRaisesRegex(OverlayError,'overlaps'):validate_existing_routing(b'/answers/* /other 302\n',overlay.merge_statuses)
    def test_wrong_html_extra_refresh_or_hidden_target_rejected(self):
        overlay=self.fx.apply();row=overlay.merge_statuses[self.fx.source];raw=render_canonical_stub(self.fx.source,row)
        for changed in [raw+b'X',raw.replace(b'<p>',b'<p hidden>'),raw.replace(b'</head>',b'<meta http-equiv="refresh" content="0"></head>')]:
            with self.assertRaisesRegex(OverlayError,'reviewed bytes'):validate_canonical_stub_bytes(self.fx.source,row,changed)
    def test_static_artifacts_never_pass_live_readback(self):
        overlay=self.fx.apply()
        with self.assertRaisesRegex(OverlayError,'Actual Root'):validate_live_stub_readback(overlay,{'approved':False},{'production_binding':{'commit_sha':'x'}})
    def test_actual_bound_stub200_target200_readback_cannot_waive_failed_quality(self):
        overlay=self.fx.apply();source,target=self.fx.source,self.fx.target;row=overlay.merge_statuses[source]
        state={'routes':{route_for(source):{'kind':'canonical_stub','source_path':source,'target':route_for(target),'compiled_sha256':row['stub_html_sha256']},route_for(target):{'kind':'article','path':target,'compiled_sha256':'f'*64}},'raw_source_pins':{source:'a'*64,target:'b'*64},'production_binding':{'commit_sha':'c'*40,'deployment_id':'synthetic-only','artifact_sha256':'d'*64,'served_receipt_sha256':'e'*64}}
        receipt={'fixture_only':True,'approved':True,'review_kind':'canonical-stub-live-readback','production_binding':state['production_binding'],'actual_root_read_complete':True,'compiled_collection_fingerprint':state_fingerprint(state,q),'source_fit_dispositions_sha256':sha(q.canonical_json(overlay.merge_statuses).encode()),'rows':{source:{'stub_url':SITE+route_for(source),'stub_status':200,'stub_final_url':SITE+route_for(source),'stub_html_sha256':row['stub_html_sha256'],'canonical_href':SITE+route_for(target),'target_url':SITE+route_for(target),'target_status':200,'target_final_url':SITE+route_for(target),'target_effective_canonical_sha256':self.fx.record['effective_canonical_source_sha256'],'target_html_sha256':'f'*64,'meta_refresh_seconds':None}}}
        proof=validate_live_stub_readback(overlay,receipt,state);self.assertTrue(proof['live_stub_readback_verified']);self.assertFalse(proof['live_http_301_verified'])
        result={'canonical_stub_live_readback_required':True,'incremental_release_passed':True,'candidate_collection_fingerprint':state_fingerprint(state,q),'eligible_completion_passed':False,'errors':[]}
        final=attach_root_live_readback(result,overlay,receipt,state);self.assertTrue(final['live_stub_readback_verified']);self.assertFalse(final['final_completion_marker_allowed'])
        receipt['rows'][source]['target_status']=301
        with self.assertRaisesRegex(OverlayError,'stub200/canonical/target200'):validate_live_stub_readback(overlay,receipt,state)
    def test_real_stub_route_is_counted_with_coupled_target_and_final_waits_live_readback(self):
        fx=StateFixture(self.tmp.name);source,target=fx.paths[-1],fx.paths[0]
        row={'status':STATUS,'article_pass':False,'target_path':target,'policy':POLICY,'owner_quote_sha256':OWNER_QUOTE_SHA256,'stub_html_sha256':'d'*64}
        fx.current['routes'][route_for(source)]={'kind':'canonical_stub','source_path':source,'target':route_for(target),'compiled_sha256':'d'*64}
        fx.current['merged_sources'][source]=row;fx.map[source]={'status':STATUS,'target_path':target}
        fx.report=fx.make_report(violations=[]);fx.report.update(merge_artifact_passed=True,merge_hosting_status='CANONICAL_STUB_ARTIFACTS_VERIFIED_PENDING_LIVE_READBACK')
        result=fx.gate();self.assertTrue(result['incremental_release_passed']);self.assertEqual(2,result['changed_route_count'])
        self.assertFalse(result['live_http_301_verified']);self.assertFalse(result['live_stub_readback_verified']);self.assertFalse(result['final_completion_marker_allowed']);self.assertTrue(result['canonical_stub_live_readback_required'])
        fx.current['merged_sources'][source]['article_pass']=True
        with self.assertRaisesRegex(OverlayError,'article PASS'):fx.gate()
    def test_whole_artifact_guard_requires_exact_stubs_and_rejects_unrelated_changes(self):
        overlay=self.fx.apply();row=overlay.merge_statuses[self.fx.source];path=stub_artifact_path(self.fx.source);raw=render_canonical_stub(self.fx.source,row)
        prior={path:b'Old complete article','research/example.html':b'Untouched research'};candidate={path:raw,'research/example.html':b'Untouched research'}
        args=dict(prior_files=prior,candidate_files=candidate,changed_article_paths=[],changed_hub_paths=[],validated_derived_routes=[],merged_sources={self.fx.source:row},expected_redirect_bytes=None,private_sidecars={},expected_canonical_stub_bytes={path:raw})
        result=compare_complete_artifacts(**args);self.assertEqual([path],result['changed_artifact_paths'])
        candidate['research/example.html']=b'Unrelated mutation'
        with self.assertRaisesRegex(OverlayError,'Unrelated/nonlibrary'):compare_complete_artifacts(**args)
        candidate['research/example.html']=b'Untouched research';candidate[path]=raw+b'Changed'
        with self.assertRaisesRegex(OverlayError,'stub bytes differ'):compare_complete_artifacts(**args)


if __name__=='__main__':unittest.main()
