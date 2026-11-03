"""Private bounded composition proposal. It never invokes the all300 compiler.

An independently bound prior effective payload is copied exactly for every
untouched route. Only explicit reviewed revisions supply a replacement. All
records are still analyzed by the unchanged zero-exception current gate.
"""
from __future__ import annotations
import copy
from dataclasses import dataclass
from pathlib import Path
import re
import json

from library_publication_overlay import (PublicationOverlay, OverlayError, HEX,
    canonical, sha, require, read_bound_json, key_hash, source_head,
    remove_exact_qualifier, next_step_span, FREE_CHECK_TOKEN, LIMIT_SENTENCE,
    enforce_frozen_articles, hrefs, utc_calendar_day)
from library_publication_release import route_for, route_forms, state_fingerprint
from library_publication_eligibility import Finite45Eligibility
from library_publication_generated_pdf import PDF_ROUTES


@dataclass(frozen=True)
class CompositionTrust:
    prior_state_sha256: str
    prior_payload_sha256: str
    current_leaf_manifest_sha256: str
    active_revision_plan_sha256: str
    related_requirements_sha256: str
    current_pins_sha256: str
    production_receipt_sha256: str | None = None
    frozen_receipt_sha256: str | None = None
    published_count: int | None = None



def validated_published_article_count(value, prior):
    """Validate an independently pinned count against actual prior articles.

    Retired raw sources remain immutable history. They are not current articles
    and cannot inflate this count or be silently removed from the history set.
    Payload coverage, exact artifact bytes and production provenance are checked
    separately by bind_prior_content/bind_prior_production.
    """
    require(type(value) is int and value > 0,
        'Explicit independently pinned published ARTICLE count required')
    routes=prior.get('routes')
    history=prior.get('raw_source_pins')
    retired=prior.get('merged_sources',{})
    require(isinstance(routes,dict) and isinstance(history,dict)
        and isinstance(retired,dict),'Prior article inventory malformed')
    paths=[]
    for route,row in routes.items():
        require(isinstance(row,dict),'Prior route row malformed')
        if row.get('kind')!='article':continue
        rel=row.get('path')
        require(isinstance(rel,str) and re.fullmatch(r'answers/[a-z0-9-]+/[a-z0-9-]+\.md',rel)
            and route==route_for(rel),'Prior article route/path differs')
        paths.append(rel)
    require(len(paths)==len(set(paths)),'Duplicate prior article path')
    require(value==len(paths),'Pinned published ARTICLE count differs from actual prior article inventory')
    require(not (set(paths)&set(retired)),'Retired raw history is also a prior article')
    require(set(history)==set(paths)|set(retired),
        'Prior raw source history hides or invents article/retired path')
    return value


def json_hash(q, value):
    return sha(q.canonical_json(value).encode())


def payload_hashes(payload, finite):
    """Bind the exact full text, metadata and body without reserializing it."""
    full=payload.get('effective_full_source')
    require(isinstance(full,str),'Exact prior/revised effective full source required')
    meta,body=finite.source_body(full)
    require(payload.get('body')==body and payload.get('meta')==meta,'Effective body/metadata disagree with full source')
    head=source_head(full,body)
    require(payload.get('effective_head')==head,'Effective head differs from exact full source')
    return meta,body,head


def _binding_fields(binding):
    return bool(isinstance(binding,dict) and set(binding)>={'commit_sha','deployment_id','artifact_sha256','served_receipt_sha256'}
        and re.fullmatch('[0-9a-f]{40}',str(binding['commit_sha']))
        and HEX.fullmatch(str(binding['artifact_sha256']))
        and HEX.fullmatch(str(binding['served_receipt_sha256'])) and binding['deployment_id'])


def bind_prior_content(*,prior,payloads,actual_artifacts,q):
    article_paths={row['path'] for row in prior['routes'].values() if row['kind']=='article'}
    require(set(payloads)==article_paths,'Prior payload registry hides or invents article')
    pdf_routes={route for route,row in prior['routes'].items() if row['kind']=='generated_pdf'}
    require(not pdf_routes or pdf_routes==PDF_ROUTES,'Prior generated PDF inventory must register both exact existing Manual paths only')
    for route in pdf_routes:
        require(set(prior['routes'][route])=={'kind','compiled_sha256'},'Unsupported generated PDF inventory row')
    artifact_routes={route for route,row in prior['routes'].items() if row['kind'] in {'article','auxiliary','generated_pdf','canonical_stub'}}
    require(set(actual_artifacts)==artifact_routes,'Prior compiled route-byte inventory differs')
    for route,row in prior['routes'].items():
        if row['kind'] in {'article','auxiliary','generated_pdf','canonical_stub'}:
            require(isinstance(actual_artifacts[route],bytes) and sha(actual_artifacts[route])==row['compiled_sha256'],'Prior actual compiled bytes changed')
        if row['kind']=='article':
            p=payloads[row['path']]
            require(sha(p['effective_full_source'].encode())==row['effective_canonical_sha256']
                and sha(p['body'].encode())==row['body_sha256']
                and json_hash(q,p['meta'])==row['metadata_sha256'],'Prior effective payload is not its compiled manifest row')


def bind_prior_production(*, prior, payloads, actual_artifacts, actual_binding,
                          receipt, q, payload_file_sha256):
    """Every effective article and compiled auxiliary byte belongs to this prior.

    The independently reviewed receipt is the owning build/served source-to-
    render proof. This code verifies its exact bindings; it cannot manufacture
    that proof from a raw checkout or an unverified deployment identifier.
    """
    require(_binding_fields(actual_binding) and prior.get('production_binding')==actual_binding,'Prior production identity differs')
    require(receipt and receipt.get('approved') is True
        and receipt.get('review_kind')=='prior-production-effective-payload'
        and receipt.get('actual_served_readback') is True
        and receipt.get('source_render_equality_passed') is True
        and receipt.get('production_binding')==actual_binding
        and receipt.get('payload_bundle_sha256')==payload_file_sha256
        and receipt.get('compiled_collection_fingerprint')==state_fingerprint(prior,q),
        'Independent prior artifact/served/source-to-render proof missing or stale')
    bind_prior_content(prior=prior,payloads=payloads,actual_artifacts=actual_artifacts,q=q)
    require(receipt.get('compiled_route_hashes')=={route:sha(raw) for route,raw in sorted(actual_artifacts.items())},'Prior receipt artifact byte inventory differs')


def neutral_footer_issues(overlay,rel,record,contract):
    """Check the same strict neutral-footer contract for every current record."""
    if not contract:return ['Approved neutral footer contract missing']
    try:
        start,end=next_step_span(record['body'])
        method=contract.get('method_token')
        require(isinstance(method,str) and re.fullmatch(r'\[[^\]]+\]\(https://[^\s)]+\)',method),'Footer method token is not an exact public reference')
        correction=contract.get('free_correction_statement','')
        require(isinstance(correction,str),'Footer correction statement malformed')
        offer=contract.get('offer',{})
        name,price,href=offer.get('name'),offer.get('price'),offer.get('href')
        require(isinstance(name,str) and re.fullmatch(r'[A-Za-z][A-Za-z 0-9-]{1,70}',name),'Footer offer name malformed')
        require(isinstance(price,str) and re.fullmatch(r'\$[0-9,]+(?:\.[0-9]{2})?',price),'Footer offer price malformed')
        require(isinstance(href,str) and href.startswith('https://broadcastwell.com/'),'Footer offer destination malformed')
        expected=[FREE_CHECK_TOKEN+'. '+LIMIT_SENTENCE]
        if correction:expected.append(correction)
        expected.extend([method,name+': ['+price+']('+href+').'])
        require(record['body'][start:end]=='\n\n'+'\n\n'.join(expected)+'\n\n','Current footer differs from one neutral offer-line contract')
        price_receipt=overlay._load_receipt(offer.get('live_price_receipt_sha256'))
        require(price_receipt and price_receipt.get('approved') is True and price_receipt.get('review_kind')=='live-offer-price'
            and all(price_receipt.get(k)==offer.get(k) for k in ['name','price','href'])
            and price_receipt.get('checked_on')==utc_calendar_day(),'Current matching live-price receipt missing or stale')
        return []
    except (KeyError,TypeError,ValueError) as error:
        return [str(error)]


class ComposedPublicationOverlay(PublicationOverlay):
    def _s5_issue(self,rel,message):
        if self.s5_scope is not None and rel in self.s5_scope.frozen:
            self.deferred_s5_diagnostics.setdefault(rel,[]).append(message)
        else:self.pending.append(rel+': '+message)
    def _check_sources(self):
        super()._check_sources()
        for rel,note in self.leaf_manifest['pages'].items():
            require(bool(HEX.fullmatch(str(note.get('raw_source_sha256'))))
                and sha((self.docs/rel).read_bytes())==note['raw_source_sha256'],rel+': Exact current raw source bytes differ')

    @classmethod
    def compose(cls,docs_dir,*,prior_state,prior_payload_bundle,current_leaf_manifest,
        active_revision_plan,related_requirements,current_pins,trust,finite_links,
        quality_module,actual_prior_artifacts,actual_prior_binding,receipt_store,
        field_handoff_path,frozen_effective_pins=None,publication_evidence=True,s5_scope=None):
        """Compose all current records; never transform an untouched prior body.

        Preview is explicit and unpublishable. It still binds every supplied
        file/record and runs all current rules. It cannot create a permit while
        a production provenance error is pending.
        """
        self=cls();self.docs=Path(docs_dir).resolve();self.q=quality_module;self.finite=finite_links
        self.receipt_store=dict(receipt_store);self.pending=[];self.records={};self.target_stamps={}
        self.metadata_consumers={};self._strict_current_passed=False
        self._eligible_current_passed=False
        require(s5_scope is None or isinstance(s5_scope,Finite45Eligibility),'Arbitrary S5 skiplist is forbidden')
        self.s5_scope=s5_scope;self.deferred_s5_diagnostics={}
        self.prior=read_bound_json(prior_state,trust.prior_state_sha256)
        bundle=read_bound_json(prior_payload_bundle,trust.prior_payload_sha256)
        self.leaf_manifest=read_bound_json(current_leaf_manifest,trust.current_leaf_manifest_sha256)
        plan=read_bound_json(active_revision_plan,trust.active_revision_plan_sha256)
        self.mapping=read_bound_json(related_requirements,trust.related_requirements_sha256)
        self.pins=read_bound_json(current_pins,trust.current_pins_sha256)
        self._field_handoff=Path(field_handoff_path).resolve()
        # Only this run's actual shared handoff is accepted, never a conveniently absent substitute.
        require(self._field_handoff==self.docs.parents[2]/'LIVE/FIELD_TEST_TO_LIBRARY.md','Incorrect shared field-test handoff path')
        self._field_stamp=self._field_handoff.read_bytes() if self._field_handoff.exists() else None
        prior_payloads=bundle.get('pages',{})
        require(self.prior.get('schema_version')==bundle.get('schema_version')==plan.get('schema_version')==1,'Composition schema differs')
        require(set(self.mapping.get('pages',{}))==set(self.pins['pages']),'Related requirements and current pinned history differ')
        self.published_article_count=validated_published_article_count(trust.published_count,self.prior)
        require(set(self.pins['pages'])==set(self.prior['raw_source_pins'])
            and key_hash(self.pins['pages'])==self.pins['keys_sha256'],'Published exact key set differs')
        self._check_sources()
        for rel,pin in self.pins['pages'].items():
            raw=(self.docs/rel).read_bytes()
            require(sha(raw)==pin['raw_source_sha256'] and sha(canonical(raw).encode())==pin['canonical_source_sha256'],'Current300 source pin differs')
        bind_prior_content(prior=self.prior,payloads=prior_payloads,actual_artifacts=actual_prior_artifacts,q=self.q)
        production_receipt=self._load_receipt(trust.production_receipt_sha256)
        provenance_error=None
        try:
            bind_prior_production(prior=self.prior,payloads=prior_payloads,actual_artifacts=actual_prior_artifacts,
                actual_binding=actual_prior_binding,receipt=production_receipt,q=self.q,payload_file_sha256=trust.prior_payload_sha256)
        except (KeyError,TypeError,ValueError) as error:
            if publication_evidence:raise
            provenance_error=str(error)
        if not publication_evidence:
            self.pending.append('Composition preview has no publication authority: '+(provenance_error or 'explicit preview mode'))
        active=plan.get('pages',{})
        if self.s5_scope is not None:self.s5_scope.reject_active(active)
        retired=copy.deepcopy(self.prior.get('merged_sources',{}))
        for path,status in retired.items():
            require(status.get('status') in {'MERGED_301','MERGED_CANONICAL_STUB'} and status.get('article_pass') is False
                and path in self.leaf_manifest['pages'] and status.get('target_path') in prior_payloads,'Prior retired source disposition differs')
            require(self.prior['raw_source_pins'].get(path)==self.leaf_manifest['pages'][path]['canonical_source_sha256'],'Retired raw source history changed')
            if status['status']=='MERGED_CANONICAL_STUB':
                from library_publication_canonical_stub import validate_canonical_stub_bytes,POLICY
                route=route_for(path)
                require(self.prior['routes'].get(route)=={'kind':'canonical_stub','source_path':path,'target':route_for(status['target_path']),'compiled_sha256':status['stub_html_sha256']},'Prior canonical stub route manifest differs')
                validate_canonical_stub_bytes(path,status,actual_prior_artifacts[route])
                self._canonical_stub_policy=POLICY
            else:
                for route in route_forms(path):
                    require(self.prior['routes'].get(route)=={'kind':'redirect','status':301,'target':route_for(status['target_path']),'source_path':path},'Prior source lacks both real301 forms')
        self.merge_statuses=retired
        self._merge_plan={path:{'target_path':row['target_path']} for path,row in retired.items()}
        self._new_merge_plan={}
        require(isinstance(active,dict) and set(active)<=set(self.leaf_manifest['pages']),'Active revision names an unknown current leaf')
        require(not set(active)&set(retired),'A retired source cannot be revived as an article revision')
        require(set(prior_payloads)<=set(self.leaf_manifest['pages']),'Prior effective article disappeared without a reviewed merge stage')
        require(set(self.leaf_manifest['pages'])-set(prior_payloads)-set(retired)<=set(active),'New current leaf has no explicit independently pinned active revision')
        if plan.get('approved') is not True:
            require(not publication_evidence,'Active revision plan is not approved')
            self.pending.append('Active revision plan remains an unapproved private preview')
        self.retained_prior_paths=[];self.active_revision_paths=sorted(active)
        for rel,note in sorted(self.leaf_manifest['pages'].items()):
            if rel in retired:continue
            raw=(self.docs/rel).read_bytes();full=canonical(raw)
            raw_meta,raw_body=self.finite.source_body(full)
            raw_head=source_head(full,raw_body)
            stage=self.finite.transform(rel,raw_body)
            prior_payload=prior_payloads.get(rel)
            if rel in active:
                revision=active[rel]
                expected_before=self.prior['routes'].get(route_for(rel),{}).get('effective_canonical_sha256')
                require(revision.get('before_effective_canonical_sha256')==expected_before,'Active revision before-production binding differs')
                require(revision.get('raw_canonical_source_sha256')==sha(full.encode())
                    and revision.get('post_finite94_body_sha256')==sha(stage.encode()),'Active revision source or finite94 pin differs')
                payload=revision.get('payload',{})
                meta,body,head=payload_hashes(payload,self.finite)
                require(revision.get('after_effective_canonical_sha256')==sha(payload['effective_full_source'].encode())
                    and revision.get('after_body_sha256')==sha(body.encode())
                    and revision.get('after_metadata_sha256')==json_hash(self.q,meta),'Active revision after body/metadata pins differ')
                decision=self._load_receipt(revision.get('revision_receipt_sha256'))
                good=bool(decision and decision.get('approved') is True and decision.get('review_kind')=='reviewed-effective-revision'
                    and decision.get('path')==rel and decision.get('before_effective_canonical_sha256')==expected_before
                    and decision.get('raw_canonical_source_sha256')==sha(full.encode())
                    and decision.get('after_effective_canonical_sha256')==revision['after_effective_canonical_sha256']
                    and decision.get('fact_ledger_sha256')==json_hash(self.q,revision.get('fact_ledger',[]))
                    and decision.get('effective_payload_sha256')==json_hash(self.q,payload))
                if not good:self.pending.append(rel+': Independent exact active revision/fact-ledger receipt missing')
                require(isinstance(revision.get('fact_ledger'),list),'Active exact fact ledger required')
                if re.findall(r'\d+(?:[.,]\d+)?',stage.split('## Related')[0])!=re.findall(r'\d+(?:[.,]\d+)?',body.split('## Related')[0]):
                    require(bool(revision['fact_ledger']),'Active numeric/date change requires explicit fact ledger')
                for fact in revision['fact_ledger']:
                    require(set(fact)=={'old_span','new_span','old_sha256','new_sha256'} and isinstance(fact['old_span'],str) and isinstance(fact['new_span'],str),'Malformed active fact binding')
                    require((fact['old_span'] in full or prior_payload and fact['old_span'] in prior_payload['effective_full_source']) and fact['new_span'] in payload['effective_full_source']
                        and sha(fact['old_span'].encode())==fact['old_sha256'] and sha(fact['new_span'].encode())==fact['new_sha256'],'Active fact span binding differs')
                omissions=set(revision.get('approved_navigation_omissions',[]))
                for omitted in omissions:
                    target=self._target(omitted,self.docs/rel)
                    require(target is not None and target.is_file() and target.is_relative_to(self.docs/'answers') and target.name!='index.md','Active omission is not optional sibling navigation')
                previous_primary=hrefs(stage.split('## Next step')[0])|hrefs(prior_payload['body'].split('## Next step')[0]) if prior_payload else hrefs(stage.split('## Next step')[0])
                require(previous_primary-hrefs(body.split('## Next step')[0])<=omissions,'Active revision loses a primary evidence destination')
                if payload.get('footer_contract'):
                    method=payload['footer_contract'].get('method_token')
                    require(isinstance(method,str),'Active footer method token missing')
                    from library_publication_method_label import validate_composite_method_label
                    validate_composite_method_label(self,rel,method=method,raw_full=full,post_finite_body=stage,prior_payload=prior_payload,revision=revision,payload=payload)
                origin='explicit-reviewed-active-revision'
            else:
                require(prior_payload is not None,'Untouched effective payload missing')
                require(self.prior['raw_source_pins'].get(rel)==note['canonical_source_sha256'],'Raw source changed outside the active revision group')
                payload=copy.deepcopy(prior_payload)
                meta,body,head=payload_hashes(payload,self.finite)
                origin='exact-prior-effective-payload'
                self.retained_prior_paths.append(rel)
            require(meta.get('library_cluster')==raw_meta.get('library_cluster'),'Effective revision changes protected cluster')
            for field in set(raw_meta)|set(meta):
                if raw_meta.get(field)!=meta.get(field):
                    require(field in {'title','headline','description','also_asked_as','library_subtopic','date_modified'},'Effective revision changes protected metadata')
            require(body.startswith('# '+meta['title']+'\n') and meta['headline']==meta['title'],'Effective H1/title/headline differ')
            effective=payload['effective_full_source'];effective_sha=sha(effective.encode())
            metadata_delta={k:{'old':raw_meta.get(k),'new':copy.deepcopy(meta.get(k))} for k in set(raw_meta)|set(meta) if raw_meta.get(k)!=meta.get(k)}
            record={'path':rel,'file':self.docs/rel,'meta':copy.deepcopy(meta),'cluster':meta['library_cluster'],
                'body':body,'source_sha256':sha(raw),'canonical_source_sha256':effective_sha,
                'raw_canonical_source_sha256':sha(full.encode()),'post_finite94_body_sha256':sha(stage.encode()),
                'effective_canonical_source_sha256':effective_sha,'effective_body_sha256':sha(body.encode()),
                'effective_full_source':effective,'raw_head':raw_head,'effective_head':head,
                'raw_head_sha256':sha(raw_head.encode()),'effective_head_sha256':sha(head.encode()),
                'raw_meta':raw_meta,'metadata_delta':metadata_delta,'effective_meta_sha256':json_hash(self.q,meta),
                'operations':[],'inverse_reconstructs_post_finite94':False,'composition_origin':origin,
                'review_ids':copy.deepcopy(payload.get('review_ids',{}))}
            self.records[rel]=record
            for kind in ['source','writing']:
                if not self._article_receipt(record['review_ids'].get(kind),record,kind):
                    self._s5_issue(rel,'Fresh complete current '+kind+' receipt missing')
            for issue in neutral_footer_issues(self,rel,record,payload.get('footer_contract')):
                self._s5_issue(rel,issue)
            try:remove_exact_qualifier(body)
            except ValueError as error:self._s5_issue(rel,str(error))
            try:self._validate_related(rel,body,self.mapping['pages'].get(rel) or note.get('related_requirements',{}))
            except ValueError as error:self._s5_issue(rel,str(error))
            # Compare retained payload exactly, even its head whitespace and metadata serialization.
            if rel not in active:require(payload==prior_payload,'Untouched prior payload changed during composition')
        if self._field_stamp is not None:
            if self.s5_scope is not None:require(isinstance(frozen_effective_pins,dict) and set(frozen_effective_pins)==set(self.s5_scope.frozen),'Frozen effective pins must cover exactly the accepted45')
            frozen_receipt=self._load_receipt(trust.frozen_receipt_sha256)
            require(frozen_receipt and frozen_receipt.get('approved') is True
                and frozen_receipt.get('review_kind')=='field-test-freeze'
                and frozen_receipt.get('handoff_sha256')==sha(self._field_stamp)
                and frozen_receipt.get('frozen_effective_pins')==frozen_effective_pins and frozen_effective_pins,
                'Existing field-test handoff lacks exact independent frozen served pins')
            enforce_frozen_articles(self,frozen_effective_pins)
        if self.s5_scope is not None:self.s5_scope.validate_records(self.records)
        self._check_unchanged()
        return self

    def _check_unchanged(self):
        super()._check_unchanged()
        if self.s5_scope is not None:self.s5_scope.assert_current()
        if hasattr(self,'_field_handoff'):
            now=self._field_handoff.read_bytes() if self._field_handoff.exists() else None
            require(now==self._field_stamp,'Field-test handoff appeared or changed during/after composition')

    def metadata_consumer_errors(self):
        # Composition always uses one effective registry, including already-published overlays.
        fingerprint=self.public_metadata_fingerprint()
        return ['Effective metadata consumer missing/stale: '+name for name in ['page-head-and-structured-data','library-hubs','llms'] if self.metadata_consumers.get(name)!=fingerprint]

    def composition_receipt(self):
        return {'retained_prior_effective_paths':self.retained_prior_paths,'active_revision_paths':self.active_revision_paths,
            'retired_raw_history_paths':sorted(self.merge_statuses),
            'all_records':len(self.records),'retained_payloads_byte_exact':True,'whole_current_gate_required':True,
            'all300_compiler_invoked':False,'baseline_exceptions':0,'publication_authority':not self.pending and (self._eligible_current_passed if self.s5_scope is not None else self._strict_current_passed),
            'all_published_current_passed':False if self.s5_scope is not None else self._strict_current_passed,
            'current_rule_scope':'ELIGIBLE_UNFROZEN' if self.s5_scope is not None else 'ALL_EFFECTIVE_ARTICLES',
            'deferred_frozen_status':'DEFERRED_FIELD_TEST' if self.s5_scope is not None else None,
            'deferred_frozen_paths':sorted(self.s5_scope.frozen) if self.s5_scope is not None else []}
