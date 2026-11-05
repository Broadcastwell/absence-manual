"""Reject unreviewed or broader follow-up releases at their real boundaries."""
import copy, hashlib, json, os, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from library_followup_release import safe_file, validate_artifacts, validate_sources, PLAN, PIN

class FollowupReleaseTests(unittest.TestCase):
    def test_a_real_observed_artifact_does_not_approve_itself(self):
        data={'artifact_review':{'approved':False},'approved_artifact_sha256':{'index.html':'new'},
              'artifact_changes':{'index.html':{'before_sha256':'old','after_sha256':'new'}}}
        with self.assertRaisesRegex(ValueError,'review is pending'):
            validate_artifacts(data,{'index.html':'old'},{'index.html':'new'})

    def test_an_approved_home_does_not_admit_an_extra_public_file(self):
        data={'artifact_review':{'approved':True},'approved_artifact_sha256':{'index.html':'new'},
              'artifact_changes':{'index.html':{'before_sha256':'old','after_sha256':'new'}}}
        with self.assertRaisesRegex(ValueError,'Whole built artifact differs'):
            validate_artifacts(data,{'index.html':'old'},{'index.html':'new','private.json':'leak'})

    def test_source_pin_cannot_hide_an_unlisted_source_change(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data={'base_commit':'base','candidate_source_sha256':{'docs/index.md':'new'},
                              'base_source_sha256':{'docs/index.md':'old'},'source_changes':{}}
            with patch('library_followup_release.source_inventory',side_effect=[data['candidate_source_sha256'],(data['base_source_sha256'],{})]):
                with self.assertRaisesRegex(ValueError,'Unlisted source change'):
                    validate_sources(root,data)

    def test_frozen_source_damage_cannot_inherit_a_finite_approval(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data={'base_commit':'base','candidate_source_sha256':{},'base_source_sha256':{},'source_changes':{}}
            with patch('library_followup_release.source_inventory',side_effect=[{},({}, {})]), patch('library_field_freeze_navigation.FrozenNavigation',side_effect=ValueError('Frozen source changed')):
                with self.assertRaisesRegex(ValueError,'Frozen source changed'):
                    validate_sources(root,data)

    def test_escaping_input_path_is_rejected_before_reading(self):
        with tempfile.TemporaryDirectory() as td:
            for path in ['../outside.json','C:/outside.json','/outside.json','nested\\outside.json']:
                with self.subTest(path=path),self.assertRaisesRegex(ValueError,'Unsafe'):
                    safe_file(Path(td),path)

    def test_final_stub_guard_rejects_partial_followup_mode(self):
        from library_publication_verify_stubs import reviewed_stub_pages
        with self.assertRaisesRegex(ValueError,'unknown, partial or mixed'):
            reviewed_stub_pages(Path('unread'),Path('unread'),{'BW_LIBRARY_FOLLOWUP_OTHER':'bad'})

    def test_final_stub_guard_rejects_mixed_followup_mode(self):
        from library_publication_verify_stubs import reviewed_stub_pages
        with self.assertRaisesRegex(ValueError,'unknown, partial or mixed'):
            reviewed_stub_pages(Path('unread'),Path('unread'),{'BW_LIBRARY_FOLLOWUP_PLAN_SHA256':'a'*64,'BW_OWNER_REPAIR_INPUTS':'bad'})

    def test_mixed_followup_and_research_modes_are_rejected(self):
        from library_build_dispatch import from_environment
        with patch.dict(os.environ,{'BW_LIBRARY_FOLLOWUP_PLAN_SHA256':'a'*64,'BW_RESEARCH_RELEASE_INPUTS':'inputs','BW_RESEARCH_RELEASE_INPUTS_SHA256':'b'*64},clear=True):
            with self.assertRaisesRegex(ValueError,'cannot mix'):
                from_environment({'docs_dir':'unread'})

if __name__=='__main__':unittest.main()
