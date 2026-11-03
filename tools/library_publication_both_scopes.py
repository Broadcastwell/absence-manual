"""Add the unchanged literalq comparison to the runtime qualifier-free gate."""
import copy
from library_publication_overlay import require,sha,read_bound_json
from library_publication_eligibility import scope_for
from library_publication_release import (full_report_binding,state_fingerprint,
    prepare_incremental_permit as runtime_prepare_permit)

POLICY='ORIGINAL_LITERAL_Q_AND_EXACT_QUALIFIER_RUNTIME_V1'


def validate_scope_union(report,state,q):
    """Keep each scope's violation identity and fraction independent."""
    paths={r['path'] for r in state['routes'].values() if r['kind']=='article'}
    count=len(paths)*(len(paths)-1)//2
    require(report.get('comparison_policy')==POLICY and report.get('compiled_collection_fingerprint')==state_fingerprint(state,q),'Both-scope quality snapshot is missing or belongs to another collection')
    scopes=report.get('comparison_scopes',{})
    require(set(scopes)=={'literal','runtime'},'Both comparison scopes must be explicit')
    expected=[]
    for name in ['runtime','literal']:
        scope=scopes[name]
        require(scope.get('all_pairs_compared') is True and scope.get('pair_count')==count and isinstance(scope.get('violations'),list),'Incomplete literal/runtime all-pairs evidence')
        for violation in scope['violations']:
            row=copy.deepcopy(violation)
            require(row.get('pages') and set(row['pages'])<=paths,'Comparison scope hides an effective article')
            if name=='literal':row['key']='literal:'+row['key'];row['comparison_scope']='original_literal_q'
            expected.append(row)
    require(report.get('violations')==expected,'Combined gate hides or conflates a literal/runtime violation')
    return True


def attach_literal_scope(overlay,state,*,current_annotations,runtime_report):
    """No source rewriting, baseline exemption or replacement normalization."""
    overlay._check_unchanged();q=overlay.q;binding=full_report_binding(state,q)
    require(runtime_report.get('analysis_completed') is True and runtime_report.get('all_pairs_compared') is True
        and runtime_report.get('compiled_collection_fingerprint')==binding['compiled_collection_fingerprint']
        and runtime_report.get('effective_article_paths')==binding['effective_article_paths']
        and runtime_report.get('baseline_exceptions')==0,'Both scopes require exact complete runtime collection proof')
    require(runtime_report.get('comparison_policy') is None,'Do not attach the literal scope twice')
    pages={};pins={}
    for rel,r in overlay.records.items():
        opening=q.paragraph_after_heading(r['body']).strip();comp=q.comparison_prose(r['body'])
        require(current_annotations['pages'][rel]['canonical_source_sha256']==r['effective_canonical_source_sha256']
            and current_annotations['pages'][rel]['opening_sha256']==sha(opening.encode()),'Literal scope annotation/source binding differs')
        pages[rel]={**copy.deepcopy(r),'opening':opening,'opening_sha256':sha(opening.encode()),'six':q.sequences(q.words(comp),6),'eight':q.sequences(q.words(q.comparison_prose(opening)),8)}
        pins[rel]={'effective_full_sha256':r['effective_canonical_source_sha256'],'body_sha256':sha(r['body'].encode()),'literal_comparable_sha256':sha(comp.encode())}
    pair_count=len(pages)*(len(pages)-1)//2
    require(runtime_report.get('pair_count')==pair_count,'Runtime report hides actual comparison pairs')
    orders,errors=q.hub_orders(overlay.docs,pages);require(not errors and orders==runtime_report['actual_hub_orders'],'Both scopes must use exact actual current hub order')
    literal=q.analyze(pages,current_annotations['pages'],orders,current_annotations['index_question_titles']['records'],overlay.docs)
    result=copy.deepcopy(runtime_report);original=copy.deepcopy(result['violations'])
    result['comparison_policy']=POLICY
    result['comparison_scopes']={'runtime':{'all_pairs_compared':True,'pair_count':pair_count,'violations':original},
        'literal':{'all_pairs_compared':True,'pair_count':pair_count,'violations':copy.deepcopy(literal['violations'])}}
    result['comparison_input_pins']=pins
    frozen=getattr(scope_for(overlay),'frozen',frozenset())
    for violation in literal['violations']:
        row=copy.deepcopy(violation);row['key']='literal:'+row['key'];row['comparison_scope']='original_literal_q'
        result['violations'].append(row)
        for rel in row['pages']:
            ready=result['page_readiness'][rel]
            if rel in frozen:ready['deferred_diagnostics'].append(row)
            else:ready['passed']=False;ready['status']='FAIL';ready['errors'].append(row)
    scope=scope_for(overlay)
    if scope is not None:
        scope.decorate(result,overlay);overlay._eligible_current_passed=result['eligible_completion_passed'];overlay._strict_current_passed=False
    else:
        result['passed']=not result['global_fatal_errors'] and not result['violations'] and all(r.get('passed') is True for r in result['page_readiness'].values())
        overlay._strict_current_passed=result['passed']
    return result


def prepare_both_scope_permit(overlay,**kwargs):
    report=kwargs['full_current_report'];state=kwargs['candidate_state']
    validate_scope_union(report,state,overlay.q)
    previous=read_bound_json(kwargs['previous_manifest_path'],kwargs['trusted_previous_sha256'])
    validate_scope_union(previous.get('current_quality_snapshot',{}),previous,overlay.q)
    require(set(report.get('comparison_input_pins',{}))==set(overlay.records),'Both-scope input coverage differs')
    for rel,r in overlay.records.items():
        pin=report['comparison_input_pins'][rel]
        require(pin=={'effective_full_sha256':r['effective_canonical_source_sha256'],'body_sha256':sha(r['body'].encode()),'literal_comparable_sha256':sha(overlay.q.comparison_prose(r['body']).encode())},'Both-scope effective inputs changed after comparison')
    for name in ['literal','runtime']:
        scope=report.get('comparison_scopes',{}).get(name,{})
        require(scope.get('all_pairs_compared') is True and scope.get('pair_count')==len(overlay.records)*(len(overlay.records)-1)//2,'Incomplete literal/runtime all-pairs evidence')
    permit=runtime_prepare_permit(overlay,**kwargs)
    permit.result['comparison_policy']=POLICY;permit.result['both_comparison_scopes_verified']=True
    return permit
