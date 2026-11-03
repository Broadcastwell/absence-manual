"""Meaningful independent-scope regressions; no real page approval."""
import copy,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from library_publication_overlay import QUALIFIER,current_comparison_prose,sha,OverlayError
from library_publication_release import state_fingerprint,full_report_binding
from library_publication_both_scopes import attach_literal_scope,validate_scope_union,POLICY
from test_publication_overlay import q
from test_publication_release import StateFixture


def word(prefix,n):
    return prefix+chr(97+n//26)+chr(97+n%26)


class BothScopeTests(unittest.TestCase):
    def test_literal_only_similarity_survives_qualifier_removal_runtime_clear(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs=Path(tmp);hub=docs/'answers/measurement/index.md';hub.parent.mkdir(parents=True)
            records={};notes={};paths=['answers/measurement/a.md','answers/measurement/b.md']
            for i,path in enumerate(paths):
                title='Distinct '+('first' if i==0 else 'second')+' question?'
                opening=' '.join(word('open'+('alpha' if i==0 else 'bravo'),j) for j in range(12))
                shared=' '.join(word('shared',j) for j in range(24));unique=' '.join(word('left' if i==0 else 'right',j) for j in range(90))
                body='# '+title+'\n\n'+opening+'.\n\n'+QUALIFIER+'\n\n'+shared+' '+unique+'.\n'
                meta={'title':title,'headline':title,'description':'A unique '+str(i)+' description.','also_asked_as':[]}
                records[path]={'path':path,'body':body,'meta':meta,'cluster':'measurement','effective_canonical_source_sha256':sha(body.encode())}
                notes[path]={'canonical_source_sha256':sha(body.encode()),'opening_sha256':sha((opening+'.').encode()),'opening_shape':'first' if i==0 else 'second','lead_figures':['fixture'+str(i)]}
            hub.write_text('\n'.join('- [Page]('+p.rsplit('/',1)[1]+')' for p in paths)+'\n',encoding='utf-8')
            overlay=SimpleNamespace(records=records,q=q,docs=docs,_check_unchanged=lambda:None)
            state={'routes':{('/'+p[:-3]+'/'):{'kind':'article','path':p,'compiled_sha256':sha(p.encode())} for p in paths},'raw_source_pins':{p:sha(p.encode()) for p in paths}}
            runtime_pages={}
            for p,r in records.items():
                op=q.paragraph_after_heading(r['body']).strip();comp=current_comparison_prose(r['body'],q)
                runtime_pages[p]={**r,'opening':op,'six':q.sequences(q.words(comp),6),'eight':q.sequences(q.words(q.comparison_prose(op)),8)}
            orders,errors=q.hub_orders(docs,runtime_pages);self.assertEqual([],errors)
            a=q.analyze(runtime_pages,notes,orders,[],docs)
            self.assertFalse(any(v['kind']=='six_word_similarity' for v in a['violations']))
            report={**a,**full_report_binding(state,q),'analysis_completed':True,'all_pairs_compared':True,'pair_count':1,'baseline_exceptions':0,'actual_hub_orders':orders,'global_fatal_errors':[],'page_readiness':{p:{'passed':True,'status':'PASS','errors':[]} for p in paths}}
            result=attach_literal_scope(overlay,state,current_annotations={'pages':notes,'index_question_titles':{'records':[]}},runtime_report=report)
            self.assertTrue(any(v['kind']=='six_word_similarity' for v in result['comparison_scopes']['literal']['violations']))
            self.assertTrue(any(v['key'].startswith('literal:') and v['kind']=='six_word_similarity' for v in result['violations']))
            self.assertFalse(result['passed']);self.assertFalse(result['page_readiness'][paths[0]]['passed']);self.assertTrue(validate_scope_union(result,state,q))
            tampered=copy.deepcopy(result);tampered['violations']=[v for v in tampered['violations'] if not v['key'].startswith('literal:')]
            with self.assertRaisesRegex(OverlayError,'hides or conflates'):validate_scope_union(tampered,state,q)

    def test_old_runtime_violation_cannot_hide_new_or_worse_literal_violation(self):
        with tempfile.TemporaryDirectory() as tmp:
            fx=StateFixture(tmp)
            for old_fraction in [None,'21/100']:
                old_literal=[] if old_fraction is None else [dict(fx.old_violation,key='literal:fixture-old-pair',comparison_scope='original_literal_q',score_fraction=old_fraction)]
                fx.prior['current_quality_snapshot']['violations']=[fx.old_violation]+old_literal;fx.save()
                new_literal=dict(fx.old_violation,key='literal:fixture-old-pair',comparison_scope='original_literal_q',score_fraction='22/100')
                # Runtime remains25%, which is higher than either literal ratio.
                fx.report=fx.make_report(violations=[fx.old_violation,new_literal]);result=fx.gate()
                self.assertFalse(result['incremental_release_passed'])
                self.assertTrue(any(isinstance(e,dict) and e.get('kind')=='new_or_worse_untouched_violation' and e['violation']['key'].startswith('literal:') for e in result['errors']))

    def test_missing_scope_or_pair_coverage_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            fx=StateFixture(tmp);report=fx.report
            with self.assertRaisesRegex(OverlayError,'Both-scope'):validate_scope_union(report,fx.current,q)
            report=copy.deepcopy(report);report['comparison_policy']=POLICY;report['comparison_scopes']={'runtime':{'all_pairs_compared':True,'pair_count':28,'violations':report['violations']},'literal':{'all_pairs_compared':True,'pair_count':27,'violations':[]}}
            with self.assertRaisesRegex(OverlayError,'Incomplete'):validate_scope_union(report,fx.current,q)


if __name__=='__main__':unittest.main()
