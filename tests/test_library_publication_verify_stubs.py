import ast,copy,json,os,re,sys,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace

SUPPORT=Path(os.environ.get('BW_OVERLAY_SUPPORT_REPO',Path(__file__).resolve().parents[1])).resolve()
sys.path.insert(0,str(SUPPORT/'tools'))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from library_publication_overlay import sha
from library_publication_canonical_stub import POLICY,STATUS,OWNER_QUOTE_SHA256,render_canonical_stub,stub_artifact_path,SITE
from library_publication_release import route_for
from library_publication_verify_stubs import validate_stub_artifacts,reviewed_stub_pages
from library_answers import built_relative,ownership_violations,page_url


class FinalStubTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.source='answers/fixes/old-question.md';self.target='answers/fixes/current-question.md'
        self.row={'status':STATUS,'article_pass':False,'policy':POLICY,'owner_quote_sha256':OWNER_QUOTE_SHA256,
          'target_path':self.target,'target_title':'Current question','source_canonical_sha256':'a'*64,
          'decision_receipt_sha256':'b'*64,'meta_refresh_seconds':None}
        self.row['stub_html_sha256']=sha(render_canonical_stub(self.source,self.row))
        self.decision={'approved':True,'review_kind':'reviewed-source-fit-canonical-stub','source_fit_status':STATUS,
          'source_path':self.source,'target_path':self.target,'source_canonical_sha256':'a'*64,
          'owner_quote_sha256':OWNER_QUOTE_SHA256,'stub_html_sha256':self.row['stub_html_sha256'],'meta_refresh_seconds':None}
        self.overlay=SimpleNamespace(merge_statuses={self.source:self.row},records={self.target:{}},
          _check_unchanged=lambda:None,_load_receipt=lambda key:self.decision if key=='b'*64 else None)
        self.stub=self.root/stub_artifact_path(self.source);self.stub.parent.mkdir(parents=True);self.stub.write_bytes(render_canonical_stub(self.source,self.row))
        self.article=self.root/stub_artifact_path(self.target);self.article.parent.mkdir(parents=True)
        self.article.write_text('<html><head><link rel="canonical" href="'+SITE+route_for(self.target)+'"></head><body><h1>Current question</h1></body></html>',encoding='utf-8')
    def tearDown(self):self.tmp.cleanup()
    def reject(self):
        with self.assertRaises(ValueError):validate_stub_artifacts(self.overlay,self.root)
    def test_exact_reviewed_stub_and_real_target(self):
        result=validate_stub_artifacts(self.overlay,self.root)
        self.assertEqual(set(result),{self.source});self.assertIsNone(result[self.source]['http_status_observed'])
        self.assertFalse(result[self.source]['live_http_301_verified'])
    def test_inherited_map_with_no_new_merges_and_new_reviewed_target_fullhash(self):
        # The owning compiler validated the current target revision. An
        # inherited byte-identical stub retains its original exact decision;
        # this final structural check must not demand a new invented decision.
        self.overlay._new_merge_plan={}
        self.overlay.records[self.target]={'effective_canonical_source_sha256':'c'*64}
        self.decision['target_effective_canonical_sha256']='d'*64
        result=validate_stub_artifacts(self.overlay,self.root)
        self.assertEqual(set(result),{self.source})
    def test_no_inputs_never_creates_exemption(self):self.assertEqual(reviewed_stub_pages(self.root,self.root,{}),{})
    def test_partial_inputs_rejected(self):
        with self.assertRaises(ValueError):reviewed_stub_pages(self.root,self.root,{'BW_LIBRARY_PUBLICATION_INPUTS':'x'})
    def test_owner_mode_rejected_even_without_ordinary_inputs(self):
        with self.assertRaisesRegex(ValueError,'Owner repair final-stub dispatch'):reviewed_stub_pages(self.root,self.root,{'BW_OWNER_REPAIR_INPUTS':'owner.json'})
    def test_mixed_owner_mode_rejected(self):
        with self.assertRaisesRegex(ValueError,'mixed mode'):reviewed_stub_pages(self.root,self.root,{'BW_OWNER_REPAIR_INPUTS':'owner.json','BW_LIBRARY_PUBLICATION_INPUTS':'ordinary.json','BW_LIBRARY_PUBLICATION_INPUTS_SHA256':'a'*64})
    def test_empty_owner_key_still_rejected(self):
        with self.assertRaisesRegex(ValueError,'Owner repair final-stub dispatch'):reviewed_stub_pages(self.root,self.root,{'BW_OWNER_REPAIR_INPUTS_SHA256':''})
    def test_flag_alone_is_not_a_stub(self):self.row['policy']='claimed-stub';self.reject()
    def test_article_pass_claim_rejected(self):self.row['article_pass']=True;self.reject()
    def test_http301_status_rejected(self):self.row['status']='MERGED_301';self.reject()
    def test_missing_root_decision(self):self.row['decision_receipt_sha256']='c'*64;self.reject()
    def test_unapproved_root_decision(self):self.decision['approved']=False;self.reject()
    def test_arbitrary_review_kind(self):self.decision['review_kind']='article';self.reject()
    def test_wrong_decision_target(self):self.decision['target_path']='answers/fixes/other.md';self.reject()
    def test_rerouted_inherited_stub_without_new_decision(self):
        other='answers/fixes/other.md';self.overlay.records[other]={}
        self.row['target_path']=other;raw=render_canonical_stub(self.source,self.row)
        self.row['stub_html_sha256']=sha(raw);self.stub.write_bytes(raw);self.reject()
    def test_wrong_decision_source(self):self.decision['source_path']='answers/fixes/other.md';self.reject()
    def test_wrong_original_source_hash(self):self.decision['source_canonical_sha256']='c'*64;self.reject()
    def test_wrong_authority(self):self.decision['owner_quote_sha256']='c'*64;self.reject()
    def test_changed_stub_even_if_hash_replaced(self):
        raw=self.stub.read_bytes().replace(b'Read the combined answer:',b'<script>alert(1)</script>Read:')
        self.stub.write_bytes(raw);self.row['stub_html_sha256']=sha(raw);self.decision['stub_html_sha256']=sha(raw);self.reject()
    def test_unreviewed_refresh_rejected(self):
        self.row['meta_refresh_seconds']=0;self.stub.write_bytes(render_canonical_stub(self.source,self.row));self.reject()
    def test_missing_target(self):self.article.unlink();self.reject()
    def test_missing_target_registry_record(self):self.overlay.records={};self.reject()
    def test_target_chain(self):self.overlay.merge_statuses[self.target]=copy.deepcopy(self.row);self.reject()
    def test_wrong_target_canonical(self):self.article.write_text('<link rel="canonical" href="file:///private">');self.reject()
    def test_duplicate_target_canonical(self):self.article.write_text(self.article.read_text()*2);self.reject()
    def test_duplicate_canonical_attributes(self):self.article.write_text('<link rel="canonical" href="'+SITE+route_for(self.target)+'" href="https://other.test/">');self.reject()
    def test_unreviewed_alternate_html(self):
        p=self.root/(route_for(self.source).strip('/')+'.html');p.parent.mkdir(parents=True,exist_ok=True);p.write_text('alternate');self.reject()
    def test_stage_bytes_wrong_hash_reject(self):
        p=self.root/'stage.json';p.write_text('{}')
        blue=self.root/'tools/library-publication/release.json';blue.parent.mkdir(parents=True);blue.write_text(json.dumps({'schema_version':1,'approved':True,'inputs':{}}))
        with self.assertRaisesRegex(ValueError,'Trusted input bytes changed'):reviewed_stub_pages(self.root,self.root,{'BW_LIBRARY_PUBLICATION_INPUTS':str(p),'BW_LIBRARY_PUBLICATION_INPUTS_SHA256':'f'*64})
    def test_staged_scope_cannot_differ_from_approved_blueprint(self):
        inputs={'schema_version':1,'files':{'merges':{'path':'merges.json','sha256':'a'*64}},'receipt_files':[]}
        blue=self.root/'tools/library-publication/release.json';blue.parent.mkdir(parents=True);blue.write_text(json.dumps({'schema_version':1,'approved':True,'inputs':inputs}))
        altered=copy.deepcopy(inputs);altered['files']['merges']['sha256']='b'*64
        p=self.root/'stage.json';p.write_text(json.dumps(altered));pin=sha(p.read_bytes())
        with self.assertRaisesRegex(ValueError,'differ from the committed'):reviewed_stub_pages(self.root,self.root,{'BW_LIBRARY_PUBLICATION_INPUTS':str(p),'BW_LIBRARY_PUBLICATION_INPUTS_SHA256':pin})
    def test_blueprint_unapproved_reject(self):
        blue=self.root/'tools/library-publication/release.json';blue.parent.mkdir(parents=True);blue.write_text(json.dumps({'schema_version':1,'approved':False}))
        with self.assertRaisesRegex(ValueError,'Root-approved blueprint'):reviewed_stub_pages(self.root,self.root,{'BW_LIBRARY_PUBLICATION_INPUTS':'x','BW_LIBRARY_PUBLICATION_INPUTS_SHA256':'a'*64})
    def test_no_input_nonselfcanonical_still_runs_exact_ordinary_checks(self):
        # Execute the actual complete owning per-page loop, not a copied
        # imitation of its canonical check. Empty exception set cannot skip it.
        path=Path(__file__).resolve().parents[1]/'tools/verify_build.py'
        tree=ast.parse(path.read_text(encoding='utf-8'))
        funcs={'fail','front_matter','strip_tags','article_words','built_path','expected_canonical'}
        constants={'ALT_TEXT_FLOOR','BUY_ENTRY','CREDIT_LINE','AUDIT_PROMISE','RETIRED_OFFER_TEXT','TECHARTICLE_CLASSES','ARTICLE_TYPES','WORD_FLOOR_CLASSES','ISO_STAMP','CHAPTER_WORD_FLOOR','FRONT_MATTER'}
        nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in funcs or isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in constants for t in n.targets)]
        loop=next(n for n in tree.body if isinstance(n,ast.For) and isinstance(n.target,ast.Tuple) and [t.id for t in n.target.elts]==['rel','cls'])
        doc=self.root/'docs';doc.mkdir();site=self.root/'ordinary';site.mkdir()
        route=site/stub_artifact_path(self.source);route.parent.mkdir(parents=True);route.write_bytes(self.stub.read_bytes())
        ns={'re':re,'json':json,'SITE':site,'DOCS':doc,'problems':[],
          'manifest':{self.source:'page'},'canonical_stub_pages':reviewed_stub_pages(self.root,site,{}),
          'built_relative':built_relative,'ownership_violations':ownership_violations,'page_url':page_url}
        exec(compile(ast.Module(body=nodes+[loop],type_ignores=[]),str(path),'exec'),ns)
        self.assertTrue(any('canonical is '+SITE+route_for(self.target) in x for x in ns['problems']))
        self.assertTrue(any('header is missing' in x for x in ns['problems']))
        self.assertTrue(any('emits no article level JSON-LD' in x for x in ns['problems']))

if __name__=='__main__':unittest.main()
