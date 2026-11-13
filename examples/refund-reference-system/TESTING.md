# Verification and evidence guide

This is a **teaching verification plan**, not a production test attestation. The executable cases are in `build0/test_refund.py`. Run them from the repository root with:

```sh
python3 -m unittest discover -s examples/refund-reference-system/build0 -p 'test_*.py' -v
```

## Evidence matrix — Build 0

| Scenario | Expected E7 observation | Expected simulated E8 truth | Security / operations lesson |
|---|---|---|---|
| Authorized CASE-204 / $500 | AUTHORIZED → CONFIRMED | One RF-1042 CONFIRMED | Fixed trusted policy gates precede effects |
| Wrong tenant, principal, case, amount, policy or approval | No operation | No refund | A caller-supplied proposal cannot authorize itself |
| Repeated preparation | Same RF-1042, immutable fields | Unchanged | Duplicate case creation is not a second financial intent |
| Repeated dispatch | Rejected once state is no longer AUTHORIZED | Only one RF-1042 | No blind retry after dispatch |
| Lost acknowledgment after mock provider commit | UNKNOWN | One RF-1042 CONFIRMED | Local uncertainty is not payment failure |
| Reconciliation of lost acknowledgment | CONFIRMED after matching lookup | Original confirmed RF-1042 | Provider observation, not model text, resolves outcome |
| No provider row after an uncertain dispatch | DISPATCHED, unresolved | No row | Missing evidence is not permission to retry |
| Conflicting provider amount | UNKNOWN, unresolved | Contradictory record | Do not manufacture a confirmed result |
| New process reads existing SQLite stores | Existing state retained | Existing truth retained | Recovery relies on durable files, not process memory |
| Unknown operation cannot be reconciled or dispatched | No operation | No row | The effect path requires prior authorized intent |

**What these tests cannot prove:** process isolation, real authentication, human approval, concurrent E2 fencing, secure E5-to-E6 topology, provider idempotency retention, payment settlement, network fault distributions, privacy compliance, or the complete C01–C09 contracts. These require separate implementations, external agreements, and risk-proportionate assurance. A green test demonstrates only its declared fixture result.

## Reviewer workflow

Read Chapter 22 and `ARCHITECTURE.md`; run the tests; reproduce the CLI sequence in `build0/README.md`; inspect the E7 and mock E8 tables independently; then record which guarantees remain assumptions. Never point these examples at a real payment API.
