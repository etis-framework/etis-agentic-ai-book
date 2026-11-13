"""Executable evidence: no real provider, network, secrets, or external packages."""
import sqlite3
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
        with sqlite3.connect(self.provider) as db:
            return db.execute('SELECT COUNT(*) FROM refunds').fetchone()[0]

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
        with sqlite3.connect(self.local) as db:
            db.execute("UPDATE operations SET status='DISPATCHED' WHERE operation_id=?",(OPERATION,))
        self.assertEqual(reconcile(self.local,self.provider),'UNKNOWN')
        with self.assertRaises(Denied): dispatch(self.local,self.provider)
        self.assertEqual(self.count(),0)

    def test_conflicting_provider_record_cannot_be_accepted(self):
        prepare(self.local)
        with sqlite3.connect(self.local) as db:
            db.execute("UPDATE operations SET status='UNKNOWN' WHERE operation_id=?",(OPERATION,))
        with sqlite3.connect(self.provider) as db:
            db.execute('INSERT INTO refunds VALUES (?,?,?,?)',(OPERATION,CASE,100,'CONFIRMED'))
        self.assertEqual(reconcile(self.local,self.provider),'UNKNOWN')

    def test_reopen_databases_after_lost_ack(self):
        """A separate SQLite connection can recover E7/E8 after an invocation ends."""
        prepare(self.local)
        dispatch(self.local, self.provider, lose_ack=True)
        with sqlite3.connect(self.local) as local_db, sqlite3.connect(self.provider) as provider_db:
            self.assertEqual(local_db.execute('SELECT status FROM operations').fetchone()[0], 'UNKNOWN')
            self.assertEqual(provider_db.execute('SELECT operation_id,status FROM refunds').fetchone(),
                             (OPERATION, 'CONFIRMED'))
        self.assertEqual(reconcile(self.local, self.provider), 'CONFIRMED')
        self.assertEqual(self.count(), 1)

    def test_repeated_authorization_cannot_change_immutable_intent(self):
        """Second preparation does not mutate the authorized operation record."""
        prepare(self.local)
        with sqlite3.connect(self.local) as db:
            before = db.execute('SELECT * FROM operations').fetchall()
        prepare(self.local)
        with sqlite3.connect(self.local) as db:
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
