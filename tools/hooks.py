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
