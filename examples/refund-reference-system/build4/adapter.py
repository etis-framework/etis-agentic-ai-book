"""E6/C07 fixture adapter and independent mock E8 truth database.

The provider has a unique operation key and a status query, but no real payment
connection. An injected lost acknowledgment happens AFTER committing the effect.
"""
from contextlib import contextmanager, closing
from pathlib import Path
import sqlite3
from provider_contracts import (Capabilities, ContractViolation, Outcome,
                                ProviderConflict, ProviderObservation,
                                ProviderUnavailable, RefundCommand, PROVIDER_VERSION)


class SQLiteFixtureProvider:
    """Isolated simulated provider account; never available to advisory code."""

    capabilities = Capabilities()

    def __init__(self, database: Path):
        self.database = database
        self.capabilities.validate()

    @contextmanager
    def _connect(self):
        self.database.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        db = sqlite3.connect(self.database, timeout=2.0, isolation_level='IMMEDIATE')
        try:
            db.execute('PRAGMA busy_timeout=2000')
            db.execute('''CREATE TABLE IF NOT EXISTS provider_refunds (
              operation_id TEXT PRIMARY KEY, case_id TEXT NOT NULL,
              tenant_id TEXT NOT NULL, amount_cents INTEGER NOT NULL,
              currency TEXT NOT NULL, provider_reference TEXT NOT NULL,
              status TEXT NOT NULL, contract_version TEXT NOT NULL)''')
            with db:
                yield db
        finally:
            db.close()

    @staticmethod
    def _confirmed(operation: RefundCommand, source: str):
        result = ProviderObservation(Outcome.CONFIRMED, operation.operation_id,
            operation.amount_cents, 'MOCK-' + operation.operation_id, source, PROVIDER_VERSION)
        result.validate()
        return result

    # The provider's PRIMARY KEY models scoped idempotency for this one
    # fictional SQLite account. Real processors require a documented scope,
    # retention period, conflict behavior, and authoritative status API.
    def send(self, command: RefundCommand, *, lose_ack: bool = False) -> ProviderObservation:
        command.validate()
        if type(lose_ack) is not bool:
            raise ContractViolation('invalid failure injection')
        with self._connect() as db:
            db.execute('''INSERT OR IGNORE INTO provider_refunds VALUES (?,?,?,?,?,?,?,?)''',
                (command.operation_id, command.case_id, command.tenant_id,
                 command.amount_cents, command.currency, 'MOCK-' + command.operation_id,
                 'CONFIRMED', PROVIDER_VERSION))
            actual = db.execute('SELECT case_id,tenant_id,amount_cents,currency,provider_reference,status,contract_version FROM provider_refunds WHERE operation_id=?',
                                (command.operation_id,)).fetchone()
            if actual != (command.case_id, command.tenant_id, command.amount_cents,
                          command.currency, 'MOCK-' + command.operation_id, 'CONFIRMED', PROVIDER_VERSION):
                raise ProviderConflict('same provider key has contradictory immutable attributes')
        # The transaction has committed when this fault is injected. The caller
        # must treat the missing reply as UNKNOWN, not as a failed payment or
        # permission to retry under another operation ID.
        if lose_ack:
            raise ProviderUnavailable('acknowledgment lost after potential effect; lookup required')
        return self._confirmed(command, 'provider-commit')

    # This is a read-only inquiry into mock E8 business truth. NOT_FOUND is
    # ambiguous evidence, not proof the earlier request had no effect.
    def lookup(self, command: RefundCommand) -> ProviderObservation:
        command.validate()
        # An absent mock store is a fixture-only NOT_FOUND observation, not
        # evidence that the earlier effect failed. Never initialize E8 on C08.
        actual = None
        if self.database.exists():
            with closing(sqlite3.connect(self.database.resolve().as_uri()+'?mode=ro',
                                         uri=True, timeout=2.0)) as db:
                db.execute('PRAGMA query_only=ON')
                actual = db.execute('SELECT case_id,tenant_id,amount_cents,currency,provider_reference,status,contract_version FROM provider_refunds WHERE operation_id=?',
                                    (command.operation_id,)).fetchone()
        if actual is None:
            observation = ProviderObservation(Outcome.NOT_FOUND, command.operation_id,
                None, None, 'provider-status-query', PROVIDER_VERSION)
            observation.validate()
            return observation
        if actual != (command.case_id, command.tenant_id, command.amount_cents,
                      command.currency, 'MOCK-' + command.operation_id, 'CONFIRMED', PROVIDER_VERSION):
            raise ProviderConflict('provider status inconsistent with authorized operation')
        return self._confirmed(command, 'provider-status-query')
