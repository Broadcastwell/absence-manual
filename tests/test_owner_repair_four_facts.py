"""Actual existing public CSV bytes, synthetic record declarations only."""
from pathlib import Path
import copy,sys,unittest
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE/'tools'))
import library_owner_repair as p
import library_owner_repair_four_facts as f


class FourFactTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  import library_publication_build
  repo=Path(library_publication_build.__file__).resolve().parent.parent
  cls.files={'research/data/'+name:(repo/'docs/research/data'/name).read_bytes() for name in f.FILES}
  cls.pins={p.SITE+path:p.sha(raw) for path,raw in cls.files.items()}
 def fixture(self):
  primary={'canonical-presence-target-urls':'study1-url-classifications.csv','classification-sensitivity':'citation-class-shares-post-audit.csv','llms-presence-origins':'study1-llms-presence.csv','rovira-own-reanalysis':'rovira-workbook-reanalysis.csv'}
  reg={}
  for key,(count,base) in f.EXPECTED.items():
   url=p.SITE+'research/data/'+primary[key]
   reg[key]={'source_kind':'published-study','numeric_cut':True,'count':count,'base':base,'observed_at':'2026-10-30','source_url':url,'public_text':self.files['research/data/'+primary[key]].decode('utf-8-sig').splitlines()[0],'inputs':[{'source_url':p.SITE+'research/data/'+n,'sha256':self.pins[p.SITE+'research/data/'+n]} for n in sorted(f.INPUTS[key])],'published_aggregate':True,'calculation_kind':'existing-published-finite-workbook-reanalysis' if key=='rovira-own-reanalysis' else 'existing-published-aggregate-row'}
  r=reg['canonical-presence-target-urls'];r.update(calculation_kind='owner-authorized-public-row-aggregate',published_aggregate=False,aggregate_quote_exists_in_prior_publication=False,calculation={'membership_filter':{'scope':'target'},'membership_unique_key':'url_id','base_predicates':{'fetched_html':'True'},'count_predicates':{'canonical':'True'},'membership_file':'study1-citation-membership.csv','observation_file':'study1-url-classifications.csv','distinct_membership_ids':5861,'count':4179,'base':4420})
  return reg
 def test_actual_csv_recomputes_four_distinct_correct_units(self):
  out=f.validate_four_public_facts(self.fixture(),actual_prior_files=self.files,root_source_url_pins=self.pins)
  self.assertEqual(4179,out['canonical_derived_count']);self.assertEqual(4420,out['canonical_derived_base']);self.assertFalse(out['canonical_claimed_preprinted'])
 def test_wrong_primary_hash_or_extra_url_rejects(self):
  for mode in ['hash','extra']:
   pins=copy.deepcopy(self.pins)
   if mode=='hash':pins[next(iter(pins))]='0'*64
   else:pins['https://docs.broadcastwell.com/research/data/unapproved.csv']='0'*64
   with self.assertRaises(p.RepairError):f.validate_four_public_facts(self.fixture(),actual_prior_files=self.files,root_source_url_pins=pins)
 def test_wrong_count_base_date_sourcekind_or_fake_preprinted_aggregate_rejects(self):
  for key,value in [('count',1),('base',5861),('observed_at','2026-11-03'),('source_kind','private-watch'),('published_aggregate',True),('aggregate_quote_exists_in_prior_publication',True)]:
   reg=self.fixture();reg['canonical-presence-target-urls'][key]=value
   with self.subTest(key=key),self.assertRaises(p.RepairError):f.validate_four_public_facts(reg,actual_prior_files=self.files,root_source_url_pins=self.pins)
 def test_wrong_aggregate_join_or_omitted_input_rejects(self):
  for mode in ['scope','predicate','input']:
   reg=self.fixture();r=reg['canonical-presence-target-urls']
   if mode=='scope':r['calculation']['membership_filter']={'scope':'combined'}
   elif mode=='predicate':r['calculation']['base_predicates']={}
   else:r['inputs'].pop()
   with self.assertRaises(p.RepairError):f.validate_four_public_facts(reg,actual_prior_files=self.files,root_source_url_pins=self.pins)
 def test_llms_origin_selector_cannot_omit_or_substitute_url_unit(self):
  rows=[{'scope':'target','unit':'distinct final origin','count':'774'},{'scope':'target','unit':'URL','count':'2141'}]
  with self.assertRaises(p.RepairError):f.unique(rows,scope='target')
  self.assertEqual('774',f.unique(rows,scope='target',unit='distinct final origin')['count'])


if __name__=='__main__':unittest.main()
