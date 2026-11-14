"""Build 5 demonstration: E2 lease/fencing with the genuine Build 4 E5 subprocess.

The demo/test harness alone issues ephemeral local fixture assertions and grants.
The E2 coordinator and runner cannot mint finance grants or access provider data.
"""
import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'build3'))
from contracts import AMOUNT, CASE, TENANT, issue_fixture_grant
from client import request, ServiceUnavailable
sys.path.insert(0,str(HERE.parent/'build2'))
from identity import LocalAssertionAuthority
from coordinator import DurableCoordinator
from runner import BoundedRunner, RunnerUnavailable


def run(scenario: str) -> int:
    """Exercise original E5 gate; no financial authorization in E2."""
    with tempfile.TemporaryDirectory(prefix='etis-build5-') as folder:
        directory=Path(folder)
        identity_secret=os.urandom(32)
        finance_secret=os.urandom(32)
        (directory/'identity.key').write_bytes(identity_secret)
        (directory/'finance.key').write_bytes(finance_secret)
        issued=int(time.time())
        assertion=LocalAssertionAuthority(identity_secret).issue(
            subject='investigator-204',tenant_id=TENANT,case_id=CASE,
            allowed_sources=('EV-204',),now=datetime.fromtimestamp(issued,timezone.utc))
        grant=issue_fixture_grant(finance_secret,now=issued)
        sock=directory/'e5.sock'
        server=subprocess.Popen([sys.executable,str(HERE.parent/'build4'/'service.py'),
            '--socket',str(sock),'--key',str(directory/'finance.key'),
            '--identity-key',str(directory/'identity.key'),'--data',str(directory/'payment'),
            '--ready',str(directory/'ready')],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        try:
            for _ in range(300):
                if (directory/'ready').exists():
                    break
                if server.poll() is not None:
                    raise RuntimeError('E5 exited before ready')
                time.sleep(0.01)
            else:
                raise RuntimeError('E5 readiness timed out')
            coordinator=DurableCoordinator(directory/'e2.sqlite3',lease_seconds=5)
            coordinator.initialize()
            lease=coordinator.acquire('worker-a',now=issued)
            def e5_request(action: str) -> dict:
                body={'action':action,'case_id':CASE,'tenant_id':TENANT,
                      'amount_cents':AMOUNT,'agent_assertion':assertion,
                      'approval_grant':grant if scenario!='denied' else '',
                      'lose_ack':scenario=='lost-ack' and action=='execute',
                      'outage_before_send':scenario=='outage' and action=='execute'}
                try:
                    return request(sock,body)
                except ServiceUnavailable as exc:
                    raise RunnerUnavailable('E5 transport ambiguous; no retry') from exc
            runner=BoundedRunner(coordinator,e5_request)
            first=runner.step(lease,now=issued)
            print('first:',first,coordinator.state())
            if scenario in ('lost-ack','outage'):
                # Deterministic recovery simulation: old lease expires. New E2
                # epoch must NOT replay execute; it may only request status.
                recovered=coordinator.acquire('worker-b',now=issued+6)
                second=runner.step(recovered,now=issued+6)
                print('takeover:',second,coordinator.state())
                expected='CONFIRMED' if scenario=='lost-ack' else 'NEEDS_RECONCILIATION'
                return 0 if first=='NEEDS_RECONCILIATION' and second==expected else 2
            expected='DENIED' if scenario=='denied' else 'CONFIRMED'
            return 0 if first==expected else 2
        finally:
            server.terminate()
            try:
                server.communicate(timeout=3)
            except subprocess.TimeoutExpired:
                server.kill()
                server.communicate()


def main() -> int:
    parser=argparse.ArgumentParser(description='ETIS Build 5 bounded E2 coordinator')
    parser.add_argument('--scenario',required=True,choices=('approved','denied','lost-ack','outage'))
    return run(parser.parse_args().scenario)

if __name__=='__main__':
    raise SystemExit(main())
