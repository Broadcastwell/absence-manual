"""Recount Study 1 published tables from scalar observations and memberships.

Python standard library only. Reads no fetched response body and makes no
network request. Usage: python reproduce_study1.py PATH_TO_PUBLIC_DATA
"""
from pathlib import Path
from collections import Counter,defaultdict
from statistics import NormalDist
from urllib.parse import urlsplit
import csv,math,sys,json

root=Path(sys.argv[1]);read=lambda f:list(csv.DictReader((root/f).open(encoding='utf-8-sig',newline='')))
units=read('study1-url-classifications.csv');byid={r['url_id']:r for r in units}
assert len(byid)==len(units)
yes=lambda r,k:r.get(k)=='True'
def classify(r):
 if not yes(r,'fetched_html'):return 'fetch failure'
 if yes(r,'wikipedia_family'):return 'definitely not optimized'
 if r['seo_plugins'] or any(yes(r,k) for k in ('json_ld','microdata','news_domain','ads')):return 'definitely optimized'
 if not (yes(r,'title_nonempty') and yes(r,'description_nonempty')):return 'probably not optimized'
 if any(yes(r,k) for k in ('analytics','https','canonical','viewport','open_graph','robots_seo_hint')) or r['sitemap_xml']=='present' or (r['ttfb_seconds'] and 0<=float(r['ttfb_seconds'])<3):return 'probably optimized'
 return 'unclassified'
for r in units:assert r['classification']==classify(r),r['url_id']
members=defaultdict(set);positions=defaultdict(list)
occ=read('study1-citation-membership.csv')
for r in occ:
 assert r['url_id'] in byid
 for scope in (r['scope'],'combined'):
  for engine,category in [('all','all'),(r['engine'],'all'),('all',r['category']),(r['engine'],r['category'])]:members[(scope,engine,category)].add(r['url_id'])
  for engine in ('all',r['engine']):positions[(scope,engine,r['citation_array_position'])].append(r['url_id'])
z=NormalDist().inv_cdf(.975);checked=0
def check(r,k,n):
 global checked
 assert int(r['count'])==k and int(r['base'])==n,(r,k,n)
 if n:
  # Roots of the Wilson score inequality, independently of the original code.
  a=n+z*z;b=-2*k-z*z;c=k*k/n
  h=math.sqrt(max(0,b*b-4*a*c))
  values=[100*k/n,100*(-b-h)/(2*a),100*(-b+h)/(2*a)]
  for key,v in zip(('percent','wilson_95_low','wilson_95_high'),values):assert abs(float(r[key])-v)<.000051,(key,r,v)
 else:assert all(r[k]=='' for k in ('percent','wilson_95_low','wilson_95_high'))
 checked+=1
def subset(r):
 allids=members[(r['scope'],r['engine'],r['category'])]
 return allids,{i for i in allids if yes(byid[i],'fetched_html')}
for r in read('study1-class-shares.csv'):
 _,ok=subset(r);check(r,sum(byid[i]['classification']==r['measure'] for i in ok),len(ok))
for r in read('study1-fetch-outcomes.csv'):
 ids,_=subset(r);check(r,sum(byid[i]['fetch_outcome']==r['measure'] for i in ids),len(ids))
for r in read('study1-wikipedia-shares.csv'):
 ids,ok=subset(r);base=ids if r['denominator']=='all eligible cited URLs' else ok
 check(r,sum(yes(byid[i],'wikipedia_family') for i in base),len(base))
origin=lambda i:'://'.join(urlsplit(byid[i]['final_url'])[:2])
for r in read('study1-llms-presence.csv'):
 _,ok=subset(r);state=r['measure'].split()[-1]
 if r['unit']=='distinct final origin':
  hosts={origin(i):byid[i]['llms_txt'] for i in ok};k=sum(x==state for x in hosts.values());n=len(hosts)
 else:k=sum(byid[i]['llms_txt']==state for i in ok);n=len(ok)
 check(r,k,n)
def types(i):return {t.removeprefix('https://schema.org/').removeprefix('http://schema.org/') for t in byid[i]['schema_types'].split(';') if t.strip()}
for r in read('study1-schema-types.csv'):
 _,ok=subset(r);check(r,sum(r['measure'] in types(i) for i in ok),len(ok))
for r in read('study1-citation-order.csv'):
 ids=positions[(r['scope'],r['engine'],r['citation_array_position'])]
 if r['unit']=='distinct exact URL at this array position':ids=set(ids)
 assert len(ids)==int(r['all_units_at_position'])
 ok=[i for i in ids if yes(byid[i],'fetched_html')];check(r,sum(byid[i]['classification']==r['measure'] for i in ok),len(ok))
hosts={}
for i in byid:
 if yes(byid[i],'fetched_html'):
  key=origin(i);value={k:byid[i][k] for k in ('robots_txt','sitemap_xml','llms_txt')}
  assert key not in hosts or hosts[key]==value
  hosts[key]=value
pubhosts=read('study1-host-evidence.csv');assert len(pubhosts)==len(hosts)
for r in pubhosts:assert hosts[r['origin']]=={k:r[k] for k in ('robots_txt','sitemap_xml','llms_txt')}
print(json.dumps(dict(status='PASS',meaning='Writer reproduction, not independent publication approval',urls=len(units),citation_memberships=len(occ),strata=len(members),numeric_table_rows_checked=checked,host_rows_checked=len(pubhosts)),indent=2))
