from contextlib import closing
"""Executable evidence: no real provider, network, secrets, or external packages."""
import sqlite3
from concurrent.futures import ThreadPoolExecutor
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from refund import (initialize, prepare, dispatch, reconcile, status, Denied,
                    AMOUNT_CENTS, CASE, OPERATION)

class Build0Test(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.local = Path(self.tmp.name)/'operations.sqlite3'
        self.provider = Path(self.tmp.name)/'provider.sqlite3'
        initialize(self.local, self.provider)

    def count(self):
        with closing(sqlite3.connect(self.provider)) as db, db:
            return db.execute('SELECT COUNT(*) FROM refunds').fetchone()[0]

    def test_two_concurrent_dispatchers_only_one_wins(self):
        """Atomic E7 state claim permits one simulated consequential call."""
        prepare(self.local)
        def attempt(_):
            try:
                return dispatch(self.local, self.provider)
            except Denied:
                return 'DENIED'
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(attempt, range(2)))
        self.assertCountEqual(results, ['CONFIRMED', 'DENIED'])
        self.assertEqual(self.count(), 1)

    def test_provider_unavailable_stays_dispatched_and_cannot_retry(self):
        """A committed E7 claim survives failure before mock E8 can commit."""
        from refund import ProviderUnavailable
        prepare(self.local)
        with self.assertRaises(ProviderUnavailable):
            dispatch(self.local, self.provider, fail_before_provider_commit=True)
        self.assertEqual(status(self.local)[0], 'DISPATCHED')
        self.assertEqual(self.count(), 0)
        self.assertEqual(reconcile(self.local, self.provider), 'UNKNOWN')
        with self.assertRaises(Denied):
            dispatch(self.local, self.provider)

    def test_reject_noninteger_and_boolean_money(self):
        """Python bool is an int subtype, so explicit type checks matter."""
        for value in (True, False, 50000.0, '50000', None, -1):
            with self.subTest(value=value), self.assertRaises(Denied):
                prepare(self.local, amount_cents=value)
        for value in (True, 50000.0, '50000', None):
            with self.subTest(value=value), self.assertRaises(Denied):
                prepare(self.local, refundable_cents=value)
        for value in (1, 'true', None):
            with self.subTest(value=value), self.assertRaises(Denied):
                prepare(self.local, approved=value)
        self.assertIsNone(status(self.local))

    def test_stores_must_be_separate(self):
        """Do not accidentally collapse E7 and mock E8 into one authority."""
        with self.assertRaises(ValueError):
            initialize(self.local, self.local)

    def test_cli_denial_is_bounded_and_nonzero(self):
        """An expected denial is a readable JSON error, not a traceback."""
        script = Path(__file__).with_name('refund.py')
        proc = subprocess.run([sys.executable, str(script), 'dispatch',
                               '--directory', self.tmp.name],
                              text=True, capture_output=True, check=False)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(__import__('json').loads(proc.stderr)['error'], 'DENIED')
        self.assertNotIn('Traceback', proc.stderr)
        self.assertEqual(self.count(), 0)

    def test_conflicting_provider_state_cannot_override_e7(self):
        """A different amount is not silently accepted as a matching refund."""
        prepare(self.local)
        with closing(sqlite3.connect(self.provider)) as db, db:
            db.execute('INSERT INTO refunds VALUES (?,?,?,?)',
                       (OPERATION, CASE, 1234, 'CONFIRMED'))
        with self.assertRaises(Denied):
            dispatch(self.local, self.provider)
        self.assertEqual(status(self.local)[0], 'DISPATCHED')
        self.assertEqual(reconcile(self.local, self.provider), 'UNKNOWN')
        self.assertEqual(self.count(), 1)  # Contradictory record, not a verified refund

    def test_success_and_duplicate_preparation(self):
        self.assertEqual(prepare(self.local), OPERATION)
        self.assertEqual(prepare(self.local), OPERATION)
        self.assertEqual(dispatch(self.local,self.provider), 'CONFIRMED')
        self.assertEqual(self.count(),1)
        with self.assertRaises(Denied): dispatch(self.local,self.provider)

    def test_lost_ack_and_recovery(self):
        prepare(self.local)
        self.assertEqual(dispatch(self.local,self.provider,lose_ack=True),'UNKNOWN')
        self.assertEqual(status(self.local)[0],'UNKNOWN')
        with self.assertRaises(Denied): dispatch(self.local,self.provider)
        self.assertEqual(reconcile(self.local,self.provider),'CONFIRMED')
        self.assertEqual(self.count(),1)

    def test_denials_do_not_create_operation(self):
        for bad in ({'tenant':'another_tenant'}, {'approved':False},
                    {'principal':'agent_token'}, {'amount_cents':AMOUNT_CENTS+1},
                    {'refundable_cents':AMOUNT_CENTS-1}, {'policy_version':'obsolete'},
                    {'case_id':'CASE-999'}):
            with self.subTest(bad=bad), self.assertRaises(Denied):
                prepare(self.local,**bad)
        self.assertIsNone(status(self.local))
        self.assertEqual(self.count(),0)

    def test_no_intent_cannot_dispatch(self):
        with self.assertRaises(Denied): dispatch(self.local,self.provider)

    def test_provider_absence_does_not_allow_resubmission(self):
        prepare(self.local)
        with closing(sqlite3.connect(self.local)) as db, db:
            db.execute("UPDATE operations SET status='DISPATCHED' WHERE operation_id=?",(OPERATION,))
        self.assertEqual(reconcile(self.local,self.provider),'UNKNOWN')
        with self.assertRaises(Denied): dispatch(self.local,self.provider)
        self.assertEqual(self.count(),0)

    def test_conflicting_provider_record_cannot_be_accepted(self):
        prepare(self.local)
        with closing(sqlite3.connect(self.local)) as db, db:
            db.execute("UPDATE operations SET status='UNKNOWN' WHERE operation_id=?",(OPERATION,))
        with closing(sqlite3.connect(self.provider)) as db, db:
            db.execute('INSERT INTO refunds VALUES (?,?,?,?)',(OPERATION,CASE,100,'CONFIRMED'))
        self.assertEqual(reconcile(self.local,self.provider),'UNKNOWN')

    def test_reopen_databases_after_lost_ack(self):
        """A separate SQLite connection can recover E7/E8 after an invocation ends."""
        prepare(self.local)
        dispatch(self.local, self.provider, lose_ack=True)
        with closing(sqlite3.connect(self.local)) as local_db, local_db, closing(sqlite3.connect(self.provider)) as provider_db, provider_db:
            self.assertEqual(local_db.execute('SELECT status FROM operations').fetchone()[0], 'UNKNOWN')
            self.assertEqual(provider_db.execute('SELECT operation_id,status FROM refunds').fetchone(),
                             (OPERATION, 'CONFIRMED'))
        self.assertEqual(reconcile(self.local, self.provider), 'CONFIRMED')
        self.assertEqual(self.count(), 1)

    def test_repeated_authorization_cannot_change_immutable_intent(self):
        """Second preparation does not mutate the authorized operation record."""
        prepare(self.local)
        with closing(sqlite3.connect(self.local)) as db, db:
            before = db.execute('SELECT * FROM operations').fetchall()
        prepare(self.local)
        with closing(sqlite3.connect(self.local)) as db, db:
            after = db.execute('SELECT * FROM operations').fetchall()
        self.assertEqual(before, after)
        self.assertEqual(self.count(), 0)

    def test_reconcile_cannot_create_intent_or_provider_effect(self):
        """Lookup is not an alternate authorization or payment path."""
        with self.assertRaises(Denied):
            reconcile(self.local, self.provider)
        self.assertIsNone(status(self.local))
        self.assertEqual(self.count(), 0)

    def test_authorized_not_dispatched_is_not_a_provider_success(self):
        """A durable local AUTHORIZED row is not proof that the provider was called."""
        prepare(self.local)
        self.assertEqual(status(self.local)[0], 'AUTHORIZED')
        self.assertEqual(self.count(), 0)
        with self.assertRaises(Denied):
            reconcile(self.local, self.provider)
        self.assertEqual(self.count(), 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
