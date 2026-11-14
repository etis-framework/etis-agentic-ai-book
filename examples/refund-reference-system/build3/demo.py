"""Credential-free end-to-end teaching demo; local approval key stays in fixture harness.

The demo is not a security sandbox: both subprocesses run as the same OS user.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
import importlib.util
_spec=importlib.util.spec_from_file_location('etis_build2_identity',Path(__file__).resolve().parents[1]/'build2'/'identity.py')
_identity=importlib.util.module_from_spec(_spec)
sys.modules[_spec.name]=_identity
_spec.loader.exec_module(_identity)
LocalAssertionAuthority=_identity.LocalAssertionAuthority

from client import request
from contracts import issue_fixture_grant,CASE,TENANT,AMOUNT


def run(scenario: str) -> dict:
    with tempfile.TemporaryDirectory(prefix='etis-build3-') as name:
        base=Path(name)
        secret=os.urandom(32)
        identity_key=os.urandom(32)
        identity_file=base/'identity_key'
        identity_file.write_bytes(identity_key)
        identity_file.chmod(0o600)
        key=base/'key'
        key.write_bytes(secret)
        key.chmod(0o600)
        socket_path=base/'e5.sock'
        ready=base/'ready'
        command=[sys.executable,str(Path(__file__).with_name('service.py')),
                 '--socket',str(socket_path),'--secret',str(key),
                 '--identity-secret',str(identity_file),
                 '--data',str(base/'protected-state'),'--ready',str(ready)]
        proc=subprocess.Popen(command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            for _ in range(250):
                if ready.exists():break
                if proc.poll() is not None:raise RuntimeError('E5 fixture failed to start')
                time.sleep(.02)
            else:raise RuntimeError('E5 fixture readiness timeout')
            now=int(time.time())
            grant=issue_fixture_grant(secret,now=now) if scenario in {'approved','outage'} else ''
            if scenario=='tampered':grant=issue_fixture_grant(secret,now=now)
            if scenario=='tampered':grant=grant[:-1]+('0' if grant[-1]!='0' else '1')
            body={'action':'execute','case_id':CASE,'tenant_id':TENANT,
                  'amount_cents':AMOUNT,'agent_assertion':LocalAssertionAuthority(identity_key).issue(
                      subject='investigator_204',tenant_id=TENANT,case_id=CASE,
                      allowed_sources=('EV-204',),now=datetime.now(timezone.utc)),
                  'approval_grant':grant,'simulate_outage':scenario=='outage'}
            response=request(socket_path,body)
            operation=base/'protected-state'/'operations.sqlite3'
            provider=base/'protected-state'/'provider.sqlite3'
            response['e7_created']=operation.exists()
            response['mock_e8_created']=provider.exists()
            return response
        finally:
            proc.terminate()
            try:proc.wait(timeout=3)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()


def main() -> int:
    parser=argparse.ArgumentParser(description='ETIS Build 3 protected E5 fixture')
    parser.add_argument('--scenario',choices=('compromised','approved','tampered','outage'),
                        default='compromised')
    args=parser.parse_args()
    try:
        response=run(args.scenario)
    except (RuntimeError,OSError) as exc:
        print(json.dumps({'status':'UNAVAILABLE','error':type(exc).__name__}))
        return 3
    print(json.dumps(response,sort_keys=True))
    return 0 if response['status']=='CONFIRMED' else 2

if __name__=='__main__':sys.exit(main())
