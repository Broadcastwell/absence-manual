import unittest
from analyze_page_signals import classify,interval

class RegisteredPrecedence(unittest.TestCase):
    def test_failure_is_never_negative(self):
        self.assertEqual(classify({'fetched_html':False},True),'fetch failure')
    def test_wikipedia_overrides_plugin(self):
        self.assertEqual(classify({'fetched_html':True,'seo_plugins':['Yoast SEO']},True),'definitely not optimized')
    def test_strong_overrides_missing_title(self):
        self.assertEqual(classify({'fetched_html':True,'json_ld':True},False),'definitely optimized')
    def test_missing_description_overrides_https(self):
        self.assertEqual(classify({'fetched_html':True,'title_nonempty':True,'https':True},False),'probably not optimized')
    def test_residual_is_unclassified(self):
        self.assertEqual(classify({'fetched_html':True,'title_nonempty':True,'description_nonempty':True,'ttfb_seconds':4},False),'unclassified')
    def test_ttfb_threshold_is_strict(self):
        r=dict(fetched_html=True,title_nonempty=True,description_nonempty=True,ttfb_seconds=3)
        self.assertEqual(classify(r,False),'unclassified')
        r['ttfb_seconds']=2.999;self.assertEqual(classify(r,False),'probably optimized')
    def test_wilson_zero_and_full_have_nonzero_width(self):
        self.assertGreater(interval(0,100)[2],0);self.assertLess(interval(100,100)[1],100)

if __name__=='__main__':unittest.main()
