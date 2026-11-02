"""Require three completed public OSF plans before any new study computation.

This is a fail-closed check, not a registration substitute. The local status
file cannot open the gate by itself. This script does not compute outcomes.
"""
from __future__ import annotations
import datetime as dt
import json
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
STATUS = ROOT / 'registration_status.json'
UA = 'BroadcastwellResearchBot/1.0 (+https://docs.broadcastwell.com/research/)'

def verify_registrations(study_numbers=(1, 2, 3)) -> list[dict]:
    state = json.loads(STATUS.read_text(encoding='utf-8'))
    studies = state['studies']
    if [r['number'] for r in studies] != [1, 2, 3]:
        raise RuntimeError('Three distinct, ordered study records are required.')
    if len({r['record_id'] for r in studies}) != 3:
        raise RuntimeError('Each study requires its own registration.')
    receipts = []
    selected = [row for row in studies if row['number'] in study_numbers]
    if not selected or set(study_numbers) != {row['number'] for row in selected}:
        raise RuntimeError('Unknown study selection.')
    for index, row in enumerate(selected):
        if index:
            time.sleep(1.05)
        rid = row['record_id']
        if not rid.isalnum():
            raise RuntimeError('Unexpected registration identifier.')
        url = f'https://api.osf.io/v2/registrations/{rid}/'
        try:
            with urlopen(Request(url, headers={'User-Agent': UA}), timeout=30) as response:
                raw = response.read()
        except (HTTPError, URLError, TimeoutError) as exc:
            raise RuntimeError(f'Study {row["number"]}: registration not publicly verifiable ({exc}). No analysis permitted.') from exc
        data = json.loads(raw)['data']
        a = data['attributes']
        if data.get('id') != rid or not a.get('public'):
            raise RuntimeError(f'Study {row["number"]}: wrong or non-public record.')
        if a.get('archiving') is not False:
            raise RuntimeError(f'Study {row["number"]}: archiving completion is not confirmed.')
        for key in ('pending_registration_approval', 'withdrawn', 'pending_withdrawal', 'embargoed'):
            if a.get(key):
                raise RuntimeError(f'Study {row["number"]}: registration is {key}.')
        stamp = a.get('date_registered')
        if not stamp:
            raise RuntimeError(f'Study {row["number"]}: no registration timestamp.')
        dt.datetime.fromisoformat(stamp.replace('Z', '+00:00'))
        # Keep an exact primary-source receipt; record immutable protocol content
        # for subsequent checks against the local analysis implementation.
        target = ROOT / 'registration-receipts'
        target.mkdir(exist_ok=True)
        (target / f'{rid}.json').write_bytes(raw)
        receipts.append({'study': row['number'], 'id': rid,
                         'date_registered': stamp, 'title': a.get('title'),
                         'checked_at': dt.datetime.now(dt.timezone.utc).isoformat()})
    return receipts

if __name__ == '__main__':
    try:
        result = verify_registrations()
    except RuntimeError as exc:
        raise SystemExit('REGISTRATION GATE CLOSED: ' + str(exc))
    print(json.dumps({'registration_gate': 'open', 'receipts': result}, indent=2))
