"""Generated HTML/CSS must retain the accepted LF bytes on every platform."""
from pathlib import Path
import tempfile
import unittest

from tools import performance_assets


class PerformanceAssetLineEndingTests(unittest.TestCase):
    def test_real_html_and_css_outputs_preserve_lf_and_unicode(self):
        with tempfile.TemporaryDirectory() as folder:
            site=Path(folder)
            first='body {\n  color: #123456;\n}\n'
            second='p::before {\n  content: "Café";\n}\n'
            (site/'first.css').write_bytes(first.encode())
            (site/'second.css').write_bytes(second.encode())
            page=site/'index.html'
            page.write_bytes(('<!doctype html>\n<html>\n<head>\n'
                '<link rel="stylesheet" href="first.css">\n'
                '<link rel="stylesheet" href="second.css">\n'
                '</head>\n<body><article><p>Café “dated record”.</p></article></body>\n'
                '</html>\n').encode())
            performance_assets.on_post_build({'site_dir':str(site)})
            outputs=list((site/'assets/stylesheets').glob('combined-*.css'))
            self.assertEqual(1,len(outputs))
            with self.subTest(output='HTML'):
                html=page.read_bytes()
                self.assertNotIn(b'\r',html)
                self.assertIn('Café “dated record”.'.encode(),html)
                self.assertEqual(1,html.count(b'<link rel="stylesheet"'))
            with self.subTest(output='CSS'):
                self.assertEqual((first+'\n'+second).encode(),outputs[0].read_bytes())


if __name__=='__main__':unittest.main()
