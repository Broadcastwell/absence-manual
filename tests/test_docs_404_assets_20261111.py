"""The not-found page loads its stylesheets, scripts, fonts and images at any depth (STEP 3.3 B134,
11 November 2026).

GitHub Pages answers every missing address with 404.html, so /no-such-page, /research/no-such-study/ and
/a/b/c/ all receive the same bytes. A relative address in that page resolves against the missing address,
so it breaks one level down or deeper: the B130 review found production's 404 at /research/no-such-study/
without its main stylesheet, because tools/performance_assets.py wrote the stylesheet bundle's link relative
to the page. MkDocs links everything else in an error template from the path of site_url
(mkdocs.commands.build._build_template), so the hook now does the same on an error page and every other page
keeps its relative links. These tests render overrides/404.html through MkDocs and Material, run the hook on
it, and fail on any address in the result that would resolve differently at another depth.
"""
import json
import re
import shutil
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from mkdocs.commands.build import _build_template
from mkdocs.config import load_config
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation

from tools import performance_assets

ROOT = Path(__file__).resolve().parents[1]
HOST = "https://docs.broadcastwell.com"
DEPTHS = ("/no-such-page", "/research/no-such-study/", "/a/b/c/")
URL_ATTRIBUTES = {"href", "src", "srcset", "imagesrcset", "poster", "data", "action", "xlink:href"}


class Addresses(HTMLParser):
    """Every address in a page: (tag, attribute, value), srcset lists split into their addresses."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.found = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name not in URL_ATTRIBUTES or value is None:
                continue
            values = [part.strip().split()[0] for part in value.split(",") if part.strip()] if name.endswith("srcset") else [value]
            self.found.extend((tag, name, v) for v in values)

    handle_startendtag = handle_starttag


def addresses(html):
    parser = Addresses()
    parser.feed(html)
    found = list(parser.found)
    found += [("style", "url", m.group(1)) for m in re.finditer(r"url\(\s*['\"]?([^'\")]+?)['\"]?\s*\)", html)]
    config = re.search(r'<script id="__config" type="application/json">(.*?)</script>', html, flags=re.S)
    if config:
        data = json.loads(config.group(1))
        found += [("script", "__config." + key, data[key]) for key in ("base", "search") if key in data]
    return found


def depth_dependent(html):
    """The addresses that resolve to a different target at a deeper missing address."""
    moving = []
    for tag, name, value in addresses(html):
        if value.startswith("#") or urlsplit(value).scheme in {"mailto", "tel", "data", "javascript"}:
            continue
        if len({urljoin(HOST + depth, value) for depth in DEPTHS}) != 1:
            moving.append((tag, name, value))
    return moving


class NotFoundAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_config(str(ROOT / "mkdocs.yml"))
        cls.default = cls.config["extra"].get("SHARED_NAV")
        cls.sources = [ROOT / "docs"] + [Path(d) for d in cls.config.theme.dirs]

    @classmethod
    def tearDownClass(cls):
        cls.config["extra"]["SHARED_NAV"] = cls.default

    def source(self, path):
        for folder in self.sources:
            if (folder / path).is_file():
                return folder / path
        return None

    def built_not_found(self, shared, site):
        """overrides/404.html as the build writes it: MkDocs' error-template render, then the bundling hook."""
        self.config["extra"]["SHARED_NAV"] = shared
        template = self.config.theme.get_env().get_template("404.html")
        html = _build_template("404.html", template, Files([]), self.config, Navigation([], []))
        for href in re.findall(r'<link rel="stylesheet" href="/([^"]+)"', html):
            target = site / href
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(self.source(href), target)
        (site / "404.html").write_text(html, encoding="utf-8", newline="\n")
        performance_assets.on_post_build({"site_dir": str(site), "site_url": self.config["site_url"]})
        return (site / "404.html").read_text(encoding="utf-8")

    def test_every_address_in_the_not_found_page_holds_at_any_depth(self):
        for shared in (False, True):
            with self.subTest(shared=shared), tempfile.TemporaryDirectory() as folder:
                site = Path(folder).resolve()
                html = self.built_not_found(shared, site)
                self.assertEqual([], depth_dependent(html))
                bundles = re.findall(r'<link rel="stylesheet" href="([^"]+)">', html)
                self.assertEqual(1, len(bundles))
                self.assertRegex(bundles[0], r"\A/assets/stylesheets/combined-[0-9a-f]{16}\.css\Z")
                self.assertIn('<link rel="stylesheet" href="/assets/brand/docs.css" media="all">', html)
                for tag, name, value in addresses(html):
                    parts = urlsplit(urljoin(HOST + DEPTHS[1], value))
                    if tag == "a" or parts.netloc != urlsplit(HOST).netloc or name == "__config.base":
                        continue
                    path = parts.path.lstrip("/")
                    with self.subTest(asset=value):
                        self.assertTrue((site / path).is_file() or self.source(path), value)

    def test_the_check_fails_on_a_relative_asset_link(self):
        page = ('<link rel="stylesheet" href="assets/stylesheets/combined-0131a34b0a08f9a4.css">'
                '<link rel="stylesheet" href="/assets/brand/docs.css" media="all">'
                '<script src="assets/brand/nav.js" defer></script><img src="/assets/a.png" srcset="assets/a-400.webp 400w">'
                '<style>@font-face { src: url("fonts/geist.woff2"); }</style><a href="#bw-main">Skip</a>')
        self.assertEqual([("link", "href", "assets/stylesheets/combined-0131a34b0a08f9a4.css"),
                          ("script", "src", "assets/brand/nav.js"), ("img", "srcset", "assets/a-400.webp"),
                          ("style", "url", "fonts/geist.woff2")], depth_dependent(page))

    def test_every_other_page_keeps_its_relative_bundle_link(self):
        with tempfile.TemporaryDirectory() as folder:
            site = Path(folder).resolve()
            (site / "first.css").write_text("a { color: #0b1220; }\n", encoding="utf-8", newline="\n")
            (site / "second.css").write_text("p { color: #1d4ed8; }\n", encoding="utf-8", newline="\n")
            pages = {"index.html": "", "research/no-such-study/index.html": "../../", "404.html": "/", "a/b/c/404.html": "../../../"}
            for rel, up in pages.items():
                (site / rel).parent.mkdir(parents=True, exist_ok=True)
                (site / rel).write_text('<link rel="stylesheet" href="%sfirst.css">\n<link rel="stylesheet" href="%ssecond.css">\n'
                                        % (up, up), encoding="utf-8", newline="\n")
            performance_assets.on_post_build({"site_dir": str(site), "site_url": HOST + "/"})
            bundle = next((site / "assets/stylesheets").glob("combined-*.css")).name
            expected = {"index.html": "assets/stylesheets/", "research/no-such-study/index.html": "../../assets/stylesheets/",
                        "404.html": "/assets/stylesheets/", "a/b/c/404.html": "../../../assets/stylesheets/"}
            for rel, prefix in expected.items():
                with self.subTest(page=rel):
                    self.assertEqual('<link rel="stylesheet" href="%s%s">\n\n' % (prefix, bundle), (site / rel).read_text(encoding="utf-8"))

    def test_the_error_page_follows_a_site_url_below_the_server_root(self):
        with tempfile.TemporaryDirectory() as folder:
            site = Path(folder).resolve()
            for name in ("a.css", "b.css"):
                (site / name).write_text("b { color: #0b1220; }\n", encoding="utf-8", newline="\n")
            (site / "404.html").write_text('<link rel="stylesheet" href="a.css">\n<link rel="stylesheet" href="b.css">\n',
                                           encoding="utf-8", newline="\n")
            performance_assets.on_post_build({"site_dir": str(site), "site_url": "https://example.com/docs/"})
            self.assertRegex((site / "404.html").read_text(encoding="utf-8"),
                             r'\A<link rel="stylesheet" href="/docs/assets/stylesheets/combined-[0-9a-f]{16}\.css">\n\n\Z')


if __name__ == "__main__":
    unittest.main()
