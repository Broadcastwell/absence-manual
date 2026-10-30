"""Inventory first tokens in the released target-question bank, not search demand."""
from pathlib import Path
import csv,json,sys,math
from collections import Counter
source,out=map(Path,sys.argv[1:]);out.mkdir(parents=True,exist_ok=True)
d=json.loads(source.read_text(encoding='utf-8'))
rows=[dict(category=c['id'],question_id=q['id'],question=q['text'],first_token=q['text'].strip().split()[0].lower()) for c in d['categories'] for q in c['questions']]
counts=Counter(r['first_token'] for r in rows);n=len(rows)
def write(name,values):
 with (out/name).open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=list(values[0]),lineterminator='\n');w.writeheader();w.writerows(values)
summary=[]
for name in ['what','best','which','how','other']:
 k=counts[name] if name!='other' else sum(v for t,v in counts.items() if t not in ['what','best','which','how'])
 z=1.959963984540054;p=k/n;den=1+z*z/n;center=(p+z*z/(2*n))/den;half=z*math.sqrt((p*(1-p)+z*z/(4*n))/n)/den
 summary.append(dict(first_token_group=name,count=k,target_questions=n,percent=round(100*p,4),wilson_low=round(100*max(0,center-half),4),wilson_high=round(100*min(1,center+half),4),scope='Fixed released bank; not a random sample or search-demand estimate'))
write('target-question-inventory.csv',rows);write('target-question-first-words.csv',summary)
print(json.dumps(summary,indent=2))
