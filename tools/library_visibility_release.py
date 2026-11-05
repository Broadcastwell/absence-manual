"""Apply individually reviewed discovery edits to the actual published sources.

The input hashes refer to PR98's effective Markdown, not an older raw article.
Historical source files, approvals, study events and the field-test registration
remain separate immutable inputs. No observation grants artifact approval.
"""
from pathlib import Path
import copy
import hashlib
import json
import re

PATH = 'tools/library-visibility-20261105.json'
POLICY = 'OWNER_2026_11_05_VISIBILITY_V1'
BASE = 'ed24a5f0d1332f64d4630913e6e37b0543e49ee8'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()


def require(condition, message):
    if not condition:
        raise ValueError(message)


class VisibilityEdits:
    def __init__(self, root, binding):
        self.root = Path(root)
        raw = (self.root / PATH).read_bytes()
        require(binding == digest(raw), 'Current visibility decisions differ from their reviewed binding')
        self.data = json.loads(raw)
        require(self.data['policy'] == POLICY and self.data['serving_base_commit'] == BASE,
                'Visibility decisions must bind the actual PR98 release')
        self.pages = self.data['pages']
        self.static = self.data['static_pages']
        self.seen = set()
        require(len(self.pages) == 393, 'Visibility scope must contain all 393 eligible Markdown pages')
        frozen = json.loads((self.root / 'tools/library_field_freeze_navigation.json').read_bytes())
        self.frozen_paths = set(frozen['pages'])
        frozen_urls = {r['url'] for r in frozen['frozen_sitemap_entries']}
        require(len(frozen_urls) == 45, 'Registered field-test population differs')
        require(not frozen_urls & {r['url'] for r in self.pages.values()},
                'A frozen page cannot receive a visibility edit')
        require(len(self.static) == 2, 'Both current standalone data pages must be reviewed')
        require(len({r['meta']['title'] for r in self.pages.values()}) == len(self.pages),
                'Visibility titles must be unique')
        require(len({r['meta']['description'] for r in self.pages.values()}) == len(self.pages),
                'Visibility descriptions must be unique')
        for path, row in self.pages.items():
            title = row['meta']['title']
            require(title.endswith('?') and len(title) < 60, 'Title is not a concise question: ' + path)
            require(150 <= len(row['meta']['description']) <= 160, 'Description length differs: ' + path)
            require(row['meta']['headline'] == title and row['meta']['template'] == 'followup.html',
                    'Current title consumer is missing: ' + path)
            require(row['meta']['schema_type'] in {'Article', 'TechArticle'},
                    'Unsupported Article declaration: ' + path)

    def apply(self, path, body, meta):
        if path not in self.pages:
            return body, meta
        row = self.pages[path]
        require(digest(body.encode()) == row['before_body_sha256'],
                'Actual published article changed before visibility edits: ' + path)
        require(digest(canonical(meta)) == row['before_meta_sha256'],
                'Actual published metadata changed before visibility edits: ' + path)
        for edit in row['edits']:
            require(edit['before'] and body.count(edit['before']) == edit['count'],
                    'Visibility edit does not match the complete current article: ' + path)
            body = body.replace(edit['before'], edit['after'])
        require(digest(body.encode()) == row['after_body_sha256'],
                'Visibility result differs from reviewed article: ' + path)
        prose = re.sub(r'^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$', '', body, flags=re.M | re.S)
        require(re.findall(r'^# (.+)$', prose, flags=re.M) == [row['meta']['title']],
                'The visible question and head must agree: ' + path)
        self.seen.add(path)
        return body, copy.deepcopy(row['meta'])

    def prepare_outputs(self, site):
        require(self.seen == set(self.pages), 'Not every visibility decision reached its actual page')
        site = Path(site)
        text = (site / 'llms.txt').read_text(encoding='utf8')
        for edit in self.data['llms_edits']:
            require(text.count(edit['before']) == edit['count'], 'Current llms entry differs from reviewed input')
            text = text.replace(edit['before'], edit['after'])
        (site / 'llms.txt').write_text(text, encoding='utf8', newline='\n')
        for path, row in self.static.items():
            raw = (site / path).read_bytes()
            require(digest(raw) == row['before_sha256'], 'Standalone data source changed: ' + path)
            text = raw.decode('utf8')
            for edit in row['edits']:
                require(text.count(edit['before']) == edit['count'], 'Standalone edit differs: ' + path)
                text = text.replace(edit['before'], edit['after'])
            raw = text.encode('utf8')
            require(digest(raw) == row['after_sha256'], 'Standalone output differs: ' + path)
            (site / path).write_bytes(raw)
        xml = (site / 'sitemap.xml').read_bytes()
        for row in self.static.values():
            before = ('<loc>' + row['url'] + '</loc>').encode()
            require(xml.count(before) == 1, 'Standalone sitemap URL is missing')
            xml = xml.replace(before, before + ('<lastmod>' + self.data['revision_utc'] + '</lastmod>').encode())
        (site / 'sitemap.xml').write_bytes(xml)

    def navigation(self, nav, files):
        from library_publication_build import LegacyNavigationPage
        views = {}
        frozen_pagination = []
        for file in files:
            page = getattr(file, 'page', None)
            if page is not None and file.src_uri in self.frozen_paths:
                neighbors = []
                for neighbor in [page.previous_page, page.next_page]:
                    if neighbor:
                        label = neighbor.title
                        if label is None:
                            label = self.pages.get(neighbor.file.src_uri, {}).get('prior_title')
                        require(isinstance(label, str) and label, 'Frozen neighbor lacks its actual prior title')
                        neighbors.append(LegacyNavigationPage(getattr(neighbor, '_page', neighbor), label))
                    else:
                        neighbors.append(None)
                frozen_pagination.append((page, neighbors))
        def current(page):
            path = page.file.src_uri
            if path not in self.pages:
                return page
            base = getattr(page, '_page', page)
            view = LegacyNavigationPage(base, self.pages[path]['meta']['title'])
            views[id(page)] = view
            return view
        def walk(items):
            result = []
            for item in items:
                if getattr(item, 'children', None) is not None:
                    item.children = walk(item.children)
                result.append(current(item) if getattr(item, 'is_page', False) else item)
            return result
        nav.items = walk(nav.items)
        nav.pages = [views.get(id(p), p) for p in nav.pages]
        for page in nav.pages:
            page.previous_page = views.get(id(page.previous_page), page.previous_page)
            page.next_page = views.get(id(page.next_page), page.next_page)
        if getattr(nav, 'homepage', None):
            nav.homepage = views.get(id(nav.homepage), nav.homepage)
        for page, neighbors in frozen_pagination:
            page.previous_page, page.next_page = neighbors
        return nav

