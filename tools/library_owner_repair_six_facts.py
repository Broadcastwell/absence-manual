"""Exact two-record extension; the original four-record proof stays intact."""
import csv,io
from library_owner_repair import require,sha,SITE
from library_owner_repair_four_facts import validate_four_public_facts,EXPECTED as FOUR,URLS as FOUR_URLS,unique

JSON_ID='json-ld-presence-target-urls'
EMPTY_ID='empty-citation-lists-target-answers'
URLS=FOUR_URLS|{SITE+'research/data/answer-citation-bases.csv',SITE+'research/data/collect_page_signals.py'}


def validate_six_public_facts(registry,*,actual_prior_files,root_source_url_pins):
    require(set(registry)==set(FOUR)|{JSON_ID,EMPTY_ID} and set(root_source_url_pins)==URLS,'Finite six-record/primary-file coverage differs')
    old=validate_four_public_facts({k:registry[k] for k in FOUR},actual_prior_files=actual_prior_files,root_source_url_pins={u:root_source_url_pins[u] for u in FOUR_URLS})
    raw={}
    for url in URLS:
        path=url.removeprefix(SITE);require(path in actual_prior_files and sha(actual_prior_files[path])==root_source_url_pins[url],'Finite six public source bytes differ');raw[url]=actual_prior_files[path]
    for key,count,base,date,filenames in [(JSON_ID,3616,4420,'2026-10-30',{'study1-citation-membership.csv','study1-url-classifications.csv','collect_page_signals.py'}),(EMPTY_ID,39,2095,'2026-09-22 through2026-09-23',{'answer-citation-bases.csv'})]:
        r=registry[key]
        require(r.get('source_kind')=='published-study' and r.get('numeric_cut') is True and (r.get('count'),r.get('base'),r.get('observed_at'))==(count,base,date),'Added finite source count/base/date/kind differs')
        require(r.get('source_url') in URLS and r['public_text'] in raw[r['source_url']].decode('utf-8-sig'),'Added exact public row/header missing')
        require({i.get('source_url') for i in r.get('inputs',[])}=={SITE+'research/data/'+f for f in filenames} and len(r['inputs'])==len(filenames),'Added finite source input coverage differs')
        for inp in r['inputs']:require(inp.get('sha256')==sha(raw[inp['source_url']]),'Added finite source input hash differs')
    r=registry[JSON_ID];c=r.get('calculation',{})
    require(r.get('calculation_kind')=='owner-authorized-public-row-aggregate' and r.get('published_aggregate') is False and r.get('aggregate_quote_exists_in_prior_publication') is False,'Derived JSON-LD count cannot claim a preprinted aggregate')
    require(c.get('membership_filter')=={'scope':'target'} and c.get('membership_unique_key')=='url_id' and c.get('base_predicates')=={'fetched_html':'True'} and c.get('count_predicates')=={'json_ld':'True'} and c.get('membership_file')=='study1-citation-membership.csv' and c.get('observation_file')=='study1-url-classifications.csv','JSON-LD finite join/predicates differ')
    require(c.get('frozen_field_definition')=='At least one nonempty parsed JSON object or array; not vocabulary validation. Parse failure on another script can coexist.','JSON-LD recorded field meaning changed')
    read=lambda name:list(csv.DictReader(io.StringIO(raw[SITE+'research/data/'+name].decode('utf-8-sig'))))
    members={x['url_id'] for x in read('study1-citation-membership.csv') if x['scope']=='target'}
    observed=read('study1-url-classifications.csv');require(len({x['url_id'] for x in observed})==len(observed),'Duplicate JSON-LD observation identity')
    base=[x for x in observed if x['url_id'] in members and x['fetched_html']=='True'];count=[x for x in base if x['json_ld']=='True']
    require((len(members),len(count),len(base))==(5861,3616,4420) and (c.get('count'),c.get('base'),c.get('distinct_membership_ids'))==(3616,4420,5861),'JSON-LD public aggregate recomputation differs')
    r=registry[EMPTY_ID]
    require(r.get('calculation_kind')=='existing-published-aggregate-row' and r.get('published_aggregate') is True,'Empty-list published aggregate status differs')
    row=unique(read('answer-citation-bases.csv'),scope='target',engine='all',category='all')
    require((int(row['zero_citation_answers']),int(row['valid_answers']))==(39,2095),'Empty-list count/base or unit selector differs')
    return {**old,'all_six_exact':True,'json_ld_derived_count':3616,'json_ld_derived_base':4420,'json_ld_vocabulary_validation_claimed':False,'empty_list_count':39,'empty_list_base':2095}
