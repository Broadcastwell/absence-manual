"""Current document titles and historical navigation labels use separate objects."""
from pathlib import Path
from types import SimpleNamespace
import hashlib,json,os,sys,tempfile,unittest
from jinja2 import Environment,FileSystemLoader
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File,Files,InclusionLevel
from mkdocs.structure.pages import Page
from mkdocs.structure.nav import Navigation,Section
from mkdocs.contrib.search import SearchPlugin
from mkdocs.utils.templates import url_filter
import material
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE/'tools'))
import library_publication_build as build
from library_publication_overlay import sha,OverlayError
from library_quality import canonical_json
OWNING=Path(os.environ.get('BW_TITLE_TEST_REPO',str(HERE)))
OLD='How do Suede, Profound and AthenaHQ differ in sampling AI answers and measuring share of voice?'
CURRENT='How do AI visibility providers differ in sampling answers and measuring share of voice?'
REL='answers/measurement/current.md';BEFORE='answers/measurement/before.md';AFTER='answers/measurement/after.md'

class TitleSeparationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.docs=self.root/'docs';self.site=self.root/'site';self.docs.mkdir();self.site.mkdir()
        self.cfg=MkDocsConfig();self.cfg['site_name']='The Absence Manual';self.cfg['site_url']='https://docs.example.test/';self.cfg['docs_dir']=str(self.docs);self.cfg['site_dir']=str(self.site)
        errors,_=self.cfg.validate();self.assertFalse(errors,errors)
        self.files=Files([File(r,str(self.docs),str(self.site),True,inclusion=InclusionLevel.INCLUDED) for r in [BEFORE,REL,AFTER]])
        self.pages=[Page(t,f,self.cfg) for t,f in zip(['Before question?',OLD,'After question?'],self.files)];self.actual=self.pages[1]
        self.section=Section('Questions',self.pages.copy());self.parent=Section('Library',[self.section]);self.section.parent=self.parent
        for i,p in enumerate(self.pages):p.parent=self.section;p.previous_page=self.pages[i-1] if i else None;p.next_page=self.pages[i+1] if i+1<len(self.pages) else None
        self.nav=Navigation([self.parent],self.pages.copy())
        self.body='# '+CURRENT+'\n\nThe dated records remain separate: 3 of 30 answers and 12 of 150 answers.\n\nAlso asked as: '+OLD+'\n'
        meta={'title':CURRENT,'description':'The measured units remain separate.','also_asked_as':[OLD],'library_cluster':'measurement'}
        self.records={BEFORE:{'meta':{'title':'Before question?'},'body':'Before question?'},REL:{'meta':meta,'body':self.body},AFTER:{'meta':{'title':'After question?'},'body':'After question?'}}
        self.overlay=SimpleNamespace(records=self.records,leaf_manifest={'pages':{r:{} for r in self.records}},merge_statuses={},_field_handoff=self.root/'absent-handoff',_field_stamp=None)
        self.aliases={BEFORE:'Before question?',REL:OLD,AFTER:'After question?'}
        self.raw='# Historical source.\n';f=self.docs/REL;f.parent.mkdir(parents=True);f.write_text(self.raw,encoding='utf-8',newline='\n')
        self.records[REL].update(source_sha256=sha(f.read_bytes()),effective_body_sha256=sha(self.body.encode()),effective_meta_sha256=sha(canonical_json(meta).encode()),post_finite94_body_sha256=sha(self.raw.encode()))
        self.session=build.BuildSession();self.session.docs=self.docs;self.session.overlay=self.overlay;self.session.q=SimpleNamespace(canonical_json=canonical_json);self.session.hubs={}
        self.env=Environment(loader=FileSystemLoader([str(OWNING/'overrides'),str(Path(material.__file__).parent/'templates')]),autoescape=True)
        self.env.filters['url']=url_filter
    def apply(self):build.retain_legacy_navigation(self.nav,self.files,self.overlay,self.aliases)
    def render_document(self):
        self.actual.markdown=self.session.markdown(self.raw,self.actual);self.actual.render(self.cfg,self.files)
    def block(self,name,page=None):
        t=self.env.get_template('main.html');context=t.new_context({'page':page or self.actual,'nav':self.nav,'config':self.cfg,'base_url':'../..','features':[]})
        return ''.join(t.blocks[name](context))
    def nav_markup(self,ref=None):
        ctx={'page':ref or self.actual,'config':self.cfg,'base_url':'../..','features':[]}
        t=self.env.get_template('partials/nav-item.html');mod=t.make_module(ctx)
        return str(mod.render(self.nav.pages[1],'_2',1))
    def test_actual_document_render_and_owned_head_social_use_current_title(self):
        self.apply();self.render_document();head=self.block('htmltitle');social=self.block('extrahead')
        self.assertIn('<title>'+CURRENT+' | The Absence Manual</title>',head)
        self.assertIn('property="og:title" content="'+CURRENT+'"',social)
        self.assertIn('name="twitter:title" content="'+CURRENT+'"',social)
        self.assertIn('"name": "'+CURRENT+'"',social)
        self.assertEqual(CURRENT,self.actual.title);self.assertEqual(self.body,self.actual.markdown)
    def test_real_search_plugin_uses_current_document_title(self):
        self.apply();self.render_document();search=SearchPlugin();search.load_config({});search.config.lang=['en'];search.on_pre_build(self.cfg);search.on_page_context({},self.actual,config=self.cfg)
        rows=json.loads(search.search_index.generate_search_index())['docs'];self.assertTrue(rows)
        self.assertEqual(CURRENT,rows[0]['title']);self.assertEqual(REL.replace('.md','/'),rows[0]['location'])
    def test_view_cache_is_shared_by_recursive_nav_and_neighbor_refs(self):
        self.apply();v=self.nav.pages[1]
        self.assertIs(v,self.section.children[1]);self.assertIs(v,self.pages[0].next_page);self.assertIs(v,self.pages[2].previous_page)
        self.assertIs(self.actual,v._page);self.assertIs(self.actual,self.files.get_file_from_path(REL).page)
        self.assertIs(self.pages[0],self.nav.pages[0]);self.assertIs(self.pages[2],self.nav.pages[2])
        self.assertIs(self.section,v.parent);self.assertIs(self.actual.file,v.file);self.assertEqual(self.actual.url,v.url)
    def test_real_page_view_equality_is_symmetric_and_both_are_unhashable(self):
        self.apply();v=self.nav.pages[1]
        self.assertTrue(v==self.actual);self.assertTrue(self.actual==v);self.assertFalse(v!=self.actual);self.assertFalse(self.actual!=v)
        self.assertFalse(v==self.pages[0]);self.assertFalse(self.pages[0]==v);self.assertTrue(v!=self.pages[0]);self.assertTrue(self.pages[0]!=v)
        for p in [self.actual,v]:
            with self.assertRaises(TypeError):hash(p)
    def test_actual_active_and_view_active_share_parent_state(self):
        self.apply();v=self.nav.pages[1];self.actual.active=True
        self.assertTrue(v.active);self.assertTrue(self.section.active);self.assertTrue(self.parent.active)
        v.active=False;self.assertFalse(self.actual.active);self.assertFalse(self.section.active);self.assertFalse(self.parent.active)
        v.active=True;self.assertTrue(self.actual.active);self.assertTrue(self.parent.active)
    def test_actual_material_active_nav_and_neighbor_pagination_keep_old_label(self):
        self.apply();self.render_document();v=self.nav.pages[1];self.actual.active=True;nav=self.nav_markup()
        self.assertIn(OLD,nav);self.assertNotIn(CURRENT,nav);self.assertIn('md-nav__link--active',nav)
        before=self.block('footer',self.pages[0]);after=self.block('footer',self.pages[2])
        self.assertIn('Next: '+OLD,before);self.assertIn('Previous: '+OLD,after)
        self.assertNotIn(CURRENT,before+after);self.assertEqual(OLD,v.title)
    def test_navigation_label_cannot_overwrite_current_document_title(self):
        self.apply();self.render_document();v=self.nav.pages[1]
        with self.assertRaisesRegex(OverlayError,'label is fixed'):v.title='Changed label'
        self.assertEqual(CURRENT,self.actual.title);self.assertEqual(OLD,v.title)
    def test_same_title_identity_does_not_wrap_or_replace_nav_objects(self):
        self.aliases[REL]=CURRENT;self.actual.title=CURRENT;pages=self.nav.pages;items=self.nav.items
        self.apply();self.assertIs(pages,self.nav.pages);self.assertIs(items,self.nav.items);self.assertIs(self.actual,self.nav.pages[1])
    def test_current_hub_metadata_also_updates_real_page_title(self):
        rel='answers/measurement/index.md';f=File(rel,str(self.docs),str(self.site),True,inclusion=InclusionLevel.INCLUDED);p=Page('Old hub',f,self.cfg)
        self.session.hubs={rel:{'meta':{'title':'Current hub'},'body':'# Current hub\n'}}
        self.assertEqual('# Current hub\n',self.session.markdown('# Old hub\n',p));self.assertEqual('Current hub',p.title)
    def test_existing_excluded_file_fix_is_retained_for_retired_alias(self):
        self.overlay.merge_statuses={REL:{'status':'MERGED_CANONICAL_STUB','target_path':AFTER}};self.records.pop(REL)
        self.records[AFTER]={'meta':{'title':'After question?','also_asked_as':[OLD]},'body':'Historical alias '+OLD}
        self.apply();self.assertIs(InclusionLevel.EXCLUDED,self.actual.file.inclusion);self.assertIs(self.actual.file,self.files.get_file_from_path(REL));self.assertNotIn(self.actual.file,self.files.documentation_pages())

    def test_dropped_nav_page_keeps_legacy_neighbor_view_without_reappearing(self):
        rel='answers/measurement/dropped.md';f=File(rel,str(self.docs),str(self.site),True,inclusion=InclusionLevel.INCLUDED);dropped=Page('Dropped question?',f,self.cfg);self.files.append(f)
        self.records[rel]={'meta':{'title':'Dropped question?'},'body':'Dropped question?'};self.overlay.leaf_manifest['pages'][rel]={}
        self.nav.pages.insert(1,dropped);self.section.children.insert(1,dropped);dropped.parent=self.section
        dropped.previous_page=self.actual;dropped.next_page=self.actual
        self.apply();self.render_document();view=self.nav.pages[1]
        self.assertIs(view,dropped.previous_page);self.assertIs(view,dropped.next_page);self.assertEqual(OLD,dropped.next_page.title)
        self.assertIs(dropped,f.page);self.assertFalse(any(p is dropped for p in self.nav.pages));self.assertFalse(any(p is dropped for p in self.section.children))
        self.assertEqual(CURRENT,self.actual.title)
    def test_never_nav_file_page_keeps_legacy_neighbor_view_and_stays_omitted(self):
        rel='answers/measurement/not-in-nav.md';f=File(rel,str(self.docs),str(self.site),True,inclusion=InclusionLevel.NOT_IN_NAV);omitted=Page('Omitted question?',f,self.cfg);self.files.append(f)
        omitted.previous_page=self.actual;omitted.next_page=self.actual
        self.apply();self.render_document();view=self.nav.pages[1]
        self.assertIs(view,omitted.previous_page);self.assertIs(view,omitted.next_page);self.assertEqual(OLD,omitted.previous_page.title)
        self.assertIs(omitted,f.page);self.assertFalse(any(p is omitted for p in self.nav.pages));self.assertIs(InclusionLevel.NOT_IN_NAV,f.inclusion)

if __name__=='__main__':unittest.main()
