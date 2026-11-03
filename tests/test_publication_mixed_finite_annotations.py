"""Synthetic routing regressions, never actual page or approval receipts."""
import copy
import json
import tempfile
import unittest
from unittest.mock import patch

from tools import library_quality as q, library_company_panel as panel
from test_publication_overlay import Fixture, encoded
from library_publication_overlay import (PublicationOverlay, validate_current_annotations,
    run_current_rendered_quality, qualitative_observation_key, sha)
import test_publication_company_panel as panel_tests


def current_pages(overlay):
    pages = copy.deepcopy(overlay.records)
    for p in pages.values():
        opening = q.paragraph_after_heading(p['body']).strip()
        p.update(opening=opening, opening_sha256=sha(opening.encode()))
    return pages


class MixedCurrentAnnotationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.fx = Fixture(self.temp.name)
        self.overlay = self.fx.approve_fixture()
        self.metadata = self.fx.annotations(self.overlay)
        self.rel = self.fx.paths[0]

    def mixed(self, rel=None):
        rel = rel or self.rel
        original = copy.deepcopy(self.metadata['pages'][rel])
        binding = self.fx.qualitative_note(self.overlay, self.metadata, rel)
        for key in ['lead_figures', 'lead_figure_spans']:
            self.metadata['pages'][rel][key] = original[key]
        return binding

    def validate(self):
        return validate_current_annotations(self.overlay, current_pages(self.overlay), self.metadata)

    def test_mixed_validates_both_leads_without_mutating_caller(self):
        binding = self.mixed()
        before = copy.deepcopy(self.metadata)
        notes, observations = self.validate()
        self.assertEqual(before, self.metadata)
        self.assertTrue(notes[self.rel]['lead_figures'])
        self.assertIn('qualitative_opening', notes[self.rel])
        self.assertEqual(binding['observation_key'], observations[self.rel])

    def test_mixed_numeric_span_still_required(self):
        self.mixed()
        note = self.metadata['pages'][self.rel]
        note['lead_figure_spans'][note['lead_figures'][0]] = ['not in the opening']
        with self.assertRaisesRegex(ValueError, 'lead figure span'):
            self.validate()

    def test_mixed_numeric_identity_still_required(self):
        self.mixed()
        self.metadata['pages'][self.rel]['lead_figures'] = ['unregistered-numeric-cut']
        with self.assertRaisesRegex(ValueError, 'unknown lead figure'):
            self.validate()

    def test_only_controlled_extra_field_is_removed_from_numeric_copy(self):
        self.mixed()
        self.metadata['pages'][self.rel]['arbitrary_allowance'] = True
        with self.assertRaisesRegex(ValueError, 'unknown/private page audit fields'):
            self.validate()

    def test_mixed_malformed_qualitative_binding_fails(self):
        self.mixed()
        self.metadata['pages'][self.rel]['qualitative_opening'] = {'waived': True}
        with self.assertRaisesRegex(ValueError, 'exact observation/quote/span/receipt'):
            self.validate()

    def test_mixed_stale_qualitative_quote_fails(self):
        binding = self.mixed()
        binding['source_quote'] += ' Unreviewed change.'
        with self.assertRaisesRegex(ValueError, 'observation approval missing or stale'):
            self.validate()

    def test_mixed_independent_observation_receipt_required(self):
        binding = self.mixed()
        self.overlay.receipt_store.pop(binding['independent_receipt_sha256'])
        with self.assertRaisesRegex(ValueError, 'observation approval missing or stale'):
            self.validate()

    def test_mixed_full_current_writing_receipt_required(self):
        self.mixed()
        self.overlay.receipt_store.pop(self.metadata['pages'][self.rel]['writing_review_sha256'])
        with self.assertRaisesRegex(ValueError, 'full-page writing receipt missing'):
            self.validate()

    def test_mixed_qualitative_cannot_disguise_registered_aggregate(self):
        binding = self.mixed()
        figure = self.metadata['figures'][self.metadata['pages'][self.rel]['lead_figures'][0]]
        binding.update(source_url=figure['source_url'], record=figure['record'])
        binding['observation_key'] = qualitative_observation_key(binding, q)[0]
        with self.assertRaisesRegex(ValueError, 'disguises a registered aggregate'):
            self.validate()

    def test_existing_pure_qualitative_mode_is_unchanged(self):
        self.fx.qualitative_note(self.overlay, self.metadata, self.rel)
        notes, observations = self.validate()
        self.assertEqual([], notes[self.rel]['lead_figures'])
        self.assertIn(self.rel, observations)

    def test_four_mixed_uses_count_the_qualitative_limit(self):
        for rel in self.fx.paths[:4]:
            self.mixed(rel)
        result = run_current_rendered_quality(self.overlay, current_annotations=self.metadata,
                                             trusted_index_references_sha256=self.fx.reference_hash)
        self.assertFalse(result['passed'])
        self.assertTrue(any(r['kind'] == 'qualitative_lead_limit' for r in result['violations']))

    def test_mixed_and_pure_uses_share_one_qualitative_allowance(self):
        for rel in self.fx.paths[:2]:
            self.mixed(rel)
        for rel in self.fx.paths[2:4]:
            self.fx.qualitative_note(self.overlay, self.metadata, rel)
        result = run_current_rendered_quality(self.overlay, current_annotations=self.metadata,
                                             trusted_index_references_sha256=self.fx.reference_hash)
        self.assertFalse(result['passed'])
        cases = [r for r in result['violations'] if r['kind'] == 'qualitative_lead_limit']
        self.assertEqual(1, len(cases))
        self.assertEqual(4, cases[0]['count'])


class FiniteCompanyCurrentRoutingTests(unittest.TestCase):
    def setUp(self):
        # Existing fictional helper fixture cannot pass production immutable
        # load_registry. Only that loader is patched in these helper tests;
        # actual q.validate_annotations and finite body/kind/case guards run.
        self.fx = panel_tests.CompanyPanelTests()
        self.fx.setUp()
        self.addCleanup(self.fx.doCleanups)

    def fixture(self, numeric=False):
        data, meta, body, page, note, expected = self.fx.fixture(numeric=numeric)
        case = data['cases'][meta['evidence_case']]
        overlay = PublicationOverlay()
        overlay.q = q
        overlay.receipt_store = {}
        page['raw_canonical_source_sha256'] = page['canonical_source_sha256']
        page['effective_canonical_source_sha256'] = page['canonical_source_sha256']
        page['review_ids'] = {}
        for kind in ['source', 'writing']:
            receipt = {'approved': True, 'fixture_only': True, 'actual_full_read_complete': True,
                       'review_kind': kind, 'scope': 'full-effective-article', 'path': page['path'],
                       'canonical_source_sha256': page['raw_canonical_source_sha256'],
                       'effective_canonical_source_sha256': page['effective_canonical_source_sha256'],
                       'effective_body_sha256':sha(page['body'].encode()),
                       'finite_body_review_lineage':{
                           'evidence_kind':q.COMPANY_PANEL_KIND,'evidence_case':page['meta']['evidence_case'],
                           'review_kind':kind,'original_review_sha256':note[kind+'_review_sha256'],
                           'reviewed_body_sha256':sha(panel.canonical_body(page['body']).encode())}}
            raw = encoded(receipt)
            key = sha(raw)
            overlay.receipt_store[key] = raw
            page['review_ids'][kind] = key
        shapes = ['source_first'] + [f'fictional-shape-{i}' for i in range(7)]
        figures = {}
        for record in data['cases'].values():
            figures.update(panel.expected_figures(record, q.figure_key))
        metadata = {'schema_version': 1, 'shape_definitions': {k:'Fictional explicit class '+k for k in shapes},
                    'cluster_plans': {'changes': shapes}, 'figures': figures,
                    'pages': {page['path']:note}, 'index_question_titles': {'source_sha256':'a'*64,'records':[]}}
        return data, overlay, page, note, metadata

    def validate(self, data, overlay, page, metadata):
        with patch.object(panel, 'load_registry', return_value=data) as loader:
            result = validate_current_annotations(overlay, {page['path']:page}, metadata)
            self.assertTrue(loader.called)
            return result

    def test_exact_finite_qualitative_mode_delegates_to_real_q_without_general_binding(self):
        data, overlay, page, note, metadata = self.fixture()
        before = copy.deepcopy(metadata)
        notes, general_keys = self.validate(data, overlay, page, metadata)
        self.assertEqual({}, general_keys)
        self.assertEqual([], notes[page['path']]['lead_figures'])
        self.assertTrue(notes[page['path']]['lead_observations'])
        self.assertNotIn('qualitative_opening', notes[page['path']])
        self.assertEqual(before, metadata)

    def test_exact_finite_numeric_mode_remains_numeric(self):
        data, overlay, page, note, metadata = self.fixture(numeric=True)
        notes, general_keys = self.validate(data, overlay, page, metadata)
        self.assertTrue(notes[page['path']]['lead_figures'])
        self.assertEqual([], notes[page['path']]['lead_observations'])
        self.assertEqual({}, general_keys)

    def test_finite_wrong_kind_cannot_fall_back_to_general_mode(self):
        data, overlay, page, note, metadata = self.fixture()
        page['meta']['evidence_kind'] = 'published-study'
        with self.assertRaisesRegex(ValueError, 'exact owning evidence kind'):
            validate_current_annotations(overlay, {page['path']:page}, metadata)

    def test_unknown_finite_case_rejected_by_owning_validator(self):
        data, overlay, page, note, metadata = self.fixture()
        page['meta']['evidence_case'] = 'not-one-of-six'
        with self.assertRaisesRegex(ValueError, 'unknown/off-registry case'):
            self.validate(data, overlay, page, metadata)

    def test_wrong_bank_id_still_rejected_by_raw_q(self):
        data, overlay, page, note, metadata = self.fixture()
        note['bank_id'] = 'LB-Q9999'
        with self.assertRaisesRegex(ValueError, 'annotation bank ID differs'):
            self.validate(data, overlay, page, metadata)

    def test_changed_finite_body_rejected_by_immutable_case_binding(self):
        data, overlay, page, note, metadata = self.fixture()
        page['body'] += '\nUnreviewed body change.\n'
        with self.assertRaisesRegex(ValueError, 'body changed'):
            self.validate(data, overlay, page, metadata)

    def test_finite_mode_cannot_add_general_qualitative_allowance(self):
        data, overlay, page, note, metadata = self.fixture()
        note['qualitative_opening'] = {'arbitrary':True}
        with self.assertRaisesRegex(ValueError, 'unknown/private page audit fields'):
            self.validate(data, overlay, page, metadata)

    def test_finite_observation_key_cannot_be_renamed(self):
        data, overlay, page, note, metadata = self.fixture()
        note['lead_observations'] = ['renamed-allowance']
        with self.assertRaisesRegex(ValueError, 'observation keys'):
            self.validate(data, overlay, page, metadata)

    def test_finite_full_current_source_receipt_is_required(self):
        data, overlay, page, note, metadata = self.fixture()
        overlay.receipt_store.pop(page['review_ids']['source'])
        with self.assertRaisesRegex(ValueError, 'finite company-panel full-page source receipt missing'):
            self.validate(data, overlay, page, metadata)

    def test_finite_full_current_writing_receipt_is_required(self):
        data, overlay, page, note, metadata = self.fixture()
        overlay.receipt_store.pop(page['review_ids']['writing'])
        with self.assertRaisesRegex(ValueError, 'finite company-panel full-page writing receipt missing'):
            self.validate(data, overlay, page, metadata)

    def test_finite_qualitative_cannot_receive_fake_numeric_one(self):
        data, overlay, page, note, metadata = self.fixture()
        note['lead_figures'] = [next(iter(metadata['figures']))]
        with self.assertRaisesRegex(ValueError, 'no fake count-one'):
            self.validate(data, overlay, page, metadata)

    def test_validated_finite_observation_is_retained_for_unchanged_max3_counter(self):
        data, overlay, page, note, metadata = self.fixture()
        notes, _ = self.validate(data, overlay, page, metadata)
        # Counting-only copies are fictional and have no publication approval.
        # This directly exercises the unchanged q counter on returned notes.
        pages, annotations = {}, {}
        for i in range(4):
            rel = f'answers/changes/counter-copy-{i}.md'
            p = copy.deepcopy(page)
            p['path'] = rel
            p['meta'].update(title=f'Fictional distinct title {i}', headline=f'Fictional distinct headline {i}', description=f'Fictional unique descriptor {i}')
            pages[rel] = p
            annotations[rel] = copy.deepcopy(notes[page['path']])
        result = q.analyze(pages, annotations, {'changes':list(pages)}, [], self.fx.docs)
        limits = [r for r in result['violations'] if r['kind'] == 'lead_observation_limit']
        self.assertEqual(set(notes[page['path']]['lead_observations']),
                         {r['observation'] for r in limits})
        self.assertEqual(len(notes[page['path']]['lead_observations']), len(limits))
        self.assertTrue(all(r['count'] == 4 for r in limits))


if __name__ == '__main__':
    unittest.main()
