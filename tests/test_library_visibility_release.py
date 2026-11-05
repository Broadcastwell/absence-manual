"""Regression checks for the new consumer's source and freeze boundaries."""
from pathlib import Path
from types import SimpleNamespace
import copy, sys, unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from library_visibility_release import VisibilityEdits, canonical, digest


class VisibilityTests(unittest.TestCase):
    def session(self):
        session=object.__new__(VisibilityEdits)
        before='# Old question?\n\nA dated observation remains unchanged.\n'
        after=before.replace('Old question?','New question?')
        meta={'title':'Old question?'}
        session.pages={'answers/example.md':{'before_body_sha256':digest(before.encode()),'before_meta_sha256':digest(canonical(meta)),'after_body_sha256':digest(after.encode()),'edits':[{'before':'# Old question?','after':'# New question?','count':1}],'meta':{'title':'New question?'}}}
        session.seen=set()
        return session,before,meta,after

    def test_source_change_is_rejected_before_applying_edit(self):
        session,body,meta,_=self.session()
        with self.assertRaisesRegex(ValueError,'published article changed'):
            session.apply('answers/example.md',body+'A later correction.\n',meta)
        self.assertEqual(session.seen,set())

    def test_current_metadata_change_is_not_discarded(self):
        session,body,meta,_=self.session();meta['updated']='2026-11-06'
        with self.assertRaisesRegex(ValueError,'published metadata changed'):
            session.apply('answers/example.md',body,meta)

    def test_finite_edit_preserves_the_observation(self):
        session,body,meta,expected=self.session()
        out,newmeta=session.apply('answers/example.md',body,meta)
        self.assertEqual(out,expected);self.assertEqual(newmeta['title'],'New question?')
        self.assertEqual(meta,{'title':'Old question?'})

    def test_unlisted_frozen_source_is_not_changed(self):
        session,body,meta,_=self.session()
        self.assertEqual(session.apply('answers/frozen.md',body,meta),(body,meta))
        self.assertEqual(session.seen,set())

    def test_current_navigation_keeps_frozen_neighbors_old(self):
        session=object.__new__(VisibilityEdits)
        session.pages={'answers/current.md':{'meta':{'title':'Current question?'}}}
        session.frozen_paths={'answers/frozen.md'}
        def page(path,title):
            p=SimpleNamespace(title=title,is_page=True,previous_page=None,next_page=None)
            p.file=SimpleNamespace(src_uri=path,page=p)
            return p
        frozen=page('answers/frozen.md','Registered frozen title')
        current=page('answers/current.md','Old current title')
        frozen.next_page=current;current.previous_page=frozen
        nav=SimpleNamespace(items=[frozen,current],pages=[frozen,current],homepage=frozen)
        session.navigation(nav,[frozen.file,current.file])
        self.assertEqual(nav.pages[1].title,'Current question?')
        current.title='Current question?'
        self.assertEqual(frozen.next_page.title,'Old current title')
        self.assertEqual(frozen.title,'Registered frozen title')

    def test_generated_hub_uses_actual_prior_title_before_rendering(self):
        session=object.__new__(VisibilityEdits)
        session.pages={'answers/example/index.md':{'prior_title':'Published hub title','meta':{'title':'Which examples can I read?'}}}
        session.frozen_paths={'answers/example/frozen.md'}
        hub=SimpleNamespace(title=None,is_page=True,previous_page=None,next_page=None)
        frozen=SimpleNamespace(title='Registered question',is_page=True,previous_page=hub,next_page=None)
        hub.file=SimpleNamespace(src_uri='answers/example/index.md',page=hub)
        frozen.file=SimpleNamespace(src_uri='answers/example/frozen.md',page=frozen)
        hub.next_page=frozen
        nav=SimpleNamespace(items=[hub,frozen],pages=[hub,frozen],homepage=None)
        session.navigation(nav,[hub.file,frozen.file])
        self.assertEqual(frozen.previous_page.title,'Published hub title')


if __name__=='__main__':unittest.main()
