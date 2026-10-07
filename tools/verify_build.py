"""Structural checks on the built site.

Run after `mkdocs build`. Fails the build if the manual stops being ungated,
crawlable or extractable without JavaScript. This runs in CI before every
deploy so a future edit cannot quietly reintroduce a form, drop a canonical
tag, ship an image with no alt text, or publish a thin chapter.

Pages are checked by class. Every page carries a `page_class` in its front
matter: chapter, note, appendix or page. Chapters must clear a word floor.
Every class carries every other check.
"""

import json
import pathlib
import subprocess
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DOCS = ROOT / "docs"

SITE_URL = "https://docs.broadcastwell.com/"
CHAPTER_WORD_FLOOR = 2500
ALT_TEXT_FLOOR = 40
OWNERSHIP_PROOF = "googlefda93e56a71f6d4d.html"

EM_DASH = "—"
EN_DASH = "–"
DOUBLE_HYPHEN = "-" + "-"
BANNED_DASH_ENTITIES = re.compile(r"&(mdash|ndash|#8211|#8212);", re.I)
APPROVED_PALETTE = {
    # Light theme values, still used by the PDF and by the light social card.
    "#111827", "#475569", "#64748B", "#94A3B8", "#BFDBFE",
    "#1D4ED8", "#3B82F6", "#EFF6FF", "#FFFFFF",
    # Dark theme values, the ones the marketing site serves.
    "#0A0A0B", "#0A0E1A", "#F8FAFC", "#CBD5E1",
    # Shared Broadcastwell design system 2.0 light surfaces and neutral ink.
    "#F7F9FC", "#EFF4FB", "#101828", "#475467", "#667085", "#D5DDE8", "#1E40AF",
}

# The only purchase address a page may carry, and the words that may no longer appear.
BUY_AUDIT = "https://broadcastwell.com/buy/audit"
RETIRED_OFFER_TEXT = [
    "currently on hold", "Check Audit availability", "Check Diagnostic availability",
    "working draft", "founding rate", "$89",
]

# Sairam's ruling of 5 October 2026, section 0. Every remaining offer is always buyable, the
# $990 AI Visibility Diagnostic is retired and the AI Fact Check is removed. None of the words
# below may reach a reader: page text, buttons, alt text, meta, JSON-LD, llms.txt, the search
# index, the learning downloads and the PDFs this site serves.
CREDIT_LINE = "The $490 credits once against the $2,900 Fix Sprint within 30 days of delivery, so the Sprint is $2,410."
AUDIT_PROMISE = "Findings within 48 hours of your category confirmation"
AVAILABILITY_WORDS = re.compile(
    r"(?i)\bpaused\b|\bpause\b|\bpilot\b|\bclosed\b|not currently offered|\bnot open\b|\breopens?\b"
    r"|\bis full\b|orders in total|\(\s*\d+\s+orders?\s*\)|\b\d+\s+orders\b|\bwaitlist\b"
    r"|\btemporarily\b|limited availability|\bnext batch\b|\bcapacity\b"
)
RETIRED_OFFERS = re.compile(
    r"(?i)\$990|ai fact check|/buy/diagnostic|/buy/ai-fact-check"
    r"|broadcastwell\.com/ai-fact-check|broadcastwell\.com/ai-visibility-audit"
)
# "Diagnostic" as something to buy. The lower-case word is the manual's own self-run method (the
# two-gate diagnostic of Chapter 2) and stays. History may describe past diagnostic work with no
# price, status or buy link; the published case study title is the one capitalised use allowed.
DIAGNOSTIC_OFFER = re.compile(r"\bDiagnostic\b")
DIAGNOSTIC_HISTORY = [
    "[Neurvalis AI Visibility Diagnostic | Broadcastwell](https://broadcastwell.com/neurvalis-ai-visibility-diagnostic):"
    " How Broadcastwell's AI Visibility Diagnostic gave Neurvalis",
]
# Dated research with a DOI is the record of what was observed on its date, other sellers' offer
# names included, so it is not rewritten. The theme's own scripts and styles carry no copy.
RULING_EXEMPT = ("assets/research/", "absence-ladder-volume-ii.pdf", "assets/javascripts/", "assets/stylesheets/")
SERVED_TEXT = {".html", ".txt", ".xml", ".json", ".js", ".css", ".svg", ".vtt", ".md"}


def ruling_hits(text):
    """Every banned word, retired offer and Diagnostic-for-sale in one served text."""
    text = " ".join(text.split())
    for allowed in DIAGNOSTIC_HISTORY:
        text = text.replace(allowed, " ")
    hits = []
    for rx in (AVAILABILITY_WORDS, RETIRED_OFFERS, DIAGNOSTIC_OFFER):
        for m in rx.finditer(text):
            hits.append(text[max(0, m.start() - 50):m.end() + 50])
    return hits

VALID_CLASSES = {"chapter", "note", "appendix", "page"}
TECHARTICLE_CLASSES = {"chapter", "appendix"}
ARTICLE_TYPES = {"TechArticle", "Article"}
WORD_FLOOR_CLASSES = {"chapter"}

ISO_STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\+\d{2}:\d{2}|Z)$")
FRONT_MATTER = re.compile(r"(?s)\A\s*\n?-{3}\n(.*?)\n-{3}\n")
TABLE_RULE = re.compile(r"(?m)^\|[-|\s:]+$")

problems = []


def fail(msg):
    problems.append(msg)


def front_matter(text):
    m = FRONT_MATTER.search(text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        k, v = line.split(":", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def strip_tags(html):
    body = re.sub(r"(?is)<script.*?</script>", " ", html)
    body = re.sub(r"(?is)<style.*?</style>", " ", body)
    return re.sub(r"(?is)<[^>]+>", " ", body)


def article_words(html):
    m = re.search(r"(?is)<article[^>]*>(.*?)</article>", html)
    if not m:
        return None
    return len(strip_tags(m.group(1)).split())


def built_path(md_rel):
    stem = md_rel[: -len(".md")]
    if stem == "index":
        return "index.html"
    return stem + "/index.html"


def expected_canonical(md_rel):
    stem = md_rel[: -len(".md")]
    if stem == "index":
        return SITE_URL
    return SITE_URL + stem + "/"


# ---------- site root artefacts ----------

robots = SITE / "robots.txt"
if not robots.exists():
    fail("robots.txt missing from the built site root")
else:
    body = robots.read_text(encoding="utf8")
    for agent in [
        "OAI-SearchBot",
        "PerplexityBot",
        "Claude-SearchBot",
        "Googlebot",
        "Google-Extended",
        "Applebot",
        "Bingbot",
    ]:
        if re.search(r"(?im)^User\-agent:\s*%s\s*$" % re.escape(agent), body) is None:
            fail("robots.txt does not name the crawler %s" % agent)
    if re.search(r"(?im)^Disallow:", body):
        fail("robots.txt contains a Disallow rule")
    if re.search(r"(?i)crawl\-delay", body):
        fail("robots.txt contains a crawl delay")
    if "Sitemap:" not in body:
        fail("robots.txt does not reference the sitemap")

sitemap = SITE / "sitemap.xml"
if not sitemap.exists():
    fail("sitemap.xml missing from the built site root")

cname = SITE / "CNAME"
if not cname.exists() or cname.read_text(encoding="utf8").strip() != "docs.broadcastwell.com":
    fail("CNAME missing or wrong in the built site root")

if not (DOCS / OWNERSHIP_PROOF).exists():
    fail("the search engine ownership proof %s is missing from docs" % OWNERSHIP_PROOF)
if not (SITE / OWNERSHIP_PROOF).exists():
    fail("the search engine ownership proof %s did not reach the built site" % OWNERSHIP_PROOF)


# ---------- the ungated PDF mirror ----------

STABLE_PDF = SITE / "absence-manual.pdf"
if not STABLE_PDF.exists():
    fail("the PDF mirror absence-manual.pdf is missing from the built site")
else:
    versioned = sorted(SITE.glob("absence-manual-v*.pdf"))
    if not versioned:
        fail("no versioned PDF alongside the stable absence-manual.pdf")
    if STABLE_PDF.stat().st_size < 200_000:
        fail("the PDF mirror is smaller than the manual can possibly be")
    newest_source = 0
    try:
        newest_source = int(
            subprocess.check_output(
                ["git", "log", "-1", "--format=%ct", "--", "docs"],
                cwd=str(ROOT), stderr=subprocess.DEVNULL,
            ).decode().strip() or 0
        )
    except Exception:
        newest_source = 0
    if newest_source and STABLE_PDF.stat().st_mtime < newest_source:
        fail(
            "the PDF mirror is older than the newest commit touching docs, so it has drifted "
            "from the HTML. Run tools/build_pdf.py after mkdocs build."
        )


# ---------- page manifest from front matter ----------

manifest = {}
for src in sorted(DOCS.rglob("*.md")):
    rel = src.relative_to(DOCS).as_posix()
    meta = front_matter(src.read_text(encoding="utf8"))
    cls = meta.get("page_class")
    if cls is None:
        fail("%s has no page_class in its front matter" % rel)
        continue
    if cls not in VALID_CLASSES:
        fail("%s has page_class %r, which is not one of %s" % (rel, cls, sorted(VALID_CLASSES)))
        continue
    for key in ("date_published", "date_modified"):
        stamp = meta.get(key, "")
        if not ISO_STAMP.match(stamp):
            fail("%s has %s %r, which is not a full ISO timestamp with a timezone" % (rel, key, stamp))
    if not meta.get("schema_type"):
        fail("%s has no schema_type in its front matter" % rel)
    elif cls in TECHARTICLE_CLASSES and meta["schema_type"] != "TechArticle":
        fail("%s is a %s and must be marked up as TechArticle, not %s" % (rel, cls, meta["schema_type"]))
    elif meta["schema_type"] not in ARTICLE_TYPES:
        fail("%s has schema_type %s, which is not an allowed article type" % (rel, meta["schema_type"]))
    manifest[rel] = cls


# ---------- prose hygiene on every markdown file ----------

for src in sorted(DOCS.rglob("*.md")):
    rel = src.relative_to(DOCS).as_posix()
    text = TABLE_RULE.sub("", FRONT_MATTER.sub("", src.read_text(encoding="utf8")))
    if EM_DASH in text:
        fail("%s contains an em dash in its prose" % rel)
    if EN_DASH in text:
        fail("%s contains an en dash in its prose" % rel)
    if BANNED_DASH_ENTITIES.search(text):
        fail("%s contains a banned dash entity in its prose" % rel)
    if DOUBLE_HYPHEN in text:
        fail("%s contains a double hyphen in its prose" % rel)


# ---------- shared palette source scan ----------

for asset in [
    DOCS / "assets" / "manual.css",
    DOCS / "assets" / "absence-manual-2026-08.svg",
    DOCS / "assets" / "absence-manual-2026-09.svg",
]:
    if not asset.exists():
        fail("shared visual asset %s is missing" % asset.relative_to(DOCS))
        continue
    colours = re.findall(r"#[0-9A-Fa-f]{6}", asset.read_text(encoding="utf8"))
    for colour in colours:
        if colour.upper() not in APPROVED_PALETTE:
            fail("%s uses colour %s outside the approved blue and neutral palette" % (asset.relative_to(DOCS), colour))


# ---------- the shared shell's own rules ----------

shell_css = (DOCS / "assets" / "manual.css").read_text(encoding="utf8")
for rule in [".bw-shell-pill {", ".bw-shell-menu summary {", ".bw-shell-menu-panel a {"]:
    at = shell_css.find(rule)
    if at < 0 or "min-height: 44px" not in shell_css[at:shell_css.find("}", at)]:
        fail("%s must clear 44 px" % rule)
if ".bw-shell-nav { display: none; }" not in shell_css:
    fail("the text links must collapse at phone widths")
if ".bw-shell-menu { display: block;" not in shell_css:
    fail("a disclosure must take their place at phone widths")
if re.search(r"\.bw-shell-pill \{ display: none", shell_css):
    fail("the pill must stay visible at phone widths")
if ".bw-shell-columns { grid-template-columns: 1fr;" not in shell_css:
    fail("the footer columns must stack below 640")
if re.search(r"text-transform:\s*uppercase", shell_css, re.I):
    fail("no label may be set in capitals")

# ---------- per page checks ----------

for rel, cls in sorted(manifest.items()):
    out = SITE / built_path(rel)
    if not out.exists():
        fail("%s did not build to %s" % (rel, built_path(rel)))
        continue
    html = out.read_text(encoding="utf8")

    for form in re.findall(r"(?is)<form\b[^>]*>", html):
        if re.search(r"(?is)\baction=", form):
            fail("%s contains a form that submits somewhere" % rel)
    if re.search(r"(?is)<input\b[^>]*type=[\"']?email", html):
        fail("%s contains an email input" % rel)
    if re.search(r"(?is)<input\b[^>]*(name|id)=[\"']?(email|newsletter|subscribe)", html):
        fail("%s contains a subscription input" % rel)
    if re.search(r"(?is)<input\b[^>]*type=[\"']?password", html):
        fail("%s contains a password input" % rel)
    for hook in ("data-paywall", 'class="paywall"', 'id="paywall"', "data-gated", 'class="signup'):
        if hook in html:
            fail("%s contains the gating hook %s" % (rel, hook))

    canon = re.findall(r'(?is)rel="canonical"\s+href="([^"]+)"', html)
    if len(canon) != 1:
        fail("%s has %d canonical tags, expected exactly 1" % (rel, len(canon)))
    elif canon[0] != expected_canonical(rel):
        fail("%s canonical is %s, expected %s" % (rel, canon[0], expected_canonical(rel)))

    heads = re.findall(r"(?is)<h1\b", html)
    if len(heads) != 1:
        fail("%s has %d h1 elements, expected exactly 1" % (rel, len(heads)))

    for img in re.findall(r"(?is)<img\b[^>]*>", html):
        m = re.search(r"(?is)alt=[\"'](.*?)[\"']", img)
        if m is None or len(m.group(1).strip()) < ALT_TEXT_FLOOR:
            fail("%s has an image whose alt text is missing or shorter than %d characters"
                 % (rel, ALT_TEXT_FLOOR))

    # The permalink anchor sits inside the heading it links to, so it has to stay out
    # of the accessible name, and an aria-hidden element must not be focusable.
    for link in re.findall(r'(?is)<a class="headerlink"[^>]*>', html):
        if 'aria-hidden="true"' not in link:
            fail("%s has a permalink anchor inside a heading with no aria-hidden" % rel)
        if 'tabindex="-1"' not in link:
            fail("%s has a permalink anchor that is hidden but still focusable" % rel)

    # The shell every Broadcastwell surface carries.
    head = html[html.find("<header"):html.find("</header>")]
    foot = html[html.rfind("<footer"):html.rfind("</footer>")]
    for needed in [
        'class="bw-wordmark" href="https://broadcastwell.com"',
        'href="https://broadcastwell.com/pricing">Pricing<',
        'href="https://app.broadcastwell.com/signin">Sign in<',
        'class="bw-shell-pill" href="%s" aria-label="Get the Category Audit, $490">' % BUY_AUDIT,
    ]:
        if needed not in head:
            fail("%s header is missing %s" % (rel, needed))
    for column in ("Product", "Research", "Company", "Contact"):
        if (">%s</h2>" % column) not in foot:
            fail("%s footer is missing the %s column" % (rel, column))
    if "Broadcastwell LLC. Indiana, USA. Copyright 2026." not in foot:
        fail("%s footer is missing the bottom bar" % rel)
    for slug in ("privacy", "terms", "cookies"):
        if ('href="https://broadcastwell.com/%s">' % slug) not in foot:
            fail("%s footer is missing the %s link" % (rel, slug))
    if foot.find("excluded from its own sample") > foot.find("bw-shell-columns"):
        fail("%s footer does not keep its own disclosure note above the shared columns" % rel)
    if chr(183) in html:
        fail("%s contains a middle dot" % rel)
    if "buy.stripe.com" in html:
        fail("%s links a checkout directly; every buy link goes through %s" % (rel, BUY_AUDIT))
    for anchor in re.findall(r'(?is)<a\b[^>]*href="mailto:[^"]*"[^>]*>(.*?)</a>', html):
        if re.search(r"(?i)\$\d|audit|diagnostic|availability|buy|order", strip_tags(anchor)):
            fail("%s has a mailto link used as a purchase control: %s" % (rel, strip_tags(anchor).strip()[:60]))
    for retired in RETIRED_OFFER_TEXT:
        if retired in strip_tags(html):
            fail("%s still says %r" % (rel, retired))
    if 'class="bw-next-step"' in html:
        at = html.find('class="bw-next-step"')
        block = html[at:html.find("</section>", at)]
        for needed in ('href="%s">Get the Category Audit, $490<' % BUY_AUDIT, CREDIT_LINE, AUDIT_PROMISE):
            if needed not in block:
                fail("%s next step block must carry %r" % (rel, needed))
        if "bw-paused" in block or "Diagnostic" in block:
            fail("%s next step block still shows a paused state or the retired Diagnostic" % rel)
    types = []
    for block in re.findall(r"(?is)<script type=\"application/ld\+json\">(.*?)</script>", html):
        try:
            parsed = json.loads(block)
        except Exception as exc:
            fail("%s has JSON-LD that does not parse: %s" % (rel, exc))
            continue
        types.append(parsed.get("@type"))
        for key in ("datePublished", "dateModified"):
            if key in parsed and not ISO_STAMP.match(str(parsed[key])):
                fail("%s emits %s as %r, which is not a full ISO timestamp with a timezone"
                     % (rel, key, parsed[key]))
    if cls in TECHARTICLE_CLASSES and "TechArticle" not in types:
        fail("%s is a %s but emits no TechArticle block" % (rel, cls))
    if not (set(types) & ARTICLE_TYPES):
        fail("%s emits no article level JSON-LD block" % rel)

    if cls in WORD_FLOOR_CLASSES:
        words = article_words(html)
        if words is None:
            fail("%s has no article element to measure" % rel)
        elif words < CHAPTER_WORD_FLOOR:
            fail("%s is a chapter and renders only %d article words, floor is %d"
                 % (rel, words, CHAPTER_WORD_FLOOR))


# ---------- llms.txt: the dated price block and no direct checkout ----------

llms = SITE / "llms.txt"
if not llms.exists():
    fail("llms.txt missing from the built site root")
else:
    body = llms.read_text(encoding="utf8")
    if "## Current prices and terms (" not in body:
        fail("llms.txt has no dated Current prices and terms block")
    if "buy.stripe.com" in body:
        fail("llms.txt links a checkout directly")
    if BUY_AUDIT not in body:
        fail("llms.txt does not give %s" % BUY_AUDIT)
    for retired in RETIRED_OFFER_TEXT:
        if retired in body:
            fail("llms.txt still says %r" % retired)
    if CREDIT_LINE not in body:
        fail("llms.txt does not carry the credit line exactly as ruled on 5 October 2026")
    if AUDIT_PROMISE not in body:
        fail("llms.txt does not carry the Category Audit promise %r" % AUDIT_PROMISE)
    for required in (
        "Category Exclusive: included with the Fix Sprint and the program at no extra charge.",
        "The Category Audit, white-label reports and every Index service stay open to everyone.",
        "Availability check: https://app.broadcastwell.com/exclusive",
        "Index Verified: free for every checked vendor on the Absence Index:",
        "No payment changes any Index number. https://index.broadcastwell.com/verified/",
        "[Index Verified and Category Exclusive | Broadcastwell](https://broadcastwell.com/index-verified)",
    ):
        if required not in body:
            fail("llms.txt is missing the verified offer rule %r" % required)

home = SITE / "index.html"
if home.exists():
    home_html = home.read_text(encoding="utf8")
    for needed in (CREDIT_LINE, AUDIT_PROMISE, 'href="%s"' % BUY_AUDIT):
        if needed not in home_html:
            fail("the front page offer section does not carry %r" % needed)


# ---------- section 0 of the 5 October 2026 ruling, on everything served ----------

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None
    fail("pypdf is needed to read the served PDFs; install requirements.txt")


def pdf_text(path):
    if PdfReader is None:
        return ""
    return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)


ruling_files = 0
for served in sorted(SITE.rglob("*")):
    if not served.is_file():
        continue
    rel = served.relative_to(SITE).as_posix()
    if rel.startswith(RULING_EXEMPT):
        continue
    suffix = served.suffix.lower()
    if suffix == ".pdf":
        text = pdf_text(served)
    elif suffix in SERVED_TEXT:
        text = served.read_text(encoding="utf8", errors="replace")
    else:
        continue
    ruling_files += 1
    for hit in ruling_hits(text):
        fail("%s breaks the 5 October 2026 ruling: ...%s..." % (rel, hit))
if ruling_files == 0:
    fail("the ruling scan read no served files")


# Agent Ready is separate from the engine measurement method and published research.
facts = SITE / "vendor-facts" / "index.html"
if not facts.exists():
    fail("Vendor Facts File standard missing from the built site")
else:
    facts_text = facts.read_text(encoding="utf8")
    for required in (
        "Vendor Facts File v1", "It is not a ranking signal.", "SAMPLE DATA",
        "https://app.broadcastwell.com/standard/vendor-facts.schema.json",
        "https://creativecommons.org/licenses/by/4.0/", "get_company", "get_pricing",
        "get_fit", "get_integrations", "get_compliance", "get_links",
        "Format validation does not verify the truth of a claim.",
    ):
        if required not in facts_text:
            fail("Vendor Facts File is missing %r" % required)
if llms.exists():
    for required in (
        "Agent Test: $490 once.", "Findings within 48 hours of task confirmation.",
        "White-label Agent Test: $490 per agency client report, run by ChatGPT Work with Cloud browser, two runs per task.",
        "One credit per Sprint.",
        "https://broadcastwell.com/buy/agent-test", "https://broadcastwell.com/agent-ready",
        "Ask <Vendor>: a read-only connector", "https://app.broadcastwell.com/mcp/vendor/kalvenor",
        "Vendor Facts File v1: an open schema (CC BY 4.0)",
    ):
        if required not in llms.read_text(encoding="utf8"):
            fail("llms.txt is missing the Agent Ready rule %r" % required)
    for prefix in ("- Agent Test:", "- [Agent Ready:"):
        lines = [line for line in llms.read_text(encoding="utf8").splitlines() if line.startswith(prefix)]
        if len(lines) != 1:
            fail("llms.txt must have exactly one commercial Agent Test entry for %r" % prefix)
            continue
        if "ChatGPT Work with Cloud browser" not in lines[0] or "two runs per task" not in lines[0]:
            fail("llms.txt commercial Agent Test entry must name the cloud agent and two runs per task")
        if any(old in lines[0] for old in ("Perplexity Computer", "two agents", "both agents")):
            fail("llms.txt commercial Agent Test entry has superseded agent scope")

if problems:
    print("Build verification failed:")
    for p in problems:
        print("  " + p)
    sys.exit(1)

print("Build verification passed. %d pages checked (%s); %d served files clear of the 5 October 2026 ruling words." % (
    len(manifest),
    ", ".join("%d %s" % (sum(1 for c in manifest.values() if c == k), k)
              for k in sorted(VALID_CLASSES) if any(c == k for c in manifest.values())),
    ruling_files,
))
