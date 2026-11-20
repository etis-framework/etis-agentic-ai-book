from contextlib import closing
"""Build 3 contract and hostile-client tests; no real keys or payment provider."""
import json
import socket
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from datetime import datetime,timezone
import importlib.util
_spec=importlib.util.spec_from_file_location('etis_build2_identity',Path(__file__).resolve().parents[1]/'build2'/'identity.py')
_identity=importlib.util.module_from_spec(_spec)
sys.modules[_spec.name]=_identity
_spec.loader.exec_module(_identity)
LocalAssertionAuthority=_identity.LocalAssertionAuthority
import unittest

from client import request,ServiceUnavailable
from contracts import (issue_fixture_grant,verify_grant,AuthorizationDenied,
                       CASE,TENANT,AMOUNT)
from demo import run

class IsolatedGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='etis-gate-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.secret=os.urandom(32)
        key=self.root/'key';key.write_bytes(self.secret);key.chmod(0o600)
        self.identity_key=os.urandom(32)
        identity_file=self.root/'identity-key'
        identity_file.write_bytes(self.identity_key);identity_file.chmod(0o600)
        self.agent_token=LocalAssertionAuthority(self.identity_key).issue(
            subject='investigator_204',tenant_id=TENANT,case_id=CASE,
            allowed_sources=('EV-204',),now=datetime.now(timezone.utc))
        self.assertEqual(LocalAssertionAuthority(self.identity_key).verify(
            self.agent_token,now=datetime.now(timezone.utc)).case_id,CASE)
        self.sock=self.root/'socket';ready=self.root/'ready'
        self.proc=subprocess.Popen([sys.executable,str(Path(__file__).with_name('service.py')),
            '--socket',str(self.sock),'--secret',str(key),'--identity-secret',str(identity_file),
            '--data',str(self.root/'protected'),'--ready',str(ready)],
            stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        self.addCleanup(self._stop)
        for _ in range(250):
            if ready.exists():break
            if self.proc.poll() is not None:self.fail('E5 service exited')
            time.sleep(.02)
        else:self.fail('service readiness timeout')

    def _stop(self):
        self.proc.terminate()
        try:self.proc.wait(timeout=3)
        except subprocess.TimeoutExpired:self.proc.kill();self.proc.wait()

    def body(self,grant='',**changes):
        b={'action':'execute','case_id':CASE,'tenant_id':TENANT,'amount_cents':AMOUNT,
           'agent_assertion':self.agent_token,'approval_grant':grant,'simulate_outage':False}
        b.update(changes)
        return b

    def assert_no_effect(self):
        self.assertFalse((self.root/'protected'/'operations.sqlite3').exists())
        self.assertFalse((self.root/'protected'/'provider.sqlite3').exists())

    def grant(self,**changes):return issue_fixture_grant(self.secret,now=int(time.time()),**changes)

    def test_valid_agent_token_is_not_payment_approval(self):
        # An authenticated investigator is still not a finance approver.
        self.assertEqual(request(self.sock,self.body())['status'],'DENIED')
        self.assert_no_effect()

    def test_advisory_forgery_cannot_mint_operation(self):
        for extra in ({'approval_grant':'RF-1042'}, {'proposal_id':'ADV-TRACE-204'},
                      {'approval_grant':'APP-204'}):
            with self.subTest(extra=extra):
                self.assertEqual(request(self.sock,self.body(**extra))['status'],'DENIED')
                self.assert_no_effect()

    def test_denial_wrong_amount_tenant_case_bool_and_extra_fields(self):
        for change in ({'amount_cents':True},{'amount_cents':49_999},
                       {'tenant_id':'other_tenant'},{'case_id':'OTHER-204'},
                       {'action':'approve'},{'simulate_outage':1},{'role':'finance'}):
            with self.subTest(change=change):
                self.assertEqual(request(self.sock,self.body(**change))['status'],'DENIED')
                self.assert_no_effect()

    def test_tampered_wrong_scope_and_expired_grants(self):
        for grant in (self.grant()[:-1]+'x',self.grant(amount_cents=1),
                      self.grant(approver='agent_204'),
                      issue_fixture_grant(self.secret,now=int(time.time())-70)):
            with self.subTest(grant=grant[:12]):
                self.assertEqual(request(self.sock,self.body(grant))['status'],'DENIED')
                self.assert_no_effect()

    def test_authorized_one_effect_and_replay_refused(self):
        grant=self.grant()
        good=request(self.sock,self.body(grant))
        self.assertEqual(good['status'],'CONFIRMED')
        self.assertEqual(good['data']['operation_id'],'RF-1042')
        from pathlib import Path
        import sqlite3
        provider=self.root/'protected'/'provider.sqlite3'
        with closing(sqlite3.connect(provider)) as db, db:
            self.assertEqual(db.execute('select count(*) from refunds').fetchone()[0],1)
        self.assertEqual(request(self.sock,self.body(grant))['status'],'DENIED')
        with closing(sqlite3.connect(provider)) as db, db:
            self.assertEqual(db.execute('select count(*) from refunds').fetchone()[0],1)

    def test_outage_durable_unresolved_no_blind_retry(self):
        import sqlite3
        grant=self.grant()
        self.assertEqual(request(self.sock,self.body(grant,simulate_outage=True))['status'],'UNKNOWN')
        with closing(sqlite3.connect(self.root/'protected'/'operations.sqlite3')) as db, db:
            self.assertEqual(db.execute('select status from operations').fetchone()[0],'DISPATCHED')
        self.assertEqual(request(self.sock,self.body(grant))['status'],'UNKNOWN')
        with closing(sqlite3.connect(self.root/'protected'/'provider.sqlite3')) as db, db:
            self.assertEqual(db.execute('select count(*) from refunds').fetchone()[0],0)

    def test_concurrent_duplicate_requests_only_one_confirmed(self):
        import concurrent.futures
        grant=self.grant()
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            result=list(pool.map(lambda _:request(self.sock,self.body(grant))['status'],range(6)))
        self.assertEqual(result.count('CONFIRMED'),1)
        self.assertEqual(result.count('DENIED'),5)

    def test_conflicting_mock_provider_record_after_e7_claim_is_unknown(self):
        import sqlite3
        provider=self.root/'protected'/'provider.sqlite3'
        provider.parent.mkdir(parents=True,exist_ok=True)
        with closing(sqlite3.connect(provider)) as db, db:
            db.execute('CREATE TABLE refunds(operation_id TEXT PRIMARY KEY,case_id TEXT NOT NULL UNIQUE,amount_cents INTEGER NOT NULL,status TEXT NOT NULL)')
            db.execute('INSERT INTO refunds VALUES(?,?,?,?)',('RF-1042','CASE-204',1,'CONFIRMED'))
        outcome=request(self.sock,self.body(self.grant()))
        self.assertEqual(outcome['status'],'UNKNOWN')
        with closing(sqlite3.connect(self.root/'protected'/'operations.sqlite3')) as db, db:
            self.assertEqual(db.execute('SELECT status FROM operations').fetchone()[0],'DISPATCHED')
        self.assertEqual(request(self.sock,self.body(self.grant()))['status'],'UNKNOWN')
        with closing(sqlite3.connect(provider)) as db, db:
            self.assertEqual(db.execute('SELECT amount_cents FROM refunds').fetchone()[0],1)

    def test_service_unavailable_is_not_failed_payment(self):
        self._stop()
        with self.assertRaises(ServiceUnavailable):request(self.sock,self.body())

    def test_grant_is_not_a_valid_agent_assertion(self):
        # Distinct audience/purpose: E5 grant is not Build2 E1 fixture token.
        self.assertRaises(AuthorizationDenied,verify_grant,self.agent_token,self.secret,now=int(time.time()))

    def test_forged_or_missing_identity_rejected_even_with_grant(self):
        grant=self.grant()
        for assertion in ('FORGED', '', self.agent_token[:-1]+'x'):
            with self.subTest(assertion=assertion[:12]):
                self.assertEqual(request(self.sock,self.body(grant,agent_assertion=assertion))['status'],'DENIED')
                self.assert_no_effect()

    def test_non_json_request_refused(self):
        import socket
        with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
            s.connect(str(self.sock));s.sendall(b'{not-json}\n')
            self.assertEqual(json.loads(s.recv(4096))['status'],'DENIED')

    def test_aborted_client_does_not_terminate_service(self):
        """An E3 peer may drop its reply; E5 must survive that transport fault."""
        # Complete, validly framed *unauthorized* request, then forbid reads.
        # The shutdown ensures a server response encounters a closed peer.
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as peer:
            peer.connect(str(self.sock))
            payload = json.dumps(self.body(), sort_keys=True).encode() + b'\n'
            peer.sendall(payload)
            peer.shutdown(socket.SHUT_RDWR)
        # Check subsequent useful service, not only process liveness.
        self.assertEqual(request(self.sock, self.body())['status'], 'DENIED')
        self.assertIsNone(self.proc.poll())
        self.assert_no_effect()

    def test_post_effect_reply_lost_does_not_redispatch(self):
        """Lost reply after a granted effect cannot create another RF-1042."""
        import sqlite3
        grant = self.grant()
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as peer:
            peer.connect(str(self.sock))
            peer.sendall(json.dumps(self.body(grant), sort_keys=True).encode() + b'\n')
            peer.shutdown(socket.SHUT_RDWR)
        provider = self.root / 'protected' / 'provider.sqlite3'
        for _ in range(80):
            if provider.exists():
                break
            time.sleep(0.025)
        self.assertTrue(provider.exists(), 'approved operation was never dispatched')
        self.assertEqual(request(self.sock, self.body(grant))['status'], 'DENIED')
        self.assertIsNone(self.proc.poll())
        with closing(sqlite3.connect(provider)) as db, db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM refunds').fetchone()[0], 1)

    def test_incomplete_frame_expires_and_next_request_is_served(self):
        """A partial E3 frame must not monopolize the sequential E5 worker."""
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as peer:
            peer.settimeout(2)
            peer.connect(str(self.sock))
            peer.sendall(b'{')
            started = time.monotonic()
            outcome = request(self.sock, self.body())
            self.assertLess(time.monotonic() - started, 2.5)
            self.assertEqual(outcome['status'], 'DENIED')
        self.assertIsNone(self.proc.poll())
        self.assert_no_effect()

    def test_slow_trickle_does_not_extend_absolute_frame_deadline(self):
        """A malicious caller cannot reset the timeout with each byte."""
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as peer:
            peer.connect(str(self.sock))
            peer.sendall(b'{')
            for _ in range(3):
                time.sleep(0.22)
                try:
                    peer.sendall(b' ')
                except (BrokenPipeError, ConnectionResetError):
                    break
            self.assertEqual(request(self.sock, self.body())['status'], 'DENIED')
        self.assertIsNone(self.proc.poll())
        self.assert_no_effect()

    def test_oversized_frame_rejected_and_service_recovers(self):
        """Server framing limit is checked before parsing or authorization."""
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as peer:
            peer.settimeout(2)
            peer.connect(str(self.sock))
            peer.sendall(b'X' * 8200 + b'\n')
            try:
                response = peer.recv(4096)
                if response:
                    self.assertEqual(json.loads(response)['status'], 'DENIED')
            except (ConnectionResetError, BrokenPipeError):
                pass
        self.assertEqual(request(self.sock, self.body())['status'], 'DENIED')
        self.assert_no_effect()

    def test_demo_path(self):
        self.assertEqual(run('compromised')['status'],'DENIED')
        self.assertEqual(run('approved')['status'],'CONFIRMED')
        self.assertEqual(run('outage')['status'],'UNKNOWN')

if __name__=='__main__':unittest.main()
