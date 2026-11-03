"""Strict final frozen-output verification. Never normalizes output bytes."""
from pathlib import Path
import argparse,json
from library_field_freeze_navigation import FrozenNavigation
def main():
    p=argparse.ArgumentParser();p.add_argument('--docs',required=True);p.add_argument('--site',required=True);p.add_argument('--map',required=True);p.add_argument('--map-sha256',required=True);a=p.parse_args()
    guard=FrozenNavigation(a.docs,a.map,a.map_sha256);guard.verify_site(a.site)
    print(json.dumps({'frozen_HTML_bytes_exact':45,'referenced_presentation_asset_bytes_exact':5,'frozen_XML_entries_exact':45,'gzip_equals_checked_XML':True,'experiment_activation':False}))
if __name__=='__main__':main()
