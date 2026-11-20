"""E4/C03 fixture gateway: source-selection, provenance and freshness controls.

Only the gateway looks up catalog data. Customer prose is never an instruction,
verified business authority or a payment operation. Source labels are fixtures.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Mapping
from identity import ContextUnavailable, ScopeDenied, VerifiedScope

MAX_AGE_SECONDS = 300
MAX_NARRATIVE = 500

@dataclass(frozen=True)
class CatalogRecord:
    tenant_id: str
    case_id: str
    source_id: str
    evidence_version: str
    observed_at: datetime
    replacement_delivered: bool | None
    narrative: str
    classification: str = 'CASE_RESTRICTED'

    def __post_init__(self) -> None:
        if (not isinstance(self.tenant_id, str) or not isinstance(self.case_id, str) or
            not isinstance(self.source_id, str) or not isinstance(self.evidence_version, str) or
            self.classification != 'CASE_RESTRICTED' or not isinstance(self.narrative, str) or
            len(self.narrative) > MAX_NARRATIVE or
            (self.replacement_delivered is not None and type(self.replacement_delivered) is not bool) or
            not isinstance(self.observed_at, datetime) or self.observed_at.tzinfo is None or
            self.observed_at.utcoffset() is None):
            raise ScopeDenied('invalid catalog record')


@dataclass(frozen=True)
class ScopedEvidence:
    record: CatalogRecord
    retrieved_at: datetime
    principal: str
    purpose: str
    provenance: str


class FixtureCatalog:
    """Read-only educational data lookup, keyed by tenant/case/source."""
    def __init__(self, records: Mapping[tuple[str, str, str], CatalogRecord], *, fail: bool = False):
        self._records = dict(records)
        self._fail = fail

    def get(self, tenant_id: str, case_id: str, source_id: str) -> CatalogRecord:
        if self._fail:
            raise ContextUnavailable('context source unavailable')
        # The lookup key restricts selection, but the record's own provenance
        # is checked below too: a misindexed entry must fail closed.
        record = self._records.get((tenant_id, case_id, source_id))
        if record is None:
            raise ScopeDenied('source not available for asserted scope')
        if (record.tenant_id, record.case_id, record.source_id) != (tenant_id, case_id, source_id):
            raise ScopeDenied('catalog index does not match record provenance')
        return record


def retrieve(scope: VerifiedScope, *, source_id: str, catalog: FixtureCatalog,
             now: datetime) -> ScopedEvidence:
    """Simulated C03 gate. Consume only verifier output, never self-asserted claims."""
    if type(scope) is not VerifiedScope or type(catalog) is not FixtureCatalog:
        raise ScopeDenied('verified fixture scope and catalog required')
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise ScopeDenied('aware time required')
    utc = now.astimezone(timezone.utc)
    # A signed identity assertion alone does not authorize arbitrary retrieval:
    # the selected source must also be on the delegation allowlist.
    if not isinstance(source_id, str) or source_id not in scope.allowed_sources:
        raise ScopeDenied('source not delegated')
    if scope.purpose != 'review_replacement_complaint' or int(utc.timestamp()) >= scope.expires_at:
        raise ScopeDenied('scope expired or wrong purpose')
    # The tenant/case restriction comes from VerifiedScope (E1 verifier output),
    # not from text supplied by the adviser or the retrieved narrative.
    record = catalog.get(scope.tenant_id, scope.case_id, source_id)
    # Compare trusted fixture timestamps, not model-authored claims of freshness.
    # Negative age is future-dated evidence, not magically newer authority.
    age = (utc - record.observed_at.astimezone(timezone.utc)).total_seconds()
    if age < 0 or age > MAX_AGE_SECONDS:
        raise ScopeDenied('source observation outside freshness window')
    if record.classification != 'CASE_RESTRICTED':
        raise ScopeDenied('unsupported classification')
    # A provenance label travels with advice; it never turns context into
    # policy, payment approval, or proof of settlement.
    return ScopedEvidence(record, utc, scope.subject, scope.purpose,
                          provenance='fixture-catalog/v1;untrusted-for-E5')
