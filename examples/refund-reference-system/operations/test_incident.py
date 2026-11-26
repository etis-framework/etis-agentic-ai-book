"""Chapter 30 negative tests: actual Build 4/5 durable fixtures, no new payment route.

The tests may set up a mock provider effect with Build 4. The *observer* does
not import or invoke that provider; before/after database digests make a local
non-mutation claim falsifiable. Tests do NOT prove external provider absence.
"""
from contextlib import closing
from hashlib import sha256
from pathlib import Path
import sys
import tempfile
import unittest
import sqlite3

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/'build4'))
from provider_contracts import RefundCommand
from adapter import SQLiteFixtureProvider
from ledger import OperationalLedger
from workflow import OutcomeUnknown, RefundWorkflow
sys.path.insert(0, str(HERE.parent/'build5'))
from coordinator import DurableCoordinator
from incident import assess, Signal, SignalKind, ProviderStatus, IncidentInputError


class IncidentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='etis-incident-')
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.e2_file, self.e7_file, self.e8_file = [root / n for n in
            ('coordination.sqlite3','operations.sqlite3','provider.sqlite3')]
        self.e2 = DurableCoordinator(self.e2_file, lease_seconds=5)
        self.e2.initialize()
        self.owner = self.e2.acquire('worker1', now=100)
        self.ledger = OperationalLedger(self.e7_file)
        self.provider = SQLiteFixtureProvider(self.e8_file)
        self.command = RefundCommand()
        self.workflow = RefundWorkflow(self.ledger, self.provider)
        # Actual Build 4 effect fixture; acknowledgment is lost AFTER mock E8 commit.
        with self.assertRaises(OutcomeUnknown):
            self.workflow.execute(self.command, lose_ack=True)
        self.e2.mark_execute_intent(self.owner, now=100)
        self.e2.observe(self.owner, now=100, action='execute', outcome='UNKNOWN')

    @staticmethod
    def signals(*kinds):
        return tuple(Signal(i+1,f'evt{i+1}',k) for i,k in enumerate(kinds))

    def check_read_only(self, provider, signals, **kwargs):
        files = (self.e2_file,self.e7_file,self.e8_file)
        old = tuple(sha256(f.read_bytes()).hexdigest() for f in files)
        with closing(sqlite3.connect(self.e8_file)) as db, db:
            count = db.execute('SELECT count(*) FROM provider_refunds').fetchone()[0]
        result = assess(self.e2_file,self.e7_file,provider=provider,signals=signals,**kwargs)
        self.assertEqual(tuple(sha256(f.read_bytes()).hexdigest() for f in files),old)
        with closing(sqlite3.connect(self.e8_file)) as db, db:
            self.assertEqual(db.execute('SELECT count(*) FROM provider_refunds').fetchone()[0], count)
        self.assertEqual(count,1)
        self.assertEqual(result.operation_id,'RF-1042')
        self.assertEqual(result.allowed_action,'READ_ONLY_RECONCILE_OR_ESCALATE')
        return result

    def test_lost_ack_unknown_with_confirmed_synthetic_e8_still_requires_review(self):
        result=self.check_read_only(ProviderStatus.CONFIRMED,self.signals(SignalKind.E7_UNKNOWN))
        self.assertEqual((result.severity,result.disposition),('SEV2','INQUIRE'))

    def test_not_found_is_not_payment_failure(self):
        result=self.check_read_only(ProviderStatus.NOT_FOUND,self.signals(SignalKind.E7_UNKNOWN))
        self.assertEqual(result.disposition,'INQUIRE')
        self.assertNotIn('FAILED',str(result.as_record()))

    def test_outage_never_produces_dispatch(self):
        result=self.check_read_only(ProviderStatus.UNAVAILABLE,self.signals(SignalKind.E8_UNAVAILABLE))
        self.assertEqual(result.next_role,'reconciliation-operator')

    def test_conflicting_provider_evidence_escalates(self):
        result=self.check_read_only(ProviderStatus.CONFLICT,self.signals(SignalKind.E8_CONFLICT))
        self.assertEqual((result.severity,result.disposition),('SEV1','ESCALATE'))

    def test_out_of_order_signals_have_identical_disposition(self):
        values=self.signals(SignalKind.E7_UNKNOWN,SignalKind.E8_UNAVAILABLE)
        left=self.check_read_only(ProviderStatus.UNAVAILABLE,values)
        right=self.check_read_only(ProviderStatus.UNAVAILABLE,tuple(reversed(values)))
        self.assertEqual(left,right)

    def test_missing_telemetry_never_closes_case(self):
        values=(Signal(1,'evt1',SignalKind.E7_UNKNOWN),Signal(3,'evt3',SignalKind.E8_UNAVAILABLE))
        result=self.check_read_only(ProviderStatus.CONFIRMED,values)
        self.assertTrue(result.event_gap)
        self.assertEqual(result.disposition,'INQUIRE')

    def test_empty_signal_stream_is_missing_evidence(self):
        self.assertEqual(self.workflow.reconcile(self.command),'CONFIRMED')
        result=self.check_read_only(ProviderStatus.CONFIRMED,())
        self.assertTrue(result.event_gap)
        self.assertEqual(result.disposition,'INQUIRE')

    def test_duplicate_event_identity_rejected(self):
        values=(Signal(1,'evt1',SignalKind.E7_UNKNOWN),Signal(2,'evt1',SignalKind.E7_UNKNOWN))
        with self.assertRaises(IncidentInputError):
            assess(self.e2_file,self.e7_file,provider=ProviderStatus.CONFIRMED,signals=values)

    def test_duplicate_event_sequence_rejected(self):
        values=(Signal(1,'evt1',SignalKind.E7_UNKNOWN),Signal(1,'evt2',SignalKind.E8_UNAVAILABLE))
        with self.assertRaises(IncidentInputError):
            assess(self.e2_file,self.e7_file,provider=ProviderStatus.CONFIRMED,signals=values)

    def test_stale_epoch_cannot_authorize_action(self):
        result=self.check_read_only(ProviderStatus.CONFIRMED,self.signals(SignalKind.STALE_OWNER),expected_epoch=0)
        self.assertEqual((result.severity,result.disposition),('SEV1','QUARANTINE'))

    def test_revoked_token_quarantines(self):
        result=self.check_read_only(ProviderStatus.CONFIRMED,self.signals(SignalKind.TOKEN_REVOKED))
        self.assertEqual((result.severity,result.next_role),('SEV1','security-incident-command'))

    def test_unavailable_verifier_quarantines(self):
        result=self.check_read_only(ProviderStatus.CONFIRMED,self.signals(SignalKind.VERIFIER_UNAVAILABLE))
        self.assertEqual(result.disposition,'QUARANTINE')

    def test_no_credential_or_untrusted_payload_in_report(self):
        # An unsafe event ID is rejected; no free-form event detail is accepted.
        with self.assertRaises(IncidentInputError):
            assess(self.e2_file,self.e7_file,provider=ProviderStatus.UNAVAILABLE,
                   signals=(Signal(1,'Bearer secret-token',SignalKind.E5_DENIED),))
        report=self.check_read_only(ProviderStatus.UNAVAILABLE,self.signals(SignalKind.E5_DENIED)).as_record()
        self.assertFalse(any(s in repr(report).lower() for s in ('bearer ','secret-token','grant_key','identity.key')))
        self.assertEqual(set(report),{'severity','disposition','next_role','operation_id','e7_status',
                                     'e2_phase','e2_epoch','signals','event_gap','rationale','allowed_action'})

    def test_missing_evidence_files_fail_closed_no_creation(self):
        self.e2_file.unlink()
        with self.assertRaises(IncidentInputError):
            assess(self.e2_file,self.e7_file,provider=ProviderStatus.NOT_FOUND,signals=())
        self.assertFalse(self.e2_file.exists())

    def test_local_conflicting_confirmation_history_is_not_erased(self):
        # First reconcile provides local CONFIRMED, then new evidence contradicts it.
        self.assertEqual(self.workflow.reconcile(self.command),'CONFIRMED')
        before = self.ledger.history(self.command)
        with closing(sqlite3.connect(self.e8_file)) as db, db:
            db.execute('UPDATE provider_refunds SET amount_cents=1 WHERE operation_id=?',('RF-1042',))
        with self.assertRaises(OutcomeUnknown):
            self.workflow.reconcile(self.command)
        history = self.ledger.history(self.command)
        self.assertEqual(history[:len(before)],before)
        result=self.check_read_only(ProviderStatus.CONFLICT,self.signals(SignalKind.E8_CONFLICT))
        self.assertEqual((result.e7_status,result.disposition),('UNKNOWN','ESCALATE'))


if __name__=='__main__':
    unittest.main()
