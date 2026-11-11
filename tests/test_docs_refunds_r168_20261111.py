"""One refund wording on the docs (STEP 3.3 B134, follow-up 3 item 2, ruling R-168, 11 November 2026).

The ruled sentences are the only refund sentences on any surface. Where a longer sentence folded a refund into a
clause, it is split so the ruled sentence stands whole: the Answer Repair long form is three sentences, the
Agency Deadline Audit sentence ends "of delivery", the Fix Sprint pair and the live question sentence are word
for word. The served llms.txt comes from the released consumer plus the plan's literal edits, so the same four
lines are plan llms edits and docs/llms.txt lines. tools/verify_build.py fails a served file that keeps an older
wording; these tests read that list from verify_build.py, so there is one list. The 45 registered pages, the 53
research pages and dated records (the operating framework's quotation of the 9 November 2026 pages, the answer
library's dated agency records) are not edited.
"""
import ast
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PLAN = ROOT / "tools" / "library-followup-20261105.json"

AR_LONG = ("If we miss the deliverable or deadline, we initiate a full $490 refund within five business days. "
           "You keep the work. You may also request a full refund within 30 days of delivery.")
AR_SHORT = "Full refund on request within 30 days of delivery."
AUDIT = "Refundable in full within 30 days of delivery."
SPRINT = "Measured gain on the agreed test, or the full $3,900 back. You keep the work."
LIVE = "If we do not deliver within 24 hours of payment, we refund the $19 in full."

CHANGED = {
    "index.md": [AR_LONG, "Findings within 48 hours of recorded scope confirmation. " + AUDIT, SPRINT, LIVE],
    "agency-training.md": ["- **The refund.** " + AUDIT],
    "media-kit.md": ["> Answer Repair, $490 once: one buyer question fixed with a source-backed page or change, "
                     "due 48 hours after Ready. " + AR_SHORT],
    "rfp-guide.md": ["**Our answer:** Answer Repair costs $490 once. " + AR_LONG + " Every refund term is quoted",
                     "agrees one primary test before payment and measures it again at day 30. " + SPRINT],
    "llms.txt": ["Due 48 elapsed hours after recorded Ready. " + AR_LONG + " https://broadcastwell.com/answer-repair",
                 "Findings within 48 hours of recorded scope confirmation. " + AUDIT + " No full-page deployment.",
                 SPRINT + " Includes ChatGPT Business Hub readiness parts 1 to 4", LIVE,
                 "under the agency brand. Findings within 48 hours of recorded scope confirmation. " + AUDIT],
}
LLMS_LINES = {
    "- Answer Repair: $490.": "- Answer Repair: $490. One buyer question and one completed source-backed page or "
    "equivalent fix. Choose Live or Handoff before payment. Live access and approval must be complete before "
    "payment. Due 48 elapsed hours after recorded Ready. " + AR_LONG + " https://broadcastwell.com/answer-repair",
    "- Agency Deadline Audit: $490 per client report, white label.": None,
    "- Fix Sprint: $3,900": None,
    "- [Agency Deadline Audit | Broadcastwell](https://broadcastwell.com/for-agencies):": None,
}


def verify_build_constant(name):
    tree = ast.parse((ROOT / "tools" / "verify_build.py").read_text(encoding="utf8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError(name + " is missing from verify_build.py")


def text(rel):
    return (DOCS / rel).read_text(encoding="utf-8")


def public_sources():
    frozen = set(json.loads((ROOT / "tools" / "library_field_freeze_navigation.json").read_bytes())["pages"])
    for path in sorted(DOCS.rglob("*")):
        rel = path.relative_to(DOCS).as_posix()
        if not path.is_file() or path.suffix not in {".md", ".txt", ".json", ".html", ".csv"}:
            continue
        if rel in frozen or rel.startswith(("research/", "assets/research/")):
            continue
        yield rel, path


class RefundSentenceTests(unittest.TestCase):
    def test_each_changed_source_carries_the_ruled_sentences(self):
        for rel, sentences in CHANGED.items():
            body = text(rel)
            for sentence in sentences:
                with self.subTest(source=rel, sentence=sentence[:60]):
                    self.assertIn(sentence, body)

    def test_no_public_docs_source_keeps_an_older_refund_wording(self):
        old_wording = verify_build_constant("OLD_REFUND_WORDING")
        self.assertGreaterEqual(len(old_wording), 10)
        for rel, path in public_sources():
            body = path.read_text(encoding="utf-8", errors="replace")
            for old in old_wording:
                with self.subTest(source=rel, old=old):
                    self.assertNotIn(old, body)

    def test_the_older_wording_list_never_matches_a_ruled_sentence(self):
        old_wording = verify_build_constant("OLD_REFUND_WORDING")
        ruled = verify_build_constant("RULED_REFUND_SENTENCES")
        self.assertEqual(ruled, (AR_LONG, AUDIT, SPRINT, LIVE))
        for sentence in (AR_LONG, AR_SHORT, AUDIT, SPRINT, LIVE,
                         "If we miss the work or the deadline, we start the refund ourselves.",
                         "Agreed in writing before payment, with no automatic enrollment."):
            for old in old_wording:
                self.assertNotIn(old, sentence)

    def test_context_pack_answers_use_the_live_question_and_fix_sprint_sentences(self):
        pack = json.loads((DOCS / "context-pack" / "broadcastwell.json").read_bytes())
        answers = {a["id"]: a for group in pack["groups"].values() for a in group}
        self.assertTrue(answers["pricing-live-question"]["answer"].endswith(LIVE))
        self.assertTrue(answers["pricing-fix-sprint"]["answer"].endswith("measured again at day 30. " + SPRINT))
        for answer in answers.values():
            self.assertEqual(answer["reviewed"], "2026-11-09")

    def test_served_llms_lines_are_plan_edits_that_end_in_the_source_lines(self):
        plan = json.loads(PLAN.read_bytes())
        source = text("llms.txt").splitlines()
        edits = plan["llms_edits"]
        for prefix, whole in LLMS_LINES.items():
            line = next(l for l in source if l.startswith(prefix))
            if whole:
                self.assertEqual(line, whole)
            with self.subTest(line=prefix):
                last = [e for e in edits if e["after"].startswith(prefix) and e["after"] == line]
                self.assertEqual(len(last), 1)
                self.assertEqual(last[0]["count"], 1)
                self.assertNotEqual(last[0]["before"], last[0]["after"])

    def test_the_operating_framework_keeps_its_dated_quotation(self):
        body = text("operating-framework.md")
        self.assertIn("quoted below exactly as our pricing, offer and method pages state them on 9 November 2026.", body)
        for quoted in (LIVE, AR_LONG, SPRINT):
            self.assertIn('> "' + quoted + '"', body)

    def test_no_changed_source_shows_the_derived_471(self):
        for rel in CHANGED:
            self.assertNotIn("$471", text(rel))
        self.assertNotIn("$471", text("context-pack/broadcastwell.json"))


if __name__ == "__main__":
    unittest.main()
