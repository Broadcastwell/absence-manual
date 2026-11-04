"""Finite53 Research consumers, independently checked against actual sources.

This module never changes the Library registry or silently exempts a prefix.
"""
from datetime import datetime,timezone
import copy,gzip,io,json,re
from types import SimpleNamespace
from urllib.parse import urlsplit
from library_research_support import require,sha,URLS,entry,transform_datasets

SITE='https://docs.broadcastwell.com/'
FRAG=re.compile(rb'<url\b[^>]*>.*?</url>',re.S)


def research_url(source):
    require(source.startswith('docs/research/') and source.endswith('/index.md'),
        'Research source route is not a finite index page')
    return SITE+source.removeprefix('docs/').removesuffix('index.md')


def _rows(raw):
    import xml.etree.ElementTree as ET
    require(b'<!DOCTYPE' not in raw and b'<!ENTITY' not in raw,'Unsafe Research sitemap')
    root=ET.fromstring(raw);fragments=list(FRAG.finditer(raw));children=list(root)
    require(root.tag=='{http://www.sitemaps.org/schemas/sitemap/0.9}urlset'
        and len(children)==len(fragments),'Sitemap row/fragment boundary differs')
    result={}
    for child,m in zip(children,fragments):
        require(child.tag=='{http://www.sitemaps.org/schemas/sitemap/0.9}url','Unexpected sitemap child')
        url=child.findtext('{*}loc');require(url and url not in result,'Duplicate/missing sitemap URL')
        result[url]={'raw':m.group(),'lastmod':child.findtext('{*}lastmod'),'start':m.start(),'end':m.end()}
    return result


def _research_dates(permit):
    permit.check();result={}
    for path,record in permit.research_records.items():
        value=record['meta'].get('date_modified')
        try:stamp=datetime.fromisoformat(value.replace('Z','+00:00'))
        except (ValueError,TypeError,AttributeError):raise ValueError('Research exact modification timestamp missing')
        require(stamp.tzinfo is not None and stamp<=datetime.now(timezone.utc),
            'Research modification timestamp missing timezone or future')
        result[research_url('docs/'+path)]=value[:10]
    require(len(result)==53,'Exact53 Research sitemap sources missing')
    return result


def generate_research_sitemaps(prior_xml,prior_gz,*,permit,static_dataset_files):
    """Source generator: update only53 exact lastmods, then two Dataset entries."""
    permit.check();require(gzip.decompress(prior_gz)==prior_xml,'Prior generated XML/gzip disagree')
    dates=_research_dates(permit);rows=_rows(prior_xml);require(set(dates)<=set(rows),'Existing53 Research routes missing')
    result=prior_xml
    for url,row in sorted(rows.items(),key=lambda item:item[1]['start'],reverse=True):
        if url not in dates:continue
        require(row['lastmod'] is not None and row['raw'].count(b'<lastmod>')==1,'Research lastmod element absent/repeated')
        new=re.sub(rb'(<lastmod>)[^<]*(</lastmod>)',lambda m:m[1]+dates[url].encode()+m[2],row['raw'],count=1)
        result=result[:row['start']]+new+result[row['end']:]
    b=io.BytesIO()
    with gzip.GzipFile(fileobj=b,filename='',mode='wb',compresslevel=9,mtime=0) as stream:stream.write(result)
    result,compressed=transform_datasets(result,b.getvalue(),support=permit.support,static_dataset_files=static_dataset_files)
    validate_research_sitemaps(prior_xml,result,compressed,permit=permit)
    return result,compressed


def validate_research_sitemaps(before,after,compressed,*,permit):
    """Independent expected/inverse: every other XML fragment stays exact."""
    permit.check();require(gzip.decompress(compressed)==after,'Research sitemap/gzip mismatch')
    old=_rows(before);new=_rows(after);dates=_research_dates(permit)
    require(set(new)==set(old)|set(URLS),'Research sitemap adds/drops an unrelated URL')
    # Remove only the two previously absent exact generated entries, leaving
    # whitespace and all existing elements available for a byte-exact inverse.
    restored=after
    for url in URLS:
        require(url in new and new[url]['lastmod'] is None and new[url]['raw']==entry(url).strip(),
            'Dataset sitemap entry is not exact finite no-lastmod form')
        if url not in old:
            require(restored.count(entry(url))==1,'Dataset insertion spacing/boundary differs')
            restored=restored.replace(entry(url),b'',1)
        else:require(new[url]['raw']==old[url]['raw'],'Existing Dataset entry changed')
    for url,row in sorted(new.items(),key=lambda item:item[1]['start'],reverse=True):
        if url not in dates:continue
        require(row['lastmod']==dates[url] and row['raw'].count(b'<lastmod>')==1,
            'Research sitemap lastmod is not its current exact source date')
        inverse=re.sub(rb'(<lastmod>)[^<]*(</lastmod>)',lambda m:m[1]+old[url]['lastmod'].encode()+m[2],row['raw'],count=1)
        require(restored.count(row['raw'])==1,'Research sitemap element is not unique')
        restored=restored.replace(row['raw'],inverse,1)
    require(restored==before,'Research sitemap changed bytes outside53 lastmod fields/two Dataset entries')
    from library_research_release import _PROOF_TOKEN
    permit._record_proof('sitemap',{'all53_source_metadata_consumed':True,'two_exact_Dataset_entries':True,
        'all_other_XML_bytes_exact':True,'xml_sha256':sha(after),'gzip_sha256':sha(compressed)},_PROOF_TOKEN)
    return True


def validate_research_search(prior_bytes,candidate_bytes,*,permit,contexts):
    """Generate actual Material entries; preserve every other actual row."""
    permit.check();require(set(contexts)==set(permit.research_records),'Exact53 actual Research contexts required')
    old=json.loads(prior_bytes);new=json.loads(candidate_bytes)
    require({k:v for k,v in old.items() if k!='docs'}=={k:v for k,v in new.items() if k!='docs'},
        'Search non-document configuration changed')
    roots={research_url('docs/'+p).removeprefix(SITE) for p in permit.research_records}
    def selected(row):return row.get('location','').split('#')[0].lstrip('/') in roots
    require([r for r in old['docs'] if not selected(r)]==[r for r in new['docs'] if not selected(r)],
        'Search rows outside the finite53 Research pages changed')
    from material.plugins.search.plugin import SearchIndex
    generated=SearchIndex(**new['config'])
    for path,c in contexts.items():
        record=permit.research_records[path]
        require(c['markdown']==record['body'] and c['meta']==record['meta'],
            'Research search actual body/metadata is stale')
        page=SimpleNamespace(meta=record['meta'],title=record['meta']['title'],content=c['html'],toc=c['toc'],
            url=research_url('docs/'+path).removeprefix(SITE))
        generated.add_entry_from_context(page)
    require([r for r in new['docs'] if selected(r)]==generated.entries,
        'Research search rows differ from actual Material-produced53 contexts')
    from library_research_release import _PROOF_TOKEN
    permit._record_proof('search',{'finite53_entries_match_actual_contexts':True,'all_other_rows_exact':True,
        'actual_sha256':sha(candidate_bytes)},_PROOF_TOKEN)
    return True
