"""Actual named owner-repair PDF observations and independent Root bindings.

The ordinary cover-date-only Manual validator remains unchanged. This module
does not render/create/edit a PDF, fabricate a visual read, or infer HTTP301.
"""
from __future__ import annotations
import copy,io,json,re
from functools import lru_cache
from library_owner_repair import require,sha,digest,POLICY,PDF_PATHS,MANUAL_PDFS,SAMPLE_PDFS

@lru_cache(maxsize=8)
def _inspect_pdf_serialized(raw):
    from pypdf import PdfReader
    reader=PdfReader(io.BytesIO(raw));require(not reader.is_encrypted,'Encrypted PDF unsupported')
    require(0<len(reader.pages)<=1000,'PDF page count invalid')
    rows=[]
    for i,page in enumerate(reader.pages,1):
        runs=[]
        def visitor(text,cm,tm,font,size):
            if not text.strip():return
            font=font or {};descendants=font.get('/DescendantFonts',[])
            actual=descendants[0].get_object() if descendants else font
            descriptor=actual.get('/FontDescriptor',{})
            if hasattr(descriptor,'get_object'):descriptor=descriptor.get_object()
            weight=descriptor.get('/FontWeight')
            runs.append({'text':text,'font_size':str(size),'font_base_name':str(font.get('/BaseFont','')),
              'actual_descriptor_font_weight':str(weight) if weight is not None else None,
              'font_flags':str(descriptor.get('/Flags','')),
              'text_matrix':[str(x) for x in tm],'current_matrix':[str(x) for x in cm]})
        text=page.extract_text(visitor_text=visitor);require(isinstance(text,str) and text.strip(),'Complete readable PDF text required')
        rows.append({'page':i,'text_sha256':sha(text.encode()),'text':text,
          'actual_font_text_runs':runs,
          'geometry':{'media_box':[str(x) for x in page.mediabox],'crop_box':[str(x) for x in page.cropbox],'rotation':page.rotation}})
    return json.dumps({'sha256':sha(raw),'page_count':len(rows),'pages':rows},sort_keys=True,ensure_ascii=False,separators=(',',':'))


def inspect_pdf(raw):
    # Repeated proof checks reuse only immutable serialized observations.
    # Every caller receives a fresh object; mutation cannot alter the proof.
    return json.loads(_inspect_pdf_serialized(raw))


def exact_path_or_identical_alias(record,path,old_sha256,new_sha256):
    if record.get('path')==path:return True
    aliases=record.get('exact_alias_paths')
    require(isinstance(aliases,list) and len(aliases)==len(set(aliases)) and path in aliases and set(aliases)<=PDF_PATHS,'PDF shared read is not bound to exact allowed aliases')
    require(record.get('before_pdf_sha256')==old_sha256 and record.get('after_pdf_sha256')==new_sha256,'PDF shared alias bytes differ')
    return True


def actual_page_read(row,pdf_sha256,frame_sha256,prior_visual_receipts):
    mode=row.get('read_mode','fresh-actual-view')
    if mode=='fresh-actual-view':require(row.get('actually_viewed') is True,'PDF page was not actually viewed');return
    require(mode=='exact-prior-reading-carry' and row.get('actually_viewed') is False,'Unsupported/false fresh PDF reading claim')
    key=row.get('prior_reading_receipt_sha256');require(key in prior_visual_receipts and sha(prior_visual_receipts[key])==key,'Actual prior PDF reading receipt missing/different')
    carry=json.loads(prior_visual_receipts[key])
    require(carry.get('approved') is True and carry.get('reviewer')=='root' and carry.get('review_kind')=='root-exact-prior-pdf-reading-carry' and carry.get('Root_independently_checked_original_page_read_scope') is True,'Root exact prior page-read adjudication missing')
    original=carry.get('original_read_receipt_sha256');require(original in prior_visual_receipts and sha(prior_visual_receipts[original])==original,'Original actual reading evidence missing/different')
    require(carry.get('pdf_sha256')==pdf_sha256 and carry.get('pages',{}).get(str(row['page']))==frame_sha256,'Prior actual PDF/page raster binding differs')


def rectangle(rect,width,height):
    require(isinstance(rect,list) and len(rect)==4 and all(type(x) is int for x in rect),'PDF visual rectangle malformed')
    l,t,r,b=rect;require(0<=l<r<=width and 0<=t<b<=height,'PDF visual rectangle outside actual image')
    return l,t,r,b


def unchanged_pixels_outside_rectangles(before,after,rectangles,protected_defects):
    from PIL import Image,ImageChops,ImageDraw
    a=Image.open(io.BytesIO(before)).convert('RGBA');b=Image.open(io.BytesIO(after)).convert('RGBA')
    require(a.size==b.size,'Inherited-layout page geometry/raster size changed')
    require(rectangles is not None,'Exact Root-approved changed rectangles required')
    diff=ImageChops.difference(a,b);draw=ImageDraw.Draw(diff)
    for raw in rectangles:
        l,t,r,bot=rectangle(raw,*a.size);require((r-l)*(bot-t)<a.width*a.height,'Whole-page visual exclusion forbidden')
        for defect in protected_defects:
            dl,dt,dr,db=rectangle(defect['rectangle'],*a.size)
            require(r<=dl or dr<=l or bot<=dt or db<=t,'Approved visual edit may not mask an inherited defect')
        draw.rectangle((l,t,r-1,bot-1),fill=(0,0,0,0))
    require(not any(diff.tobytes()),'PDF pixels changed outside the exact approved rectangles')
    return True


def validate_target_style_claim(review,observation,path,source_change_pins):
    claim=review.get('target_text_style_preserved')
    if claim is not True:return {'target_text_style_preserved':False,'style_preservation_PASS_claimed':False}
    required=source_change_pins.get('docs/'+path,{}).get('required_style_target_ids')
    bindings=review.get('actual_font_style_bindings',[])
    require(isinstance(required,list) and required and len(required)==len(set(required)) and {b.get('target_id') for b in bindings}==set(required) and len(bindings)==len(required),'Every Root source-plan style target needs an exact binding')
    for binding in bindings:
        page=binding['page'];found=[]
        for version,key in [('before','before_font_run_sha256'),('after','after_font_run_sha256')]:
            record=observation[version]['pages'][page-1]
            require(record['page']==page,'Style binding page differs')
            matches=[r for r in record['actual_font_text_runs'] if digest(r)==binding[key]]
            require(len(matches)==1,'Exact actual font resource/text run binding missing');found.append(matches[0])
        old,new=found
        require(old['actual_descriptor_font_weight'] is not None and old['actual_descriptor_font_weight']==new['actual_descriptor_font_weight'],'Actual PDF resource font weight changed or is unproved; matching font name/flags is insufficient')
        family=lambda r:re.sub(r'^/?[A-Z]{6}\+','',r['font_base_name'])
        require(family(old)==family(new) and old['font_flags']==new['font_flags'],'Actual font family/flags changed despite preservation claim')
        require(old['font_size']==new['font_size'],'Target font size changed despite preservation claim')
        require(binding['before_text'] in old['text'] and binding['after_text'] in new['text'],'Target text is not in the actual bound font run')
    return {'target_text_style_preservation_claimed':True,'actual_resource_font_weights_checked':True,'font_family_flags_and_size_checked':True,'style_targets_checked':len(bindings),'other_style_rules_require_independent_source_and_visual_evidence':True,'global_style_PASS_granted':False}

def capture_pdf_observation(path,old,new,*,prior_artifact_sha256,before_inputs,after_inputs,actual_ci):
    from library_publication_generated_pdf import validate_ci
    require(path in PDF_PATHS,'Unlisted owner PDF path')
    validate_ci(actual_ci)
    a,b=inspect_pdf(old),inspect_pdf(new)
    return {'schema_version':1,'review_kind':'owner-repair-linux-pdf-observation','approval':'NONE_FACT_CAPTURE_ONLY',
      'path':path,'prior_artifact_sha256':prior_artifact_sha256,'before':a,'after':b,
      'before_consumed_inputs':copy.deepcopy(before_inputs),'after_consumed_inputs':copy.deepcopy(after_inputs),
      'actual_ci':copy.deepcopy(actual_ci),'http_status_observed':None,'http301_verified':False}

def validate_owner_pdf_review(*,path,old,new,review_raw,review_sha256,observation,
    visual_raw,visual_sha256,rendered_frames,before_inputs,after_inputs,
    prior_artifact_sha256,source_change_pins,approved_code_pins,current_ci,
    source_review_raw,source_review_sha256,prior_visual_receipts=None):
    from library_publication_generated_pdf import validate_ci
    require(path in PDF_PATHS and sha(review_raw)==review_sha256 and sha(visual_raw)==visual_sha256,'Named PDF/review bytes differ')
    review=json.loads(review_raw);visual=json.loads(visual_raw)
    require(review.get('approved') is True and review.get('reviewer')=='root' and review.get('review_kind')=='root-owner-repair-pdf' and review.get('policy')==POLICY,'Independent Root exact PDF review missing')
    require(review.get('path')==path and review.get('before_sha256')==sha(old) and review.get('after_sha256')==sha(new),'Root PDF path/old/new pin differs')
    require(review.get('prior_artifact_sha256')==prior_artifact_sha256,'Root PDF before artifact differs')
    require(observation.get('approval')=='NONE_FACT_CAPTURE_ONLY' and observation.get('review_kind')=='owner-repair-linux-pdf-observation','Actual first PDF observation missing')
    require(review.get('observation_sha256')==digest(observation),'Root PDF observation binding differs')
    require(observation.get('path')==path and observation.get('prior_artifact_sha256')==prior_artifact_sha256,'PDF observation path/prior differs')
    require(observation.get('before')==inspect_pdf(old) and observation.get('after')==inspect_pdf(new),'Actual full PDF text/geometry differs from reviewed observation')
    require(observation.get('before_consumed_inputs')==before_inputs and observation.get('after_consumed_inputs')==after_inputs,'PDF consumed inputs changed')
    validate_ci(observation['actual_ci']);validate_ci(current_ci)
    require(current_ci['repository']==observation['actual_ci']['repository'],'Actual PDF rerun repository differs')
    changed={p for p in set(before_inputs)|set(after_inputs) if before_inputs.get(p)!=after_inputs.get(p)}
    allowed={**source_change_pins,**approved_code_pins}
    for p in changed:
        pin=allowed.get(p,{})
        # Consumed-input maps hash physical bytes. Markdown source approval
        # separately retains its canonical and, where different, physical pin.
        before_pin=pin.get('before_sha256')
        if p in source_change_pins and p.endswith('.md'):
            before_pin=source_change_pins[p].get('before_actual_physical_source_sha256',before_pin)
        require(p in allowed and before_pin==before_inputs.get(p) and pin.get('after_sha256')==after_inputs.get(p),'PDF source/generator input changed outside exact Root plan')
    require(review.get('after_consumed_inputs_sha256')==digest(after_inputs) and review.get('before_consumed_inputs_sha256')==digest(before_inputs),'Root PDF input-map digest differs')
    require(review.get('full_text_and_geometry_sha256')==digest({'before':observation['before'],'after':observation['after']}),'Root full PDF proof differs')
    require(sha(source_review_raw)==source_review_sha256==review.get('source_review_receipt_sha256'),'PDF source receipt bytes differ')
    source=json.loads(source_review_raw)
    require(source.get('approved') is True and source.get('review_kind')=='source-exact-owner-repair-pdf-text' and source.get('policy')==POLICY and source.get('before_pdf_sha256')==sha(old) and source.get('after_pdf_sha256')==sha(new),'Actual exact PDF Source peer missing')
    exact_path_or_identical_alias(source,path,sha(old),sha(new))
    require(source.get('full_text_and_geometry_sha256')==review.get('full_text_and_geometry_sha256') and source.get('after_consumed_inputs_sha256')==digest(after_inputs) and source.get('all_original_figures_quotes_dates_preserved_or_exact_source_approved') is True and review.get('all_text_changes_source_reviewed') is True,'PDF exact source-text preservation review differs')
    require(review.get('visual_receipt_sha256')==visual_sha256 and visual.get('approved') is True and visual.get('reviewer')=='root' and visual.get('review_kind')=='actual-owner-repair-full-pdf-visual-read','Actual independent full PDF visual receipt missing')
    require(visual.get('before_pdf_sha256')==sha(old) and visual.get('after_pdf_sha256')==sha(new),'Visual PDF byte binding differs')
    exact_path_or_identical_alias(visual,path,sha(old),sha(new))
    expected={(version,i) for version,record in [('before',observation['before']),('after',observation['after'])] for i in range(1,record['page_count']+1)}
    rows=visual.get('frames',[]);require(len(rows)==len(expected) and {(r.get('version'),r.get('page')) for r in rows}==expected,'Full old/new PDF individual-page visual coverage missing')
    by_key={(r['version'],r['page']):r for r in rows};prior_visual_receipts=prior_visual_receipts or {};inherited=[];all_after_clear=True
    for row in rows:
        key=(row['version'],row['page'])
        require(key in rendered_frames and sha(rendered_frames[key])==row.get('render_sha256'),'Actual PDF raster frame bytes differ')
        actual_page_read(row,sha(old) if row['version']=='before' else sha(new),row['render_sha256'],prior_visual_receipts)
        defects=row.get('preexisting_defects',[]) if row['version']=='before' else []
        if row['version']=='before' and defects:
            require(isinstance(defects,list) and len({d.get('id') for d in defects})==len(defects) and all(isinstance(d.get('id'),str) and d['id'] and isinstance(d.get('description'),str) and d['description'] and isinstance(d.get('rectangle'),list) for d in defects),'Specific original PDF defect inventory missing')
            require(row.get('no_clipping_overlap_missing_glyphs') is False and type(row.get('layout_readable')) is bool,'Original known defects must not be reported as a clean layout')
        elif row['version']=='before':require(row.get('layout_readable') is True and row.get('no_clipping_overlap_missing_glyphs') is True,'Original PDF layout needs an honest defect inventory')
        if row['version']=='after' and not (row.get('layout_readable') is True and row.get('no_clipping_overlap_missing_glyphs') is True):
            all_after_clear=False;original=by_key.get(('before',row['page']),{});known=original.get('preexisting_defects',[])
            require(known and row.get('no_new_layout_defects') is True and row.get('inherited_defect_ids')==[d['id'] for d in known],'After layout has a new/unreviewed defect')
            rectangles=review.get('approved_visual_change_rectangles',{}).get(str(row['page']))
            unchanged_pixels_outside_rectangles(rendered_frames[('before',row['page'])],rendered_frames[key],rectangles,known)
            inherited.append({'page':row['page'],'defect_ids':row['inherited_defect_ids'],'no_new_defect_pixel_proof':True})
    require(visual.get('all_original_figures_quotes_dates_preserved_or_exact_source_approved') is True,'PDF scientific preservation review missing')
    require(review.get('first_linux_artifact_id') and re.fullmatch('[0-9a-f]{64}',str(review.get('first_linux_artifact_sha256'))),'Actual first Linux artifact binding missing')
    style=validate_target_style_claim(review,observation,path,source_change_pins)
    return {'path':path,'before_sha256':sha(old),'after_sha256':sha(new),'actual_Root_visual_review_complete':True,
      'root_review_sha256':review_sha256,'visual_receipt_sha256':visual_sha256,
      'first_ci':observation['actual_ci'],'actual_rerun_ci':copy.deepcopy(current_ci),
      'same_consumed_source_inputs':True,'observed_http_status':None,'http301_verified':False,
      'target_style_review':style,
      'before_layout_defect_inventory':[{'page':r['page'],'defects':r['preexisting_defects']} for r in rows if r['version']=='before' and r.get('preexisting_defects')],
      'all_after_pages_layout_clear':all_after_clear,'explicit_inherited_layout_defects':inherited,
      'global_layout_PASS_inferred_from_preservation':False}
