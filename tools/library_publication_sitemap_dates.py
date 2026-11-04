"""Prior publication lastmod belongs to unchanged, exactly bound records.

Source date_modified is not silently substituted for an already published
sitemap date. Changed/new records require their reviewed actual modification
timestamp. No source, XML, receipt or approval is written here.
"""
import copy,re
from datetime import date,datetime,timezone
from library_publication_overlay import require,sha,canonical
from library_publication_composition import bind_prior_production

POLICY='UNCHANGED_EFFECTIVE_PUBLICATION_LASTMOD_V1'


def _stamp(value):
    require(isinstance(value,str),'Sitemap modification timestamp missing')
    try:stamp=datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError:raise ValueError('Sitemap requires actual reviewed ISO modification timestamp')
    require(stamp.tzinfo is not None,'Sitemap modification timestamp needs timezone')
    stamp=stamp.astimezone(timezone.utc)
    require(stamp<=datetime.now(timezone.utc),'Sitemap modification timestamp is in the future')
    return stamp


def _prior_hub_paths(prior):
    import re
    return {route.removeprefix('/')+'index.md' for route,row in prior['routes'].items()
        if row['kind']=='auxiliary' and re.fullmatch(r'/answers/(?:[a-z0-9-]+/)?',route)}


def _prior_hub_raw_source(previous):
    # Effective full source remains independently hashed and parsed below.
    # Legacy producers used the same bytes for raw and effective hubs.
    raw=previous.get('raw_canonical_source_sha256',previous.get('canonical_source_sha256'))
    require(isinstance(raw,str) and re.fullmatch(r'[0-9a-f]{64}',raw),
        'Prior hub raw source SHA malformed')
    return raw


def _derive_dates(registry,*,prior_xml,prior_payloads,prior_hubs,research_support=None):
    """Pure diagnostic calculation; it does not confer publication authority."""
    from library_publication_consumers import _sitemap_rows,SITE,public_route
    registry.assert_current();overlay=registry.overlay;prior=overlay.prior;q=overlay.q
    old_rows={row['url']:row for row in _sitemap_rows(prior_xml,research_support)}
    require(set(prior_hubs)==_prior_hub_paths(prior),'Prior hub payload/source pins hide or invent a hub')
    active=set(getattr(overlay,'active_revision_paths',[]))
    frozen=getattr(getattr(overlay,'s5_scope',None),'frozen',frozenset())
    dates={};audit={}
    for path,record in {**registry.records,**registry.hubs}.items():
        url=SITE+public_route(path);old=old_rows.get(url)
        source=sha(canonical((overlay.docs/path).read_bytes()).encode())
        if path in registry.records:
            previous=prior_payloads.get(path);row=prior['routes'].get(public_route(path),{})
            if previous:
                require(row.get('kind')=='article' and row.get('effective_canonical_sha256')==sha(previous['effective_full_source'].encode())
                    and row.get('body_sha256')==sha(previous['body'].encode())
                    and row.get('metadata_sha256')==sha(q.canonical_json(previous['meta']).encode()),'Prior article payload differs from trusted compiled state')
            unchanged=bool(previous and path not in active
                and prior['raw_source_pins'].get(path)==source
                and record['effective_canonical_source_sha256']==row['effective_canonical_sha256']
                and record['body']==previous['body'] and record['meta']==previous['meta'])
            require(unchanged or path in active,'Changed/new article lacks the explicit reviewed active revision')
        else:
            previous=prior_hubs.get(path)
            if previous:
                require(sha(previous['effective_full_source'].encode())==previous['canonical_source_sha256'],'Prior hub full source pin differs')
                meta,body=overlay.finite.source_body(previous['effective_full_source'])
                require(meta==previous['meta'] and body==previous['body'],'Prior hub body/metadata differ from full source')
            raw_source=_prior_hub_raw_source(previous) if previous else None
            unchanged=bool(previous and source==raw_source
                and record['body']==previous['body'] and record['meta']==previous['meta'])
        if unchanged:
            require(old is not None,'Unchanged prior record is missing its actual published sitemap row')
            stamp=old['lastmod']
            try:parsed=date.fromisoformat(stamp)
            except (TypeError,ValueError):raise ValueError('Actual prior sitemap lastmod must be an exact calendar date')
            require(parsed<=datetime.now(timezone.utc).date(),'Prior publication lastmod is in the future')
            reason='EXACT_UNCHANGED_PRIOR_PUBLICATION_LASTMOD'
        else:
            require(path not in frozen,'Frozen effective sitemap record changed')
            current=_stamp(record['meta'].get('date_modified'))
            if previous:
                require(current>_stamp(previous['meta'].get('date_modified')),'Changed/active record retains stale source modification timestamp')
            if old:
                require(current.date()>=date.fromisoformat(old['lastmod']),'Changed record would backdate its actual prior publication lastmod')
            stamp=current.date().isoformat();reason='ACTUAL_REVIEWED_CHANGED_OR_NEW_MODIFICATION_DATE'
        dates[url]=stamp;audit[path]={'lastmod':stamp,'policy':reason,'source_date_modified':record['meta']['date_modified']}
    return dates,audit


class BoundPublicationDates:
    def __init__(self):
        raise TypeError('Use bind_publication_dates with an actual approved prior producer')

    def expected(self,registry,prior_xml):
        registry.assert_current()
        require(registry.fingerprint==self._registry and sha(prior_xml)==self._xml,'Publication-lastmod proof belongs to another registry/XML')
        dates,audit=_derive_dates(registry,prior_xml=prior_xml,prior_payloads=self._payloads,prior_hubs=self._hubs,research_support=self._research_support)
        require(dates==self._dates and audit==self._audit,'Publication-lastmod inputs changed after exact binding')
        return copy.deepcopy(dates)

    def audit(self):return copy.deepcopy(self._audit)


def bind_publication_dates(registry,*,prior_xml,prior_payload_bundle,prior_hub_bundle,
    actual_prior_artifacts,producer_receipt,payload_file_sha256,hub_file_sha256,research_support=None):
    overlay=registry.overlay
    require(prior_payload_bundle.get('schema_version')==prior_hub_bundle.get('schema_version')==1,'Publication-lastmod payload schema differs')
    payloads=prior_payload_bundle.get('pages',{});hubs=prior_hub_bundle.get('hubs',{})
    bind_prior_production(prior=overlay.prior,payloads=payloads,actual_artifacts=actual_prior_artifacts,
        actual_binding=overlay.prior['production_binding'],receipt=producer_receipt,q=overlay.q,payload_file_sha256=payload_file_sha256)
    require(producer_receipt.get('hub_payload_bundle_sha256')==hub_file_sha256
        and producer_receipt.get('hub_source_render_equality_passed') is True,'Independent prior hub payload/source/render proof missing or stale')
    raw_proof_fields=('hub_raw_source_git_proof_passed','hub_raw_source_pins','hub_payload_canonical_json_sha256')
    if (any('raw_canonical_source_sha256' in hub for hub in hubs.values())
            or any(field in producer_receipt for field in raw_proof_fields)):
        # The optional raw/effective split is valid only inside the entire
        # independently approved hub bundle and its explicit Git-source proof.
        raw_sources={path:_prior_hub_raw_source(hub) for path,hub in hubs.items()}
        require(producer_receipt.get('hub_raw_source_git_proof_passed') is True
            and producer_receipt.get('hub_raw_source_pins')==raw_sources,
            'Independent prior raw hub Git proof missing or stale')
        bundle=producer_receipt.get('hub_payload_canonical_json_sha256')
        require(isinstance(bundle,str) and re.fullmatch(r'[0-9a-f]{64}',bundle)
            and bundle==sha(overlay.q.canonical_json(prior_hub_bundle).encode()),
            'Prior hub payload object differs from independently approved bundle')
    require(overlay.prior['routes']['/sitemap.xml']['compiled_sha256']==sha(prior_xml)
        and actual_prior_artifacts.get('/sitemap.xml')==prior_xml,'Prior XML differs from actual trusted publication')
    dates,audit=_derive_dates(registry,prior_xml=prior_xml,prior_payloads=payloads,prior_hubs=hubs,research_support=research_support)
    result=object.__new__(BoundPublicationDates)
    result._registry=registry.fingerprint;result._xml=sha(prior_xml)
    result._payloads=copy.deepcopy(payloads);result._hubs=copy.deepcopy(hubs)
    result._dates=dates;result._audit=audit;result._research_support=research_support
    return result
