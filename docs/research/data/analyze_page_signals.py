"""Registered, offline Study 1 analysis of exact citation URLs.

No response bodies are read. The signal JSONL and explicit citation arrays are
the inputs. Registration verification is a separate prerequisite receipt.
"""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl
from collections import Counter, defaultdict
import argparse, csv, datetime as dt, fnmatch, hashlib, json, math

CLASSES = ['definitely optimized','probably optimized','probably not optimized','definitely not optimized','unclassified']
FLAGS = ['title_nonempty','description_nonempty','canonical','open_graph','viewport','json_ld','json_ld_parse_failure','microdata','analytics','ads','https','news_domain','robots_seo_hint']

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def resource(url): return urlunsplit((*urlsplit(url)[:4],''))

def wiki(url, rules):
    host=(urlsplit(url).hostname or '').lower()
    return any(host==x or host.endswith('.'+x) for x in rules['wikipedia_sisters'])

def classify(row, is_wiki):
    if not row.get('fetched_html'): return 'fetch failure'
    if is_wiki: return 'definitely not optimized'
    if row.get('seo_plugins') or any(row.get(k) for k in ('json_ld','microdata','news_domain','ads')): return 'definitely optimized'
    if not row.get('title_nonempty') or not row.get('description_nonempty'): return 'probably not optimized'
    ttfb=row.get('ttfb_seconds')
    if any(row.get(k) for k in ('analytics','https','canonical','viewport','open_graph','robots_seo_hint')) or row.get('sitemap_xml')=='present' or (isinstance(ttfb,(int,float)) and 0<=ttfb<3): return 'probably optimized'
    return 'unclassified'

def failure(row):
    if row.get('fetched_html'): return 'successful HTML'
    state=row.get('state','unknown'); code=row.get('status')
    if state=='response':
        if code==200: return 'non-HTML response'
        if code in (401,403,429): return 'blocked HTTP '+str(code)
        if isinstance(code,int) and 400<=code<500: return 'other HTTP 4xx'
        if isinstance(code,int) and code>=500: return 'HTTP 5xx'
        return 'other HTTP response'
    if 'timeout' in state.lower() or 'timed out' in row.get('error','').lower(): return 'timeout'
    return state

def interval(k,n):
    if not n:return ('','','')
    z=1.959963984540054;p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt((p*(1-p)+z*z/(4*n))/n)/d
    return (round(100*p,4),round(100*max(0,c-h),4),round(100*min(1,c+h),4))

def write(path,rows,fields=None):
    rows=list(rows);fields=fields or list(rows[0])
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)

def value_row(key,label,k,n,unit,base):
    pct,lo,hi=interval(k,n)
    return dict(scope=key[0],engine=key[1],category=key[2],measure=label,count=k,base=n,percent=pct,wilson_95_low=lo,wilson_95_high=hi,unit=unit,denominator=base)

def safe_url(url,deny):
    p=urlsplit(url);host=(p.hostname or '').lower()
    restricted=any(fnmatch.fnmatch(host,x) or host.endswith('.'+x.removeprefix('*.')) for x in deny)
    secret=any(any(t in k.lower() for t in ('token','password','secret','api_key','apikey','email','auth','signature')) for k,v in parse_qsl(p.query))
    return '' if restricted or secret else url

def analyze(a):
    freeze=json.loads(a.freeze.read_text(encoding='utf-8'))
    for name,expected in freeze['files'].items():
        if sha(a.freeze.parent/name)!=expected: raise ValueError('Frozen input changed: '+name)
    rules=json.loads(a.rules.read_text(encoding='utf-8'))
    release=json.loads(a.release.read_text(encoding='utf-8'))
    targets={c['id']:{q['id'] for q in c['questions']} for c in release['categories']}
    controls={(r['category_id'],r['question_id']) for r in json.loads(a.controls.read_text(encoding='utf-8'))}
    deny={s.strip().lower() for s in a.exclude_hosts.read_text().splitlines() if s.strip() and not s.startswith('#')}
    raw=[json.loads(s) for s in a.signals.read_text(encoding='utf-8').splitlines() if s.strip()]
    collected={r['requested_url']:r for r in raw}
    if len(collected)!=len(raw):raise ValueError('Duplicate resource records')
    expected_occ=[];excluded=[];seen_answers=set()
    for s in a.answers.read_text(encoding='utf-8').splitlines():
        if not s.strip():continue
        r=json.loads(s);cat=r['category_id'];qid=r['question_id'];key=(cat,qid,r['engine'],r['repeat_index'])
        if key in seen_answers:raise ValueError('Repeated answer identity')
        seen_answers.add(key)
        scope='target' if qid in targets[cat] else 'control' if (cat,qid) in controls else None
        if scope is None:raise ValueError('Unrecognized question')
        for pos,url in enumerate(r['cited_urls']):
            p=urlsplit(url)
            if p.scheme not in ('http','https') or not p.hostname or p.username or p.password: raise ValueError('Malformed citation')
            common=dict(scope=scope,category=cat,question_id=qid,engine=r['engine'],repeat=r['repeat_index'],captured_at=r['captured_at'],citation_array_position=pos+1,url_id=hashlib.sha256(url.encode()).hexdigest())
            if r.get('excluded') or r.get('exclusion_reason'):excluded.append(common);continue
            expected_occ.append((url,common))
    urls=sorted({u for u,c in expected_occ})
    if set(collected)!={resource(u) for u in urls}:raise ValueError('Incomplete or surplus resource collection')
    a.out.mkdir(parents=True,exist_ok=True)
    units={};public=[];members=defaultdict(set);occurrences=[];positions=defaultdict(list)
    for u in urls:
        r=collected[resource(u)];is_wiki=wiki(u,rules);klass=classify(r,is_wiki)
        final=r.get('url',resource(u));p=urlsplit(final);origin=p.scheme+'://'+p.netloc
        row=dict(url_id=hashlib.sha256(u.encode()).hexdigest(),original_url=safe_url(u,deny),requested_resource=safe_url(resource(u),deny),final_url=safe_url(final,deny),public_url_withheld=not bool(safe_url(u,deny)),fetched_html=bool(r.get('fetched_html')),classification=klass,fetch_outcome=failure(r),http_status=r.get('status',''),fetch_started_utc=r.get('collection_started_at',''),fetched_utc=r.get('fetched_at',''),content_type=r.get('content_type',''),ttfb_seconds=r.get('ttfb_seconds',''),wikipedia_family=is_wiki,robots_txt=r.get('robots_txt','unknown'),sitemap_xml=r.get('sitemap_xml','unknown'),llms_txt=r.get('llms_txt','unknown'),seo_plugins=';'.join(r.get('seo_plugins',[])),schema_types=';'.join(r.get('schema_types',[])))
        for k in FLAGS:row[k]=r.get(k,'')
        units[u]=(r,klass,row,origin);public.append(row)
    for u,c in expected_occ:
        r,klass,row,origin=units[u]
        for scope in (c['scope'],'combined'):
            for eng,cat in [('all','all'),(c['engine'],'all'),('all',c['category']),(c['engine'],c['category'])]:members[(scope,eng,cat)].add(u)
            positions[(scope,'all',c['citation_array_position'])].append(u)
            positions[(scope,c['engine'],c['citation_array_position'])].append(u)
        occurrences.append(c)
    shares=[];outcomes=[];wikis=[];llms=[];schema=[];hosts={}
    for key,us in sorted(members.items()):
        ok={u for u in us if units[u][0].get('fetched_html')};counts=Counter(units[u][1] for u in ok)
        for klass in CLASSES:shares.append(value_row(key,klass,counts[klass],len(ok),'distinct exact URL','successful complete HTML, including unclassified'))
        states=Counter(units[u][2]['fetch_outcome'] for u in us)
        for state,n in sorted(states.items()):outcomes.append(value_row(key,state,n,len(us),'distinct exact URL','all eligible cited URLs'))
        for base_name,subset in [('all eligible cited URLs',us),('successful complete HTML',ok)]:
            wikis.append(value_row(key,'Wikipedia or sister project',sum(units[u][2]['wikipedia_family'] for u in subset),len(subset),'distinct exact URL',base_name))
        origins=defaultdict(list)
        for u in sorted(ok):origins[units[u][3]].append(units[u][0])
        for origin,rs in origins.items():
            for k in ('robots_txt','sitemap_xml','llms_txt'):
                if len({r.get(k,'unknown') for r in rs})>1:raise ValueError('Inconsistent cached host file')
            hosts[origin]=dict(origin=safe_url(origin,deny),origin_id=hashlib.sha256(origin.encode()).hexdigest(),robots_txt=rs[0].get('robots_txt','unknown'),sitemap_xml=rs[0].get('sitemap_xml','unknown'),llms_txt=rs[0].get('llms_txt','unknown'))
        for state in ('present','absent','unknown'):
            llms.append(value_row(key,'llms.txt '+state,sum(rs[0].get('llms_txt','unknown')==state for rs in origins.values()),len(origins),'distinct final origin','origins of successful complete HTML URLs'))
            llms.append(value_row(key,'llms.txt '+state,sum(units[u][0].get('llms_txt','unknown')==state for u in ok),len(ok),'distinct exact URL','successful complete HTML URLs; host result repeated across URLs'))
        typecounts=Counter()
        for u in ok:
            # Keep empty declarations in the scalar source, but an empty string
            # is not a schema type. No optimization classification is changed.
            types={t.removeprefix('https://schema.org/').removeprefix('http://schema.org/') for t in units[u][0].get('schema_types',[]) if t.strip()}
            typecounts.update(types)
        for t,n in sorted(typecounts.items()):schema.append(value_row(key,t,n,len(ok),'distinct exact URL','successful complete HTML URLs; multiple types may occur'))
    order=[]
    for (scope,engine,position),us in sorted(positions.items()):
        for unit_name,subset in [('citation occurrence',us),('distinct exact URL at this array position',set(us))]:
            ok=[u for u in subset if units[u][0].get('fetched_html')];n=len(ok);counts=Counter(units[u][1] for u in ok)
            for klass in CLASSES:
                row=value_row((scope,engine,'all'),klass,counts[klass],n,unit_name,'successful complete HTML at the specified citation-array position')
                row['citation_array_position']=position;row['all_units_at_position']=len(subset);order.append(row)
    write(a.out/'study1-url-classifications.csv',public)
    write(a.out/'study1-citation-membership.csv',occurrences)
    write(a.out/'study1-class-shares.csv',shares)
    write(a.out/'study1-fetch-outcomes.csv',outcomes)
    write(a.out/'study1-wikipedia-shares.csv',wikis)
    write(a.out/'study1-llms-presence.csv',llms)
    write(a.out/'study1-schema-types.csv',schema,['scope','engine','category','measure','count','base','percent','wilson_95_low','wilson_95_high','unit','denominator'])
    write(a.out/'study1-host-evidence.csv',[hosts[k] for k in sorted(hosts)])
    write(a.out/'study1-citation-order.csv',order)
    write(a.out/'study1-excluded-citations.csv',excluded,['scope','category','question_id','engine','repeat','captured_at','citation_array_position','url_id'])
    # The public scalar projection and membership table permit independent recounts.
    summary=dict(analysis_utc=dt.datetime.now(dt.timezone.utc).isoformat(),exact_urls=len(urls),requested_resources=len(collected),citation_occurrences=len(expected_occ),excluded_citations=len(excluded),successful_html=sum(r['fetched_html'] for r in public),withheld_public_urls=sum(r['public_url_withheld'] for r in public),earliest_collection=min(r['collection_started_at'] for r in raw),latest_collection=max(r['collection_started_at'] for r in raw),source_sha256={str(p.name):sha(p) for p in [a.answers,a.release,a.controls,a.signals,a.rules,a.freeze]},outputs_sha256={p.name:sha(p) for p in sorted(a.out.glob('*.csv'))})
    (a.out/'study1-summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ['answers','release','controls','signals','rules','freeze','exclude-hosts','out']:p.add_argument('--'+name,type=Path,required=True)
    analyze(p.parse_args())
