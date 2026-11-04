"""Actual internal target-only shape, synthetic307/19 fixture authority only."""
from pathlib import Path
from types import SimpleNamespace
import copy,importlib.util,json,tempfile,unittest
import library_owner_repair_post_s5 as current
from test_owner_post_s5_contract import fixture,raw
H=Path(__file__).resolve().parents[1]
oldpath=H/'tests/fixtures/owner_required28/original_post_s5_v2.py'
spec=importlib.util.spec_from_file_location('_sealed_original_OwnerV2',oldpath)
original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)

def make_session(root):
    c,v,o,files,_,decisions=fixture()
    o._new_merge_plan={};o._merge_plan={p:{'target_path':r['target_path']} for p,r in o.merge_statuses.items()}
    values={'production_receipt':v['producer_raw'],'prior_state':raw(v['prior']),'prior_payload':raw(v['payload']),'current_leaf_manifest':raw(v['leaves']),'merges':raw(v['new_merges'])}
    paths={}
    for name,value in values.items():
        path=root/(name+'.json');path.write_bytes(value);paths[name]=path
    context=root/'context.json';context.write_bytes(raw(c))
    config={'post_s5_context':{'path':'context.json','sha256':current.sha(raw(c))}}
    archive=SimpleNamespace(namelist=lambda:list(files),read=lambda p:files[p])
    s=SimpleNamespace(overlay=o,prior=v['prior'],inputs={'files':v['input_files'],'actual_prior_production_binding':v['actual_binding']},_file=lambda n:paths[n],archive=archive)
    return s,config,lambda ref:(context,context.read_bytes()),files,decisions

class TargetOnlyPlanTests(unittest.TestCase):
    def test_original_sealedV2_control_rejects_real_internal_shape(self):
        with tempfile.TemporaryDirectory() as t:
            s,c,l,_,_=make_session(Path(t))
            with self.assertRaisesRegex(ValueError,'retain exact inherited19'):original.bind_session_context(s,c,l)
    def test_current_accepts_targets_with_full_disposition_and_original19_closure(self):
        with tempfile.TemporaryDirectory() as t:
            s,c,l,_,_=make_session(Path(t));b=current.bind_session_context(s,c,l)
            self.assertEqual(19,len(b.stubs));self.assertEqual(307,len(b.pages))
    def test_missing_extra_target_new_merge_reject(self):
        for mode in ['missing','extra','target','new']:
            with tempfile.TemporaryDirectory() as t:
                s,c,l,_,_=make_session(Path(t));plan=s.overlay._merge_plan
                if mode=='missing':plan.pop(next(iter(plan)))
                elif mode=='extra':plan['answers/x/unreviewed.md']={'target_path':current.LEGAL}
                elif mode=='target':plan[next(iter(plan))]={'target_path':'answers/x/wrong.md'}
                else:s.overlay._new_merge_plan={'answers/x/new.md':{}}
                with self.subTest(mode=mode),self.assertRaises(ValueError):current.bind_session_context(s,c,l)
    def test_full_disposition_decision_and_stub_bytes_remain_strict(self):
        for mode in ['full','decision','stub']:
            with tempfile.TemporaryDirectory() as t:
                s,c,l,files,decisions=make_session(Path(t))
                if mode=='full':
                    s.overlay.merge_statuses=copy.deepcopy(s.overlay.merge_statuses)
                    s.overlay.merge_statuses[next(iter(s.overlay.merge_statuses))]['article_pass']=True
                elif mode=='decision':decisions.pop(next(iter(decisions)))
                else:files[next(p for p in files if 'retired' in p)]+=b' '
                with self.subTest(mode=mode),self.assertRaises(ValueError):current.bind_session_context(s,c,l)

if __name__=='__main__':unittest.main(verbosity=2)
