"""Three explicit policies. Missing/unknown/mixed active keys fail closed."""
import os
from library_publication_overlay import require
_CURRENT=None


class OrdinaryHookSession:
    def __init__(self,session):self._session=session
    def __getattr__(self,name):return getattr(self._session,name)
    def retain_owner_navigation(self,nav,files):
        from library_publication_build import retain_legacy_navigation
        from library_inherited_presentation import retain_appendix_from_actual_prior
        nav=retain_legacy_navigation(nav,files,self._session.overlay,self._session.aliases)
        nav,self.appendix_nav_proof=retain_appendix_from_actual_prior(nav,files,self._session)
        return nav


def from_environment(config):
    global _CURRENT
    _CURRENT=None
    groups=[{k for k in os.environ if k.startswith(prefix)} for prefix in
        ['BW_LIBRARY_PUBLICATION_','BW_OWNER_REPAIR_','BW_RESEARCH_RELEASE_','BW_LIBRARY_FOLLOWUP_']]
    require(sum(bool(g) for g in groups)<=1,'Ordinary S5/Owner/Research active modes cannot mix')
    expected=[{'BW_LIBRARY_PUBLICATION_INPUTS','BW_LIBRARY_PUBLICATION_INPUTS_SHA256'},
        {'BW_OWNER_REPAIR_INPUTS','BW_OWNER_REPAIR_INPUTS_SHA256'},
        {'BW_RESEARCH_RELEASE_INPUTS','BW_RESEARCH_RELEASE_INPUTS_SHA256'},
        {'BW_LIBRARY_FOLLOWUP_PLAN_SHA256'}]
    for group,allowed in zip(groups,expected):
        if group:require(group==allowed,'Unknown/partial explicit build policy environment')
    if groups[3]:
        from library_followup_release import FollowupSession, PLAN, sha
        from pathlib import Path
        root=Path(config['docs_dir']).resolve().parent
        require(os.environ['BW_LIBRARY_FOLLOWUP_PLAN_SHA256']==sha((root/PLAN).read_bytes()), 'Follow-up environment does not bind the reviewed plan')
        _CURRENT=FollowupSession.load(config);return _CURRENT
    if groups[2]:
        from library_research_build import from_environment as research
        _CURRENT=research(config);return _CURRENT
    if groups[1]:
        from library_owner_repair_build import from_environment as owner
        _CURRENT=owner(config);return _CURRENT
    from library_publication_build import from_environment as ordinary
    _CURRENT=OrdinaryHookSession(ordinary(config));return _CURRENT


def current_session():
    require(_CURRENT is not None,'No exact current owning build session')
    return _CURRENT
