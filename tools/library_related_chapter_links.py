"""Finite, source-pinned build repair. This module never writes source files."""
from __future__ import annotations

import hashlib
import json
import posixpath
from pathlib import Path, PurePosixPath
import re
import unicodedata
from urllib.parse import unquote, urlsplit

import yaml


APPROVED_MAP_SHA256 = '4ae10f72b10b99f7047bfebe2ad1f1eecb28e452e42ca4b6e1ef6da66c9d78f8'
APPROVED_KEYS_SHA256 = '63ff07ec60940ef6fed07603d418d47520ba69972b31e8267a528f8c056f8dd7'
EXPECTED_COUNT = 94
HEX = re.compile(r'[0-9a-f]{64}')
SOURCE_PATH = re.compile(r'answers/[a-z0-9-]+/[a-z0-9-]+\.md')
CHAPTER_PATH = re.compile(r'[a-z0-9-]+\.md')
LINK_LINE = re.compile(r'- \[([^\]\r\n]+)\]\(([^()\s]+)\)[ \t]*')
INLINE_LINK = re.compile(r'(?<!!)\[[^\]\r\n]+\]\(([^()\s]+)\)')
FIELDS = {'canonical_source_sha256', 'related_section_sha256',
          'chapter_path', 'label', 'action'}
REPLACE_FIELDS = {'replace_href', 'replace_label'}


def require(ok, message):
    if not ok:
        raise ValueError('Finite Related repair: ' + message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical_source(raw):
    """The unchanged library_quality.load_pages full-source hash contract."""
    return raw.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        require(key not in value, 'duplicate JSON key: ' + key)
        value[key] = item
    return value


def source_body(text):
    match = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    require(match is not None, 'missing YAML front matter')
    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        raise ValueError('Finite Related repair: invalid YAML front matter') from error
    require(isinstance(meta, dict), 'front matter must be an object')
    # MkDocs meta.get_data removes leading body newlines at this boundary.
    return meta, text[match.end():].lstrip('\n')


def related_parts(markdown):
    related = list(re.finditer(r'(?m)^## Related[ \t\r]*$', markdown))
    next_step = list(re.finditer(r'(?m)^## Next step[ \t\r]*$', markdown))
    require(len(related) == len(next_step) == 1, 'need one Related and one Next step heading')
    start, end = related[0].start() + len('## Related'), next_step[0].start()
    require(start < end, 'Related must precede Next step')
    section = markdown[start:end]
    require(not re.search(r'(?m)^##\s', section), 'unexpected heading inside Related')
    return markdown[:start], section, markdown[end:]


def plain_label(value):
    require(isinstance(value, str) and value and value == value.strip(), 'empty or padded label')
    require(len(value.splitlines()) == 1, 'newline in label')
    require(not any(unicodedata.category(c).startswith('C') for c in value), 'control or newline in label')
    require(not re.search(r'[\[\]()<>*_`\\#!|~]', value), 'Markdown or HTML in label')
    return value


def safe_path(docs, value, pattern, description):
    require(isinstance(value, str) and pattern.fullmatch(value) is not None,
            'unsafe ' + description + ': ' + str(value))
    path = (docs / PurePosixPath(value)).resolve()
    require(path.is_relative_to(docs) and path.is_file(), 'missing or escaped ' + description + ': ' + value)
    return path


def related_links(section):
    result, offset = [], 0
    for line in section.splitlines(keepends=True):
        content = line.rstrip('\r\n')
        if content.strip():
            match = LINK_LINE.fullmatch(content)
            require(match is not None, 'Related must contain only complete Markdown link bullets')
            result.append({'label': match[1], 'href': match[2],
                           'end': offset + len(content),
                           'token': '[' + match[1] + '](' + match[2] + ')'})
        offset += len(line)
    return result


def related_local_target(href, source, docs):
    """Resolve only local docs destinations, retaining the actual file's case."""
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        require(parsed.scheme in {'http', 'https'} and bool(parsed.netloc), 'unsafe original Related URL')
        if parsed.netloc.casefold() != 'docs.broadcastwell.com':
            return None
        local = docs / unquote(parsed.path).lstrip('/')
    else:
        require(not parsed.query, 'unexpected query on a local Related URL')
        path = unquote(parsed.path)
        local = (docs / path.lstrip('/')) if path.startswith('/') else (source.parent / path)
        if not path:
            local = source
    resolved = local.resolve()
    require(resolved.is_relative_to(docs), 'original Related target escapes docs')
    # Only equate a public directory URL and a source route when that source
    # actually exists. Distinct fragments remain distinct destinations.
    if resolved.suffix != '.md':
        candidates = (Path(str(resolved).rstrip('/\\') + '.md'), resolved / 'index.md')
        resolved = next((candidate.resolve() for candidate in candidates if candidate.is_file()), resolved)
        require(resolved.is_relative_to(docs), 'resolved Related target escapes docs')
    return resolved


def href_identity(href, source, docs):
    parsed = urlsplit(href)
    target = related_local_target(href, source, docs)
    if target is None:
        return (parsed.scheme.casefold(), parsed.netloc.casefold(),
                parsed.path.rstrip('/'), parsed.query, unquote(parsed.fragment))
    return ('local', str(target).casefold(), parsed.query, unquote(parsed.fragment))


def no_duplicates(links, source, docs):
    identities = [href_identity(link['href'], source, docs) for link in links]
    require(len(identities) == len(set(identities)), 'duplicate Related destination')


def is_answer_leaf(key):
    return (isinstance(key, str) and SOURCE_PATH.fullmatch(key) is not None
            and PurePosixPath(key).name != 'index.md')


def validate_answer_related_chapter(body, source, docs):
    """Part 7: Related itself needs 3-6 links and an actual Manual chapter."""
    docs, source = Path(docs).resolve(), Path(source).resolve()
    require(source.is_relative_to(docs), 'answer source escapes docs')
    require(is_answer_leaf(source.relative_to(docs).as_posix()), 'not an answer leaf')
    _, section, _ = related_parts(body)
    links = related_links(section)
    require(3 <= len(links) <= 6, 'answer Related must have three to six links')
    no_duplicates(links, source, docs)
    chapters = []
    for link in links:
        target = related_local_target(link['href'], source, docs)
        if target is not None and target.is_file() and target.suffix == '.md':
            meta, _ = source_body(canonical_source(target.read_bytes()))
            if meta.get('page_class') == 'chapter':
                chapters.append(target)
    require(bool(chapters), 'answer Related has no actual page_class: chapter')
    return tuple(chapters)


def transform_section(section, entry, source, docs):
    links = related_links(section)
    no_duplicates(links, source, docs)
    new_link = '[' + entry['label'] + '](' + entry['_chapter_href'] + ')'
    if entry['action'] == 'append':
        require(bool(links), 'empty original Related section')
        end = links[-1]['end']
        newline = '\r\r\n' if '\r\r\n' in section else '\r\n' if '\r\n' in section else '\n'
        result = section[:end] + newline + '- ' + new_link + section[end:]
    else:
        token = '[' + entry['replace_label'] + '](' + entry['replace_href'] + ')'
        require(sum(link['token'] == token for link in links) == 1,
                'replacement must match exactly one original Related link')
        result = section.replace(token, new_link, 1)
    after = related_links(result)
    require(3 <= len(after) <= 6, 'Related must have three to six links after repair')
    no_duplicates(after, source, docs)
    require(sum(link['href'] == entry['_chapter_href'] for link in after) == 1,
            'new chapter must appear exactly once')
    return result


def validate_entry(key, entry, docs):
    """Pure entry checks; runtime only reaches these through the finite map."""
    require(isinstance(entry, dict), 'entry must be an object')
    action = entry.get('action')
    require(action in {'append', 'replace'}, 'unknown action')
    require(set(entry) == FIELDS | (REPLACE_FIELDS if action == 'replace' else set()),
            'unknown or missing entry fields')
    for field in ('canonical_source_sha256', 'related_section_sha256'):
        require(isinstance(entry[field], str) and HEX.fullmatch(entry[field]), 'invalid hash: ' + field)
    source = safe_path(docs, key, SOURCE_PATH, 'answer path')
    chapter = safe_path(docs, entry['chapter_path'], CHAPTER_PATH, 'chapter path')
    plain_label(entry['label'])
    text = canonical_source(source.read_bytes())
    require(digest(text.encode('utf-8')) == entry['canonical_source_sha256'], 'stale full source: ' + key)
    meta, body = source_body(text)
    require(meta.get('page_class') == 'page' and meta.get('library_cluster') == PurePosixPath(key).parts[1],
            'answer metadata does not match its path')
    chapter_raw = chapter.read_bytes()
    chapter_meta, _ = source_body(canonical_source(chapter_raw))
    require(chapter_meta.get('page_class') == 'chapter', 'target is not a Manual chapter')
    prefix, section, suffix = related_parts(body)
    require(digest(section.encode('utf-8')) == entry['related_section_sha256'], 'stale Related section: ' + key)
    record = dict(entry)
    record['_chapter_href'] = posixpath.relpath(entry['chapter_path'], str(PurePosixPath(key).parent))
    require(record['_chapter_href'] == '../../' + entry['chapter_path'], 'wrong chapter relative route')
    if action == 'replace':
        plain_label(entry['replace_label'])
        require(isinstance(entry['replace_href'], str) and bool(entry['replace_href']), 'missing replacement href')
        require(entry['replace_href'] in INLINE_LINK.findall(prefix),
                'replacement destination must remain linked inline before Related')
    transformed = prefix + transform_section(section, record, source, docs) + suffix
    out_prefix, _, out_suffix = related_parts(transformed)
    require(out_prefix == prefix and out_suffix == suffix, 'repair escaped Related')
    record.update(_body=body, _source=source, _chapter=chapter,
                  _chapter_raw_sha256=digest(chapter_raw))
    return record


def validate_mapping(mapping, docs_dir):
    docs = Path(docs_dir).resolve()
    require(docs.is_dir(), 'docs directory missing')
    require(isinstance(mapping, dict) and set(mapping) == {'version', 'pages'}, 'unknown map fields')
    require(type(mapping['version']) is int and mapping['version'] == 1, 'unknown map version')
    pages = mapping['pages']
    require(isinstance(pages, dict) and len(pages) == EXPECTED_COUNT, 'map must contain exactly 94 entries')
    require(all(isinstance(key, str) and SOURCE_PATH.fullmatch(key) for key in pages), 'unsafe source key')
    key_hash = digest(json.dumps(sorted(pages), separators=(',', ':')).encode('utf-8'))
    require(key_hash == APPROVED_KEYS_SHA256, 'unknown or missing reviewed answer key')
    result = {}
    for key, entry in pages.items():
        try:
            result[key] = validate_entry(key, entry, docs)
        except (OSError, UnicodeError, ValueError) as error:
            raise ValueError('Finite Related repair for ' + key + ': ' + str(error)) from error
    counts = {action: sum(entry['action'] == action for entry in pages.values())
              for action in ('append', 'replace')}
    require(counts == {'append': 90, 'replace': 4}, 'reviewed action counts changed')
    return result


class FiniteChapterLinks:
    def __init__(self, docs_dir, map_path):
        self.docs = Path(docs_dir).resolve()
        raw = Path(map_path).read_bytes()
        mapping = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=unique_object)
        require(digest(raw) == APPROVED_MAP_SHA256, 'map differs from the reviewed bytes')
        self.entries = validate_mapping(mapping, self.docs)
        # Validate the complete collection before MkDocs renders any page.
        # The finite repair still changes only its reviewed94 sources; this
        # additional guard grants no new transformation or baseline exception.
        leaves = sorted(path for path in (self.docs / 'answers').glob('*/*.md')
                        if path.name != 'index.md')
        self.validated_answer_leaves = []
        for source in leaves:
            key = source.relative_to(self.docs).as_posix()
            _, body = source_body(canonical_source(source.read_bytes()))
            self.transform(key, body)
            self.validated_answer_leaves.append(key)
        self.validated_answer_leaves = tuple(self.validated_answer_leaves)

    def transform(self, key, markdown):
        if key not in self.entries:
            if is_answer_leaf(key):
                validate_answer_related_chapter(markdown, self.docs / key, self.docs)
            return markdown
        record = self.entries[key]
        current = canonical_source(record['_source'].read_bytes())
        require(digest(current.encode('utf-8')) == record['canonical_source_sha256'], 'source changed after pre-build: ' + key)
        require(digest(record['_chapter'].read_bytes()) == record['_chapter_raw_sha256'], 'chapter changed after pre-build')
        require(canonical_source(markdown.encode('utf-8')) == record['_body'],
                'MkDocs input differs from pinned source body: ' + key)
        prefix, section, suffix = related_parts(markdown)
        require(digest(canonical_source(section.encode('utf-8')).encode('utf-8')) == record['related_section_sha256'],
                'MkDocs Related differs from reviewed section: ' + key)
        result = prefix + transform_section(section, record, record['_source'], self.docs) + suffix
        out_prefix, _, out_suffix = related_parts(result)
        require(out_prefix == prefix and out_suffix == suffix, 'runtime repair escaped Related')
        validate_answer_related_chapter(result, record['_source'], self.docs)
        return result
