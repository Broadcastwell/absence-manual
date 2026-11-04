"""Exact one-section verified public-video addition; no general embed rule."""
from html.parser import HTMLParser
from library_owner_repair import require,sha,POLICY,json_unique
from library_owner_repair_consumers import json_hash

PATH='answers/chatgpt/which-legal-practice-software-does-chatgpt-recommend.md'
PLAYBACK_SHA256='c88e92665eccc3a07753e0d4b6839725f62ce1c256475537c17b7962c180f818'
WATCH='https://www.youtube.com/watch?v=VzeAMK38r8Q'
EMBED='https://www.youtube.com/embed/VzeAMK38r8Q'
TITLE='Which legal software gets named? Absence Index, September 2026'
STYLE='display:block;width:100%;height:auto;aspect-ratio:16/9;border:0'
EDIT_OLD_SHA256='8f5f4f398eea49900e04bfe9e09f83f685d7e46736973b86c936536136528b76'
EDIT_NEW_SHA256='250ed37c1e9591027170ed81cb02972b38d6c8969254bc7860d25b188747e46e'


def validate_legal_video(*,record,ledger,playback_raw,frames,source_media_raw,source_media_sha256,current_source_peer_sha256):
    require(record['path']==PATH and len(ledger['body_edits'])==1,'Legal video must be the exact single body edit')
    edit=ledger['body_edits'][0]
    require(edit['old']=='## Also asked as' and edit['old_sha256']==EDIT_OLD_SHA256 and edit['new_sha256']==EDIT_NEW_SHA256 and sha(edit['new'].encode())==EDIT_NEW_SHA256,'Legal video section differs from exact reviewed bytes')
    require(record['body'].count(edit['new'])==1,'Exact legal media section missing/repeated in actual body')
    require(sha(playback_raw)==PLAYBACK_SHA256,'Root actual playback verification differs')
    d=json_unique(playback_raw)
    require(d.get('public_watch_url')==WATCH and d.get('title')==TITLE and d.get('channel')=='Broadcastwell' and d.get('anonymous_oembed_HTTP_status')==200 and d.get('actual_frame_progress_verified') is True,'Verified exact public title/playback missing')
    require(len(d.get('native_frames_actually_viewed_by_Root',[]))==2 and set(frames)==set(d['frame_sha256']),'Actual Root playback frame coverage differs')
    for name,value in frames.items():
        actual=sha(value) if isinstance(value,bytes) else value
        require(actual==d['frame_sha256'][name],'Actual Root playback image/hash binding differs')
    class Media(HTMLParser):
        def __init__(self):super().__init__();self.frames=[];self.scripts=[]
        def handle_starttag(self,t,a):
            if t=='iframe':self.frames.append(a)
            if t=='script':self.scripts.append(a)
    p=Media();p.feed(record['body']);p.close()
    expected=[('src',EMBED),('title',TITLE),('loading','lazy'),('style',STYLE),('allowfullscreen',None)]
    require(p.frames==[expected] and not p.scripts and record['body'].count(WATCH)==1,'Legal video has an extra iframe/script/autoplay/attribute or missing exact watch fallback')
    require(sha(source_media_raw)==source_media_sha256,'Source media receipt bytes differ');s=json_unique(source_media_raw)
    require(s.get('approved') is True and s.get('review_kind')=='source' and s.get('scope')=='source-owner-repair-legal-video' and s.get('policy')==POLICY and s.get('path')==PATH,'Exact Source media scope missing')
    require(s.get('current_scoped_Source_receipt_sha256')==current_source_peer_sha256 and s.get('effective_canonical_source_sha256')==sha(record['effective_full_source'].encode()) and s.get('effective_body_sha256')==sha(record['body'].encode()) and s.get('effective_meta_sha256')==json_hash(record['meta']),'Source media full/body/meta/source peer binding differs')
    require(s.get('repair_change_ledger_sha256')==json_hash(ledger) and s.get('Root_playback_receipt_sha256')==PLAYBACK_SHA256 and s.get('all_other_body_bytes_exact') is True and s.get('no_new_measurement_or_S5_approval') is True,'Source exact one-section preservation/playback binding missing')
    return {'verified_exact_public_video':True,'only_one_reviewed_section_added':True,'ordinary_S5_PASS_granted':False,'fresh_Child_visual_read_claim':False}
