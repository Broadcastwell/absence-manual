"""Stage only reviewed input files and an exact previously verified artifact."""
from pathlib import Path
import argparse,hashlib,json,os

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
ACCEPTED_HANDOFF_SHA256='3f09732e9a23c36ea0852fa6dcec96c0c1c9f0c1cb55d2f4af722072ac17eb1b'
ACCEPTED_REGISTRY_SHA256='c346b0f6a7997449f4eccbaf662b53f7ae25ba21a57341f786dc7d673db1798c'


def _bridge_target(docs):
    value=Path(docs)
    if '..' in value.parts:raise ValueError('Handoff bridge docs path contains parent traversal')
    docs=value.absolute()
    if not docs.is_dir() or len(docs.parents)<3:raise ValueError('Handoff bridge docs directory invalid')
    base=docs.parents[2];target=base/'LIVE/FIELD_TEST_TO_LIBRARY.md'
    for location in {docs,*docs.parents,target,*target.parents}:
        if location.is_symlink() or getattr(location,'is_junction',lambda:False)():
            raise ValueError('Handoff bridge rejects existing symlink/junction parents or target')
    if target.resolve(strict=False)!=target or not target.resolve(strict=False).is_relative_to(base.resolve(strict=True)):
        raise ValueError('Handoff bridge target escapes the required workspace namespace')
    return target


def bridge_accepted_handoff(*,docs,source,handoff_sha256,registry_sha256):
    # Caller main invokes this only AFTER approved-blueprint/all-file/receipt
    # pins verify. It copies authority bytes; it never creates an approval.
    if handoff_sha256!=ACCEPTED_HANDOFF_SHA256 or registry_sha256!=ACCEPTED_REGISTRY_SHA256:
        raise ValueError('Handoff bridge is restricted to the current accepted45 authority hashes')
    source=Path(source);raw=source.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=ACCEPTED_HANDOFF_SHA256:raise ValueError('Accepted handoff source bytes changed')
    target=_bridge_target(docs)
    if target.exists():
        if not target.is_file() or target.read_bytes()!=raw:raise ValueError('Conflicting existing accepted handoff; no overwrite permitted')
        return {'status':'EXISTING_MATCHING_UNTOUCHED','path':str(target),'sha256':handoff_sha256}
    target.parent.mkdir(parents=True,exist_ok=True)
    if _bridge_target(docs)!=target:raise ValueError('Handoff bridge namespace changed')
    # Exclusive creation also refuses a target installed after the check.
    with target.open('xb') as stream:stream.write(raw)
    if target.read_bytes()!=raw:raise ValueError('Created accepted handoff differs from pinned bytes')
    return {'status':'EXACT_ACCEPTED_BYTES_COPIED','path':str(target),'sha256':handoff_sha256}


def main():
    p=argparse.ArgumentParser();p.add_argument('--blueprint',required=True);p.add_argument('--artifact',required=True);p.add_argument('--out',required=True);p.add_argument('--write-github-env',action='store_true');p.add_argument('--docs',type=Path);a=p.parse_args()
    blueprint=Path(a.blueprint).resolve();data=json.loads(blueprint.read_text(encoding='utf-8'))
    if data.get('schema_version')!=1 or data.get('approved') is not True:raise SystemExit('Prepared input blueprint is not reviewed')
    archive=Path(a.artifact).resolve()
    if digest(archive)!=data['prior_artifact_sha256']:raise SystemExit('Downloaded prior artifact does not match the independent binding')
    result=data['inputs'];files={}
    for name,row in result['files'].items():
        path=archive if name=='prior_artifact' else (blueprint.parent/row['path']).resolve()
        if digest(path)!=row['sha256']:raise SystemExit('Reviewed input bytes changed: '+name)
        files[name]={'path':str(path),'sha256':row['sha256']}
    result['files']=files
    for row in result.get('receipt_files',[]):
        path=(blueprint.parent/row['path']).resolve()
        if digest(path)!=row['sha256']:raise SystemExit('Formal review receipt changed')
        row['path']=str(path)
    if not {'field_freeze_handoff','field_freeze_registry'}<=set(files):raise SystemExit('Accepted45 authority inputs missing')
    bridge_accepted_handoff(docs=a.docs or blueprint.parent.parent/'docs',
        source=files['field_freeze_handoff']['path'],handoff_sha256=files['field_freeze_handoff']['sha256'],
        registry_sha256=files['field_freeze_registry']['sha256'])
    out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);target=out/'inputs.json'
    target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    values={'BW_LIBRARY_PUBLICATION_INPUTS':str(target),'BW_LIBRARY_PUBLICATION_INPUTS_SHA256':digest(target)}
    if a.write_github_env:
        env=Path(os.environ['GITHUB_ENV'])
        with env.open('a',encoding='utf-8',newline='\n') as f:
            for name,value in values.items():f.write(name+'='+value+'\n')
    print(json.dumps(values,indent=2))
if __name__=='__main__':main()
