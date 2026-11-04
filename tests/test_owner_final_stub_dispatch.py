"""Owner final dispatch fixture tests; no actual producer approval claim."""
import json,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import library_owner_repair as p
import library_publication_verify_stubs as v
from test_owner_post_s5_contract import fixture,bind,raw
from library_publication_canonical_stub import stub_artifact_path

class OwnerFinalDispatchTests(unittest.TestCase):
    def test_no_inputs_preserves_no_exception_behavior(self):
        with tempfile.TemporaryDirectory() as td:self.assertEqual({},v.reviewed_stub_pages(td,td,{}))
    def test_unknown_partial_empty_and_mixed_mode_reject(self):
        for env in [{'BW_OWNER_REPAIR_OTHER':'x'},{'BW_OWNER_REPAIR_INPUTS':'x'},
                    {'BW_OWNER_REPAIR_INPUTS':'','BW_OWNER_REPAIR_INPUTS_SHA256':''},
                    {'BW_OWNER_REPAIR_INPUTS':'x','BW_OWNER_REPAIR_INPUTS_SHA256':'a'*64,'BW_LIBRARY_PUBLICATION_INPUTS':''}]:
            with self.subTest(env=env),self.assertRaises(ValueError):v.reviewed_stub_pages('.','.',env)
    def fixture(self,root):
        c,args,overlay,files,_,_=fixture();binding=bind(c,args)
        namespace=root/'tools/library-owner-repair';namespace.mkdir(parents=True)
        config=raw({'schema_version':1,'policy':p.POLICY,'fixture_only':True});(namespace/'inputs.json').write_bytes(config)
        blue={'schema_version':1,'policy':p.POLICY,'approved':True,'review_kind':'root-exact-owner-repair-inputs',
              'owner_inputs':{'path':'inputs.json','sha256':p.sha(config)},'files':{'inputs.json':p.sha(config)}}
        (namespace/'release.json').write_bytes(raw(blue));staged=root/'staged.json';staged.write_bytes(config)
        site=root/'site'
        for rel,data in files.items():target=site/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        closed=[]
        session=SimpleNamespace(overlay=overlay,post_s5_binding=binding,check_repair=lambda:None,archive=SimpleNamespace(close=lambda:closed.append(True)))
        env={'BW_OWNER_REPAIR_INPUTS':str(staged),'BW_OWNER_REPAIR_INPUTS_SHA256':p.sha(config)}
        return env,site,blue,namespace,staged,session,closed
    def test_explicit_future_owner_dispatch_closes_all19_after_load(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);env,site,_,_,_,session,closed=self.fixture(root)
            with patch('library_owner_repair_build.OwnerRepairBuildSession.load',return_value=session) as load:
                result=v.reviewed_stub_pages(root,site,env)
            self.assertEqual(19,len(result));self.assertEqual([True],closed);self.assertEqual(root/'docs',load.call_args.args[0])
            self.assertTrue(all(r['live_http_301_verified'] is False for r in result.values()))
    def test_committed_blueprint_approval_or_manifest_or_staged_bytes_reject(self):
        for mode in ['approval','manifest','staged']:
            with tempfile.TemporaryDirectory() as td:
                root=Path(td);env,site,blue,namespace,staged,session,_=self.fixture(root)
                if mode=='approval':blue['approved']=False
                if mode=='manifest':blue['files']['inputs.json']='0'*64
                if mode=='staged':staged.write_bytes(b'{}')
                (namespace/'release.json').write_bytes(raw(blue))
                with patch('library_owner_repair_build.OwnerRepairBuildSession.load',return_value=session) as load,self.assertRaises(ValueError):v.reviewed_stub_pages(root,site,env)
                load.assert_not_called()
    def test_future_owner_still_rejects_missing_decision_after_load(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);env,site,_,_,_,session,closed=self.fixture(root);session.overlay._load_receipt=lambda key:None
            with patch('library_owner_repair_build.OwnerRepairBuildSession.load',return_value=session),self.assertRaises(ValueError):v.reviewed_stub_pages(root,site,env)
            self.assertEqual([True],closed)
    def test_future_owner_still_rejects_tampered_stub_after_load(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);env,site,_,_,_,session,closed=self.fixture(root);stub=site/stub_artifact_path(next(iter(session.overlay.merge_statuses)));stub.write_bytes(stub.read_bytes()+b' ')
            with patch('library_owner_repair_build.OwnerRepairBuildSession.load',return_value=session),self.assertRaises(ValueError):v.reviewed_stub_pages(root,site,env)
            self.assertEqual([True],closed)

if __name__=='__main__':unittest.main()
