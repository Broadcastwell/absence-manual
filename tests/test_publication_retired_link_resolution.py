"""Real MkDocs file/resolver regressions for reviewed canonical HTML stubs."""
from pathlib import Path
from types import SimpleNamespace
import json,sys,tempfile,unittest
from jinja2 import Template
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File,Files,InclusionLevel
from mkdocs.structure.pages import Page
from mkdocs.contrib.search import SearchPlugin
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE/'tools'))
from library_publication_build import retain_legacy_navigation
from library_publication_overlay import OverlayError

FROZEN='answers/geo-basics/frozen.md'
DONOR='answers/measurement/old.md'
TARGET='answers/buying/current.md'
LINK='- [Old question](../measurement/old.md)'
EXPECTED='<li><a href="../../measurement/old/">Old question</a></li>'

class RetiredLinkTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.docs=self.root/'docs';self.site=self.root/'site';self.docs.mkdir();self.site.mkdir()
        self.cfg=MkDocsConfig();self.cfg['site_name']='Fixture';self.cfg['site_url']='https://docs.example.test/';self.cfg['use_directory_urls']=True
        self.cfg['docs_dir']=str(self.docs);self.cfg['site_dir']=str(self.site)
        errors,_warnings=self.cfg.validate();self.assertFalse(errors,errors)
        self.files=Files([File(r,str(self.docs),str(self.site),use_directory_urls=True,inclusion=InclusionLevel.INCLUDED) for r in [FROZEN,DONOR,TARGET]])
        self.pages=[Page(t,f,self.cfg) for t,f in zip(['Frozen question?','Old question?','Broader question?'],self.files)]
        self.pages[0].next_page=self.pages[1];self.pages[1].previous_page=self.pages[0];self.pages[1].next_page=self.pages[2];self.pages[2].previous_page=self.pages[1]
        self.nav=SimpleNamespace(items=self.pages,pages=self.pages)
        self.overlay=SimpleNamespace(records={FROZEN:{'meta':{'title':'Frozen question?'},'body':'Frozen question?'},TARGET:{'meta':{'title':'Broader question?','also_asked_as':['Old question?']},'body':'Old question?'}},leaf_manifest={'pages':{r:{} for r in [FROZEN,DONOR,TARGET]}},merge_statuses={DONOR:{'status':'MERGED_CANONICAL_STUB','article_pass':False,'target_path':TARGET}})
        self.aliases={FROZEN:'Frozen question?',DONOR:'Old question?',TARGET:'Broader question?'}
    def apply(self):return retain_legacy_navigation(self.nav,self.files,self.overlay,self.aliases)
    def test_same_retired_file_is_resolvable_but_not_an_included_document(self):
        donor=self.files.get_file_from_path(DONOR);url=donor.url;self.apply()
        self.assertIs(donor,self.files.get_file_from_path(DONOR));self.assertEqual(url,donor.url)
        self.assertIs(InclusionLevel.EXCLUDED,donor.inclusion)
        self.assertEqual([FROZEN,TARGET],[f.src_uri for f in self.files.documentation_pages()])
        self.assertEqual(3,len(self.files));self.assertEqual([FROZEN,DONOR,TARGET],[f.src_uri for f in self.files.documentation_pages(inclusion=InclusionLevel.all)])
    def test_real_markdown_resolver_retains_historical_directory_href(self):
        self.apply();p=self.pages[0];p.markdown='# Frozen question?\n\n'+LINK
        with self.assertLogs('mkdocs.structure.pages',level='INFO') as caught:p.render(self.cfg,self.files)
        self.assertIn(EXPECTED,p.content);self.assertNotIn('old.md',p.content)
        self.assertTrue(all(r.levelno<=20 for r in caught.records))
        self.assertIn('excluded from the built site',' '.join(caught.output))
    def test_original_remove_control_reproduces_unresolved_md_href_warning(self):
        self.files.remove(self.files.get_file_from_path(DONOR));p=self.pages[0];p.markdown='# Frozen question?\n\n'+LINK
        with self.assertLogs('mkdocs.structure.pages',level='WARNING') as caught:p.render(self.cfg,self.files)
        self.assertIn('<a href="../measurement/old.md">',p.content);self.assertNotIn(EXPECTED,p.content)
        self.assertIn('not found among documentation files',' '.join(caught.output))
    def test_sidebar_objects_titles_and_prev_next_are_unchanged(self):
        navpages=self.nav.pages;nextpage=self.pages[0].next_page;previous=self.pages[2].previous_page;donor=self.pages[1]
        self.apply();view=self.nav.pages[1]
        self.assertIs(donor,view._page);self.assertIs(donor.file.page,donor)
        self.assertIs(view,self.pages[0].next_page);self.assertIs(view,self.pages[2].previous_page)
        self.assertEqual('Old question?',view.title);self.assertIs(self.pages[2],view.next_page)
    def test_actual_document_loop_does_not_render_or_search_index_donor(self):
        self.apply();search=SearchPlugin();search.load_config({});search.config.lang=['en'];search.on_pre_build(self.cfg)
        rendered=[]
        for f in self.files.documentation_pages():
            p=f.page;p.markdown='# '+p.title+'\n\nRetained article.';p.render(self.cfg,self.files);rendered.append(f.src_uri)
            search.on_page_context({},p,config=self.cfg)
        self.assertEqual([FROZEN,TARGET],rendered);self.assertIsNone(self.pages[1].content)
        data=json.loads(search.search_index.generate_search_index());self.assertFalse(any(d['location'].startswith('answers/measurement/old/') for d in data['docs']))
        self.assertTrue(any(d['location'].startswith('answers/buying/current/') for d in data['docs']))
    def test_actual_mkdocs_sitemap_document_list_excludes_donor(self):
        self.apply();import mkdocs
        template=Path(mkdocs.__file__).parent/'templates/sitemap.xml';xml=Template(template.read_text(encoding='utf-8')).render(pages=self.files.documentation_pages())
        self.assertNotIn('/answers/measurement/old/',xml);self.assertIn('/answers/buying/current/',xml)
    def test_excluded_donor_is_never_copied_as_a_static_source(self):
        self.apply();donor=self.files.get_file_from_path(DONOR)
        from unittest.mock import patch
        with patch.object(donor,'copy_file',side_effect=AssertionError('Retired source copied')):self.files.copy_static_files()
        self.assertEqual([],list(self.site.rglob('*')))
    def test_missing_reviewed_retired_file_still_rejects(self):
        self.files.remove(self.files.get_file_from_path(DONOR))
        with self.assertRaisesRegex(OverlayError,'Retired raw source missing'):self.apply()

if __name__=='__main__':unittest.main()
