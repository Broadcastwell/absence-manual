"""Fictional negative cases for the unchanged LIBRARY416 quality thresholds."""
import copy
from fractions import Fraction
import json
from pathlib import Path
import tempfile
import unittest

from tools import library_quality as q

ROOT = Path(__file__).resolve().parents[1]


def page(name, text='', shape='figure_first'):
    return {'path':name,'cluster':'measurement','meta':{'title':name+' question',
        'headline':name+' question','description':name+' distinct description'},
        'body':text,'opening':text,'source_sha256':'a'*64,'canonical_source_sha256':'a'*64,'opening_sha256':'b'*64,
        'six':q.sequences(q.words(text),6),'eight':q.sequences(q.words(text),8),
        'quality_annotation':{'opening_shape':shape,'lead_figures':['one']}}


def baseline_fixture():
    pages = {f'answers/measurement/fictional-{i}.md':page(f'fictional-{i}') for i in range(150)}
    snapshot = {name:{'source_sha256':p['source_sha256'],'canonical_source_sha256':p['canonical_source_sha256'],'opening_sha256':p['opening_sha256'],
        'opening_shape':'figure_first','lead_figures':['one']} for name,p in pages.items()}
    baseline = {'schema_version':1,'frozen_pages':snapshot,'exceptions':{}}
    trusted = {'snapshot_sha256':q.digest(q.canonical_json(snapshot).encode()),
               'baseline_sha256':q.digest(q.canonical_json(baseline).encode())}
    return pages,baseline,trusted


class QualityRuleTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.docs = Path(self.temporary.name)/'docs'
        self.docs.mkdir()

    def seal_fixture_cases(self, baseline, trusted):
        trusted['baseline_sha256']=q.digest(q.canonical_json(baseline).encode())

    def analyze_two(self, left, right):
        pages={'a':page('a',left),'b':page('b',right,'date_first')}
        notes={name:{'opening_shape':p['quality_annotation']['opening_shape'],'lead_figures':[]} for name,p in pages.items()}
        return q.analyze(pages,notes,{'measurement':['a','b']},[],self.docs)

    def test_exact_twenty_percent_passes_and_twenty_five_fails(self):
        at=self.analyze_two('one two three four five six alpha beta gamma delta',
                            'one two three four five six white black green red')
        above=self.analyze_two('one two three four five six alpha beta gamma',
                               'one two three four five six white black green')
        self.assertFalse(any(r['kind']=='six_word_similarity' for r in at['violations']))
        self.assertEqual(Fraction(at['highest_pair_per_cluster']['measurement']['score_fraction']),Fraction(1,5))
        self.assertTrue(any(r['kind']=='six_word_similarity' for r in above['violations']))

    def test_smaller_set_is_the_denominator_not_union_or_larger_page(self):
        a=page('a');b=page('b')
        a['six']={tuple(str(i)+str(j) for j in range(6)) for i in range(5)}
        b['six']=set(list(a['six'])[:2])|{tuple('x'+str(i)+str(j) for j in range(6)) for i in range(100)}
        result=q.analyze({'a':a,'b':b},{'a':{'opening_shape':'a','lead_figures':[]},'b':{'opening_shape':'b','lead_figures':[]}}, {'measurement':['a','b']},[],self.docs)
        rule=next(r for r in result['violations'] if r['kind']=='six_word_similarity')
        self.assertEqual((rule['shared_sequences'],rule['smaller_sequence_set'],rule['score_fraction']),(2,5,'2/5'))

    def test_six_word_sets_deduplicate_repeated_occurrences(self):
        self.assertEqual(len(q.sequences(q.words('one two three four five six '*100),6)),6)

    def test_any_shared_eight_word_sequence_fails_even_inside_opening(self):
        result=self.analyze_two('Different start alpha beta gamma delta epsilon zeta eta theta ending.',
                                'Another lead alpha beta gamma delta epsilon zeta eta theta finish.')
        self.assertTrue(any(r['kind']=='eight_word_opening' and 'alpha beta gamma delta epsilon zeta eta theta' in r['shared_sequences'] for r in result['violations']))
        seven=self.analyze_two('First alpha beta gamma delta epsilon zeta eta last.',
                               'Other alpha beta gamma delta epsilon zeta eta finish.')
        self.assertFalse(any(r['kind']=='eight_word_opening' for r in seven['violations']))

    def test_normalization_prevents_case_punctuation_and_number_separator_evasion(self):
        self.assertEqual(q.words("Vendor’s 2,095-answer result: AI-VISIBILITY!"),q.words("vendor's 2095 answer result ai visibility"))

    def test_opening_text_normalizes_line_endings_but_file_hashes_stay_exact(self):
        folder=self.docs/'answers/measurement';folder.mkdir(parents=True)
        text='---\nlibrary_cluster: measurement\n---\n\n# Fictional question\n\nA fictional answer has 3 of 10 observations. \n\n## What we measured\n\nFictional fixture only.\n'
        (folder/'lf.md').write_bytes(text.encode())
        (folder/'crlf.md').write_bytes(text.replace('\n','\r\n').encode())
        pages=q.load_pages(self.docs);a=pages['answers/measurement/lf.md'];b=pages['answers/measurement/crlf.md']
        self.assertEqual(a['opening'],b['opening'])
        self.assertEqual(a['opening_sha256'],b['opening_sha256'])
        self.assertNotEqual(a['source_sha256'],b['source_sha256'])
        self.assertEqual(a['canonical_source_sha256'],b['canonical_source_sha256'])
        (folder/'crlf.md').write_bytes(text.replace('3 of 10','4 of 10').replace('\n','\r\n').encode())
        changed=q.load_pages(self.docs)['answers/measurement/crlf.md']
        self.assertNotEqual(a['canonical_source_sha256'],changed['canonical_source_sha256'])

    def test_only_named_fixed_blocks_and_link_labels_are_excluded(self):
        prose='# Question\n\nUnique evidence stays. [Common label](https://example.test/)\n\n## What we measured\n\nA specific source fact remains.\n\n'+q.LIMIT_SENTENCE+'\n\n## Next step\n\nFixed purchase text.\nPrepared by the Broadcastwell team.'
        actual=q.comparison_prose(prose)
        self.assertIn('Unique evidence stays',actual)
        self.assertIn('A specific source fact remains',actual)
        for excluded in ('Common label','example.test','Fixed purchase text',q.LIMIT_SENTENCE,'Prepared by'):
            self.assertNotIn(excluded,actual)

    def test_actual_hub_order_controls_adjacency(self):
        folder=self.docs/'answers/measurement';folder.mkdir(parents=True)
        names=['z','a','m'];pages={}
        for name in names:
            path=folder/(name+'.md');path.write_text('source',encoding='utf-8')
            pages[path.relative_to(self.docs).as_posix()]=page(name,'one two three four five six seven')
        (folder/'index.md').write_text('\n'.join(f'[{name}]({name}.md)' for name in names),encoding='utf-8')
        order,errors=q.hub_orders(self.docs,pages)
        self.assertEqual(errors,[])
        self.assertEqual(order['measurement'],['answers/measurement/'+name+'.md' for name in names])
        notes={key:{'opening_shape':'same' if i<2 else 'different','lead_figures':[]} for i,key in enumerate(order['measurement'])}
        result=q.analyze(pages,notes,order,[],self.docs)
        adjacency=[r['hub_order_pair'] for r in result['violations'] if r['kind']=='opening_adjacency']
        self.assertEqual(adjacency,[order['measurement'][:2]])

    def test_overused_shape_count_cannot_increase_with_new_pages(self):
        pages,baseline,trusted=baseline_fixture();names=list(pages)[:5]
        row=q.fact('opening_concentration',names,cluster='measurement',shape='figure_first',count=5,total=10)
        row['key']='opening_concentration:measurement:figure_first'
        baseline['exceptions'][row['key']]=row
        self.seal_fixture_cases(baseline,trusted)
        current=dict(row,pages=names+['new'],count=6,total=11)
        pages['new']=page('new')
        errors,_,_=q.apply_baseline({'violations':[current]},pages,baseline,trusted)
        self.assertEqual(errors,[current])
        # A genuinely resolved ratio is no longer a violation and is reported.
        errors,_,resolved=q.apply_baseline({'violations':[]},pages,baseline,trusted)
        self.assertEqual(errors,[]);self.assertEqual(resolved,[row['key']])

    def test_existing_adjacency_does_not_exempt_a_new_neighbor_pair(self):
        pages,baseline,trusted=baseline_fixture();a,b=list(pages)[:2]
        before=q.fact('opening_adjacency',[a,b],hub_order_pair=[a,b],cluster='measurement',shape='same')
        baseline['exceptions'][before['key']]=before
        self.seal_fixture_cases(baseline,trusted)
        pages['new']=page('new')
        after=q.fact('opening_adjacency',[a,'new'],hub_order_pair=[a,'new'],cluster='measurement',shape='same')
        errors,_,_=q.apply_baseline({'violations':[after]},pages,baseline,trusted)
        self.assertEqual(errors,[after])

    def test_old_pair_exception_cannot_cover_new_page_or_changed_source(self):
        pages,baseline,trusted=baseline_fixture();a,b=list(pages)[:2]
        row=q.fact('eight_word_opening',[a,b],shared_sequences=['one two three four five six seven eight'])
        baseline['exceptions'][row['key']]=row
        self.seal_fixture_cases(baseline,trusted)
        self.assertEqual(q.apply_baseline({'violations':[row]},pages,baseline,trusted)[0],[])
        pages['new']=page('new')
        new=q.fact('eight_word_opening',[a,'new'],shared_sequences=row['shared_sequences'])
        self.assertEqual(q.apply_baseline({'violations':[new]},pages,baseline,trusted)[0],[new])
        pages[a]['source_sha256']='c'*64
        pages[a]['canonical_source_sha256']='c'*64
        with self.assertRaisesRegex(ValueError,'frozen baseline page changed'):
            q.apply_baseline({'violations':[row]},pages,baseline,trusted)

    def test_new_page_baseline_injection_or_relabelled_old_shape_fails(self):
        pages,baseline,trusted=baseline_fixture();a=next(iter(pages))
        baseline['exceptions']['fake']={'pages':['new']}
        with self.assertRaisesRegex(ValueError,'names a new page'):
            q.apply_baseline({'violations':[]},pages,baseline,trusted)
        baseline['exceptions']={};pages[a]['quality_annotation']['opening_shape']='relabelled'
        with self.assertRaisesRegex(ValueError,'classification changed'):
            q.apply_baseline({'violations':[]},pages,baseline,trusted)

    def test_overused_figure_cannot_add_one_new_leading_page(self):
        pages,baseline,trusted=baseline_fixture();names=list(pages)[:4]
        row=q.fact('lead_figure_limit',names,figure='one',count=4);row['key']='lead_figure_limit:one'
        baseline['exceptions'][row['key']]=row;pages['new']=page('new')
        self.seal_fixture_cases(baseline,trusted)
        after=dict(row,pages=names+['new'],count=5)
        self.assertEqual(q.apply_baseline({'violations':[after]},pages,baseline,trusted)[0],[after])

    def test_all_multi_figure_leads_count_once_per_page(self):
        pages={str(i):page(str(i),'one two three four five six seven '+str(i)) for i in range(4)}
        notes={key:{'opening_shape':key,'lead_figures':['first','second']} for key in pages}
        result=q.analyze(pages,notes,{'measurement':list(pages)},[],self.docs)
        over=[r for r in result['violations'] if r['kind']=='lead_figure_limit']
        self.assertEqual({r['figure'] for r in over},{'first','second'})
        self.assertTrue(all(r['count']==4 for r in over))

    def test_three_leads_pass_and_supporting_use_is_not_a_fourth_lead(self):
        pages={str(i):page(str(i),'one two three four five six seven '+str(i)) for i in range(4)}
        notes={key:{'opening_shape':key,'lead_figures':['first'] if key!='3' else ['different']} for key in pages}
        result=q.analyze(pages,notes,{'measurement':list(pages)},[],self.docs)
        self.assertEqual(result['lead_figure_pages']['first'],['0','1','2'])
        self.assertFalse(any(r['kind']=='lead_figure_limit' for r in result['violations']))

    def test_figure_identity_uses_published_cut_not_spelling_rounding_or_url_alias(self):
        record={'source_url':'https://doi.org/10.5281/zenodo.12345','record':{'metric':'named','subject':'Vendor A','category':'dental','engine':'ChatGPT','capture_date':'2026-09-22'},'count':'108','base':'150','unit':'answers','label':'Observed names','source_review_sha256':'a'*64}
        alias=copy.deepcopy(record);alias.update(source_url='https://dx.doi.org/10.5281/zenodo.12345/',count='108.0',base=150)
        self.assertEqual(q.figure_key(record),q.figure_key(alias))
        alias['unit']='valid answers'
        self.assertEqual(q.figure_key(record),q.figure_key(alias))
        record['record']['capture_date']='2026-09-22|2026-09-23'
        alias['record']['capture_date']='2026-09-23|2026-09-22'
        self.assertEqual(q.figure_key(record),q.figure_key(alias))
        other=copy.deepcopy(record);other['record']['engine']='Claude'
        self.assertNotEqual(q.figure_key(record),q.figure_key(other))
        other=copy.deepcopy(record);other['record']['page_slug']='fabricated-uniqueness'
        with self.assertRaises(ValueError):q.figure_key(other)
        derived=copy.deepcopy(record);derived.update(count='72',base='100')
        metadata={'schema_version':1,'pages':{},'shape_definitions':{'one':'a real shape'},'cluster_plans':{},'figures':{q.figure_key(record):record,q.figure_key(derived):derived}}
        with self.assertRaisesRegex(ValueError,'multiple count/base identities'):
            q.validate_annotations({},metadata)

    def test_own_title_headline_equal_is_allowed_but_cross_field_duplicate_fails(self):
        a,b=page('a'),page('b')
        self.assertEqual(q.uniqueness({'a':a},self.docs,[]),[])
        b['meta']['description']=a['meta']['headline']
        self.assertTrue(any(r['kind']=='metadata_duplicate' for r in q.uniqueness({'a':a,'b':b},self.docs,[])))

    def test_manual_index_and_alias_cross_duplicates_fail(self):
        a,b=page('a'),page('b')
        (self.docs/'chapter.md').write_text('---\npage_class: chapter\ntitle: '+json.dumps('Chapter 2: '+a['meta']['title'])+'\n---\n# Chapter heading\n',encoding='utf-8')
        result=q.uniqueness({'a':a},self.docs,[{'title':a['meta']['headline'],'url':'https://index.broadcastwell.com/questions/fictional/'}])
        self.assertEqual({r['scope'] for r in result if r['kind']=='reference_title_duplicate'},{'Manual chapter','Index question'})
        a['meta']['also_asked_as']=[b['meta']['title'].upper()+'?']
        self.assertTrue(any(r['kind']=='alias_title_duplicate' for r in q.uniqueness({'a':a,'b':b},self.docs,[])))

    def test_unreviewed_or_changed_opening_never_silently_classifies(self):
        p=page('a','One specific measured opening.')
        metadata={'schema_version':1,'pages':{'a':{}},'shape_definitions':{'one':'specific'},'cluster_plans':{'measurement':['one']},'figures':{}}
        with self.assertRaisesRegex(ValueError,'at least eight'):
            q.validate_annotations({'a':p},metadata)
        with self.assertRaises(ValueError):q.exact_number(True)

    def test_changed_opening_unbound_extra_fact_and_false_span_fail(self):
        p=page('a','Vendor A was named in 3 of 10 fictional answers.')
        p['meta']['demand_evidence']='LB-Q9000, fictional validation receipt'
        record={'source_url':'https://doi.org/10.5281/zenodo.12345','record':{'metric':'named','subject':'vendor-a'},'count':'3','base':'10','unit':'answers','label':'Fictional test observation','source_review_sha256':'a'*64}
        fid=q.figure_key(record)
        note={'bank_id':'LB-Q9000','source_sha256':p['source_sha256'],'canonical_source_sha256':p['canonical_source_sha256'],'opening_sha256':p['opening_sha256'],
              'opening_shape':'shape0','classification_reason':'Fictional vendor subject leads.',
              'writing_review_sha256':'a'*64,'source_review_sha256':'a'*64,'lead_figures':[fid],
              'lead_figure_spans':{fid:['3 of 10']}}
        shapes={f'shape{i}':'Fictional declared structure '+str(i) for i in range(8)}
        meta={'schema_version':1,'pages':{'a':note},'shape_definitions':shapes,
              'cluster_plans':{'measurement':list(shapes)},'figures':{fid:record}}
        self.assertEqual(q.validate_annotations({'a':p},meta),meta['pages'])
        p['opening_sha256']='c'*64
        with self.assertRaisesRegex(ValueError,'opening changed'):q.validate_annotations({'a':p},meta)
        p['opening_sha256']='b'*64;note['lead_figure_spans'][fid]=['unprinted count']
        with self.assertRaisesRegex(ValueError,'actual opening'):q.validate_annotations({'a':p},meta)

    def test_frozen_exception_count_cannot_be_inflated(self):
        pages,baseline,trusted=baseline_fixture();names=list(pages)[:5]
        row=q.fact('opening_concentration',names,cluster='measurement',shape='figure_first',count=5,total=10)
        row['key']='opening_concentration:measurement:figure_first'
        baseline['exceptions'][row['key']]=row;self.seal_fixture_cases(baseline,trusted)
        baseline['exceptions'][row['key']]['count']=999
        with self.assertRaisesRegex(ValueError,'baseline cases/counts differ'):
            q.apply_baseline({'violations':[row]},pages,baseline,trusted)

    def test_tampered_frozen_snapshot_fails_even_at_same150_count(self):
        pages,baseline,trusted=baseline_fixture();name=next(iter(baseline['frozen_pages']))
        baseline['frozen_pages'][name]['opening_shape']='relabelled'
        with self.assertRaisesRegex(ValueError,'trusted hash'):
            q.apply_baseline({'violations':[]},pages,baseline,trusted)

    def test_private_host_agent_paths_and_raw_audit_fields_are_rejected(self):
        for value in ({'path':'C:/Users/example/private.json'}, {'reviewer':'/root/reviewer'}, {'thread_id':'private'}):
            with self.assertRaisesRegex(ValueError,'Private host/agent/thread'):
                q.public_metadata(value)
        with self.assertRaisesRegex(ValueError,'Unknown/private'):
            q.validate_annotations({}, {'schema_version':1,'raw_queries':['private source context']})


class RepositoryQualityTests(unittest.TestCase):
    def test_current_library_passes_only_its_frozen_specific_baseline(self):
        result=q.run(ROOT/'docs',q.read_json(ROOT/'tools/library_quality_annotations.json'),q.read_json(ROOT/'tools/library_quality_baseline.json'))
        self.assertTrue(result['passed'],json.dumps(result.get('errors',[]),ensure_ascii=False)[:4000])
        self.assertEqual(result['new_page_exceptions'],0)


if __name__=='__main__':
    unittest.main()
