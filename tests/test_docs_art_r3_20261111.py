"""The art director's live round 2 on the docs, as the lead's art round 3 rules decide it (STEP 3.3 B126,
11 November 2026), and the docs lines queued after B117.

Point 1: under the headline of a docs article, one sentence on what Broadcastwell does and for whom (the
ENTITY.md 12-word description word for word) and one primary action, the free check; the headline stays,
so an answer page keeps the buyer's question (rule 4); research pages carry no promotional audit link.
Point 7: on wide screens the chapter list has no sticky title to scroll under, rests on whole items and
hides an item its bottom edge would cut. Point 8: the page label hangs from the chapter list's text edge.
Point 18: the selected item takes the one selected state (rule 1). Queued: the executive template's retired
title, the doubled Kalvenor label on /vendor-facts/ and the Bloomington price sentence without "from ... to".
The 45 registered field-study pages keep main.html and their reviewed bytes.
"""
import json
import re
import sys
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
ENTITY_12 = "Broadcastwell measures and fixes whether AI search engines name B2B software companies."
LEDE = ('<div class="bw-docs-lede"><p>' + ENTITY_12 + '</p><a class="bw-button bw-button--primary" '
        'href="https://audit.broadcastwell.com/">Run the free check</a></div>')


def text(rel):
    return (DOCS / rel).read_text(encoding="utf-8")


def wide_block(css):
    at = css.index("@media screen and (min-width: 76.25em) {\n  .md-sidebar--primary .md-nav--primary > .md-nav__title")
    return css[at:css.index("\n}\n", at)]


class LedeTests(unittest.TestCase):
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

    def test_the_sentence_is_the_entity_description_word_for_word(self):
        # brand/ENTITY.md, version 1 of 10 November 2026, the 12-word description.
        brand = (ROOT / "overrides/brand.html").read_text(encoding="utf-8")
        self.assertEqual(brand.count(LEDE), 1)
        self.assertEqual(len(ENTITY_12.rstrip(".").split()), 12)

    def test_an_article_shows_the_sentence_and_the_one_action_right_under_its_headline(self):
        markdown = "# How can a page get cited by ChatGPT?\n\nThe answer first.\n\n## First section\n\nMore text.\n"
        for template in ("followup.html", "business-hub.html"):
            with self.subTest(template=template):
                meta = {"title": "Q", "template": template, "description": "d", "page_class": "page",
                        "library_cluster": "chatgpt", "date_published": "2026-11-02T00:00:00+00:00"}
                article = self.render("answers/chatgpt/example.md", meta, markdown)
                self.assertEqual(article.count(LEDE), 1)
                self.assertEqual(article.count("bw-docs-lede"), 1)
                head = article.index("</h1>")
                self.assertEqual(article[head:head + len("</h1>\n" + LEDE)], "</h1>\n" + LEDE)
                self.assertIn("How can a page get cited by ChatGPT?", article[:head])
                self.assertLess(article.index(LEDE), article.index("<p>The answer first.</p>"))
                self.assertEqual(article.count("bw-button--primary"), 1)

    def test_research_pages_carry_no_promotional_action(self):
        meta = {"title": "Study", "template": "followup.html", "description": "d", "page_class": "research",
                "updated": "2026-11-01", "next_review": "2027-02-01"}
        article = self.render("research/studies/example/index.md", meta, "# Study\n\nFinding.\n")
        self.assertNotIn("bw-docs-lede", article)
        self.assertNotIn("audit.broadcastwell.com", article)

    def test_registered_pages_keep_the_reviewed_shell(self):
        meta = {"title": "Registered", "description": "d", "library_cluster": "fixes"}
        article = self.render("answers/fixes/can-google-ai-overview-answers-be-changed.md", meta, "# Registered\n\nText.\n")
        self.assertNotIn("bw-docs-lede", article)
        main = (ROOT / "overrides/main.html").read_text(encoding="utf-8")
        self.assertNotIn("bw-docs-lede", main)


class ReleaseGuardTests(unittest.TestCase):
    """The follow-up release's final-article check allows this one block, only right under the headline."""

    def test_the_guard_knows_the_template_lede(self):
        sys.path.insert(0, str(ROOT / "tools"))
        import library_followup_release as release
        self.assertEqual(release.DOCS_LEDE, LEDE)

    def test_the_lede_is_removed_once_and_only_from_under_the_headline(self):
        sys.path.insert(0, str(ROOT / "tools"))
        from library_followup_release import without_docs_lede
        head = [("start", "h1", ()), ("text", "Question?"), ("end", "h1")]
        lede = [("start", "div", (("class", "bw-docs-lede"),)), ("text", "Sentence."), ("end", "div")]
        body = [("start", "p", ()), ("text", "Answer."), ("end", "p")]
        self.assertEqual(without_docs_lede(head + lede + body, lede, False), head + body)
        self.assertEqual(without_docs_lede(head + lede + body, lede, True), head + lede + body)
        self.assertEqual(without_docs_lede(head + body + lede, lede, False), head + body + lede)
        self.assertEqual(without_docs_lede(head + lede + lede + body, lede, False), head + lede + body)
        self.assertEqual(without_docs_lede(body, lede, False), body)


class SidebarTests(unittest.TestCase):
    def setUp(self):
        self.css = (ROOT / "docs/assets/brand/docs.css").read_text(encoding="utf-8")
        self.layer = (ROOT / "tools/brand-docs.css").read_text(encoding="utf-8")

    def test_the_stylesheet_is_the_vendored_brand_then_the_docs_layer(self):
        self.assertTrue(self.css.endswith(self.layer))

    def test_wide_chapter_list_has_no_sticky_title_and_shows_whole_items(self):
        block = wide_block(self.css)
        self.assertIn(".md-sidebar--primary .md-nav--primary > .md-nav__title { display: none; }", block)
        # No column snapping: an open section's items snap inside their own list and would trap the column.
        self.assertNotIn("scroll-snap-type", self.layer)
        script = (ROOT / "docs/assets/brand/docs-controls.js").read_text(encoding="utf-8")
        self.assertIn("window.matchMedia('(min-width: 76.25em)')", script)
        self.assertIn("column.style.clipPath = head || tail ? 'inset(' + head + 'px 0 ' + tail + 'px 0)' : '';", script)
        self.assertIn("window.requestAnimationFrame(function () { window.requestAnimationFrame(settle); });", script)

    def test_the_page_label_hangs_from_the_chapter_list_text_edge(self):
        self.assertIn("body:has(.md-sidebar--primary:not([hidden])) .bw-document-tools { padding-left: "
                      "calc(var(--bw-layout-margin) + 0.8rem); }", wide_block(self.css))

    def test_the_selected_item_takes_the_one_selected_state(self):
        nav = re.search(r"\.bw-site-nav__trigger\[aria-current=\"page\"\][^{]*\{([^}]*)\}", self.css).group(1)
        self.assertIn("color:var(--bw-color-accent)", nav)
        self.assertIn("text-decoration-thickness:var(--bw-stroke-focus)", nav)
        self.assertIn("text-underline-offset:0.45em", nav)
        self.assertIn(".md-nav__link--active, .md-nav__item .md-nav__link--active { font-weight: var(--bw-weight-regular); "
                      "text-decoration: underline; text-decoration-thickness: var(--bw-stroke-focus); "
                      "text-underline-offset: 0.45em; }", self.layer)
        self.assertNotIn(".md-nav__item .md-nav__link--active { font-weight: var(--bw-weight-semibold); }", self.layer)
        self.assertNotIn("1E3A8A", self.layer.upper())

    def test_the_lede_follows_the_brand_tokens(self):
        rule = re.search(r"\.md-typeset \.bw-docs-lede p \{([^}]*)\}", self.layer).group(1)
        self.assertIn("font-family: var(--bw-font-sans)", rule)
        self.assertIn("max-width: var(--bw-measure)", rule)
        self.assertNotRegex(self.layer, r"(?i)linear-gradient|radial-gradient")


class QueuedLineTests(unittest.TestCase):
    def test_the_executive_template_drops_the_retired_title(self):
        template = text("assets/learning/audit/executive-template.txt")
        self.assertTrue(template.startswith("# Executive delivery template for orders before 26 October 2026\n"))
        self.assertNotIn("Category Audit", template)
        self.assertIn("for orders before 26 October 2026", text("resources/audit/executive-template.md"))

    def test_vendor_facts_labels_kalvenor_once(self):
        page = text("vendor-facts.md")
        self.assertEqual(page.count("Kalvenor is our example vendor (Sample data, fictional company)."), 1)
        self.assertNotIn("Kalvenor is fictional (Sample data", page)

    def test_bloomington_states_the_prices_without_a_range(self):
        page = text("services/bloomington-indiana.md")
        self.assertIsNone(re.search(r"(?i)\bfrom (a |an )?\$|\bstarting at\b|\$[0-9][0-9,]*\s*(to|-)\s*\$", page))
        self.assertNotIn("to a monthly Program", page)
        self.assertEqual(page.count("The smallest order is a $19 live question on one buyer question, and the table "
                                    "below lists each offer with its price."), 1)
        for price in ("| $19 once |", "| $490 once |", "| $490 per client report |", "| $3,900 ($3,410 after the $490 credit) |",
                      "| $490 a month |", "| $5,500 a month |"):
            self.assertEqual(page.count(price), 1)

    def test_not_found_page_names_the_chapter_navigation_without_a_position(self):
        page = (ROOT / "overrides/404.html").read_text(encoding="utf-8")
        self.assertIn("or pick a chapter from the manual's chapter navigation.", page)
        self.assertNotRegex(page, r"navigation (above|below|on the left|on the right)")

    def test_no_registered_page_source_changes(self):
        frozen = json.loads((ROOT / "tools/library_field_freeze_navigation.json").read_bytes())["pages"]
        changed = set(json.loads((ROOT / "tools/library-followup-20261105.json").read_bytes())["source_changes"])
        for rel in frozen:
            self.assertNotIn("docs/" + rel, changed)


if __name__ == "__main__":
    unittest.main()
