"""The brand frame (overrides/brand.html, brand system 3.0.0) rendered through MkDocs and Material.

Every page outside the 45 registered field-study pages renders through followup.html or
business-hub.html, which extend brand.html; the registered pages keep main.html and the reviewed
shell. mkdocs.yml extra.SHARED_NAV picks today's links (false, the default) or brand/nav.json
(true). Both values are rendered here (brief 11.1: one switch per repository, tested both ways).
"""
import json
import re
import tempfile
import unittest
from pathlib import Path

from mkdocs.commands.build import get_context
from mkdocs.config import load_config
from mkdocs.structure.files import File, Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page

ROOT = Path(__file__).resolve().parents[1]
NAV = json.loads((ROOT / "vendor" / "brand" / "nav.json").read_text(encoding="utf-8"))
TODAY_ITEMS = ["Answer Operations", "For agencies", "Answer Repair", "Pricing", "Research", "About"]


class BrandFrameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_config(str(ROOT / "mkdocs.yml"))
        cls.default = cls.config["extra"].get("SHARED_NAV")
        cls.tmp = tempfile.TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.config["extra"]["SHARED_NAV"] = cls.default
        cls.tmp.cleanup()

    def render(self, shared, src, meta, markdown="# Title\n\nText.\n\n## First section\n\nMore text.\n", template=None):
        self.config["extra"]["SHARED_NAV"] = shared
        env = self.config.theme.get_env()
        f = File(src, str(ROOT / "docs"), self.tmp.name, True)
        files = Files([f])
        page = Page(None, f, self.config)
        page.markdown = markdown
        page.meta = dict(meta)
        page.render(self.config, files)
        context = get_context(Navigation([page], [page]), files, self.config, page)
        return env.get_template(template or page.meta.get("template", "main.html")).render(context)

    def hub(self, shared):
        meta = {"title": "Title", "template": "business-hub.html", "description": "d", "page_class": "page",
                "schema_type": "Article", "date_published": "2026-11-09T00:00:00+00:00", "date_modified": "2026-11-09T00:00:00+00:00"}
        return self.render(shared, "chatgpt-business-hub/index.md", meta)

    @staticmethod
    def header(html):
        at = html.index('<header class="bw-site-nav"')
        return html[at:html.index("</header>", at)]

    @staticmethod
    def footer(html):
        return html[html.rindex('<footer class="bw-site-footer'):html.rindex("</footer>")]

    def test_the_switch_is_one_boolean(self):
        self.assertIsInstance(self.default, bool)
        self.assertEqual(len(re.findall(r"^\s*SHARED_NAV:", (ROOT / "mkdocs.yml").read_text(encoding="utf-8"), re.M)), 1)

    def test_one_search_control_in_each_state(self):
        # R-147: with the shared navigation on, its site-wide Search is the only search control.
        off, on = self.hub(False), self.hub(True)
        self.assertIn('data-md-component="search"', off)
        self.assertIn('data-manual-toggle="__search"', off)
        self.assertNotIn("app.broadcastwell.com/search", off)
        self.assertNotIn('data-md-component="search"', on)
        self.assertNotIn('data-manual-toggle="__search"', on)
        self.assertEqual(len(re.findall(r'class="bw-site-nav__action" href="https://app\.broadcastwell\.com/search"', on)), 1)
        for html in (off, on):
            self.assertIn('data-manual-toggle="__drawer"', html)
            self.assertIn('data-md-component="header"', html)

    def test_research_article_bodies_carry_no_contact_link(self):
        # R-147: verify_build.py checks the research rule on the article body; the shared header and
        # footer carry the doors, the phone and the email on every page.
        pattern = re.compile(r"mailto:|tel:|hello@broadcastwell|broadcastwell\.com/contact")
        research = [p for p in sorted((ROOT / "docs").rglob("*.md"))
                    if re.search(r"^page_class:\s*research\s*$", p.read_text(encoding="utf-8"), re.M)]
        self.assertEqual(len(research), 53)
        for path in research:
            with self.subTest(page=path.relative_to(ROOT).as_posix()):
                self.assertIsNone(pattern.search(path.read_text(encoding="utf-8")))
        meta = {"title": "Study", "template": "followup.html", "description": "d", "page_class": "research",
                "updated": "2026-11-01", "next_review": "2027-02-01"}
        for shared in (False, True):
            html = self.render(shared, "research/studies/example/index.md", meta)
            article = re.search(r"(?s)<article(?:\s[^>]*)?>(.*)</article>", html).group(1)
            self.assertIsNone(pattern.search(article), shared)

    def test_off_draws_todays_links_in_the_brand_markup(self):
        html = self.hub(False)
        head = self.header(html)
        self.assertEqual(re.findall(r'class="bw-site-nav__trigger" href="[^"]+">([^<]+)</a>', head), TODAY_ITEMS)
        self.assertIn('class="bw-button bw-button--secondary" href="https://broadcastwell.com/answer-repair">Fix one answer, $490</a>', head)
        self.assertNotIn("Start free", html)
        foot = self.footer(html)
        self.assertEqual(re.findall(r'<h2 class="bw-site-footer__title" id="bw-footer-\d">([^<]+)</h2>', foot),
                         ["Product", "Research", "Free tools", "Company", "Contact"])
        self.assertIn('<a href="https://x.com/broadcastwellhq">X</a>', foot)
        self.assertIn('<time datetime="2026-11-09">9 November 2026</time>', foot)
        self.assertNotIn("bw-shared-", html)

    def test_on_draws_nav_json_and_marks_the_current_page(self):
        html = self.hub(True)
        head = self.header(html)
        self.assertEqual(re.findall(r'<summary class="bw-site-nav__trigger[^"]*" id="bw-nav-menu-\d">([^<]+)<', head) +
                         re.findall(r'<li><a class="bw-site-nav__trigger" href="[^"]+">([^<]+)</a></li>', head),
                         ["Platform", "Services", "Research", "Company", "Pricing"])
        self.assertIn('href="https://audit.broadcastwell.com/">Start free</a>', head)
        self.assertIn('href="https://broadcastwell.com/contact">Talk to us</a>', head)
        self.assertIn('href="https://docs.broadcastwell.com/chatgpt-business-hub/" aria-current="page">ChatGPT Business Hub readiness</a>', head)
        foot = self.footer(html)
        self.assertEqual(re.findall(r'<h2 class="bw-site-footer__title" id="bw-footer-\d">([^<]+)</h2>', foot),
                         [c["title"] for c in NAV["footer"]["columns"]])
        self.assertNotIn("Last updated", foot)
        self.assertNotIn("Answer Operations", head)

    def test_both_ways_one_header_one_skip_link_and_the_manual_tools(self):
        for shared in (False, True):
            with self.subTest(shared=shared):
                html = self.hub(shared)
                self.assertEqual(html.count("data-bw-nav"), 1)
                self.assertEqual(html.count('class="bw-skip"'), 1)
                self.assertIn('class="bw-skip" href="#title">Skip to content</a>', html)
                self.assertIn('class="md-header bw-docs-header" data-md-component="header"', html)
                self.assertEqual('data-md-component="search"' in html, not shared)
                self.assertIn('data-manual-toggle="__drawer"', html)
                self.assertIn('assets/brand/docs.css" media="all">', html)
                self.assertIn('assets/brand/nav.js" defer></script>', html)
                self.assertNotIn("site-chrome.js", html)
                self.assertNotIn("inter-latin-var.woff2", html)
                self.assertEqual(html.count("<footer"), 1)

    def test_research_pages_keep_their_disclosure_and_dates_both_ways(self):
        meta = {"title": "Study", "template": "followup.html", "description": "d", "page_class": "research",
                "updated": "2026-11-01", "next_review": "2027-02-01"}
        for shared in (False, True):
            with self.subTest(shared=shared):
                html = self.render(shared, "research/studies/example/index.md", meta)
                foot = self.footer(html)
                self.assertIn("bw-research-footer", foot)
                self.assertIn("excluded from its own sample", foot)
                self.assertIn('<time datetime="2026-11-01">2026-11-01</time>', foot)
        # Today's research pages carry no contact solicitation; the shared navigation does (Talk to
        # us, the phone and the address), which verify_build.py reports when the switch is turned on.
        off = self.render(False, "research/studies/example/index.md", meta)
        self.assertIsNone(re.search(r"mailto:|tel:|hello@broadcastwell|broadcastwell.com/contact", off))

    def test_registered_pages_keep_the_reviewed_shell(self):
        meta = {"title": "Registered", "description": "d", "library_cluster": "fixes", "date_modified": "2026-11-02T00:00:00+00:00"}
        for shared in (False, True):
            with self.subTest(shared=shared):
                html = self.render(shared, "answers/fixes/can-google-ai-overview-answers-be-changed.md", meta)
                self.assertIn('class="bw-shared-bar"', html)
                self.assertIn("site-chrome.js", html)
                self.assertIn("inter-latin-var.woff2", html)
                self.assertNotIn("data-bw-nav", html)
                self.assertNotIn("assets/brand/", html)

    def test_not_found_page_says_where_the_visitor_is_and_offers_the_doors(self):
        for shared in (False, True):
            with self.subTest(shared=shared):
                self.config["extra"]["SHARED_NAV"] = shared
                env = self.config.theme.get_env()
                context = get_context(Navigation([], []), Files([]), self.config, None)
                html = env.get_template("404.html").render(context)
                self.assertIn("<title>Page not found | The Absence Manual</title>", html)
                # R-147: GitHub Pages answers a missing address with this page and status 404; the
                # page itself carries no robots meta tag (no noindex).
                self.assertNotRegex(html, r'(?i)<meta[^>]+name="robots"|noindex')
                self.assertIn("You are on docs.broadcastwell.com", html)
                self.assertIn('<a href="https://docs.broadcastwell.com/">Go to the manual', html)
                self.assertIn('class="bw-button bw-button--primary" href="https://audit.broadcastwell.com/">Run the free check</a>', html)
                self.assertIn('class="bw-button bw-button--secondary" href="https://broadcastwell.com/contact">Talk to us</a>', html)
                self.assertEqual(html.count("data-bw-nav"), 1)
                self.assertIn('class="bw-skip" href="#bw-main"', html)
                self.assertIn('id="bw-main"', html)
                for banned in ("!", "—", "--", " I ", " my ", "oops", "sorry"):
                    article = html[html.index('<div class="bw-docs-notfound">'):html.index("</article>")]
                    self.assertNotIn(banned, re.sub(r"<[^>]+>", " ", article).lower() if banned.islower() else re.sub(r"<[^>]+>", " ", article))


if __name__ == "__main__":
    unittest.main()
