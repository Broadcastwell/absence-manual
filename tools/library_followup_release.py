"""Explicit owner-authorized maintenance of the reviewed published site.

The prior Research build remains a separately validated, immutable input.
This route admits only individually reviewed source changes and the exact
complete artifact inventory reviewed after a real build. It cannot turn an
unapproved observation, a partial source list, or a frozen edit into a release.
"""
from pathlib import Path
from datetime import datetime, timezone
from types import SimpleNamespace
import argparse, copy, gzip, hashlib, io, json, os, re, subprocess, sys, zipfile

PLAN = 'tools/library-followup-20261105.json'
PIN = 'tools/library-followup-20261105.sha256'
WORK = '.library-followup-work'
POLICY = 'OWNER_2026_11_05_EXACT_FOLLOWUP_V1'
PRIVATE = {'relaunch-build-provenance.json', 'library-release-proof.json',
           'library-effective-payload.json', 'library-compiled-state.json'}
sha = lambda raw: hashlib.sha256(raw).hexdigest()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + '\n').encode()

def safe_file(root, relative):
    require(isinstance(relative, str) and relative and '\\' not in relative
            and ':' not in relative and not relative.startswith('/')
            and '..' not in Path(relative).parts, 'Unsafe follow-up input path')
    p = Path(root)
    for part in Path(relative).parts:
        p = p / part
        require(not p.is_symlink() and not getattr(p, 'is_junction', lambda: False)(),
                'Follow-up symlink or junction is forbidden')
    require(p.is_file(), 'Follow-up input is missing: ' + relative)
    return p

def plan(root):
    raw = safe_file(root, PLAN).read_bytes()
    require(safe_file(root, PIN).read_text(encoding='ascii').strip() == sha(raw),
            'Follow-up plan pin differs')
    data = json.loads(raw)
    require(data.get('policy') == POLICY and isinstance(data.get('source_review_complete'), bool),
            'Explicit owner-authorized source-review state is missing')
    require(data.get('base_commit') == '88d6b6bb11f8b4bd713ee7e4e79c863ff9973518',
            'First follow-up must bind the actual released Research main')
    require(data.get('prior_artifact_id') == 13359529469 and data.get('prior_artifact_sha256')
            == '1badcad3e2416b9b156d8a310b7a59b5a06b1d8b529ab04837f042f7ddf700c1',
            'Actual reviewed PR97 artifact binding differs')
    return data

def source_inventory(root, ref=None):
    if ref:
        raw = subprocess.check_output(['git', '-c', 'core.autocrlf=false', 'archive', '--format=zip', '-0', ref], cwd=root)
        from library_research_source_archive import archive_files
        files = archive_files(raw)
        return {p: sha(b) for p, b in files.items()}, files
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
    return {p: sha(safe_file(root, p).read_bytes()) for p in names if p and p not in {PLAN, PIN}}

def validate_sources(root, data):
    actual = source_inventory(root)
    require(actual == data['candidate_source_sha256'],
            'Complete current source inventory differs from reviewed files')
    before, _ = source_inventory(root, data['base_commit'])
    require(before == data['base_source_sha256'], 'Actual prior Git source inventory differs')
    delta = {p for p in set(before) | set(actual) if p not in {PLAN, PIN} and before.get(p) != actual.get(p)}
    require(delta == set(data['source_changes']), 'Unlisted source change in follow-up')
    for p, r in data['source_changes'].items():
        require(r['before_sha256'] == before.get(p) and r['after_sha256'] == actual.get(p),
                'Reviewed source delta differs: ' + p)
    from library_field_freeze_navigation import FrozenNavigation
    FrozenNavigation(root / 'docs', root / 'tools/library_field_freeze_navigation.json',
                     'ec8e3d76d21ee607974ffa5c2e7c82eb75c3d17f8b727e62d8d35d37830d91f7')
    science = json.loads(safe_file(root, 'tools/library_research_release_paths.json').read_bytes())
    for p, digest in science['immutable_science_and_registered_downloads'].items():
        require(sha(safe_file(root, 'docs/' + p).read_bytes()) == digest,
                'Scientific or registered file changed: ' + p)
    return {'complete_source_files': len(actual), 'reviewed_source_changes': len(delta),
            'scientific_and_registered_files_preserved': len(science['immutable_science_and_registered_downloads'])}

def prepare(root, artifact, baseline_artifact):
    data = plan(root)
    proof = validate_sources(root, data)
    require(sha(artifact.read_bytes()) == data['prior_artifact_sha256'], 'Prior artifact bytes differ')
    prior = root / WORK / 'prior'
    _, files = source_inventory(root, data['base_commit'])
    prior.mkdir(parents=True, exist_ok=True)
    for rel, raw in files.items():
        target = prior / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            require(target.read_bytes() == raw, 'Existing immutable baseline source differs: ' + rel)
        else:
            target.write_bytes(raw)
    # Execute the unchanged released preparation module against its exact
    # released sources. No prior approval or historical pin is rewritten.
    environment = dict(os.environ)
    environment['GIT_DIR'] = subprocess.check_output(['git', 'rev-parse', '--absolute-git-dir'], cwd=root, text=True).strip()
    environment['GIT_WORK_TREE'] = str(prior)
    result = subprocess.run([sys.executable, str(prior / 'tools/library_research_activation.py'),
        'prepare', '--repo', str(prior), '--source-ref', data['base_commit'],
        '--artifact', str(baseline_artifact.resolve())], cwd=root, env=environment, capture_output=True, text=True)
    require(result.returncode == 0, 'Prior Research preparation failed: ' + result.stderr[-3000:])
    (root / WORK / 'prior-stage-result.json').write_text(result.stdout, encoding='utf-8')
    (root / WORK / 'source-proof.json').write_bytes(json_bytes(proof))
    return proof

SITEMAP_PAGE = re.compile(r'https://docs\.broadcastwell\.com/[a-z0-9-]+(?:/[a-z0-9-]+)*/')

def add_reviewed_sitemap_rows(xml, rows, site):
    """Append only explicitly reviewed new page URLs; never edit or reorder an existing row."""
    require(isinstance(rows, list), 'Reviewed sitemap additions must be a list')
    for row in rows:
        url, date = row.get('url'), row.get('lastmod')
        require(isinstance(url, str) and SITEMAP_PAGE.fullmatch(url), 'Reviewed sitemap addition must be a docs page URL')
        require(isinstance(date, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', date), 'Reviewed sitemap addition needs an ISO date')
        require(('<loc>' + url + '</loc>').encode() not in xml, 'Reviewed sitemap addition already present: ' + url)
        require((Path(site) / url.removeprefix('https://docs.broadcastwell.com/') / 'index.html').is_file(),
                'Reviewed sitemap addition has no built page: ' + url)
        require(xml.count(b'</urlset>') == 1, 'Sitemap closing boundary differs')
        entry = '    <url>\n         <loc>' + url + '</loc>\n         <lastmod>' + date + '</lastmod>\n    </url>\n'
        xml = xml.replace(b'</urlset>', entry.encode() + b'</urlset>', 1)
    return xml

def route(path):
    return path.removesuffix('index.md') + 'index.html' if path.endswith('/index.md') or path == 'index.md' else path.removesuffix('.md') + '/index.html'

class FollowupSession:
    @classmethod
    def load(cls, config):
        self = cls()
        self.root = Path(config['docs_dir']).resolve().parent
        self.docs = self.root / 'docs'
        self.data = plan(self.root)
        self.source_proof = validate_sources(self.root, self.data)
        self.work = self.root / WORK
        prior = self.work / 'prior'
        require(prior.is_dir(), 'Exact released baseline was not staged')
        old_plan = json.loads((prior / 'tools/library-research-support.json').read_bytes())
        from library_research_build import ResearchBuildSession
        self.previous = ResearchBuildSession.load(prior / 'docs', prior / old_plan['release_inputs']['path'],
            old_plan['release_inputs']['sha256'], self.work / 'validated-prior')
        self.base = self.previous.base
        archive_path = self.root / self.data['prior_artifact_path']
        require(sha(archive_path.read_bytes()) == self.data['prior_artifact_sha256'], 'Prior public archive changed')
        self.archive = zipfile.ZipFile(archive_path)
        self.before = {p: self.archive.read(p) for p in self.archive.namelist() if not p.endswith('/') and p not in PRIVATE}
        self.changed_markdown = {p.removeprefix('docs/') for p in self.data['source_changes'] if p.startswith('docs/') and p.endswith('.md')}
        self.contexts = {}
        self.expected_sources = {}
        self.visibility = None
        if self.data.get('visibility_decisions_sha256'):
            from library_visibility_release import VisibilityEdits
            self.visibility = VisibilityEdits(self.root, self.data['visibility_decisions_sha256'])
        return self

    def source_markdown(self, markdown, page, finite_links):
        p = page.file.src_uri
        if p in self.changed_markdown:
            from library_related_chapter_links import source_body
            meta, body = source_body(safe_file(self.docs, p).read_text(encoding='utf-8'))
            require(markdown == body and page.meta == meta, 'Changed page does not use reviewed source: ' + p)
        else:
            body = self.previous.markdown(finite_links.transform(p, markdown), page)
            for edit in self.data.get('effective_edits', {}).get(p, []):
                require(body.count(edit['before']) == edit['count'],
                        'Published source differs from its exact reviewed edit: ' + p)
                body = body.replace(edit['before'], edit['after'])
            if p in self.data.get('effective_dates', {}):
                page.meta['date_modified'] = self.data['effective_dates'][p]
        if self.visibility:
            body, page.meta = self.visibility.apply(p, body, page.meta)
            page.title = page.meta['title']
        self.expected_sources[p] = {'body': body, 'meta': copy.deepcopy(page.meta)}
        return body

    def retain_owner_navigation(self, nav, files):
        nav = self.previous.retain_owner_navigation(nav, files)
        return self.visibility.navigation(nav, files) if self.visibility else nav

    def capture_page(self, output, page):
        self.previous.capture_page(output, page)
        require(self.expected_sources[page.file.src_uri] == {'body': page.markdown, 'meta': page.meta},
                'Rendered page input changed after its reviewed source was selected')
        self.contexts[page.file.src_uri] = {'markdown': page.markdown, 'meta': copy.deepcopy(page.meta),
                                          'content': page.content, 'rendered_html': output}
        return output

    def retain_styles(self, site_dir):
        from library_inherited_presentation import retain_frozen_stylesheets_from_actual_prior
        retain_frozen_stylesheets_from_actual_prior(self.base, site_dir)

    def prepare_outputs(self, site_dir):
        self.site = Path(site_dir)
        self.previous.prepare_outputs(site_dir)
        # The prior consumer generates exactly its previously reviewed entries.
        # Only literal decisions reviewed for this release are applied after it.
        llms = (self.site / 'llms.txt').read_text(encoding='utf-8')
        for r in self.data['llms_edits']:
            require(llms.count(r['before']) == r['count'], 'llms decision no longer matches prior text')
            llms = llms.replace(r['before'], r['after'])
        (self.site / 'llms.txt').write_text(llms, encoding='utf-8', newline='\n')
        if self.visibility:
            self.visibility.prepare_outputs(self.site)
        xml = (self.site / 'sitemap.xml').read_bytes()
        for url, date in self.data['lastmod_edits'].items():
            pattern = rb'(<url>\s*<loc>' + re.escape(url.encode()) + rb'</loc>\s*<lastmod>)([^<]+)(</lastmod>)'
            xml, count = re.subn(pattern, lambda m: m[1] + date.encode() + m[3], xml)
            require(count == 1, 'Exact existing sitemap row missing: ' + url)
        xml = add_reviewed_sitemap_rows(xml, self.data.get('sitemap_additions', []), self.site)
        (self.site / 'sitemap.xml').write_bytes(xml)
        (self.site / 'sitemap.xml.gz').write_bytes(gzip.compress(xml, mtime=0))
        self.render_proof = validate_render_contexts(self.contexts, self.site)
        (self.work / 'render-contexts.json').write_bytes(json_bytes(self.contexts))
        (self.work / 'render-proof.json').write_bytes(json_bytes(self.render_proof))


def validate_render_contexts(contexts, site):
    """Check every complete page body, head and declared Article against its inputs."""
    import markdown
    from html.parser import HTMLParser
    from library_publication_consumers import _HeadAndArticle, _RenderSignature
    from urllib.parse import urljoin
    class ArticleBounds(HTMLParser):
        def __init__(self, text):
            super().__init__(); self.text=text; self.depth=0; self.spans=[]; self.offsets=[0]
            for line in text.splitlines(keepends=True):self.offsets.append(self.offsets[-1]+len(line))
        def position(self):
            line,column=self.getpos();return self.offsets[line-1]+column
        def handle_starttag(self, tag, attrs):
            if tag == 'article':
                if not self.depth:self.start=self.position()+len(self.get_starttag_text())
                self.depth+=1
        def handle_endtag(self, tag):
            if tag == 'article' and self.depth:
                self.depth-=1
                if not self.depth:self.spans.append((self.start,self.position()))
    class ArticleSignature(_RenderSignature):
        def handle_endtag(self, tag):
            if tag != 'img':
                super().handle_endtag(tag)
        def handle_starttag(self, tag, attrs):
            if tag == 'img':
                # Only the unchanged performance-assets hook adds these image
                # presentation attributes. Source, alt text and all other
                # structure remain in the comparison and final artifact pin.
                attrs = [(k,v) for k,v in attrs if k not in
                         {'width','height','srcset','sizes','decoding','loading'}]
            super().handle_starttag(tag, attrs)
    require(len(contexts) >= 400, 'Complete rendered page coverage is missing')
    outputs = {}
    for path, context in contexts.items():
        meta = context['meta']; url = 'https://docs.broadcastwell.com/' + route(path).removesuffix('index.html')
        expected = markdown.markdown(context['markdown'],
            extensions=['toc','tables','fenced_code','attr_list','md_in_html','def_list','footnotes','admonition'],
            extension_configs={'toc':{'permalink':True,'toc_depth':3}})
        if meta.get('page_class') == 'research':
            expected = re.sub(r'(<h2\b[^>]*id="what-our-own-data-shows"[^>]*>.*?)(?=<h2\b[^>]*id="sources")',
                r'<section class="bw-own-data" aria-label="What our own data shows">\1</section>',expected,flags=re.S)
            expected = '<div class="bw-research-content">' + expected + '</div>'
        source = _RenderSignature('https://docs.broadcastwell.com/' + path, True); source.feed(expected)
        rendered = _RenderSignature(url); rendered.feed(context['content'])
        require(source.tokens == rendered.tokens, 'Full rendered body differs from reviewed source: ' + path)
        raw = (site / route(path)).read_bytes(); parsed = _HeadAndArticle(); parsed.feed(raw.decode())
        bounds=ArticleBounds(raw.decode());bounds.feed(raw.decode())
        require(len(bounds.spans) == 1 and bounds.depth == 0, 'Exactly one final article wrapper is required: ' + path)
        start,end=bounds.spans[0]
        final_body = ArticleSignature(url); final_body.feed(raw.decode()[start:end])
        input_body = ArticleSignature(url); input_body.feed(context['content'])
        require(final_body.tokens[:len(input_body.tokens)] == input_body.tokens,
                'Final visible article changed after source rendering: ' + path)
        require(parsed.canonical == [url], 'Canonical differs from the real page route: ' + path)
        title = str(meta.get('title', ''))
        normalized_title = ' '.join(title.split())
        require(parsed.title in {normalized_title, normalized_title + ' | The Absence Manual'}, 'Page title differs from its metadata: ' + path)
        for name, value in {'description':meta.get('description',''), 'og:title':title,
                            'og:description':meta.get('description',''), 'og:url':url}.items():
            require(parsed.meta.get(name) == [value], 'Rendered metadata differs: ' + path + ' ' + name)
        articles = [x for x in parsed.scripts if x.get('@type') in {'Article','TechArticle'}]
        if meta.get('schema_type') in {'Article','TechArticle'}:
            require(len(articles) == 1, 'A single declared Article is required: ' + path)
            for name, value in {'headline':meta.get('headline',title),'description':meta.get('description',''),
                                'datePublished':str(meta.get('date_published','')),
                                'dateModified':str(meta.get('date_modified','')),'url':url}.items():
                require(articles[0].get(name) == value, 'Article differs from its reviewed page: ' + path + ' ' + name)
        require(len([x for x in parsed.scripts if x.get('@type') == 'BreadcrumbList']) == 1,
                'A single breadcrumb is required: ' + path)
        outputs[path] = sha(raw)
    return {'complete_page_count':len(outputs),'full_body_source_comparison':True,
            'final_visible_article_preserves_complete_rendered_body':True,
            'current_heads_and_declared_articles':True,'final_html_sha256':outputs}

def output_inventory(site):
    return {p.relative_to(site).as_posix(): sha(p.read_bytes()) for p in site.rglob('*')
            if p.is_file() and p.relative_to(site).as_posix() not in PRIVATE}

def validate_artifacts(data, before, after):
    require(data.get('artifact_review', {}).get('approved') is True,
            'Actual complete candidate artifact review is pending; observation is not approval')
    require(after == data['approved_artifact_sha256'], 'Whole built artifact differs from actual reviewed output')
    actual = {p for p in set(before) | set(after) if before.get(p) != after.get(p)}
    require(actual == set(data['artifact_changes']), 'Complete changed public file scope differs')
    for p, r in data['artifact_changes'].items():
        require(r == {'before_sha256': before.get(p), 'after_sha256': after.get(p)}, 'Artifact delta pin differs: ' + p)
    return len(actual)

def verify(root):
    data = plan(root)
    source_proof = validate_sources(root, data)
    site = root / 'site'
    actual = output_inventory(site)
    if data.get('visibility_decisions_sha256'):
        from verify_visibility_release import validate as validate_visibility
        visibility = validate_visibility(site, json.loads((root / 'tools/library-visibility-20261105.json').read_bytes()),
                                         [r['url'] for r in data.get('sitemap_additions', [])])
        (root / 'visibility-release-check.json').write_bytes(json_bytes(visibility))
    with zipfile.ZipFile(root / data['prior_artifact_path']) as z:
        before = {p: sha(z.read(p)) for p in z.namelist() if not p.endswith('/') and p not in PRIVATE}
    observation = {'observed_utc': datetime.now(timezone.utc).isoformat(), 'approved': False,
                   'source_proof': source_proof, 'files': actual,
                   'changes': {p: {'before_sha256': before.get(p), 'after_sha256': actual.get(p)}
                               for p in sorted(set(before) | set(actual)) if before.get(p) != actual.get(p)}}
    (root / 'followup-candidate-observation.NOT_APPROVED.json').write_bytes(json_bytes(observation))
    require(data['source_review_complete'] is True, 'Current source review is still pending')
    # The command-line freeze gate also runs independently in CI.
    changed = validate_artifacts(data, before, actual)
    result = {'policy': POLICY, 'actual_complete_public_files': len(actual), 'actual_changed_files': changed,
              'source_proof': source_proof, 'approved_plan_sha256': sha((root / PLAN).read_bytes())}
    (root / 'followup-release-result.json').write_bytes(json_bytes(result))
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'verify'])
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--artifact', type=Path)
    parser.add_argument('--baseline-artifact', type=Path)
    args = parser.parse_args()
    root = args.repo.resolve()
    if args.action == 'prepare':
        require(args.artifact is not None and args.baseline_artifact is not None,
                'Both exact published baseline artifacts are required')
        result = prepare(root, args.artifact.resolve(), args.baseline_artifact.resolve())
    else:
        result = verify(root)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
