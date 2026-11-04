"""Pure finite contract tests. Synthetic in-memory approvals are NOT real reads."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import copy,hashlib,json,unittest
from types import SimpleNamespace
O=Path(__file__).resolve().parents[1];sys.path.insert(0,str(O/'tools'))
import library_owner_discovery_consumer_five as m

class Registry:
 def __init__(self,fixture):
  self.records=copy.deepcopy(fixture['records']);self.fingerprint=m.jhash(self.records);self.hubs=copy.deepcopy(fixture['hubs']);self.receipts={'library-hubs':{'synthetic_base_receipt':True}}
 def assert_current(self):
  if m.jhash(self.records)!=self.fingerprint:raise ValueError('Synthetic registry changed')
 def receipt(self,name,**kwargs):self.assert_current();self.receipts[name]=kwargs;return kwargs

class FiveTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.fixture=json.loads((Path(__file__).parent/'fixtures/discovery-consumer-five/actual-public-baseline.json').read_bytes())
  cls.date_raw=(Path(__file__).parent/'fixtures/discovery-consumer-five/actual-root-hub-date-event.json').read_bytes();cls.date=m.checked_hub_date_event(cls.date_raw,m.catalog())
 def case(self):
  f=copy.deepcopy(self.fixture);c=m.catalog();reg=Registry(f);data={'source_changes':{},'baseline_production_binding':{'commit_sha':f['public_before_receipt']['current_production']},
    'generated_hubs':{'docs/'+p:{'effective_body_sha256':n['after_body_sha256'],'effective_meta_sha256':self.date['hub_metadata'][p]['after_meta_sha256']}for p,n in c['hubs'].items()}}
  mem={};refs={}
  def add(k,v):
   raw=(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'))+'\n').encode();ref={'path':k+'.json','sha256':m.sha(raw)};mem[ref['path']]=raw;refs[k]=ref;return ref
  add('plan',f['plan']);data['discovery_consumer_five']={'catalog_sha256':m.CATALOG_SHA256,'plan_sha256':refs['plan']['sha256']}
  for kind,k in [('source','Source_review'),('writing','Writing_review')]:add(k,{'approved':True,'synthetic_test_approval':True,'review_kind':kind,'scope':'owner-exact-discovery-consumer-five','policy':m.POLICY,
    'catalog_sha256':m.CATALOG_SHA256,'consumer_plan_sha256':refs['plan']['sha256'],'complete_hub_before_after_read':True,'five_exact_descriptions_reviewed':True,'leaf_source_metadata_or_ordinary_S5_approval':False})
  add('public_before',f['public_before_receipt'])
  mem['hub_date_event.json']=self.date_raw;refs['hub_date_event']={'path':'hub_date_event.json','sha256':m.HUB_DATE_EVENT_SHA256}
  add('Root_review',{'approved':True,'synthetic_test_approval':True,'reviewer':'root','review_kind':'root-exact-discovery-consumer-five','policy':m.POLICY,
    'owner_source_plan_sha256':'a'*64,'consumer_plan_sha256':refs['plan']['sha256'],'catalog_sha256':m.CATALOG_SHA256,'Source_review_sha256':refs['Source_review']['sha256'],
    'Writing_review_sha256':refs['Writing_review']['sha256'],'actual_public_before_receipt_sha256':refs['public_before']['sha256'],'hub_date_event_sha256':m.HUB_DATE_EVENT_SHA256,'full_two_hub_before_after_actually_read':True,
    'dated_global_consumer_truth_correction_no_field_treatment':True,'leaf_or_frozen_leaf_search_treatment_approval':False,'actual_private_adoption_utc':self.date['actual_private_adoption_utc']})
  def load(ref):
   raw=mem[ref['path']]
   if m.sha(raw)!=ref['sha256']:raise ValueError('Synthetic bound bytes differ')
   return Path(ref['path']),raw
  owner=SimpleNamespace(data=data,freeze_data={'pages':{p:{}for p in f['frozen_paths']}},assert_current=lambda:None)
  kwargs=dict(config={'discovery_consumer_five':refs},load=load,owner_plan=owner,registry=reg,hubs=reg.hubs,frozen_paths=set(f['frozen_paths']),source_plan_sha256='a'*64,
    actual_prior_files={p:b.encode()for p,b in f['actual_prior_three'].items()})
  return f,c,reg,mem,refs,kwargs
 def bind(self):
  x=self.case();obj,hubs=m.bind_consumer_five(**x[-1]);return x,obj,hubs
 def test_exact_five_and_all_other_hub_bytes(self):
  (f,c,reg,_,_,_),obj,hubs=self.bind();self.assertEqual(12,len(hubs));self.assertEqual(reg.records,f['records']);obj.check(hubs)
  for p in set(hubs)-set(c['hubs']):self.assertEqual(hubs[p],f['hubs'][p])
  for p in c['hubs']:
   self.assertEqual(hubs[p]['meta'],self.date['hub_metadata'][p]['after'])
   self.assertEqual({k:v for k,v in hubs[p]['meta'].items()if k!='date_modified'},{k:v for k,v in f['hubs'][p]['meta'].items()if k!='date_modified'})
  after,proof=obj.llms(f['llms_before'].encode());self.assertEqual(c['llms_after_sha256'],m.sha(after));self.assertTrue(proof['exact_inverse_or_actual_contexts'])
 def test_opaque_constructor(self):
  with self.assertRaises((ValueError,TypeError)):m.ConsumerFive(object())
 def test_missing_declared_config_rejects(self):
  *_,kw=self.case();kw['config']={}
  with self.assertRaises(ValueError):m.bind_consumer_five(**kw)
 def test_unapproved_root_rejects(self):
  *_,kw=self.case();refs=kw['config']['discovery_consumer_five'];old=kw['load']
  def load(ref):
   p,b=old(ref)
   if ref==refs['Root_review']:d=json.loads(b);d['approved']=False;b=json.dumps(d).encode()
   return p,b
  kw['load']=load
  with self.assertRaises(ValueError):m.bind_consumer_five(**kw)
 def test_wrong_source_scope_rejects(self):
  *_,kw=self.case();refs=kw['config']['discovery_consumer_five'];old=kw['load']
  def load(ref):
   p,b=old(ref)
   if ref==refs['Source_review']:d=json.loads(b);d['scope']='full-effective-article';b=json.dumps(d).encode()
   return p,b
  kw['load']=load
  with self.assertRaises(ValueError):m.bind_consumer_five(**kw)
 def test_wrong_leaf_metadata_rejects(self):
  _,c,reg,_,_,kw=self.case();reg.records[c['rows'][0]['leaf_path']]['meta']['description']='New leaf metadata is forbidden'
  with self.assertRaises(ValueError):m.bind_consumer_five(**kw)
 def test_wrong_frozen_set_rejects(self):
  *_,kw=self.case();kw['frozen_paths'].remove(next(iter(kw['frozen_paths'])))
  with self.assertRaises(ValueError):m.bind_consumer_five(**kw)
 def test_extra_hub_card_change_rejects(self):
  f,c,*_=self.case();h=copy.deepcopy(f['hubs']);h['answers/fixes/index.md']['body']+='\nForeign nav.\n'
  with self.assertRaises(ValueError):m.project_hubs(h,c)
 def test_wrong_hub_date_rejects(self):
  f,c,*_=self.case();h=copy.deepcopy(f['hubs']);h['answers/fixes/index.md']['meta']['date_modified']='2099-01-01'
  with self.assertRaises(ValueError):m.project_hubs(h,c)
 def test_wrong_actual_date_event_bytes_rejects(self):
  d=json.loads(self.date_raw);d['actual_private_adoption_utc']='2099-01-01T00:00:00+00:00'
  with self.assertRaises(ValueError):m.checked_hub_date_event(json.dumps(d).encode(),m.catalog())
 def test_missing_date_event_ref_rejects(self):
  *_,kw=self.case();kw['config']['discovery_consumer_five'].pop('hub_date_event')
  with self.assertRaises(ValueError):m.bind_consumer_five(**kw)
 def test_original_date_applied_only_once_and_unrelated_meta_preserved(self):
  f,c,*_=self.case();h=m.project_hubs(f['hubs'],c,self.date)
  for p in c['hubs']:
   self.assertEqual(h[p]['meta'],self.date['hub_metadata'][p]['after'])
   inverse={**h[p]['meta'],'date_modified':self.date['hub_metadata'][p]['before']['date_modified']}
   self.assertEqual(inverse,f['hubs'][p]['meta'])
 def test_llms_other_line_change_rejects(self):
  f,c,*_=self.case()
  with self.assertRaises(ValueError):m.project_llms(f['llms_before'].encode()+b'\nforeign',c)
 def test_llms_missing_target_rejects(self):
  f,c,*_=self.case();old=c['rows'][0]['old_llms_line']
  with self.assertRaises(ValueError):m.project_llms(f['llms_before'].replace(old,'missing').encode(),c)
 def test_current_public_before_wrong_path_rejects(self):
  *_,kw=self.case();old=kw['load'];ref=kw['config']['discovery_consumer_five']['public_before']
  def load(r):
   p,b=old(r)
   if r==ref:d=json.loads(b);d['rows'][0]['path']='foreign';b=json.dumps(d).encode()
   return p,b
  kw['load']=load
  with self.assertRaises(ValueError):m.bind_consumer_five(**kw)
 def test_current_public_before_actual_bytes_reject(self):
  *_,kw=self.case();kw['actual_prior_files']['llms.txt']=b'foreign'
  with self.assertRaises(ValueError):m.bind_consumer_five(**kw)
 def test_no_later_leaf_or_hub_mutation(self):
  (f,c,reg,_,_,_),obj,hubs=self.bind();reg.records[next(iter(reg.records))]['meta']['description']='foreign'
  with self.assertRaises(ValueError):obj.check(hubs)
 def test_no_later_unrelated_hub_mutation(self):
  (_,_,reg,_,_,_),obj,hubs=self.bind();hubs['answers/buying/index.md']['body']+='foreign'
  with self.assertRaises(ValueError):obj.check(hubs)
 def test_actual_baseline45_search_rows_byte_exact(self):
  f=self.fixture;self.assertTrue(m.frozen_search_exact(f['search_before'].encode(),f['search_owner_base'].encode(),set(f['frozen_paths'])))
 def test_frozen_search_changed_value_rejects(self):
  f=self.fixture;raw=f['search_owner_base'].encode();p=f['frozen_paths'][0].removesuffix('.md')+'/'
  row,fragment=next((r,b)for r,b in m._search_rows(raw)if r['location'].split('#')[0]==p);changed=dict(row,text=row['text']+'foreign')
  after=raw.replace(fragment,json.dumps(changed,separators=(',',':')).encode(),1)
  with self.assertRaises(ValueError):m.frozen_search_exact(f['search_before'].encode(),after,set(f['frozen_paths']))
 def test_frozen_search_same_object_different_raw_bytes_rejects(self):
  f=self.fixture;raw=f['search_owner_base'].encode();p=f['frozen_paths'][0].removesuffix('.md')+'/'
  _,fragment=next((r,b)for r,b in m._search_rows(raw)if r['location'].split('#')[0]==p)
  after=raw.replace(fragment,fragment.replace(b'{',b'{ ',1),1)
  with self.assertRaises(ValueError):m.frozen_search_exact(f['search_before'].encode(),after,set(f['frozen_paths']))
 def test_missing_search_rows_both_sides_rejects(self):
  with self.assertRaises(ValueError):m.frozen_search_exact(b'{"docs":[]}',b'{"docs":[]}',set(self.fixture['frozen_paths']))
 def test_hub_only_search_change_does_not_change_frozen_leaf_rows(self):
  f=self.fixture;raw=f['search_owner_base'].encode();row,fragment=next((r,b)for r,b in m._search_rows(raw)if r['location']=='answers/fixes/')
  changed=dict(row,text=row['text']+' Synthetic allowed hub-only derived content.');after=raw.replace(fragment,json.dumps(changed,separators=(',',':')).encode(),1)
  self.assertTrue(m.frozen_search_exact(f['search_before'].encode(),after,set(f['frozen_paths'])))

if __name__=='__main__':unittest.main(verbosity=2)
