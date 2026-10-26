"""Deployment must reject stale, foreign, mismatched or incomplete previews."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('preview', Path(__file__).parents[1] / 'tools/validate_preview.py')
preview = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preview)

class VerifiedPreviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        self.expected = {'source_head': 'h' * 40, 'source_tree': 't' * 40,
                         'repository': 'Broadcastwell/absence-manual', 'run_id': '123'}
        for name in preview.REQUIRED:
            (self.site / name).write_bytes(b'fixture')
        self.proof = self.site / 'relaunch-build-provenance.json'
        self.proof.write_text(json.dumps(self.expected), encoding='utf8')

    def test_exact_complete_artifact_is_accepted(self):
        self.assertEqual(preview.validate_preview(self.site, self.expected), self.expected)

    def test_foreign_stale_and_different_tree_artifacts_are_rejected(self):
        for key in self.expected:
            with self.subTest(key=key):
                wrong = dict(self.expected, **{key: 'other'})
                self.proof.write_text(json.dumps(wrong), encoding='utf8')
                with self.assertRaises(ValueError):
                    preview.validate_preview(self.site, self.expected)

    def test_every_required_output_is_required(self):
        for name in preview.REQUIRED:
            with self.subTest(name=name):
                path = self.site / name
                path.unlink()
                with self.assertRaises(ValueError):
                    preview.validate_preview(self.site, self.expected)
                path.write_bytes(b'fixture')

    def test_missing_and_malformed_provenance_are_rejected(self):
        self.proof.unlink()
        with self.assertRaises(FileNotFoundError):
            preview.validate_preview(self.site, self.expected)
        self.proof.write_text('not json', encoding='utf8')
        with self.assertRaises(json.JSONDecodeError):
            preview.validate_preview(self.site, self.expected)

if __name__ == '__main__':
    unittest.main()
