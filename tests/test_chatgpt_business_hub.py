"""ChatGPT Business Hub guides: schema, examples, context packs, copy rules and overlap."""
import csv
import datetime
import hashlib
import json
import re
import unittest
from pathlib import Path
from urllib.parse import urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
HUB = DOCS / "chatgpt-business-hub"
PAGES = ["index.md", "business-facts-file.md", "context-pack.md", "watch.md", "reconciliation-report.md"]
SCHEMA_PATH = DOCS / "business-facts.schema.json"
FACTS_FILES = [DOCS / "business-facts.json", DOCS / "examples" / "kalvenor-business-facts.json"]
PACK_FILES = [DOCS / "context-pack" / "broadcastwell.json", DOCS / "context-pack" / "kalvenor.json"]
RECONCILIATION_CSV = DOCS / "examples" / "kalvenor-reconciliation-2026-10.csv"
SITE = "https://docs.broadcastwell.com/"

READINESS_ANCHORS = [
    "ownership-verification", "organization-data", "product-data", "llms-txt", "crawler-policy",
    "sitemap", "name-consistency", "commerce-connection", "business-facts-file", "context-pack",
]
PACK_GROUPS = ["company", "pricing", "fit", "integrations", "compliance", "links"]
FIVE_ENGINES = ["ChatGPT", "Claude", "Perplexity", "Google AI Overviews", "Google AI Mode"]
PACK_SOURCE_PAGES = {
    "https://broadcastwell.com/pricing", "https://broadcastwell.com/faq",
    "https://broadcastwell.com/answer-repair", "https://broadcastwell.com/fix-sprint",
    "https://broadcastwell.com/for-agencies", "https://broadcastwell.com/security",
    "https://broadcastwell.com/methodology",
}
LADDER_PRICES = {
    "Live question": ("19", "once"), "Answer Repair": ("490", "once"),
    "Agency Deadline Audit": ("490", "per client report"), "Fix Sprint": ("3900", "once"),
    "Care": ("490", "a month"), "Program": ("5500", "a month"),
}
FRESHNESS_DAYS = 90
PRICING_EXPIRY_DAYS = 30
OTHER_EXPIRY_DAYS = 90
SHINGLE_WORDS = 6
NEAR_DUPLICATE_LIMIT = 0.20
UPDATED_LINE = "Updated 9 November 2026."
# The client enrolment block is the lead's exact copy. It is pinned by hash and exempt from the
# generated-copy scan below; any edit to it must come with a new reviewed hash.
CLIENT_BLOCK_ANCHOR = '<a id="clients"></a>'
CLIENT_BLOCK_SHA256 = "f3dd7d7b53166fad843dd3b4ac85cf3d520f79972ad68ae8ed8a917d9e2a2ecb"
CLIENT_BLOCK_NEXT_HEADING = "## Why measure prompts too"
# STEP 3.2 (9 November 2026): the lead's exact client sentence and rarity sentence. STEP 3.3 (brief
# 9.4 and 18.2, 10 November 2026): the table headed "Part (status as of 9 November 2026)" and its
# "Pending" cells are removed; the client block is the anchor and the one client sentence, unchanged.
CLIENT_SENTENCE = ("Our current clients Vantaa Tax, Neurvalis and Valren Atelier are enrolled in this program; "
                   "their readiness work is under way, and we claim each of them on the first day OpenAI opens "
                   "the tool to them.")
RARITY_SENTENCE = ("On 9 November 2026 we checked the 40 companies in our competitor review; 0 of them published "
                   "a readiness program for this tool.")
REMOVED_TABLE_HEADER = "| Part (status as of 9 November 2026) | Vantaa Tax | Neurvalis | Valren Atelier |"
REMOVED_STATUS_WORDS = ("Pending", "status as of 9 November 2026", "Preparation status", "Prepared, 9 November 2026")
# Organization sameAs on every page outside the 45 registered pages (owner ruling, 9 November 2026):
# the six channels plus GitHub, in this order.
SAME_AS = [
    "https://www.linkedin.com/company/broadcastwell", "https://x.com/broadcastwellhq",
    "https://broadcastwell.substack.com/", "https://www.youtube.com/@Broadcastwell",
    "https://www.instagram.com/broadcastwell/", "https://www.tiktok.com/@broadcastwell.com",
    "https://github.com/Broadcastwell",
]

# Public copy rules for STEP 3.1, matched case-insensitively as whole phrases.
BANNED_PHRASES = [
    "category audit", "white-label category audit", "ai visibility diagnostic", "re-measure",
    "sprint channel add-on", "free audit", "paused", "on hold", "waitlist", "pilot", "early-stage",
    "coming soon", "6.7x", "40 percent", "41 percent", "40%", "41%", "our limitations",
    "no reviews yet", "founded 2026", "twelve people", "incomplete", "pending", "delve", "tapestry",
    "seamless", "unlock", "game-changer", "cutting-edge", "fast-paced", "leverage", "robust",
    "holistic", "empower", "number one", "leading", "closed",
    "temporarily", "capacity", "limited availability", "not open", "reopen", "studio", "boutique",
    "startup", "founder-led", "four engines",
]
BANNED_PRICES = ["$89", "$169", "$190", "$900", "$990", "$1,500", "$2,410", "$2,900", "$4,500", "$13,500"]
BANNED_CASE_SENSITIVE = ["Diagnostic"]
# Company names that public copy must never carry, stored as SHA-256 of the lowercase word.
WITHHELD_NAME_SHA256 = {
    "8597fc7dcf92c5772471c8deb7892eeb874a960bc0d8c8b41d11deaeb87320e0",
    "9f0a2de9440866323f25b65209c7fce68fad18127caf49dc805c2b658a77a1f8",
    "1b55c05b1e1cdc64865d7333aae4d3c5b0085f77a95d08982e6e3ae68ce79fa9",
}
FIVE_ENGINE_LIST = "ChatGPT, Claude, Perplexity, Google AI Overviews and Google AI Mode"


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)


def split_page(path):
    text = Path(path).read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, re.S)
    if not match:
        raise ValueError("Front matter missing: %s" % path)
    return yaml.safe_load(match.group(1)), match.group(2)


# ---------- a small JSON Schema 2020-12 validator for the keywords the schema uses ----------

SUPPORTED_KEYWORDS = {
    "$schema", "$id", "title", "description", "$defs", "$ref", "type", "properties", "required",
    "additionalProperties", "items", "minItems", "maxItems", "minLength", "maxLength", "pattern",
    "const", "enum", "format", "oneOf",
}
TYPES = {
    "object": lambda v: isinstance(v, dict), "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str), "boolean": lambda v: isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
}
HOSTNAME = re.compile(r"^(?=.{1,253}$)[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?(\.[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$")
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def schema_keywords(schema, found=None):
    found = set() if found is None else found
    if isinstance(schema, dict):
        found.update(schema)
        for key in ("properties", "$defs"):
            for child in schema.get(key, {}).values():
                schema_keywords(child, found)
        for key in ("items",):
            if isinstance(schema.get(key), dict):
                schema_keywords(schema[key], found)
        for child in schema.get("oneOf", []):
            schema_keywords(child, found)
    return found


def format_ok(kind, value):
    if kind == "date":
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            return False
        try:
            datetime.date.fromisoformat(value)
        except ValueError:
            return False
        return True
    if kind == "uri":
        parts = urlsplit(value)
        return bool(parts.scheme and parts.netloc)
    if kind == "email":
        return bool(EMAIL.match(value))
    if kind == "hostname":
        return bool(HOSTNAME.match(value))
    raise ValueError("Unsupported format " + kind)


def validate(instance, schema, root, path="$"):
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/$defs/"):
            raise ValueError("Only local $defs references are supported")
        return validate(instance, root["$defs"][ref.split("/")[-1]], root, path)
    errors = []
    if "type" in schema and not TYPES[schema["type"]](instance):
        return [path + ": expected " + schema["type"]]
    if "const" in schema and (instance != schema["const"] or type(instance) is not type(schema["const"])):
        errors.append(path + ": must equal " + json.dumps(schema["const"]))
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(path + ": not an allowed value")
    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            errors.append(path + ": too short")
        if len(instance) > schema.get("maxLength", 10 ** 9):
            errors.append(path + ": too long")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append(path + ": does not match its pattern")
        if "format" in schema and not format_ok(schema["format"], instance):
            errors.append(path + ": not a valid " + schema["format"])
    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            errors.append(path + ": too few items")
        if len(instance) > schema.get("maxItems", 10 ** 9):
            errors.append(path + ": too many items")
        if "items" in schema:
            for index, item in enumerate(instance):
                errors += validate(item, schema["items"], root, "%s[%d]" % (path, index))
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(path + ": missing " + key)
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in properties:
                    errors.append(path + ": unknown field " + key)
        for key, child in properties.items():
            if key in instance:
                errors += validate(instance[key], child, root, path + "." + key)
    if "oneOf" in schema:
        matches = sum(1 for option in schema["oneOf"] if not validate(instance, option, root, path))
        if matches != 1:
            errors.append(path + ": must match exactly one allowed shape, matched %d" % matches)
    return errors


def all_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from all_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from all_strings(item)


def business_facts_report(data, schema, today):
    """Return (errors, warnings) for the twelve published validator rules."""
    errors = validate(data, schema, schema)
    warnings = []
    if errors:
        return errors, warnings
    reviewed = datetime.date.fromisoformat(data["last_reviewed"])
    if reviewed > today:
        errors.append("rule 4: last_reviewed is in the future")
    for value in all_strings(data):
        if re.match(r"(?i)^[a-z][a-z0-9+.-]*://", value) and not value.startswith("https://"):
            errors.append("rule 5: URL is not HTTPS: " + value)
    domain = data["domain"]
    facts = urlsplit(data["facts_url"])
    if not (facts.hostname == domain or facts.hostname.endswith("." + domain)) or facts.path != "/business-facts.json":
        errors.append("rule 6: facts_url must be /business-facts.json on the domain or a subdomain")
    for profile in data["same_as"]:
        if urlsplit(profile).hostname in {domain, "www." + domain}:
            errors.append("rule 7: same_as points at the business's own domain")
    names = [offer["name"] for offer in data["offers"]]
    if len(names) != len(set(names)):
        errors.append("rule 10: offer names repeat")
    if data.get("sample") is True and not (data.get("fictional") is True and str(data.get("label", "")).startswith("SAMPLE DATA")):
        errors.append("rule 11: a sample must be fictional and labeled SAMPLE DATA")
    if (today - reviewed).days > FRESHNESS_DAYS:
        warnings.append("rule 12: last_reviewed is more than %d days old" % FRESHNESS_DAYS)
    return errors, warnings


# ---------- copy checks ----------

def banned_hits(text):
    hits = []
    lowered = text.lower()
    for phrase in BANNED_PHRASES:
        if re.search(r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])", lowered):
            hits.append(phrase)
    for price in BANNED_PRICES:
        if re.search(re.escape(price) + r"(?![0-9,])", text):
            hits.append(price)
    for word in BANNED_CASE_SENSITIVE:
        if re.search(r"\b" + word + r"\b", text):
            hits.append(word)
    for token in set(re.findall(r"[a-z]+", lowered)):
        if hashlib.sha256(token.encode()).hexdigest() in WITHHELD_NAME_SHA256:
            hits.append("withheld company name")
    for mark, name in ((chr(0x2014), "em dash"), (chr(0x2013), "en dash"), (chr(0xB7), "middle dot"), ("!", "exclamation mark")):
        if mark in text:
            hits.append(name)
    prose = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    prose = re.sub(r"(?m)^\|[-|\s:]+$", "", prose)
    if "-" + "-" in prose:
        hits.append("double hyphen")
    return hits


def client_block(body):
    """The exact lead-supplied block, from its anchor line to the heading that follows it."""
    start = body.index(CLIENT_BLOCK_ANCHOR + chr(10))
    end = body.index(chr(10) + CLIENT_BLOCK_NEXT_HEADING, start)
    return body[start:end]


def new_public_texts():
    texts = {"docs/chatgpt-business-hub/" + name: (HUB / name).read_text(encoding="utf-8") for name in PAGES}
    hub = texts["docs/chatgpt-business-hub/index.md"]
    texts["docs/chatgpt-business-hub/index.md"] = hub.replace(client_block(hub), "")
    for path in FACTS_FILES + PACK_FILES + [SCHEMA_PATH, RECONCILIATION_CSV]:
        texts[path.relative_to(ROOT).as_posix()] = path.read_text(encoding="utf-8")
    llms = (DOCS / "llms.txt").read_text(encoding="utf-8")
    texts["docs/llms.txt (new lines)"] = "\n".join(
        line for line in llms.splitlines() if "chatgpt-business-hub/" in line or "business-facts.json" in line)
    return texts


# ---------- near-duplicate measure ----------

def prose_tokens(markdown):
    body = re.sub(r"\A---\n.*?\n---\n", "", markdown, flags=re.S)
    body = re.sub(r"(?ms)^```.*?^```[ \t]*$", " ", body)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    body = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", body)
    body = re.sub(r"\{#[^}]*\}", " ", body)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"https?://\S+", " ", body)
    return re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)*", body.lower().replace(chr(0x2019), "'"))


def shingles(tokens, size=SHINGLE_WORDS):
    return {tuple(tokens[i:i + size]) for i in range(len(tokens) - size + 1)}


def overlap(left, right):
    smaller = min(len(left), len(right))
    return len(left & right) / smaller if smaller else 0.0


def near_duplicate_rows():
    """Shared six-word sequences over the smaller page, for every new-page pairing."""
    new = {name: shingles(prose_tokens((HUB / name).read_text(encoding="utf-8"))) for name in PAGES}
    rows = []
    names = sorted(new)
    for i, left in enumerate(names):
        for right in names[i + 1:]:
            rows.append((overlap(new[left], new[right]), "chatgpt-business-hub/" + left, "chatgpt-business-hub/" + right))
    for path in sorted(DOCS.rglob("*.md")):
        if path.parent == HUB:
            continue
        existing = shingles(prose_tokens(path.read_text(encoding="utf-8")))
        if not existing:
            continue
        for name, grams in new.items():
            rows.append((overlap(grams, existing), "chatgpt-business-hub/" + name, path.relative_to(DOCS).as_posix()))
    return sorted(rows, reverse=True)


class BusinessFactsFileTests(unittest.TestCase):
    def setUp(self):
        self.schema = load_json(SCHEMA_PATH)
        self.today = datetime.date.today()

    def test_schema_declares_2020_12_and_uses_only_supported_keywords(self):
        self.assertEqual(self.schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(self.schema["$id"], SITE + "business-facts.schema.json")
        self.assertEqual(schema_keywords(self.schema) - SUPPORTED_KEYWORDS, set())

    def test_both_example_files_validate_against_the_schema_and_rules(self):
        for path in FACTS_FILES:
            with self.subTest(path=path.name):
                errors, _ = business_facts_report(load_json(path), self.schema, self.today)
                self.assertEqual(errors, [])

    def test_kalvenor_file_is_labeled_fictional_in_its_own_fields(self):
        data = load_json(FACTS_FILES[1])
        self.assertIs(data["sample"], True)
        self.assertIs(data["fictional"], True)
        self.assertTrue(data["label"].startswith("SAMPLE DATA"))
        self.assertIn("fictional", data["legal_name"])
        self.assertEqual(data["domain"], "kalvenor.example")

    def test_broadcastwell_file_carries_only_the_published_ladder_and_company_facts(self):
        data = load_json(FACTS_FILES[0])
        offers = {o["name"]: (o["price"]["amount"], o["price"]["unit"]) for o in data["offers"]}
        self.assertEqual(offers, LADDER_PRICES)
        self.assertTrue(all(o["price"]["currency"] == "USD" for o in data["offers"]))
        self.assertEqual(data["legal_name"], "Broadcastwell LLC")
        self.assertEqual(data["address"], {"street_address": "517 E Kirkwood Ave", "locality": "Bloomington",
                                           "region": "IN", "postal_code": "47408", "country": "US"})
        self.assertEqual(data["contact"]["phone"], "+1-812-345-7272")
        self.assertEqual(data["facts_url"], SITE + "business-facts.json")
        self.assertNotIn("sample", data)

    def test_the_validator_rejects_each_broken_rule(self):
        good = load_json(FACTS_FILES[0])
        cases = {
            "missing legal_name": lambda d: d.pop("legal_name"),
            "unknown field": lambda d: d.update(rating=5),
            "plain HTTP profile": lambda d: d["same_as"].append("http://example.org/broadcastwell"),
            "published price without amount": lambda d: d["offers"][0]["price"].pop("amount"),
            "unpublished price with amount": lambda d: d["offers"][0].update(price={"published": False, "price_url": "https://broadcastwell.com/pricing", "amount": "19"}),
            "lowercase currency": lambda d: d["offers"][0]["price"].update(currency="usd"),
            "facts_url elsewhere": lambda d: d.update(facts_url="https://example.org/business-facts.json"),
            "facts_url wrong path": lambda d: d.update(facts_url="https://broadcastwell.com/facts.json"),
            "own domain in same_as": lambda d: d["same_as"].append("https://broadcastwell.com/about"),
            "repeated offer": lambda d: d["offers"].append(dict(d["offers"][0])),
            "future review": lambda d: d.update(last_reviewed=(self.today + datetime.timedelta(days=2)).isoformat()),
            "impossible date": lambda d: d.update(last_reviewed="2026-02-30"),
            "sample without label": lambda d: d.update(sample=True, fictional=True),
            "three-letter country": lambda d: d["address"].update(country="USA"),
        }
        for name, mutate in cases.items():
            with self.subTest(case=name):
                broken = json.loads(json.dumps(good))
                mutate(broken)
                errors, _ = business_facts_report(broken, self.schema, self.today)
                self.assertTrue(errors, name)

    def test_repeated_keys_are_rejected_before_validation(self):
        with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
            json.loads('{"domain": "a.example", "domain": "b.example"}', object_pairs_hook=reject_duplicate_keys)

    def test_a_stale_review_is_a_warning_not_a_format_error(self):
        data = load_json(FACTS_FILES[0])
        later = datetime.date.fromisoformat(data["last_reviewed"]) + datetime.timedelta(days=FRESHNESS_DAYS + 1)
        errors, warnings = business_facts_report(data, self.schema, later)
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)


class ContextPackTests(unittest.TestCase):
    def answers(self, pack):
        return [(group, answer) for group in PACK_GROUPS for answer in pack["groups"][group]]

    def test_packs_use_the_six_connector_groups(self):
        for path in PACK_FILES:
            with self.subTest(path=path.name):
                self.assertEqual(list(load_json(path)["groups"]), PACK_GROUPS)

    def test_every_answer_has_a_source_review_date_and_expiry(self):
        for path in PACK_FILES:
            pack = load_json(path)
            ids = [answer["id"] for _, answer in self.answers(pack)]
            self.assertEqual(len(ids), len(set(ids)), path.name)
            for field in ("context_pack_version", "business", "domain", "owner", "facts_url", "rules", "facts", "policies"):
                self.assertTrue(pack.get(field), (path.name, field))
            for group, answer in self.answers(pack):
                with self.subTest(pack=path.name, answer=answer.get("id")):
                    self.assertTrue(answer["question"].strip().endswith("?"))
                    self.assertTrue(answer["answer"].strip())
                    self.assertTrue(answer["source_url"].startswith("https://"))
                    reviewed = datetime.date.fromisoformat(answer["reviewed"])
                    expires = datetime.date.fromisoformat(answer["expires"])
                    days = PRICING_EXPIRY_DAYS if group == "pricing" else OTHER_EXPIRY_DAYS
                    self.assertEqual((expires - reviewed).days, days)
            for row in pack["facts"]:
                self.assertTrue(row["source_url"].startswith("https://"))

    def test_broadcastwell_pack_answers_only_from_the_seven_public_pages(self):
        pack = load_json(PACK_FILES[0])
        answers = self.answers(pack)
        self.assertTrue(10 <= len(answers) <= 15)
        self.assertEqual({a["source_url"] for _, a in answers} - PACK_SOURCE_PAGES, set())
        self.assertNotIn("sample", pack)

    def test_kalvenor_pack_is_fictional_everywhere(self):
        pack = load_json(PACK_FILES[1])
        self.assertIs(pack["sample"], True)
        self.assertIs(pack["fictional"], True)
        self.assertTrue(pack["label"].startswith("SAMPLE DATA"))
        for _, answer in self.answers(pack):
            self.assertTrue(answer["answer"].startswith("SAMPLE DATA"))
            self.assertEqual(urlsplit(answer["source_url"]).hostname, "kalvenor.example")


class CopyRuleTests(unittest.TestCase):
    def test_no_banned_string_dash_or_exclamation_in_any_new_public_file(self):
        for name, text in new_public_texts().items():
            with self.subTest(file=name):
                self.assertEqual(banned_hits(text), [])

    def test_any_mention_of_five_engines_names_all_five(self):
        units = {name: text for name, text in new_public_texts().items() if "context-pack/" not in name}
        for path in PACK_FILES:
            for answers in load_json(path)["groups"].values():
                for answer in answers:
                    units[path.name + " " + answer["id"]] = answer["answer"]
        for name, text in units.items():
            with self.subTest(unit=name):
                if re.search(r"(?i)\bfive[- ]engines?\b", text):
                    self.assertIn(FIVE_ENGINE_LIST, text)

    def test_reconciliation_sample_is_labeled_and_names_the_five_engines(self):
        with RECONCILIATION_CSV.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row["sample"], "SAMPLE DATA")
            self.assertEqual(row["company"], "Kalvenor (fictional)")
            self.assertEqual(row["month"], "2026-10")
            if row["record"] == "Receipts" and row["measure"] != "planned_answers":
                self.assertTrue(row["base"].isdigit(), row)
                self.assertLessEqual(int(row["value"]), int(row["base"]))
        engines = {row["engine"] for row in rows if row["record"] == "Receipts"}
        self.assertEqual(engines, set(FIVE_ENGINES))
        hub = [row for row in rows if row["record"] == "Hub"]
        self.assertTrue(hub and all("fictional" in row["note"].lower() for row in hub))


class PageStructureTests(unittest.TestCase):
    def test_each_page_has_one_question_dates_and_structured_data_inputs(self):
        for name in PAGES:
            with self.subTest(page=name):
                meta, body = split_page(HUB / name)
                self.assertTrue(meta["title"].endswith("?") and len(meta["title"]) < 60)
                self.assertEqual(meta["headline"], meta["title"])
                self.assertTrue(150 <= len(meta["description"]) <= 160)
                self.assertEqual(meta["page_class"], "page")
                self.assertIn(meta["schema_type"], {"Article", "TechArticle"})
                self.assertEqual(meta["date_published"], "2026-11-09T00:00:00+00:00")
                self.assertEqual(meta["date_modified"], "2026-11-09T00:00:00+00:00")
                self.assertEqual(meta["template"], "business-hub.html")
                self.assertEqual(re.findall(r"(?m)^# (.+)$", re.sub(r"(?ms)^```.*?^```", "", body)), [meta["title"]])
                self.assertIn("\n" + UPDATED_LINE + "\n", body)
                self.assertIn("## Sources", body)

    def test_each_page_links_the_other_four_and_the_explainer(self):
        for name in PAGES:
            _, body = split_page(HUB / name)
            for other in PAGES:
                if other != name:
                    with self.subTest(page=name, target=other):
                        self.assertIn("](%s" % other, body)

    def test_explainer_carries_the_shared_check_anchors_and_required_sections(self):
        meta, body = split_page(HUB / "index.md")
        for anchor in READINESS_ANCHORS:
            self.assertEqual(len(re.findall(r"(?m)^### .+ \{#" + re.escape(anchor) + r"\}$", body)), 1, anchor)
        first_words = " ".join(body.split("\n# ", 1)[-1].split("\n", 1)[1].split()[:60])
        self.assertIn("You cannot claim your business in ChatGPT yet.", first_words)
        for phrase in ("ChatGPT Business Hub", "ChatGPT Search Console", "ChatGPT webmaster tools",
                       "how to get your business listed in ChatGPT", "claim your business in ChatGPT"):
            self.assertIn(phrase.lower(), body.lower())
        self.assertEqual(body.count("not ChatGPT Business, which is OpenAI's subscription plan"), 1)
        for link in ("https://broadcastwell.com/fix-sprint", "https://broadcastwell.com/pricing",
                     "https://broadcastwell.com/methodology",
                     "https://app.broadcastwell.com/tools/chatgpt-business-hub-readiness"):
            self.assertIn("(" + link + ")", body)
        self.assertEqual(body.count("| Expected |"), 2)

    def test_faq_has_five_to_seven_questions_shown_on_the_page(self):
        meta, body = split_page(HUB / "index.md")
        self.assertTrue(5 <= len(meta["faq"]) <= 7)
        visible = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", body)
        for item in meta["faq"]:
            self.assertIn("### " + item["question"] + "\n\n" + item["answer"] + "\n", visible)

    def test_client_block_is_exact_and_sits_directly_after_the_offer_section(self):
        _, body = split_page(HUB / "index.md")
        self.assertNotIn("CLIENT-ENROLMENT-BLOCK", body)
        block = client_block(body)
        self.assertEqual(hashlib.sha256(block.encode("utf-8")).hexdigest(), CLIENT_BLOCK_SHA256)
        self.assertEqual(body.count(CLIENT_BLOCK_ANCHOR), 1)
        lines = body.splitlines()
        at = lines.index(CLIENT_BLOCK_ANCHOR)
        before = [line for line in lines[:at] if line.strip()]
        self.assertTrue(before[-1].startswith("Parts 1 to 4 are included in the [Fix Sprint]"))
        self.assertEqual(lines[at - 1], "")
        offer_heading = max(i for i, line in enumerate(lines[:at]) if line.startswith("## "))
        self.assertTrue(lines[offer_heading].startswith("## What our ChatGPT Business Hub Readiness work includes"))
        self.assertTrue(body[body.index(block) + len(block):].startswith(chr(10) + CLIENT_BLOCK_NEXT_HEADING))

    def test_guides_stay_outside_the_navigation_but_reach_llms_and_two_existing_pages(self):
        # Navigation is shared by the 45 registered field-study pages, so it must not change.
        root_nav = yaml.safe_load((DOCS / ".pages").read_text(encoding="utf-8"))["nav"]
        self.assertNotIn("chatgpt-business-hub", root_nav)
        self.assertFalse((HUB / ".pages").exists())
        self.assertNotIn("chatgpt-business-hub", (ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        llms = (DOCS / "llms.txt").read_text(encoding="utf-8")
        for name in PAGES:
            route = "" if name == "index.md" else name[:-3] + "/"
            self.assertEqual(llms.count("](%schatgpt-business-hub/%s)" % (SITE, route)), 1, name)
        self.assertIn("](%sbusiness-facts.json)" % SITE, llms)
        for page in ("why-does-chatgpt-not-mention-us.md", "vendor-facts.md"):
            self.assertIn("](chatgpt-business-hub/index.md)", (DOCS / page).read_text(encoding="utf-8"))


class PriceBlockTests(unittest.TestCase):
    def test_price_block_names_the_readiness_parts_in_each_offer(self):
        lines = (DOCS / "llms.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines.count("## Current prices and terms (9 November 2026)"), 1)
        rows = {prefix: [line for line in lines if line.startswith(prefix)] for prefix in ("- Fix Sprint: ", "- Care: ", "- Program: ")}
        self.assertTrue(all(len(found) == 1 for found in rows.values()))
        self.assertTrue(rows["- Fix Sprint: "][0].endswith(
            " Includes ChatGPT Business Hub readiness parts 1 to 4: " + SITE + "chatgpt-business-hub/ https://broadcastwell.com/answer-repair"))
        for prefix in ("- Care: ", "- Program: "):
            self.assertTrue(rows[prefix][0].endswith(
                " Includes ChatGPT Business Hub readiness parts 1 to 6, with the claim on the first day OpenAI opens the tool to the client."))


class SitemapAdditionTests(unittest.TestCase):
    XML = chr(10).join(['<?xml version="1.0"?>', '<urlset>', '    <url>',
                        '         <loc>https://docs.broadcastwell.com/</loc>', '    </url>', '</urlset>', '']).encode()
    CLOSING = ("</urlset>" + chr(10)).encode()

    def setUp(self):
        import sys, tempfile
        sys.path.insert(0, str(ROOT / "tools"))
        from library_followup_release import add_reviewed_sitemap_rows
        self.add = add_reviewed_sitemap_rows
        self.tmp = tempfile.TemporaryDirectory()
        self.site = Path(self.tmp.name)
        (self.site / "chatgpt-business-hub").mkdir()
        (self.site / "chatgpt-business-hub" / "index.html").write_text("page", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_reviewed_page_is_appended_and_existing_rows_keep_their_bytes(self):
        row = {"url": SITE + "chatgpt-business-hub/", "lastmod": "2026-11-08"}
        xml = self.add(self.XML, [row], self.site)
        self.assertTrue(xml.startswith(self.XML[:-len(self.CLOSING)]))
        self.assertTrue(xml.endswith(self.CLOSING))
        self.assertEqual(xml.count(b"<loc>" + row["url"].encode() + b"</loc>"), 1)
        self.assertIn(b"<lastmod>2026-11-08</lastmod>", xml)
        self.assertEqual(self.add(self.XML, [], self.site), self.XML)

    def test_unreviewed_shapes_are_rejected(self):
        bad = [
            {"url": SITE, "lastmod": "2026-11-08"},
            {"url": SITE + "chatgpt-business-hub/", "lastmod": "8 November 2026"},
            {"url": "https://example.com/chatgpt-business-hub/", "lastmod": "2026-11-08"},
            {"url": SITE + "missing-page/", "lastmod": "2026-11-08"},
        ]
        for row in bad:
            with self.subTest(row=row), self.assertRaises(ValueError):
                self.add(self.XML, [row], self.site)
        with self.assertRaisesRegex(ValueError, "already present"):
            row = {"url": SITE + "chatgpt-business-hub/", "lastmod": "2026-11-08"}
            self.add(self.add(self.XML, [row], self.site), [row], self.site)


class NearDuplicateTests(unittest.TestCase):
    def test_no_guide_shares_more_than_a_fifth_of_its_six_word_sequences(self):
        worst = near_duplicate_rows()[0]
        self.assertLessEqual(worst[0], NEAR_DUPLICATE_LIMIT, worst)



class ClientReadinessTests(unittest.TestCase):
    """STEP 3.2 client sentence and rarity sentence; STEP 3.3 removes the status table under the sentence."""

    def setUp(self):
        self.text = (HUB / "index.md").read_text(encoding="utf-8")
        self.meta, self.body = split_page(HUB / "index.md")
        self.block = client_block(self.body)

    def test_client_sentence_is_exact_once_and_nothing_follows_it_in_the_block(self):
        self.assertEqual(self.body.count(CLIENT_SENTENCE), 1)
        self.assertEqual(self.block, CLIENT_BLOCK_ANCHOR + chr(10) + CLIENT_SENTENCE + chr(10))
        self.assertNotIn("readiness work is prepared", self.text)

    def test_rarity_sentence_is_exact_once_inside_the_readiness_offer_section(self):
        self.assertEqual(self.body.count(RARITY_SENTENCE), 1)
        offer = self.body.index("## What our ChatGPT Business Hub Readiness work includes")
        self.assertTrue(offer < self.body.index(RARITY_SENTENCE) < self.body.index(CLIENT_BLOCK_ANCHOR))
        self.assertIn(chr(10) * 2 + RARITY_SENTENCE + chr(10) * 2, self.body)
        for claim in ("first in", "number one", "the only", "only company", "leading"):
            self.assertNotIn(claim, RARITY_SENTENCE.lower())

    def test_no_hub_page_or_facts_file_carries_the_word_transitioned(self):
        for path in [HUB / name for name in PAGES] + FACTS_FILES + [ROOT / "overrides" / "followup.html"]:
            with self.subTest(file=path.name):
                self.assertNotIn("transitioned", path.read_text(encoding="utf-8").lower())

    def test_the_status_table_and_its_pending_cells_are_gone_from_every_hub_page(self):
        for path in [HUB / name for name in PAGES] + FACTS_FILES + [ROOT / "docs" / "llms.txt"]:
            text = path.read_text(encoding="utf-8")
            with self.subTest(file=path.name):
                self.assertNotIn(REMOVED_TABLE_HEADER, text)
                for word in REMOVED_STATUS_WORDS:
                    self.assertNotIn(word, text)
        for client in ("Vantaa Tax", "Neurvalis", "Valren Atelier"):
            self.assertEqual(self.body.count(client), 1, client)

    def test_the_block_holds_only_the_anchor_and_the_sentence(self):
        lines = [line for line in self.block.splitlines() if line.strip()]
        self.assertEqual(lines, [CLIENT_BLOCK_ANCHOR, CLIENT_SENTENCE])
        self.assertNotIn("| ", self.block)


class OrganizationSameAsTests(unittest.TestCase):
    """The followup template (and business-hub, which extends it) swaps the registered pages' shared
    sameAs for the seven current profiles; main.html and the shared footer keep their reviewed bytes."""

    def setUp(self):
        self.followup = (ROOT / "overrides" / "followup.html").read_text(encoding="utf-8")
        self.main = (ROOT / "overrides" / "main.html").read_text(encoding="utf-8")
        self.footer = (ROOT / "overrides" / "partials" / "site-footer.html").read_text(encoding="utf-8")

    def shared_same_as(self):
        return json.loads(re.search(r"\{% set org_same_as = (\[.*?\]) %\}", self.main, re.S).group(1))

    def test_followup_template_replaces_the_shared_list_with_the_seven_profiles_in_order(self):
        old = '"sameAs": ' + json.dumps(self.shared_same_as())
        new = '"sameAs": ' + json.dumps(SAME_AS)
        self.assertIn("{{ super() | replace('" + old + "', '" + new + "') }}", self.followup)
        self.assertEqual(len(set(SAME_AS)), 7)

    def test_registered_shared_templates_keep_their_reviewed_bytes(self):
        catalog = json.loads((ROOT / "tools" / "library_owner_repair_surface_templates.json").read_text(encoding="utf-8"))
        for path in ("overrides/main.html", "overrides/partials/site-footer.html"):
            with self.subTest(template=path):
                digest = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
                self.assertIn(digest, catalog["repository_templates"][path]["accepted_actual_raw_sha256"])

    def test_footer_adds_x_and_tiktok_beside_linkedin_and_writing(self):
        old = ('<li><a href="https://www.linkedin.com/company/broadcastwell">LinkedIn</a></li>'
               '<li><a href="https://broadcastwell.substack.com/">Writing</a></li>')
        new = ('<li><a href="https://www.linkedin.com/company/broadcastwell">LinkedIn</a></li>'
               '<li><a href="https://x.com/broadcastwellhq">X</a></li>'
               '<li><a href="https://broadcastwell.substack.com/">Writing</a></li>'
               '<li><a href="https://www.tiktok.com/@broadcastwell.com">TikTok</a></li>')
        self.assertEqual(self.footer.count(old), 1)
        self.assertIn("{% block footer %}{{ super() | replace('" + old + "', '" + new + "') }}{% endblock %}",
                      self.followup)

    def test_both_business_facts_files_list_the_seven_profiles(self):
        self.assertEqual(load_json(FACTS_FILES[0])["same_as"], SAME_AS)
        _, body = split_page(HUB / "business-facts-file.md")
        example = json.loads(re.search(r"```json\n(\{.*?\})\n```", body, re.S).group(1))
        self.assertEqual(example["same_as"], SAME_AS)


if __name__ == "__main__":
    unittest.main()
