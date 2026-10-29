"""Publication-audit receipts are narrow evidence, never outcome measurements."""

from pathlib import Path
import tempfile
import unittest

import yaml

from tools.library_answers import (
    APPROVED_PUBLICATION_AUDITS, AUDIT_METHOD_LABEL,
    DEFAULT_METHOD_LABEL, SCOPED_METHOD_LABEL, LIMIT_SENTENCE, validate_answer,
    validate_source_evidence, external_evidence_links,
)


MAIN = "https://broadcastwell.com/best-geo-agencies"
STARTUP = "https://broadcastwell.com/best-geo-agencies-for-startups"
SCOPE_ONE = "We counted published material; this was not a new provider test or proof of service quality, AI outcomes or client results."
COUNT_ONE = "Only Yes cells count; Partial, No and Not verified contribute nothing."
ORDER_ONE = "We list the agencies in alphabetical order, without a ranking; Broadcastwell is not scored."
# Independent literals from the four reviewed public record panels. Fixture
# authors do not derive expected statuses/counts from the implementation.
SOURCE_FACTS = {
    MAIN: {
        "hash": "4c2722c06bb8308bc8900e85d18599cfdd2a1ee870261152455a1ccbfe47af54",
        "time": "2026-10-29T14:37:02.799269+00:00",
        "records": [
            ("go-fish-digital", "Go Fish Digital", ["Partial", "No", "Yes", "No", "No", "Yes", "Yes", "No"], 3),
            ("minuttia", "Minuttia", ["Partial", "No", "Yes", "Partial", "No", "Yes", "Yes", "Partial"], 3),
        ],
        "dates": "Original field reads: 15 September 2026. Reviews: 16 September 2026. Prices, refund terms and engine lists were read again on 28 October 2026; other cells retain their earlier dates.",
    },
    STARTUP: {
        "hash": "0e9c684aa54488edcbd6518e6205ea51ff3de58a6addb6b22dde027e15e47fa6",
        "time": "2026-10-29T14:37:02.864788+00:00",
        "records": [
            ("citant", "Citant", ["Yes", "Yes", "Yes", "Partial", "Yes", "No", "Not verified", "No"], 4),
            ("embarque", "Embarque", ["Partial", "No", "Yes", "Partial", "Yes", "Yes", "Yes", "Partial"], 4),
        ],
        "dates": "Original field reads: 15 September 2026. Reviews: 16 September 2026. Citant's Method and Open data cells were rechecked on 23 October 2026. Citant's Reviews cell was Not verified on 29 September 2026. Other cells retain their original dates.",
    },
}


class PublicationAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.docs = Path(self.temp.name) / "docs"
        self.path = self.docs / "answers" / "buying" / "publication-fixture.md"
        self.path.parent.mkdir(parents=True)
        (self.docs / "index.md").write_text("# Fixture root\n", encoding="utf8")
        self.fixture(MAIN)

    def fixture(self, source):
        facts = SOURCE_FACTS[source]
        self.meta = {
            "title": "What can this publication fixture establish?",
            "headline": "What can this publication fixture establish?",
            "description": "A fictional validation question about a dated publication-score receipt.",
            "page_class": "page", "schema_type": "Article",
            "date_published": "2026-10-29T00:00:00+00:00",
            "date_modified": "2026-10-29T00:00:00+00:00",
            "hide": ["navigation"], "library_cluster": "buying",
            "library_owner": "Priya Nair, Management Consultant",
            "demand_source": "manual-faq", "demand_evidence": "Fictional fixture, 29 October 2026; never published",
            "is_based_on": source, "evidence_kind": "published-audit",
            "evidence_audit_records": [row[0] for row in facts["records"]],
            "evidence_audit_observed_at": facts["time"],
            "evidence_audit_snapshot_sha256": facts["hash"],
        }
        record_id, name, _, count = facts["records"][0]
        table = "| Agency | Method | Open data | Engines | Price | Refund | B2B cases | Reviews | Machine readable | Yes count |\n"
        table += "|---|---|---|---|---|---|---|---|---|---|\n"
        for rid, agency, statuses, score in facts["records"]:
            table += "| " + " | ".join(["[" + agency + "](" + source + "#" + rid + ")", *statuses, str(score) + "/8"]) + " |\n"
        self.body = f"""# What can this publication fixture establish?

[{name}]({source}#{record_id}) has {count} of 8 Yes cells in the saved 29 October 2026 publication-audit snapshot. This fictional fixture tests receipt handling and is never published.

## What we measured

Measured: source snapshot read on 29 October 2026.

{SCOPE_ONE}

{COUNT_ONE} {ORDER_ONE}

{facts['dates']}

[Published criteria]({source}#scorecard).

{table}

## What this means for you

This score does not prove client results. A publication check cannot show service quality. A Partial price cell does not mean that no price was published. A Yes refund cell records published terms, without verifying refund performance.

## Also asked as

This is a validation fixture, without a second publishable question.

## Related

[Criteria]({source}#scorecard).
[Record]({source}#{record_id}).
[Manual](https://docs.broadcastwell.com/).

## Next step

[Free 10-question check (one engine)](https://audit.broadcastwell.com/).
{LIMIT_SENTENCE}
[Fix one answer, $490](https://broadcastwell.com/answer-repair).
[{AUDIT_METHOD_LABEL}]({source}#scorecard)

Prepared by the Broadcastwell team.

Page owner: Priya Nair, Management Consultant. Corrections: hello@broadcastwell.com
"""
        self.body = self.body.replace("## What this means for you", " ".join(["fixture"] * 130) + "\n\n## What this means for you")

    def errors(self):
        self.path.write_text("---\n" + yaml.safe_dump(self.meta, sort_keys=False) + "---\n\n" + self.body, encoding="utf8")
        return "\n".join(validate_answer(self.path, self.docs))

    def test_all_four_pinned_records_and_recount_are_exact(self):
        self.assertEqual(set(APPROVED_PUBLICATION_AUDITS), set(SOURCE_FACTS))
        for source, facts in SOURCE_FACTS.items():
            self.fixture(source)
            self.assertEqual(self.errors(), "")
            actual = APPROVED_PUBLICATION_AUDITS[source]
            self.assertEqual(actual["snapshot_sha256"], facts["hash"])
            self.assertEqual(actual["observed_at"], facts["time"])
            expected_ids = {row[0] for row in facts["records"]}
            if source == MAIN:
                expected_ids.update({"first-page-sage", "omniscient", "optimist", "relevance", "single-grain", "skale", "webfx"})
            self.assertEqual(set(actual["records"]), expected_ids)
            for rid, name, statuses, count in facts["records"]:
                self.assertEqual(actual["records"][rid]["name"], name)
                self.assertEqual(list(actual["records"][rid]["statuses"]), statuses)
                self.assertEqual(statuses.count("Yes"), count)

    def test_two_distinct_truthful_scope_and_date_wordings_pass(self):
        for source in SOURCE_FACTS:
            self.fixture(source)
            self.assertEqual(self.errors(), "")
            self.body = self.body.replace(
                "Measured: source snapshot read on 29 October 2026.",
                "Measured: 29 October 2026 is the source-snapshot read date.",
            ).replace(
                SCOPE_ONE,
                "The scores concern publicly checkable documents, without retesting providers or claiming evidence of their results.",
            ).replace(
                COUNT_ONE,
                "The Yes cells alone form the total; every other response adds zero.",
            ).replace(
                ORDER_ONE,
                "The list runs from A to Z, not a ranking; the publisher is outside the scorecard.",
            )
            dates = "On 15 September 2026 the company sites were checked. 16 September 2026 is the review read date. "
            if source == MAIN:
                dates += "On 28 October 2026 engine lists, refund terms and prices were checked again."
            else:
                dates += "On 23 October 2026 Citant's Method and Open data were rechecked. 29 September 2026 is when Citant's Reviews cell was Not verified."
            self.body = self.body.replace(SOURCE_FACTS[source]["dates"], dates)
            self.assertEqual(self.errors(), "")

    def test_arbitrary_url_and_other_source_kind_are_rejected(self):
        for url in ("https://example.com/scorecard", MAIN + "/", MAIN + "?version=1", MAIN + "#scorecard", "http://broadcastwell.com/best-geo-agencies", [], {}):
            with self.subTest(url=url):
                self.meta["is_based_on"] = url
                self.assertIn("outside the two approved audit URLs", self.errors())

    def test_snapshot_hash_and_actual_read_time_are_bound(self):
        for key, bad in (("evidence_audit_snapshot_sha256", "0" * 64), ("evidence_audit_observed_at", "2026-10-28T00:00:00+00:00")):
            original = self.meta[key]
            self.meta[key] = bad
            self.assertIn(key, self.errors())
            self.meta[key] = original

    def test_exact_approved_audit_links_join_the_external_http_check(self):
        links = external_evidence_links(
            "[Method](" + MAIN + "#scorecard) [Record](" + STARTUP + "#citant) "
            "[Other](https://example.com/audit) [Suffix](" + MAIN + "-other)"
        )
        self.assertEqual(links, {MAIN, STARTUP})

    def test_missing_duplicate_cross_source_and_nonstring_records_fail(self):
        for value in (None, [], "go-fish-digital", ["go-fish-digital", "go-fish-digital"], ["citant"], [1], [{}]):
            with self.subTest(records=value):
                self.meta["evidence_audit_records"] = value
                self.assertIn("published-audit", self.errors())

    def test_method_must_use_exact_audit_scorecard_in_body_and_footer(self):
        original = self.body
        self.body = original.replace("[Published criteria](" + MAIN + "#scorecard)", "Published criteria")
        self.body = self.body.replace("[Criteria](" + MAIN + "#scorecard)", "Criteria")
        # The footer alone is not a What we measured method receipt.
        self.assertIn("criteria must be linked in What we measured", self.errors())
        self.body = original.replace("[" + AUDIT_METHOD_LABEL + "](" + MAIN + "#scorecard)", "[" + AUDIT_METHOD_LABEL + "](https://broadcastwell.com/methodology)")
        self.assertIn("method label must link to the publication-audit scorecard", self.errors())
        for label in (DEFAULT_METHOD_LABEL, SCOPED_METHOD_LABEL):
            self.body = original.replace(AUDIT_METHOD_LABEL, label)
            self.assertIn("must not use an answer-study", self.errors())

    def test_unrelated_index_doi_cannot_substitute_for_audit(self):
        self.meta["is_based_on"] = "https://doi.org/10.5281/zenodo.22907695"
        self.assertIn("outside the two approved audit URLs", self.errors())
        self.fixture(MAIN)
        self.meta["evidence_method_receipts"] = ["https://doi.org/10.5281/zenodo.22907695"]
        self.assertIn("not answer-study method receipts", self.errors())

    def test_record_links_and_first_paragraph_receipt_cannot_be_omitted(self):
        self.body = self.body.replace(MAIN + "#go-fish-digital", MAIN + "#wrong-record")
        errors = self.errors()
        self.assertIn("exact source anchor", errors)
        self.assertIn("first publication-audit paragraph", errors)

    def test_missing_status_changed_status_and_wrong_count_fail(self):
        for old, new in (("| Partial | No | Yes | No | No | Yes | Yes | No | 3/8", "| Yes | No | Yes | No | No | Yes | Yes | No | 3/8"),
                         ("| 3/8", "| 4/8"), ("has 3 of 8", "has 5 of 8"), ("has 3 of 8", "has 3 of 7")):
            original = self.body
            self.assertIn(old, original)
            self.body = original.replace(old, new, 1)
            self.assertTrue(self.errors())
            self.body = original

    def test_not_verified_cannot_be_converted_to_no(self):
        self.fixture(STARTUP)
        self.body = self.body.replace("| Not verified |", "| No |")
        self.assertIn("eight statuses and Yes counts", self.errors())

    def test_all_eight_criteria_and_alphabetical_order_are_required(self):
        original = self.body
        self.body = original.replace("| Refund |", "| Guarantee success |")
        self.assertIn("table must match", self.errors())
        lines = original.splitlines()
        indices = [index for index, line in enumerate(lines) if line.startswith("| [")]
        lines[indices[0]], lines[indices[1]] = lines[indices[1]], lines[indices[0]]
        self.body = "\n".join(lines)
        self.assertIn("alphabetical records", self.errors())

    def test_scope_count_rule_publisher_and_mixed_dates_cannot_disappear(self):
        original = self.body
        for phrase in (SCOPE_ONE, COUNT_ONE, ORDER_ONE,
                       "15 September 2026", "16 September 2026", "28 October 2026"):
            self.body = original.replace(phrase, "")
            self.assertIn("published-audit", self.errors())
        self.fixture(STARTUP)
        for date in ("23 October 2026", "29 September 2026"):
            original = self.body
            self.body = original.replace(date, "29 October 2026")
            self.assertIn("published-audit", self.errors())
            self.body = original

    def test_scope_assertions_cannot_be_missing_or_contradicted(self):
        original = self.body
        for old, new in (
            (SCOPE_ONE, "This fixture gives a score, without declaring its scope."),
            (SCOPE_ONE, "We counted published material, but this is a fresh provider test that proves client results."),
            (SCOPE_ONE, "This is not publication evidence; it is a new performance test."),
            (ORDER_ONE, "These agencies are listed, with Broadcastwell included in the scoring."),
            (COUNT_ONE, "Both Yes and Partial contribute to the total."),
        ):
            self.body = original.replace(old, new)
            self.assertIn("published-audit", self.errors(), new)
        for claim in ("The agencies were retested on 29 October 2026.", "Partial cells also count toward this score.", "The scorecard measures client results.", "These scores prove client results.", "The publisher is scored.", "This is not publication evidence.", "The scorecard ranks agencies by quality."):
            self.body = original.replace("[Published criteria]", claim + "\n\n[Published criteria]")
            self.assertRegex(self.errors(), r"(?:publication|published)-audit", claim)

    def test_dates_cannot_be_reassigned_even_if_correct_dates_remain(self):
        original = self.body
        for claim in ("Reviews were read on 28 October 2026.", "The source snapshot was read on 28 October 2026.", "Prices were rechecked on 29 October 2026."):
            self.body = original.replace("[Published criteria]", claim + "\n\n[Published criteria]")
            self.assertIn("contradicts the approved field/read dates", self.errors(), claim)
        self.fixture(STARTUP)
        for claim in ("Citant's Method was rechecked on 28 October 2026.", "Citant's Reviews cell was Not verified on 23 October 2026."):
            original = self.body
            self.body = original.replace("[Published criteria]", claim + "\n\n[Published criteria]")
            self.assertIn("contradicts the approved field/read dates", self.errors(), claim)
            self.body = original

    def test_prices_fail_even_if_a_historical_page_published_them(self):
        original = self.body
        for claim in ("Minuttia costs $5,000 per month.", "Citant charges USD 440.", "Embarque costs 1500 dollars.", "Go Fish Digital is free.", "Minuttia currently starts at a quoted monthly rate."):
            self.body = original.replace("## Also asked as", claim + "\n\n## Also asked as")
            self.assertIn("pricing claim" if "$" not in claim and "USD" not in claim and "dollars" not in claim else "price claims", self.errors())
        self.body = original.replace("[Fix one answer, $490](https://broadcastwell.com/answer-repair)", "[Fix one answer, $491](https://broadcastwell.com/answer-repair)")
        self.assertIn("price claims", self.errors())

    def test_only_exact_next_step_cta_has_a_monetary_exception(self):
        self.assertEqual(self.errors(), "")
        self.body = self.body.replace("## Also asked as", "An unsupported $490 provider fee.\n\n## Also asked as")
        self.assertIn("price claims", self.errors())

    def test_current_results_quality_and_ranking_inferences_fail(self):
        original = self.body
        for claim in ("This score proves client results.", "The audit shows current AI recommendations.", "Minuttia delivers better client results.", "Citant is the best value for money.", "This count guarantees improved rankings.", "The score makes Citant the winner.", "This audit reflects current client results.", "The score proves that Embarque is cheapest.", "This audit measures service quality."):
            self.body = original.replace("## Also asked as", claim + "\n\n## Also asked as")
            self.assertIn("cannot claim service quality", self.errors(), claim)

    def test_honest_negated_limits_are_allowed(self):
        for source in SOURCE_FACTS:
            self.fixture(source)
            self.body = self.body.replace("## Also asked as", "The score does not prove client results. The audit cannot show service quality. This count never guarantees current AI recommendations. No publication score can prove client results. The audit shows no evidence of better client results.\n\n## Also asked as")
            self.assertEqual(self.errors(), "")

    def test_existing_banned_prose_and_false_ownership_guards_remain(self):
        original = self.body
        for claim, expected in (("A seamless result.", "banned prose"), ("Broadcastwell's founder previously owned and sold Neurvalis and Valren Atelier.", "false ownership claim")):
            self.body = original + "\n" + claim
            self.assertIn(expected, self.errors())

    def test_old_method_branch_return_labels_and_urls_are_unchanged(self):
        for kind, source, label in (("", "https://doi.org/10.5281/zenodo.22907695", DEFAULT_METHOD_LABEL),
                                    ("published-study", "https://doi.org/10.5281/zenodo.23202939", SCOPED_METHOD_LABEL)):
            meta = {"is_based_on": source, "evidence_kind": kind, "evidence_method_receipts": [source]}
            body = "## What we measured\n[Study method](" + source + ").\n## What this means for you\n[" + label + "](https://broadcastwell.com/methodology)"
            errors, actual_label = validate_source_evidence(meta, body, self.docs)
            self.assertEqual(actual_label, label)
            self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
