"""Reference pages added on 9 November 2026: structure, copy rules, downloads, links and overlap."""
import csv
import math
import re
import sys
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_chatgpt_business_hub as hub  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE = "https://docs.broadcastwell.com/"

# Each page with the buyer phrase that must appear in its title, H1, URL and opening words.
PAGES = {
    "release-notes.md": "release notes",
    "model-releases.md": "model release",
    "articles.md": "articles",
    "media-kit.md": "media kit",
    "operating-framework.md": "operating framework",
    "service-model.md": "service model",
    "rfp-guide.md": "rfp",
    "content-templates/content-brief.md": "content brief",
    "content-templates/content-strategy.md": "content strategy",
    "cite.md": "cite",
    "webinars.md": "webinars",
    "workshops.md": "workshops",
    "cases/format.md": "completed ai visibility case",
    "standards/local-pages.md": "local pages",
}
URL_WORDS = {
    "release-notes.md": "release-notes", "model-releases.md": "model-releases", "articles.md": "articles",
    "media-kit.md": "media-kit", "operating-framework.md": "operating-framework", "service-model.md": "service-model",
    "rfp-guide.md": "rfp", "content-templates/content-brief.md": "content-brief",
    "content-templates/content-strategy.md": "content-strategy", "cite.md": "cite", "webinars.md": "webinars",
    "workshops.md": "workshops", "cases/format.md": "cases", "standards/local-pages.md": "local-pages",
}
DOWNLOADS = DOCS / "content-templates" / "downloads"
CITATIONS = DOCS / "assets" / "citations"
UPDATED_LINE = "Updated 9 November 2026."
TEAM = [
    ("Sairam Sivakumar", "Founder"),
    ("Priya Nair", "Management Consultant, delivery lead and reviewer"),
    ("Vikram Patel", "AI Architect and Specialist"),
    ("Ananya Rao", "AI Engineer"),
    ("Arjun Mehta", "Management Consultant"),
    ("Ethan Brooks", "Management Consultant"),
    ("Rohan Iyer", "AI Engineer"),
    ("Daniel Kim", "AI Engineer"),
    ("Marcus Reed", "AI Architect and Specialist"),
    ("Noah Bennett", "AI Architect and Specialist"),
    ("Lauren Chen", "AI Architect and Specialist"),
    ("Maya Thompson", "AI Architect and Specialist"),
]


def route(name):
    return SITE + name[:-3] + "/"


def body_of(name):
    return hub.split_page(DOCS / name)


def opening_words(body, count=60):
    after_h1 = body.split("\n# ", 1)[-1].split("\n", 1)[1]
    return " ".join(after_h1.split()[:count])


def new_public_texts():
    texts = {"docs/" + name: (DOCS / name).read_text(encoding="utf-8") for name in PAGES}
    for path in sorted(DOWNLOADS.iterdir()) + sorted(CITATIONS.iterdir()):
        texts[path.relative_to(ROOT).as_posix()] = path.read_text(encoding="utf-8")
    llms = (DOCS / "llms.txt").read_text(encoding="utf-8")
    texts["docs/llms.txt (new lines)"] = "\n".join(
        line for line in llms.splitlines() if any(route(name) in line for name in PAGES))
    return texts


def wilson(k, n, z=1.959963984540054):
    p = k / n
    centre = p + z * z / (2 * n)
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    scale = 1 + z * z / n
    return round(100 * (centre - margin) / scale, 1), round(100 * (centre + margin) / scale, 1)


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
                self.assertTrue(meta["title"].endswith("?") and len(meta["title"]) < 60)
                self.assertEqual(meta["headline"], meta["title"])
                self.assertTrue(150 <= len(meta["description"]) <= 160)
                self.assertEqual(meta["page_class"], "page")
                self.assertEqual(meta["schema_type"], "Article")
                self.assertEqual(meta["date_published"], "2026-11-09T00:00:00+00:00")
                # STEP 3.3 B117 changed some of these pages; their modified date is that change.
                self.assertIn(meta["date_modified"], ("2026-11-09T00:00:00+00:00", "2026-11-11T07:30:00Z"))
                self.assertEqual(meta["template"], "business-hub.html")
                self.assertEqual(re.findall(r"(?m)^# (.+)$", re.sub(r"(?ms)^```.*?^```", "", body)), [meta["title"]])
                updated = "Updated 11 November 2026." if meta["date_modified"] == "2026-11-11T07:30:00Z" else UPDATED_LINE
                self.assertIn("\n" + updated + "\n", body)
                self.assertIn("## Sources", body)

    def test_buyer_phrase_in_title_url_and_first_sixty_words(self):
        for name, phrase in PAGES.items():
            with self.subTest(page=name):
                meta, body = body_of(name)
                self.assertIn(phrase, meta["title"].lower())
                self.assertIn(URL_WORDS[name], route(name))
                self.assertIn(phrase, opening_words(body).lower())

    def test_pages_link_to_existing_pages_and_resolve(self):
        for name in PAGES:
            with self.subTest(page=name):
                _, body = body_of(name)
                targets = re.findall(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)", body)
                existing = [t for t in targets if (DOCS / name).parent.joinpath(t).resolve().relative_to(DOCS.resolve()).as_posix() not in PAGES]
                self.assertGreaterEqual(len(existing), 1, "links out to an existing docs page")
                self.assertGreaterEqual(len(set(targets)), 3)
                for target in targets:
                    self.assertTrue((DOCS / name).parent.joinpath(target).resolve().is_file(), target)

    def test_pages_stay_outside_the_navigation_but_reach_llms_and_an_existing_hub(self):
        # The navigation is shared by the 45 registered field-study pages, so it must not change.
        root_nav = yaml.safe_load((DOCS / ".pages").read_text(encoding="utf-8"))["nav"]
        mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        for name in PAGES:
            with self.subTest(page=name):
                self.assertNotIn(name, root_nav)
                self.assertNotIn(name.split("/")[0].removesuffix(".md"), root_nav)
                self.assertNotIn(name, mkdocs)
        for folder in ("content-templates", "cases", "standards"):
            self.assertFalse((DOCS / folder / ".pages").exists())
        llms = (DOCS / "llms.txt").read_text(encoding="utf-8")
        resources = (DOCS / "resources.md").read_text(encoding="utf-8")
        for name in PAGES:
            with self.subTest(page=name):
                self.assertEqual(llms.count("](%s)" % route(name)), 1)
                self.assertIn("](%s)" % name, resources)

    def test_llms_lines_sit_in_the_guide_block_after_the_business_facts_file(self):
        lines = (DOCS / "llms.txt").read_text(encoding="utf-8").splitlines()
        anchor = next(i for i, line in enumerate(lines) if line.startswith("- [Broadcastwell business facts file]("))
        block = lines[anchor + 1:anchor + 1 + len(PAGES)]
        self.assertEqual([re.search(r"\]\((\S+)\)", line).group(1) for line in block], [route(name) for name in PAGES])
        for name, line in zip(PAGES, block):
            meta, _ = body_of(name)
            self.assertEqual(line, "- [%s](%s): %s" % (meta["title"], route(name), meta["description"]))


class CopyRuleTests(unittest.TestCase):
    def test_no_banned_string_dash_or_exclamation_in_any_new_public_file(self):
        for name, text in new_public_texts().items():
            with self.subTest(file=name):
                self.assertEqual(hub.banned_hits(text), [])

    def test_any_mention_of_five_engines_names_all_five(self):
        for name, text in new_public_texts().items():
            with self.subTest(file=name):
                if re.search(r"(?i)\bfive[- ]engines?\b", text) and not name.endswith((".bib", ".ris")):
                    self.assertIn(hub.FIVE_ENGINE_LIST, text)

    def test_only_the_six_published_prices_appear(self):
        allowed = {"$19", "$471", "$490", "$3,900", "$3,410", "$5,500"}
        for name, text in new_public_texts().items():
            with self.subTest(file=name):
                self.assertEqual(set(re.findall(r"\$[0-9][0-9,]*", text)) - allowed, set())

    def test_no_client_case_page_or_withheld_name_is_linked(self):
        for name, text in new_public_texts().items():
            with self.subTest(file=name):
                self.assertNotRegex(text.lower(), r"ai-visibility-(audit|diagnostic|case-study)")


class DownloadTests(unittest.TestCase):
    def test_each_template_has_matching_markdown_and_csv_fields(self):
        for stem in ("content-brief", "content-strategy"):
            with self.subTest(template=stem):
                for kind, field_column in (("template", "field"), ("kalvenor-sample", "field")):
                    markdown = (DOWNLOADS / ("%s-%s.txt" % (stem, kind))).read_text(encoding="utf-8")
                    md_fields = [row.split(" | ")[0].lstrip("| ") for row in markdown.splitlines()
                                 if row.startswith("| ") and not row.startswith(("| Field", "| ---"))]
                    with (DOWNLOADS / ("%s-%s.csv" % (stem, kind))).open(encoding="utf-8", newline="") as handle:
                        rows = list(csv.DictReader(handle))
                    self.assertEqual(md_fields, [row[field_column] for row in rows])
                    self.assertEqual(len(rows), 18)
                    if kind == "kalvenor-sample":
                        self.assertTrue(all(row["sample"] == "SAMPLE DATA, fictional" for row in rows))
                        self.assertIn("Fictional sample.", markdown)
                    else:
                        self.assertTrue(all(row["value"] == "" for row in rows))

    def test_template_pages_offer_both_formats_with_download_names(self):
        for stem in ("content-brief", "content-strategy"):
            _, body = body_of("content-templates/%s.md" % stem)
            for kind in ("template", "kalvenor-sample"):
                self.assertIn('(downloads/%s-%s.txt){: download="%s-%s.md" }' % (stem, kind, stem, kind), body)
                self.assertIn('(downloads/%s-%s.csv){: download="%s-%s.csv" }' % (stem, kind, stem, kind), body)

    def test_citation_files_hold_the_same_records_as_the_page(self):
        bib = (CITATIONS / "broadcastwell-research.bib").read_text(encoding="utf-8")
        ris = (CITATIONS / "broadcastwell-research.ris").read_text(encoding="utf-8")
        _, body = body_of("cite.md")
        self.assertEqual(len(re.findall(r"(?m)^@\w+\{", bib)), 21)
        self.assertEqual(len(re.findall(r"(?m)^TY  - ", ris)), 21)
        self.assertEqual(len(re.findall(r"(?m)^ER  - $", ris)), 21)
        page_dois = set(re.findall(r"\| DOI \[([^\]]+)\]", body))
        self.assertEqual(page_dois, set(re.findall(r"(?m)^  doi = \{([^}]+)\}", bib)))
        self.assertEqual(page_dois, set(re.findall(r"(?m)^DO  - (\S+)$", ris)))
        for doi in ("10.5281/zenodo.22907695", "10.5281/zenodo.21789120"):
            self.assertIn(doi, page_dois)
        self.assertIn("abstract_id=7234418", body)
        self.assertEqual(bib.count("{") , bib.count("}"))


class ContentTests(unittest.TestCase):
    def test_media_kit_lists_the_team_exactly(self):
        _, body = body_of("media-kit.md")
        team = body.split("\n## Team\n", 1)[1].split("\n## ", 1)[0]
        rows = re.findall(r"(?m)^\| ([A-Z][a-z]+ [A-Z][a-z]+) \| ([^|]+) \|$", team)
        self.assertEqual([(name, role.strip()) for name, role in rows], TEAM)
        self.assertIn("Broadcastwell is a team of consultants and engineers. Sairam Sivakumar, Founder, is "
                      "accountable for every order.", body)

    def test_case_format_is_labeled_fictional_in_every_figure(self):
        _, body = body_of("cases/format.md")
        first = [line for line in body.split("\n# ", 1)[1].splitlines()[1:] if line.strip()][0]
        self.assertTrue(first.startswith("**Fictional sample.**"))
        self.assertIn("<figcaption>Fictional sample.", body)
        self.assertIn("<caption>Fictional sample:", body)
        self.assertIn('<svg role="img" aria-label="Fictional sample:', body)
        # A <title> element in the body would be read as the page title by the release checks.
        self.assertNotIn("<title", body)
        headers = [line for line in body.splitlines() if line.startswith("| ") and "---" not in line
                   and line.split(" | ")[0] in ("| Field (fictional sample)", "| Capture (fictional sample)",
                                                "| Measure (fictional sample)", "| Fictional sample, ChatGPT",
                                                "| Field")]
        self.assertGreaterEqual(len(headers), 7)
        for header in headers:
            self.assertIn("ictional sample", header)

    def test_case_format_intervals_match_the_published_counts(self):
        _, body = body_of("cases/format.md")
        for k, n, low, high in re.findall(r"\| (\d+) of (\d+) \| [\d.]+% \| ([\d.]+)% to ([\d.]+)% \|", body):
            with self.subTest(count="%s of %s" % (k, n)):
                self.assertEqual(wilson(int(k), int(n)), (float(low), float(high)))
        self.assertIn("| 15 of 29 | 51.7% | 34.4% to 68.6% |", body)
        self.assertIn("| 0 of 10 | 0.0% | 0.0% to 27.8% |", body)

    def test_local_pages_rule_is_dated_with_three_evidence_types_and_six_reasons(self):
        _, body = body_of("standards/local-pages.md")
        self.assertIn("This is our editorial rule, dated 9 November 2026", body)
        for kind in ("A local address", "A local customer we may name", "A local source we can cite"):
            self.assertIn("| " + kind + " |", body)
        self.assertEqual(re.findall(r"(?m)^\| (L\d) \|", body), ["L1", "L2", "L3", "L4", "L5", "L6"])

    def test_model_release_rows_cite_a_provider_page_and_make_no_forecast(self):
        _, body = body_of("model-releases.md")
        for host in ("help.openai.com", "support.claude.com", "perplexity.ai/changelog", "gemini.google",
                     "blog.google"):
            self.assertIn(host, body)
        self.assertNotRegex(body.lower(), r"\b(will release|expected to launch|forecast:)")

    def test_webinar_and_workshop_pages_offer_a_session_by_email_and_no_live_event(self):
        for name in ("webinars.md", "workshops.md"):
            _, body = body_of(name)
            self.assertIn("[hello@broadcastwell.com](mailto:hello@broadcastwell.com)", body)
            self.assertIn("We list no scheduled live events.", body)


class NearDuplicateTests(unittest.TestCase):
    def test_no_new_page_shares_more_than_a_fifth_of_its_six_word_sequences(self):
        worst = near_duplicate_rows()[0]
        self.assertLessEqual(worst[0], hub.NEAR_DUPLICATE_LIMIT, worst)


if __name__ == "__main__":
    unittest.main()
