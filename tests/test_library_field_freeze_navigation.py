"""Synthetic fragment tests only; actual45 proof is read-only and separate."""
from pathlib import Path
import json,subprocess,sys,unittest
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE/'tools'))
from library_field_freeze_navigation import (digest,primary_navigation_span,pagination_spans,retain_primary_navigation,retain_sitemap_entries,PAGINATION_PATH)

def html(nav='Old',body='Exact fact.',next_href='old/',next_title='Old'):
    return ('<!doctype html><html><head><link rel="next" href="'+next_href+'"></head><body>é<!-- <nav class="md-nav--primary">ignored</nav> --><nav class="md-nav md-nav--primary"><nav>Nested '+nav+'</nav></nav><article>'+body+'</article><a href="'+next_href+'" rel="next">Next: '+next_title+'</a></body></html>').encode()
def row(old):
    a,b=primary_navigation_span(old);return {'source_path':'answers/measurement/a.md','served_html_sha256':digest(old),'primary_navigation':old[a:b].decode(),'primary_navigation_sha256':digest(old[a:b])}
class NavigationTests(unittest.TestCase):
    def test_truth_correction_changes_only_the_two_recorded_navigation_labels(self):
        original = subprocess.check_output(['git','show','119b8e4e7709b3871904c11abea37bec4150ca3d:tools/library_field_freeze_navigation.json'],cwd=HERE)
        self.assertEqual(digest(original),'e8d4688604fdcb57e38944ce6937ce7fa788da73ec96b77902042990f8806f4c')
        before=json.loads(original)
        after=json.loads((HERE/'tools/library_field_freeze_navigation.json').read_bytes())
        record=json.loads((HERE/'tools/step31-navigation-deviation.json').read_bytes())
        self.assertEqual(len(record['pages']),45)
        self.assertEqual(before['presentation_asset_pins'],after['presentation_asset_pins'])
        self.assertEqual(before['frozen_sitemap_entries'],after['frozen_sitemap_entries'])
        for path, old in before['pages'].items():
            new=after['pages'][path]
            expected=old['primary_navigation']
            for label,replacement in record['replacements'].items():
                self.assertEqual(expected.count(label),1)
                expected=expected.replace(label,replacement)
            self.assertEqual(new['primary_navigation'],expected)
            self.assertNotIn('Category Audit',expected)
            mutable={'primary_navigation','primary_navigation_sha256','served_html_sha256'}
            self.assertEqual({k:v for k,v in old.items() if k not in mutable},{k:v for k,v in new.items() if k not in mutable})
            self.assertEqual(digest(expected.encode()),new['primary_navigation_sha256'])
            receipt=next(r for r in record['pages'] if r['source']==path)
            self.assertEqual(receipt['before_sha256'],old['served_html_sha256'])
            self.assertEqual(receipt['after_sha256'],new['served_html_sha256'])
            self.assertTrue(receipt['every_byte_outside_primary_navigation_unchanged'])
    def test_nested_nav_and_nonascii_offsets_retain_only_primary_fragment(self):
        old=html();current=html('New26links');new,r=retain_primary_navigation(current,row(old));self.assertEqual(old,new);self.assertFalse(r['whole_page_overwrite']);self.assertTrue(r['every_other_byte_retained'])
    def test_body_head_footer_or_pagination_drift_fails(self):
        old=html()
        for current in [html('New',body='Different fact.'),html('New').replace(b'<head>',b'<head><meta name="changed">'),html('New',next_href='different/')]:
            with self.assertRaisesRegex(ValueError,'differs outside'):retain_primary_navigation(current,row(old))
    def test_missing_repeated_or_unclosed_primary_nav_fails(self):
        for raw in [b'<article>No navigation</article>',html()+b'<nav class="md-nav--primary"></nav>',b'<nav class="md-nav--primary">']:
            with self.assertRaises(ValueError):primary_navigation_span(raw)
    def test_only_root_reviewed_Q0311_two_fragments_can_be_restored(self):
        old=html(next_href='../../chatgpt/',next_title='ChatGPT answers');r=row(old);r['source_path']=PAGINATION_PATH
        r['pagination']={n:{'fragment':old[a:b].decode(),'sha256':digest(old[a:b])} for n,(a,b) in pagination_spans(old).items()}
        r['root_pagination_approval']={'approved':True,'fragment_sha256':{k:v['sha256'] for k,v in r['pagination'].items()}}
        restored,receipt=retain_primary_navigation(html('New26links',next_href='../searchable/',next_title='Searchable'),r);self.assertEqual(old,restored);self.assertEqual(2,len(receipt['additional_Root_reviewed_Q0311_fragments']))
        r['source_path']='answers/measurement/other.md'
        with self.assertRaisesRegex(ValueError,'Only exact Root-reviewed'):retain_primary_navigation(html('New'),r)
    def test_unreviewed_or_mutated_pagination_rejected(self):
        old=html();r=row(old);r['source_path']=PAGINATION_PATH;r['pagination']={};r['pagination']['extra']={'fragment':'bad','sha256':digest(b'bad')};r['root_pagination_approval']={'approved':False}
        with self.assertRaises(ValueError):retain_primary_navigation(html('New'),r)
    def test_exact_frozen_xml_fragment_retained_without_touching_others(self):
        original=b'<urlset><url><loc>https://x/frozen/</loc><lastmod>new</lastmod></url><url><loc>https://x/new/</loc><lastmod>new</lastmod></url></urlset>';fragment='<url><loc>https://x/frozen/</loc><lastmod>old</lastmod></url>'
        out=retain_sitemap_entries(original,[{'url':'https://x/frozen/','exact_entry':fragment,'sha256':digest(fragment.encode())}]);self.assertIn(fragment.encode(),out);self.assertIn(b'<url><loc>https://x/new/</loc><lastmod>new</lastmod></url>',out)
        with self.assertRaisesRegex(ValueError,'missing'):retain_sitemap_entries(original,[{'url':'https://x/missing/','exact_entry':fragment,'sha256':digest(fragment.encode())}])
if __name__=='__main__':unittest.main()
