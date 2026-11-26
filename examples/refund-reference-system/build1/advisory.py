"""Bounded deterministic E3 fixture; never imports the refund adapter."""
import hashlib
from contracts import (ADVISER_VERSION, SCHEMA_VERSION, AdvisoryUnavailable,
                       Disposition, Evidence, InvalidAdvisory, Proposal,
                       Uncertainty, WorkRequest, validate_proposal)
from model_interface import CandidateModel

def advise(work: WorkRequest, evidence: Evidence, model: CandidateModel | None = None) -> Proposal:
    """Only output C04 data; failures cannot trigger a consequential action.

    Model exceptions are contained as unavailable; malformed model output is
    separately rejected. No permissive fallback or payment execution occurs.
    """
    if not isinstance(work, WorkRequest) or not isinstance(evidence, Evidence):
        raise InvalidAdvisory("invalid request/evidence type")
    if (evidence.case_id != work.case_id or evidence.tenant_id != work.tenant_id or
            evidence.version != work.evidence_version or not evidence.verified):
        raise InvalidAdvisory("unverified or mismatched evidence")
    if model is not None:
        try:
            raw = model.propose(work, evidence)
        except Exception as exc:
            # Do not embed exception text; provider errors can leak secrets.
            raise AdvisoryUnavailable("advisory dependency unavailable") from exc
        proposal = Proposal.parse(raw)
    else:
        if evidence.replacement_delivered is False:
            disposition, reason, uncertainty, explanation = (
                Disposition.RECOMMEND_REVIEW, "REPLACEMENT_NOT_DELIVERED", Uncertainty.HIGH,
                "Verified fixture indicates non-delivery; human review is required.")
        elif evidence.replacement_delivered is True:
            disposition, reason, uncertainty, explanation = (
                Disposition.DO_NOT_RECOMMEND, "REPLACEMENT_DELIVERED", Uncertainty.LOW,
                "Verified fixture records delivery; the refund is not recommended.")
        else:
            disposition, reason, uncertainty, explanation = (
                Disposition.INSUFFICIENT_EVIDENCE, "DELIVERY_UNRESOLVED", Uncertainty.UNRESOLVED,
                "Delivery is unresolved; obtain independent evidence before review.")
        # Preserve the short human-readable ID. Long valid correlations need
        # a bounded deterministic identifier; '0' distinguishes this namespace
        # from direct IDs, whose correlation begins with an ASCII letter.
        proposal_id = "ADV-" + work.correlation_id
        if len(proposal_id) > 64:
            proposal_id = "ADV-0" + hashlib.sha256(work.correlation_id.encode('ascii')).hexdigest()[:59]
        proposal = Proposal(schema_version=SCHEMA_VERSION,
            proposal_id=proposal_id,
            correlation_id=work.correlation_id, case_id=work.case_id,
            tenant_id=work.tenant_id, requested_amount_cents=work.requested_amount_cents,
            currency=work.currency, source_ids=(evidence.source_id,),
            evidence_version=evidence.version, adviser_version=ADVISER_VERSION,
            disposition=disposition, reason_code=reason, explanation=explanation,
            uncertainty=uncertainty, review_required=True)
    validate_proposal(proposal, work, evidence)
    return proposal
