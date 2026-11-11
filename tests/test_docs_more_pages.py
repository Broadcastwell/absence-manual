"""Second set of reference pages added on 9 November 2026: services, course, research tools and elevations."""
import csv
import hashlib
import json
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
SITE = "https://docs.broadcastwell.com/"
UPDATED_LINE = "Updated 9 November 2026."

INDUSTRIES = [
    "construction-software", "crm-software", "dealership-software", "dental-software", "field-service-software",
    "hotel-software", "insurance-agency-software", "legal-practice-software", "loan-origination-software",
    "project-management-software", "property-management-software", "radiology-software",
    "transportation-software", "veterinary-software",
]
ENGINES = {
    "chatgpt-visibility": "ChatGPT", "claude-visibility": "Claude", "perplexity-visibility": "Perplexity",
    "google-ai-overviews-visibility": "Google AI Overviews", "google-ai-mode-visibility": "Google AI Mode",
}
# Each page with the buyer phrase that must appear in its title and opening words, and a word of its URL.
PAGES = {"ai-search-glossary.md": ("glossary", "ai-search-glossary")}
for slug in ENGINES:
    PAGES["services/%s.md" % slug] = (slug.replace("-", " "), slug)
for slug in INDUSTRIES:
    PAGES["services/industries/%s.md" % slug] = (slug.replace("-", " "), slug)
PAGES.update({
    "industry-benchmarks.md": ("industry benchmarks", "industry-benchmarks"),
    "services/bloomington-indiana.md": ("bloomington", "bloomington-indiana"),
    "ai-visibility-course/index.md": ("course", "ai-visibility-course"),
    "ai-visibility-course/lesson-1-one-ai-answer.md": ("course", "lesson-1"),
    "ai-visibility-course/lesson-2-repeat-the-question.md": ("course", "lesson-2"),
    "ai-visibility-course/lesson-3-find-the-base.md": ("course", "lesson-3"),
    "ai-visibility-course/lesson-4-read-the-sources.md": ("course", "lesson-4"),
    "ai-visibility-course/lesson-5-recheck-fairly.md": ("course", "lesson-5"),
    "research-report.md": ("research report", "research-report"),
    "print-edition.md": ("print edition", "print-edition"),
    "search-patents.md": ("search patents", "search-patents"),
    "product-docs.md": ("product documentation", "product-docs"),
    "launchpad/certificate.md": ("certificate", "certificate"),
    "agency-training.md": ("agency training", "agency-training"),
    "ai-referral-analytics-template.md": ("ai referral", "ai-referral"),
    "browser-extension.md": ("browser extension", "browser-extension"),
    "open-data.md": ("open data", "open-data"),
    "chart-library.md": ("chart library", "chart-library"),
    "comparisons.md": ("comparisons", "comparisons"),
})
DOWNLOADS = [
    DOCS / "assets/ai-referral/ai-referrals-channel-group.csv",
    DOCS / "assets/ai-referral/ai-referrals-source-regex.txt",
    DOCS / "assets/ai-referral/ai-referrals-test-cases.csv",
    DOCS / "assets/playbooks/source-correction-steps-2026-11-09.csv",
    DOCS / "assets/product-docs/kalvenor-connector-tools-list.json",
    DOCS / "assets/research/print/research-report-sha256.txt",
]
APP_TEMPLATE_PATTERN = (r"^(.*\.)?(chatgpt\.com|chat\.openai\.com|claude\.ai|perplexity\.ai|copilot\.microsoft\.com"
                        r"|copilot\.cloud\.microsoft)$")
PRINT_EDITION = DOCS / "assets/research/print/Study1_The_Shortlist_Gap_print_edition_2026-11-09.pdf"
STUDY1 = DOCS / "assets/research/study1/Study1_The_Shortlist_Gap_2026-09.pdf"
STUDY1_SHA256 = "21d03ff5eb70575ca59ad548b2930919bf1aeb3ad5e760621ac307cc73e8e881"
LINK = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")


def route(name):
    return SITE + (name[:-len("index.md")] if name.endswith("/index.md") else name[:-3] + "/")


def body_of(name):
    return hub.split_page(DOCS / name)


def resolve(page, target):
    return (DOCS / page).parent.joinpath(target).resolve().relative_to(DOCS.resolve()).as_posix()


def public_texts():
    texts = {"docs/" + name: (DOCS / name).read_text(encoding="utf-8") for name in PAGES}
    for path in DOWNLOADS:
        texts[path.relative_to(ROOT).as_posix()] = path.read_text(encoding="utf-8")
    llms = (DOCS / "llms.txt").read_text(encoding="utf-8")
    texts["docs/llms.txt (new lines)"] = "\n".join(
        line for line in llms.splitlines() if any("](%s)" % route(name) in line for name in PAGES))
    return texts


def near_duplicate_rows():
    new = {name: hub.shingles(hub.prose_tokens((DOCS / name).read_text(encoding="utf-8"))) for name in PAGES}
    rows = []
    for path in sorted(DOCS.rglob("*.md")):
        rel = path.relative_to(DOCS).as_posix()
        existing = new.get(rel) or hub.shingles(hub.prose_tokens(path.read_text(encoding="utf-8")))
        if not existing:
            continue
        for name, grams in new.items():
            if name != rel and (rel not in new or name < rel):
                rows.append((hub.overlap(grams, existing), name, rel))
    return sorted(rows, reverse=True)


class PageStructureTests(unittest.TestCase):
    def test_each_page_has_one_question_dates_and_article_inputs(self):
        for name in PAGES:
            with self.subTest(page=name):
                meta, body = body_of(name)
                self.assertTrue(meta["title"].endswith("?") and len(meta["title"]) < 60, meta["title"])
                self.assertEqual(meta["headline"], meta["title"])
                self.assertTrue(150 <= len(meta["description"]) <= 160, len(meta["description"]))
                self.assertEqual(meta["page_class"], "page")
                self.assertEqual(meta["schema_type"], "Article")
                self.assertEqual(meta["date_published"], "2026-11-09T00:00:00+00:00")
                # STEP 3.3 B117 changed some of these pages; their modified date is that change.
                self.assertIn(meta["date_modified"], ("2026-11-09T00:00:00+00:00", "2026-11-11T07:30:00Z"))
                self.assertEqual(meta["template"], "business-hub.html")
                self.assertEqual(re.findall(r"(?m)^# (.+)$", body), [meta["title"]])
                updated = "Updated 11 November 2026." if meta["date_modified"] == "2026-11-11T07:30:00Z" else UPDATED_LINE
                self.assertIn("\n" + updated + "\n", body)
                self.assertIn("## Sources", body)
                # Fenced code is not a configured extension, and a <title> in a body is read as the page title.
                self.assertNotIn("```", body)
                self.assertNotIn("<title", body)

    def test_titles_and_descriptions_are_unique_across_the_site(self):
        visibility = json.loads((ROOT / "tools/library-visibility-20261105.json").read_bytes())["pages"]
        seen_titles, seen_descriptions = {}, {}
        for path in DOCS.rglob("*.md"):
            rel = path.relative_to(DOCS).as_posix()
            try:
                meta = visibility[rel]["meta"] if rel in visibility else hub.split_page(path)[0]
            except (AttributeError, yaml.YAMLError):
                continue
            seen_titles.setdefault(meta.get("title"), []).append(rel)
            seen_descriptions.setdefault(meta.get("description"), []).append(rel)
        for name in PAGES:
            with self.subTest(page=name):
                meta, _ = body_of(name)
                self.assertEqual(seen_titles[meta["title"]], [name])
                self.assertEqual(seen_descriptions[meta["description"]], [name])

    def test_buyer_phrase_in_title_url_and_first_sixty_words(self):
        for name, (phrase, url_word) in PAGES.items():
            with self.subTest(page=name):
                meta, body = body_of(name)
                self.assertIn(phrase, meta["title"].lower())
                self.assertIn(url_word, route(name))
                self.assertIn(phrase, first.opening_words(body).lower())

    def test_pages_link_out_to_existing_pages_and_every_link_resolves(self):
        for name in PAGES:
            with self.subTest(page=name):
                _, body = body_of(name)
                targets = LINK.findall(body)
                for target in targets:
                    self.assertTrue((DOCS / name).parent.joinpath(target).resolve().is_file(), target)
                existing = {resolve(name, t) for t in targets} - set(PAGES)
                self.assertGreaterEqual(len(existing), 2, "links out to two existing docs pages")
                self.assertGreaterEqual(len(set(targets)), 3)

    def test_each_page_is_linked_from_at_least_two_existing_pages(self):
        inbound = {name: set() for name in PAGES}
        for path in DOCS.rglob("*.md"):
            rel = path.relative_to(DOCS).as_posix()
            if rel in PAGES:
                continue
            text = path.read_text(encoding="utf-8")
            for target in LINK.findall(text):
                try:
                    hit = resolve(rel, target)
                except ValueError:
                    continue
                if hit in inbound:
                    inbound[hit].add(rel)
            for href in re.findall(r'href="(/[^"#]*)"', text):
                for name in PAGES:
                    if SITE.rstrip("/") + href == route(name):
                        inbound[name].add(rel)
        for name, sources in inbound.items():
            with self.subTest(page=name):
                self.assertGreaterEqual(len(sources), 2, sorted(sources))
                self.assertIn("resources.md", sources)

    def test_pages_stay_outside_the_navigation_and_reach_llms(self):
        root_nav = yaml.safe_load((DOCS / ".pages").read_text(encoding="utf-8"))["nav"]
        mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        for name in PAGES:
            with self.subTest(page=name):
                self.assertNotIn(name, root_nav)
                self.assertNotIn(name.split("/")[0], root_nav)
                self.assertNotIn(name, mkdocs)
        for folder in ("services", "services/industries", "ai-visibility-course", "launchpad"):
            self.assertFalse((DOCS / folder / ".pages").exists())
        llms = (DOCS / "llms.txt").read_text(encoding="utf-8")
        for name in PAGES:
            with self.subTest(page=name):
                self.assertEqual(llms.count("](%s)" % route(name)), 1)

    def test_llms_lines_follow_the_first_reference_block_in_order(self):
        lines = (DOCS / "llms.txt").read_text(encoding="utf-8").splitlines()
        anchor = next(i for i, line in enumerate(lines)
                      if line.startswith("- [When do we write local pages for a city or region?]("))
        block = lines[anchor + 1:anchor + 1 + len(PAGES)]
        self.assertEqual([re.search(r"\]\((\S+)\)", line).group(1) for line in block], [route(n) for n in PAGES])
        for name, line in zip(PAGES, block):
            meta, _ = body_of(name)
            self.assertEqual(line, "- [%s](%s): %s" % (meta["title"], route(name), meta["description"]))


class CopyRuleTests(unittest.TestCase):
    def test_no_banned_string_dash_or_exclamation_in_any_new_public_text(self):
        for name, text in public_texts().items():
            with self.subTest(file=name):
                self.assertEqual(hub.banned_hits(text), [])

    def test_any_mention_of_five_engines_names_all_five(self):
        for name, text in public_texts().items():
            with self.subTest(file=name):
                if re.search(r"(?i)\bfive[- ]engines?\b", text):
                    self.assertIn(hub.FIVE_ENGINE_LIST, text)

    def test_only_the_published_ladder_prices_appear(self):
        allowed = {"$19", "$471", "$490", "$3,900", "$3,410", "$5,500"}
        for name, text in public_texts().items():
            with self.subTest(file=name):
                self.assertEqual(set(re.findall(r"\$[0-9][0-9,]*", text)) - allowed, set())

    def test_no_client_case_page_or_model_string(self):
        for name, text in public_texts().items():
            with self.subTest(file=name):
                self.assertNotRegex(text.lower(), r"ai-visibility-(audit|diagnostic|case-study)")
                self.assertNotRegex(text, r"(?i)\bgpt-?\d|\bo\d-(mini|pro)\b|\bn8n\b")

    def test_print_stylesheet_has_no_important_flag(self):
        css = (DOCS / "assets/print/print-edition.css").read_text(encoding="utf-8")
        self.assertTrue(css.lstrip().startswith("/*"))
        self.assertNotIn("!", css)
        self.assertIn("@media print", css)


class ServicePageTests(unittest.TestCase):
    def test_engine_pages_measure_all_five_and_name_their_engine(self):
        for slug, engine in ENGINES.items():
            with self.subTest(engine=engine):
                _, body = body_of("services/%s.md" % slug)
                self.assertIn(hub.FIVE_ENGINE_LIST, body)
                self.assertIn(engine, first.opening_words(body))

    def test_industry_pages_link_both_answers_pages_and_the_index(self):
        answers = {p.name for p in (DOCS / "answers/industries").glob("*.md")}
        self.assertEqual(len(INDUSTRIES), 14)
        for slug in INDUSTRIES:
            with self.subTest(industry=slug):
                _, body = body_of("services/industries/%s.md" % slug)
                linked = {Path(t).name for t in LINK.findall(body) if "answers/industries/" in t}
                self.assertGreaterEqual(len(linked & answers), 2)
                self.assertIn("https://index.broadcastwell.com/", body)

    def test_only_one_place_page_and_it_follows_the_local_pages_rule(self):
        places = [p.name for p in (DOCS / "services").glob("*.md") if p.stem not in ENGINES]
        self.assertEqual(places, ["bloomington-indiana.md"])
        _, body = body_of("services/bloomington-indiana.md")
        first_section = body.split("\n## ", 2)[1]
        self.assertTrue(first_section.startswith("The local evidence for this page"))
        self.assertIn("517 E Kirkwood Ave, Bloomington, IN 47408", first_section)
        self.assertIn("(../standards/local-pages.md)", first_section)
        self.assertIn("services/bloomington-indiana.md", (DOCS / "standards/local-pages.md").read_text(encoding="utf-8"))


class DownloadTests(unittest.TestCase):
    def test_ai_referral_pattern_matches_the_app_template_and_its_test_cases(self):
        _, body = body_of("ai-referral-analytics-template.md")
        self.assertIn("    " + APP_TEMPLATE_PATTERN + "\n", body)
        text = (DOCS / "assets/ai-referral/ai-referrals-source-regex.txt").read_text(encoding="utf-8")
        self.assertIn("\n" + APP_TEMPLATE_PATTERN + "\n", text)
        with (DOCS / "assets/ai-referral/ai-referrals-channel-group.csv").open(encoding="utf-8", newline="") as handle:
            self.assertEqual(next(csv.DictReader(handle))["value"], APP_TEMPLATE_PATTERN)
        pattern = re.compile(APP_TEMPLATE_PATTERN)
        with (DOCS / "assets/ai-referral/ai-referrals-test-cases.csv").open(encoding="utf-8", newline="") as handle:
            cases = list(csv.DictReader(handle))
        self.assertEqual(len(cases), 13)
        for case in cases:
            with self.subTest(source=case["source"]):
                self.assertEqual(bool(pattern.fullmatch(case["source"])), case["matches_pattern"] == "yes")

    def test_googles_broad_example_would_catch_the_sources_the_page_names(self):
        broad = re.compile(r"^.*ai|.*\.openai.*|.*chatgpt.*|.*gemini.*|.*gpt.*|.*copilot.*|.*perplexity.*")
        for source in ("email", "mail.example.com", "chatgpt.com.example"):
            self.assertTrue(broad.match(source))
            self.assertIsNone(re.compile(APP_TEMPLATE_PATTERN).fullmatch(source))

    def test_print_edition_is_a_cover_sheet_plus_the_unchanged_report(self):
        from pypdf import PdfReader
        self.assertEqual(hashlib.sha256(STUDY1.read_bytes()).hexdigest(), STUDY1_SHA256)
        edition, original = PdfReader(PRINT_EDITION), PdfReader(STUDY1)
        self.assertEqual(len(edition.pages), len(original.pages) + 1)
        self.assertEqual(len(edition.pages), 22)
        cover = " ".join(edition.pages[0].extract_text().split())
        for needed in ("10.5281/zenodo.22982426", STUDY1_SHA256, "US Letter", "CC BY 4.0"):
            self.assertIn(needed, cover)
        for index, page in enumerate(original.pages):
            self.assertEqual(edition.pages[index + 1].get_contents().get_data(), page.get_contents().get_data())

    def test_checksum_list_matches_every_listed_file(self):
        lines = [line for line in (DOCS / "assets/research/print/research-report-sha256.txt").read_text(
            encoding="utf-8").splitlines() if line and not line.startswith("#")]
        self.assertEqual(len(lines), 10)
        for line in lines:
            digest, url = line.split("  ")
            with self.subTest(file=url):
                path = DOCS / url.removeprefix(SITE)
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)

    def test_research_report_table_matches_the_pdfs(self):
        from pypdf import PdfReader
        _, body = body_of("research-report.md")
        rows = re.findall(r"\| \[[^\]]+\]\((assets/research/[^)]+\.pdf)\) \| [^|]+ \| (\d+) \| (\d+) KB \|", body)
        self.assertEqual(len(rows), 7)
        for path, pages, size in rows:
            with self.subTest(pdf=path):
                self.assertEqual(len(PdfReader(DOCS / path).pages), int(pages))
                self.assertEqual(round((DOCS / path).stat().st_size / 1024), int(size))

    def test_connector_response_lists_six_read_only_sample_tools(self):
        data = json.loads((DOCS / "assets/product-docs/kalvenor-connector-tools-list.json").read_text(encoding="utf-8"))
        self.assertTrue(data["label"].startswith("SAMPLE DATA."))
        tools = data["response"]["result"]["tools"]
        self.assertEqual([t["name"] for t in tools], ["get_company", "get_pricing", "get_fit", "get_integrations",
                                                     "get_compliance", "get_links"])
        self.assertTrue(all(t["annotations"]["readOnlyHint"] for t in tools))

    def test_source_correction_steps_file_has_seven_owned_steps(self):
        with (DOCS / "assets/playbooks/source-correction-steps-2026-11-09.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual([r["step"] for r in rows], [str(i) for i in range(1, 8)])
        self.assertTrue(all(r["owner"] and r["stop_if"] for r in rows))


class ContentTests(unittest.TestCase):
    def test_glossary_defines_citation_and_every_term_has_an_anchor_and_a_source(self):
        _, body = body_of("ai-search-glossary.md")
        entries = re.split(r"(?m)^### ", body)[1:]
        self.assertGreaterEqual(len(entries), 35)
        for entry in entries:
            with self.subTest(term=entry.splitlines()[0]):
                self.assertRegex(entry.splitlines()[0], r"\{#[a-z0-9-]+\}$")
                self.assertRegex(entry, r"\]\((https?://|[a-z0-9./-]+\.(md|csv|json))|<a href=\"https?://")
        self.assertIn("{#citation}", body)

    def test_patent_page_cites_nine_verified_records(self):
        _, body = body_of("search-patents.md")
        numbers = set(re.findall(r"patents\.google\.com/patent/([A-Z0-9]+)/en", body))
        self.assertEqual(numbers, {"US11354342B2", "US11769017B1", "US11886828B1", "US20250005303A1",
                                   "US20240289407A1", "US11663201B2", "US12579133B2", "WO2024064249A1",
                                   "US20240296295A1"})

    def test_certificate_page_states_the_published_pass_rule(self):
        launchpad = (DOCS / "launchpad.md").read_text(encoding="utf-8")
        self.assertIn("Pass at least 20/25 questions and all five safety questions, plus the structured case at 6/8",
                      launchpad)
        _, body = body_of("launchpad/certificate.md")
        for needed in ("At least 20 of 25 correct", "All five correct", "At least 6 of 8",
                       "https://app.broadcastwell.com/launchpad/verify/<certificate ID>", "not accredited"):
            self.assertIn(needed, body)

    def test_fair_recheck_table_matches_the_repeat_disagreement_data(self):
        text = (DOCS / "resources/guides/fair-recheck.md").read_text(encoding="utf-8")
        with (DOCS / "research/data/repeat-disagreement.csv").open(encoding="utf-8", newline="") as handle:
            rows = {r["engine"]: r for r in csv.DictReader(handle) if r["category"] == "all"}
        for engine in hub.FIVE_ENGINES:
            row = rows[engine]
            expected = "<tr><td>%s</td><td>%s of %s</td><td>%.1f%%</td><td>%.1f%% to %.1f%%</td></tr>" % (
                engine, format(int(row["mixed_complete_vendor_question_cells"]), ","),
                format(int(row["complete_vendor_question_cells"]), ","), float(row["mixed_pct"]),
                float(row["wilson_low_pct"]), float(row["wilson_high_pct"]))
            with self.subTest(engine=engine):
                self.assertIn(expected, text)

    def test_comparisons_page_lists_thirteen_existing_answers(self):
        _, body = body_of("comparisons.md")
        answers = {t for t in LINK.findall(body) if t.startswith("answers/")}
        self.assertEqual(len(answers), 14)  # thirteen comparisons plus the case-study answer
        for target in answers:
            self.assertTrue((DOCS / target).is_file(), target)


class NearDuplicateTests(unittest.TestCase):
    def test_no_new_page_shares_more_than_a_fifth_of_its_six_word_sequences(self):
        worst = near_duplicate_rows()[0]
        self.assertLessEqual(worst[0], hub.NEAR_DUPLICATE_LIMIT, worst)


if __name__ == "__main__":
    unittest.main()
