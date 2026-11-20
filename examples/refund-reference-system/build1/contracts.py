"""Build 1's bounded C02/C04 contracts; no privileged operation types.

Validate at the boundary, without coercing model-originated data. This module
is not an authentication service or a transaction authorization control.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping
import re

CASE = "CASE-204"
TENANT = "retailer_a"
AMOUNT_CENTS = 50_000
SCHEMA_VERSION = "advisory-v1"
EVIDENCE_VERSION = "case204-fixture-v1"
ADVISER_VERSION = "deterministic-adviser-v1"
MAX_EXPLANATION = 400

class InvalidAdvisory(ValueError):
    """Untrusted request, evidence or output fails a strict contract."""

class AdvisoryUnavailable(RuntimeError):
    """Optional advisory dependency unavailable; do not execute an effect."""

class Disposition(str, Enum):
    RECOMMEND_REVIEW = "RECOMMEND_REVIEW"
    DO_NOT_RECOMMEND = "DO_NOT_RECOMMEND"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"

class Uncertainty(str, Enum):
    LOW = "LOW"
    HIGH = "HIGH"
    UNRESOLVED = "UNRESOLVED"

_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]{2,63}$")

def required_id(value: object, name: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise InvalidAdvisory(f"invalid {name}")
    return value

# Model output is data from a lower-trust source. Compare the entire key set:
# accepting an extra ``approved`` or ``provider_key`` would silently expand C04.
# In particular, never coerce unknown fields into a trusted authorization shape.
def exact_fields(raw: Mapping[str, Any], expected: frozenset[str]) -> None:
    if not isinstance(raw, dict) or frozenset(raw) != expected:
        raise InvalidAdvisory("proposal field set mismatch")

@dataclass(frozen=True)
class WorkRequest:
    """C02-style bounded fixture work, NOT authenticated E1 identity."""
    correlation_id: str
    case_id: str
    tenant_id: str
    requested_amount_cents: int
    currency: str
    evidence_version: str

    def __post_init__(self) -> None:
        # The advisory correlation identifies an investigation, never a payment.
        # Using the fixed operation ID here would blur the C04/E5 boundary.
        required_id(self.correlation_id, "correlation_id")
        if self.correlation_id == "RF-1042":
            raise InvalidAdvisory("financial operation identifiers are prohibited")
        if (self.case_id != CASE or self.tenant_id != TENANT or
            type(self.requested_amount_cents) is not int or
            self.requested_amount_cents != AMOUNT_CENTS or self.currency != "USD" or
            self.evidence_version != EVIDENCE_VERSION):
            raise InvalidAdvisory("work outside bounded fixture scope")

@dataclass(frozen=True)
class Evidence:
    """Explicitly supplied E4-like facts, not retrieval or policy authority."""
    source_id: str
    case_id: str
    tenant_id: str
    version: str
    replacement_delivered: bool | None
    verified: bool
    narrative: str

    def __post_init__(self) -> None:
        required_id(self.source_id, "source_id")
        if (self.case_id != CASE or self.tenant_id != TENANT or
            self.version != EVIDENCE_VERSION or
            self.replacement_delivered not in (True, False, None) or
            type(self.verified) is not bool or not isinstance(self.narrative, str) or
            len(self.narrative) > 500):
            raise InvalidAdvisory("evidence out of scope, stale, or malformed")
        if self.replacement_delivered is not None and type(self.replacement_delivered) is not bool:
            raise InvalidAdvisory("replacement status must be bool or None")

@dataclass(frozen=True)
class Proposal:
    """An immutable C04 recommendation. It contains no authorization bit or key."""
    schema_version: str
    proposal_id: str
    correlation_id: str
    case_id: str
    tenant_id: str
    requested_amount_cents: int
    currency: str
    source_ids: tuple[str, ...]
    evidence_version: str
    adviser_version: str
    disposition: Disposition
    reason_code: str
    explanation: str
    uncertainty: Uncertainty
    review_required: bool

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise InvalidAdvisory("unsupported proposal schema")
        for name in ("proposal_id", "correlation_id", "reason_code", "adviser_version"):
            required_id(getattr(self, name), name)
        if self.proposal_id == "RF-1042" or self.correlation_id == "RF-1042":
            raise InvalidAdvisory("proposal identifiers cannot be payment identifiers")
        if (self.case_id != CASE or self.tenant_id != TENANT or
            type(self.requested_amount_cents) is not int or
            self.requested_amount_cents != AMOUNT_CENTS or
            self.currency != "USD" or self.evidence_version != EVIDENCE_VERSION):
            raise InvalidAdvisory("proposal outside work scope")
        if (type(self.source_ids) is not tuple or not self.source_ids or
            len(self.source_ids) > 8 or
            any(not isinstance(v, str) for v in self.source_ids) or
            len(set(self.source_ids)) != len(self.source_ids)):
            raise InvalidAdvisory("invalid evidence sources")
        for source in self.source_ids:
            required_id(source, "source_id")
        if (type(self.disposition) is not Disposition or type(self.uncertainty) is not Uncertainty or
            type(self.review_required) is not bool or not self.review_required or
            not isinstance(self.explanation, str) or not 1 <= len(self.explanation) <= MAX_EXPLANATION):
            raise InvalidAdvisory("invalid recommendation fields")
        if (self.disposition is Disposition.INSUFFICIENT_EVIDENCE and
            self.uncertainty is not Uncertainty.UNRESOLVED):
            raise InvalidAdvisory("unresolved advice must declare uncertainty")

    @classmethod
    # Validate candidate fields before interpreting enum values.
    # This C04 data is never an E5 finance grant.
    def parse(cls, raw: Mapping[str, Any]) -> "Proposal":
        """Reject additional fields, including forged approved/provider_key."""
        exact_fields(raw, frozenset(cls.__dataclass_fields__))
        try:
            values = dict(raw)
            values["disposition"] = Disposition(values["disposition"])
            values["uncertainty"] = Uncertainty(values["uncertainty"])
            if type(values["source_ids"]) is not list:
                raise InvalidAdvisory("source_ids must be a list")
            values["source_ids"] = tuple(values["source_ids"])
            return cls(**values)
        except (ValueError, TypeError, KeyError) as exc:
            raise InvalidAdvisory("invalid proposal payload") from exc

    def to_dict(self) -> dict[str, object]:
        return {**vars(self), "source_ids": list(self.source_ids),
                "disposition": self.disposition.value, "uncertainty": self.uncertainty.value}


def validate_proposal(proposal: Proposal, work: WorkRequest, evidence: Evidence) -> None:
    """A separate fixture validator. Passing does NOT mean E5 authorization."""
    if not isinstance(proposal, Proposal) or not isinstance(work, WorkRequest) or not isinstance(evidence, Evidence):
        raise InvalidAdvisory("invalid types")
    if (proposal.correlation_id != work.correlation_id or
        proposal.case_id != work.case_id or proposal.tenant_id != work.tenant_id or
        proposal.requested_amount_cents != work.requested_amount_cents or
        proposal.currency != work.currency or proposal.evidence_version != work.evidence_version or
        proposal.source_ids != (evidence.source_id,) or
        evidence.case_id != work.case_id or evidence.tenant_id != work.tenant_id or
        evidence.version != work.evidence_version or not evidence.verified):
        raise InvalidAdvisory("proposal correlation, scope or evidence mismatch")
    if evidence.replacement_delivered is None and proposal.disposition is not Disposition.INSUFFICIENT_EVIDENCE:
        raise InvalidAdvisory("unsupported recommendation from missing facts")
    if evidence.replacement_delivered is True and proposal.disposition is Disposition.RECOMMEND_REVIEW:
        raise InvalidAdvisory("recommendation contradicts verified delivery")
