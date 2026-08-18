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
DOUBLE_HYPHEN = "-" + "-"

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
    if DOUBLE_HYPHEN in text:
        fail("%s contains a double hyphen in its prose" % rel)


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


if problems:
    print("Build verification failed:")
    for p in problems:
        print("  " + p)
    sys.exit(1)

print("Build verification passed. %d pages checked (%s)." % (
    len(manifest),
    ", ".join("%d %s" % (sum(1 for c in manifest.values() if c == k), k)
              for k in sorted(VALID_CLASSES) if any(c == k for c in manifest.values())),
))
