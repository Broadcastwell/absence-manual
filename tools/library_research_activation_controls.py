"""Exact controls for the owner's single-PR Research activation.

The prior publication archive stays immutable. Only the listed, reviewed
activation code and individually pinned input files may accompany Research's
60 source files. This is not an allowance for arbitrary non-Research edits.
"""
from pathlib import Path
from library_research_support import require, sha, _file

BUNDLE = 'tools/library-research-inputs/'
ACTIVATION_CODE = frozenset({
    '.gitattributes', '.gitignore', '.github/workflows/verify.yml',
    'tools/library_research_activation.py',
    'tools/library_research_activation_controls.py',
    'tools/library_research_support.py',
    'tools/library_research_source_archive.py',
    'tools/library_research_release.py',
    'tests/test_research_activation.py',
    'tools/library_published_discovery_consumer_five.py',
    'tests/test_published_discovery_consumer_five.py',
    'tools/library_inherited_presentation.py',
    'tests/test_research_support.py',
    'tools/library_research_render.py',
})


def is_control(path):
    return path in {'tools/library-research-support.json',
                    'tools/library-research-support.sha256'} or path.startswith(BUNDLE)


def bundle_file(staged):
    require(staged.startswith('.library-research-work/') and '..' not in Path(staged).parts,
            'Research bundle staging path differs')
    return BUNDLE + staged.removeprefix('.library-research-work/')


def validate_bundle(root, plan):
    delivery = plan.get('activation_delivery')
    if delivery is None:
        return set()
    fields={'external_files', 'prior_source_commit', 'prior_artifact_id'}
    require(set(delivery) in [fields,fields|{'source_archive_parts'}],
            'Research activation delivery schema differs')
    if 'source_archive_parts' in delivery:
        require(delivery['source_archive_parts']==[
            '.library-research-work/source-archive/part-%02d.bin'%i for i in range(1,4)],
            'Approved source archive needs exactly three ordered pinned parts')
        require(all(p in plan['staged_file_sha256'] for p in delivery['source_archive_parts']),
            'An approved source archive part is not pinned')
    external = delivery['external_files']
    require(set(external) == {'.library-research-work/prior-public.zip',
                             '.library-research-work/prior-source.gitLF.zip'},
            'Only the exact prior public and source archives may be supplied externally')
    manifest = plan['staged_file_sha256']
    require(all(manifest.get(p) == h for p, h in external.items()),
            'External Research archive pins differ from the approved closure')
    expected = {bundle_file(p): h for p, h in manifest.items() if p not in external}
    directory = Path(root) / BUNDLE
    actual = {p.relative_to(root).as_posix() for p in directory.rglob('*') if p.is_file()}
    require(actual == set(expected), 'Committed Research bundle has missing or unlisted files')
    for p, h in expected.items():
        require(sha(_file(root, p).read_bytes()) == h, 'Committed Research input bytes changed: ' + p)
    return set(expected)


def validate_activation_delta(root, support, data, before, after):
    changes = data.get('reviewed_activation_source_changes')
    if changes is None:
        return set()
    require(support.plan.get('activation_delivery') is not None,
            'Activation source bridge requires the complete committed bundle')
    require(set(changes) == ACTIVATION_CODE, 'Activation code scope differs from the finite route')
    for path, row in changes.items():
        require(set(row) == {'before_sha256', 'after_sha256'}, 'Activation source pin schema differs')
        require(row['before_sha256'] == (sha(before[path]) if path in before else None)
                and path in after and row['after_sha256'] == sha(after[path])
                and _file(root, path).read_bytes() == after[path],
                'Reviewed activation source changed: ' + path)
    controls = validate_bundle(root, support.plan)
    require(all(after.get(p) == _file(root, p).read_bytes() for p in controls),
            'Candidate archive omits or changes an approved Research control')
    return set(changes) | controls
