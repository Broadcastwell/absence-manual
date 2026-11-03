"""Separate S2 freeze hook; no S5 editorial overlay activation."""
from pathlib import Path
import importlib.util,json
from mkdocs.plugins import event_priority
HERE=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location('_bw_field_freeze_navigation',HERE/'library_field_freeze_navigation.py')
MODULE=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(MODULE)
# Root-adopted finite map; all source, HTML, assets and sitemap pins are mandatory.
MAP_SHA256='e8d4688604fdcb57e38944ce6937ce7fa788da73ec96b77902042990f8806f4c'
GUARD=None
def on_pre_build(config):
    global GUARD
    GUARD=MODULE.FrozenNavigation(config['docs_dir'],HERE/'library_field_freeze_navigation.json',MAP_SHA256)
@event_priority(-200)
def on_post_build(config):
    if GUARD is None:raise ValueError('Frozen navigation must validate before rendering')
    result=GUARD.post_build(config['site_dir'])
    (Path(config['site_dir']).parent/'library-field-freeze-retention.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
