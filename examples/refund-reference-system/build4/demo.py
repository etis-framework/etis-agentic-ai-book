"""Runnable Build 4 scenarios: lost ack, reconciliation, missing evidence, denial.

Credentials and provider are temporary educational fixtures, not real services.
"""
import argparse
from datetime import datetime,timezone
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'build3'))
from contracts import issue_fixture_grant, CASE,TENANT,AMOUNT
sys.path.insert(0,str(HERE.parent/'build2'))
from identity import LocalAssertionAuthority
from client import request, ServiceUnavailable


def run(scenario: str) -> int:
    with tempfile.TemporaryDirectory(prefix='etis-build4-') as folder:
        d=Path(folder)
        identity_key=os.urandom(32)
        grant_key=os.urandom(32)
        (d/'identity.key').write_bytes(identity_key)
        (d/'grant.key').write_bytes(grant_key)
        now=int(time.time())
        assertion=LocalAssertionAuthority(identity_key).issue(subject='investigator-204',
            tenant_id=TENANT,case_id=CASE,allowed_sources=('EV-204',),
            now=datetime.fromtimestamp(now,timezone.utc))
        grant=issue_fixture_grant(grant_key,now=now)
        body={'action':'execute','case_id':CASE,'tenant_id':TENANT,'amount_cents':AMOUNT,
              'agent_assertion':assertion,'approval_grant':grant if scenario!='denied' else '',
              'lose_ack':scenario=='lost-ack','outage_before_send':scenario=='outage'}
        sock=d/'gate.sock'
        p=subprocess.Popen([sys.executable,str(HERE/'service.py'),
            '--socket',str(sock),'--key',str(d/'grant.key'),
            '--identity-key',str(d/'identity.key'),'--data',str(d/'data'),
            '--ready',str(d/'ready')],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        try:
            for _ in range(300):
                if (d/'ready').exists():break
                if p.poll() is not None:raise RuntimeError('E5 subprocess exited')
                time.sleep(.01)
            else:raise RuntimeError('E5 service startup deadline')
            first=request(sock,body)
            print('execute:',first)
            if scenario in {'lost-ack','outage'}:
                body['action']='reconcile';body['lose_ack']=False;body['outage_before_send']=False
                second=request(sock,body)
                print('reconcile:',second)
                expected='CONFIRMED' if scenario=='lost-ack' else 'UNKNOWN'
                return 0 if first['status']=='UNKNOWN' and second['status']==expected else 2
            expected='DENIED' if scenario=='denied' else 'CONFIRMED'
            return 0 if first['status']==expected else 2
        finally:
            p.terminate()
            try:p.communicate(timeout=3)
            except subprocess.TimeoutExpired:p.kill();p.communicate()


def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument('--scenario',choices=['approved','denied','lost-ack','outage'],required=True)
    return run(p.parse_args().scenario)


if __name__=='__main__':raise SystemExit(main())
