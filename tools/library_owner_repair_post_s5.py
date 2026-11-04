"""Dormant, exact307/326/19 post-S5 Owner contract. No production claim.

Actual Root-approved production bytes and a separate exact context receipt are
required; synthetic test bindings are fixtures, never an activation template.
"""
from __future__ import annotations
import copy,json
from library_owner_repair import require,sha,digest,json_unique,exact_edits
from library_owner_repair_consumers import json_hash

ARTICLE_COUNT=307
RAW_COUNT=326
STUB_COUNT=19
PAIR_COUNT=46971
LEGAL='answers/chatgpt/which-legal-practice-software-does-chatgpt-recommend.md'
INFO='research/glossary/information-gain/index.md'
TRIM_SHA='6ee84ad5db688ee2664b27d724d8d8e58cb26b5e379fa7bfeb08a620dd160db9'
CUMULATIVE_SHA='d2474b7a10aacc6fd398d04af6d73626a972e01ddbba1c3ab0954b25631994dc'
INFO_AFTER='41d0de6497383c72858a32ee310bd1b23636efb639398605fe5206c07590419f'
_TOKEN=object()


class PostS5Binding:
    def __init__(self,data,pages,stubs,token):
        require(token is _TOKEN,'Post-S5 binding must be independently bound')
        self.data=copy.deepcopy(data);self.pages=set(pages);self.stubs=copy.deepcopy(stubs)
        self._seal=digest([self.data,sorted(self.pages),self.stubs])
    def check(self):
        require(self._seal==digest([self.data,sorted(self.pages),self.stubs]),'Post-S5 binding changed')


def bind_post_s5(raw,expected_sha256,*,producer_raw,prior,payload,leaves,new_merges,
                 input_files,actual_binding):
    require(sha(raw)==expected_sha256,'Post-S5 Root context hash differs')
    d=json_unique(raw);producer=json_unique(producer_raw)
    require(d.get('approved') is True and d.get('reviewer')=='root'
        and d.get('review_kind')=='root-exact-post-small-S5-owner-context'
        and d.get('schema_version')==1,'Actual post-small-S5 Root context approval missing')
    require(d.get('article_count')==ARTICLE_COUNT and d.get('raw_article_count')==RAW_COUNT
        and d.get('inherited_stub_count')==STUB_COUNT,'Only exact307 effective/326raw/19 inherited supported')
    require(producer.get('approved') is True
        and producer.get('review_kind')=='prior-production-effective-payload'
        and producer.get('actual_served_readback') is True
        and producer.get('source_render_equality_passed') is True
        and producer.get('hub_source_render_equality_passed') is True,'Actual approved source/render/served producer required')
    require(d.get('production_receipt_sha256')==sha(producer_raw),'Post-S5 context uses a different producer')
    require(d.get('production_binding')==producer.get('production_binding')==prior.get('production_binding')==actual_binding,'Post-S5 actual production identity differs')
    for name in ['prior_state','prior_payload','prior_hub_payload','current_leaf_manifest','merges']:
        require(d.get('input_sha256',{}).get(name)==input_files[name]['sha256'],'Post-S5 context input pin differs: '+name)
    for name,value in [('prior_state',prior),('prior_payload',payload),('current_leaf_manifest',leaves),('merges',new_merges)]:
        require(d.get('input_object_sha256',{}).get(name)==json_hash(value),'Post-S5 bound input object differs: '+name)
    require(producer.get('payload_bundle_sha256')==input_files['prior_payload']['sha256']
        and producer.get('hub_payload_bundle_sha256')==input_files['prior_hub_payload']['sha256'],'Producer payload/hub identity differs')
    pages=set(payload.get('pages',{}));raw_pages=set(leaves.get('pages',{}))
    stubs=prior.get('merged_sources',{})
    require(len(pages)==ARTICLE_COUNT and len(raw_pages)==RAW_COUNT and len(stubs)==STUB_COUNT
        and not pages&set(stubs) and raw_pages==pages|set(stubs),'Effective/raw/retired universe differs')
    require(set(prior.get('raw_source_pins',{}))==raw_pages,'Historical raw326 pins incomplete')
    require(new_merges.get('merges')=={},'Owner repair cannot add any new retirement')
    require(d.get('inherited_dispositions_sha256')==json_hash(stubs),'Exact inherited disposition digest differs')
    report=prior.get('current_quality_snapshot',{})
    require(report.get('analysis_completed') is True and report.get('baseline_exceptions')==0
        and report.get('pair_count')==PAIR_COUNT and set(report.get('page_readiness',{}))==pages,'Actual prior307 whole-current analysis missing')
    for scope in ['literal','runtime']:
        r=report.get('comparison_scopes',{}).get(scope,{})
        require(r.get('all_pairs_compared') is True and r.get('pair_count')==PAIR_COUNT,'Actual prior both46971 proof missing')
    frozen={p for p,r in report['page_readiness'].items() if r.get('status')=='DEFERRED_FIELD_TEST'}
    require(len(frozen)==45 and all(report['page_readiness'][p].get('passed') in {None,False} for p in frozen),'Exactly45 deferred, never PASS, required')
    return PostS5Binding(d,pages,stubs,_TOKEN)


def bind_session_context(session,config,load):
    ref=config.get('post_s5_context');require(ref is not None,'Dormant future adapter requires explicit approved post-S5 context')
    raw=load(ref)[1]
    binding=bind_post_s5(raw,ref['sha256'],producer_raw=session._file('production_receipt').read_bytes(),
        prior=session.prior,payload=json.loads(session._file('prior_payload').read_bytes()),
        leaves=json.loads(session._file('current_leaf_manifest').read_bytes()),
        new_merges=json.loads(session._file('merges').read_bytes()),input_files=session.inputs['files'],
        actual_binding=session.inputs['actual_prior_production_binding'])
    expected_targets={source:{'target_path':row['target_path']} for source,row in binding.stubs.items()}
    require(set(session.overlay.records)==binding.pages and session.overlay.merge_statuses==binding.stubs
        and not session.overlay._new_merge_plan and session.overlay._merge_plan==expected_targets,'Compiled collection does not retain exact inherited19')
    validate_inherited_closure(session.overlay,binding,{p:session.archive.read(p) for p in session.archive.namelist() if not p.endswith('/')})
    return binding


def validate_inherited_closure(overlay,binding,files):
    from library_publication_canonical_stub import (POLICY,STATUS,OWNER_QUOTE_SHA256,
        stub_artifact_path,validate_canonical_stub_bytes)
    from library_publication_verify_stubs import Canonicals
    from library_publication_release import route_for
    binding.check();overlay._check_unchanged()
    require(overlay.merge_statuses==binding.stubs and set(overlay.records)==binding.pages,'Inherited map or effective pages changed')
    for source,row in binding.stubs.items():
        target=row.get('target_path')
        require(row.get('policy')==POLICY and row.get('status')==STATUS and row.get('article_pass') is False
            and row.get('owner_quote_sha256')==OWNER_QUOTE_SHA256 and target in overlay.records
            and target not in binding.stubs,'Inherited canonical stub is unreviewed or chained')
        decision=overlay._load_receipt(row.get('decision_receipt_sha256'))
        require(decision and decision.get('approved') is True
            and decision.get('review_kind')=='reviewed-source-fit-canonical-stub'
            and decision.get('source_fit_status')==STATUS
            and all(decision.get(k)==row.get(k) for k in ['target_path','source_canonical_sha256','owner_quote_sha256','stub_html_sha256','meta_refresh_seconds'])
            and decision.get('source_path')==source,'Original approved inherited decision is absent/different')
        artifact=stub_artifact_path(source);validate_canonical_stub_bytes(source,row,files.get(artifact))
        require(source not in files and route_for(source).strip('/')+'.html' not in files,'Unreviewed retired alternate remains')
        target_html=files.get(stub_artifact_path(target));require(isinstance(target_html,bytes),'Inherited target HTML absent')
        reader=Canonicals();reader.feed(target_html.decode());reader.close()
        require(reader.urls==['https://docs.broadcastwell.com'+route_for(target)],'Inherited target is not exact self-canonical')
    return {'inherited_stubs':STUB_COUNT,'unchanged_original_decision_closure':True,
        'actual_http_status_observed':None,'HTTP301_claim':False}


def validate_post_quality(before,after,*,changed_content_paths,frozen_paths,binding):
    from library_owner_repair import validate_quality_transition
    binding.check()
    return validate_quality_transition(before,after,changed_content_paths=changed_content_paths,
        frozen_paths=frozen_paths,post_s5_binding=binding)


def validate_info_trim(record,*,trim_raw,cumulative_raw,pretrim_full,source_parser,actual_ledger_raw):
    require(record['path']==INFO,'Trim belongs only to exact information-gain source')
    require(sha(trim_raw)==TRIM_SHA and sha(cumulative_raw)==CUMULATIVE_SHA
        and cumulative_raw==actual_ledger_raw,'Only exact Root V7 trim/cumulative ledger is supported')
    trim=json_unique(trim_raw);cumulative=json_unique(cumulative_raw)
    require(trim.get('path')==cumulative.get('path')==INFO and len(trim['body_edits'])==4,'Exact four-trim scope differs')
    require(sha(pretrim_full.encode())==trim['before_effective_canonical_sha256'],'Exact V6 intermediate full source differs')
    old_meta,old_body=source_parser(pretrim_full)
    require(sha(record['effective_full_source'].encode())==INFO_AFTER==trim['after_effective_canonical_sha256']==cumulative['after_effective_canonical_sha256'],'Exact Root V7 full source differs')
    require(exact_edits(old_body.encode(),trim['body_edits']).decode()==record['body'],'V7 four-trim forward/inverse differs')
    expected={k:{'old':old_meta.get(k),'new':record['meta'].get(k)} for k in sorted(set(old_meta)|set(record['meta'])) if old_meta.get(k)!=record['meta'].get(k)}
    require(expected==trim['metadata_delta'] and set(expected)=={'date_modified','updated'},'V7 trim metadata exceeds actual dated repair')
    return {'exact_Root_V7_trim':True,'four_spans_inverse_exact':True,'general_prose_waiver':False}


def validate_legal_ordinary(overlay,record,ordinary_ids,prior_readiness):
    require(record['path']==LEGAL and prior_readiness.get('passed') is True and prior_readiness.get('status')=='PASS','Only actual Legal prior-PASS media case supported')
    require(isinstance(ordinary_ids,dict) and set(ordinary_ids)=={'source','writing'},'Separate ordinary full-current Legal peer IDs required')
    for kind in ['source','writing']:
        require(overlay._article_receipt(ordinary_ids[kind],record,kind),'Actual full-current ordinary Legal '+kind+' peer missing')
    require(record.get('review_ids')==ordinary_ids,'Legal base payload must retain ordinary peer IDs, never scoped repair IDs')
    return True
