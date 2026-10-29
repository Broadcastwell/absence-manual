"""Independent literals for a proposed seven-record source extension.

These validation fixtures are fictional. They are not drafted library pages.
"""
import re
import unittest

import test_answers_published_audit as original_audit_tests
from tools.library_answers import (
    APPROVED_PUBLICATION_AUDITS, PUBLICATION_AUDIT_REVIEW_STATUS_UPDATES,
)


# These literals come from the pinned public cards, not the guard constants.
EXTRA_FACTS = (
    ("first-page-sage", "First Page Sage", ("Partial", "No", "Yes", "No", "No", "Yes", "No", "No"), 2),
    ("omniscient", "Omniscient Digital", ("Partial", "No", "Yes", "Partial", "No", "Yes", "Yes", "Partial"), 3),
    ("optimist", "Optimist", ("Partial", "No", "Yes", "Partial", "No", "Yes", "Not verified", "Partial"), 2),
    ("relevance", "Relevance", ("Partial", "No", "Yes", "No", "No", "Yes", "Not verified", "Partial"), 2),
    ("single-grain", "Single Grain", ("Partial", "No", "Yes", "No", "No", "Yes", "Yes", "Partial"), 3),
    ("skale", "Skale", ("Partial", "No", "Yes", "Partial", "No", "Yes", "Not verified", "Partial"), 2),
    ("webfx", "WebFX", ("Partial", "No", "Yes", "Partial", "No", "Yes", "Not verified", "Yes"), 3),
)
REVIEW_UPDATE_IDS = {"optimist", "relevance", "skale", "webfx"}
MAIN, STARTUP = original_audit_tests.MAIN, original_audit_tests.STARTUP


class PublicationAuditExtensionTests(unittest.TestCase):
    def setUp(self):
        self.fixture_helper = original_audit_tests.PublicationAuditTests()
        self.fixture_helper.setUp()
        self.addCleanup(self.fixture_helper.doCleanups)

    def fixture(self, rows):
        f = self.fixture_helper
        f.fixture(MAIN)
        rows = sorted(rows, key=lambda row: row[1].casefold())
        f.meta["evidence_audit_records"] = [row[0] for row in rows]
        rid, name, states, count = rows[0]
        old_opening = "[Go Fish Digital](" + MAIN + "#go-fish-digital) has 3 of 8 Yes cells"
        new_opening = "[" + name + "](" + MAIN + "#" + rid + ") has " + str(count) + " of 8 Yes cells"
        assert old_opening in f.body
        f.body = f.body.replace(old_opening, new_opening, 1)
        table = "| Agency | Method | Open data | Engines | Price | Refund | B2B cases | Reviews | Machine readable | Yes count |\n"
        table += "|---|---|---|---|---|---|---|---|---|---|\n"
        for record_id, record_name, statuses, score in rows:
            table += "| " + " | ".join(["[" + record_name + "](" + MAIN + "#" + record_id + ")", *statuses, str(score) + "/8"]) + " |\n"
        f.body, changes = re.subn(r"\| Agency \|[^\n]*\n(?:\|[^\n]*\n)+", lambda _: table, f.body, count=1)
        assert changes == 1
        dated_updates = " ".join(name + "'s Reviews cell was Not verified on 29 September 2026." for rid, name, _, _ in rows if rid in REVIEW_UPDATE_IDS)
        if dated_updates:
            f.body = f.body.replace("[Published criteria]", dated_updates + "\n\n[Published criteria]", 1)
        return f

    def test_all_seven_independent_source_literals_and_counts_are_exact(self):
        records = APPROVED_PUBLICATION_AUDITS[MAIN]["records"]
        for rid, name, statuses, count in EXTRA_FACTS:
            with self.subTest(record=rid):
                self.assertEqual(records[rid], {"name": name, "statuses": statuses})
                self.assertEqual(statuses.count("Yes"), count)
                self.assertEqual(len(statuses), 8)

    def test_every_individual_record_with_its_actual_dates_passes(self):
        for row in EXTRA_FACTS:
            with self.subTest(record=row[0]):
                f = self.fixture([row])
                self.assertEqual(f.errors(), "")

    def test_all_seven_records_pass_in_alphabetical_order(self):
        f = self.fixture(EXTRA_FACTS)
        self.assertEqual(f.errors(), "")

    def test_new_source_metadata_keeps_the_existing_exact_pins(self):
        main = APPROVED_PUBLICATION_AUDITS[MAIN]
        self.assertEqual(set(APPROVED_PUBLICATION_AUDITS), {MAIN, STARTUP})
        self.assertEqual(main["observed_at"], "2026-10-29T14:37:02.799269+00:00")
        self.assertEqual(main["snapshot_sha256"], "4c2722c06bb8308bc8900e85d18599cfdd2a1ee870261152455a1ccbfe47af54")
        self.assertEqual(main["dates"], ("15 September 2026", "16 September 2026", "28 October 2026"))
        self.assertEqual(PUBLICATION_AUDIT_REVIEW_STATUS_UPDATES, {MAIN: {
            "optimist": ("29 September 2026", "Not verified"),
            "relevance": ("29 September 2026", "Not verified"),
            "skale": ("29 September 2026", "Not verified"),
            "webfx": ("29 September 2026", "Not verified"),
        }})

    def test_missing_named_not_verified_update_fails_all_four(self):
        for row in EXTRA_FACTS:
            if row[0] not in REVIEW_UPDATE_IDS:
                continue
            with self.subTest(record=row[0]):
                f = self.fixture([row])
                f.body = f.body.replace(row[1] + "'s Reviews cell was Not verified on 29 September 2026.", "")
                self.assertIn("reviews = 29 September 2026", f.errors())

    def test_wrong_update_date_and_wrong_record_attribution_fail(self):
        for row in EXTRA_FACTS:
            if row[0] not in REVIEW_UPDATE_IDS:
                continue
            with self.subTest(record=row[0]):
                f = self.fixture([row])
                f.body = f.body.replace(row[1] + "'s Reviews cell was Not verified on 29 September 2026.", row[1] + "'s Reviews cell was Not verified on 29 October 2026.")
                self.assertIn("contradicts the approved field/read dates", f.errors())
                f = self.fixture([row])
                f.body = f.body.replace(row[1] + "'s Reviews cell was Not verified on 29 September 2026.", "An unselected agency's Reviews cell was Not verified on 29 September 2026.")
                self.assertIn("reviews = 29 September 2026", f.errors())

    def test_status_update_is_not_a_new_review_read_or_original_read_date(self):
        f = self.fixture([EXTRA_FACTS[2]])
        for extra in ("Optimist's Reviews were freshly read on 29 September 2026.", "All original company-site fields were read on 29 September 2026."):
            with self.subTest(claim=extra):
                original = f.body
                f.body = original.replace("[Published criteria]", extra + "\n\n[Published criteria]", 1)
                self.assertIn("contradicts the approved field/read dates", f.errors())
                f.body = original

    def test_unselected_update_cannot_supply_the_selected_record_date(self):
        f = self.fixture([EXTRA_FACTS[2]])
        f.body = f.body.replace("Optimist's Reviews cell was Not verified on 29 September 2026.", "Skale's Reviews cell was Not verified on 29 September 2026.")
        errors = f.errors()
        self.assertIn("reviews = 29 September 2026", errors)
        self.assertIn("contradicts the approved field/read dates", errors)

    def test_status_update_cannot_smuggle_in_a_fresh_read_or_reread(self):
        for row in EXTRA_FACTS:
            if row[0] not in REVIEW_UPDATE_IDS:
                continue
            for claim in (
                row[1] + "'s Reviews were freshly read and Not verified on 29 September 2026.",
                row[1] + "'s Reviews were reread on 29 September 2026 and Not verified.",
                row[1] + "'s Reviews were read on 29 September 2026 and Not verified.",
            ):
                with self.subTest(record=row[0], claim=claim):
                    f = self.fixture([row])
                    f.body = f.body.replace(row[1] + "'s Reviews cell was Not verified on 29 September 2026.", claim)
                    self.assertIn("review-status update is not evidence of a fresh review read", f.errors())

    def test_truthful_negated_read_clarification_does_not_change_status_date(self):
        for row in EXTRA_FACTS:
            if row[0] not in REVIEW_UPDATE_IDS:
                continue
            with self.subTest(record=row[0]):
                f = self.fixture([row])
                f.body = f.body.replace(
                    row[1] + "'s Reviews cell was Not verified on 29 September 2026.",
                    row[1] + "'s Reviews were Not verified on 29 September 2026, without a new read of the review platform.",
                )
                self.assertEqual(f.errors(), "")

    def test_review_update_date_is_not_accepted_for_other_new_records(self):
        for row in EXTRA_FACTS:
            if row[0] in REVIEW_UPDATE_IDS:
                continue
            with self.subTest(record=row[0]):
                f = self.fixture([row])
                f.body = f.body.replace("[Published criteria]", row[1] + "'s Reviews cell was Not verified on 29 September 2026.\n\n[Published criteria]", 1)
                self.assertIn("contradicts the approved field/read dates", f.errors())

    def test_not_verified_states_cannot_be_replaced_with_no(self):
        for row in EXTRA_FACTS:
            if row[0] not in REVIEW_UPDATE_IDS:
                continue
            with self.subTest(record=row[0]):
                f = self.fixture([row])
                f.body = f.body.replace("| Not verified |", "| No |")
                self.assertIn("eight statuses and Yes counts", f.errors())

    def test_wrong_count_and_status_fail_for_every_new_record(self):
        for row in EXTRA_FACTS:
            with self.subTest(record=row[0]):
                f = self.fixture([row])
                f.body = f.body.replace("| " + str(row[3]) + "/8 |", "| " + str(row[3] + 1) + "/8 |")
                self.assertIn("table must match", f.errors())
                f = self.fixture([row])
                f.body = f.body.replace("| Partial |", "| Yes |", 1)
                self.assertIn("table must match", f.errors())

    def test_wrong_anchor_aliases_and_cross_source_are_rejected(self):
        f = self.fixture([EXTRA_FACTS[1]])
        f.body = f.body.replace(MAIN + "#omniscient", MAIN + "#omniscient-digital")
        self.assertIn("exact source anchor", f.errors())
        f = self.fixture([EXTRA_FACTS[1]])
        f.meta["evidence_audit_records"] = ["omniscient-digital"]
        self.assertIn("not approved for this source", f.errors())
        f = self.fixture([EXTRA_FACTS[1]])
        f.meta["is_based_on"] = STARTUP
        self.assertIn("not approved for this source", f.errors())

    def test_all_new_provider_prices_and_outcome_inferences_still_fail(self):
        for row in EXTRA_FACTS:
            for suffix in (" is free.", " delivers better client results."):
                with self.subTest(record=row[0], suffix=suffix):
                    f = self.fixture([row])
                    f.body = f.body.replace("## Also asked as", row[1] + suffix + "\n\n## Also asked as")
                    self.assertIn("publication-audit", f.errors())

    def test_old_snapshot_boundaries_cannot_be_overridden_for_new_records(self):
        f = self.fixture([EXTRA_FACTS[1]])
        f.meta["evidence_audit_observed_at"] = "2026-10-29T18:00:00+00:00"
        self.assertIn("exact approved evidence_audit_observed_at", f.errors())
        f = self.fixture([EXTRA_FACTS[1]])
        f.meta["evidence_audit_snapshot_sha256"] = "0" * 64
        self.assertIn("exact approved evidence_audit_snapshot_sha256", f.errors())
        f = self.fixture([EXTRA_FACTS[1]])
        f.meta["is_based_on"] = MAIN + "/"
        self.assertIn("outside the two approved audit URLs", f.errors())


if __name__ == "__main__":
    unittest.main()
