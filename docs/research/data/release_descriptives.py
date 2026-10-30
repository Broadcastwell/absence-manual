"""Descriptive tables from published release counts, separate from Study 1.

These are additional analyses requested in the research brief, not preregistered
Study 2 host-class outcomes. No answer is recollected and no private scorer is
introduced. Inputs are the versioned public release and its archived counts.
"""
from pathlib import Path
import argparse, csv, datetime as dt, json, math, zipfile
from collections import defaultdict

def wilson(k,n):
    if not n:return ('','')
    z=1.959963984540054;p=k/n;den=1+z*z/n
    mid=(p+z*z/(2*n))/den;half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return round(100*(mid-half),4),round(100*(mid+half),4)
def table(path,rows):
    if not rows:return
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def analyze(release,out):
    out.mkdir(exist_ok=True,parents=True);repeat=defaultdict(lambda:[0,0,0]);vendors=[];concentration=[];pairs=[]
    for cat in release['categories']:
        for vendor in cat['vendors']:
            named=vendor['mention_rate'];cited=vendor['citation_rate'];k=named['count'];n=named['base'];lo,hi=wilson(k,n)
            vendors.append({'release':release['release_id'],'category':cat['id'],'vendor':vendor['name'],'canonical_domain':vendor['canonical_domain'],'named_count':k,'valid_target_base':n,'named_pct':round(100*k/n,4),'wilson_low_pct':lo,'wilson_high_pct':hi,'at_most_one_quarter':4*k<=n,'qualifying_cited_count':cited['count'],'qualifying_cited_base':cited['base'],'source':'Published release vendor counts; no fresh per-answer scoring'})
        totals=defaultdict(int);base=0
        for v in cat['vendors']:
            totals[v['name']]=v['mention_rate']['count'];base+=v['mention_rate']['count']
        strata=[('all',totals,base)]
        engine_totals=defaultdict(lambda:defaultdict(int));engine_bases=defaultdict(int)
        for cell in cat['engine_presence']:
            engine=cell['engine']
            for name,k in cell['vendor_counts'].items():
                engine_totals[engine][name]+=k;engine_bases[engine]+=k
                for key in [('all','all'),(engine,'all'),(engine,cat['id'])]:
                    if cell['base']==3:repeat[key][0]+=int(0<k<3);repeat[key][1]+=1
                    else:repeat[key][2]+=1
        strata.extend((e,t,engine_bases[e]) for e,t in engine_totals.items())
        for engine,counts,n in strata:
            ranked=sorted(counts.items(),key=lambda x:(-x[1],x[0]));k=sum(v for _,v in ranked[:3]);lo,hi=wilson(k,n)
            concentration.append({'category':cat['id'],'engine':engine,'top_three':' | '.join(x[0] for x in ranked[:3]),'top_three_named_occurrences':k,'all_checked_vendor_named_occurrences':n,'share_pct':round(100*k/n,4) if n else '','wilson_low_pct':lo,'wilson_high_pct':hi,'unit':'Checked-vendor naming occurrences; an answer can name several vendors'})
        n=sum(v['mention_rate']['base'] for v in cat['vendors']);named=sum(v['mention_rate']['count'] for v in cat['vendors']);cited=sum(v['citation_rate']['count'] for v in cat['vendors']);lo,hi=wilson(cited,named);lo2,hi2=wilson(named-cited,n)
        pairs.append({'category':cat['id'],'eligible_vendor_answer_pairs':n,'named_pairs':named,'qualifying_own_domain_cited_pairs':cited,'named_without_own_citation_pairs':named-cited,'cited_among_named_pct':round(100*cited/named,4) if named else '','cited_among_named_wilson_low':lo,'cited_among_named_wilson_high':hi,'named_without_citation_among_all_pairs_pct':round(100*(named-cited)/n,4),'without_citation_wilson_low':lo2,'without_citation_wilson_high':hi2,'provenance':'Publisher aggregate counts; qualifier dictionary is not in the deposited release, so not a new individual-verdict reproduction'})
    repeat_rows=[]
    for (engine,category),(k,n,excluded) in sorted(repeat.items()):
        lo,hi=wilson(k,n);repeat_rows.append({'engine':engine,'category':category,'mixed_complete_vendor_question_cells':k,'complete_vendor_question_cells':n,'incomplete_cells_excluded':excluded,'mixed_pct':round(100*k/n,4),'wilson_low_pct':lo,'wilson_high_pct':hi,'unit':'A checked vendor by category question by engine; mixed means named in one or two of three valid repeats'})
    total={k:sum(r[k] for r in pairs) for k in ['eligible_vendor_answer_pairs','named_pairs','qualifying_own_domain_cited_pairs','named_without_own_citation_pairs']};n=total['eligible_vendor_answer_pairs'];named=total['named_pairs'];cited=total['qualifying_own_domain_cited_pairs'];lo,hi=wilson(cited,named);lo2,hi2=wilson(named-cited,n)
    pairs.append(dict(category='all',**total,cited_among_named_pct=round(100*cited/named,4),cited_among_named_wilson_low=lo,cited_among_named_wilson_high=hi,named_without_citation_among_all_pairs_pct=round(100*(named-cited)/n,4),without_citation_wilson_low=lo2,without_citation_wilson_high=hi2,provenance=pairs[0]['provenance']))
    table(out/'vendor-presence.csv',vendors);table(out/'repeat-disagreement.csv',repeat_rows);table(out/'vendor-concentration.csv',concentration);table(out/'vendor-naming-citation.csv',pairs)
    return {'repeat': [r for r in repeat_rows if r['category']=='all'],'vendor_pair_total':pairs[-1],'low_presence_count':sum(v['at_most_one_quarter'] for v in vendors),'vendor_records':len(vendors)}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--release',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();print(json.dumps(analyze(json.loads(a.release.read_text(encoding='utf-8')),a.out),indent=2))
