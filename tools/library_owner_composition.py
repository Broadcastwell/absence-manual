"""Owner-only inherited NULL-five admission; never footer or S5 approval."""
from pathlib import Path
import copy,hashlib,json,re,zipfile

CATALOG_SHA256='a3ded5ba7e8b21da2dacecd35f70b89ae62cbaa8f32307b0958e4c67bfa52d94'
POLICY='OWNER_EXACT_INHERITED_NULL_METHOD5_V1'
_TOKEN=object()
sha=lambda raw:hashlib.sha256(raw).hexdigest()
def digest(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def need(v,m):
    if not v:raise ValueError(m)
def catalog():
    raw=Path(__file__).with_name('library_owner_composition_cases.json').read_bytes()
    need(sha(raw)==CATALOG_SHA256,'Owner NULL-five catalog changed')
    c=json.loads(raw)
    need(len(c['answer_cases24'])==24 and len(c['prior_FAIL22'])==22
        and len(c['ordinary_prior_PASS2'])==2 and len(c['inherited_null_method5'])==5
        and set(c['inherited_null_method5'])<=set(c['prior_FAIL22']),
        'Owner NULL-five finite scope differs')
    return c
def footer_span(body):
    marker='Prepared by the Broadcastwell team.'
    need(body.count('## Next step\n')==1 and body.count(marker)==1,'Owner inherited footer boundary differs')
    a=body.index('## Next step\n');b=body.index(marker,a)+len(marker)
    return body[a:b]


def check_case(path,before,revision,readiness,scoped_ids,ordinary_ids,ledger_sha):
    """Exact finite case projection, independent of approval flags."""
    c=catalog();expected=c['answer_cases24'].get(path)
    need(expected is not None,'Owner composition case not in exact24')
    after=revision['payload']
    actual={'prior_status':readiness.get('status'),
        'before_full_sha256':sha(before['effective_full_source'].encode()),
        'after_full_sha256':revision['after_effective_canonical_sha256'],
        'after_body_sha256':revision['after_body_sha256'],
        'after_meta_sha256':revision['after_metadata_sha256'],
        'footer_contract_sha256':digest(before.get('footer_contract')),
        'footer_contract_present':'footer_contract' in before,
        'footer_span_sha256':sha(footer_span(before['body']).encode()),
        'scoped_review_ids':scoped_ids,'ordinary_review_ids':ordinary_ids,
        'ledger_sha256':ledger_sha,'source_kind':before.get('source_kind'),
        'is_based_on':before['meta'].get('is_based_on')}
    need(actual==expected,'Owner composition exact before/after/ledger/peer/status case differs: '+path)
    need(('footer_contract' in before)==('footer_contract' in after)
        and before.get('footer_contract')==after.get('footer_contract')
        and footer_span(before['body'])==footer_span(after['body']),
        'Owner repair changes an inherited whole footer contract or span')
    need(after.get('source_kind')==before.get('source_kind')
        and after['meta'].get('is_based_on')==before['meta'].get('is_based_on'),
        'Owner NULL-five cannot transfer source kind or method basis')
    need(sha(after['effective_full_source'].encode())==actual['after_full_sha256']
        and sha(after['body'].encode())==actual['after_body_sha256']
        and digest(after['meta'])==actual['after_meta_sha256'],
        'Owner after payload full/body/meta disagrees with actual case')
    if path in c['ordinary_prior_PASS2']:
        need(readiness.get('passed') is True and after.get('review_ids')==ordinary_ids
            and set(ordinary_ids or{})=={'source','writing'}
            and all(ordinary_ids[k]!=scoped_ids[k] for k in ['source','writing']),
            'Owner prior-PASS pages need separate ordinary full-article IDs')
    else:
        need(readiness.get('status')=='FAIL' and readiness.get('passed') is False
            and after.get('review_ids')==scoped_ids,'Owner scoped receipt is not a prior-FAIL identity')
    if path in c['inherited_null_method5']:
        need(isinstance(after.get('footer_contract'),dict)
            and after['footer_contract'].get('method_token') is None,
            'Owner NULL-five admission is only inherited None, never a string')
    return actual


class OwnerNullMethodPermit:
    def __init__(self,evidence,pins,owner,post,token):
        need(token is _TOKEN,'Owner NULL-five permit requires independently checked Root inputs')
        self._evidence=copy.deepcopy(evidence);self._pins=tuple(pins)
        self._owner=owner;self._post=post
        self._seal=digest(self._evidence);self._seen=set()
    def assert_current(self):
        need(self._seal==digest(self._evidence),'Owner NULL-five permit mutated')
        self._owner.assert_current();self._post.check()
        for name,pin in self._pins:
            need(sha(Path(name).read_bytes())==pin,'Owner NULL-five bound file changed: '+name)
    def assert_context(self,*,prior,payload_bundle,active_plan,actual_binding,frozen_paths):
        self.assert_current();e=self._evidence
        need(digest(prior)==e['prior_object_sha256'] and digest(payload_bundle)==e['payload_object_sha256']
            and digest(active_plan)==e['active_object_sha256'] and actual_binding==e['production_binding']
            and sorted(frozen_paths)==e['frozen_paths45'],
            'Owner NULL-five permit belongs to a different actual composition')
    def admit_inherited_null(self,path,before,revision):
        self.assert_current();c=catalog()
        need(path in c['inherited_null_method5'],'Owner permit cannot defer a string/other FAIL/PASS method')
        expected=c['answer_cases24'][path];after=revision['payload']
        need(self._evidence['cases24'][path]==expected
            and sha(before['effective_full_source'].encode())==expected['before_full_sha256']
            and sha(after['effective_full_source'].encode())==expected['after_full_sha256']
            and after.get('footer_contract')==before.get('footer_contract')
            and digest(after.get('footer_contract'))==expected['footer_contract_sha256']
            and after['footer_contract'].get('method_token') is None
            and sha(footer_span(before['body']).encode())==sha(footer_span(after['body']).encode())==expected['footer_span_sha256'],
            'Owner inherited NULL-five after/footer/span no longer exact')
        self._seen.add(path)
    def assert_complete(self):
        self.assert_current()
        need(self._seen==set(catalog()['inherited_null_method5']),
            'Owner NULL-five admission did not consume exactly the actual five')


def prepare_evidence(docs,inputs,inputs_sha256):
    """Pure bound reads only; no BuildSession, staging or permit is created."""
    from library_owner_repair_build import bound_file
    from library_owner_repair import OwnerRepairPlan,validate_before_read_receipt,exact_edits
    from library_owner_repair_post_s5 import bind_post_s5
    from library_owner_repair_consumers import repair_ledger,validate_peer,json_hash
    from library_publication_composition import bind_prior_production
    import library_quality as q
    import library_related_chapter_links as finite
    docs=Path(docs).resolve();path=Path(inputs).resolve();root=path.parent;pins=[]
    raw=path.read_bytes();need(sha(raw)==inputs_sha256,'Owner NULL-five input bytes differ')
    config=json.loads(raw);pins.append((str(path),inputs_sha256))
    def load(ref,base=root):
        p,b=bound_file(base,ref);pins.append((str(p),sha(b)));return b
    base_raw=load(config['base_inputs']);base=json.loads(base_raw)
    base_root=(root/config['base_inputs']['path']).parent
    base_raws={n:load(ref,base_root) for n,ref in base['files'].items()}
    need(sha(Path(q.__file__).read_bytes()) in (base['quality_module_sha256'] if isinstance(base['quality_module_sha256'],list) else [base['quality_module_sha256']])
        and sha(Path(finite.__file__).read_bytes())==base['finite_module_sha256'],
        'Owner primitive checker quality/finite module differs from actual base')
    prior=json.loads(base_raws['prior_state']);bundle=json.loads(base_raws['prior_payload']);active=json.loads(base_raws['active_revisions'])
    leaves=json.loads(base_raws['current_leaf_manifest']);merges=json.loads(base_raws['merges'])
    producer_raw=base_raws['production_receipt'];producer=json.loads(producer_raw)
    with zipfile.ZipFile(Path(base_root/base['files']['prior_artifact']['path'])) as archive:
        public={n:archive.read(n) for n in archive.namelist() if not n.endswith('/')}
    need(sha(base_raws['prior_artifact'])==base['actual_prior_production_binding']['artifact_sha256'],'Owner prior artifact binding differs')
    artifacts={}
    for route,row in prior['routes'].items():
        if row['kind']=='redirect':continue
        name=route.strip('/')+'/index.html' if route.endswith('/') else route.lstrip('/')
        artifacts[route]=public[name]
    bind_prior_production(prior=prior,payloads=bundle['pages'],actual_artifacts=artifacts,
        actual_binding=base['actual_prior_production_binding'],receipt=producer,q=q,
        payload_file_sha256=base['files']['prior_payload']['sha256'])
    post_raw=load(config['post_s5_context'])
    post=bind_post_s5(post_raw,config['post_s5_context']['sha256'],producer_raw=producer_raw,
        prior=prior,payload=bundle,leaves=leaves,new_merges=merges,input_files=base['files'],
        actual_binding=base['actual_prior_production_binding'])
    plan_raw=load(config['owner_source_plan']);plan=json.loads(plan_raw)
    need(sha(plan_raw)==config['owner_source_plan_sha256'] and plan['base_inputs_sha256']==sha(base_raw),
        'Owner source plan/base reference differs')
    owner=OwnerRepairPlan.bind(plan_raw,sha(plan_raw),authority_read_receipt=load(config['authority_read_receipt']),
        registry_bytes=load(config['freeze_registry']),handoff_bytes=load(config['freeze_handoff']),nav_map_bytes=load(config['freeze_nav_map']),
        actual_prior_binding=base['actual_prior_production_binding'],actual_answer_paths=post.pages,
        actual_research_paths={p.relative_to(docs).as_posix() for p in (docs/'research').rglob('*.md')},
        bank_ids={p:json.loads(base_raws['current_pins'])['pages'][p]['bank_id'] for p in post.pages},post_s5_binding=post)
    before_raw=load(config['root_current_before_read_receipt'])
    need(sha(before_raw)==plan['root_current_before_read_receipt_sha256'],'Owner actual Root before48 differs')
    validate_before_read_receipt(before_raw,sha(before_raw),plan=owner,actual_prior_files=public)
    for rel,row in plan.get('approved_code_changes',{}).items():
        file=(docs.parent/rel).resolve()
        need(file.is_relative_to(docs.parent) and file.is_file() and sha(file.read_bytes())==row['after_sha256'],
            'Owner actual Root-reviewed code/config bytes differ')
        pins.append((str(file),row['after_sha256']))
    c=catalog();need(plan['source_changes']==c['source_changes49']
        and set(config['source_inputs'])==set(c['source_changes49']),'Owner exact49/43 catalog differs')
    for source,note in plan['source_changes'].items():
        after_raw=load(config['source_inputs'][source]['after_source'])
        need(sha(after_raw)==note['after_sha256'],'Owner exact49 after source bytes differ')
        if not source.startswith('docs/answers/'):
            actual=docs.parent/source;need(actual.is_file() and actual.read_bytes()==after_raw,'Owner actual nonanswer after source differs')
            pins.append((str(actual),sha(after_raw)))
    store={sha(producer_raw):producer_raw}
    for ref in base.get('receipt_files',[]):
        b=load(ref,base_root);store[sha(b)]=b
    for ref in config.get('receipt_files',[]):
        b=load(ref);store[sha(b)]=b
    cases={};ready=prior['current_quality_snapshot']['page_readiness']
    need(set(active.get('pages',{}))==set(c['answer_cases24']) and active.get('approved') is True,'Owner exact24 active revision scope differs')
    for rel,revision in active['pages'].items():
        before=bundle['pages'][rel];bound=config['source_inputs']['docs/'+rel];after_raw=load(bound['after_source'])
        meta,body=finite.source_body(after_raw.decode());payload=revision['payload']
        need(payload['effective_full_source']==after_raw.decode() and payload['meta']==meta and payload['body']==body,
            'Owner active payload is not the actual approved after file')
        ledger_raw=load(bound['change_ledger']);ledger=json.loads(ledger_raw)
        need(json_hash(ledger)==sha(ledger_raw) and ledger==repair_ledger(rel,before,after_raw.decode(),ledger['body_edits'],meta),
            'Owner exact24 forward/inverse metadata/body ledger differs')
        need(exact_edits(before['body'].encode(),ledger['body_edits']).decode()==body,
            'Owner pre-composition literal forward replay differs')
        reverse=[{'old':e['new'],'new':e['old'],'old_sha256':e['new_sha256'],'new_sha256':e['old_sha256']}
            for e in reversed(ledger['body_edits'])]
        need(exact_edits(body.encode(),reverse).decode()==before['body'],
            'Owner pre-composition literal reverse replay differs')
        record={'path':rel,'raw_canonical_source_sha256':revision['raw_canonical_source_sha256'],
            'before_effective_canonical_source_sha256':sha(before['effective_full_source'].encode()),
            'effective_full_source':after_raw.decode(),'meta':meta,'body':body}
        prior_pass=ready[rel].get('passed') is True
        for kind,key in bound['review_ids'].items():
            need(key in store,'Owner exact scoped Source/Writing bytes missing')
            validate_peer(store[key],key,record,kind,sha(ledger_raw),prior_S5_pass=prior_pass)
        ordinary=bound.get('ordinary_review_ids')
        if prior_pass:
            for kind in ['source','writing']:
                key=ordinary[kind];peer=json.loads(store[key])
                need(sha(store[key])==key and peer.get('approved') is True and peer.get('actual_full_read_complete') is True
                    and peer.get('review_kind')==kind and peer.get('scope')=='full-effective-article'
                    and peer.get('path')==rel and peer.get('canonical_source_sha256')==record['raw_canonical_source_sha256']
                    and peer.get('effective_canonical_source_sha256')==sha(after_raw),
                    'Owner prior-PASS distinct ordinary full article check missing')
        cases[rel]=check_case(rel,before,revision,ready[rel],bound['review_ids'],ordinary,sha(ledger_raw))
    projection={k:v for k,v in config.items() if k!='owner_composition_review'}
    frozen=sorted(owner.freeze_data['pages'])
    evidence={'policy':POLICY,'catalog_sha256':CATALOG_SHA256,
        'config_projection_sha256':digest(projection),'base_inputs_sha256':sha(base_raw),
        'owner_source_plan_sha256':sha(plan_raw),'post_s5_context_sha256':sha(post_raw),
        'Root_current_before_read_sha256':sha(before_raw),'production_receipt_sha256':sha(producer_raw),
        'production_binding':base['actual_prior_production_binding'],
        'prior_object_sha256':digest(prior),'payload_object_sha256':digest(bundle),'active_object_sha256':digest(active),
        'source49_catalog_sha256':digest(plan['source_changes']),'frozen_paths45':frozen,'cases24':cases,
        'prior_FAIL22':c['prior_FAIL22'],'ordinary_prior_PASS2':c['ordinary_prior_PASS2'],
        'inherited_NULL5':c['inherited_null_method5'],'normal_string_method_checks_preserved':True}
    return evidence,list(dict(pins).items()),owner,post


def bind_owner_composition(docs,inputs,inputs_sha256):
    evidence,pins,owner,post=prepare_evidence(docs,inputs,inputs_sha256)
    from library_owner_repair_build import bound_file
    config=json.loads(Path(inputs).read_bytes());ref=config.get('owner_composition_review')
    need(ref is not None,'Explicit Root Owner NULL-five composition review missing')
    file,raw=bound_file(Path(inputs).resolve().parent,ref);review=json.loads(raw)
    check_Root_review(review,evidence)
    pins.append((str(file),sha(raw)))
    return OwnerNullMethodPermit(evidence,pins,owner,post,_TOKEN)


def check_Root_review(review,evidence):
    need(review.get('approved') is True and review.get('reviewer')=='root'
        and review.get('review_kind')=='root-exact-owner-inherited-null5-composition'
        and review.get('policy')==POLICY and review.get('composition_evidence_sha256')==digest(evidence)
        and review.get('ordinary_S5_or_footer_validity_approval') is False,
        'Actual Root exact Owner NULL-five composition review absent or stale')
    return True


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description='Derive exact evidence and a false Root review template; never issue a permit.')
    p.add_argument('--docs',required=True);p.add_argument('--inputs',required=True)
    p.add_argument('--inputs-sha256',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();evidence,_,_,_=prepare_evidence(a.docs,a.inputs,a.inputs_sha256)
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    (out/'COMPOSITION_EVIDENCE.json').write_text(json.dumps(evidence,ensure_ascii=False,sort_keys=True,separators=(',',':')),encoding='utf-8',newline='\n')
    review={'approved':False,'reviewer':'root','review_kind':'root-exact-owner-inherited-null5-composition',
        'policy':POLICY,'composition_evidence_sha256':digest(evidence),'ordinary_S5_or_footer_validity_approval':False}
    (out/'ROOT_COMPOSITION_REVIEW.NOT_APPROVED.json').write_text(json.dumps(review,sort_keys=True,separators=(',',':')),encoding='utf-8',newline='\n')
    print(json.dumps({'approved':False,'evidence_sha256':digest(evidence),'permit_issued':False}))
