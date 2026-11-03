"""Current production stays exact; the unwired active candidate stays strict."""
from pathlib import Path
import hashlib,importlib.util,os,unittest
from unittest.mock import patch
import yaml
ROOT=Path(__file__).resolve().parents[1]


class DormantIdentityTests(unittest.TestCase):
    def test_configuration_is_exact_dormant_or_exact_reviewed_claude_activation(self):
        # The code-only historical phase remains a supported exact configuration.
        # The active phase requires this finite Root-reviewed release, never a
        # catch/fallback to raw rendering or an arbitrary approved input folder.
        import json
        from pathlib import PurePosixPath, PureWindowsPath
        config=yaml.safe_load((ROOT/'mkdocs.yml').read_text())
        dormant=['tools/hooks.py','tools/performance_assets.py','tools/library_field_freeze_hook.py']
        active=['tools/library_publication_hooks_candidate.py','tools/performance_assets.py','tools/library_field_freeze_hook.py']
        self.assertNotIn('from_environment',(ROOT/'tools/hooks.py').read_text())
        self.assertFalse((ROOT/'tools/library_publication_release.json').exists())
        self.assertFalse((ROOT/'tools/library_publication_inputs').exists())
        if config['hooks']==dormant:
            self.assertNotIn('tools/library_publication_hooks_candidate.py',config['hooks'])
            return
        self.assertEqual(active,config['hooks'])
        namespace=ROOT/'tools/library-publication'
        root=ROOT.resolve()
        def safe_local(value):
            self.assertIsInstance(value,str)
            posix=PurePosixPath(value);windows=PureWindowsPath(value)
            self.assertTrue(value and '\\' not in value and not posix.is_absolute()
                            and not windows.is_absolute() and not windows.drive)
            self.assertNotIn('..',posix.parts)
            self.assertEqual(posix.as_posix(),value)
            path=namespace.joinpath(*posix.parts)
            self.assertTrue(path.resolve().is_relative_to(namespace.resolve()))
            self.assertTrue(namespace.resolve().is_relative_to(root))
            for location in [path,*path.parents]:
                self.assertFalse(location.is_symlink(),str(location))
                self.assertFalse(getattr(location,'is_junction',lambda:False)(),str(location))
                if location==ROOT:break
            return path
        release=safe_local('release.json');raw=release.read_bytes()
        self.assertEqual('082db3fc2f1af26b2c89cc9900c7503981c5d020a370876fae157aa05b2b922c',hashlib.sha256(raw).hexdigest())
        plan=json.loads(raw)
        self.assertEqual(1,plan['schema_version']);self.assertIs(plan['approved'],True)
        self.assertEqual(13228384449,plan['prior_artifact_id'])
        artifact_sha='50679ec2917536b2ead8671adcb731f9e642c94cf3af23e09c6fe4bcefc0d91c'
        self.assertEqual(artifact_sha,plan['prior_artifact_sha256'])
        inputs=plan['inputs'];self.assertEqual(326,inputs['published_count'])
        self.assertEqual(artifact_sha,inputs['actual_prior_production_binding']['artifact_sha256'])
        bound={}
        for name,row in inputs['files'].items():
            path=safe_local(row['path'])
            if name=='prior_artifact':
                # This is deliberately not a committed ZIP. The owning CI
                # downloader and stage require its actual ID/digest/bytes.
                self.assertEqual('PRIOR_ARTIFACT_DOWNLOAD_REQUIRED.zip',row['path'])
                self.assertEqual(artifact_sha,row['sha256'])
                continue
            self.assertTrue(path.is_file(),str(path))
            self.assertEqual(row['sha256'],hashlib.sha256(path.read_bytes()).hexdigest(),name)
            if path.suffix=='.json':bound[name]=json.loads(path.read_text(encoding='utf-8'))
        for row in inputs['receipt_files']:
            path=safe_local(row['path']);self.assertTrue(path.is_file(),str(path))
            self.assertEqual(row['sha256'],hashlib.sha256(path.read_bytes()).hexdigest())
        downloaded=ROOT/'reviewed-prior-publication.zip'
        if downloaded.exists():
            self.assertFalse(downloaded.is_symlink())
            self.assertEqual(artifact_sha,hashlib.sha256(downloaded.read_bytes()).hexdigest())
        expected={
            'answers/claude/does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-t.md',
            'answers/claude/how-does-claude-web-search-work.md',
            'answers/claude/which-construction-software-does-claude-recommend.md',
            'answers/claude/which-crm-software-does-claude-recommend.md',
            'answers/claude/which-dealership-software-does-claude-recommend.md',
            'answers/claude/which-dental-software-does-claude-recommend.md',
            'answers/claude/which-field-service-software-does-claude-recommend.md',
            'answers/claude/which-hotel-software-does-claude-recommend.md',
            'answers/claude/which-insurance-agency-software-does-claude-recommend.md',
            'answers/claude/which-legal-practice-software-does-claude-recommend.md',
            'answers/claude/which-loan-origination-software-does-claude-recommend.md',
            'answers/claude/which-project-management-software-does-claude-recommend.md'}
        revisions=bound['active_revisions']
        self.assertIs(revisions['approved'],True)
        self.assertEqual(expected,set(revisions['pages']))
        self.assertTrue(all(r['payload']['meta']['library_cluster']=='claude' for r in revisions['pages'].values()))
        self.assertEqual('c346b0f6a7997449f4eccbaf662b53f7ae25ba21a57341f786dc7d673db1798c',inputs['files']['field_freeze_registry']['sha256'])
        frozen={row['source_path'] for row in bound['field_freeze_registry']['rows']}
        self.assertEqual(45,len(frozen));self.assertTrue(expected.isdisjoint(frozen))
        self.assertEqual(frozen,set(inputs['frozen_effective_pins']))
        self.assertFalse(bound['merges']['merges'])
        self.assertEqual(expected,set(bound['authorized_changes']['pages']))

    def test_unwired_active_candidate_rejects_missing_pinned_inputs(self):
        path=ROOT/'tools/library_publication_hooks_candidate.py'
        spec=importlib.util.spec_from_file_location('_strict_unwired_candidate',path);candidate=importlib.util.module_from_spec(spec);spec.loader.exec_module(candidate)
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaisesRegex(ValueError,'Independently pinned prepared library inputs'):
                candidate.on_pre_build({'docs_dir':str(ROOT/'docs'),'site_dir':str(ROOT/'site')})


if __name__=='__main__':unittest.main()
