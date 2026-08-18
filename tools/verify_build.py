"""Structural checks on the built site.

Run after `mkdocs build`. Fails the build if the manual stops being
ungated, crawlable or extractable without JavaScript. This runs in CI so a
future edit cannot quietly reintroduce a form, drop a canonical tag or ship
an image with no alt text.
"""

import json
import pathlib
import re
import sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"

EM_DASH = "—"
DOUBLE_HYPHEN = "--"

problems = []


def fail(msg):
    problems.append(msg)


def html_pages():
    for p in sorted(SITE.rglob("*.html")):
        yield p, p.read_text(encoding="utf8")


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
    if "Disallow:" in body:
        fail("robots.txt contains a Disallow rule")
    if re.search(r"(?i)crawl\-delay", body):
        fail("robots.txt contains a crawl delay")
    if "Sitemap:" not in body:
        fail("robots.txt does not reference the sitemap")

sitemap = SITE / "sitemap.xml"
if not sitemap.exists():
    fail("sitemap.xml missing from the built site root")
else:
    sm = sitemap.read_text(encoding="utf8")
    for slug in [
        "/absence-ladder/",
        "/measurement-noise/",
        "/posts/same-score-different-problem/",
        "/posts/half-its-own-shortlist/",
    ]:
        if slug not in sm:
            fail("sitemap.xml does not list %s" % slug)

cname = SITE / "CNAME"
if not cname.exists() or cname.read_text(encoding="utf8").strip() != "docs.broadcastwell.com":
    fail("CNAME missing or wrong in the built site root")

SKIP_PAGES = {"404.html"}


def is_ownership_proof(rel):
    """Search engine ownership proof files are one line of plain text served
    with an .html extension. They are not pages and are exempt from the page
    checks below."""
    return re.fullmatch(r"google[0-9a-f]+\.html", rel) is not None


for path, html in html_pages():
    rel = path.relative_to(SITE).as_posix()
    if is_ownership_proof(rel):
        continue

    for form in re.findall(r"(?is)<form\b[^>]*>", html):
        if re.search(r"(?is)\baction=", form):
            fail("%s contains a form that submits somewhere" % rel)
    if re.search(r"(?is)<input\b[^>]*type=[\"']?email", html):
        fail("%s contains an email input" % rel)
    if re.search(r"(?is)<input\b[^>]*(name|id)=[\"']?(email|newsletter|subscribe)", html):
        fail("%s contains a subscription input" % rel)

    if rel not in SKIP_PAGES and 'rel="canonical"' not in html:
        fail("%s has no canonical link tag" % rel)

    heads = re.findall(r"(?is)<h1\b", html)
    if rel not in SKIP_PAGES and len(heads) != 1:
        fail("%s has %d h1 elements, expected exactly 1" % (rel, len(heads)))

    for img in re.findall(r"(?is)<img\b[^>]*>", html):
        m = re.search(r"(?is)alt=[\"'](.*?)[\"']", img)
        if m is None or len(m.group(1).strip()) < 40:
            fail("%s has an image whose alt text is missing or too short to state a finding" % rel)

    for block in re.findall(r"(?is)<script type=\"application/ld\+json\">(.*?)</script>", html):
        try:
            json.loads(block)
        except Exception as exc:
            fail("%s has JSON-LD that does not parse: %s" % (rel, exc))

FRONT_MATTER = re.compile(r"(?s)\A\s*\n?[-]{3}\n.*?\n[-]{3}\n")

for src in sorted(DOCS.rglob("*.md")):
    text = FRONT_MATTER.sub("", src.read_text(encoding="utf8"))
    rel = src.relative_to(DOCS).as_posix()
    if EM_DASH in text:
        fail("%s contains an em dash in its prose" % rel)
    if DOUBLE_HYPHEN in text:
        fail("%s contains a double hyphen in its prose" % rel)

for path, html in html_pages():
    rel = path.relative_to(SITE).as_posix()
    body = re.sub(r"(?is)<script.*?</script>", " ", html)
    body = re.sub(r"(?is)<style.*?</style>", " ", body)
    body = re.sub(r"(?is)<[^>]+>", " ", body)
    if EM_DASH in body:
        fail("%s renders an em dash" % rel)

for slug in ["absence-ladder", "measurement-noise"]:
    page = SITE / slug / "index.html"
    if not page.exists():
        fail("%s did not build to its own directory URL" % slug)
        continue
    html = page.read_text(encoding="utf8")
    if "TechArticle" not in html:
        fail("%s is not marked up as a TechArticle" % slug)
    body = re.sub(r"(?is)<script.*?</script>", " ", html)
    body = re.sub(r"(?is)<[^>]+>", " ", body)
    words = len(body.split())
    if words < 2500:
        fail("%s renders only %d words of server side text" % (slug, words))

if problems:
    print("Build verification failed:")
    for p in problems:
        print("  " + p)
    sys.exit(1)

print("Build verification passed.")
