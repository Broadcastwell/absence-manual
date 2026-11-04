"""Dormant finite28 extension; Source proposals are not Root adoption receipts.

The internal catalog names only the selected17 record readings and11 literal
precision corrections. It grants no global Rule4/ordinaryS5 approval. The
existing approved Owner plan, exact current producer and scoped peers remain
mandatory in the caller. Public source membership is an explicitly typed
independent Source-review proof, not a fresh network observation by this code.
"""
from __future__ import annotations
import json,re
from pathlib import Path
from library_owner_repair import require,sha,exact_edits,POLICY
from library_owner_repair_consumers import json_hash

CATALOG_SHA256='d7ac7a36caab1eb4277c010fd6527127101b75cc5f819faec9bd2778df525bfa'
CATALOG_PATH=Path(__file__).with_name('library_owner_repair_required28.json')
ANTHROPIC='answers/claude/does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-t.md'
CLASSES={'rule4_record_reading','specific_precision'}

def load_catalog():
    raw=CATALOG_PATH.read_bytes()
    require(sha(raw)==CATALOG_SHA256,'Finite28 internal catalog bytes differ')
    d=json.loads(raw)
    require(d.get('schema_version')==1 and len(d.get('cases',{}))==28
        and sum(r['class']=='rule4_record_reading' for r in d['cases'].values())==17
        and sum(r['class']=='specific_precision' for r in d['cases'].values())==11
        and d.get('new_lead_observation_ids')==[]
        and d.get('global_Rule4_completion_granted') is False,'Only exact17+11 catalog supported')
    return d

def validate_named_case(path,kind,bank_ids):
    r=load_catalog()['cases'].get(path)
    require(r is not None and r['class']==kind,'Unlisted finite28 source/class')
    require(bank_ids.get(path)==r['bank_id'],'Finite28 question identity differs')
    return r

def validate_complete_required_scope(data):
    """New finite classes require the entire43-source union, not a partial fix."""
    catalog=load_catalog();rows=data.get('source_changes',{})
    require(data.get('required28_catalog_sha256')==CATALOG_SHA256,
        'Exact required28 Source selection is not bound by the Root plan')
    nonPDF={p for p,r in rows.items() if r.get('class')!='sample_pdf'}
    require(nonPDF==set(catalog['required_owner_nonPDF_sources']) and len(nonPDF)==43,
        'Required Owner43 source union is incomplete/extra or contains an already-fixed target')
    for path,spec in catalog['cases'].items():
        require(rows['docs/'+path].get('class')==spec['class'],
            'A required record/precision case was hidden under another source class')
    return {'required28':28,'nonPDF_sources':43,'Root_review_inferred':False}

def _opening(body):
    # Use the same owning q implementation; no new comparison normalization.
    import library_quality as q
    return q.paragraph_after_heading(body).strip()

def validate_case(record,*,before,ledger,kind,bank_ids,actual_adoption_utc,
                  source_proof_raw,source_proof_sha256,current_source_peer_sha256):
    path=record['path'];spec=validate_named_case(path,kind,bank_ids)
    require(sha(before['effective_full_source'].encode())==spec['before_effective_sha256']
        and sha(before['body'].encode())==spec['before_body_sha256']
        and json_hash(before['meta'])==spec['before_meta_sha256'],
        'Finite28 before is not the exact current source/effective artifact')
    require(record['before_effective_canonical_source_sha256']==spec['before_effective_sha256'],
        'Finite28 raw/effective before anchor confused')
    require(ledger['body_edits']==spec['body_edits']
        and exact_edits(before['body'].encode(),ledger['body_edits']).decode()==record['body']
        and sha(record['body'].encode())==spec['selected_proposed_body_sha256'],
        'Finite28 selected literal/inverse/body differs')
    expected=dict(spec['selected_proposed_metadata'])
    expected['date_modified']=actual_adoption_utc
    if path.startswith('research/'):
        # Existing Research updated field follows the actual modification date;
        # published/date_published and every other source field remain exact.
        if 'updated' in expected:expected['updated']=actual_adoption_utc
    require(record['meta']==expected,'Finite28 metadata exceeds exact selection/date/required union')
    require(re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00',actual_adoption_utc),
        'Finite28 actual Root UTC adoption is pending/malformed')
    if spec['opening_must_stay_exact']:
        require(_opening(record['body'])==_opening(before['body']),
            'Record insertion cannot silently replace/reclassify the opening')
    require(sha(source_proof_raw)==source_proof_sha256,'Finite28 Source proof bytes differ')
    proof=json.loads(source_proof_raw)
    keys={'approved','review_kind','scope','policy','path','bank_id','source_packet_sha256',
        'source_evidence_anchor_sha256','source_family','canonical_source_sha256',
        'before_effective_canonical_source_sha256','effective_canonical_source_sha256',
        'effective_body_sha256','effective_meta_sha256','repair_change_ledger_sha256',
        'current_scoped_Source_receipt_sha256','specific_source_truth_and_narrow_fit_approved',
        'new_measurement','introduced_numeric_cut','ordinary_full_article_approval',
        'numeric_cut','count','base','new_lead_observation_ids',
        'record_membership_and_quoted_context_independently_checked','source_public_URLs',
        'exact_new_reading_literals'}
    require(set(proof)==keys,'Finite28 typed Source schema contains missing/uncontrolled fields')
    scope='source-owner-repair-record-reading' if kind=='rule4_record_reading' else 'source-owner-repair-specific-precision'
    require(proof.get('approved') is True and proof.get('review_kind')=='source'
        and proof.get('scope')==scope and proof.get('policy')==POLICY,
        'Finite28 independent typed Source proof missing')
    require(proof.get('path')==path and proof.get('bank_id')==spec['bank_id']
        and proof.get('source_packet_sha256')==spec['source_packet_sha256']
        and proof.get('source_evidence_anchor_sha256')==spec['source_evidence_anchor_sha256']
        and proof.get('source_family')==spec['source_family'],
        'Finite28 exact original Source record/family/packet lineage differs')
    require(proof.get('canonical_source_sha256')==record['raw_canonical_source_sha256']
        and proof.get('before_effective_canonical_source_sha256')==spec['before_effective_sha256']
        and proof.get('effective_canonical_source_sha256')==sha(record['effective_full_source'].encode())
        and proof.get('effective_body_sha256')==sha(record['body'].encode())
        and proof.get('effective_meta_sha256')==json_hash(record['meta'])
        and proof.get('repair_change_ledger_sha256')==json_hash(ledger)
        and proof.get('current_scoped_Source_receipt_sha256')==current_source_peer_sha256,
        'Finite28 Source current raw/effective/body/meta/ledger/scoped binding differs')
    require(proof.get('specific_source_truth_and_narrow_fit_approved') is True
        and proof.get('new_measurement') is False
        and proof.get('introduced_numeric_cut') is False
        and proof.get('new_lead_observation_ids')==[]
        and proof.get('ordinary_full_article_approval') is False,
        'Finite28 proof cannot grant new measurement or ordinaryS5 approval')
    if kind=='rule4_record_reading':
        require(proof.get('numeric_cut') is False and proof.get('count') is None
            and proof.get('base') is None and proof.get('new_lead_observation_ids')==[],
            'Qualitative source reading cannot become numeric1 or a new lead identity')
        require(proof.get('record_membership_and_quoted_context_independently_checked') is True,
            'Original record/quote/date/classification membership review missing')
    require(proof.get('source_public_URLs')==spec['exact_public_urls'],
        'Finite28 Source URL inventory differs; host wildcards are forbidden')
    require(proof.get('exact_new_reading_literals')==[e['new'] for e in spec['body_edits']],
        'Finite28 approved quote/date/unit/record reading differs from exact Source selection')
    return {'finite_case':path,'class':kind,'source_family':spec['source_family'],
        'exact_inverse':True,'specific_Source_proof_checked':True,
        'new_numeric_cut':False,'new_lead_observation_ids':[],
        'fresh_public_source_fetch_claimed':False,'ordinary_S5_PASS_granted':False}

def validate_anthropic_ordinary(overlay,record,ordinary_ids,prior_readiness):
    require(record['path']==ANTHROPIC and prior_readiness.get('passed') is True
        and prior_readiness.get('status')=='PASS','Only exact Q0275 priorPASS record case supported')
    require(isinstance(ordinary_ids,dict) and set(ordinary_ids)=={'source','writing'},
        'Q0275 fresh ordinary full-current Source/Writing peers required')
    for kind in ['source','writing']:
        require(overlay._article_receipt(ordinary_ids[kind],record,kind),
            'Actual Q0275 full-current ordinary '+kind+' peer missing')
    require(record.get('review_ids')==ordinary_ids,
        'Q0275 must retain ordinary peer IDs, never scoped repair IDs')
    return True
