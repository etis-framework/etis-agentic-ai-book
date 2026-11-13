"""Build 0: inspectable deterministic refund fixture for CASE-204.

Run locally with Python's standard library. E7 and mock E8 intentionally occupy
independent SQLite files: there is no distributed transaction or real payment.

The code contains *logical* boundaries, not independently protected processes.
Never treat a Python import or a fixture Boolean as production authorization.
"""

import argparse
from contextlib import contextmanager
import json
from pathlib import Path
import sqlite3
import sys
from typing import Iterator

CASE = 'CASE-204'
OPERATION = 'RF-1042'
AMOUNT_CENTS = 50_000
TENANT = 'retailer_a'
PRINCIPAL = 'authenticated_customer_204'
POLICY = 'refund-policy-v12'


class Denied(Exception):
    """Policy denial or prohibited workflow transition; no new payment effect."""


class ProviderUnavailable(Exception):
    """Mock transport/provider failure; outcome must be investigated, not retried."""


@contextmanager
def connection(path: Path) -> Iterator[sqlite3.Connection]:
    """Own connection lifetime and commit/rollback for exactly one SQLite file.

    Production replacement: dedicated E7 store with scoped credentials, migration,
    connection lifecycle management and deployment-appropriate durability policy.
    """
    db = sqlite3.connect(str(path), timeout=3)
    try:
        db.execute('PRAGMA busy_timeout = 3000')
        with db:
            yield db
    finally:
        db.close()


def initialize(local: Path, provider: Path) -> None:
    """Create independent E7 and mock E8 stores, not an atomic two-store unit."""
    if local.resolve() == provider.resolve():
        raise ValueError('E7 and mock E8 must use separate database paths')
    for name in (local, provider):
        name.parent.mkdir(parents=True, exist_ok=True)
    with connection(local) as db:
        db.execute('''CREATE TABLE IF NOT EXISTS operations (
          operation_id TEXT PRIMARY KEY, case_id TEXT NOT NULL UNIQUE,
          tenant TEXT NOT NULL, principal TEXT NOT NULL, amount_cents INTEGER NOT NULL,
          policy_version TEXT NOT NULL, status TEXT NOT NULL,
          observation TEXT NOT NULL DEFAULT '')''')
    with connection(provider) as db:
        db.execute('''CREATE TABLE IF NOT EXISTS refunds (
          operation_id TEXT PRIMARY KEY, case_id TEXT NOT NULL UNIQUE,
          amount_cents INTEGER NOT NULL, status TEXT NOT NULL)''')


def authorize(*, case_id: str, tenant: str, principal: str, amount_cents: int,
              refundable_cents: int, approved: bool, policy_version: str) -> None:
    """E5 fixture rule. These inputs are supplied by *trusted fixture code* only.

    IMPORTANT: validating these fields does not authenticate a caller. Build 3
    must independently obtain authorization from protected identity and policy
    sources, without letting E3/C04 advisory content issue an RF-1042 operation.
    """
    if (case_id != CASE or tenant != TENANT or principal != PRINCIPAL or
            type(amount_cents) is not int or amount_cents != AMOUNT_CENTS or
            type(refundable_cents) is not int or refundable_cents < amount_cents or
            type(approved) is not bool or not approved or policy_version != POLICY):
        raise Denied('E5: refund authorization denied')


def prepare(local: Path, *, case_id: str = CASE, tenant: str = TENANT,
            principal: str = PRINCIPAL, amount_cents: int = AMOUNT_CENTS,
            refundable_cents: int = AMOUNT_CENTS, approved: bool = True,
            policy_version: str = POLICY) -> str:
    """Authorize a fixed request, then persist an immutable E7 operation identity.

    Repeated identical preparation is an idempotent read of the same intent.
    It never mints another payment ID. This remains only a single-case fixture.
    """
    authorize(case_id=case_id, tenant=tenant, principal=principal,
              amount_cents=amount_cents, refundable_cents=refundable_cents,
              approved=approved, policy_version=policy_version)
    with connection(local) as db:
        db.execute('''INSERT OR IGNORE INTO operations
          (operation_id,case_id,tenant,principal,amount_cents,policy_version,status)
          VALUES (?,?,?,?,?,?,?)''',
          (OPERATION, CASE, TENANT, PRINCIPAL, AMOUNT_CENTS, POLICY, 'AUTHORIZED'))
        row = db.execute('''SELECT case_id,tenant,principal,amount_cents,
                              policy_version FROM operations WHERE operation_id=?''',
                         (OPERATION,)).fetchone()
        if row != (CASE, TENANT, PRINCIPAL, AMOUNT_CENTS, POLICY):
            raise Denied('immutable refund operation conflict')
    return OPERATION


def status(local: Path):
    """Read E7's local observation, never a claim about actual settlement."""
    with connection(local) as db:
        return db.execute('SELECT status,observation FROM operations WHERE operation_id=?',
                          (OPERATION,)).fetchone()


def dispatch(local: Path, provider: Path, *, lose_ack: bool = False,
             fail_before_provider_commit: bool = False) -> str:
    """Claim one E7 dispatch and invoke E6 -> mock E8 at most once.

    Atomic *local* compare-and-set prevents two callers winning AUTHORIZED.
    There is no claim of E2 lease fencing or a cross-database transaction.
    After claiming DISPATCHED, any uncertain effect requires reconciliation.
    """
    with connection(local) as db:
        # SQLite serializes the write; the affected-row count is the authority
        # for whether this caller may proceed to the simulated effect.
        cursor = db.execute('''UPDATE operations SET status='DISPATCHED'
            WHERE operation_id=? AND status='AUTHORIZED' ''', (OPERATION,))
        if cursor.rowcount != 1:
            raise Denied('dispatch requires exactly one AUTHORIZED durable intent')
        cents = db.execute('SELECT amount_cents FROM operations WHERE operation_id=?',
                           (OPERATION,)).fetchone()[0]
    # E7's transaction is committed before the external mock-provider call.
    # A crash, I/O error or provider outage from here is NOT authorization to
    # retry. E7 will remain DISPATCHED (or UNKNOWN after a known lost ack).
    if fail_before_provider_commit:
        raise ProviderUnavailable('simulated provider unavailable; reconcile before any retry')
    with connection(provider) as db:
        db.execute('''INSERT OR IGNORE INTO refunds(operation_id,case_id,amount_cents,status)
            VALUES (?,?,?,?)''', (OPERATION, CASE, cents, 'CONFIRMED'))
        actual = db.execute('SELECT case_id,amount_cents,status FROM refunds WHERE operation_id=?',
                            (OPERATION,)).fetchone()
        if actual != (CASE, cents, 'CONFIRMED'):
            raise Denied('conflicting mock provider record; escalate')
    if lose_ack:
        with connection(local) as db:
            db.execute('''UPDATE operations SET status='UNKNOWN',
                observation='acknowledgment lost' WHERE operation_id=?
                AND status='DISPATCHED' ''', (OPERATION,))
        return 'UNKNOWN'
    with connection(local) as db:
        db.execute('''UPDATE operations SET status='CONFIRMED',
            observation='provider confirmed' WHERE operation_id=?
            AND status='DISPATCHED' ''', (OPERATION,))
    return 'CONFIRMED'


def reconcile(local: Path, provider: Path) -> str:
    """Read mock E8 status; never create a new financial effect or identity."""
    with connection(local) as db:
        row = db.execute('SELECT status,amount_cents FROM operations WHERE operation_id=?',
                         (OPERATION,)).fetchone()
    if not row:
        raise Denied('no durable intent')
    if row[0] not in {'UNKNOWN', 'DISPATCHED', 'CONFIRMED'}:
        raise Denied('reconciliation is not a dispatch replacement')
    with connection(provider) as db:
        actual = db.execute('SELECT case_id,amount_cents,status FROM refunds WHERE operation_id=?',
                            (OPERATION,)).fetchone()
    if actual != (CASE, row[1], 'CONFIRMED'):
        # Neither a missing nor a contradictory record permits a second call.
        # A future service will record a durable review/escalation event here.
        return 'UNKNOWN'
    with connection(local) as db:
        db.execute('''UPDATE operations SET status='CONFIRMED',
            observation='provider status lookup' WHERE operation_id=?
            AND status IN ('UNKNOWN','DISPATCHED','CONFIRMED')''', (OPERATION,))
    return 'CONFIRMED'


def main() -> int:
    """Run one local teaching operation; emit bounded errors without a traceback."""
    parser = argparse.ArgumentParser(description='ETIS Build 0 local simulator')
    parser.add_argument('action', choices=['prepare', 'dispatch', 'dispatch-lost-ack',
                                           'dispatch-provider-unavailable', 'reconcile', 'status'])
    parser.add_argument('--directory', type=Path, default=Path('.build0-demo'))
    args = parser.parse_args()
    local = args.directory / 'operations.sqlite3'
    provider = args.directory / 'provider.sqlite3'
    try:
        initialize(local, provider)
        if args.action == 'prepare':
            result = prepare(local)
        elif args.action.startswith('dispatch'):
            result = dispatch(local, provider,
                              lose_ack=args.action == 'dispatch-lost-ack',
                              fail_before_provider_commit=args.action == 'dispatch-provider-unavailable')
        elif args.action == 'reconcile':
            result = reconcile(local, provider)
        else:
            result = status(local)
        print(json.dumps({'case': CASE, 'operation': OPERATION,
                          'result': result, 'local': status(local)}))
        return 0
    except (Denied, ProviderUnavailable, sqlite3.Error, OSError, ValueError) as exc:
        # Production CLI/API: structured event, correlation ID, safe message,
        # distinct policy/availability status, and telemetry without PII.
        kind = ('DENIED' if isinstance(exc, Denied) else
                'PROVIDER_UNAVAILABLE' if isinstance(exc, ProviderUnavailable) else
                'STORAGE_OR_INPUT_ERROR')
        print(json.dumps({'error': kind, 'detail': str(exc),
                          'operation': OPERATION, 'action': args.action}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
