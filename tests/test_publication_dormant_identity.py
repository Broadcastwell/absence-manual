"""Current production stays exact; the unwired active candidate stays strict."""
from pathlib import Path
import hashlib,importlib.util,os,unittest
from unittest.mock import patch
import yaml
ROOT=Path(__file__).resolve().parents[1]


class DormantIdentityTests(unittest.TestCase):
    def test_active_candidate_is_not_wired_into_current_configuration(self):
        config=yaml.safe_load((ROOT/'mkdocs.yml').read_text())
        self.assertEqual(['tools/hooks.py','tools/performance_assets.py','tools/library_field_freeze_hook.py'],config['hooks'])
        self.assertNotIn('tools/library_publication_hooks_candidate.py',config['hooks'])
        self.assertNotIn('from_environment',(ROOT/'tools/hooks.py').read_text())
        self.assertFalse((ROOT/'tools/library_publication_release.json').exists())
        self.assertFalse((ROOT/'tools/library_publication_inputs').exists())

    def test_unwired_active_candidate_rejects_missing_pinned_inputs(self):
        path=ROOT/'tools/library_publication_hooks_candidate.py'
        spec=importlib.util.spec_from_file_location('_strict_unwired_candidate',path);candidate=importlib.util.module_from_spec(spec);spec.loader.exec_module(candidate)
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaisesRegex(ValueError,'Independently pinned prepared library inputs'):
                candidate.on_pre_build({'docs_dir':str(ROOT/'docs'),'site_dir':str(ROOT/'site')})


if __name__=='__main__':unittest.main()
