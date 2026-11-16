"""Bounded E2 runner: delegates all financial authority and effects to Build 4.

A lost response is UNKNOWN. Recovery is status-only; the runner has no E6
adapter import, E7 provider write, grant issuer, or route to re-execute.
"""
from pathlib import Path
from typing import Callable, Mapping, Any
from coordinator import CASE, OPERATION, DurableCoordinator, Ownership

class RunnerUnavailable(RuntimeError):
    """Request to E5 was not observed; payment effect may still have occurred."""

class BoundedRunner:
    def __init__(self, coordinator: DurableCoordinator,
                 e5_request: Callable[[str], Mapping[str, Any]]):
        self.coordinator=coordinator
        self.e5_request=e5_request

    def step(self, owner: Ownership, *, now: int) -> str:
        # E2 fences its own state writes, but this owner epoch is NOT verified
        # inside Build 4 E5. Do not infer production end-to-end fencing.
        action=self.coordinator.choose(owner,now=now)
        if action=='none':
            return self.coordinator.state()['phase']
        if action=='execute':
            # Must be committed before any external E5 IPC; if we crash here,
            # another worker can only reconcile/escalate, never send anew.
            self.coordinator.mark_execute_intent(owner,now=now)
        try:
            response=self.e5_request(action)
            if type(response) is not dict or response.get('status') not in ('CONFIRMED','DENIED','UNKNOWN'):
                raise RunnerUnavailable('untrusted or unrecognized E5 response')
            status=response['status']
            if status=='CONFIRMED':
                proof=response.get('data')
                if (type(proof) is not dict or
                    proof != {'case_id':CASE,'operation_id':OPERATION}):
                    raise RunnerUnavailable('E5 confirmation lacks matching operation identity')
        except (OSError,TimeoutError,RunnerUnavailable):
            status='UNKNOWN'
        # Stale owners may have initiated work but cannot commit stale findings;
        # the replacement worker must query E5/E8 via reconciliation.
        self.coordinator.observe(owner,now=now,action=action,outcome=status)
        return self.coordinator.state()['phase']
