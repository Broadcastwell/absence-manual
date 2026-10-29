"""A pinned 32-page publication audit never becomes a provider benchmark."""
import copy
import json
from pathlib import Path
import unittest

import test_answers_published_audit as original
from tools.library_answers import external_evidence_links, validate_source_evidence
from tools.library_list_audit import (
    LIST_AUDIT_SOURCE, LIST_AUDIT_METHOD_URL, LIST_AUDIT_METHOD_LABEL,
    LIST_AUDIT_RECEIPT_PATH, LIST_AUDIT_RECEIPT_URL,
)

EXPECTED_HTML = "8de93b046f9c782eaa18d5c0852886590356a47400d2e19ef2780371a7c1d9f9"
EXPECTED_RECEIPT = "065fe507a5bd3cc2decadb5653bf003474cf26e6573dcc67b3678e5ca5dd8bf7"
SOURCE = "https://broadcastwell.com/best-geo-agencies-lists-audited"
METHOD = SOURCE + "#how-scored"


class PublishedListAuditTests(unittest.TestCase):
    def setUp(self):
        self.f = original.PublicationAuditTests()
        self.f.setUp()
        self.addCleanup(self.f.doCleanups)
        self.receipt_path = self.f.docs / LIST_AUDIT_RECEIPT_PATH
        self.receipt_path.parent.mkdir(parents=True)
        self.original_receipt = (Path(__file__).resolve().parents[1] / "docs" / LIST_AUDIT_RECEIPT_PATH).read_bytes()
        self.receipt_path.write_bytes(self.original_receipt)
        self.f.meta = {k: v for k, v in self.f.meta.items() if not k.startswith("evidence_audit_")}
        self.f.meta.update(evidence_kind="published-list-audit", is_based_on=SOURCE,
            evidence_list_audit_snapshot_sha256=EXPECTED_HTML,
            evidence_list_audit_receipt_sha256=EXPECTED_RECEIPT,
            evidence_list_audit_field_date="2026-09-17")
        self.f.body = f"""# What can this publication fixture establish?

Use a fictional publication record to practise comparing different kinds of reviews. [Our audit read on 17 September 2026]({SOURCE}) records 29 of 32 list rows as Yes for self-inclusion. These are validation fixtures only.

## What we measured

Measured: the method reads each list page once; repeated publishers remain separate. The receipt has 29 Yes entries, 2 No entries and 1 Parent company listed entry. The six criteria concern disclosure, selection criteria, claim sources, dates, prices and corrections. Broadcastwell is outside its scored table. The count does not measure agency quality or client results.

[Source]({SOURCE}). [Six criteria]({METHOD}). [Public receipt]({LIST_AUDIT_RECEIPT_URL}).

## What this means for you

This fixture exercises receipt integrity, truthful scope and dated counting. It is never a publishable library page.

## Also asked as

What can this publication fixture establish?

## Related

[Source]({SOURCE}). [Criteria]({METHOD}). [Manual](https://docs.broadcastwell.com/).

## Next step

[Free 10-question check (one engine)](https://audit.broadcastwell.com/).
{original.LIMIT_SENTENCE}
[Fix one answer, $490](https://broadcastwell.com/answer-repair).
[{LIST_AUDIT_METHOD_LABEL}]({METHOD})

Prepared by the Broadcastwell team.

Page owner: Priya Nair, Management Consultant. Corrections: hello@broadcastwell.com
"""
        # These words only reach the existing length boundary in a mechanical
        # negative fixture. They are not a draft or a similarity exemption.
        self.f.body = self.f.body.replace("## What this means for you", " ".join(["fixture"] * 170) + "\n\n## What this means for you")

    def asset(self):
        return json.loads(self.original_receipt)

    def write_asset(self, value):
        self.receipt_path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf8")

    def test_exact_source_pins_all_32_rows_and_192_criteria_pass(self):
        self.assertEqual(self.f.errors(), "")
        data = self.asset()
        self.assertEqual(data["source_html_sha256"], EXPECTED_HTML)
        self.assertEqual(data["field_read_date"], "2026-09-17")
        self.assertEqual(len(data["records"]), 32)
        self.assertEqual(len({r["list_url"] for r in data["records"]}), 32)
        self.assertEqual(sum(len(r["criteria_statuses"]) for r in data["records"]), 192)
        self.assertEqual(data["summary"], {"rows": 32, "in_own_list_yes": 29, "in_own_list_no": 2, "parent_company_listed": 1})
        self.assertFalse(data["publisher_scored"])

    def test_two_truthful_authored_scope_versions_pass(self):
        self.f.body = self.f.body.replace("the method reads each list page once; repeated publishers remain separate", "each list page is counted once, including separate pages from one publisher")
        self.f.body = self.f.body.replace("Broadcastwell is outside its scored table", "The publisher is not scored")
        self.f.body = self.f.body.replace("The count does not measure agency quality or client results", "These publication checks cannot establish service quality")
        self.assertEqual(self.f.errors(), "")

    def test_source_url_aliases_and_wrong_source_kinds_fail(self):
        for source in (SOURCE + "/", SOURCE + "?v=1", SOURCE + "#how-scored", "http://broadcastwell.com/best-geo-agencies-lists-audited", original.MAIN, "https://doi.org/10.5281/zenodo.22907695"):
            with self.subTest(source=source):
                self.f.meta["is_based_on"] = source
                self.assertIn("exact approved 32-list URL", self.f.errors())
        self.f.meta["is_based_on"] = SOURCE
        self.f.meta["evidence_kind"] = "published-audit"
        self.assertIn("outside the two approved audit URLs", self.f.errors())

    def test_all_metadata_pins_are_required_and_cannot_change(self):
        for key in ("evidence_list_audit_snapshot_sha256", "evidence_list_audit_receipt_sha256", "evidence_list_audit_field_date"):
            old = self.f.meta[key]
            for bad in (None, "other"):
                self.f.meta[key] = bad
                self.assertIn("exact approved " + key, self.f.errors())
            self.f.meta[key] = old

    def test_missing_invalid_duplicate_key_and_extra_asset_fields_fail(self):
        self.receipt_path.unlink()
        self.assertIn("cannot be verified", self.f.errors())
        self.receipt_path.write_text('{"records": [], "records": []}', encoding="utf8")
        self.assertIn("duplicate", self.f.errors())
        self.receipt_path.write_text("not JSON", encoding="utf8")
        self.assertIn("cannot be verified", self.f.errors())
        data = self.asset(); data["unreviewed"] = True
        self.write_asset(data)
        self.assertIn("differs from the exact approved", self.f.errors())

    def test_every_self_inclusion_status_is_hash_bound(self):
        for index in range(32):
            with self.subTest(row=index):
                data = self.asset()
                data["records"][index]["in_own_list"] = "No" if data["records"][index]["in_own_list"] == "Yes" else "Yes"
                self.write_asset(data)
                self.assertIn("differs from the exact approved", self.f.errors())

    def test_every_one_of_192_six_criterion_cells_is_bound(self):
        for index in range(32):
            for cell in range(6):
                with self.subTest(row=index, cell=cell):
                    data = self.asset()
                    states = data["records"][index]["criteria_statuses"]
                    states[cell] = "No" if states[cell] == "Yes" else "Yes"
                    self.write_asset(data)
                    self.assertIn("differs from the exact approved", self.f.errors())

    def test_parent_status_cannot_become_yes_and_publishers_cannot_be_collapsed(self):
        data = self.asset()
        row = next(r for r in data["records"] if r["in_own_list"] == "Parent company listed")
        row["in_own_list"] = "Yes"
        self.write_asset(data)
        self.assertIn("29 Yes, 2 No and 1 Parent", self.f.errors())
        self.receipt_path.write_bytes(self.original_receipt)
        self.f.body = self.f.body.replace("reads each list page once", "treats every publisher as counted once")
        self.assertIn("not unique publishers", self.f.errors())

    def test_source_dates_method_or_publisher_asset_fields_cannot_change(self):
        for key, value in (("field_read_date", "2026-10-29"), ("method_url", SOURCE + "#scorecard"), ("source_html_sha256", "0" * 64), ("publisher_scored", True)):
            data = self.asset(); data[key] = value; self.write_asset(data)
            self.assertIn("differs from the exact approved", self.f.errors())

    def test_row_omission_reordering_or_url_substitution_fails(self):
        for kind in ("omit", "reorder", "url"):
            data = self.asset()
            if kind == "omit": data["records"].pop()
            if kind == "reorder": data["records"].reverse()
            if kind == "url": data["records"][0]["list_url"] = "https://example.com/list"
            self.write_asset(data)
            self.assertIn("differs from the exact approved", self.f.errors())

    def test_canonical_json_allows_only_format_changes(self):
        self.receipt_path.write_text(json.dumps(self.asset(), sort_keys=True, indent=4).replace("\n", "\r\n"), encoding="utf8")
        self.assertEqual(self.f.errors(), "")

    def test_body_requires_all_three_source_links_and_custom_footer(self):
        original_body = self.f.body
        for url in (SOURCE, METHOD, LIST_AUDIT_RECEIPT_URL):
            self.f.body = original_body.replace("](" + url + ")", "](https://example.com/)")
            self.assertIn("must be linked in What we measured", self.f.errors())
        self.f.body = original_body.replace(LIST_AUDIT_METHOD_LABEL, original.DEFAULT_METHOD_LABEL)
        self.assertIn("cannot use a study or eight-cell", self.f.errors())

    def test_first_paragraph_wrong_date_count_base_or_receipt_fails(self):
        original_body = self.f.body
        for old, new in (("29 of 32", "30 of 32"), ("29 of 32", "29 of 33"), ("17 September 2026", "29 October 2026")):
            self.f.body = original_body.replace(old, new, 1)
            self.assertIn("first list-audit paragraph", self.f.errors())

    def test_scope_publisher_count_rule_and_six_criteria_cannot_disappear(self):
        original_body = self.f.body
        for old in ("Broadcastwell is outside its scored table.", "The count does not measure agency quality or client results.", "The six criteria concern disclosure, selection criteria, claim sources, dates, prices and corrections.", "2 No entries", "1 Parent company listed entry"):
            self.f.body = original_body.replace(old, "")
            self.assertIn("list-audit", self.f.errors())

    def test_contradictory_scope_dates_parent_or_outcomes_fail(self):
        original_body = self.f.body
        for claim in ("The publisher is scored.", "These lists were read on 29 October 2026.", "Parent company listed counts as Yes.", "This is a new provider test.", "The audit proves current AI recommendations.", "Onely delivers better client results.", "AEO Vision is free."):
            self.f.body = original_body.replace("## Also asked as", claim + "\n\n## Also asked as")
            self.assertIn("audit", self.f.errors(), claim)

    def test_cross_method_metadata_and_monetary_claims_fail(self):
        self.f.meta["evidence_method_receipts"] = ["https://doi.org/10.5281/zenodo.22907695"]
        self.assertIn("cannot use eight-cell audit or answer-study metadata", self.f.errors())
        self.f.meta.pop("evidence_method_receipts")
        self.f.body = self.f.body.replace("## Also asked as", "An unsupported $490 provider price.\n\n## Also asked as")
        self.assertIn("price claims", self.f.errors())

    def test_unrelated_negation_cannot_hide_an_affirmative_predicate(self):
        original_body = self.f.body
        for claim, expected in (
            ("The publisher is not anonymous and is scored.", "cannot score its publisher"),
            ("The publisher is not anonymous and scored.", "cannot score its publisher"),
            ("The publisher is not anonymous and is included in the scoring.", "cannot score its publisher"),
            ("Parent company listed is not ambiguous and counts as Yes.", "cannot convert Parent company listed"),
            ("Parent company listed is not ambiguous and is Yes.", "cannot convert Parent company listed"),
            ("Parent company listed is not ambiguous and was converted to Yes.", "cannot convert Parent company listed"),
        ):
            with self.subTest(claim=claim):
                self.f.body = original_body.replace("## Also asked as", claim + "\n\n## Also asked as")
                self.assertIn(expected, self.f.errors())

    def test_direct_true_negation_is_allowed_and_supplies_the_disclosure(self):
        original_body = self.f.body
        for publisher_claim in (
            "The publisher is not anonymous and is not scored.",
            "The publisher is never scored.",
            "Broadcastwell is excluded from the scoring.",
        ):
            for parent_claim in (
                "Parent company listed is not ambiguous and does not count as Yes.",
                "Parent company listed never counts as Yes.",
                "Parent company listed was not converted to Yes.",
            ):
                with self.subTest(publisher=publisher_claim, parent=parent_claim):
                    self.f.body = original_body.replace("Broadcastwell is outside its scored table.", publisher_claim)
                    self.f.body = self.f.body.replace("## Also asked as", parent_claim + "\n\n## Also asked as")
                    self.assertEqual(self.f.errors(), "")
        self.f.body = original_body.replace("Broadcastwell is outside its scored table.", "The publisher is not anonymous.")
        self.assertIn("outside scoring", self.f.errors())

    def test_exact_list_source_joins_external_check_without_url_widening(self):
        links = external_evidence_links("[A](" + SOURCE + ") [B](" + METHOD + ") [C](" + SOURCE + "/) [D](" + SOURCE + "?v=1)")
        self.assertEqual(links, {SOURCE})


if __name__ == "__main__":
    unittest.main()
