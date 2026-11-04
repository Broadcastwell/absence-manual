"""Portable real-runtime tests; no sys.modules substitution or build session."""
import ast,hashlib,json,pathlib,types
R=pathlib.Path(__file__).resolve().parents[1]
PROPOSED=R/'tools'
FIXTURE=pathlib.Path(__file__).parent/'fixtures/owner-content-surface/actual-seven-public-source-cases.json'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def pin(p):return {'path':str(p),'sha256':sha(p.read_bytes())}
def load_comparators():
    import library_owner_repair as p
    import library_owner_repair_consumers as c
    from library_related_chapter_links import source_body
    env={k:getattr(p,k) for k in ['require','sha','SITE','LABELS','spans','validate_primary_labels','validate_navigation_only','validate_pagination_labels']}
    env.update({k:getattr(c,k) for k in ['public_url','validate_render_context','validate_content_surface']})
    env['__file__']=p.__file__
    return env,source_body
def actual_cases(source_body):
    data=json.loads(FIXTURE.read_bytes());cases=[]
    for row in data['cases']:
        c=dict(row);c['before']=c['before'].encode();c['after']=c['after'].encode()
        c['context']=dict(c['context'],rendered_html=c['after'].decode())
        require(sha(c['before'])==row['before_HTML_sha256'] and sha(c['after'])==row['after_HTML_sha256'],'Fixture actual HTML pin differs')
        for version in ['before','after']:
            m,b=source_body(c[version+'_record']['effective_full_source'])
            require(m==c[version+'_record']['meta'] and b==c[version+'_record']['body'],'Fixture full Source boundary differs')
        cases.append(c)
    return cases,pin(FIXTURE)
def final_navigation_loop(env,cases,proofs):
    # Extract only the proposed final caller's actual nav loop. This does not
    # construct an OwnerRepairPlan or run its build/session/final-artifact gate.
    tree=ast.parse(pathlib.Path(env['__file__']).read_text())
    gate=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='validate_artifact_delta')
    loop=next(n for n in gate.body if isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=='page')
    rows=json.loads(FIXTURE.read_bytes())['cases']
    plan={'source_changes':{'docs/'+c['path']:c['source_note'] for c in rows}}
    scope={env['public_url'](c['path'])+'index.html':{'class':'source_content','source_path':'docs/'+c['path']} for c in rows}
    before={env['public_url'](c['path'])+'index.html':c['before'] for c in cases}
    after={env['public_url'](c['path'])+'index.html':c['after'] for c in cases}
    e=dict(env,plan=types.SimpleNamespace(data=plan),scope=scope,nav_universe=set(before),prior=before,candidate=after,content_proofs=proofs)
    exec(compile(ast.Module(body=[loop],type_ignores=[]),'actual-final-navigation-loop','exec'),e)
    return True
