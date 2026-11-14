"""Build 4 E6/C07 provider contract: explicit capabilities, typed effects and observations.

Only integer minor currency units and one stable operation ID are accepted. This
is a simulated provider, not a guarantee about an actual payment network.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Protocol

CASE = 'CASE-204'
TENANT = 'retailer_a'
OPERATION = 'RF-1042'
AMOUNT_CENTS = 50_000
PROVIDER_VERSION = 'etis-fixture-provider-v1'


class ContractViolation(ValueError):
    """Caller input or provider response violates an immutable boundary."""


class ProviderUnavailable(RuntimeError):
    """No authoritative response; may have applied the effect."""


class ProviderConflict(RuntimeError):
    """A stable operation ID maps to contradictory provider evidence."""


class Outcome(Enum):
    CONFIRMED = 'CONFIRMED'
    REJECTED = 'REJECTED'
    NOT_FOUND = 'NOT_FOUND'
    UNKNOWN = 'UNKNOWN'


@dataclass(frozen=True)
class Capabilities:
    """A measured/pinned adapter contract, not a discovery-based promise."""
    version: str = PROVIDER_VERSION
    supports_idempotency: bool = True
    supports_lookup: bool = True
    stable_key_scope: str = 'provider-account'
    retention_seconds: int = 86_400

    def validate(self) -> None:
        if (self.version != PROVIDER_VERSION or
            type(self.supports_idempotency) is not bool or
            type(self.supports_lookup) is not bool or
            type(self.stable_key_scope) is not str or
            self.stable_key_scope != 'provider-account' or
            type(self.retention_seconds) is not int or
            self.retention_seconds < 86_400):
            raise ContractViolation('provider capabilities incompatible with Build 4')


@dataclass(frozen=True)
class RefundCommand:
    case_id: str = CASE
    tenant_id: str = TENANT
    operation_id: str = OPERATION
    amount_cents: int = AMOUNT_CENTS
    currency: str = 'USD'

    def validate(self) -> None:
        if (self.case_id != CASE or self.tenant_id != TENANT or
            self.operation_id != OPERATION or
            type(self.amount_cents) is not int or self.amount_cents != AMOUNT_CENTS or
            self.currency != 'USD'):
            raise ContractViolation('provider command violates fixed case, amount or currency')


@dataclass(frozen=True)
class ProviderObservation:
    """Result with explicit source; an absent record is not proof of no effect."""
    outcome: Outcome
    operation_id: str
    amount_cents: int | None
    provider_reference: str | None
    source: str
    contract_version: str

    def validate(self) -> None:
        if (not isinstance(self.outcome, Outcome) or self.operation_id != OPERATION or
            self.contract_version != PROVIDER_VERSION or
            self.source not in {'provider-commit', 'provider-status-query'}):
            raise ContractViolation('invalid provider observation metadata')
        if self.outcome == Outcome.CONFIRMED:
            if (type(self.amount_cents) is not int or self.amount_cents != AMOUNT_CENTS or
                not isinstance(self.provider_reference, str) or
                self.provider_reference != 'MOCK-' + OPERATION):
                raise ContractViolation('confirmed effect lacks matching provider proof')
        elif self.amount_cents is not None or self.provider_reference is not None:
            raise ContractViolation('non-confirmed observation carries unsupported effect proof')


class ProviderPort(Protocol):
    """Only the trusted E6 adapter side implements this protocol."""
    capabilities: Capabilities
    def send(self, command: RefundCommand, *, lose_ack: bool = False) -> ProviderObservation: ...
    def lookup(self, command: RefundCommand) -> ProviderObservation: ...
