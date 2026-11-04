"""Finite activation regressions; all payloads in these tests are synthetic."""
from pathlib import Path
from types import SimpleNamespace
import copy, hashlib, json, sys, tempfile, unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import library_research_activation as activation
import library_research_activation_controls as controls
from library_research_support import sha,qsha


class ResearchActivationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def prepared(self):
        rel = '.library-research-work/inputs.json'
        body = b'{"synthetic":true}\n'
        p = self.root / controls.bundle_file(rel)
        p.parent.mkdir(parents=True); p.write_bytes(body)
        external = {'.library-research-work/prior-public.zip':'a'*64,
                    '.library-research-work/prior-source.gitLF.zip':'b'*64}
        plan = {'staged_file_sha256':{rel:sha(body), **external},
                'activation_delivery':{'external_files':external,
                    'prior_source_commit':'c'*40,'prior_artifact_id':1}}
        before = {}; after = {controls.bundle_file(rel):body}; changes = {}
        for path in controls.ACTIVATION_CODE:
            raw = ('synthetic reviewed activation ' + path).encode()
            p = self.root / path; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(raw)
            after[path] = raw
            changes[path] = {'before_sha256':None,'after_sha256':sha(raw)}
        return plan, before, after, {'reviewed_activation_source_changes':changes}

    def test_no_research_source_selects_owner(self):
        self.assertEqual('owner', activation.mode(self.root))

    def test_partial_research_source_fails_before_selection(self):
        p = self.root / activation.MODULE; p.parent.mkdir(parents=True); p.write_text('synthetic')
        with self.assertRaisesRegex(ValueError, 'Partial'):
            activation.mode(self.root)

    def test_approved_plan_without_manuscripts_selects_code_only_activation(self):
        p=self.root/activation.PLAN;p.parent.mkdir(parents=True);p.write_text('synthetic')
        with patch.object(activation,'blueprint',return_value=({},{})):
            self.assertEqual('activation',activation.mode(self.root))

    def test_identity_projection_rejects_research_or_library_changes(self):
        prior={'docs/research/a.md':b'old','docs/answers/a.md':b'unchanged'}
        current={**prior,'tools/activation.py':b'reviewed'}
        candidate={'docs/research/a.md':b'new'}
        inputs={'source_files':{'docs/research/a.md':{'after_sha256':sha(b'new')}},
                'candidate_source_inventory_sha256':qsha({p:sha(b) for p,b in sorted({**current,**candidate}.items())})}
        activation.identity_projection(prior,current,candidate,inputs)
        for path in prior:
            changed={**current,path:b'unreviewed'}
            with self.subTest(path=path),self.assertRaises(ValueError):
                activation.identity_projection(prior,changed,candidate,inputs)

    def test_exact_reviewed_activation_delta_is_finite(self):
        plan, before, after, data = self.prepared()
        actual = controls.validate_activation_delta(self.root,SimpleNamespace(plan=plan),data,before,after)
        self.assertEqual(set(after), actual)

    def test_changed_activation_code_rejected(self):
        plan, before, after, data = self.prepared()
        path = 'tools/library_research_release.py'
        after[path] += b'\nchanged'
        (self.root/path).write_bytes(after[path])
        with self.assertRaisesRegex(ValueError, 'Reviewed activation source changed'):
            controls.validate_activation_delta(self.root,SimpleNamespace(plan=plan),data,before,after)

    def test_unlisted_code_cannot_be_added_to_bridge(self):
        plan, before, after, data = self.prepared()
        data['reviewed_activation_source_changes']['docs/answers/index.md'] = {'before_sha256':None,'after_sha256':'d'*64}
        with self.assertRaisesRegex(ValueError, 'scope differs'):
            controls.validate_activation_delta(self.root,SimpleNamespace(plan=plan),data,before,after)

    def test_unlisted_control_file_rejected(self):
        plan, before, after, data = self.prepared()
        (self.root/controls.BUNDLE/'unexpected.py').write_text('synthetic unrelated code')
        with self.assertRaisesRegex(ValueError, 'unlisted files'):
            controls.validate_bundle(self.root,plan)

    def test_changed_control_bytes_rejected(self):
        plan, before, after, data = self.prepared()
        (self.root/controls.BUNDLE/'inputs.json').write_bytes(b'changed synthetic input')
        with self.assertRaisesRegex(ValueError, 'input bytes changed'):
            controls.validate_bundle(self.root,plan)

    def test_missing_control_in_candidate_archive_rejected(self):
        plan, before, after, data = self.prepared()
        del after[controls.BUNDLE+'inputs.json']
        with self.assertRaisesRegex(ValueError, 'omits or changes'):
            controls.validate_activation_delta(self.root,SimpleNamespace(plan=plan),data,before,after)

    def test_extra_external_input_rejected(self):
        plan, before, after, data = self.prepared()
        plan['activation_delivery']['external_files']['.library-research-work/foreign.zip'] = 'e'*64
        with self.assertRaisesRegex(ValueError, 'Only the exact prior'):
            controls.validate_bundle(self.root,plan)

    def test_staging_refuses_overwrite_and_traversal(self):
        activation.write_checked(self.root,'safe/input',b'first')
        with self.assertRaisesRegex(ValueError, 'Conflicting'):
            activation.write_checked(self.root,'safe/input',b'other')
        with self.assertRaisesRegex(ValueError, 'escapes'):
            activation.write_checked(self.root,'../outside',b'bad')

    def test_prior_archive_retains_container_and_requires_exact_git_files(self):
        import io,zipfile
        def zipped(data,compression):
            stream=io.BytesIO()
            with zipfile.ZipFile(stream,'w',compression=compression) as z:z.writestr('source.txt',data)
            return stream.getvalue()
        approved=zipped(b'original',zipfile.ZIP_STORED)
        regenerated=zipped(b'original',zipfile.ZIP_DEFLATED)
        ref='.library-research-work/source-archive/part-01.bin'
        p=self.root/controls.bundle_file(ref);p.parent.mkdir(parents=True);p.write_bytes(approved)
        plan={'activation_delivery':{'source_archive_parts':[ref],'prior_source_commit':'c'*40,
              'external_files':{'.library-research-work/prior-source.gitLF.zip':sha(approved)}}}
        with patch.object(activation,'git_archive',return_value=regenerated):
            self.assertEqual(approved,activation.prior_source_bytes(self.root,self.root,plan))
        with patch.object(activation,'git_archive',return_value=zipped(b'changed',zipfile.ZIP_DEFLATED)):
            with self.assertRaisesRegex(ValueError,'actual Git commit'):
                activation.prior_source_bytes(self.root,self.root,plan)
        p.write_bytes(b'changed container')
        with patch.object(activation,'git_archive',return_value=regenerated):
            with self.assertRaisesRegex(ValueError,'transport differs'):
                activation.prior_source_bytes(self.root,self.root,plan)


if __name__ == '__main__':
    unittest.main()
