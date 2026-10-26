"""Fail closed unless the verified preview is the complete production tree."""
import json
import os
from pathlib import Path
import subprocess
import sys

REQUIRED = ('index.html', 'llms.txt', 'absence-manual.pdf', 'sitemap.xml', 'CNAME')

def validate_preview(site, expected):
    site = Path(site)
    proof = json.loads((site / 'relaunch-build-provenance.json').read_text(encoding='utf8'))
    if proof != expected:
        raise ValueError('Verified artifact provenance does not match this production tree')
    for name in REQUIRED:
        if not (site / name).is_file():
            raise ValueError('Verified preview is incomplete: ' + name)
    return proof

if __name__ == '__main__':
    site = Path(sys.argv[1] if len(sys.argv) > 1 else 'site')
    tree = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'], text=True).strip()
    validate_preview(site, {
        'source_head': os.environ['EXPECTED_HEAD'], 'source_tree': tree,
        'repository': os.environ['GITHUB_REPOSITORY'], 'run_id': os.environ['EXPECTED_RUN'],
    })
    (site / 'relaunch-build-provenance.json').unlink()
    print('The complete verified artifact matches the production tree; no rebuild required.')
