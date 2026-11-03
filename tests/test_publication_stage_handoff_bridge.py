"""Fictional temporary authority bytes; real pins never relaxed in production."""
from pathlib import Path
import hashlib,importlib.util,json,os,sys,tempfile,unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('_bridge_candidate',ROOT/'tools/library_publication_stage.py')
stage=importlib.util.module_from_spec(spec);spec.loader.exec_module(stage)


class StageBridgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.docs=self.root/'a/repo/docs';self.docs.mkdir(parents=True)
        self.source=self.root/'source.md';self.raw=b'Fictional unit-test authority bytes.\r\n';self.source.write_bytes(self.raw)
        self.hash=hashlib.sha256(self.raw).hexdigest();self.target=self.root/'LIVE/FIELD_TEST_TO_LIBRARY.md'
        self.patcher=patch.object(stage,'ACCEPTED_HANDOFF_SHA256',self.hash);self.patcher.start();self.addCleanup(self.patcher.stop)

    def bridge(self,**changes):
        args={'docs':self.docs,'source':self.source,'handoff_sha256':self.hash,'registry_sha256':stage.ACCEPTED_REGISTRY_SHA256};args.update(changes)
        return stage.bridge_accepted_handoff(**args)

    def test_only_exact_bytes_copied_to_required_namespace(self):
        result=self.bridge()
        self.assertEqual(self.raw,self.target.read_bytes())
        self.assertEqual('EXACT_ACCEPTED_BYTES_COPIED',result['status'])
        self.assertEqual(self.docs.parents[2]/'LIVE/FIELD_TEST_TO_LIBRARY.md',Path(result['path']))

    def test_existing_matching_file_is_never_written_or_touched(self):
        self.target.parent.mkdir();self.target.write_bytes(self.raw);before=self.target.stat().st_mtime_ns
        original=Path.open
        def read_only(value,mode='r',*args,**kwargs):
            if any(flag in mode for flag in ['w','a','x','+']):raise AssertionError('Existing match must never be written')
            return original(value,mode,*args,**kwargs)
        with patch.object(Path,'open',read_only):result=self.bridge()
        self.assertEqual('EXISTING_MATCHING_UNTOUCHED',result['status']);self.assertEqual(before,self.target.stat().st_mtime_ns)
        self.assertEqual(self.raw,self.target.read_bytes())

    def test_conflicting_existing_file_is_not_overwritten(self):
        self.target.parent.mkdir();self.target.write_bytes(b'Different existing authority')
        with self.assertRaisesRegex(ValueError,'Conflicting existing'):self.bridge()
        self.assertEqual(b'Different existing authority',self.target.read_bytes())

    def test_existing_target_directory_is_not_replaced(self):
        self.target.mkdir(parents=True)
        with self.assertRaisesRegex(ValueError,'Conflicting existing'):self.bridge()
        self.assertTrue(self.target.is_dir())

    def test_wrong_handoff_or_registry_hash_is_rejected_before_copy(self):
        for changes in [{'handoff_sha256':'0'*64},{'registry_sha256':'1'*64}]:
            with self.subTest(changes=changes):
                with self.assertRaisesRegex(ValueError,'current accepted45'):self.bridge(**changes)
        self.assertFalse(self.target.exists())

    def test_tampered_source_bytes_are_not_copied(self):
        self.source.write_bytes(self.raw+b'changed')
        with self.assertRaisesRegex(ValueError,'source bytes changed'):self.bridge()
        self.assertFalse(self.target.exists())

    def test_parent_traversal_docs_path_rejected(self):
        with self.assertRaisesRegex(ValueError,'parent traversal'):self.bridge(docs=self.docs/'..')
        self.assertFalse(self.target.exists())

    def test_existing_parent_symlink_rejected_actual_where_supported(self):
        outside=self.root/'outside';outside.mkdir()
        try:os.symlink(outside,self.target.parent,target_is_directory=True)
        except OSError as error:self.skipTest('OS denies symlink creation: '+str(error))
        with self.assertRaisesRegex(ValueError,'symlink/junction'):self.bridge()
        self.assertFalse((outside/self.target.name).exists())

    def test_existing_symlink_target_rejected_actual_where_supported(self):
        self.target.parent.mkdir();other=self.root/'other.md';other.write_bytes(self.raw)
        try:os.symlink(other,self.target)
        except OSError as error:self.skipTest('OS denies symlink creation: '+str(error))
        with self.assertRaisesRegex(ValueError,'symlink/junction'):self.bridge()
        self.assertEqual(self.raw,other.read_bytes())

    def test_parent_junction_flag_is_rejected(self):
        self.target.parent.mkdir()
        with patch.object(Path,'is_junction',lambda value:value==self.target.parent,create=True):
            with self.assertRaisesRegex(ValueError,'symlink/junction'):self.bridge()
        self.assertFalse(self.target.exists())

    def test_parent_symlink_flag_rejected_even_without_OS_creation_privilege(self):
        self.target.parent.mkdir()
        with patch.object(Path,'is_symlink',lambda value:value==self.target.parent):
            with self.assertRaisesRegex(ValueError,'symlink/junction'):self.bridge()
        self.assertFalse(self.target.exists())

    def test_target_symlink_flag_rejected_even_without_OS_creation_privilege(self):
        self.target.parent.mkdir();self.target.write_bytes(self.raw)
        with patch.object(Path,'is_symlink',lambda value:value==self.target):
            with self.assertRaisesRegex(ValueError,'symlink/junction'):self.bridge()
        self.assertEqual(self.raw,self.target.read_bytes())

    def test_resolved_path_escape_rejected(self):
        original=Path.resolve;outside=self.root.parent/'outside-namespace.md'
        def resolve(value,*args,**kwargs):return outside if value==self.target else original(value,*args,**kwargs)
        with patch.object(Path,'resolve',resolve):
            with self.assertRaisesRegex(ValueError,'escapes'):self.bridge()
        self.assertFalse(self.target.exists())

    def cli(self,approved=True,bad_pin=False,bad_receipt=False):
        artifact=self.root/'prior.zip';artifact.write_bytes(b'Fictional artifact')
        reg=self.root/'registry.json';reg.write_text('{}')
        receipt=self.root/'receipt.json';receipt.write_text('{}')
        digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
        data={'schema_version':1,'approved':approved,'prior_artifact_sha256':digest(artifact),'inputs':{'files':{'prior_artifact':{'path':str(artifact),'sha256':digest(artifact)},'field_freeze_handoff':{'path':str(self.source),'sha256':'0'*64 if bad_pin else self.hash},'field_freeze_registry':{'path':str(reg),'sha256':digest(reg)}},'receipt_files':[{'path':str(receipt),'sha256':'0'*64 if bad_receipt else digest(receipt)}]}}
        blueprint=self.root/'blueprint.json';blueprint.write_text(json.dumps(data))
        return ['stage','--blueprint',str(blueprint),'--artifact',str(artifact),'--out',str(self.root/'out'),'--docs',str(self.docs)]

    def test_false_blueprint_never_calls_bridge(self):
        with patch.object(sys,'argv',self.cli(approved=False)),patch.object(stage,'bridge_accepted_handoff') as bridge:
            with self.assertRaisesRegex(SystemExit,'not reviewed'):stage.main()
            bridge.assert_not_called()
        self.assertFalse(self.target.exists())

    def test_any_file_or_receipt_pin_failure_never_calls_bridge(self):
        for kwargs in [{'bad_pin':True},{'bad_receipt':True}]:
            with patch.object(sys,'argv',self.cli(**kwargs)),patch.object(stage,'bridge_accepted_handoff') as bridge:
                with self.assertRaises(SystemExit):stage.main()
                bridge.assert_not_called()
        self.assertFalse(self.target.exists())

    def test_bridge_is_reached_only_after_all_approved_input_pin_checks(self):
        with patch.object(sys,'argv',self.cli()),patch.object(stage,'bridge_accepted_handoff',side_effect=RuntimeError('all checks completed')) as bridge:
            with self.assertRaisesRegex(RuntimeError,'all checks completed'):stage.main()
            bridge.assert_called_once()
        self.assertFalse(self.target.exists())


if __name__=='__main__':unittest.main()
