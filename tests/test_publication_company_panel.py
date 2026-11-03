"""Finite internal registry and fictional negative/annotation fixtures.

Full unpublished manuscripts are not checked into test fixtures. The separate
private exact-six proof reads reviewed input files. Internal helper fixtures
below cannot pass the production immutable registry loader.
"""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from tools import library_answers as answers, library_company_panel as panel, library_quality as q

ROOT = Path(__file__).resolve().parents[1]


class CompanyPanelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.docs = Path(self.temp.name)/'docs'
        self.registry_path = self.docs.parent/'tools'/panel.REGISTRY_PATH
        target = self.registry_path
        target.parent.mkdir(parents=True)
        self.actual = json.loads((ROOT/'tools'/panel.REGISTRY_PATH).read_text(encoding='utf-8'))
        target.write_text(json.dumps(self.actual), encoding='utf-8')
        self.case_key = next(iter(self.actual['cases']))

    def fixture(self, numeric=False):
        data = copy.deepcopy(self.actual)
        key = next(k for k,c in data['cases'].items() if bool(c['numeric_leads']) == numeric)
        case = data['cases'][key]
        opening = 'A fictional retained observation belongs to a dated public record.'
        body = '# Fictional question\n\n'+opening+'\n\n## What we measured\n\n'+ '\n'.join(panel.PUBLIC_SOURCES)+'\n\n## Next step\n\n'+f'[{panel.METHOD_LABEL}]({panel.METHOD_URL})'+'\n\n'+panel.NEUTRAL_OFFER+'\n'
        offset = body.index(opening)
        case.update(body_sha256=panel._sha(body), opening={'literal':opening, 'sha256':panel._sha(opening), 'start_Unicode_codepoint':offset, 'end_Unicode_codepoint':offset+len(opening), 'complete_body_sha256':panel._sha(body)}, quotes=[], source_review_receipts=['a'*64], writing_review_receipts=['c'*64],independent_writing_review_sha256='b'*64,opening_shape='source_first',classification_reason='Fictional API fixture, no actual classification approval.')
        meta = {'evidence_kind':panel.KIND, 'evidence_case':key, 'is_based_on':panel.SOURCE, 'evidence_method_receipts':[panel.METHOD_URL,*panel.PUBLIC_SOURCES], 'library_cluster':'changes', 'demand_evidence':'LB-Q9001 synthetic unit fixture', 'title':'Fictional title', 'headline':'Fictional headline', 'description':'Fictional description'}
        expected = panel.expected_figures(case,q.figure_key)
        page = {'file':self.docs/'answers/changes/fixture.md', 'path':'answers/changes/fixture.md', 'cluster':'changes', 'meta':meta,'body':body,'opening':opening, 'opening_sha256':q.digest(opening.encode()), 'source_sha256':q.digest(body.encode()), 'canonical_source_sha256':q.digest(body.encode()), 'six':q.sequences(q.words(body),6),'eight':q.sequences(q.words(opening),8)}
        observations = [o['observation_key'] for o in case['qualitative_leads']]
        note = {'bank_id':'LB-Q9001','source_sha256':page['source_sha256'],'canonical_source_sha256':page['canonical_source_sha256'],'opening_sha256':page['opening_sha256'],'opening_shape':'source_first','classification_reason':case['classification_reason'],'source_review_sha256':'a'*64,'writing_review_sha256':'b'*64,'lead_figures':list(expected),'lead_figure_spans':{k:[opening] for k in expected},'lead_observations':observations,'lead_observation_spans':{k:[opening] for k in observations}}
        return data,meta,body,page,note,expected

    def test_exact_public_registry_is_readable_and_only_six_cases(self):
        data = panel.load_registry(self.docs)
        self.assertEqual(6,len(data['cases']))
        self.assertEqual(4,sum(not c['numeric_leads'] for c in data['cases'].values()))
        self.assertEqual(4,sum(len(c['numeric_leads']) for c in data['cases'].values()))

    def test_loader_uses_internal_tools_registry_without_docs_asset(self):
        self.assertEqual(self.actual,panel.load_registry(self.docs))
        self.assertFalse((self.docs/'assets/library/php2shell-company-panel-six.json').exists())

    def test_legacy_public_asset_alone_cannot_supply_registry(self):
        legacy=self.docs/'assets/library/php2shell-company-panel-six.json'
        legacy.parent.mkdir(parents=True)
        legacy.write_bytes(self.registry_path.read_bytes())
        self.registry_path.unlink()
        with self.assertRaises(OSError):panel.load_registry(self.docs)

    def test_no_private_packets_prompts_model_versions_or_paths_in_registry(self):
        encoded = panel._canonical(self.actual)
        self.assertNotIn('C:\\Users',encoded)
        self.assertNotIn('PRIVATE-S6',encoded)
        for field in ('private_packet','prompt','model_version','local_path'):
            self.assertNotIn('"'+field+'"',encoded)

    def test_wrong_public_source_hash_is_rejected(self):
        data = copy.deepcopy(self.actual)
        data['public_source_sha256'][next(iter(panel.PUBLIC_SOURCES))] = '0'*64
        self.registry_path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError,'registry differs'):
            panel.load_registry(self.docs)
        with self.assertRaisesRegex(ValueError,'wrong public source'):
            panel._validate_registry(data)

    def test_duplicate_registry_key_is_rejected(self):
        self.registry_path.write_text('{"cases":{},"cases":{}}')
        with self.assertRaisesRegex(ValueError,'duplicate'):
            panel.load_registry(self.docs)

    def test_registry_tampering_cannot_supply_another_case_or_body_approval(self):
        for field in ('body_sha256','source_review_receipts','writing_review_receipts'):
            with self.subTest(field=field):
                data=copy.deepcopy(self.actual);data['cases'][self.case_key][field]='c'*64
                self.registry_path.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError,'registry differs'):panel.load_registry(self.docs)

    def test_wrong_excerpt_quote_offset_or_source_date_rejected(self):
        for mode in ('excerpt','quote','date'):
            with self.subTest(mode=mode):
                data=copy.deepcopy(self.actual);case=data['cases'][self.case_key]
                record=data['answer_records'][case['record_keys'][0]]
                if mode=='excerpt':record['excerpt']+=' changed'
                elif mode=='date':record['captured_at_utc']='2026-10-24T00:00:00Z'
                else:case['quotes'][0]['source_matches'][0]['excerpt_start_Unicode_codepoint']+=1
                with self.assertRaises(ValueError):panel._validate_registry(data)

    def test_numeric_counts_recomputed_from_members_not_caller_numbers(self):
        for field,value in [('count',1),('base',150)]:
            with self.subTest(field=field):
                data=copy.deepcopy(self.actual);case=next(c for c in data['cases'].values() if c['numeric_leads'])
                case['numeric_leads'][0]['figure'][field]=value
                with self.assertRaises(ValueError):panel._validate_registry(data)

    def test_numeric_member_and_unit_mutations_rejected(self):
        for mode in ('members','date','unit'):
            with self.subTest(mode=mode):
                data=copy.deepcopy(self.actual);case=next(c for c in data['cases'].values() if c['numeric_leads']);cut=case['numeric_leads'][0]
                if mode=='members':cut['members'].pop()
                elif mode=='date':cut['figure']['record']['capture_date']='2026-10-24'
                else:cut['match_unit']='answer-text'
                with self.assertRaises(ValueError):panel._validate_registry(data)

    def test_nextcloud_groups_preserve_overlapping_chatgpt_member(self):
        case=next(c for c in self.actual['cases'].values() if len(c['numeric_leads'])==3)
        groups=[c['members'] for c in case['numeric_leads']]
        self.assertEqual([1,2,3],[len(g) for g in groups])
        self.assertEqual('ChatGPT',groups[0][0]['engine'])
        self.assertEqual('ChatGPT',groups[1][0]['engine'])
        self.assertEqual(5,len({m['engine'] for g in groups for m in g}))

    def test_public_entry_cannot_accept_fictional_helper_fixture(self):
        _,meta,body,_,_,_=self.fixture()
        self.assertTrue(panel.validate_company_panel(meta,body,self.docs))

    def test_pure_case_helper_accepts_its_exact_synthetic_bound_input(self):
        data,meta,body,_,_,_=self.fixture()
        self.assertIs(panel._validate_case(meta,body,data),data['cases'][meta['evidence_case']])
        self.assertIs(panel._validate_case(meta,'\n'+body.replace('\n','\r\n'),data),data['cases'][meta['evidence_case']])

    def test_wrong_kind_source_case_or_receipts_rejected(self):
        for field,value in [('evidence_kind','published-study'),('is_based_on',answers.SEPTEMBER_INDEX_DOI),('evidence_case','another-unreviewed-case'),('evidence_method_receipts',[panel.METHOD_URL])]:
            with self.subTest(field=field):
                data,meta,body,_,_,_=self.fixture();meta[field]=value
                with self.assertRaises(ValueError):panel._validate_case(meta,body,data)

    def test_wrong_body_date_quote_or_footer_rejected_by_full_body_binding(self):
        for replacement in ('different observation','23 October 2027','invented quotation','Fix one answer, $490'):
            with self.subTest(replacement=replacement):
                data,meta,body,_,_,_=self.fixture()
                changed=body.replace('fictional retained observation',replacement)
                with self.assertRaisesRegex(ValueError,'body changed'):panel._validate_case(meta,changed,data)

    def test_qualitative_annotation_empty_figures_are_bound_not_waived(self):
        data,_,_,page,note,figures=self.fixture()
        with patch.object(panel,'load_registry',return_value=data):
            panel.validate_annotation(page,note,figures,q.figure_key)
        self.assertEqual([],note['lead_figures'])
        self.assertTrue(note['lead_observations'])

    def test_fake_numeric_one_on_qualitative_case_rejected(self):
        data,_,_,page,note,figures=self.fixture();note['lead_figures']=['fake-count-one']
        with patch.object(panel,'load_registry',return_value=data):
            with self.assertRaisesRegex(ValueError,'no fake count-one'):panel.validate_annotation(page,note,figures,q.figure_key)

    def test_qualitative_registry_cannot_be_given_numeric_count_one(self):
        data=copy.deepcopy(self.actual)
        case=next(c for c in data['cases'].values() if c['qualitative_leads'])
        case['qualitative_leads'][0]['count']=1
        with self.assertRaisesRegex(ValueError,'fake numeric cut'):panel._validate_registry(data)

    def test_exact_numeric_annotation_stays_numeric(self):
        data,_,_,page,note,figures=self.fixture(numeric=True)
        with patch.object(panel,'load_registry',return_value=data):
            panel.validate_annotation(page,note,figures,q.figure_key)
        self.assertTrue(note['lead_figures'])
        self.assertEqual([],note['lead_observations'])

    def test_unknown_reminted_or_missing_qualitative_keys_rejected(self):
        for value in ([],['another-key'],['same-meaning-new-name']):
            data,_,_,page,note,figures=self.fixture();note['lead_observations']=value
            with patch.object(panel,'load_registry',return_value=data):
                with self.assertRaisesRegex(ValueError,'observation keys'):panel.validate_annotation(page,note,figures,q.figure_key)

    def test_wrong_qualitative_span_or_independent_receipt_rejected(self):
        for field,value in [('lead_observation_spans',{}),('source_review_sha256','c'*64),('writing_review_sha256','d'*64)]:
            data,_,_,page,note,figures=self.fixture();note[field]=value
            with patch.object(panel,'load_registry',return_value=data):
                with self.assertRaises(ValueError):panel.validate_annotation(page,note,figures,q.figure_key)

    def test_opening_shape_cannot_be_relabelled_to_make_distribution_pass(self):
        data,_,_,page,note,figures=self.fixture();note['opening_shape']='date_first'
        with patch.object(panel,'load_registry',return_value=data):
            with self.assertRaisesRegex(ValueError,'classification differs'):panel.validate_annotation(page,note,figures,q.figure_key)

    def test_wrong_numeric_cut_annotation_or_missing_threecuts_rejected(self):
        data,_,_,page,note,figures=self.fixture(numeric=True)
        figures[next(iter(figures))]['count']=1
        # Break alias with the synthetic registry to test independent equality.
        data2=copy.deepcopy(self.actual);key=page['meta']['evidence_case']
        data['cases'][key]['numeric_leads']=data2['cases'][key]['numeric_leads']
        with patch.object(panel,'load_registry',return_value=data):
            with self.assertRaisesRegex(ValueError,'wrong numeric source'):panel.validate_annotation(page,note,figures,q.figure_key)

    def test_all_collection_qualitative_reuse_limit_is_three(self):
        _,_,_,page,note,_=self.fixture()
        for count,expected in [(3,False),(4,True)]:
            pages={str(i):copy.deepcopy(page) for i in range(count)};notes={k:copy.deepcopy(note) for k in pages}
            result=q.analyze(pages,notes,{'changes':list(pages)},[],self.docs)
            self.assertEqual(expected,any(v['kind']=='lead_observation_limit' for v in result['violations']))
            self.assertEqual(count,len(result['lead_observation_pages'][note['lead_observations'][0]]))

    def test_shared_dreamhost_chronology_has_one_identity_used_twice(self):
        keys=[o['observation_key'] for c in self.actual['cases'].values() for o in c['qualitative_leads']]
        key='php2shell-public-dreamhost-answer-before-later-resolution-and-check'
        self.assertEqual(2,keys.count(key))

    def test_noncompany_source_cannot_use_empty_numeric_annotation(self):
        _,_,_,page,note,_=self.fixture();page['meta'].pop('evidence_kind')
        fake={'source_url':answers.SEPTEMBER_INDEX_DOI,'record':{'metric':'fiction','subject':'fiction'},'count':2,'base':10,'unit':'fixture','label':'Fixture','source_review_sha256':'a'*64}
        metadata={'schema_version':1,'shape_definitions':{k:k for k in ['source_first','a','b','c','d','e','f','g']},'cluster_plans':{'changes':['source_first','a','b','c','d','e','f','g']},'figures':{q.figure_key(fake):fake},'pages':{page['path']:note}}
        with self.assertRaisesRegex(ValueError,'restricted to the exact six'):q.validate_annotations({page['path']:page},metadata)
        note['lead_observations']=[];note['lead_observation_spans']={}
        with self.assertRaisesRegex(ValueError,'no independently identified lead figure'):q.validate_annotations({page['path']:page},metadata)


if __name__=='__main__':
    unittest.main()
