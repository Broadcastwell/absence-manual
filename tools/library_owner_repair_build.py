"""One-release owner repair adapter; the ordinary BuildSession stays strict.

This is an explicit alternate policy dispatch, never a fallback after a failed
ordinary S5 release. All source/render/current-quality checks still execute.
Root must supply actually reviewed inputs. No supplied path grants approval.
"""
from __future__ import annotations
import copy,importlib.util,json,os,re,zipfile
from pathlib import Path
from library_owner_repair import (POLICY,OLD_CSS,OLD_CSS_SHA256,PDF_PATHS,SITE,
    require,sha,digest,json_unique,safe_path,OwnerRepairPlan,exact_edits,
    restore_frozen_stylesheet,validate_navigation_only,validate_quality_transition,
    validate_artifact_delta,css_comment_only,validate_before_read_receipt)
from library_owner_repair_consumers import (compose_effective_payload,repair_ledger,
    validate_peer,validate_static_peer,json_hash,apply_llms_lines,apply_nonlibrary_sitemap_dates,
    validate_actual_search,validate_render_context,validate_content_surface,validate_fact_bindings,public_url)
from library_publication_build import BuildSession,toc_data,toc_restore,json_bytes
from library_publication_consumers import (validate_page_contexts,
    generate_effective_llms,generate_effective_sitemaps)
from library_publication_release import make_compiled_state,complete_current_analysis
from library_publication_both_scopes import attach_literal_scope,validate_scope_union


def public_route(path):return '/'+public_url(path)


def bound_file(root,row):
    require(isinstance(row,dict) and set(row)=={'path','sha256'},'Bound file reference differs')
    safe_path(row['path']);cursor=root
    require(not cursor.is_symlink(),'Bound input namespace is a symlink')
    for part in Path(row['path']).parts:
        cursor=cursor/part;require(not cursor.is_symlink(),'Bound input has a symlink component')
    p=cursor.resolve()
    require(p.is_relative_to(root.resolve()) and p.is_file(),'Bound input escapes its namespace')
    raw=p.read_bytes();require(sha(raw)==row['sha256'],'Bound repair input changed: '+row['path'])
    return p,raw


def frozen_bundle_before_guard(session,site_dir):
    """Run at -190: only exact old asset + stylesheet tags; guard at -200 next."""
    site=Path(site_dir).resolve();old=session.archive.read(OLD_CSS)
    require(sha(old)==OLD_CSS_SHA256,'Actual old frozen bundle changed')
    bundles=[p for p in site.glob('assets/stylesheets/combined-*.css') if p.relative_to(site).as_posix()!=OLD_CSS]
    require(len(bundles)==1,'Expected one actual new combined stylesheet')
    new_path=bundles[0].relative_to(site).as_posix();new_bytes=bundles[0].read_bytes()
    target=site/OLD_CSS
    if target.exists():require(target.read_bytes()==old,'Existing frozen bundle differs')
    else:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(old)
    for row in session.owner_plan.freeze_data['pages'].values():
        path=row['served_html_path'];p=site/path
        require(p.is_file(),'Frozen candidate HTML missing')
        current=p.read_bytes();restored=restore_frozen_stylesheet(page=path,
          before=session.archive.read(path),candidate=current,new_bundle_path=new_path,
          new_bundle_bytes=new_bytes,baseline_files={OLD_CSS:old})
        if current!=restored:p.write_bytes(restored)
    # This function does not certify HTML. The unchanged accepted45 guard must
    # still reject any body, metadata, nav, layout or other asset difference.


class OwnerRepairBuildSession(BuildSession):
    @classmethod
    def load(cls,docs_dir,inputs_path,expected_sha256,work_dir):
        path=Path(inputs_path).resolve();raw=path.read_bytes()
        require(sha(raw)==expected_sha256,'Repair dispatch bytes changed')
        config=json_unique(raw)
        require(config.get('schema_version')==1 and config.get('policy')==POLICY,'Unknown repair dispatch')
        root=path.parent;load=lambda row:bound_file(root,row)
        base_path,base_raw=load(config['base_inputs'])
        from library_owner_composition import bind_owner_composition
        owner_composition_permit=bind_owner_composition(docs_dir,path,expected_sha256)
        self=super().load(docs_dir,base_path,sha(base_raw),work_dir,
            owner_composition_permit=owner_composition_permit)
        self.repair_config=config;self.repair_input_sha256=expected_sha256;self.repair_root=root
        self.repair_sources={};self.repair_before_sources={};self.repair_contexts={};self.repair_receipts={}
        self._repair_load=load
        from library_owner_repair_post_s5 import bind_session_context
        self.post_s5_binding=bind_session_context(self,config,load)
        prior_payload=json.loads(self._file('prior_payload').read_bytes())['pages']
        require(set(prior_payload)==set(self.overlay.records),'Owner prior payload coverage differs')
        registry=load(config['freeze_registry'])[1];handoff=load(config['freeze_handoff'])[1];navmap=load(config['freeze_nav_map'])[1]
        authority=load(config['authority_read_receipt'])[1];plan_raw=load(config['owner_source_plan'])[1]
        answers=set(self.overlay.records)
        research={p.relative_to(self.docs).as_posix() for p in (self.docs/'research').rglob('*.md')}
        current_pins=json.loads(self._file('current_pins').read_bytes())['pages']
        bank_ids={p:current_pins[p]['bank_id'] for p in self.overlay.records}
        self.owner_plan=OwnerRepairPlan.bind(plan_raw,sha(plan_raw),authority_read_receipt=authority,
          registry_bytes=registry,handoff_bytes=handoff,nav_map_bytes=navmap,
          actual_prior_binding=self.inputs['actual_prior_production_binding'],
          actual_answer_paths=answers,actual_research_paths=research,bank_ids=bank_ids,post_s5_binding=self.post_s5_binding)
        require(config.get('owner_source_plan_sha256')==sha(plan_raw),'Dispatch/source plan pin differs')
        require(self.owner_plan.data.get('base_inputs_sha256')==sha(base_raw),'Owner plan/base composition binding differs')
        require(config.get('llms_line_edits',[])==self.owner_plan.data.get('llms_literal_decisions',[]),'llms input differs from the exact Root-reviewed owner literal decisions')
        before_read=load(config['root_current_before_read_receipt'])[1]
        require(self.owner_plan.data.get('root_current_before_read_receipt_sha256')==sha(before_read),'Before-read/source-plan binding differs')
        self.before_read_proof=validate_before_read_receipt(before_read,sha(before_read),plan=self.owner_plan,actual_prior_files={p:self.archive.read(p) for p in self.archive.namelist() if not p.endswith('/')})
        for rel,pin in self.owner_plan.data.get('approved_code_changes',{}).items():
            safe_path(rel);file=(self.docs.parent/rel).resolve()
            require(file.is_relative_to(self.docs.parent) and file.is_file() and sha(file.read_bytes())==pin['after_sha256'],'Actual Root-reviewed code/config bytes differ')
        require(set(config['source_inputs'])==set(self.owner_plan.data['source_changes']),'Source-input coverage differs')
        for row in config.get('receipt_files',[]):
            receipt=load(row)[1];peer=json_unique(receipt)
            require(isinstance(peer,dict) and peer.get('review_kind') in {'source','writing'} and peer.get('scope') in {'owner-exact-repair-changes','bounded-owner-policy-or-comment-inverse'},'Owner receipt store admits only the required typed peer JSON; no raw/private brief upload')
            self.repair_receipts[sha(receipt)]=receipt
        for source,note in self.owner_plan.data['source_changes'].items():
            bound=config['source_inputs'][source];after_raw=load(bound['after_source'])[1]
            require(sha(after_raw)==note['after_sha256'],'Owner after source bytes differ')
            if source.startswith('docs/') and source.endswith('.md'):
                rel=source[5:];after_full=after_raw.decode()
                meta,body=self.overlay.finite.source_body(after_full)
                if rel in answers:
                    before=prior_payload[rel];raw_pin=self.prior['raw_source_pins'][rel]
                    require(self.overlay.records[rel]['raw_canonical_source_sha256']==raw_pin,'Protected raw answer changed')
                    require(sha(before['effective_full_source'].encode())==note['before_sha256'],'Before is not actual production effective answer')
                else:
                    before_raw=load(bound['before_source'])[1]
                    require(sha(before_raw)==note['before_sha256'],'Nonlibrary before source differs')
                    before_meta,before_body=self.overlay.finite.source_body(before_raw.decode())
                    before={'meta':before_meta,'body':before_body,'effective_full_source':before_raw.decode()};raw_pin=sha(before_raw)
                    require((self.docs/rel).read_bytes()==after_raw,'Actual nonlibrary source is not exact Root after bytes')
                ledger_raw=load(bound['change_ledger'])[1];ledger=json_unique(ledger_raw)
                require(sha(ledger_raw)==note['repair_change_ledger_sha256'] and json_hash(ledger)==sha(ledger_raw),'Ledger must be exact canonical qJSON without newline')
                expected=repair_ledger(rel,before,after_full,ledger['body_edits'],meta)
                require(ledger==expected,'Exact before/after repair ledger differs')
                record={'path':rel,'raw_canonical_source_sha256':raw_pin,
                  'before_effective_canonical_source_sha256':note['before_sha256'],
                  'effective_full_source':after_full,'meta':meta,'body':body}
                prior_pass=bool(rel in answers and self.prior['current_quality_snapshot']['page_readiness'][rel].get('passed') is True)
                if prior_pass:
                    from library_owner_repair_post_s5 import validate_legal_ordinary
                    from library_owner_repair_required28 import ANTHROPIC,validate_anthropic_ordinary
                    readiness=self.prior['current_quality_snapshot']['page_readiness'][rel]
                    if note['class']=='legal_video':
                        validate_legal_ordinary(self.overlay,self.overlay.records[rel],bound.get('ordinary_review_ids'),readiness)
                    else:
                        require(note['class']=='rule4_record_reading' and rel==ANTHROPIC,'No generic prior-PASS scoped repair allowance')
                        validate_anthropic_ordinary(self.overlay,self.overlay.records[rel],bound.get('ordinary_review_ids'),readiness)
                for kind in ['source','writing']:
                    key=bound['review_ids'][kind];require(key in self.repair_receipts,'Scoped repair peer missing')
                    validate_peer(self.repair_receipts[key],key,record,kind,sha(ledger_raw),prior_S5_pass=prior_pass)
                if rel in answers:
                    composed=compose_effective_payload(before,after_full=after_full,
                      body_edits=ledger['body_edits'],expected_before_sha256=note['before_sha256'],
                      raw_source_sha256=raw_pin,review_ids={**bound['review_ids'],'path':rel},
                      receipt_store=self.repair_receipts,source_parser=self.overlay.finite.source_body,
                      allowed_metadata_fields={'title','headline','description','date_modified'},
                      actual_adoption_utc=note['actual_adoption_utc'],prior_S5_pass=prior_pass,ordinary_review_ids=bound.get('ordinary_review_ids'))
                    actual=self.overlay.records[rel]
                    require(actual['effective_full_source']==composed['effective_full_source'] and actual['body']==composed['body'] and actual['meta']==composed['meta'] and actual['review_ids']==composed['review_ids'],'Base compiler did not consume exact repair payload and peer-ID scopes')
                else:
                    require(exact_edits(before['body'].encode(),ledger['body_edits']).decode()==body,'Nonlibrary body does not reconstruct from actual before')
                    require(meta.get('date_published')==before['meta'].get('date_published'),'Nonlibrary published date changed')
                    require(meta.get('date_modified')==note['actual_adoption_utc'],'Nonlibrary actual modification date differs')
                self.repair_sources[rel]=record
                self.repair_before_sources[rel]=copy.deepcopy(before)
                if note['class']=='appendix_seo':
                    from library_owner_repair_absence_seo import validate_seo_source
                    validate_seo_source(rel,before['effective_full_source'],after_full,self.overlay.finite.source_body)
                from library_owner_repair_post_s5 import INFO,validate_info_trim
                if rel==INFO:
                    validate_info_trim(record,trim_raw=load(bound['V7_four_trim_ledger'])[1],cumulative_raw=load(bound['V7_cumulative_ledger'])[1],pretrim_full=load(bound['V6_intermediate_source'])[1].decode(),source_parser=self.overlay.finite.source_body,actual_ledger_raw=ledger_raw)
                if note['class']=='legal_video':
                    from library_owner_repair_legal_video import validate_legal_video
                    media=load(bound['source_media_receipt'])[1]
                    validate_legal_video(record=record,ledger=ledger,playback_raw=load(bound['Root_playback_receipt'])[1],frames=bound['Root_playback_frame_sha256'],source_media_raw=media,source_media_sha256=sha(media),current_source_peer_sha256=bound['review_ids']['source'])
                if note['class']=='rule4_fact':
                    fact_raw=load(bound['published_facts'])[1];proof_raw=load(bound['published_facts_source_receipt'])[1]
                    fact_records=json_unique(fact_raw);proof=json_unique(proof_raw)
                    require(proof.get('approved') is True and proof.get('review_kind')=='source' and proof.get('scope')=='source-published-owner-repair-facts' and proof.get('policy')==POLICY and proof.get('published_fact_registry_sha256')==sha(fact_raw) and proof.get('current_scoped_Source_receipt_sha256')==bound['review_ids']['source'],'Actual published fact source binding missing')
                    require(proof.get('path')==rel and proof.get('effective_canonical_source_sha256')==sha(after_raw) and proof.get('effective_body_sha256')==sha(body.encode()) and proof.get('effective_meta_sha256')==json_hash(meta) and proof.get('fact_truth_and_narrow_fit_approved') is True,'Published fact peer current full/body/meta/fit differs')
                    require(proof.get('fact_bindings')==bound['fact_bindings'] and proof.get('fact_bindings_sha256')==json_hash(bound['fact_bindings']),'Source actual fact span bindings differ')
                    from library_owner_repair_six_facts import validate_six_public_facts,URLS
                    prior_files={p:self.archive.read(p) for p in self.archive.namelist() if not p.endswith('/')}
                    validate_six_public_facts(fact_records,actual_prior_files=prior_files,root_source_url_pins=self.owner_plan.data['rule4_public_source_sha256'])
                    validate_fact_bindings(bound['fact_bindings'],published_records=fact_records,after_body=body,allowed_public_urls=URLS)
                if note['class'] in {'rule4_record_reading','specific_precision'}:
                    from library_owner_repair_required28 import validate_case
                    proof=load(bound['specific_Source_evidence_receipt'])[1]
                    validate_case(record,before=before,ledger=ledger,kind=note['class'],
                        bank_ids=bank_ids,
                        actual_adoption_utc=note['actual_adoption_utc'],
                        source_proof_raw=proof,source_proof_sha256=bound['specific_Source_evidence_receipt']['sha256'],
                        current_source_peer_sha256=bound['review_ids']['source'])
            else:
                before=load(bound['before_source'])[1]
                require(sha(before)==note['before_sha256'] and (self.docs.parent/source).read_bytes()==after_raw,'Static/policy source before/after differs')
                if note['class']=='sample_pdf':
                    # PDF text/geometry/source/visual proof belongs to the
                    # exact named PDF validator, not a UTF-8 body-edit ledger.
                    continue
                ledger_raw=load(bound['change_ledger'])[1];ledger=json_unique(ledger_raw)
                require(json_hash(ledger)==sha(ledger_raw)==note['repair_change_ledger_sha256'],'Static ledger pin differs')
                require(exact_edits(before,ledger['body_edits'])==after_raw,'Static/policy literal inverse differs')
                if note['class']=='css_comment':css_comment_only(before,after_raw)
                if note['class']=='repository_rule':
                    require(len(ledger['body_edits'])==1 and ledger['body_edits'][0]['old_sha256']=='d6d183d2ee0c1c46ecd59a2b0c1fff60e200f9c0c2bd4a4c33f9482c735d761b' and ledger['body_edits'][0]['new_sha256']=='9290261dccd11c6267cbae84041ed8661942013f20c7f166114d8c6dd679e99c','CLAUDE repair exceeds the exact authorized prices/offers line')
                for kind in ['source','writing']:
                    key=bound['review_ids'][kind];require(key in self.repair_receipts,'Bound static repair peer missing')
                    validate_static_peer(self.repair_receipts[key],key,path=source.removeprefix('docs/'),before=before,after=after_raw,ledger=ledger,kind=kind)
        # Every unedited effective payload must remain exact, especially the
        # 23 real current PASS bodies; no parked S5 manuscript is imported.
        changed_answers=set(self.repair_sources)&answers
        require(set(self.overlay.active_revision_paths)==changed_answers,'Repair active map contains unlisted article changes')
        for rel in answers-changed_answers:
            require(self.overlay.records[rel]['effective_full_source']==prior_payload[rel]['effective_full_source'],'Unlisted prior effective article changed')
        self._repair_seal=digest([self.repair_config,self.repair_sources,self.repair_before_sources]);return self

    def check_repair(self):
        self.owner_plan.assert_current();self.post_s5_binding.check();self.overlay._check_unchanged()
        require(digest([self.repair_config,self.repair_sources,self.repair_before_sources])==self._repair_seal,'Repair inputs/records changed after bind')
        for source,note in self.owner_plan.data['source_changes'].items():
            if source.removeprefix('docs/') in self.overlay.records:continue
            require(sha((self.docs.parent/source).read_bytes())==note['after_sha256'],'Actual finite nonlibrary/policy/CSS source changed after bind')
        for rel,pin in self.owner_plan.data.get('approved_code_changes',{}).items():require(sha((self.docs.parent/rel).read_bytes())==pin['after_sha256'],'Actual Root-reviewed code changed after bind')

    def retain_owner_navigation(self,nav,files):
        from library_publication_build import retain_legacy_navigation
        from library_owner_repair_absence_seo import PATH,retain_appendix_navigation
        nav=retain_legacy_navigation(nav,files,self.overlay,self.aliases)
        if PATH in self.repair_sources:
            nav,self.appendix_nav_proof=retain_appendix_navigation(nav,files,path=PATH,before=self.repair_before_sources[PATH]['effective_full_source'],after=self.repair_sources[PATH]['effective_full_source'],source_parser=self.overlay.finite.source_body)
        return nav

    def markdown(self,markdown,page):
        result=super().markdown(markdown,page);rel=page.file.src_uri
        if rel in self.repair_sources:
            r=self.repair_sources[rel]
            require(result==r['body'] if rel in self.overlay.records else markdown==r['body'],'Actual repair Markdown differs')
            require(page.meta==r['meta'],'Actual repair metadata differs')
            page.title=page.meta['title']
        return result

    def capture_page(self,output,page):
        super().capture_page(output,page)
        if page.file.src_uri in self.repair_sources:
            self.repair_contexts[page.file.src_uri]={'markdown':page.markdown,'meta':copy.deepcopy(page.meta),'html':page.content,'toc':toc_data(page.toc),'rendered_html':output}
        return output

    def prepare_outputs(self,site_dir):
        self.check_repair();super().prepare_outputs(site_dir)
        llms_edits=self.repair_config.get('llms_line_edits',[])
        allowed_urls={SITE+public_route(p).strip('/')+'/' for p in self.repair_sources}
        # Ordinary library rows already consume effective metadata. Separate
        # owner-requested resource summaries retain their exact existing
        # title/site-name prefix unless Root's finite literal says otherwise.
        self.expected_repair_llms,self.llms_proof=apply_llms_lines((self.site/'llms.txt').read_bytes(),llms_edits,allowed_urls=allowed_urls)
        (self.site/'llms.txt').write_bytes(self.expected_repair_llms)
        nonlibrary={SITE+public_route(p).strip('/')+'/':r['meta'] for p,r in self.repair_sources.items() if not p.startswith('answers/')}
        dates={u:m['date_modified'][:10] for u,m in nonlibrary.items()}
        frozen_urls={r['url'] for r in self.owner_plan.freeze_data['frozen_sitemap_entries']}
        self.expected_repair_xml,self.expected_repair_gz,self.xml_proof,self.gz_proof=apply_nonlibrary_sitemap_dates((self.site/'sitemap.xml').read_bytes(),dates,approved_source_metadata=nonlibrary,frozen_urls=frozen_urls)
        (self.site/'sitemap.xml').write_bytes(self.expected_repair_xml);(self.site/'sitemap.xml.gz').write_bytes(self.expected_repair_gz)
        require(set(self.repair_contexts)==set(self.repair_sources),'Actual repair render coverage differs')
        for path,context in self.repair_contexts.items():context['rendered_html']=(self.site/(public_route(path).strip('/')+'/index.html')).read_bytes().decode()
        cache={'repair_input_sha256':self.repair_input_sha256,'adapter_sha256':sha(Path(__file__).read_bytes()),'contexts':self.repair_contexts}
        (self.work/'actual-owner-repair-contexts.json').write_bytes(json_bytes(cache))
        self.capture_candidate_observations()

    def capture_candidate_observations(self):
        """Always-artifact evidence even when final exact review is pending."""
        prior={p:self.archive.read(p) for p in self.archive.namelist() if not p.endswith('/') and p!='relaunch-build-provenance.json'}
        built={p.relative_to(self.site).as_posix():p.read_bytes() for p in self.site.rglob('*') if p.is_file()}
        delta={p:{'before_sha256':sha(prior[p]) if p in prior else None,'after_sha256':sha(built[p]) if p in built else None} for p in sorted(set(prior)|set(built)) if prior.get(p)!=built.get(p)}
        (self.work/'candidate-public-delta.NOT_APPROVED.json').write_bytes(json_bytes({'policy':POLICY,'approval':False,'actual_delta':delta,'candidate_all_file_sha256':{p:sha(raw) for p,raw in sorted(built.items())}}))
        import platform
        missing=[p for p in sorted(PDF_PATHS) if p in prior and p not in built]
        if missing:(self.work/'pdf-observations.AWAITING_PDF_BUILD.json').write_bytes(json_bytes({'approval':False,'paths':missing,'reason':'MkDocs precedes the owning fresh PDF build'}))
        changed=[p for p in sorted(PDF_PATHS) if p in prior and p in built and prior[p]!=built[p]]
        if not changed:return
        if platform.system()!='Linux':
            (self.work/'pdf-observations.PENDING_ACTUAL_LINUX.json').write_bytes(json_bytes({'approval':False,'paths':changed,'reason':'No actual Linux CI observation on this host'}));return
        from library_owner_repair_pdf import capture_pdf_observation
        from library_publication_generated_pdf import linux_ci_binding,manual_inputs
        ci=linux_ci_binding(self.docs.parent);out=self.work/'pdf-observations';out.mkdir(exist_ok=True)
        for p in changed:
            before_map=self.repair_config.get('pdf_before_input_maps',{}).get(p)
            require(before_map is not None and self.owner_plan.data.get('pdf_before_input_map_sha256',{}).get(p)==digest(before_map),'Actual prior PDF consumed-input map requires Root source-plan binding')
            after_map=manual_inputs(self.docs.parent) if p.startswith('absence-manual') else {'docs/'+p:sha((self.docs/p).read_bytes())}
            observation=capture_pdf_observation(p,prior[p],built[p],prior_artifact_sha256=self.inputs['actual_prior_production_binding']['artifact_sha256'],before_inputs=before_map,after_inputs=after_map,actual_ci=ci)
            (out/(p.replace('/','__')+'.NOT_APPROVED.json')).write_bytes(json_bytes(observation))

    def verify_release(self,site_dir):
        """No ordinary permit is called or its FAIL converted to a repair PASS."""
        self.site=Path(site_dir).resolve();self.check_repair()
        # The owning workflow builds Manual PDFs AFTER MkDocs. Recapture
        # candidate facts now; the post-build snapshot was necessarily early.
        self.capture_candidate_observations()
        ordinary=json.loads((self.work/'actual-render-contexts.json').read_bytes())
        require(ordinary['registry_sha256']==self.registry.fingerprint and ordinary['bridge_sha256']==sha(Path(__import__('library_publication_build').__file__).read_bytes()),'Ordinary actual context cache changed')
        contexts={p:{**c,'toc':toc_restore(c['toc']),'rendered_html':c['rendered_html'].encode()} for p,c in ordinary['contexts'].items()}
        for p,c in contexts.items():require((self.site/(public_route(p).strip('/')+'/index.html')).read_bytes()==c['rendered_html'],'Final library bytes changed after capture')
        validate_page_contexts(self.registry,contexts=contexts)
        extra=json.loads((self.work/'actual-owner-repair-contexts.json').read_bytes())
        require(extra['repair_input_sha256']==self.repair_input_sha256 and extra['adapter_sha256']==sha(Path(__file__).read_bytes()),'Repair actual context cache changed')
        content_proofs={};search_contexts={};expected_records={}
        for p,c in extra['contexts'].items():
            raw=(self.site/(public_route(p).strip('/')+'/index.html')).read_bytes()
            validate_render_context(p,self.repair_sources[p],c,raw)
            artifact=public_route(p).strip('/')+'/index.html'
            content_proofs[artifact]=validate_content_surface(p,self.repair_before_sources[p],self.repair_sources[p],c,self.archive.read(artifact),raw)
            search_contexts[p]={**c,'toc':toc_restore(c['toc'])};expected_records[p]=self.repair_sources[p]
        require(set(extra['contexts'])==set(self.repair_sources),'Cached repair context coverage differs')
        # Hubs reflect the three eligible descriptions. Validate generated
        # contexts too, while untouched nonlibrary search entries stay exact.
        for p,r in {**self.registry.records,**self.hubs}.items():
            root=public_route(p).strip('/')+'/'
            old=[r for r in json.loads(self.archive.read('search/search_index.json'))['docs'] if r.get('location','').split('#')[0]==root]
            new=[r for r in json.loads((self.site/'search/search_index.json').read_bytes())['docs'] if r.get('location','').split('#')[0]==root]
            if old!=new:search_contexts[p]=contexts[p];expected_records[p]=r
        search_proof=validate_actual_search(self.archive.read('search/search_index.json'),(self.site/'search/search_index.json').read_bytes(),changed_contexts=search_contexts,expected_records=expected_records)
        require((self.site/'llms.txt').read_bytes()==self.expected_repair_llms and (self.site/'sitemap.xml').read_bytes()==self.expected_repair_xml and (self.site/'sitemap.xml.gz').read_bytes()==self.expected_repair_gz,'Final repair derived consumer bytes differ')
        for name in ['page-head-and-structured-data','library-hubs','llms']:
            require(name in self.registry.receipts,'Actual effective consumer proof missing')
            self.overlay.register_metadata_consumer(name,self.overlay.public_metadata_fingerprint())
        # The existing deploy validator consumes then deletes this one exact
        # provenance envelope before upload-pages-artifact. It is not among
        # the actual787 public files. No other file is excluded here.
        prior={p:self.archive.read(p) for p in self.archive.namelist() if not p.endswith('/') and p!='relaunch-build-provenance.json'}
        built={p.relative_to(self.site).as_posix():p.read_bytes() for p in self.site.rglob('*') if p.is_file()}
        require('relaunch-build-provenance.json' not in built,'Provenance envelope must be created only after successful verification')
        self.freeze.check_sources(self.docs);self.freeze.check_files(built);self.s5_scope.certify_artifacts(built)
        routes={public_route(p):built[public_route(p).strip('/')+'/index.html'] for p in contexts}
        for p in ['llms.txt','sitemap.xml','sitemap.xml.gz','search/search_index.json']:routes['/'+p]=built[p]
        for p in ['absence-manual.pdf','absence-manual-v1.0-2026-08-18.pdf']:routes['/'+p]=built[p]
        from library_owner_repair_post_s5 import validate_inherited_closure
        from library_publication_canonical_stub import stub_artifact_path,validate_stub_build
        validate_inherited_closure(self.overlay,self.post_s5_binding,built)
        for source in self.overlay.merge_statuses:routes[public_route(source)]=built[stub_artifact_path(source)]
        merge_receipt=validate_stub_build(self.overlay,existing_redirects=self.archive.read('_redirects') if '_redirects' in self.archive.namelist() else b'',built_files=built,llms_text=built['llms.txt'].decode())
        state=make_compiled_state(self.overlay,built_route_artifacts=routes,redirects=self.overlay._merge_plan)
        notes=json.loads(self._file('current_annotations').read_bytes())
        require(set(notes['pages'])==set(self.overlay.records),'Repair annotations must cover actual326')
        for p,r in self.overlay.records.items():
            note=notes['pages'][p]
            require(note['opening_sha256']==sha(self.q.paragraph_after_heading(r['body']).strip().encode()),'Repair opening annotation differs')
            require(note['canonical_source_sha256'] in {r['raw_canonical_source_sha256'],r['effective_canonical_source_sha256']},'Repair annotation needs independently bound current hash')
            note.update(source_sha256=r['source_sha256'],canonical_source_sha256=r['effective_canonical_source_sha256'])
        report=complete_current_analysis(self.overlay,state,current_annotations=notes,trusted_index_references_sha256=json_hash(notes['index_question_titles']),merge_build_receipt=merge_receipt)
        report=attach_literal_scope(self.overlay,state,current_annotations=notes,runtime_report=report)
        validate_scope_union(report,state,self.q)
        transition=validate_quality_transition(self.prior['current_quality_snapshot'],report,changed_content_paths=set(self.repair_sources)&set(self.overlay.records),frozen_paths=set(self.s5_scope.frozen),post_s5_binding=self.post_s5_binding)
        (self.work/'whole-current-report.json').write_bytes(json_bytes(report))
        (self.work/'compiled-state.json').write_bytes(json_bytes(state))
        # Actual artifacts/PDFs are observations until independent Root exact
        # byte and full visual receipts are supplied. Never invent them here.
        review_raw=self._repair_load(self.repair_config['root_artifact_review'])[1];review=json_unique(review_raw)
        require(review.get('approved') is True and review.get('reviewer')=='root' and review.get('review_kind')=='root-exact-owner-repair-artifacts' and review.get('policy')==POLICY and review.get('source_plan_sha256')==self.repair_config['owner_source_plan_sha256'],'Independent Root exact artifact review missing')
        actual_delta={p:{'before_sha256':sha(prior[p]) if p in prior else None,'after_sha256':sha(built[p]) if p in built else None} for p in set(prior)|set(built) if prior.get(p)!=built.get(p)}
        require(review.get('actual_delta')==actual_delta,'Root exact after-artifact delta differs')
        nav_proofs={}
        for p,row in self.owner_plan.data['artifact_scope'].items():
            if row['class']=='navigation_only':
                a,b=__import__('library_owner_repair').spans(prior[p]),__import__('library_owner_repair').spans(built[p])
                require(len(a.styles)==len(b.styles)==1,'Actual stylesheet coverage differs')
                old_css=prior[p][a.styles[0][0]:a.styles[0][1]];new_css=built[p][b.styles[0][0]:b.styles[0][1]]
                nav_proofs[p]=validate_navigation_only(p,prior[p],built[p],old_css=old_css,new_css=new_css)
            elif row['class']=='generated_hub':
                source=row['source_path'].removeprefix('docs/');require(source in self.hubs,'Unlisted generated content artifact')
                h=self.hubs[source];approval=self.owner_plan.data['generated_hubs'][row['source_path']]
                require(approval['effective_body_sha256']==sha(h['body'].encode()) and approval['effective_meta_sha256']==json_hash(h['meta']),'Generated hub differs from exact Root review')
                c=contexts[source];content_proofs[p]={'source_path':row['source_path'],'after_sha256':sha(c['rendered_html']),'source_render_exact':True}
        pdf_proofs=self._validated_pdf_reviews(prior,built)
        derived={'llms.txt':self.llms_proof,'sitemap.xml':self.xml_proof,'sitemap.xml.gz':self.gz_proof,'search/search_index.json':search_proof}
        result=validate_artifact_delta(self.owner_plan,prior=prior,candidate=built,pdf_reviews=pdf_proofs,navigation_proofs=nav_proofs,content_proofs=content_proofs,derived_proofs=derived)
        result.update(transition);result['root_artifact_review_sha256']=sha(review_raw)
        result['whole_current_quality_passed']=report.get('passed') is True;result['eligible_S5_completion_passed']=report.get('eligible_completion_passed') is True
        result['owner_finite_repair_passed']=True;result['public_or_live_verified']=False
        result['owner_brief_all_items_complete']=False
        (self.work/'owner-repair-result.json').write_bytes(json_bytes(result));return result

    def _validated_pdf_reviews(self,prior,built):
        from library_owner_repair_pdf import validate_owner_pdf_review
        from library_publication_generated_pdf import linux_ci_binding,manual_inputs
        result={};current_ci=linux_ci_binding(self.docs.parent)
        for p in PDF_PATHS:
            if prior.get(p)==built.get(p):continue
            row=self.repair_config.get('pdf_reviews',{}).get(p);require(row is not None,'Changed named PDF awaits actual Linux/full-text/all-page Root visual review')
            actual_after=manual_inputs(self.docs.parent) if p.startswith('absence-manual') else {'docs/'+p:sha((self.docs/p).read_bytes())}
            require(actual_after==row['after_inputs'],'Actual PDF consumed source/config/generator differs on successful rerun')
            require(self.owner_plan.data.get('pdf_before_input_map_sha256',{}).get(p)==digest(row['before_inputs']),'PDF prior consumed inputs are not Root-plan bound')
            kwargs={k:self._repair_load(row[k])[1] for k in ['review_raw','visual_raw','source_review_raw']}
            observation=json_unique(self._repair_load(row['observation'])[1]);frames={}
            for f in row['rendered_frames']:frames[(f['version'],f['page'])]=self._repair_load(f['file'])[1]
            prior_reads={ref['sha256']:self._repair_load(ref)[1] for ref in row.get('prior_visual_receipts',[])}
            result[p]=validate_owner_pdf_review(path=p,old=prior[p],new=built[p],review_sha256=sha(kwargs['review_raw']),visual_sha256=sha(kwargs['visual_raw']),source_review_sha256=sha(kwargs['source_review_raw']),observation=observation,rendered_frames=frames,before_inputs=row['before_inputs'],after_inputs=row['after_inputs'],prior_artifact_sha256=self.inputs['actual_prior_production_binding']['artifact_sha256'],source_change_pins=self.owner_plan.data['source_changes'],approved_code_pins=self.owner_plan.data.get('approved_code_changes',{}),current_ci=current_ci,prior_visual_receipts=prior_reads,**kwargs)
        return result


_CURRENT=None


def current_session():
    require(isinstance(_CURRENT,OwnerRepairBuildSession),'Owner repair was not explicitly bound before stylesheet retention')
    return _CURRENT


def from_environment(config):
    global _CURRENT
    path=os.environ.get('BW_OWNER_REPAIR_INPUTS');pin=os.environ.get('BW_OWNER_REPAIR_INPUTS_SHA256')
    require(path and re.fullmatch('[0-9a-f]{64}',str(pin)),'Explicit independently pinned owner repair inputs are required')
    require(not any(k in os.environ for k in ['BW_LIBRARY_PUBLICATION_INPUTS','BW_LIBRARY_PUBLICATION_INPUTS_SHA256']),'Owner repair and ordinary S5 dispatch cannot be active together')
    require(not any(k.startswith('BW_OWNER_REPAIR_') and k not in {'BW_OWNER_REPAIR_INPUTS','BW_OWNER_REPAIR_INPUTS_SHA256'} for k in os.environ),'Unknown Owner dispatch key')
    _CURRENT=OwnerRepairBuildSession.load(config['docs_dir'],path,pin,Path(config['site_dir']).resolve().parent/'.owner-repair-work')
    return _CURRENT


def main():
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--inputs',required=True);p.add_argument('--inputs-sha256',required=True);p.add_argument('--docs',required=True);p.add_argument('--site',required=True);p.add_argument('--work',required=True);a=p.parse_args()
    session=OwnerRepairBuildSession.load(a.docs,a.inputs,a.inputs_sha256,a.work)
    # This CLI is read-only with respect to the built site. Derived expected
    # bytes are recomputed from trusted prior sources, never from stale cache.
    session.site=Path(a.site).resolve()
    spec=importlib.util.spec_from_file_location('_bw_repair_verify_llms',session.docs.parent/'tools/generate_answers_llms.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    hm={p:r['meta'] for p,r in session.hubs.items()}
    base_llms=generate_effective_llms(session.registry,original=session.archive.read('llms.txt'),hub_metadata=hm,source_generator=module)
    allowed={SITE+public_route(p).strip('/')+'/' for p in session.repair_sources}
    session.expected_repair_llms,session.llms_proof=apply_llms_lines(base_llms,session.repair_config.get('llms_line_edits',[]),allowed_urls=allowed)
    xml,_=generate_effective_sitemaps(session.registry,prior_xml=session.archive.read('sitemap.xml'),hub_metadata=hm,merged_sources=session.overlay.merge_statuses,field_freeze=session.freeze,publication_dates=session.publication_dates)
    nonlib={SITE+public_route(p).strip('/')+'/':r['meta'] for p,r in session.repair_sources.items() if not p.startswith('answers/')}
    dates={u:m['date_modified'][:10] for u,m in nonlib.items()}
    session.expected_repair_xml,session.expected_repair_gz,session.xml_proof,session.gz_proof=apply_nonlibrary_sitemap_dates(xml,dates,approved_source_metadata=nonlib,frozen_urls={r['url'] for r in session.owner_plan.freeze_data['frozen_sitemap_entries']})
    print(json.dumps(session.verify_release(a.site),indent=2))


if __name__=='__main__':main()
