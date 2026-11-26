"""Negative and crash-window evidence for the Chapter 28 pure decision fixture."""
import unittest
from dataclasses import replace
from recovery_cases import (CASE, OPERATION, EvidenceError, ProviderView,
                            RecoveryDecision, Snapshot, decide)


class RecoveryTests(unittest.TestCase):
    def base(self, view=ProviderView.NOT_FOUND):
        return Snapshot(CASE, OPERATION, True, "UNKNOWN", view)

    def test_not_found_never_declares_failure(self):
        # An absent provider record cannot prove that the previous send failed.
        self.assertEqual(decide(self.base()), RecoveryDecision.ESCALATE)

    def test_unavailable_requires_inquiry_not_execution(self):
        self.assertEqual(decide(self.base(ProviderView.UNAVAILABLE)), RecoveryDecision.INQUIRE)

    def test_conflicting_observations_escalate(self):
        self.assertEqual(decide(self.base(ProviderView.CONFLICT)), RecoveryDecision.ESCALATE)

    def test_lost_ack_confirmation_matches_original_operation(self):
        snapshot=replace(self.base(ProviderView.CONFIRMED),
                         proof_case_id=CASE, proof_operation_id=OPERATION)
        self.assertEqual(decide(snapshot), RecoveryDecision.CONFIRM)

    def test_wrong_operation_proof_escalates(self):
        snapshot=replace(self.base(ProviderView.CONFIRMED),
                         proof_case_id=CASE, proof_operation_id="RF-9999")
        self.assertEqual(decide(snapshot), RecoveryDecision.ESCALATE)

    def test_crash_before_send_but_after_e2_intent_cannot_restart_effect(self):
        snapshot=replace(self.base(ProviderView.NOT_FOUND), e7_state="ABSENT")
        self.assertEqual(decide(snapshot), RecoveryDecision.ESCALATE)

    def test_no_intent_cannot_recover_by_issuing_effect(self):
        snapshot=replace(self.base(), intent_committed=False, e7_state="ABSENT")
        self.assertEqual(decide(snapshot), RecoveryDecision.ESCALATE)

    def test_wrong_case_and_bool_injection_are_invalid(self):
        for changes in ({"case_id":"OTHER"},{"intent_committed":1},{"e7_state":"FAILED"}):
            with self.subTest(changes=changes), self.assertRaises(EvidenceError):
                decide(replace(self.base(), **changes))

    def test_invalid_proof_shapes_are_rejected(self):
        with self.assertRaises(EvidenceError):
            decide(replace(self.base(ProviderView.CONFIRMED),proof_case_id=CASE))
        with self.assertRaises(EvidenceError):
            decide(replace(self.base(),proof_case_id=CASE))
        with self.assertRaises(EvidenceError):
            decide(replace(self.base(),provider_view="CONFIRMED"))

    def test_unhashable_e7_state_is_typed_evidence_error(self):
        for state in ([], {}):
            with self.subTest(state=state), self.assertRaises(EvidenceError):
                decide(replace(self.base(), e7_state=state))

    def test_confirmation_before_dispatch_is_escalated(self):
        # A PREPARED record is not evidence of a durable dispatch claim.
        snapshot = replace(self.base(ProviderView.CONFIRMED), e7_state='PREPARED',
                           proof_case_id=CASE, proof_operation_id=OPERATION)
        self.assertEqual(decide(snapshot), RecoveryDecision.ESCALATE)

    def test_fixture_does_not_expose_effectful_method(self):
        import recovery_cases
        for unsafe in ("execute", "send", "dispatch", "refund", "issue_grant"):
            self.assertFalse(hasattr(recovery_cases,unsafe))


if __name__ == "__main__":
    unittest.main()
