"""Pure token/actual-text case tests; no Owner/ordinary session or Root approval."""
from pathlib import Path
from types import SimpleNamespace
import ast,copy,json,sys,tempfile,unittest
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H/'tools'))
import library_owner_composition as p

class PrimitiveTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=p.catalog();cls.rows=json.loads((H/'tests/fixtures/owner-null-method/actual24-readonly-public-text-cases.json').read_bytes())['rows']
 def setUp(self):
  self.rows=copy.deepcopy(self.__class__.rows)
  self.e={'cases24':copy.deepcopy(self.c['answer_cases24']),'prior_object_sha256':p.digest({'fixture':'prior'}),
   'payload_object_sha256':p.digest({'fixture':'payload'}),'active_object_sha256':p.digest({'fixture':'active'}),
   'production_binding':{'fixture':'No actual production authority'},'frozen_paths45':sorted('fixture-frozen-'+str(i) for i in range(45))}
  # Tests exercise the module-private constructor only. No public binder is
  # called; the fixture stubs are not OwnerPlan/PostS5 approvals or receipts.
  self.token=p.OwnerNullMethodPermit(self.e,[],SimpleNamespace(assert_current=lambda:None),SimpleNamespace(check=lambda:None),p._TOKEN)
 def check(self,path):
  r=self.rows[path];return p.check_case(path,r['before'],r['revision'],r['readiness'],r['scoped_ids'],r['ordinary_ids'],r['ledger_sha256'])
 def test_all_actual24_exact_cases_and_five_only_nullable(self):
  for path in self.rows:self.assertEqual(self.c['answer_cases24'][path],self.check(path))
  self.assertEqual(5,len(self.c['inherited_null_method5']));self.assertEqual(22,len(self.c['prior_FAIL22']))
 def test_public_dict_flag_or_wrong_constructor_token_cannot_issue(self):
  with self.assertRaises(ValueError):p.OwnerNullMethodPermit(self.e,[],None,None,object())
  self.assertIsNot(type({}),p.OwnerNullMethodPermit);self.assertIsNot(type(True),p.OwnerNullMethodPermit)
 def test_exactfive_can_be_consumed_and_complete(self):
  for path in self.c['inherited_null_method5']:
   r=self.rows[path];self.token.admit_inherited_null(path,r['before'],r['revision'])
  self.token.assert_complete()
 def test_missing_five_consumption_rejects(self):
  with self.assertRaises(ValueError):self.token.assert_complete()
 def test_all17_otherFAIL_and_twoPASS_cannot_use_null_permit(self):
  for path in set(self.rows)-set(self.c['inherited_null_method5']):
   r=self.rows[path]
   with self.subTest(path=path),self.assertRaises(ValueError):self.token.admit_inherited_null(path,r['before'],r['revision'])
 def test_footer_object_span_or_afterhash_change_rejects(self):
  path=self.c['inherited_null_method5'][0];r=self.rows[path]
  for mode in ['contract','span','after']:
   revision=copy.deepcopy(r['revision'])
   if mode=='contract':revision['payload']['footer_contract']['extra']='changed'
   elif mode=='span':revision['payload']['body']=revision['payload']['body'].replace('Prepared by the Broadcastwell team.','Altered footer.')
   else:revision['payload']['effective_full_source']+='\nAltered.'
   with self.subTest(mode=mode),self.assertRaises(ValueError):self.token.admit_inherited_null(path,r['before'],revision)
 def test_none_to_string_or_int_is_not_an_inherited_null_admission(self):
  path=self.c['inherited_null_method5'][0];r=self.rows[path]
  for method in ['[Other](https://example.org/)',42,False]:
   revision=copy.deepcopy(r['revision']);revision['payload']['footer_contract']['method_token']=method
   with self.subTest(method=method),self.assertRaises(ValueError):self.token.admit_inherited_null(path,r['before'],revision)
 def test_context_before_payload_active_binding_or_freeze_mismatch_rejects(self):
  good={'prior':{'fixture':'prior'},'payload_bundle':{'fixture':'payload'},'active_plan':{'fixture':'active'},
   'actual_binding':self.e['production_binding'],'frozen_paths':self.e['frozen_paths45']}
  self.token.assert_context(**good)
  for key in good:
   bad=copy.deepcopy(good);bad[key]=[] if key=='frozen_paths' else {'foreign':'value'}
   with self.subTest(key=key),self.assertRaises(ValueError):self.token.assert_context(**bad)
 def test_mutated_token_evidence_or_bound_file_rejects(self):
  self.token._evidence['cases24']={}
  with self.assertRaises(ValueError):self.token.assert_current()
  with tempfile.TemporaryDirectory(dir=H) as t:
   f=Path(t)/'fixture';f.write_bytes(b'exact')
   token=p.OwnerNullMethodPermit(self.e,[(str(f),p.sha(b'exact'))],SimpleNamespace(assert_current=lambda:None),SimpleNamespace(check=lambda:None),p._TOKEN)
   f.write_bytes(b'changed')
   with self.assertRaises(ValueError):token.assert_current()
 def test_peer_ledger_status_sourcekind_or_basis_change_rejects(self):
  path=self.c['inherited_null_method5'][0];old=copy.deepcopy(self.rows[path])
  for mode in ['peer','ledger','status','kind','basis']:
   self.rows[path]=copy.deepcopy(old);r=self.rows[path]
   if mode=='peer':r['scoped_ids']['source']='0'*64
   elif mode=='ledger':r['ledger_sha256']='0'*64
   elif mode=='status':r['readiness']['status']='PASS';r['readiness']['passed']=True
   elif mode=='kind':r['revision']['payload']['source_kind']='foreign-kind'
   else:r['revision']['payload']['meta']['is_based_on']='https://example.org/foreign'
   with self.subTest(mode=mode),self.assertRaises(ValueError):self.check(path)
 def test_priorPASS_cannot_replace_distinct_ordinary_with_scoped(self):
  for path in self.c['ordinary_prior_PASS2']:
   r=self.rows[path];r['ordinary_ids']=r['scoped_ids']
   with self.subTest(path=path),self.assertRaises(ValueError):self.check(path)
 def test_explicit_Root_review_boolean_alone_or_stale_digest_cannot_authorize(self):
  good={'approved':True,'reviewer':'root','review_kind':'root-exact-owner-inherited-null5-composition',
   'policy':p.POLICY,'composition_evidence_sha256':p.digest(self.e),'ordinary_S5_or_footer_validity_approval':False}
  self.assertTrue(p.check_Root_review(good,self.e))
  for key,value in [('approved',False),('review_kind','ordinary-full-S5'),('composition_evidence_sha256','0'*64),('ordinary_S5_or_footer_validity_approval',True)]:
   with self.subTest(key=key),self.assertRaises(ValueError):p.check_Root_review({**good,key:value},self.e)
 def test_core_added_condition_is_only_None_AND_typed_permit_and_strings_still_validate(self):
  source=(H/'tools/library_publication_composition.py').read_text();tree=ast.parse(source)
  node=next(n for n in ast.walk(tree) if isinstance(n,ast.If) and isinstance(n.test,ast.BoolOp)
   and 'method is None' in ast.unparse(n.test) and 'owner_composition_permit is not None' in ast.unparse(n.test))
  self.assertEqual(ast.unparse(node.test),'method is None and owner_composition_permit is not None')
  self.assertFalse(any(isinstance(n,ast.Try) for n in ast.walk(node)))
  calls=[n for n in ast.walk(ast.Module(body=node.orelse,type_ignores=[])) if isinstance(n,ast.Call)]
  self.assertTrue(any(isinstance(n.func,ast.Name) and n.func.id=='validate_composite_method_label' for n in calls))
  self.assertTrue(any(isinstance(n.func,ast.Name) and n.func.id=='require' for n in calls))
  self.assertIn("for issue in neutral_footer_issues(self,rel,record,payload.get('footer_contract')):",source)
 def test_owner_binds_before_super_and_ordinary_default_is_None(self):
  source=(H/'tools/library_owner_repair_build.py').read_text()
  self.assertLess(source.index('owner_composition_permit=bind_owner_composition'),source.index('self=super().load'))
  self.assertIn('owner_composition_permit=None',(H/'tools/library_publication_build.py').read_text())

if __name__=='__main__':unittest.main(verbosity=2)
