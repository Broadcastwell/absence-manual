"""The account analyses reference page added on 9 November 2026 (STEP 3.2 switch on, owner ruling R-090).

The page lists every analysis that is available now in a client account, grouped by what buyers do,
with what it reads, what it returns and the label that ships with its results. It never names a
model, vendor, cost or token, and it stays outside the navigation like the other reference pages.
"""
import re
import sys
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_chatgpt_business_hub as hub  # noqa: E402
import test_docs_content_pages as first  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
NAME = "account-analyses.md"
ROUTE = "https://docs.broadcastwell.com/account-analyses/"
LINK = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")
CHECKED = ("A modeled estimate, not a measurement. It is shown with its basis and checked against your next "
           "delivered measurement, with that check shown beside it once it exists.")
# The ruled label of each labeled analysis, by its title (brief 7.3). Advertising context from public
# sources is on as ruled with no label.
LABELS = {
    "Answer tone review": "Tone labels describe wording quoted from receipts; they are not scored and are not part of the Index.",
    "Third-party correction drafts": "A draft for you to send from your own addresses; Broadcastwell sends nothing to anyone.",
    "Follow-up questions": "Proposed follow-up questions, not observed answers; our measurements are single turn.",
    "Tone change alert": "A comparison of tone labels between the wording of two measurements, not a scored rate.",
    "Naming likelihood": CHECKED,
    "Ad campaign drafts for approval": "Drafts only; you apply any change in your own ad account; Broadcastwell applies nothing.",
    "Outreach drafts for approval": "Drafts you send from your own addresses; Broadcastwell sends nothing to anyone.",
    "Modeled AI influence": CHECKED,
    "Shared planning assumptions": "This plan states the work and its pace. It is not a promise of results.",
    "Clean and planted context compared": ("A model's reading of your sources, not an engine; it says what your sources "
                                           "support, not how engines answer."),
}
# Titles of analyses that need outside data; they stay on the fictional sample and are not listed.
DATA_TITLES = ["AI shopping visibility", "Social perception", "Reddit topic research", "Consumer panel question weights"]


def page():
    return hub.split_page(DOCS / NAME)


def entries(body):
    return dict(re.findall(r"(?ms)^### (.+?)\n\n(.*?)(?=^### |^## )", body))


class AccountAnalysesPageTests(unittest.TestCase):
    def test_one_question_with_dates_and_article_inputs(self):
        meta, body = page()
        self.assertTrue(meta["title"].endswith("?") and len(meta["title"]) < 60, meta["title"])
        self.assertEqual(meta["headline"], meta["title"])
        self.assertTrue(150 <= len(meta["description"]) <= 160, len(meta["description"]))
        self.assertEqual((meta["page_class"], meta["schema_type"], meta["template"]), ("page", "Article", "business-hub.html"))
        self.assertEqual(meta["date_published"], "2026-11-09T00:00:00+00:00")
        self.assertEqual(meta["date_modified"], "2026-11-09T00:00:00+00:00")
        self.assertEqual(re.findall(r"(?m)^# (.+)$", body), [meta["title"]])
        self.assertIn("\nUpdated 9 November 2026.\n", body)
        self.assertIn("## Sources", body)
        self.assertNotIn("```", body)
        self.assertNotIn("<title", body)
        self.assertIn("analyses", meta["title"].lower())
        self.assertIn("analyses", first.opening_words(body).lower())
        self.assertIn("available now", first.opening_words(body).lower())

    def test_fifty_one_analyses_each_with_what_it_reads_returns_and_its_label(self):
        _, body = page()
        found = entries(body)
        self.assertEqual(len(found), 51)
        self.assertEqual(len(re.findall(r"(?m)^## ", body)), 9, "seven buyer groups, the check note and sources")
        for title, text in found.items():
            with self.subTest(analysis=title):
                self.assertIn("\n**What it reads.** ", "\n" + text)
                self.assertIn("\n**What it returns, item by item.** ", text)
                if title in LABELS:
                    self.assertIn("\n**Label on every result.** " + LABELS[title], text)
                else:
                    self.assertNotIn("**Label on every result.**", text)
        for title in ("Naming likelihood", "Modeled AI influence"):
            self.assertIn('"Checked against your next delivered measurement once it exists."', found[title])
        self.assertIn("Advertising context from public sources", found)
        for title in DATA_TITLES:
            self.assertNotIn("### " + title + "\n", body)

    def test_no_model_vendor_cost_or_token_and_no_banned_copy(self):
        text = (DOCS / NAME).read_text(encoding="utf-8")
        llms = [line for line in (DOCS / "llms.txt").read_text(encoding="utf-8").splitlines() if ROUTE in line]
        for label, value in (("page", text), ("llms line", "\n".join(llms))):
            with self.subTest(text=label):
                self.assertEqual(hub.banned_hits(value), [])
                self.assertNotRegex(value, r"(?i)\b(?:sonnet|haiku|opus|anthropic|openai|gpt-?\d|claude-|token|tokens|cost|costs|budget|microusd|n8n)\b")
                self.assertEqual(re.findall(r"\$[0-9][0-9,]*", value), [])
                self.assertNotRegex(value, r"[^\x0a\x20-\x7e]")
        self.assertIn(hub.FIVE_ENGINE_LIST, text)

    def test_links_out_inbound_from_two_pages_outside_the_navigation_and_one_llms_line(self):
        meta, body = page()
        targets = LINK.findall(body)
        for target in targets:
            self.assertTrue((DOCS / target).is_file(), target)
        self.assertGreaterEqual(len(set(targets)), 3)
        inbound = sorted(path.relative_to(DOCS).as_posix() for path in DOCS.rglob("*.md")
                         if path.name != NAME and "](" + NAME + ")" in path.read_text(encoding="utf-8"))
        # Linked from two pages outside the visibility decisions, so no reviewed body hash moves.
        self.assertGreaterEqual(len(inbound), 2, inbound)
        self.assertTrue({"product-docs.md", "service-model.md"} <= set(inbound), inbound)
        root_nav = yaml.safe_load((DOCS / ".pages").read_text(encoding="utf-8"))["nav"]
        self.assertNotIn(NAME, root_nav)
        self.assertNotIn(NAME, (ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        lines = (DOCS / "llms.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual([line for line in lines if ROUTE in line], ["- [%s](%s): %s" % (meta["title"], ROUTE, meta["description"])])
        at = lines.index("- [%s](%s): %s" % (meta["title"], ROUTE, meta["description"]))
        self.assertTrue(lines[at - 1].startswith("- [Which AI visibility vendor comparisons have we published?]("))


if __name__ == "__main__":
    unittest.main()
