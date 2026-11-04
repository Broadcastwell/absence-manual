"""Actual53 source/render proof, including the existing Research wrappers."""
import re
from library_research_support import require,sha
from library_research_consumers import research_url
from library_publication_consumers import _RenderSignature,_HeadAndArticle


def validate_research_contexts(permit,contexts):
    permit.check();require(set(contexts)==set(permit.research_records),'Exact53 Research render coverage missing')
    import markdown
    for path,record in permit.research_records.items():
        c=contexts[path];meta=record['meta'];url=research_url('docs/'+path)
        require(c['markdown']==record['body'] and c['meta']==meta,'Research actual render inputs differ')
        expected=markdown.markdown(record['body'],extensions=['toc','tables','attr_list','md_in_html','def_list','footnotes','admonition'],extension_configs={'toc':{'permalink':True,'toc_depth':3}})
        # These are exactly the existing shared on_page_content transformations,
        # not an arbitrary text/structure exclusion. Every token remains checked.
        expected=re.sub(r'<a class="headerlink"(?![^>]*aria-hidden)',
            '<a class="headerlink" aria-hidden="true" tabindex="-1"',expected)
        if meta.get('page_class')=='research':
            expected=re.sub(r'(<h2\b[^>]*id="what-our-own-data-shows"[^>]*>.*?)(?=<h2\b[^>]*id="sources")',
                r'<section class="bw-own-data" aria-label="What our own data shows">\1</section>',expected,flags=re.S)
            expected='<div class="bw-research-content">'+expected+'</div>'
        expected=re.sub(r'<table(?![^>]*\btabindex=)(?=[\s>])','<table tabindex="0"',expected)
        wanted=_RenderSignature('https://docs.broadcastwell.com/'+path,True);wanted.feed(expected)
        actual=_RenderSignature(url);actual.feed(c['html'])
        require(actual.tokens==wanted.tokens,'Research actual full visible body differs from exact source: '+path)
        raw=c['rendered_html'];require(isinstance(raw,bytes),'Actual final Research HTML bytes required')
        head=_HeadAndArticle();head.feed(raw.decode())
        require(head.canonical==[url] and head.title==meta['title']+' | The Absence Manual',
            'Research canonical/title does not consume actual metadata')
        for key,value in {'description':meta['description'],'og:title':meta['title'],'og:description':meta['description'],
                'og:url':url,'twitter:title':meta['title'],'twitter:description':meta['description']}.items():
            require(head.meta.get(key)==[value],'Research social/description differs: '+key)
        articles=[a for a in head.scripts if a.get('@type')=='Article']
        require(len(articles)==1,'Research actual Article JSON-LD missing/repeated')
        for key,value in {'headline':meta.get('headline',meta['title']),'name':meta.get('headline',meta['title']),'description':meta['description'],
            'datePublished':meta['date_published'],'dateModified':meta['date_modified'],'url':url}.items():
            require(articles[0].get(key)==value,'Research structured metadata is stale: '+key)
        article=re.findall(r'<article\b[^>]*>(.*?)</article>',raw.decode(),re.S)
        footer=re.compile(r'\s*<hr>\s*<p class="manual-footer-version">Broadcastwell research\. Sources and dates are stated on each page\. Prose and derived tables CC BY 4\.0, site code MIT\. External sources retain their own licenses\. Not peer reviewed\. <a href="([^"]+)">Evidence standard</a>\.</p>\s*\Z')
        match=footer.search(article[0]) if len(article)==1 else None
        from urllib.parse import urljoin
        require(match is not None and urljoin(url,match.group(1))=='https://docs.broadcastwell.com/research/standard/'
            and article[0][:match.start()].strip()==c['html'].strip(),
            'Final Research article differs after late HTML postprocessing')
    from library_research_release import _PROOF_TOKEN
    permit._record_proof('render',{'all53_full_bodies_and_current_heads_proven':True,
        'actual_final_HTML_sha256':{p:sha(c['rendered_html']) for p,c in contexts.items()}},_PROOF_TOKEN)
    return True
