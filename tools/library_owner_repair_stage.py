"""Stage a Root-reviewed portable owner pack without rewriting input JSON.

The ordinary stage helper expands paths into machine-specific JSON. This
separate finite dispatcher keeps reviewed relative bytes identical on Linux
and Windows; it never promotes an unapproved template or changes manuscripts.
"""
from pathlib import Path
import argparse,json,os,io,zipfile
from library_owner_repair import (POLICY,AUTHORITY_SHA256,HANDOFF_SHA256,REGISTRY_SHA256,
    require,sha,json_unique,safe_path,OwnerRepairPlan,validate_before_read_receipt)
from library_owner_repair_build import bound_file
from library_publication_stage import bridge_accepted_handoff


def checked_target(root,relative):
    safe_path(relative);cursor=root
    for p in [root,*root.parents]:require(not p.is_symlink() and not getattr(p,'is_junction',lambda:False)(),'Stage root has symlink/junction parents')
    for part in Path(relative).parts:
        cursor=cursor/part
        require(not cursor.is_symlink() and not getattr(cursor,'is_junction',lambda:False)(),'Stage target has a symlink/junction component')
    require(cursor.resolve(strict=False).is_relative_to(root.resolve(strict=False)),'Stage target escapes namespace')
    return cursor


def stage(*,blueprint,blueprint_sha256,artifact,out,docs):
    path=Path(blueprint).resolve();raw=path.read_bytes();require(sha(raw)==blueprint_sha256,'Owner stage blueprint bytes differ')
    d=json_unique(raw)
    require(d.get('schema_version')==1 and d.get('policy')==POLICY and d.get('approved') is True and d.get('review_kind')=='root-exact-owner-repair-inputs','Exact Root owner-input approval missing')
    root=path.parent;payloads={}
    require(isinstance(d.get('files'),dict) and d['files'],'Finite approved file manifest required')
    for rel,pin in d['files'].items():
        file,content=bound_file(root,{'path':rel,'sha256':pin})
        require(sha(content)!=AUTHORITY_SHA256,'Raw private authority PDF must never enter repository/CI input pack')
        payloads[rel]=content
    prior=d['prior_artifact'];safe_path(prior['path']);archive=Path(artifact).read_bytes()
    require(sha(archive)==prior['sha256'] and prior['path'] not in payloads,'Actual exact prior artifact binding differs')
    payloads[prior['path']]=archive
    config_ref=d['owner_inputs'];require(config_ref['path'] in payloads and sha(payloads[config_ref['path']])==config_ref['sha256'],'Owner dispatch file missing/different')
    config=json_unique(payloads[config_ref['path']]);require(config.get('policy')==POLICY,'Owner dispatch policy differs')
    config_root=Path(config_ref['path']).parent
    def contents(ref):
        safe_path(ref['path']);rel=(config_root/ref['path']).as_posix();require(rel in payloads and sha(payloads[rel])==ref['sha256'],'Owner dispatch bound file is absent/different');return payloads[rel]
    def references(value):
        if isinstance(value,dict):
            if set(value)=={'path','sha256'}:contents(value)
            else:
                for child in value.values():references(child)
        elif isinstance(value,list):
            for child in value:references(child)
    references(config)
    base_raw=contents(config['base_inputs']);base=json_unique(base_raw)
    require(base.get('published_count')==307,'Owner base must bind exact actual post-small-S5307')
    for name,row in base['files'].items():
        safe_path(row['path']);rel=(config_root/Path(config['base_inputs']['path']).parent/row['path']).as_posix()
        require(rel in payloads and sha(payloads[rel])==row['sha256'],'Portable base input missing/different: '+name)
    for row in base.get('receipt_files',[]):
        safe_path(row['path']);rel=(config_root/Path(config['base_inputs']['path']).parent/row['path']).as_posix();require(rel in payloads and sha(payloads[rel])==row['sha256'],'Portable base peer missing/different')
    plan=json_unique(contents(config['owner_source_plan']))
    require(plan.get('approved') is True and plan.get('kind')==POLICY and plan.get('base_inputs_sha256')==sha(base_raw),'Actual approved portable source plan/base binding missing')
    require(plan.get('baseline_production_binding')==base['actual_prior_production_binding'] and base['actual_prior_production_binding']['artifact_sha256']==sha(archive),'Owner source/base/actual artifact identity differs')
    authority=contents(config['authority_read_receipt']);registry=contents(config['freeze_registry']);handoff=contents(config['freeze_handoff']);navmap=contents(config['freeze_nav_map'])
    require(sha(registry)==REGISTRY_SHA256 and sha(handoff)==HANDOFF_SHA256,'Stage accepted45 authority differs')
    base_root=config_root/Path(config['base_inputs']['path']).parent
    def base_json(name):return json_unique(payloads[(base_root/base['files'][name]['path']).as_posix()])
    leaves=base_json('current_leaf_manifest')['pages'];pins=base_json('current_pins')['pages']
    from library_owner_repair_post_s5 import bind_post_s5
    require('post_s5_context' in config,'Approved post-S5 context required before staging')
    context=contents(config['post_s5_context'])
    post_s5=bind_post_s5(context,config['post_s5_context']['sha256'],producer_raw=payloads[(base_root/base['files']['production_receipt']['path']).as_posix()],prior=base_json('prior_state'),payload=base_json('prior_payload'),leaves=base_json('current_leaf_manifest'),new_merges=base_json('merges'),input_files=base['files'],actual_binding=base['actual_prior_production_binding'])
    bound=OwnerRepairPlan.bind(contents(config['owner_source_plan']),config['owner_source_plan_sha256'],authority_read_receipt=authority,registry_bytes=registry,handoff_bytes=handoff,nav_map_bytes=navmap,actual_prior_binding=base['actual_prior_production_binding'],actual_answer_paths=post_s5.pages,actual_research_paths={p.relative_to(Path(docs)).as_posix() for p in (Path(docs)/'research').rglob('*.md')},bank_ids={p:pins[p]['bank_id'] for p in post_s5.pages},post_s5_binding=post_s5)
    before=contents(config['root_current_before_read_receipt']);require(sha(before)==bound.data.get('root_current_before_read_receipt_sha256'),'Stage Root before-read pin differs')
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:prior_files={n:zipped.read(n) for n in zipped.namelist() if not n.endswith('/')}
    validate_before_read_receipt(before,sha(before),plan=bound,actual_prior_files=prior_files)
    # Copy only after every declared byte and portable reference passed. An
    # existing matching file is not changed; conflicting bytes fail closed.
    target_root=Path(out).absolute()
    targets={rel:checked_target(target_root,rel) for rel in payloads}
    for rel,target in targets.items():
        if target.exists():require(target.is_file() and target.read_bytes()==payloads[rel],'Conflicting existing owner stage file')
    for rel,target in targets.items():
        if not target.exists():
            target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as stream:stream.write(payloads[rel])
    bridge=bridge_accepted_handoff(docs=docs,source=targets[(config_root/Path(config['freeze_handoff']['path'])).as_posix()],handoff_sha256=HANDOFF_SHA256,registry_sha256=REGISTRY_SHA256)
    return {'BW_OWNER_REPAIR_INPUTS':str(targets[config_ref['path']]),'BW_OWNER_REPAIR_INPUTS_SHA256':config_ref['sha256'],'accepted_handoff_bridge':bridge,'manuscripts_modified':0,'ordinary_S5_approval_granted':False}


def main():
    p=argparse.ArgumentParser();p.add_argument('--blueprint',required=True);p.add_argument('--blueprint-sha256',required=True);p.add_argument('--artifact',required=True);p.add_argument('--out',required=True);p.add_argument('--docs',required=True);p.add_argument('--write-github-env',action='store_true');a=p.parse_args()
    result=stage(blueprint=a.blueprint,blueprint_sha256=a.blueprint_sha256,artifact=a.artifact,out=a.out,docs=a.docs)
    if a.write_github_env:
        require(not os.environ.get('BW_LIBRARY_PUBLICATION_INPUTS'),'Owner/ordinary dispatch cannot both be staged')
        with Path(os.environ['GITHUB_ENV']).open('a',encoding='utf-8',newline='\n') as stream:
            for key in ['BW_OWNER_REPAIR_INPUTS','BW_OWNER_REPAIR_INPUTS_SHA256']:stream.write(key+'='+result[key]+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
