"""Actual private owning validator, local only, no page or approval writes."""
from pathlib import Path
import importlib.util,json,os,sys,unittest
SUPPORT=Path(os.environ.get('BW_OVERLAY_SUPPORT_REPO',Path(__file__).resolve().parents[1])).resolve();sys.path[:0]=[str(SUPPORT),str(SUPPORT/'tools')]
module_path=Path(__file__).resolve().parents[1]/'tools/library_answers.py'
spec=importlib.util.spec_from_file_location('_owner_cta_candidate',module_path);candidate=importlib.util.module_from_spec(spec);spec.loader.exec_module(candidate)

CTA='Answer Repair: [$490](https://broadcastwell.com/answer-repair).'
def body(footer):return '# A question?\n\nDated publication evidence.\n\n## Next step\n\n'+footer+'\n\nPrepared by the Broadcastwell team.\n'


class OwnerNeutralCtaTests(unittest.TestCase):
    def test_exact_new_neutral_cta_inside_footer_is_allowed(self):
        self.assertEqual([],candidate._audit_unsupported_claims(body(CTA)))
    def test_legacy_raw_fixed_offer_remains_allowed_once(self):
        self.assertEqual([],candidate._audit_unsupported_claims(body('[Fix one answer, $490](https://broadcastwell.com/answer-repair)')))
    def test_same_price_in_measured_prose_still_rejected(self):
        s=body(CTA).replace('Dated publication evidence.','Dated publication evidence. '+CTA)
        self.assertTrue(candidate._audit_unsupported_claims(s))
    def test_duplicate_new_or_old_and_new_price_still_rejected(self):
        for text in [CTA+'\n\n'+CTA,'[Fix one answer, $490](https://broadcastwell.com/answer-repair)\n\n'+CTA]:
            with self.subTest(text=text):self.assertTrue(candidate._audit_unsupported_claims(body(text)))
    def test_wrong_link_price_label_or_extra_prose_not_exempt(self):
        for text in [CTA.replace('$490','$491'),CTA.replace('/answer-repair','/another-offer'),CTA.replace('Answer Repair:','A different service:'),CTA+' Extra commercial claim.','Use '+CTA]:
            with self.subTest(text=text):self.assertTrue(candidate._audit_unsupported_claims(body(text)))
    def test_other_provider_price_or_second_price_still_rejected(self):
        self.assertTrue(candidate._audit_unsupported_claims(body(CTA+'\n\nAnother supplier charges $990.')))
    def test_unchanged_outcome_ranking_prohibition_still_rejected(self):
        self.assertTrue(candidate._audit_unsupported_claims(body(CTA).replace('Dated publication evidence.','The scorecard proves the best provider.')))


if __name__=='__main__':unittest.main()
