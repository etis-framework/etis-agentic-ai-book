"""Chapter 30 educational read-only incident observer for existing E2/E7 databases.

This module deliberately imports NO payment adapter, service client, grant issuer,
network stack or provider write API. Its decision is an operator work item, not
an E5 authorization or an external financial settlement assertion.

For teaching: compare independently committed E2 and E7 snapshots, then sort
synthetic redacted signal envelopes by a fixture sequence. Real clocks, audit
custody, provider proof and execution fencing are NOT represented here.
"""
from contextlib import closing
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import sqlite3

CASE = 'CASE-204'
OPERATION = 'RF-1042'
AMOUNT = 50_000


class IncidentInputError(ValueError):
    """An invalid fixture must not be silently converted to trustworthy evidence."""


class SignalKind(str, Enum):
    """Fixed alert taxonomy: no arbitrary text or secrets reach the output."""
    E7_UNKNOWN = 'E7_UNKNOWN'
    E8_UNAVAILABLE = 'E8_UNAVAILABLE'
    E8_CONFLICT = 'E8_CONFLICT'
    TELEMETRY_GAP = 'TELEMETRY_GAP'
    STALE_OWNER = 'STALE_OWNER'
    TOKEN_REVOKED = 'TOKEN_REVOKED'
    VERIFIER_UNAVAILABLE = 'VERIFIER_UNAVAILABLE'
    E5_DENIED = 'E5_DENIED'


class ProviderStatus(str, Enum):
    """An *operator-provided synthetic observation*, not a provider API reply."""
    CONFIRMED = 'CONFIRMED'
    NOT_FOUND = 'NOT_FOUND'
    UNAVAILABLE = 'UNAVAILABLE'
    CONFLICT = 'CONFLICT'


@dataclass(frozen=True)
class Signal:
    seq: int
    event_id: str
    kind: SignalKind
    # Explicitly no free-form payload. Untrusted details are never logged.

    def validate(self):
        if type(self.seq) is not int or self.seq < 1:
            raise IncidentInputError('invalid fixture event sequence')
        if type(self.event_id) is not str or not 1 <= len(self.event_id) <= 24 or not all(
                c.isascii() and (c.isalnum() or c in '-_') for c in self.event_id):
            raise IncidentInputError('invalid event identifier')
        if not isinstance(self.kind, SignalKind):
            raise IncidentInputError('signal taxonomy violation')


@dataclass(frozen=True)
class Finding:
    """Allowlisted, JSON-safe incident record without credentials or raw case data."""
    severity: str
    disposition: str
    next_role: str
    operation_id: str
    e7_status: str
    e2_phase: str
    e2_epoch: int
    signals: tuple[str, ...]
    event_gap: bool
    rationale: str
    allowed_action: str = 'READ_ONLY_RECONCILE_OR_ESCALATE'

    def as_record(self):
        """Fixed output fields; never serialize external objects or SQL payloads."""
        return {
            'severity': self.severity, 'disposition': self.disposition,
            'next_role': self.next_role, 'operation_id': self.operation_id,
            'e7_status': self.e7_status, 'e2_phase': self.e2_phase,
            'e2_epoch': self.e2_epoch, 'signals': list(self.signals),
            'event_gap': self.event_gap, 'rationale': self.rationale,
            'allowed_action': self.allowed_action,
        }


def _read_one(path: Path, query: str, args: tuple):
    """Open an existing file read-only; never create a DB on a missing path.

    mode=ro blocks SQL writes; query strings are fixed by this module, while
    identity values are bound parameters. This is NOT tamper-resistant custody.
    """
    if not isinstance(path, Path) or not path.is_file():
        raise IncidentInputError('required local evidence file unavailable')
    try:
        with closing(sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True,
                                        timeout=1.0)) as db:
            db.execute('PRAGMA query_only=ON')
            return db.execute(query, args).fetchone()
    except sqlite3.Error as exc:
        raise IncidentInputError('local evidence unavailable or invalid') from exc


def assess(e2_db: Path, e7_db: Path, *, provider: ProviderStatus,
           signals: tuple[Signal, ...], expected_epoch: int | None = None) -> Finding:
    """Read-only, fail-conservative operational recommendation.

    E8 status is caller-supplied simulated data. Even CONFIRMED does not grant
    E7 mutation or authorize a new C07 payment; an operator must verify E8
    identity, immutable attributes, provenance, finality and C08 access.
    """
    if not isinstance(provider, ProviderStatus) or type(signals) is not tuple:
        raise IncidentInputError('typed synthetic incident inputs required')
    if type(expected_epoch) is not int and expected_epoch is not None:
        raise IncidentInputError('invalid epoch')
    if expected_epoch is not None and expected_epoch < 0:
        raise IncidentInputError('invalid epoch')
    for signal in signals:
        if not isinstance(signal, Signal):
            raise IncidentInputError('unexpected event object')
        signal.validate()
    if len({s.event_id for s in signals}) != len(signals) or len({s.seq for s in signals}) != len(signals):
        raise IncidentInputError('duplicate event identity or sequence')
    ordered = sorted(signals, key=lambda s: s.seq)
    gap = (bool(ordered) and (
        ordered[0].seq != 1 or any(b.seq != a.seq + 1 for a, b in zip(ordered, ordered[1:]))))
    kinds = {s.kind for s in ordered}
    e2 = _read_one(e2_db, 'SELECT operation_id,phase,epoch FROM work WHERE case_id=?', (CASE,))
    e7 = _read_one(e7_db, 'SELECT case_id,tenant_id,amount_cents,currency,status FROM operations WHERE operation_id=?', (OPERATION,))
    if (e2 is None or e2[0] != OPERATION or type(e2[2]) is not int or
        e2[1] not in {'READY','EXECUTE_IN_FLIGHT','NEEDS_RECONCILIATION','CONFIRMED','DENIED','ESCALATED'} or
        e7 is None or e7[:4] != (CASE,'retailer_a',AMOUNT,'USD') or
        e7[4] not in {'AUTHORIZED','DISPATCHED','UNKNOWN','CONFIRMED'}):
        raise IncidentInputError('local records fail fixed-case contract')
    stale = expected_epoch is not None and expected_epoch != e2[2]
    compromise = (SignalKind.TOKEN_REVOKED in kinds or SignalKind.VERIFIER_UNAVAILABLE in kinds)
    conflict = provider == ProviderStatus.CONFLICT or SignalKind.E8_CONFLICT in kinds
    missing = gap or SignalKind.TELEMETRY_GAP in kinds
    if compromise:
        severity, disposition, role, reason = 'SEV1','QUARANTINE','security-incident-command','credential or verifier trust unavailable'
    elif stale or SignalKind.STALE_OWNER in kinds:
        severity, disposition, role, reason = 'SEV1','QUARANTINE','incident-command','current-owner execution fencing unproven'
    elif conflict:
        severity, disposition, role, reason = 'SEV1','ESCALATE','finance-and-incident-command','conflicting provider evidence'
    elif provider != ProviderStatus.CONFIRMED or e7[4] != 'CONFIRMED' or missing:
        severity, disposition, role, reason = 'SEV2','INQUIRE','reconciliation-operator','effect or evidence remains unresolved'
    else:
        # A local CONFIRMED + synthetic provider confirmation still requires
        # independent production evidence before real closure.
        severity, disposition, role, reason = 'SEV2','REVIEW','finance-owner','fixture observations require external verification'
    return Finding(severity, disposition, role, OPERATION, e7[4],e2[1],e2[2],
                   tuple(s.kind.value for s in ordered),missing,reason)
