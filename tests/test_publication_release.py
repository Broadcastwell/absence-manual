"""Synthetic private regressions for real301s and bounded incremental gates."""
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import unittest

from test_publication_overlay import Fixture, q, encoded
from library_publication_overlay import OverlayError, sha
from library_publication_release import (MergeTrust, apply_reviewed_merges,
    route_for, route_forms, render_merged_redirects, validate_merge_build,
    exclude_merged_files, make_compiled_state, state_fingerprint,
    full_report_binding, incremental_release_gate, require_full_completion,
    complete_current_analysis)
from library_publication_release import prepare_incremental_permit


class StateFixture:
    def __init__(self, directory, count=8):
        self.path = Path(directory) / 'prior-state.json'
        self.paths = [f'answers/measurement/page-{i}.md' for i in range(count)]
        self.binding = {'commit_sha':'a'*40,'deployment_id':'fixture-production','artifact_sha256':'b'*64,'served_receipt_sha256':'c'*64}
        self.prior = {'schema_version':1,'routes':{},'raw_source_pins':{path:sha(('raw'+path).encode()) for path in self.paths},'merged_sources':{},'production_binding':self.binding}
        for path in self.paths:
            self.prior['routes'][route_for(path)] = {'kind':'article','path':path,'effective_canonical_sha256':sha(('effective'+path).encode()),'body_sha256':sha(('body'+path).encode()),'metadata_sha256':sha(('meta'+path).encode()),'compiled_sha256':sha(('html'+path).encode())}
        self.prior['routes']['/answers/measurement/'] = {'kind':'auxiliary','compiled_sha256':sha(b'old hub')}
        self.prior['routes']['/llms.txt'] = {'kind':'auxiliary','compiled_sha256':sha(b'old llms')}
        self.old_violation = {'kind':'six_word_similarity','key':'fixture-old-pair','pages':self.paths[-2:],'score_fraction':'1/4'}
        self.prior['current_quality_snapshot'] = {'compiled_collection_fingerprint':state_fingerprint(self.prior,q),'analysis_completed':True,'baseline_exceptions':0,'violations':[self.old_violation],
            'page_readiness':{path:{'passed':path not in self.old_violation['pages'],'errors':[] if path not in self.old_violation['pages'] else [self.old_violation]} for path in self.paths}}
        self.save()
        self.current = copy.deepcopy(self.prior)
        self.map = {}
        self.change(self.paths[0])
        self.report = self.make_report()

    def save(self):
        self.path.write_bytes(encoded(self.prior)); self.trusted = sha(self.path.read_bytes())

    def change(self, path):
        row = self.current['routes'][route_for(path)]
        row.update(effective_canonical_sha256=sha(('new-effective'+path).encode()),body_sha256=sha(('new-body'+path).encode()),metadata_sha256=sha(('new-meta'+path).encode()),compiled_sha256=sha(('new-html'+path).encode()))
        self.map[path] = {'before_effective_canonical_sha256':self.prior['routes'][route_for(path)]['effective_canonical_sha256'],'after_effective_canonical_sha256':row['effective_canonical_sha256'],'after_body_sha256':row['body_sha256'],'after_metadata_sha256':row['metadata_sha256']}

    def make_report(self, violations=None):
        paths = sorted(row['path'] for row in self.current['routes'].values() if row['kind']=='article')
        violations = copy.deepcopy([self.old_violation] if violations is None else violations)
        readiness = {path:{'passed':True,'errors':[]} for path in paths}
        for row in violations:
            for path in row['pages']: readiness[path] = {'passed':False,'errors':[row]}
        aux = [route for route,row in self.current['routes'].items() if row['kind']=='auxiliary' and row!=self.prior['routes'].get(route)]
        return {**full_report_binding(self.current,q),'analysis_completed':True,'all_pairs_compared':True,'pair_count':len(paths)*(len(paths)-1)//2,'baseline_exceptions':0,'page_readiness':readiness,'violations':violations,'global_fatal_errors':[],'validated_changed_auxiliary_routes':aux,'passed':not violations,'merge_build_passed':True}

    def gate(self, **updates):
        args = {'previous_manifest_path':self.path,'trusted_previous_sha256':self.trusted,'actual_prior_production_binding':self.binding,'candidate_state':self.current,'actual_candidate_state':copy.deepcopy(self.current),'authorized_change_map':self.map,'full_current_report':self.report,'q':q}
        args.update(updates)
        return incremental_release_gate(**args)


class IncrementalTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.fx = StateFixture(self.temp.name)

    def test_group_pass_keeps_untouched_failures_and_final_closed(self):
        result = self.fx.gate()
        self.assertTrue(result['incremental_release_passed'])
        self.assertFalse(result['full_current_passed'])
        self.assertEqual(2,result['untouched_failure_count'])
        self.assertEqual(0,result['baseline_exceptions'])
        with self.assertRaisesRegex(OverlayError,'full current PASS'):
            require_full_completion(result)

    def test_scope_is_actual_diff_not_map_whitelist(self):
        with self.assertRaisesRegex(OverlayError,'all actual changed'):
            self.fx.gate(authorized_change_map={})

    def test_extra_unchanged_map_page_cannot_expand_scope(self):
        allowed = copy.deepcopy(self.fx.map); allowed[self.fx.paths[1]] = copy.deepcopy(next(iter(allowed.values())))
        with self.assertRaisesRegex(OverlayError,'all actual changed'):
            self.fx.gate(authorized_change_map=allowed)

    def test_hidden_actual_body_or_metadata_change_rejected(self):
        actual = copy.deepcopy(self.fx.current)
        actual['routes'][route_for(self.fx.paths[1])]['metadata_sha256'] = 'e'*64
        with self.assertRaisesRegex(OverlayError,'hides actual compiled'):
            self.fx.gate(actual_candidate_state=actual)

    def test_authorized_map_is_exact_body_and_metadata(self):
        self.fx.map[self.fx.paths[0]]['after_body_sha256'] = 'f'*64
        with self.assertRaisesRegex(OverlayError,'exact authorized map'):
            self.fx.gate()

    def test_prior_manifest_requires_actual_production_binding(self):
        wrong = dict(self.fx.binding,commit_sha='d'*40)
        with self.assertRaisesRegex(OverlayError,'actual current production'):
            self.fx.gate(actual_prior_production_binding=wrong)

    def test_prior_bytes_tamper_rejected(self):
        self.fx.path.write_bytes(self.fx.path.read_bytes()+b' ')
        with self.assertRaisesRegex(OverlayError,'Trusted input bytes changed'):
            self.fx.gate()

    def test_cap_is_no_more_than_fifty_actual_routes(self):
        self.fx = StateFixture(self.temp.name, count=60)
        for path in self.fx.paths[:51]: self.fx.change(path)
        self.fx.report=self.fx.make_report()
        result=self.fx.gate()
        self.assertFalse(result['incremental_release_passed']); self.assertEqual(51,result['changed_route_count'])
        with self.assertRaisesRegex(OverlayError,'cannot exceed50'):
            self.fx.gate(maximum_changed_routes=51)

    def test_hub_and_llms_changes_count_toward_cap(self):
        self.fx.current['routes']['/answers/measurement/']['compiled_sha256']=sha(b'new hub')
        self.fx.current['routes']['/llms.txt']['compiled_sha256']=sha(b'new llms')
        self.fx.report=self.fx.make_report()
        result=self.fx.gate(); self.assertTrue(result['incremental_release_passed']); self.assertEqual(3,result['changed_route_count'])

    def test_changed_page_cannot_inherit_old_violation(self):
        violation={'kind':'lead_figure_limit','key':'old-overloaded-fact','pages':self.fx.paths[:4],'count':4}
        self.fx.prior['current_quality_snapshot']['violations'].append(violation); self.fx.save()
        self.fx.report=self.fx.make_report([self.fx.old_violation,violation])
        result=self.fx.gate(); self.assertFalse(result['incremental_release_passed'])

    def test_new_untouched_adjacency_also_blocks_group(self):
        violation={'kind':'opening_adjacency','key':'new-pair-after-merge','pages':self.fx.paths[3:5]}
        self.fx.report=self.fx.make_report([self.fx.old_violation,violation])
        result=self.fx.gate(); self.assertFalse(result['incremental_release_passed'])
        self.assertTrue(any(isinstance(error,dict) and error.get('kind')=='new_or_worse_untouched_violation' for error in result['errors']))

    def test_new_untouched_readiness_failure_is_not_an_expiry_exemption(self):
        untouched=self.fx.paths[2]
        self.fx.report['page_readiness'][untouched]={'passed':False,'errors':['UTC price receipt expired']}
        result=self.fx.gate()
        self.assertFalse(result['incremental_release_passed'])
        self.assertTrue(any(isinstance(e,dict) and e.get('kind')=='new_untouched_readiness_failure' for e in result['errors']))

    def test_missing_prior_readiness_rows_are_rejected(self):
        del self.fx.prior['current_quality_snapshot']['page_readiness'][self.fx.paths[-1]];self.fx.save()
        with self.assertRaisesRegex(OverlayError,'complete readiness rows'):
            self.fx.gate()

    def test_sitemap_gzip_search_changes_all_count_toward_cap(self):
        for route in ['/sitemap.xml','/sitemap.xml.gz','/search/search_index.json']:
            self.fx.current['routes'][route]={'kind':'auxiliary','compiled_sha256':sha(route.encode())}
        self.fx.report=self.fx.make_report()
        result=self.fx.gate();self.assertTrue(result['incremental_release_passed']);self.assertEqual(4,result['changed_route_count'])

    def test_baseline_allowance_is_rejected(self):
        self.fx.report['baseline_exceptions']=1
        with self.assertRaisesRegex(OverlayError,'allowances are forbidden'):
            self.fx.gate()

    def test_full_collection_report_cannot_hide_unmodified_page(self):
        self.fx.report['effective_article_paths'].remove(self.fx.paths[-1])
        with self.assertRaisesRegex(OverlayError,'hides an effective page'):
            self.fx.gate()

    def test_missing_complete_analysis_rejected(self):
        self.fx.report['all_pairs_compared']=False
        with self.assertRaisesRegex(OverlayError,'comparison evidence incomplete'):
            self.fx.gate()

    def test_raw_change_outside_map_is_rejected(self):
        self.fx.current['raw_source_pins'][self.fx.paths[2]]='f'*64
        self.fx.report=self.fx.make_report()
        with self.assertRaisesRegex(OverlayError,'outside the exact map'):
            self.fx.gate()

    def test_unreviewed_article_removal_is_not_a_merge(self):
        del self.fx.current['routes'][route_for(self.fx.paths[1])]
        self.fx.report=self.fx.make_report()
        with self.assertRaisesRegex(OverlayError,'explicit reviewed disposition'):
            self.fx.gate()

    def test_research_or_client_route_change_forbidden(self):
        self.fx.current['routes']['/research/example/']={'kind':'auxiliary','compiled_sha256':'d'*64}
        self.fx.report=self.fx.make_report()
        with self.assertRaisesRegex(OverlayError,'Client/research/nonlibrary'):
            self.fx.gate()

    def test_merge_and_target_are_coupled_and_both_forms_count(self):
        source,target=self.fx.paths[1],self.fx.paths[0]
        del self.fx.current['routes'][route_for(source)]
        for route in route_forms(source): self.fx.current['routes'][route]={'kind':'redirect','status':301,'target':route_for(target),'source_path':source}
        self.fx.current['merged_sources'][source]={'status':'MERGED_301','article_pass':False,'target_path':target}
        self.fx.map[source]={'status':'MERGED_301','target_path':target}
        self.fx.report=self.fx.make_report()
        # A caller-provided favorable field cannot invent an owning hosting adapter.
        self.fx.report['live_http_301_verified']=True
        result=self.fx.gate(); self.assertFalse(result['incremental_release_passed']); self.assertEqual(3,result['changed_route_count'])
        self.assertEqual('PLANNED_RULES_ONLY_UNVERIFIED',result['merge_hosting_status'])
        self.assertTrue(any('actual hosting routing' in str(e) for e in result['errors']))
        self.fx.current['merged_sources'][source]['article_pass']=True
        with self.assertRaisesRegex(OverlayError,'not be labeled an article PASS'):
            self.fx.gate()

    def test_final_requires_a_separately_clean_full_result(self):
        self.fx.report=self.fx.make_report([])
        result=self.fx.gate(); self.assertTrue(result['full_current_passed']); require_full_completion(result)


class MergeTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.fx=Fixture(self.temp.name); self.base=self.fx.approve_fixture()
        self.source,self.target=self.fx.paths[:2]
        span='of 10 on 1 November 2026.'
        facts=[{'id':'fixture-observation','source_span':span,'target_span':span,'source_span_sha256':sha(span.encode()),'target_span_sha256':sha(span.encode())}]
        row={'target_path':self.target,'source_canonical_sha256':self.base.records[self.source]['raw_canonical_source_sha256'],'target_canonical_sha256':self.base.records[self.target]['raw_canonical_source_sha256'],'target_effective_canonical_sha256':self.base.records[self.target]['effective_canonical_source_sha256'],'required_fact_ids':['fixture-observation'],'preserved_fact_bindings':facts}
        decision={'approved':True,'review_kind':'reviewed-source-fit-merge-301','source_path':self.source,'target_path':self.target,'source_canonical_sha256':row['source_canonical_sha256'],'target_effective_canonical_sha256':row['target_effective_canonical_sha256'],'source_fit_status':'MERGED_301','preserved_fact_bindings_sha256':sha(q.canonical_json(facts).encode()),'fixture_only':True}
        row['decision_receipt_sha256']=self.fx.receipt(decision); self.base.receipt_store.update(self.fx.store)
        self.plan={'schema_version':1,'approved':True,'merges':{self.source:row}}
        self.plan_path=Path(self.temp.name)/'merge.json'
        self.orders={'measurement':[path for path in self.fx.paths if path!=self.source]}

    def merged(self):
        self.plan_path.write_bytes(encoded(self.plan))
        return apply_reviewed_merges(self.base,self.plan_path,MergeTrust(sha(self.plan_path.read_bytes())),hub_orders=self.orders)

    def build(self, overlay):
        existing=b'# Existing rules stay exact\n/old /retained/ 301\n'
        redirects=render_merged_redirects(existing,overlay._merge_plan,overlay.records)
        built={'_redirects':redirects,route_for(self.target).strip('/')+'/index.html':b'<article>actual fixture target</article>'}
        built['answers/measurement/index.html']=self.hub_html(overlay)['measurement'].encode()
        built['answers/index.html']=self.hub_html(overlay)['measurement'].encode()
        return existing,built

    def hub_html(self,overlay):
        return {'measurement':'<article class="md-content__inner md-typeset">'+''.join('<a href="'+route_for(path)+'">Fixture</a>' for path in self.orders['measurement'])+'</article>'}

    def test_merge_excludes_effective_source_preserves_raw_and_pins(self):
        before=(self.fx.docs/self.source).read_bytes(); merged=self.merged()
        self.assertNotIn(self.source,merged.records); self.assertIn(self.source,merged.pins['pages'])
        self.assertIn(self.source,merged.leaf_manifest['pages'])
        self.assertEqual(before,(self.fx.docs/self.source).read_bytes())
        self.assertFalse(merged.merge_statuses[self.source]['article_pass'])
        self.assertFalse(any(row['path']==self.source for row in merged.public_leaf_records()))

    def test_planned_cloudflare_style_rules_both_forms_preserve_prefix_but_do_not_prove_HTTP(self):
        merged=self.merged(); existing,built=self.build(merged)
        self.assertTrue(built['_redirects'].startswith(existing))
        for form in route_forms(self.source): self.assertIn((form+' '+route_for(self.target)+' 301\n').encode(),built['_redirects'])
        result=validate_merge_build(merged,existing_redirects=existing,built_files=built,hub_texts=['target only'],llms_text='target only',hub_html_by_cluster=self.hub_html(merged))
        self.assertTrue(result['passed'])
        self.assertFalse(result['live_http_301_verified']);self.assertFalse(result['hosting_routing_verified']);self.assertFalse(result['merge_publication_allowed'])
        self.assertEqual(2,result['planned_301_forms']);self.assertNotIn('real_301_forms',result)

    def test_html200_fake_or_missing_redirect_rejected(self):
        merged=self.merged(); existing,built=self.build(merged)
        built[route_for(self.source).strip('/')+'/index.html']=b'<meta http-equiv="refresh">'
        with self.assertRaisesRegex(OverlayError,'still has a served HTML'):
            validate_merge_build(merged,existing_redirects=existing,built_files=built,hub_texts=[],llms_text='',hub_html_by_cluster=self.hub_html(merged))

    def test_missing_target_or_source_in_llms_rejected(self):
        merged=self.merged(); existing,built=self.build(merged)
        with self.assertRaisesRegex(OverlayError,'remains in public hub/llms'):
            validate_merge_build(merged,existing_redirects=existing,built_files=built,hub_texts=[],llms_text=route_for(self.source),hub_html_by_cluster=self.hub_html(merged))
        del built[route_for(self.target).strip('/')+'/index.html']
        with self.assertRaisesRegex(OverlayError,'destination HTML missing'):
            validate_merge_build(merged,existing_redirects=existing,built_files=built,hub_texts=[],llms_text='',hub_html_by_cluster=self.hub_html(merged))

    def test_redirect_chain_cycle_and_overlap_rejected(self):
        merged=self.merged()
        for existing,pattern in [(('/legacy '+route_for(self.source)+' 301\n').encode(),'chain'),(b'/a /b 301\n/b /a 301\n','cycle'),(b'/answers/* /fallback 200\n','overlaps merged source')]:
            with self.assertRaisesRegex(OverlayError,pattern): render_merged_redirects(existing,merged._merge_plan,merged.records)

    def test_only_served_files_removed_no_research_touch(self):
        files=[SimpleNamespace(src_uri=path) for path in self.fx.paths]+[SimpleNamespace(src_uri='research/report.md')]
        result=exclude_merged_files(files,[self.source])
        self.assertNotIn(self.source,[file.src_uri for file in result]); self.assertIn('research/report.md',[file.src_uri for file in result])
        with self.assertRaisesRegex(OverlayError,'Only answer sources'):
            exclude_merged_files(files,['research/report.md'])

    def test_missing_required_fact_or_stale_target_rejected(self):
        self.plan['merges'][self.source]['required_fact_ids'].append('missing-french-launch-fact')
        with self.assertRaisesRegex(OverlayError,'required preserved fact'):
            self.merged()
        self.plan['merges'][self.source]['required_fact_ids'].pop()
        self.plan['merges'][self.source]['target_effective_canonical_sha256']='f'*64
        with self.assertRaisesRegex(OverlayError,'reviewed target'):
            self.merged()

    def test_current_whole_analysis_uses_effective_hubs_and_no_source_article_pass(self):
        merged=self.merged(); existing,built=self.build(merged)
        receipt=validate_merge_build(merged,existing_redirects=existing,built_files=built,hub_texts=[],llms_text='',hub_html_by_cluster=self.hub_html(merged))
        artifacts={route_for(path):('actual fixture '+path).encode() for path in merged.records}
        state=make_compiled_state(merged,built_route_artifacts=artifacts,redirects=merged._merge_plan)
        self.assertIn(self.source,state['raw_source_pins'])
        metadata=self.fx.annotations(merged)
        # Fixture annotation helper assumes original ordinal bank IDs; retain
        # the existing exact bound notes for all remaining original sources.
        original_notes=self.fx.annotations(self.base)
        metadata['figures']=original_notes['figures']; metadata['pages']={path:note for path,note in original_notes['pages'].items() if path!=self.source}
        result=complete_current_analysis(merged,state,current_annotations=metadata,trusted_index_references_sha256=self.fx.reference_hash,merge_build_receipt=receipt)
        self.assertFalse(result['passed']);self.assertTrue(result['merge_artifact_passed']);self.assertFalse(result['merge_build_passed'])
        self.assertTrue(any('actual hosting routing' in str(e) for e in result['global_fatal_errors']))
        self.assertEqual(21,result['pair_count']); self.assertNotIn(self.source,result['page_readiness'])
        self.assertEqual('MERGED_301',result['source_fit_statuses'][self.source]['status'])

    def test_numeric_annotation_receipt_mismatch_is_explicit_page_failure(self):
        artifacts={route_for(path):b'fixture html' for path in self.base.records}
        state=make_compiled_state(self.base,built_route_artifacts=artifacts,redirects={})
        notes=self.fx.annotations(self.base);notes['pages'][self.target]['writing_review_sha256']='f'*64
        report=complete_current_analysis(self.base,state,current_annotations=notes,trusted_index_references_sha256=self.fx.reference_hash)
        self.assertTrue(report['analysis_completed']);self.assertFalse(report['page_readiness'][self.target]['passed'])
        self.assertTrue(any('annotation writing receipt' in str(e) for e in report['page_readiness'][self.target]['errors']))

    def test_later_merge_appends_only_new301_and_preserves_old_source_state(self):
        old=self.merged();first_bytes=render_merged_redirects(b'# pre-existing\n',old._merge_plan,old.records)
        newer=copy.copy(old);newer.records=copy.deepcopy(old.records);second=self.fx.paths[2];newer.records.pop(second)
        newer._merge_plan=dict(old._merge_plan);newer._merge_plan[second]={'target_path':self.target}
        newer._new_merge_plan={second:{'target_path':self.target}}
        newer.merge_statuses=dict(old.merge_statuses);newer.merge_statuses[second]={'status':'MERGED_301','article_pass':False,'target_path':self.target}
        raw=render_merged_redirects(first_bytes,newer._new_merge_plan,newer.records)
        self.assertTrue(raw.startswith(first_bytes))
        self.assertEqual(1,raw.count((route_forms(self.source)[0]+' ').encode()))
        built={'_redirects':raw,route_for(self.target).strip('/')+'/index.html':b'fixture target'}
        self.orders={'measurement':list(newer.records)}
        built['answers/measurement/index.html']=self.hub_html(newer)['measurement'].encode();built['answers/index.html']=self.hub_html(newer)['measurement'].encode()
        result=validate_merge_build(newer,existing_redirects=first_bytes,built_files=built,hub_texts=[],llms_text='',hub_html_by_cluster=self.hub_html(newer))
        self.assertEqual(4,result['planned_301_forms']);self.assertEqual(2,len(result['source_fit_statuses']));self.assertFalse(result['live_http_301_verified'])

    def test_actual_hub_cannot_hide_an_unmodified_leaf(self):
        merged=self.merged();existing,built=self.build(merged)
        html=self.hub_html(merged)
        html['measurement']=html['measurement'].replace('<a href="'+route_for(self.target)+'">Fixture</a>','')
        built['answers/measurement/index.html']=html['measurement'].encode()
        with self.assertRaisesRegex(OverlayError,'hides an effective article'):
            validate_merge_build(merged,existing_redirects=existing,built_files=built,hub_texts=[],llms_text='',hub_html_by_cluster=html)

    def test_computed_group_permit_does_not_open_default_full_gate(self):
        binding={'commit_sha':'a'*40,'deployment_id':'fixture','artifact_sha256':'b'*64,'served_receipt_sha256':'c'*64}
        old_artifacts={route_for(path):('old actual fixture '+record['effective_canonical_source_sha256']).encode() for path,record in self.base.records.items()}
        previous=make_compiled_state(self.base,built_route_artifacts=old_artifacts,redirects={},production_binding=binding)
        old_notes=self.fx.annotations(self.base)
        untouched=self.fx.paths[-1]
        # The positive bounded fixture carries an already-failing untouched row.
        # A new failure after prior PASS is separately rejected above.
        self.base.records[untouched]['review_ids'].pop('writing')
        previous['current_quality_snapshot']=complete_current_analysis(self.base,previous,current_annotations=old_notes,trusted_index_references_sha256=self.fx.reference_hash)
        previous_path=Path(self.temp.name)/'actual-prior.json';previous_path.write_bytes(encoded(previous))
        rel=self.source;raw_body=self.base.finite.source_body((self.fx.docs/rel).read_text())[1]
        old=raw_body.split('## What we measured\n\n')[1].split('\n\n')[0]
        new=old+' Newly reviewed distinct fixture support.';start=raw_body.index(old)
        entry=self.fx.bodies['pages'][rel]
        entry['patches']=[{'old':old,'new':new,'start':start,'old_sha256':sha(old.encode()),'new_sha256':sha(new.encode()),'fact_ledger':[]}]
        entry['post_patches_body_sha256']=sha((raw_body[:start]+new+raw_body[start+len(old):]).encode())
        draft=self.fx.approve_fixture();notes=self.fx.annotations(draft)
        untouched=self.fx.paths[-1]
        del self.fx.bodies['pages'][untouched]['reviews']['writing']
        current=self.fx.compile()
        artifacts={route_for(path):(old_artifacts[route_for(path)] if record['effective_canonical_source_sha256']==self.base.records[path]['effective_canonical_source_sha256'] else ('new actual fixture '+record['effective_canonical_source_sha256']).encode()) for path,record in current.records.items()}
        state=make_compiled_state(current,built_route_artifacts=artifacts,redirects={})
        report=complete_current_analysis(current,state,current_annotations=notes,trusted_index_references_sha256=self.fx.reference_hash)
        before,after=previous['routes'][route_for(rel)],state['routes'][route_for(rel)]
        allowed={rel:{'before_effective_canonical_sha256':before['effective_canonical_sha256'],'after_effective_canonical_sha256':after['effective_canonical_sha256'],'after_body_sha256':after['body_sha256'],'after_metadata_sha256':after['metadata_sha256']}}
        permit=prepare_incremental_permit(current,built_route_artifacts=artifacts,candidate_state=state,previous_manifest_path=previous_path,trusted_previous_sha256=sha(previous_path.read_bytes()),actual_prior_production_binding=binding,authorized_change_map=allowed,full_current_report=report)
        self.assertTrue(permit.result['incremental_release_passed']);self.assertFalse(permit.result['full_current_passed'])
        self.assertIn(untouched,permit.result['untouched_current_failures'])
        self.assertEqual(current.records[rel]['body'],permit.markdown_after_finite94(rel,raw_body))
        with self.assertRaisesRegex(OverlayError,'Publication blocked'):
            current.transform_after_finite94(rel,raw_body)
        with self.assertRaisesRegex(OverlayError,'full current PASS'):
            require_full_completion(permit.result)


if __name__=='__main__': unittest.main()
