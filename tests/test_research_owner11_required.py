"""Private pure-input tests; no owning imports/build, actual future producer or approval."""
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime,timezone,timedelta
import copy,importlib.util,json,re,sys,tempfile,unittest
import yaml
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parents[1]
F=H/'tests/fixtures/research_owner11'
sys.path.insert(0,str(H/'tools'))
import library_research_owner_preservation as gate
from library_research_support import sha,qsha

MASTER=F/'fixture_index.json'
def parse(full):
    m=re.match(r'\A---\n(.*?)\n---\n(.*)\Z',full,re.S)
    return {'meta':yaml.safe_load(m[1]),'body':m[2].lstrip('\n'),'effective_full_source':full}
def rebuild(record):
    return '---\n'+yaml.safe_dump(record['meta'],sort_keys=False,allow_unicode=True)+'---\n\n'+record['body']

class Owner11PureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=MASTER.read_bytes();assert sha(raw)=='bfe7fa171329549a126dcbc95992c20718583f3ae67f108316806b55a40286bd'
        assert json.loads(raw)['Source_required_manifest_sha256']=='2975e8403e6f0cf9e695909193328a78e4dd0a5e7b608d5e231748010f239adf'
        cls.master=json.loads(raw);cls.catalog=gate.catalog()
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='owner11-pure-',dir=H)
        self.root=Path(self.temp.name);self.files={};self.before={};self.after={}
        self.event=datetime.now(timezone.utc).isoformat()
        self.data={'Owner11_required_Source_manifest_sha256':self.catalog['Source_required_manifest_sha256'],
            'Owner11_preserved_claim_spans':{},'Owner11_Source_lineage':{},
            'Owner11_actual_Research_adoption_utc':self.event,'Owner11_presentation_date_edits':{}}
        for path,spec in self.catalog['sources'].items():
            original=self.master['sources'][path]
            full=(F/original['expected_before_file']['path']).read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n')
            self.before[path]=parse(full);after=copy.deepcopy(self.before[path])
            edits=gate._expected_presentation(spec,self.event)
            for e in edits:after['body']=after['body'].replace(e['old'],e['new'],1)
            after['body']+='\nSynthetic future Research fixture only; no actual adoption.\n'
            for k in ['updated','date_modified']:after['meta'][k]=self.event
            after['effective_full_source']=rebuild(after);self.after[path]=after
            self.data['Owner11_preserved_claim_spans'][path]=[{k:x[k] for k in ['id','text','sha256']} for x in spec['required_spans']]
            self.data['Owner11_presentation_date_edits'][path]=edits
            refs={'source_id':spec['id']}
            for key,masterkey in [('scoped_Source','current_scoped_Source_receipt'),('Source_evidence','current_fact_or_precision_Source_evidence'),('repair_ledger','original_Root_repair_change_ledger')]:
                ref=original[masterkey];raw=(F/ref['path']).read_bytes();assert sha(raw)==ref['sha256']
                rel='.library-research-work/source-lineage/'+spec['id']+'/'+key+'.json'
                p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
                refs[key]={'path':rel,'sha256':ref['sha256']};self.files[rel]=ref['sha256']
            self.data['Owner11_Source_lineage'][path]=refs
        self.support=SimpleNamespace(plan={'staged_file_sha256':self.files},assert_current=lambda:None)
    def tearDown(self):self.temp.cleanup()
    def check(self):
        return gate.validate_required_owner11(root=self.root,support=self.support,data=self.data,
            before_records=self.before,after_records=self.after)
    def first(self):return self.catalog['required_paths'][0]
    def test_exact_complete101_and33_possible_date_slots(self):
        proof=self.check()
        self.assertEqual(11,len(proof['rows']));self.assertEqual(101,sum(len(x['required_span_ids']) for x in proof['rows']))
        self.assertFalse(proof['Research_release_or_ordinary_Source_kind_or_S5_PASS_granted'])
        self.assertEqual(33,sum(len(x['presentation_slots']) for x in self.catalog['sources'].values()))
    def test_exact_unchanged11_need_no_new_date_rewrite(self):
        self.after=copy.deepcopy(self.before)
        self.data['Owner11_presentation_date_edits']={p:[] for p in self.after}
        self.assertTrue(all(not x['presentation']['changed'] for x in self.check()['rows']))
    def test_missing_extra_or_foreign_source_case_rejects(self):
        for key in ['Owner11_preserved_claim_spans','Owner11_Source_lineage','Owner11_presentation_date_edits']:
            old=copy.deepcopy(self.data[key]);self.data[key].pop(self.first())
            with self.subTest(key=key,mode='missing'),self.assertRaises(ValueError):self.check()
            self.data[key]=copy.deepcopy(old);self.data[key]['research/foreign/index.md']=[]
            with self.subTest(key=key,mode='extra'),self.assertRaises(ValueError):self.check()
            self.data[key]=old
    def test_missing_extra_shortened_reordered_or_new_ID_span_rejects(self):
        path=self.first();old=copy.deepcopy(self.data['Owner11_preserved_claim_spans'][path])
        for mode in ['missing','extra','shortened','reordered','foreign-id']:
            rows=copy.deepcopy(old)
            if mode=='missing':rows.pop()
            elif mode=='extra':rows.append({'id':'foreign','text':'\n','sha256':sha(b'\n')})
            elif mode=='shortened':rows[0]['text']=rows[0]['text'][:20];rows[0]['sha256']=sha(rows[0]['text'].encode())
            elif mode=='reordered':rows.reverse()
            else:rows[0]['id']='foreign'
            self.data['Owner11_preserved_claim_spans'][path]=rows
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.check()
        self.data['Owner11_preserved_claim_spans'][path]=old
    def test_unrelated_surviving_substring_does_not_replace_fact_or_qualification(self):
        path=self.first();old=copy.deepcopy(self.data['Owner11_preserved_claim_spans'][path])
        self.data['Owner11_preserved_claim_spans'][path]=[{'id':'anything','text':'\n','sha256':sha(b'\n')}]
        with self.assertRaises(ValueError):self.check()
        self.data['Owner11_preserved_claim_spans'][path]=old
        self.after[path]['body']=self.after[path]['body'].replace(old[0]['text'],'An unrelated sentence survives.',1)
        with self.assertRaises(ValueError):self.check()
    def test_scientific_count_and_historical_capture_date_edits_reject(self):
        path=self.first();old=self.after[path]['body']
        for before,after in [('1,259','1,260'),('22 and 23 September 2026','22 and 23 September 2027')]:
            self.after[path]['body']=old.replace(before,after,1)
            with self.subTest(before=before),self.assertRaises(ValueError):self.check()
        self.after[path]['body']=old
    def test_stale_before_body_metadata_or_full_source_rejects(self):
        path=self.first();old=copy.deepcopy(self.before[path])
        for key in ['body','meta','effective_full_source']:
            self.before[path]=copy.deepcopy(old)
            if key=='meta':self.before[path][key]['description']+=' altered'
            else:self.before[path][key]+=' altered'
            with self.subTest(key=key),self.assertRaises(ValueError):self.check()
        self.before[path]=old
    def test_real_PR93_source_is_not_mistaken_for_unpublished_after_Risk_baseline(self):
        path=self.first()
        actual=F/'negative-pr93-before.md'
        self.before[path]=parse(actual.read_text(encoding='utf-8-sig').replace('\r\n','\n').replace('\r','\n'))
        with self.assertRaisesRegex(ValueError,'Actual published after-Risk Owner11 before-source differs'):
            self.check()
    def test_changed_protected_publication_and_access_dates_reject(self):
        path=self.first();old=copy.deepcopy(self.after[path])
        self.after[path]['meta']['date_published']='2026-11-04T00:00:00+00:00'
        with self.assertRaises(ValueError):self.check()
        self.after[path]=copy.deepcopy(old)
        self.after[path]['body']=self.after[path]['body'].replace('urldate = {2026-11-03}','urldate = {2026-11-04}',1)
        with self.assertRaises(ValueError):self.check()
        self.after[path]=old
    def test_missing_or_foreign_Source_receipt_or_case_rejects(self):
        path=self.first();old=copy.deepcopy(self.data['Owner11_Source_lineage'][path])
        other=self.catalog['required_paths'][1]
        for mode in ['missing','foreign','foreign-id']:
            self.data['Owner11_Source_lineage'][path]=copy.deepcopy(old)
            if mode=='missing':self.data['Owner11_Source_lineage'][path].pop('Source_evidence')
            elif mode=='foreign':self.data['Owner11_Source_lineage'][path]['scoped_Source']=copy.deepcopy(self.data['Owner11_Source_lineage'][other]['scoped_Source'])
            else:self.data['Owner11_Source_lineage'][path]['source_id']='foreign'
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.check()
        self.data['Owner11_Source_lineage'][path]=old
    def test_receipt_bytes_or_committed_closure_tampering_rejects(self):
        ref=self.data['Owner11_Source_lineage'][self.first()]['scoped_Source'];p=self.root/ref['path'];old=p.read_bytes()
        p.write_bytes(old+b' ')
        with self.assertRaises(ValueError):self.check()
        p.write_bytes(old);self.files.pop(ref['path'])
        with self.assertRaises(ValueError):self.check()
    def test_missing_or_changed_manifest_digest_rejects(self):
        self.data['Owner11_required_Source_manifest_sha256']='0'*64
        with self.assertRaises(ValueError):self.check()
    def test_mutable_date_unknown_ID_wrong_text_missing_inverse_rejects(self):
        # Use a Nov3-before page, whose visible token changes on the actual Nov4
        # fixture date. This is a pure token test, not a real Research event.
        path='research/playbooks/site-structure-basics/index.md'
        old=copy.deepcopy(self.data['Owner11_presentation_date_edits'][path]);self.assertTrue(old)
        for mode in ['missing','foreign','wrongtext','wronghash']:
            rows=copy.deepcopy(old)
            if mode=='missing':rows.pop()
            elif mode=='foreign':rows[0]['id']='foreign-date'
            elif mode=='wrongtext':rows[0]['new']='updated January 1, 2030.';rows[0]['new_sha256']=sha(rows[0]['new'].encode())
            else:rows[0]['new_sha256']='0'*64
            self.data['Owner11_presentation_date_edits'][path]=rows
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.check()
        self.data['Owner11_presentation_date_edits'][path]=old
    def test_missing_wrong_or_future_actual_event_rejects(self):
        old=self.data['Owner11_actual_Research_adoption_utc']
        for value in [None,'not-a-date',(datetime.now(timezone.utc)+timedelta(days=2)).isoformat()]:
            self.data['Owner11_actual_Research_adoption_utc']=value
            with self.subTest(value=value),self.assertRaises(ValueError):self.check()
        self.data['Owner11_actual_Research_adoption_utc']=old
    def test_incoherent_metadata_or_unwritten_date_replacement_rejects(self):
        path='research/playbooks/site-structure-basics/index.md';old=copy.deepcopy(self.after[path])
        self.after[path]['meta']['updated']=self.before[path]['meta']['updated']
        with self.assertRaises(ValueError):self.check()
        self.after[path]=copy.deepcopy(old)
        edit=self.data['Owner11_presentation_date_edits'][path][0]
        self.after[path]['body']=self.after[path]['body'].replace(edit['new'],edit['old'],1)
        with self.assertRaises(ValueError):self.check()
    def test_internal_catalog_is_portable_and_finite(self):
        raw=(H/'tools/library_research_owner_required_spans.json').read_bytes()
        self.assertNotIn(b'Downloads',raw);self.assertNotIn(b'C:\\',raw);self.assertNotIn(b'C:/',raw)
        self.assertEqual(101,len(self.catalog['all_required_span_ids']))

if __name__=='__main__':unittest.main(verbosity=2)
