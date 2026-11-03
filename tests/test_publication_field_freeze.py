"""Synthetic finite45 freeze checks; no actual sample compilation."""
import copy,gzip,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE/'tools'))
import library_publication_field_freeze as f
from library_publication_overlay import sha,OverlayError

class FreezeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.docs=self.root/'docs';self.docs.mkdir();self.handoff=self.root/'handoff.md';self.handoff.write_bytes(b'Synthetic freeze, no activation.');rows=[];entries=[];self.files={}
        for i in range(45):
            p='answers/measurement/fixture-'+str(i)+'.md';s=self.docs/p;s.parent.mkdir(parents=True,exist_ok=True);s.write_bytes(('# Fixture '+str(i)+'\n').encode());html=p[:-3]+'/index.html';self.files[html]=('<article>Fixture '+str(i)+'</article>').encode();url='https://docs.broadcastwell.com/'+p[:-3]+'/';entry='<url><loc>'+url+'</loc><lastmod>2026-11-02</lastmod></url>'
            rows.append({'source_path':p,'source_sha256':sha(s.read_bytes()),'active_canonical_sha256':sha(s.read_bytes()),'served_html_path':html,'served_html_sha256':sha(self.files[html]),'source_frozen':True,'prose_date_metadata_related_links_navigation_frozen':True});entries.append({'url':url,'exact_entry':entry,'sha256':sha(entry.encode())})
        assets=[]
        for i in range(5):p='assets/fixture-'+str(i)+'.css';self.files[p]=b'exact fixture CSS';assets.append({'path':p,'sha256':sha(self.files[p])})
        xml=('<urlset>'+''.join(r['exact_entry'] for r in entries)+'</urlset>').encode();self.files['sitemap.xml']=xml;self.files['sitemap.xml.gz']=gzip.compress(xml,mtime=0)
        self.registry=self.root/'registry.json';self.registry.write_bytes(json.dumps({'fixture_only':True,'handoff_sha256':sha(self.handoff.read_bytes()),'frozen_sample_count':45,'rows':rows,'frozen_sitemap_entries':entries,'presentation_asset_pins':assets,'activation_authorized':False,'experiment_edits_applied':0}).encode());digest=sha(self.registry.read_bytes());self.pin=patch.object(f,'ROOT_REGISTRY_SHA256',digest);self.pin.start();self.addCleanup(self.pin.stop);self.guard=f.FieldFreeze(self.registry,digest,self.handoff,sha(self.handoff.read_bytes()))
    def test_all45_sources_served_HTML_assets_and_exact_entries_pass_identity(self):
        self.guard.check_sources(self.docs);self.guard.check_files(self.files);self.assertEqual(45,len(self.guard.sitemap_dates()))
    def test_source_date_metadata_or_navigation_head_change_is_rejected(self):
        rel=next(iter(self.guard.paths));original=(self.docs/rel).read_bytes();(self.docs/rel).write_bytes(original+b'date_modified: changed\n')
        with self.assertRaisesRegex(OverlayError,'Frozen source/date/metadata') :self.guard.check_sources(self.docs)
        (self.docs/rel).write_bytes(original);changed=copy.deepcopy(self.files);changed[rel[:-3]+'/index.html']+=b'<nav>new label</nav>'
        with self.assertRaisesRegex(OverlayError,'HTML/navigation/head'):self.guard.check_files(changed)
    def test_shared_asset_or_exact_sitemap_date_change_is_rejected(self):
        changed=copy.deepcopy(self.files);changed['assets/fixture-0.css']+=b'changed'
        with self.assertRaisesRegex(OverlayError,'shared presentation'):self.guard.check_files(changed)
        changed=copy.deepcopy(self.files);changed['sitemap.xml']=changed['sitemap.xml'].replace(b'2026-11-02',b'2026-11-03',1)
        with self.assertRaisesRegex(OverlayError,'exact sitemap entry'):self.guard.check_files(changed)
    def test_sample_revision_merge_or_midbuild_handoff_change_is_rejected(self):
        path=next(iter(self.guard.paths))
        with self.assertRaisesRegex(OverlayError,'active revision'):self.guard.reject_active_sample_changes({path:{}},{})
        with self.assertRaisesRegex(OverlayError,'merge source or destination'):self.guard.reject_active_sample_changes({}, {'answers/measurement/other.md':{'target_path':path}})
        self.handoff.write_bytes(b'Synthetic changed handoff')
        with self.assertRaisesRegex(OverlayError,'changed during build'):self.guard.assert_current()

if __name__=='__main__':unittest.main()
