"""Build 4 adversarial and failure-driven tests; no external services or money.

Exercise provider effects and local observations independently. The service
fixture is exercised across an actual OS process to retain the E5 boundary.
"""
from contextlib import closing
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'build3'))
from contracts import issue_fixture_grant
sys.path.insert(0,str(HERE.parent/'build2'))
from identity import LocalAssertionAuthority
from provider_contracts import (AMOUNT_CENTS, Capabilities, ContractViolation, Outcome,
                                ProviderConflict, RefundCommand)
from adapter import SQLiteFixtureProvider
from ledger import InvalidTransition, OperationalLedger
from workflow import OutcomeUnknown, RefundWorkflow


class Build4Test(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='etis-b4-test-')
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.command=RefundCommand()
        self.ledger=OperationalLedger(self.root/'operations.sqlite3')
        self.provider=SQLiteFixtureProvider(self.root/'provider.sqlite3')
        self.workflow=RefundWorkflow(self.ledger,self.provider)

    def test_authorized_single_effect(self):
        self.assertEqual(self.workflow.execute(self.command),'CONFIRMED')
        self.assertEqual(self.ledger.state(self.command)[4],'CONFIRMED')
        self.assertEqual(self.provider.lookup(self.command).outcome,Outcome.CONFIRMED)

    def test_concurrent_dispatchers_one_effect(self):
        def attempt(_):
            try:
                return self.workflow.execute(self.command)
            except InvalidTransition:
                return 'DENIED'
        with ThreadPoolExecutor(max_workers=6) as pool:
            results=list(pool.map(attempt,range(6)))
        self.assertEqual(results.count('CONFIRMED'),1)
        self.assertEqual(results.count('DENIED'),5)
        with closing(sqlite3.connect(self.provider.database)) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM provider_refunds').fetchone()[0],1)

    def test_replayed_execute_does_not_call_provider_twice(self):
        self.workflow.execute(self.command)
        with self.assertRaises(InvalidTransition):self.workflow.execute(self.command)
        with closing(sqlite3.connect(self.provider.database)) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM provider_refunds').fetchone()[0],1)

    def test_lost_ack_requires_authoritative_reconciliation(self):
        # Ambiguous send result requires provider inquiry, never a second effect.
        with self.assertRaises(OutcomeUnknown):self.workflow.execute(self.command,lose_ack=True)
        self.assertEqual(self.ledger.state(self.command)[4],'UNKNOWN')
        self.assertEqual(self.workflow.reconcile(self.command),'CONFIRMED')
        self.assertEqual(self.ledger.state(self.command)[5],'provider-status-query')
        with self.assertRaises(InvalidTransition):self.workflow.execute(self.command)

    def test_outage_missing_record_stays_unknown(self):
        with self.assertRaises(OutcomeUnknown):self.workflow.execute(self.command,outage_before_send=True)
        with self.assertRaises(OutcomeUnknown):self.workflow.reconcile(self.command)
        self.assertEqual(self.ledger.state(self.command)[4],'UNKNOWN')
        self.assertEqual(self.provider.lookup(self.command).outcome,Outcome.NOT_FOUND)

    def test_reconcile_does_not_create_ledger_or_provider(self):
        with self.assertRaises(InvalidTransition):self.workflow.reconcile(self.command)
        self.assertFalse(self.provider.database.exists())

    def test_conflicting_stable_operation_key_blocks_dispatch(self):
        with self.provider._connect() as db:
            db.execute('INSERT INTO provider_refunds VALUES (?,?,?,?,?,?,?,?)',
                ('RF-1042','CASE-204','retailer_a',1,'USD','MOCK-RF-1042','CONFIRMED',
                 'etis-fixture-provider-v1'))
            db.commit()
        with self.assertRaises(OutcomeUnknown):self.workflow.execute(self.command)
        self.assertEqual(self.ledger.state(self.command)[4],'UNKNOWN')
        with self.assertRaises(OutcomeUnknown):self.workflow.reconcile(self.command)
        with closing(sqlite3.connect(self.provider.database)) as db:
            self.assertEqual(db.execute('SELECT amount_cents FROM provider_refunds').fetchone()[0],1)

    def test_provider_conflict_revokes_earlier_local_confirmation(self):
        self.workflow.execute(self.command)
        with closing(sqlite3.connect(self.provider.database)) as db:
            db.execute('UPDATE provider_refunds SET amount_cents=1 WHERE operation_id=?',('RF-1042',))
            db.commit()
        with self.assertRaises(OutcomeUnknown):self.workflow.reconcile(self.command)
        self.assertEqual(self.ledger.state(self.command)[4],'UNKNOWN')

    def test_reconciliation_conflict_preserves_prior_confirmation_history(self):
        self.assertEqual(self.workflow.execute(self.command),'CONFIRMED')
        before=self.ledger.history(self.command)
        self.assertEqual([row[0] for row in before],
                         ['PREPARE','DISPATCH_CLAIM','CONFIRM'])
        self.assertEqual(before[-1][2:4],('provider-commit','MOCK-RF-1042'))
        with closing(sqlite3.connect(self.provider.database)) as db:
            db.execute('UPDATE provider_refunds SET amount_cents=1 WHERE operation_id=?',
                       ('RF-1042',))
            db.commit()
        with self.assertRaises(OutcomeUnknown):
            self.workflow.reconcile(self.command)
        self.assertEqual(self.ledger.state(self.command)[4],'UNKNOWN')
        after=self.ledger.history(self.command)
        self.assertEqual(after[:len(before)],before)
        self.assertEqual(after[-1],('OBSERVE_UNKNOWN','UNKNOWN',
                                    'provider-conflict','MOCK-RF-1042'))

    def test_lost_ack_and_reconciliation_preserve_all_local_transitions(self):
        with self.assertRaises(OutcomeUnknown):
            self.workflow.execute(self.command,lose_ack=True)
        self.assertEqual(self.workflow.reconcile(self.command),'CONFIRMED')
        history=self.ledger.history(self.command)
        self.assertEqual([h[0] for h in history],
                         ['PREPARE','DISPATCH_CLAIM','OBSERVE_UNKNOWN','CONFIRM'])
        self.assertEqual(history[-1][2],'provider-status-query')
        with closing(sqlite3.connect(self.provider.database)) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM provider_refunds').fetchone()[0],1)

    def test_idempotency_scope_must_be_documented(self):
        with self.assertRaises(ContractViolation):
            RefundWorkflow(self.ledger,self.provider,capabilities=Capabilities(stable_key_scope='unknown'))

    def test_missing_lookup_capability_is_not_silently_accepted(self):
        with self.assertRaises(ContractViolation):
            RefundWorkflow(self.ledger,self.provider,capabilities=Capabilities(supports_lookup=False))

    def test_inadequate_retention_contract_rejected(self):
        with self.assertRaises(ContractViolation):
            RefundWorkflow(self.ledger,self.provider,capabilities=Capabilities(retention_seconds=1))

    def test_boolean_money_not_valid(self):
        with self.assertRaises(ContractViolation):RefundCommand(amount_cents=True).validate()

    def test_wrong_case_and_currency_rejected(self):
        for cmd in (RefundCommand(case_id='CASE-OTHER'),RefundCommand(currency='EUR')):
            with self.subTest(cmd=cmd),self.assertRaises(ContractViolation):cmd.validate()

    def test_nonconfirmed_provider_evidence_cannot_confirm(self):
        self.ledger.prepare(self.command);self.ledger.claim_dispatch(self.command)
        with self.assertRaises(ContractViolation):
            self.ledger.confirm(self.command,'forged',source='provider-status-query')

    def test_provider_is_isolated_sqlite_database(self):
        self.workflow.execute(self.command)
        self.assertNotEqual(self.ledger.database,self.provider.database)
        with closing(sqlite3.connect(self.ledger.database)) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM operations').fetchone()[0],1)
        with closing(sqlite3.connect(self.provider.database)) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM provider_refunds').fetchone()[0],1)


class ProcessBoundaryTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix="etis-b4-process-")
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.identity_key=os.urandom(32)
        self.grant_key=os.urandom(32)
        (self.root/'identity.key').write_bytes(self.identity_key)
        (self.root/'grant.key').write_bytes(self.grant_key)
        now=int(time.time())
        self.token=LocalAssertionAuthority(self.identity_key).issue(subject='investigator-204',
            tenant_id='retailer_a',case_id='CASE-204',allowed_sources=('EV-204',),
            now=datetime.fromtimestamp(now,timezone.utc))
        self.grant=issue_fixture_grant(self.grant_key,now=now)
        self.sock=self.root/'server.sock'
        self.proc=subprocess.Popen([sys.executable,str(HERE/'service.py'),
            '--socket',str(self.sock),'--key',str(self.root/'grant.key'),
            '--identity-key',str(self.root/'identity.key'),
            '--data',str(self.root/'data'),'--ready',str(self.root/'ready')],
            stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        self.addCleanup(self.stop_service)
        for _ in range(200):
            if (self.root/'ready').exists():break
            if self.proc.poll() is not None:self.fail('service exited before ready')
            time.sleep(.01)
        else:self.fail('service never ready')

    def stop_service(self):
        if self.proc.poll() is None:self.proc.terminate()
        try:self.proc.communicate(timeout=3)
        except subprocess.TimeoutExpired:self.proc.kill();self.proc.communicate()

    def body(self,**changes):
        x={'action':'execute','case_id':'CASE-204','tenant_id':'retailer_a',
           'amount_cents':50_000,'agent_assertion':self.token,
           'approval_grant':self.grant,'lose_ack':False,'outage_before_send':False}
        x.update(changes);return x

    def call(self,body):
        # Reuse the Build 3 transport so no untrusted adapter import is needed.
        from client import request
        return request(self.sock,body)

    def test_valid_token_without_approval_cannot_create_provider_or_ledger(self):
        response=self.call(self.body(approval_grant='APP-204'))
        self.assertEqual(response['status'],'DENIED')
        self.assertFalse((self.root/'data'/'operations.sqlite3').exists())
        self.assertFalse((self.root/'data'/'provider.sqlite3').exists())

    def test_signed_approval_happy_path_and_replay(self):
        self.assertEqual(self.call(self.body())['status'],'CONFIRMED')
        self.assertEqual(self.call(self.body())['status'],'DENIED')

    def test_lost_ack_reconcile_via_service_no_second_send(self):
        self.assertEqual(self.call(self.body(lose_ack=True))['status'],'UNKNOWN')
        self.assertEqual(self.call(self.body(action='reconcile'))['status'],'CONFIRMED')
        self.assertEqual(self.call(self.body())['status'],'DENIED')
        with closing(sqlite3.connect(self.root/'data'/'provider.sqlite3')) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM provider_refunds').fetchone()[0],1)

    def test_restart_reconcile_uses_existing_effect_and_identity(self):
        self.assertEqual(self.call(self.body(lose_ack=True))['status'],'UNKNOWN')
        self.stop_service()
        # A replacement E5 process uses the same protected fixture stores and
        # keys, but a fresh socket path so no stale socket is unlinked blindly.
        second_sock=self.root/'recovery.sock'
        recovery_ready=self.root/'recovery.ready'
        proc=subprocess.Popen([sys.executable,str(HERE/'service.py'),
            '--socket',str(second_sock),'--key',str(self.root/'grant.key'),
            '--identity-key',str(self.root/'identity.key'),
            '--data',str(self.root/'data'),'--ready',str(recovery_ready)],
            stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        def stop_recovery():
            if proc.poll() is None:proc.terminate()
            try:proc.communicate(timeout=3)
            except subprocess.TimeoutExpired:proc.kill();proc.communicate()
        self.addCleanup(stop_recovery)
        for _ in range(200):
            if recovery_ready.exists():break
            if proc.poll() is not None:self.fail('recovery service terminated')
            time.sleep(.01)
        else:self.fail('recovery service startup timed out')
        from client import request
        result=request(second_sock,self.body(action='reconcile'))
        self.assertEqual(result['status'],'CONFIRMED')
        with closing(sqlite3.connect(self.root/'data'/'provider.sqlite3')) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM provider_refunds').fetchone()[0],1)

    def test_outage_and_missing_provider_record_never_confirms(self):
        self.assertEqual(self.call(self.body(outage_before_send=True))['status'],'UNKNOWN')
        self.assertEqual(self.call(self.body(action='reconcile'))['status'],'UNKNOWN')

    def test_wrong_tenant_and_boolean_amount_denied(self):
        for changes in ({'tenant_id':'other'},{'amount_cents':True}):
            with self.subTest(changes=changes):self.assertEqual(self.call(self.body(**changes))['status'],'DENIED')
        self.assertFalse((self.root/'data'/'provider.sqlite3').exists())

    def test_expired_finance_grant_cannot_authorize_reconciliation(self):
        # The short-lived fixture grant is insufficient for a delayed operator
        # recovery workflow: production must supply distinct read-only rights.
        # Avoid Python's script-local `service` module collision with Build 3.
        spec=importlib.util.spec_from_file_location('etis_build4_service_under_test',HERE/'service.py')
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        old=issue_fixture_grant(self.grant_key,now=int(time.time())-120)
        response=module.handle(self.body(action='reconcile',approval_grant=old),
            identity=LocalAssertionAuthority(self.identity_key),
            grant_key=self.grant_key,
            ledger_path=self.root/'data'/'operations.sqlite3',
            provider_path=self.root/'data'/'provider.sqlite3',
            now=int(time.time()))
        self.assertEqual(response['status'],'DENIED')
        self.assertFalse((self.root/'data'/'provider.sqlite3').exists())

    def test_reconciliation_injection_flag_denied(self):
        self.assertEqual(self.call(self.body(action='reconcile',lose_ack=True))['status'],'DENIED')
        self.assertFalse((self.root/'data'/'provider.sqlite3').exists())

    def test_stalled_connection_has_bounded_delay(self):
        with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
            s.connect(str(self.sock));s.sendall(b'{"action":')
            time.sleep(1.0)
            self.assertEqual(self.call(self.body(approval_grant=''))['status'],'DENIED')
        self.assertIsNone(self.proc.poll())

    def test_disconnected_client_cannot_kill_service(self):
        with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
            s.connect(str(self.sock));s.sendall(b'garbage\n')
        time.sleep(.1)
        self.assertEqual(self.call(self.body(approval_grant=''))['status'],'DENIED')
        self.assertIsNone(self.proc.poll())


if __name__=='__main__': unittest.main()
