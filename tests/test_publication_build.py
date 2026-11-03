"""Bounded hook/navigation adapter regressions; no browser or network."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import os,sys,unittest,tempfile
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE/'tools'))
from library_publication_build import BuildSession,retain_legacy_navigation,safe_navigation_label,from_environment
from library_publication_overlay import OverlayError

def page(path):return SimpleNamespace(file=SimpleNamespace(src_uri=path),title=None,children=None,previous_page=None,next_page=None)

class BuildTests(unittest.TestCase):
    def test_final_capture_binds_actual_postprocessor_bytes_and_retains_template_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=BuildSession();s.site=Path(tmp);rel='answers/measurement/a.md'
            s.registry=SimpleNamespace(records={rel:{}},hubs={})
            s.contexts={rel:{'pre_postbuild_rendered_html':'<head>separate CSS</head><article>Exact fact.</article>','rendered_html':'old'}}
            path=s.site/'answers/measurement/a/index.html';path.parent.mkdir(parents=True);raw=b'<head>combined CSS</head><article>Exact fact.</article>';path.write_bytes(raw)
            s.capture_final_html()
            self.assertEqual(raw,s.contexts[rel]['rendered_html'].encode())
            self.assertIn('separate CSS',s.contexts[rel]['pre_postbuild_rendered_html'])
    def test_final_capture_rejects_missing_or_partial_actual_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=BuildSession();s.site=Path(tmp);rel='answers/measurement/a.md';s.registry=SimpleNamespace(records={rel:{}},hubs={});s.contexts={}
            with self.assertRaisesRegex(OverlayError,'coverage'):s.capture_final_html()
            s.contexts={rel:{'rendered_html':'old'}}
            with self.assertRaisesRegex(OverlayError,'missing'):s.capture_final_html()
    def test_identity_keeps_existing_navigation_objects_and_order(self):
        a,b='answers/measurement/a.md','answers/measurement/b.md';pages=[page(a),page(b)];files=[p.file for p in pages]
        pages[0].next_page=pages[1];pages[1].previous_page=pages[0]
        original=pages;nav=SimpleNamespace(items=pages,pages=pages)
        records={a:{'meta':{'title':'First question?'},'body':'First question?'},b:{'meta':{'title':'Second question?'},'body':'Second question?'}}
        overlay=SimpleNamespace(records=records,leaf_manifest={'pages':{a:{},b:{}}},merge_statuses={})
        retain_legacy_navigation(nav,files,overlay,{a:'First question?',b:'Second question?'})
        self.assertIs(original,nav.pages);self.assertEqual(2,len(files));self.assertIs(pages[1],pages[0].next_page)
    def test_new_leaf_stays_served_without_changing_historical_sidebar_membership(self):
        a,n,b='answers/measurement/a.md','answers/measurement/new.md','answers/measurement/b.md'
        pages=[page(a),page(n),page(b)];files=[p.file for p in pages];section=SimpleNamespace(children=pages);nav=SimpleNamespace(items=[section],pages=pages)
        records={p:{'meta':{'title':t},'body':t} for p,t in [(a,'First question?'),(n,'New question?'),(b,'Second question?')]}
        overlay=SimpleNamespace(records=records,leaf_manifest={'pages':{p:{} for p in records}},merge_statuses={})
        retain_legacy_navigation(nav,files,overlay,{a:'First question?',b:'Second question?'})
        self.assertEqual([a,b],[p.file.src_uri for p in nav.pages]);self.assertEqual(3,len(files));self.assertIs(nav.pages[1],nav.pages[0].next_page)
    def test_retired_alias_node_remains_but_its_HTML_source_leaves_served_files(self):
        a,b='answers/measurement/a.md','answers/measurement/b.md';pages=[page(a),page(b)];files=[p.file for p in pages];nav=SimpleNamespace(items=pages,pages=pages)
        overlay=SimpleNamespace(records={b:{'meta':{'title':'Broader question?','also_asked_as':['Old question?']},'body':'Also asked as: Old question?'}},leaf_manifest={'pages':{a:{},b:{}}},merge_statuses={a:{'status':'MERGED_301','article_pass':False,'target_path':b}})
        retain_legacy_navigation(nav,files,overlay,{a:'Old question?',b:'Broader question?'})
        self.assertEqual(2,len(nav.pages));self.assertEqual([b],[f.src_uri for f in files]);self.assertEqual('Old question?',nav.pages[0].title)
    def test_changed_legacy_label_needs_visible_alias_and_banned_labels_fail(self):
        a='answers/measurement/a.md';p=page(a);overlay=SimpleNamespace(records={a:{'meta':{'title':'New question?','also_asked_as':[]},'body':'New question?'}},leaf_manifest={'pages':{a:{}}},merge_statuses={})
        with self.assertRaisesRegex(OverlayError,'visible retained alias'):
            retain_legacy_navigation(SimpleNamespace(items=[p],pages=[p]),[p.file],overlay,{a:'Old question?'})
        for label in ['A winner','Startup software','<script>alert(1)</script>']:
            with self.assertRaises(OverlayError):safe_navigation_label(label)
    def test_missing_independently_pinned_inputs_never_fall_back_to_raw(self):
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaisesRegex(OverlayError,'Independently pinned'):
                from_environment({'site_dir':'site','docs_dir':'docs'})

if __name__=='__main__':unittest.main()
