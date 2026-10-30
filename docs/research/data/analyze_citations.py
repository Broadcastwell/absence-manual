"""Reproduce registered descriptive citation statistics from deposited arrays.

No web requests or text-based URL extraction. Inputs are explicit CLI paths.
The supplied classification hash must match the pre-aggregation frozen table.
"""
from pathlib import Path
import argparse,csv,hashlib,json,math
from collections import Counter,defaultdict
from urllib.parse import urlsplit

CLASSES=['vendor site','review platform','Wikipedia or sister project','news or trade media','agency, consultancy or blog','directory or listicle site','forum','video','government or standards body','other','unclassified URL entry']

def wilson(k,n):
 if not n:return '', ''
 z=1.959963984540054;p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt((p*(1-p)+z*z/(4*n))/n)/d
 return round(max(0,c-h)*100,4),round(min(1,c+h)*100,4)
def rate(k,n):return round(100*k/n,4) if n else ''
def write(path,rows,fields=None):
 rows=list(rows);fields=fields or (list(rows[0]) if rows else [])
 with path.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def host_of(value):
 if not isinstance(value,str):return None
 try:
  u=urlsplit(value)
  if u.scheme.lower() not in ('http','https') or not u.hostname:return None
  return u.hostname.lower().removeprefix('www.')
 except (ValueError,UnicodeError):return None
def keys(scope,engine,category):
 return [(s,e,c) for s in (scope,'combined') for e,c in [('all','all'),(engine,'all'),('all',category),(engine,category)]]

def analyze(a):
 actual=hashlib.sha256(a.classes.read_bytes()).hexdigest()
 if actual!=a.class_sha256:raise ValueError('Frozen class-table hash mismatch')
 classes={x['host']:x for x in csv.DictReader(a.classes.open(encoding='utf-8'))}
 release=json.loads(a.release.read_text(encoding='utf-8'))
 targets={c['id']:{q['id'] for q in c['questions']} for c in release['categories']}
 controls={(x['category_id'],x['question_id']) for x in json.loads(a.controls.read_text(encoding='utf-8'))}
 raw=[json.loads(x) for x in a.answers.read_text(encoding='utf-8').splitlines() if x.strip()]
 answers=[];exclusions=[];citations=[];invalid=[];seen_answers=set()
 for row in raw:
  cat=row['category_id'];qid=row['question_id'];engine=row['engine'];repeat=row['repeat_index']
  uid='|'.join([cat,qid,engine,str(repeat)])
  if uid in seen_answers:raise ValueError('Duplicate observation '+uid)
  seen_answers.add(uid)
  if qid in targets[cat]:scope='target'
  elif (cat,qid) in controls:scope='control'
  else:raise ValueError('Unknown question '+uid)
  if not isinstance(row['cited_urls'],list):raise ValueError('Citation array required')
  common={'answer_id':uid,'scope':scope,'engine':engine,'category':cat,'question_id':qid,'repeat':repeat,'captured_at':row['captured_at']}
  if row['excluded']:
   exclusions.append(dict(common,reason=row['exclusion_reason'],quarantined_array_entries=len(row['cited_urls'])));continue
  urls=row['cited_urls'];seen=set();unique=0
  for index,url in enumerate(urls):
   exact=url if isinstance(url,str) else json.dumps(url,sort_keys=True,ensure_ascii=False)
   duplicate=exact in seen;seen.add(exact);unique+=not duplicate
   host=host_of(url)
   if host and host not in classes:raise ValueError('Host absent from frozen table: '+host)
   cls=classes[host]['class'] if host else 'unclassified URL entry'
   if cls not in CLASSES:raise ValueError('Unknown class '+cls)
   record=dict(common,array_index=index,original_url=exact,host=host or '',source_class=cls,duplicate_in_answer=int(duplicate),ambiguity=classes[host]['ambiguity'] if host else 'true')
   citations.append(record)
   if not host:invalid.append(record)
  answers.append(dict(common,array_entries=len(urls),exact_unique_entries=unique,zero_citation=int(not urls)))
 # Answer bases are independent of URL-array length, preserving empty arrays.
 answer_totals=defaultdict(lambda:[0,0,0])
 for row in answers:
  for key in keys(row['scope'],row['engine'],row['category']):
   cell=answer_totals[key];cell[0]+=1;cell[1]+=row['zero_citation'];cell[2]+=row['array_entries']
 class_rows=[];top_rows=[];host_rows=[];concentration=[];review_rows=[]
 for variant in ['all array entries','deduplicated exact URL per answer','ambiguous hosts recoded other']:
  class_counts=defaultdict(Counter);host_counts=defaultdict(Counter);denominators=Counter()
  for row in citations:
   if variant=='deduplicated exact URL per answer' and row['duplicate_in_answer']:continue
   cls='other' if variant=='ambiguous hosts recoded other' and row['host'] and row['ambiguity']=='true' else row['source_class']
   for key in keys(row['scope'],row['engine'],row['category']):
    denominators[key]+=1;class_counts[key][cls]+=1
    if row['host']:host_counts[key][row['host']]+=1
  for key in sorted(answer_totals):
   scope,engine,category=key;n=denominators[key];prefix={'variant':variant,'scope':scope,'engine':engine,'category':category}
   for cls in CLASSES:
    k=class_counts[key][cls];lo,hi=wilson(k,n)
    class_rows.append(dict(prefix,source_class=cls,citation_occurrences=k,all_array_entries_base=n,share_pct=rate(k,n),wilson_low_pct=lo,wilson_high_pct=hi))
   if sum(class_counts[key].values())!=n:raise ValueError('Class totals do not reconcile')
   if variant=='ambiguous hosts recoded other':continue
   ordered=sorted(host_counts[key].items(),key=lambda x:(-x[1],x[0]));h=len(ordered)
   for rank,(host,k) in enumerate(ordered,1):
    lo,hi=wilson(k,n);r=dict(prefix,rank=rank,host=host,citation_occurrences=k,all_array_entries_base=n,share_pct=rate(k,n),wilson_low_pct=lo,wilson_high_pct=hi,source_class=classes[host]['class'],ambiguity=classes[host]['ambiguity'])
    host_rows.append(r)
    if rank<=20:top_rows.append(r)
   for cut in ['top 10 hosts','top ceiling one percent of hosts']:
    take=min(10,h) if cut=='top 10 hosts' else min(h,max(1,math.ceil(h*.01)))
    k=sum(x[1] for x in ordered[:take]);lo,hi=wilson(k,n)
    concentration.append(dict(prefix,cut=cut,distinct_hosts=h,hosts_in_cut=take,citation_occurrences=k,all_array_entries_base=n,share_pct=rate(k,n),wilson_low_pct=lo,wilson_high_pct=hi,tie_rule='descending count, then alphabetical exact hostname'))
   for host in ['g2.com','capterra.com','getapp.com','trustradius.com','softwareadvice.com','gartner.com']:
    # Exact preserved host counts, not silently collapsed subdomain families.
    k=host_counts[key][host];lo,hi=wilson(k,n)
    review_rows.append(dict(prefix,host=host,citation_occurrences=k,all_array_entries_base=n,share_pct=rate(k,n),wilson_low_pct=lo,wilson_high_pct=hi))
 a.out.mkdir(parents=True,exist_ok=True)
 write(a.out/'citation-occurrences.csv',citations)
 write(a.out/'citation-invalid.csv',invalid,fields=list(citations[0]))
 write(a.out/'answer-citation-audit.csv',answers)
 write(a.out/'excluded-answers.csv',exclusions)
 write(a.out/'citation-class-shares.csv',class_rows)
 write(a.out/'cited-hosts.csv',host_rows)
 write(a.out/'top-twenty-hosts.csv',top_rows)
 write(a.out/'citation-concentration.csv',concentration)
 write(a.out/'review-platform-occurrences.csv',review_rows)
 bases=[]
 for key,(n,zero,entries) in sorted(answer_totals.items()):
  lo,hi=wilson(zero,n);bases.append({'scope':key[0],'engine':key[1],'category':key[2],'valid_answers':n,'zero_citation_answers':zero,'zero_share_pct':rate(zero,n),'wilson_low_pct':lo,'wilson_high_pct':hi,'citation_array_entries':entries})
 write(a.out/'answer-citation-bases.csv',bases)
 summary={'captured_answers':len(raw),'valid_answers':len(answers),'excluded_answers':len(exclusions),'eligible_array_entries':len(citations),'invalid_entries':len(invalid),'duplicate_entries':sum(x['duplicate_in_answer'] for x in citations),'class_sha256':actual,'target':next(x for x in bases if x['scope']=='target' and x['engine']=='all' and x['category']=='all')}
 return summary

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for key in ['answers','release','controls','classes','out']:p.add_argument('--'+key,type=Path,required=True)
 p.add_argument('--class-sha256',required=True)
 print(json.dumps(analyze(p.parse_args()),indent=2))
