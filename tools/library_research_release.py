"""Separate finite53/60 Research permit; never an ordinary S5 cap exception.

Only a Library-reviewed current source/artifact plan can construct this token.
Every public byte delta is counted, including53ResearchHTML/sevendata/derived
outputs. Source/render/search/quality/freeze checks are separate prerequisites.
"""
from pathlib import Path
from collections import Counter
import copy,json,re,hashlib
from library_research_support import require,sha,qsha,URLS,ResearchSupport,PLAN,PIN,_file
from library_research_source_archive import bind_source_archives

POLICY='LIBRARY_FINITE_RESEARCH_RELEASE_53_60_V1'
PATHS_SHA256='da6a14368425acaacae6e857e8b13f74fb4a67ccb38694114cb16366f7ae58d9'
_TOKEN=object()
_PROOF_TOKEN=object()
PRIVATE_SIDECARS={'relaunch-build-provenance.json','library-release-proof.json','library-effective-payload.json','library-compiled-state.json'}

def paths():
    raw=Path(__file__).with_name('library_research_release_paths.json').read_bytes()
    require(sha(raw)==PATHS_SHA256,'Finite Research path catalog changed')
    d=json.loads(raw)
    require(len(d['source_paths'])==60 and len(d['article_artifact_paths'])==53
        and len(d['data_artifact_paths'])==7 and len(d['immutable_science_and_registered_downloads'])==56
        and len(d['Owner11_rebased_claim_sources'])==11,'Research finite path/count declaration differs')
    return d

def _safe(path):
    require(isinstance(path,str) and path and '\\' not in path and not path.startswith('/')
        and ':' not in path and '..' not in Path(path).parts,'Unsafe Research relative path')

class ResearchReleasePermit:
    def __init__(self,root,data,support,research_records,candidate_source_pins,token):
        require(token is _TOKEN,'Research permit requires an independently reviewed exact plan')
        self.root=Path(root);self.data=copy.deepcopy(data);self.support=support
        self.research_records=copy.deepcopy(research_records);self._proofs={};self._proof_pins={}
        self._source_pins=copy.deepcopy(candidate_source_pins)
        self._seal=(str(self.root.resolve()),qsha(data),qsha(self.research_records),qsha(self._source_pins))
    def check(self):
        require(self._seal==(str(self.root.resolve()),qsha(self.data),qsha(self.research_records),qsha(self._source_pins)),'Bound Research plan changed')
        self.support.assert_current()
        require(self._proof_pins=={k:qsha(v) for k,v in self._proofs.items()},'Research proof cache changed outside owning validators')
    @property
    def proofs(self):return copy.deepcopy(self._proofs)
    def _record_proof(self,name,value,token):
        self.check();require(token is _PROOF_TOKEN,'Caller-created Research proof forbidden')
        self._proofs[name]=copy.deepcopy(value);self._proof_pins[name]=qsha(value)
    def check_sources(self):
        self.check()
        for path,digest in self._source_pins.items():
            require(sha(_file(self.root,path).read_bytes())==digest,
                'Exact tracked Research/Library/code source changed after binding: '+path)
    def expected_artifact_paths(self):
        self.check();return set(self.data['artifact_changes'])
    def verify_public_delta(self,prior,candidate,*,frozen_pins,exact_stub_bytes,
                            library_artifact_paths,protected_scientific_pins):
        self.check();catalog=paths()
        private_delta={p for p in PRIVATE_SIDECARS if prior.get(p)!=candidate.get(p)}
        prior={p:r for p,r in prior.items() if p not in PRIVATE_SIDECARS}
        candidate={p:r for p,r in candidate.items() if p not in PRIVATE_SIDECARS}
        actual={p for p in set(prior)|set(candidate) if prior.get(p)!=candidate.get(p)}
        require(actual==set(self.data['artifact_changes']),'Actual whole public Research delta differs from exact Root map')
        allowed=set(catalog['article_artifact_paths'])|set(catalog['data_artifact_paths'])|set(catalog['allowed_derived_artifact_paths'])
        require(actual<=allowed,'Unlisted public/nonlibrary/Manual/CSS/Library artifact changed')
        for path,row in self.data['artifact_changes'].items():
            require(row['before_sha256']==(sha(prior[path]) if path in prior else None)
                and row['after_sha256']==(sha(candidate[path]) if path in candidate else None),
                'Actual Research artifact before/after bytes differ: '+path)
        for p in library_artifact_paths:
            require(p in prior and candidate.get(p)==prior[p],'Library article/hub bytes changed during Research release')
        require(len(exact_stub_bytes)==19,'Research release lost inherited19 disposition closure')
        for p,raw in exact_stub_bytes.items():
            require(prior.get(p)==raw==candidate.get(p),'Inherited canonical200 stub bytes changed')
        require(len(frozen_pins)==50,'Research exact45HTML+5presentation freeze incomplete')
        for p,digest in frozen_pins.items():require(sha(candidate.get(p,b''))==digest,'Frozen public artifact changed')
        require(protected_scientific_pins==catalog['immutable_science_and_registered_downloads'],
            'Protected53scientificCSV/3registered-download identity differs')
        for p,digest in protected_scientific_pins.items():
            require(p in prior and sha(prior[p])==digest==sha(candidate.get(p,b'')),
                'Original scientific/registered public bytes changed')
        result={'policy':POLICY,'changed_artifact_paths':sorted(actual),
            'actual_changed_artifact_count':len(actual),'ordinary_S5_cap_changed':False,
            'unchanged_Library_article_hub_and_19stub_bytes':True,
            'all56_scientific_registered_downloads_exact':True,'full_current_S5_PASS_granted':False,
            'existing_owning_private_sidecars_not_public_routes':sorted(private_delta)}
        self._record_proof('whole_public_delta',result,_PROOF_TOKEN)
        return result
    def finish(self):
        self.check_sources()
        needed={'sources','render','sitemap','search','library_consumers','quality','freeze','stubs','PDF','whole_public_delta'}
        require(set(self.proofs)==needed,'Research release lacks complete actual proof closure')
        review=self.data.get('artifact_review',{})
        require(review.get('approved') is True and review.get('review_kind')=='root-exact-research-candidate-artifacts'
            and review.get('Root_actual_full_candidate_read') is True
            and review.get('artifact_changes_object_sha256')==qsha(self.data['artifact_changes'])
            and review.get('new_interpretation_PDF_Source_text_and_Root_visual_read') is True,
            'Actual Root candidate/PDF artifact review remains pending')
        pdf=self.data.get('notice_PDF_review',{})
        notice='research/data/report-interpretation-notice-2026-11-03.pdf'
        require(pdf.get('approved') is True and pdf.get('path')==notice
            and pdf.get('sha256')==self.data['artifact_changes'].get(notice,{}).get('after_sha256')
            and pdf.get('Source_full_text_read') is True and pdf.get('Root_all_pages_visually_read') is True
            and isinstance(pdf.get('pages'),int) and pdf['pages']>0
            and len(pdf.get('actual_original_page_image_sha256',[]))==pdf['pages']
            and all(re.fullmatch('[0-9a-f]{64}',str(v)) for v in pdf['actual_original_page_image_sha256'])
            and re.fullmatch('[0-9a-f]{64}',str(pdf.get('full_text_sha256'))),
            'Exact new interpretation-notice PDF Source/full-text/all-page visual proof missing')
        return {'policy':POLICY,'finite_Research_release_passed':True,'whole_current_Library_S5_PASS':False,
            'ordinary_S5_cap_changed':False,'proofs':copy.deepcopy(self.proofs)}

def bind_release(root,raw,expected_sha256,*,support,actual_prior_binding,
                 prior_source_archive_raw,candidate_source_archive_raw,prior_public_files,
                 current_payload,prior_state,producer_raw):
    require(isinstance(support,ResearchSupport),'Research release needs exact reviewed module/policy support')
    support.assert_current();require(sha(raw)==expected_sha256,'Research release plan bytes differ')
    ref=support.plan.get('release_inputs',{})
    require(ref.get('sha256')==expected_sha256 and _file(support.root,ref.get('path','')).read_bytes()==raw,
        'Research release is not the exact committed Root aggregate source/evidence plan')
    d=json.loads(raw);catalog=paths()
    require(d.get('schema_version')==1 and d.get('policy')==POLICY
        and d.get('approved') is True and d.get('review_kind')=='library-root-reviewed-finite-research-release'
        and d.get('Root_actual_source_review_complete') is True,'Actual finite Library Research source review missing')
    producer=json.loads(producer_raw)
    require(producer.get('approved') is True and producer.get('review_kind')=='prior-production-effective-payload'
        and producer.get('actual_served_readback') is True and producer.get('source_render_equality_passed') is True
        and producer.get('hub_source_render_equality_passed') is True,'Actual postOwner Library producer not approved')
    require(d.get('production_receipt_sha256')==sha(producer_raw)
        and d.get('production_binding')==producer.get('production_binding')==actual_prior_binding==prior_state.get('production_binding'),
        'Research plan is not bound to actual current production')
    prior_source_files,candidate_source_files=bind_source_archives(producer=producer,
        prior_archive_raw=prior_source_archive_raw,candidate_archive_raw=candidate_source_archive_raw,
        approved_candidate_inventory_sha256=d.get('candidate_source_inventory_sha256'),root=Path(root))
    pages=set(current_payload.get('pages',{}));stubs=prior_state.get('merged_sources',{})
    require(len(pages)==307 and len(stubs)==19 and len(prior_state.get('raw_source_pins',{}))==326
        and not pages&set(stubs),'Research baseline must be actual307/326raw/19canonical200')
    require(d.get('current_payload_object_sha256')==qsha(current_payload)
        and d.get('inherited_dispositions_sha256')==qsha(stubs),'Research changed actual Library payload/disposition identity')
    quality=prior_state.get('current_quality_snapshot',{})
    require(quality.get('analysis_completed') is True and quality.get('baseline_exceptions')==0
        and set(quality.get('page_readiness',{}))==pages,'Actual Library whole current report missing')
    for name in ['literal','runtime']:
        scope=quality.get('comparison_scopes',{}).get(name,{})
        require(scope.get('all_pairs_compared') is True and scope.get('pair_count')==46971,
            'Actual Library both46971 comparison proof missing')
    frozen={p for p,r in quality['page_readiness'].items() if r.get('status')=='DEFERRED_FIELD_TEST'}
    require(len(frozen)==45 and all(quality['page_readiness'][p].get('passed') is None for p in frozen),
        'Exactly45 deferred, never PASS, required')
    require(set(d.get('source_files',{}))==set(catalog['source_paths']),
        'Only exact60 Research source inputs supported')
    source_delta={p for p in set(prior_source_files)|set(candidate_source_files) if prior_source_files.get(p)!=candidate_source_files.get(p)}
    # Library authors the independently reviewed support plan/pin pair; Research
    # authors only docs/research. No other shared/source changes can be hidden.
    code=d.get('Library_owned_activation_before_pins',{})
    require(set(code)=={PLAN,PIN},
        'Unlisted shared Research activation source')
    from library_research_activation_controls import validate_activation_delta
    activation=validate_activation_delta(root,support,d,prior_source_files,candidate_source_files)
    require(source_delta<=set(catalog['source_paths'])|set(code)|activation,'Unrelated source/config/Library edit in Research release')
    for path,row in d['source_files'].items():
        _safe(path)
        require(row.get('before_sha256')==(sha(prior_source_files[path]) if path in prior_source_files else None)
            and row.get('after_sha256')==(sha(candidate_source_files[path]) if path in candidate_source_files else None),
            'Research current source before/after pin differs: '+path)
    for path,before_pin in code.items():
        require(before_pin==(sha(prior_source_files[path]) if path in prior_source_files else None)
            and candidate_source_files.get(path)==_file(support.root,path).read_bytes(),
            'Research exact Library control source binding differs')
    reviews=d.get('full_source_reviews',{})
    sources={p for p in catalog['source_paths'] if p.endswith('.md')}
    require(set(reviews)==sources,'Exact53 current full-source review bindings required')
    require(d.get('source_read_evidence_map_sha256')==qsha(reviews),
        'Root aggregate Research approval does not bind actual53 read-evidence map')
    import library_related_chapter_links as finite
    research_records={};before_research_records={}
    for source in sorted(sources):
        after=candidate_source_files[source].decode('utf-8-sig').replace('\r\n','\n').replace('\r','\n')
        meta,body=finite.source_body(after);review=reviews[source]
        old_full=prior_source_files[source].decode('utf-8-sig').replace('\r\n','\n').replace('\r','\n')
        evidence=review.get('evidence_receipt',{})
        require(set(evidence)=={'path','sha256'}
            and support.plan.get('staged_file_sha256',{}).get(evidence.get('path'))==evidence.get('sha256'),
            'Research actual read evidence is not in exact committed file closure')
        evidence_raw=_file(support.root,evidence['path']).read_bytes()
        require(sha(evidence_raw)==evidence['sha256']
            and json.loads(evidence_raw)=={k:v for k,v in review.items() if k!='evidence_receipt'},
            'Research actual read evidence missing/forged/different')
        require(review.get('approved') is True and review.get('current_full_file_actually_read') is True
            and review.get('review_kind')=='reviewed-current-research-source'
            and review.get('scope')=='Research-release-current-source-reading'
            and review.get('path')==source and isinstance(review.get('reviewer'),str) and review['reviewer'].strip()
            and isinstance(review.get('actual_read_scope'),str) and review['actual_read_scope'].strip()
            and review.get('before_canonical_source_sha256')==sha(old_full.encode())
            and review.get('after_canonical_source_sha256')==sha(after.encode())
            and review.get('after_body_sha256')==sha(body.encode())
            and review.get('after_metadata_sha256')==qsha(meta),
            'Research full-source review is missing/stale: '+source)
        old_meta,old_body=finite.source_body(old_full)
        before_research_records[source.removeprefix('docs/')]=dict(meta=old_meta,body=old_body,effective_full_source=old_full)
        require(meta.get('date_published')==old_meta.get('date_published'),
            'Research original publication date changed')
        require(meta.get('title')==old_meta.get('title'),
            'This finite Research release does not authorize global navigation title changes')
        if after!=old_full:
            from library_publication_sitemap_dates import _stamp
            require(_stamp(meta.get('date_modified'))>_stamp(old_meta.get('date_modified')),
                'Research edited source lacks actual newer modification timestamp')
        research_records[source.removeprefix('docs/')]=dict(meta=meta,body=body,effective_full_source=after)
    for p,digest in catalog['immutable_science_and_registered_downloads'].items():
        source='docs/'+p
        require(source in prior_source_files and sha(prior_source_files[source])==digest
            and sha(candidate_source_files.get(source,b''))==digest
            and sha(prior_public_files.get(p,b''))==digest,'Original scientific/registered source or public pin differs')
    from library_research_owner_preservation import validate_required_owner11
    owner11=validate_required_owner11(root=root,support=support,data=d,
        before_records=before_research_records,after_records=research_records)
    require(set(d.get('artifact_changes',{}))<=set(catalog['article_artifact_paths'])|set(catalog['data_artifact_paths'])|set(catalog['allowed_derived_artifact_paths']),
        'Root Research public map contains an out-of-scope file')
    result=ResearchReleasePermit(root,d,support,research_records,
        {p:sha(raw) for p,raw in candidate_source_files.items()},_TOKEN)
    result._record_proof('sources',{'complete_prior_GitLF_archive_producer_bound':True,
        'complete_candidate_GitLF_inventory_Root_bound':True,'only_finite60_plus_exact_Library_controls':True,
        'all53_current_full_source_reviews_bound':True,'all11_Owner_claim_sources_reconciled':True,
        'Owner11_complete_Source_required_preservation':owner11},_PROOF_TOKEN)
    return result

def validate_quality_identity(before,after):
    """No Library body/peer edit is permitted; both scopes remain independent."""
    require(before.get('analysis_completed') is True and after.get('analysis_completed') is True
        and before.get('baseline_exceptions')==after.get('baseline_exceptions')==0,
        'Research must retain truthful complete Library analysis')
    require(before['page_readiness']==after['page_readiness'],'Library readiness/peer/rule row changed during Research release')
    require(before.get('global_fatal_errors')==after.get('global_fatal_errors')
        and before.get('passed')==after.get('passed'),
        'Research introduced a global Library failure or invented wholePASS')
    for name in ['literal','runtime']:
        a=before['comparison_scopes'][name];b=after['comparison_scopes'][name]
        require(a['pair_count']==b['pair_count']==46971 and a['all_pairs_compared'] is b['all_pairs_compared'] is True
            and a['violations']==b['violations'],'One Library comparison scope changed/regressed')
    return {'actual307_Library_readiness_unchanged':True,'both46971_unchanged':True,
        'actual_readiness_counts':dict(Counter(r['status'] for r in after['page_readiness'].values())),
        'S5_full_PASS_granted':False}
