# Chapter 28 — failure and recovery decision cases

This directory is a **separate pure educational fixture**, not Build 6, a payment client or a newly granted E5 recovery service. Run from the repository root:

```bash
python3 -m unittest discover -s examples/refund-reference-system/reliability -p 'test_*.py' -v
```

`recovery_cases.py` receives explicit, validated `Snapshot` values and classifies matching simulated E8 confirmations, ambiguous `NOT_FOUND`, outages and conflicts. `test_recovery_cases.py` exercises post-effect lost acknowledgment, E2 intent before E5 IPC, absent E7 operation, wrong proof, invalid types and forced escalation. No fixture action dispatches a refund, signs an approval, queries a real provider or updates E7. A decision of `CONFIRM` **does not** authorize E7 mutation in any production application: E5 recovery identity, proof provenance, amount/currency matching and finality must be evaluated independently. `NOT_FOUND` is not `FAILED`.

## Guided recovery decision lab

Start with `recovery_cases.py:Snapshot.validate` and `decide`. Then read `test_recovery_cases.py:RecoveryTests.base` and run the suite above. For each case, distinguish what the mock provider claims from what the local workflow actually knows:

| Simulated evidence | Expected `RecoveryDecision` | What the learner should conclude |
|---|---|---|
| Matching provider `CONFIRMED`, durable intent and matching CASE-204/RF-1042 proof | `CONFIRM` | An educational classification of trusted-looking evidence; production E5 must still validate the full proof before any state change |
| Provider `NOT_FOUND` after possible dispatch | `ESCALATE` | Absence of a record is **not** evidence that a payment failed or safe retry permission |
| Provider `UNAVAILABLE` | `INQUIRE` | Preserve uncertainty and investigate without issuing another effect |
| Conflicting case or operation proof | `ESCALATE` | Reject mismatched evidence instead of rewriting local truth |
| No durable intent or E7 operation | `ESCALATE` | Recovery must not create a new operation or bypass normal admission |

Follow `test_lost_ack_confirmation_matches_original_operation`, `test_not_found_never_declares_failure`, and `test_wrong_operation_proof_escalates` in that order. Then compare with the executable Build 4 `RefundWorkflow.reconcile` path: this Chapter 28 helper **classifies** a snapshot; Build 4 performs an independently authorized fixture status query and records an observation.

**Defend three decisions:** (1) Why is `NOT_FOUND` not `FAILED`? (2) Why does the matching operation ID matter even when the amount appears correct? (3) Which independent checks would be needed before updating E7 in a real enterprise workflow?

## Boundary and evidence

Use Build 4's tested `workflow.py`, `adapter.py`, `ledger.py` and Build 5's tested `coordinator.py` and `runner.py` for the executed local E5/E7/E8 demonstration; the pure Chapter 28 decision aid is intentionally not wired into these services. All provider behavior is simulated. See Chapter 28 Table 28.2 and `IMPLEMENTATION_EVIDENCE_MAP.md` for implemented versus specified boundaries. Existing Builds 0–5 retain their checked-in `architecture.svg` diagrams; this directory introduces **no additional build architecture**.
