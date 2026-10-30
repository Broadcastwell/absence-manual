"""Shared validation helpers for the evidence-backed answer library."""

import html
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import urlsplit, unquote

import yaml

try:
    from tools.library_list_audit import (LIST_AUDIT_SOURCE, LIST_AUDIT_METHOD_URL,
        LIST_AUDIT_METHOD_LABEL, LIST_AUDIT_RECEIPT_URL, validate_list_audit)
except ModuleNotFoundError:
    from library_list_audit import (LIST_AUDIT_SOURCE, LIST_AUDIT_METHOD_URL,
        LIST_AUDIT_METHOD_LABEL, LIST_AUDIT_RECEIPT_URL, validate_list_audit)

try:
    from tools.library_documentation_review import (DOC_REVIEW_SOURCE, DOC_REVIEW_METHOD_URL,
        DOC_REVIEW_METHOD_LABEL, DOC_REVIEW_RECEIPT_URL, validate_documentation_review)
except ModuleNotFoundError:
    from library_documentation_review import (DOC_REVIEW_SOURCE, DOC_REVIEW_METHOD_URL,
        DOC_REVIEW_METHOD_LABEL, DOC_REVIEW_RECEIPT_URL, validate_documentation_review)

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
AUDIT_METHOD_LABEL = "Our published agency-audit criteria."
AUDIT_CRITERIA = (
    "Method", "Open data", "Engines", "Price", "Refund", "B2B cases",
    "Reviews", "Machine readable",
)
# These are publication-record observations, not answer-engine experiments.
# Snapshot hashes bind the exact saved HTML; a later source needs a fresh review.
APPROVED_PUBLICATION_AUDITS = {
    "https://broadcastwell.com/best-geo-agencies": {
        "observed_at": "2026-10-29T14:37:02.799269+00:00",
        "snapshot_sha256": "4c2722c06bb8308bc8900e85d18599cfdd2a1ee870261152455a1ccbfe47af54",
        "records": {
            "go-fish-digital": {"name": "Go Fish Digital", "statuses": ("Partial", "No", "Yes", "No", "No", "Yes", "Yes", "No")},
            "minuttia": {"name": "Minuttia", "statuses": ("Partial", "No", "Yes", "Partial", "No", "Yes", "Yes", "Partial")},
            "first-page-sage": {"name": "First Page Sage", "statuses": ("Partial", "No", "Yes", "No", "No", "Yes", "No", "No")},
            "omniscient": {"name": "Omniscient Digital", "statuses": ("Partial", "No", "Yes", "Partial", "No", "Yes", "Yes", "Partial")},
            "optimist": {"name": "Optimist", "statuses": ("Partial", "No", "Yes", "Partial", "No", "Yes", "Not verified", "Partial")},
            "relevance": {"name": "Relevance", "statuses": ("Partial", "No", "Yes", "No", "No", "Yes", "Not verified", "Partial")},
            "single-grain": {"name": "Single Grain", "statuses": ("Partial", "No", "Yes", "No", "No", "Yes", "Yes", "Partial")},
            "skale": {"name": "Skale", "statuses": ("Partial", "No", "Yes", "Partial", "No", "Yes", "Not verified", "Partial")},
            "webfx": {"name": "WebFX", "statuses": ("Partial", "No", "Yes", "Partial", "No", "Yes", "Not verified", "Yes")},
        },
        "dates": ("15 September 2026", "16 September 2026", "28 October 2026"),
        "date_context": "Prices, refund terms and engine lists were read again on 28 October 2026; other cells retain their earlier dates.",
    },
    "https://broadcastwell.com/best-geo-agencies-for-startups": {
        "observed_at": "2026-10-29T14:37:02.864788+00:00",
        "snapshot_sha256": "0e9c684aa54488edcbd6518e6205ea51ff3de58a6addb6b22dde027e15e47fa6",
        "records": {
            "citant": {"name": "Citant", "statuses": ("Yes", "Yes", "Yes", "Partial", "Yes", "No", "Not verified", "No")},
            "embarque": {"name": "Embarque", "statuses": ("Partial", "No", "Yes", "Partial", "Yes", "Yes", "Yes", "Partial")},
        },
        "dates": ("15 September 2026", "16 September 2026"),
        "date_context": "Other cells retain their original dates.",
    },
}
# Named review-status updates in the same pinned main audit snapshot.
PUBLICATION_AUDIT_REVIEW_STATUS_UPDATES = {
    "https://broadcastwell.com/best-geo-agencies": {
        "optimist": ("29 September 2026", "Not verified"),
        "relevance": ("29 September 2026", "Not verified"),
        "skale": ("29 September 2026", "Not verified"),
        "webfx": ("29 September 2026", "Not verified"),
    },
}
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
            or href.split("#", 1)[0] in APPROVED_PUBLICATION_AUDITS
            or href.split("#", 1)[0] == LIST_AUDIT_SOURCE
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


def _audit_table_rows(measured):
    """Read only the explicit eight-criterion Markdown score table."""
    header = ("Agency", *AUDIT_CRITERIA, "Yes count")
    rows, active = [], False
    for line in measured.splitlines():
        if not line.strip().startswith("|"):
            if active:
                break
            continue
        cells = tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
        if not active:
            active = tuple(cell.casefold() for cell in cells) == tuple(cell.casefold() for cell in header)
        elif all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        else:
            rows.append(cells)
    return rows


def _audit_unsupported_claims(body):
    """Keep this source kind confined to dated publication checks."""
    errors = []
    before_next, separator, next_step = body.partition("## Next step")
    # Only the existing fixed Answer Repair CTA is a monetary exception.
    if separator:
        next_step = next_step.replace(
            "[Fix one answer, $490](https://broadcastwell.com/answer-repair)", "", 1,
        )
    # Section names such as "What this means for you" are navigation labels,
    # not assertions about a nearby result. Keep them out of claim parsing.
    claim_text = plain_text(re.sub(r"(?m)^#{1,6}[^\n]*$", "", before_next + "\n" + next_step))
    if re.search(r"(?:[$\u00a3\u20ac]\s*\d|\b(?:USD|GBP|EUR)\s*\d|\b\d[\d,.]*\s*(?:dollars|pounds|euros)\b)", claim_text, re.I):
        errors.append("publication-audit does not support monetary price claims; only the fixed Next step CTA is allowed")
    names = "|".join(re.escape(record["name"]) for audit in APPROVED_PUBLICATION_AUDITS.values() for record in audit["records"].values())
    if re.search(r"\b(?:" + names + r")\b[^.!?]{0,45}\b(?:charges?|costs?|currently prices?|starts? at|is free)\b", claim_text, re.I):
        errors.append("publication-audit does not support a provider's current pricing claim")
    # Negated limitations are welcome. Inspect each affirmative outcome verb,
    # rather than banning a whole sentence just for mentioning client results.
    for clause in re.split(r"[.!?;]|\bbut\b|\bhowever\b", claim_text, flags=re.I):
        if not re.search(r"\b(?:results?|quality|traffic|conversions?|rankings?|recommendations?|best|winner|value for money|cheapest|cheaper|lowest price)\b", clause, re.I):
            continue
        if not re.search(r"\b(?:scores?|scorecards?|counts?|audits?|yeses|" + names + r")\b", clause, re.I):
            continue
        for match in re.finditer(r"\b(?:prove[sd]?|show[sn]?|measures?|means?|demonstrates?|predicts?|guarantees?|delivers?|achieves?|increases?|improves?|outperforms?|wins?|ranks?|makes?|confirms?|establishes?|indicates?|reflects?|is the best|is cheapest|is cheaper|has the lowest price)\b", clause, re.I):
            prefix = clause[max(0, match.start() - 80):match.start()]
            suffix = clause[match.end():]
            negated = re.search(r"\b(?:not|never|cannot|can't|doesn't|don't|isn't|aren't)\b(?!\s+only\b)[^,;]*$|\bno (?:publication )?(?:score|count|audit|evidence)\b[^,;]*$", prefix, re.I)
            no_evidence = re.match(r"\s+no evidence\b", suffix, re.I)
            if not (negated or no_evidence):
                errors.append("publication-audit cannot claim service quality, current AI outcomes, client results or a ranking")
                break
    return errors


def _audit_prose(measured):
    """Keep authored prose separate from headings and the fixed source table."""
    prose = "\n".join(line for line in measured.splitlines()
                      if not line.lstrip().startswith(("|", "#")))
    paragraphs = [plain_text(part) for part in re.split(r"\n\s*\n", prose) if plain_text(part)]
    units = [unit.strip() for paragraph in paragraphs
             for unit in re.split(r"[.!?;]\s*", paragraph) if unit.strip()]
    return paragraphs, units


def _audit_negates(text, concept):
    """Recognize a bounded negated assertion, without accepting 'not only'."""
    negative = r"\b(?:not(?!\s+only\b)|no|never|cannot|can't|doesn't|don't|isn't|aren't|wasn't|weren't|without|rather than|instead of)\b"
    return bool(re.search(negative + r"[^.!?;]{0,150}\b(?:" + concept + r")\b", text, re.I))


def _audit_scope_and_dates(source, selected, measured):
    """Check visible assertions, not a reusable paragraph of fixed wording."""
    errors = []
    paragraphs, units = _audit_prose(measured)
    text = " ".join(paragraphs)
    publication = any(
        re.search(r"\b(?:published|publication|publicly (?:available|checkable))\b", unit, re.I)
        and re.search(r"\b(?:counts?|counted|scores?|read|checks?|audit|documents?|material|evidence|records?|criteria|cells?)\b", unit, re.I)
        and not _audit_negates(unit, r"published (?:evidence|material|records?)|publication (?:evidence|check|audit)")
        for unit in units
    )
    if not publication:
        errors.append("published-audit must identify its scope as a read/check of published evidence")
    test_concept = r"retest(?:ing|ed|s)?|(?:new|fresh|live) (?:provider |agency |performance )?(?:test|tests|measurement)|(?:provider|agency) (?:test|tests|testing)"
    outcome_concept = r"results?|outcomes?|performance|quality|recommendations?|proof of (?:client |AI )?results"
    if not any(_audit_negates(paragraph, test_concept) and _audit_negates(paragraph, outcome_concept)
               for paragraph in paragraphs):
        errors.append("published-audit needs a plain limitation: no new provider test and no proof of results")
    if not re.search(r"\balphabetical(?:ly)?\b|\bA\s+(?:to|-)\s*Z\b", text, re.I):
        errors.append("published-audit must disclose alphabetical ordering")
    if not any(_audit_negates(unit, r"rank(?:ing|ings|ed)?|order of merit|merit") for unit in units):
        errors.append("published-audit must disclose that its order is not a ranking")
    publisher_unscored = any(
        re.search(r"\b(?:Broadcastwell|publisher)\b", unit, re.I)
        and (re.search(r"\bunscored\b|\b(?:outside|excluded from|not part of) the (?:scorecard|scoring|scores?)\b", unit, re.I)
             or _audit_negates(unit, r"scored|rated|assessed"))
        for unit in units
    )
    if not publisher_unscored:
        errors.append("published-audit must disclose that Broadcastwell/the publisher is not scored")
    yes_only = any(
        re.search(r"\bonly (?:the )?Yes\b|\bYes(?: (?:cells|responses|entries))? (?:alone|only)\b", unit, re.I)
        and re.search(r"\b(?:counts?|total(?:led|ed|s)?|scores?|scoring|contribut(?:e|es|ed)|adds?|form)\b", unit, re.I)
        for unit in units
    )
    if not yes_only:
        errors.append("published-audit must explain that Yes alone contributes to its count")
    for unit in units:
        if _audit_negates(unit, r"published (?:evidence|material|records?)|publication (?:evidence|check|audit)"):
            errors.append("published-audit cannot deny its publication-evidence scope")
        publisher_score = re.search(r"\b(?:Broadcastwell|publisher)\b.{0,40}\b(?:scored|rated|assessed|included in (?:the )?(?:scoring|scorecard))\b", unit, re.I)
        if publisher_score and not _audit_negates(unit, r"scored|rated|assessed|included in (?:the )?(?:scoring|scorecard)"):
            errors.append("published-audit cannot claim that Broadcastwell/the publisher is scored")
        positive_rank = re.search(r"\brank(?:ed|ing|ings|s)?\b|\border of merit\b|\bbest to worst\b", unit, re.I)
        if positive_rank and not _audit_negates(unit, r"rank(?:ed|ing|ings|s)?|order of merit|best to worst"):
            errors.append("published-audit cannot claim that the scorecard ranks agencies")
        if re.search(r"\b(?:Partial|Not verified|No cells?)\b[^.!?]{0,35}\b(?:also count|counts? toward|contribut(?:e|es) to|adds? one|worth one)\b", unit, re.I):
            if not _audit_negates(unit, r"counts? toward|contribut(?:e|es) to|adds? one|worth one"):
                errors.append("published-audit cannot count Partial, No or Not verified as Yes")
        positive_retest = re.search(r"\b(?:retest(?:ed|ing)? (?:the )?(?:providers|agencies)|(?:providers|agencies) (?:were |are )?retested|(?:new|fresh|live) (?:provider|agency|performance) tests?)\b", unit, re.I)
        if positive_retest and not _audit_negates(unit, test_concept):
            errors.append("published-audit cannot describe the snapshot as a new provider test")

    # Each required historical read is attached to the field it describes.
    # A date merely listed elsewhere on the page does not satisfy this check.
    roles = {
        "snapshot": r"snapshot|saved (?:source|audit|page)|source (?:read|page|HTML)",
        "original": r"original(?:ly)?|initial|first|company[ -]sites?|sites? (?:were )?(?:read|checked)",
        "reviews": r"reviews?|ratings?",
        "method": r"method",
        "open_data": r"open data|data cells?",
        "price": r"prices?|pricing",
        "refund": r"refunds?(?: terms)?",
        "engine": r"engines?(?: lists?)?",
    }
    def has_date(role, date, extra=None):
        return any(date in unit and re.search(r"\b(?:" + roles[role] + r")\b", unit, re.I)
                   and (extra is None or re.search(extra, unit, re.I)) for unit in units)
    required = [("snapshot", "29 October 2026", None),
                ("original", "15 September 2026", None),
                ("reviews", "16 September 2026", None)]
    if source.endswith("/best-geo-agencies"):
        required += [(role, "28 October 2026", None) for role in ("price", "refund", "engine")]
    if "citant" in selected:
        required += [(role, "23 October 2026", r"\bCitant\b") for role in ("method", "open_data")]
        required += [("reviews", "29 September 2026", r"\bCitant\b.*\bNot verified\b|\bNot verified\b.*\bCitant\b")]
    review_updates = PUBLICATION_AUDIT_REVIEW_STATUS_UPDATES.get(source, {})
    for record_id in selected:
        if record_id in review_updates:
            date, status = review_updates[record_id]
            name = re.escape(APPROVED_PUBLICATION_AUDITS[source]["records"][record_id]["name"])
            context = r"\b" + name + r"\b.*\b" + re.escape(status) + r"\b|\b" + re.escape(status) + r"\b.*\b" + name + r"\b"
            required.append(("reviews", date, context))
    for role, date, extra in required:
        if not has_date(role, date, extra):
            errors.append("published-audit field/read date missing or misattributed: " + role + " = " + date)

    allowed = {
        "snapshot": {"29 October 2026"}, "original": {"15 September 2026"},
        "reviews": {"16 September 2026"}, "method": {"15 September 2026"},
        "open_data": {"15 September 2026"}, "price": {"15 September 2026"},
        "refund": {"15 September 2026"}, "engine": {"15 September 2026"},
    }
    if source.endswith("/best-geo-agencies"):
        for role in ("price", "refund", "engine"):
            allowed[role].add("28 October 2026")
    for unit in units:
        dates = list(re.finditer(r"\b\d{1,2} (?:September|October) 2026\b", unit))
        positions = [(match.start(), role) for role, pattern in roles.items()
                     for match in re.finditer(r"\b(?:" + pattern + r")\b", unit, re.I)]
        for date in dates:
            if not positions:
                continue
            _, role = min(positions, key=lambda item: abs(item[0] - date.start()))
            valid_dates = set(allowed[role])
            if re.search(r"\bCitant\b", unit, re.I):
                if role in ("method", "open_data"):
                    valid_dates.add("23 October 2026")
                if role == "reviews":
                    valid_dates.add("29 September 2026")
            if role == "reviews":
                for record_id in selected:
                    if record_id in review_updates:
                        update_date, status = review_updates[record_id]
                        name = re.escape(APPROVED_PUBLICATION_AUDITS[source]["records"][record_id]["name"])
                        if re.search(r"\b" + name + r"\b", unit, re.I) and re.search(r"\b" + re.escape(status) + r"\b", unit, re.I):
                            valid_dates.add(update_date)
                            # This date records a verification-status update,
                            # not another read of a review platform. Remove the
                            # status phrase before checking negation so its
                            # word Not cannot negate an affirmative reread.
                            assertion = re.sub(r"\bNot verified\b", "unverified", unit, flags=re.I)
                            read_concept = r"re[- ]?read|re[- ]?checked|fresh(?:ly)? (?:read|checked|reviewed)|read|reviewed|checked"
                            if update_date in unit and re.search(r"\b(?:" + read_concept + r")\b", assertion, re.I) and not _audit_negates(assertion, read_concept):
                                errors.append("published-audit review-status update is not evidence of a fresh review read: " + record_id)
            if date.group() not in valid_dates:
                errors.append("published-audit contradicts the approved field/read dates: " + role + " = " + date.group())
    return errors


def validate_publication_audit(meta, body, measured):
    """Validate exactly the approved publication snapshots and record cuts."""
    errors = []
    source = str(meta.get("is_based_on", ""))
    audit = APPROVED_PUBLICATION_AUDITS.get(source)
    if audit is None:
        return ["published-audit source is outside the two approved audit URLs"]
    for key, expected in (("evidence_audit_observed_at", audit["observed_at"]),
                          ("evidence_audit_snapshot_sha256", audit["snapshot_sha256"])):
        if str(meta.get(key, "")) != expected:
            errors.append("published-audit requires the exact approved " + key)
    selected = meta.get("evidence_audit_records")
    if not isinstance(selected, list) or not selected or any(not isinstance(item, str) for item in selected):
        errors.append("published-audit requires a nonempty evidence_audit_records list")
        selected = []
    if len(set(selected)) != len(selected):
        errors.append("published-audit record IDs must be unique")
    if any(item not in audit["records"] for item in selected):
        errors.append("published-audit record is not approved for this source")
    selected = [item for item in selected if item in audit["records"]]
    if meta.get("evidence_method_receipts"):
        errors.append("published-audit uses its own scorecard, not answer-study method receipts")
    errors.extend(_audit_scope_and_dates(source, selected, measured))
    rows = _audit_table_rows(measured)
    expected_rows = []
    for record_id in sorted(selected, key=lambda item: audit["records"][item]["name"].casefold()):
        record = audit["records"][record_id]
        count = record["statuses"].count("Yes")
        expected_rows.append((record["name"], *record["statuses"], str(count) + "/8"))
        link = source + "#" + record_id
        if link not in markdown_links(measured):
            errors.append("published-audit record must link to its exact source anchor: " + link)
    actual_rows = [tuple(plain_text(cell) for cell in row) for row in rows]
    if actual_rows != expected_rows or not expected_rows:
        errors.append("published-audit table must match the exact approved alphabetical records, eight statuses and Yes counts")
    first = plain_text(paragraph_after_heading(body))
    selected_counts = {audit["records"][item]["statuses"].count("Yes") for item in selected}
    pairs = re.findall(r"\b(\d+)\s*(?:/|of|out of)\s*(\d+)\b", plain_text(body), re.I)
    if any(int(base) != 8 or int(count) not in selected_counts for count, base in pairs):
        errors.append("published-audit count/base differs from its approved record")
    opening_receipt = False
    for record_id in selected:
        record = audit["records"][record_id]
        count = record["statuses"].count("Yes")
        name = re.escape(record["name"])
        claims = re.findall(name + r"[^.!?\n|]{0,140}?\b(\d+)\s*(?:/|of|out of)\s*(\d+)\b", plain_text(body), re.I)
        if any((int(value), int(base)) != (count, 8) for value, base in claims):
            errors.append("published-audit score is attributed to the wrong record: " + record["name"])
        if re.search(name + r"[^.!?]{0,140}?\b" + str(count) + r"\s*(?:/|of|out of)\s*8\b", first, re.I) and source + "#" + record_id in markdown_links(paragraph_after_heading(body)):
            opening_receipt = True
    if not opening_receipt:
        errors.append("first publication-audit paragraph must name an approved record, give its score/base and link its source anchor")
    if DEFAULT_METHOD_LABEL in body or SCOPED_METHOD_LABEL in body:
        errors.append("published-audit must not use an answer-study or universal v1.1 method label")
    errors.extend(_audit_unsupported_claims(body))
    return errors


def validate_source_evidence(meta, body, docs):
    """Bind a source to its own method without relaxing any page/build rule."""
    errors = []
    kind = meta.get("evidence_kind", "")
    source = str(meta.get("is_based_on", ""))
    start = body.find("## What we measured")
    end = body.find("## What this means for you")
    measured = body[start:end] if 0 <= start < end else ""
    method_label = DEFAULT_METHOD_LABEL
    method_url = "https://broadcastwell.com/methodology"
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
    elif kind == "published-audit":
        method_label = AUDIT_METHOD_LABEL
        method_url = source + "#scorecard"
        errors.extend(validate_publication_audit(meta, body, measured))
        if method_url not in markdown_links(measured):
            errors.append("publication-audit criteria must be linked in What we measured")
    elif kind == "published-list-audit":
        method_label = LIST_AUDIT_METHOD_LABEL
        method_url = LIST_AUDIT_METHOD_URL
        errors.extend(validate_list_audit(meta, body, measured, docs,
            plain_text=plain_text, markdown_links=markdown_links,
            paragraph_after_heading=paragraph_after_heading,
            audit_prose=_audit_prose, audit_negates=_audit_negates,
            unsupported_claims=_audit_unsupported_claims))
    elif kind == "published-documentation-review":
        method_label = DOC_REVIEW_METHOD_LABEL
        method_url = DOC_REVIEW_METHOD_URL
        errors.extend(validate_documentation_review(meta, body, measured, docs,
            plain_text=plain_text, markdown_links=markdown_links,
            paragraph_after_heading=paragraph_after_heading))
    else:
        errors.append("unknown evidence_kind")
    if f"[{method_label}]({method_url})" not in body:
        errors.append("method label must link to the publication-audit scorecard" if kind == "published-audit" else "method label must link to the list-audit criteria" if kind == "published-list-audit" else "method label must link to the dated documentation review" if kind == "published-documentation-review" else "method label must link to the published answer-study method")
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
    approved_audit_evidence = (
        meta.get("evidence_kind") == "published-audit"
        and str(meta.get("is_based_on", "")) in APPROVED_PUBLICATION_AUDITS
        and str(meta.get("is_based_on")) + "#scorecard" in markdown_links(body)
    )
    approved_list_audit_evidence = (
        meta.get("evidence_kind") == "published-list-audit"
        and meta.get("is_based_on") == LIST_AUDIT_SOURCE
        and LIST_AUDIT_METHOD_URL in markdown_links(body)
        and LIST_AUDIT_RECEIPT_URL in markdown_links(body)
    )
    approved_documentation_evidence = (
        meta.get("evidence_kind") == "published-documentation-review"
        and meta.get("is_based_on") == DOC_REVIEW_SOURCE
        and DOC_REVIEW_SOURCE in markdown_links(body)
        and DOC_REVIEW_RECEIPT_URL in markdown_links(body)
    )
    if not (standard_evidence or approved_gsc_evidence or approved_audit_evidence or approved_list_audit_evidence or approved_documentation_evidence):
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
