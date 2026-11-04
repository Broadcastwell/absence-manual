"""Actual-prior finite presentation retention after Owner repair.

Only the accepted45 stylesheet href/asset and the one Appendix B legacy nav
label are retained. The unchanged full frozen/public guards still run after it.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit
import re
from library_publication_overlay import require,sha,canonical

PATH='absence-rules.md'
OLD='Appendix B. Absence classification rules and precedence'
NEW='Appendix B. Absence classification rules'
HEADLINE=('Absence classification rules and precedence: the six question shapes, their '
          'regular-expression rules and the fixed order in which they are applied')


class AppendixNavLabel(HTMLParser):
    def __init__(self):super().__init__();self.depth=0;self.active=False;self.parts=[];self.labels=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='nav':
            if self.depth:self.depth+=1
            elif 'md-nav--primary' in a.get('class','').split():self.depth=1
        link=urlsplit(urljoin('https://docs.broadcastwell.com/absence-rules/',a.get('href','')))
        if self.depth and tag=='a' and link.path=='/absence-rules/' and not link.fragment:
            require(not self.active,'Nested Appendix nav link');self.active=True;self.parts=[]
    def handle_endtag(self,tag):
        if tag=='a' and self.active:self.labels.append(' '.join(''.join(self.parts).split()));self.active=False
        if tag=='nav' and self.depth:self.depth-=1
    def handle_data(self,data):
        if self.active:self.parts.append(data)


def retain_appendix_from_actual_prior(nav,files,session):
    from library_publication_build import LegacyNavigationPage
    from library_publication_consumers import _HeadAndArticle
    full=canonical((session.docs/PATH).read_bytes());meta,body=session.overlay.finite.source_body(full)
    if meta.get('title')==OLD:return nav,None
    require(meta.get('title')==NEW and meta.get('headline')==HEADLINE and body.startswith('# '+OLD+'\n'),
        'Inherited Appendix source no longer has its exact reviewed title/H1')
    prior=session.archive.read('absence-rules/index.html');head=_HeadAndArticle();head.feed(prior.decode())
    require(head.title==NEW+' | The Absence Manual' and head.canonical==['https://docs.broadcastwell.com/absence-rules/'],
        'Actual prior Appendix document title/canonical does not prove inherited state')
    reader=AppendixNavLabel();reader.feed(prior.decode());reader.close()
    require(reader.labels==[OLD],'Actual prior primary-nav Appendix label differs')
    actual=[f.page for f in files if f.src_uri==PATH and getattr(f,'page',None) is not None]
    require(len(actual)==1 and sum(p is actual[0] for p in nav.pages)==1,'Inherited Appendix original Page missing/repeated')
    page=actual[0]
    if page.title is None:
        require(page.markdown is None and page.meta=={}
            and canonical(page.file.content_string.encode())==full,
            'Unread inherited Appendix Page differs from its checked source')
    else:require(page.title in {OLD,NEW},'Unexpected inherited Appendix Page label')
    page.title=NEW;view=LegacyNavigationPage(page,OLD)
    def replace(items):
        out=[]
        for item in items:
            if getattr(item,'children',None) is not None:item.children=replace(item.children)
            out.append(view if item is page else item)
        return out
    nav.items=replace(nav.items);nav.pages=[view if p is page else p for p in nav.pages]
    if getattr(nav,'homepage',None) is page:nav.homepage=view
    for file in files:
        original=getattr(file,'page',None)
        if original is None:continue
        for attr in ['previous_page','next_page']:
            if getattr(original,attr,None) is page:setattr(original,attr,view)
    require(all(getattr(f,'page',None) is not view for f in files),'Inherited Appendix replaced actual File.page')
    return nav,{'inherited_actual_prior_HTML_sha256':sha(prior),'current_source_sha256':sha(full.encode()),
        'legacy_nav_label_exact':OLD,'document_title_exact':NEW,'new_repair_or_approval':False}


def retain_frozen_stylesheets_from_actual_prior(session,site_dir):
    from library_publication_build import BuildSession
    from library_owner_repair import OLD_CSS,OLD_CSS_SHA256,restore_frozen_stylesheet
    require(isinstance(session,BuildSession),'Inherited presentation requires owning compiled BuildSession')
    session.overlay._check_unchanged();session.freeze.assert_current()
    site=Path(site_dir).resolve();old=session.archive.read(OLD_CSS)
    require(sha(old)==OLD_CSS_SHA256,'Inherited accepted old bundle differs')
    bundles=list(site.glob('assets/stylesheets/combined-*.css'))
    new=[p for p in bundles if p.relative_to(site).as_posix()!=OLD_CSS]
    if not new:
        require((site/OLD_CSS).is_file() and (site/OLD_CSS).read_bytes()==old,
            'No inherited current stylesheet bundle exists')
        return {'old_bundle_already_current':True,'new_change_authorized':False}
    require(len(new)==1,'Inherited rendering has an extra stylesheet bundle')
    path=new[0].relative_to(site).as_posix();raw=new[0].read_bytes()
    require(path=='assets/stylesheets/combined-'+sha(raw)[:16]+'.css'
        and path in session.archive.namelist() and session.archive.read(path)==raw,
        'Inherited rendering changed the current actual-prior stylesheet')
    target=site/OLD_CSS
    if target.exists():require(target.read_bytes()==old,'Existing inherited old bundle differs')
    else:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(old)
    for row in session.freeze.data['rows']:
        page=row['served_html_path'];p=site/page;current=p.read_bytes()
        restored=restore_frozen_stylesheet(page=page,before=session.archive.read(page),candidate=current,
            new_bundle_path=path,new_bundle_bytes=raw,baseline_files={OLD_CSS:old})
        if restored!=current:p.write_bytes(restored)
    return {'exact45_inherited_stylesheet_fragments_only':True,'new_change_authorized':False}
