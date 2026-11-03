"""Finite six reviewed readings of historical public company-panel records.

Offline and immutable by default. This is not the separate answer study,
an engine test, a complete-transcript claim, or a current security assessment.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

KIND = 'published-company-panel'
SOURCE = 'https://index.broadcastwell.com/php2shell/'
METHOD_URL = SOURCE + '#faq'
METHOD_LABEL = 'Company-panel grades and dated records.'
REGISTRY_PATH = 'library_company_panel_six.json'
REGISTRY_SHA256 = '7e23ed49831997fce81b65b7248ef8f3bc3eb58bbee63655e2064628f83dc995'
PUBLIC_SOURCES = {
    SOURCE+'data/ai-answers.json': '0026e2318308be9f6ae19a378ceb80d2a94d89a0c8f840e290665cf3bf005302',
    SOURCE+'data/statements.json': 'aa7c04950da978381e6ef57dcf8382aa28d2c262be25a4996e7ac75315cb61d9',
}
HEX = re.compile(r'[0-9a-f]{64}')
NEUTRAL_OFFER = 'Answer Repair: [$490](https://broadcastwell.com/answer-repair).'


def _need(ok, message):
    if not ok:
        raise ValueError('company-panel: '+message)


def _sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def _unique(pairs):
    result = {}
    for key, value in pairs:
        _need(key not in result, 'duplicate registry key')
        result[key] = value
    return result


def canonical_body(body):
    # split_markdown preserves the blank line after frontmatter. No other
    # whitespace/content normalization can make an unreviewed body pass.
    return body.replace('\r\n', '\n').replace('\r', '\n').lstrip('\n')


def load_registry(docs):
    data = json.loads((Path(docs).parent/'tools'/REGISTRY_PATH).read_text(encoding='utf-8-sig'), object_pairs_hook=_unique)
    _need(_sha(_canonical(data)) == REGISTRY_SHA256, 'registry differs from exact independently reviewed six-case pins')
    _validate_registry(data)
    return data


def _match(url, unit, target):
    parsed = urlsplit(url)
    host = parsed.hostname or ''
    if host.startswith('www.'):
        host = host[4:]
    return (host if unit == 'host' else host+parsed.path) == target


def _validate_registry(data):
    _need(data['schema_version'] == 1 and data['evidence_kind'] == KIND, 'registry kind/schema mismatch')
    _need(data['public_source_sha256'] == PUBLIC_SOURCES, 'wrong public source URL/hash')
    _need((data['source_url'], data['method_url'], data['method_label']) == (SOURCE, METHOD_URL, METHOD_LABEL), 'wrong public method')
    _need(len(data['cases']) == 6, 'registry must contain exactly the finite six cases')
    # Defense beyond the whole registry hash: projections have no local paths,
    # private case IDs, prompts, model-version fields or host/agent context.
    encoded = _canonical(data)
    _need(not re.search(r'PRIVATE-S6|\b[A-Za-z]:[\\/]|/root/|"(?:prompt|model_version|local_path|private_packet)"', encoded, re.I), 'private execution fields in public registry')
    for key, record in data['answer_records'].items():
        _need(key == record['record_key'] == '|'.join((record['company_slug'], record['engine'], record['captured_at_utc'])), 'wrong answer identity/date')
        _need(record['excerpt_sha256'] == _sha(record['excerpt']), 'wrong public excerpt hash')
        _need(record['public_asset_URL'] == SOURCE+'data/ai-answers.json', 'wrong answer asset')
    for key, record in data['statement_records'].items():
        _need(key == record['record_key'], 'wrong statement identity')
        _need(record['excerpt_sha256'] == (_sha(record['excerpt']) if record['excerpt'] is not None else None), 'wrong statement excerpt hash')
        _need(record['public_asset_URL'] == SOURCE+'data/statements.json', 'wrong statement asset')
    identities = {}
    for case in data['cases'].values():
        opening = case['opening']
        _need(opening['sha256'] == _sha(opening['literal']) and opening['complete_body_sha256'] == case['body_sha256'], 'wrong opening/body binding')
        for receipt in case['source_review_receipts']+case['writing_review_receipts']:
            _need(bool(HEX.fullmatch(receipt)), 'missing actual independent review receipt pin')
        _need(bool(HEX.fullmatch(case['independent_writing_review_sha256'])), 'independent full-current writing peer missing')
        _need(case['opening_shape'] and case['classification_reason'], 'actual independent opening classification missing')
        records = [data['answer_records'][key] for key in case['record_keys']]
        _need(len(records) == len(set(case['record_keys'])), 'duplicated selected answer')
        for quote in case['quotes']:
            _need(_sha(quote['literal']) == quote['sha256'] and quote['source_matches'], 'wrong quotation binding')
            for match in quote['source_matches']:
                source = data['answer_records'][match['record_key']]
                left, right = match['excerpt_start_Unicode_codepoint'], match['excerpt_end_Unicode_codepoint']
                _need(source['excerpt_sha256'] == match['excerpt_sha256'] and source['excerpt'][left:right] == quote['literal'], 'quotation differs from exact public excerpt/span')
        for item in case['numeric_leads']:
            _need(item['match_unit'] in {'host', 'path'}, 'unsupported numeric cut unit')
            f = item['figure']
            _need(f['record']['metric'] == item['observation_key'] and f['record']['subject'] == item['target'], 'numeric cut identity was reminted')
            selected = [r for r in records if not r['excluded']]
            _need(f['base'] == len(selected) == 5 and type(f['count']) is int, 'numeric cut needs its actual five-record population')
            members = [{'engine':r['engine'], 'captured_at_utc':r['captured_at_utc'], 'literal_matched_URLs':[u for u in r['cited_urls'] if _match(u, item['match_unit'], item['target'])]} for r in selected]
            members = [m for m in members if m['literal_matched_URLs']]
            _need(members == item['members'] and len(members) == f['count'], 'numeric cut/member count differs from exact printed path/host records')
            _need(all(r['captured_at_utc'][:10] == f['record']['capture_date'] for r in selected), 'wrong numeric capture date')
            identity = _canonical({k:item[k] for k in ('match_unit', 'target', 'members')})
            old = identities.setdefault(item['observation_key'], identity)
            _need(old == identity, 'one observation key has conflicting numeric meanings')
        for item in case['qualitative_leads']:
            _need(item['kind'] in {'qualitative_comparison', 'qualitative_chronology', 'qualitative_source_reading'}, 'unreviewed qualitative kind')
            _need('count' not in item and 'base' not in item and item['source_quotes_or_exact_fields'], 'qualitative observation cannot be a fake numeric cut')
            identity = _canonical(item['source_quotes_or_exact_fields'])
            old = identities.setdefault(item['observation_key'], identity)
            _need(old == identity, 'shared qualitative observation was reminted')


def _validate_case(meta, body, data):
    _need(meta.get('evidence_kind') == KIND, 'wrong evidence kind')
    _need(meta.get('is_based_on') == SOURCE, 'wrong primary public panel source')
    _need(set(meta.get('evidence_method_receipts', [])) == {METHOD_URL, *PUBLIC_SOURCES} and len(meta['evidence_method_receipts']) == 3, 'wrong company-panel method receipts')
    _need(not any(k.startswith(('evidence_audit_', 'evidence_list_audit_', 'evidence_documentation_')) for k in meta), 'unrelated evidence binding')
    key = meta.get('evidence_case')
    _need(key in data['cases'], 'unknown/off-registry case')
    case = data['cases'][key]
    body = canonical_body(body)
    _need(_sha(body) == case['body_sha256'], 'body changed after exact full Source/Writer binding')
    span = case['opening']
    _need(body[span['start_Unicode_codepoint']:span['end_Unicode_codepoint']] == span['literal'], 'wrong actual opening span')
    for quote in case['quotes']:
        _need(all(body[offset:offset+len(quote['literal'])] == quote['literal'] for offset in quote['page_offsets']), 'wrong page quotation span')
    _need(body.count(f'[{METHOD_LABEL}]({METHOD_URL})') == 1, 'wrong company-specific footer method')
    next_step = body.split('## Next step\n', 1)
    _need(len(next_step) == 2 and next_step[1].splitlines().count(NEUTRAL_OFFER) == 1, 'wrong exact neutral paid-offer line')
    _need(all(url in body for url in PUBLIC_SOURCES), 'published source links missing')
    return case


def validate_company_panel(meta, body, docs):
    try:
        _validate_case(meta, body, load_registry(docs))
        return []
    except (OSError, ValueError, KeyError, TypeError) as error:
        return [str(error)]


def expected_figures(case, figure_key):
    return {figure_key(item['figure']):item['figure'] for item in case['numeric_leads']}


def validate_annotation(page, note, figures, figure_key):
    """Same immutable six-case source binding; never a caller supplied allowlist."""
    docs = Path(page['file']).parents[2]
    case = _validate_case(page['meta'], page['body'], load_registry(docs))
    expected = expected_figures(case, figure_key)
    _need(note.get('lead_figures') == list(expected), 'numeric leads differ from true source-bound cuts; no fake count-one qualitative figure')
    _need(all(figures.get(k) == record for k, record in expected.items()), 'wrong numeric source/date/unit/count/base/review binding')
    observations = [item['observation_key'] for item in case['qualitative_leads']]
    _need(note.get('lead_observations') == observations, 'wrong qualitative observation keys')
    _need(note.get('lead_observation_spans') == {key:[case['opening']['literal']] for key in observations}, 'qualitative opening needs its exact independently source-bound span')
    _need(note.get('lead_figure_spans') == {key:[case['opening']['literal']] for key in expected}, 'wrong numeric opening spans')
    _need(note.get('source_review_sha256') == case['source_review_receipts'][-1], 'wrong actual source-review continuation')
    _need(note.get('writing_review_sha256') == case['independent_writing_review_sha256'], 'wrong actual independent writing peer binding')
    _need(note.get('opening_shape') == case['opening_shape'] and note.get('classification_reason') == case['classification_reason'], 'opening classification differs from actual independent peer')
    _need(bool(expected) != bool(observations), 'case must have the approved numeric or qualitative lead mode')
