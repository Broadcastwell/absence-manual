"""Reproduce side-by-side published named counts; no transition is computed."""
from pathlib import Path
import argparse,csv,json,math
def interval(k,n):
 z=1.959963984540054;p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt((p*(1-p)+z*z/(4*n))/n)/d
 return round(max(0,c-h)*100,1),round(min(1,c+h)*100,1)
def compare(august,september):
 new={c['id']:c for c in september['categories']};rows=[]
 for c in august['categories']:
  nc=new[c['id']];vendors={v['name']:v for v in nc['vendors']}
  for v in c['vendors']:
   if v['name'] not in vendors:continue
   r={'category':{'crm':'CRM','project_management':'Project management'}.get(c['id'],c['id']),'vendor':v['name']}
   for prefix,entry in [('august',v),('september',vendors[v['name']])]:
    k=entry['mention_rate']['count'];n=entry['mention_rate']['base'];lo,hi=interval(k,n)
    r.update({prefix+'_count':k,prefix+'_base':n,prefix+'_pct':round(100*k/n,1),prefix+'_wilson_low':lo,prefix+'_wilson_high':hi})
   rows.append(r)
 return rows
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--august',type=Path,required=True);p.add_argument('--september',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 rows=compare(json.loads(a.august.read_text(encoding='utf-8')),json.loads(a.september.read_text(encoding='utf-8')))
 with a.out.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print('Saved',len(rows),'dated vendor rows. No persistence or change estimate computed.')
