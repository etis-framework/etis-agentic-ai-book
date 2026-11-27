#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Protected-host release decision. Never run with candidate-controlled trust inputs."""
import argparse
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

from evaluate_security_gate import evaluate, read_json, require, FIELDS, unique_object

SHA = re.compile(r'[0-9a-f]{64}\Z')
COMMIT = re.compile(r'[0-9a-f]{40}\Z')
ABSENCE_HINTS = {'candidate_service_absent', 'candidate_module_absent_from_default_inc',
                 'candidate_cli_absent_from_standard_location_and_path'}


def timestamp(value):
    require(isinstance(value, str) and value.endswith('Z'), 'expected UTC timestamp')
    return datetime.fromisoformat(value[:-1] + '+00:00')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run_crypto(args):
    return subprocess.run(['openssl', *args], check=True, capture_output=True, timeout=15).stdout


def signed_document(path, reviewer_key, maintainer_key):
    # Read once; verify and parse the same bytes. Keys are supplied by protected operator.
    raw = path.read_bytes()
    require(0 < len(raw) <= 2_000_000, 'authorization document size')
    fingerprints = [digest(run_crypto(['pkey', '-pubin', '-in', str(key), '-outform', 'DER']))
                    for key in (reviewer_key, maintainer_key)]
    require(fingerprints[0] != fingerprints[1], 'reviewer and maintainer keys must differ')
    with tempfile.TemporaryDirectory() as tmp:
        payload = Path(tmp) / 'payload.json'
        payload.write_bytes(raw)
        for key, suffix in ((reviewer_key, '.reviewer.sig'), (maintainer_key, '.maintainer.sig')):
            signature = Path(str(path) + suffix)
            run_crypto(['dgst', '-sha256', '-verify', str(key), '-signature', str(signature), str(payload)])
    return json.loads(raw, object_pairs_hook=unique_object, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x))), fingerprints, digest(raw)


def finding_key(row):
    return tuple(row[k] for k in FIELDS)


def finding_fingerprint(row):
    # Include severity, scanner fix/status, and applicability observation. Full raw report
    # hash below additionally binds every scanner field, not only these selected fields.
    return digest(json.dumps({k: row[k] for k in (*FIELDS, 'severity', 'fixed_version', 'scanner_status', 'applicability_hint')},
                             sort_keys=True, separators=(',', ':')).encode())


def decide(strict, authorization, revoked, commit, scan_time, now):
    require(COMMIT.fullmatch(commit), 'invalid candidate commit')
    require(strict['policy'] == 'strict-no-exceptions' and strict['hardening_pass'] is True, 'strict evidence or hardening failed')
    require(timedelta(0) <= now - scan_time <= timedelta(hours=24), 'scan evidence stale or future-dated')
    require(set(authorization) == {'schema_version','authorization_id','candidate_commit','role','architecture','image_id','evidence_sha256','issued_at','expires_at','decisions'}, 'invalid authorization schema')
    require(type(authorization['schema_version']) is int and authorization['schema_version'] == 1, 'invalid authorization version')
    auth_id = authorization['authorization_id']
    require(isinstance(auth_id, str) and re.fullmatch(r'[A-Za-z0-9_-]{1,100}', auth_id), 'invalid authorization ID')
    require(auth_id not in revoked, 'authorization revoked')
    require(authorization['candidate_commit'] == commit, 'candidate commit mismatch')
    require(all(authorization[k] == strict[k] for k in ('role','architecture','image_id','evidence_sha256')), 'authorization scope/evidence mismatch')
    issued, expires = (timestamp(authorization[k]) for k in ('issued_at','expires_at'))
    require(scan_time <= issued <= now < expires and timedelta(0) < expires-issued <= timedelta(days=30), 'invalid or expired authorization window')
    require(isinstance(authorization['decisions'], list), 'invalid decisions')
    rows = {}
    for row in authorization['decisions']:
        require(set(row) == {'finding_sha256','disposition','rationale','advisory','supported_fix','reviewed_at','review_note_sha256','absence_confirmed'}, 'invalid decision schema')
        fingerprint = row['finding_sha256']
        require(isinstance(fingerprint, str) and SHA.fullmatch(fingerprint) and fingerprint not in rows, 'invalid/duplicate finding authorization')
        require(row['disposition'] in {'not_affected','risk_accepted'}, 'invalid disposition')
        require(isinstance(row['rationale'], str) and len(row['rationale'].strip()) >= 40, 'missing substantive review rationale')
        require(isinstance(row['advisory'], str) and row['advisory'].startswith('https://security-tracker.debian.org/tracker/CVE-'), 'missing distribution advisory')
        require(row['supported_fix'] is False, 'supported fix or unknown fix status blocks')
        require(isinstance(row['review_note_sha256'], str) and SHA.fullmatch(row['review_note_sha256']), 'missing independent review evidence digest')
        require(type(row['absence_confirmed']) is bool and row['absence_confirmed'] == (row['disposition'] == 'not_affected'), 'absence assertion inconsistent with disposition')
        reviewed = timestamp(row['reviewed_at'])
        require(scan_time <= reviewed <= issued and now-reviewed <= timedelta(hours=24), 'upstream review stale or inconsistent')
        rows[fingerprint] = row
    findings = []
    used = set()
    for finding in strict['findings']:
        item = dict(finding)
        fingerprint = finding_fingerprint(finding)
        decision = rows.get(fingerprint)
        item['authorized_disposition'] = None
        if decision:
            require(finding['severity'] == 'HIGH', 'only HIGH findings eligible; critical non-waivable')
            require(finding['assessment'] == 'under_investigation', 'unregistered finding cannot be authorized')
            require(not finding['fixed_version'], 'scanner reports a fix; remediation required')
            require(decision['advisory'].endswith('/' + finding['cve']), 'advisory/CVE mismatch')
            if decision['disposition'] == 'not_affected':
                require(finding['applicability_hint'] in ABSENCE_HINTS, 'no affirmative absence candidate')
            item['authorized_disposition'] = decision['disposition']
            item['authorization_rationale'] = decision['rationale']
            item['review_note_sha256'] = decision['review_note_sha256']
            item['blocking'] = False
            used.add(fingerprint)
        findings.append(item)
    require(used == set(rows), 'unused or changed finding authorization')
    blockers = sum(x['blocking'] for x in findings)
    result = dict(strict, policy='protected-governed-v1', candidate_commit=commit,
                  authorization_id=auth_id, authorization_expires_at=authorization['expires_at'],
                  findings=findings, blocking_findings=blockers,
                  status='PASS' if not blockers else 'BLOCKED', production_certified=False)
    return result


def openvex(result, author, now):
    # Image-wide statement only if every scanner record for that CVE is independently
    # authorized not_affected. Never convert accepted risk into non-applicability.
    by_cve = defaultdict(list)
    for row in result['findings']:
        by_cve[row['cve']].append(row)
    statements = []
    if result['status'] == 'PASS':
        for cve, rows in sorted(by_cve.items()):
            if all(r['authorized_disposition'] == 'not_affected' for r in rows):
                statements.append({'vulnerability': {'name': cve},
                    'products': [{'@id': 'urn:etis:image-config:' + result['image_id']}],
                    'status': 'not_affected', 'justification': 'vulnerable_code_not_present',
                    'impact_statement': ' '.join(sorted({r['authorization_rationale'] for r in rows}))})
    if not statements:
        return None
    return {'@context':'https://openvex.dev/ns/v0.2.0',
            '@id':'urn:etis:authorization:' + result['authorization_id'], 'author':author,
            'timestamp':now.isoformat(), 'version':1, 'statements':statements}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory', type=Path)
    p.add_argument('role', choices=('companion','dev'))
    p.add_argument('architecture', choices=('amd64','arm64'))
    p.add_argument('image_id')
    p.add_argument('candidate_commit')
    p.add_argument('--authority-dir', type=Path, required=True, help='operator-controlled directory outside candidate checkout')
    p.add_argument('--output-dir', type=Path, required=True, help='new operator-controlled output directory')
    a = p.parse_args()
    here = Path(__file__).resolve().parent
    # The directory, trusted checkout, clock, scanner and evidence custody are operator
    # responsibilities. This CLI is NOT an exception switch for candidate CI.
    authority = a.authority_dir.resolve(strict=True)
    require(not authority.is_relative_to(here.parents[1]), 'authority must be outside evaluator checkout')
    a.output_dir.mkdir()
    try:
        auth, fingerprints, auth_hash = signed_document(authority/'authorization.json', authority/'reviewer.pem', authority/'maintainer.pem')
        revocations = read_json(authority/'revocations.json')
        require(set(revocations) == {'schema_version','revoked_authorization_ids'} and revocations['schema_version'] == 1
                and isinstance(revocations['revoked_authorization_ids'], list)
                and all(isinstance(x,str) and x for x in revocations['revoked_authorization_ids']), 'invalid revocation register')
        for row in auth['decisions']:
            note_hash = row['review_note_sha256']
            require(isinstance(note_hash,str) and SHA.fullmatch(note_hash), 'invalid review note digest')
            note = (authority/'review-notes'/ (note_hash + '.txt')).read_bytes()
            require(bool(note.strip()) and digest(note) == note_hash, 'missing or changed independent review note')
        strict = evaluate(a.directory, a.role, a.architecture, a.image_id, here/'vulnerability-assessments.json', here/'risk-acceptances.json')
        scan_time = datetime.fromisoformat(strict['scan_created_at'].replace('Z','+00:00'))
        require(scan_time.utcoffset() is not None, 'scan time must include offset')
        now = datetime.now(timezone.utc)
        result = decide(strict, auth, set(revocations['revoked_authorization_ids']), a.candidate_commit, scan_time, now)
        result.update(authorization_sha256=auth_hash, reviewer_key_sha256=fingerprints[0], maintainer_key_sha256=fingerprints[1])
        vex = openvex(result, 'ETIS independently reviewed authorization ' + fingerprints[0], now)
        if vex:
            (a.output_dir/'vex.UNVALIDATED.json').write_text(json.dumps(vex, indent=2)+'\n')
    except (ValueError, KeyError, TypeError, AttributeError, IndexError, OSError, subprocess.SubprocessError) as exc:
        result = {'status':'ERROR','error':str(exc),'production_certified':False}
    (a.output_dir/'governed-decision.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print('Protected release decision:', result['status'])
    return {'PASS':0,'BLOCKED':1,'ERROR':2}[result['status']]


if __name__ == '__main__':
    raise SystemExit(main())
