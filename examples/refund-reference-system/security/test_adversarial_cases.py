"""Ch29 compromised bounded investigator against the actual Build 3 E5 subprocess.

Only a local teaching fixture: same-UID process separation is not a credential
security boundary; tests assert local side effects, not external provider truth.
"""
from contextlib import closing
from datetime import datetime, timezone
import os
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'build3'))
sys.path.insert(0, str(ROOT / 'build2'))
from client import request
from contracts import CASE, TENANT, AMOUNT, issue_fixture_grant
from identity import LocalAssertionAuthority


class HijackedInvestigatorAgainstRealE5(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='etis-ch29-attack-')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.finance_secret = os.urandom(32)
        self.e1_secret = os.urandom(32)
        finance_key = self.base / 'finance-key'
        identity_key = self.base / 'identity-key'
        finance_key.write_bytes(self.finance_secret)
        identity_key.write_bytes(self.e1_secret)
        finance_key.chmod(0o600)
        identity_key.chmod(0o600)
        self.e1_token = LocalAssertionAuthority(self.e1_secret).issue(
            subject='investigator_204', tenant_id=TENANT, case_id=CASE,
            allowed_sources=('EV-204',), now=datetime.now(timezone.utc))
        self.socket = self.base / 'service.sock'
        ready = self.base / 'ready'
        self.protected = self.base / 'e5-owned'
        self.proc = subprocess.Popen([
            sys.executable, str(ROOT / 'build3' / 'service.py'),
            '--socket', str(self.socket), '--secret', str(finance_key),
            '--identity-secret', str(identity_key),
            '--data', str(self.protected), '--ready', str(ready),
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.addCleanup(self._stop)
        for _ in range(250):
            if ready.exists():
                break
            if self.proc.poll() is not None:
                self.fail('E5 subprocess exited before readiness')
            time.sleep(0.02)
        else:
            self.fail('E5 readiness timeout')

    def _stop(self):
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()

    def attack(self, **overrides):
        body = dict(action='execute', case_id=CASE, tenant_id=TENANT,
                    amount_cents=AMOUNT, agent_assertion=self.e1_token,
                    approval_grant='', simulate_outage=False)
        body.update(overrides)
        return request(self.socket, body)

    def assert_no_financial_side_effect(self):
        self.assertFalse((self.protected / 'operations.sqlite3').exists(),
                         'DENIED must precede any E7 operation intent')
        self.assertFalse((self.protected / 'provider.sqlite3').exists(),
                         'DENIED must precede any mock E8 effect')

    def test_valid_identity_without_finance_grant_denied_without_effect(self):
        self.assertEqual(self.attack()['status'], 'DENIED')
        self.assert_no_financial_side_effect()

    def test_forged_advisory_fields_denied(self):
        for fake in ({'proposal_id': 'ADV-TRACE-204'},
                     {'advisory_decision': 'approved'},
                     {'approval_grant': 'RF-1042'},
                     {'approval_grant': 'APP-204'}):
            with self.subTest(fake=fake):
                self.assertEqual(self.attack(**fake)['status'], 'DENIED')
                self.assert_no_financial_side_effect()

    def test_valid_token_cannot_be_repurposed_as_finance_grant(self):
        self.assertEqual(self.attack(approval_grant=self.e1_token)['status'], 'DENIED')
        self.assert_no_financial_side_effect()

    def test_mismatched_amount_and_scope_denied(self):
        for mutation in ({'amount_cents': 1}, {'amount_cents': 50_001},
                         {'tenant_id': 'tenant_b'}, {'case_id': 'CASE-205'},
                         {'action': 'admin_dispatch'}):
            with self.subTest(mutation=mutation):
                self.assertEqual(self.attack(**mutation)['status'], 'DENIED')
                self.assert_no_financial_side_effect()

    def test_tampered_finance_grant_denied(self):
        valid = issue_fixture_grant(self.finance_secret, now=int(time.time()))
        self.assertEqual(self.attack(approval_grant=valid[:-1] + ('0' if valid[-1] != '0' else '1'))['status'], 'DENIED')
        self.assert_no_financial_side_effect()

    def test_authorized_positive_control_uses_same_gate(self):
        # An independent test operator, NOT the compromised investigator, creates
        # this fixture grant. This demonstrates a functional gate, not issuer custody.
        grant = issue_fixture_grant(self.finance_secret, now=int(time.time()))
        response = self.attack(approval_grant=grant)
        self.assertEqual(response['status'], 'CONFIRMED')
        self.assertEqual(response['data']['operation_id'], 'RF-1042')
        with closing(sqlite3.connect(self.protected / 'provider.sqlite3')) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM refunds').fetchone()[0], 1)
            self.assertEqual(db.execute('SELECT amount_cents FROM refunds').fetchone()[0], AMOUNT)
        self.assertEqual(self.attack(approval_grant=grant)['status'], 'DENIED')
        with closing(sqlite3.connect(self.protected / 'provider.sqlite3')) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM refunds').fetchone()[0], 1)


if __name__ == '__main__':
    unittest.main()
