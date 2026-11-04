"""PRIVATE finite Appendix B document-title/navigation separation proposal."""
from library_publication_overlay import canonical,require,sha
from library_publication_build import LegacyNavigationPage

PATH='absence-rules.md'
OLD_TITLE='Appendix B. Absence classification rules and precedence'
NEW_TITLE='Appendix B. Absence classification rules'


def validate_seo_source(path,before,after,source_parser):
    require(path==PATH,'SEO repair is restricted to the exact Appendix B source')
    require(isinstance(before,(bytes,str)) and isinstance(after,(bytes,str)),'Exact source text/bytes required')
    old=canonical(before.encode() if isinstance(before,str) else before)
    new=canonical(after.encode() if isinstance(after,str) else after)
    oldmeta,oldbody=source_parser(old);meta,body=source_parser(new)
    require(oldmeta.get('title')==OLD_TITLE and meta.get('title')==NEW_TITLE,'Unreviewed Appendix B title literal')
    require(oldbody==body,'Appendix B H1/body/science must remain exact')
    changed={k for k in set(oldmeta)|set(meta) if oldmeta.get(k)!=meta.get(k)}
    require(changed=={'title','date_modified'},'Appendix B permits only title and actual modification time')
    return {'path':PATH,'before_canonical_sha256':sha(old.encode()),
      'after_canonical_sha256':sha(new.encode()),'body_exact':True,
      'unchanged_headline_H1_science':True,'Root_approval_granted':False}


def retain_appendix_navigation(nav,files,*,path,before,after,source_parser):
    """Caller must already bind the exact approved Owner source-plan row.

    Only the Appendix B nav label is retained. Real document/search/social
    title uses the approved shorter title; every File.page remains original.
    """
    proof=validate_seo_source(path,before,after,source_parser)
    actual=[f.page for f in files if f.src_uri==PATH and getattr(f,'page',None) is not None]
    require(len(actual)==1,'Appendix B must have one actual MkDocs Page')
    page=actual[0];require(sum(p is page for p in nav.pages)==1,'Appendix B nav identity missing/repeated')
    if page.title is None:
        # MkDocs constructs navigation before reading untitled Page sources.
        # Admit only that untouched state and the exact already-bound after file.
        require(page.markdown is None and page.meta=={}
            and canonical(page.file.content_string.encode())==canonical(after.encode() if isinstance(after,str) else after),
            'Unread Appendix B Page differs from the exact approved source')
    else:
        require(page.title in {OLD_TITLE,NEW_TITLE},'Unexpected Appendix B navigation label')
    page.title=NEW_TITLE;view=LegacyNavigationPage(page,OLD_TITLE)
    def replace(items):
        result=[]
        for item in items:
            if getattr(item,'children',None) is not None:item.children=replace(item.children)
            result.append(view if item is page else item)
        return result
    nav.items=replace(nav.items);nav.pages=[view if p is page else p for p in nav.pages]
    if getattr(nav,'homepage',None) is page:nav.homepage=view
    for file in files:
        original=getattr(file,'page',None)
        if original is None:continue
        for attr in ['previous_page','next_page']:
            neighbor=getattr(original,attr,None)
            if neighbor is page:setattr(original,attr,view)
    require(all(getattr(f,'page',None) is not view for f in files),'Actual File.page cannot become a navigation view')
    return nav,proof
