"""Finite repair regressions, including all reviewed real sources and MkDocs bodies."""
from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from types import SimpleNamespace
import unittest

from mkdocs.utils import meta as mkdocs_meta


ROOT = Path(__file__).resolve().parents[1]
REPO = Path(os.environ.get('BW_CHAPTER_REPAIR_TEST_REPO', str(ROOT))).resolve()
DOCS = REPO / 'docs'
MAP = ROOT / 'tools/library_related_chapters.json'


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


repair = load_module('related_chapters_under_test', ROOT / 'tools/library_related_chapter_links.py')


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.docs = Path(self.temp.name).resolve()
        self.key = 'answers/testing/example.md'
        self.source = self.docs / self.key
        self.source.parent.mkdir(parents=True)
        self.chapter = self.docs / 'one.md'
        self.chapter.write_text('---\npage_class: chapter\ntitle: One\n---\n# One\n', encoding='utf-8')
        self.text = (
            '---\npage_class: page\nlibrary_cluster: testing\ntitle: Example\n---\n\n'
            '# Example\n\nAn answer and its [retained source](https://vendor.example/keep).\n\n'
            '## What we measured\n\nA dated figure, 4 of 5, on 6 October 2026.\n\n'
            '## What this means for you\n\nKeep this exact paragraph.\n\n'
            '## Also asked as\n\nOriginal question?\n\n## Related\n\n'
            '- [Existing](https://vendor.example/keep)\n'
            '- [Evidence](https://vendor.example/data)\n'
            '- [Other](https://other.example/)\n\n'
            '## Next step\n\nFree first. Then repair.\n\nOwner and footer unchanged.\n')
        self.write_source(self.text)

    def write_source(self, text):
        self.source.write_bytes(text.encode('utf-8'))

    def entry(self, action='append'):
        text = repair.canonical_source(self.source.read_bytes())
        _, body = repair.source_body(text)
        _, section, _ = repair.related_parts(body)
        entry = {'canonical_source_sha256': repair.digest(text.encode()),
                 'related_section_sha256': repair.digest(section.encode()),
                 'chapter_path': 'one.md', 'label': 'The Manual chapter', 'action': action}
        if action == 'replace':
            entry.update(replace_label='Existing', replace_href='https://vendor.example/keep')
        return entry

    def compiled(self, entry=None):
        return repair.validate_entry(self.key, entry or self.entry(), self.docs)

    def runtime(self, compiled=None):
        # Unit fixture only: production constructor always validates the pinned94 map.
        runtime = object.__new__(repair.FiniteChapterLinks)
        runtime.docs = self.docs
        runtime.entries = {self.key: compiled or self.compiled()}
        return runtime

    def test_append_changes_only_related_and_keeps_source_bytes(self):
        before = self.source.read_bytes()
        compiled = self.compiled()
        body, _ = mkdocs_meta.get_data(repair.canonical_source(before))
        result = self.runtime(compiled).transform(self.key, body)
        prefix, section, suffix = repair.related_parts(body)
        out_prefix, out_section, out_suffix = repair.related_parts(result)
        self.assertEqual(prefix, out_prefix)
        self.assertEqual(suffix, out_suffix)
        self.assertEqual(4, len(repair.related_links(out_section)))
        self.assertIn('- [The Manual chapter](../../one.md)', out_section)
        self.assertEqual(before, self.source.read_bytes())

    def test_replace_retains_exact_original_inline_link(self):
        compiled = self.compiled(self.entry('replace'))
        result = self.runtime(compiled).transform(self.key, compiled['_body'])
        prefix, section, suffix = repair.related_parts(result)
        self.assertIn('[retained source](https://vendor.example/keep)', prefix)
        self.assertNotIn('[Existing](https://vendor.example/keep)', section)
        self.assertIn('[The Manual chapter](../../one.md)', section)
        self.assertEqual(3, len(repair.related_links(section)))
        self.assertTrue(suffix.endswith('Owner and footer unchanged.\n'))

    def test_crlf_and_bom_pin_and_runtime_preserve_outside_bytes(self):
        self.source.write_bytes(b'\xef\xbb\xbf' + self.text.replace('\n', '\r\n').encode())
        compiled = self.compiled()
        body = compiled['_body'].replace('\n', '\r\n')
        result = self.runtime(compiled).transform(self.key, body)
        before = repair.related_parts(body)
        after = repair.related_parts(result)
        self.assertEqual(before[0].encode(), after[0].encode())
        self.assertEqual(before[2].encode(), after[2].encode())

    def test_stale_full_source_even_when_related_is_unchanged(self):
        entry = self.entry()
        self.write_source(self.text.replace('Keep this exact paragraph.', 'Changed paragraph.'))
        with self.assertRaisesRegex(ValueError, 'stale full source'):
            self.compiled(entry)

    def test_missing_source_rejected_before_any_page_transform(self):
        entry = self.entry()
        self.source.unlink()
        with self.assertRaisesRegex(ValueError, 'missing or escaped answer path'):
            self.compiled(entry)

    def test_separate_related_pin_cannot_be_forged_by_full_source_pin(self):
        entry = self.entry()
        self.write_source(self.text.replace('[Other]', '[Changed]'))
        entry['canonical_source_sha256'] = repair.digest(repair.canonical_source(self.source.read_bytes()).encode())
        with self.assertRaisesRegex(ValueError, 'stale Related'):
            self.compiled(entry)

    def test_source_changed_after_prebuild_is_rejected(self):
        runtime = self.runtime()
        body = runtime.entries[self.key]['_body']
        self.write_source(self.text.replace('Original question?', 'Different question?'))
        with self.assertRaisesRegex(ValueError, 'source changed after pre-build'):
            runtime.transform(self.key, body)

    def test_chapter_changed_after_prebuild_is_rejected(self):
        runtime = self.runtime()
        self.chapter.write_text('---\npage_class: chapter\n---\nChanged chapter\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'chapter changed after pre-build'):
            runtime.transform(self.key, runtime.entries[self.key]['_body'])

    def test_altered_mkdocs_body_cannot_borrow_a_valid_source_pin(self):
        runtime = self.runtime()
        with self.assertRaisesRegex(ValueError, 'MkDocs input differs'):
            runtime.transform(self.key, runtime.entries[self.key]['_body'].replace('exact paragraph', 'other paragraph'))

    def test_wrong_replacement_label_is_not_normalized(self):
        entry = self.entry('replace')
        entry['replace_label'] = 'existing'
        with self.assertRaisesRegex(ValueError, 'exactly one original'):
            self.compiled(entry)

    def test_replacement_href_must_be_a_real_inline_link_before_related(self):
        self.write_source(self.text.replace('[retained source](https://vendor.example/keep)', 'https://vendor.example/keep'))
        with self.assertRaisesRegex(ValueError, 'remain linked inline'):
            self.compiled(self.entry('replace'))

    def test_replacement_link_after_related_does_not_count_as_inline_proof(self):
        self.write_source(self.text.replace('[retained source](https://vendor.example/keep)', 'source') + '\n[Later](https://vendor.example/keep)\n')
        with self.assertRaisesRegex(ValueError, 'remain linked inline'):
            self.compiled(self.entry('replace'))

    def test_duplicate_chapter_absolute_and_relative_routes_rejected(self):
        self.write_source(self.text.replace('https://other.example/', 'https://docs.broadcastwell.com/one/'))
        with self.assertRaisesRegex(ValueError, 'duplicate Related'):
            self.compiled()

    def test_overflow_and_underflow_are_rejected(self):
        self.write_source(self.text.replace('## Next step', '- [Fourth](https://four.example/)\n- [Fifth](https://five.example/)\n- [Sixth](https://six.example/)\n\n## Next step'))
        with self.assertRaisesRegex(ValueError, 'three to six'):
            self.compiled()
        self.write_source(self.text.replace('- [Evidence](https://vendor.example/data)\n', '').replace('- [Other](https://other.example/)\n', ''))
        with self.assertRaisesRegex(ValueError, 'three to six'):
            self.compiled()

    def test_markdown_and_unicode_line_break_labels_are_rejected(self):
        for label in ['[bad](https://evil.example)', '**bad**', '<b>bad</b>', 'bad\nline', 'bad\u2028line', 'bad\u2029line']:
            with self.subTest(label=repr(label)):
                entry = self.entry()
                entry['label'] = label
                with self.assertRaises(ValueError):
                    self.compiled(entry)

    def test_source_path_traversal_absolute_windows_and_encoded_paths(self):
        for path in ['../example.md', '/answers/testing/example.md', 'C:/example.md', 'answers/testing/../example.md', 'answers\\testing\\example.md', 'answers/testing/%2e%2e.md']:
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, 'unsafe answer path'):
                repair.validate_entry(path, self.entry(), self.docs)

    def test_missing_external_traversal_and_nonchapter_targets(self):
        for target in ['missing.md', 'https://external.example/chapter.md', '../one.md', '/one.md']:
            with self.subTest(target=target):
                entry = self.entry()
                entry['chapter_path'] = target
                with self.assertRaises(ValueError):
                    self.compiled(entry)
        self.chapter.write_text('---\npage_class: page\n---\nA resource, not a chapter.\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'not a Manual chapter'):
            self.compiled()

    def test_unknown_entry_field_and_action_are_rejected(self):
        for patch in [{'escape': True}, {'action': 'delete'}]:
            entry = self.entry()
            entry.update(patch)
            with self.assertRaises(ValueError):
                self.compiled(entry)

    def test_root_relative_and_source_routes_share_identity_only_if_existing(self):
        root = repair.href_identity('/answers/testing/example/', self.source, self.docs)
        relative = repair.href_identity('example.md', self.source, self.docs)
        absolute = repair.href_identity('https://docs.broadcastwell.com/answers/testing/example/', self.source, self.docs)
        self.assertEqual(root, relative)
        self.assertEqual(root, absolute)

    def test_distinct_external_and_local_fragments_are_not_duplicates(self):
        self.assertNotEqual(repair.href_identity('https://vendor.example/page#webfx', self.source, self.docs),
                            repair.href_identity('https://vendor.example/page#scorecard', self.source, self.docs))
        self.assertNotEqual(repair.href_identity('../../one.md#first', self.source, self.docs),
                            repair.href_identity('https://docs.broadcastwell.com/one/#second', self.source, self.docs))

    def test_global_guard_rejects_missing_related_chapter_on_unmapped_leaf(self):
        body, _ = mkdocs_meta.get_data(repair.canonical_source(self.source.read_bytes()))
        with self.assertRaisesRegex(ValueError, 'no actual page_class: chapter'):
            repair.validate_answer_related_chapter(body, self.source, self.docs)
        runtime = self.runtime()
        runtime.entries = {}
        with self.assertRaisesRegex(ValueError, 'no actual page_class: chapter'):
            runtime.transform(self.key, body)

    def test_global_guard_does_not_count_inline_chapter(self):
        self.write_source(self.text.replace('Keep this exact paragraph.',
                                           'Keep this [inline Manual chapter](../../one.md).'))
        body, _ = mkdocs_meta.get_data(repair.canonical_source(self.source.read_bytes()))
        with self.assertRaisesRegex(ValueError, 'no actual page_class: chapter'):
            repair.validate_answer_related_chapter(body, self.source, self.docs)

    def test_global_guard_rejects_appendix_page_and_research_as_chapter(self):
        self.write_source(self.text.replace('https://other.example/', '../../one.md'))
        body, _ = mkdocs_meta.get_data(repair.canonical_source(self.source.read_bytes()))
        for page_class in ['appendix', 'page', 'research']:
            self.chapter.write_text('---\npage_class: ' + page_class + '\n---\n# Resource\n', encoding='utf-8')
            with self.subTest(page_class=page_class), self.assertRaisesRegex(ValueError, 'no actual page_class: chapter'):
                repair.validate_answer_related_chapter(body, self.source, self.docs)

    def test_global_guard_accepts_real_chapter_without_changing_unmapped_body(self):
        self.write_source(self.text.replace('https://other.example/', '../../one.md#one'))
        body, _ = mkdocs_meta.get_data(repair.canonical_source(self.source.read_bytes()))
        self.assertEqual((self.chapter,), repair.validate_answer_related_chapter(body, self.source, self.docs))
        runtime = self.runtime()
        runtime.entries = {}
        self.assertEqual(body, runtime.transform(self.key, body))

    def test_global_guard_enforces_link_count_on_unmapped_pages(self):
        text = self.text.replace('https://other.example/', '../../one.md')
        too_few = text.replace('- [Evidence](https://vendor.example/data)\n', '')
        too_many = text.replace('## Next step', '- [Four](https://four.example/)\n- [Five](https://five.example/)\n- [Six](https://six.example/)\n- [Seven](https://seven.example/)\n\n## Next step')
        for value in [too_few, too_many]:
            body, _ = mkdocs_meta.get_data(value)
            with self.assertRaisesRegex(ValueError, 'three to six'):
                repair.validate_answer_related_chapter(body, self.source, self.docs)

    def test_nonanswer_pages_and_cluster_index_are_not_global_guard_leaves(self):
        runtime = self.runtime()
        for key in ['answers/testing/index.md', 'research/example.md', 'one.md']:
            with self.subTest(key=key):
                self.assertEqual('# Unrelated page\n', runtime.transform(key, '# Unrelated page\n'))


class ReviewedMap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = MAP.read_bytes()
        cls.mapping = json.loads(cls.raw.decode('utf-8-sig'))
        cls.runtime = repair.FiniteChapterLinks(DOCS, MAP)

    def test_all94_actual_mkdocs_bodies_and_all150_frozen_sources_unchanged(self):
        baseline_path = REPO / 'tools/library_quality_baseline.json'
        baseline_raw = baseline_path.read_bytes()
        baseline = json.loads(baseline_raw)
        before = {key: (DOCS / key).read_bytes() for key in baseline['frozen_pages']}
        self.assertEqual(150, len(before))
        self.assertEqual(94, len(self.runtime.entries))
        for key, entry in self.runtime.entries.items():
            with self.subTest(key=key):
                body, _ = mkdocs_meta.get_data(repair.canonical_source(entry['_source'].read_bytes()))
                changed = self.runtime.transform(key, body)
                prefix, _, suffix = repair.related_parts(body)
                out_prefix, out_section, out_suffix = repair.related_parts(changed)
                self.assertEqual(prefix.encode(), out_prefix.encode())
                self.assertEqual(suffix.encode(), out_suffix.encode())
                self.assertTrue(3 <= len(repair.related_links(out_section)) <= 6)
                self.assertIn('](' + entry['_chapter_href'] + ')', out_section)
        self.assertEqual(before, {key: (DOCS / key).read_bytes() for key in before})
        self.assertEqual(baseline_raw, baseline_path.read_bytes())

    def test_all_actual_library_leaves_pass_global_guard_after_finite_transform(self):
        annotations = json.loads((REPO / 'tools/library_quality_annotations.json').read_text(encoding='utf-8-sig'))
        sources = sorted(path for path in (DOCS / 'answers').glob('*/*.md') if path.name != 'index.md')
        keys = {path.relative_to(DOCS).as_posix() for path in sources}
        self.assertEqual(keys, set(annotations['pages']))
        self.assertEqual(keys, set(self.runtime.validated_answer_leaves))
        before = {str(path): path.read_bytes() for path in sources}
        for source in sources:
            key = source.relative_to(DOCS).as_posix()
            body, _ = mkdocs_meta.get_data(repair.canonical_source(source.read_bytes()))
            result = self.runtime.transform(key, body)
            with self.subTest(key=key):
                chapters = repair.validate_answer_related_chapter(result, source, DOCS)
                self.assertTrue(chapters)
                if key not in self.runtime.entries:
                    self.assertEqual(body.encode(), result.encode())
        self.assertEqual(before, {str(path): path.read_bytes() for path in sources})

    def test_prebuild_collection_rejects_a_new_unmapped_leaf_without_chapter(self):
        with tempfile.TemporaryDirectory(prefix='chapter-global-prebuild-') as temp:
            docs = Path(temp) / 'docs'
            shutil.copytree(DOCS, docs)
            source = docs / 'answers/testing/new-unmapped.md'
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text('---\npage_class: page\n---\n# New answer\n\n'
                              '## Related\n\n- [One](https://one.example/)\n'
                              '- [Two](https://two.example/)\n- [Three](https://three.example/)\n\n'
                              '## Next step\n\nFixed material.\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'no actual page_class: chapter'):
                repair.FiniteChapterLinks(docs, MAP)

    def test_unknown_or_missing_reviewed_keys_and_unknown_root_fields_rejected(self):
        for kind in ['missing', 'unknown', 'field', 'version']:
            mapping = copy.deepcopy(self.mapping)
            if kind == 'missing':
                mapping['pages'].pop(next(iter(mapping['pages'])))
            elif kind == 'unknown':
                mapping['pages']['answers/testing/unknown.md'] = mapping['pages'].pop(next(iter(mapping['pages'])))
            elif kind == 'field':
                mapping['extra'] = True
            else:
                mapping['version'] = True
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                repair.validate_mapping(mapping, DOCS)

    def test_edited_map_bytes_and_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'map.json'
            path.write_bytes(self.raw + b'\n')
            with self.assertRaisesRegex(ValueError, 'reviewed bytes'):
                repair.FiniteChapterLinks(DOCS, path)
            path.write_text('{"version":1,"version":1,"pages":{}}', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'duplicate JSON key'):
                repair.FiniteChapterLinks(DOCS, path)

    @unittest.skipUnless(shutil.which('git'), 'Git is required for the checkout regression')
    def test_actual_single_path_attributes_preserve_raw_map_on_crlf_checkout(self):
        attributes = (ROOT / '.gitattributes').read_bytes()
        with tempfile.TemporaryDirectory(prefix='chapter-map-checkout-') as temp:
            root = Path(temp).resolve()
            self.assertTrue(root.is_relative_to(Path(tempfile.gettempdir()).resolve()))
            empty = root / 'empty-config'
            empty.write_bytes(b'')
            env = dict(os.environ)
            for name in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE',
                         'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES'):
                env.pop(name, None)
            env.update(GIT_ATTR_NOSYSTEM='1', GIT_CONFIG_NOSYSTEM='1',
                       GIT_CONFIG_GLOBAL=str(empty))

            def git(*args):
                return subprocess.run(['git', '-C', str(root), *args], check=True,
                                      capture_output=True, text=True, encoding='utf-8', env=env).stdout

            git('init', '--quiet')
            git('config', 'core.autocrlf', 'true')
            git('config', 'core.safecrlf', 'false')
            git('config', 'core.attributesfile', str(empty))
            target = root / 'tools/library_related_chapters.json'
            target.parent.mkdir()
            target.write_bytes(self.raw)
            git('add', '--', 'tools/library_related_chapters.json')
            target.unlink()
            git('checkout-index', '--force', '--', 'tools/library_related_chapters.json')
            negative = target.read_bytes()
            self.assertIn(b'\r\n', negative)
            self.assertNotEqual(self.raw, negative)
            with self.assertRaisesRegex(ValueError, 'reviewed bytes'):
                repair.FiniteChapterLinks(DOCS, target)
            (root / '.gitattributes').write_bytes(attributes)
            git('add', '--', '.gitattributes')
            effective = git('check-attr', 'text', 'eol', '--', 'tools/library_related_chapters.json')
            self.assertIn('text: set', effective)
            self.assertIn('eol: lf', effective)
            target.unlink()
            git('checkout-index', '--force', '--', 'tools/library_related_chapters.json')
            self.assertEqual(self.raw, target.read_bytes())
            self.assertEqual(94, len(repair.FiniteChapterLinks(DOCS, target).entries))

    def test_real_smart_apostrophe_replacements_are_exact_and_inline(self):
        for key in ['answers/agents/can-veterinary-software-integrate-with-chatgpt.md',
                    'answers/industries/crm-software-chatgpt-free.md']:
            entry = self.mapping['pages'][key]
            self.assertIn('\u2019', entry['replace_label'])
            self.assertNotIn('\ufffd', entry['replace_label'])
            compiled = self.runtime.entries[key]
            prefix, section, _ = repair.related_parts(compiled['_body'])
            token = '[' + entry['replace_label'] + '](' + entry['replace_href'] + ')'
            self.assertEqual(1, section.count(token))
            self.assertIn(entry['replace_href'], repair.INLINE_LINK.findall(prefix))

    def test_actual_hooks_import_without_tools_package_and_preserve_content_wrapper(self):
        hooks = load_module('finite_hooks_under_test', ROOT / 'tools/hooks.py')
        with self.assertRaisesRegex(ValueError, 'must validate before'):
            hooks.on_page_markdown('body', SimpleNamespace(file=SimpleNamespace(src_uri='index.md')))
        hooks.on_pre_build({'docs_dir': str(DOCS)})
        for key, entry in self.runtime.entries.items():
            body, _ = mkdocs_meta.get_data(repair.canonical_source(entry['_source'].read_bytes()))
            page = SimpleNamespace(file=SimpleNamespace(src_uri=key))
            self.assertEqual(self.runtime.transform(key, body), hooks.on_page_markdown(body, page))
        unchanged = 'An unrelated page.\n'
        self.assertEqual(unchanged, hooks.on_page_markdown(unchanged, SimpleNamespace(file=SimpleNamespace(src_uri='index.md'))))
        output = hooks.on_page_content('<h2 id="what-our-own-data-shows">Own</h2><p>Data</p><h2 id="sources">Sources</h2><table><a class="headerlink" href="#x">x</a>',
                                       SimpleNamespace(meta={'page_class': 'research'}))
        self.assertIn('<div class="bw-research-content">', output)
        self.assertIn('<section class="bw-own-data"', output)
        self.assertIn('<table tabindex="0">', output)
        self.assertIn('aria-hidden="true" tabindex="-1"', output)


if __name__ == '__main__':
    unittest.main()
