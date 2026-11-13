"""ETIS Build 0: deterministic CASE-204 teaching fixture, Python standard library only.

Two SQLite databases deliberately distinguish local E7 operational knowledge from
simulated external E8 provider truth. This is NOT a payment integration.
"""
# Conceptual organization (kept in one readable module for a first-time reader):
#   1. Fixture identifiers and state storage (E7 / mock E8)
#   2. Independent authorization and durable intent (E5 / E7)
#   3. Isolated mock effect dispatch (E6 → simulated E8)
#   4. Reconciliation and reader-facing CLI (E7 observation of E8)
# These logical boundaries are NOT separate security processes. Part IV adds the
# missing isolation and contracts progressively; importing these functions
# directly is never a production authority boundary.
import argparse
import json
import sqlite3
from pathlib import Path

CASE = 'CASE-204'
OPERATION = 'RF-1042'
AMOUNT_CENTS = 50000
TENANT = 'retailer_a'
PRINCIPAL = 'authenticated_customer_204'
POLICY = 'refund-policy-v12'

class Denied(Exception):
    """Refused by the fixture policy or workflow, not a provider-result claim."""
    pass


def connection(path):
    """Open one local SQLite file; this is not a cross-database transaction."""
    db = sqlite3.connect(str(path))
    db.execute('PRAGMA busy_timeout = 3000')
    return db


def initialize(local, provider):
    """Make independent E7 and mock E8 stores; no cross-store atomicity exists."""
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


def authorize(*, case_id, tenant, principal, amount_cents, refundable_cents,
              approved, policy_version):
    """E5: fixed independent policy; inputs are trusted fixture values, not advisory text."""
    if (case_id != CASE or tenant != TENANT or principal != PRINCIPAL or
            amount_cents != AMOUNT_CENTS or refundable_cents < amount_cents or
            not approved or policy_version != POLICY):
        raise Denied('E5: refund authorization denied')


def prepare(local, *, case_id=CASE, tenant=TENANT, principal=PRINCIPAL,
            amount_cents=AMOUNT_CENTS, refundable_cents=AMOUNT_CENTS,
            approved=True, policy_version=POLICY):
    """Authorize before recording intent, with immutable operation identity."""
    authorize(case_id=case_id, tenant=tenant, principal=principal,
              amount_cents=amount_cents, refundable_cents=refundable_cents,
              approved=approved, policy_version=policy_version)
    with connection(local) as db:
        db.execute('''INSERT OR IGNORE INTO operations
          (operation_id,case_id,tenant,principal,amount_cents,policy_version,status)
          VALUES (?,?,?,?,?,?,?)''',
          (OPERATION, CASE, TENANT, PRINCIPAL, AMOUNT_CENTS, POLICY, 'AUTHORIZED'))
        row = db.execute('SELECT case_id,tenant,principal,amount_cents,policy_version FROM operations WHERE operation_id=?',
                         (OPERATION,)).fetchone()
        if row != (CASE, TENANT, PRINCIPAL, AMOUNT_CENTS, POLICY):
            raise Denied('immutable refund operation conflict')
    return OPERATION


def status(local):
    """Report E7 observation only; local state never proves a provider effect."""
    with connection(local) as db:
        row = db.execute('SELECT status,observation FROM operations WHERE operation_id=?',
                         (OPERATION,)).fetchone()
    return row


def dispatch(local, provider, *, lose_ack=False):
    """E6 simulated provider; never resubmit an UNKNOWN operation."""
    with connection(local) as db:
        row = db.execute('SELECT status,amount_cents FROM operations WHERE operation_id=?',
                         (OPERATION,)).fetchone()
        if not row:
            raise Denied('no authorized durable intent')
        state, cents = row
        if state != 'AUTHORIZED':
            raise Denied(f'dispatch prohibited from {state}; reconcile first')
        db.execute("UPDATE operations SET status='DISPATCHED' WHERE operation_id=? AND status='AUTHORIZED'", (OPERATION,))
    # The simulated E8 commit is independent of E7. If the process stops here,
    # local DISPATCHED may coexist with a completed mock-provider refund.
    try:
        with connection(provider) as db:
            db.execute('''INSERT OR IGNORE INTO refunds(operation_id,case_id,amount_cents,status)
                VALUES (?,?,?,?)''', (OPERATION, CASE, cents, 'CONFIRMED'))
            actual = db.execute('SELECT case_id,amount_cents,status FROM refunds WHERE operation_id=?',
                                (OPERATION,)).fetchone()
            if actual != (CASE, cents, 'CONFIRMED'):
                raise Denied('provider operation conflict')
        if lose_ack:
            raise TimeoutError('simulated lost acknowledgment AFTER provider commit')
    except TimeoutError:
        with connection(local) as db:
            db.execute("UPDATE operations SET status='UNKNOWN',observation='acknowledgment lost' WHERE operation_id=?", (OPERATION,))
        return 'UNKNOWN'
    # If the process crashes before this local update, the persisted DISPATCHED
    # state is unresolved and may only be reconciled, not dispatched again.
    with connection(local) as db:
        db.execute("UPDATE operations SET status='CONFIRMED',observation='provider confirmed' WHERE operation_id=?", (OPERATION,))
    return 'CONFIRMED'


def reconcile(local, provider):
    """Read authoritative provider evidence; absence is not proof of failure."""
    with connection(local) as db:
        row = db.execute('SELECT status,amount_cents FROM operations WHERE operation_id=?',
                         (OPERATION,)).fetchone()
    if not row:
        raise Denied('no durable intent')
    if row[0] not in {'UNKNOWN','DISPATCHED','CONFIRMED'}:
        raise Denied('reconciliation is not a dispatch replacement')
    with connection(provider) as db:
        provider_row = db.execute('SELECT case_id,amount_cents,status FROM refunds WHERE operation_id=?',
                                  (OPERATION,)).fetchone()
    # Confirm only a matching original case, amount, and stable operation ID.
    if provider_row == (CASE, row[1], 'CONFIRMED'):
        with connection(local) as db:
            db.execute("UPDATE operations SET status='CONFIRMED',observation='provider status lookup' WHERE operation_id=?", (OPERATION,))
        return 'CONFIRMED'
    # An inconsistent or missing record is escalated; it is never interpreted
    # as permission to issue another $500 refund.
    return 'UNKNOWN'


def main():
    parser = argparse.ArgumentParser(description='ETIS Build 0 local simulator')
    parser.add_argument('action', choices=['prepare','dispatch','dispatch-lost-ack','reconcile','status'])
    parser.add_argument('--directory', type=Path, default=Path('.build0-demo'))
    a = parser.parse_args()
    a.directory.mkdir(parents=True, exist_ok=True)
    local = a.directory/'operations.sqlite3'
    provider = a.directory/'provider.sqlite3'
    initialize(local, provider)
    if a.action == 'prepare':
        result = prepare(local)
    elif a.action in {'dispatch','dispatch-lost-ack'}:
        result = dispatch(local, provider, lose_ack=a.action.endswith('lost-ack'))
    elif a.action == 'reconcile':
        result = reconcile(local, provider)
    else:
        result = status(local)
    print(json.dumps({'case': CASE,'operation': OPERATION,'result': result,'local': status(local)}))

if __name__ == '__main__':
    main()
