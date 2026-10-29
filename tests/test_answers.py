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
    CLUSTER_OWNERS, LIMIT_SENTENCE, GSC_EXPECTED_SUMMARY, GSC_SUMMARY_PATH, GSC_SUMMARY_URL,
    SCOPED_METHOD_LABEL, DEFAULT_METHOD_LABEL, GSC_SCOPE_SENTENCE, built_relative, normalized_question,
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
        self.assertFalse(ownership_violations("Neurvalis and Valren Atelier are separate named companies."))

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
        self.assertEqual(namespace["ruling_hits"]("Neurvalis and Valren Atelier are separate named companies."), [])

    def test_client_studies_counts_and_links_do_not_imply_founder_ownership(self):
        permitted_client_evidence = (
            "Broadcastwell worked with Valren Atelier to establish a baseline.",
            "Broadcastwell's AI visibility baseline assessment gave Neurvalis a starting point.",
            "Valren Atelier is active client work.",
            "Neurvalis AI Automation was our client.",
            "Broadcastwell clients: VantaaTax, Neurvalis, Valren Atelier.",
            "Three client case studies cover VantaaTax, Neurvalis and Valren Atelier.",
            "[Neurvalis client study](https://broadcastwell.com/neurvalis-ai-visibility-diagnostic)",
            "[Valren Atelier client study](https://broadcastwell.com/valren-ai-visibility-audit)",
        )
        for value in permitted_client_evidence:
            with self.subTest(client_evidence=value):
                self.assertEqual(ownership_violations(value), [])
                self.assertEqual(ownership_violations(json.dumps({"text": value})), [])
        self.assertTrue(ownership_violations("Broadcastwell's founder previously owned and sold Neurvalis AI Automation and Valren Atelier."))

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



class SourceMethodRuleTests(unittest.TestCase):
    def setUp(self):
        self.fixture = LibraryRuleTests("test_complete_fixture_passes")
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def make_gsc(self):
        fixture = self.fixture
        fixture.meta.update(evidence_kind="search-console-export", is_based_on=GSC_SUMMARY_URL)
        fixture.body = fixture.body.replace(
            "This test fixture describes a 30-answer repeat check dated 28 October 2026. You can read its validation rules below.",
            "The 27 October 2026 export has134 queries in our length filter and969 impressions. You can inspect the aggregate without reading private query text.")
        fixture.body = fixture.body.replace(DEFAULT_METHOD_LABEL, SCOPED_METHOD_LABEL)
        fixture.body = fixture.body.replace("Measured: this fixture is for validation tests and is never published. It has a dated source and a declared base.",
            "Measured:134 distinct queries generated969 impressions and0 query-table clicks from1,000 query rows. "
            "The92-day window runs from26 July to25 October2026; the export date is27 October2026. "
            "The filter retains queries with at least12 whitespace-separated words. " + GSC_SCOPE_SENTENCE + "\n\n"
            "[Aggregate source](" + GSC_SUMMARY_URL + "). "
            "[Google impression/click definitions](https://support.google.com/webmasters/answer/7042828). "
            "[Google AI feature reporting](https://developers.google.com/search/docs/appearance/ai-features).")
        # Ordinary fixture language below is normalized; the metadata/JSON stays exact.
        for old, new in (("has134", "has 134"),("and969", "and 969"),("generated969", "generated 969"),("and0", "and 0"),
                         ("from1,000", "from 1,000"),("The92", "The 92"),("from26", "from 26"),("to25", "to 25"),
                         ("October2026", "October 2026"),("is27", "is 27"),("least12", "least 12")):
            fixture.body=fixture.body.replace(old,new)
        # A GSC-only page must pass without an unrelated research link masking
        # the approved aggregate URL at the final published-evidence guard.
        fixture.body = fixture.body.replace(
            "[Source DOI](https://doi.org/10.5281/zenodo.22907695).",
            "[Aggregate record](" + GSC_SUMMARY_URL + ").")
        fixture.body = fixture.body.replace(
            "[Published Index](https://index.broadcastwell.com/).",
            "[Google metric definitions](https://support.google.com/webmasters/answer/7042828).")
        asset=fixture.docs/GSC_SUMMARY_PATH;asset.parent.mkdir(parents=True,exist_ok=True)
        asset.write_text(json.dumps(GSC_EXPECTED_SUMMARY),encoding="utf8")
        fixture.write()
        return asset

    def make_study(self):
        fixture=self.fixture
        doi="https://doi.org/10.5281/zenodo.23197560"
        fixture.meta.update(evidence_kind="published-study",is_based_on=doi,evidence_method_receipts=[doi])
        fixture.body=fixture.body.replace(DEFAULT_METHOD_LABEL,SCOPED_METHOD_LABEL)
        fixture.body=fixture.body.replace("Measured: this fixture is for validation tests and is never published. It has a dated source and a declared base.",
            "Measured: this fixture describes the separate public-browsing study protocol. "
            "The [published study method]("+doi+") specifies the tasks and scored outcomes.")
        fixture.write()

    def errors(self):
        return "\n".join(validate_answer(self.fixture.path,self.fixture.docs))

    def test_approved_aggregate_passes_without_relaxing_default_doi_rules(self):
        self.make_gsc()
        self.assertNotRegex(self.fixture.body, r"https://(?:index\.broadcastwell\.com/|broadcastwell\.com/research/|doi\.org/)")
        self.assertEqual(self.errors(),"")
        self.fixture.meta.pop("evidence_kind")
        self.fixture.write()
        self.assertIn("non-September sources",self.errors())

    def test_gsc_tampered_counts_hash_and_raw_fields_fail(self):
        asset=self.make_gsc()
        for key,value in (("matching_distinct_queries",135),("matching_query_table_clicks",False),("source_queries_csv_sha256","0"*64),
                          ("raw_queries",["private fixture text"]),("local_path","C:/private/source.csv")):
            with self.subTest(key=key):
                payload=dict(GSC_EXPECTED_SUMMARY);payload[key]=value
                asset.write_text(json.dumps(payload),encoding="utf8")
                self.assertIn("differs from approved",self.errors())

    def test_gsc_rejects_arbitrary_url_unknown_kind_and_duplicate_json_keys(self):
        asset=self.make_gsc()
        self.fixture.meta["is_based_on"]="https://example.org/summary.json";self.fixture.write()
        self.assertIn("exact approved aggregate",self.errors())
        self.fixture.meta["is_based_on"]=GSC_SUMMARY_URL;self.fixture.meta["evidence_kind"]="arbitrary-source";self.fixture.write()
        self.assertIn("unknown evidence_kind",self.errors())
        self.fixture.meta["evidence_kind"]="search-console-export";self.fixture.write()
        asset.write_text('{"schema_version":"private duplicate",'+json.dumps(GSC_EXPECTED_SUMMARY)[1:],encoding="utf8")
        self.assertIn("duplicate JSON key",self.errors())

    def test_gsc_requires_actual_filter_scope_dates_and_primary_definitions(self):
        self.make_gsc();original=self.fixture.body
        for removed in ("at least 12 whitespace-separated words","https://support.google.com/webmasters/answer/7042828",
                        GSC_SCOPE_SENTENCE,"92-day","1,000 query rows"):
            with self.subTest(removed=removed):
                self.fixture.body=original.replace(removed,"");self.fixture.write()
                self.assertIn("Search Console",self.errors())

    def test_approved_study_needs_its_method_receipt_and_truthful_label(self):
        self.make_study();self.assertEqual(self.errors(),"")
        self.fixture.body=self.fixture.body.replace(SCOPED_METHOD_LABEL,DEFAULT_METHOD_LABEL);self.fixture.write()
        self.assertIn("universal v1.1",self.errors())
        self.fixture.body=self.fixture.body.replace(DEFAULT_METHOD_LABEL,SCOPED_METHOD_LABEL)
        self.fixture.meta.pop("evidence_method_receipts");self.fixture.write()
        self.assertIn("requires a list",self.errors())

    def test_study_rejects_unknown_doi_and_unlinked_or_arbitrary_receipts(self):
        self.make_study()
        self.fixture.meta["is_based_on"]="https://doi.org/10.5281/zenodo.99999999";self.fixture.write()
        self.assertIn("outside the approved DOI",self.errors())
        self.fixture.meta["is_based_on"]="https://doi.org/10.5281/zenodo.23197560"
        self.fixture.meta["evidence_method_receipts"].append("https://example.org/method");self.fixture.write()
        self.assertIn("unapproved study method receipt",self.errors())
        self.fixture.meta["evidence_method_receipts"].pop()
        self.fixture.body=self.fixture.body.replace("https://doi.org/10.5281/zenodo.23197560","https://example.org/unrelated");self.fixture.write()
        self.assertIn("must be linked in What we measured",self.errors())

    def test_gsc_rejects_false_universal_method_and_missing_first_figure(self):
        self.make_gsc()
        self.fixture.body=self.fixture.body.replace(SCOPED_METHOD_LABEL,DEFAULT_METHOD_LABEL);self.fixture.write()
        self.assertIn("universal v1.1",self.errors())
        self.fixture.body=self.fixture.body.replace(DEFAULT_METHOD_LABEL,SCOPED_METHOD_LABEL)
        self.fixture.body=self.fixture.body.replace("has 134 queries in our length filter and 969 impressions","has a measured result")
        self.fixture.write();self.assertIn("first Search Console paragraph",self.errors())


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
