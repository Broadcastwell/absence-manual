"""The art director's live round 3 on the docs, as the lead's art round 4 rules decide it (STEP 3.3 B130,
11 November 2026).

Point 8: at 1440 everything hangs on the 120 to 1320 container the wordmark uses (the chapter list's text
and the page label at 120, the rule above Previous and Next from 120 to 1320). Points 2 and 19: the footer
takes the app's spacing and wrap. Point 5: inset panels and cards run full-bleed on a phone and captions keep
75 characters a line at 1440. Point 16: the colophon is body text on a phone. Point 7 and 10: a heading
stands 24px clear of what sits under it, the closing panel sizes to its content, cards are 8px and panels
12px. Point 4: the not-found page's section heading is a statement. Study 6 and Study 7, studies served under
/research/ whose sources are classed as pages, carry no lede, like the other research pages, without any
change to their reviewed source files. The B126 lede and its release guard stay exactly as they were.
"""
import hashlib
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
DOCS = ROOT / "docs"
LEDE = ('<div class="bw-docs-lede"><p>Broadcastwell measures and fixes whether AI search engines name B2B software '
        'companies.</p><a class="bw-button bw-button--primary" href="https://audit.broadcastwell.com/">Run the free '
        'check</a></div>')
STUDIES = ("research/study6-wrong-about-you.md", "research/study7-ai-written-rfp.md")


def block(css, opener):
    at = css.index(opener)
    return css[at:css.index("\n}\n", at)]


class LayerTests(unittest.TestCase):
    def setUp(self):
        self.css = (ROOT / "docs/assets/brand/docs.css").read_text(encoding="utf-8")
        self.layer = (ROOT / "tools/brand-docs.css").read_text(encoding="utf-8")

    def test_the_served_stylesheet_ends_with_this_layer(self):
        self.assertTrue(self.css.endswith(self.layer))

    def test_the_side_lists_and_the_label_hang_on_the_container(self):
        wide = block(self.layer, "@media screen and (min-width: 76.25em) {\n  .md-sidebar--primary .md-nav--primary > .md-nav__title")
        for rule in (".md-sidebar .md-sidebar__scrollwrap { margin-inline: calc(-1 * var(--bw-space-8)); }",
                     ".md-sidebar .md-sidebar__inner { padding-inline: 0 var(--bw-space-8); }",
                     ".md-sidebar :is(.md-nav--primary, .md-nav--secondary) > .md-nav__list { padding-inline: var(--bw-space-8) 0; }",
                     ".md-sidebar .md-nav__link { margin-inline: 0; }",
                     ".md-sidebar--secondary .md-nav--secondary > .md-nav__title { padding-inline: var(--bw-space-8) 0; }",
                     ".md-sidebar--primary[hidden] ~ .md-content > .md-content__inner { max-width: none; margin-left: 0; }"):
            self.assertIn(rule, wide)
        # The sticky title stays dropped (B126, point 7) and the label has no inset of its own.
        self.assertIn(".md-sidebar--primary .md-nav--primary > .md-nav__title { display: none; }", wide)
        self.assertNotIn(".bw-document-tools { padding-left", self.layer)
        tools = re.search(r"\n\.bw-document-tools \{([^}]*)\}", self.layer).group(1)
        self.assertIn("padding: var(--bw-space-8) var(--bw-layout-margin)", tools)
        self.assertIn("max-width: calc(var(--bw-layout-container) + 2 * var(--bw-layout-margin))", tools)

    def test_the_rule_above_previous_and_next_runs_on_the_container(self):
        rule = re.search(r"\n\.bw-document-pagination \{([^}]*)\}", self.layer).group(1)
        self.assertIn("width: calc(100% - 2 * var(--bw-layout-margin))", rule)
        self.assertIn("max-width: var(--bw-layout-container)", rule)
        self.assertIn("padding: var(--bw-space-32) 0", rule)
        self.assertIn("border-top: var(--bw-stroke-hairline) solid var(--bw-color-line)", rule)

    def test_the_footer_takes_the_app_spacing_and_wrap(self):
        for rule in (".bw-site-footer :where(p, address) { margin: 0; }",
                     ".bw-site-footer :where(p) { text-wrap: pretty; }",
                     ".bw-site-footer :where(h2, h3) { text-wrap: balance; }",
                     ".bw-site-footer.bw-research-footer { padding-inline: 0; }",
                     ".bw-research-footer .bw-docs-research-note + .bw-site-footer__last { margin-top: 0; }"):
            self.assertIn(rule, self.layer)
        self.assertNotIn("\n.bw-research-footer .bw-site-footer__last { margin-top: 0; }", self.layer)

    def test_panels_and_cards_run_full_bleed_on_a_phone(self):
        phone = block(self.layer, "@media (max-width: 767px) {\n  .md-typeset :is(.bw-next-step")
        self.assertIn(".md-typeset :is(.bw-next-step, .bw-own-data, .admonition, details),", phone)
        self.assertIn("margin-inline: calc(-1 * var(--bw-layout-margin)); padding-inline: var(--bw-layout-margin); "
                      "border-inline-width: 0; border-radius: 0;", phone)
        self.assertIn(".manual-footer-version, .md-typeset p.manual-footer-version { max-width: none; "
                      "font-size: var(--bw-text-16); line-height: var(--bw-leading-16); }", phone)
        self.assertIn(".md-content__inner, .md-content__inner:has(.bw-learning) { margin-inline: 0; "
                      "padding-inline: var(--bw-layout-margin); }", self.layer)

    def test_captions_keep_a_caption_measure(self):
        self.assertIn("--bw-measure-caption: 42ch;", self.layer)
        for selector in (".md-typeset figure figcaption {", ".manual-footer-version {", ".md-typeset p.manual-footer-version {"):
            rule = self.layer[self.layer.index("\n" + selector):]
            self.assertIn("max-width: var(--bw-measure-caption)", rule[:rule.index("}")])

    def test_a_heading_stands_24px_clear_of_what_follows(self):
        for selector in (".md-typeset h2 {", ".md-typeset h3 {", ".md-typeset :is(h4, h5, h6) {"):
            rule = self.layer[self.layer.index("\n" + selector):]
            self.assertRegex(rule[:rule.index("}")], r"margin: var\(--bw-space-\d+\) 0 var\(--bw-space-24\);")
        self.assertIn(".md-typeset .bw-next-step h2 { margin: 0 0 var(--bw-space-12);", self.layer)
        self.assertIn(".bw-docs-notfound .bw-door h3 { margin: 0 0 var(--bw-space-12);", self.layer)
        self.assertIn(".md-typeset .bw-learning .card :is(h2, h3) { margin-bottom: var(--bw-space-24); }", self.layer)

    def test_the_closing_panel_sizes_to_its_content_and_radii_follow_the_hierarchy(self):
        for name in ("bw-next-step", "bw-own-data"):
            panel = re.search(r"\n\.md-typeset \." + name + r" \{([^}]*)\}", self.layer).group(1)
            self.assertIn("width: fit-content; max-width: 100%;", panel)
            self.assertIn("border-radius: var(--bw-radius-12)", panel)
        self.assertIn(".md-typeset .bw-learning .card, .md-typeset .bw-learning .grid > .card { border-radius: var(--bw-radius-8); }", self.layer)
        self.assertIn(".md-typeset .bw-learning :is(.panel, .step) { border-radius: var(--bw-radius-12); }", self.layer)
        self.assertIn(".md-typeset .bw-learning .grid > .card:is(:hover, :focus-within) { border-color: var(--bw-color-accent); box-shadow: none; }", self.layer)

    def test_the_layer_stays_on_the_brand(self):
        self.assertNotRegex(self.layer, r"(?i)linear-gradient|radial-gradient|1E3A8A|text-transform: uppercase")


class TemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_config(str(ROOT / "mkdocs.yml"))
        cls.tmp = tempfile.TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def render(self, src, meta, markdown):
        env = self.config.theme.get_env()
        f = File(src, str(DOCS), self.tmp.name, True)
        files = Files([f])
        page = Page(None, f, self.config)
        page.markdown = markdown
        page.meta = dict(meta)
        page.render(self.config, files)
        context = get_context(Navigation([page], [page]), files, self.config, page)
        html = env.get_template(page.meta.get("template", "main.html")).render(context)
        return re.search(r"(?s)<article(?:\s[^>]*)?>(.*)</article>", html).group(1)

    def test_studies_served_under_research_carry_no_lede(self):
        meta = {"title": "Study 6", "template": "followup.html", "description": "d", "page_class": "page"}
        for src in STUDIES:
            with self.subTest(src=src):
                article = self.render(src, meta, "# Study\n\nFinding.\n")
                self.assertNotIn("bw-docs-lede", article)

    def test_a_page_outside_research_keeps_the_one_lede(self):
        meta = {"title": "Chapter", "template": "followup.html", "description": "d", "page_class": "page"}
        article = self.render("ai-source-standard.md", meta, "# How can you read it?\n\nAnswer.\n")
        self.assertEqual(article.count(LEDE), 1)
        self.assertIn("</h1>\n" + LEDE, article)

    def test_the_lede_and_its_release_guard_are_unchanged(self):
        import sys
        sys.path.insert(0, str(ROOT / "tools"))
        import library_followup_release as release
        self.assertEqual(release.DOCS_LEDE, LEDE)
        self.assertEqual((ROOT / "overrides/brand.html").read_text(encoding="utf-8").count(LEDE), 1)

    def test_the_study_sources_are_the_reviewed_files(self):
        plan = json.loads((ROOT / "tools/library-followup-20261105.json").read_bytes())
        visibility = json.loads((ROOT / "tools/library-visibility-20261105.json").read_bytes())
        for rel in STUDIES:
            with self.subTest(rel=rel):
                raw = (DOCS / rel).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), plan["base_source_sha256"]["docs/" + rel])
                self.assertIn("page_class: page\n", raw.decode("utf-8"))
                self.assertIn(rel, visibility["pages"])

    def test_the_not_found_section_heading_is_a_statement(self):
        page = (ROOT / "overrides/404.html").read_text(encoding="utf-8")
        self.assertNotIn("Two ways to start", page)
        self.assertIn("<h2>You can run the free check yourself or have us do the work</h2>", page)
        self.assertIn("or pick a chapter from the manual's chapter navigation.", page)


if __name__ == "__main__":
    unittest.main()
