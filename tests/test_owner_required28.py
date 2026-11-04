"""Synthetic approvals/dates only; actual selected before/body data is read-only.

No Root receipt, actual future307 producer or final43 source is minted here.
"""
from pathlib import Path
import copy,json,sys,unittest
from types import SimpleNamespace
from unittest.mock import patch
import yaml
REPO=Path(__file__).resolve().parents[1]
HERE=REPO/'tests/fixtures/owner_required28'
sys.path.insert(0,str(REPO/'tools'))
import library_owner_repair as p
import library_owner_repair_required28 as x
from library_owner_repair_consumers import json_hash,repair_ledger,validate_peer
import library_related_chapter_links as finite

FIXTURE_DATE='2099-01-01T00:00:00+00:00'
raw=lambda d:json.dumps(d,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()

def fixture(path=None):
    catalog=x.load_catalog();path=path or next(iter(catalog['cases']));spec=catalog['cases'][path]
    refs=json.loads((HERE/'before_manifest.json').read_bytes())['rows'][path]
    f=HERE/refs['before']['path'];data=f.read_bytes()
    assert p.sha(data)==refs['before']['sha256'],'Published before fixture changed'
    a=finite.canonical_source(data);am,ab=finite.source_body(a)
    before={'effective_full_source':a,'meta':am,'body':ab}
    body=p.exact_edits(ab.encode(),spec['body_edits']).decode()
    meta=copy.deepcopy(spec['selected_proposed_metadata']);meta['date_modified']=FIXTURE_DATE
    if path.startswith('research/') and 'updated' in meta:meta['updated']=FIXTURE_DATE
    full='---\n'+yaml.safe_dump(meta,sort_keys=False,allow_unicode=True)+'---\n\n'+body
    record={'path':path,'raw_canonical_source_sha256':'a'*64,'before_effective_canonical_source_sha256':spec['before_effective_sha256'],'effective_full_source':full,'body':body,'meta':meta}
    ledger=repair_ledger(path,before,full,spec['body_edits'],meta)
    proof={'approved':True,'review_kind':'source','scope':'source-owner-repair-record-reading' if spec['class']=='rule4_record_reading' else 'source-owner-repair-specific-precision',
      'policy':p.POLICY,'path':path,'bank_id':spec['bank_id'],'source_packet_sha256':spec['source_packet_sha256'],'source_evidence_anchor_sha256':spec['source_evidence_anchor_sha256'],'source_family':spec['source_family'],
      'canonical_source_sha256':'a'*64,'before_effective_canonical_source_sha256':spec['before_effective_sha256'],'effective_canonical_source_sha256':p.sha(full.encode()),'effective_body_sha256':p.sha(body.encode()),'effective_meta_sha256':json_hash(meta),
      'repair_change_ledger_sha256':json_hash(ledger),'current_scoped_Source_receipt_sha256':'b'*64,
      'specific_source_truth_and_narrow_fit_approved':True,'new_measurement':False,'introduced_numeric_cut':False,'ordinary_full_article_approval':False,
      'numeric_cut':False if spec['class']=='rule4_record_reading' else None,'count':None,'base':None,'new_lead_observation_ids':[],
      'record_membership_and_quoted_context_independently_checked':True,'source_public_URLs':spec['exact_public_urls'],
      'exact_new_reading_literals':[e['new'] for e in spec['body_edits']]}
    return record,before,ledger,spec,proof

def run_case(f):
    record,before,ledger,spec,proof=f;r=raw(proof)
    return x.validate_case(record,before=before,ledger=ledger,kind=spec['class'],bank_ids={record['path']:spec['bank_id']},actual_adoption_utc=FIXTURE_DATE,source_proof_raw=r,source_proof_sha256=p.sha(r),current_source_peer_sha256='b'*64)

class Finite28Tests(unittest.TestCase):
    def test_all28_selected_actual_literal_bodies_positive_only_synthetic_future_proof(self):
        c=x.load_catalog()['cases'];self.assertEqual(28,len(c))
        for path in c:
            with self.subTest(path=path):
                result=run_case(fixture(path));self.assertTrue(result['exact_inverse']);self.assertFalse(result['ordinary_S5_PASS_granted'])
    def test_internal_catalog_tamper_and_exact_counts_reject(self):
        with patch.object(Path,'read_bytes',return_value=b'{}'),self.assertRaises(p.RepairError):x.load_catalog()
    def test_no_local_paths_or_implementation_asset_or_new_leadkeys(self):
        blob=x.CATALOG_PATH.read_text();self.assertNotIn('C:\\',blob);self.assertNotIn('file://',blob)
        self.assertEqual([],x.load_catalog()['new_lead_observation_ids'])
        self.assertFalse((HERE/'docs').exists())
    def test_offlist_wrongkind_wrongbank_and_frozen_reject(self):
        path=next(iter(x.load_catalog()['cases']));s=x.load_catalog()['cases'][path]
        for testpath,kind,ids in [('answers/x/other.md',s['class'],{}),(path,'rule4_fact',{path:s['bank_id']}),(path,s['class'],{path:'LB-Q9999'})]:
            with self.subTest(path=testpath,kind=kind),self.assertRaises(p.RepairError):x.validate_named_case(testpath,kind,ids)
        with self.assertRaises(p.RepairError):p.validate_source_class('docs/'+path,{'class':s['class']},answer_paths={path},research_paths=set(),bank_ids={path:s['bank_id']},frozen_sources={path})
    def test_actual_before_effective_body_meta_cannot_be_replaced(self):
        for field in ['effective_full_source','body','meta']:
            f=fixture();f[1][field]='changed' if field!='meta' else {}
            with self.subTest(field=field),self.assertRaises(p.RepairError):run_case(f)
    def test_after_body_number_quote_date_and_outside_change_reject(self):
        for suffix in [' altered count1',' wrong quote',' on1January1900',' unrelated new advice']:
            f=fixture();f[0]['body']+=suffix
            with self.subTest(suffix=suffix),self.assertRaises(p.RepairError):run_case(f)
    def test_exact_ledger_segmentation_and_quote_reject(self):
        for key in ['old','new','old_sha256','new_sha256']:
            f=fixture();f[2]['body_edits']=copy.deepcopy(f[2]['body_edits']);f[2]['body_edits'][0][key]+='tamper'
            with self.subTest(key=key),self.assertRaises(p.RepairError):run_case(f)
    def test_metadata_union_and_published_fields_and_date_cannot_drift(self):
        for key in ['description','date_published','evidence_kind','date_modified']:
            f=fixture();f[0]['meta'][key]='changed'
            with self.subTest(key=key),self.assertRaises(p.RepairError):run_case(f)
        for s in x.load_catalog()['cases'].values():
            if s['metadata_union']:self.assertIn('description',s['selected_proposed_metadata'])
    def test_wrong_source_hash_missing_unapproved_kind_path_source_peer_and_anchor_reject(self):
        for key,val in [('approved',False),('review_kind','writing'),('scope','source-published-owner-repair-facts'),('path','answers/x/other.md'),('source_packet_sha256','c'*64),('source_evidence_anchor_sha256','c'*64),('current_scoped_Source_receipt_sha256','c'*64),('canonical_source_sha256','c'*64)]:
            f=fixture();f[4][key]=val
            with self.subTest(key=key),self.assertRaises(p.RepairError):run_case(f)
        f=fixture();r=raw(f[4])
        with self.assertRaises(p.RepairError):x.validate_case(f[0],before=f[1],ledger=f[2],kind=f[3]['class'],bank_ids={f[0]['path']:f[3]['bank_id']},actual_adoption_utc=FIXTURE_DATE,source_proof_raw=r,source_proof_sha256='0'*64,current_source_peer_sha256='b'*64)
    def test_fake_numeric_cut_one_or_new_observation_reject(self):
        for key,value in [('numeric_cut',True),('count',1),('base',1),('new_lead_observation_ids',['new-fake-fact']),('introduced_numeric_cut',True),('new_measurement',True)]:
            f=fixture();f[4][key]=value
            with self.subTest(key=key),self.assertRaises(p.RepairError):run_case(f)
    def test_url_wildcard_and_identity_relabel_and_absent_membership_reject(self):
        for key,value in [('source_public_URLs',['https://*.zenodo.org/']),('source_family','new-family-to-evade-count'),('record_membership_and_quoted_context_independently_checked',False)]:
            f=fixture();f[4][key]=value
            with self.subTest(key=key),self.assertRaises(p.RepairError):run_case(f)
    def test_source_wrong_quote_date_or_unit_and_uncontrolled_extra_field_reject(self):
        for value in [['wrong quote'],['record captured2090'],['distinct events instead of answers']]:
            f=fixture();f[4]['exact_new_reading_literals']=value
            with self.subTest(value=value),self.assertRaises(p.RepairError):run_case(f)
        f=fixture();f[4]['uncontrolled_record_identity']='renamed-fact'
        with self.assertRaises(p.RepairError):run_case(f)
    def test_shared_robot_four_consumers_and_other_real_families_remain_visible(self):
        d=x.load_catalog();self.assertEqual(['LB-Q0274','LB-Q0275','LB-Q0276','existing LB-Q0641'],d['shared_record_families']['robots-declarations'])
        self.assertEqual({'LB-Q0636','LB-Q0643'},set(d['shared_record_families']['Dentrix-Ascend-C05']))
        self.assertFalse(d['global_Rule4_completion_granted'])
    def test_q0541_portable_temporal_projection_binds_original_source_provenance(self):
        data=(HERE/'q0541_temporal_provenance_projection.json').read_bytes()
        self.assertEqual('c0140f505dce49f2910d41950f36cdf576499738663ffaccb2eb9a723b9daead',p.sha(data))
        actual=json.loads(data)
        self.assertEqual('a5e60a1c788dde146a5cafeae9b3e1b11b4811f815c383d5a5771e86596c9329',actual['original_addendum_sha256'])
        spec=next(s for s in x.load_catalog()['cases'].values() if s['bank_id']=='LB-Q0541')
        self.assertEqual(actual['original_correction_object_sha256'],spec['source_evidence_anchor_sha256'])
        self.assertEqual('8c9722b9c89597eb959d0e5b8d46a513bec409741e0afad33f9edbec30c31d1d',actual['correct_temporal_Source_review_sha256'])
        self.assertEqual('LB-Q0541',actual['bank_id'])
        self.assertEqual('Its wrong label meant a contradiction with the dated vendor reference used for the check.',actual['temporal_correction']['exact_replacement'])
        statement=actual['exact_public_statement']
        self.assertEqual('2026-09-22T23:32:39.111Z',statement['observations'][0]['captured_at'])
        self.assertEqual('2026-10-08T03:16:35.775Z',statement['proof_read_at'])
        self.assertEqual('https://mortgagetech.ice.com/product-history',statement['proof_url'])
        self.assertEqual('July 18, 2023 AIQ is now ICE Data & Document Automation and ICE Mortgage Analyzers',statement['proof_quote'])
        self.assertEqual('ICE Mortgage Technology ships AI capabilities under the AIQ product family',actual['exact_quote'])
        self.assertEqual('loan-origination-software|q8|Claude|1',statement['quote_record_id'])
        self.assertEqual('Team review: in progress',statement['review_label'])
        self.assertNotIn('C:\\',data.decode());self.assertNotIn('file://',data.decode())
    def test_new_cases_require_exact43_nonPDF_union_and_bound_catalog_not_partial_fix(self):
        catalog=x.load_catalog();rows={p:{'class':'repository_rule'} for p in catalog['required_owner_nonPDF_sources']}
        for path,s in catalog['cases'].items():rows['docs/'+path]={'class':s['class']}
        d={'required28_catalog_sha256':x.CATALOG_SHA256,'source_changes':rows}
        self.assertEqual(43,x.validate_complete_required_scope(d)['nonPDF_sources'])
        for mode in ['missing','extra','class','catalog']:
            bad=copy.deepcopy(d)
            if mode=='missing':bad['source_changes'].pop(next(iter(rows)))
            elif mode=='extra':bad['source_changes']['docs/research/unreviewed.md']={'class':'rule4_fact'}
            elif mode=='class':bad['source_changes']['docs/'+next(iter(catalog['cases']))]={'class':'answer_metadata'}
            else:bad['required28_catalog_sha256']='0'*64
            with self.subTest(mode=mode),self.assertRaises(p.RepairError):x.validate_complete_required_scope(bad)
    def test_q0275_requires_actual_pass_and_both_separate_ordinary_peers(self):
        ids={'source':'c'*64,'writing':'d'*64};record={'path':x.ANTHROPIC,'review_ids':ids};calls=[]
        overlay=SimpleNamespace(_article_receipt=lambda key,rec,kind:calls.append(kind) or True)
        self.assertTrue(x.validate_anthropic_ordinary(overlay,record,ids,{'passed':True,'status':'PASS'}));self.assertEqual(['source','writing'],calls)
        for readiness in [{'passed':False,'status':'FAIL'},{'passed':True,'status':'FAIL'}]:
            with self.assertRaises(p.RepairError):x.validate_anthropic_ordinary(overlay,record,ids,readiness)
        for broken in [None,{'source':'c'*64}, {'source':'c'*64,'writing':'d'*64,'extra':'e'*64}]:
            with self.assertRaises(p.RepairError):x.validate_anthropic_ordinary(overlay,record,broken,{'passed':True,'status':'PASS'})
        for other in ['answers/x/not-finite.md','answers/chatgpt/which-legal-practice-software-does-chatgpt-recommend.md']:
            with self.assertRaises(p.RepairError):x.validate_anthropic_ordinary(overlay,{'path':other,'review_ids':ids},ids,{'passed':True,'status':'PASS'})
    def test_q0275_false_ordinary_source_or_writer_never_scoped_substitute(self):
        ids={'source':'c'*64,'writing':'d'*64};record={'path':x.ANTHROPIC,'review_ids':ids}
        for denied in ['source','writing']:
            ov=SimpleNamespace(_article_receipt=lambda key,rec,kind:kind!=denied)
            with self.subTest(denied=denied),self.assertRaises(p.RepairError):x.validate_anthropic_ordinary(ov,record,ids,{'passed':True,'status':'PASS'})
        ov=SimpleNamespace(_article_receipt=lambda *args:True)
        record['review_ids']={'source':'e'*64,'writing':'f'*64}
        with self.assertRaises(p.RepairError):x.validate_anthropic_ordinary(ov,record,ids,{'passed':True,'status':'PASS'})

if __name__=='__main__':unittest.main(verbosity=2)
