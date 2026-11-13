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
| Two concurrent local dispatch callers | Exactly one wins `AUTHORIZED → DISPATCHED` | One RF-1042 only | Local compare-and-set is atomic, not a substitute for E2 fencing |
| Simulated provider unavailable before commit | DISPATCHED; unresolved | No row | Dependency failure cannot trigger automatic new dispatch |
| Boolean, float or string monetary input | No operation | No row | Validate value **and** type, never coerce monetary input silently |
| Contradictory preexisting provider operation | DISPATCHED; unresolved | Contradictory row remains | Do not accept a conflicting observation as confirmation |
| CLI policy denial | JSON error on stderr, exit status 2 | No row | Expected failures should be diagnosable without a Python traceback |

**What these tests cannot prove:** process isolation, real authentication, human approval, concurrent E2 fencing, secure E5-to-E6 topology, provider idempotency retention, payment settlement, network fault distributions, privacy compliance, or the complete C01–C09 contracts. These require separate implementations, external agreements, and risk-proportionate assurance. A green test demonstrates only its declared fixture result.

## Reviewer workflow

Read Chapter 22 and `ARCHITECTURE.md`; run the tests; reproduce the CLI sequence in `build0/README.md`; inspect the E7 and mock E8 tables independently; then record which guarantees remain assumptions. Never point these examples at a real payment API.

The added fault scenarios are intentionally *fixture mechanisms*. Build 0 does not record a durable structured escalation queue, audit-grade logging or classified retriable provider error. The full cross-build controls and planned acceptance criteria are in [`ENGINEERING_STANDARD.md`](ENGINEERING_STANDARD.md).

## Build 1 — bounded C04 test evidence

Run `python3 -m unittest discover -s examples/refund-reference-system/build1 -p 'test_*.py' -v` and independently rerun the Build 0 suite. The Build 1 tests cover three deterministic dispositions, forged privilege fields, malformed and cross-tenant inputs, evidence version mismatch, inconsistent correlation, prompt-injection prose as inert data, dependency timeout/errors, and unchanged E7/E8 fixture tables. In particular `test_e7_e8_unchanged_and_no_operation_creation` checks isolated local mock tables with repeated advice, and the import-boundary test checks the supplied source for accidental privileged imports. **These tests do not prove OS isolation, real identity, transaction authorization or live provider denial.** Chapters 25, 29 and 31 require the stronger hijacked-agent valid-token attack with independent E5 enforcement.
