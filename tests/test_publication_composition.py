"""Synthetic regression fixtures. These approvals never describe real pages."""
import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from test_publication_overlay import Fixture,q,encoded
from library_publication_overlay import sha,canonical,OverlayError,PublicationOverlay,QUALIFIER,run_current_rendered_quality
from library_publication_release import make_compiled_state,state_fingerprint,complete_current_analysis
from library_publication_composition import ComposedPublicationOverlay,CompositionTrust,json_hash


class CompositionFixture:
    def __init__(self,root):
        self.root=Path(root)/'Downloads/LIBRARY2_2026-11/docs-repo'
        self.fx=Fixture(self.root);self.old=self.fx.approve_fixture()
        self.paths=self.fx.paths;self.docs=self.fx.docs
        self.payload={'schema_version':1,'pages':{}}
        for rel,r in self.old.records.items():
            self.payload['pages'][rel]={k:copy.deepcopy(r[k]) for k in ['meta','body','effective_head','effective_full_source','review_ids']}
            self.payload['pages'][rel]['footer_contract']=copy.deepcopy(self.fx.footers['pages'][rel])
        self.binding={'commit_sha':'a'*40,'deployment_id':'synthetic-only','artifact_sha256':'b'*64,'served_receipt_sha256':'c'*64}
        self.artifacts={'/'+rel.removesuffix('.md')+'/':('Synthetic compiled '+rel).encode() for rel in self.paths}
        self.artifacts['/answers/measurement/']=b'Synthetic hub'
        self.prior=make_compiled_state(self.old,built_route_artifacts=self.artifacts,redirects={},production_binding=self.binding)
        self.plan={'schema_version':1,'approved':True,'pages':{}}
        self.pins=copy.deepcopy(self.fx.pins)
        for rel in self.paths:self.pins['pages'][rel]['raw_source_sha256']=sha((self.docs/rel).read_bytes())
        self.leaves=copy.deepcopy(self.fx.leaves)
        for rel in self.paths:self.leaves['pages'][rel]['raw_source_sha256']=sha((self.docs/rel).read_bytes())
        self.handoff=self.docs.parents[2]/'LIVE/FIELD_TEST_TO_LIBRARY.md'
        self.handoff.parent.mkdir(exist_ok=True)
        self.add_revision(self.paths[0])
        self.save()

    def store(self,receipt):return self.fx.receipt(dict(receipt,fixture_only=True))

    def add_revision(self,rel):
        p=copy.deepcopy(self.payload['pages'][rel])
        p['body']=p['body'].replace('## What this means for you','A private synthetic reviewed explanatory sentence.\n\n## What this means for you',1)
        p['effective_full_source']=p['effective_head']+p['body']
        full_hash=sha(p['effective_full_source'].encode())
        reviews={kind:self.store({'review_kind':kind,'approved':True,'actual_full_read_complete':True,'scope':'full-effective-article','path':rel,'canonical_source_sha256':self.leaves['pages'][rel]['canonical_source_sha256'],'effective_canonical_source_sha256':full_hash}) for kind in ['source','writing']}
        p['review_ids']=reviews
        row={'before_effective_canonical_sha256':self.prior['routes']['/'+rel.removesuffix('.md')+'/']['effective_canonical_sha256'],
            'raw_canonical_source_sha256':self.leaves['pages'][rel]['canonical_source_sha256'],
            'post_finite94_body_sha256':self.pins['pages'][rel]['post_finite94_body_sha256'],
            'payload':p,'after_effective_canonical_sha256':full_hash,'after_body_sha256':sha(p['body'].encode()),
            'after_metadata_sha256':json_hash(q,p['meta']),'fact_ledger':[]}
        row['revision_receipt_sha256']=self.store({'review_kind':'reviewed-effective-revision','approved':True,'path':rel,
            'before_effective_canonical_sha256':row['before_effective_canonical_sha256'],
            'raw_canonical_source_sha256':row['raw_canonical_source_sha256'],'after_effective_canonical_sha256':full_hash,
            'fact_ledger_sha256':json_hash(q,[]),'effective_payload_sha256':json_hash(q,p)})
        self.plan['pages'][rel]=row

    def save(self):
        for name,data in [('prior',self.prior),('payload',self.payload),('leaves',self.leaves),('plan',self.plan),('map',self.fx.mapping),('pins',self.pins)]:
            (self.root/(name+'.json')).write_bytes(encoded(data))
        self.production_receipt=self.store({'approved':True,'review_kind':'prior-production-effective-payload','actual_served_readback':True,'source_render_equality_passed':True,'production_binding':self.binding,'payload_bundle_sha256':sha(encoded(self.payload)),'compiled_collection_fingerprint':state_fingerprint(self.prior,q),'compiled_route_hashes':{r:sha(b) for r,b in sorted(self.artifacts.items())}})
        self.trust=CompositionTrust(sha(encoded(self.prior)),sha(encoded(self.payload)),sha(encoded(self.leaves)),sha(encoded(self.plan)),sha(encoded(self.fx.mapping)),sha(encoded(self.pins)),production_receipt_sha256=self.production_receipt,published_count=sum(row['kind']=='article' for row in self.prior['routes'].values()))

    def compose(self,**updates):
        args=dict(docs_dir=self.docs,prior_state=self.root/'prior.json',prior_payload_bundle=self.root/'payload.json',current_leaf_manifest=self.root/'leaves.json',active_revision_plan=self.root/'plan.json',related_requirements=self.root/'map.json',current_pins=self.root/'pins.json',trust=self.trust,finite_links=self.fx.stage,quality_module=q,actual_prior_artifacts=self.artifacts,actual_prior_binding=self.binding,receipt_store=self.fx.store,field_handoff_path=self.handoff)
        args.update(updates)
        return ComposedPublicationOverlay.compose(**args)


class CompositionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.c=CompositionFixture(self.temp.name)

    def test_only_active_revision_changes_and_prior_payloads_are_exact(self):
        with patch.object(PublicationOverlay,'compile',side_effect=AssertionError('All300 compiler must not run')):
            overlay=self.c.compose()
        self.assertEqual(8,len(overlay.records));self.assertEqual(7,len(overlay.retained_prior_paths))
        for rel in overlay.retained_prior_paths:
            prior=self.c.payload['pages'][rel];r=overlay.records[rel]
            self.assertEqual(prior['body'],r['body']);self.assertEqual(prior['meta'],r['meta']);self.assertEqual(prior['effective_full_source'],r['effective_full_source'])
        self.assertEqual([],overlay.pending)

    def test_default_full_gate_stays_closed_until_whole_quality_pass(self):
        overlay=self.c.compose();rel=self.c.paths[0]
        raw=self.c.fx.stage.source_body(canonical((self.c.docs/rel).read_bytes()))[1]
        with self.assertRaisesRegex(OverlayError,'quality gate'):
            overlay.transform_after_finite94(rel,raw)
        fingerprint=overlay.public_metadata_fingerprint()
        for name in ['page-head-and-structured-data','library-hubs','llms']:overlay.register_metadata_consumer(name,fingerprint)
        result=run_current_rendered_quality(overlay,current_annotations=self.c.fx.annotations(overlay),trusted_index_references_sha256=self.c.fx.reference_hash)
        self.assertTrue(result['passed'],result['errors'])
        self.assertEqual(overlay.records[rel]['body'],overlay.transform_after_finite94(rel,raw))

    def test_missing_prior_production_proof_rejected(self):
        store=dict(self.c.fx.store);store.pop(self.c.production_receipt)
        with self.assertRaisesRegex(OverlayError,'production-effective|prior artifact'):
            self.c.compose(receipt_store=store)

    def test_preview_without_production_proof_is_explicitly_blocked(self):
        store=dict(self.c.fx.store);store.pop(self.c.production_receipt)
        overlay=self.c.compose(receipt_store=store,publication_evidence=False)
        self.assertTrue(any('no publication authority' in e for e in overlay.pending))

    def test_preview_cannot_hide_actual_prior_artifact_tampering(self):
        artifacts=dict(self.c.artifacts);artifacts[next(iter(artifacts))]=b'Tampered'
        with self.assertRaisesRegex(OverlayError,'compiled bytes changed'):
            self.c.compose(actual_prior_artifacts=artifacts,publication_evidence=False)

    def test_payload_tamper_rejected_before_production_claim(self):
        self.c.payload['pages'][self.c.paths[-1]]['body']+='\nTampered'
        self.c.save()
        with self.assertRaisesRegex(OverlayError,'payload is not'):
            self.c.compose(publication_evidence=False)

    def test_missing_untouched_payload_rejected(self):
        del self.c.payload['pages'][self.c.paths[-1]];self.c.save()
        with self.assertRaisesRegex(OverlayError,'hides or invents'):
            self.c.compose()

    def test_source_drift_outside_group_rejected_even_with_rebound_current_pin(self):
        rel=self.c.paths[-1];p=self.c.docs/rel;p.write_bytes(p.read_bytes()+b'\nChanged source\n')
        h=sha(canonical(p.read_bytes()).encode());self.c.leaves['pages'][rel]['canonical_source_sha256']=h
        self.c.leaves['pages'][rel]['raw_source_sha256']=sha(p.read_bytes())
        self.c.pins['pages'][rel]['canonical_source_sha256']=h;self.c.pins['pages'][rel]['raw_source_sha256']=sha(p.read_bytes());self.c.save()
        with self.assertRaisesRegex(OverlayError,'outside the active revision'):
            self.c.compose()

    def test_active_after_metadata_and_body_hashes_are_exact(self):
        self.c.plan['pages'][self.c.paths[0]]['after_metadata_sha256']='e'*64;self.c.save()
        with self.assertRaisesRegex(OverlayError,'after body/metadata pins'):
            self.c.compose()

    def test_active_before_production_binding_exact(self):
        self.c.plan['pages'][self.c.paths[0]]['before_effective_canonical_sha256']='e'*64;self.c.save()
        with self.assertRaisesRegex(OverlayError,'before-production'):
            self.c.compose()

    def test_active_reviewer_missing_remains_current_failure(self):
        del self.c.fx.store[self.c.plan['pages'][self.c.paths[0]]['revision_receipt_sha256']]
        overlay=self.c.compose()
        self.assertTrue(any(self.c.paths[0] in e and 'revision/fact-ledger' in e for e in overlay.pending))

    def test_new_leaf_requires_explicit_active_revision(self):
        rel='answers/measurement/new-leaf.md';raw=(self.c.docs/self.c.paths[-1]).read_bytes();(self.c.docs/rel).write_bytes(raw)
        self.c.leaves['pages'][rel]={'canonical_source_sha256':sha(canonical(raw).encode()),'raw_source_sha256':sha(raw)};self.c.save()
        with self.assertRaisesRegex(OverlayError,'no explicit independently pinned'):
            self.c.compose()

    def test_actual_full_current_analysis_logs_untouched_failure(self):
        rel=self.c.paths[-1];p=self.c.payload['pages'][rel]
        p['body']=p['body'].replace('\n\n'+QUALIFIER,'',1);p['effective_full_source']=p['effective_head']+p['body']
        route='/'+rel.removesuffix('.md')+'/'
        self.c.prior['routes'][route].update(body_sha256=sha(p['body'].encode()),effective_canonical_sha256=sha(p['effective_full_source'].encode()))
        self.c.save();overlay=self.c.compose()
        f=overlay.public_metadata_fingerprint()
        for name in ['page-head-and-structured-data','library-hubs','llms']:overlay.register_metadata_consumer(name,f)
        state=make_compiled_state(overlay,built_route_artifacts=self.c.artifacts,redirects={})
        result=complete_current_analysis(overlay,state,current_annotations=self.c.fx.annotations(overlay),trusted_index_references_sha256=self.c.fx.reference_hash)
        self.assertTrue(result['all_pairs_compared']);self.assertEqual(28,result['pair_count']);self.assertFalse(result['passed'])
        self.assertFalse(result['page_readiness'][rel]['passed']);self.assertEqual(0,result['baseline_exceptions'])

    def test_changed_page_cannot_skip_footer_or_related_checks(self):
        rel=self.c.paths[0];p=self.c.plan['pages'][rel]['payload'];p.pop('footer_contract')
        self.c.save();overlay=self.c.compose()
        self.assertTrue(any(e.startswith(rel+': ') and 'footer contract' in e for e in overlay.pending))

    def test_wrong_shared_handoff_path_rejected(self):
        with self.assertRaisesRegex(OverlayError,'Incorrect shared'):
            self.c.compose(field_handoff_path=self.c.root/'absent-handoff.md')

    def test_existing_field_handoff_requires_bound_served_pins(self):
        self.c.handoff.write_text('Freeze one page')
        with self.assertRaisesRegex(OverlayError,'frozen served pins'):
            self.c.compose()

    def test_field_handoff_appearing_after_compose_blocks_output(self):
        overlay=self.c.compose();self.c.handoff.write_text('Freeze now')
        with self.assertRaisesRegex(OverlayError,'appeared or changed'):
            overlay.effective_metadata(self.c.paths[0])

    def test_all_metadata_consumers_must_use_same_effective_registry(self):
        overlay=self.c.compose();self.assertEqual(3,len(overlay.metadata_consumer_errors()))
        with self.assertRaisesRegex(OverlayError,'stale metadata'):
            overlay.register_metadata_consumer('llms','d'*64)

    def test_unapproved_group_cannot_compose_as_publication(self):
        self.c.plan['approved']=False;self.c.save()
        with self.assertRaisesRegex(OverlayError,'plan is not approved'):
            self.c.compose()
        self.assertTrue(self.c.compose(publication_evidence=False).pending)

    def test_canonical_equal_line_ending_mutation_after_compose_is_rejected(self):
        overlay=self.c.compose();p=self.c.docs/self.c.paths[-1]
        p.write_bytes(p.read_bytes().replace(b'\n',b'\r\n'))
        with self.assertRaisesRegex(OverlayError,'Exact current raw source bytes differ'):
            overlay.effective_metadata(self.c.paths[0])

    def test_active_numeric_change_needs_fact_ledger_even_with_new_pins(self):
        row=self.c.plan['pages'][self.c.paths[0]];p=row['payload']
        p['body']=p['body'].replace('1 of 10','2 of 10',1);p['effective_full_source']=p['effective_head']+p['body']
        row['after_body_sha256']=sha(p['body'].encode());row['after_effective_canonical_sha256']=sha(p['effective_full_source'].encode())
        self.c.save()
        with self.assertRaisesRegex(OverlayError,'numeric/date change requires'):
            self.c.compose()

    def test_active_primary_source_destination_cannot_disappear(self):
        row=self.c.plan['pages'][self.c.paths[0]];p=row['payload'];old='https://example.test/source/0'
        p['body']=p['body'].replace(old,'https://example.test/replacement/0');p['effective_full_source']=p['effective_head']+p['body']
        row['after_body_sha256']=sha(p['body'].encode());row['after_effective_canonical_sha256']=sha(p['effective_full_source'].encode())
        self.c.save()
        with self.assertRaisesRegex(OverlayError,'loses a primary evidence'):
            self.c.compose()

    def retire_prior_source(self):
        from library_publication_release import route_for,route_forms
        source,target=self.c.paths[-1],self.c.paths[0]
        self.c.prior['routes'].pop(route_for(source));self.c.artifacts.pop(route_for(source));self.c.payload['pages'].pop(source)
        for route in route_forms(source):self.c.prior['routes'][route]={'kind':'redirect','status':301,'target':route_for(target),'source_path':source}
        self.c.prior['merged_sources'][source]={'status':'MERGED_301','article_pass':False,'target_path':target,'decision_receipt_sha256':'d'*64}
        self.c.save();return source,target

    def test_prior_real301_remains_retired_raw_history_in_later_group(self):
        source,target=self.retire_prior_source();raw=(self.c.docs/source).read_bytes();overlay=self.c.compose()
        self.assertEqual(7,len(overlay.records));self.assertNotIn(source,overlay.records)
        self.assertEqual('MERGED_301',overlay.merge_statuses[source]['status']);self.assertEqual({},overlay._new_merge_plan)
        self.assertEqual(raw,(self.c.docs/source).read_bytes())

    def test_retired_source_cannot_be_silently_revived(self):
        source,_=self.retire_prior_source();self.c.plan['pages'][source]={};self.c.save()
        with self.assertRaisesRegex(OverlayError,'cannot be revived'):
            self.c.compose()

    def test_later_target_revision_preserves_prior_merged_evidence(self):
        source,target=self.retire_prior_source();p=self.c.payload['pages'][target]
        p['body']=p['body'].replace('## What this means for you','[Previously merged study](https://evidence.fixture.test/merged-study)\n\n## What this means for you')
        p['effective_full_source']=p['effective_head']+p['body'];fullhash=sha(p['effective_full_source'].encode())
        from library_publication_release import route_for
        self.c.prior['routes'][route_for(target)].update(effective_canonical_sha256=fullhash,body_sha256=sha(p['body'].encode()))
        self.c.plan['pages'][target]['before_effective_canonical_sha256']=fullhash;self.c.save()
        with self.assertRaisesRegex(OverlayError,'loses a primary evidence'):
            self.c.compose()


if __name__=='__main__':unittest.main()
