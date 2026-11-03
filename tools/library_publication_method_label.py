"""Exact reviewed composite-only method-label corrections; raw footer unchanged."""
from pathlib import Path
import importlib.util,re
from library_publication_overlay import require,sha,canonical,next_step_span,LINK


def validate_composite_method_label(overlay,rel,*,method,raw_full,post_finite_body,prior_payload,revision,payload):
    """Allow no URL/scope substitution and no unreviewed prose transformation."""
    match=LINK.fullmatch(method or '')
    require(match is not None,'Composite method token must be one exact Markdown link')
    label,url=match.groups()
    previous=prior_payload['body'] if prior_payload is not None else post_finite_body
    # Preserve the existing composite rule for an exact already-present method
    # token, including sources whose method reference was outside the footer.
    if method in raw_full or prior_payload is not None and method in prior_payload['body']:return False
    start,end=next_step_span(previous)
    old_span=previous[start:end]
    candidates=[]
    for token in re.findall(r'(?m)^\[[^\n]+\]\(https://[^\s)]+\)\s*$',old_span):
        token=token.strip();old_match=LINK.fullmatch(token)
        if old_match and old_match[2]==url:candidates.append(token)
    if not candidates:
        for token in re.findall(r'(?m)^\[[^\n]+\]\(https://[^\s)]+\)\s*$',previous):
            token=token.strip();old_match=LINK.fullmatch(token)
            if old_match and old_match[2]==url:candidates.append(token)
    candidates=sorted(set(candidates))
    require(len(candidates)==1,'Exact prior method token with same approved source-specific URL required')
    old=candidates[0]
    if old==method:return False
    note=revision.get('method_token_revision')
    require(isinstance(note,dict) and set(note)=={'old','new','decision_receipt_sha256'}
        and note['old']==old and note['new']==method,'Finite old/new method-label decision required')
    record={'path':rel,'raw_canonical_source_sha256':sha(raw_full.encode()),'effective_canonical_source_sha256':sha(payload['effective_full_source'].encode())}
    for kind in ['source','writing']:
        require(overlay._article_receipt(payload.get('review_ids',{}).get(kind),record,kind),'Method-label correction needs exact full-candidate '+kind+' approval')
    validator_path=overlay.docs.parent/'tools/library_answers.py'
    validator_bytes=validator_path.read_bytes();validator_sha=sha(canonical(validator_bytes).encode())
    spec=importlib.util.spec_from_file_location('_bw_reviewed_method_kind',validator_path);validator=importlib.util.module_from_spec(spec);spec.loader.exec_module(validator)
    errors,expected_label=validator.validate_source_evidence(payload['meta'],payload['body'],overlay.docs)
    require(not errors and expected_label==label,'Corrected method label fails actual full-candidate source-kind validation: '+'; '.join(errors))
    require(validator_path.read_bytes()==validator_bytes,'Source-kind validator changed during method correction')
    decision=overlay._load_receipt(note['decision_receipt_sha256'])
    require(decision and decision.get('approved') is True and decision.get('review_kind')=='reviewed-source-specific-method-label'
        and decision.get('path')==rel and decision.get('raw_canonical_source_sha256')==record['raw_canonical_source_sha256']
        and decision.get('before_effective_canonical_sha256')==revision.get('before_effective_canonical_sha256')
        and decision.get('effective_canonical_source_sha256')==record['effective_canonical_source_sha256']
        and decision.get('old')==old and decision.get('new')==method and decision.get('method_url')==url
        and decision.get('source_kind')==payload['meta'].get('evidence_kind','') and decision.get('is_based_on')==payload['meta'].get('is_based_on')
        and decision.get('source_validator_canonical_sha256')==validator_sha
        and decision.get('full_candidate_review_ids')==payload.get('review_ids'), 'Independent exact method-label/source-kind decision missing or stale')
    return True
