"""Capture unapproved candidate facts after fresh PDFs; never certify a release."""
import argparse,json
from pathlib import Path


def observe(*,docs,inputs,inputs_sha256,site,work):
    from library_owner_repair_build import OwnerRepairBuildSession
    session=OwnerRepairBuildSession.load(docs,inputs,inputs_sha256,work)
    try:
        session.site=Path(site).resolve()
        session.capture_candidate_observations()
        return {'approved':False,'observation_only':True,
            'phase':'AFTER_FRESH_PDF_BEFORE_FINAL_CHECKS',
            'owner_inputs_sha256':inputs_sha256,
            'built_site_changed_by_observer':False,
            'Root_artifact_PDF_or_publication_approval':False}
    finally:
        session.archive.close()


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inputs',required=True);p.add_argument('--inputs-sha256',required=True)
    p.add_argument('--docs',required=True);p.add_argument('--site',required=True);p.add_argument('--work',required=True)
    a=p.parse_args()
    print(json.dumps(observe(docs=a.docs,inputs=a.inputs,inputs_sha256=a.inputs_sha256,
        site=a.site,work=a.work),indent=2))
