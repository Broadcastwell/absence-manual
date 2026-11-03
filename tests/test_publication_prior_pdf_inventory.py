"""Actual published PR83 PDF-byte inventory slice, never a producer approval."""
from pathlib import Path
import copy,json,sys,unittest
from types import SimpleNamespace
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE/'tools'))
from library_publication_overlay import sha,OverlayError
from library_publication_composition import bind_prior_content
from library_publication_generated_pdf import PDF_ROUTES,validate_reviewed_pdf_changes

class PriorPdfInventoryTests(unittest.TestCase):
    def setUp(self):
        fixture=HERE/'tests/fixtures/generated-pdf-inventory';self.source=json.loads((fixture/'SOURCE.json').read_text(encoding='utf-8'));self.pdf=(fixture/'pr83-published-manual.pdf').read_bytes()
        self.assertEqual('e5a0db7f26329b6b18ef8bf71ac8e83ff07379be807673965d870f0f3cf8f653',sha(self.pdf))
        self.assertEqual('d808ded453712bd6330eb0f52baf97fcb345d684abc195d5852cbe50ecddcc17',self.source['actual_official_artifact_sha256'])
        self.prior={'routes':copy.deepcopy(self.source['inventory_unit_rows_for_actual_existing_paths'])};self.actual={route:self.pdf for route in self.prior['routes']};self.q=SimpleNamespace(canonical_json=lambda v:json.dumps(v,sort_keys=True,separators=(',',':')))
    def bind(self):return bind_prior_content(prior=self.prior,payloads={},actual_artifacts=self.actual,q=self.q)
    def test_exact_actual_existing_two_PDF_rows_bind_without_any_approval_receipt(self):
        self.assertEqual(PDF_ROUTES,set(self.prior['routes']));self.assertIsNone(self.bind());self.assertFalse(self.source['approved_new_PDF_receipt_created'])
    def test_registered_actual_PDF_hash_is_not_waived(self):
        self.prior['routes']['/absence-manual.pdf']['compiled_sha256']='0'*64
        with self.assertRaisesRegex(OverlayError,'actual compiled bytes changed'):self.bind()
    def test_changed_actual_bytes_are_not_waived(self):
        self.actual['/absence-manual.pdf']+=b'\n% negative-test mutation only\n'
        with self.assertRaisesRegex(OverlayError,'actual compiled bytes changed'):self.bind()
    def test_new_or_different_version_path_is_rejected_even_with_same_actual_bytes(self):
        for path in ['/another.pdf','/absence-manual-v2.0-2026-11-03.pdf','/Absence-manual.pdf']:
            old=copy.deepcopy(self.prior);self.prior['routes'][path]={'kind':'generated_pdf','compiled_sha256':sha(self.pdf)};self.actual[path]=self.pdf
            with self.assertRaisesRegex(OverlayError,'exact existing Manual paths only'):self.bind()
            self.prior=old;self.actual.pop(path)
    def test_partial_registered_pair_or_missing_actual_artifact_is_rejected(self):
        row=self.prior['routes'].pop('/absence-manual.pdf')
        with self.assertRaisesRegex(OverlayError,'both exact existing'):self.bind()
        self.prior['routes']['/absence-manual.pdf']=row;self.actual.pop('/absence-manual.pdf')
        with self.assertRaisesRegex(OverlayError,'route-byte inventory differs'):self.bind()
    def test_unsupported_row_cannot_carry_an_inventory_exception(self):
        self.prior['routes']['/absence-manual.pdf']['unsupported_extra_field']='not an approval'
        with self.assertRaisesRegex(OverlayError,'Unsupported generated PDF inventory row'):self.bind()
    def test_extra_actual_PDF_not_registered_is_rejected(self):
        self.actual['/unregistered.pdf']=self.pdf
        with self.assertRaisesRegex(OverlayError,'route-byte inventory differs'):self.bind()
    def test_inventory_binding_does_not_authorize_changed_PDFs(self):
        self.bind();old={p.lstrip('/'):self.pdf for p in PDF_ROUTES};new={p:raw+b'\n% negative-test mutation\n' for p,raw in old.items()}
        with self.assertRaisesRegex(OverlayError,'exact two-existing-path review plan'):
            validate_reviewed_pdf_changes(plan=None,prior_files=old,candidate_files=new,repo=HERE,prior_artifact_sha256=self.source['actual_official_artifact_sha256'],prior_production_binding=None,receipt_loader=lambda digest:None)

if __name__=='__main__':unittest.main()
