"""Private meaningful effective-consumer/UTC regressions, synthetic where stated."""
import copy,datetime,gzip,importlib.util,json,os,pathlib,sys,tempfile,unittest
from types import SimpleNamespace
from unittest.mock import patch
HERE=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'tools'))
from library_publication_overlay import PublicationOverlay,OverlayError,sha,utc_calendar_day,FREE_CHECK_TOKEN,LIMIT_SENTENCE,next_step_span
from library_publication_composition import neutral_footer_issues
from library_publication_consumers import (EffectiveRegistry,render_hub_body,generate_effective_hubs,generate_effective_llms,generate_effective_sitemaps,validate_effective_sitemap,validate_effective_search,compare_complete_artifacts,validate_page_contexts,public_route)

def encoded(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
class Fixture:
    def __init__(self):
        self.paths=['answers/measurement/first.md','answers/measurement/second.md']
        self.records={}
        for i,p in enumerate(self.paths):
            meta={'title':['First question?','Second question?'][i],'headline':['First question?','Second question?'][i],'description':['First dated result.','Second dated result.'][i],'date_published':'2026-10-28T01:00:00+00:00','date_modified':'2026-10-29T02:00:00+00:00','library_cluster':'measurement','library_order':i}
            body='# '+meta['title']+'\n\n'+meta['description']+'\n'
            self.records[p]={'meta':meta,'cluster':'measurement','body':body,'effective_canonical_source_sha256':sha(body.encode())}
        q=SimpleNamespace(canonical_json=lambda x:encoded(x).decode())
        self.overlay=SimpleNamespace(records=self.records,q=q,_check_unchanged=lambda:None)
        self.registry=EffectiveRegistry(self.overlay)
        self.raw={p:copy.deepcopy(r['meta']) for p,r in self.records.items()}
        common={'date_published':'2026-10-28T01:00:00+00:00','date_modified':'2026-10-30T03:00:00+00:00','library_order':1}
        self.hubs={'answers/index.md':{'meta':dict(common,title='All answers',headline='All answers',description='2 answers with dates.'),'body':'# All answers\n\nThese 2 pages have dates.\n\n## Start here\n\n- [First question?](measurement/first.md) First dated result.\n\n[Research](../research/study.md)\n','canonical_sha256':'a'*64},'answers/measurement/index.md':{'meta':dict(common,title='Measurement',headline='Measurement',description='Measurements with dates.'),'body':'# Measurement\n\nThese 2 answers have dates.\n\n## Questions\n\n[First question?](first.md)\n\nFirst dated result.\n\n[Second question?](second.md)\n\nSecond dated result.\n\n[Research](../../research/study.md)\n','canonical_sha256':'b'*64}}
        self.generated=generate_effective_hubs(self.registry,hub_sources=self.hubs,raw_leaf_metadata=self.raw,approved_hub_changes={})
        self.hubmeta={p:r['meta'] for p,r in self.generated.items()}
        self.xml=b'<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        for url in ['https://docs.broadcastwell.com/','https://docs.broadcastwell.com/research/record/','https://docs.broadcastwell.com/answers/','https://docs.broadcastwell.com/answers/measurement/','https://docs.broadcastwell.com/answers/measurement/first/','https://docs.broadcastwell.com/answers/measurement/second/']:
            self.xml+=b'<url><loc>'+url.encode()+b'</loc><lastmod>2026-11-02</lastmod></url>\n'
        self.xml+=b'</urlset>\n'

    def contexts(self):
        import markdown,html
        result={}
        for path,r in {**self.registry.records,**self.registry.hubs}.items():
            m=r['meta'];url='https://docs.broadcastwell.com'+public_route(path)
            body=markdown.markdown(r['body'],extensions=['toc','tables','attr_list','md_in_html','def_list','footnotes','admonition'],extension_configs={'toc':{'permalink':True,'toc_depth':3}})
            # These fixture links are ordinary leaf .md targets; MkDocs emits directory URLs.
            body=body.replace('.md"','/"')
            article={'@type':'Article','headline':m['headline'],'name':m['headline'],'description':m['description'],'datePublished':m['date_published'],'dateModified':m['date_modified'],'url':url,'isBasedOn':m.get('is_based_on','')}
            meta={'description':m['description'],'og:title':m['title'],'og:description':m['description'],'og:url':url,'twitter:title':m['title'],'twitter:description':m['description']}
            head='<title>'+html.escape(m['title'])+' | The Absence Manual</title><link rel="canonical" href="'+url+'">'+''.join('<meta name="'+k+'" content="'+html.escape(v,quote=True)+'">' for k,v in meta.items())
            head+='<script type="application/ld+json">'+json.dumps(article)+'</script><script type="application/ld+json">'+json.dumps({'@type':'BreadcrumbList','itemListElement':[{'name':m['title']}]})+'</script>'
            rendered=head+'<article>'+body+'\n<hr><p class="manual-footer-version">Broadcastwell answer library. Prose and figures CC BY 4.0. Site code MIT. <a href="https://docs.broadcastwell.com/answers/">Read the library</a>.</p></article>'
            result[path]={'meta':copy.deepcopy(m),'markdown':r['body'],'html':body,'toc':[],'rendered_html':rendered.encode()}
        return result

    def search(self,contexts):
        from material.plugins.search.plugin import SearchIndex
        index=SearchIndex(lang=['en'])
        for p,c in contexts.items():
            index.add_entry_from_context(SimpleNamespace(meta=c['meta'],title=c['meta']['title'],content=c['html'],toc=c['toc'],url=public_route(p).lstrip('/')))
        return {'config':{'lang':['en']},'docs':[{'location':'research/record/','title':'Research record','text':'Unchanged research.'}]+index.entries}


class ConsumerTests(unittest.TestCase):
    def setUp(self):self.f=Fixture()
    def test_identity_hubs_preserve_every_existing_byte(self):
        for p,h in self.f.hubs.items():self.assertEqual(h['body'],self.f.generated[p]['body']);self.assertEqual(h['meta'],self.f.generated[p]['meta'])
    def test_changed_title_description_uses_real_effective_metadata(self):
        r=self.f.registry.records[self.f.paths[0]];r['meta']['title']='Updated question?';r['meta']['description']='Updated dated result.'
        # Construct an explicit new registry, as the owning compile would do.
        self.f.overlay.records=self.f.registry.records;registry=EffectiveRegistry(self.f.overlay)
        body=render_hub_body(registry,path='answers/measurement/index.md',body=self.f.hubs['answers/measurement/index.md']['body'],raw_leaf_metadata=self.f.raw)
        self.assertIn('[Updated question?](first.md)\n\nUpdated dated result.',body);self.assertIn('[Research](../../research/study.md)',body)
    def test_changed_hub_requires_exact_reviewed_body_binding(self):
        self.f.overlay.records[self.f.paths[0]]['meta']['description']='Revised fact.';registry=EffectiveRegistry(self.f.overlay)
        with self.assertRaisesRegex(OverlayError,'reviewed generated-body binding'):
            generate_effective_hubs(registry,hub_sources=self.f.hubs,raw_leaf_metadata=self.f.raw,approved_hub_changes={})
    def test_nonmetadata_excerpt_is_not_silently_rewritten(self):
        body=self.f.hubs['answers/measurement/index.md']['body'].replace('First dated result.','A separately written excerpt.')
        with self.assertRaisesRegex(OverlayError,'excerpt differs'):
            render_hub_body(self.f.registry,path='answers/measurement/index.md',body=body,raw_leaf_metadata=self.f.raw)
    def test_subtopic_change_requires_explicit_group_patch(self):
        self.f.overlay.records[self.f.paths[0]]['meta']['library_subtopic']='New group';registry=EffectiveRegistry(self.f.overlay)
        with self.assertRaisesRegex(OverlayError,'Subtopic change'):
            render_hub_body(registry,path='answers/measurement/index.md',body=self.f.hubs['answers/measurement/index.md']['body'],raw_leaf_metadata=self.f.raw)
    def test_missing_effective_hub_leaf_rejected(self):
        body=self.f.hubs['answers/measurement/index.md']['body'].replace('[Second question?](second.md)\n\nSecond dated result.\n','')
        with self.assertRaisesRegex(OverlayError,'hides or duplicates'):
            render_hub_body(self.f.registry,path='answers/measurement/index.md',body=body,raw_leaf_metadata=self.f.raw)
    def test_sitemap_dates_derive_metadata_and_nonlibrary_elements_stay_exact(self):
        xml,gz=generate_effective_sitemaps(self.f.registry,prior_xml=self.f.xml,hub_metadata=self.f.hubmeta)
        self.assertIn(b'<loc>https://docs.broadcastwell.com/research/record/</loc><lastmod>2026-11-02</lastmod>',xml)
        self.assertIn(b'<loc>https://docs.broadcastwell.com/answers/measurement/first/</loc><lastmod>2026-10-29</lastmod>',xml)
        self.assertEqual(xml,gzip.decompress(gz));self.assertEqual(255,gz[9]);self.assertEqual(b'\0\0\0\0',gz[4:8])
        self.assertEqual((xml,gz),generate_effective_sitemaps(self.f.registry,prior_xml=self.f.xml,hub_metadata=self.f.hubmeta))
    def test_nonlibrary_sitemap_entry_change_is_rejected(self):
        xml,_=generate_effective_sitemaps(self.f.registry,prior_xml=self.f.xml,hub_metadata=self.f.hubmeta)
        bad=xml.replace(b'<loc>https://docs.broadcastwell.com/research/record/</loc><lastmod>2026-11-02',b'<loc>https://docs.broadcastwell.com/research/record/</loc><lastmod>2026-11-03')
        with self.assertRaisesRegex(OverlayError,'nonlibrary sitemap'):
            validate_effective_sitemap(self.f.registry,prior_xml=self.f.xml,candidate_xml=bad,hub_metadata=self.f.hubmeta)
    def test_stale_leaf_sitemap_date_rejected(self):
        with self.assertRaisesRegex(OverlayError,'stale metadata dates'):
            validate_effective_sitemap(self.f.registry,prior_xml=self.f.xml,candidate_xml=self.f.xml,hub_metadata=self.f.hubmeta)
    def test_stale_unconsumed_hub_metadata_rejected(self):
        wrong=copy.deepcopy(self.f.hubmeta);wrong['answers/index.md']['description']='Caller claims this changed.'
        with self.assertRaisesRegex(OverlayError,'actual effective hub metadata'):
            generate_effective_sitemaps(self.f.registry,prior_xml=self.f.xml,hub_metadata=wrong)
    def test_unknown_prior_library_removal_requires_merge(self):
        bad=self.f.xml.replace(b'</urlset>',b'<url><loc>https://docs.broadcastwell.com/answers/measurement/lost/</loc><lastmod>2026-11-02</lastmod></url></urlset>')
        with self.assertRaisesRegex(OverlayError,'without reviewed301'):
            generate_effective_sitemaps(self.f.registry,prior_xml=bad,hub_metadata=self.f.hubmeta)
    def test_unknown_derived_artifact_cannot_hide_nonlibrary_change(self):
        with self.assertRaisesRegex(OverlayError,'Unknown derived exclusion'):
            compare_complete_artifacts(prior_files={'research/a.html':b'A'},candidate_files={'research/a.html':b'B'},changed_article_paths=[],changed_hub_paths=[],validated_derived_routes=['/research/a.html'],merged_sources=[],expected_redirect_bytes=None,private_sidecars={})
    def test_full_artifact_compare_rejects_other_manual_or_static_bytes(self):
        with self.assertRaisesRegex(OverlayError,'Unrelated/nonlibrary'):
            compare_complete_artifacts(prior_files={'valid-measurement/index.html':b'A'},candidate_files={'valid-measurement/index.html':b'B'},changed_article_paths=[],changed_hub_paths=[],validated_derived_routes=[],merged_sources=[],expected_redirect_bytes=None,private_sidecars={})
    def test_sitemap_gzip_and_search_deltas_are_explicit(self):
        result=compare_complete_artifacts(prior_files={'sitemap.xml':b'A','sitemap.xml.gz':b'B','search/search_index.json':b'C'},candidate_files={'sitemap.xml':b'D','sitemap.xml.gz':b'E','search/search_index.json':b'F'},changed_article_paths=[],changed_hub_paths=[],validated_derived_routes=['/sitemap.xml','/sitemap.xml.gz','/search/search_index.json'],merged_sources=[],expected_redirect_bytes=None,private_sidecars={})
        self.assertEqual(3,len(result['changed_artifact_paths']))
    def test_caller_fingerprint_does_not_create_consumption_receipt(self):
        self.assertNotIn('llms',self.f.registry.receipts);self.assertNotIn('search',self.f.registry.receipts)
        self.f.overlay.records[self.f.paths[0]]['meta']['description']='Changed after registry.'
        with self.assertRaisesRegex(OverlayError,'registry changed'):
            self.f.registry.receipt('llms',consumed_paths=self.f.paths,outputs={'/llms.txt':b'invented'},proof={})
    def test_actual_page_contexts_bind_head_body_and_metadata(self):
        contexts=self.f.contexts();receipt=validate_page_contexts(self.f.registry,contexts=contexts)
        self.assertEqual(4,len(receipt['output_sha256']));self.assertTrue(receipt['proof']['whole_visible_article_matches_renderer_HTML'])
    def test_stale_social_metadata_rejected(self):
        contexts=self.f.contexts();p=self.f.paths[0]
        contexts[p]['rendered_html']=contexts[p]['rendered_html'].replace(b'name="og:description" content="First dated result."',b'name="og:description" content="Old result."')
        with self.assertRaisesRegex(OverlayError,'social/description'):
            validate_page_contexts(self.f.registry,contexts=contexts)
    def test_rendered_body_cannot_hide_a_source_fact_even_with_matching_context_meta(self):
        contexts=self.f.contexts();p=self.f.paths[0]
        contexts[p]['html']=contexts[p]['html'].replace('First dated result.','Hidden replacement.')
        contexts[p]['rendered_html']=contexts[p]['rendered_html'].replace(b'First dated result.</p>',b'Hidden replacement.</p>')
        with self.assertRaisesRegex(OverlayError,'complete effective Markdown'):
            validate_page_contexts(self.f.registry,contexts=contexts)
    def test_search_matches_actual_pinned_renderer_contexts(self):
        contexts=self.f.contexts();search=self.f.search(contexts)
        validate_effective_search(self.f.registry,prior_bytes=encoded(search),candidate_bytes=encoded(search),actual_page_contexts=contexts)
        self.assertTrue(self.f.registry.receipts['search']['proof']['nonlibrary_rows_exact'])
    def test_search_nonlibrary_entry_change_rejected(self):
        contexts=self.f.contexts();old=self.f.search(contexts);new=copy.deepcopy(old);new['docs'][0]['text']='Changed research.'
        with self.assertRaisesRegex(OverlayError,'Nonlibrary search'):
            validate_effective_search(self.f.registry,prior_bytes=encoded(old),candidate_bytes=encoded(new),actual_page_contexts=contexts)
    def test_caller_supplied_stale_search_html_rejected(self):
        contexts=self.f.contexts();old=self.f.search(contexts);p=self.f.paths[0];contexts[p]['html']=contexts[p]['html'].replace('First dated result.','Old body.')
        with self.assertRaisesRegex(OverlayError,'complete effective Markdown'):
            validate_effective_search(self.f.registry,prior_bytes=encoded(old),candidate_bytes=encoded(old),actual_page_contexts=contexts)


class UtcPriceTests(unittest.TestCase):
    def setUp(self):
        self.offer={'name':'Fix one answer','price':'$490','href':'https://broadcastwell.com/answer-repair'}
        self.method='[Dated method](https://doi.org/10.1234/method)'
        self.body='# Question?\n\nAnswer.\n\n## Next step\n\n'+FREE_CHECK_TOKEN+'. '+LIMIT_SENTENCE+'\n\n'+self.method+'\n\nFix one answer: [$490](https://broadcastwell.com/answer-repair).\n\nPrepared by the Broadcastwell team.\n\nPage owner: Fixture, Analyst. Corrections: hello@broadcastwell.com\n'
        self.overlay=PublicationOverlay();self.overlay.pending=[];self.overlay.receipt_store={}
        self.contract={'method_token':self.method,'free_correction_statement':'','offer':dict(self.offer)}
    def price(self,day):
        raw=encoded(dict(self.offer,approved=True,review_kind='live-offer-price',checked_on=day,checked_on_timezone='UTC'))
        key=sha(raw);self.overlay.receipt_store[key]=raw;self.contract['offer']['live_price_receipt_sha256']=key
    def clock(self):
        class Clock:
            @staticmethod
            def now(tz):
                if tz is not datetime.timezone.utc:raise AssertionError('Must ask the UTC clock, not the Windows local calendar')
                return datetime.datetime(2026,11,3,0,1,tzinfo=datetime.timezone.utc)
        return patch('library_publication_overlay.datetime',Clock)
    def test_utc_day_receipt_accepts_while_indianapolis_is_previous_day(self):
        self.price('2026-11-03')
        with self.clock():self.assertEqual([],neutral_footer_issues(self.overlay,'fixture',{'body':self.body},self.contract));self.assertEqual('2026-11-03',utc_calendar_day())
    def test_previous_utc_day_receipt_stays_stale_without_local_exemption(self):
        self.price('2026-11-02')
        with self.clock():self.assertTrue(neutral_footer_issues(self.overlay,'fixture',{'body':self.body},self.contract))
    def test_future_utc_day_receipt_rejected(self):
        self.price('2026-11-04')
        with self.clock():self.assertTrue(neutral_footer_issues(self.overlay,'fixture',{'body':self.body},self.contract))
    def test_full_overlay_footer_uses_same_utc_contract(self):
        self.price('2026-11-03');a,b=next_step_span(self.body);entry=dict(self.contract,old_next_step_sha256=sha(self.body[a:b].encode()))
        with self.clock():self.overlay._footer('fixture',self.body,entry,[])
        self.assertEqual([],self.overlay.pending)


if __name__=='__main__':unittest.main()
