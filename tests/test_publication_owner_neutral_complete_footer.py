"""Owner's complete neutral footer; actual existing source-kind regressions."""
from pathlib import Path
import re
import shutil
import tempfile
import unittest

from tools import library_answers as a

ROOT = Path(__file__).resolve().parents[1]
CTA = 'Answer Repair: [$490](https://broadcastwell.com/answer-repair).'
LEGACY = '[Fix one answer, $490](https://broadcastwell.com/answer-repair)'


def body(footer=CTA):
    return '# A question?\n\nA dated reported result.\n\n## Next step\n\n' + footer + '\n\nPrepared by the Broadcastwell team.\n'


class CompleteNeutralFooterTests(unittest.TestCase):
    def rejected(self, value):
        allowed, errors = a._answer_repair_footer(value)
        self.assertFalse(allowed)
        self.assertTrue(errors)

    def test_exact_complete_neutral_line_inside_next_step(self):
        self.assertEqual((True, []), a._answer_repair_footer(body()))

    def test_pure_legacy_behavior_remains_unchanged(self):
        self.assertEqual((False, []), a._answer_repair_footer(body('For a checked fact, ' + LEGACY + '.')))

    def test_duplicate_neutral_lines_rejected(self):
        self.rejected(body(CTA + '\n\n' + CTA))

    def test_legacy_and_neutral_mixture_rejected(self):
        self.rejected(body(LEGACY + '\n\n' + CTA))

    def test_wrong_price_rejected(self):
        self.rejected(body(CTA.replace('$490', '$491')))

    def test_wrong_target_rejected(self):
        self.rejected(body(CTA.replace('/answer-repair', '/for-agencies')))

    def test_external_target_rejected(self):
        self.rejected(body(CTA.replace('https://broadcastwell.com/answer-repair', 'https://example.org/pay')))

    def test_wrong_label_rejected(self):
        self.rejected(body(CTA.replace('[$490]', '[Buy a result, $490]')))

    def test_wrong_offer_name_rejected(self):
        self.rejected(body(CTA.replace('Answer Repair:', 'Another offer:')))

    def test_prefixed_prose_is_not_a_complete_neutral_line(self):
        self.rejected(body('Use ' + CTA))

    def test_trailing_prose_is_not_a_complete_neutral_line(self):
        self.rejected(body(CTA + ' A result is guaranteed.'))

    def test_trailing_spaces_do_not_create_approved_complete_line(self):
        self.rejected(body(CTA + ' '))

    def test_neutral_line_before_next_step_rejected(self):
        self.rejected('# A question?\n\n' + CTA + '\n\n## Next step\n\nFree check.\n')

    def test_neutral_line_after_another_section_rejected(self):
        self.rejected(body('Free check.\n\n## A different section\n\n' + CTA))

    def test_missing_next_step_rejected(self):
        self.rejected(body().replace('## Next step', '## A different section'))

    def test_duplicate_next_step_rejected(self):
        self.rejected(body() + '\n## Next step\n\nMore.\n')

    def test_second_paid_footer_line_rejected(self):
        self.rejected(body(CTA + '\n\nAnother service costs $190.'))

    def test_second_own_paid_link_outside_footer_rejected(self):
        self.rejected(body().replace('A dated reported result.', 'A dated reported result.\n\nAnother service: [$990](https://broadcastwell.com/for-agencies).'))

    def test_second_answer_repair_destination_outside_footer_rejected(self):
        self.rejected(body().replace('A dated reported result.', 'A dated reported result.\n\n[Read](https://broadcastwell.com/answer-repair).'))

    def test_wrong_new_offer_does_not_hide_behind_legacy(self):
        self.rejected(body(LEGACY + '\n\n' + CTA.replace('$490', '$491')))

    def test_reported_external_vendor_price_is_not_removed_or_waived(self):
        value = body().replace('A dated reported result.', 'Reported vendor plan: $25, from its dated published page.')
        self.assertEqual((True, []), a._answer_repair_footer(value))
        self.assertIn('Reported vendor plan: $25', value)


    def test_neutral_line_after_prepared_by_rejected(self):
        self.rejected(body('Free check.') + '\n' + CTA + '\n')

    def test_neutral_line_after_owner_byline_rejected(self):
        self.rejected(body('Free check.') + '\nPage owner: Ananya Rao, AI Engineer. Corrections: hello@broadcastwell.com\n\n' + CTA + '\n')

    def test_missing_prepared_by_boundary_rejected(self):
        self.rejected(body().replace('Prepared by the Broadcastwell team.\n', ''))

    def test_duplicate_prepared_by_boundary_rejected(self):
        self.rejected(body() + '\nPrepared by the Broadcastwell team.\n')

    def test_prepared_by_before_next_step_rejected(self):
        self.rejected('# A question?\n\nPrepared by the Broadcastwell team.\n\n## Next step\n\n' + CTA + '\n')


class ExistingPublishedSourceKindsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.docs = Path(cls.temp.name) / 'docs'
        shutil.copytree(ROOT / 'docs', cls.docs)
        cls.samples = {}
        for p in sorted(a.leaf_answers(ROOT / 'docs')):
            meta, _ = a.split_markdown(p.read_text(encoding='utf8'))
            kind = meta.get('evidence_kind', 'default-index')
            cls.samples.setdefault(kind, p.relative_to(ROOT / 'docs'))
        cls.expected = {'default-index', 'published-study', 'published-audit',
                        'published-list-audit', 'published-documentation-review', 'search-console-export'}
        if not cls.expected <= set(cls.samples):
            raise AssertionError('Actual published source-kind fixtures are missing: ' + str(cls.expected - set(cls.samples)))

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def changed(self, kind):
        rel = self.samples[kind]
        original = (ROOT / 'docs' / rel).read_text(encoding='utf8')
        self.assertEqual([], a.validate_answer(ROOT / 'docs' / rel, ROOT / 'docs'))
        meta, before = a.split_markdown(original)
        paragraphs = [p for p in before.split('\n\n') if LEGACY in p]
        self.assertEqual(1, len(paragraphs))
        old = paragraphs[0]
        self.assertGreater(before.index(old), before.index('## Next step'))
        updated = original.replace(old, CTA, 1)
        self.assertEqual(original, updated.replace(CTA, old, 1))
        after_meta, after = a.split_markdown(updated)
        self.assertEqual(meta, after_meta)
        self.assertEqual(a.validate_source_evidence(meta, before, ROOT / 'docs'),
                         a.validate_source_evidence(after_meta, after, self.docs))
        target = self.docs / rel
        target.write_text(updated, encoding='utf8')
        self.assertEqual([], a.validate_answer(target, self.docs))
        return target, updated, meta, after

    def test_actual_default_index_footer_format_only(self):
        self.changed('default-index')

    def test_actual_published_study_footer_format_only(self):
        self.changed('published-study')

    def test_actual_publication_audit_footer_format_only(self):
        self.changed('published-audit')

    def test_actual_list_audit_footer_format_only(self):
        self.changed('published-list-audit')

    def test_actual_documentation_review_footer_format_only(self):
        self.changed('published-documentation-review')

    def test_actual_search_console_footer_format_only(self):
        self.changed('search-console-export')

    def test_neutral_offer_does_not_allow_unapproved_scientific_source(self):
        target, updated, _, _ = self.changed('default-index')
        text = updated.replace('https://doi.org/10.5281/zenodo.22907695', 'https://doi.org/10.5281/zenodo.99999999')
        target.write_text(text, encoding='utf8')
        self.assertTrue(any('source' in e for e in a.validate_answer(target, self.docs)))

    def test_neutral_offer_does_not_allow_wrong_method_scope(self):
        target, updated, _, after = self.changed('published-study')
        self.assertIn(a.SCOPED_METHOD_LABEL, after)
        target.write_text(updated.replace(a.SCOPED_METHOD_LABEL, a.DEFAULT_METHOD_LABEL), encoding='utf8')
        self.assertTrue(any('universal v1.1' in e for e in a.validate_answer(target, self.docs)))

    def test_neutral_offer_does_not_allow_changed_gsc_figures(self):
        target, updated, _, _ = self.changed('search-console-export')
        self.assertIn('969 impressions', updated)
        target.write_text(updated.replace('969 impressions', '970 impressions'), encoding='utf8')
        self.assertTrue(any('969 impressions' in e for e in a.validate_answer(target, self.docs)))


if __name__ == '__main__':
    unittest.main()
