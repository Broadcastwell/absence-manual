from pathlib import Path
import os,sys,tempfile,unittest
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File,Files,InclusionLevel
from mkdocs.structure.pages import Page
from mkdocs.structure.nav import Navigation,Section
from mkdocs.contrib.search import SearchPlugin
import json
HERE=Path(__file__).resolve().parents[1]
SUPPORT=Path(os.environ.get('BW_OVERLAY_SUPPORT_REPO',HERE))
sys.path[:0]=[str(HERE/'tools'),str(SUPPORT/'tools'),str(SUPPORT)]
from library_related_chapter_links import source_body
from library_owner_repair_absence_seo import PATH,OLD_TITLE,NEW_TITLE,validate_seo_source,retain_appendix_navigation


class AbsenceSeoTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);r=Path(self.tmp.name)
        self.docs=r/'docs';self.site=r/'site';self.docs.mkdir();self.site.mkdir()
        self.cfg=MkDocsConfig();self.cfg['site_name']='The Absence Manual';self.cfg['site_url']='https://docs.example.test/';self.cfg['docs_dir']=str(self.docs);self.cfg['site_dir']=str(self.site);self.assertFalse(self.cfg.validate()[0])
        self.files=Files([File(p,str(self.docs),str(self.site),True,inclusion=InclusionLevel.INCLUDED) for p in ['before.md',PATH,'after.md','omitted.md']])
        self.pages=[Page(t,f,self.cfg) for t,f in zip(['Before',OLD_TITLE,'After','Omitted'],self.files)]
        self.actual=self.pages[1];self.section=Section('Appendices',self.pages[:3]);self.parent=Section('Manual',[self.section]);self.section.parent=self.parent
        for i,p in enumerate(self.pages):p.parent=self.section;p.previous_page=self.pages[i-1] if i else None;p.next_page=self.pages[i+1] if i+1<len(self.pages) else None
        self.pages[3].previous_page=self.actual;self.pages[3].next_page=self.actual
        self.nav=Navigation([self.parent],self.pages[:3].copy())
        self.before='---\ntitle: '+OLD_TITLE+'\nheadline: '+OLD_TITLE+'\ndate_published: 2026-08-18T00:00:00+00:00\ndate_modified: 2026-10-28T00:00:00+00:00\n---\n\n# '+OLD_TITLE+'\n\nThe full science stays exact: 3 of 30.\n'
        self.after=self.before.replace('title: '+OLD_TITLE+'\n','title: '+NEW_TITLE+'\n',1).replace('date_modified: 2026-10-28','date_modified: 2026-11-03')
    def apply(self):return retain_appendix_navigation(self.nav,self.files,path=PATH,before=self.before,after=self.after,source_parser=source_body)
    def test_exact_source_delta_and_real_page_view(self):
        nav,proof=self.apply();view=nav.pages[1]
        self.assertEqual(NEW_TITLE,self.actual.title);self.assertEqual(OLD_TITLE,view.title);self.assertTrue(proof['body_exact'])
        self.assertIs(self.actual,self.files.get_file_from_path(PATH).page);self.assertIs(view,self.section.children[1]);self.assertIs(view,self.pages[0].next_page);self.assertIs(view,self.pages[2].previous_page)
    def test_omitted_neighbor_uses_same_view_without_returning_to_nav(self):
        self.apply();v=self.nav.pages[1];self.assertIs(v,self.pages[3].previous_page);self.assertIs(v,self.pages[3].next_page)
        self.assertFalse(any(p is self.pages[3] for p in self.nav.pages));self.assertIs(self.pages[3],self.files.get_file_from_path('omitted.md').page)
    def test_active_parent_and_symmetric_identity(self):
        self.apply();v=self.nav.pages[1];self.actual.active=True;self.assertTrue(v.active);self.assertTrue(self.parent.active)
        v.active=False;self.assertFalse(self.actual.active);self.assertFalse(self.parent.active);self.assertTrue(v==self.actual);self.assertTrue(self.actual==v)
    def test_real_search_uses_shorter_document_title(self):
        self.apply();meta,body=source_body(self.after);self.actual.meta=meta;self.actual.markdown=body;self.actual.render(self.cfg,self.files)
        search=SearchPlugin();search.load_config({});search.config.lang=['en'];search.on_pre_build(self.cfg);search.on_page_context({},self.actual,config=self.cfg)
        rows=json.loads(search.search_index.generate_search_index())['docs'];self.assertEqual(NEW_TITLE,rows[0]['title']);self.assertEqual(OLD_TITLE,self.nav.pages[1].title)
    def test_actual_mkdocs_unread_page_uses_exact_bound_after_source(self):
        # Actual get_navigation creates Page(None) before read_source runs.
        del self.actual.title
        (self.docs/PATH).write_text(self.after,encoding='utf-8')
        self.assertIsNone(self.actual.title)
        nav,proof=self.apply()
        self.assertEqual(NEW_TITLE,self.actual.title);self.assertEqual(OLD_TITLE,nav.pages[1].title)
        self.assertIs(self.actual,self.files.get_file_from_path(PATH).page);self.assertTrue(proof['body_exact'])
    def test_unread_page_with_different_source_or_loaded_state_rejects(self):
        del self.actual.title
        (self.docs/PATH).write_text(self.after.replace('3 of 30','4 of 30'),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'Unread Appendix B Page'):self.apply()
        (self.docs/PATH).write_text(self.after,encoding='utf-8')
        self.actual.meta={'unexpected':'loaded'}
        with self.assertRaisesRegex(ValueError,'Unread Appendix B Page'):self.apply()
    def test_unexpected_explicit_navigation_title_still_rejects(self):
        self.actual.title='Unreviewed Appendix label'
        with self.assertRaisesRegex(ValueError,'Unexpected Appendix B navigation label'):self.apply()
    def test_unrelated_path_rejected(self):
        with self.assertRaises(ValueError):validate_seo_source('other.md',self.before,self.after,source_body)
    def test_body_or_H1_change_rejected(self):
        with self.assertRaises(ValueError):validate_seo_source(PATH,self.before,self.after.replace('3 of 30','4 of 30'),source_body)
    def test_headline_change_rejected(self):
        with self.assertRaises(ValueError):validate_seo_source(PATH,self.before,self.after.replace('headline: '+OLD_TITLE,'headline: '+NEW_TITLE),source_body)
    def test_published_date_change_rejected(self):
        with self.assertRaises(ValueError):validate_seo_source(PATH,self.before,self.after.replace('date_published: 2026-08-18','date_published: 2026-08-19'),source_body)
    def test_wrong_title_rejected(self):
        with self.assertRaises(ValueError):validate_seo_source(PATH,self.before,self.after.replace('title: '+NEW_TITLE+'\n','title: Other\n'),source_body)
    def test_missing_actual_modification_delta_rejected(self):
        with self.assertRaises(ValueError):validate_seo_source(PATH,self.before,self.after.replace('date_modified: 2026-11-03','date_modified: 2026-10-28'),source_body)

if __name__=='__main__':unittest.main()
