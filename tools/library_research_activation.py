"""Stage the exact reviewed Research candidate without changing publication mode implicitly."""
from pathlib import Path
import argparse, io, json, os, re, subprocess, zipfile
from library_research_support import PLAN, PIN, MODULE, TEXT_POLICY, require, sha, qsha, _file, optional_support
from library_research_activation_controls import validate_bundle, bundle_file, is_control
from library_research_source_archive import archive_files


def blueprint(root):
    raw = _file(root, PLAN).read_bytes()
    require(_file(root, PIN).read_text(encoding='ascii').strip() == sha(raw),
            'Research activation plan/pin differs')
    plan = json.loads(raw)
    require(plan.get('approved') is True and plan.get('Root_actual_module_and_policy_read') is True,
            'Research activation has no Root module/policy approval')
    validate_bundle(root, plan)
    inputs = json.loads(_file(root, bundle_file(plan['release_inputs']['path'])).read_bytes())
    require(inputs.get('approved') is True and inputs.get('Root_actual_source_review_complete') is True,
            'Research source review is incomplete')
    return plan, inputs


def mode(root):
    present = [(root / p).exists() for p in [MODULE, TEXT_POLICY]]
    if not any(present):
        if any((root / p).exists() for p in [PLAN,PIN]):
            blueprint(root)
            return 'activation'
        return 'owner'
    require(all(present), 'Partial Research activation is forbidden')
    plan, inputs = blueprint(root)
    optional_support(root)
    for path, row in inputs['source_files'].items():
        require(sha(_file(root, path).read_bytes()) == row['after_sha256'],
                'Research mode only accepts the exact reviewed candidate: ' + path)
    return 'research'


def identity_projection(prior, current, candidate, inputs):
    require(set(candidate)==set(inputs['source_files']), 'Identity candidate source scope differs')
    for path,row in inputs['source_files'].items():
        require(current.get(path)==prior.get(path),
                'Activation cannot publish a Research manuscript or data edit: '+path)
        require(sha(candidate[path])==row['after_sha256'], 'Identity candidate bytes changed')
    projected={**current,**candidate}
    require(qsha({p:sha(raw) for p,raw in sorted(projected.items()) if not is_control(p)})
            ==inputs['candidate_source_inventory_sha256'],
            'Activation source differs from the reviewed complete inventory')


def public_identity(root, artifact, source_ref=None):
    """Carry the verified public bytes forward for this code-only activation.

    The parallel Research job builds the complete reviewed candidate on Linux.
    This job does not replay an obsolete Owner repair against different code,
    or claim a new public content build when all public bytes are unchanged.
    """
    plan,inputs=blueprint(root)
    require(mode(root)=='activation', 'Public identity is only for code-only activation')
    require(inputs.get('artifact_review',{}).get('approved') is True,
            'Research candidate artifact review remains pending')
    ref=source_ref or subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    prior_raw=git_archive(root,plan['activation_delivery']['prior_source_commit'])
    artifact_raw=artifact.read_bytes()
    external=plan['activation_delivery']['external_files']
    require(sha(prior_raw)==external['.library-research-work/prior-source.gitLF.zip']
            and sha(artifact_raw)==external['.library-research-work/prior-public.zip'],
            'Identity publication must use the exact approved prior archives')
    current=archive_files(git_archive(root,ref))
    prior=archive_files(prior_raw)
    candidate=archive_files(_file(root,bundle_file('.library-research-work/research60.zip')).read_bytes())
    identity_projection(prior,current,candidate,inputs)
    for path,raw in current.items():
        require(_file(root,path).read_bytes()==raw,'Activation checkout differs from tested Git source')
    public=archive_files(artifact_raw)
    for path,raw in public.items():write_checked(root/'site',path,raw)
    result={'policy':'EXACT_PRIOR_PUBLIC_BYTES_CODE_ONLY_ACTIVATION_V1',
            'actual_tested_source_ref':ref,'prior_content_production_binding':inputs['production_binding'],
            'prior_verified_artifact_sha256':sha(artifact_raw),
            'public_content_changed':False,'research_manuscripts_published':0,
            'files_before_provenance_refresh':{p:sha(raw) for p,raw in sorted(public.items())},
            'linux_Research_candidate_build_required_before_merge':True}
    (root/'activation-public-identity.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result


def git_archive(root, ref):
    require(re.fullmatch('[0-9a-f]{40}', ref) is not None, 'Exact Git commit or tree required')
    return subprocess.check_output(['git', '-c', 'core.autocrlf=false', 'archive',
                                   '--format=zip', ref], cwd=root)


def write_checked(root, rel, data):
    target = root / rel
    require(not Path(rel).is_absolute() and '..' not in Path(rel).parts and ':' not in rel,
            'Research staging path escapes its directory')
    for p in [root, *root.parents, target, *target.parents]:
        require(not p.is_symlink() and not getattr(p, 'is_junction', lambda: False)(),
                'Research staging symlink/junction forbidden')
    if target.exists():
        require(target.is_file() and target.read_bytes() == data, 'Conflicting Research staging file: ' + rel)
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def stage_bundle(root, repository, artifact, candidate_archive):
    plan, inputs = blueprint(root)
    delivery = plan['activation_delivery']
    source = git_archive(repository, delivery['prior_source_commit'])
    public = artifact.read_bytes()
    external = {'.library-research-work/prior-public.zip': public,
                '.library-research-work/prior-source.gitLF.zip': source}
    require({p: sha(b) for p, b in external.items()} == delivery['external_files'],
            'Actual prior artifact/source archive differs from the reviewed bytes')
    bundle = root / '.research-ci-bundle'
    for rel, digest in plan['staged_file_sha256'].items():
        data = external[rel] if rel in external else _file(root, bundle_file(rel)).read_bytes()
        require(sha(data) == digest, 'Research portable input differs: ' + rel)
        write_checked(bundle, rel, data)
    write_checked(root, '.library-research-work/candidate.gitLF.zip', candidate_archive)
    from library_research_stage import stage
    result = stage(root, bundle)
    result['candidate_archive_sha256'] = sha(candidate_archive)
    return result


def prepare(root, artifact, *, candidate_check=False, source_ref=None):
    plan, inputs = blueprint(root)
    ref = source_ref or subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    raw = git_archive(root, ref)
    if not candidate_check:
        require(mode(root) == 'research', 'Research preparation needs the exact committed candidate')
        return root, stage_bundle(root, root, artifact, raw)
    files = archive_files(raw)
    candidate_zip = _file(root, bundle_file('.library-research-work/research60.zip')).read_bytes()
    candidate = archive_files(candidate_zip)
    require(set(candidate) == set(inputs['source_files']), 'Research exercise source scope differs')
    require(all(sha(b) == inputs['source_files'][p]['after_sha256'] for p, b in candidate.items()),
            'Research exercise candidate changed')
    files.update(candidate)
    target = root / '.research-candidate-check'
    require(not target.exists(), 'Preserve an existing candidate exercise; choose a clean checkout')
    target.mkdir()
    for p, data in files.items():
        write_checked(target, p, data)
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_STORED) as z:
        for p, data in sorted(files.items()):
            info = zipfile.ZipInfo(p, (1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    result = stage_bundle(target, root, artifact, stream.getvalue())
    result['unpublished_candidate_exercise'] = True
    return target, result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['mode', 'prepare', 'public-identity'])
    p.add_argument('--repo', type=Path, default=Path('.'))
    p.add_argument('--artifact', type=Path)
    p.add_argument('--candidate-check', action='store_true')
    p.add_argument('--source-ref')
    p.add_argument('--write-github-env', action='store_true')
    a = p.parse_args(); root = a.repo.resolve()
    if a.action == 'mode':
        print(mode(root)); return
    require(a.artifact is not None, 'The verified prior public artifact is required')
    if a.action=='public-identity':
        result=public_identity(root,a.artifact.resolve(),a.source_ref)
        print(json.dumps({k:v for k,v in result.items() if k!='files_before_provenance_refresh'},indent=2));return
    target, result = prepare(root, a.artifact.resolve(), candidate_check=a.candidate_check, source_ref=a.source_ref)
    result['repo'] = str(target)
    if a.write_github_env:
        with Path(os.environ['GITHUB_ENV']).open('a', encoding='utf-8', newline='\n') as f:
            for key in ['BW_RESEARCH_RELEASE_INPUTS', 'BW_RESEARCH_RELEASE_INPUTS_SHA256']:
                f.write(key + '=' + result[key] + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
