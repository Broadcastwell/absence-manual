"""Actual prior public files, synthetic finite declarations, no approvals."""
from pathlib import Path
import copy,sys,unittest
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE/'tools'))
import library_owner_repair as p
import library_owner_repair_six_facts as s
import test_owner_repair_four_facts as four_tests


class SixFactTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  import library_publication_build
  repo=Path(library_publication_build.__file__).resolve().parent.parent
  cls.files={u.removeprefix(p.SITE):(repo/'docs'/u.removeprefix(p.SITE)).read_bytes() for u in s.URLS};cls.pins={p.SITE+path:p.sha(raw) for path,raw in cls.files.items()}
 def fixture(self):
  reg=four_tests.FourFactTests.fixture(self)
  calc={'membership_filter':{'scope':'target'},'membership_unique_key':'url_id','base_predicates':{'fetched_html':'True'},'count_predicates':{'json_ld':'True'},'membership_file':'study1-citation-membership.csv','observation_file':'study1-url-classifications.csv','distinct_membership_ids':5861,'count':3616,'base':4420,'frozen_field_definition':'At least one nonempty parsed JSON object or array; not vocabulary validation. Parse failure on another script can coexist.'}
  reg[s.JSON_ID]={'source_kind':'published-study','numeric_cut':True,'count':3616,'base':4420,'observed_at':'2026-10-30','source_url':p.SITE+'research/data/study1-url-classifications.csv','public_text':self.files['research/data/study1-url-classifications.csv'].decode('utf-8-sig').splitlines()[0],'inputs':[{'source_url':p.SITE+'research/data/'+n,'sha256':self.pins[p.SITE+'research/data/'+n]} for n in ['study1-citation-membership.csv','study1-url-classifications.csv','collect_page_signals.py']],'calculation_kind':'owner-authorized-public-row-aggregate','published_aggregate':False,'aggregate_quote_exists_in_prior_publication':False,'calculation':calc}
  reg[s.EMPTY_ID]={'source_kind':'published-study','numeric_cut':True,'count':39,'base':2095,'observed_at':'2026-09-22 through2026-09-23','source_url':p.SITE+'research/data/answer-citation-bases.csv','public_text':'target,all,all,2095,39,1.8616,1.3648,2.5346,18893','inputs':[{'source_url':p.SITE+'research/data/answer-citation-bases.csv','sha256':self.pins[p.SITE+'research/data/answer-citation-bases.csv']}],'calculation_kind':'existing-published-aggregate-row','published_aggregate':True}
  return reg
 def test_actual_six_distinct_facts_recompute_without_new_measurement(self):
  r=s.validate_six_public_facts(self.fixture(),actual_prior_files=self.files,root_source_url_pins=self.pins)
  self.assertTrue(r['all_six_exact']);self.assertEqual(3616,r['json_ld_derived_count']);self.assertEqual(39,r['empty_list_count']);self.assertFalse(r['json_ld_vocabulary_validation_claimed'])
 def test_wrong_json_ld_cut_definition_or_predicates_reject(self):
  for mode in ['count','definition','predicate','preprinted']:
   reg=self.fixture();r=reg[s.JSON_ID]
   if mode=='count':r['count']=1
   elif mode=='definition':r['calculation']['frozen_field_definition']='Validated schema vocabulary.'
   elif mode=='predicate':r['calculation']['count_predicates']['json_ld_parse_failure']='False'
   else:r['published_aggregate']=True
   with self.assertRaises(p.RepairError):s.validate_six_public_facts(reg,actual_prior_files=self.files,root_source_url_pins=self.pins)
 def test_empty_lists_must_not_be_scheduled_answers_or_wrong_date(self):
  for key,value in [('base',2100),('count',1),('observed_at','2026-11-03')]:
   reg=self.fixture();reg[s.EMPTY_ID][key]=value
   with self.assertRaises(p.RepairError):s.validate_six_public_facts(reg,actual_prior_files=self.files,root_source_url_pins=self.pins)
 def test_missing_classifier_source_or_extra_fact_rejects(self):
  for mode in ['classifier','newfact']:
   reg=self.fixture()
   if mode=='classifier':reg[s.JSON_ID]['inputs'].pop()
   else:reg['invented-fact']=copy.deepcopy(reg[s.EMPTY_ID])
   with self.assertRaises(p.RepairError):s.validate_six_public_facts(reg,actual_prior_files=self.files,root_source_url_pins=self.pins)


if __name__=='__main__':unittest.main()
