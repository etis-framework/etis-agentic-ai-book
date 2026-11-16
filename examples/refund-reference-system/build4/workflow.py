"""Build 4 E5-authorized workflow across E7/C06, E6/C07 and mock E8/C08.

Policy and approvals must be verified *before* this class is called. This object
is created only inside the Build 4 E5 service; its public methods are not an
untrusted financial API. A new operation must never be created by reconcile().
"""
import sqlite3
from adapter import SQLiteFixtureProvider
from ledger import InvalidTransition, OperationalLedger
from provider_contracts import (Capabilities, ContractViolation, Outcome,
    ProviderConflict, ProviderUnavailable, RefundCommand)


class OutcomeUnknown(RuntimeError):
    """No safe claim of provider failure or success has been established."""


class RefundWorkflow:
    def __init__(self, ledger: OperationalLedger, provider: SQLiteFixtureProvider,
                 *, capabilities: Capabilities | None = None):
        self.ledger = ledger
        self.provider = provider
        caps = capabilities if capabilities is not None else provider.capabilities
        caps.validate()
        if not (caps.supports_idempotency and caps.supports_lookup):
            raise ContractViolation('required documented provider capabilities unavailable')

    def execute(self, command: RefundCommand, *, lose_ack: bool = False,
                outage_before_send: bool = False) -> str:
        command.validate()
        if type(lose_ack) is not bool or type(outage_before_send) is not bool:
            raise ContractViolation('invalid simulation flags')
        # Two durable local transitions precede the possible external effect.
        # Once DISPATCHED is claimed, a crash may leave its outcome unknown;
        # retrying under a fresh operation identity risks a duplicate refund.
        self.ledger.prepare(command)
        self.ledger.claim_dispatch(command)  # committed before E6 call
        try:
            if outage_before_send:
                raise ProviderUnavailable('injected outage after durable dispatch claim')
            observation=self.provider.send(command,lose_ack=lose_ack)
            observation.validate()
            if observation.outcome != Outcome.CONFIRMED:
                raise OutcomeUnknown('send did not establish a confirmed effect')
            self.ledger.confirm(command,observation.provider_reference,source=observation.source)
            return 'CONFIRMED'
        except (ProviderUnavailable,ProviderConflict,OutcomeUnknown) as exc:
            self.ledger.observe_unknown(command,'provider-conflict' if isinstance(exc,ProviderConflict)
                else 'provider-unavailable' if outage_before_send else 'ack-lost')
            raise OutcomeUnknown('external effect unresolved; reconcile, never blindly resend') from exc
        except (OSError,ValueError,sqlite3.Error) as exc:
            self.ledger.observe_unknown(command,'infrastructure-uncertain')
            raise OutcomeUnknown('storage/adapter fault after dispatch claim') from exc

    def reconcile(self, command: RefundCommand) -> str:
        command.validate()
        # Reconciliation is for an *existing dispatched operation* only.
        # It must never initialize a new refund or call provider.send().
        row=self.ledger.state(command)
        if row is None or row[4] not in {'DISPATCHED','UNKNOWN','CONFIRMED'}:
            raise InvalidTransition('no previously dispatched operation to reconcile')
        # No send(), no prepare(), no claim_dispatch(): reconciliation is read-only E8.
        try:
            observation=self.provider.lookup(command)
            observation.validate()
        except (ProviderConflict,ProviderUnavailable,ContractViolation,OSError,ValueError,sqlite3.Error) as exc:
            self.ledger.observe_unknown(command,'provider-conflict' if isinstance(exc,ProviderConflict)
                else 'infrastructure-uncertain')
            raise OutcomeUnknown('provider lookup cannot prove outcome') from exc
        if observation.outcome != Outcome.CONFIRMED:
            # NOT_FOUND is not proof that a prior request did not execute.
            self.ledger.observe_unknown(command,'provider-unavailable')
            raise OutcomeUnknown('missing/ambiguous provider record; no redispatch')
        self.ledger.confirm(command,observation.provider_reference,source=observation.source)
        return 'CONFIRMED'
