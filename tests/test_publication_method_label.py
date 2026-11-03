"""Actual source-kind validator plus synthetic full-body approval bindings."""
import copy,shutil,tempfile,unittest
from pathlib import Path
from library_publication_overlay import PublicationOverlay,sha,OverlayError,canonical
from library_publication_method_label import validate_composite_method_label
from test_publication_overlay import q,encoded,SUPPORT


class MethodFixture:
    def __init__(self,directory):
        self.repo=Path(directory);self.docs=self.repo/'docs';self.docs.mkdir();(self.repo/'tools').mkdir()
        shutil.copyfile(SUPPORT/'tools/library_answers.py',self.repo/'tools/library_answers.py')
        self.rel='answers/measurement/synthetic-method.md';self.old='[Every figure comes from the published method, v1.1.](https://broadcastwell.com/methodology)';self.new='[Our answer-study method, v1.1.](https://broadcastwell.com/methodology)'
        self.oldbody='# Synthetic question?\n\nA study observation.\n\n## What we measured\n\nThe [published study method](https://doi.org/10.5281/zenodo.23270124) retains dated statements.\n\n## What this means for you\n\nRetain the dated statement.\n\n## Next step\n\n'+self.old+'\n\nPrepared by the Broadcastwell team.\n'
        self.oldbody+='\nPage owner: Synthetic reviewer. Corrections: hello@broadcastwell.com\n'
        self.body=self.oldbody.replace(self.old,self.new)
        self.full=self.oldbody;self.payload={'effective_full_source':self.body,'body':self.body,'meta':{'evidence_kind':'published-study','is_based_on':'https://doi.org/10.5281/zenodo.23270124','evidence_method_receipts':['https://doi.org/10.5281/zenodo.23270124']},'review_ids':{}}
        self.overlay=PublicationOverlay();self.overlay.docs=self.docs;self.overlay.receipt_store={}
        for kind in ['source','writing']:
            self.payload['review_ids'][kind]=self.store({'fixture_only':True,'approved':True,'actual_full_read_complete':True,'review_kind':kind,'scope':'full-effective-article','path':self.rel,'canonical_source_sha256':sha(self.full.encode()),'effective_canonical_source_sha256':sha(self.body.encode())})
        self.decision={'fixture_only':True,'approved':True,'review_kind':'reviewed-source-specific-method-label','path':self.rel,'raw_canonical_source_sha256':sha(self.full.encode()),'before_effective_canonical_sha256':sha(self.oldbody.encode()),'effective_canonical_source_sha256':sha(self.body.encode()),'old':self.old,'new':self.new,'method_url':'https://broadcastwell.com/methodology','source_kind':'published-study','is_based_on':self.payload['meta']['is_based_on'],'source_validator_canonical_sha256':sha(canonical((self.repo/'tools/library_answers.py').read_bytes()).encode()),'full_candidate_review_ids':self.payload['review_ids']}
        self.revision={'before_effective_canonical_sha256':sha(self.oldbody.encode()),'method_token_revision':{'old':self.old,'new':self.new,'decision_receipt_sha256':self.store(self.decision)}}
    def store(self,r):
        raw=encoded(r);h=sha(raw);self.overlay.receipt_store[h]=raw;return h
    def validate(self):return validate_composite_method_label(self.overlay,self.rel,method=self.new,raw_full=self.full,post_finite_body=self.oldbody,prior_payload={'body':self.oldbody},revision=self.revision,payload=self.payload)


class MethodLabelTests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.fx=MethodFixture(self.tmp.name)
    def test_exact_reviewed_label_same_source_url_and_source_kind_passes(self):self.assertTrue(self.fx.validate())
    def test_missing_finite_label_decision_fails(self):
        self.fx.revision.pop('method_token_revision')
        with self.assertRaisesRegex(OverlayError,'Finite old/new'):self.fx.validate()
    def test_missing_full_current_writing_receipt_fails(self):
        self.fx.payload['review_ids']['writing']=None
        with self.assertRaisesRegex(OverlayError,'full-candidate writing'):self.fx.validate()
    def test_same_label_cannot_change_method_url(self):
        self.fx.new=self.fx.new.replace('/methodology','/a-different-method')
        with self.assertRaisesRegex(OverlayError,'same approved source-specific URL'):self.fx.validate()
    def test_actual_source_kind_validator_rejects_unsupported_primary_source(self):
        self.fx.payload['meta']['is_based_on']='https://doi.org/10.5281/zenodo.99999999'
        with self.assertRaisesRegex(OverlayError,'source-kind validation'):self.fx.validate()
    def test_stale_decision_validator_pin_or_body_hash_rejected(self):
        self.fx.decision['source_validator_canonical_sha256']='e'*64;self.fx.revision['method_token_revision']['decision_receipt_sha256']=self.fx.store(self.fx.decision)
        with self.assertRaisesRegex(OverlayError,'decision missing or stale'):self.fx.validate()
    def test_universal_sentence_elsewhere_in_full_study_body_still_blocks(self):
        self.fx.payload['body']+='\nEvery figure comes from the published method, v1.1.\n'
        with self.assertRaisesRegex(OverlayError,'source-kind validation'):self.fx.validate()
    def test_unchanged_actual_prior_method_requires_no_new_label_exception(self):
        self.fx.oldbody=self.fx.body;self.assertFalse(self.fx.validate())


if __name__=='__main__':unittest.main()
