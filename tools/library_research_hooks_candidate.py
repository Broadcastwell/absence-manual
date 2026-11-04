"""Build hooks for The Absence Manual.

The table of contents extension puts its permalink anchor inside the heading it
links to, so the pilcrow became part of the heading's accessible name and a
chapter title was announced as "Chapter 2. The Absence Ladder" followed by a
paragraph mark. The anchor is decoration beside a heading that already has an
id, so it is hidden from the accessibility tree and taken out of the tab order.
An aria-hidden element must not be focusable, which is why both attributes are
set together.
"""

import re

PERMALINK = re.compile(r'<a class="headerlink"(?![^>]*aria-hidden)')
REPLACEMENT = '<a class="headerlink" aria-hidden="true" tabindex="-1"'


def on_page_content(html, page=None, config=None, files=None):
    html = PERMALINK.sub(REPLACEMENT, html)
    if page and page.meta.get('page_class') == 'research':
        html = re.sub(
            r'(<h2\b[^>]*id="what-our-own-data-shows"[^>]*>.*?)(?=<h2\b[^>]*id="sources")',
            r'<section class="bw-own-data" aria-label="What our own data shows">\1</section>',
            html, flags=re.S)
        html = '<div class="bw-research-content">' + html + '</div>'
    # Material wraps tables in scroll regions after rendering. A focusable table
    # lets keyboard users scroll that region without requiring a mouse or script.
    return re.sub(r'<table(?![^>]*\btabindex=)(?=[\s>])', '<table tabindex="0"', html)

# MkDocs loads hook files by location, without guaranteeing a tools package.
# Import the reviewed sibling directly; preserve the existing content hook above.
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

_CHAPTER_MODULE_PATH = Path(__file__).with_name("library_related_chapter_links.py")
_CHAPTER_SPEC = spec_from_file_location("_bw_finite_related_chapter_links", _CHAPTER_MODULE_PATH)
if _CHAPTER_SPEC is None or _CHAPTER_SPEC.loader is None:
    raise RuntimeError("Cannot load the finite Related chapter hook")
_CHAPTER_MODULE = module_from_spec(_CHAPTER_SPEC)
_CHAPTER_SPEC.loader.exec_module(_CHAPTER_MODULE)
_CHAPTER_LINKS = None
_PUBLICATION = None


def on_pre_build(config):
    global _CHAPTER_LINKS, _PUBLICATION
    _CHAPTER_LINKS = _CHAPTER_MODULE.FiniteChapterLinks(
        config["docs_dir"], Path(__file__).with_name("library_related_chapters.json"))
    # MkDocs loads hooks by location; add only this reviewed sibling directory.
    import sys
    sibling = str(Path(__file__).resolve().parent)
    if sibling not in sys.path:
        sys.path.insert(0, sibling)
    from library_build_dispatch import from_environment
    _PUBLICATION = from_environment(config)


def on_page_markdown(markdown, page, config=None, files=None):
    if _CHAPTER_LINKS is None:
        raise ValueError("Finite Related map must validate before rendering pages")
    staged = _CHAPTER_LINKS.transform(page.file.src_uri, markdown)
    return _PUBLICATION.markdown(staged, page)


from mkdocs.plugins import event_priority


@event_priority(-100)
def on_nav(nav, config=None, files=None):
    return _PUBLICATION.retain_owner_navigation(nav,files)


@event_priority(-100)
def on_post_page(output, page, config=None):
    return _PUBLICATION.capture_page(output, page)


@event_priority(-300)
def on_post_build(config):
    _PUBLICATION.prepare_outputs(config['site_dir'])
