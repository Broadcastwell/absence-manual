"""Private reviewed-merge and bounded-release proposal; no source/file/network writes.

The existing full gate remains the default. A group result is explicitly a
limited release result and cannot authorize a full-completion marker.
"""
from __future__ import annotations
import copy
from dataclasses import dataclass
import fnmatch
from fractions import Fraction
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlsplit, urljoin

from library_publication_overlay import (OverlayError, LEAF, HEX, canonical,
    sha, require, read_bound_json, current_comparison_prose, validate_current_annotations)
from library_publication_generated_pdf import PDF_ROUTES,ReviewedPdfChanges
from library_publication_eligibility import Finite45Eligibility,DEFERRED,scope_for


DERIVED_ROUTES = frozenset({'/llms.txt', '/llms-full.txt', '/sitemap.xml',
                            '/sitemap.xml.gz', '/search/search_index.json'})


def allowed_auxiliary_route(route):
    return route in DERIVED_ROUTES or bool(re.fullmatch(r'/answers/(?:[a-z0-9-]+/)?',route))


def route_for(path):
    require(bool(LEAF.fullmatch(path)) and not path.endswith('/index.md'), 'Merge/release path must be an answer leaf')
    return '/' + path.removesuffix('.md') + '/'


def route_forms(path):
    canonical_route = route_for(path)
    return [canonical_route.rstrip('/'), canonical_route]


def merged_artifact_paths(path):
    route = route_for(path).strip('/')
    return {route + '/index.html', route + '.html', path}


def parse_redirects(raw):
    rules = []
    for line in canonical(raw).splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        require(len(parts) in {2, 3}, 'Unsupported existing redirect syntax requires review')
        source, target = parts[:2]
        status = int(parts[2]) if len(parts) == 3 and parts[2].isdigit() else 302 if len(parts) == 2 else None
        require(source.startswith('/') and status in {200, 301, 302, 303, 307, 308, 404, 410}, 'Unsupported redirect source/status')
        rules.append({'source': source, 'target': target, 'status': status})
    return rules


def _literal_target(rule):
    parsed = urlsplit(rule['target'])
    if parsed.netloc and parsed.netloc != 'docs.broadcastwell.com':
        return None
    return parsed.path if rule['target'].startswith('/') or parsed.netloc == 'docs.broadcastwell.com' else None


def _matches(pattern, route):
    # Conservative overlap detection; dynamic rules are never assumed harmless.
    pattern = re.sub(r':[A-Za-z][A-Za-z0-9_]*', '*', pattern)
    return fnmatch.fnmatchcase(route, pattern)


def render_merged_redirects(existing_bytes, merges, effective_articles):
    """Return planned Cloudflare-style rule text; it proves no HTTP behavior.

    The owning deployment currently uses GitHub Pages, which does not honor
    this file. A separately reviewed real routing adapter and both-slash live
    HTTP301 receipts are required before any merge can be published.
    """
    rules = parse_redirects(existing_bytes)
    new = []
    for source, row in sorted(merges.items()):
        target = row['target_path']
        require(target in effective_articles and source not in effective_articles, 'Merged source/target effective set differs')
        for route in route_forms(source):
            require(not any(_matches(rule['source'], route) for rule in rules), 'Existing redirect/rewrite overlaps merged source')
            new.append({'source': route, 'target': route_for(target), 'status': 301})
    combined = rules + new
    literal = {}
    for rule in combined:
        if '*' in rule['source'] or ':' in rule['source']:
            require(not any(_matches(rule['source'], row['target']) for row in new), 'Dynamic existing rule overlaps merge destination')
            continue
        require(rule['source'] not in literal, 'Duplicate existing/generated redirect source')
        literal[rule['source']] = rule
    for source, rule in literal.items():
        if rule['status'] not in {301, 302, 303, 307, 308}:
            continue
        target, visited, depth = _literal_target(rule), {source}, 0
        while target in literal and literal[target]['status'] in {301, 302, 303, 307, 308}:
            require(target not in visited, 'Redirect cycle')
            visited.add(target); depth += 1
            target = _literal_target(literal[target])
        require(depth == 0, 'Redirect chain requires explicit correction; do not publish a new chain')
    suffix = ''.join(f"{rule['source']} {rule['target']} 301\n" for rule in new).encode()
    separator = b'' if not existing_bytes or existing_bytes.endswith((b'\n', b'\r')) else b'\n'
    return existing_bytes + separator + suffix


@dataclass(frozen=True)
class MergeTrust:
    plan_sha256: str
    expected_decision_kind: str = 'reviewed-source-fit-merge-301'


def apply_reviewed_merges(base_overlay, merge_plan_path, trust, *, hub_orders):
    """Exclude approved sources from effective records; original Markdown stays."""
    plan = read_bound_json(merge_plan_path, trust.plan_sha256)
    require(plan.get('schema_version') == 1 and plan.get('approved') is True, 'Merge plan is not approved')
    merges = plan.get('merges', {})
    require(isinstance(merges, dict) and merges, 'Explicit merge entries required')
    result = copy.copy(base_overlay)
    result.records = copy.deepcopy(base_overlay.records)
    result.pending = list(base_overlay.pending)
    result.metadata_consumers = {}
    result._strict_current_passed = False
    result.merge_statuses = copy.deepcopy(getattr(base_overlay,'merge_statuses',{}))
    for source, row in merges.items():
        route_for(source)
        target = row.get('target_path')
        route_for(target)
        require(source != target and source in base_overlay.records and target in base_overlay.records and target not in merges, 'Missing target, self merge or merge chain')
        require(source not in {r['target_path'] for r in result.merge_statuses.values()},'Cannot retire a prior301 destination and create a chain')
        old, destination = base_overlay.records[source], base_overlay.records[target]
        require(row.get('source_canonical_sha256') == old['raw_canonical_source_sha256'], 'Merge source pin differs')
        require(row.get('target_canonical_sha256') == destination['raw_canonical_source_sha256'], 'Merge target raw pin differs')
        require(row.get('target_effective_canonical_sha256') == destination['effective_canonical_source_sha256'], 'Merge target effective content not the reviewed target')
        decision = base_overlay._load_receipt(row.get('decision_receipt_sha256'))
        require(bool(decision and decision.get('approved') is True and decision.get('review_kind') == trust.expected_decision_kind
                     and decision.get('source_path') == source and decision.get('target_path') == target
                     and decision.get('source_canonical_sha256') == row['source_canonical_sha256']
                     and decision.get('target_effective_canonical_sha256') == row['target_effective_canonical_sha256']
                     and decision.get('source_fit_status') == 'MERGED_301'), 'Independent reviewed merge decision missing or stale')
        facts = row.get('preserved_fact_bindings', [])
        require(isinstance(facts, list) and facts, 'Merge requires explicit source-to-target fact ledger')
        required_fact_ids = row.get('required_fact_ids', [])
        require(isinstance(required_fact_ids, list) and required_fact_ids and set(required_fact_ids) <= {fact.get('id') for fact in facts}, 'Merge omits a required preserved fact')
        original_source = canonical((base_overlay.docs / source).read_bytes())
        for fact in facts:
            require(set(fact) == {'id', 'source_span', 'target_span', 'source_span_sha256', 'target_span_sha256'}, 'Malformed merge fact binding')
            require(fact['source_span'] in original_source and fact['target_span'] in destination['body'], 'Merged fact not present in exact source/target')
            require(sha(fact['source_span'].encode()) == fact['source_span_sha256'] and sha(fact['target_span'].encode()) == fact['target_span_sha256'], 'Merge fact binding digest differs')
        require(decision.get('preserved_fact_bindings_sha256') == sha(base_overlay.q.canonical_json(facts).encode()), 'Merge decision does not bind the exact fact ledger')
        aliases = destination['meta'].get('also_asked_as', [])
        if isinstance(aliases,str): aliases=[aliases]
        required_aliases=row.get('required_aliases',[])
        require(isinstance(required_aliases,list) and all(isinstance(alias,str) and alias.strip() and alias in aliases for alias in required_aliases), 'Reviewed merged question aliases missing from effective target metadata')
        del result.records[source]
        # These requirements cease to be article requirements only for an
        # explicitly approved 301 source. No other route's errors disappear.
        result.pending = [error for error in result.pending if not error.startswith(source + ': ')]
        result.merge_statuses[source] = {'status': 'MERGED_301', 'article_pass': False,
                                        'target_path': target, 'decision_receipt_sha256': row['decision_receipt_sha256']}
    expected = set(base_overlay.records) - set(merges)
    require(set(result.records) == expected, 'Effective merged collection differs')
    result.q = EffectiveHubQuality(base_overlay.q, hub_orders, expected)
    result._merge_plan = copy.deepcopy(getattr(base_overlay,'_merge_plan',{}))
    result._merge_plan.update(copy.deepcopy(merges))
    result._new_merge_plan=copy.deepcopy(merges)
    result.pending.append('Planned merge rules only: actual hosting routing and both-slash live HTTP301 proof are not implemented in this proposal')
    return result


class EffectiveHubQuality:
    """Use actual effective hub order without mutating raw hub files/validator."""
    def __init__(self, original, orders, expected_paths):
        self.original = original
        self.orders = copy.deepcopy(orders)
        self.expected = set(expected_paths)

    def __getattr__(self, name):
        return getattr(self.original, name)

    def hub_orders(self, docs, pages):
        errors, listed = [], []
        require(set(pages) == self.expected, 'Effective hub order collection differs')
        clusters = {page['cluster'] for page in pages.values()}
        require(set(self.orders) == clusters, 'Effective hub cluster coverage differs')
        for cluster, paths in self.orders.items():
            if len(paths) != len(set(paths)): errors.append('Effective hub duplicates leaf: ' + cluster)
            for path in paths:
                if path not in pages or pages[path]['cluster'] != cluster:
                    errors.append('Effective hub includes missing/merged/wrong-cluster leaf: ' + path)
                listed.append(path)
        if set(listed) != self.expected: errors.append('Effective hubs do not cover the current effective leaves')
        return copy.deepcopy(self.orders), errors


def exclude_merged_files(files, merged_paths):
    """MkDocs on_files adapter returns a filtered collection; source untouched."""
    requested = set(merged_paths)
    require(all(LEAF.fullmatch(path) and not path.endswith('/index.md') for path in requested), 'Only answer sources may leave served Files')
    found = [file for file in files if getattr(file, 'src_uri', getattr(file, 'src_path', None)) in requested]
    require(len(found) == len(requested), 'Merged Files coverage differs')
    # MkDocs Files exposes remove; a plain sequence is supported for tests.
    if isinstance(files, list):
        return [file for file in files if file not in found]
    for file in found:
        files.remove(file)
    return files


class _HubLinks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.active=0; self.found=False; self.links=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='article' and ('md-content__inner' in attrs.get('class','').split() or self.active):
            self.active+=1; self.found=True
        if self.active and tag=='a' and attrs.get('href'): self.links.append(attrs['href'])
    def handle_endtag(self,tag):
        if tag=='article' and self.active: self.active-=1


def effective_hub_orders_from_html(overlay, hub_html_by_cluster):
    clusters={record['cluster'] for record in overlay.records.values()}
    require(set(hub_html_by_cluster)==clusters,'Actual effective hub HTML coverage differs')
    orders={}
    for cluster,html in hub_html_by_cluster.items():
        reader=_HubLinks();reader.feed(html.decode('utf-8') if isinstance(html,bytes) else html)
        require(reader.found,'Actual built hub article wrapper missing')
        paths=[]
        for href in reader.links:
            parsed=urlsplit(urljoin('https://docs.broadcastwell.com/answers/'+cluster+'/',href))
            if parsed.netloc!='docs.broadcastwell.com':continue
            path=parsed.path.strip('/')+'.md'
            if not LEAF.fullmatch(path) or path.endswith('/index.md'):continue
            require(path in overlay.records and overlay.records[path]['cluster']==cluster,'Actual hub links merged/missing/wrong-cluster article')
            paths.append(path)
        require(len(paths)==len(set(paths)),'Actual hub lists an article twice')
        require(set(paths)=={path for path,record in overlay.records.items() if record['cluster']==cluster},'Actual hub hides an effective article')
        orders[cluster]=paths
    return orders


def validate_merge_build(overlay, *, existing_redirects, built_files, llms_text, hub_texts=None, hub_html_by_cluster=None):
    merges = getattr(overlay, '_merge_plan', {})
    expected = render_merged_redirects(existing_redirects, getattr(overlay,'_new_merge_plan',merges), overlay.records)
    require(built_files.get('_redirects') == expected, 'Planned redirect-rule artifact differs; HTML200 fallback is not a merge')
    actual_hubs={}
    clusters={record['cluster'] for record in overlay.records.values()}
    for cluster in clusters:
        path='answers/'+cluster+'/index.html'
        require(path in built_files,'Actual built cluster hub HTML missing')
        actual_hubs[cluster]=built_files[path]
    require('answers/index.html' in built_files,'Actual built library root hub HTML missing')
    parsed_hubs=[]
    for base,html in [("https://docs.broadcastwell.com/answers/",built_files['answers/index.html'])]+[("https://docs.broadcastwell.com/answers/"+cluster+'/',raw) for cluster,raw in actual_hubs.items()]:
        reader=_HubLinks();reader.feed(html.decode('utf-8') if isinstance(html,bytes) else html)
        require(reader.found,'Actual complete built hub article boundary is missing')
        parsed_hubs.extend(urlsplit(urljoin(base,href)).path.rstrip('/') for href in reader.links)
    for source, row in merges.items():
        require(not (merged_artifact_paths(source) & set(built_files)), 'Merged source still has a served HTML/Markdown artifact')
        require(route_for(row['target_path']).strip('/') + '/index.html' in built_files, 'Merged destination HTML missing')
        require(route_for(source).rstrip('/') not in parsed_hubs,'Merged source remains in actual public hub article')
        require(route_for(source) not in llms_text and route_for(source).rstrip('/') not in llms_text,'Merged source remains in public hub/llms output')
    actual_orders=effective_hub_orders_from_html(overlay,actual_hubs)
    return {'passed': True, 'source_fit_statuses': copy.deepcopy(overlay.merge_statuses),
            'effective_hub_orders':actual_orders,
            'redirect_artifact_sha256': sha(expected), 'planned_301_forms': sum(2 for _ in merges),
            'scope':'PLANNED_STATIC_RULES_AND_COLLECTION_ONLY',
            'hosting_routing_verified':False,'live_http_301_verified':False,
            'merge_publication_allowed':False}


def state_fingerprint(manifest, q):
    return sha(q.canonical_json({'routes': manifest['routes'], 'raw_source_pins': manifest['raw_source_pins']}).encode())


def make_compiled_state(overlay, *, built_route_artifacts, redirects, production_binding=None):
    """Derive route hashes from actual candidate bytes and effective records.

    built_route_artifacts maps each public route to its actual built bytes.
    Auxiliary hub/llms routes belong in this mapping and count toward the cap.
    The external exact-head artifact/served receipt binds production_binding.
    """
    routes = {}
    for path, record in overlay.records.items():
        route = route_for(path)
        require(route in built_route_artifacts, 'Actual built article missing from compiled state')
        routes[route] = {'kind': 'article', 'path': path,
                         'effective_canonical_sha256': record['effective_canonical_source_sha256'],
                         'body_sha256': sha(record['body'].encode()),
                         'metadata_sha256': record['effective_meta_sha256'],
                         'compiled_sha256': sha(built_route_artifacts[route])}
    for source, row in redirects.items():
        disposition=getattr(overlay,'merge_statuses',{}).get(source,{})
        if disposition.get('status')=='MERGED_CANONICAL_STUB':
            from library_publication_canonical_stub import validate_canonical_stub_bytes
            route=route_for(source);require(route in built_route_artifacts,'Actual canonical stub bytes missing')
            validate_canonical_stub_bytes(source,disposition,built_route_artifacts[route])
            routes[route]={'kind':'canonical_stub','source_path':source,'target':route_for(row['target_path']),'compiled_sha256':sha(built_route_artifacts[route])}
        else:
            for route in route_forms(source):
                require(route not in built_route_artifacts, 'Redirect source may not be represented by HTML200 bytes')
                routes[route] = {'kind': 'redirect', 'status': 301, 'target': route_for(row['target_path']), 'source_path': source}
    for route, raw in built_route_artifacts.items():
        require(isinstance(raw, bytes), 'Compiled route artifact must be actual bytes')
        if route not in routes:
            if route in PDF_ROUTES:
                routes[route]={'kind':'generated_pdf','compiled_sha256':sha(raw)}
                continue
            require(allowed_auxiliary_route(route), 'Unexpected client/research/nonlibrary route change surface')
            routes[route] = {'kind': 'auxiliary', 'compiled_sha256': sha(raw)}
    return {'schema_version': 1, 'routes': routes,
            'raw_source_pins': {path: note['canonical_source_sha256'] for path, note in overlay.leaf_manifest['pages'].items()},
            'merged_sources': copy.deepcopy(getattr(overlay, 'merge_statuses', {})),
            'production_binding': copy.deepcopy(production_binding)}


def full_report_binding(state, q):
    return {'compiled_collection_fingerprint': state_fingerprint(state, q),
            'effective_article_paths': sorted(row['path'] for row in state['routes'].values() if row['kind'] == 'article')}


def assess_current_records(overlay, *, current_annotations,trusted_index_references_sha256):
    """Analyze the entire effective collection; incomplete annotations fail closed.

    Missing ordinary article receipts are route-level FAILs, not exceptions.
    Mechanically invalid annotation coverage prevents a group gate entirely,
    because comparison against every current page would be unproved.
    """
    if getattr(overlay,'s5_scope',None) is not None:
        overlay._strict_current_passed=False;overlay._eligible_current_passed=False
    overlay._check_unchanged()
    q = overlay.q
    scope=scope_for(overlay);frozen=scope.frozen if scope is not None else frozenset()
    pages, readiness, fatal = {}, {}, []
    for rel, record in overlay.records.items():
        page = copy.deepcopy(record)
        errors = [error for error in overlay.pending if error.startswith(rel + ': ')]
        try:
            comparable = current_comparison_prose(page['body'], q)
        except ValueError as error:
            if rel not in frozen:errors.append(str(error))
            comparable = q.comparison_prose(page['body'])
        if rel not in frozen:
            try:
                overlay._validate_related(rel, page['body'], overlay.mapping['pages'].get(rel) or overlay.leaf_manifest['pages'][rel].get('related_requirements', {}))
            except ValueError as error:errors.append(str(error))
            for kind in ['source', 'writing']:
                if not overlay._article_receipt(record['review_ids'].get(kind), record, kind):errors.append('Fresh complete current ' + kind + ' receipt missing')
        opening = q.paragraph_after_heading(page['body']).strip()
        page.update(opening=opening, opening_sha256=sha(opening.encode()),
                    six=q.sequences(q.words(comparable), 6), eight=q.sequences(q.words(q.comparison_prose(opening)), 8))
        pages[rel] = page
        if rel in frozen:
            # Only composition's explicit S5 diagnostic bucket is deferred.
            # Any ordinary pending condition on a frozen path stays fatal.
            readiness[rel]={'status':DEFERRED,'passed':None,'errors':[],
                'deferred_diagnostics':copy.deepcopy(getattr(overlay,'deferred_s5_diagnostics',{}).get(rel,[])),
                'effective_canonical_sha256':record['effective_canonical_source_sha256']}
        else:readiness[rel] = {'status':'PASS' if not errors else 'FAIL','passed': not errors, 'errors': errors,
                          'effective_canonical_sha256': record['effective_canonical_source_sha256']}
    fatal.extend(error for error in overlay.pending if not any(error.startswith(path + ': ') for path in pages))
    fatal.extend(error for error in overlay.pending if any(error.startswith(path+': ') for path in frozen))
    fatal.extend(overlay.metadata_consumer_errors())
    analysis, completed, orders = {'violations': []}, False, {}
    try:
        notes, qualitative = validate_current_annotations(overlay, pages, current_annotations)
        for rel,page in pages.items():
            if rel in frozen:continue
            for kind in ['source','writing']:
                if page['meta'].get('evidence_kind') == getattr(q,'COMPANY_PANEL_KIND',None) and getattr(q,'COMPANY_PANEL_KIND',None) is not None:
                    from library_publication_overlay import validate_finite_current_review
                    try:validate_finite_current_review(overlay,page,notes[rel],kind,current_annotations['figures'])
                    except ValueError as error:
                        readiness[rel]['passed']=False
                        readiness[rel]['errors'].append(str(error))
                elif notes[rel].get(kind+'_review_sha256') != page['review_ids'].get(kind):
                    readiness[rel]['passed']=False
                    readiness[rel]['errors'].append('Current annotation '+kind+' receipt differs from the reviewed effective record')
        refs = current_annotations['index_question_titles']
        require(sha(q.canonical_json(refs).encode()) == trusted_index_references_sha256 and len(refs.get('records', [])) == 140, 'Trusted140Index references differ')
        orders, hub_errors = q.hub_orders(overlay.docs, pages)
        fatal.extend(hub_errors)
        analysis = q.analyze(pages, notes, orders, refs['records'], overlay.docs)
        for key in sorted(set(qualitative.values())):
            paths = sorted(path for path, observation in qualitative.items() if observation == key)
            if len(paths) > 3: analysis['violations'].append({'kind':'qualitative_lead_limit','key':key,'pages':paths,'count':len(paths)})
        completed = True
    except (KeyError, TypeError, ValueError) as error:
        fatal.append('Complete current annotation/analysis failure: ' + str(error))
    for violation in analysis['violations']:
        for rel in violation['pages']:
            require(rel in readiness,'Unknown collection-violation page')
            if rel in frozen:readiness[rel]['deferred_diagnostics'].append(violation)
            else:
                readiness[rel]['passed'] = False;readiness[rel]['status']='FAIL'
                readiness[rel]['errors'].append(violation)
    result={**analysis,'analysis_completed':completed,'all_pairs_compared':completed,
        'pair_count':len(pages)*(len(pages)-1)//2 if completed else 0,'page_readiness':readiness,
        'global_fatal_errors':fatal,'actual_hub_orders':orders,'baseline_exceptions':0}
    result['passed']=completed and not fatal and not analysis['violations'] and all(row['passed'] for row in readiness.values())
    if scope is not None:scope.decorate(result,overlay)
    return result


def complete_current_analysis(overlay,state,*,current_annotations,trusted_index_references_sha256,
    validated_auxiliary_routes=(),merge_build_receipt=None,reviewed_generated_pdf_changes=None):
    result={**full_report_binding(state,overlay.q),**assess_current_records(overlay,current_annotations=current_annotations,trusted_index_references_sha256=trusted_index_references_sha256)}
    fatal=result['global_fatal_errors'];orders=result['actual_hub_orders']
    merge_receipt = merge_build_receipt or {}
    if getattr(overlay, '_merge_plan', {}) and merge_receipt.get('passed') is not True:
        fatal.append('Planned-rule/served-Files/hub/llms merge artifact proof missing')
    elif getattr(overlay,'_merge_plan',{}) and merge_receipt.get('effective_hub_orders') != orders:
        fatal.append('Actual built hub order differs from the whole-current comparison order')
    result.update({
              'validated_changed_auxiliary_routes':sorted(validated_auxiliary_routes),
              'validated_generated_pdf_routes':sorted(reviewed_generated_pdf_changes.routes) if isinstance(reviewed_generated_pdf_changes,ReviewedPdfChanges) else [],
              'source_fit_statuses':copy.deepcopy(getattr(overlay,'merge_statuses',{})),
              'merge_artifact_passed':merge_receipt.get('passed') is True,
              'merge_build_passed':False if getattr(overlay,'_merge_plan',{}) else merge_receipt.get('passed') is True,
              'merge_hosting_status':('CANONICAL_STUB_ARTIFACTS_VERIFIED_PENDING_LIVE_READBACK' if getattr(overlay,'_canonical_stub_policy',None) and merge_receipt.get('passed') is True else 'PLANNED_RULES_ONLY_UNVERIFIED') if getattr(overlay,'_merge_plan',{}) else 'NO_MERGES',
              'live_http_301_verified':False,
              'baseline_exceptions':0})
    scope=scope_for(overlay)
    if scope is not None:
        scope.validate_state(state);scope.decorate(result,overlay)
        overlay._strict_current_passed=False
        overlay._eligible_current_passed=result['eligible_completion_passed']
    else:result['passed']=result['analysis_completed'] and not fatal and not result['violations'] and all(row['passed'] for row in result['page_readiness'].values())
    return result


def _violation_worsened(current, previous):
    if not previous or not set(current['pages']) <= set(previous['pages']): return True
    if current.get('kind') == 'six_word_similarity':
        return Fraction(current['score_fraction']) > Fraction(previous['score_fraction'])
    if current.get('kind') == 'opening_concentration':
        return Fraction(current['count'], current['total']) > Fraction(previous['count'], previous['total'])
    if current.get('kind') in {'lead_figure_limit','qualitative_lead_limit'}:
        return current['count'] > previous['count']
    if current.get('kind') == 'eight_word_opening':
        return not set(current['shared_sequences']) <= set(previous['shared_sequences'])
    return False


def incremental_release_gate(*, previous_manifest_path, trusted_previous_sha256,
                             actual_prior_production_binding, candidate_state,
                             actual_candidate_state, authorized_change_map,
                             full_current_report, q, maximum_changed_routes=50,
                             reviewed_generated_pdf_changes=None,s5_scope=None):
    """No whitelist/scope parameter. Actual state deltas define every changed URL."""
    require(type(maximum_changed_routes) is int and 1 <= maximum_changed_routes <= 50, 'Release cap cannot exceed50')
    previous = read_bound_json(previous_manifest_path, trusted_previous_sha256)
    require(previous.get('schema_version') == candidate_state.get('schema_version') == 1, 'Compiled state schema differs')
    require(previous.get('production_binding') == actual_prior_production_binding and actual_prior_production_binding,
            'Prior manifest is not bound to the actual current production commit/artifact/served receipt')
    require(set(actual_prior_production_binding) >= {'commit_sha','deployment_id','artifact_sha256','served_receipt_sha256'}
            and bool(re.fullmatch(r'[0-9a-f]{40}', actual_prior_production_binding['commit_sha']))
            and HEX.fullmatch(actual_prior_production_binding['artifact_sha256'])
            and HEX.fullmatch(actual_prior_production_binding['served_receipt_sha256'])
            and actual_prior_production_binding['deployment_id'], 'Prior production binding fields invalid')
    require(candidate_state == actual_candidate_state, 'Candidate manifest hides actual compiled body/metadata/route changes')
    old, current = previous['routes'], candidate_state['routes']
    changed = sorted(route for route in set(old) | set(current) if old.get(route) != current.get(route))
    require(all(route.startswith('/answers/') or allowed_auxiliary_route(route) or route in PDF_ROUTES for route in changed), 'Client/research/nonlibrary route change forbidden')
    pdf_changes=set(changed)&PDF_ROUTES
    if pdf_changes:
        require(isinstance(reviewed_generated_pdf_changes,ReviewedPdfChanges),'Changed generated PDFs require exact independent Root review proof')
        reviewed_generated_pdf_changes.validate_states(old,current,changed)
    else:require(reviewed_generated_pdf_changes is None,'Stale generated PDF review supplied for unchanged routes')
    require(set(full_current_report.get('validated_generated_pdf_routes',[]))==pdf_changes,'Generated PDF report hides or invents a reviewed public route')
    errors = []
    if len(changed) > maximum_changed_routes: errors.append('Actual changed routes exceed the release cap')
    articles = {row['path'] for row in current.values() if row['kind'] == 'article'}
    prior_quality = previous.get('current_quality_snapshot', {})
    require(prior_quality.get('compiled_collection_fingerprint') == state_fingerprint(previous,q)
            and prior_quality.get('analysis_completed') is True and prior_quality.get('baseline_exceptions') == 0,
            'Prior production needs its bound zero-exception whole-collection quality snapshot, even when FAIL')
    binding = full_report_binding(candidate_state, q)
    require(full_current_report.get('compiled_collection_fingerprint') == binding['compiled_collection_fingerprint'], 'Quality report belongs to another compiled collection')
    require(set(full_current_report.get('effective_article_paths', [])) == articles, 'Quality report hides an effective page')
    require(full_current_report.get('all_pairs_compared') is True and full_current_report.get('pair_count') == len(articles)*(len(articles)-1)//2, 'Full-collection comparison evidence incomplete')
    require(full_current_report.get('baseline_exceptions') == 0, 'Existing baseline allowances are forbidden in current release gates')
    require(full_current_report.get('analysis_completed') is True, 'Current whole-collection analysis did not complete')
    per_page = full_current_report.get('page_readiness', {})
    require(set(per_page) == articles, 'Readiness report must name every current effective article')
    if s5_scope is not None:
        require(isinstance(s5_scope,Finite45Eligibility),'Arbitrary S5 exception is forbidden')
        eligible,frozen,eligible_pass=s5_scope.validate_report(full_current_report,candidate_state,previous)
        if not s5_scope.preservation_passed:errors.append('Exact frozen preservation proof is required for every release')
    else:
        require(not full_current_report.get('explicit_field_exception'),'Field exception lacks exact accepted authority')
        eligible,frozen,eligible_pass=articles,set(),False
    prior_articles={row['path'] for row in previous['routes'].values() if row['kind']=='article'}
    prior_readiness=prior_quality.get('page_readiness',{})
    require(set(prior_readiness)==prior_articles,'Prior whole-collection snapshot lacks complete readiness rows')
    changed_articles = {current[route]['path'] for route in changed if route in current and current[route]['kind'] == 'article'}
    require(not changed_articles&frozen,'Frozen effective article cannot change in a release')
    merged = candidate_state.get('merged_sources', {})
    changed_merges = {path: row for path, row in merged.items() if any(route in changed for route in route_forms(path))}
    canonical_merges=bool(merged) and all(r.get('status')=='MERGED_CANONICAL_STUB' for r in merged.values())
    if changed_merges and not canonical_merges:
        errors.append('Merge publication blocked: planned static rules do not prove actual hosting routing or both-slash live HTTP301; reviewed routing adapter is not implemented')
    for route in changed:
        before, after = old.get(route), current.get(route)
        require(after is not None, 'Public route removal requires an explicit reviewed disposition, not a404')
        if before and before['kind'] == 'article' and after['kind'] != 'article':
            require(before['path'] in changed_merges, 'Article was removed without its reviewed merge')
        if before and before['kind'] == 'redirect':
            require(before == after, 'Existing redirect rules must be preserved')
    required_map_paths = changed_articles | set(changed_merges)
    require(set(authorized_change_map) == required_map_paths, 'Authorized change map does not match all actual changed articles/merges')
    for path in changed_articles:
        row = current[route_for(path)]
        allowed = authorized_change_map[path]
        require(allowed.get('after_effective_canonical_sha256') == row['effective_canonical_sha256']
                and allowed.get('after_body_sha256') == row['body_sha256']
                and allowed.get('after_metadata_sha256') == row['metadata_sha256'], 'Changed body/metadata does not match exact authorized map')
        before = old.get(route_for(path), {})
        require(allowed.get('before_effective_canonical_sha256') == before.get('effective_canonical_sha256'), 'Before-production content binding differs')
        if per_page[path].get('passed') is not True: errors.append('Changed article current rules/receipts fail: ' + path)
    for path, row in changed_merges.items():
        require(row.get('status') in {'MERGED_301','MERGED_CANONICAL_STUB'} and row.get('article_pass') is False, 'Merged source must not be labeled an article PASS')
        require(row['target_path'] in changed_articles, 'Merge target content must be a coupled reviewed change in the same release')
        require(authorized_change_map[path].get('status') == row['status'] and authorized_change_map[path].get('target_path') == row['target_path'], 'Merge authorization differs')
        require(full_current_report.get('merge_artifact_passed',full_current_report.get('merge_build_passed')) is True, 'Planned merge artifact proof missing')
        if row['status']=='MERGED_CANONICAL_STUB':
            from library_publication_canonical_stub import POLICY,OWNER_QUOTE_SHA256
            require(row.get('policy')==POLICY and row.get('owner_quote_sha256')==OWNER_QUOTE_SHA256,'Canonical stub owner authority differs')
            require(current.get(route_for(path))=={'kind':'canonical_stub','source_path':path,'target':route_for(row['target_path']),'compiled_sha256':row['stub_html_sha256']},'Canonical stub exact compiled source route differs')
            require(full_current_report.get('merge_hosting_status')=='CANONICAL_STUB_ARTIFACTS_VERIFIED_PENDING_LIVE_READBACK','Canonical stub artifact status differs; never inferHTTP301')
        else:
            for route in route_forms(path):
                require(current.get(route) == {'kind':'redirect','status':301,'target':route_for(row['target_path']),'source_path':path}, 'Both slash forms need the exact intended301 rule')
    raw_changes = {path for path in set(previous['raw_source_pins']) | set(candidate_state['raw_source_pins'])
                   if previous['raw_source_pins'].get(path) != candidate_state['raw_source_pins'].get(path)}
    require(raw_changes <= required_map_paths, 'Raw source/metadata changed outside the exact map')
    violations = full_current_report.get('violations', [])
    old_violations = {row.get('key',q.canonical_json({'kind':row['kind'],'pages':row['pages']})):row for row in prior_quality.get('violations',[])}
    for violation in violations:
        pages = violation.get('pages')
        require(isinstance(pages, list) and pages and set(pages) <= articles, 'Unscoped/unknown whole-collection violation')
        if set(pages)<=frozen:continue
        if set(pages) & changed_articles: errors.append(violation)
        else:
            key = violation.get('key',q.canonical_json({'kind':violation['kind'],'pages':pages}))
            if _violation_worsened(violation, old_violations.get(key)):
                errors.append({'kind':'new_or_worse_untouched_violation','violation':violation})
    for path,row in per_page.items():
        if path in frozen:continue
        if path not in changed_articles and prior_readiness.get(path,{}).get('passed') is True and row.get('passed') is not True:
            errors.append({'kind':'new_untouched_readiness_failure','path':path,'errors':row.get('errors',[])})
    errors.extend(full_current_report.get('global_fatal_errors', []))
    # Auxiliary routes are derived artifacts, never an escape for arbitrary HTML.
    changed_aux = [route for route in changed if current.get(route, {}).get('kind') == 'auxiliary']
    require(set(full_current_report.get('validated_changed_auxiliary_routes', [])) == set(changed_aux), 'Changed hub/llms artifacts lack exact effective-registry validation')
    untouched_failures = sorted(path for path, row in per_page.items() if path in eligible and not row.get('passed') and path not in changed_articles)
    overall_pass = False if s5_scope is not None else not violations and all(row.get('passed') for row in per_page.values()) and not full_current_report.get('global_fatal_errors')
    require(full_current_report.get('passed') is overall_pass, 'Full-current status contradicts explicit remaining failures')
    scoped_complete=eligible_pass and s5_scope.preservation_passed if s5_scope is not None else overall_pass
    return {'incremental_release_passed': not errors, 'full_current_passed': overall_pass,
            'candidate_collection_fingerprint':state_fingerprint(candidate_state,q),
            'final_completion_marker_allowed': scoped_complete and not errors and not canonical_merges,
            'result_kind': 'BOUNDED_INCREMENTAL_RELEASE_ONLY',
            'changed_routes': changed, 'changed_route_count': len(changed),
            'changed_articles': sorted(changed_articles), 'coupled_merged_sources': sorted(changed_merges),
            'changed_auxiliary_routes': changed_aux,
            'changed_generated_pdf_routes':sorted(pdf_changes),
            'generated_pdf_root_receipt_sha256':reviewed_generated_pdf_changes.root_receipt_sha256 if pdf_changes else None,
            'merge_hosting_status':('CANONICAL_STUB_ARTIFACTS_VERIFIED_PENDING_LIVE_READBACK' if canonical_merges else 'PLANNED_RULES_ONLY_UNVERIFIED') if merged else 'NO_MERGES',
            'canonical_stub_live_readback_required':canonical_merges,'live_stub_readback_verified':False,
            'live_http_301_verified':False,
            'untouched_current_failures': untouched_failures,
            'untouched_failure_count': len(untouched_failures),
            'remaining_whole_collection_violations': violations,
            'errors': errors, 'baseline_exceptions': 0,
            'explicit_field_exception':s5_scope is not None,
            's5_scope':s5_scope.description(articles,prior_articles) if s5_scope is not None else None,
            'eligible_current_passed':eligible_pass if s5_scope is not None else overall_pass,
            'eligible_completion_passed':scoped_complete and not errors,
            'frozen_preservation_passed':s5_scope.preservation_passed if s5_scope is not None else None,
            'all_published_current_passed':overall_pass,
            'deferred_frozen_only_violations':[v for v in violations if set(v['pages'])<=frozen] if s5_scope is not None else []}


def require_full_completion(result,*,s5_scope=None):
    if result.get('canonical_stub_live_readback_required'):
        require(result.get('live_stub_readback_verified') is True and result.get('live_http_301_verified') is False,'Final marker requires actual canonical stub200/target200 Root readback; neverHTTP301')
    if result.get('explicit_field_exception'):
        require(isinstance(s5_scope,Finite45Eligibility),'Scoped final marker needs exact accepted finite45 authority')
        s5_scope.assert_current();scope=result.get('s5_scope',{})
        require(scope.get('registry_sha256')==s5_scope.freeze.registry_sha256 and scope.get('deferred_count')==45 and scope.get('deferred_status')==DEFERRED and set(scope.get('deferred_paths',[]))==set(s5_scope.frozen),'Final marker S5 exception is off-registry')
        require(result.get('eligible_current_passed') is True and result.get('eligible_completion_passed') is True and result.get('frozen_preservation_passed') is True and s5_scope.preservation_passed and result.get('full_current_passed') is False and result.get('all_published_current_passed') is False and result.get('final_completion_marker_allowed') is True,'Final marker requires every eligible current PASS, exact frozen preservation and all release gates')
    else:
        require(s5_scope is None and result.get('full_current_passed') is True and result.get('final_completion_marker_allowed') is True,
                'Final marker requires full current PASS; an incremental release is insufficient')


_PERMIT_TOKEN = object()


class BoundedPublicationPermit:
    """Dedicated partial-release path; the default full gate is unchanged."""
    def __init__(self, overlay, state, result, token):
        require(token is _PERMIT_TOKEN and result['incremental_release_passed'], 'A computed successful bounded gate is required')
        self.overlay, self.state, self.result = overlay, copy.deepcopy(state), copy.deepcopy(result)

    def _record(self,path):
        self.overlay._check_unchanged()
        require(path in self.overlay.records,'Merged/unknown source cannot emit an article')
        record=self.overlay.records[path]; row=self.state['routes'].get(route_for(path),{})
        require(row.get('kind')=='article' and row.get('effective_canonical_sha256')==record['effective_canonical_source_sha256']
                and row.get('body_sha256')==sha(record['body'].encode())
                and row.get('metadata_sha256')==record['effective_meta_sha256'],'Candidate body/metadata changed after its bounded gate')
        return record

    def markdown_after_finite94(self,path,markdown):
        record=self._record(path)
        require(sha(markdown.encode())==record['post_finite94_body_sha256'],'Bounded MkDocs input differs from pinned finite94 stage')
        return record['body']

    def metadata(self,path):
        return copy.deepcopy(self._record(path)['meta'])


def prepare_incremental_permit(overlay, *, built_route_artifacts, candidate_state,
                               previous_manifest_path, trusted_previous_sha256,
                               actual_prior_production_binding, authorized_change_map,
                               full_current_report, maximum_changed_routes=50,
                               reviewed_generated_pdf_changes=None):
    """Derive actual candidate state here; caller cannot pass a smaller scope."""
    actual=make_compiled_state(overlay,built_route_artifacts=built_route_artifacts,
                               redirects=getattr(overlay,'_merge_plan',{}),
                               production_binding=candidate_state.get('production_binding'))
    result=incremental_release_gate(previous_manifest_path=previous_manifest_path,
        trusted_previous_sha256=trusted_previous_sha256,
        actual_prior_production_binding=actual_prior_production_binding,
        candidate_state=candidate_state,actual_candidate_state=actual,
        authorized_change_map=authorized_change_map,full_current_report=full_current_report,
        q=overlay.q,maximum_changed_routes=maximum_changed_routes,
        reviewed_generated_pdf_changes=reviewed_generated_pdf_changes,s5_scope=scope_for(overlay))
    require(result['incremental_release_passed'],'Bounded release failed; no publication permit')
    return BoundedPublicationPermit(overlay,actual,result,_PERMIT_TOKEN)
