"""Synthetic stage/Source declarations; existing Root playback facts only."""
from pathlib import Path
import copy,io,json,sys,tempfile,unittest
from unittest.mock import patch
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE/'tools'))
import library_owner_repair as p
import library_owner_repair_stage as stage
import library_owner_repair_legal_video as video
from library_owner_repair_consumers import json_hash
from library_owner_repair_pdf import exact_path_or_identical_alias,unchanged_pixels_outside_rectangles,actual_page_read,validate_target_style_claim
from test_owner_repair_policy import edit


class StageTests(unittest.TestCase):
 def test_unapproved_unknown_policy_or_wrong_blueprint_hash_fail_before_staging(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);file=root/'blueprint.json';d={'schema_version':1,'policy':p.POLICY,'approved':False,'review_kind':'root-exact-owner-repair-inputs'}
   for override,pin in [({},None),({'approved':True,'policy':'OTHER'},None),({'approved':True},'0'*64)]:
    file.write_bytes(p.encoded({**d,**override}));out=root/'stage'
    with self.assertRaises(p.RepairError):stage.stage(blueprint=file,blueprint_sha256=pin or p.sha(file.read_bytes()),artifact=root/'absent.zip',out=out,docs=root/'repo/docs')
    self.assertFalse(out.exists())
 def test_missing_nested_dispatch_file_fails_before_output_or_handoff(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);archive=root/'prior.zip';archive.write_bytes(b'fixture archive');cfg={'policy':p.POLICY,'base_inputs':{'path':'missing.json','sha256':'0'*64}};(root/'inputs.json').write_bytes(p.encoded(cfg))
   d={'schema_version':1,'policy':p.POLICY,'approved':True,'review_kind':'root-exact-owner-repair-inputs','files':{'inputs.json':p.sha(p.encoded(cfg))},'prior_artifact':{'path':'prior.zip','sha256':p.sha(archive.read_bytes())},'owner_inputs':{'path':'inputs.json','sha256':p.sha(p.encoded(cfg))}};file=root/'blueprint.json';file.write_bytes(p.encoded(d))
   with self.assertRaises(p.RepairError):stage.stage(blueprint=file,blueprint_sha256=p.sha(file.read_bytes()),artifact=archive,out=root/'stage',docs=root/'repo/docs')
   self.assertFalse((root/'stage').exists());self.assertFalse((root/'LIVE').exists())
 def test_private_authority_upload_guard_with_synthetic_preimage(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);secret=b'PRIVATE BRIEF FIXTURE, never actual brief';(root/'disguised.bin').write_bytes(secret)
   d={'schema_version':1,'policy':p.POLICY,'approved':True,'review_kind':'root-exact-owner-repair-inputs','files':{'disguised.bin':p.sha(secret)}};file=root/'blueprint.json';file.write_bytes(p.encoded(d))
   with patch.object(stage,'AUTHORITY_SHA256',p.sha(secret)),self.assertRaisesRegex(p.RepairError,'private authority'):stage.stage(blueprint=file,blueprint_sha256=p.sha(file.read_bytes()),artifact=root/'none.zip',out=root/'stage',docs=root/'repo/docs')
   self.assertFalse((root/'stage').exists())
 def test_stage_target_must_remain_inside_exact_namespace(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);self.assertEqual(root/'safe/file.json',stage.checked_target(root,'safe/file.json'))
   for path in ['../outside','C:/outside','/outside']:
    with self.assertRaises(p.RepairError):stage.checked_target(root,path)


class MediaTests(unittest.TestCase):
 def fixture(self):
  section='## Watch the legal-software summary\n\n<iframe src="'+video.EMBED+'" title="'+video.TITLE+'" loading="lazy" style="'+video.STYLE+'" allowfullscreen></iframe>\n\n[Watch “'+video.TITLE+'” on YouTube]('+video.WATCH+').\n\n## Also asked as'
  e=edit('## Also asked as',section);ledger={'body_edits':[e]};body='# Existing question\n\nOriginal observation.\n\n'+section
  record={'path':video.PATH,'body':body,'effective_full_source':body,'meta':{}}
  playback=(HERE/'tests/fixtures/owner-repair/legal-public-playback-root-verified.json').read_bytes();d=json.loads(playback)
  source={'approved':True,'review_kind':'source','scope':'source-owner-repair-legal-video','policy':p.POLICY,'path':video.PATH,'current_scoped_Source_receipt_sha256':'a'*64,'effective_canonical_source_sha256':p.sha(body.encode()),'effective_body_sha256':p.sha(body.encode()),'effective_meta_sha256':json_hash({}),'repair_change_ledger_sha256':json_hash(ledger),'Root_playback_receipt_sha256':video.PLAYBACK_SHA256,'all_other_body_bytes_exact':True,'no_new_measurement_or_S5_approval':True};raw=p.encoded(source)
  return dict(record=record,ledger=ledger,playback_raw=playback,frames=d['frame_sha256'],source_media_raw=raw,source_media_sha256=p.sha(raw),current_source_peer_sha256='a'*64)
 def test_exact_one_verified_video_section_keeps_s5_fail_separate(self):
  result=video.validate_legal_video(**self.fixture());self.assertTrue(result['verified_exact_public_video']);self.assertFalse(result['ordinary_S5_PASS_granted']);self.assertFalse(result['fresh_Child_visual_read_claim'])
 def test_wrong_leaf_frame_playback_or_source_binding_rejects(self):
  for mode in ['leaf','frame','playback','source']:
   k=self.fixture()
   if mode=='leaf':k['record']['path']='answers/chatgpt/another.md'
   elif mode=='frame':k['frames'][next(iter(k['frames']))]='0'*64
   elif mode=='playback':k['playback_raw']+=b'changed'
   else:k['current_source_peer_sha256']='0'*64
   with self.subTest(mode=mode),self.assertRaises(p.RepairError):video.validate_legal_video(**k)
 def test_autoplay_extra_iframe_external_script_or_changed_style_rejects(self):
  for text in ['<script>run()</script>','<iframe src="https://other.example"></iframe>']:
   k=self.fixture();k['record']['body']+=text
   with self.assertRaises(p.RepairError):video.validate_legal_video(**k)
  k=self.fixture();k['record']['body']=k['record']['body'].replace('loading="lazy"','loading="eager" autoplay')
  with self.assertRaises(p.RepairError):video.validate_legal_video(**k)


class PdfCarryTests(unittest.TestCase):
 def test_alias_read_requires_same_pdf_bytes_and_exact_named_paths(self):
  d={'exact_alias_paths':['assets/samples/Kalvenor_Sample_Category_Audit.pdf','assets/samples/Category_Audit_sample_Kalvenor_fictional.pdf'],'before_pdf_sha256':'a'*64,'after_pdf_sha256':'b'*64}
  self.assertTrue(exact_path_or_identical_alias(d,d['exact_alias_paths'][1],'a'*64,'b'*64))
  for path,old,new in [('another.pdf','a'*64,'b'*64),(d['exact_alias_paths'][1],'c'*64,'b'*64)]:
   with self.assertRaises(p.RepairError):exact_path_or_identical_alias(d,path,old,new)
 def test_prior_actual_read_carry_requires_original_receipt_and_exact_raster(self):
  original=b'Original read fixture bytes';orig=p.sha(original);carry={'approved':True,'reviewer':'root','review_kind':'root-exact-prior-pdf-reading-carry','Root_independently_checked_original_page_read_scope':True,'original_read_receipt_sha256':orig,'pdf_sha256':'a'*64,'pages':{'1':'b'*64}};raw=p.encoded(carry);key=p.sha(raw);row={'read_mode':'exact-prior-reading-carry','actually_viewed':False,'prior_reading_receipt_sha256':key,'page':1}
  actual_page_read(row,'a'*64,'b'*64,{key:raw,orig:original})
  for store,raster in [({key:raw},'b'*64),({key:raw,orig:original},'c'*64)]:
   with self.assertRaises(p.RepairError):actual_page_read(row,'a'*64,raster,store)
 def test_pixel_proof_rejects_masking_original_defect_or_unlisted_changes(self):
  from PIL import Image,ImageDraw
  def png(img):buf=io.BytesIO();img.save(buf,format='PNG');return buf.getvalue()
  a=Image.new('RGB',(40,40),'white');b=a.copy();ImageDraw.Draw(b).rectangle((0,0,39,3),fill='black')
  old,new=png(a),png(b);defects=[{'id':'old-overlap','rectangle':[10,20,30,30]}]
  self.assertTrue(unchanged_pixels_outside_rectangles(old,new,[[0,0,40,4]],defects))
  for rects in [[[0,0,40,40]],[[0,0,40,30]],[]]:
   with self.assertRaises(p.RepairError):unchanged_pixels_outside_rectangles(old,new,rects,defects)
 def test_same_font_name_flags_do_not_hide_actual_bold_to_regular_loss(self):
  path='assets/samples/Kalvenor_Sample_Category_Audit.pdf';old={'text':'What moves','font_size':'11','font_base_name':'Inter-Regular','font_flags':'4','actual_descriptor_font_weight':'600'}
  new={**old,'actual_descriptor_font_weight':'400'}
  def check(after):
   obs={'before':{'pages':[{'page':1,'actual_font_text_runs':[old]}]},'after':{'pages':[{'page':1,'actual_font_text_runs':[after]}]}}
   review={'target_text_style_preserved':True,'actual_font_style_bindings':[{'target_id':'protected-bold-prefix','page':1,'before_font_run_sha256':p.digest(old),'after_font_run_sha256':p.digest(after),'before_text':'What moves','after_text':'What moves'}]}
   return validate_target_style_claim(review,obs,path,{'docs/'+path:{'required_style_target_ids':['protected-bold-prefix']}})
  self.assertTrue(check(old)['actual_resource_font_weights_checked'])
  with self.assertRaisesRegex(p.RepairError,'font weight'):check(new)
  with self.assertRaises(p.RepairError):check({**old,'actual_descriptor_font_weight':None})


if __name__=='__main__':unittest.main()
