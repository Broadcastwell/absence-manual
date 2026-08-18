# absence-manual

Source for The Absence Manual, a free technical manual on AI search
visibility published at https://docs.broadcastwell.com/. One chapter per URL,
built with MkDocs and served by GitHub Pages.

Prose and figures are CC BY 4.0 (see CONTENT-LICENSE.md). Site code is MIT
(see LICENSE).

## Build locally

    pip install -r requirements.txt
    mkdocs serve

## Structure

    docs/index.md              landing page and table of contents
    docs/absence-ladder.md     Chapter 2
    docs/measurement-noise.md  Chapter 6
    docs/posts/                standalone notes cut from the chapters
    docs/robots.txt            crawler policy, served at the site root
    docs/CNAME                 custom domain for GitHub Pages
    overrides/                 theme templates that emit the JSON-LD blocks

Every statistic on the site traces to a published figure in one of the three
State of GEO volumes, whose data and code are at
https://github.com/Broadcastwell/state-of-geo-2026.
