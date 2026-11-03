"""Exact two-path generated-Manual-PDF review gate; no renderer or network.

Capture records facts, never approval. Root supplies independently reviewed,
byte-bound receipts after inspecting the actual first Linux-CI artifact.
"""
from __future__ import annotations
import argparse,copy,datetime,io,json,os,platform,re,subprocess,zipfile
from pathlib import Path
import yaml
from library_publication_overlay import require,sha,HEX

PDF_PATHS=frozenset({'absence-manual.pdf','absence-manual-v1.0-2026-08-18.pdf'})
PDF_ROUTES=frozenset('/'+p for p in PDF_PATHS)
TOKEN=object()

def encoded(value):return (json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'))+'\n').encode()

def manual_inputs(repo):
    """Closed, conservative input set for the current pinned build_pdf.py."""
    repo=Path(repo).resolve();docs=repo/'docs'
    order=yaml.safe_load((docs/'.pages').read_text(encoding='utf-8'))['nav']
    paths={repo/'mkdocs.yml',repo/'requirements.txt',repo/'tools/build_pdf.py',docs/'.pages'}
    for entry in order:
        require(isinstance(entry,str),'PDF nav syntax changed; input inventory needs review')
        if entry in {'resources.md','resources','research','answers'}:continue
        if entry=='posts':paths.update((docs/'posts').glob('*.md'))
        else:
            require(entry.endswith('.md') and '/' not in entry and '\\' not in entry,'PDF input-order scope changed')
            paths.add(docs/entry)
    for folder in [docs/'figures',docs/'assets/fonts']:
        paths.update(p for p in folder.rglob('*') if p.is_file())
    require(all(p.is_file() and p.resolve().is_relative_to(repo) for p in paths),'PDF source input missing/escapes repository')
    return {p.relative_to(repo).as_posix():sha(p.read_bytes()) for p in sorted(paths)}

def linux_ci_binding(repo):
    require(platform.system()=='Linux' and os.environ.get('RUNNER_OS')=='Linux' and os.environ.get('GITHUB_ACTIONS')=='true','Fresh PDF review binding requires actual Linux GitHub Actions')
    event=json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text(encoding='utf-8'))
    head=event.get('pull_request',{}).get('head',{}).get('sha')
    require(bool(re.fullmatch(r'[0-9a-f]{40}',str(head))),'Actual PR source head missing')
    def git(arg):return subprocess.check_output(['git','-C',str(repo),'rev-parse',arg],text=True).strip()
    result={'runner_os':'Linux','source_head':head,'checkout_commit':git('HEAD'),'source_tree':git('HEAD^{tree}'),'repository':os.environ.get('GITHUB_REPOSITORY'),'workflow_ref':os.environ.get('GITHUB_WORKFLOW_REF'),'run_id':os.environ.get('GITHUB_RUN_ID'),'run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT')}
    validate_ci(result);return result

def validate_ci(row):
    require(isinstance(row,dict) and row.get('runner_os')=='Linux','PDF candidate is not a Linux-CI observation')
    require(all(re.fullmatch(r'[0-9a-f]{40}',str(row.get(k))) for k in ['source_head','checkout_commit','source_tree']),'PDF CI commit/tree binding missing')
    require(re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',str(row.get('repository'))) and '/.github/workflows/verify.yml@' in str(row.get('workflow_ref')),'PDF CI owning repository/workflow missing')
    require(all(re.fullmatch(r'[1-9][0-9]*',str(row.get(k))) for k in ['run_id','run_attempt']),'PDF CI run/attempt missing')

def inspect_pdf_pair(old,new):
    from pypdf import PdfReader
    a,b=PdfReader(io.BytesIO(old)),PdfReader(io.BytesIO(new))
    require(len(a.pages)==len(b.pages)==116,'Reviewed Manual PDF must retain exactly116pages')
    pages=[];changes=[];cover=None
    for index,(op,np) in enumerate(zip(a.pages,b.pages),1):
        ot,nt=op.extract_text(),np.extract_text()
        require(isinstance(ot,str) and isinstance(nt,str),'Complete PDF text extraction failed')
        geom=lambda p:{'media_box':[str(x) for x in p.mediabox],'crop_box':[str(x) for x in p.cropbox],'rotation':p.rotation}
        require(geom(op)==geom(np),'Manual PDF page geometry changed')
        if ot!=nt:
            changes.append(index);old_dates=re.findall(r'Built (\d{4}-\d{2}-\d{2})',ot);new_dates=re.findall(r'Built (\d{4}-\d{2}-\d{2})',nt)
            require(index==1 and len(old_dates)==len(new_dates)==1 and old_dates!=new_dates,'Unsupported Manual PDF text change')
            before='Built '+old_dates[0];after='Built '+new_dates[0]
            require(ot.count(before)==1 and ot.replace(before,after)==nt,'Only the exact cover build date may change')
            cover={'page':1,'old_literal':before,'new_literal':after}
        pages.append({'page':index,'old_text_sha256':sha(ot.encode()),'new_text_sha256':sha(nt.encode()),'geometry':geom(op)})
    require(changes==[1] and cover is not None,'Generated PDF review requires the explicit single cover-date change')
    return {'page_count':116,'changed_text_pages':changes,'only_explicit_change':cover,'pages':pages}

class ReviewedPdfChanges:
    def __init__(self,rows,root_receipt_sha256,actual_ci,token):
        require(token is TOKEN,'Generated PDF changes need the computed independent review gate')
        self.rows=copy.deepcopy(rows);self.root_receipt_sha256=root_receipt_sha256;self.actual_ci=copy.deepcopy(actual_ci)
        self._seal=sha(encoded([self.rows,self.root_receipt_sha256,self.actual_ci]))
    def assert_bound(self):require(sha(encoded([self.rows,self.root_receipt_sha256,self.actual_ci]))==self._seal,'Reviewed generated PDF proof changed after validation')
    @property
    def routes(self):self.assert_bound();return {'/'+p for p in self.rows}
    def validate_artifacts(self,prior,candidate):
        self.assert_bound()
        require(set(self.rows)==PDF_PATHS,'PDF approval must cover both exact existing mirror paths')
        for p,row in self.rows.items():
            require(p in prior and p in candidate and sha(prior[p])==row['old_sha256'] and sha(candidate[p])==row['new_sha256'],'Exact reviewed PDF bytes changed or existing path missing')
    def validate_states(self,previous,current,changed):
        self.assert_bound()
        expected={r for r in changed if r in PDF_ROUTES}
        require(expected==self.routes,'Generated PDF route change inventory differs from its exact review')
        for p,row in self.rows.items():
            r='/'+p
            require(previous.get(r)=={'kind':'generated_pdf','compiled_sha256':row['old_sha256']} and current.get(r)=={'kind':'generated_pdf','compiled_sha256':row['new_sha256']},'Generated PDF compiled route binding differs')

def validate_reviewed_pdf_changes(*,plan,prior_files,candidate_files,repo,prior_artifact_sha256,prior_production_binding,receipt_loader,current_ci=None):
    changed={p for p in PDF_PATHS if prior_files.get(p)!=candidate_files.get(p)}
    require(all(p in prior_files and p in candidate_files for p in PDF_PATHS),'Both exact existing Manual PDF paths are required')
    if not changed:
        require(plan is None or plan.get('changes')=={},'Stale PDF approval names unchanged output');return None
    require(changed==PDF_PATHS,'Both generated Manual mirrors must change together')
    require(isinstance(plan,dict) and plan.get('schema_version')==1 and set(plan.get('changes',{}))==PDF_PATHS,'Changed generated PDFs require an exact two-existing-path review plan')
    rows=plan['changes'];keys={'old_sha256','new_sha256','root_review_receipt_sha256'}
    require(all(set(r)==keys and all(HEX.fullmatch(str(v)) for v in r.values()) for r in rows.values()),'Unsupported generated PDF review entry')
    require(len({r['old_sha256'] for r in rows.values()})==len({r['new_sha256'] for r in rows.values()})==len({r['root_review_receipt_sha256'] for r in rows.values()})==1,'Manual mirror bytes/root review differ')
    digest=next(iter(rows.values()))['root_review_receipt_sha256'];review=receipt_loader(digest)
    require(review and review.get('approved') is True and review.get('reviewer')=='root' and review.get('review_kind')=='root-reviewed-generated-manual-pdf-change','Independent Root PDF approval missing')
    require(review.get('changes')=={p:{k:v for k,v in r.items() if k!='root_review_receipt_sha256'} for p,r in rows.items()},'Root PDF review does not bind exact old/new files')
    require(review.get('prior_artifact_sha256')==prior_artifact_sha256,'Root PDF review prior production artifact differs')
    actual_inputs=manual_inputs(repo);require(review.get('unchanged_manual_source_and_generator_inputs')==actual_inputs,'Manual source/generator inputs changed since Root PDF review')
    prior_inputs=receipt_loader(review.get('prior_manual_source_inputs_receipt_sha256'))
    require(prior_inputs and prior_inputs.get('approved') is True and prior_inputs.get('reviewer')=='root' and prior_inputs.get('review_kind')=='prior-production-manual-source-inputs' and prior_inputs.get('production_binding')==prior_production_binding and prior_inputs.get('manual_source_and_generator_inputs')==actual_inputs,'Independent actual prior-production Manual input pins differ or are missing')
    require(HEX.fullmatch(str(review.get('first_linux_ci_artifact_sha256'))) and re.fullmatch(r'[1-9][0-9]*',str(review.get('first_linux_ci_artifact_id'))),'Reviewed actual first LinuxCI artifact binding missing')
    first=receipt_loader(review.get('first_linux_ci_candidate_receipt_sha256'))
    require(first and first.get('review_kind')=='fresh-linux-manual-pdf-candidate' and first.get('approval')=='NONE_FACT_CAPTURE_ONLY','Actual first LinuxCI candidate receipt missing')
    validate_ci(first['actual_ci']);require(first['manual_source_and_generator_inputs']==actual_inputs,'First candidate Manual inputs differ')
    require(first['prior_artifact_sha256']==prior_artifact_sha256 and first['pdf_sha256']=={p:r['new_sha256'] for p,r in rows.items()},'Reviewed firstCI candidate does not bind exact PDF bytes')
    actual_ci=linux_ci_binding(repo) if current_ci is None else current_ci;validate_ci(actual_ci)
    require(actual_ci['repository']==first['actual_ci']['repository'],'Rerun PDF repository differs')
    token=ReviewedPdfChanges(rows,digest,actual_ci,TOKEN);token.validate_artifacts(prior_files,candidate_files)
    first_path=sorted(PDF_PATHS)[0];proof=inspect_pdf_pair(prior_files[first_path],candidate_files[first_path])
    require(review.get('text_and_geometry_proof')==proof,'Root116-page exact text/geometry proof differs from actual PDF bytes')
    layout=review.get('layout_proof',{});require(isinstance(layout.get('renderer'),dict) and layout['renderer'] and set(layout.get('pages',{}))=={str(i) for i in range(1,117)},'Root116-page layout proof missing')
    for i in range(1,117):
        row=layout['pages'][str(i)];require(set(row)=={'old_render_sha256','new_render_sha256'} and all(HEX.fullmatch(str(v)) for v in row.values()),'PDF layout page hashes malformed')
        if i>1:require(row['old_render_sha256']==row['new_render_sha256'],'A non-cover page raster changed')
    visual=receipt_loader(review.get('root_changed_page_visual_receipt_sha256'))
    require(visual and visual.get('approved') is True and visual.get('reviewer')=='root' and visual.get('review_kind')=='actual-generated-manual-cover-visual-read','Root actual changed-page visual receipt missing')
    expected={('old',layout['pages']['1']['old_render_sha256']),('new',layout['pages']['1']['new_render_sha256'])}
    frames=visual.get('frames',[])
    require(len(frames)==2 and {(r.get('version'),r.get('sha256')) for r in frames}==expected and all(r.get('actually_viewed') is True and isinstance(r.get('filename'),str) and r['filename'] for r in frames),'Root did not bind actual old/new cover reads')
    require(visual.get('old_pdf_sha256')=={p:r['old_sha256'] for p,r in rows.items()} and visual.get('pdf_sha256')=={p:r['new_sha256'] for p,r in rows.items()} and visual.get('only_expected_cover_build_date_changed') is True,'Root visual PDF binding/scope differs')
    return token

def capture(repo,site,prior_archive,out):
    repo=Path(repo).resolve();site=Path(site).resolve();out=Path(out).resolve();out.mkdir(parents=True,exist_ok=True)
    ci=linux_ci_binding(repo);inputs=manual_inputs(repo);prior_archive=Path(prior_archive)
    with zipfile.ZipFile(prior_archive) as z:prior={p:z.read(p) for p in PDF_PATHS}
    current={p:(site/p).read_bytes() for p in PDF_PATHS}
    saved=out/'candidate-generated-pdfs';saved.mkdir(exist_ok=True)
    for p,raw in current.items():(saved/p).write_bytes(raw)
    record={'schema_version':1,'review_kind':'fresh-linux-manual-pdf-candidate','approval':'NONE_FACT_CAPTURE_ONLY','captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_ci':ci,'manual_source_and_generator_inputs':inputs,'prior_artifact_sha256':sha(prior_archive.read_bytes()),'pdf_sha256':{p:sha(raw) for p,raw in current.items()}}
    try:record['machine_text_and_geometry_proof']=inspect_pdf_pair(prior[sorted(PDF_PATHS)[0]],current[sorted(PDF_PATHS)[0]])
    except (ValueError,KeyError) as e:record['machine_comparison_error']=str(e)
    (out/'fresh-linux-pdf-candidate.json').write_bytes(encoded(record));return record

def main():
    p=argparse.ArgumentParser();p.add_argument('capture',choices=['capture']);p.add_argument('--repo',required=True);p.add_argument('--site',required=True);p.add_argument('--prior-artifact',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    r=capture(a.repo,a.site,a.prior_artifact,a.out);print(json.dumps({'approval':r['approval'],'pdf_sha256':r['pdf_sha256'],'actual_ci':r['actual_ci']},indent=2))
if __name__=='__main__':main()
