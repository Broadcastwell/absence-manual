"""Collect registered public page signals; no outcome shares are computed here.

The deny file is a local, private list of domains that must never be fetched.
Raw response bodies stay in the designated local cache and are not a release.
"""
from pathlib import Path
import argparse,concurrent.futures as cf,csv,datetime as dt,fnmatch,hashlib,ipaddress,json,re,socket,threading,time
from html.parser import HTMLParser
from urllib.parse import urlsplit,urlunsplit,urljoin
from urllib.request import Request,build_opener,HTTPRedirectHandler
from urllib.error import HTTPError
from urllib.robotparser import RobotFileParser
from registration_gate import verify_registrations

UA='BroadcastwellResearchBot/1.0 (+https://docs.broadcastwell.com/research/)'
LIMIT=8*1024*1024
def stamp():return dt.datetime.now(dt.timezone.utc).isoformat()
class StopRedirect(HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):return None

class Collector:
 def __init__(self,cache,deny):
  self.cache=cache;cache.mkdir(parents=True,exist_ok=True);self.deny=deny
  self.guard=threading.Lock();self.host_locks={};self.last={};self.delays={};self.futures={};self.policies={}
  self.opener=build_opener(StopRedirect)
 def permitted_host(self,host):
  host=(host or '').lower().rstrip('.')
  if not host or any(fnmatch.fnmatchcase(host,d) or host.endswith('.'+d) for d in self.deny):return False
  try:
   ips={r[4][0] for r in socket.getaddrinfo(host,None,type=socket.SOCK_STREAM)}
   return bool(ips) and all(ipaddress.ip_address(x).is_global for x in ips)
  except OSError:return False
 def once(self,url):
  parsed=urlsplit(url)
  if parsed.scheme not in ('http','https') or parsed.username or parsed.password or not self.permitted_host(parsed.hostname):
   return {'url':url,'fetched_at':stamp(),'state':'restricted_or_nonpublic_destination'},b''
  url=urlunsplit((parsed.scheme,parsed.netloc,parsed.path or '/',parsed.query,''));key=hashlib.sha256(url.encode()).hexdigest()
  meta=self.cache/(key+'.json');bodyfile=self.cache/(key+'.bin')
  with self.guard:
   if key in self.futures:future=self.futures[key];owner=False
   else:future=cf.Future();self.futures[key]=future;owner=True
  if not owner:return future.result()
  try:
   if meta.exists():result=(json.loads(meta.read_text(encoding='utf-8')),bodyfile.read_bytes() if bodyfile.exists() else b'');future.set_result(result);return result
   host=parsed.hostname.lower()
   with self.guard:lock=self.host_locks.setdefault(host,threading.Lock())
   record={'url':url,'fetched_at':stamp()};data=b''
   with lock:
    time.sleep(max(0,self.delays.get(host,1.05)-(time.monotonic()-self.last.get(host,0))));self.last[host]=time.monotonic();start=time.monotonic()
    try:
     with self.opener.open(Request(url,headers={'User-Agent':UA,'Accept':'text/html,text/plain,application/xml;q=0.9,*/*;q=0.1'}),timeout=18) as res:
      first=res.read(1);record['ttfb_seconds']=round(time.monotonic()-start,6)
      data=first+res.read(LIMIT)
      record.update(state='oversized' if len(data)>LIMIT else 'response',status=res.status,content_type=res.headers.get('Content-Type',''),location=res.headers.get('Location',''))
    except HTTPError as e:record.update(state='response',status=e.code,content_type=e.headers.get('Content-Type',''),location=e.headers.get('Location',''),ttfb_seconds=round(time.monotonic()-start,6))
    except Exception as e:record.update(state=type(e).__name__,error=str(e)[:180])
   record['body_sha256']=hashlib.sha256(data).hexdigest();bodyfile.write_bytes(data);meta.write_text(json.dumps(record),encoding='utf-8')
   result=(record,data);future.set_result(result);return result
  except BaseException as e:future.set_exception(e);raise
 def policy(self,origin):
  with self.guard:
   if origin in self.policies:future=self.policies[origin];owner=False
   else:future=cf.Future();self.policies[origin]=future;owner=True
  if not owner:return future.result()
  try:
   url=origin+'/robots.txt';seen=set();result=(False,'unknown',None)
   for _ in range(6):
    if url in seen:break
    seen.add(url);m,b=self.once(url);status=m.get('status')
    if status in (301,302,303,307,308):url=urljoin(url,m.get('location',''));continue
    if status==200 and m['state']=='response' and 'html' not in m.get('content_type','').lower():
     text=b.decode('utf-8','replace');rp=RobotFileParser();rp.parse(text.splitlines());result=(rp,'present',bool(re.search(r'^\s*sitemap\s*:',text,re.I|re.M)))
     delay=rp.crawl_delay(UA) or rp.crawl_delay('*') or 0;rate=rp.request_rate(UA) or rp.request_rate('*')
     if rate and rate.requests:delay=max(delay,rate.seconds/rate.requests)
     with self.guard:self.delays[urlsplit(origin).hostname]=max(1.05,float(delay))
    elif status in (404,410):result=(None,'absent',False)
    break
   future.set_result(result);return result
  except BaseException as e:future.set_result((False,'unknown',None));return future.result()
 def follow(self,url):
  chain=[];seen=set()
  for _ in range(7):
   p=urlsplit(url)
   if p.scheme not in ('http','https') or not self.permitted_host(p.hostname):return {'state':'restricted_or_nonpublic_destination','url':url,'redirect_chain':chain},b''
   url=urlunsplit((p.scheme,p.netloc,p.path or '/',p.query,''))
   if url in seen:return {'state':'redirect_loop','url':url,'redirect_chain':chain},b''
   seen.add(url);origin=p.scheme+'://'+p.netloc;policy,rs,hints=self.policy(origin)
   if policy is False:return {'state':'robots_unavailable','url':url,'redirect_chain':chain,'robots_state':rs},b''
   if policy is not None and not policy.can_fetch(UA,url):return {'state':'robots_disallowed','url':url,'redirect_chain':chain,'robots_state':rs},b''
   m,b=self.once(url)
   if m.get('status') in (301,302,303,307,308):
    chain.append({'url':url,'status':m['status'],'location':m.get('location','')});url=urljoin(url,m.get('location',''));continue
   return {**m,'redirect_chain':chain,'robots_state':rs,'robots_seo_hint':hints},b
  return {'state':'redirect_limit','url':url,'redirect_chain':chain},b''
 def host_files(self,origin):
  _,rs,hint=self.policy(origin);result={'robots_txt':rs,'robots_seo_hint':hint}
  for name in ['sitemap.xml','llms.txt']:
   m,b=self.follow(origin+'/'+name);status=m.get('status');typ=m.get('content_type','').lower();state='unknown'
   if status in (404,410):state='absent'
   elif status==200 and m['state']=='response' and 'html' not in typ:
    if name=='sitemap.xml':state='present' if re.search(rb'<(?:\w+:)?(?:sitemapindex|urlset)\b',b,re.I) else 'unknown'
    else:state='present' if b.strip() and ('text/' in typ or 'markdown' in typ) else 'unknown'
   result[name.replace('.','_')]=state
  return result

class Signals(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.title=[];self.in_title=False;self.description=False;self.canonical=False;self.og=False;self.viewport=False;self.microdata=False;self.types=set();self.ld=[];self.in_ld=False;self.current=[]
 def handle_starttag(self,tag,attrs):
  a={k.lower():v for k,v in attrs};tag=tag.lower()
  if tag=='title':self.in_title=True
  if tag=='meta':
   name=(a.get('name') or '').lower();value=(a.get('content') or '').strip()
   if name=='description' and value:self.description=True
   if name=='viewport' and value:self.viewport=True
   if (a.get('property') or '').lower().startswith('og:') and value:self.og=True
  if tag=='link' and 'canonical' in (a.get('rel') or '').lower().split() and a.get('href'):self.canonical=True
  if 'itemscope' in a:self.microdata=True
  if a.get('itemtype'):self.types.update(a['itemtype'].split())
  if tag=='script' and (a.get('type') or '').lower().split(';')[0].strip()=='application/ld+json':self.in_ld=True;self.current=[]
 def handle_endtag(self,tag):
  if tag.lower()=='title':self.in_title=False
  if tag.lower()=='script' and self.in_ld:self.ld.append(''.join(self.current));self.in_ld=False
 def handle_data(self,data):
  if self.in_title:self.title.append(data)
  if self.in_ld:self.current.append(data)

def extract(data,rules):
 text=data.decode('utf-8','replace');p=Signals();p.feed(text);valid_ld=False;invalid_ld=False
 def types(obj):
  if isinstance(obj,dict):
   value=obj.get('@type',[])
   p.types.update([value] if isinstance(value,str) else [str(x) for x in value] if isinstance(value,list) else [])
   for v in obj.values():types(v)
  elif isinstance(obj,list):
   for v in obj:types(v)
 for raw in p.ld:
  try:obj=json.loads(raw);valid_ld|=bool(obj) and isinstance(obj,(dict,list));types(obj)
  except (ValueError,TypeError):invalid_ld=True
 plugins=[k for k,patterns in rules['plugins'].items() if any(re.search(x,text,re.I) for x in patterns)]
 return {'title_nonempty':bool(''.join(p.title).strip()),'description_nonempty':p.description,'canonical':p.canonical,'open_graph':p.og,'viewport':p.viewport,'json_ld':valid_ld,'json_ld_parse_failure':invalid_ld,'microdata':p.microdata,'schema_types':sorted(p.types),'seo_plugins':plugins,'analytics':any(re.search(x,text,re.I) for x in rules['analytics']),'ads':any(re.search(x,text,re.I) for x in rules['advertising'])}

def main(a):
 verify_registrations((1,2,3));rules=json.loads(a.rules.read_text(encoding='utf-8'));news={r['host'] for r in csv.DictReader(a.news.open(encoding='utf-8'))};deny={x.strip().lower() for x in a.exclude_hosts.read_text().splitlines() if x.strip() and not x.startswith('#')}
 raw=[json.loads(x) for x in a.answers.read_text(encoding='utf-8').splitlines() if x.strip()]
 occurrences=[];audit=[];units=set()
 for row in raw:
  base={k:row.get(k) for k in ['category_id','question_id','engine','repeat_index','captured_at']}
  excluded=bool(row.get('excluded',False) or row.get('exclusion_reason'))
  for i,url in enumerate(row.get('cited_urls',[])):
   item={**base,'array_index':i,'original_url':url,'excluded_answer':excluded}
   try:p=urlsplit(url);valid=p.scheme in ('http','https') and bool(p.hostname) and not p.username and not p.password
   except (ValueError,TypeError):valid=False
   if not valid:item['reason']='malformed_or_non_http';audit.append(item);continue
   if excluded:item['reason']='excluded_answer';audit.append(item);continue
   occurrences.append(item);units.add(url)
 a.out.mkdir(parents=True,exist_ok=True)
 (a.out/'study1-occurrences.json').write_text(json.dumps(occurrences),encoding='utf-8');(a.out/'study1-extraction-audit.json').write_text(json.dumps(audit),encoding='utf-8')
 # Distinct exact identifiers may share a fragment-free requested resource.
 requests=sorted({urlunsplit((*urlsplit(u)[:4],'')) for u in units})
 collector=Collector(a.cache,deny);out=a.out/'page-signals.jsonl';done={}
 if out.exists():
  for line in out.read_text(encoding='utf-8').splitlines():
   x=json.loads(line);done[x['requested_url']]=x
 def collect(url):
  record={'requested_url':url,'collection_started_at':stamp()}
  try:
   m,b=collector.follow(url);record.update(m);record['fetched_html']=m.get('status')==200 and m.get('state')=='response' and 'html' in m.get('content_type','').lower()
   if record['fetched_html']:
    record.update(extract(b,rules));p=urlsplit(m['url']);host=p.hostname.lower().removeprefix('www.');record['news_domain']=host in news
    record['https']=p.scheme=='https';record.update(collector.host_files(p.scheme+'://'+p.netloc))
  except Exception as e:record.update(state=type(e).__name__,error=str(e)[:180],fetched_html=False)
  return record
 pending=[u for u in requests if u not in done];print('Registered collection:',len(units),'exact units;',len(requests),'requested resources;',len(pending),'pending.',flush=True)
 with out.open('a',encoding='utf-8') as f,cf.ThreadPoolExecutor(max_workers=a.workers) as pool:
  futures={pool.submit(collect,u):u for u in pending}
  for i,future in enumerate(cf.as_completed(futures),1):
   record=future.result();f.write(json.dumps(record,ensure_ascii=False)+'\n');f.flush()
   if i%100==0:print('Saved page records:',i,'of',len(pending),flush=True)
 print('Collection complete. No optimization class shares computed.',flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--answers',type=Path,required=True);p.add_argument('--rules',type=Path,required=True);p.add_argument('--news',type=Path,required=True);p.add_argument('--exclude-hosts',type=Path,required=True);p.add_argument('--cache',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--workers',type=int,default=16);main(p.parse_args())
