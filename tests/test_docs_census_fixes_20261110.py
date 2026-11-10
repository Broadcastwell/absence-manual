"""The STEP 3.2 truth census fixes of 10 November 2026 (twelve docs findings, our own wording only).

Each corrected sentence is pinned where it is published, and none of the old phrases may return anywhere in
docs/. The /answers/buying/ hub is served from its pinned published body through a reviewed visibility edit,
so its one old summary line stays in the unserved hub source only as that edit's before text, and the served
text is the corrected summary. No registered field-study page is touched.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
VISIBILITY = ROOT / "tools/library-visibility-20261105.json"
PLAN = ROOT / "tools/library-followup-20261105.json"
FREEZE = ROOT / "tools/library_field_freeze_navigation.json"

ANSWER = "answers/buying/which-geo-agencies-serve-new-companies.md"
HUB = "answers/buying/index.md"
SUMMARY = ("Citant and Embarque are candidates in our dated comparison of agencies for new companies. "
           "Their 29 October 2026 snapshots each have four of eight Yes cells.")
HUB_SOURCE_LINE = ("Citant and Embarque each have four Yes cells out of eight in our dated startup comparison; "
                   "inspect the different evidence behind those equal totals.")
STATE = "State: supported, conflicting, stale, not found or awaiting review"

# Every corrected sentence, with the number of times it appears in its file.
CORRECTED = {
    ANSWER: [
        ("description: " + SUMMARY, 1),
        ("If you are choosing GEO help for a new company, our dated comparison of agencies for new companies "
         "includes Citant and Embarque as candidates to examine.", 1),
        ("- [The comparison for new companies](https://broadcastwell.com/best-geo-agencies-for-startups)", 1),
        ("Citant's Open data cell concerns the published dataset behind its assessment.", 1),
    ],
    "llms.txt": [
        ("- [Which GEO agencies serve new companies?](https://docs.broadcastwell.com/answers/buying/"
         "which-geo-agencies-serve-new-companies/): " + SUMMARY, 1),
    ],
    "launchpad.md": [
        ("New individual referral approvals for work in California, Massachusetts or New Jersey start only "
         "after counsel clearance is recorded. Learn is open.", 1),
    ],
    "research/index.md": [
        ("**Field test:** our [registered 45-page, three-arm protocol](studies/evidence-refresh-field-test/) "
         "freezes the allocation and proposed additions at [OSF dmfpj](https://doi.org/10.17605/OSF.IO/DMFPJ).", 1),
    ],
    "research/academic-access/index.md": [
        ("its three frozen files fix the design, allocation and proposed additions.\n\nOSF preserves the "
         "registered plans.", 1),
    ],
    "resources/audit/executive-template.md": [("All remain open until evidence exists.", 1)],
    "assets/learning/audit/executive-template.txt": [("All remain open until evidence exists.", 1)],
    "resources/briefs/integration.md": [
        ("Unsupported setup claims remain omitted or explicitly marked unconfirmed.", 1)],
    "assets/learning/briefs/integration.txt": [
        ("Unsupported setup claims remain omitted or explicitly marked unconfirmed.", 1)],
    "resources/briefs/procurement.md": [
        ("Mark them as awaiting evidence and identify the accountable reviewer before procurement proceeds.", 1)],
    "assets/learning/briefs/procurement.txt": [
        ("Mark them as awaiting evidence and identify the accountable reviewer before procurement proceeds.", 1)],
    "resources/guides/product-facts.md": [("A candidate claim stays unapproved until the reviewer resolves it.", 1)],
    "assets/learning/resources/product-facts.txt": [
        ("A candidate claim stays unapproved until the reviewer resolves it.", 1)],
    "resources/playbooks/fact-verification.md": [
        ("Versioned fact row with approved or unapproved wording, source, owner, reviewer, permitted uses, state "
         "and review trigger.", 1)],
    "assets/learning/playbooks/fact-verification.txt": [
        ("Versioned fact row with approved or unapproved wording, source, owner, reviewer, permitted uses, state "
         "and review trigger.", 1)],
    # The worksheet label and its field name, and the key of the blank export.
    "resources/worksheets/product-facts.md": [
        ('<label for="f8">' + STATE + '</label><textarea id="f8" name="' + STATE + '"', 1)],
    "assets/learning/worksheets/product-facts.json": [('"' + STATE + '": ""', 1)],
}

# The old phrases of the twelve findings. None may return in docs/.
OLD = [
    "held pending lawyer review",
    "startup comparison",
    "Field test, data pending",
    "Data collection is pending.",
    "All remain pending until evidence exists.",
    "explicitly pending",
    "Mark them pending evidence",
    "A candidate claim remains pending until the reviewer resolves it.",
    "approved or pending wording",
    "not found or pending",
]
TEXT_SUFFIXES = {".md", ".txt", ".json", ".csv", ".html", ".js", ".xml", ".yml", ".yaml", ".svg", ".css", ".bib",
                 ".ris", ".tsv"}


def read(rel):
    return (DOCS / rel).read_text(encoding="utf-8")


class CensusFixesTests(unittest.TestCase):
    def test_each_corrected_sentence_is_published_once(self):
        for rel, sentences in CORRECTED.items():
            text = read(rel)
            for sentence, count in sentences:
                with self.subTest(file=rel, sentence=sentence[:50]):
                    self.assertEqual(text.count(sentence), count)

    def test_no_old_phrase_returns_in_docs(self):
        found = []
        for path in sorted(DOCS.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            rel = path.relative_to(DOCS).as_posix()
            text = path.read_text(encoding="utf-8", errors="replace")
            if rel == HUB:
                # The unserved hub source keeps the one line its reviewed visibility edit replaces.
                self.assertEqual(text.count(HUB_SOURCE_LINE), 1)
                text = text.replace(HUB_SOURCE_LINE, "")
            found.extend((rel, phrase) for phrase in OLD if phrase in text)
        self.assertEqual(found, [])

    def test_served_answer_hub_and_llms_texts_carry_the_corrected_summary(self):
        decisions = json.loads(VISIBILITY.read_bytes())
        self.assertEqual(decisions["pages"][ANSWER]["meta"]["description"], SUMMARY)
        self.assertTrue(150 <= len(SUMMARY) <= 160)
        hub = [e for e in decisions["pages"][HUB]["edits"] if e["before"] == HUB_SOURCE_LINE]
        self.assertEqual(hub, [{"after": SUMMARY, "before": HUB_SOURCE_LINE, "count": 1}])
        llms = [e for e in decisions["llms_edits"] if "/which-geo-agencies-serve-new-companies/)" in e["before"]]
        self.assertEqual(len(llms), 1)
        self.assertTrue(llms[0]["after"].endswith("): " + SUMMARY))

    def test_no_served_decision_reintroduces_an_old_phrase(self):
        decisions = json.loads(VISIBILITY.read_bytes())
        plan = json.loads(PLAN.read_bytes())
        served = [r["meta"]["description"] for r in decisions["pages"].values()]
        served += [e["after"] for r in decisions["pages"].values() for e in r["edits"]]
        served += [e["after"] for e in decisions["llms_edits"]]
        served += [e["after"] for e in plan["llms_edits"]]
        served += [e["after"] for edits in plan.get("effective_edits", {}).values() for e in edits]
        self.assertEqual([(phrase, text[:80]) for text in served for phrase in OLD if phrase in text], [])

    def test_no_registered_field_study_page_is_among_the_corrected_pages(self):
        frozen = set(json.loads(FREEZE.read_bytes())["pages"])
        corrected = {rel for rel in CORRECTED if rel.endswith(".md")}
        self.assertEqual(len(frozen), 45)
        self.assertEqual(frozen & corrected, set())


if __name__ == "__main__":
    unittest.main()
