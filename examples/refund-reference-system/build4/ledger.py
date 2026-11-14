"""E7/C06 durable local operation state: commit before provider dispatch.

This is a single-site SQLite educational ledger. It does not implement E2
multi-worker ownership fencing, distributed locking, or a durable outbox worker.
"""
from contextlib import contextmanager
from pathlib import Path
import sqlite3
from provider_contracts import RefundCommand, ContractViolation


class InvalidTransition(ValueError):
    """Operation already dispatched, incompatible or in an illegal state."""


class OperationalLedger:
    def __init__(self, database: Path):
        self.database = database

    @contextmanager
    def _connect(self):
        self.database.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        db = sqlite3.connect(self.database, timeout=2.0)
        db.execute('PRAGMA busy_timeout=2000')
        db.execute('''CREATE TABLE IF NOT EXISTS operations (
            operation_id TEXT PRIMARY KEY, case_id TEXT NOT NULL,
            tenant_id TEXT NOT NULL, amount_cents INTEGER NOT NULL,
            currency TEXT NOT NULL, status TEXT NOT NULL,
            observation TEXT NOT NULL, provider_reference TEXT)''')
        try:
            with db:
                yield db
        finally:
            db.close()

    def state(self, command: RefundCommand):
        command.validate()
        with self._connect() as db:
            row = db.execute('SELECT case_id,tenant_id,amount_cents,currency,status,observation,provider_reference FROM operations WHERE operation_id=?',
                             (command.operation_id,)).fetchone()
        if row and row[:4] != (command.case_id, command.tenant_id, command.amount_cents, command.currency):
            raise ContractViolation('durable operation identity reused with different immutable attributes')
        return row

    def prepare(self, command: RefundCommand):
        command.validate()
        with self._connect() as db:
            db.execute('''INSERT OR IGNORE INTO operations VALUES (?,?,?,?,?,?,?,?)''',
                (command.operation_id,command.case_id,command.tenant_id,
                 command.amount_cents,command.currency,'AUTHORIZED','grant verified',None))
        row=self.state(command)
        if row is None or row[4] != 'AUTHORIZED':
            raise InvalidTransition('preparation cannot reset an already claimed operation')

    def claim_dispatch(self, command: RefundCommand):
        with self._connect() as db:
            c=db.execute('''UPDATE operations SET status='DISPATCHED',observation='provider call may have begun'
                WHERE operation_id=? AND status='AUTHORIZED' ''',(command.operation_id,))
            if c.rowcount != 1:
                raise InvalidTransition('exactly one authorized dispatch claim required')

    def observe_unknown(self, command: RefundCommand, detail: str):
        if detail not in {'ack-lost','provider-unavailable','provider-conflict','infrastructure-uncertain'}:
            raise ValueError('unapproved diagnostic classification')
        with self._connect() as db:
            db.execute('''UPDATE operations SET status='UNKNOWN',observation=?
                WHERE operation_id=? AND status IN ('DISPATCHED','UNKNOWN','CONFIRMED')''',
                (detail,command.operation_id))

    def confirm(self, command: RefundCommand, provider_reference: str, *, source: str):
        if source not in {'provider-commit','provider-status-query'} or provider_reference != 'MOCK-'+command.operation_id:
            raise ContractViolation('cannot confirm without validated provider evidence')
        with self._connect() as db:
            c=db.execute('''UPDATE operations SET status='CONFIRMED',observation=?,provider_reference=?
                WHERE operation_id=? AND status IN ('DISPATCHED','UNKNOWN','CONFIRMED')''',
                (source,provider_reference,command.operation_id))
            if c.rowcount != 1:
                raise InvalidTransition('provider proof cannot authorize a new local operation')
