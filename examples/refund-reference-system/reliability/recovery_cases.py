"""Chapter 28: pure, typed recovery classification; NEVER an effectful adapter.

All observation values are synthetic fixtures. This module has no send, execute,
provider credential, network or database write; it cannot enforce production E5
ownership fencing. See README for scope and tests.
"""
from dataclasses import dataclass
from enum import Enum

CASE = "CASE-204"
OPERATION = "RF-1042"


class EvidenceError(ValueError):
    """Invalid or contradictory evidence fixture."""


class ProviderView(str, Enum):
    CONFIRMED = "CONFIRMED"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    UNAVAILABLE = "UNAVAILABLE"


class RecoveryDecision(str, Enum):
    CONFIRM = "CONFIRM"
    INQUIRE = "INQUIRE"
    ESCALATE = "ESCALATE"


@dataclass(frozen=True)
class Snapshot:
    case_id: str
    operation_id: str
    intent_committed: bool
    e7_state: str
    provider_view: ProviderView
    proof_case_id: str | None = None
    proof_operation_id: str | None = None

    def validate(self) -> None:
        if self.case_id != CASE or self.operation_id != OPERATION:
            raise EvidenceError("unrecognized recovery identity")
        if type(self.intent_committed) is not bool:
            raise EvidenceError("intent flag must be bool")
        if self.e7_state not in {"ABSENT", "PREPARED", "DISPATCHED", "UNKNOWN", "CONFIRMED"}:
            raise EvidenceError("invalid E7 state")
        if not isinstance(self.provider_view, ProviderView):
            raise EvidenceError("invalid provider observation")
        if self.provider_view == ProviderView.CONFIRMED:
            if not self.proof_case_id or not self.proof_operation_id:
                raise EvidenceError("confirmation lacks correlation fields")
        elif self.proof_case_id is not None or self.proof_operation_id is not None:
            raise EvidenceError("nonconfirmation cannot carry confirmation proof")


def decide(snapshot: Snapshot) -> RecoveryDecision:
    """Classify evidence without dispatching or declaring provider failure.

    CONFIRM is an *educational classification only*, assuming a trusted E8
    source. Real systems must verify provenance, amount, currency, finality,
    retention and authorized E5 reconciliation before changing E7.
    """
    if not isinstance(snapshot, Snapshot):
        raise EvidenceError("expected Snapshot")
    snapshot.validate()
    if snapshot.provider_view == ProviderView.CONFIRMED:
        if (snapshot.proof_case_id, snapshot.proof_operation_id) != (CASE, OPERATION):
            return RecoveryDecision.ESCALATE
        if not snapshot.intent_committed or snapshot.e7_state == "ABSENT":
            return RecoveryDecision.ESCALATE
        return RecoveryDecision.CONFIRM
    if snapshot.provider_view == ProviderView.CONFLICT:
        return RecoveryDecision.ESCALATE
    if not snapshot.intent_committed and snapshot.e7_state == "ABSENT":
        return RecoveryDecision.ESCALATE  # requires normal admission, not "recovery" dispatch
    return RecoveryDecision.INQUIRE if snapshot.provider_view == ProviderView.UNAVAILABLE else RecoveryDecision.ESCALATE
