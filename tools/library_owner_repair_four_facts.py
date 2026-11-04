"""Four owner-approved public-CSV readings, including one explicit aggregate.

No new engine calls, qualitative numeric1, source-kind change, or claim that
the derived4179/4420 total was already printed in the public CSV.
"""
import csv,io,json
from library_owner_repair import require,sha,SITE
from library_owner_repair_consumers import json_hash

EXPECTED={'canonical-presence-target-urls':(4179,4420),'classification-sensitivity':(1706,18893),'llms-presence-origins':(774,1600),'rovira-own-reanalysis':(456,1000)}
INPUTS={'canonical-presence-target-urls':{'study1-citation-membership.csv','study1-url-classifications.csv'},'classification-sensitivity':{'citation-class-shares.csv','citation-class-shares-post-audit.csv','host-class-post-audit-changes.csv'},'llms-presence-origins':{'study1-llms-presence.csv'},'rovira-own-reanalysis':{'rovira-workbook-reanalysis.csv','rovira-median-differences.csv'}}
FILES={'study1-citation-membership.csv','study1-url-classifications.csv','citation-class-shares.csv','citation-class-shares-post-audit.csv','host-class-post-audit-changes.csv','study1-llms-presence.csv','rovira-workbook-reanalysis.csv','rovira-median-differences.csv'}
URLS={SITE+'research/data/'+f for f in FILES}


def unique(rows,**conditions):
    result=[r for r in rows if all(r.get(k)==v for k,v in conditions.items())]
    require(len(result)==1,'Published aggregate selector is missing/ambiguous, including its unit')
    return result[0]


def validate_four_public_facts(registry,*,actual_prior_files,root_source_url_pins):
    require(set(registry)==set(EXPECTED),'Owner four-fact registry coverage differs')
    require(set(root_source_url_pins)==URLS,'Root exact public CSV URL map differs')
    raw={};rows={}
    for url in sorted(URLS):
        path=url.removeprefix(SITE);require(path in actual_prior_files and sha(actual_prior_files[path])==root_source_url_pins[url],'Actual prior public CSV bytes differ')
        raw[url]=actual_prior_files[path];rows[path.rsplit('/',1)[-1]]=list(csv.DictReader(io.StringIO(raw[url].decode('utf-8-sig'))))
    for key,r in registry.items():
        require(r.get('source_kind')=='published-study' and r.get('numeric_cut') is True and (r.get('count'),r.get('base'))==EXPECTED[key] and r.get('observed_at')=='2026-10-30','Finite source count/base/date/kind differs')
        require(r.get('source_url') in URLS and r['public_text'] in raw[r['source_url']].decode('utf-8-sig'),'Exact public CSV quote/header missing')
        require({i.get('source_url') for i in r.get('inputs',[])}=={SITE+'research/data/'+f for f in INPUTS[key]} and len(r['inputs'])==len(INPUTS[key]),'Finite fact input coverage differs')
        for inp in r['inputs']:require(inp.get('source_url') in URLS and inp.get('sha256')==sha(raw[inp['source_url']]),'Published fact input URL/hash differs')
        if key!='canonical-presence-target-urls':require(r.get('published_aggregate') is True and r.get('calculation_kind')==('existing-published-finite-workbook-reanalysis' if key=='rovira-own-reanalysis' else 'existing-published-aggregate-row'),'Existing aggregate provenance differs')
    canonical=registry['canonical-presence-target-urls'];calc=canonical.get('calculation',{})
    require(canonical.get('calculation_kind')=='owner-authorized-public-row-aggregate' and canonical.get('published_aggregate') is False and canonical.get('aggregate_quote_exists_in_prior_publication') is False,'Derived aggregate cannot be relabeled as a preprinted quote')
    require(calc.get('membership_filter')=={'scope':'target'} and calc.get('membership_unique_key')=='url_id' and calc.get('base_predicates')=={'fetched_html':'True'} and calc.get('count_predicates')=={'canonical':'True'} and calc.get('membership_file')=='study1-citation-membership.csv' and calc.get('observation_file')=='study1-url-classifications.csv','Finite canonical join/predicate contract differs')
    members={r['url_id'] for r in rows['study1-citation-membership.csv'] if r['scope']=='target'}
    observed=rows['study1-url-classifications.csv'];require(len({r['url_id'] for r in observed})==len(observed),'URL observation identity duplicated')
    base=[r for r in observed if r['url_id'] in members and r['fetched_html']=='True'];count=[r for r in base if r['canonical']=='True']
    require((len(members),len(count),len(base))==(5861,4179,4420) and calc.get('distinct_membership_ids')==5861 and calc.get('count')==4179 and calc.get('base')==4420,'Actual canonical aggregate recomputation differs')
    post=unique(rows['citation-class-shares-post-audit.csv'],variant='all array entries',scope='target',engine='all',category='all',source_class='review platform')
    before=unique(rows['citation-class-shares.csv'],variant='all array entries',scope='target',engine='all',category='all',source_class='review platform')
    require((int(before['citation_occurrences']),int(post['citation_occurrences']),int(post['all_array_entries_base']))==(1663,1706,18893),'Classification before/after cut differs')
    llms=unique(rows['study1-llms-presence.csv'],scope='target',engine='all',category='all',measure='llms.txt present',unit='distinct final origin')
    unknown=unique(rows['study1-llms-presence.csv'],scope='target',engine='all',category='all',measure='llms.txt unknown',unit='distinct final origin')
    require((int(llms['count']),int(llms['base']),int(unknown['count']))==(774,1600,85),'llms origin/unknown cut differs from URL-unit row')
    workbook=unique(rows['rovira-workbook-reanalysis.csv'],file='GS-1-word-title-restriction.xlsx',sheet='Full 1')
    differences=[r for r in rows['rovira-median-differences.csv'] if r['file']=='GS-1-word-title-restriction.xlsx' and r['sheet']=='Full 1']
    require((int(workbook['differing_medians']),int(workbook['result_positions']),len(differences))==(456,1000,456),'Finite published workbook arithmetic differs')
    require(len({r['row'] for r in differences})==456,'Workbook changed-position identities duplicate')
    return {'all_four_exact':True,'canonical_derived_count':4179,'canonical_derived_base':4420,'canonical_claimed_preprinted':False,'ordinary_source_kind_or_lead_allowance_changed':False}
