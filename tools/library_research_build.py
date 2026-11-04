"""Explicit finite Research mode; never a fallback after an ordinary failure."""
from pathlib import Path
import copy,importlib.util,json,os,re,zipfile
from library_research_support import require,sha,qsha,optional_support,check_optional_sources,URLS,dataset_path,_file
from library_research_release import bind_release,validate_quality_identity,POLICY,_PROOF_TOKEN
from library_research_consumers import generate_research_sitemaps,validate_research_sitemaps
from library_research_render import validate_research_contexts
from library_publication_build import BuildSession,toc_data,toc_restore,json_bytes
from library_publication_overlay import read_bound_json


def bound(root,row):
    require(isinstance(row,dict) and set(row)=={'path','sha256'},'Research input ref schema differs')
    raw=_file(root,row['path']).read_bytes();require(sha(raw)==row['sha256'],'Research staged input changed')
    return _file(root,row['path']),raw


class ResearchBuildSession:
    @classmethod
    def load(cls,docs_dir,input_path,expected_sha256,work_dir):
        self=cls();self.docs=Path(docs_dir).resolve();self.root=self.docs.parent
        self.work=Path(work_dir).resolve();self.work.mkdir(parents=True,exist_ok=True)
        self.support=optional_support(self.root);require(self.support is not None,'Research mode lacks exact reviewed module/policy')
        ref=self.support.plan.get('release_inputs',{})
        require(Path(input_path).resolve()==_file(self.root,ref.get('path','')).resolve()
            and expected_sha256==ref.get('sha256'),'Research mode is not committed Library-approved input binding')
        path,raw=bound(self.root,ref);self.inputs=json.loads(raw);d=self.inputs
        require(d.get('policy')==POLICY and d.get('approved') is True,'Research source plan is not Root approved')
        files=d['portable_files']
        def file(name):return bound(path.parent,files[name])[0]
        self._file=file
        require(d.get('candidate_archive_path')=='.library-research-work/candidate.gitLF.zip',
            'Actual candidate GitLF archive must use exact ignored Library work path')
        base_path=file('base_inputs');base_json=json.loads(base_path.read_bytes())
        for name in ['active_revisions','merges']:
            row=base_json['files'][name];value=read_bound_json(base_path.parent/row['path'],row['sha256'])
            require(value.get('pages' if name=='active_revisions' else 'merges')=={},
                'Research mode cannot revise or newly retire a Library page')
        self.base=BuildSession.load(self.docs,base_path,files['base_inputs']['sha256'],self.work/'library')
        b=self.base;self.overlay=b.overlay;self.registry=b.registry;self.archive=b.archive
        require(len(b.overlay.records)==307 and len(b.overlay.merge_statuses)==19
            and not b.overlay.active_revision_paths and not b.overlay._new_merge_plan,
            'Research mode requires actual307/19 inherited/empty new changes')
        prior_files={n:self.archive.read(n) for n in self.archive.namelist() if not n.endswith('/')}
        self.prior_public=prior_files
        payload=read_bound_json(b._file('prior_payload'),b.inputs['files']['prior_payload']['sha256'])
        producer_raw=b._file('production_receipt').read_bytes()
        self.permit=bind_release(self.root,raw,expected_sha256,support=self.support,
            actual_prior_binding=b.inputs['actual_prior_production_binding'],
            prior_source_archive_raw=file('prior_source_archive').read_bytes(),
            candidate_source_archive_raw=_file(self.root,d['candidate_archive_path']).read_bytes(),
            prior_public_files=prior_files,current_payload=payload,prior_state=b.prior,producer_raw=producer_raw)
        self.library_contexts=b.contexts;self.research_contexts={};self.site=None
        require(check_optional_sources(self.root)==[],'Research source/headline/qualification checker failed')
        return self

    def retain_owner_navigation(self,nav,files):
        from library_publication_build import retain_legacy_navigation
        from library_inherited_presentation import retain_appendix_from_actual_prior
        nav=retain_legacy_navigation(nav,files,self.overlay,self.base.aliases)
        nav,self.appendix_nav_proof=retain_appendix_from_actual_prior(nav,files,self.base)
        return nav

    def markdown(self,markdown,page):
        path=page.file.src_uri
        if path in self.permit.research_records:
            r=self.permit.research_records[path]
            require(markdown==r['body'] and page.meta==r['meta'],'Research renderer did not consume exact current source')
            return markdown
        return self.base.markdown(markdown,page)

    def capture_page(self,output,page):
        self.base.capture_page(output,page);path=page.file.src_uri
        if path in self.permit.research_records:
            self.research_contexts[path]={'markdown':page.markdown,'meta':copy.deepcopy(page.meta),
                'html':page.content,'toc':toc_data(page.toc),'pre_postbuild_rendered_html':output,'rendered_html':output}
        return output

    def prepare_outputs(self,site_dir):
        self.site=Path(site_dir).resolve();self.base.prepare_outputs(site_dir)
        for path,c in self.research_contexts.items():
            c['rendered_html']=(self.site/(path.removesuffix('index.md')+'index.html')).read_text(encoding='utf-8')
        require(set(self.research_contexts)==set(self.permit.research_records),'All53 actual Research pages were not captured')
        files={u:(self.site/dataset_path(u)).read_bytes() for u in URLS}
        xml,gz=generate_research_sitemaps((self.site/'sitemap.xml').read_bytes(),(self.site/'sitemap.xml.gz').read_bytes(),
            permit=self.permit,static_dataset_files=files)
        (self.site/'sitemap.xml').write_bytes(xml);(self.site/'sitemap.xml.gz').write_bytes(gz)
        (self.work/'research-render-contexts.json').write_bytes(json_bytes({'session_module_sha256':sha(Path(__file__).read_bytes()),
            'source_plan_sha256':qsha(self.inputs),'contexts':self.research_contexts}))
        self.capture_candidate_observations('AFTER_MKDOCS_BEFORE_FRESH_MANUAL')

    def capture_candidate_observations(self,phase):
        from library_research_release import PRIVATE_SIDECARS
        require(phase in {'AFTER_MKDOCS_BEFORE_FRESH_MANUAL','AFTER_FRESH_MANUAL_BEFORE_FINAL_PERMIT'},
            'Unknown Research observation phase')
        before={p:r for p,r in self.prior_public.items() if p not in PRIVATE_SIDECARS}
        after={p.relative_to(self.site).as_posix():p.read_bytes() for p in self.site.rglob('*')
            if p.is_file() and p.relative_to(self.site).as_posix() not in PRIVATE_SIDECARS}
        delta={p:{'before_sha256':sha(before[p]) if p in before else None,
            'after_sha256':sha(after[p]) if p in after else None} for p in sorted(set(before)|set(after)) if before.get(p)!=after.get(p)}
        (self.work/('candidate-public-observation.'+phase+'.NOT_APPROVED.json')).write_bytes(json_bytes({
            'approved':False,'phase':phase,'source_plan_sha256':qsha(self.inputs),
            'actual_candidate_public_sha256':{p:sha(raw) for p,raw in sorted(after.items())},'actual_delta':delta}))

    def verify_release(self,site_dir):
        from library_published_discovery_consumer_five import checked_published_binding
        published5=checked_published_binding(self.base)
        from library_publication_consumers import validate_page_contexts,generate_effective_llms,generate_effective_sitemaps,validate_effective_search,public_route
        from library_publication_canonical_stub import validate_stub_build,render_canonical_stub,stub_artifact_path
        from library_publication_release import make_compiled_state,complete_current_analysis
        from library_publication_both_scopes import attach_literal_scope
        self.site=Path(site_dir).resolve();b=self.base;b.site=self.site;b.overlay._check_unchanged();self.permit.check_sources()
        cache=json.loads((b.work/'actual-render-contexts.json').read_bytes())
        require(cache['registry_sha256']==b.registry.fingerprint
            and cache['bridge_sha256']==sha(Path(__import__('library_publication_build').__file__).read_bytes()),'Library render cache is stale')
        library={p:{**c,'toc':toc_restore(c['toc']),'rendered_html':c['rendered_html'].encode()} for p,c in cache['contexts'].items()}
        research_cache=json.loads((self.work/'research-render-contexts.json').read_bytes())
        require(research_cache['session_module_sha256']==sha(Path(__file__).read_bytes())
            and research_cache['source_plan_sha256']==qsha(self.inputs),'Research render cache is stale')
        research={p:{**c,'toc':toc_restore(c['toc']),'rendered_html':c['rendered_html'].encode()} for p,c in research_cache['contexts'].items()}
        for path,c in {**library,**research}.items():
            route=public_route(path) if path in library else '/'+path.removesuffix('index.md')
            require((self.site/(route.strip('/')+'/index.html')).read_bytes()==c['rendered_html'],'Final HTML changed after capture')
        validate_page_contexts(b.registry,contexts=library);validate_research_contexts(self.permit,research)
        spec=importlib.util.spec_from_file_location('_Research_identity_llms',self.root/'tools/generate_answers_llms.py')
        source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
        hubmeta={p:r['meta'] for p,r in b.hubs.items()}
        expected_llms=generate_effective_llms(b.registry,original=self.archive.read('llms.txt'),hub_metadata=hubmeta,source_generator=source)
        if published5 is not None:expected_llms,_=published5.llms(expected_llms)
        require((self.site/'llms.txt').read_bytes()==expected_llms==self.prior_public['llms.txt'],'Research changed llms or Library discovery')
        base_xml,base_gz=generate_effective_sitemaps(b.registry,prior_xml=self.archive.read('sitemap.xml'),hub_metadata=hubmeta,
            merged_sources=b.overlay.merge_statuses,field_freeze=b.freeze,publication_dates=b.publication_dates,research_support=self.support)
        xml=(self.site/'sitemap.xml').read_bytes();gz=(self.site/'sitemap.xml.gz').read_bytes()
        validate_research_sitemaps(base_xml,xml,gz,permit=self.permit)
        validate_effective_search(b.registry,prior_bytes=self.archive.read('search/search_index.json'),
            candidate_bytes=(self.site/'search/search_index.json').read_bytes(),actual_page_contexts=library,
            merged_sources=b.overlay.merge_statuses,research_permit=self.permit,research_contexts=research)
        if published5 is not None:published5.search(self.archive.read('search/search_index.json'),(self.site/'search/search_index.json').read_bytes())
        for name in ['page-head-and-structured-data','library-hubs','llms']:
            require(name in b.registry.receipts,'Actual Library consumer proof missing')
            b.overlay.register_metadata_consumer(name,b.overlay.public_metadata_fingerprint())
        self.permit._record_proof('library_consumers',{'307_leaf_and12_hub_actual_contexts':True,'llms_byte_exact':True},_PROOF_TOKEN)
        built={p.relative_to(self.site).as_posix():p.read_bytes() for p in self.site.rglob('*') if p.is_file()}
        b.freeze.check_sources(self.docs);b.freeze.check_files(built);b.freeze.check_sitemap(xml);b.s5_scope.certify_artifacts(built)
        self.permit._record_proof('freeze',{'exact45_source_HTML_XML_and5_assets':True},_PROOF_TOKEN)
        stub=validate_stub_build(b.overlay,existing_redirects=self.archive.read('_redirects') if '_redirects' in self.archive.namelist() else b'',built_files=built,llms_text=built['llms.txt'].decode())
        from library_publication_verify_stubs import validate_stub_artifacts
        closure=validate_stub_artifacts(b.overlay,self.site)
        require(set(closure)==set(b.prior['merged_sources']) and len(closure)==19,
            'Research mode lost original19 exact approved decision/target closure')
        exact_stubs={stub_artifact_path(p):render_canonical_stub(p,row) for p,row in b.overlay.merge_statuses.items()}
        self.permit._record_proof('stubs',{'exact19_current_decision_renderer_bound':True},_PROOF_TOKEN)
        routes={public_route(p):built[public_route(p).strip('/')+'/index.html'] for p in library}
        for p in ['llms.txt','sitemap.xml','sitemap.xml.gz','search/search_index.json','absence-manual.pdf','absence-manual-v1.0-2026-08-18.pdf']:routes['/'+p]=built[p]
        for p,raw in exact_stubs.items():routes['/'+p.removesuffix('index.html')]=raw
        state=make_compiled_state(b.overlay,built_route_artifacts=routes,redirects=b.overlay._merge_plan)
        notes=read_bound_json(b._file('current_annotations'),b.inputs['files']['current_annotations']['sha256'])
        notes['pages']={p:n for p,n in notes['pages'].items() if p in b.overlay.records}
        for p,r in b.overlay.records.items():
            n=notes['pages'][p];require(n['opening_sha256']==sha(b.q.paragraph_after_heading(r['body']).strip().encode()),'Research changed Library opening')
            n.update(source_sha256=r['source_sha256'],canonical_source_sha256=r['effective_canonical_source_sha256'])
        report=complete_current_analysis(b.overlay,state,current_annotations=notes,
            trusted_index_references_sha256=sha(b.q.canonical_json(notes['index_question_titles']).encode()),
            validated_auxiliary_routes=['/sitemap.xml','/sitemap.xml.gz','/search/search_index.json'],merge_build_receipt=stub)
        report=attach_literal_scope(b.overlay,state,current_annotations=notes,runtime_report=report)
        self.permit._record_proof('quality',validate_quality_identity(b.prior['current_quality_snapshot'],report),_PROOF_TOKEN)
        for p in ['absence-manual.pdf','absence-manual-v1.0-2026-08-18.pdf']:
            require(built[p]==self.prior_public[p],'Research changed Manual PDF bytes')
        sample_paths={p for p in self.prior_public if p.endswith('.pdf') and p.startswith('assets/')}
        require(all(built.get(p)==self.prior_public[p] for p in sample_paths),'Research changed existing sample/data PDF')
        self.permit._record_proof('PDF',{'actual_Manual_and_existing_sample_PDFs_exact':True,
            'new_notice_PDF_review_separately_required':True},_PROOF_TOKEN)
        frozen={r['served_html_path']:r['served_html_sha256'] for r in b.freeze.data['rows']}
        frozen.update({r['path']:r['sha256'] for r in b.freeze.data['presentation_asset_pins']})
        library_artifacts={public_route(p).strip('/')+'/index.html' for p in library}
        (self.work/'whole-current-report.json').write_bytes(json_bytes(report))
        (self.work/'Research-proof-closure.NOT_APPROVED.json').write_bytes(json_bytes(self.permit.proofs))
        self.capture_candidate_observations('AFTER_FRESH_MANUAL_BEFORE_FINAL_PERMIT')
        result=self.permit.verify_public_delta(self.prior_public,built,frozen_pins=frozen,
            exact_stub_bytes=exact_stubs,library_artifact_paths=library_artifacts,
            protected_scientific_pins=__import__('library_research_release').paths()['immutable_science_and_registered_downloads'])
        (self.work/'Research-complete-artifact-comparison.json').write_bytes(json_bytes(result))
        (self.work/'Research-proof-closure.NOT_APPROVED.json').write_bytes(json_bytes(self.permit.proofs))
        return self.permit.finish()


def from_environment(config):
    allowed={'BW_RESEARCH_RELEASE_INPUTS','BW_RESEARCH_RELEASE_INPUTS_SHA256'}
    require({k for k in os.environ if k.startswith('BW_RESEARCH_RELEASE_')}==allowed,
        'Research mode needs exact complete known environment keys')
    require(not any(k.startswith(('BW_OWNER_REPAIR_','BW_LIBRARY_PUBLICATION_')) for k in os.environ),
        'Research mode cannot mix with Owner or ordinary S5')
    path=os.environ['BW_RESEARCH_RELEASE_INPUTS'];pin=os.environ['BW_RESEARCH_RELEASE_INPUTS_SHA256']
    require(path and re.fullmatch('[0-9a-f]{64}',pin),'Exact Research input hash required')
    return ResearchBuildSession.load(config['docs_dir'],path,pin,Path(config['site_dir']).resolve().parent/'.library-research-work/render')


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--inputs',required=True);p.add_argument('--inputs-sha256',required=True)
    p.add_argument('--docs',required=True);p.add_argument('--site',required=True);p.add_argument('--work',required=True);a=p.parse_args()
    session=ResearchBuildSession.load(a.docs,a.inputs,a.inputs_sha256,a.work)
    try:print(json.dumps(session.verify_release(a.site),indent=2))
    finally:session.archive.close()
