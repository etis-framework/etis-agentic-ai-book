#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Protected operator only: execute every image authorization, never trust submitted PASS files."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone
from authorize_release import COMMIT, timestamp
from evaluate_security_gate import ID, read_json, require

SCOPES = {(role, arch) for role in ('companion', 'dev') for arch in ('amd64', 'arm64')}


def validate_manifest(doc):
    require(set(doc) == {'candidate_commit', 'images'}, 'invalid manifest')
    require(COMMIT.fullmatch(doc['candidate_commit']), 'invalid commit')
    require(isinstance(doc['images'], list) and len(doc['images']) == 4, 'four scopes required')
    seen = set()
    for row in doc['images']:
        require(set(row) == {'role','architecture','image_id'}, 'invalid image entry')
        scope = row['role'], row['architecture']
        require(scope in SCOPES and scope not in seen, 'invalid or duplicate scope')
        require(ID.fullmatch(row['image_id']), 'invalid image ID')
        seen.add(scope)
    require(seen == SCOPES, 'incomplete scopes')
    require(len({row['image_id'] for row in doc['images']}) == 4, 'duplicate image identity')
    return doc


def aggregate(doc, results, now):
    validate_manifest(doc)
    require(len(results) == 4, 'incomplete decisions')
    expected = {(r['role'], r['architecture']): r['image_id'] for r in doc['images']}
    seen, ids, keys = set(), set(), set()
    for r in results:
        scope = r['role'], r['architecture']
        require(scope in expected and scope not in seen, 'unexpected or duplicate decision scope')
        seen.add(scope)
        require(r['candidate_commit'] == doc['candidate_commit'] and r['image_id'] == expected[scope], 'decision identity mismatch')
        require(r['policy'] == 'protected-governed-v1' and r['status'] == 'PASS' and r['hardening_pass'] is True and r['blocking_findings'] == 0 and r['production_certified'] is False, 'image decision failed')
        require(all(f['blocking'] is False and f['severity'] != 'CRITICAL' for f in r['findings']), 'blocking finding')
        require(now < timestamp(r['authorization_expires_at']), 'expired decision')
        require(r['authorization_id'] not in ids, 'reused authorization ID')
        ids.add(r['authorization_id'])
        keys.add((r['reviewer_key_sha256'],r['maintainer_key_sha256']))
    require(seen == SCOPES and len(keys) == 1, 'scope or authority mismatch')
    return {'status':'PASS','scope':'container-security-only','candidate_commit':doc['candidate_commit'], 'production_certified':False,'release_authorized':False,'decisions':results}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('protected_root',type=Path)
    p.add_argument('output',type=Path)
    a=p.parse_args()
    root=a.protected_root.resolve(strict=True)
    here=Path(__file__).resolve().parent
    require(not root.is_relative_to(here.parents[1]), 'protected root outside policy checkout required')
    a.output.mkdir()
    try:
        doc=validate_manifest(read_json(root/'manifest.json'))
        results=[]
        for row in doc['images']:
            role,arch=row['role'],row['architecture']
            scope=f'{role}-{arch}'
            output=a.output/scope
            authority=root/'authority'/scope
            # Each invocation verifies signatures and original evidence anew.
            subprocess.run([sys.executable,'-B',str(here/'authorize_release.py'),str(root/'evidence'/arch),role,arch,row['image_id'],doc['candidate_commit'],'--authority-dir',str(authority),'--output-dir',str(output)],check=True,timeout=120)
            results.append(read_json(output/'governed-decision.json'))
        result=aggregate(doc,results,datetime.now(timezone.utc))
    except (ValueError, KeyError, TypeError, AttributeError, OSError, subprocess.SubprocessError) as exc:
        result={'status':'BLOCKED','error':str(exc),'release_authorized':False,'production_certified':False}
    (a.output/'aggregate-security.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Aggregate container security:',result['status'])
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':
    raise SystemExit(main())
