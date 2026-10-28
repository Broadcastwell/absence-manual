"""Library rules reject duplicate questions, missing receipts and bad links."""

import ast
import json
from pathlib import Path
import re
from types import SimpleNamespace
import tempfile
import unittest

from jinja2 import DictLoader, Environment
import yaml

from tools.generate_answers_llms import answers_section, regenerate
from tools.library_answers import (
    CLUSTER_OWNERS, LIMIT_SENTENCE, built_relative, normalized_question,
    ownership_violations, page_url, resolve_local_link, validate_answer,
    validate_collection,
)
from tools.verify_answers import check_external_links

ROOT = Path(__file__).resolve().parents[1]


class LibraryRuleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.docs = Path(self.temp.name) / "docs"
        self.path = self.docs / "answers" / "measurement" / "what-does-one-repeat-check-show.md"
        self.path.parent.mkdir(parents=True)
        self.meta = {
            "title": "What does one repeat check show?",
            "headline": "What does one repeat check show?",
            "description": "A 30-answer repeat check describes its dated question set.",
            "page_class": "page", "schema_type": "Article",
            "date_published": "2026-10-28T00:00:00+00:00",
            "date_modified": "2026-10-28T00:00:00+00:00",
            "hide": ["navigation"], "library_cluster": "measurement",
            "library_owner": CLUSTER_OWNERS["measurement"],
            "demand_source": "manual-faq", "demand_evidence": "Fixture demand record, 28 October 2026",
            "is_based_on": "https://doi.org/10.5281/zenodo.22907695",
            "also_asked_as": ["What can a repeated check tell us?"],
        }
        self.body = """# What does one repeat check show?

This test fixture describes a 30-answer repeat check dated 28 October 2026. You can read its validation rules below.

## What we measured

Measured: this fixture is for validation tests and is never published. It has a dated source and a declared base.

## What this means for you

The fixture verifies the rules that a real evidence page must satisfy.

## Also asked as

What can a repeated check tell us?

## Related

[Source DOI](https://doi.org/10.5281/zenodo.22907695).
[Published Index](https://index.broadcastwell.com/).
[Method](https://broadcastwell.com/methodology).

## Next step

[Free 10-question check (one engine)](https://audit.broadcastwell.com/).
LIMIT
[Fix one answer, $490](https://broadcastwell.com/answer-repair).
[Every figure comes from the published method, v1.1.](https://broadcastwell.com/methodology)

Prepared by the Broadcastwell team.

Page owner: Vikram Patel, AI Architect. Corrections: hello@broadcastwell.com
""".replace("LIMIT", LIMIT_SENTENCE)
        # Length here is a mechanical boundary fixture, not publishable copy.
        self.body = self.body.replace("## What this means for you", " ".join(["fixture"] * 240) + "\n\n## What this means for you")
        self.write()

    def write(self):
        self.path.write_text("---\n" + yaml.safe_dump(self.meta, sort_keys=False) + "---\n\n" + self.body, encoding="utf8")

    def test_complete_fixture_passes(self):
        self.assertEqual(validate_answer(self.path, self.docs), [])

    def test_markdown_table_rules_are_syntax_and_prose_dashes_still_fail(self):
        self.body = self.body.replace("## What this means for you", "| Count | Base |\n|---|---:|\n| 3 | 10 |\n\n## What this means for you")
        self.write()
        self.assertEqual(validate_answer(self.path, self.docs), [])
        self.body += "\nA prose -- interruption.\n"
        self.write()
        self.assertTrue(any("banned prose" in item for item in validate_answer(self.path, self.docs)))

    def test_directory_index_url_and_output_match_mkdocs(self):
        for source, output, url in (
            ("index.md", "index.html", "https://docs.broadcastwell.com/"),
            ("answers/index.md", "answers/index.html", "https://docs.broadcastwell.com/answers/"),
            ("answers/measurement/index.md", "answers/measurement/index.html", "https://docs.broadcastwell.com/answers/measurement/"),
            ("answers/measurement/question.md", "answers/measurement/question/index.html", "https://docs.broadcastwell.com/answers/measurement/question/"),
        ):
            self.assertEqual(built_relative(source), output)
            self.assertEqual(page_url(source), url)

    def test_required_metadata_owner_and_digit_are_enforced(self):
        for key in ("demand_source", "demand_evidence", "library_owner", "is_based_on"):
            with self.subTest(key=key):
                old = self.meta.pop(key)
                self.write()
                self.assertTrue(validate_answer(self.path, self.docs))
                self.meta[key] = old
        self.meta["library_owner"] = "Someone Else, Reviewer"
        self.write()
        self.assertTrue(any("roster" in item for item in validate_answer(self.path, self.docs)))
        self.meta["library_owner"] = CLUSTER_OWNERS["measurement"]
        self.body = self.body.replace("30-answer repeat check dated 28 October 2026", "repeat check")
        self.write()
        self.assertTrue(any("first answer paragraph" in item for item in validate_answer(self.path, self.docs)))

    def test_order_banned_prose_and_purchase_routes_are_rejected(self):
        self.body = self.body.replace("## Related", "## Elsewhere").replace("fixture is", "landscape is")
        self.body += "\n[Buy](https://broadcastwell.com/buy/record-check)\n"
        self.write()
        errors = "\n".join(validate_answer(self.path, self.docs))
        for phrase in ("sections", "banned prose", "purchase links"):
            self.assertIn(phrase, errors)

    def test_titles_and_folded_synonyms_cannot_become_second_pages(self):
        duplicate = self.docs / "another.md"
        duplicate.write_text("---\ntitle: What can a repeated check tell us?\n---\n", encoding="utf8")
        self.assertTrue(any("folded synonym" in item for item in validate_collection(self.docs)))
        duplicate.write_text("---\ntitle: What does one repeat check show?\n---\n", encoding="utf8")
        self.assertTrue(any("duplicate title" in item for item in validate_collection(self.docs)))

    def test_false_claim_is_detected_after_html_and_space_normalization(self):
        claim = "Broadcastwell's founder previously owned and sold Neurvalis AI Automation and Valren Atelier."
        self.assertTrue(ownership_violations(claim))
        self.assertTrue(ownership_violations(claim.replace("owned and sold", "<b>owned</b>\n and sold")))
        self.assertFalse(ownership_violations("Neurvalis and Valren Atelier are client records."))

    def test_served_text_scan_rejects_false_claim_in_llms_and_search_json(self):
        source = ast.parse((ROOT / "tools" / "verify_build.py").read_text(encoding="utf8"))
        constants = {"DIAGNOSTIC_HISTORY", "AVAILABILITY_WORDS", "RETIRED_OFFERS", "DIAGNOSTIC_OFFER", "RELAUNCH_REMOVALS"}
        nodes = [node for node in source.body if
                 (isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id in constants for target in node.targets))
                 or (isinstance(node, ast.FunctionDef) and node.name == "ruling_hits")]
        namespace = {"re": re, "ownership_violations": ownership_violations}
        exec(compile(ast.Module(body=nodes, type_ignores=[]), "verify_build.ruling_hits", "exec"), namespace)
        claim = "Broadcastwell's founder previously owned and sold Neurvalis AI Automation and Valren Atelier."
        for text in ("# Broadcastwell\n\n" + claim, json.dumps({"docs": [{"text": claim}]})):
            with self.subTest(text=text):
                self.assertTrue(namespace["ruling_hits"](text))
        self.assertEqual(namespace["ruling_hits"]("Neurvalis and Valren Atelier are client records."), [])

    def test_every_answer_hub_needs_a_named_owner_and_team_byline(self):
        hub = self.docs / "answers" / "index.md"
        meta = {"title": "Library hub", "library_hub": True, "page_class": "page", "schema_type": "Article",
                "library_owner": CLUSTER_OWNERS["measurement"]}
        body = "# Library hub\n\nPrepared by the Broadcastwell team.\n\nPage owner: Vikram Patel, AI Architect. Corrections: hello@broadcastwell.com\n"
        hub.write_text("---\n" + yaml.safe_dump(meta) + "---\n" + body, encoding="utf8")
        self.assertEqual(validate_collection(self.docs), [])
        hub.write_text("---\n" + yaml.safe_dump(meta) + "---\n" + body.replace("Prepared by the Broadcastwell team.", ""), encoding="utf8")
        self.assertTrue(any("hub is missing its team byline" in item for item in validate_collection(self.docs)))
        meta["library_owner"] = "Unapproved Owner"
        hub.write_text("---\n" + yaml.safe_dump(meta) + "---\n" + body, encoding="utf8")
        self.assertTrue(any("hub owner" in item for item in validate_collection(self.docs)))

    def test_internal_links_resolve_source_and_directory_pages(self):
        target = self.docs / "answers" / "index.md"
        target.write_text("hub", encoding="utf8")
        self.assertEqual(resolve_local_link("https://docs.broadcastwell.com/answers/", self.path, self.docs), target)
        self.body += "\n[Missing](/missing-page/)\n"
        self.write()
        self.assertTrue(any("broken internal link" in item for item in validate_answer(self.path, self.docs)))
        self.body = self.body.replace("/missing-page/", "https://docs.broadcastwell.com/answers/#absent")
        self.write()
        self.assertTrue(any("broken internal anchor" in item for item in validate_answer(self.path, self.docs)))

    def test_evidence_urls_are_fetched_once_and_fail_on_non_200(self):
        self.body += "\n[Same Index](https://index.broadcastwell.com/#fragment)\n"
        self.write()
        calls = []
        class Response:
            status = 200
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self, count): return b"x"
        def opener(request, timeout):
            calls.append(request.full_url)
            return Response()
        results, errors = check_external_links(self.docs, opener=opener)
        self.assertEqual(calls, ["https://index.broadcastwell.com/"])
        self.assertEqual(errors, [])
        Response.status = 403
        _, errors = check_external_links(self.docs, opener=opener)
        self.assertEqual(len(errors), 1)
        self.assertIn("403", errors[0])

    def test_llms_generation_is_idempotent_and_preserves_price_bytes(self):
        original = b"# Broadcastwell\r\n\r\n## Current prices and terms (26 October 2026)\r\n\r\nAnswer Repair: $490.\r\n\r\n## Research\r\nKeep this exact.\r\n"
        generated = regenerate(original, answers_section(self.docs))
        self.assertTrue(generated.startswith(original))
        self.assertEqual(regenerate(generated, answers_section(self.docs)), generated)
        self.assertIn(page_url(self.path.relative_to(self.docs)).encode(), generated)
        with self.assertRaises(ValueError):
            regenerate(original + b"## Answers\nold\n## Answers\n", answers_section(self.docs))
        middle = original + b"## Answers\nold\n\n## After\r\nUntouched.\r\n"
        self.assertTrue(regenerate(middle, answers_section(self.docs)).endswith(b"## After\r\nUntouched.\r\n"))

    def test_template_emits_article_organization_author_and_source_doi(self):
        template = (ROOT / "overrides" / "main.html").read_text(encoding="utf8")
        env = Environment(loader=DictLoader({"main.html": template, "base.html": "{% block extrahead %}{% endblock %}"}))
        env.filters["url"] = lambda path: "/" + path
        canonical = page_url(self.path.relative_to(self.docs))
        page = SimpleNamespace(title=self.meta["title"], meta=self.meta, canonical_url=canonical, is_homepage=False)
        config = {"site_name": "The Absence Manual", "site_url": "https://docs.broadcastwell.com/", "site_description": "Test description"}
        rendered = env.get_template("main.html").render(page=page, config=config)
        blocks = [json.loads(value) for value in re.findall(r'<script type="application/ld\+json">(.*?)</script>', rendered)]
        article = next(value for value in blocks if value.get("@type") == "Article")
        self.assertEqual(article["mainEntityOfPage"]["@id"], canonical)
        self.assertEqual(article["isBasedOn"], self.meta["is_based_on"])
        self.assertEqual(article["author"]["@type"], "Organization")

    def test_library_uses_its_own_next_step_and_date_instead_of_duplicate_legacy_cta(self):
        template = (ROOT / "overrides" / "main.html").read_text(encoding="utf8")
        env = Environment(loader=DictLoader({"main.html": template, "base.html": "{% block content %}Article body{% endblock %}"}))
        env.filters["url"] = lambda path: "/" + path
        config = {"site_url": "https://docs.broadcastwell.com/", "extra": {"manual_version_label": "Version 1.0"}}
        page = SimpleNamespace(meta=self.meta)
        rendered = env.get_template("main.html").render(page=page, config=config)
        self.assertNotIn('class="bw-next-step"', rendered)
        self.assertNotIn("Last reviewed 26 October", rendered)
        self.assertIn("Broadcastwell answer library", rendered)
        page.meta = {"library_hub": True}
        rendered = env.get_template("main.html").render(page=page, config=config)
        self.assertNotIn('class="bw-next-step"', rendered)
        page.meta = {}
        rendered = env.get_template("main.html").render(page=page, config=config)
        self.assertIn('class="bw-next-step"', rendered)
        self.assertIn("Agency Audit, $490 per client report", rendered)

    def test_library_footer_uses_the_pages_date_without_changing_the_manual_footer(self):
        source = (ROOT / "overrides" / "partials" / "site-footer.html").read_text(encoding="utf8")
        env = Environment(loader=DictLoader({"footer.html": source}))
        page = SimpleNamespace(meta=dict(self.meta, date_modified="2026-11-04T00:00:00+00:00"))
        rendered = env.get_template("footer.html").render(page=page)
        self.assertIn('<time datetime="2026-11-04">4 November 2026</time>', rendered)
        self.assertNotIn('datetime="2026-10-26"', rendered)
        page.meta = {}
        rendered = env.get_template("footer.html").render(page=page)
        self.assertIn('<time datetime="2026-10-26">26 October 2026</time>', rendered)


class RepositoryLibraryTests(unittest.TestCase):
    def test_all_current_answers_and_owned_markdown_pass(self):
        self.assertEqual(validate_collection(ROOT / "docs"), [])

    def test_book_order_keeps_chapters_and_does_not_read_answer_directory_as_a_file(self):
        source = ast.parse((ROOT / "tools" / "build_pdf.py").read_text(encoding="utf8"))
        function = next(node for node in source.body if isinstance(node, ast.FunctionDef) and node.name == "read_order")
        namespace = {"DOCS": ROOT / "docs", "yaml": yaml}
        exec(compile(ast.Module(body=[function], type_ignores=[]), "build_pdf.read_order", "exec"), namespace)
        order = namespace["read_order"]()
        self.assertTrue(all(path.is_file() for path in order))
        self.assertIn(ROOT / "docs" / "index.md", order)
        self.assertIn(ROOT / "docs" / "for-buyers.md", order)
        self.assertFalse(any(path.is_relative_to(ROOT / "docs" / "answers") for path in order))


if __name__ == "__main__":
    unittest.main()
