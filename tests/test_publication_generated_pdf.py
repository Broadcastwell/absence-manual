"""Synthetic 116-page PDFs only; no real receipt, visual claim or renderer."""
from pathlib import Path
import copy,io,json,sys,tempfile,unittest
from unittest.mock import patch
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE/'tools'))
from library_publication_generated_pdf import (PDF_PATHS,PDF_ROUTES,manual_inputs,inspect_pdf_pair,validate_reviewed_pdf_changes,linux_ci_binding)
from library_publication_overlay import sha,OverlayError
from library_publication_consumers import compare_complete_artifacts
from test_publication_release import StateFixture,q
from library_publication_release import incremental_release_gate,state_fingerprint

def pdf(date,changed_page=None,pages=116):
    from pypdf import PdfWriter
    from pypdf.generic import DictionaryObject,NameObject,DecodedStreamObject
    w=PdfWriter();font=DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')});ref=w._add_object(font)
    for n in range(1,pages+1):
        p=w.add_blank_page(width=600,height=800);text='Built '+date if n==1 else 'Synthetic manual page '+str(n)
        if n==changed_page:text+=' unsupported edit'
        stream=DecodedStreamObject();stream.set_data(('BT /F1 12 Tf 40 700 Td ('+text+') Tj ET').encode());p[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):ref})});p[NameObject('/Contents')]=w._add_object(stream)
    out=io.BytesIO();w.write(out);return out.getvalue()

class Fixture:
    def __init__(self,folder):
        self.repo=Path(folder);(self.repo/'docs/posts').mkdir(parents=True);(self.repo/'tools').mkdir()
        for rel,text in {'mkdocs.yml':'extra: {}\n','requirements.txt':'pypdf==6.19.0\n','tools/build_pdf.py':'# synthetic pinned generator fixture\n','docs/.pages':'nav: [index.md, posts, answers]\n','docs/index.md':'# Synthetic manual\n','docs/posts/note.md':'# Synthetic post\n'}.items():(self.repo/rel).write_text(text,encoding='utf-8',newline='\n')
        self.old=pdf('2026-11-02');self.new=pdf('2026-11-03');self.prior={p:self.old for p in PDF_PATHS};self.current={p:self.new for p in PDF_PATHS};self.store={};self.binding={'commit_sha':'a'*40,'deployment_id':'synthetic','artifact_sha256':'b'*64,'served_receipt_sha256':'c'*64}
        self.ci={'runner_os':'Linux','source_head':'a'*40,'checkout_commit':'d'*40,'source_tree':'e'*40,'repository':'fixture/repo','workflow_ref':'fixture/repo/.github/workflows/verify.yml@refs/pull/1/merge','run_id':'1','run_attempt':'1'}
        self.inputs=manual_inputs(self.repo);self.proof=inspect_pdf_pair(self.old,self.new)
        first={'fixture_only':True,'review_kind':'fresh-linux-manual-pdf-candidate','approval':'NONE_FACT_CAPTURE_ONLY','actual_ci':self.ci,'manual_source_and_generator_inputs':self.inputs,'prior_artifact_sha256':'b'*64,'pdf_sha256':{p:sha(self.new) for p in PDF_PATHS}}
        prior={'fixture_only':True,'approved':True,'reviewer':'root','review_kind':'prior-production-manual-source-inputs','production_binding':self.binding,'manual_source_and_generator_inputs':self.inputs}
        self.layout={'renderer':{'fixture_only':True,'name':'synthetic-raster-receipt','version':'fixture','dpi':144},'pages':{str(i):{'old_render_sha256':sha(('page'+str(i)).encode()),'new_render_sha256':sha(('changedcover' if i==1 else 'page'+str(i)).encode())} for i in range(1,117)}}
        visual={'fixture_only':True,'approved':True,'reviewer':'root','review_kind':'actual-generated-manual-cover-visual-read','old_pdf_sha256':{p:sha(self.old) for p in PDF_PATHS},'pdf_sha256':{p:sha(self.new) for p in PDF_PATHS},'only_expected_cover_build_date_changed':True,'frames':[{'filename':'fixture-old-cover.png','version':'old','sha256':self.layout['pages']['1']['old_render_sha256'],'actually_viewed':True},{'filename':'fixture-new-cover.png','version':'new','sha256':self.layout['pages']['1']['new_render_sha256'],'actually_viewed':True}]}
        self.review={'fixture_only':True,'approved':True,'reviewer':'root','review_kind':'root-reviewed-generated-manual-pdf-change','changes':{p:{'old_sha256':sha(self.old),'new_sha256':sha(self.new)} for p in PDF_PATHS},'prior_artifact_sha256':'b'*64,'unchanged_manual_source_and_generator_inputs':self.inputs,'prior_manual_source_inputs_receipt_sha256':self.add(prior),'first_linux_ci_artifact_sha256':'f'*64,'first_linux_ci_artifact_id':'123','first_linux_ci_candidate_receipt_sha256':self.add(first),'text_and_geometry_proof':self.proof,'layout_proof':self.layout,'root_changed_page_visual_receipt_sha256':self.add(visual)}
        self.bind_review()
    def add(self,obj):
        key=sha(json.dumps(obj,sort_keys=True).encode());self.store[key]=copy.deepcopy(obj);return key
    def bind_review(self):
        key=self.add(self.review);self.plan={'schema_version':1,'changes':{p:{'old_sha256':sha(self.old),'new_sha256':sha(self.new),'root_review_receipt_sha256':key} for p in PDF_PATHS}}
    def validate(self,**extra):
        args=dict(plan=self.plan,prior_files=self.prior,candidate_files=self.current,repo=self.repo,prior_artifact_sha256='b'*64,prior_production_binding=self.binding,receipt_loader=self.store.get,current_ci=self.ci);args.update(extra);return validate_reviewed_pdf_changes(**args)

class GeneratedPdfTests(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.f=Fixture(self.tmp.name)
    def test_exact_root_review_accepts_two_paths_and_binds_actual_bytes(self):
        proof=self.f.validate();self.assertEqual(PDF_ROUTES,proof.routes);proof.validate_artifacts(self.f.prior,self.f.current)
    def test_absent_review_rejects_fresh_candidate_but_identity_needs_no_exception(self):
        with self.assertRaisesRegex(OverlayError,'exact two-existing-path'):self.f.validate(plan=None)
        self.assertIsNone(self.f.validate(plan=None,candidate_files=self.f.prior))
    def test_new_pdf_path_or_other_manual_version_is_rejected(self):
        self.f.plan['changes']['another.pdf']=self.f.plan['changes'].pop('absence-manual.pdf')
        with self.assertRaisesRegex(OverlayError,'two-existing-path'):self.f.validate()
    def test_stale_or_missing_mirror_bytes_fail(self):
        self.f.current['absence-manual.pdf']+=b'changed'
        with self.assertRaisesRegex(OverlayError,'Exact reviewed PDF bytes'):self.f.validate()
    def test_review_token_cannot_be_mutated_after_independent_validation(self):
        token=self.f.validate();token.rows['absence-manual.pdf']['new_sha256']='0'*64
        with self.assertRaisesRegex(OverlayError,'proof changed after'):token.validate_artifacts(self.f.prior,self.f.current)
    def test_changed_manual_source_or_generator_fails(self):
        (self.f.repo/'tools/build_pdf.py').write_text('# changed generator\n')
        with self.assertRaisesRegex(OverlayError,'source/generator inputs'):self.f.validate()
    def test_independent_prior_manual_pins_are_required(self):
        self.f.review.pop('prior_manual_source_inputs_receipt_sha256');self.f.bind_review()
        with self.assertRaisesRegex(OverlayError,'prior-production Manual input'):self.f.validate()
    def test_non_root_or_unapproved_review_fails(self):
        self.f.review['reviewer']='another-agent';self.f.bind_review()
        with self.assertRaisesRegex(OverlayError,'Independent Root'):self.f.validate()
    def test_linux_binding_and_current_actual_environment_are_required(self):
        wrong=dict(self.f.ci,runner_os='Windows')
        with self.assertRaisesRegex(OverlayError,'Linux-CI'):self.f.validate(current_ci=wrong)
        with patch.dict('os.environ',{},clear=True):
            with self.assertRaisesRegex(OverlayError,'actual Linux GitHub'):linux_ci_binding(self.f.repo)
    def test_no_unviewed_cover_or_changed_noncover_layout(self):
        self.f.review['layout_proof']['pages']['2']['new_render_sha256']='0'*64;self.f.bind_review()
        with self.assertRaisesRegex(OverlayError,'non-cover page raster'):self.f.validate()
        self.f.review['layout_proof']['pages']['2']['new_render_sha256']=self.f.review['layout_proof']['pages']['2']['old_render_sha256'];self.f.review['root_changed_page_visual_receipt_sha256']='0'*64;self.f.bind_review()
        with self.assertRaisesRegex(OverlayError,'changed-page visual'):self.f.validate()
    def test_actual_pdf_text_may_change_only_explicit_cover_date(self):
        with self.assertRaisesRegex(OverlayError,'Unsupported Manual PDF text'):inspect_pdf_pair(self.f.old,pdf('2026-11-03',changed_page=50))
        with self.assertRaisesRegex(OverlayError,'116pages'):inspect_pdf_pair(self.f.old,pdf('2026-11-03',pages=115))
    def test_full_artifact_guard_allows_exact_pdf_proof_and_nothing_else(self):
        token=self.f.validate();prior=dict(self.f.prior,**{'manual/index.html':b'exact'});current=dict(self.f.current,**{'manual/index.html':b'exact'})
        kw=dict(prior_files=prior,candidate_files=current,changed_article_paths=set(),changed_hub_paths=set(),validated_derived_routes=set(),merged_sources={},expected_redirect_bytes=None,private_sidecars=set())
        with self.assertRaisesRegex(OverlayError,'Unrelated/nonlibrary'):compare_complete_artifacts(**kw)
        r=compare_complete_artifacts(**kw,reviewed_generated_pdf_changes=token);self.assertEqual(sorted(PDF_PATHS),r['reviewed_generated_pdf_artifacts']);self.assertTrue(r['other_nonlibrary_artifacts_byte_exact']);self.assertFalse(r['nonlibrary_artifacts_byte_exact'])
        current['another.pdf']=b'not permitted'
        with self.assertRaisesRegex(OverlayError,'another.pdf'):compare_complete_artifacts(**kw,reviewed_generated_pdf_changes=token)
    def test_two_pdf_routes_are_counted_and_can_cross_the_fifty_cap(self):
        token=self.f.validate();state_folder=self.f.repo/'state';state_folder.mkdir();fx=StateFixture(state_folder,count=55)
        # Synthetic previously published compiled PDF rows, not real production.
        for p in PDF_PATHS:fx.prior['routes']['/'+p]={'kind':'generated_pdf','compiled_sha256':sha(self.f.old)};fx.current['routes']['/'+p]={'kind':'generated_pdf','compiled_sha256':sha(self.f.new)}
        fx.prior['current_quality_snapshot']['compiled_collection_fingerprint']=state_fingerprint(fx.prior,q)
        fx.save()
        for p in fx.paths[:48]:fx.change(p)
        fx.report=fx.make_report();fx.report['validated_generated_pdf_routes']=sorted(PDF_ROUTES)
        args=dict(previous_manifest_path=fx.path,trusted_previous_sha256=fx.trusted,actual_prior_production_binding=fx.binding,candidate_state=fx.current,actual_candidate_state=fx.current,authorized_change_map=fx.map,full_current_report=fx.report,q=q,reviewed_generated_pdf_changes=token)
        r=incremental_release_gate(**args);self.assertEqual(50,r['changed_route_count']);self.assertTrue(r['incremental_release_passed'])
        fx.change(fx.paths[48]);fx.report=fx.make_report();fx.report['validated_generated_pdf_routes']=sorted(PDF_ROUTES);args['full_current_report']=fx.report
        r=incremental_release_gate(**args);self.assertEqual(51,r['changed_route_count']);self.assertFalse(r['incremental_release_passed'])
        args['reviewed_generated_pdf_changes']=None
        with self.assertRaisesRegex(OverlayError,'Root review proof'):incremental_release_gate(**args)

if __name__=='__main__':unittest.main()
