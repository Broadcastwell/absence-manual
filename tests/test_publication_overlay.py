"""Private scaffold regressions. Synthetic fixtures are never real approvals."""
from __future__ import annotations
import copy
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import random
import string
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / 'tools'))
SUPPORT = Path(os.environ['BW_OVERLAY_SUPPORT_REPO']).resolve()
sys.path.insert(0, str(SUPPORT))
from tools import library_quality as q
from library_publication_overlay import (PublicationOverlay, TrustedInputs, FiniteStage,
    OverlayError, QUALIFIER, FREE_CHECK_TOKEN, LIMIT_SENTENCE, sha, canonical,
    key_hash, opening_span, next_step_span, remove_exact_qualifier,
    invert_operations, current_comparison_prose, run_current_rendered_quality,
    read_bound_json, qualitative_observation_key, enforce_frozen_articles)

finite_path = Path(os.environ.get('BW_OVERLAY_FINITE_MODULE', str(SUPPORT / 'tools/library_related_chapter_links.py')))
spec = importlib.util.spec_from_file_location('private_overlay_original_finite', finite_path)
finite_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(finite_module)


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


class NoopFinite:
    def transform(self, path, body):
        return body


class Fixture:
    def __init__(self, directory):
        self.root = Path(directory)
        self.docs = self.root / 'docs'
        self.folder = self.docs / 'answers/measurement'
        self.folder.mkdir(parents=True)
        (self.docs / 'valid-measurement.md').write_text('---\ntitle: Valid measurement\npage_class: chapter\n---\n\n# Valid measurement\n\nFixture chapter.\n')
        (self.docs / 'resource.md').write_text('---\ntitle: Resource\npage_class: page\n---\n\n# Resource\n')
        self.pins = {'schema_version': 1, 'page_count': 8, 'pages': {}}
        self.mapping = {'schema_version': 1, 'proposal_only': False, 'exact_page_count': 8, 'pages': {}}
        self.leaves = {'pages': {}}
        self.bodies = {'pages': {}}
        self.footers = {'pages': {}}
        self.store = {}
        self.stage = FiniteStage(finite_module, NoopFinite())
        self.references = {'source_sha256': 'a' * 64, 'records': [{'title': f'Unrelated reference question {i}', 'url': f'https://index.example.test/questions/{i}/'} for i in range(140)]}
        self.reference_hash = sha(q.canonical_json(self.references).encode())
        for i in range(8):
            rng = random.Random(i)
            tokens = [''.join(rng.choices(string.ascii_lowercase, k=9)) for _ in range(120)]
            rel = f'answers/measurement/fixture-{i}.md'
            opening = ' '.join(tokens[:20]) + f' {i+1} of 10 on 1 November 2026.'
            narrative = ' '.join(tokens[20:]) + '.'
            old_related = '\n\n- [Valid measurement](../../valid-measurement.md)\n- [Source](https://example.test/source/' + str(i) + ')\n- [Resource](../../resource.md)\n\n'
            body = f'# Fixture {tokens[0]}?\n\n{opening}\n\n## What we measured\n\n{narrative}\n\n[Source](https://example.test/source/{i})\n\n## What this means for you\n\n{tokens[2]} {tokens[3]}.\n\n## Also asked as\n\nFixture alias {tokens[1]}?\n\n## Related' + old_related + '## Next step\n\nUse the ' + FREE_CHECK_TOKEN + '. ' + LIMIT_SENTENCE + '\n\n[Scoped study method](https://doi.org/10.1234/fixture)\n\nFor a sourced error, [Fix one answer, $490](https://broadcastwell.com/answer-repair).\n\nPrepared by the Broadcastwell team.\n\nPage owner: Fixture Reviewer, Analyst. Corrections: hello@broadcastwell.com\n'
            head = f'---\ntitle: Fixture {tokens[0]}?\nheadline: Fixture {tokens[0]}?\ndescription: Private {tokens[1]} example.\npage_class: page\nlibrary_cluster: measurement\ndemand_evidence: LB-Q{i+1:04d}, fixture only\n---\n\n'
            raw = (head + body).encode()
            (self.docs / rel).write_bytes(raw)
            canonical_pin = sha(raw)
            self.pins['pages'][rel] = {'canonical_source_sha256': canonical_pin, 'post_finite94_body_sha256': sha(body.encode())}
            new_related = old_related + '- [More measurement answers](https://docs.broadcastwell.com/answers/measurement/)\n- [Index record](https://index.broadcastwell.com/categories/crm/)\n\n'
            self.mapping['pages'][rel] = {'canonical_source_sha256': canonical_pin, 'post_finite94_body_sha256': sha(body.encode()),
                'post_finite94_related_sha256': sha(old_related.encode()), 'related_markdown': new_related,
                'related_markdown_sha256': sha(new_related.encode()), 'chapter_path': 'valid-measurement.md',
                'own_cluster_hub_path': 'answers/measurement/index.md', 'index_applicable': True,
                'required_index_href': 'https://index.broadcastwell.com/categories/crm/',
                'source_link_paragraph_before_related': '', 'omitted_optional_sibling_hrefs': []}
            self.leaves['pages'][rel] = {'canonical_source_sha256': canonical_pin}
            self.bodies['pages'][rel] = {'canonical_source_sha256': canonical_pin, 'post_finite94_body_sha256': sha(body.encode()), 'patches': [], 'post_patches_body_sha256': sha(body.encode()), 'reviews': {}}
            start, end = next_step_span(body)
            self.footers['pages'][rel] = {'old_next_step_sha256': sha(body[start:end].encode()), 'method_token': '[Scoped study method](https://doi.org/10.1234/fixture)', 'offer': {'name': 'Answer Repair', 'price': '$490', 'href': 'https://broadcastwell.com/answer-repair'}}
        self.paths = sorted(self.pins['pages'])
        (self.folder / 'index.md').write_text('---\ntitle: Measurement answers\npage_class: page\n---\n\n# Measurement\n\n' + '\n'.join(f'- [Fixture {i}](fixture-{i}.md)' for i in range(8)) + '\n')
        self.pins['keys_sha256'] = key_hash(self.paths)
        self.mapping['exact_keys_sha256'] = self.pins['keys_sha256']
        self.bind_inputs()

    def bind_inputs(self):
        for name, value in [('pins', self.pins), ('map', self.mapping), ('leaves', self.leaves)]:
            (self.root / (name + '.json')).write_bytes(encoded(value))
        self.trust = TrustedInputs(sha(encoded(self.pins)), sha(encoded(self.mapping)), sha(encoded(self.leaves)), key_hash(self.paths), 8,
            sha(json.dumps(self.bodies, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()),
            sha(json.dumps(self.footers, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()))

    def compile(self, body_entries=True, footer_entries=True):
        self.bind_inputs()
        return PublicationOverlay.compile(self.docs, canonical_pins=self.root / 'pins.json', related_map=self.root / 'map.json',
            expected_current_leaf_manifest=self.root / 'leaves.json', trusted_inputs=self.trust,
            finite_links=self.stage, quality_module=q,
            reviewed_body_patches=self.bodies if body_entries else None,
            neutral_footer_map=self.footers if footer_entries else None, receipt_store=self.store)

    def receipt(self, value):
        raw = encoded(value)
        self.store[sha(raw)] = raw
        return sha(raw)

    def approve_fixture(self):
        # These are synthetic test receipts, never evidence about real pages.
        price_id = self.receipt({'review_kind': 'live-offer-price', 'approved': True, 'name': 'Answer Repair', 'price': '$490', 'href': 'https://broadcastwell.com/answer-repair', 'checked_on': datetime.now(timezone.utc).date().isoformat(), 'fixture_only': True})
        for footer in self.footers['pages'].values():
            footer['offer']['live_price_receipt_sha256'] = price_id
        preview = self.compile()
        for rel, record in preview.records.items():
            for kind in ['source', 'writing']:
                self.bodies['pages'][rel]['reviews'][kind] = self.receipt({'review_kind': kind, 'approved': True, 'actual_full_read_complete': True, 'scope': 'full-effective-article', 'path': rel, 'canonical_source_sha256': record['raw_canonical_source_sha256'], 'effective_canonical_source_sha256': record['effective_canonical_source_sha256'], 'fixture_only': True})
        return self.compile()

    def annotations(self, overlay):
        metadata = {'schema_version': 1, 'shape_definitions': {f'shape-{i}': f'Private test structure {i}' for i in range(8)}, 'cluster_plans': {'measurement': [f'shape-{i}' for i in range(8)]}, 'figures': {}, 'pages': {}, 'index_question_titles': self.references}
        for i, (rel, record) in enumerate(sorted(overlay.records.items())):
            figure = {'source_url': f'https://doi.org/10.1234/fixture{i}', 'record': {'subject': f'fixture-{i}', 'metric': 'retained', 'capture_date': '2026-11-01'}, 'count': str(i+1), 'base': '10', 'unit': 'events', 'label': f'Private test fact {i}', 'source_review_sha256': record['review_ids']['source']}
            figure_id = q.figure_key(figure)
            metadata['figures'][figure_id] = figure
            opening = q.paragraph_after_heading(record['body']).strip()
            metadata['pages'][rel] = {'bank_id': f'LB-Q{i+1:04d}', 'source_sha256': record['source_sha256'], 'canonical_source_sha256': record['canonical_source_sha256'], 'opening_sha256': sha(opening.encode()), 'opening_shape': f'shape-{i}', 'classification_reason': 'Synthetic explicit fixture classification.', 'source_review_sha256': record['review_ids']['source'], 'writing_review_sha256': record['review_ids']['writing'], 'lead_figures': [figure_id], 'lead_figure_spans': {figure_id: [str(i+1)]}}
        return metadata

    def qualitative_note(self, overlay, metadata, rel, record=None):
        source_record = record or {'capture_date': '2026-11-01', 'subject': 'fixture-specific-vendor', 'metric': 'one-answer-citation', 'engine': 'fixture-engine', 'question': 'q-fixture', 'run': 'one-retained-record'}
        page = overlay.records[rel]
        opening = q.paragraph_after_heading(page['body']).strip()
        binding = {'source_url': 'https://doi.org/10.1234/qualitative-fixture', 'record': source_record,
                   'source_quote': 'Exact private fixture quote representing one published record.', 'opening_span': opening,
                   'observation_key': '', 'independent_receipt_sha256': ''}
        binding['observation_key'] = qualitative_observation_key(binding, q)[0]
        binding['independent_receipt_sha256'] = self.receipt({'approved': True, 'review_kind': 'qualitative-opening-observation', 'scope': 'exact-published-observation', 'not_reworded_aggregate': True, 'path': rel, 'canonical_source_sha256': page['raw_canonical_source_sha256'], 'effective_canonical_source_sha256': page['effective_canonical_source_sha256'], 'observation_key': binding['observation_key'], 'source_quote_sha256': sha(binding['source_quote'].encode()), 'opening_span_sha256': sha(opening.encode()), 'fixture_only': True})
        overlay.receipt_store.update(self.store)
        metadata['pages'][rel].update(lead_figures=[], lead_figure_spans={}, qualitative_opening=binding)
        return binding


class OverlayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.fx = Fixture(self.temp.name)

    def test_preview_is_blocked_until_full_receipts(self):
        overlay = self.fx.compile(body_entries=False, footer_entries=False)
        self.assertTrue(overlay.pending)
        rel = self.fx.paths[0]
        body = finite_module.source_body(canonical((self.fx.docs / rel).read_bytes()))[1]
        with self.assertRaisesRegex(OverlayError, 'Publication blocked'):
            overlay.transform_after_finite94(rel, body)
        self.assertIn(QUALIFIER, overlay.transform_after_finite94(rel, body, publication=False))

    def test_complete_fixture_receipts_enable_publication(self):
        overlay = self.fx.approve_fixture()
        self.assertEqual([], overlay.pending)
        result = run_current_rendered_quality(overlay, current_annotations=self.fx.annotations(overlay), trusted_index_references_sha256=self.fx.reference_hash)
        self.assertTrue(result['passed'], result['errors'])
        rel = self.fx.paths[0]
        body = finite_module.source_body(canonical((self.fx.docs / rel).read_bytes()))[1]
        result = overlay.transform_after_finite94(rel, body)
        self.assertEqual(1, result.count(QUALIFIER))
        self.assertIn('Answer Repair: [$490](https://broadcastwell.com/answer-repair).', result)
        self.assertNotIn('For a sourced error', result)

    def test_exact_inverse_restores_each_full_input(self):
        overlay = self.fx.compile()
        for rel, record in overlay.records.items():
            body = finite_module.source_body(canonical((self.fx.docs / rel).read_bytes()))[1]
            self.assertEqual(body, invert_operations(record['body'], record['operations']))

    def test_stage_order_or_repeat_application_rejected(self):
        overlay = self.fx.approve_fixture()
        rel = self.fx.paths[0]
        with self.assertRaisesRegex(OverlayError, 'exact finite94 stage'):
            overlay.transform_after_finite94(rel, overlay.records[rel]['body'])

    def test_ordinary_source_drift_is_rejected(self):
        rel = self.fx.paths[0]
        with (self.fx.docs / rel).open('a') as stream: stream.write('\nExtra fact.\n')
        with self.assertRaisesRegex(OverlayError, 'source changed'):
            self.fx.compile()

    def test_bom_crlf_packaging_keeps_canonical_binding(self):
        rel = self.fx.paths[0]
        path = self.fx.docs / rel
        path.write_bytes(b'\xef\xbb\xbf' + path.read_bytes().replace(b'\n', b'\r\n'))
        self.assertEqual(8, len(self.fx.compile().records))

    def test_mid_build_source_and_target_drift(self):
        overlay = self.fx.compile()
        rel = self.fx.paths[0]
        body = finite_module.source_body(canonical((self.fx.docs / rel).read_bytes()))[1]
        target = self.fx.docs / 'valid-measurement.md'
        target.write_text(target.read_text() + '\nChanged chapter.\n')
        with self.assertRaisesRegex(OverlayError, 'target changed'):
            overlay.transform_after_finite94(rel, body, publication=False)

    def test_unknown_added_leaf_rejected(self):
        (self.fx.folder / 'unknown.md').write_bytes((self.fx.docs / self.fx.paths[0]).read_bytes())
        with self.assertRaisesRegex(OverlayError, 'coverage differs'):
            self.fx.compile()

    def test_missing_map_key_rejected(self):
        del self.fx.mapping['pages'][self.fx.paths[0]]
        with self.assertRaisesRegex(OverlayError, 'map coverage differs'):
            self.fx.compile()

    def test_bound_input_bytes_not_self_trusted(self):
        path = self.fx.root / 'pins.json'
        path.write_bytes(path.read_bytes() + b' ')
        with self.assertRaisesRegex(OverlayError, 'Trusted input bytes changed'):
            read_bound_json(path, self.fx.trust.canonical_pins_sha256)

    def test_duplicate_json_key_rejected(self):
        path = self.fx.root / 'duplicate.json'
        path.write_bytes(b'{"pages":{},"pages":{}}')
        with self.assertRaisesRegex(OverlayError, 'Duplicate JSON key'):
            read_bound_json(path, sha(path.read_bytes()))

    def test_research_page_cannot_substitute_for_chapter(self):
        (self.fx.docs / 'valid-measurement.md').write_text('---\ntitle: Research\npage_class: research\n---\n\n# Research\n')
        with self.assertRaisesRegex(ValueError, 'no actual page_class'):
            self.fx.compile()

    def test_wrong_hub_rejected(self):
        rel = self.fx.paths[0]
        entry = self.fx.mapping['pages'][rel]
        entry['related_markdown'] = entry['related_markdown'].replace('https://docs.broadcastwell.com/answers/measurement/', 'https://docs.broadcastwell.com/answers/other/')
        entry['related_markdown_sha256'] = sha(entry['related_markdown'].encode())
        with self.assertRaisesRegex(OverlayError, 'missing local Related target|own exact cluster hub'):
            self.fx.compile()

    def test_csv_cannot_replace_applicable_index_html(self):
        rel = self.fx.paths[0]
        entry = self.fx.mapping['pages'][rel]
        entry['required_index_href'] = 'https://index.broadcastwell.com/data/release.csv'
        entry['related_markdown'] = entry['related_markdown'].replace('https://index.broadcastwell.com/categories/crm/', entry['required_index_href'])
        entry['related_markdown_sha256'] = sha(entry['related_markdown'].encode())
        with self.assertRaisesRegex(OverlayError, 'reviewed HTML route'):
            self.fx.compile()

    def test_third_sibling_rejected(self):
        entry = self.fx.mapping['pages'][self.fx.paths[0]]
        entry['related_markdown'] = '\n\n- [Chapter](../../valid-measurement.md)\n- [Hub](index.md)\n- [Index](https://index.broadcastwell.com/categories/crm/)\n' + ''.join(f'- [Sibling {i}](fixture-{i}.md)\n' for i in [1, 2, 3]) + '\n'
        entry['related_markdown_sha256'] = sha(entry['related_markdown'].encode())
        entry['source_link_paragraph_before_related'] = 'Additional source: [Resource](../../resource.md).\n\n'
        with self.assertRaisesRegex(OverlayError, 'more than two sibling'):
            self.fx.compile()

    def test_evidence_loss_rejected(self):
        entry = self.fx.mapping['pages'][self.fx.paths[0]]
        entry['related_markdown'] += '- [Unique](https://example.test/unique)\n'
        # Inject an original unique Related source to prove actual loss detection.
        rel = self.fx.paths[0]
        path = self.fx.docs / rel
        full = canonical(path.read_bytes()).replace('- [Resource](../../resource.md)', '- [Unique](https://example.test/unique)')
        path.write_bytes(full.encode())
        body = finite_module.source_body(full)[1]
        self.fx.pins['pages'][rel]['canonical_source_sha256'] = sha(full.encode())
        self.fx.pins['pages'][rel]['post_finite94_body_sha256'] = sha(body.encode())
        self.fx.leaves['pages'][rel]['canonical_source_sha256'] = sha(full.encode())
        entry['canonical_source_sha256'] = sha(full.encode())
        entry['post_finite94_body_sha256'] = sha(body.encode())
        entry['post_finite94_related_sha256'] = sha(finite_module.related_parts(body)[1].encode())
        entry['related_markdown'] = entry['related_markdown'].replace('- [Unique](https://example.test/unique)\n', '')
        entry['related_markdown_sha256'] = sha(entry['related_markdown'].encode())
        with self.assertRaisesRegex(OverlayError, 'loses an evidence destination'):
            self.fx.compile(body_entries=False)

    def test_method_scope_change_rejected(self):
        self.fx.footers['pages'][self.fx.paths[0]]['method_token'] = '[Different method](https://example.test/method)'
        with self.assertRaisesRegex(OverlayError, 'actual method token'):
            self.fx.compile()

    def test_unverified_price_keeps_gate_closed(self):
        overlay = self.fx.compile()
        self.assertTrue(any('live-price' in item for item in overlay.pending))

    def test_receipt_bytes_or_output_reuse_rejected(self):
        self.fx.approve_fixture()
        rel = self.fx.paths[0]
        digest = self.fx.bodies['pages'][rel]['reviews']['writing']
        self.fx.store[digest] += b' '
        self.assertTrue(any(rel + ': fresh complete writing' in item for item in self.fx.compile().pending))

    def test_qualifier_exclusion_does_not_remove_adjacent_prose(self):
        body = '# Question\n\nOpening unique words.\n\n' + QUALIFIER + '\n\nOrdinary disclaimer remains fully comparable to other pages.\n'
        result = current_comparison_prose(body, q)
        self.assertNotIn(QUALIFIER, result)
        self.assertIn('Ordinary disclaimer remains fully comparable', result)
        with self.assertRaisesRegex(OverlayError, 'Exactly one'):
            remove_exact_qualifier(body + '\n' + QUALIFIER)
        with self.assertRaisesRegex(OverlayError, 'own paragraph'):
            remove_exact_qualifier(body.replace('\n\n' + QUALIFIER, '\n\nDifferent paragraph.\n\n' + QUALIFIER))

    def test_nonlibrary_content_is_identical(self):
        overlay = self.fx.compile()
        text = '<section>Research content and accessible table.</section>'
        self.assertEqual(text, overlay.transform_after_finite94('research/example.md', text))

    def test_complete_receipts_do_not_skip_machine_gate(self):
        overlay = self.fx.approve_fixture()
        rel = self.fx.paths[0]
        body = finite_module.source_body(canonical((self.fx.docs / rel).read_bytes()))[1]
        with self.assertRaisesRegex(OverlayError, 'Current rendered quality gate has not passed'):
            overlay.transform_after_finite94(rel, body)

    def test_mutated_compiled_body_cannot_reuse_receipts(self):
        overlay = self.fx.approve_fixture()
        overlay.records[self.fx.paths[0]]['body'] += '\nUnapproved body mutation.\n'
        with self.assertRaisesRegex(OverlayError, 'compiled body mutated'):
            run_current_rendered_quality(overlay, current_annotations={}, trusted_index_references_sha256=self.fx.reference_hash)

    def test_private_map_status_keeps_gate_closed(self):
        self.fx.mapping['proposal_only'] = True
        overlay = self.fx.approve_fixture()
        result = run_current_rendered_quality(overlay, current_annotations=self.fx.annotations(overlay), trusted_index_references_sha256=self.fx.reference_hash)
        self.assertFalse(result['passed'])
        self.assertTrue(any('private proposal' in str(item) for item in result['errors']))

    def test_numeric_patch_without_ledger_rejected(self):
        rel = self.fx.paths[0]
        raw_body = finite_module.source_body(canonical((self.fx.docs / rel).read_bytes()))[1]
        start, end = opening_span(raw_body)
        old, new = raw_body[start:end], raw_body[start:end].replace('of 10', 'of 11')
        entry = self.fx.bodies['pages'][rel]
        entry['patches'] = [{'start': start, 'old': old, 'new': new, 'old_sha256': sha(old.encode()), 'new_sha256': sha(new.encode()), 'fact_ledger': []}]
        entry['post_patches_body_sha256'] = sha((raw_body[:start] + new + raw_body[end:]).encode())
        with self.assertRaisesRegex(OverlayError, 'numeric/date change lacks fact ledger'):
            self.fx.compile()

    def test_duplicate_relative_absolute_destination_rejected(self):
        entry = self.fx.mapping['pages'][self.fx.paths[0]]
        entry['related_markdown'] += '- [Same chapter](https://docs.broadcastwell.com/valid-measurement/)\n'
        entry['related_markdown_sha256'] = sha(entry['related_markdown'].encode())
        with self.assertRaisesRegex(ValueError, 'duplicate Related destination'):
            self.fx.compile()

    def test_seven_related_links_rejected(self):
        entry = self.fx.mapping['pages'][self.fx.paths[0]]
        entry['related_markdown'] += '- [Extra source](https://example.test/extra)\n- [Other source](https://example.test/other)\n'
        entry['related_markdown_sha256'] = sha(entry['related_markdown'].encode())
        with self.assertRaisesRegex(ValueError, 'three to six'):
            self.fx.compile()

    def test_strict_current_gate_passes_only_clean_fixture(self):
        overlay = self.fx.approve_fixture()
        metadata = self.fx.annotations(overlay)
        with patch.object(q, 'apply_baseline', side_effect=AssertionError('Must never be called')):
            result = run_current_rendered_quality(overlay, current_annotations=metadata, trusted_index_references_sha256=self.fx.reference_hash)
        self.assertTrue(result['passed'], result['errors'])
        self.assertEqual([], result['grandfathered_cases'])

    def test_effective_annotation_rebind_required(self):
        overlay = self.fx.approve_fixture()
        metadata = self.fx.annotations(overlay)
        metadata['pages'][self.fx.paths[0]]['canonical_source_sha256'] = self.fx.pins['pages'][self.fx.paths[0]]['canonical_source_sha256']
        result = run_current_rendered_quality(overlay, current_annotations=metadata, trusted_index_references_sha256=self.fx.reference_hash)
        self.assertFalse(result['passed'])
        self.assertTrue(any('source content changed' in str(item) for item in result['errors']))

    def test_current_eight_word_violation_not_grandfathered(self):
        first, second = self.fx.paths[:2]
        phrase = 'Eight matching words must remain a real violation'
        for rel in [first, second]:
            raw_body = finite_module.source_body(canonical((self.fx.docs / rel).read_bytes()))[1]
            start, end = opening_span(raw_body)
            old, new = raw_body[start:end], raw_body[start:end] + ' ' + phrase
            entry = self.fx.bodies['pages'][rel]
            entry['patches'] = [{'start': start, 'old': old, 'new': new, 'old_sha256': sha(old.encode()), 'new_sha256': sha(new.encode()), 'fact_ledger': []}]
            entry['post_patches_body_sha256'] = sha((raw_body[:start] + new + raw_body[end:]).encode())
        overlay = self.fx.approve_fixture()
        metadata = self.fx.annotations(overlay)
        # Analyze must see the middle/end of the opening, irrespective of any
        # historical exception a raw baseline might have named.
        with patch.object(q, 'apply_baseline', side_effect=AssertionError('Must never be called')):
            result = run_current_rendered_quality(overlay, current_annotations=metadata, trusted_index_references_sha256=self.fx.reference_hash)
        self.assertFalse(result['passed'])
        self.assertTrue(any(item.get('kind') == 'eight_word_opening' for item in result['violations']))
        self.assertEqual(0, result['current_baseline_exceptions'])

    def test_current_full_body_six_word_violation_fails(self):
        first, second = self.fx.paths[:2]
        bodies = {rel: finite_module.source_body(canonical((self.fx.docs / rel).read_bytes()))[1] for rel in [first, second]}
        marker = '## What we measured\n\n'
        narrative = bodies[first].split(marker)[1].split('\n\n')[0]
        old = bodies[second].split(marker)[1].split('\n\n')[0]
        start = bodies[second].index(old)
        entry = self.fx.bodies['pages'][second]
        entry['patches'] = [{'start': start, 'old': old, 'new': narrative, 'old_sha256': sha(old.encode()), 'new_sha256': sha(narrative.encode()), 'fact_ledger': []}]
        entry['post_patches_body_sha256'] = sha((bodies[second][:start] + narrative + bodies[second][start + len(old):]).encode())
        overlay = self.fx.approve_fixture()
        result = run_current_rendered_quality(overlay, current_annotations=self.fx.annotations(overlay), trusted_index_references_sha256=self.fx.reference_hash)
        self.assertFalse(result['passed'])
        self.assertTrue(any(item['kind'] == 'six_word_similarity' for item in result['violations']))

    def test_current_lead_fourth_use_fails(self):
        overlay = self.fx.approve_fixture()
        metadata = self.fx.annotations(overlay)
        figure_id = metadata['pages'][self.fx.paths[0]]['lead_figures'][0]
        for rel in self.fx.paths[:4]:
            metadata['pages'][rel]['lead_figures'] = [figure_id]
            metadata['pages'][rel]['lead_figure_spans'] = {figure_id: ['1']}
        result = run_current_rendered_quality(overlay, current_annotations=metadata, trusted_index_references_sha256=self.fx.reference_hash)
        self.assertFalse(result['passed'])
        self.assertTrue(any(item['kind'] == 'lead_figure_limit' for item in result['violations']))

    def test_current_shape_adjacency_and_concentration_fail(self):
        overlay = self.fx.approve_fixture()
        metadata = self.fx.annotations(overlay)
        for rel in self.fx.paths[:4]:
            metadata['pages'][rel]['opening_shape'] = 'shape-0'
        result = run_current_rendered_quality(overlay, current_annotations=metadata, trusted_index_references_sha256=self.fx.reference_hash)
        self.assertFalse(result['passed'])
        self.assertTrue({'opening_adjacency', 'opening_concentration'} <= {item['kind'] for item in result['violations']})

    def test_qualitative_lead_needs_exact_independent_observation(self):
        overlay = self.fx.approve_fixture()
        metadata = self.fx.annotations(overlay)
        rel = self.fx.paths[0]
        self.fx.qualitative_note(overlay, metadata, rel)
        with patch.object(q, 'apply_baseline', side_effect=AssertionError('Must never be called')):
            result = run_current_rendered_quality(overlay, current_annotations=metadata, trusted_index_references_sha256=self.fx.reference_hash)
        self.assertTrue(result['passed'], result['errors'])
        self.assertEqual([], metadata['pages'][rel]['lead_figures'])
        metadata['pages'][rel]['qualitative_opening']['source_quote'] += ' Changed quote.'
        result = run_current_rendered_quality(overlay, current_annotations=metadata, trusted_index_references_sha256=self.fx.reference_hash)
        self.assertFalse(result['passed'])
        self.assertTrue(any('observation approval missing or stale' in str(item) for item in result['errors']))

    def test_qualitative_cannot_hide_registered_quantitative_fact(self):
        overlay = self.fx.approve_fixture()
        metadata = self.fx.annotations(overlay)
        rel = self.fx.paths[0]
        binding = self.fx.qualitative_note(overlay, metadata, rel)
        figure = next(iter(metadata['figures'].values()))
        binding['source_url'] = figure['source_url']
        binding['record'] = figure['record']
        binding['observation_key'] = qualitative_observation_key(binding, q)[0]
        result = run_current_rendered_quality(overlay, current_annotations=metadata, trusted_index_references_sha256=self.fx.reference_hash)
        self.assertFalse(result['passed'])
        self.assertTrue(any('disguises a registered aggregate' in str(item) for item in result['errors']))

    def test_qualitative_same_observation_fourth_lead_fails(self):
        overlay = self.fx.approve_fixture()
        metadata = self.fx.annotations(overlay)
        for rel in self.fx.paths[:4]:
            self.fx.qualitative_note(overlay, metadata, rel)
        result = run_current_rendered_quality(overlay, current_annotations=metadata, trusted_index_references_sha256=self.fx.reference_hash)
        self.assertFalse(result['passed'])
        self.assertTrue(any(item['kind'] == 'qualitative_lead_limit' for item in result['violations']))

    def test_effective_metadata_has_one_export_and_requires_all_consumers(self):
        rel = self.fx.paths[0]
        raw_meta = finite_module.source_body(canonical((self.fx.docs / rel).read_bytes()))[0]
        new_description = 'An approved American spelling metadata fixture.'
        self.fx.bodies['pages'][rel]['metadata_overlay'] = {'description': {'old': raw_meta['description'], 'new': new_description}}
        overlay = self.fx.approve_fixture()
        metadata = self.fx.annotations(overlay)
        self.assertEqual(new_description, overlay.effective_metadata(rel)['description'])
        exported = next(item for item in overlay.public_leaf_records() if item['path'] == rel)
        self.assertEqual(new_description, exported['description'])
        result = run_current_rendered_quality(overlay, current_annotations=metadata, trusted_index_references_sha256=self.fx.reference_hash)
        self.assertFalse(result['passed'])
        self.assertTrue(any('metadata consumer missing' in str(item) for item in result['errors']))
        with self.assertRaisesRegex(OverlayError, 'stale metadata'):
            overlay.register_metadata_consumer('llms', '0' * 64)
        fingerprint = overlay.public_metadata_fingerprint()
        for consumer in ['page-head-and-structured-data', 'library-hubs', 'llms']:
            overlay.register_metadata_consumer(consumer, fingerprint)
        result = run_current_rendered_quality(overlay, current_annotations=metadata, trusted_index_references_sha256=self.fx.reference_hash)
        self.assertTrue(result['passed'], result['errors'])

    def test_frozen_served_article_cannot_change_behind_frozen_source(self):
        overlay = self.fx.approve_fixture()
        rel = self.fx.paths[0]
        frozen_input_sha = self.fx.pins['pages'][rel]['canonical_source_sha256']
        enforce_frozen_articles(overlay, {rel: frozen_input_sha})
        result = run_current_rendered_quality(overlay, current_annotations=self.fx.annotations(overlay), trusted_index_references_sha256=self.fx.reference_hash)
        self.assertFalse(result['passed'])
        self.assertTrue(any('frozen served content would change' in str(item) for item in result['errors']))


if __name__ == '__main__':
    unittest.main()
