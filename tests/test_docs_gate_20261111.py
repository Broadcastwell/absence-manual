"""The STEP 3.3 writing gate on the docs (B117, 11 November 2026).

Pins the batch's corrections where they are published: the $19 credit without the derived $471 (owner
ruling R-150), the one ENTITY.md Organization on every brand page, the research pages' author from their
byline and their published date on the page, the ENTITY.md email, phone and footer line, the Kalvenor label,
the 404 wording that holds at every width, and brand 3.0.2's Procurement link. Three answer pages are served
from their released body, so their corrections are the plan's effective edits and their sources stay as
they are. No registered field-study page is touched.
"""
import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PLAN = ROOT / "tools/library-followup-20261105.json"
VISIBILITY = ROOT / "tools/library-visibility-20261105.json"
FREEZE = ROOT / "tools/library_field_freeze_navigation.json"
BRAND = ROOT / "overrides/brand.html"

R150 = "credited in full against the $490 Answer Repair within 30 days for the same account"
SAMPLE = "Sample data, fictional company"
ENTITY_25 = ("Broadcastwell asks ChatGPT, Claude, Perplexity, Google AI Overviews and Google AI Mode your buyers' "
             "questions, records who they name, and fixes the pages they read.")
ENTITY_SAME_AS = [
    "https://www.linkedin.com/company/broadcastwell", "https://x.com/broadcastwellhq",
    "https://www.youtube.com/@Broadcastwell", "https://www.instagram.com/broadcastwell/",
    "https://www.tiktok.com/@broadcastwell.com", "https://broadcastwell.substack.com/",
]
TEAM = {
    "Sairam Sivakumar": "Founder", "Priya Nair": "Management Consultant, delivery lead and reviewer",
    "Vikram Patel": "AI Architect and Specialist", "Ananya Rao": "AI Engineer", "Arjun Mehta": "Management Consultant",
    "Ethan Brooks": "Management Consultant", "Rohan Iyer": "AI Engineer", "Daniel Kim": "AI Engineer",
    "Marcus Reed": "AI Architect and Specialist", "Noah Bennett": "AI Architect and Specialist",
    "Lauren Chen": "AI Architect and Specialist", "Maya Thompson": "AI Architect and Specialist",
}

# A corrected sentence and the old wording it replaces, per source page.
CORRECTED = {
    "index.md": [("$19 once, " + R150 + ".", "so the repair then costs $471"),
                 ("### You need to understand the category {#i-need-to-understand-the-category}", "### I need to"),
                 ("### You need to evaluate a provider {#i-need-to-evaluate-a-provider}", None),
                 ("### You need to run a measurement program {#i-need-to-run-a-measurement-program}", None)],
    "operating-framework.md": [("The pricing page also states that the $19 live question is " + R150 + ".", "$471")],
    "services/bloomington-indiana.md": [("Credited in full against the $490 Answer Repair within 30 days for the same account.", "$471"),
                                        ("our phone number is (812) 345 7272.", "345-7272")],
    "media-kit.md": [("| Phone | (812) 345 7272 |", "812-345-7272"), ("> " + ENTITY_25, "builds the source-backed pages that change it")],
    "named-zero-times.md": [("measures it on the four engines of the 4 August 2026 collection", None),
                            ("should be treated as undated, not merely informal.", "treated as incomplete")],
    "engine-divergence.md": [("It does not claim the four engines of the 4 August 2026 collection have equal buyer share", None),
                             ("Substantial but partial agreement is consistent with the 14 of 32 result", "but incomplete")],
    "valid-measurement.md": [("its own instrument fell short in 7 of 40 categories.", "instrument is incomplete")],
    "for-buyers.md": [("That variation is how these systems work.", "That is not a fault, it is")],
    "measurement-noise.md": [("That movement is how the products work:", "This is not a defect, it is")],
    "absence-ladder.md": [("That answer shows if you are fighting for admission to a category or for preference within one; the two need different work, different content and different evidence.", "whether you are fighting")],
    "account-analyses.md": [("If you are named less, named more or described differently, it reports the change", "whether you are named less"),
                            ("Kalvenor Systems (" + SAMPLE + "), labeled as an example", None)],
    "model-releases.md": [("A Google model release does not by itself establish a change in either one.", "A Gemini model release")],
    "ai-referral-analytics-template.md": [("| ChatGPT, Microsoft Copilot and the other assistants Google lists |", "ChatGPT, Gemini, Microsoft Copilot")],
    "services/chatgpt-visibility.md": [("start with your own site when ChatGPT leaves you out or gets a fact wrong:", "the first place to look")],
    "standards/local-pages.md": [("4. **No thin pages.**", "No placeholder pages")],
    "resources/demos/receipt.md": [("Check your answers", "Check my answers")],
    "resources/guides/read-an-answer.md": [("## How can you tell whether an AI citation supports the claim beside it? {#how-can-i-tell-whether-an-ai-citation-supports-the-claim-beside-it}", "How can I tell"),
                                           ("- question: How can you tell whether an AI citation supports the claim beside it?", None)],
    "answers/agents/can-transportation-software-integrate-with-chatgpt.md": [("Alvys separately reports MCP access for ChatGPT;", "reports beta MCP access for ChatGPT;"),
                                                                             ("cannot establish that connector's permissions", "the beta connector")],
    "research/insights/engines-change-without-telling-you/index.md": [("The August 2026 observation used **four engines**", None)],
}
# The three pages served from their released body: corrected through the plan's effective edits.
RELEASED = {
    "answers/changes/what-should-a-vendor-say-while-an-incident-is-uncertain.md": "non-product PHP web pages taken offline for patching.",
    "answers/chatgpt/which-transportation-software-does-chatgpt-recommend.md": "Before reading the counts, decide which work you are evaluating: brokerage, carrier operations or shipper planning.",
    "answers/geo-basics/which-review-sites-for-geo-should-a-buyer-compare.md": "check who published it and which kind of evidence you are reading:",
}
# Research files whose bytes the research release policy pins because they carry the GEO 40% or 41% figure in
# its reviewed fragile framing (docs/research/data/research-release-policy.json): left exactly as reviewed.
PINNED_RESEARCH = {
    "docs/research/claims/index.md", "docs/research/evidence/quotable-numbers/index.md",
    "docs/research/evidence/unverified-numbers/index.md", "docs/research/insights/one-channel-is-a-risk/index.md",
    "docs/research/playbooks/pages-an-ai-engine-can-quote/index.md", "docs/research/sources/giomelakis-2019/index.md",
}
KALVENOR_PAGES = [
    "rfp-guide.md", "resources/three-rates.md", "chatgpt-business-hub/index.md", "chart-library.md", "account-analyses.md",
    "agency-training.md", "ai-visibility-course/index.md", "ai-visibility-course/lesson-1-one-ai-answer.md",
    "ai-visibility-course/lesson-3-find-the-base.md", "ai-visibility-course/lesson-4-read-the-sources.md",
    "ai-visibility-course/lesson-5-recheck-fairly.md", "cases/format.md", "chatgpt-business-hub/business-facts-file.md",
    "chatgpt-business-hub/context-pack.md", "chatgpt-business-hub/reconciliation-report.md",
    "content-templates/content-brief.md", "content-templates/content-strategy.md", "product-docs.md",
    "resources/playbooks/source-correction.md", "service-model.md", "vendor-facts.md",
]


def text(rel):
    return (DOCS / rel).read_text(encoding="utf-8")


def source_files():
    return [p for p in DOCS.rglob("*") if p.is_file() and p.suffix in {".md", ".txt", ".json", ".csv", ".html"}]


class GateCorrectionTests(unittest.TestCase):
    def test_each_corrected_sentence_is_published_once_and_the_old_wording_is_gone(self):
        for rel, rows in CORRECTED.items():
            body = text(rel)
            for new, old in rows:
                with self.subTest(page=rel, sentence=new[:60]):
                    self.assertEqual(body.count(new), 1)
                    if old:
                        self.assertNotIn(old, body)

    def test_released_pages_take_their_corrections_through_effective_edits_only(self):
        plan = json.loads(PLAN.read_bytes())
        for rel, after in RELEASED.items():
            with self.subTest(page=rel):
                self.assertTrue(any(e["after"].endswith(after) or after in e["after"] for e in plan["effective_edits"][rel]))
                self.assertNotIn("docs/" + rel, plan["source_changes"])

    def test_no_docs_page_or_download_shows_the_derived_471(self):
        for path in source_files():
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertNotIn("$471", path.read_text(encoding="utf-8", errors="replace"))

    def test_llms_source_states_the_credit_the_ruled_way(self):
        llms = text("llms.txt")
        self.assertIn("$19 once, " + R150 + ".", llms)
        self.assertIn("> " + ENTITY_25, llms)
        self.assertNotIn("Answer Operations: buyer answers built", llms)
        plan = json.loads(PLAN.read_bytes())
        afters = [e["after"] for e in plan["llms_edits"]]
        self.assertIn("$19 once, " + R150 + ".", afters)
        self.assertIn("> " + ENTITY_25, afters)

    def test_only_the_entity_email_addresses_and_phone_appear(self):
        for path in source_files():
            raw = path.read_text(encoding="utf-8", errors="replace")
            rel = path.relative_to(ROOT).as_posix()
            with self.subTest(path=rel):
                if rel not in PINNED_RESEARCH:
                    self.assertNotIn("research@broadcastwell.com", raw)
                if path.suffix == ".md":
                    # The JSON examples keep the business facts file's own +1-812-345-7272 form.
                    self.assertIsNone(re.search(r"(?<!\+1-)(\(812\) |812-)345-7272", raw))

    def test_every_kalvenor_page_carries_the_label(self):
        for rel in KALVENOR_PAGES:
            with self.subTest(page=rel):
                body = text(rel)
                self.assertIn("Kalvenor", body)
                self.assertIn("(" + SAMPLE + ")", body)

    def test_pinned_research_files_keep_their_reviewed_bytes(self):
        import hashlib
        policy = json.loads((DOCS / "research/data/research-release-policy.json").read_bytes())
        for rel in PINNED_RESEARCH:
            with self.subTest(path=rel):
                self.assertEqual(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest(), policy["reviewed_headline_files"][rel]["sha256"])

    def test_the_referral_template_names_gemini_once_and_keeps_its_downloads(self):
        # Section 14.5: the one mention is the test host the downloadable test cases carry.
        page = text("ai-referral-analytics-template.md")
        self.assertEqual(page.lower().count("gemini"), 1)
        self.assertIn("`gemini.google.com`", page)
        cases = (DOCS / "assets/ai-referral/ai-referrals-test-cases.csv").read_text(encoding="utf-8")
        self.assertIn("gemini.google.com,referral,no,", cases)

    def test_registered_field_study_pages_are_untouched(self):
        frozen = json.loads(FREEZE.read_bytes())["pages"]
        changed = set(json.loads(PLAN.read_bytes())["source_changes"])
        for rel in frozen:
            with self.subTest(page=rel):
                self.assertNotIn("docs/" + rel, changed)


class EntityTemplateTests(unittest.TestCase):
    def setUp(self):
        self.brand = BRAND.read_text(encoding="utf-8")

    def test_the_one_organization_uses_the_entity_texts(self):
        self.assertIn('"description": "' + ENTITY_25 + '"', self.brand)
        self.assertIn('{% set bw_org_id = "https://broadcastwell.com/#organization" %}', self.brand)
        same = re.search(r'"sameAs": (\[[^\]]*\])\n\} %\}\n\{#- The team record', self.brand, re.S).group(1)
        self.assertEqual(json.loads(same), ENTITY_SAME_AS)
        for needed in ('"legalName": "Broadcastwell LLC"', '"telephone": "+18123457272"', '"streetAddress": "517 E Kirkwood Ave"',
                       '"postalCode": "47408"', '"name": "Sairam Sivakumar", "jobTitle": "Founder"', '"logo": "https://'):
            self.assertIn(needed, self.brand)

    def test_the_team_record_is_the_twelve_with_their_roles(self):
        import sys
        sys.path.insert(0, str(ROOT / "tools"))
        from team_record import TEAM as RECORD, expected_author
        block = re.search(r'\{% set bw_team = (\{.*?\}) %\}', self.brand, re.S).group(1)
        self.assertEqual(json.loads(block), TEAM)
        self.assertEqual(RECORD, TEAM)
        self.assertEqual(expected_author({"page_class": "research", "lead": "Priya Nair"})["jobTitle"], TEAM["Priya Nair"])
        self.assertEqual(expected_author({"library_cluster": "fixes", "library_owner": "Rohan Iyer, AI Engineer"})["name"], "Rohan Iyer")
        self.assertEqual(expected_author({"page_class": "page"}), {"@type": "Organization", "@id": "https://broadcastwell.com/#organization", "name": "Broadcastwell"})

    def test_every_research_lead_and_library_owner_is_one_of_the_twelve(self):
        vis = json.loads(VISIBILITY.read_bytes())
        for rel, row in vis["pages"].items():
            meta = row["meta"]
            name = meta.get("lead") if meta.get("page_class") == "research" else (meta.get("library_owner") or "").split(",")[0].strip()
            if name:
                with self.subTest(page=rel):
                    self.assertIn(name, TEAM)

    def test_research_pages_show_their_published_date(self):
        self.assertIn("Published <time datetime=\"{{ (page.meta.get('published') | string)[:10] }}\">", self.brand)
        self.assertIn('<p class="bw-docs-dateline">Published {{ bw_date(page.meta.get("date_published")) }}.', self.brand)

    def test_not_found_page_wording_holds_at_every_width(self):
        page = (ROOT / "overrides/404.html").read_text(encoding="utf-8")
        self.assertNotIn("navigation above", page)
        self.assertIn("or pick a chapter from the manual's chapter navigation.", page)


class Brand302Tests(unittest.TestCase):
    def test_footer_legal_rows_gain_procurement_after_integrity_standard(self):
        shared = (ROOT / "overrides/partials/brand/footer-shared.html").read_text(encoding="utf-8")
        self.assertIn('<li><a href="https://broadcastwell.com/integrity">Integrity Standard</a></li>'
                      '<li><a href="https://broadcastwell.com/procurement">Procurement</a></li>', shared)
        today = (ROOT / "overrides/partials/brand/footer-today.html").read_text(encoding="utf-8")
        self.assertIn('<li><a href="https://broadcastwell.com/cookies">Cookies</a></li>'
                      '<li><a href="https://broadcastwell.com/procurement">Procurement</a></li>', today)
        self.assertIn('<p class="bw-site-footer__line">When you broadcast, broadcast well.</p>', today)
        self.assertNotIn("Answer Operations. Buyer answers", today)

    # STEP 3.3 B146: brand 3.0.2 is vendored, so the wordmark rule and the Procurement link come from
    # vendor/brand/ itself and the B117 overlays (a docs-layer wordmark rule, withBrand302) are gone.
    def test_the_wordmark_never_wraps(self):
        css = (ROOT / "docs/assets/brand/docs.css").read_text(encoding="utf-8")
        components = (ROOT / "vendor/brand/components.css").read_text(encoding="utf-8")
        rule = re.search(r"^\.bw-logotype\{[^}]*\}", components, re.M).group(0)
        self.assertIn("flex-shrink:0;white-space:nowrap;", rule)
        self.assertIn(rule, css)
        layer = (ROOT / "tools/brand-docs.css").read_text(encoding="utf-8")
        self.assertNotRegex(layer, r"\.bw-logotype\s*\{[^}]*white-space")

    def test_the_vendored_package_carries_procurement(self):
        nav = json.loads((ROOT / "vendor/brand/nav.json").read_text(encoding="utf-8"))
        labels = [item["label"] for item in nav["footer"]["legal"]]
        self.assertEqual(labels.index("Procurement"), labels.index("Integrity Standard") + 1)
        version = json.loads((ROOT / "vendor/brand/VERSION.json").read_text(encoding="utf-8"))
        self.assertEqual(version["version"], "3.0.2")
        out = subprocess.run(["node", "--input-type=module", "-e",
                              "import * as c from './tools/brand_chrome.mjs';"
                              "process.stdout.write(String('withBrand302' in c));"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(out.stdout, "false", out.stderr)


if __name__ == "__main__":
    unittest.main()
