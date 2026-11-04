"""Exact Source-approved Owner11 preservation, separate from ordinary S5.

The owning Research binder supplies records parsed from the actual approved
prior Git archive and candidate archive. This module grants no release token.
"""
from pathlib import Path
from datetime import datetime, timezone
import calendar, json, re
from library_research_support import require, sha, qsha, _file

CATALOG_SHA256='d21170b21a09eb3361cd54a8c8ced52b500070e31d1f17823d4c7f8fb0bdda53'
POLICY='SOURCE_REQUIRED_OWNER_RESEARCH11_PRESERVATION_V1'


def catalog():
    raw=Path(__file__).with_name('library_research_owner_required_spans.json').read_bytes()
    require(sha(raw)==CATALOG_SHA256,'Source-required Owner11 internal catalog changed')
    d=json.loads(raw)
    require(d.get('schema_version')==1 and d.get('policy')==POLICY
        and len(d['required_paths'])==11 and len(set(d['required_paths']))==11
        and set(d['sources'])==set(d['required_paths'])
        and len(d['required_source_ids'])==11 and len(set(d['required_source_ids']))==11,
        'Source-required Owner11 source IDs/paths differ')
    ids=[]
    for path in d['required_paths']:
        r=d['sources'][path]
        require(r['path']==path and r['id'] in d['required_source_ids'],
            'Source-required Owner11 case identity differs')
        require(r['required_span_ids']==[x['id'] for x in r['required_spans']],
            'Source-required Owner11 span identity declaration differs')
        ids.extend(r['required_span_ids'])
        for x in r['required_spans']:
            require(x['text'] and sha(x['text'].encode())==x['sha256']
                and x['exact_occurrences_in_before_body']==1,
                'Source-required complete text/hash differs')
    require(ids==d['all_required_span_ids'] and len(ids)==len(set(ids))==d['required_span_count']==101,
        'Source-required complete101 span identity set differs')
    return d


def _read_lineage(root,support,ref,expected):
    require(isinstance(ref,dict) and set(ref)=={'path','sha256'}
        and ref['sha256']==expected
        and support.plan.get('staged_file_sha256',{}).get(ref['path'])==expected,
        'Owner11 Source lineage receipt is foreign, absent or outside committed closure')
    raw=_file(root,ref['path']).read_bytes()
    require(sha(raw)==expected,'Owner11 Source lineage receipt bytes changed')
    return json.loads(raw)


def _stamp(value):
    require(isinstance(value,str),'Owner11 actual adoption event must be an explicit string')
    try:result=datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError:raise ValueError('Owner11 adoption event is not actual ISO datetime')
    require(result.tzinfo is not None and result.utcoffset().total_seconds()==0
        and result<=datetime.now(timezone.utc),'Owner11 actual adoption event is future or not UTC')
    return result


def _expected_presentation(spec,event):
    stamp=_stamp(event);day=stamp.date().isoformat()
    human=calendar.month_name[stamp.month]+' '+str(stamp.day)+', '+str(stamp.year)
    result=[]
    for slot in spec['presentation_slots']:
        old=slot['current_exact_token']
        require(sha(old.encode())==slot['current_exact_token_sha256'],
            'Source-required presentation-before token changed')
        if slot['id'].endswith('-CITE-UPDATED'):new='updated '+human+'.'
        elif slot['id'].endswith('-BIBTEX-UPDATED'):new='updated '+day
        elif slot['id'].endswith('-LAST-UPDATED'):new='Last updated: '+day+'.'
        else:raise ValueError('Unapproved Owner11 presentation slot ID')
        if old!=new:result.append({'id':slot['id'],'old':old,'new':new,
            'old_sha256':sha(old.encode()),'new_sha256':sha(new.encode())})
    return result


def _validate_presentation(spec,before,after,event,supplied):
    require(isinstance(supplied,list),'Exact Owner11 presentation inverse list missing')
    if before['effective_full_source']==after['effective_full_source']:
        require(after['meta']==before['meta'] and supplied==[],
            'Unchanged Owner11 source acquired a presentation rewrite')
        return {'changed':False,'finite_presentation_edit_ids':[]}
    stamp=_stamp(event)
    require(stamp>_stamp(before['meta']['date_modified']),
        'Owner11 changed source needs actual later Root modification event')
    for key,old in spec['presentation_metadata_before'].items():
        require(before['meta'].get(key)==old and after['meta'].get(key)==event,
            'Owner11 presentation metadata differs from actual Root event')
    expected=_expected_presentation(spec,event)
    require(supplied==expected,'Owner11 presentation edits are not the exact reviewed33-slot projection')
    # Invert only these exact finite tokens in the new page. Other new Research
    # prose is independently reviewed by the existing53-source reading gate.
    restored=after['body']
    for edit in reversed(expected):
        require(restored.count(edit['new'])==1,
            'Owner11 presentation-after token is absent or ambiguous')
        restored=restored.replace(edit['new'],edit['old'],1)
    forward=restored
    for edit in expected:
        require(forward.count(edit['old'])==1,'Owner11 presentation inverse-before token is ambiguous')
        forward=forward.replace(edit['old'],edit['new'],1)
    require(forward==after['body'],'Owner11 finite presentation forward/inverse differs')
    for slot in spec['presentation_slots']:
        require(before['body'].count(slot['current_exact_token'])==1
            and restored.count(slot['current_exact_token'])==1,
            'Owner11 preserved presentation-before slot is absent after exact inverse')
    return {'changed':True,'finite_presentation_edit_ids':[x['id'] for x in expected],
        'actual_adoption_utc':event,'presentation_inverse_body_sha256':sha(restored.encode())}


def validate_required_owner11(*,root,support,data,before_records,after_records):
    """Strict finite input gate, called only after actual prior archive binding."""
    d=catalog();support.assert_current()
    require(data.get('Owner11_required_Source_manifest_sha256')==d['Source_required_manifest_sha256'],
        'Exact Source-approved required11 preservation manifest not bound')
    supplied=data.get('Owner11_preserved_claim_spans',{})
    lineage=data.get('Owner11_Source_lineage',{})
    dates=data.get('Owner11_presentation_date_edits',{})
    expected_paths=set(d['required_paths'])
    require(set(supplied)==set(lineage)==set(dates)==expected_paths,
        'Owner11 missing/extra/foreign source or presentation case')
    event=data.get('Owner11_actual_Research_adoption_utc');_stamp(event)
    result=[]
    for path in d['required_paths']:
        spec=d['sources'][path]
        require(path in before_records and path in after_records,
            'Owner11 actual archived/candidate parsed source missing')
        before=before_records[path];after=after_records[path]
        require(sha(before['effective_full_source'].encode())==spec['before_canonical_full_sha256']
            and sha(before['body'].encode())==spec['before_body_sha256']
            and qsha(before['meta'])==spec['before_metadata_sha256'],
            'Actual published after-Risk Owner11 before-source differs from Source-approved baseline')
        expected=[{k:x[k] for k in ['id','text','sha256']} for x in spec['required_spans']]
        require(supplied[path]==expected,
            'Owner11 required IDs/text are missing, extra, shortened, substituted or reordered')
        for item in spec['required_spans']:
            require(before['body'].count(item['text'])==item['exact_occurrences_in_before_body']
                and after['body'].count(item['text'])>=item['exact_occurrences_in_before_body'],
                'Complete Source-required scientific/qualification/history span lost: '+item['id'])
        for key,value in spec['protected_publication_metadata'].items():
            require(before['meta'].get(key)==value==after['meta'].get(key),
                'Owner11 original publication metadata changed')
        refs=lineage[path]
        require(isinstance(refs,dict) and set(refs)=={'source_id','scoped_Source','Source_evidence','repair_ledger'}
            and refs['source_id']==spec['id'],'Owner11 Source lineage case ID/schema differs')
        peer=_read_lineage(root,support,refs['scoped_Source'],spec['Source_scoped_receipt_sha256'])
        evidence=_read_lineage(root,support,refs['Source_evidence'],spec['Source_evidence_receipt_sha256'])
        _read_lineage(root,support,refs['repair_ledger'],spec['Source_repair_ledger_sha256'])
        for receipt in [peer,evidence]:
            require(receipt.get('approved') is True and receipt.get('review_kind')=='source'
                and receipt.get('path')==path
                and receipt.get('effective_canonical_source_sha256')==spec['before_canonical_full_sha256']
                and receipt.get('effective_body_sha256')==spec['before_body_sha256']
                and receipt.get('effective_meta_sha256')==spec['before_metadata_sha256'],
                'Owner11 Source receipt is unapproved, foreign or stale for actual baseline')
        require(peer.get('scope')=='owner-exact-repair-changes'
            and peer.get('repair_change_ledger_sha256')==spec['Source_repair_ledger_sha256']
            and evidence.get('scope')==spec['Source_evidence_scope']
            and evidence.get('current_scoped_Source_receipt_sha256')==spec['Source_scoped_receipt_sha256'],
            'Owner11 original scoped/fact-or-precision Source lineage differs')
        presentation=_validate_presentation(spec,before,after,event,dates[path])
        result.append({'path':path,'source_id':spec['id'],'required_span_ids':spec['required_span_ids'],
            'before_body_sha256':spec['before_body_sha256'],
            'after_body_sha256':sha(after['body'].encode()),'Source_receipts_exact':True,
            'presentation':presentation})
    support.assert_current()
    return {'policy':POLICY,'internal_catalog_sha256':CATALOG_SHA256,
        'Source_required_manifest_sha256':d['Source_required_manifest_sha256'],
        'exact_required_sources':11,'exact_required_scientific_qualification_history_spans':101,
        'actual_prior_archive_records_match_Source_baseline':True,'rows':result,
        'Research_release_or_ordinary_Source_kind_or_S5_PASS_granted':False}
