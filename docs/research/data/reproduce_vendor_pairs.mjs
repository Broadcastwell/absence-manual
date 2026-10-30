// Deterministic secondary-data analysis using the publisher's public matching function.
// Arguments: publisher matching module, published input JSON, answer JSONL, release JSON, output directory.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
const [moduleFile,inputFile,answerFile,releaseFile,outDir]=process.argv.slice(2);
if(!outDir)throw Error('Five input/output paths required.');
const {matchVendor}=await import(pathToFileURL(path.resolve(moduleFile)));
const inputBytes=fs.readFileSync(inputFile);
if(crypto.createHash('sha256').update(inputBytes).digest('hex')!=='5f94ee1c2aaa9d6d7d4e8176e781f2a78e4f4bcab15077f051b8ccc8255795ac')throw Error('Published input hash mismatch');
const input=JSON.parse(inputBytes),release=JSON.parse(fs.readFileSync(releaseFile,'utf8'));
const answers=fs.readFileSync(answerFile,'utf8').trim().split(/\r?\n/).map(JSON.parse);
const observations=[],strata=new Map(),reconciled=[];
function wilson(k,n){if(!n)return ['',''];const z=1.959963984540054,d=1+z*z/n,p=k/n,c=(p+z*z/(2*n))/d,h=z*Math.sqrt((p*(1-p)+z*z/(4*n))/n)/d;return [Math.max(0,c-h)*100,Math.min(1,c+h)*100].map(v=>Number(v.toFixed(4)));}
function add(engine,category,named,cited){const key=JSON.stringify([engine,category]);if(!strata.has(key))strata.set(key,{engine,category,eligible_vendor_answer_pairs:0,named_pairs:0,own_domain_cited_pairs:0,named_without_own_citation_pairs:0});const r=strata.get(key);r.eligible_vendor_answer_pairs++;r.named_pairs+=Number(named);r.own_domain_cited_pairs+=Number(cited);r.named_without_own_citation_pairs+=Number(named&&!cited);}
function csv(file,rows){const cell=v=>'"'+String(v??'').replaceAll('"','""')+'"';fs.writeFileSync(path.join(outDir,file),Object.keys(rows[0]).map(cell).join(',')+'\n'+rows.map(r=>Object.values(r).map(cell).join(',')).join('\n')+'\n');}
for(const c of input.categories){
 const rc=release.categories.find(x=>x.id===c.id);if(!rc)throw Error('Unmatched release category '+c.id);
 const ids=new Set(c.questions.map(q=>q.id));const valid=answers.filter(r=>r.category_id===c.id&&ids.has(r.question_id)&&!r.excluded);
 for(const v of c.vendors){let named=0,cited=0;
  for(const a of valid){const m=matchVendor(v,a.answer_text,a.cited_urls);named+=Number(m.named);cited+=Number(m.cited);
   observations.push({category:c.id,vendor:v.name,engine:a.engine,question_id:a.question_id,repeat:a.repeat_index,capture_date:a.captured_at,named:Number(m.named),own_domain_cited:Number(m.cited)});
   for(const [e,cat] of [[a.engine,c.id],[a.engine,'all'],['all',c.id],['all','all']])add(e,cat,m.named,m.cited);
  }
  const rv=rc.vendors.find(x=>x.name===v.name);const ok=rv&&named===rv.mention_rate.count&&cited===rv.citation_rate.count&&valid.length===rv.mention_rate.base&&valid.length===rv.citation_rate.base;
  reconciled.push({category:c.id,vendor:v.name,reproduced_named:named,published_named:rv?.mention_rate.count,reproduced_cited:cited,published_cited:rv?.citation_rate.count,valid_base:valid.length,reconciles:Number(Boolean(ok))});
 }
}
fs.mkdirSync(outDir,{recursive:true});csv('vendor-pair-reconciliation.csv',reconciled);
const bad=reconciled.filter(r=>!r.reconciles);if(bad.length)throw Error('Publisher reconciliation failed for '+bad.length+' vendor records; pair outcomes withheld.');
const rows=[...strata.values()].sort((a,b)=>(a.category+'|'+a.engine).localeCompare(b.category+'|'+b.engine)).map(r=>{const a=wilson(r.own_domain_cited_pairs,r.named_pairs),b=wilson(r.named_without_own_citation_pairs,r.eligible_vendor_answer_pairs);return {...r,cited_among_named_pct:Number((100*r.own_domain_cited_pairs/r.named_pairs).toFixed(4)),cited_among_named_wilson_low:a[0],cited_among_named_wilson_high:a[1],named_without_citation_among_all_pct:Number((100*r.named_without_own_citation_pairs/r.eligible_vendor_answer_pairs).toFixed(4)),without_citation_wilson_low:b[0],without_citation_wilson_high:b[1]};});
csv('vendor-pairs.csv',observations);csv('vendor-pair-summary.csv',rows);
console.log(JSON.stringify({reconciled_vendor_records:reconciled.length,pair_rows:observations.length,overall:rows.find(r=>r.category==='all'&&r.engine==='all')},null,2));
