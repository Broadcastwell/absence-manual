"""Private proposed MkDocs/CI adapter. Inputs must be independently pinned.

Builds are previews until verify_release succeeds against every actual output.
No source file is written. The ordinary full-publication gate is unchanged.
"""
from __future__ import annotations
import argparse,copy,importlib.util,json,os,re,sys
from pathlib import Path
from types import SimpleNamespace
import zipfile

from library_publication_overlay import (read_bound_json,sha,canonical,FiniteStage,
    source_head,require,HEX)
from library_publication_composition import (ComposedPublicationOverlay,CompositionTrust,
    validated_published_article_count)
from library_publication_release import (MergeTrust,apply_reviewed_merges,route_for,
    render_merged_redirects,validate_merge_build,make_compiled_state,
    complete_current_analysis,prepare_incremental_permit)
from library_publication_consumers import (EffectiveRegistry,generate_effective_hubs,
    generate_effective_llms,generate_effective_sitemaps,validate_page_contexts,
    validate_effective_search,compare_complete_artifacts,public_route,LIBRARY_HUB)
from library_publication_generated_pdf import PDF_PATHS,PDF_ROUTES,validate_reviewed_pdf_changes
from library_publication_field_freeze import FieldFreeze
from library_publication_eligibility import Finite45Eligibility
from library_publication_both_scopes import attach_literal_scope,prepare_both_scope_permit


def json_bytes(value):return (json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode()
def reviewed_file_hash(actual,expected):
    # A blueprint can pin the exact pre-existing Windows and Git LF byte forms.
    # No source or baseline normalization is performed.
    return actual in expected if isinstance(expected,list) else actual==expected
def toc_data(toc):return [{'id':x.id,'url':x.url,'children':toc_data(x.children)} for x in toc]
def toc_restore(items):return [SimpleNamespace(id=x['id'],url=x['url'],children=toc_restore(x['children'])) for x in items]


def safe_navigation_label(label):
    require(isinstance(label,str) and label.strip() and '<' not in label and '\n' not in label,'Unsafe legacy navigation label')
    require(not re.search(r'(?i)\b(?:winner|leader|startup|beta|optimisation|organisation|behaviour|colour|analysing|prioritise)\b',label),'Banned legacy navigation label needs a separately reviewed solution')
    return label


def retain_legacy_navigation(nav,files,overlay,aliases):
    """Fixed historic question aliases prevent a hidden site-wide title delta.

    Retired nodes point to independently reviewed canonical stubs. New leaves
    remain served and discoverable through current hubs/search/sitemap/llms.
    """
    known=set(overlay.leaf_manifest['pages']);retired=getattr(overlay,'merge_statuses',{})
    require(set(aliases)<=known,'Legacy alias map names a nonlibrary/unknown raw leaf')
    dropped=set()
    for page in nav.pages:
        rel=page.file.src_uri
        if rel not in known:continue
        if rel not in aliases:dropped.add(id(page));continue
        label=safe_navigation_label(aliases[rel]);record=overlay.records.get(rel)
        if record is None:
            require(rel in retired,'Missing legacy navigation article lacks a reviewed disposition')
            record=overlay.records[retired[rel]['target_path']]
        if label!=record['meta']['title']:
            require(label in record['meta'].get('also_asked_as',[]) and label in record['body'],'Legacy question label is not a visible retained alias')
        page.title=label
    def prune(items):
        result=[]
        for item in items:
            if id(item) in dropped:continue
            if getattr(item,'children',None) is not None:item.children=prune(item.children)
            result.append(item)
        return result
    if dropped:
        nav.items=prune(nav.items);nav.pages=[p for p in nav.pages if id(p) not in dropped]
        for i,page in enumerate(nav.pages):
            page.previous_page=nav.pages[i-1] if i else None
            page.next_page=nav.pages[i+1] if i+1<len(nav.pages) else None
    present={getattr(f,'src_uri',getattr(f,'src_path',None)):f for f in files}
    for source in retired:
        require(source in present,'Retired raw source missing from build Files')
        files.remove(present[source])
    return nav


from library_publication_sitemap_dates import bind_publication_dates,POLICY as PUBLICATION_LASTMOD_POLICY


class BuildSession:
    @classmethod
    def load(cls,docs_dir,inputs_path,expected_sha256,work_dir):
        self=cls();self.docs=Path(docs_dir).resolve();self.inputs_path=Path(inputs_path).resolve()
        self.inputs=read_bound_json(self.inputs_path,expected_sha256);require(self.inputs.get('schema_version')==1,'Build input schema differs')
        self.work=Path(work_dir).resolve();self.work.mkdir(parents=True,exist_ok=True)
        def file(name):
            row=self.inputs['files'][name];path=(self.inputs_path.parent/row['path']).resolve()
            require(sha(path.read_bytes())==row['sha256'],'Pinned prepared input changed: '+name)
            return path
        self._file=file
        require({'field_freeze_registry','field_freeze_handoff'}<=set(self.inputs['files']),'Accepted45-page freeze requires exact reconciled registry/handoff inputs; activation is held')
        self.freeze=FieldFreeze(file('field_freeze_registry'),self.inputs['files']['field_freeze_registry']['sha256'],file('field_freeze_handoff'),self.inputs['files']['field_freeze_handoff']['sha256'])
        self.freeze.check_sources(self.docs)
        self.freeze.reject_active_sample_changes(read_bound_json(file('active_revisions'),self.inputs['files']['active_revisions']['sha256']).get('pages',{}),read_bound_json(file('merges'),self.inputs['files']['merges']['sha256']).get('merges',{}))
        sys.path.insert(0,str(self.docs.parent))
        from tools import library_quality as q
        require(reviewed_file_hash(sha(Path(q.__file__).read_bytes()),self.inputs['quality_module_sha256']),'Current quality module differs from the reviewed input')
        require(reviewed_file_hash(sha((self.docs.parent/'tools/library_quality_baseline.json').read_bytes()),self.inputs['historical_baseline_sha256']),'Historical baseline changed')
        module_path=self.docs.parent/'tools/library_related_chapter_links.py';map_path=self.docs.parent/'tools/library_related_chapters.json'
        require(sha(module_path.read_bytes())==self.inputs['finite_module_sha256'] and sha(map_path.read_bytes())==self.inputs['finite_map_sha256'],'Original finite94 code/map changed')
        spec=importlib.util.spec_from_file_location('_bw_build_finite',module_path);finite=importlib.util.module_from_spec(spec);spec.loader.exec_module(finite)
        self.stage=FiniteStage(finite,finite.FiniteChapterLinks(self.docs,map_path));self.q=q
        self.prior=read_bound_json(file('prior_state'),self.inputs['files']['prior_state']['sha256'])
        archive=file('prior_artifact');self.archive=zipfile.ZipFile(archive)
        require(sha(archive.read_bytes())==self.prior['production_binding']['artifact_sha256'],'Actual prior artifact differs from its production binding')
        # All real derived outputs must be explicit rows, including unchanged ones.
        for name in ['sitemap.xml','sitemap.xml.gz','search/search_index.json','llms.txt']:
            if name in self.archive.namelist():require('/'+name in self.prior['routes'],'Prior state hides a derived public route: '+name)
        self.prior_artifacts={}
        for route,row in self.prior['routes'].items():
            if row['kind']=='redirect':continue
            name=route.strip('/')+'/index.html' if route.endswith('/') else route.lstrip('/')
            self.prior_artifacts[route]=self.archive.read(name)
        producer=file('production_receipt');store={sha(producer.read_bytes()):producer.read_bytes()}
        for row in self.inputs.get('receipt_files',[]):
            p=(self.inputs_path.parent/row['path']).resolve();raw=p.read_bytes();require(sha(raw)==row['sha256'],'Formal review receipt bytes changed');store[row['sha256']]=raw
        # Canonical approvals remain immutable; an explicit per-checkout raw
        # snapshot handles LF/CRLF packaging without rewriting any source.
        pins=read_bound_json(file('current_pins'),self.inputs['files']['current_pins']['sha256'])
        leaves=read_bound_json(file('current_leaf_manifest'),self.inputs['files']['current_leaf_manifest']['sha256'])
        actual={p.relative_to(self.docs).as_posix() for p in (self.docs/'answers').glob('*/*.md') if p.name!='index.md'}
        require(actual==set(leaves['pages']),'Current raw leaf coverage differs')
        self.s5_scope=Finite45Eligibility(self.freeze,self.docs,actual)
        for rel,note in leaves['pages'].items():
            raw=(self.docs/rel).read_bytes();require(sha(canonical(raw).encode())==note['canonical_source_sha256'],'Canonical source changed before raw packaging snapshot')
            note['raw_source_sha256']=sha(raw)
            if rel in pins['pages']:
                require(pins['pages'][rel]['canonical_source_sha256']==note['canonical_source_sha256'],'Current canonical source history differs')
                pins['pages'][rel]['raw_source_sha256']=sha(raw)
        buildpins=self.work/'checkout-pins.json';buildleaf=self.work/'checkout-leaves.json';buildpins.write_bytes(json_bytes(pins));buildleaf.write_bytes(json_bytes(leaves))
        trust=CompositionTrust(self.inputs['files']['prior_state']['sha256'],self.inputs['files']['prior_payload']['sha256'],sha(buildleaf.read_bytes()),self.inputs['files']['active_revisions']['sha256'],self.inputs['files']['related_requirements']['sha256'],sha(buildpins.read_bytes()),production_receipt_sha256=sha(producer.read_bytes()),frozen_receipt_sha256=self.inputs.get('frozen_receipt_sha256'),published_count=validated_published_article_count(self.inputs.get('published_count'),self.prior))
        overlay=ComposedPublicationOverlay.compose(self.docs,prior_state=file('prior_state'),prior_payload_bundle=file('prior_payload'),current_leaf_manifest=buildleaf,active_revision_plan=file('active_revisions'),related_requirements=file('related_requirements'),current_pins=buildpins,trust=trust,finite_links=self.stage,quality_module=q,actual_prior_artifacts=self.prior_artifacts,actual_prior_binding=self.inputs['actual_prior_production_binding'],receipt_store=store,field_handoff_path=self.docs.parents[2]/'LIVE/FIELD_TEST_TO_LIBRARY.md',frozen_effective_pins=self.inputs.get('frozen_effective_pins'),s5_scope=self.s5_scope)
        raw_metas={};hub_sources={}
        for rel in leaves['pages']:
            raw_metas[rel]=finite.source_body(canonical((self.docs/rel).read_bytes()))[0]
        for path in [self.docs/'answers/index.md']+sorted((self.docs/'answers').glob('*/index.md')):
            full=canonical(path.read_bytes());meta,body=finite.source_body(full);hub_sources[path.relative_to(self.docs).as_posix()]={'meta':meta,'body':body,'canonical_sha256':sha(full.encode())}
        merges=read_bound_json(file('merges'),self.inputs['files']['merges']['sha256'])
        if merges.get('merges'):
            future=set(overlay.records)-set(merges['merges']);orders={}
            for cluster in {r['cluster'] for r in overlay.records.values()}:
                source=self.docs/'answers'/cluster/'index.md';body=hub_sources[source.relative_to(self.docs).as_posix()]['body'];ordered=[]
                for _,href in re.findall(r'\[([^]]+)\]\(([^\s)]+)',body):
                    target=finite.related_local_target(href,source,self.docs)
                    if target is not None and target.is_relative_to(self.docs):
                        rel=target.relative_to(self.docs).as_posix()
                        if rel in future:ordered.append(rel)
                orders[cluster]=ordered
            from library_publication_canonical_stub import apply_reviewed_canonical_stubs
            overlay=apply_reviewed_canonical_stubs(overlay,file('merges'),self.inputs['files']['merges']['sha256'],hub_orders=orders)
        self.overlay=overlay;self.registry=EffectiveRegistry(overlay)
        changes=read_bound_json(file('hub_changes'),self.inputs['files']['hub_changes']['sha256'])
        self.hubs=generate_effective_hubs(self.registry,hub_sources=hub_sources,raw_leaf_metadata=raw_metas,approved_hub_changes=changes.get('pages',{}),merged_sources=overlay.merge_statuses)
        self.publication_dates=None
        if self.inputs.get('sitemap_lastmod_policy') is not None:
            require(self.inputs['sitemap_lastmod_policy']==PUBLICATION_LASTMOD_POLICY,'Unknown sitemap publication-lastmod policy')
            hubs_file=file('prior_hub_payload')
            self.publication_dates=bind_publication_dates(self.registry,prior_xml=self.archive.read('sitemap.xml'),
                prior_payload_bundle=read_bound_json(file('prior_payload'),self.inputs['files']['prior_payload']['sha256']),
                prior_hub_bundle=read_bound_json(hubs_file,self.inputs['files']['prior_hub_payload']['sha256']),
                actual_prior_artifacts=self.prior_artifacts,producer_receipt=overlay._load_receipt(sha(producer.read_bytes())),
                payload_file_sha256=self.inputs['files']['prior_payload']['sha256'],hub_file_sha256=self.inputs['files']['prior_hub_payload']['sha256'])
        self.aliases=read_bound_json(file('navigation_aliases'),self.inputs['files']['navigation_aliases']['sha256'])['pages']
        self.contexts={};self.site=None
        return self

    def markdown(self,markdown,page):
        rel=page.file.src_uri
        if rel in self.overlay.records:
            record=self.overlay.records[rel]
            # Preview emission checks this exact page and the live handoff.
            # Full raw/target/metadata guards run at compile, post-build and
            # final verification; publication is never granted here.
            require(sha((self.docs/rel).read_bytes())==record['source_sha256'],'Current page source changed during preview render')
            require(sha(record['body'].encode())==record['effective_body_sha256']
                and sha(self.q.canonical_json(record['meta']).encode())==record['effective_meta_sha256'],'Pinned preview record changed')
            field=self.overlay._field_handoff
            require((field.read_bytes() if field.exists() else None)==self.overlay._field_stamp,'Field handoff changed during preview render')
            require(sha(markdown.encode())==record['post_finite94_body_sha256'],'Hook stage is not the exact finite94 output')
            page.meta=copy.deepcopy(record['meta'])
            return record['body']
        if rel in self.hubs:
            page.meta=copy.deepcopy(self.hubs[rel]['meta']);return self.hubs[rel]['body']
        require(rel not in self.overlay.merge_statuses,'Retired source reached article rendering')
        return markdown

    def capture_page(self,output,page):
        rel=page.file.src_uri
        if rel in self.overlay.records or rel in self.hubs:
            self.contexts[rel]={'markdown':page.markdown,'meta':copy.deepcopy(page.meta),'html':page.content,'toc':toc_data(page.toc),'pre_postbuild_rendered_html':output,'rendered_html':output}
        return output

    def capture_final_html(self):
        # This late post-build hook runs after the existing performance-assets
        # processor. Retain the earlier template output for inspection, then
        # bind actual final bytes. Full article/head/source checks below still
        # reject a postprocessor that drops or changes an effective fact.
        require(set(self.contexts)==set(self.registry.records)|set(self.registry.hubs),'Actual render context coverage differs before final capture')
        for path,context in self.contexts.items():
            output=self.site/(public_route(path).strip('/')+'/index.html')
            require(output.is_file(),'Actual final HTML is missing: '+path)
            context['rendered_html']=output.read_bytes().decode('utf-8')

    def prepare_outputs(self,site_dir):
        self.site=Path(site_dir).resolve();require(self.site!=self.docs and not self.docs.is_relative_to(self.site),'Invalid build output location')
        require(not (self.site/'llms-full.txt').exists(),'An llms-full output needs an explicit effective consumer before adoption')
        spec=importlib.util.spec_from_file_location('_bw_llms_source_generator',self.docs.parent/'tools/generate_answers_llms.py');source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
        hubmeta={p:r['meta'] for p,r in self.hubs.items()}
        llms=generate_effective_llms(self.registry,original=self.archive.read('llms.txt'),hub_metadata=hubmeta,source_generator=source);(self.site/'llms.txt').write_bytes(llms)
        xml,gz=generate_effective_sitemaps(self.registry,prior_xml=self.archive.read('sitemap.xml'),hub_metadata=hubmeta,merged_sources=self.overlay.merge_statuses,field_freeze=self.freeze,publication_dates=getattr(self,'publication_dates',None))
        (self.site/'sitemap.xml').write_bytes(xml);(self.site/'sitemap.xml.gz').write_bytes(gz)
        old=self.archive.read('_redirects') if '_redirects' in self.archive.namelist() else b''
        if getattr(self.overlay,'_canonical_stub_policy',None):
            from library_publication_canonical_stub import render_canonical_stub,stub_artifact_path,validate_existing_routing
            validate_existing_routing(old,self.overlay.merge_statuses)
            for source,row in self.overlay.merge_statuses.items():
                target=self.site/stub_artifact_path(source);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(render_canonical_stub(source,row))
            if old:(self.site/'_redirects').write_bytes(old)
            self.expected_redirects=old if old else None
        else:
            new=render_merged_redirects(old,self.overlay._new_merge_plan,self.overlay.records)
            if new or old:(self.site/'_redirects').write_bytes(new)
            self.expected_redirects=new if new or old else None
        self.capture_final_html()
        (self.work/'actual-render-contexts.json').write_bytes(json_bytes({'registry_sha256':self.registry.fingerprint,'contexts':self.contexts,'bridge_sha256':sha(Path(__file__).read_bytes())}))

    def verify_release(self,site_dir):
        self.site=Path(site_dir).resolve();self.overlay._check_unchanged()
        cache=json.loads((self.work/'actual-render-contexts.json').read_text(encoding='utf-8'))
        require(cache['registry_sha256']==self.registry.fingerprint and cache['bridge_sha256']==sha(Path(__file__).read_bytes()),'Actual render context cache is stale')
        contexts={p:{**c,'toc':toc_restore(c['toc']),'rendered_html':c['rendered_html'].encode()} for p,c in cache['contexts'].items()}
        for path,context in contexts.items():
            require((self.site/(public_route(path).strip('/')+'/index.html')).read_bytes()==context['rendered_html'],'Final built HTML differs after its actual render capture')
        validate_page_contexts(self.registry,contexts=contexts)
        spec=importlib.util.spec_from_file_location('_bw_verified_llms_generator',self.docs.parent/'tools/generate_answers_llms.py');source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
        hubmeta={p:r['meta'] for p,r in self.hubs.items()}
        expected_llms=generate_effective_llms(self.registry,original=self.archive.read('llms.txt'),hub_metadata=hubmeta,source_generator=source)
        require((self.site/'llms.txt').read_bytes()==expected_llms,'Final llms bytes differ from the actual effective consumer')
        expected_xml,expected_gz=generate_effective_sitemaps(self.registry,prior_xml=self.archive.read('sitemap.xml'),hub_metadata=hubmeta,merged_sources=self.overlay.merge_statuses,field_freeze=self.freeze,publication_dates=getattr(self,'publication_dates',None))
        require((self.site/'sitemap.xml').read_bytes()==expected_xml and (self.site/'sitemap.xml.gz').read_bytes()==expected_gz,'Final sitemap/gzip differ from the actual effective consumer')
        validate_effective_search(self.registry,prior_bytes=self.archive.read('search/search_index.json'),candidate_bytes=(self.site/'search/search_index.json').read_bytes(),actual_page_contexts=contexts,merged_sources=self.overlay.merge_statuses)
        # Register only after actual generators/output validators have consumed it.
        for name in ['page-head-and-structured-data','library-hubs','llms']:
            require(name in self.registry.receipts,'Actual effective consumer proof missing')
            self.overlay.register_metadata_consumer(name,self.overlay.public_metadata_fingerprint())
        prior_files={p:self.archive.read(p) for p in self.archive.namelist() if p not in {'relaunch-build-provenance.json','library-release-proof.json','library-effective-payload.json','library-compiled-state.json'}}
        built={p.relative_to(self.site).as_posix():p.read_bytes() for p in self.site.rglob('*') if p.is_file()}
        self.freeze.check_sources(self.docs);self.freeze.check_files(built)
        self.s5_scope.certify_artifacts(built)
        pdf_plan=read_bound_json(self._file('reviewed_generated_pdf_changes'),self.inputs['files']['reviewed_generated_pdf_changes']['sha256']) if 'reviewed_generated_pdf_changes' in self.inputs['files'] else None
        reviewed_pdfs=validate_reviewed_pdf_changes(plan=pdf_plan,prior_files=prior_files,candidate_files=built,repo=self.docs.parent,prior_artifact_sha256=self.inputs['actual_prior_production_binding']['artifact_sha256'],prior_production_binding=self.inputs['actual_prior_production_binding'],receipt_loader=self.overlay._load_receipt)
        registered_pdf_routes=PDF_ROUTES&set(self.prior['routes'])
        require(not registered_pdf_routes or registered_pdf_routes==PDF_ROUTES,'Prior compiled state has incomplete PDF route coverage')
        if reviewed_pdfs is not None:require(registered_pdf_routes==PDF_ROUTES,'Prior production manifest must register both actual existing PDF routes before a reviewed PDF change')
        routes={public_route(p):built[public_route(p).strip('/')+'/index.html'] for p in contexts}
        for p in ['llms.txt','sitemap.xml','sitemap.xml.gz','search/search_index.json']:routes['/'+p]=built[p]
        for route in registered_pdf_routes:routes[route]=built[route.lstrip('/')]
        if getattr(self.overlay,'_canonical_stub_policy',None):
            from library_publication_canonical_stub import stub_artifact_path
            for source in self.overlay.merge_statuses:routes[route_for(source)]=built[stub_artifact_path(source)]
        state=make_compiled_state(self.overlay,built_route_artifacts=routes,redirects=self.overlay._merge_plan)
        actual_changed=[r for r in set(self.prior['routes'])|set(state['routes']) if self.prior['routes'].get(r)!=state['routes'].get(r)]
        changed_aux=[r for r in actual_changed if state['routes'].get(r,{}).get('kind')=='auxiliary']
        notes=read_bound_json(self._file('current_annotations'),self.inputs['files']['current_annotations']['sha256'])
        require(set(notes['pages']) in [set(self.overlay.leaf_manifest['pages']),set(self.overlay.records)],'Current annotation coverage differs')
        notes['pages']={p:n for p,n in notes['pages'].items() if p in self.overlay.records}
        for path,record in self.overlay.records.items():
            note=notes['pages'][path];opening=self.q.paragraph_after_heading(record['body']).strip()
            require(note['opening_sha256']==sha(opening.encode()),'Effective opening needs independently reviewed annotations')
            require(note['canonical_source_sha256'] in {record['raw_canonical_source_sha256'],record['effective_canonical_source_sha256']},'Current annotation source binding differs')
            note.update(source_sha256=record['source_sha256'],canonical_source_sha256=record['effective_canonical_source_sha256'])
        merge_receipt=None
        if self.overlay._merge_plan:
            validator=validate_merge_build
            if getattr(self.overlay,'_canonical_stub_policy',None):
                from library_publication_canonical_stub import validate_stub_build
                validator=validate_stub_build
            merge_receipt=validator(self.overlay,existing_redirects=self.archive.read('_redirects') if '_redirects' in self.archive.namelist() else b'',built_files=built,llms_text=built['llms.txt'].decode())
        report=complete_current_analysis(self.overlay,state,current_annotations=notes,trusted_index_references_sha256=sha(self.q.canonical_json(notes['index_question_titles']).encode()),validated_auxiliary_routes=changed_aux,merge_build_receipt=merge_receipt,reviewed_generated_pdf_changes=reviewed_pdfs)
        report=attach_literal_scope(self.overlay,state,current_annotations=notes,runtime_report=report)
        self.overlay._check_unchanged()
        allowed=read_bound_json(self._file('authorized_changes'),self.inputs['files']['authorized_changes']['sha256'])['pages']
        changed_articles={state['routes'][r]['path'] for r in actual_changed if state['routes'].get(r,{}).get('kind')=='article'}
        changed_hubs={p for p in self.hubs if public_route(p) in changed_aux}
        stub_bytes=None
        if getattr(self.overlay,'_canonical_stub_policy',None):
            from library_publication_canonical_stub import render_canonical_stub,stub_artifact_path
            stub_bytes={stub_artifact_path(p):render_canonical_stub(p,row) for p,row in self.overlay.merge_statuses.items()}
        comparison=compare_complete_artifacts(prior_files=prior_files,candidate_files=built,changed_article_paths=changed_articles,changed_hub_paths=changed_hubs,validated_derived_routes=[r for r in changed_aux if r in {'/llms.txt','/sitemap.xml','/sitemap.xml.gz','/search/search_index.json'}],merged_sources=self.overlay.merge_statuses,expected_redirect_bytes=self.expected_redirects,private_sidecars={'relaunch-build-provenance.json'},reviewed_generated_pdf_changes=reviewed_pdfs,expected_canonical_stub_bytes=stub_bytes)
        (self.work/'whole-current-report.json').write_bytes(json_bytes(report));(self.work/'complete-artifact-comparison.json').write_bytes(json_bytes(comparison))
        if reviewed_pdfs is not None:(self.work/'generated-pdf-review-result.json').write_bytes(json_bytes({'exact_reviewed_paths':sorted(reviewed_pdfs.rows),'root_receipt_sha256':reviewed_pdfs.root_receipt_sha256,'successful_rerun_actual_ci':reviewed_pdfs.actual_ci,'actual_pdf_hashes':{p:sha(built[p]) for p in PDF_PATHS}}))
        permit=prepare_both_scope_permit(self.overlay,built_route_artifacts=routes,candidate_state=state,previous_manifest_path=self._file('prior_state'),trusted_previous_sha256=self.inputs['files']['prior_state']['sha256'],actual_prior_production_binding=self.inputs['actual_prior_production_binding'],authorized_change_map=allowed,full_current_report=report,reviewed_generated_pdf_changes=reviewed_pdfs)
        (self.work/'bounded-release-result.json').write_bytes(json_bytes(permit.result));(self.work/'compiled-state.json').write_bytes(json_bytes(state))
        return permit.result


def from_environment(config):
    inputs=os.environ.get('BW_LIBRARY_PUBLICATION_INPUTS');digest=os.environ.get('BW_LIBRARY_PUBLICATION_INPUTS_SHA256')
    require(inputs and digest and HEX.fullmatch(digest),'Independently pinned prepared library inputs are required; no implicit raw fallback')
    work=Path(config['site_dir']).resolve().parent/'.library-publication-work'
    return BuildSession.load(config['docs_dir'],inputs,digest,work)


def main():
    p=argparse.ArgumentParser();p.add_argument('--inputs',required=True);p.add_argument('--inputs-sha256',required=True);p.add_argument('--docs',required=True);p.add_argument('--site',required=True);p.add_argument('--work',required=True);a=p.parse_args()
    session=BuildSession.load(a.docs,a.inputs,a.inputs_sha256,a.work)
    # This verifier never creates a render receipt or changes build output.
    require((Path(a.work)/'actual-render-contexts.json').exists(),'No actual MkDocs render contexts; build through the proposed hooks first')
    old=session.archive.read('_redirects') if '_redirects' in session.archive.namelist() else b''
    session.expected_redirects=(old or None) if getattr(session.overlay,'_canonical_stub_policy',None) else (render_merged_redirects(old,session.overlay._new_merge_plan,session.overlay.records) or None)
    print(json.dumps(session.verify_release(a.site),indent=2))


if __name__=='__main__':main()
