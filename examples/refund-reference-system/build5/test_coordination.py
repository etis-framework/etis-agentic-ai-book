"""Tests for atomic E2 ownership, fencing, crashes, and real E5 mediation."""
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import Mock

from coordinator import CoordinationError, DurableCoordinator, StaleOwner
from runner import BoundedRunner, RunnerUnavailable

HERE=Path(__file__).resolve().parent


class CoordinatorTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'e2.sqlite3'
        self.store=DurableCoordinator(self.path,lease_seconds=5)
        self.store.initialize()

    def owner(self,worker='a',now=100):
        return self.store.acquire(worker,now=now)

    def test_case_identity_and_initial_state(self):
        self.store.initialize()
        s=self.store.state()
        self.assertEqual(('RF-1042','READY',0),(s['operation_id'],s['phase'],s['epoch']))

    def test_lease_excludes_second_worker(self):
        self.owner()
        with self.assertRaises(CoordinationError):self.owner('b',now=104)

    def test_expiry_permits_fenced_replacement(self):
        a=self.owner()
        b=self.owner('b',now=105)
        self.assertEqual(b.epoch,a.epoch+1)
        with self.assertRaises(StaleOwner):self.store.choose(a,now=104)

    def test_same_worker_cannot_reclaim_active_epoch(self):
        self.owner()
        with self.assertRaises(CoordinationError):self.owner(now=101)

    def test_expired_lease_cannot_commit_result(self):
        a=self.owner()
        self.store.mark_execute_intent(a,now=100)
        with self.assertRaises(StaleOwner):self.store.observe(a,now=105,action='execute',outcome='CONFIRMED')

    def test_lease_renewal_and_old_lease_rejected(self):
        a=self.owner()
        b=self.store.renew(a,now=104)
        self.assertEqual(b.epoch,a.epoch)
        self.assertGreater(b.expires_at,a.expires_at)
        with self.assertRaises(StaleOwner):self.store.choose(a,now=104)
        self.assertEqual(self.store.choose(b,now=104),'execute')

    def test_invalid_worker_and_clock(self):
        for w in ('','../pwn','a b','x'*49,2,'🍕'):
            with self.subTest(worker=w),self.assertRaises(CoordinationError):self.owner(w)
        for t in (True,-1,'now'):
            with self.subTest(now=t),self.assertRaises(CoordinationError):self.owner(now=t)

    def test_clock_cannot_overflow_sqlite_lease_timestamp(self):
        for now in (2**63-1,2**63):
            with self.subTest(now=now),self.assertRaises(CoordinationError):
                self.owner(now=now)
        self.assertEqual(self.store.state()['epoch'],0)
        owner=self.owner(now=2**63-6)
        self.assertEqual(owner.expires_at,2**63-1)
        with self.assertRaises(CoordinationError):
            self.store.renew(owner,now=2**63-5)
        self.assertEqual(self.store.state()['expires_at'],owner.expires_at)

    def test_execute_intent_committed_before_e5_failure(self):
        a=self.owner()
        def disconnected(_):raise RunnerUnavailable('lost reply')
        r=BoundedRunner(self.store,disconnected)
        self.assertEqual(r.step(a,now=100),'NEEDS_RECONCILIATION')
        self.assertEqual(self.store.state()['last_outcome'],'execute:UNKNOWN')
        b=self.owner('b',now=105)
        self.assertEqual(self.store.choose(b,now=105),'reconcile')

    def test_crash_after_intent_before_e5_call_does_not_retry(self):
        a=self.owner()
        self.store.mark_execute_intent(a,now=100)
        restarted=DurableCoordinator(self.path,lease_seconds=5)
        b=restarted.acquire('restart',now=105)
        self.assertEqual(restarted.choose(b,now=105),'reconcile')
        with self.assertRaises(CoordinationError):restarted.mark_execute_intent(b,now=105)

    def test_reconciliation_never_promotes_missing_evidence(self):
        a=self.owner()
        calls=[]
        def e5(action):
            calls.append(action)
            return {'status':'UNKNOWN'}
        r=BoundedRunner(self.store,e5)
        self.assertEqual(r.step(a,now=100),'NEEDS_RECONCILIATION')
        self.assertEqual(r.step(a,now=101),'NEEDS_RECONCILIATION')
        self.assertEqual(calls,['execute','reconcile'])

    def test_reconciliation_denied_is_escalated_not_payment_failed(self):
        a=self.owner()
        outcomes=iter(({'status':'UNKNOWN'},{'status':'DENIED'}))
        r=BoundedRunner(self.store,lambda _:next(outcomes))
        r.step(a,now=100)
        self.assertEqual(r.step(a,now=101),'ESCALATED')
        self.assertEqual(r.step(a,now=102),'ESCALATED')

    def test_invalid_reply_fails_closed_as_unknown(self):
        a=self.owner()
        r=BoundedRunner(self.store,lambda _:{'status':'PAID'})
        self.assertEqual(r.step(a,now=100),'NEEDS_RECONCILIATION')

    def test_confirmed_is_terminal_and_cannot_redispatch(self):
        a=self.owner()
        fn=Mock(return_value={'status':'CONFIRMED','data':{'case_id':'CASE-204','operation_id':'RF-1042'}})
        r=BoundedRunner(self.store,fn)
        self.assertEqual(r.step(a,now=100),'CONFIRMED')
        self.assertEqual(r.step(a,now=100),'CONFIRMED')
        fn.assert_called_once_with('execute')

    def test_forged_confirmation_with_wrong_operation_is_unknown(self):
        a=self.owner()
        r=BoundedRunner(self.store,lambda _:{'status':'CONFIRMED',
            'data':{'case_id':'CASE-204','operation_id':'RF-9999'}})
        self.assertEqual(r.step(a,now=100),'NEEDS_RECONCILIATION')
        self.assertEqual(self.store.state()['last_outcome'],'execute:UNKNOWN')

    def test_confirmation_without_proof_is_unknown(self):
        a=self.owner()
        r=BoundedRunner(self.store,lambda _:{'status':'CONFIRMED'})
        self.assertEqual(r.step(a,now=100),'NEEDS_RECONCILIATION')

    def test_crash_after_effect_before_e2_receipt_reconciles_once(self):
        a=self.owner()
        self.store.mark_execute_intent(a,now=100)
        b=self.owner('recovery',now=105)
        seen=[]
        def e5(action):
            seen.append(action)
            return {'status':'CONFIRMED','data':{
                'case_id':'CASE-204','operation_id':'RF-1042'}}
        self.assertEqual(BoundedRunner(self.store,e5).step(b,now=105),'CONFIRMED')
        self.assertEqual(seen,['reconcile'])

    def test_denied_is_terminal(self):
        a=self.owner()
        r=BoundedRunner(self.store,lambda _:{'status':'DENIED'})
        self.assertEqual(r.step(a,now=100),'DENIED')
        self.assertEqual(self.store.choose(a,now=100),'none')

    def test_fake_same_epoch_rejected(self):
        a=self.owner()
        from coordinator import Ownership
        forged=Ownership('wrong',a.epoch,a.expires_at)
        with self.assertRaises(StaleOwner):self.store.mark_execute_intent(forged,now=100)

    def test_concurrent_acquire_has_one_winner(self):
        success=[]
        failures=[]
        def attempt(name):
            try:success.append(self.store.acquire(name,now=100))
            except CoordinationError as exc:failures.append(type(exc).__name__)
        threads=[threading.Thread(target=attempt,args=(f'w{i}',)) for i in range(8)]
        for t in threads:t.start()
        for t in threads:t.join()
        self.assertEqual(len(success),1)
        self.assertEqual(len(failures),7)

    def test_stale_owner_cannot_override_new_owner_reconcile(self):
        # E2 epochs fence stale local writes, not an E5 financial request.
        a=self.owner()
        self.store.mark_execute_intent(a,now=100)
        b=self.owner('b',now=105)
        self.store.observe(b,now=105,action='reconcile',outcome='UNKNOWN')
        with self.assertRaises(StaleOwner):self.store.observe(a,now=104,action='execute',outcome='CONFIRMED')
        self.assertEqual(self.store.state()['phase'],'NEEDS_RECONCILIATION')

    def test_wrong_transition_and_outcome(self):
        a=self.owner()
        with self.assertRaises(CoordinationError):self.store.observe(a,now=100,action='execute',outcome='CONFIRMED')
        with self.assertRaises(CoordinationError):self.store.observe(a,now=100,action='execute',outcome='BOGUS')
        self.store.mark_execute_intent(a,now=100)
        with self.assertRaises(CoordinationError):self.store.mark_execute_intent(a,now=100)

    def test_direct_run_demonstrations_with_real_e5_subprocess(self):
        for scenario in ('approved','denied','lost-ack','outage'):
            with self.subTest(scenario=scenario):
                completed=subprocess.run([sys.executable,str(HERE/'demo.py'),
                    '--scenario',scenario],capture_output=True,text=True,timeout=15)
                self.assertEqual(completed.returncode,0,completed.stdout+'\n'+completed.stderr)

if __name__=='__main__':unittest.main()
