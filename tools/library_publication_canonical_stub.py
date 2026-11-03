"""Finite owner-authorized GitHub Pages canonical HTML stubs, never HTTP301.

This module performs no file/network writes and grants no hosting/DNS change.
Generated artifact proof and later actual served readback are separate states.
"""
from __future__ import annotations
import copy,re
from html import escape
from html.parser import HTMLParser
from library_publication_overlay import require,sha,read_bound_json,canonical
from library_publication_release import route_for,EffectiveHubQuality,parse_redirects,_matches

OWNER_QUOTE='Redirects on docs: no DNS, hosting or Cloudflare zone change without my yes. Use redirect pages GitHub Pages can serve, with a canonical link to the target.'
OWNER_QUOTE_SHA256=sha(OWNER_QUOTE.encode())
POLICY='OWNER_GITHUB_PAGES_CANONICAL_HTML200_V1'
STATUS='MERGED_CANONICAL_STUB'
SITE='https://docs.broadcastwell.com'


def stub_artifact_path(source):return route_for(source).strip('/')+'/index.html'


def render_canonical_stub(source,row):
    route_for(source);target=row.get('target_path');route_for(target)
    require(source!=target,'Canonical stub self-target forbidden')
    require(row.get('policy')==POLICY and row.get('owner_quote_sha256')==OWNER_QUOTE_SHA256,'Canonical stub lacks exact owner policy')
    label=row.get('target_title')
    require(isinstance(label,str) and label.strip() and len(label)<=400 and '\n' not in label and '<' not in label,'Canonical stub visible target label malformed')
    require(not re.search(r'(?i)\b(?:winner|leader|startup|beta|optimisation|organisation|behaviour|colour|analysing|prioritise)\b',label),'Unsafe canonical stub label needs current review')
    refresh=row.get('meta_refresh_seconds')
    require(refresh is None or type(refresh) is int and 0<=refresh<=30,'Meta refresh requires exact reviewed integer seconds')
    url=SITE+route_for(target)
    lines=['<!doctype html>','<html lang="en">','<head>','<meta charset="utf-8">','<meta name="viewport" content="width=device-width, initial-scale=1">','<title>This answer has moved | The Absence Manual</title>','<link rel="canonical" href="'+escape(url,quote=True)+'">']
    if refresh is not None:lines.append('<meta http-equiv="refresh" content="'+str(refresh)+'; url='+escape(url,quote=True)+'">')
    lines+=['</head>','<body>','<main>','<h1>This answer has moved</h1>','<p>Read the combined answer: <a href="'+escape(url,quote=True)+'">'+escape(label)+'</a>.</p>','</main>','</body>','</html>','']
    return '\n'.join(lines).encode()


def validate_canonical_stub_bytes(source,row,raw):
    require(isinstance(raw,bytes) and raw==render_canonical_stub(source,row),'Canonical stub HTML/canonical/visible link/refresh differs from exact reviewed bytes')
    require(sha(raw)==row.get('stub_html_sha256'),'Canonical stub byte pin differs')
    return {'artifact_path':stub_artifact_path(source),'sha256':sha(raw),'policy':POLICY,'scope':'STATIC_CANONICAL_STUB_BYTES_ONLY','http_status_observed':None,'live_http_301_verified':False}


def apply_reviewed_canonical_stubs(base,plan_path,plan_sha256,*,hub_orders):
    plan=read_bound_json(plan_path,plan_sha256)
    require(plan.get('schema_version')==1 and plan.get('approved') is True and plan.get('routing_policy')==POLICY
        and plan.get('owner_quote')==OWNER_QUOTE and plan.get('owner_quote_sha256')==OWNER_QUOTE_SHA256,'Canonical stub plan lacks exact reviewed owner policy')
    merges=plan.get('merges');require(isinstance(merges,dict) and merges,'Explicit finite canonical stub map required')
    frozen=getattr(getattr(base,'s5_scope',None),'frozen',frozenset())
    require(not frozen&(set(merges)|{r.get('target_path') for r in merges.values()}),'Frozen source or destination excluded from this finite canonical stub policy')
    result=copy.copy(base);result.records=copy.deepcopy(base.records);result.pending=list(base.pending);result.metadata_consumers={};result._strict_current_passed=False;result._eligible_current_passed=False
    result.merge_statuses=copy.deepcopy(getattr(base,'merge_statuses',{}));old_targets={r['target_path'] for r in result.merge_statuses.values()}
    for source,row in merges.items():
        route_for(source);target=row.get('target_path');route_for(target)
        require(source!=target and source in base.records and target in base.records and target not in merges and source not in old_targets,'Missing target, self target or canonical stub chain/cycle')
        old,destination=base.records[source],base.records[target]
        require(row.get('source_canonical_sha256')==old['raw_canonical_source_sha256'] and row.get('target_canonical_sha256')==destination['raw_canonical_source_sha256']
            and row.get('target_effective_canonical_sha256')==destination['effective_canonical_source_sha256'],'Canonical stub exact source/target body pins differ')
        facts=row.get('preserved_fact_bindings');required=row.get('required_fact_ids')
        require(isinstance(facts,list) and facts and isinstance(required,list) and required and len(required)==len(set(required))
            and set(required)=={f.get('id') for f in facts},'Canonical stub requires every exact reviewed preserved fact')
        raw=canonical((base.docs/source).read_bytes())
        for fact in facts:
            require(set(fact)=={'id','source_span','target_span','source_span_sha256','target_span_sha256'} and fact['source_span'] in raw and fact['target_span'] in destination['body']
                and sha(fact['source_span'].encode())==fact['source_span_sha256'] and sha(fact['target_span'].encode())==fact['target_span_sha256'],'Canonical stub loses or misbinds a source fact')
        aliases=destination['meta'].get('also_asked_as',[]);aliases=[aliases] if isinstance(aliases,str) else aliases
        required_aliases=row.get('required_aliases')
        require(isinstance(required_aliases,list) and required_aliases and all(isinstance(a,str) and a.strip() and a in aliases and a in destination['body'] for a in required_aliases),'Canonical stub historical aliases missing from visible target and metadata')
        for kind in ['source','writing']:require(base._article_receipt(destination.get('review_ids',{}).get(kind),destination,kind),'Canonical stub target lacks exact complete current '+kind+' approval')
        decision=base._load_receipt(row.get('decision_receipt_sha256'))
        require(decision and decision.get('approved') is True and decision.get('review_kind')=='reviewed-source-fit-canonical-stub'
            and decision.get('source_path')==source and decision.get('target_path')==target and decision.get('source_fit_status')==STATUS
            and decision.get('source_canonical_sha256')==row['source_canonical_sha256'] and decision.get('target_effective_canonical_sha256')==row['target_effective_canonical_sha256']
            and decision.get('owner_quote_sha256')==OWNER_QUOTE_SHA256 and decision.get('required_fact_ids')==required
            and decision.get('preserved_fact_bindings_sha256')==sha(base.q.canonical_json(facts).encode())
            and decision.get('required_aliases')==required_aliases and decision.get('meta_refresh_seconds')==row.get('meta_refresh_seconds'), 'Independent finite canonical stub decision missing or stale')
        disposition={'status':STATUS,'article_pass':False,'target_path':target,'target_title':destination['meta']['title'],
            'policy':POLICY,'owner_quote_sha256':OWNER_QUOTE_SHA256,'decision_receipt_sha256':row['decision_receipt_sha256'],
            'source_canonical_sha256':row['source_canonical_sha256'],'meta_refresh_seconds':row.get('meta_refresh_seconds')}
        disposition['stub_html_sha256']=sha(render_canonical_stub(source,disposition))
        require(decision.get('stub_html_sha256')==disposition['stub_html_sha256'],'Canonical stub decision does not bind exact generated bytes')
        del result.records[source];result.pending=[e for e in result.pending if not e.startswith(source+': ')]
        result.merge_statuses[source]=disposition
    expected=set(base.records)-set(merges);require(set(result.records)==expected,'Canonical stub effective collection differs')
    result.q=EffectiveHubQuality(base.q,hub_orders,expected)
    result._merge_plan={p:copy.deepcopy(r) for p,r in result.merge_statuses.items()};result._new_merge_plan={p:copy.deepcopy(result.merge_statuses[p]) for p in merges}
    result._canonical_stub_policy=POLICY
    return result


def validate_existing_routing(existing_bytes,dispositions):
    rules=parse_redirects(existing_bytes)
    for source,row in dispositions.items():
        for route in [route_for(source).rstrip('/'),route_for(source),route_for(row['target_path']).rstrip('/'),route_for(row['target_path'])]:
            require(not any(_matches(r['source'],route) for r in rules),'Existing redirect/rewrite overlaps a canonical stub source or target')
    return existing_bytes


def validate_stub_build(overlay,*,existing_redirects,built_files,llms_text):
    from library_publication_release import _HubLinks,effective_hub_orders_from_html
    from urllib.parse import urljoin,urlsplit
    dispositions=overlay.merge_statuses
    require(dispositions and all(r.get('status')==STATUS for r in dispositions.values()),'Mixed/unreviewed canonical dispositions')
    validate_existing_routing(existing_redirects,dispositions)
    require(built_files.get('_redirects',b'')==existing_redirects,'Existing routing bytes changed; static canonical stubs require no rules file')
    clusters={r['cluster'] for r in overlay.records.values()};hubs={c:built_files['answers/'+c+'/index.html'] for c in clusters}
    parsed=[]
    for base,html in [(SITE+'/answers/',built_files['answers/index.html'])]+[(SITE+'/answers/'+c+'/',b) for c,b in hubs.items()]:
        reader=_HubLinks();reader.feed(html.decode());require(reader.found,'Actual full hub article boundary missing')
        parsed += [urlsplit(urljoin(base,h)).path.rstrip('/') for h in reader.links]
    for source,row in dispositions.items():
        path=stub_artifact_path(source);validate_canonical_stub_bytes(source,row,built_files.get(path))
        require(source not in built_files and route_for(source).strip('/')+'.html' not in built_files,'Unreviewed alternate source Markdown/HTML remains public')
        require(stub_artifact_path(row['target_path']) in built_files,'Canonical target HTML missing')
        require(route_for(source).rstrip('/') not in parsed and route_for(source).rstrip('/') not in llms_text,'Retired article remains in actual hub article membership or llms')
    return {'passed':True,'policy':POLICY,'scope':'CANONICAL_HTML200_ARTIFACTS_AND_COLLECTION_ONLY','effective_hub_orders':effective_hub_orders_from_html(overlay,hubs),
        'source_fit_statuses':copy.deepcopy(dispositions),'stub_artifact_hashes':{p:r['stub_html_sha256'] for p,r in dispositions.items()},
        'hosting_migration':False,'http_status_observed':None,'live_http_301_verified':False,'live_stub_readback_verified':False}


def validate_live_stub_readback(overlay,receipt,published_state):
    """Optional post-deploy Root proof; generated HTML never claims this result."""
    from library_publication_release import state_fingerprint
    binding=published_state.get('production_binding')
    require(binding and receipt and receipt.get('approved') is True and receipt.get('review_kind')=='canonical-stub-live-readback'
        and receipt.get('production_binding')==binding and receipt.get('actual_root_read_complete') is True
        and receipt.get('compiled_collection_fingerprint')==state_fingerprint(published_state,overlay.q)
        and receipt.get('source_fit_dispositions_sha256')==sha(overlay.q.canonical_json(overlay.merge_statuses).encode()),'Actual Root canonical stub/target readback missing')
    require(set(receipt.get('rows',{}))==set(overlay.merge_statuses),'Live canonical stub coverage differs')
    for source,row in overlay.merge_statuses.items():
        proof=receipt['rows'][source];target=overlay.records[row['target_path']]
        require(proof.get('stub_url')==SITE+route_for(source) and proof.get('stub_status')==200 and proof.get('stub_final_url')==SITE+route_for(source)
            and proof.get('stub_html_sha256')==row['stub_html_sha256'] and proof.get('canonical_href')==SITE+route_for(row['target_path'])
            and proof.get('target_url')==SITE+route_for(row['target_path']) and proof.get('target_status')==200 and proof.get('target_final_url')==SITE+route_for(row['target_path'])
            and proof.get('target_effective_canonical_sha256')==target['effective_canonical_source_sha256'] and proof.get('meta_refresh_seconds')==row.get('meta_refresh_seconds')
            and proof.get('target_html_sha256')==published_state['routes'][route_for(row['target_path'])]['compiled_sha256']
            and published_state['routes'][route_for(source)]['compiled_sha256']==row['stub_html_sha256'],'Live static stub200/canonical/target200 proof differs')
    return {'live_stub_readback_verified':True,'live_http_301_verified':False,'observed_canonical_stub_http_status':200,'observed_target_http_status':200,'routing_policy':POLICY}


def attach_root_live_readback(result,overlay,receipt,published_state):
    """After publication only: add actual readback, never waive article gates."""
    from library_publication_release import state_fingerprint
    require(result.get('canonical_stub_live_readback_required') is True and result.get('incremental_release_passed') is True
        and result.get('candidate_collection_fingerprint')==state_fingerprint(published_state,overlay.q),'Readback result/state is not the computed bounded release')
    proof=validate_live_stub_readback(overlay,receipt,published_state)
    final=copy.deepcopy(result);final.update(proof)
    final['final_completion_marker_allowed']=result.get('eligible_completion_passed') is True and not result.get('errors')
    return final
