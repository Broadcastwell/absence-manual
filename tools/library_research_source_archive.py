"""Exact GitLF source coverage. No Git invocation, fetch, or checkout writes."""
import io,json,stat,zipfile
from pathlib import PurePosixPath
from library_research_support import require,sha,qsha

CONTROLS={'tools/library-research-support.json','tools/library-research-support.sha256'}


def archive_files(raw):
    result={}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for info in z.infolist():
            path=info.filename
            require(path and '\\' not in path and ':' not in path
                and not path.startswith('/') and '..' not in PurePosixPath(path).parts,
                'Unsafe Git source archive member')
            require(stat.S_IFMT(info.external_attr>>16) in {0,stat.S_IFREG,stat.S_IFDIR},
                'Git source archive symlink/special member forbidden')
            if info.is_dir():continue
            require(path not in result,'Duplicate Git source archive member')
            result[path]=z.read(info)
    require(result,'Empty Git source archive forbidden')
    return result


def bind_source_archives(*,producer,prior_archive_raw,candidate_archive_raw,
                         approved_candidate_inventory_sha256,root):
    proof=producer.get('mechanical_proof',{}).get('exact_Git_archive',{})
    require(producer.get('approved') is True and sha(prior_archive_raw)==proof.get('sha256'),
        'Prior GitLF archive is not the actual Root-approved producer archive')
    before=archive_files(prior_archive_raw);after=archive_files(candidate_archive_raw)
    from library_research_activation_controls import is_control
    require(qsha({p:sha(raw) for p,raw in sorted(after.items()) if not is_control(p)})==approved_candidate_inventory_sha256,
        'Candidate complete GitLF source inventory differs from actual Root review')
    root=root.resolve()
    require(not root.is_symlink(),'Research checkout root symlink forbidden')
    for rel,raw in after.items():
        current=root
        for part in PurePosixPath(rel).parts:
            current=current/part;require(not current.is_symlink(),'Research candidate source symlink forbidden')
        require(current.is_file() and current.read_bytes()==raw,
            'Candidate working source is not exact committed GitLF: '+rel)
    # The actual git-archive inventory is complete. Ignored work/site files are
    # not source inputs; a caller cannot omit a tracked unrelated change.
    return before,after
