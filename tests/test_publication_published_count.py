"""Synthetic inventory/count checks, never approvals of current production."""
import copy
import dataclasses
import tempfile
import unittest
from library_publication_composition import validated_published_article_count
from library_publication_overlay import OverlayError
from library_publication_release import route_for
from test_publication_composition import CompositionFixture


def synthetic_prior(count=326, retired_count=0):
    paths=['answers/measurement/synthetic-leaf-'+str(i)+'.md' for i in range(count)]
    return {'routes':{route_for(p):{'kind':'article','path':p} for p in paths[retired_count:]},
        'raw_source_pins':{p:'a'*64 for p in paths},
        'merged_sources':{p:{'article_pass':False} for p in paths[:retired_count]}}


class PublishedCountTests(unittest.TestCase):
    def test_explicit_326_matches_actual_article_inventory(self):
        self.assertEqual(326,validated_published_article_count(326,synthetic_prior()))

    def test_no_default_bool_float_or_caller_arbitrary_count(self):
        for value in [None,True,False,326.0,'326',0,-1,300,325,327]:
            with self.subTest(value=value),self.assertRaises(OverlayError):
                validated_published_article_count(value,synthetic_prior())

    def test_326_raw_history_with_10_retirements_is_316_articles(self):
        prior=synthetic_prior(retired_count=10)
        self.assertEqual(316,validated_published_article_count(316,prior))
        with self.assertRaisesRegex(OverlayError,'actual prior article inventory'):
            validated_published_article_count(326,prior)

    def test_no_hidden_or_invented_raw_history(self):
        prior=synthetic_prior()
        prior['raw_source_pins'].pop(next(iter(prior['raw_source_pins'])))
        with self.assertRaisesRegex(OverlayError,'history hides or invents'):
            validated_published_article_count(326,prior)
        prior=synthetic_prior();prior['raw_source_pins']['answers/measurement/unlisted.md']='b'*64
        with self.assertRaisesRegex(OverlayError,'history hides or invents'):
            validated_published_article_count(326,prior)

    def test_duplicate_and_malformed_route_paths_rejected(self):
        prior=synthetic_prior();row=copy.deepcopy(next(iter(prior['routes'].values())))
        prior['routes']['/invented-route/']=row
        with self.assertRaisesRegex(OverlayError,'route/path differs|Duplicate'):
            validated_published_article_count(327,prior)
        prior=synthetic_prior();row=next(iter(prior['routes'].values()));row['path']='../outside.md'
        with self.assertRaisesRegex(OverlayError,'route/path differs'):
            validated_published_article_count(326,prior)

    def test_article_cannot_also_be_retired(self):
        prior=synthetic_prior();rel=next(iter(prior['raw_source_pins']))
        prior['merged_sources'][rel]={'article_pass':False}
        with self.assertRaisesRegex(OverlayError,'also a prior article'):
            validated_published_article_count(326,prior)

    def test_composition_itself_rejects_missing_or_wrong_trust_count(self):
        with tempfile.TemporaryDirectory() as root:
            fx=CompositionFixture(root)
            for value in [None,True,300,326]:
                with self.subTest(value=value),self.assertRaisesRegex(OverlayError,'published ARTICLE count'):
                    fx.compose(trust=dataclasses.replace(fx.trust,published_count=value))
            self.assertEqual(8,fx.compose().published_article_count)

    def test_retired_history_full_composition_count_remains_exact(self):
        from test_publication_composition import CompositionTests
        case=CompositionTests('test_prior_real301_remains_retired_raw_history_in_later_group')
        case.setUp()
        try:
            case.retire_prior_source()
            overlay=case.c.compose()
            self.assertEqual(7,overlay.published_article_count)
            self.assertEqual(8,len(overlay.pins['pages']))
            with self.assertRaisesRegex(OverlayError,'actual prior article inventory'):
                case.c.compose(trust=dataclasses.replace(case.c.trust,published_count=8))
        finally:case.doCleanups()


if __name__=='__main__':unittest.main()
