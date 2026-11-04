"""Replay only the five previously published discovery descriptions.

Legacy PR93 and current Owner's PR93 baseline have no declaration and remain
identical. A future actual producer must carry the original separately dated
Root/Source/Writing authority. No future producer approval is supplied here.
"""
import copy,json
from library_owner_discovery_consumer_five import (catalog,CATALOG_SHA256,KIND,
    HUB_DATE_EVENT_SHA256,checked_hub_date_event,jhash,leaf_stamp,project_hubs,project_llms,frozen_search_exact)
from library_owner_repair import require,sha,POLICY

SOURCE='a3e37e7aed2c25a954545894ee87fdc30386320287cb4ae020eddc108b5f784c'
WRITING='0fd33e3708bfd686ed81b83c84e3356d42b6c17f3d3b788450afe0ffa1befe21'
PLAN='d67d3d912436efc72c31ef73d163878726dc2df7059cd98edfed18112afb5fb5'
KEY='published_discovery_consumer_five'
_TOKEN=object()

def authority_bytes(overlay,digest):
    # The owning loader returns a checked JSON object, not its original bytes.
    require(overlay._load_receipt(digest) is not None,'Published consumer5 authority is missing or invalid')
    raw=overlay.receipt_store.get(digest)
    require(isinstance(raw,bytes) and sha(raw)==digest,'Published consumer5 authority bytes differ')
    return raw

def expected_tuples(c,date_event):
    return {p:{'body_sha256':r['after_body_sha256'],'metadata_sha256':date_event['hub_metadata'][p]['after_meta_sha256']}for p,r in c['hubs'].items()}

def recipe(*,producer_raw,inputs,registry,hubs,prior_hub_bundle,prior_hub_file_sha256,
           actual_prior_archive,frozen_paths):
    """Pure read/check recipe; caller already bound the actual prior producer.

    Every original authority is loaded by digest from that producer's declared
    store, never from a caller's unchecked path or a historical local pointer.
    """
    producer=json.loads(producer_raw);declared=producer.get(KEY);c=catalog()
    prior_hubs=(prior_hub_bundle or {}).get('hubs',{})
    published_signals=(sha(actual_prior_archive.read('llms.txt'))==c['llms_after_sha256']
        or any(p in prior_hubs and sha(prior_hubs[p]['body'].encode())==r['after_body_sha256']for p,r in c['hubs'].items()))
    if declared is None:
        require(not published_signals,'Published consumer5 baseline cannot drop its producer declaration')
        return None
    require(isinstance(declared,dict) and set(declared)=={
        'schema_version','policy','catalog_sha256','consumer_plan_sha256','Root_review_sha256',
        'Source_review_sha256','Writing_review_sha256','historical_public_before_sha256',
        'owner_source_plan_sha256','hub_date_event_sha256','published_hub_tuples','published_llms_sha256'},
        'Published consumer5 declaration schema differs')
    require(declared['schema_version']==1 and declared['policy']==KIND
        and declared['catalog_sha256']==CATALOG_SHA256 and declared['consumer_plan_sha256']==PLAN
        and declared['Source_review_sha256']==SOURCE and declared['Writing_review_sha256']==WRITING
        and declared['hub_date_event_sha256']==HUB_DATE_EVENT_SHA256,
        'Published consumer5 catalog/actual peer identity differs')
    require(producer.get('approved') is True and producer.get('review_kind')=='prior-production-effective-payload'
        and producer.get('production_binding')==inputs['actual_prior_production_binding']
        and producer.get('actual_served_readback') is True and producer.get('source_render_equality_passed') is True
        and producer.get('hub_source_render_equality_passed') is True,
        'Published consumer5 requires an actually approved current production producer')
    require(len(registry.records)==307 and len(frozen_paths)==45 and set(inputs['frozen_effective_pins'])==set(frozen_paths),
        'Published consumer5 needs exact current307/frozen45')
    require(producer.get('hub_payload_bundle_sha256')==prior_hub_file_sha256
        and producer.get('hub_payload_canonical_json_sha256')==jhash(prior_hub_bundle)
        and producer.get('hub_raw_source_git_proof_passed') is True
        and producer.get('hub_raw_source_pins')=={p:r['raw_canonical_source_sha256']for p,r in prior_hubs.items()},
        'Published consumer5 prior hub bundle/raw-Git proof is not the approved producer tuple')
    require(len(prior_hubs)==len(hubs)==12 and set(prior_hubs)==set(hubs)
        and declared['published_llms_sha256']==c['llms_after_sha256']
        and sha(actual_prior_archive.read('llms.txt'))==declared['published_llms_sha256'],
        'Published consumer5 actual prior discovery scope differs')
    refs={k:declared[k]for k in ['Root_review_sha256','Source_review_sha256','Writing_review_sha256',
        'historical_public_before_sha256','owner_source_plan_sha256','consumer_plan_sha256','hub_date_event_sha256']}
    raw={k:authority_bytes(registry.overlay,v)for k,v in refs.items()}
    require(all(sha(raw[k])==v for k,v in refs.items()),'Published consumer5 authority store bytes differ')
    values={k:json.loads(v)for k,v in raw.items()};plan=values['consumer_plan_sha256']
    date_event=checked_hub_date_event(raw['hub_date_event_sha256'],c)
    require(declared['published_hub_tuples']==expected_tuples(c,date_event),'Published consumer5 original actual dated hub tuple differs')
    require(plan=={'schema_version':1,'policy':KIND,'catalog_sha256':CATALOG_SHA256,
        'hubs':c['hubs'],'llms_before_sha256':c['llms_before_sha256'],'llms_after_sha256':c['llms_after_sha256']},
        'Published consumer5 original exact data plan differs')
    for kind,key in [('source','Source_review_sha256'),('writing','Writing_review_sha256')]:
        peer=values[key]
        require(peer.get('approved') is True and peer.get('review_kind')==kind
            and peer.get('scope')=='owner-exact-discovery-consumer-five' and peer.get('policy')==POLICY
            and peer.get('catalog_sha256')==CATALOG_SHA256 and peer.get('consumer_plan_sha256')==PLAN
            and peer.get('complete_hub_before_after_read') is True and peer.get('five_exact_descriptions_reviewed') is True
            and peer.get('leaf_source_metadata_or_ordinary_S5_approval') is False,
            'Published consumer5 actual narrow Source/Writing scope differs')
    root=values['Root_review_sha256'];owner=values['owner_source_plan_sha256'];before=values['historical_public_before_sha256']
    require(root.get('approved') is True and root.get('reviewer')=='root'
        and root.get('review_kind')=='root-exact-discovery-consumer-five' and root.get('policy')==POLICY
        and root.get('catalog_sha256')==CATALOG_SHA256 and root.get('consumer_plan_sha256')==PLAN
        and root.get('owner_source_plan_sha256')==declared['owner_source_plan_sha256']
        and root.get('Source_review_sha256')==SOURCE and root.get('Writing_review_sha256')==WRITING
        and root.get('actual_public_before_receipt_sha256')==declared['historical_public_before_sha256']
        and root.get('hub_date_event_sha256')==HUB_DATE_EVENT_SHA256
        and root.get('full_two_hub_before_after_actually_read') is True
        and root.get('dated_global_consumer_truth_correction_no_field_treatment') is True
        and root.get('leaf_or_frozen_leaf_search_treatment_approval') is False,
        'Original actual Root consumer5 authority is absent or foreign')
    import re
    require(re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00',str(root.get('actual_private_adoption_utc'))),
        'Original consumer5 authority lacks its actual dated event')
    require(owner.get('approved') is True and owner.get('review_kind')=='root-exact-owner-repair-source-plan'
        and owner.get('kind')==POLICY and owner.get('article_count')==307
        and owner.get('discovery_consumer_five')=={'catalog_sha256':CATALOG_SHA256,'plan_sha256':PLAN}
        and len(owner.get('source_changes',{}))==49,
        'Original approved Root Source49 consumer declaration differs')
    require(before.get('read_kind')=='actual-scripts-off-current-public-before-Consumer5'
        and before.get('current_production')==owner['baseline_production_binding']['commit_sha']
        and before.get('all_exact') is True and before.get('expected')==before.get('actual')==3,
        'Original historical public-before authority differs; it is not the future production proof')
    for row in c['rows']:
        p=row['leaf_path'];record=registry.records[p]
        require(p in frozen_paths and 'docs/'+p not in owner['source_changes']
            and sha(record['effective_full_source'].encode())==row['leaf_effective_canonical_sha256']==inputs['frozen_effective_pins'][p]
            and sha(record['body'].encode())==row['leaf_body_sha256'] and jhash(record['meta'])==row['leaf_metadata_sha256']
            and record['meta']['description']==row['old_description'],
            'Published consumer5 changed the frozen leaf/source metadata')
    after=project_hubs(hubs,c,date_event,allow_published_metadata=True)
    for p,r in c['hubs'].items():
        prior=prior_hubs[p];expected=owner['generated_hubs'].get('docs/'+p,{})
        require(prior['body']==after[p]['body'] and prior['meta']==after[p]['meta']
            and sha(prior['effective_full_source'].encode())==prior['canonical_source_sha256']
            and registry.overlay.finite.source_body(prior['effective_full_source'])==(prior['meta'],prior['body'])
            and expected=={'effective_body_sha256':r['after_body_sha256'],'effective_meta_sha256':date_event['hub_metadata'][p]['after_meta_sha256']},
            'Published consumer5 exact current hub tuple/original Root approval differs')
    require(all(after[p]['body']==r['body'] and after[p]['meta']==r['meta'] for p,r in prior_hubs.items()),
        'Published consumer5 replay cannot silently change another current hub tuple')
    return {'declaration':copy.deepcopy(declared),'authority_refs':refs,'after_hubs':after,
        'producer_sha256':sha(producer_raw),'production_binding':copy.deepcopy(inputs['actual_prior_production_binding'])}

class PublishedConsumerFive:
    def __init__(self,token,registry,checked,frozen_paths):
        require(token is _TOKEN,'Published consumer5 needs actual checked producer authority')
        self.registry=registry;self.checked=copy.deepcopy(checked);self.frozen_paths=set(frozen_paths)
        self.records_stamp=leaf_stamp(registry.records);self._stamp=jhash([self.checked,sorted(self.frozen_paths)])
    def check(self):
        self.registry.assert_current()
        require(self._stamp==jhash([self.checked,sorted(self.frozen_paths)]) and leaf_stamp(self.registry.records)==self.records_stamp,
            'Published consumer5 bound inputs or frozen leaf records changed')
        require(self.registry.hubs==self.checked['after_hubs'],'Published consumer5 hubs changed after checked replay')
        for key in self.checked['authority_refs'].values():
            require(sha(authority_bytes(self.registry.overlay,key))==key,'Published consumer5 original authority changed')
    def llms(self,raw):
        self.check();after=project_llms(raw,catalog())
        proof={'after_sha256':sha(after),'exact_inverse_or_actual_contexts':True,
            'published_consumer5_producer_sha256':self.checked['producer_sha256'],'catalog_sha256':CATALOG_SHA256}
        base=copy.deepcopy(self.registry.receipts['llms'])
        self.registry.receipt('llms',consumed_paths=self.registry.records,outputs={'/llms.txt':after},
            proof={'base_effective_metadata_receipt_sha256':jhash(base),'published_consumer5':proof})
        return after,proof
    def search(self,before,after):
        self.check();return frozen_search_exact(before,after,self.frozen_paths)

class PublishedBindingSeal:
    def __init__(self,token,declared,instance,producer_sha256):
        require(token is _TOKEN,'Published binding seal needs the checked load result')
        self.declared=declared;self.instance=instance;self.producer_sha256=producer_sha256
        self._stamp=jhash([declared,producer_sha256,instance.checked['producer_sha256'] if instance else None])
    def check(self,session):
        current=getattr(session,'published_consumer5',None)
        require(self._stamp==jhash([self.declared,self.producer_sha256,
            self.instance.checked['producer_sha256'] if self.instance else None])
            and current is self.instance and (current is not None)==self.declared,
            'Declared published consumer5 binding was dropped, replaced or changed')
        if current is not None:current.check()
        return current

def seal_published_binding(session,producer_raw):
    declared=json.loads(producer_raw).get(KEY) is not None
    instance=getattr(session,'published_consumer5',None)
    require((instance is not None)==declared and (instance is None or isinstance(instance,PublishedConsumerFive)),
        'Actual producer declaration/checked binding differs at load')
    session._published_consumer5_load_seal=PublishedBindingSeal(_TOKEN,declared,instance,sha(producer_raw))
    session._published_consumer5_load_seal.check(session)

def checked_published_binding(session):
    seal=getattr(session,'_published_consumer5_load_seal',None)
    require(isinstance(seal,PublishedBindingSeal),'Published consumer5 load seal missing')
    return seal.check(session)

def bind_published_discovery_five(**kwargs):
    checked=recipe(**kwargs)
    if checked is None:return None,kwargs['hubs']
    registry=kwargs['registry'];base_receipt=copy.deepcopy(registry.receipts['library-hubs'])
    registry.hubs=copy.deepcopy(checked['after_hubs'])
    registry.receipt('library-hubs',consumed_paths=registry.records,
        outputs={'/'+p.removesuffix('index.md'):r['body'].encode()for p,r in registry.hubs.items()},
        proof={'base_effective_metadata_consumer_receipt_sha256':jhash(base_receipt),
            'base_generator_used_unchanged_effective_metadata':True,'published_consumer5_catalog_sha256':CATALOG_SHA256,
            'actual_prior_producer_sha256':checked['producer_sha256'],'original_Root_authority_sha256':checked['declaration']['Root_review_sha256'],
            'two_hub_five_card_exact_inverses':True,'original_actual_hub_date_event_sha256':HUB_DATE_EVENT_SHA256,
            'leaf_records_and_metadata_fingerprint_unchanged':True})
    token=PublishedConsumerFive(_TOKEN,registry,checked,kwargs['frozen_paths']);token.check()
    return token,copy.deepcopy(registry.hubs)
