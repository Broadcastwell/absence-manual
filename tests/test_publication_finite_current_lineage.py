"""Fictional typed-wrapper regressions; no real review authority is minted."""
import copy
import json
import unittest
from unittest.mock import patch

import test_publication_mixed_finite_annotations as routing
from test_publication_overlay import encoded,Fixture
import tempfile
from tools import library_quality as q, library_company_panel as panel
from library_publication_overlay import (sha, validate_current_annotations,
    validate_finite_current_review, run_current_rendered_quality)
from library_publication_release import assess_current_records


class FiniteCurrentLineageTests(unittest.TestCase):
    def setUp(self):
        self.fixture_case = routing.FiniteCompanyCurrentRoutingTests()
        self.fixture_case.setUp()
        self.addCleanup(self.fixture_case.doCleanups)
        self.data,self.overlay,self.page,self.note,self.metadata=self.fixture_case.fixture()

    def validate(self):
        with patch.object(panel,'load_registry',return_value=self.data):
            return validate_current_annotations(self.overlay,{self.page['path']:self.page},self.metadata)

    def revise_receipt(self,change,kind='source'):
        receipt=json.loads(self.overlay.receipt_store[self.page['review_ids'][kind]])
        change(receipt)
        raw=encoded(receipt);key=sha(raw)
        self.overlay.receipt_store[key]=raw
        self.page['review_ids'][kind]=key

    def prepare_collection(self):
        rel=self.page['path']
        refs={'source_sha256':'a'*64,'records':[
            {'title':f'Unrelated fictional reference question {i}',
             'url':f'https://index.example.test/questions/{i}/'} for i in range(140)]}
        self.metadata['index_question_titles']=refs
        self.overlay.records={rel:self.page}
        self.overlay.docs=self.fixture_case.fx.docs
        self.overlay.pending=[]
        self.overlay.mapping={'pages':{rel:{}}}
        self.overlay.leaf_manifest={'pages':{rel:{}}}
        self.overlay._check_unchanged=lambda:None
        self.overlay._validate_related=lambda *args:None
        self.overlay.metadata_consumer_errors=lambda:[]
        hub=self.overlay.docs/'answers/changes/index.md'
        hub.parent.mkdir(parents=True,exist_ok=True)
        hub.write_text('[Fictional current question](fixture.md)\n',encoding='utf-8')
        return sha(q.canonical_json(refs).encode())

    def test_current_fullfile_wrapper_has_distinct_immutable_parent(self):
        before=copy.deepcopy((self.page,self.note,self.metadata,self.data))
        self.validate()
        for kind in ['source','writing']:
            self.assertNotEqual(self.note[kind+'_review_sha256'],self.page['review_ids'][kind])
        self.assertEqual(before,(self.page,self.note,self.metadata,self.data))

    def test_both_finite_numeric_and_qualitative_cases_use_same_exact_bridge(self):
        self.data,self.overlay,self.page,self.note,self.metadata=self.fixture_case.fixture(numeric=True)
        notes,keys=self.validate()
        self.assertTrue(notes[self.page['path']]['lead_figures'])
        self.assertEqual({},keys)

    def test_missing_current_record_review_ids_rejected(self):
        self.page.pop('review_ids')
        with self.assertRaisesRegex(ValueError,'full-page source receipt missing'):self.validate()

    def test_missing_current_source_wrapper_rejected(self):
        self.overlay.receipt_store.pop(self.page['review_ids']['source'])
        with self.assertRaisesRegex(ValueError,'full-page source receipt missing'):self.validate()

    def test_missing_current_writing_wrapper_rejected(self):
        self.overlay.receipt_store.pop(self.page['review_ids']['writing'])
        with self.assertRaisesRegex(ValueError,'full-page writing receipt missing'):self.validate()

    def test_missing_lineage_rejected(self):
        self.revise_receipt(lambda r:r.pop('finite_body_review_lineage'))
        with self.assertRaisesRegex(ValueError,'historical lineage differs'):self.validate()

    def test_wrong_or_missing_parent_rejected(self):
        for value in [None,'0'*64,self.note['writing_review_sha256']]:
            with self.subTest(value=value):
                self.revise_receipt(lambda r:r['finite_body_review_lineage'].__setitem__('original_review_sha256',value))
                with self.assertRaisesRegex(ValueError,'historical lineage differs'):self.validate()

    def test_wrong_historical_body_rejected(self):
        self.revise_receipt(lambda r:r['finite_body_review_lineage'].__setitem__('reviewed_body_sha256','0'*64))
        with self.assertRaisesRegex(ValueError,'historical lineage differs'):self.validate()

    def test_wrong_exact_current_body_rejected(self):
        self.revise_receipt(lambda r:r.__setitem__('effective_body_sha256','0'*64))
        with self.assertRaisesRegex(ValueError,'body binding differs'):self.validate()

    def test_wrong_path_raw_source_effective_source_and_scope_rejected(self):
        for field,value in [('path','answers/changes/another.md'),
            ('canonical_source_sha256','0'*64),('effective_canonical_source_sha256','0'*64),
            ('scope','opening-only'),('review_kind','writing'),('approved',False),
            ('actual_full_read_complete',False)]:
            with self.subTest(field=field):
                data,overlay,page,note,metadata=self.fixture_case.fixture()
                self.data,self.overlay,self.page,self.note,self.metadata=data,overlay,page,note,metadata
                self.revise_receipt(lambda r:r.__setitem__(field,value))
                with self.assertRaisesRegex(ValueError,'full-page source receipt missing'):self.validate()

    def test_extra_lineage_fields_rejected(self):
        self.revise_receipt(lambda r:r['finite_body_review_lineage'].__setitem__('waived',True))
        with self.assertRaisesRegex(ValueError,'historical lineage differs'):self.validate()

    def test_wrong_case_kind_or_review_kind_lineage_rejected(self):
        for field,value in [('evidence_case','arbitrary-case'),('evidence_kind','published-study'),('review_kind','writing')]:
            with self.subTest(field=field):
                self.revise_receipt(lambda r:r['finite_body_review_lineage'].__setitem__(field,value))
                with self.assertRaisesRegex(ValueError,'historical lineage differs'):self.validate()

    def test_forged_note_and_matching_forged_parent_cannot_replace_registry(self):
        self.note['source_review_sha256']='0'*64
        self.revise_receipt(lambda r:r['finite_body_review_lineage'].__setitem__('original_review_sha256','0'*64))
        with self.assertRaisesRegex(ValueError,'actual source-review continuation'):self.validate()

    def test_direct_helper_also_revalidates_owning_case_body(self):
        self.page['body']+='\nA forged new conclusion.\n'
        with patch.object(panel,'load_registry',return_value=self.data):
            with self.assertRaisesRegex(ValueError,'body changed'):
                validate_finite_current_review(self.overlay,self.page,self.note,'source',self.metadata['figures'])

    def test_current_wrapper_cannot_expand_qualitative_keys_or_numeric_cuts(self):
        self.note['lead_observations']=['forged-new-observation']
        with self.assertRaisesRegex(ValueError,'observation keys'):self.validate()

    def test_direct_helper_rejects_nonfinite_kind(self):
        self.page['meta']['evidence_kind']='published-study'
        with self.assertRaisesRegex(ValueError,'exact owning kind'):
            validate_finite_current_review(self.overlay,self.page,self.note,'source',self.metadata['figures'])

    def test_full_collection_assessment_uses_current_wrappers_and_historical_parents(self):
        refhash=self.prepare_collection()
        with patch.object(panel,'load_registry',return_value=self.data):
            result=assess_current_records(self.overlay,current_annotations=self.metadata,
                                          trusted_index_references_sha256=refhash)
        self.assertTrue(result['analysis_completed'],result['global_fatal_errors'])
        self.assertFalse(result['global_fatal_errors'])
        # This small owning-helper fixture deliberately lacks the common
        # qualifier and has one shape in a one-page collection. Those actual
        # unrelated failures remain visible; neither receipt mismatch appears.
        errors=result['page_readiness'][self.page['path']]['errors']
        self.assertIn('Exactly one reputation qualifier required',errors)
        self.assertFalse(any('receipt' in str(error) or 'lineage' in str(error) for error in errors))

    def test_full_collection_current_source_wrapper_cannot_be_stale(self):
        refhash=self.prepare_collection()
        self.revise_receipt(lambda r:r.__setitem__('canonical_source_sha256','0'*64))
        with patch.object(panel,'load_registry',return_value=self.data):
            result=assess_current_records(self.overlay,current_annotations=self.metadata,
                                          trusted_index_references_sha256=refhash)
        self.assertFalse(result['page_readiness'][self.page['path']]['passed'])
        self.assertTrue(result['global_fatal_errors'])

    def test_legacy_full_gate_uses_same_finite_bridge(self):
        refhash=self.prepare_collection()
        with patch.object(panel,'load_registry',return_value=self.data):
            result=run_current_rendered_quality(self.overlay,current_annotations=self.metadata,
                                                trusted_index_references_sha256=refhash)
        self.assertFalse(result['passed'])
        self.assertTrue(any('Exactly one reputation qualifier required' in str(e) for e in result['errors']))
        self.assertFalse(any('receipt' in str(e) or 'lineage' in str(e) for e in result['errors']))

    def test_ordinary_current_annotation_review_equality_is_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            fx=Fixture(directory);overlay=fx.approve_fixture();metadata=fx.annotations(overlay)
            metadata['pages'][fx.paths[0]]['source_review_sha256']='0'*64
            result=assess_current_records(overlay,current_annotations=metadata,
                                          trusted_index_references_sha256=fx.reference_hash)
            self.assertFalse(result['page_readiness'][fx.paths[0]]['passed'])
            self.assertIn('Current annotation source receipt differs from the reviewed effective record',
                          result['page_readiness'][fx.paths[0]]['errors'])

    def test_ordinary_wrapper_cannot_claim_finite_lineage_to_bypass_equality(self):
        with tempfile.TemporaryDirectory() as directory:
            fx=Fixture(directory);overlay=fx.approve_fixture();metadata=fx.annotations(overlay)
            rel=fx.paths[0]
            current=json.loads(overlay.receipt_store[overlay.records[rel]['review_ids']['source']])
            current['finite_body_review_lineage']={'original_review_sha256':'0'*64}
            raw=encoded(current);key=sha(raw);overlay.receipt_store[key]=raw
            overlay.records[rel]['review_ids']['source']=key
            result=assess_current_records(overlay,current_annotations=metadata,
                                          trusted_index_references_sha256=fx.reference_hash)
            self.assertFalse(result['page_readiness'][rel]['passed'])
            self.assertIn('Current annotation source receipt differs from the reviewed effective record',
                          result['page_readiness'][rel]['errors'])


if __name__=='__main__':unittest.main()
