"""One pinned publication-list audit; no engine or service-quality benchmark."""
import hashlib
import json
from pathlib import Path
import re

LIST_AUDIT_SOURCE = "https://broadcastwell.com/best-geo-agencies-lists-audited"
LIST_AUDIT_METHOD_URL = LIST_AUDIT_SOURCE + "#how-scored"
LIST_AUDIT_METHOD_LABEL = "Our published agency-list audit criteria."
LIST_AUDIT_RECEIPT_PATH = "assets/library/agency-list-audit-2026-09-17.json"
LIST_AUDIT_RECEIPT_URL = "https://docs.broadcastwell.com/" + LIST_AUDIT_RECEIPT_PATH
LIST_AUDIT_HTML_SHA256 = "8de93b046f9c782eaa18d5c0852886590356a47400d2e19ef2780371a7c1d9f9"
LIST_AUDIT_FIELD_DATE = "2026-09-17"
LIST_AUDIT_CANONICAL_SHA256 = "065fe507a5bd3cc2decadb5653bf003474cf26e6573dcc67b3678e5ca5dd8bf7"


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate list-audit receipt key")
        result[key] = value
    return result


def _immediately_negated(prefix):
    """Negate this predicate, never an unrelated earlier adjective."""
    return bool(re.search(
        r"\b(?:(?:do|does|did|is|are|was|were|has|have)\s+not|cannot|can't|never|not)\s*$",
        prefix, re.I,
    ))


def _publisher_unscored(unit):
    return bool(
        re.search(r"\b(?:Broadcastwell|publisher)\b", unit, re.I)
        and re.search(
            r"\b(?:not|never)\s+(?:scored|included in (?:the )?scoring)\b|"
            r"\bunscored\b|\boutside (?:its|the) scored table\b|"
            r"\bexcluded from (?:the )?(?:scorecard|scoring)\b",
            unit, re.I,
        )
    )


def validate_list_audit(meta, body, measured, docs, *, plain_text,
                        markdown_links, paragraph_after_heading,
                        audit_prose, audit_negates, unsupported_claims):
    errors = []
    if meta.get("is_based_on") != LIST_AUDIT_SOURCE:
        errors.append("list-audit source must be the exact approved 32-list URL")
    for key, expected in (
        ("evidence_list_audit_snapshot_sha256", LIST_AUDIT_HTML_SHA256),
        ("evidence_list_audit_receipt_sha256", LIST_AUDIT_CANONICAL_SHA256),
        ("evidence_list_audit_field_date", LIST_AUDIT_FIELD_DATE),
    ):
        if meta.get(key) != expected:
            errors.append("list-audit requires the exact approved " + key)
    if any(key.startswith("evidence_audit_") for key in meta) or meta.get("evidence_method_receipts"):
        errors.append("list-audit cannot use eight-cell audit or answer-study metadata")
    receipt = None
    try:
        receipt = json.loads((Path(docs) / LIST_AUDIT_RECEIPT_PATH).read_text(encoding="utf-8-sig"), object_pairs_hook=_unique)
        canonical = json.dumps(receipt, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf8")
        if hashlib.sha256(canonical).hexdigest() != LIST_AUDIT_CANONICAL_SHA256:
            errors.append("list-audit public receipt differs from the exact approved 32 rows, statuses, dates or method")
        records = receipt.get("records", [])
        states = [r["in_own_list"] for r in records]
        if len(records) != 32 or states.count("Yes") != 29 or states.count("No") != 2 or states.count("Parent company listed") != 1:
            errors.append("list-audit public receipt must preserve 29 Yes, 2 No and 1 Parent company listed across 32 pages")
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        errors.append("list-audit public receipt cannot be verified: " + str(error))
    links = markdown_links(measured)
    for link in (LIST_AUDIT_SOURCE, LIST_AUDIT_METHOD_URL, LIST_AUDIT_RECEIPT_URL):
        if link not in links:
            errors.append("list-audit source, criteria and public receipt must be linked in What we measured: " + link)
    first = plain_text(paragraph_after_heading(body))
    if not re.search(r"\b29\s*(?:/|of|out of)\s*32\b", first) or "17 September 2026" not in first or LIST_AUDIT_SOURCE not in markdown_links(paragraph_after_heading(body)):
        errors.append("first list-audit paragraph must carry the dated 29/32 figure and exact source link")
    text = plain_text(measured)
    if not re.search(r"\b(?:29|twenty[ -]nine)\s+Yes\b", text, re.I) or not re.search(r"\b(?:2|two)\s+No\b", text, re.I) or not re.search(r"\b(?:1|one|a separate)\s+Parent company listed\b", text, re.I):
        errors.append("list-audit visible summary must keep Yes, No and Parent company listed distinct")
    if not re.search(r"\b(?:each list page once|once per (?:list )?page|each (?:list )?page is counted once)\b", text, re.I):
        errors.append("list-audit method must count pages once, not unique publishers")
    for concept in (r"disclos", r"criteria", r"sources?", r"dates?", r"prices?", r"corrections?"):
        if not re.search(concept, text, re.I):
            errors.append("list-audit must describe all six publication criteria")
            break
    paragraphs, units = audit_prose(measured)
    _, all_units = audit_prose(body)
    if not any(_publisher_unscored(unit) for unit in units):
        errors.append("list-audit must disclose that Broadcastwell/the publisher is outside scoring")
    if not any(audit_negates(paragraph, r"(?:agency |service )?quality|client results?|outcomes?|performance") for paragraph in paragraphs):
        errors.append("list-audit must limit its evidence to publication, not service quality or outcomes")
    for unit in all_units:
        if re.search(r"\b(?:Broadcastwell|publisher)\b", unit, re.I) and re.search(r"\b(?:is|are|was|were|will be|and)\s+(?:also\s+)?(?:scored|included in (?:the )?scoring)\b", unit, re.I):
            errors.append("list-audit cannot score its publisher")
        if re.search(r"\b(?:audit|list(?:s| pages)?)\b.{0,90}\b(?:read|checked|retested)\b.{0,50}\b(\d{1,2} (?:September|October) 2026)\b", unit, re.I):
            for date in re.findall(r"\b\d{1,2} (?:September|October) 2026\b", unit):
                if date != "17 September 2026":
                    errors.append("list-audit cannot replace the 17 September field date with a later source read")
        if re.search(r"\bParent company listed\b", unit, re.I):
            for predicate in re.finditer(r"\b(?:counts? as Yes|became Yes|is Yes|converted to Yes)\b", unit, re.I):
                if not _immediately_negated(unit[:predicate.start()]):
                    errors.append("list-audit cannot convert Parent company listed to Yes")
                    break
        if re.search(r"\b(?:each|every) publisher\b.{0,30}\bcounted once\b", unit, re.I):
            errors.append("list-audit cannot collapse multiple list pages from one publisher")
        test_concept = r"(?:new|fresh|live) (?:provider|agency|performance) tests?|retested (?:the )?(?:providers|agencies)|(?:providers|agencies) (?:were )?retested"
        if re.search(r"\b(?:" + test_concept + r")\b", unit, re.I) and not audit_negates(unit, test_concept):
            errors.append("list-audit is a publication check, not a new provider test")
    for count, base in re.findall(r"\b(\d+)\s*(?:/|of|out of)\s*(\d+)\b", plain_text(body), re.I):
        if (int(count), int(base)) not in {(29, 32), (2, 32), (1, 32)}:
            errors.append("list-audit body uses a count/base outside the approved self-inclusion cuts")
    if any(label in body for label in ("Every figure comes from the published method, v1.1.", "Our answer-study method, v1.1.", "Our published agency-audit criteria.")):
        errors.append("list-audit cannot use a study or eight-cell agency method label")
    errors.extend(unsupported_claims(body))
    # Extend provider-name assertions only for this source kind. Nothing in the
    # existing audit/source branches changes its name set or acceptance rules.
    if isinstance(receipt, dict) and isinstance(receipt.get("records"), list):
        names = "|".join(re.escape(r["publisher"]) for r in receipt["records"] if isinstance(r, dict) and isinstance(r.get("publisher"), str))
        prose = plain_text(body.split("## Next step")[0])
        if names and re.search(r"\b(?:" + names + r")\b[^.!?]{0,45}\b(?:charges?|costs?|currently prices?|starts? at|is free)\b", prose, re.I):
            errors.append("list-audit cannot support a provider pricing claim")
        if names:
            named_claims = re.sub(r"\b(?:" + names + r")\b", "audit", body, flags=re.I)
            errors.extend(unsupported_claims(named_claims))
    return errors
