"""Build the versioned PDF mirror of The Absence Manual.

Generated from the same markdown source the HTML is built from, so the two
cannot drift. Run after mkdocs build. Writes two files into site/:

    absence-manual-v<version>-<date>.pdf   the versioned artefact
    absence-manual.pdf                     the stable path the landing page links

The stable path always serves the current version. Slugs published once are
permanent, so the link on the landing page never changes.
"""

import datetime
import pathlib
import re
import sys

import markdown
import yaml
from weasyprint import HTML

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"
FOOTER_MARK = "## About this manual"

CSS = """
@page {
  size: A4;
  margin: 22mm 20mm 20mm 20mm;
  @bottom-center { content: counter(page); font-size: 8pt; color: #666; }
  @top-center { content: "The Absence Manual"; font-size: 8pt; color: #999; }
}
@page :first { @top-center { content: ""; } @bottom-center { content: ""; } }
body { font-family: "DejaVu Serif", Georgia, serif; font-size: 10pt; line-height: 1.45; color: #111; }
h1 { font-size: 19pt; line-height: 1.2; margin: 0 0 4mm 0; page-break-before: always; page-break-after: avoid; }
h1.first { page-break-before: avoid; }
h2 { font-size: 12.5pt; margin: 7mm 0 2mm 0; page-break-after: avoid; }
h3 { font-size: 11pt; margin: 5mm 0 2mm 0; page-break-after: avoid; }
p { margin: 0 0 3mm 0; orphans: 3; widows: 3; }
blockquote { margin: 3mm 0; padding: 2mm 4mm; border-left: 2pt solid #888; color: #333; font-size: 9.5pt; }
table { border-collapse: collapse; width: 100%; font-size: 8.5pt; margin: 3mm 0; page-break-inside: avoid; }
th, td { border: 0.4pt solid #bbb; padding: 1.4mm 2mm; text-align: left; vertical-align: top; }
th { background: #f0f0f0; }
img { max-width: 100%; page-break-inside: avoid; }
figure { margin: 4mm 0; page-break-inside: avoid; }
figcaption { font-size: 8.5pt; color: #555; margin-top: 1.5mm; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 8.5pt; }
a { color: #14418b; text-decoration: none; }
strong { font-weight: 700; }
.cover { page-break-after: always; text-align: left; padding-top: 55mm; }
.cover h1 { font-size: 30pt; page-break-before: avoid; margin-bottom: 6mm; }
.cover .sub { font-size: 12pt; color: #333; margin-bottom: 18mm; }
.cover .meta { font-size: 9.5pt; color: #444; line-height: 1.7; }
.toc { page-break-after: always; }
.toc h1 { page-break-before: avoid; }
.toc ol { padding-left: 6mm; }
.toc li { margin-bottom: 1.4mm; font-size: 10pt; }
.colophon h1 { page-break-before: always; }
"""


def read_order():
    pages = yaml.safe_load((DOCS / ".pages").read_text(encoding="utf-8"))
    order = []
    for entry in pages["nav"]:
        if entry == "posts":
            for p in sorted((DOCS / "posts").glob("*.md")):
                order.append(p)
        else:
            order.append(DOCS / entry)
    return order


def split_front_matter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            meta = yaml.safe_load(text[3:end]) or {}
            return meta, text[end + 4 :]
    return {}, text


def strip_footer(body):
    i = body.find(FOOTER_MARK)
    return (body[:i].rstrip(), body[i:]) if i != -1 else (body.rstrip(), "")


def main():
    cfg = yaml.safe_load(
        re.sub(r"^( *)!!python[^\n]*$", r"\1null", (ROOT / "mkdocs.yml").read_text(encoding="utf-8"), flags=re.M)
    )
    version = str(cfg["extra"]["manual_version"])
    version_label = str(cfg["extra"]["manual_version_label"])
    build_date = datetime.date.today().isoformat()

    md = markdown.Markdown(
        extensions=["tables", "attr_list", "md_in_html", "sane_lists", "footnotes"]
    )

    order = read_order()
    parts = []
    titles = []
    colophon = ""

    for path in order:
        meta, body = split_front_matter(path.read_text(encoding="utf-8"))
        body, footer = strip_footer(body)
        if footer and not colophon:
            colophon = footer
        title = str(meta.get("title") or path.stem)
        titles.append(title)
        html = md.reset().convert(body)
        # resolve figure paths so weasyprint can find the images
        html = html.replace('src="figures/', f'src="{(DOCS / "figures").as_uri()}/')
        parts.append(f'<section id="{path.stem}">{html}</section>')

    toc_items = "".join(f"<li>{t}</li>" for t in titles)
    cover = f"""
<div class="cover">
  <h1 class="first">The Absence Manual</h1>
  <div class="sub">A technical manual on AI search visibility for B2B software.</div>
  <div class="meta">
    Sairam Sivakumar, Broadcastwell<br>
    {version_label}<br>
    Built {build_date}<br>
    <br>
    Read the current version at https://docs.broadcastwell.com/<br>
    Prose and figures CC BY 4.0.<br>
    <br>
    This PDF is a mirror. It is generated from the same source as the website,
    in the same build, so the two cannot drift. It is free and ungated: there is
    no form, no email field and no login anywhere in it or on the site.
  </div>
</div>
<div class="toc"><h1 class="first">Contents</h1><ol>{toc_items}</ol></div>
"""
    colophon_html = md.reset().convert(colophon).replace(
        "<h2>About this manual</h2>", "<h1>About this manual</h1>"
    )

    doc = (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<title>The Absence Manual, {version_label}</title>"
        f"<style>{CSS}</style></head><body>"
        f"{cover}{''.join(parts)}"
        f"<div class='colophon'>{colophon_html}</div>"
        "</body></html>"
    )

    SITE.mkdir(exist_ok=True)
    versioned = SITE / f"absence-manual-v{version}-{build_date}.pdf"
    stable = SITE / "absence-manual.pdf"
    HTML(string=doc, base_url=str(ROOT)).write_pdf(versioned)
    stable.write_bytes(versioned.read_bytes())
    print(f"PDF written: {versioned.name} ({versioned.stat().st_size // 1024} KB) and {stable.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
