"""Finite stylesheet preservation BEFORE the unchanged accepted45 guard."""
from mkdocs.plugins import event_priority


@event_priority(-190)
def on_post_build(config):
    from library_owner_repair_build import current_session,frozen_bundle_before_guard
    frozen_bundle_before_guard(current_session(),config['site_dir'])
