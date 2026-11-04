"""Five exact standalone discovery descriptions; no leaf/source-kind override."""
import copy,json,re
from pathlib import Path
from library_owner_repair import require,sha,POLICY

CATALOG_SHA256='e44c828358fb4c5b3ac86c8bc5280835a08e0ddb5e01d4ea2a88bc675a516607'
HUB_DATE_EVENT_SHA256='57db83b10ec6aa6e449f0b8d32eea1f78ebf607b4ea020e300beebf6371458a8'
KIND='OWNER_EXACT_DISCOVERY_CONSUMER_FIVE_V1'
_TOKEN=object()
def jhash(v):return sha(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
def leaf_stamp(records):
    def path_value(v):
        require(isinstance(v,Path),'Unsupported non-JSON leaf record value');return {'exact_path_object':str(v)}
    return sha(json.dumps(records,sort_keys=True,ensure_ascii=False,separators=(',',':'),default=path_value).encode())
def catalog():
    raw=Path(__file__).with_name('library_owner_discovery_consumer_five.json').read_bytes()
    require(sha(raw)==CATALOG_SHA256,'Exact consumer5 catalog differs');d=json.loads(raw)
    require({r['bank_id']for r in d['rows']}=={'LB-Q0534','LB-Q0637','LB-Q0638','LB-Q0640','LB-Q0642'} and len(d['rows'])==5,'Exact five identity coverage differs')
    return d
def patch_text(text,edits):
    original=text
    for old,new in edits:
        require(old and new and text.count(old)==1,'Consumer5 old literal missing/repeated');text=text.replace(old,new,1)
    inverse=text
    for old,new in reversed(edits):
        require(inverse.count(new)==1,'Consumer5 new literal missing/repeated');inverse=inverse.replace(new,old,1)
    require(inverse==original,'Consumer5 exact inverse differs');return text
def checked_hub_date_event(raw,c):
    require(sha(raw)==HUB_DATE_EVENT_SHA256,'Exact actual Root two-hub date event differs')
    d=json.loads(raw);stamp=d.get('actual_private_adoption_utc')
    require(d.get('reviewer')=='root' and d.get('catalog_sha256')==CATALOG_SHA256
        and d.get('recorded_utc')==stamp and d.get('source49_raw_hubs_and_all45_leaf_metadata_unchanged') is True
        and d.get('strict_date_guard_waiver') is False and d.get('new_build_artifact_or_publication_claimed') is False
        and set(d.get('hub_metadata',{}))==set(c['hubs'])
        and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00',str(stamp)),
        'Actual Root date event scope differs')
    from datetime import datetime
    for p,note in d['hub_metadata'].items():
        before,after=note['before'],note['after']
        require(jhash(before)==note['before_meta_sha256']==c['hubs'][p]['metadata_sha256']
            and jhash(after)==note['after_meta_sha256'] and after=={**before,'date_modified':stamp}
            and datetime.fromisoformat(stamp)>datetime.fromisoformat(before['date_modified']),
            'Root hub date event changes more than the exact actual modification time')
    return d

def project_hubs(hubs,c,date_event=None,*,allow_published_metadata=False):
    result=copy.deepcopy(hubs)
    require(set(c['hubs'])=={'answers/fixes/index.md','answers/geo-basics/index.md'},'Consumer5 hub scope differs')
    for p,note in c['hubs'].items():
        allowed=[note['metadata_sha256']]
        if date_event is not None and allow_published_metadata:allowed.append(date_event['hub_metadata'][p]['after_meta_sha256'])
        require(p in result and sha(result[p]['body'].encode())==note['before_body_sha256'] and jhash(result[p]['meta']) in allowed,'Consumer5 base hub body/meta differs')
        edits=[(r['old_card_markdown'],r['new_card_markdown'])for r in c['rows']if r['hub_path']==p]
        result[p]['body']=patch_text(result[p]['body'],edits)
        require(sha(result[p]['body'].encode())==note['after_body_sha256'],'Consumer5 exact whole hub after differs')
        if date_event is not None:
            dated=date_event['hub_metadata'][p]
            require(result[p]['meta']==dated['before'] or (allow_published_metadata and result[p]['meta']==dated['after']),
                'Consumer5 normal hub metadata differs from exact original before/after')
            result[p]['meta']=copy.deepcopy(dated['after'])
    require(all(result[p]==hubs[p]for p in set(hubs)-set(c['hubs'])),'Consumer5 changed another hub')
    return result
def project_llms(raw,c):
    require(sha(raw)==c['llms_before_sha256'],'Consumer5 llms base differs from reviewed Owner baseline')
    result=patch_text(raw.decode(),[(r['old_llms_line'],r['new_llms_line'])for r in c['rows']]).encode()
    require(sha(result)==c['llms_after_sha256'],'Consumer5 whole llms after differs');return result
def _search_rows(raw):
    text=raw.decode();decoder=json.JSONDecoder();skip=lambda i:len(text)-len(text[i:].lstrip())
    i=skip(0);require(text[i]=='{','Material search root must be an object');i+=1;found=None
    while True:
        i=skip(i)
        if text[i]=='}':break
        key,i=decoder.raw_decode(text,i);i=skip(i);require(text[i]==':','Material search key delimiter differs');i=skip(i+1)
        if key=='docs':
            require(found is None and text[i]=='[','Material search docs missing/repeated');found=[];i+=1
            while True:
                i=skip(i)
                if text[i]==']':i+=1;break
                start=i;row,i=decoder.raw_decode(text,i);require(isinstance(row,dict),'Material search row malformed')
                found.append((row,text[start:i].encode()));i=skip(i)
                if text[i]==',':i+=1
                else:require(text[i]==']','Material search row delimiter differs')
        else:_,i=decoder.raw_decode(text,i)
        i=skip(i)
        if text[i]==',':i+=1
        else:require(text[i]=='}','Material search object delimiter differs')
    require(found is not None,'Material search docs missing');return found
def frozen_search_exact(before,after,frozen_paths):
    require(len(frozen_paths)==45,'Consumer5 needs the accepted45 frozen leaves')
    a,b=_search_rows(before),_search_rows(after)
    for p in frozen_paths:
        root=p.removesuffix('.md')+'/'
        rows=lambda d:[raw for r,raw in d if r.get('location','').split('#')[0]==root]
        require(rows(a) and rows(a)==rows(b),'Consumer5 changed/missed frozen Material leaf-search rows: '+p)
    return True

class ConsumerFive:
    def __init__(self,token,*,owner_plan,registry,load,refs,plan,c,base_hubs,after_hubs,frozen_paths):
        require(token is _TOKEN,'Consumer5 requires checked Root/peer binding')
        self.owner_plan=owner_plan;self.registry=registry;self.load=load;self.refs=copy.deepcopy(refs);self.plan=copy.deepcopy(plan);self.c=c
        self.base_hubs=copy.deepcopy(base_hubs);self.after_hubs=copy.deepcopy(after_hubs);self.frozen_paths=set(frozen_paths)
        self.records_stamp=leaf_stamp(registry.records);self.fingerprint=registry.fingerprint
        self._stamp=jhash([self.refs,self.plan,self.c,self.base_hubs,self.after_hubs,sorted(self.frozen_paths)])
    def check(self,hubs):
        self.owner_plan.assert_current();self.registry.assert_current()
        require(self._stamp==jhash([self.refs,self.plan,self.c,self.base_hubs,self.after_hubs,sorted(self.frozen_paths)]),'Consumer5 checked data changed')
        for ref in self.refs.values():self.load(ref)
        require(leaf_stamp(self.registry.records)==self.records_stamp and self.registry.fingerprint==self.fingerprint,'Consumer5 changed leaf records/meta/fingerprint')
        require(hubs==self.after_hubs and self.registry.hubs==hubs,'Consumer5 effective hubs changed after checked projection')
    def llms(self,raw):
        self.check(self.registry.hubs);after=project_llms(raw,self.c)
        return after,{'after_sha256':sha(after),'exact_inverse_or_actual_contexts':True,'consumer5_catalog_sha256':CATALOG_SHA256,'five_URLs':[r['url']for r in self.c['rows']]}
    def search(self,before,after):
        self.check(self.registry.hubs);return frozen_search_exact(before,after,self.frozen_paths)

def bind_consumer_five(config,load,owner_plan,registry,hubs,frozen_paths,source_plan_sha256,actual_prior_files):
    """Called only by explicit Owner dispatch, after normal hub generation.

    Historical plans without this separate correction stay historical. A plan
    declaring it must have the exact configuration and all actual approvals;
    a missing receipt cannot silently fall back to the old descriptions.
    """
    declared=owner_plan.data.get('discovery_consumer_five')
    refs=config.get('discovery_consumer_five')
    require(bool(declared)==bool(refs),'Declared consumer5 plan/config coverage differs')
    if declared is None:return None,hubs
    require(set(declared)=={'catalog_sha256','plan_sha256'} and declared['catalog_sha256']==CATALOG_SHA256,'Root source plan consumer5 catalog differs')
    require(set(refs)=={'plan','Root_review','Source_review','Writing_review','public_before','hub_date_event'},'Consumer5 bound receipt coverage differs')
    raw={k:load(v)[1]for k,v in refs.items()};plan=json.loads(raw['plan']);c=catalog()
    date_event=checked_hub_date_event(raw['hub_date_event'],c)
    before=json.loads(raw['public_before']);expected_paths={'llms.txt','answers/fixes/index.html','answers/geo-basics/index.html'}
    require(before.get('read_kind')=='actual-scripts-off-current-public-before-Consumer5' and before.get('expected')==before.get('actual')==3
      and before.get('all_exact') is True and before.get('current_production')==owner_plan.data['baseline_production_binding']['commit_sha']
      and len(before.get('rows',[]))==3 and {r['path']for r in before['rows']}==expected_paths,'Actual consumer5 current public-before coverage differs')
    for r in before['rows']:
        expected_url='https://docs.broadcastwell.com/'+r['path'].removesuffix('index.html')
        require(r.get('url')==r.get('final_url')==expected_url and r.get('status')==200 and r.get('exact') is True
          and r['sha256']==r['expected_PR93_sha256']==sha(actual_prior_files[r['path']]),'Actual consumer5 public-before bytes differ from bound prior')
    require(sha(raw['plan'])==declared['plan_sha256'] and plan=={'schema_version':1,'policy':KIND,'catalog_sha256':CATALOG_SHA256,
        'hubs':c['hubs'],'llms_before_sha256':c['llms_before_sha256'],'llms_after_sha256':c['llms_after_sha256']},'Exact Root consumer5 data plan differs')
    leaves={r['leaf_path']for r in c['rows']};require(len(registry.records)==307 and len(frozen_paths)==45
      and set(frozen_paths)==set(owner_plan.freeze_data['pages']) and leaves<=set(frozen_paths),'Consumer5 is not exact current307/accepted frozen subset')
    require(not {'docs/'+p for p in leaves}&set(owner_plan.data['source_changes']),'Consumer5 cannot edit a frozen source')
    for r in c['rows']:
        p=r['leaf_path'];record=registry.records[p]
        require(sha(record['effective_full_source'].encode())==r['leaf_effective_canonical_sha256'] and sha(record['body'].encode())==r['leaf_body_sha256']
            and jhash(record['meta'])==r['leaf_metadata_sha256'] and record['meta']['description']==r['old_description'],'Consumer5 frozen leaf/source metadata differs')
    for kind,key in [('source','Source_review'),('writing','Writing_review')]:
        peer=json.loads(raw[key]);require(peer.get('approved') is True and peer.get('review_kind')==kind and peer.get('scope')=='owner-exact-discovery-consumer-five'
          and peer.get('policy')==POLICY and peer.get('catalog_sha256')==CATALOG_SHA256 and peer.get('consumer_plan_sha256')==sha(raw['plan'])
          and peer.get('complete_hub_before_after_read') is True and peer.get('five_exact_descriptions_reviewed') is True
          and peer.get('leaf_source_metadata_or_ordinary_S5_approval') is False,'Actual consumer5 '+kind+' peer missing')
    root=json.loads(raw['Root_review'])
    require(root.get('approved') is True and root.get('reviewer')=='root' and root.get('review_kind')=='root-exact-discovery-consumer-five'
      and root.get('policy')==POLICY and root.get('owner_source_plan_sha256')==source_plan_sha256 and root.get('consumer_plan_sha256')==sha(raw['plan'])
      and root.get('catalog_sha256')==CATALOG_SHA256 and root.get('Source_review_sha256')==sha(raw['Source_review']) and root.get('Writing_review_sha256')==sha(raw['Writing_review'])
      and root.get('actual_public_before_receipt_sha256')==sha(raw['public_before']) and root.get('full_two_hub_before_after_actually_read') is True
      and root.get('hub_date_event_sha256')==HUB_DATE_EVENT_SHA256
      and root.get('dated_global_consumer_truth_correction_no_field_treatment') is True and root.get('leaf_or_frozen_leaf_search_treatment_approval') is False
      and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00',str(root.get('actual_private_adoption_utc'))),'Actual Root separate consumer5 authority missing')
    after=project_hubs(hubs,c,date_event)
    for p,note in c['hubs'].items():
        expected=owner_plan.data['generated_hubs'].get('docs/'+p,{})
        require(expected.get('effective_body_sha256')==note['after_body_sha256'] and expected.get('effective_meta_sha256')==date_event['hub_metadata'][p]['after_meta_sha256'],'Root final generated-hub body/meta approval missing')
    checked=ConsumerFive(_TOKEN,owner_plan=owner_plan,registry=registry,load=load,refs=refs,plan=plan,c=c,base_hubs=hubs,after_hubs=after,frozen_paths=frozen_paths)
    base_receipt=copy.deepcopy(registry.receipts['library-hubs']);registry.hubs=copy.deepcopy(after)
    registry.receipt('library-hubs',consumed_paths=registry.records,outputs={('/'+p.removesuffix('index.md')):r['body'].encode()for p,r in after.items()},proof={
      'base_effective_metadata_consumer_receipt_sha256':jhash(base_receipt),'base_generator_used_unchanged_effective_metadata':True,
      'exact_separate_description_catalog_sha256':CATALOG_SHA256,'Root_consumer_authority_sha256':sha(raw['Root_review']),
      'two_hub_five_card_exact_inverses':True,'two_hub_actual_date_event_sha256':HUB_DATE_EVENT_SHA256,
      'leaf_records_and_metadata_fingerprint_unchanged':True})
    checked.check(after);return checked,after
