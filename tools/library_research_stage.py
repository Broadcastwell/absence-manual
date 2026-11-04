"""Copy only committed Library-reviewed ignored input bytes; no manuscripts."""
from pathlib import Path
import argparse,json,os
from library_research_support import require,sha,optional_support,_file


def stage(root,bundle):
    root=Path(root).absolute();bundle=Path(bundle).absolute();support=optional_support(root)
    require(support is not None and 'release_inputs' in support.plan,'No actual Root-reviewed Research release binding')
    manifest=support.plan['staged_file_sha256'];payloads={};targets={}
    # Every byte and path is checked before creating any file, including
    # matching/conflicting existing targets and all existing parent symlinks.
    for rel,digest in manifest.items():
        raw=_file(bundle,rel).read_bytes();require(sha(raw)==digest,'Research portable input changed')
        target=root/rel;current=root
        for part in Path(rel).parts:
            current=current/part
            require(not current.is_symlink() and not getattr(current,'is_junction',lambda:False)(),
                'Research staged target symlink/junction forbidden')
        require(target.resolve(strict=False).is_relative_to(root.resolve()),'Research staging path escaped')
        if target.exists():require(target.is_file() and target.read_bytes()==raw,'Research staging refuses conflicting target')
        payloads[rel]=raw;targets[rel]=target
    ref=support.plan['release_inputs'];config=json.loads(payloads[ref['path']])
    from library_research_release import POLICY
    require(config.get('schema_version')==1 and config.get('policy')==POLICY
        and config.get('approved') is True and config.get('review_kind')=='library-root-reviewed-finite-research-release',
        'Research staging requires actual Root-approved source plan')
    for row in config['portable_files'].values():
        rel=(Path(ref['path']).parent/row['path']).as_posix()
        require(rel in payloads and sha(payloads[rel])==row['sha256'],'Research portable ref not in committed exact file closure')
    base_ref=config['portable_files']['base_inputs'];base_rel=(Path(ref['path']).parent/base_ref['path']).as_posix()
    base=json.loads(payloads[base_rel]);base_dir=Path(base_rel).parent
    for row in [*base['files'].values(),*base.get('receipt_files',[])]:
        rel=(base_dir/row['path']).as_posix()
        require(rel in payloads and sha(payloads[rel])==row['sha256'],'Library base input/receipt closure is incomplete')
    for rel,raw in payloads.items():
        target=targets[rel]
        if not target.exists():
            target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as stream:stream.write(raw)
        require(target.read_bytes()==raw,'Research stage copied bytes differ')
    # This existing finite bridge copies only the accepted45 authority after
    # the entire committed blueprint/file/receipt closure has passed above.
    from library_publication_stage import bridge_accepted_handoff
    fields={}
    for name in ['field_freeze_handoff','field_freeze_registry']:
        row=base['files'][name];fields[name]=(targets[(base_dir/row['path']).as_posix()],row['sha256'])
    bridge=bridge_accepted_handoff(docs=root/'docs',source=fields['field_freeze_handoff'][0],
        handoff_sha256=fields['field_freeze_handoff'][1],registry_sha256=fields['field_freeze_registry'][1])
    return {'BW_RESEARCH_RELEASE_INPUTS':str(targets[ref['path']]),'BW_RESEARCH_RELEASE_INPUTS_SHA256':ref['sha256'],
        'accepted45_handoff_bridge':bridge,'manuscripts_changed':0}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--bundle',type=Path,required=True);p.add_argument('--write-github-env',action='store_true');a=p.parse_args()
    require(not any(k.startswith(('BW_OWNER_REPAIR_','BW_LIBRARY_PUBLICATION_')) for k in os.environ),'Cannot stage mixed policy modes')
    result=stage(a.repo,a.bundle)
    if a.write_github_env:
        with Path(os.environ['GITHUB_ENV']).open('a',encoding='utf-8',newline='\n') as f:
            for key in ['BW_RESEARCH_RELEASE_INPUTS','BW_RESEARCH_RELEASE_INPUTS_SHA256']:f.write(key+'='+result[key]+'\n')
    print(json.dumps(result,indent=2))
