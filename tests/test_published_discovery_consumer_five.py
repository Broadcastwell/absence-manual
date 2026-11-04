"""Pure actual-data tests. Future approval objects are synthetic IN MEMORY ONLY."""
import copy,importlib.util,json,pathlib,re,sys,unittest
from types import SimpleNamespace
import yaml
sys.dont_write_bytecode=True
O=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(O/'tools'))
import library_published_discovery_consumer_five as m

def source(full):
    match=re.match(r'\A---\n(.*?)\n---\n',full,re.S)
    return yaml.safe_load(match[1]),full[match.end():].lstrip('\n')
def raw(v):return (json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'))+'\n').encode()
class Registry:
    def __init__(self,f,store):
        self.records=copy.deepcopy(f['records']);self.hubs=copy.deepcopy(f['hubs']);self.fingerprint=m.jhash(self.records)
        self.receipts={'library-hubs':{'synthetic_base_receipt':True},'llms':{'synthetic_normal_llms_receipt':True}}
        self.overlay=SimpleNamespace(_load_receipt=lambda key:store[key],finite=SimpleNamespace(source_body=source))
    def assert_current(self):
        if self.fingerprint!=m.jhash(self.records):raise ValueError('Synthetic registry changed')
    def receipt(self,name,**kwargs):self.assert_current();self.receipts[name]=kwargs;return kwargs
class PublishedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        core=pathlib.Path(__file__).parent/'fixtures/discovery-consumer-five/actual-public-baseline.json'
        cls.f=json.loads(core.read_bytes());cls.p=pathlib.Path(__file__).parent/'fixtures/published-consumer-five'
        cls.date_raw=(pathlib.Path(__file__).parent/'fixtures/discovery-consumer-five/actual-root-hub-date-event.json').read_bytes();cls.date=m.checked_hub_date_event(cls.date_raw,m.catalog())
    def case(self):
        f=copy.deepcopy(self.f);c=m.catalog();store={}
        def put(v):
            b=v if isinstance(v,bytes)else raw(v);k=m.sha(b);store[k]=b;return k
        plan=put((self.p/'plan.json').read_bytes());self.assertEqual(m.PLAN,plan)
        self.assertEqual(m.SOURCE,put((self.p/'source-peer.json').read_bytes()));self.assertEqual(m.WRITING,put((self.p/'writing-peer.json').read_bytes()))
        before=put(f['public_before_receipt']);self.assertEqual(m.HUB_DATE_EVENT_SHA256,put(self.date_raw))
        owner={'approved':True,'synthetic_test_approval':True,'kind':m.POLICY,'review_kind':'root-exact-owner-repair-source-plan','article_count':307,
            'source_changes':{'synthetic-test-source-'+str(i):{}for i in range(49)},'baseline_production_binding':{'commit_sha':f['public_before_receipt']['current_production']},
            'discovery_consumer_five':{'catalog_sha256':m.CATALOG_SHA256,'plan_sha256':m.PLAN},
            'generated_hubs':{'docs/'+p:{'effective_body_sha256':r['after_body_sha256'],'effective_meta_sha256':self.date['hub_metadata'][p]['after_meta_sha256']}for p,r in c['hubs'].items()}}
        owner_id=put(owner)
        root={'approved':True,'synthetic_test_approval':True,'reviewer':'root','review_kind':'root-exact-discovery-consumer-five','policy':m.POLICY,
            'catalog_sha256':m.CATALOG_SHA256,'consumer_plan_sha256':m.PLAN,'owner_source_plan_sha256':owner_id,'Source_review_sha256':m.SOURCE,'Writing_review_sha256':m.WRITING,
            'actual_public_before_receipt_sha256':before,'hub_date_event_sha256':m.HUB_DATE_EVENT_SHA256,'full_two_hub_before_after_actually_read':True,'dated_global_consumer_truth_correction_no_field_treatment':True,
            'leaf_or_frozen_leaf_search_treatment_approval':False,'actual_private_adoption_utc':'2099-01-01T00:00:00+00:00'}
        root_id=put(root);reg=Registry(f,store);after=m.project_hubs(f['hubs'],c,self.date);prior={'schema_version':1,'hubs':{}}
        for p,row in after.items():
            full='---\n'+yaml.safe_dump(row['meta'],sort_keys=False,allow_unicode=True)+'---\n\n'+row['body']
            prior['hubs'][p]={**copy.deepcopy(row),'effective_full_source':full,'canonical_source_sha256':m.sha(full.encode()),'raw_canonical_source_sha256':'a'*64}
        llms=m.project_llms(f['llms_before'].encode(),c);files={'llms.txt':llms}
        frozen=set(f['frozen_paths']);inputs={'actual_prior_production_binding':{'synthetic_test_only':True},'frozen_effective_pins':{p:m.sha(reg.records[p]['effective_full_source'].encode())for p in frozen}}
        declaration={'schema_version':1,'policy':m.KIND,'catalog_sha256':m.CATALOG_SHA256,'consumer_plan_sha256':m.PLAN,'Root_review_sha256':root_id,
            'Source_review_sha256':m.SOURCE,'Writing_review_sha256':m.WRITING,'historical_public_before_sha256':before,'owner_source_plan_sha256':owner_id,
            'published_hub_tuples':m.expected_tuples(c,self.date),'hub_date_event_sha256':m.HUB_DATE_EVENT_SHA256,'published_llms_sha256':c['llms_after_sha256']}
        producer={'approved':True,'synthetic_test_approval':True,'review_kind':'prior-production-effective-payload','production_binding':inputs['actual_prior_production_binding'],
            'actual_served_readback':True,'source_render_equality_passed':True,'hub_source_render_equality_passed':True,'hub_payload_bundle_sha256':m.sha(raw(prior)),
            'hub_payload_canonical_json_sha256':m.jhash(prior),'hub_raw_source_git_proof_passed':True,'hub_raw_source_pins':{p:r['raw_canonical_source_sha256']for p,r in prior['hubs'].items()},m.KEY:declaration}
        kwargs=dict(producer_raw=raw(producer),inputs=inputs,registry=reg,hubs=reg.hubs,prior_hub_bundle=prior,prior_hub_file_sha256=m.sha(raw(prior)),actual_prior_archive=SimpleNamespace(read=lambda p:files[p]),frozen_paths=frozen)
        return f,store,reg,producer,kwargs
    def reject(self,edit):
        f,store,reg,p,k=self.case();edit(f,store,reg,p,k);k['producer_raw']=raw(p)
        with self.assertRaises((ValueError,KeyError)):m.bind_published_discovery_five(**k)
    def test_published_exact_replay_then_llms_and_leaf_identity(self):
        f,s,r,p,k=self.case();obj,hubs=m.bind_published_discovery_five(**k)
        self.assertEqual(r.records,f['records']);self.assertEqual(r.hubs,hubs);self.assertEqual(12,len(hubs));obj.check()
        llms,proof=obj.llms(f['llms_before'].encode());self.assertEqual(m.catalog()['llms_after_sha256'],m.sha(llms))
        self.assertEqual(r.receipts['llms']['outputs']['/llms.txt'],llms)
    def test_actual_PR93_and_current_Owner_baseline_dormant_identity(self):
        f,s,r,p,k=self.case();k['producer_raw']=(self.p/'actual-PR93-producer-public-projection.json').read_bytes()
        k['prior_hub_bundle']=json.loads((self.p/'actual-PR93-prior-hub-payload.json').read_bytes())
        k['actual_prior_archive']=SimpleNamespace(read=lambda p:f['actual_prior_three'][p].encode())
        before=copy.deepcopy(r.hubs);records=copy.deepcopy(r.records);receipts=copy.deepcopy(r.receipts)
        obj,hubs=m.bind_published_discovery_five(**k)
        self.assertIsNone(obj);self.assertIs(hubs,k['hubs']);self.assertEqual(before,r.hubs);self.assertEqual(records,r.records);self.assertEqual(receipts,r.receipts)
        session=SimpleNamespace(published_consumer5=obj);m.seal_published_binding(session,k['producer_raw'])
        self.assertIsNone(m.checked_published_binding(session));self.assertEqual(before,r.hubs)
    def test_declaration_downgrade_rejected(self):self.reject(lambda f,s,r,p,k:p.pop(m.KEY))
    def test_false_producer_rejected(self):self.reject(lambda f,s,r,p,k:p.update(approved=False))
    def test_partial_declaration_rejected(self):self.reject(lambda f,s,r,p,k:p[m.KEY].pop('policy'))
    def test_foreign_binding_rejected(self):self.reject(lambda f,s,r,p,k:p.update(production_binding={'foreign':True}))
    def test_foreign_catalog_rejected(self):self.reject(lambda f,s,r,p,k:p[m.KEY].update(catalog_sha256='0'*64))
    def test_missing_authority_rejected(self):self.reject(lambda f,s,r,p,k:s.pop(p[m.KEY]['Root_review_sha256']))
    def test_false_Root_authority_with_coherent_store_digest_rejected(self):
        def edit(f,s,r,p,k):
            root=json.loads(s[p[m.KEY]['Root_review_sha256']]);root['approved']=False
            b=raw(root);s[m.sha(b)]=b;p[m.KEY]['Root_review_sha256']=m.sha(b)
        self.reject(edit)
    def test_foreign_Source_peer_rejected(self):self.reject(lambda f,s,r,p,k:p[m.KEY].update(Source_review_sha256=m.WRITING))
    def test_shortened_prior_hub_rejected(self):self.reject(lambda f,s,r,p,k:k['prior_hub_bundle']['hubs']['answers/fixes/index.md'].update(body='short'))
    def test_stale_whole_hub_bundle_digest_rejected(self):self.reject(lambda f,s,r,p,k:p.update(hub_payload_canonical_json_sha256='0'*64))
    def test_unproven_raw_Git_tuple_rejected(self):self.reject(lambda f,s,r,p,k:p.update(hub_raw_source_git_proof_passed=False))
    def test_stale_full_hub_source_rejected(self):self.reject(lambda f,s,r,p,k:k['prior_hub_bundle']['hubs']['answers/fixes/index.md'].update(effective_full_source='foreign'))
    def test_no_new_hub_timestamp_rejected(self):self.reject(lambda f,s,r,p,k:r.hubs['answers/fixes/index.md']['meta'].update(date_modified='2099-01-01'))
    def test_normal_original_after_metadata_retains_original_adoption_date(self):
        f,s,r,p,k=self.case()
        for hub,note in self.date['hub_metadata'].items():r.hubs[hub]['meta']=copy.deepcopy(note['after'])
        obj,hubs=m.bind_published_discovery_five(**k);obj.check()
        for hub,note in self.date['hub_metadata'].items():self.assertEqual(hubs[hub]['meta'],note['after'])
    def test_foreign_or_refreshed_date_event_rejected(self):self.reject(lambda f,s,r,p,k:p[m.KEY].update(hub_date_event_sha256='0'*64))
    def test_extra_hub_card_rejected(self):self.reject(lambda f,s,r,p,k:r.hubs['answers/fixes/index.md'].update(body=r.hubs['answers/fixes/index.md']['body']+'foreign'))
    def test_unrelated_current_hub_change_rejected(self):self.reject(lambda f,s,r,p,k:r.hubs['answers/buying/index.md'].update(body=r.hubs['answers/buying/index.md']['body']+'foreign'))
    def test_leaf_metadata_change_rejected(self):self.reject(lambda f,s,r,p,k:r.records[m.catalog()['rows'][0]['leaf_path']]['meta'].update(description='foreign'))
    def test_missing_frozen_identity_rejected(self):self.reject(lambda f,s,r,p,k:k['frozen_paths'].remove(next(iter(k['frozen_paths']))))
    def test_wrong_published_llms_rejected(self):
        self.reject(lambda f,s,r,p,k:k.update(actual_prior_archive=SimpleNamespace(read=lambda p:b'foreign')))
    def test_opaque_constructor_rejected(self):
        with self.assertRaises((TypeError,ValueError)):m.PublishedConsumerFive(object(),None,{},set())
    def test_no_double_application_or_unrelated_llms_change(self):
        f,s,r,p,k=self.case();obj,hubs=m.bind_published_discovery_five(**k);after,_=obj.llms(f['llms_before'].encode())
        with self.assertRaises(ValueError):obj.llms(after)
        with self.assertRaises(ValueError):obj.llms(f['llms_before'].encode()+b'foreign')
    def test_no_later_leaf_mutation(self):
        f,s,r,p,k=self.case();obj,hubs=m.bind_published_discovery_five(**k);r.records[next(iter(r.records))]['body']+='foreign'
        with self.assertRaises(ValueError):obj.check()
    def test_no_later_hub_mutation(self):
        f,s,r,p,k=self.case();obj,hubs=m.bind_published_discovery_five(**k);r.hubs['answers/buying/index.md']['body']+='foreign'
        with self.assertRaises(ValueError):obj.check()
    def test_declared_but_binding_removed_rejected(self):
        f,s,r,p,k=self.case();obj,_=m.bind_published_discovery_five(**k)
        session=SimpleNamespace(published_consumer5=obj);m.seal_published_binding(session,k['producer_raw'])
        session.published_consumer5=None
        with self.assertRaises(ValueError):m.checked_published_binding(session)
    def test_declared_binding_replacement_rejected(self):
        f,s,r,p,k=self.case();obj,_=m.bind_published_discovery_five(**k)
        session=SimpleNamespace(published_consumer5=obj);m.seal_published_binding(session,k['producer_raw'])
        session.published_consumer5=copy.copy(obj)
        with self.assertRaises(ValueError):m.checked_published_binding(session)
    def test_load_seal_removal_rejected(self):
        f,s,r,p,k=self.case();obj,_=m.bind_published_discovery_five(**k)
        session=SimpleNamespace(published_consumer5=obj);m.seal_published_binding(session,k['producer_raw'])
        del session._published_consumer5_load_seal
        with self.assertRaises(ValueError):m.checked_published_binding(session)
if __name__=='__main__':unittest.main(verbosity=2)
