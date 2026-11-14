"""Build 2 educational E1->C03->E3/C04 composition with no E5/E6 path.

The Build 1 module uses local, script-oriented imports. Explicitly adding its
source directory preserves independent Build 1 execution for this checkpoint;
future packaging would replace this adapter with an installable package.
"""
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import sys

_BUILD1 = str(Path(__file__).resolve().parents[1] / 'build1')
if _BUILD1 not in sys.path:
    sys.path.insert(0, _BUILD1)
from advisory import advise  # noqa: E402 - build1 checkpoint adapter
from contracts import (AMOUNT_CENTS, CASE, EVIDENCE_VERSION, TENANT,  # noqa: E402
                       Evidence, InvalidAdvisory, Proposal, WorkRequest)
from context import FixtureCatalog, ScopedEvidence, retrieve
from identity import LocalAssertionAuthority, ScopeDenied

@dataclass(frozen=True)
class ReviewResult:
    proposal: Proposal
    source: str
    principal: str
    freshness_seconds: int
    note: str = 'UNTRUSTED_C04_NOT_AUTHORIZATION'


def bounded_review(*, assertion: str, issuer: LocalAssertionAuthority,
                   catalog: FixtureCatalog, source_id: str,
                   correlation_id: str, now: datetime) -> ReviewResult:
    """No refund adapter/database imported. Reject non-CASE-204 work before advice.

    Neither signature validity nor a recommendation grants payment authority.
    """
    scope = issuer.verify(assertion, now=now)
    if scope.case_id != CASE or scope.tenant_id != TENANT:
        raise ScopeDenied('no permitted Build 2 case for this identity scope')
    scoped: ScopedEvidence = retrieve(scope, source_id=source_id, catalog=catalog, now=now)
    record = scoped.record
    if record.evidence_version != EVIDENCE_VERSION:
        raise ScopeDenied('source version is not supported by Build 1 fixture')
    work = WorkRequest(correlation_id, scope.case_id, scope.tenant_id,
                       AMOUNT_CENTS, 'USD', record.evidence_version)
    evidence = Evidence(record.source_id, record.case_id, record.tenant_id,
                        record.evidence_version, record.replacement_delivered,
                        True, record.narrative)
    proposal = advise(work, evidence)
    if proposal.source_ids != (record.source_id,):
        raise InvalidAdvisory('advice provenance mismatch')
    age = int((scoped.retrieved_at - record.observed_at).total_seconds())
    return ReviewResult(proposal, record.source_id, scope.subject, age)
