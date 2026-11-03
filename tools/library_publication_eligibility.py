"""The accepted finite45 S5 exclusion; never a caller-defined skiplist."""
from __future__ import annotations
import json
from pathlib import Path
import library_publication_field_freeze as field
from library_publication_overlay import require,sha,canonical

DEFERRED='DEFERRED_FIELD_TEST'

class Finite45Eligibility:
    def __init__(self,freeze,docs,raw_universe):
        require(isinstance(freeze,field.FieldFreeze) and freeze.registry_sha256==field.ROOT_REGISTRY_SHA256,'Eligibility needs the exact accepted Root freeze registry')
        freeze.assert_current();raw=freeze.registry_path.read_bytes();require(sha(raw)==field.ROOT_REGISTRY_SHA256,'Off-registry eligibility exception')
        data=json.loads(raw);rows=data['rows'];self.rows={r['source_path']:r for r in rows}
        require(len(rows)==len(self.rows)==45 and data['activation_authorized'] is False and data['experiment_edits_applied']==0,'Eligibility is only the accepted45, without activation')
        for path,row in self.rows.items():
            require(row['url']=='https://docs.broadcastwell.com/'+path.removesuffix('.md')+'/' and row['source_sha256']==row['active_canonical_sha256'],'Frozen canonical URL/source binding differs')
        self.freeze=freeze;self.docs=Path(docs).resolve();self.raw_universe=frozenset(raw_universe);self.frozen=frozenset(self.rows)
        require(self.frozen<=self.raw_universe,'Accepted frozen leaf disappeared from actual universe')
        self.raw_stamps={p:sha((self.docs/p).read_bytes()) for p in self.frozen};self._preserved=False
        self._registry_sha256=freeze.registry_sha256
        self._rows_seal=sha(json.dumps(self.rows,sort_keys=True,ensure_ascii=False).encode())
        self._registry_semantic_seal=sha(json.dumps(data,sort_keys=True,ensure_ascii=False).encode())
        self.assert_current()
    def assert_current(self):
        require(self.freeze.registry_sha256==self._registry_sha256 and sha(json.dumps(self.rows,sort_keys=True,ensure_ascii=False).encode())==self._rows_seal and sha(json.dumps(self.freeze.data,sort_keys=True,ensure_ascii=False).encode())==self._registry_semantic_seal,'Finite eligibility/preservation data changed after binding')
        self.freeze.assert_current();self.freeze.check_sources(self.docs)
        require(all(sha((self.docs/p).read_bytes())==h for p,h in self.raw_stamps.items()),'Frozen raw source packaging changed during eligibility run')
    def partition(self,paths):
        self.assert_current();paths=set(paths)
        require(self.frozen<=paths<=self.raw_universe,'Effective eligibility universe hides frozen or adds unknown leaf')
        return paths-set(self.frozen),set(self.frozen)
    def validate_records(self,records):
        self.partition(records)
        for path,row in self.rows.items():
            record=records[path]
            require(record['raw_canonical_source_sha256']==row['source_sha256'] and record.get('composition_origin')=='exact-prior-effective-payload','Frozen effective record lacks its exact accepted source/prior origin')
    def reject_active(self,active,merges=()):
        self.partition(self.raw_universe);require(not self.frozen&set(active),'Frozen source cannot receive an active S5 revision')
        require(not self.frozen&set(merges),'Frozen source cannot be merged')
    def certify_artifacts(self,files):
        self._preserved=False;self.assert_current();self.freeze.check_files(files);self._preserved=True
    @property
    def preservation_passed(self):self.assert_current();return self._preserved is True
    def validate_state(self,state,previous=None):
        articles={r['path'] for r in state['routes'].values() if r['kind']=='article'};self.partition(articles)
        for p,row in self.rows.items():
            route='/'+p.removesuffix('.md')+'/'
            require(state['routes'][route]['compiled_sha256']==row['served_html_sha256'] and state['raw_source_pins'][p]==row['source_sha256'],'Frozen compiled/source pin changed')
            if previous is not None:require(state['routes'][route]==previous['routes'].get(route),'Frozen body/metadata/compiled route changed')
    def description(self,paths,published_paths=None):
        eligible,frozen=self.partition(paths)
        if published_paths is not None:require(self.frozen<=set(published_paths),'Prior actual publication lacks accepted sample')
        return {'authority':'Brief S5 explicit accepted field-test exclusion','registry_sha256':self.freeze.registry_sha256,
            'actual_published_article_count':len(published_paths) if published_paths is not None else None,
            'actual_published_eligible_count':len(set(published_paths)-self.frozen) if published_paths is not None else None,
            'candidate_effective_article_count':len(eligible)+45,'eligible_count':len(eligible),'deferred_count':45,
            'eligible_paths':sorted(eligible),'deferred_paths':sorted(frozen),'deferred_status':DEFERRED,'baseline_exceptions':0}
    def decorate(self,result,overlay):
        self.validate_records(overlay.records);eligible,frozen=self.partition(overlay.records)
        ready=result['page_readiness']
        require(set(ready)==set(overlay.records),'Readiness hides a published effective record')
        for p in frozen:require(ready[p].get('status')==DEFERRED and ready[p].get('passed') is None,'Frozen row must be DEFERRED_FIELD_TEST, never PASS/FAIL')
        previous=getattr(overlay,'prior',{}).get('routes');published={r['path'] for r in previous.values() if r['kind']=='article'} if previous is not None else None
        blocked=[];deferred=[]
        for violation in result['violations']:
            paths=set(violation['pages']);require(paths and paths<=set(overlay.records),'Unscoped collection violation')
            (blocked if paths&eligible else deferred).append(violation)
        passed=result['analysis_completed'] and not result['global_fatal_errors'] and not blocked and all(ready[p].get('passed') is True for p in eligible)
        result.update(s5_scope=self.description(overlay.records,published),eligible_current_passed=passed,
            eligible_completion_passed=passed and self.preservation_passed,frozen_preservation_passed=self.preservation_passed,
            eligible_blocking_violations=blocked,deferred_frozen_only_violations=deferred,passed=False,full_current_passed=False,
            all_published_current_passed=False,explicit_field_exception=True,
            leaf_count=len(overlay.records),eligible_leaf_count=len(eligible),deferred_leaf_count=45,
            grandfathered_cases=[],current_baseline_exceptions=0,
            policy='Exact accepted finite45 S5 exclusion; every eligible leaf current; frozen rows never PASS.')
        return result
    def validate_report(self,report,state,previous):
        self.validate_state(state,previous)
        paths={r['path'] for r in state['routes'].values() if r['kind']=='article'};published={r['path'] for r in previous['routes'].values() if r['kind']=='article'}
        require(report.get('s5_scope')==self.description(paths,published),'S5 eligibility report is off-registry or hides eligible leaves')
        ready=report['page_readiness'];eligible,frozen=self.partition(paths)
        for p in frozen:require(ready[p].get('status')==DEFERRED and ready[p].get('passed') is None,'Frozen article cannot be reported PASS')
        for p in eligible:require(ready[p].get('status')==('PASS' if ready[p].get('passed') is True else 'FAIL'),'Eligible article cannot be deferred')
        relevant=[v for v in report['violations'] if set(v['pages'])&eligible]
        passed=not relevant and all(ready[p].get('passed') is True for p in eligible) and not report['global_fatal_errors']
        require(report.get('eligible_current_passed') is passed and report.get('passed') is False and report.get('all_published_current_passed') is False,'Eligible/global PASS contradicts explicit frozen deferral')
        require(report.get('frozen_preservation_passed') is self.preservation_passed,'Frozen preservation proof is missing/stale')
        return eligible,frozen,passed

def scope_for(overlay):
    scope=getattr(overlay,'s5_scope',None)
    if scope is not None:require(isinstance(scope,Finite45Eligibility),'Arbitrary S5 skiplist is forbidden');scope.validate_records(overlay.records)
    return scope
