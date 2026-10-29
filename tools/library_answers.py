"""Shared validation helpers for the evidence-backed answer library."""

import html
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import urlsplit, unquote

import yaml

SITE_URL = "https://docs.broadcastwell.com/"
BUY_ENTRY = "https://broadcastwell.com/answer-repair"
LIMIT_SENTENCE = "No email is needed; runs are limited per network and per day, and by the site's daily allowance."
CLUSTER_OWNERS = {
    "geo-basics": "Priya Nair, Management Consultant",
    "buying": "Priya Nair, Management Consultant",
    "chatgpt": "Vikram Patel, AI Architect",
    "claude": "Vikram Patel, AI Architect",
    "perplexity": "Vikram Patel, AI Architect",
    "google-ai": "Vikram Patel, AI Architect",
    "measurement": "Vikram Patel, AI Architect",
    "agents": "Vikram Patel, AI Architect",
    "industries": "Ananya Rao, AI Engineer",
    "fixes": "Rohan Iyer, AI Engineer",
    "changes": "Marcus Reed, AI Specialist",
}
DEMAND_SOURCES = {
    "gsc-query", "gsc-assistant-prompt", "google-autocomplete",
    "people-also-ask", "reddit", "atp", "index-question", "manual-faq",
}
SECTION_NAMES = (
    "What we measured", "What this means for you", "Also asked as", "Related", "Next step",
)
BANNED_PROSE = re.compile(
    r"\u2014|--|\b(?:delve|tapestry|landscape|unlock|leverage|robust|seamless|"
    r"cutting-edge|game-changer|navigate|crucial|elevate|founding|founder-led|"
    r"paused|waitlist|boutique|solo)\b|in today's|it's worth noting|dive into|"
    r"at the end of the day|four[ -]engines?|free audit|early-stage|"
    r"\$(?:990|1,500|3,000|4,500|2,900|13,500)\b|"
    r"\bgpt-\d|\bclaude[- ](?:sonnet|opus|haiku)|\bgemini[- ]\d|"
    r"\bworkflow[_ -]?(?:id|\d+)",
    re.I,
)
FALSE_OWNERSHIP = re.compile(
    r"(?:Broadcastwell['’]s founder|Sairam(?: Sivakumar)?)\b.{0,100}"
    r"(?:previously owned|owned and sold|related[ -]party).{0,160}"
    r"(?:Neurvalis|Valren Atelier)|"
    r"(?:Neurvalis|Valren Atelier).{0,120}related[ -]party.{0,100}"
    r"(?:Broadcastwell|Sairam)", re.I,
)

# Exact approved records. This is a source allowlist, not a general URL escape.
SEPTEMBER_INDEX_DOI = "https://doi.org/10.5281/zenodo.22907695"
GSC_SUMMARY_URL = "https://docs.broadcastwell.com/assets/library/search-console-2026-10-27-summary.json"
GSC_SUMMARY_PATH = "assets/library/search-console-2026-10-27-summary.json"
DEFAULT_METHOD_LABEL = "Every figure comes from the published method, v1.1."
SCOPED_METHOD_LABEL = "Our answer-study method, v1.1."
GSC_SCOPE_SENTENCE = "Query wording does not identify who wrote it or what an AI engine answered."
APPROVED_STUDY_DOIS = {
    "https://doi.org/10.5281/zenodo.22907695",  # September Index, including mixed-source pages
    "https://doi.org/10.5281/zenodo.22721962",  # August Index
    "https://doi.org/10.5281/zenodo.21537014",  # State of GEO Volume I
    "https://doi.org/10.5281/zenodo.21586091",  # Volume II
    "https://doi.org/10.5281/zenodo.21789120",  # Volume III
    "https://doi.org/10.5281/zenodo.23202939",  # Head to Head
    "https://doi.org/10.5281/zenodo.23270124",  # Wrong About You
    "https://doi.org/10.5281/zenodo.23271935",  # The AI Written RFP
    "https://doi.org/10.5281/zenodo.23197560",  # Agent Gap
    "https://doi.org/10.5281/zenodo.23586713",  # PHP2Shell Answer Study
}
APPROVED_METHOD_RECEIPTS = APPROVED_STUDY_DOIS | {
    "https://docs.broadcastwell.com/assets/research/change-desk/2026-10-26/method.txt",
}
GSC_EXPECTED_SUMMARY = {'schema_version': '1.0', 'title': 'Search Console query-length summary, exported 27 October 2026', 'publisher': 'Broadcastwell', 'source': 'Google Search Console', 'observation_window': {'start': '2026-07-26', 'end': '2026-10-25', 'days': 92}, 'export_date': '2026-10-27', 'source_query_rows': 1000, 'filter': {'minimum_whitespace_words': 12}, 'matching_distinct_queries': 134, 'matching_impressions': 969, 'matching_query_table_clicks': 0, 'source_export_sha256': 'aa7b9e6b49a24724ca03099deb95279c909102c4b02bac0d111e9dba4f1edf94', 'source_queries_csv_sha256': '62db3c33c29a183e23d2394f97e6d6990c365f7bf66c555e657790255e51afa2', 'definitions': {'impressions_and_clicks': 'https://support.google.com/webmasters/answer/7042828', 'google_ai_features': 'https://developers.google.com/search/docs/appearance/ai-features'}, 'scope': 'Query length does not identify who wrote a query or what an AI engine answered. These are query-table figures, not isolated AI-feature results.'}


def split_markdown(text):
    match = re.match(r"\A\ufeff?---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not match:
        return {}, text
    return yaml.safe_load(match.group(1)) or {}, text[match.end():]


def normalized_question(value):
    value = unicodedata.normalize("NFKC", str(value)).casefold()
    return re.sub(r"\s+", " ", value).strip().rstrip("?.!")


def plain_text(value):
    value = re.sub(r"(?m)^\s*\|[-|\s:]+\|\s*$", " ", value)
    value = re.sub(r"(?is)<(?:script|style)\b.*?</(?:script|style)>", " ", value)
    value = re.sub(r"(?s)<[^>]+>", " ", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    return " ".join(html.unescape(value).split())


def ownership_violations(text):
    text = plain_text(text)
    return [m.group(0) for m in FALSE_OWNERSHIP.finditer(text)]


def page_url(relative):
    path = Path(relative).as_posix()
    if path.endswith(".md"):
        path = path[:-3]
    if path == "index":
        path = ""
    elif path.endswith("/index"):
        path = path[:-5]
    else:
        path += "/"
    return SITE_URL + path


def built_relative(relative):
    path = Path(relative).as_posix()
    if path == "index.md" or path.endswith("/index.md"):
        return path[:-3] + ".html"
    return path[:-3] + "/index.html"


def leaf_answers(docs):
    folder = Path(docs) / "answers"
    return sorted(path for path in folder.rglob("*.md") if path.name != "index.md")


def markdown_links(body):
    links = re.findall(r"!?\[[^\]]*\]\(<?([^\s)>]+)>?(?:\s+[^)]*)?\)", body)
    links += re.findall(r"\bhref=[\"']([^\"']+)[\"']", body, re.I)
    return links


def resolve_local_link(href, source, docs):
    """Return a source/static target for a same-site link, or None if external."""
    docs, source = Path(docs).resolve(), Path(source).resolve()
    parsed = urlsplit(href)
    if parsed.scheme and parsed.netloc != "docs.broadcastwell.com":
        return None
    raw = unquote(parsed.path)
    if not raw:
        return source
    if parsed.netloc or raw.startswith("/"):
        target = docs / raw.lstrip("/")
    else:
        target = source.parent / raw
    target = target.resolve()
    if not target.is_relative_to(docs):
        return target
    if target.suffix:
        return target
    if target.is_file():
        return target
    direct = target.with_suffix(".md")
    return direct if direct.exists() else target / "index.md"


def external_evidence_links(body):
    result = set()
    for href in markdown_links(body):
        parsed = urlsplit(href)
        if parsed.scheme == "https" and (
            parsed.netloc == "index.broadcastwell.com"
            or (parsed.netloc == "broadcastwell.com" and parsed.path.startswith("/research/"))
        ):
            result.add(href.split("#", 1)[0])
    return result


def paragraph_after_heading(body):
    content = re.sub(r"\A\s*# [^\n]+\n", "", body, count=1).lstrip()
    return re.split(r"\n\s*\n", content, maxsplit=1)[0]



def _reject_duplicate_json_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def validate_source_evidence(meta, body, docs):
    """Bind a source to its own method without relaxing any page/build rule."""
    errors = []
    kind = meta.get("evidence_kind", "")
    source = str(meta.get("is_based_on", ""))
    start = body.find("## What we measured")
    end = body.find("## What this means for you")
    measured = body[start:end] if 0 <= start < end else ""
    method_label = DEFAULT_METHOD_LABEL
    if not kind:
        if source != SEPTEMBER_INDEX_DOI:
            errors.append("non-September sources require approved published-study metadata")
    elif kind == "published-study":
        method_label = SCOPED_METHOD_LABEL
        if source not in APPROVED_STUDY_DOIS:
            errors.append("published-study source is outside the approved DOI allowlist")
        receipts = meta.get("evidence_method_receipts")
        if not isinstance(receipts, list) or not receipts or any(not isinstance(value, str) for value in receipts):
            errors.append("published-study requires a list of evidence_method_receipts")
            receipts = []
        if source not in receipts:
            errors.append("study method receipts must include the primary source DOI")
        if len(set(receipts)) != len(receipts):
            errors.append("study method receipts must be unique")
        for receipt in receipts:
            if receipt not in APPROVED_METHOD_RECEIPTS:
                errors.append("unapproved study method receipt: " + receipt)
            if receipt not in markdown_links(measured):
                errors.append("study method receipt must be linked in What we measured: " + receipt)
        if not re.search(r"\b(?:method|protocol|study design|record rules)\b", plain_text(measured), re.I):
            errors.append("What we measured must describe the study-specific method")
        if DEFAULT_METHOD_LABEL in body:
            errors.append("published-study must not use the universal v1.1 method sentence")
    elif kind == "search-console-export":
        method_label = SCOPED_METHOD_LABEL
        if source != GSC_SUMMARY_URL:
            errors.append("Search Console source must be the exact approved aggregate URL")
        path = Path(docs) / GSC_SUMMARY_PATH
        try:
            summary = json.loads(path.read_text(encoding="utf8"), object_pairs_hook=_reject_duplicate_json_keys)
            if json.dumps(summary, sort_keys=True) != json.dumps(GSC_EXPECTED_SUMMARY, sort_keys=True):
                errors.append("Search Console summary differs from approved counts, dates, filter, base or source hashes")
        except (OSError, ValueError) as exc:
            errors.append("Search Console aggregate cannot be verified: " + str(exc))
        text = plain_text(measured)
        required_numbers = {
            "134 distinct queries": r"\b134\b",
            "969 impressions": r"\b969\s+impressions\b",
            "zero query-table clicks": r"\b(?:0|zero)\s+(?:query[ -]table\s+)?clicks\b",
            "1000-row source base": r"\b1,?000\s+(?:source\s+)?quer(?:y|ies)(?:[ -]rows)?\b",
            "92-day window": r"\b92(?:[ -]day|\s+days)\b",
            "26 July to25October2026 window": r"\b26\s+July(?:\s+2026)?\s+(?:to|through)\s+25\s+October\s+2026\b",
            "27 October2026 export": r"\b27\s+October\s+2026\b",
            "12-word whitespace filter": r"\bat least\s+(?:12|twelve)\s+whitespace-separated\s+words\b",
        }
        for label, pattern in required_numbers.items():
            if not re.search(pattern, text, re.I):
                errors.append("Search Console evidence is missing " + label)
        first = plain_text(paragraph_after_heading(body))
        if not all(re.search(r"\b" + value + r"\b", first) for value in ("134", "969")):
            errors.append("first Search Console paragraph must include its134-query and969-impression figures")
        for link in (GSC_SUMMARY_URL, *GSC_EXPECTED_SUMMARY["definitions"].values()):
            if link not in markdown_links(measured):
                errors.append("Search Console definitions/source must be linked in What we measured: " + link)
        if GSC_SCOPE_SENTENCE not in measured:
            errors.append("Search Console evidence must state its query-authorship/answer scope limit")
        if DEFAULT_METHOD_LABEL in body:
            errors.append("Search Console figures must not use the universal v1.1 method sentence")
    else:
        errors.append("unknown evidence_kind")
    if f"[{method_label}](https://broadcastwell.com/methodology)" not in body:
        errors.append("method label must link to the published answer-study method")
    return errors, method_label


def validate_answer(path, docs):
    path, docs = Path(path), Path(docs)
    meta, body = split_markdown(path.read_text(encoding="utf8"))
    errors = []
    rel = path.relative_to(docs).as_posix()
    for key in ("title", "headline", "description", "date_published", "date_modified",
                "library_cluster", "library_owner", "demand_source", "demand_evidence",
                "is_based_on"):
        if not meta.get(key):
            errors.append("missing " + key)
    if meta.get("page_class") != "page" or meta.get("schema_type") != "Article":
        errors.append("answer must be a page with Article schema")
    cluster = meta.get("library_cluster")
    if cluster not in CLUSTER_OWNERS or meta.get("library_owner") != CLUSTER_OWNERS.get(cluster):
        errors.append("cluster owner does not match the approved roster")
    if len(path.relative_to(docs).parts) != 3 or path.parent.name != cluster:
        errors.append("answer must use answers/<cluster>/<slug>.md")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", path.stem) or len(path.stem) > 70:
        errors.append("slug must be lowercase ASCII with hyphens, at most 70 characters")
    if meta.get("demand_source") not in DEMAND_SOURCES:
        errors.append("unknown demand_source")
    if len(str(meta.get("description", ""))) >= 160:
        errors.append("description must be under 160 characters")
    if "navigation" not in meta.get("hide", []) or "toc" in meta.get("hide", []):
        errors.append("hide navigation and keep the table of contents")
    for key in ("date_published", "date_modified"):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\+\d{2}:\d{2}|Z)", str(meta.get(key, ""))):
            errors.append(key + " requires a full timestamp with timezone")
    source_errors, method_label = validate_source_evidence(meta, body, docs)
    errors.extend(source_errors)
    headings = re.findall(r"(?m)^# (.+)$", body)
    if headings != [str(meta.get("headline", ""))]:
        errors.append("exactly one H1 must match headline")
    paragraph = paragraph_after_heading(body)
    if not re.search(r"\d", plain_text(paragraph)):
        errors.append("first answer paragraph must carry a measured figure")
    sentence_count = len(re.findall(r"[.!?](?:\s|$)", plain_text(paragraph)))
    if sentence_count not in range(2, 6):
        errors.append("first answer paragraph must contain two to five sentences")
    positions = [body.find("## " + heading) for heading in SECTION_NAMES]
    if any(pos < 0 for pos in positions) or positions != sorted(positions):
        errors.append("required sections missing or out of order")
    if len(re.findall(r"\b[\w$]+\b", plain_text(body))) not in range(350, 901):
        errors.append("body must contain 350 to 900 words")
    for required in ("Measured", LIMIT_SENTENCE, "Prepared by the Broadcastwell team.",
                     "Free 10-question check (one engine)", "Fix one answer, $490",
                     method_label,
                     "Page owner: " + str(meta.get("library_owner", "")) + ". Corrections: hello@broadcastwell.com"):
        if required not in body:
            errors.append("missing " + required)
    if BANNED_PROSE.search(plain_text(body)):
        errors.append("banned prose")
    if ownership_violations(body):
        errors.append("false ownership claim")
    if body.count("Gemini") and (body.count("Gemini") > 1 or "Google AI Overviews and Google AI Mode, which most buyers call Gemini" not in body):
        errors.append("Gemini may appear only once in the approved phrase")
    next_step = body[positions[-1]:] if positions[-1] >= 0 else ""
    if next_step.find("https://audit.broadcastwell.com/") < 0 or next_step.find(BUY_ENTRY) < next_step.find("https://audit.broadcastwell.com/"):
        errors.append("Next step must put the free check before Answer Repair")
    if positions[3] >= 0 and positions[4] >= 0:
        related_links = markdown_links(body[positions[3]:positions[4]])
        if len(related_links) not in range(3, 7):
            errors.append("Related requires three to six links")
    synonyms = meta.get("also_asked_as", [])
    if isinstance(synonyms, str):
        synonyms = [term.strip() for term in synonyms.split("|") if term.strip()]
    synonym_section = body[positions[2]:positions[3]] if positions[2] >= 0 and positions[3] >= 0 else ""
    for synonym in synonyms:
        if str(synonym) not in synonym_section:
            errors.append("folded synonym missing from Also asked as: " + str(synonym))
    for href in markdown_links(body):
        parsed = urlsplit(href)
        if parsed.netloc == "buy.stripe.com" or (parsed.netloc == "broadcastwell.com" and parsed.path.startswith("/buy/")):
            errors.append("purchase links must use " + BUY_ENTRY)
        target = resolve_local_link(href, path, docs)
        if target is not None and not target.exists():
            errors.append("broken internal link: " + href)
        elif target is not None and parsed.fragment and target.suffix == ".md":
            import markdown
            _, target_body = split_markdown(target.read_text(encoding="utf8"))
            rendered = markdown.markdown(target_body, extensions=["toc", "attr_list", "md_in_html"])
            if not re.search(r'\bid=["\']' + re.escape(unquote(parsed.fragment)) + r'["\']', rendered):
                errors.append("broken internal anchor: " + href)
    if "/vendors/" in body and "Claiming or correcting a vendor record is free and never depends on a purchase." not in body:
        errors.append("vendor record requires the free correction sentence")
    standard_evidence = re.search(r"https://(?:index\.broadcastwell\.com/|broadcastwell\.com/research/|doi\.org/10\.)", body)
    approved_gsc_evidence = (
        meta.get("evidence_kind") == "search-console-export"
        and meta.get("is_based_on") == GSC_SUMMARY_URL
        and GSC_SUMMARY_URL in markdown_links(body)
    )
    if not (standard_evidence or approved_gsc_evidence):
        errors.append("missing published evidence link")
    return [rel + ": " + error for error in errors]


def validate_collection(docs):
    docs = Path(docs)
    errors, titles = [], {}
    answers = leaf_answers(docs)
    for path in sorted(docs.rglob("*.md")):
        meta, body = split_markdown(path.read_text(encoding="utf8"))
        if ownership_violations(body):
            errors.append(path.relative_to(docs).as_posix() + ": false ownership claim")
        if path.name == "index.md" and path.is_relative_to(docs / "answers"):
            rel = path.relative_to(docs).as_posix()
            if not meta.get("library_hub"):
                errors.append(rel + ": answer hub requires library_hub metadata")
            owner = meta.get("library_owner")
            if owner not in CLUSTER_OWNERS.values():
                errors.append(rel + ": answer hub owner is missing or outside the approved roster")
            if "Prepared by the Broadcastwell team." not in body:
                errors.append(rel + ": answer hub is missing its team byline")
            if "Page owner: " + str(owner) + ". Corrections: hello@broadcastwell.com" not in body:
                errors.append(rel + ": answer hub is missing its owner and corrections line")
            if meta.get("page_class") != "page" or meta.get("schema_type") != "Article":
                errors.append(rel + ": answer hub must be a page with Article schema")
        title = normalized_question(meta.get("title", ""))
        if title:
            titles.setdefault(title, []).append(path)
    for path in answers:
        errors.extend(validate_answer(path, docs))
        meta, _ = split_markdown(path.read_text(encoding="utf8"))
        if len(titles.get(normalized_question(meta.get("title", "")), [])) > 1:
            errors.append(path.relative_to(docs).as_posix() + ": duplicate title")
        synonyms = meta.get("also_asked_as", [])
        if isinstance(synonyms, str):
            synonyms = [term.strip() for term in synonyms.split("|") if term.strip()]
        for synonym in synonyms:
            if any(other != path for other in titles.get(normalized_question(synonym), [])):
                errors.append(path.relative_to(docs).as_posix() + ": folded synonym is another page title: " + synonym)
    return errors
