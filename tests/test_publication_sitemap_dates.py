"""Fictional source/payload/producer fixtures, never actual Root approvals."""
import copy,gzip,json,pathlib,sys,tempfile,unittest
from datetime import datetime,timezone,timedelta
from types import SimpleNamespace
HERE=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE/'tools'))
from library_publication_overlay import sha,canonical,OverlayError
from library_publication_release import state_fingerprint
from library_publication_consumers import (EffectiveRegistry,public_route,SITE,generate_effective_sitemaps,validate_effective_sitemap)
from library_publication_sitemap_dates import bind_publication_dates,BoundPublicationDates,_derive_dates,POLICY


def encoded(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()


class Fixture:
    def __init__(self,root):
        import yaml
        from library_related_chapter_links import source_body
        self.docs=root/'docs';self.docs.mkdir(parents=True);self.q=SimpleNamespace(canonical_json=lambda v:encoded(v).decode())
        self.finite=SimpleNamespace(source_body=source_body)
        self.path='answers/measurement/first.md';self.hub='answers/measurement/index.md'
        self.payloads={};self.prior_hubs={};self.records={};self.hubs={};self.routes={};self.artifacts={};self.sourcepins={}
        for rel in [self.path,self.hub,'answers/index.md']:
            meta={'title':rel,'headline':rel,'description':'A synthetic dated result.','library_cluster':'measurement','date_published':'2026-10-28T01:00:00+00:00','date_modified':'2026-10-29T01:00:00+00:00'}
            body='# '+rel+'\n\nA synthetic result.\n'
            full='---\n'+yaml.safe_dump(meta,sort_keys=False)+'---\n\n'+body
            actual_meta,body=source_body(full);fullpath=self.docs/rel;fullpath.parent.mkdir(parents=True,exist_ok=True);fullpath.write_text(full,encoding='utf-8')
            p={'meta':meta,'body':body,'effective_full_source':full,'canonical_source_sha256':sha(full.encode())}
            route=public_route(rel);self.artifacts[route]=('fictional compiled '+rel).encode()
            if rel==self.path:
                self.payloads[rel]=p;self.records[rel]={'meta':meta,'body':body,'cluster':'measurement','effective_canonical_source_sha256':sha(full.encode())}
                self.sourcepins[rel]=sha(full.encode());self.routes[route]={'kind':'article','path':rel,'compiled_sha256':sha(self.artifacts[route]),'effective_canonical_sha256':sha(full.encode()),'body_sha256':sha(body.encode()),'metadata_sha256':sha(encoded(meta))}
            else:self.prior_hubs[rel]=p;self.hubs[rel]={'meta':meta,'body':body};self.routes[route]={'kind':'auxiliary','compiled_sha256':sha(self.artifacts[route])}
        yesterday=(datetime.now(timezone.utc)-timedelta(days=1)).date().isoformat()
        self.xml=b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        self.nonlibrary=b'<url><loc>https://docs.broadcastwell.com/research/record/</loc><lastmod>2026-10-20</lastmod></url>'
        self.xml+=self.nonlibrary+b'\n'
        for rel in [self.path,self.hub,'answers/index.md']:
            self.xml+=b'<url><loc>'+(SITE+public_route(rel)).encode()+b'</loc><lastmod>'+yesterday.encode()+b'</lastmod></url>\n'
        self.xml+=b'</urlset>'
        self.artifacts['/sitemap.xml']=self.xml;self.routes['/sitemap.xml']={'kind':'auxiliary','compiled_sha256':sha(self.xml)}
        binding={'commit_sha':'a'*40,'deployment_id':'synthetic','artifact_sha256':'b'*64,'served_receipt_sha256':'c'*64}
        self.prior={'schema_version':1,'routes':self.routes,'raw_source_pins':self.sourcepins,'production_binding':binding}
        self.overlay=SimpleNamespace(docs=self.docs,records=self.records,prior=self.prior,q=self.q,finite=self.finite,_check_unchanged=lambda:None,active_revision_paths=[],s5_scope=None)
        self.registry=EffectiveRegistry(self.overlay);self.registry.hubs=copy.deepcopy(self.hubs)
        self.receipt={'approved':True,'review_kind':'prior-production-effective-payload','actual_served_readback':True,'source_render_equality_passed':True,'production_binding':binding,'payload_bundle_sha256':'d'*64,'compiled_collection_fingerprint':state_fingerprint(self.prior,self.q),'compiled_route_hashes':{r:sha(b) for r,b in sorted(self.artifacts.items())},'hub_payload_bundle_sha256':'e'*64,'hub_source_render_equality_passed':True,'scope':'FICTIONAL UNIT FIXTURE ONLY'}

    def bind(self):
        return bind_publication_dates(self.registry,prior_xml=self.xml,prior_payload_bundle={'schema_version':1,'pages':self.payloads},prior_hub_bundle={'schema_version':1,'hubs':self.prior_hubs},actual_prior_artifacts=self.artifacts,producer_receipt=self.receipt,payload_file_sha256='d'*64,hub_file_sha256='e'*64)

    def refresh(self):
        self.overlay.records=self.records;self.registry=EffectiveRegistry(self.overlay);self.registry.hubs=copy.deepcopy(self.hubs)


class SitemapDateTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.f=Fixture(pathlib.Path(self.temp.name))

    def generate(self,binding):
        return generate_effective_sitemaps(self.f.registry,prior_xml=self.f.xml,hub_metadata={p:r['meta'] for p,r in self.f.registry.hubs.items()},publication_dates=binding)

    def test_unchanged_identity_preserves_actual_XML_and_nonlibrary_entries(self):
        binding=self.f.bind();xml,gz=self.generate(binding)
        self.assertEqual(self.f.xml,xml);self.assertEqual(xml,gzip.decompress(gz))
        self.assertIn(self.f.nonlibrary,xml)
        self.assertEqual({'EXACT_UNCHANGED_PRIOR_PUBLICATION_LASTMOD'},{r['policy'] for r in binding.audit().values()})

    def test_no_trusted_proof_keeps_old_strict_source_date_behavior(self):
        with self.assertRaisesRegex(OverlayError,'stale metadata dates'):
            validate_effective_sitemap(self.f.registry,prior_xml=self.f.xml,candidate_xml=self.f.xml,hub_metadata=self.f.hubs and {p:r['meta'] for p,r in self.f.hubs.items()})

    def test_plain_date_mapping_cannot_grant_preservation(self):
        with self.assertRaisesRegex(OverlayError,'Arbitrary sitemap'):
            self.generate({SITE+public_route(self.f.path):'2026-10-20'})
        with self.assertRaises(TypeError):BoundPublicationDates()

    def test_unapproved_or_stale_prior_producer_fails(self):
        for field,value in [('approved',False),('hub_payload_bundle_sha256','f'*64),('hub_source_render_equality_passed',False),('source_render_equality_passed',False)]:
            f=Fixture(pathlib.Path(self.temp.name)/field);f.receipt[field]=value
            with self.assertRaises(OverlayError):f.bind()

    def test_changed_article_uses_actual_modified_date_and_not_old_publication_date(self):
        self.f.records[self.f.path]['body']+='Changed fact.\n'
        now=(datetime.now(timezone.utc)-timedelta(seconds=1)).replace(microsecond=0).isoformat()
        self.f.records[self.f.path]['meta']=dict(self.f.records[self.f.path]['meta'],date_modified=now)
        self.f.records[self.f.path]['effective_canonical_source_sha256']='9'*64
        self.f.overlay.active_revision_paths=[self.f.path];self.f.refresh();binding=self.f.bind();xml,_=self.generate(binding)
        self.assertIn(b'<lastmod>'+now[:10].encode()+b'</lastmod>',xml)
        self.assertEqual('ACTUAL_REVIEWED_CHANGED_OR_NEW_MODIFICATION_DATE',binding.audit()[self.f.path]['policy'])

    def test_active_noop_cannot_reuse_stale_modification_timestamp(self):
        self.f.overlay.active_revision_paths=[self.f.path]
        with self.assertRaisesRegex(OverlayError,'stale source modification'):self.f.bind()

    def test_new_explicit_record_uses_reviewed_modification_date(self):
        path='answers/measurement/new.md';stamp=(datetime.now(timezone.utc)-timedelta(seconds=1)).replace(microsecond=0).isoformat()
        (self.f.docs/path).write_text('# New fictional page\n')
        self.f.records[path]={'meta':dict(self.f.records[self.f.path]['meta'],title='New',date_modified=stamp),'body':'# New fictional page\n','cluster':'measurement','effective_canonical_source_sha256':'6'*64}
        self.f.overlay.active_revision_paths=[path];self.f.refresh();binding=self.f.bind();xml,_=self.generate(binding)
        self.assertIn((SITE+public_route(path)).encode(),xml)
        self.assertEqual(stamp[:10],binding.audit()[path]['lastmod'])
        self.assertEqual('ACTUAL_REVIEWED_CHANGED_OR_NEW_MODIFICATION_DATE',binding.audit()[path]['policy'])

    def test_unmapped_body_or_source_change_cannot_claim_unchanged(self):
        self.f.records[self.f.path]['body']+='Unmapped fact.';self.f.refresh()
        with self.assertRaisesRegex(OverlayError,'explicit reviewed active'):self.f.bind()
        self.f.records[self.f.path]['body']=self.f.payloads[self.f.path]['body'];self.f.refresh()
        p=self.f.docs/self.f.path;p.write_text(p.read_text()+'\n')
        with self.assertRaisesRegex(OverlayError,'explicit reviewed active'):self.f.bind()

    def test_changed_hub_uses_current_modified_date(self):
        self.f.hubs[self.f.hub]['body']+='Changed hub link.\n'
        now=(datetime.now(timezone.utc)-timedelta(seconds=1)).replace(microsecond=0).isoformat()
        self.f.hubs[self.f.hub]['meta']=dict(self.f.hubs[self.f.hub]['meta'],date_modified=now)
        self.f.refresh();binding=self.f.bind();self.generate(binding)
        self.assertEqual(now[:10],binding.audit()[self.f.hub]['lastmod'])

    def test_stale_hub_timestamp_or_missing_hub_payload_fails(self):
        self.f.hubs[self.f.hub]['body']+='Changed hub link.\n';self.f.refresh()
        with self.assertRaisesRegex(OverlayError,'stale source modification'):self.f.bind()
        self.f.hubs=copy.deepcopy(self.f.prior_hubs);self.f.prior_hubs.pop(self.f.hub)
        with self.assertRaisesRegex(OverlayError,'hide or invent'):self.f.bind()

    def test_different_prior_xml_hash_and_changed_payload_pins_fail(self):
        self.f.xml=self.f.xml.replace(b'2026-10-20',b'2026-10-21')
        with self.assertRaisesRegex(OverlayError,'Prior XML differs'):self.f.bind()
        self.f.xml=self.f.artifacts['/sitemap.xml'];self.f.payloads[self.f.path]['body']+='tampered'
        with self.assertRaisesRegex(OverlayError,'payload'):self.f.bind()

    def test_bound_source_and_body_are_rechecked_after_binding(self):
        binding=self.f.bind();self.f.records[self.f.path]['body']+='Late change'
        with self.assertRaises(OverlayError):self.generate(binding)

    def test_frozen_XML_is_exact_and_frozen_changed_record_fails(self):
        path=self.f.path;url=SITE+public_route(path)
        self.f.overlay.s5_scope=SimpleNamespace(frozen=frozenset([path]))
        binding=self.f.bind();xml,_=self.generate(binding);self.assertEqual(xml,self.f.xml)
        self.f.records[path]['body']+='Forbidden frozen edit';self.f.records[path]['effective_canonical_source_sha256']='8'*64
        self.f.overlay.active_revision_paths=[path];self.f.refresh()
        with self.assertRaisesRegex(OverlayError,'Frozen effective'):self.f.bind()

    def test_future_or_backdated_active_timestamp_is_rejected(self):
        for stamp in ['2026-10-30T01:00:00+00:00',(datetime.now(timezone.utc)+timedelta(days=1)).isoformat()]:
            self.f.overlay.active_revision_paths=[self.f.path];self.f.records[self.f.path]['meta']=dict(self.f.records[self.f.path]['meta'],date_modified=stamp)
            self.f.records[self.f.path]['effective_canonical_source_sha256']='7'*64;self.f.refresh()
            with self.assertRaises(OverlayError):self.f.bind()


    def generated_hub(self,fixture=None):
        # A real raw source stays intact while its served hub removes/relabels
        # membership. This is deliberately not raw/effective hash equality.
        import yaml
        fixture=fixture or self.f
        previous=fixture.prior_hubs[fixture.hub]
        raw=canonical((fixture.docs/fixture.hub).read_bytes())
        body='# Fictional generated hub\n\n[First](first.md)\n'
        full='---\n'+yaml.safe_dump(previous['meta'],sort_keys=False)+'---\n\n'+body
        meta,body=fixture.finite.source_body(full)
        previous.update(effective_full_source=full,canonical_source_sha256=sha(full.encode()),body=body)
        fixture.hubs[fixture.hub]={'meta':meta,'body':body}
        for path,hub in fixture.prior_hubs.items():
            hub['raw_canonical_source_sha256']=sha(canonical((fixture.docs/path).read_bytes()).encode())
        fixture.receipt.update(hub_raw_source_git_proof_passed=True,
            hub_raw_source_pins={path:hub['raw_canonical_source_sha256'] for path,hub in fixture.prior_hubs.items()},
            hub_payload_canonical_json_sha256=sha(encoded({'schema_version':1,'hubs':fixture.prior_hubs})))
        fixture.refresh()
        self.assertNotEqual(sha(raw.encode()),previous['canonical_source_sha256'])
        return fixture

    def test_generated_hub_raw_differs_from_effective_and_retains_actual_XML_date(self):
        self.generated_hub()
        binding=self.f.bind();xml,gz=self.generate(binding)
        self.assertEqual(self.f.xml,xml)
        self.assertEqual(xml,gzip.decompress(gz))
        self.assertEqual('EXACT_UNCHANGED_PRIOR_PUBLICATION_LASTMOD',binding.audit()[self.f.hub]['policy'])
        self.assertNotEqual(self.f.hubs[self.f.hub]['meta']['date_modified'][:10],binding.audit()[self.f.hub]['lastmod'])

    def test_generated_hub_raw_SHA_must_be_valid_and_match_actual_source(self):
        for value in ['',False,'ABCDEF'*10,'g'*64,'0'*63]:
            with self.subTest(raw=value):
                f=self.generated_hub(Fixture(pathlib.Path(self.temp.name)/('malformed-'+str(value))))
                f.prior_hubs[f.hub]['raw_canonical_source_sha256']=value
                with self.assertRaisesRegex(OverlayError,'raw source SHA'):f.bind()
        self.generated_hub();path=self.f.docs/self.f.hub
        path.write_bytes(path.read_bytes()+b'\nChanged raw hub.\n')
        with self.assertRaisesRegex(OverlayError,'stale source modification'):self.f.bind()

    def test_generated_hub_requires_whole_approved_bundle_and_Git_raw_receipt(self):
        cases=[('approved',False),('hub_payload_bundle_sha256','f'*64),
            ('hub_raw_source_git_proof_passed',False),('hub_raw_source_pins',{}),
            ('hub_payload_canonical_json_sha256',None),('hub_payload_canonical_json_sha256','f'*64)]
        for n,(key,value) in enumerate(cases):
            with self.subTest(field=key):
                f=self.generated_hub(Fixture(pathlib.Path(self.temp.name)/('proof-'+str(n))))
                f.receipt[key]=value
                with self.assertRaises(OverlayError):f.bind()

    def test_generated_hub_coherent_payload_or_component_tampering_is_rejected(self):
        for kind in ['full','canonical','body','meta','coherent']:
            with self.subTest(kind=kind):
                f=self.generated_hub(Fixture(pathlib.Path(self.temp.name)/kind))
                previous=f.prior_hubs[f.hub]
                if kind in ['full','coherent']:previous['effective_full_source']+='\nUnapproved generated link.\n'
                if kind=='canonical':previous['canonical_source_sha256']='f'*64
                if kind=='body':previous['body']+='Unapproved body.\n'
                if kind=='meta':previous['meta']=dict(previous['meta'],title='Unapproved title')
                if kind=='coherent':
                    previous['canonical_source_sha256']=sha(previous['effective_full_source'].encode())
                    previous['meta'],previous['body']=f.finite.source_body(previous['effective_full_source'])
                    f.hubs[f.hub]={'meta':previous['meta'],'body':previous['body']};f.refresh()
                with self.assertRaises(OverlayError):f.bind()

    def test_generated_hub_current_body_change_still_needs_actual_modified_date(self):
        self.generated_hub();self.f.hubs[self.f.hub]['body']+='New current link.\n';self.f.refresh()
        with self.assertRaisesRegex(OverlayError,'stale source modification'):self.f.bind()
        now=(datetime.now(timezone.utc)-timedelta(seconds=1)).replace(microsecond=0).isoformat()
        self.f.hubs[self.f.hub]['meta']=dict(self.f.hubs[self.f.hub]['meta'],date_modified=now)
        self.f.refresh();binding=self.f.bind();self.generate(binding)
        self.assertEqual('ACTUAL_REVIEWED_CHANGED_OR_NEW_MODIFICATION_DATE',binding.audit()[self.f.hub]['policy'])
        self.assertEqual(now[:10],binding.audit()[self.f.hub]['lastmod'])

    def test_generated_hub_split_does_not_weaken_compiled_or_render_proof(self):
        for kind in ['compiled','render','hub_render','legacy_without_raw']:
            with self.subTest(kind=kind):
                f=self.generated_hub(Fixture(pathlib.Path(self.temp.name)/kind))
                if kind=='compiled':f.artifacts[public_route(f.hub)]+=b'unapproved'
                if kind=='render':f.receipt['source_render_equality_passed']=False
                if kind=='hub_render':f.receipt['hub_source_render_equality_passed']=False
                if kind=='legacy_without_raw':
                    for hub in f.prior_hubs.values():hub.pop('raw_canonical_source_sha256')
                with self.assertRaises(OverlayError):f.bind()



    def test_declared_raw_proof_cannot_be_downgraded_by_removing_optional_fields(self):
        self.generated_hub()
        trusted_receipt=copy.deepcopy(self.f.receipt)
        trusted_artifacts=copy.deepcopy(self.f.artifacts)
        for path,previous in self.f.prior_hubs.items():
            previous.pop('raw_canonical_source_sha256')
            raw=canonical((self.f.docs/path).read_bytes())
            meta,body=self.f.finite.source_body(raw)
            previous.update(effective_full_source=raw,canonical_source_sha256=sha(raw.encode()),meta=meta,body=body)
            self.f.hubs[path]={'meta':meta,'body':body}
        self.f.refresh()
        self.assertEqual(trusted_receipt,self.f.receipt)
        self.assertEqual(trusted_artifacts,self.f.artifacts)
        self.assertNotEqual(self.f.receipt['hub_payload_canonical_json_sha256'],
            sha(encoded({'schema_version':1,'hubs':self.f.prior_hubs})))
        with self.assertRaisesRegex(OverlayError,'object differs from independently approved bundle'):
            self.f.bind()



if __name__=='__main__':unittest.main()
