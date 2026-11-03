"""Private finite editorial runtime proposal. No network, source writes or baseline exceptions.

No hook calls this module. A caller must supply independently trusted input-file
digests. Compilation permits explicit private previews; publication defaults to
requiring fresh complete source/writing receipts and an approved footer/map.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import copy
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
import yaml

QUALIFIER = 'Observed answers on stated dates, not a ranking.'
FREE_CHECK_TOKEN = '[Free 10-question check (one engine)](https://audit.broadcastwell.com/)'
LIMIT_SENTENCE = "No email is needed; runs are limited per network and per day, and by the site's daily allowance."
HEX = re.compile(r'[0-9a-f]{64}')
LEAF = re.compile(r'answers/[a-z0-9-]+/[a-z0-9-]+\.md')
LINK = re.compile(r'(?<!!)\[([^\]]+)\]\(([^()\s]+)\)')


class OverlayError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise OverlayError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def utc_calendar_day():
    """Live-price checked_on is a UTC calendar date on Windows and CI alike."""
    return datetime.now(timezone.utc).date().isoformat()


def canonical(raw):
    return raw.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')


def key_hash(keys):
    return sha(json.dumps(sorted(keys), separators=(',', ':')).encode())


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_bound_json(path, expected_sha256):
    require(bool(HEX.fullmatch(str(expected_sha256))), 'Independent trusted input digest required')
    raw = Path(path).read_bytes()
    require(sha(raw) == expected_sha256, 'Trusted input bytes changed: ' + Path(path).name)
    return json.loads(raw.decode('utf-8-sig'), object_pairs_hook=unique_object)


@dataclass(frozen=True)
class TrustedInputs:
    """Values belong in the separately reviewed caller, never derived at startup."""
    canonical_pins_sha256: str
    related_map_sha256: str
    current_leaf_manifest_sha256: str
    published_keys_sha256: str
    published_count: int = 300
    body_entries_sha256: str | None = None
    footer_entries_sha256: str | None = None


class FiniteStage:
    """Adapter only; the separately reviewed original module stays unchanged."""
    def __init__(self, module, runtime):
        self.module, self.runtime = module, runtime

    def transform(self, path, body):
        return self.runtime.transform(path, body)

    def __getattr__(self, name):
        return getattr(self.module, name)


def opening_span(body):
    match = re.match(r'\A# [^\n]+\n\n(?P<opening>.+?)(?=\n\n|\Z)', body, re.S)
    require(match is not None, 'Expected one H1 followed by first answer paragraph')
    require(not match['opening'].startswith(('#', '- ', '|', '<')), 'First answer must be a plain paragraph')
    return match.start('opening'), match.end('opening')


def remove_exact_qualifier(body):
    """A single exact mandatory paragraph at the approved boundary, nothing else."""
    _, end = opening_span(body)
    required = '\n\n' + QUALIFIER
    require(body.count(QUALIFIER) == 1, 'Exactly one reputation qualifier required')
    require(body[end:].startswith(required + '\n\n'), 'Qualifier is not its own paragraph after the opening')
    return body[:end] + body[end + len(required):]


def next_step_span(body):
    headings = list(re.finditer(r'(?m)^## Next step$', body))
    prepared = list(re.finditer(r'(?m)^Prepared by the Broadcastwell team\.$', body))
    require(len(headings) == len(prepared) == 1, 'Expected one Next step and one prepared-by line')
    start, end = headings[0].end(), prepared[0].start()
    require(start < end, 'Byline must follow Next step')
    tail = body[end:]
    require(len(re.findall(r'(?m)^Page owner:[^\n]+Corrections: hello@broadcastwell\.com$', tail)) == 1, 'Expected exact owner/corrections byline')
    return start, end


def source_head(canonical_source, body):
    require(canonical_source.endswith(body), 'Source/body extraction differs')
    return canonical_source[:-len(body)]


def hrefs(text):
    return {href for _, href in LINK.findall(text)}


def mutation(body, start, old, new, kind, operations):
    require(body[start:start + len(old)] == old, 'Exact old span differs: ' + kind)
    result = body[:start] + new + body[start + len(old):]
    operations.append({'kind': kind, 'start': start, 'old': old, 'new': new,
                       'before_sha256': sha(body.encode()), 'after_sha256': sha(result.encode())})
    return result


def invert_operations(result, operations):
    for operation in reversed(operations):
        require(sha(result.encode()) == operation['after_sha256'], 'Inverse output hash differs')
        start, new = operation['start'], operation['new']
        require(result[start:start + len(new)] == new, 'Inverse exact new span differs')
        result = result[:start] + operation['old'] + result[start + len(new):]
        require(sha(result.encode()) == operation['before_sha256'], 'Inverse input hash differs')
    return result


class PublicationOverlay:
    @classmethod
    def compile(cls, docs_dir, *, canonical_pins, related_map,
                expected_current_leaf_manifest, trusted_inputs,
                finite_links, quality_module,
                reviewed_body_patches=None, neutral_footer_map=None,
                receipt_store=None):
        self = cls()
        self.docs = Path(docs_dir).resolve()
        self.finite = finite_links
        self.q = quality_module
        self.pins = read_bound_json(canonical_pins, trusted_inputs.canonical_pins_sha256)
        self.mapping = read_bound_json(related_map, trusted_inputs.related_map_sha256)
        self.leaf_manifest = read_bound_json(expected_current_leaf_manifest, trusted_inputs.current_leaf_manifest_sha256)
        self.body_entries = copy.deepcopy((reviewed_body_patches or {}).get('pages', {}))
        self.footer_entries = copy.deepcopy((neutral_footer_map or {}).get('pages', {}))
        self.receipt_store = dict(receipt_store or {})
        self.pending = []
        self._strict_current_passed = False
        self.metadata_consumers = {}
        self.records = {}
        self.target_stamps = {}
        for supplied, expected, label in [(reviewed_body_patches, trusted_inputs.body_entries_sha256, 'body patches/receipts'), (neutral_footer_map, trusted_inputs.footer_entries_sha256, 'neutral footer')]:
            if supplied is not None:
                require(bool(HEX.fullmatch(str(expected))) and sha(json.dumps(supplied, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()) == expected, 'Independent approved ' + label + ' input digest differs')
        published = self.pins.get('pages', {})
        require(len(published) == trusted_inputs.published_count, 'Published pin count differs')
        require(key_hash(published) == trusted_inputs.published_keys_sha256 == self.pins.get('keys_sha256'), 'Published exact key set differs')
        require(set(self.mapping.get('pages', {})) == set(published), 'Related map coverage differs from pinned published set')
        require(self.mapping.get('exact_page_count') == trusted_inputs.published_count, 'Related map count differs')
        require(self.mapping.get('exact_keys_sha256') == trusted_inputs.published_keys_sha256, 'Related map key digest differs')
        require(all(LEAF.fullmatch(path) and not path.endswith('/index.md') for path in published), 'Unsafe or non-leaf published key')
        require(set(self.body_entries) <= set(self.leaf_manifest.get('pages', {})), 'Body receipt/patch names unknown leaf')
        require(set(self.footer_entries) <= set(self.leaf_manifest.get('pages', {})), 'Footer names unknown leaf')
        if self.mapping.get('proposal_only') is not False:
            self.pending.append('Related map remains a private proposal without independent adoption')
        self._check_sources()
        for rel, note in sorted(self.leaf_manifest['pages'].items()):
            source = self.docs / rel
            raw = source.read_bytes()
            full = canonical(raw)
            meta, original_body = self.finite.source_body(full) if hasattr(self.finite, 'source_body') else self.q.split_markdown(full)
            # The original finite class does not expose the module helpers.
            stage_one = self.finite.transform(rel, original_body)
            operations = []
            body_entry = self.body_entries.get(rel, {})
            related_entry = self.mapping['pages'].get(rel)
            if related_entry:
                pin = published[rel]
                require(sha(full.encode()) == pin['canonical_source_sha256'] == related_entry['canonical_source_sha256'], rel + ': immutable canonical source pin differs')
                require(sha(stage_one.encode()) == pin['post_finite94_body_sha256'] == related_entry['post_finite94_body_sha256'], rel + ': finite94 stage differs')
                body = self._patch_body(rel, stage_one, body_entry, operations)
                _, end = opening_span(body)
                if QUALIFIER in body:
                    remove_exact_qualifier(body)
                else:
                    body = mutation(body, end, '', '\n\n' + QUALIFIER, 'mandatory-qualifier', operations)
                body = self._related(rel, body, related_entry, operations)
                footer_entry = self.footer_entries.get(rel)
                if footer_entry:
                    body = self._footer(rel, body, footer_entry, operations)
                else:
                    self.pending.append(rel + ': neutral footer entry missing')
            else:
                require(not body_entry.get('patches'), rel + ': pass-through source cannot receive unregistered body overlay')
                body = original_body
                footer_entry = self.footer_entries.get(rel)
                if footer_entry:
                    candidate = self._footer(rel, body, footer_entry, [])
                    require(candidate == body, rel + ': pass-through footer must already equal the approved neutral source')
                else:
                    self.pending.append(rel + ': approved direct-source neutral footer binding missing')
            self._validate_related(rel, body, related_entry or note.get('related_requirements', {}))
            original_primary = hrefs(stage_one.split('## Next step')[0])
            current_primary = hrefs(body.split('## Next step')[0])
            allowed_navigation = set((related_entry or {}).get('omitted_optional_sibling_hrefs', []))
            corrections = {item.get('old_url') for patch in body_entry.get('patches', []) for item in patch.get('fact_ledger', [])
                           if item.get('kind') == 'corrected_url' and item.get('new_url') in current_primary}
            require(original_primary - current_primary <= allowed_navigation | corrections, rel + ': body change loses unapproved primary evidence destination')
            raw_head = source_head(full, original_body)
            effective_meta = copy.deepcopy(meta)
            metadata_delta = body_entry.get('metadata_overlay', {})
            allowed_metadata = {'title', 'headline', 'description', 'also_asked_as', 'library_subtopic', 'date_modified'}
            require(set(metadata_delta) <= allowed_metadata, rel + ': protected metadata field cannot be overlaid')
            for field, change in metadata_delta.items():
                require(isinstance(change, dict) and set(change) == {'old', 'new'} and meta.get(field) == change['old'], rel + ': metadata old value differs')
                value = change['new']
                require((isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value)) if field == 'also_asked_as' else isinstance(value, str) and value.strip(), rel + ': malformed effective metadata value')
                if field == 'date_modified':
                    require(bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})', value)), rel + ': effective modification date must be explicit ISO time')
                effective_meta[field] = value
            if {'title', 'headline'} & set(metadata_delta) or body_entry.get('h1_overlay'):
                h1 = body.splitlines()[0].removeprefix('# ')
                require(effective_meta.get('title') == effective_meta.get('headline') == h1, rel + ': effective title/headline/H1 differ')
            effective_head = ('---\n' + yaml.safe_dump(effective_meta, allow_unicode=True, sort_keys=False).rstrip() + '\n---\n\n') if metadata_delta else raw_head
            effective_full = effective_head + body
            effective_sha = sha(effective_full.encode())
            inverse = invert_operations(body, operations)
            require(inverse == stage_one if related_entry else inverse == original_body, rel + ': exact stage inverse failed')
            record = {'path': rel, 'file': source, 'meta': effective_meta, 'cluster': effective_meta.get('library_cluster'),
                      'body': body, 'source_sha256': sha(raw),
                      'canonical_source_sha256': effective_sha,
                      'raw_canonical_source_sha256': sha(full.encode()),
                      'post_finite94_body_sha256': sha(stage_one.encode()),
                      'effective_canonical_source_sha256': effective_sha,
                      'effective_body_sha256': sha(body.encode()),
                      'effective_full_source': effective_full,
                      'raw_head': raw_head, 'effective_head': effective_head,
                      'raw_head_sha256': sha(raw_head.encode()), 'effective_head_sha256': sha(effective_head.encode()),
                      'raw_meta': meta, 'metadata_delta': metadata_delta,
                      'effective_meta_sha256': sha(json.dumps(effective_meta, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()),
                      'operations': operations, 'inverse_reconstructs_post_finite94': True}
            self.records[rel] = record
            reviews = body_entry.get('reviews', {})
            for review_kind in ['writing', 'source']:
                review_id = reviews.get(review_kind)
                if not self._article_receipt(review_id, record, review_kind):
                    self.pending.append(rel + ': fresh complete ' + review_kind + ' receipt missing or stale')
            record['review_ids'] = reviews
        return self

    def _check_sources(self):
        actual = {path.relative_to(self.docs).as_posix() for path in (self.docs / 'answers').glob('*/*.md') if path.name != 'index.md'}
        require(actual == set(self.leaf_manifest.get('pages', {})), 'Complete current leaf coverage differs')
        for rel, note in self.leaf_manifest['pages'].items():
            require(bool(LEAF.fullmatch(rel)) and not rel.endswith('/index.md'), 'Unsafe current leaf path')
            path = (self.docs / rel).resolve()
            require(path.is_relative_to(self.docs) and path.is_file(), 'Missing/escaped current source')
            require(sha(canonical(path.read_bytes()).encode()) == note['canonical_source_sha256'], rel + ': source changed since explicit leaf manifest')

    def _target(self, href, source):
        # Use the original module's resolver through the injected support object.
        return self.finite.related_local_target(href, source, self.docs)

    def _validate_related(self, rel, body, entry):
        source = self.docs / rel
        self.finite.validate_answer_related_chapter(body, source, self.docs)
        _, section, _ = self.finite.related_parts(body)
        links = self.finite.related_links(section)
        hub = (source.parent / 'index.md').resolve()
        targets, siblings = [], 0
        for item in links:
            target = self._target(item['href'], source)
            if target is None:
                continue
            require(target.is_file(), rel + ': missing local Related target')
            targets.append(target)
            target_digest = sha(target.read_bytes())
            require(target not in self.target_stamps or self.target_stamps[target] == target_digest, 'Related target changed during compile')
            self.target_stamps[target] = target_digest
            if target.is_relative_to(self.docs / 'answers') and target.name != 'index.md' and target != source:
                siblings += 1
        require(hub in targets, rel + ': Related lacks its own exact cluster hub')
        require(siblings <= 2, rel + ': Related has more than two sibling answers')
        if entry.get('chapter_path'):
            require((self.docs / entry['chapter_path']).resolve() in targets, rel + ': approved chapter differs')
        if entry.get('own_cluster_hub_path'):
            require((self.docs / entry['own_cluster_hub_path']).resolve() == hub, rel + ': wrong approved hub')
        if entry.get('index_applicable'):
            href = entry.get('required_index_href')
            parsed = urlsplit(str(href))
            require(parsed.scheme == 'https' and parsed.netloc == 'index.broadcastwell.com' and not parsed.path.endswith(('.csv', '.json', '.txt')), rel + ': applicable Index destination must be the reviewed HTML route')
            require(any(item['href'] == href for item in links), rel + ': approved applicable Index link missing')

    def _patch_body(self, rel, body, entry, operations):
        if not entry:
            return body
        require(entry.get('canonical_source_sha256') == self.pins['pages'][rel]['canonical_source_sha256'], rel + ': body revision raw pin differs')
        require(entry.get('post_finite94_body_sha256') == sha(body.encode()), rel + ': body patch stage differs')
        h1 = entry.get('h1_overlay')
        if h1:
            require(isinstance(h1, dict) and set(h1) == {'old', 'new'} and all(isinstance(value, str) and value.strip() and '\n' not in value for value in h1.values()), rel + ': malformed reviewed H1 overlay')
            old, new = '# ' + h1['old'], '# ' + h1['new']
            require(body.startswith(old + '\n'), rel + ': original H1 differs')
            body = mutation(body, 0, old, new, 'reviewed-h1', operations)
        for patch in entry.get('patches', []):
            old, new, start = patch.get('old'), patch.get('new'), patch.get('start')
            require(isinstance(old, str) and old and isinstance(new, str) and type(start) is int and start >= 0, rel + ': malformed literal body patch')
            require(body.count(old) == 1, rel + ': body patch old text must occur once')
            boundary = body.index('## Related')
            require(start + len(old) <= boundary and not old.startswith('# '), rel + ': body patch crosses protected boundary')
            require(sha(old.encode()) == patch.get('old_sha256') and sha(new.encode()) == patch.get('new_sha256'), rel + ': body patch text digest differs')
            require(isinstance(patch.get('fact_ledger'), list), rel + ': explicit fact ledger required')
            if re.findall(r'\d+(?:[.,]\d+)?', old) != re.findall(r'\d+(?:[.,]\d+)?', new):
                require(bool(patch['fact_ledger']), rel + ': numeric/date change lacks fact ledger')
            body = mutation(body, start, old, new, 'reviewed-body-patch', operations)
        require(sha(body.encode()) == entry.get('post_patches_body_sha256'), rel + ': body patch output differs')
        return body

    def _related(self, rel, body, entry, operations):
        prefix, old, suffix = self.finite.related_parts(body)
        require(sha(old.encode()) == entry['post_finite94_related_sha256'], rel + ': Related input span differs')
        new = entry['related_markdown']
        require(sha(new.encode()) == entry['related_markdown_sha256'], rel + ': Related output digest differs')
        before_evidence = hrefs(prefix + old)
        body = mutation(body, len(prefix), old, new, 'finite-related', operations)
        paragraph = entry.get('source_link_paragraph_before_related', '')
        require(not paragraph or (paragraph.startswith('Additional source: ') and paragraph.endswith('.\n\n') and '\n## ' not in paragraph and '<' not in paragraph), rel + ': malformed visible source preservation paragraph')
        if paragraph:
            body = mutation(body, len(prefix) - len('## Related'), '', paragraph, 'retained-source-link', operations)
        allowed_navigation = set(entry.get('omitted_optional_sibling_hrefs', []))
        for href in allowed_navigation:
            target = self._target(href, self.docs / rel)
            require(target is not None and target.is_file() and target.is_relative_to(self.docs / 'answers') and target.name != 'index.md', rel + ': omission is not an optional sibling')
        after_prefix, after_section, _ = self.finite.related_parts(body)
        lost = before_evidence - hrefs(after_prefix + after_section)
        require(lost <= allowed_navigation, rel + ': Related change loses an evidence destination')
        return body

    def _load_receipt(self, digest):
        if not isinstance(digest, str) or not HEX.fullmatch(digest) or digest not in self.receipt_store:
            return None
        raw = self.receipt_store[digest]
        if not isinstance(raw, bytes) or sha(raw) != digest:
            return None
        try:
            data = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_object)
        except (ValueError, UnicodeError):
            return None
        return data if isinstance(data, dict) else None

    def _article_receipt(self, digest, record, kind):
        data = self._load_receipt(digest)
        return bool(data and data.get('approved') is True and data.get('actual_full_read_complete') is True
                    and data.get('review_kind') == kind and data.get('scope') == 'full-effective-article'
                    and data.get('path') == record['path']
                    and data.get('canonical_source_sha256') == record['raw_canonical_source_sha256']
                    and data.get('effective_canonical_source_sha256') == record['effective_canonical_source_sha256'])

    def _footer(self, rel, body, entry, operations):
        start, end = next_step_span(body)
        old = body[start:end]
        require(sha(old.encode()) == entry.get('old_next_step_sha256'), rel + ': footer input changed')
        method = entry.get('method_token', '')
        require(method in old and bool(LINK.fullmatch(method)) and 'method' in LINK.fullmatch(method)[1].casefold(), rel + ': preserve the actual method token/scope')
        require(FREE_CHECK_TOKEN in old and LIMIT_SENTENCE in old, rel + ': existing free-check disclosure differs')
        offer = entry.get('offer', {})
        name, price, href = offer.get('name'), offer.get('price'), offer.get('href')
        require(isinstance(name, str) and bool(re.fullmatch(r'[A-Za-z][A-Za-z 0-9-]{1,70}', name)), rel + ': malformed neutral offer name')
        require(isinstance(price, str) and bool(re.fullmatch(r'\$[0-9,]+(?:\.[0-9]{2})?', price)), rel + ': malformed offer price')
        require(isinstance(href, str) and urlsplit(href).scheme == 'https' and urlsplit(href).netloc == 'broadcastwell.com', rel + ': offer URL must be approved HTTPS company route')
        price_receipt = self._load_receipt(offer.get('live_price_receipt_sha256'))
        price_ok = bool(price_receipt and price_receipt.get('approved') is True and price_receipt.get('review_kind') == 'live-offer-price'
                        and price_receipt.get('name') == name and price_receipt.get('price') == price and price_receipt.get('href') == href
                        and bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(price_receipt.get('checked_on', ''))))
                        and price_receipt['checked_on'] == utc_calendar_day())
        if not price_ok:
            self.pending.append(rel + ': matching offer live-price receipt missing or stale')
        correction = entry.get('free_correction_statement', '')
        require(isinstance(correction, str) and (not correction or (correction in old and 'free' in correction.casefold() and 'correct' in correction.casefold() and '<' not in correction)), rel + ': correction statement must preserve its actual old source span')
        blocks = [FREE_CHECK_TOKEN + '. ' + LIMIT_SENTENCE]
        if correction:
            blocks.append(correction)
        blocks.extend([method, name + ': [' + price + '](' + href + ').'])
        new = '\n\n' + '\n\n'.join(blocks) + '\n\n'
        return mutation(body, start, old, new, 'neutral-next-step', operations)

    def _check_unchanged(self):
        self._check_sources()
        for target, digest in self.target_stamps.items():
            require(target.is_file() and sha(target.read_bytes()) == digest, 'Related target changed after compile')
        for rel, record in self.records.items():
            require(sha(record['body'].encode()) == record['effective_body_sha256'], rel + ': compiled body mutated')
            require(sha(record['effective_full_source'].encode()) == record['effective_canonical_source_sha256'], rel + ': compiled effective source mutated')
            require(sha(json.dumps(record['meta'], sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()) == record['effective_meta_sha256'], rel + ': compiled effective metadata mutated')
            raw_full = canonical((self.docs / rel).read_bytes())
            _, original_body = self.finite.source_body(raw_full)
            require(record['raw_head'] == source_head(raw_full, original_body), rel + ': original metadata prefix changed')
            require(record['effective_full_source'] == record['effective_head'] + record['body'], rel + ': effective source/body mismatch')

    def transform_after_finite94(self, path, markdown, *, publication=True):
        if path not in self.records:
            require(not LEAF.fullmatch(path), 'Unregistered answer leaf')
            return markdown
        self._check_unchanged()
        record = self.records[path]
        require(sha(markdown.encode()) == record['post_finite94_body_sha256'], path + ': MkDocs input is not the exact finite94 stage')
        if publication:
            require(not self.pending, 'Publication blocked: ' + '; '.join(self.pending[:4]))
            if getattr(self,'s5_scope',None) is not None:
                from library_publication_eligibility import scope_for
                scope_for(self)
                require(getattr(self,'_eligible_current_passed',False) and not self._strict_current_passed,'Eligible current/frozen-preservation gate has not passed')
            else:require(self._strict_current_passed, 'Current rendered quality gate has not passed')
            require(not self.metadata_consumer_errors(), 'Effective metadata consumer proof incomplete')
        return record['body']

    def effective_pages(self):
        return copy.deepcopy(self.records)

    def effective_metadata(self, path):
        self._check_unchanged()
        require(path in self.records, 'Unknown effective metadata route')
        return copy.deepcopy(self.records[path]['meta'])

    def public_leaf_records(self):
        """Single effective input for hubs, llms and structured-data generators.

        No consumer is installed by this proposal. A release caller must pass
        these records to every public generator; raw source fallback is unsafe.
        """
        self._check_unchanged()
        return [{'path': rel, 'url': 'https://docs.broadcastwell.com/' + rel.removesuffix('.md') + '/',
                 **{field: copy.deepcopy(record['meta'].get(field)) for field in ['title', 'headline', 'description', 'also_asked_as', 'library_subtopic', 'date_modified']},
                 'effective_canonical_source_sha256': record['effective_canonical_source_sha256']}
                for rel, record in sorted(self.records.items())]

    def public_metadata_fingerprint(self):
        return sha(self.q.canonical_json(self.public_leaf_records()).encode())

    def register_metadata_consumer(self, name, consumed_fingerprint):
        """Caller supplies the fingerprint actually consumed by its generator.

        This is input consistency evidence; final output/build/served comparison
        still belongs to the release gate and is not proved by registration.
        """
        require(name in {'page-head-and-structured-data', 'library-hubs', 'llms'}, 'Unknown public metadata consumer')
        require(consumed_fingerprint == self.public_metadata_fingerprint(), 'Public generator consumed stale metadata')
        self.metadata_consumers[name] = consumed_fingerprint

    def metadata_consumer_errors(self):
        if not any(record['metadata_delta'] for record in self.records.values()):
            return []
        fingerprint = self.public_metadata_fingerprint()
        return ['Effective metadata consumer missing/stale: ' + name for name in ['page-head-and-structured-data', 'library-hubs', 'llms'] if self.metadata_consumers.get(name) != fingerprint]

    def receipts(self):
        return [{key: value for key, value in record.items() if key in {
            'path', 'raw_canonical_source_sha256', 'post_finite94_body_sha256',
            'effective_canonical_source_sha256', 'operations', 'inverse_reconstructs_post_finite94',
            'metadata_delta', 'raw_head_sha256', 'effective_head_sha256'}} for record in self.records.values()]


def enforce_frozen_articles(overlay, frozen_effective_pins):
    """Private preflight: preserving raw Markdown does not permit served edits."""
    overlay._strict_current_passed = False
    overlay._eligible_current_passed = False
    for rel, expected_effective_sha256 in frozen_effective_pins.items():
        require(rel in overlay.records, 'Frozen library route is missing: ' + rel)
        if overlay.records[rel]['effective_canonical_source_sha256'] != expected_effective_sha256:
            overlay.pending.append(rel + ': field-test frozen served content would change')


def qualitative_observation_key(binding, q):
    record = binding.get('record')
    require(isinstance(record, dict) and record and set(record) <= q.RECORD_FIELDS, 'Qualitative observation needs controlled published record fields')
    require(all(isinstance(value, str) and value.strip() for value in record.values()), 'Qualitative record values must be explicit strings')
    require({'capture_date', 'subject', 'metric'} <= set(record), 'Qualitative observation lacks dated subject/metric identity')
    identity = {'source': q.source_key(binding.get('source_url', '')), 'record': {key: q.normalized(value) for key, value in sorted(record.items())}}
    return 'observation:' + sha(q.canonical_json(identity).encode()), identity


def validate_current_annotations(overlay, pages, metadata):
    """Raw validator stays intact; qualitative current leads have a separate proof."""
    q = overlay.q
    q.public_metadata(metadata)
    require(set(metadata) <= q.METADATA_FIELDS, 'Unknown current annotation fields')
    require(set(metadata.get('pages', {})) == set(pages), 'Current annotations must cover every effective leaf')
    notes = metadata['pages']
    qualitative = {rel for rel, note in notes.items() if not note.get('lead_figures')}
    numeric_metadata = copy.deepcopy(metadata)
    numeric_metadata['pages'] = {rel: note for rel, note in notes.items() if rel not in qualitative}
    q.validate_annotations({rel: page for rel, page in pages.items() if rel not in qualitative}, numeric_metadata)
    qualitative_keys = {}
    numeric_cuts = set()
    for figure in metadata.get('figures', {}).values():
        identity = q.figure_descriptor(figure)
        identity.pop('count'); identity.pop('base'); identity.pop('unit')
        numeric_cuts.add(q.canonical_json(identity))
    for rel in qualitative:
        note, page = notes[rel], pages[rel]
        require(set(note) <= q.PAGE_FIELDS | {'qualitative_opening'}, rel + ': unknown qualitative annotation fields')
        require(note.get('lead_figures') == [] and note.get('lead_figure_spans') == {}, rel + ': qualitative lead cannot mint a fake numeric figure')
        bank_ids = set(re.findall(r'\bLB-Q\d{4}\b', str(page['meta'].get('demand_evidence', ''))))
        require(len(bank_ids) == 1 and note.get('bank_id') in bank_ids, rel + ': qualitative bank binding differs')
        require(bool(HEX.fullmatch(str(note.get('source_sha256')))) and note.get('canonical_source_sha256') == page['canonical_source_sha256'], rel + ': qualitative effective source binding differs')
        require(note.get('opening_sha256') == page['opening_sha256'] and note.get('classification_reason'), rel + ': qualitative opening classification differs')
        require(note.get('opening_shape') in metadata['cluster_plans'][page['cluster']], rel + ': qualitative shape outside actual plan')
        frozen=rel in getattr(getattr(overlay,'s5_scope',None),'frozen',())
        if not frozen:
            for kind in ['source', 'writing']:
                require(overlay._article_receipt(note.get(kind + '_review_sha256'), page, kind), rel + ': qualitative full-page ' + kind + ' receipt missing')
        binding = note.get('qualitative_opening', {})
        require(set(binding) == {'source_url', 'record', 'source_quote', 'opening_span', 'observation_key', 'independent_receipt_sha256'}, rel + ': qualitative lead requires exact observation/quote/span/receipt fields')
        require(isinstance(binding['source_quote'], str) and binding['source_quote'].strip(), rel + ': exact published observation quote missing')
        require(isinstance(binding['opening_span'], str) and binding['opening_span'] and binding['opening_span'] in page['opening'], rel + ': qualitative fact is not in the actual opening')
        observation_key, identity = qualitative_observation_key(binding, q)
        require(binding['observation_key'] == observation_key, rel + ': qualitative observation identity differs')
        require(q.canonical_json(identity) not in numeric_cuts, rel + ': qualitative mode disguises a registered aggregate quantitative fact')
        receipt = overlay._load_receipt(binding['independent_receipt_sha256'])
        require(bool(receipt and receipt.get('approved') is True and receipt.get('review_kind') == 'qualitative-opening-observation'
                     and receipt.get('scope') == 'exact-published-observation' and receipt.get('not_reworded_aggregate') is True
                     and receipt.get('path') == rel and receipt.get('canonical_source_sha256') == page['raw_canonical_source_sha256']
                     and receipt.get('effective_canonical_source_sha256') == page['effective_canonical_source_sha256']
                     and receipt.get('observation_key') == observation_key and receipt.get('source_quote_sha256') == sha(binding['source_quote'].encode())
                     and receipt.get('opening_span_sha256') == sha(binding['opening_span'].encode())), rel + ': independent qualitative observation approval missing or stale')
        qualitative_keys[rel] = observation_key
    return notes, qualitative_keys


def current_comparison_prose(effective_body, quality_module):
    return quality_module.comparison_prose(remove_exact_qualifier(effective_body))


def run_current_rendered_quality(overlay, *, current_annotations, trusted_index_references_sha256):
    """Fresh effective-source analysis. Deliberately never calls apply_baseline."""
    if getattr(overlay,'s5_scope',None) is not None:
        from library_publication_release import assess_current_records
        report=assess_current_records(overlay,current_annotations=current_annotations,trusted_index_references_sha256=trusted_index_references_sha256)
        overlay._strict_current_passed=False
        overlay._eligible_current_passed=report['eligible_completion_passed']
        return report
    overlay._check_unchanged()
    overlay._strict_current_passed = False
    q = overlay.q
    errors = list(overlay.pending)
    errors.extend(overlay.metadata_consumer_errors())
    pages = {}
    for rel, record in overlay.records.items():
        page = dict(record)
        try:
            comparable = current_comparison_prose(page['body'], q)
            overlay._validate_related(rel, page['body'], overlay.mapping['pages'].get(rel) or overlay.leaf_manifest['pages'][rel].get('related_requirements', {}))
        except ValueError as error:
            errors.append(rel + ': ' + str(error))
            comparable = q.comparison_prose(page['body'])
        opening = q.paragraph_after_heading(page['body']).strip()
        page.update(opening=opening, opening_sha256=sha(opening.encode()),
                    six=q.sequences(q.words(comparable), 6), eight=q.sequences(q.words(q.comparison_prose(opening)), 8))
        pages[rel] = page
    try:
        notes, qualitative_keys = validate_current_annotations(overlay, pages, current_annotations)
        for rel, page in pages.items():
            page['quality_annotation'] = notes[rel]
            for kind in ['source', 'writing']:
                require(notes[rel][kind + '_review_sha256'] == page['review_ids'].get(kind), rel + ': current quality receipt differs from full effective review')
        references = current_annotations.get('index_question_titles', {})
        require(sha(q.canonical_json(references).encode()) == trusted_index_references_sha256, 'Published Index title snapshot changed')
        require(len(references.get('records', [])) == 140 and len({row['url'] for row in references['records']}) == 140, 'Exactly140 unique Index title references required')
        orders, hub_errors = q.hub_orders(overlay.docs, pages)
        analysis = q.analyze(pages, notes, orders, references['records'], overlay.docs)
        for observation_key in sorted(set(qualitative_keys.values())):
            paths = sorted(rel for rel, key in qualitative_keys.items() if key == observation_key)
            if len(paths) > 3:
                analysis['violations'].append({'kind': 'qualitative_lead_limit', 'observation_key': observation_key, 'pages': paths, 'count': len(paths)})
        errors.extend(hub_errors)
        errors.extend(analysis['violations'])
    except (KeyError, TypeError, ValueError) as error:
        errors.append('Fresh effective annotations invalid: ' + str(error))
        analysis = {'violations': []}
    overlay._strict_current_passed = not errors
    return dict(analysis, passed=not errors, errors=errors, leaf_count=len(pages),
                grandfathered_cases=[], current_baseline_exceptions=0,
                publication_receipts_complete=not overlay.pending,
                policy='Current effective articles only; unchanged raw baseline is separate history.')
