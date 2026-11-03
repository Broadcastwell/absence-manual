"""Finite accepted field-test freeze. This grants no experimental activation."""
from pathlib import Path
import json,re,xml.etree.ElementTree as ET
from library_publication_overlay import require,sha,canonical,read_bound_json

ROOT_REGISTRY_SHA256='c346b0f6a7997449f4eccbaf662b53f7ae25ba21a57341f786dc7d673db1798c'

class FieldFreeze:
    def __init__(self,registry_path,registry_sha256,handoff_path,handoff_sha256):
        require(registry_sha256==ROOT_REGISTRY_SHA256,'Field freeze is not the exact reconciled Root registry')
        self.registry_path=Path(registry_path);self.handoff_path=Path(handoff_path)
        self.registry_sha256=registry_sha256;self.handoff_sha256=handoff_sha256
        d=read_bound_json(self.registry_path,registry_sha256)
        require(sha(self.handoff_path.read_bytes())==handoff_sha256==d['handoff_sha256'],'Frozen handoff bytes changed')
        require(d['frozen_sample_count']==45 and len(d['rows'])==45 and len(d['frozen_sitemap_entries'])==45 and len(d['presentation_asset_pins'])==5 and d['activation_authorized'] is False and d['experiment_edits_applied']==0,'Field freeze registry coverage/activation differs')
        self.data=d;self.paths={r['source_path'] for r in d['rows']}
        require(len(self.paths)==45 and all(r['source_frozen'] and r['prose_date_metadata_related_links_navigation_frozen'] for r in d['rows']),'Incomplete field freeze scope')
        self.sitemap={r['url']:r for r in d['frozen_sitemap_entries']}
        require(len(self.sitemap)==45,'Duplicate frozen sitemap entry')
    def assert_current(self):
        require(sha(self.registry_path.read_bytes())==self.registry_sha256 and sha(self.handoff_path.read_bytes())==self.handoff_sha256,'Field freeze input changed during build')
    def check_sources(self,docs):
        self.assert_current()
        for row in self.data['rows']:
            require(sha(canonical((Path(docs)/row['source_path']).read_bytes()).encode())==row['source_sha256']==row['active_canonical_sha256'],'Frozen source/date/metadata/Related changed: '+row['source_path'])
    def reject_active_sample_changes(self,active,merges):
        self.assert_current();require(not self.paths&set(active),'Frozen page appears in active revision plan')
        require(not self.paths&(set(merges)|{r['target_path'] for r in merges.values()}),'Frozen page appears in a merge source or destination')
    def sitemap_dates(self):
        self.assert_current();return {url:ET.fromstring(row['exact_entry']).findtext('lastmod') for url,row in self.sitemap.items()}
    def check_sitemap(self,raw):
        self.assert_current();fragments=re.findall(rb'<url\b[^>]*>.*?</url>',raw,re.S);found={}
        for fragment in fragments:
            e=ET.fromstring(fragment);url=e.findtext('loc')
            if url in self.sitemap:require(url not in found,'Duplicate frozen sitemap URL');found[url]=fragment
        require(set(found)==set(self.sitemap),'Frozen sitemap URL missing')
        for url,row in self.sitemap.items():require(found[url]==row['exact_entry'].encode() and sha(found[url])==row['sha256'],'Frozen exact sitemap entry changed: '+url)
    def check_files(self,files):
        self.assert_current()
        for row in self.data['rows']:
            require(row['served_html_path'] in files and sha(files[row['served_html_path']])==row['served_html_sha256'],'Frozen served HTML/navigation/head changed: '+row['source_path'])
        for row in self.data['presentation_asset_pins']:
            require(row['path'] in files and sha(files[row['path']])==row['sha256'],'Frozen shared presentation asset changed: '+row['path'])
        self.check_sitemap(files['sitemap.xml'])
        import gzip
        require(gzip.decompress(files['sitemap.xml.gz'])==files['sitemap.xml'],'Compressed sitemap differs from the frozen-checked XML')
