"""Finite research headline review and static Dataset sitemap additions.

No network, measurements or edits to research observations. Shared callers are
owned by the Library desk; this module owns only research policy and two URLs.
"""
from pathlib import Path
import gzip
import hashlib
import json
import re
import xml.etree.ElementTree as ET

HEADLINE = re.compile(r'(?<![\d.])(?:40|41)(?:\.0)?\s*(?:%|\bpercent\b)', re.I)
RETIRED = re.compile(r'Category Audit|Re-measure|\$(?:190|990|2,900|2,410|4,500|13,500)\b', re.I)
DATASET_URLS = (
    'https://docs.broadcastwell.com/assets/research/change-desk/2026-10-26/connectwise-statements-ai/',
    'https://docs.broadcastwell.com/assets/research/change-desk/2026-10-26/software-transaction-state/',
)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def historical_order(sentence):
    # A publication year alone cannot excuse a current retired offer.
    return bool(re.search(r'\b(?:historical|retired|superseded)\b',sentence,re.I)
                and re.search(r'\b(?:order|invoice|purchase)\s+(?:dated\s+|date\s*[:=]?\s*)?20\d{2}-\d{2}-\d{2}\b',sentence,re.I)
                and not re.search(r'\b(?:buy|available|order now|purchase now|we offer)\b',sentence,re.I))

def check_sources(root):
    root=Path(root)
    policy_path=root/'docs/research/data/research-release-policy.json'
    if not policy_path.is_file():
        return ['Research release policy is missing.']
    policy=json.loads(policy_path.read_text(encoding='utf-8'))
    approved=policy['reviewed_headline_files']
    historical=policy['immutable_historical_files']
    errors=[]
    for p in (root/'docs/research').rglob('*'):
        if not p.is_file() or p==policy_path or p.suffix not in ('.md','.csv','.json'):
            continue
        rel=p.relative_to(root).as_posix()
        raw=p.read_bytes()
        text=raw.decode('utf-8-sig')
        if HEADLINE.search(text):
            record=historical.get(rel) or approved.get(rel)
            if not record or sha(raw)!=record['sha256']:
                errors.append(rel+': 40%/41% text is outside the finite reviewed fragile or historical context.')
        if p.suffix=='.md':
            body=re.sub(r'(?ms)^```.*?^```\s*$', '',text)
            for sentence in re.split(r'(?<=[.!?])\s+|\n\s*\n',body):
                if RETIRED.search(sentence) and not historical_order(sentence):
                    errors.append(rel+': retired offer/name lacks an explicit historical date: '+sentence[:180])
                if re.search(r'\bDiagnostic\b',sentence,re.I) and re.search(r'\b(?:buy|order|purchase|offer|costs?|priced?)\b',sentence,re.I) and not historical_order(sentence):
                    errors.append(rel+': Diagnostic presented as an undated offer.')
    for rel,record in historical.items():
        p=root/rel
        if not p.is_file() or sha(p.read_bytes())!=record['sha256']:
            errors.append(rel+': immutable historical evidence bytes changed.')
    for rel in policy['fragile_framing_pages']:
        p=root/rel
        if not p.is_file() or policy['fragile_framing'] not in p.read_text(encoding='utf-8'):
            errors.append(rel+': complete required fragile framing is missing.')
    return errors

def add_sitemap(site_dir):
    site=Path(site_dir)
    xml=site/'sitemap.xml'
    raw=xml.read_bytes()
    before=raw
    root=ET.fromstring(raw)
    locations=[x.text for x in root.findall('{*}url/{*}loc')]
    for url in DATASET_URLS:
        rel=url.removeprefix('https://docs.broadcastwell.com/')+'index.html'
        if not (site/rel).is_file():
            raise ValueError('Dataset page is absent: '+rel)
        if locations.count(url)>1:
            raise ValueError('Dataset sitemap entry is duplicated: '+url)
        if url not in locations:
            addition=('  <url>\n    <loc>'+url+'</loc>\n  </url>\n').encode()
            if raw.count(b'</urlset>')!=1:
                raise ValueError('Unexpected sitemap closing structure.')
            raw=raw.replace(b'</urlset>',addition+b'</urlset>')
    # Insertion preserves every existing sitemap entry byte for byte.
    if raw!=before:
        xml.write_bytes(raw)
        (site/'sitemap.xml.gz').write_bytes(gzip.compress(raw,mtime=0))
    final=ET.fromstring(raw)
    found=[x.text for x in final.findall('{*}url/{*}loc')]
    if not all(found.count(url)==1 for url in DATASET_URLS):
        raise ValueError('Research Dataset sitemap additions did not verify.')
    if gzip.decompress((site/'sitemap.xml.gz').read_bytes())!=raw:
        raise ValueError('Compressed sitemap differs from XML.')
    return {'dataset_urls':list(DATASET_URLS),'total_urls':len(found),'existing_xml_bytes_preserved':True}

if __name__=='__main__':
    import sys
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[3]
    failures=check_sources(root)
    print('\n'.join(failures) if failures else 'Research headline and retired-offer gates passed.')
    raise SystemExit(bool(failures))
