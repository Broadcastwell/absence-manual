"""Final structural verifier binding for exact reviewed static canonical stubs.

No HTTP301 or observed200 claim. Ordinary pages keep every existing check.
"""
from __future__ import annotations
import copy,json,os,re,tempfile
from pathlib import Path
from html.parser import HTMLParser
from library_publication_overlay import require,sha,read_bound_json
from library_publication_canonical_stub import (POLICY,STATUS,OWNER_QUOTE_SHA256,
    SITE,stub_artifact_path,validate_canonical_stub_bytes)
from library_publication_release import route_for


class Canonicals(HTMLParser):
    def __init__(self):super().__init__();self.urls=[]
    def handle_starttag(self,tag,attrs):
        if tag.lower()!='link':return
        values=dict(attrs)
        if 'canonical' in str(values.get('rel','')).lower().split():
            require(len(values)==len(attrs),'Target canonical has duplicate attributes')
            self.urls.append(values.get('href'))


def validate_stub_artifacts(overlay,site):
    """Called only on a BuildSession whose complete approved inputs rebound."""
    site=Path(site);overlay._check_unchanged()
    dispositions=overlay.merge_statuses;result={}
    require(isinstance(dispositions,dict),'Missing exact canonical dispositions')
    for source,row in sorted(dispositions.items()):
        require(row.get('status')==STATUS and row.get('article_pass') is False
            and row.get('policy')==POLICY and row.get('owner_quote_sha256')==OWNER_QUOTE_SHA256,
            'Unreviewed/noncanonical disposition cannot bypass article checks')
        target=row.get('target_path')
        require(target in overlay.records and target not in dispositions and target!=source,
                'Canonical stub target must be a current article, never a chain')
        decision=overlay._load_receipt(row.get('decision_receipt_sha256'))
        require(decision and decision.get('approved') is True
            and decision.get('review_kind')=='reviewed-source-fit-canonical-stub'
            and decision.get('source_fit_status')==STATUS
            and decision.get('source_path')==source and decision.get('target_path')==target
            and decision.get('source_canonical_sha256')==row.get('source_canonical_sha256')
            and decision.get('owner_quote_sha256')==OWNER_QUOTE_SHA256
            and decision.get('stub_html_sha256')==row.get('stub_html_sha256')
            and decision.get('meta_refresh_seconds')==row.get('meta_refresh_seconds'),
            'Exact approved canonical-stub decision missing or stale')
        artifact=stub_artifact_path(source);path=site/artifact
        require(path.is_file(),'Exact canonical stub artifact missing')
        validate_canonical_stub_bytes(source,row,path.read_bytes())
        require(not (site/source).exists() and not (site/(route_for(source).strip('/')+'.html')).exists(),
                'Unreviewed alternate stub source/HTML artifact remains')
        target_path=site/stub_artifact_path(target)
        require(target_path.is_file(),'Canonical stub target HTML missing')
        reader=Canonicals();reader.feed(target_path.read_text(encoding='utf-8'));reader.close()
        require(reader.urls==[SITE+route_for(target)],'Canonical stub target is not its exact public self-canonical')
        result[source]={'artifact_path':artifact,'target_path':target,
            'stub_html_sha256':row['stub_html_sha256'],'target_html_sha256':sha(target_path.read_bytes()),
            'intended_static_status':200,'http_status_observed':None,'live_http_301_verified':False}
    return result


def _logical_inputs(value):
    d=copy.deepcopy(value)
    d['files']={k:{'sha256':r['sha256']} for k,r in d['files'].items()}
    d['receipt_files']=[{'sha256':r['sha256']} for r in d.get('receipt_files',[])]
    return d


def reviewed_stub_pages(root,site,environment=None):
    """No inputs means no exception; a partial/invalid active input fails."""
    env=os.environ if environment is None else environment
    followup_keys={k for k in env if k.startswith('BW_LIBRARY_FOLLOWUP_')}
    if followup_keys:
        require(followup_keys=={'BW_LIBRARY_FOLLOWUP_PLAN_SHA256'}
            and not any(k.startswith(('BW_LIBRARY_PUBLICATION_','BW_OWNER_REPAIR_','BW_RESEARCH_RELEASE_')) for k in env),
            'Follow-up final-stub dispatch: unknown, partial or mixed mode')
        from library_followup_release import FollowupSession, PLAN
        require(env['BW_LIBRARY_FOLLOWUP_PLAN_SHA256']==sha((Path(root)/PLAN).read_bytes()),
            'Follow-up final-stub plan pin differs')
        session=FollowupSession.load({'docs_dir':str(Path(root)/'docs')})
        try:
            proof=validate_stub_artifacts(session.previous.overlay,site)
            require(len(proof)==19 and set(proof)==set(session.base.prior['merged_sources']),
                'Follow-up final guard lost exact19 inherited decisions')
            return proof
        finally:
            session.archive.close()
            session.previous.archive.close()
    research_keys={k for k in env if k.startswith('BW_RESEARCH_RELEASE_')}
    if research_keys:
        require(research_keys=={'BW_RESEARCH_RELEASE_INPUTS','BW_RESEARCH_RELEASE_INPUTS_SHA256'}
            and not any(k.startswith(('BW_LIBRARY_PUBLICATION_','BW_OWNER_REPAIR_')) for k in env),
            'Research final-stub dispatch: unknown, partial or mixed mode')
        return _reviewed_research_stub_pages(root,site,env)
    owner_keys={k for k in env if k.startswith('BW_OWNER_REPAIR_')}
    if owner_keys:
        require(owner_keys=={'BW_OWNER_REPAIR_INPUTS','BW_OWNER_REPAIR_INPUTS_SHA256'}
            and not any(k in env for k in ['BW_LIBRARY_PUBLICATION_INPUTS','BW_LIBRARY_PUBLICATION_INPUTS_SHA256']),
            'Owner repair final-stub dispatch: unknown, partial or mixed mode')
        return _reviewed_owner_stub_pages(root,site,env)
    path=env.get('BW_LIBRARY_PUBLICATION_INPUTS');pin=env.get('BW_LIBRARY_PUBLICATION_INPUTS_SHA256')
    if not path and not pin:return {}
    require(path and re.fullmatch('[0-9a-f]{64}',str(pin)),
            'Final stub verification needs both exact staged input bindings')
    root=Path(root);blue_path=root/'tools/library-publication/release.json'
    blue=json.loads(blue_path.read_text(encoding='utf-8'))
    require(blue.get('schema_version')==1 and blue.get('approved') is True,
            'Final stub exception requires the committed Root-approved blueprint')
    staged=read_bound_json(path,pin)
    require(_logical_inputs(staged)==_logical_inputs(blue['inputs']),
            'Staged final-stub inputs differ from the committed approved blueprint')
    # Reuse all owning source/prior/field/receipt/fact/alias/target guards;
    # no caller list, path-pattern or claimed stub flag creates an exemption.
    from library_publication_build import BuildSession
    with tempfile.TemporaryDirectory(prefix='bw-final-stub-proof-') as work:
        session=BuildSession.load(root/'docs',path,pin,work)
        try:return validate_stub_artifacts(session.overlay,site)
        finally:session.archive.close()


def _reviewed_owner_stub_pages(root,site,environment):
    """Explicit Owner dispatch; every ordinary article still runs normal checks."""
    root=Path(root);path=environment['BW_OWNER_REPAIR_INPUTS'];pin=environment['BW_OWNER_REPAIR_INPUTS_SHA256']
    require(path and re.fullmatch('[0-9a-f]{64}',str(pin)),'Exact Owner inputs missing')
    from library_owner_repair import POLICY as OWNER_POLICY
    from library_owner_repair_build import OwnerRepairBuildSession,bound_file
    blue_path=root/'tools/library-owner-repair/release.json'
    blue=json.loads(blue_path.read_text(encoding='utf-8'))
    require(blue.get('schema_version')==1 and blue.get('policy')==OWNER_POLICY
        and blue.get('approved') is True and blue.get('review_kind')=='root-exact-owner-repair-inputs',
        'Committed Root Owner blueprint missing')
    ref=blue.get('owner_inputs',{})
    require(ref.get('sha256')==pin and blue.get('files',{}).get(ref.get('path'))==pin,
        'Owner staged/committed input hash differs')
    committed=bound_file(blue_path.parent,ref)[1]
    require(Path(path).is_file() and Path(path).read_bytes()==committed,'Staged Owner input bytes differ')
    for rel,file_pin in blue['files'].items():bound_file(blue_path.parent,{'path':rel,'sha256':file_pin})
    with tempfile.TemporaryDirectory(prefix='bw-owner-final-stub-proof-') as work:
        session=OwnerRepairBuildSession.load(root/'docs',path,pin,work)
        try:
            session.check_repair()
            from library_owner_repair_post_s5 import validate_inherited_closure
            files={p.relative_to(Path(site)).as_posix():p.read_bytes() for p in Path(site).rglob('*') if p.is_file()}
            validate_inherited_closure(session.overlay,session.post_s5_binding,files)
            return validate_stub_artifacts(session.overlay,site)
        finally:session.archive.close()


def _reviewed_research_stub_pages(root,site,environment):
    """Actual approved Research source plan; original19 decisions stay owning."""
    from library_research_build import ResearchBuildSession
    path=environment['BW_RESEARCH_RELEASE_INPUTS'];pin=environment['BW_RESEARCH_RELEASE_INPUTS_SHA256']
    require(path and re.fullmatch('[0-9a-f]{64}',str(pin)),'Exact Research staged inputs missing')
    with tempfile.TemporaryDirectory(prefix='bw-Research-final-stub-proof-') as work:
        session=ResearchBuildSession.load(Path(root)/'docs',path,pin,work)
        try:
            proof=validate_stub_artifacts(session.overlay,site)
            require(len(proof)==19 and set(proof)==set(session.base.prior['merged_sources']),
                'Research final guard lost exact19 inherited decisions')
            return proof
        finally:session.archive.close()
