"""Finite current/prior stylesheet retention, before unchanged45 guard."""
from mkdocs.plugins import event_priority


@event_priority(-190)
def on_post_build(config):
    from library_build_dispatch import current_session,OrdinaryHookSession
    from library_research_build import ResearchBuildSession
    from library_owner_repair_build import OwnerRepairBuildSession,frozen_bundle_before_guard
    from library_inherited_presentation import retain_frozen_stylesheets_from_actual_prior
    session=current_session()
    from library_followup_release import FollowupSession
    if isinstance(session,FollowupSession):
        session.retain_styles(config['site_dir'])
    elif isinstance(session,OwnerRepairBuildSession):
        frozen_bundle_before_guard(session,config['site_dir'])
    elif isinstance(session,ResearchBuildSession):
        retain_frozen_stylesheets_from_actual_prior(session.base,config['site_dir'])
    else:
        if not isinstance(session,OrdinaryHookSession):raise ValueError('Unknown stylesheet-retention policy session')
        retain_frozen_stylesheets_from_actual_prior(session._session,config['site_dir'])
