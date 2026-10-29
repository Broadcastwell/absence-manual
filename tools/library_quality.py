"""LIBRARY 416 checks. No network, page edits or automatic new exceptions."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import hashlib
import html
from itertools import combinations
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlsplit

try:
    from tools.library_answers import (CLUSTER_OWNERS, DEFAULT_METHOD_LABEL,
        SCOPED_METHOD_LABEL, LIMIT_SENTENCE, leaf_answers, paragraph_after_heading,
        plain_text, resolve_local_link, split_markdown)
except ModuleNotFoundError:
    from library_answers import (CLUSTER_OWNERS, DEFAULT_METHOD_LABEL,
        SCOPED_METHOD_LABEL, LIMIT_SENTENCE, leaf_answers, paragraph_after_heading,
        plain_text, resolve_local_link, split_markdown)

ROOT = Path(__file__).resolve().parents[1]
# Filled only after the independently audited150-leaf snapshot is frozen.
FROZEN_WAVE_ONE_SNAPSHOT_SHA256 = '1caaae45e7ee80e0ac23a84cb17754bd9c3c0a0e136f7a417d46380f2ad7f7a2'
FROZEN_WAVE_ONE_BASELINE_SHA256 = '0cd78fbde5e1a7b6a6291bdf2bf8f9169d0744246953102469433a666056292e'
RECORD_FIELDS = {'category', 'engine', 'question', 'run', 'subject', 'metric',
                 'event_date', 'capture_date', 'cohort', 'release'}
LINK = re.compile(r'!?\[([^\]]*)\]\([^)]*\)')
HTML_LINK = re.compile(r'<a\b[^>]*>.*?</a>', re.I|re.S)
HEX = re.compile(r'[0-9a-f]{64}')
METADATA_FIELDS = {'schema_version','shape_definitions','cluster_plans','figures','pages','index_question_titles'}
PAGE_FIELDS = {'bank_id','source_sha256','opening_sha256','opening_shape','classification_reason',
               'canonical_source_sha256','writing_review_sha256','source_review_sha256','lead_figures','lead_figure_spans'}
FIGURE_FIELDS = {'source_url','record','count','base','unit','label','source_review_sha256'}


def public_metadata(value):
    """Reject private audit fields and host/agent paths from committed inputs."""
    if isinstance(value,str):
        require(not re.search(r'(?:\b[A-Za-z]:[\\/]|/root/|\bthread[_ -]?id\b)',value,re.I), 'Private host/agent/thread context is not quality metadata')
    elif isinstance(value,dict):
        for key,item in value.items():
            public_metadata(key);public_metadata(item)
    elif isinstance(value,list):
        for item in value:public_metadata(item)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(value).hexdigest()


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: '+key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=reject_duplicate_keys)


def normalized(value):
    value = unicodedata.normalize('NFKC', html.unescape(str(value))).casefold()
    return ' '.join(value.replace('\u2019', "'").replace('\u2018', "'").split())


def words(value):
    value = normalized(value)
    value = re.sub(r'(?<=\d),(?=\d)', '', value)
    return tuple(re.findall(r"\d+(?:\.\d+)?|[^\W\d_]+(?:'[^\W\d_]+)*", value, re.UNICODE))


def title_key(value):
    value = re.sub(r'^chapter\s+\d+\s*[:.\-]?\s*', '', normalized(plain_text(str(value))))
    return ' '.join(words(value))


def sequences(tokens, size):
    return {tuple(tokens[i:i+size]) for i in range(len(tokens)-size+1)}


def comparison_prose(body):
    """Remove only the brief's named fixed material, never ordinary sections."""
    body = re.split(r'(?im)^##\s+Next step\s*$', body, maxsplit=1)[0]
    body = re.sub(r'(?im)^Prepared by the Broadcastwell team\.\s*$', '', body)
    body = re.sub(r'(?im)^Page owner:[^\n]*Corrections: hello@broadcastwell\.com\s*$', '', body)
    for sentence in (DEFAULT_METHOD_LABEL, SCOPED_METHOD_LABEL, LIMIT_SENTENCE):
        body = body.replace(sentence, '')
    # Link labels AND destinations are absent from this comparison only.
    body = LINK.sub(' ', body)
    body = HTML_LINK.sub(' ', body)
    return plain_text(body)


def source_key(value):
    value = normalized(value).rstrip('/')
    match = re.fullmatch(r'(?:https?://(?:dx\.)?doi\.org/|doi:)?(10\.\d+/\S+)', value)
    if match:
        return 'doi:'+match[1]
    parsed = urlsplit(value)
    require(parsed.scheme == 'https' and bool(parsed.netloc), 'Figure source must be a published DOI or HTTPS URL')
    return parsed._replace(fragment='').geturl()


def exact_number(value):
    require(not isinstance(value, bool) and value is not None, 'Missing or Boolean figure count/base')
    text = str(value).strip().replace(',', '')
    try:
        number = Fraction(text) if '/' in text else Fraction(Decimal(text))
    except (ValueError, ZeroDivisionError, InvalidOperation):
        raise ValueError('Invalid exact figure number: '+text)
    require(number >= 0, 'Negative count/base')
    return str(number)


def figure_descriptor(record):
    require(isinstance(record, dict), 'Figure record must be an object')
    cut = record.get('record')
    require(isinstance(cut, dict) and cut and set(cut) <= RECORD_FIELDS, 'Figure needs a controlled published record/cut')
    require(cut.get('metric') and cut.get('subject'), 'Figure cut needs metric and subject')
    require(all(isinstance(v, str) and v.strip() for v in cut.values()), 'Figure cut values must be named strings')
    require(record.get('unit') and record.get('label'), 'Figure needs unit and readable label')
    count = exact_number(record.get('count'))
    base = exact_number(record['base']) if record.get('base') is not None else None
    require(base is None or Fraction(base) > 0, 'Figure base must be positive')
    def cut_value(key,value):
        value = normalized(value)
        if key in {'capture_date','event_date'} and '|' in value:
            value = '|'.join(sorted(set(value.split('|'))))
        return value
    return {'source': source_key(record.get('source_url', '')),
            'record': {k: cut_value(k,v) for k,v in sorted(cut.items())},
            'count': count, 'base': base, 'unit': normalized(record['unit'])}


def figure_key(record):
    identity = figure_descriptor(record)
    # The source metric/cut supplies the population. Renaming its unit cannot
    # mint another allowance for the same count, base and published fact.
    identity.pop('unit')
    return 'figure:'+digest(canonical_json(identity).encode('utf-8'))


def load_pages(docs):
    docs = Path(docs)
    result = {}
    for path in leaf_answers(docs):
        raw = path.read_bytes()
        text = raw.decode('utf-8-sig').replace('\r\n','\n').replace('\r','\n')
        meta, body = split_markdown(text)
        rel = path.relative_to(docs).as_posix()
        opening = paragraph_after_heading(body).strip()
        result[rel] = {'path': rel, 'file': path, 'cluster': meta.get('library_cluster'),
            'meta': meta, 'body': body, 'source_sha256': digest(raw),
            'canonical_source_sha256': digest(text.encode('utf-8')),
            'opening': opening, 'opening_sha256': digest(opening.encode('utf-8')),
            'six': sequences(words(comparison_prose(body)), 6),
            'eight': sequences(words(comparison_prose(opening)), 8)}
    return result


def hub_orders(docs, pages):
    result, errors = {}, []
    for cluster in sorted({p['cluster'] for p in pages.values()}):
        hub = Path(docs)/'answers'/cluster/'index.md'
        require(hub.is_file(), 'Cluster hub missing: '+cluster)
        _, body = split_markdown(hub.read_text(encoding='utf-8'))
        ordered = []
        for href in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', body):
            target = resolve_local_link(href, hub, docs)
            if target is None:
                continue
            try:
                rel = target.relative_to(Path(docs).resolve()).as_posix()
            except ValueError:
                continue
            if rel in pages and pages[rel]['cluster'] == cluster:
                if rel in ordered:
                    errors.append('Cluster hub lists a leaf twice: '+rel)
                else:
                    ordered.append(rel)
        expected = {k for k,p in pages.items() if p['cluster'] == cluster}
        if set(ordered) != expected:
            errors.append('Cluster hub leaf coverage differs: '+cluster)
        result[cluster] = ordered
    return result, errors


def fact(kind, pages, **details):
    names = sorted(pages)
    return {'kind': kind, 'pages': names, 'key': kind+':'+digest(canonical_json(names).encode()), **details}


def uniqueness(pages, docs, references):
    result, fields = [], defaultdict(list)
    for rel,p in pages.items():
        for field in ('title', 'headline', 'description'):
            key = title_key(p['meta'].get(field, ''))
            require(key, rel+': missing '+field)
            fields[key].append((rel, field))
    for key,items in fields.items():
        paths = sorted({rel for rel,_ in items})
        if len(paths) > 1:
            result.append(fact('metadata_duplicate', paths, normalized_text=key, fields=sorted(items)))
    reference_titles = []
    for path in sorted(Path(docs).rglob('*.md')):
        if path.is_relative_to(Path(docs)/'answers'):
            continue
        meta, body = split_markdown(path.read_text(encoding='utf-8-sig'))
        if meta.get('page_class') == 'chapter':
            values = [meta.get('title'), meta.get('headline')]+re.findall(r'(?m)^# (.+)$', body)
            reference_titles += [(title_key(v), path.relative_to(docs).as_posix(), 'Manual chapter') for v in values if v]
    require(isinstance(references, list), 'Index question title snapshot missing')
    for record in references:
        require(record.get('title') and record.get('url'), 'Index question reference needs title and URL')
        for title in {record['title'],record.get('html_title',record['title'])}:
            reference_titles.append((title_key(title), record['url'], 'Index question'))
    for key, target, scope in sorted(set(reference_titles)):
        for rel,field in fields.get(key, []):
            result.append(fact('reference_title_duplicate', [rel], field=field, reference=target, scope=scope))
    titles = defaultdict(set)
    for rel,p in pages.items():
        for field in ('title', 'headline'):
            titles[title_key(p['meta'][field])].add(rel)
    for rel,p in pages.items():
        aliases = p['meta'].get('also_asked_as', [])
        if isinstance(aliases, str):
            aliases = [v.strip() for v in aliases.split('|') if v.strip()]
        for alias in aliases:
            for other in sorted(titles[title_key(alias)]-{rel}):
                result.append(fact('alias_title_duplicate', [rel,other], alias=str(alias), alias_owner=rel))
    # Case keys also include the precise field/reference/alias, not merely page IDs.
    for row in result:
        row['key'] = row['kind']+':'+digest(canonical_json({k:v for k,v in row.items() if k!='key'}).encode())
    return result


def analyze(pages, annotations, orders, references, docs):
    violations, highest, within = [], {}, {}
    for rel,p in pages.items():
        require(p['six'], rel+': fewer than six comparable words')
    for left,right in combinations(sorted(pages), 2):
        a,b = pages[left],pages[right]
        shared = a['six'] & b['six']
        denominator = min(len(a['six']),len(b['six']))
        pair = {'pages':[left,right], 'shared_sequences':len(shared), 'smaller_sequence_set':denominator,
                'score_fraction':str(Fraction(len(shared),denominator)), 'score_percent':float(Fraction(100*len(shared),denominator))}
        for cluster in {a['cluster'],b['cluster']}:
            if cluster not in highest or Fraction(pair['score_fraction']) > Fraction(highest[cluster]['score_fraction']):
                highest[cluster] = pair
        if a['cluster'] == b['cluster'] and (a['cluster'] not in within or Fraction(pair['score_fraction']) > Fraction(within[a['cluster']]['score_fraction'])):
            within[a['cluster']] = pair
        if len(shared)*5 > denominator:
            violations.append(fact('six_word_similarity', [left,right], **{k:v for k,v in pair.items() if k!='pages'}))
        shared_opening = a['eight'] & b['eight']
        if shared_opening:
            violations.append(fact('eight_word_opening', [left,right], shared_sequences=sorted(' '.join(v) for v in shared_opening)))
    shapes, figure_pages = {}, defaultdict(list)
    for cluster,order in sorted(orders.items()):
        counts = Counter(annotations[rel]['opening_shape'] for rel in order)
        shapes[cluster] = {'total':len(order), 'used_shapes':len(counts), 'counts':dict(sorted(counts.items())),
                           'one_fifth_floor':len(order)//5}
        for left,right in zip(order,order[1:]):
            if annotations[left]['opening_shape'] == annotations[right]['opening_shape']:
                violations.append(fact('opening_adjacency', [left,right], cluster=cluster, shape=annotations[left]['opening_shape'], hub_order_pair=[left,right]))
        for shape,count in sorted(counts.items()):
            if count*5 > len(order):
                paths = [rel for rel in order if annotations[rel]['opening_shape']==shape]
                row = fact('opening_concentration', paths, cluster=cluster, shape=shape, count=count, total=len(order))
                row['key'] = 'opening_concentration:'+cluster+':'+shape
                violations.append(row)
    for rel,note in annotations.items():
        for figure in set(note['lead_figures']):
            figure_pages[figure].append(rel)
    for figure,paths in sorted(figure_pages.items()):
        if len(paths)>3:
            row = fact('lead_figure_limit', paths, figure=figure, count=len(paths))
            row['key'] = 'lead_figure_limit:'+figure
            violations.append(row)
    violations.extend(uniqueness(pages,docs,references))
    return {'violations':violations, 'highest_pair_per_cluster':highest,
            'highest_within_cluster_pair':within, 'opening_distributions':shapes,
            'lead_figure_pages':dict(sorted(figure_pages.items()))}


def validate_annotations(pages, metadata):
    public_metadata(metadata)
    require(set(metadata)<=METADATA_FIELDS, 'Unknown/private quality annotation fields')
    require(metadata.get('schema_version') == 1, 'Quality annotation schema differs')
    notes = metadata.get('pages', {})
    require(set(notes)==set(pages), 'Quality annotations must cover exactly every live/local leaf, with no unused page entries')
    shapes, plans = metadata.get('shape_definitions',{}), metadata.get('cluster_plans',{})
    require(shapes and all(isinstance(v,str) and v.strip() for v in shapes.values()), 'Human shape definitions missing')
    for cluster in {p['cluster'] for p in pages.values()}:
        plan = plans.get(cluster, [])
        require(len(set(plan))>=8 and set(plan)<=set(shapes), cluster+': plan needs at least eight defined opening shapes')
    figures = metadata.get('figures',{})
    require(figures, 'Source-reviewed figure registry missing')
    semantic = {}
    for key,record in figures.items():
        require(set(record)<=FIGURE_FIELDS, 'Unknown/private figure audit fields')
        require(key==figure_key(record), 'Figure identity differs from its exact count/base/published cut: '+key)
        require(HEX.fullmatch(record.get('source_review_sha256','')), 'Figure lacks independent source-review binding')
        identity = figure_descriptor(record)
        identity.pop('count'); identity.pop('base'); identity.pop('unit')
        cut_key = canonical_json(identity)
        require(cut_key not in semantic, 'A published fact/cut has multiple count/base identities; derived rates must use its canonical observation')
        semantic[cut_key] = key
    for rel,p in pages.items():
        note = notes[rel]
        require(set(note)<=PAGE_FIELDS, rel+': unknown/private page audit fields')
        bank_ids = set(re.findall(r'\bLB-Q\d{4}\b',str(p['meta'].get('demand_evidence',''))))
        require(len(bank_ids)==1 and note.get('bank_id') in bank_ids, rel+': annotation bank ID differs from the actual receipt metadata')
        require(HEX.fullmatch(note.get('source_sha256','')), rel+': historical raw source hash missing')
        require(note.get('canonical_source_sha256')==p['canonical_source_sha256'], rel+': source content changed after quality annotation')
        require(note.get('opening_sha256')==p['opening_sha256'], rel+': opening changed after human classification')
        require(note.get('opening_shape') in plans[p['cluster']], rel+': shape is outside the actual cluster plan')
        require(note.get('classification_reason') and HEX.fullmatch(note.get('writing_review_sha256','')), rel+': independent human shape reason/receipt missing')
        require(isinstance(note.get('lead_figures'),list) and note['lead_figures'], rel+': no independently identified lead figure')
        require(len(set(note['lead_figures']))==len(note['lead_figures']), rel+': duplicate lead fact on the same page')
        require(set(note['lead_figures'])<=set(figures), rel+': unknown lead figure')
        spans = note.get('lead_figure_spans')
        require(isinstance(spans,dict) and set(spans)==set(note['lead_figures']) and HEX.fullmatch(note.get('source_review_sha256','')), rel+': every lead fact needs its own source review/span binding')
        require(all(isinstance(values,list) and values and all(isinstance(span,str) and span and span in p['opening'] for span in values) for values in spans.values()), rel+': lead figure span is not in the actual opening')
    return notes


def apply_baseline(analysis, pages, baseline, trusted_policy):
    public_metadata(baseline)
    require(baseline.get('schema_version')==1, 'Baseline schema differs')
    snapshot = baseline.get('frozen_pages',{})
    require(isinstance(trusted_policy,dict) and trusted_policy.get('snapshot_sha256') and digest(canonical_json(snapshot).encode())==trusted_policy['snapshot_sha256'], 'Frozen150 snapshot differs from its committed trusted hash')
    require(len(snapshot)==150, 'Baseline must contain exactly the original150 leaves')
    require(set(snapshot)<=set(pages), 'A frozen live leaf was removed')
    for rel,record in snapshot.items():
        require(record['canonical_source_sha256']==pages[rel]['canonical_source_sha256'], rel+': frozen baseline page changed; old exceptions cannot follow changed source content')
        annotation = pages[rel].get('quality_annotation', {})
        require(record['opening_sha256']==pages[rel]['opening_sha256'], rel+': frozen opening changed')
        require(record['opening_shape']==annotation.get('opening_shape') and record['lead_figures']==annotation.get('lead_figures'), rel+': frozen shape/figure classification changed')
    exceptions = baseline.get('exceptions',{})
    require(all(set(row['pages'])<=set(snapshot) for row in exceptions.values()), 'Baseline exception names a new page')
    require(trusted_policy.get('baseline_sha256') and digest(canonical_json(baseline).encode())==trusted_policy['baseline_sha256'], 'Frozen baseline cases/counts differ from their committed trusted hash')
    current = {row['key']:row for row in analysis['violations']}
    errors, grandfathered = [], []
    for row in analysis['violations']:
        before = exceptions.get(row['key'])
        if row['kind']=='opening_concentration' and before:
            maximum = max(before['count'], row['total']//5)
            if row['count']<=maximum:
                grandfathered.append(dict(row, maximum_count=maximum, baseline_count=before['count']))
                continue
        # Existing overused figures may not acquire even one new leading page.
        elif before and set(row['pages'])<=set(before['pages']) and all(p in snapshot for p in row['pages']):
            if row['kind']=='six_word_similarity' and Fraction(row['score_fraction'])>Fraction(before['score_fraction']):
                errors.append(row)
            elif row['kind']=='eight_word_opening' and not set(row['shared_sequences'])<=set(before['shared_sequences']):
                errors.append(row)
            elif row['kind']=='opening_adjacency' and row['hub_order_pair']!=before['hub_order_pair']:
                errors.append(row)
            else:
                grandfathered.append(row)
            continue
        errors.append(row)
    # Adding distinct pages may resolve a former concentration. Record that
    # improvement without requiring a new exception or rewriting live prose.
    stale = sorted(set(exceptions)-set(current))
    return errors, grandfathered, stale


def run(docs, metadata, baseline, trusted_snapshot_sha256=FROZEN_WAVE_ONE_SNAPSHOT_SHA256,
        trusted_baseline_sha256=FROZEN_WAVE_ONE_BASELINE_SHA256):
    pages = load_pages(docs)
    notes = validate_annotations(pages, metadata)
    for rel,note in notes.items():
        pages[rel]['quality_annotation'] = note
    references = metadata.get('index_question_titles',{})
    require(HEX.fullmatch(references.get('source_sha256','')), 'Index question title snapshot lacks source hash')
    require(len(references.get('records',[]))==140, 'Exactly140 published Index question title references required')
    require(len({r['url'] for r in references['records']})==140, 'Index question title reference URLs are duplicated')
    orders, order_errors = hub_orders(docs,pages)
    result = analyze(pages,notes,orders,references['records'],docs)
    require(digest(canonical_json(references).encode())==baseline.get('index_question_titles_sha256'), 'Published Index question title snapshot changed')
    errors,accepted,stale = apply_baseline(result,pages,baseline,{'snapshot_sha256':trusted_snapshot_sha256,'baseline_sha256':trusted_baseline_sha256})
    result.update(passed=not errors and not order_errors, leaf_count=len(pages),
                  errors=errors, hub_errors=order_errors, baseline_cases_unchanged=accepted,
                  resolved_baseline_cases=stale, new_page_exceptions=0,
                  planned_shapes={k:metadata['cluster_plans'][k] for k in orders},
                  figures_at_three={k:v for k,v in result['lead_figure_pages'].items() if len(v)==3})
    result['opening_count_limits'] = {}
    for cluster,distribution in result['opening_distributions'].items():
        limits = {}
        for shape in metadata['cluster_plans'][cluster]:
            old = baseline['exceptions'].get('opening_concentration:'+cluster+':'+shape,{})
            limits[shape] = max(old.get('count',0),distribution['total']//5)
        result['opening_count_limits'][cluster] = limits
    result['lead_figure_counts'] = [dict(id=key,label=metadata['figures'][key]['label'],
        descriptor=figure_descriptor(metadata['figures'][key]), pages=paths,leading_page_count=len(paths),
        remaining_new_leads=max(0,3-len(paths))) for key,paths in result['lead_figure_pages'].items()]
    result['policy'] = {'six_word_sequences':'sets; intersection divided by smaller set; strictly greater than1/5 fails',
        'opening_eight_word_sequences':'any shared normalized sequence fails',
        'opening_shapes':'independently reviewed; actual hub order; eight planned shapes separate from actual distribution',
        'figure_limit':3,'frozen_snapshot_sha256':trusted_snapshot_sha256,'frozen_baseline_sha256':trusted_baseline_sha256,
        'new_page_exceptions':0}
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--docs',type=Path,default=ROOT/'docs')
    ap.add_argument('--annotations',type=Path,default=ROOT/'tools/library_quality_annotations.json')
    ap.add_argument('--baseline',type=Path,default=ROOT/'tools/library_quality_baseline.json')
    ap.add_argument('--report',type=Path,default=ROOT/'library-quality-report.json')
    args = ap.parse_args()
    try:
        result = run(args.docs,read_json(args.annotations),read_json(args.baseline))
    except (OSError,ValueError,KeyError,TypeError) as exc:
        result = {'passed':False,'fatal':str(exc),'new_page_exceptions':0}
    def input_name(path):
        try:return path.resolve().relative_to(ROOT).as_posix()
        except ValueError:return path.name
    result['inputs'] = {input_name(p):digest(p.read_bytes()) for p in (args.annotations,args.baseline) if p.is_file()}
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'passed':result['passed'],'report':str(args.report),'leaf_count':result.get('leaf_count'),
                      'new_failures':len(result.get('errors',[])),'fatal':result.get('fatal')}))
    return 0 if result['passed'] else 1


if __name__=='__main__':
    sys.exit(main())
