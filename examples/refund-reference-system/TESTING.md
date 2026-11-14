# Verification and evidence guide

This is a **teaching verification plan**, not a production test attestation. Durable operational state (E7) is the local operation ledger; the authoritative business-system responsibility (E8) is represented by a **simulated** provider record. A valid identity assertion from admission and identity (E1) is not transaction-specific authorization by trusted execution (E5). The executable cases are in `build0/test_refund.py`. Run them from the repository root with:

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

## Build 1 — bounded advisory action-proposal (C04) test evidence

Run `python3 -m unittest discover -s examples/refund-reference-system/build1 -p 'test_*.py' -v` and independently rerun the Build 0 suite. The Build 1 tests cover three deterministic dispositions, forged privilege fields, malformed and cross-tenant inputs, evidence version mismatch, inconsistent correlation, prompt-injection prose as inert data, dependency timeout/errors, and unchanged E7/E8 fixture tables. In particular `test_e7_e8_unchanged_and_no_operation_creation` checks isolated local mock tables with repeated advice, and the import-boundary test checks the supplied source for accidental privileged imports. **These tests do not prove OS isolation, real identity, transaction authorization or live provider denial.** Chapters 25, 29 and 31 require the stronger hijacked-agent valid-token attack with independent E5 enforcement.

## Build 2 / Chapter 24: identity and scoped context evidence

`python3 -m unittest discover -s examples/refund-reference-system/build2 -p 'test_*.py' -v` exercises 13 self-contained tests: valid review-only output and provenance; tampered/malformed assertions; expired/not-yet-valid claims; valid signatures for wrong tenant/case; rejection of arbitrary `VerifiedScope` values at the assertion API; source allowlist and inconsistent catalog keys; stale, future and wrong-version source records; E4 outage category; malformed claim/record types; prompt-injection-as-data; ten repeated recommendations against unmodified SQLite marker files; a valid investigator token without financial authority; and static no-payment-import checks. Run Build 0 and Build 1 tests separately as their READMEs direct.

**What these tests do not prove:** real identity, issuer security, cryptographic source attestation, a live LLM's prompt-injection resistance, protected E5/E6 access, multi-process isolation, provider idempotency or independently authenticated E8 truth. `ContextUnavailable` is not financial `UNKNOWN`. Chapter 25 must test a compromised valid-token investigator against actual independent E5 denial. The negative CLI cases intentionally exit with code 2. See `build2/README.md` for expected outputs and fixture risk table.

## Build 3 / Chapter 25: independently evaluated trusted-execution (E5) request boundary

Run `python3 -m unittest discover -s examples/refund-reference-system/build3 -p 'test_*.py' -v` and independently rerun Builds 0–2. The Build 3 suite uses an actual signed Build 2 fixture identity assertion and an independent signed transaction-specific approval; tests are fresh-process, credential-free and do not access a real provider.

| Negative or positive case | E5 result | Durable E7 and mock E8 observation | Scope of proof |
|---|---|---|---|
| Hijacked investigator with valid E1 assertion, no finance grant | DENIED | No E7 or provider database created | Independent request-path refusal, not arbitrary same-UID code isolation |
| Forged C04 approval/operation ID, extra action fields, bool-money | DENIED | No financial intent/effect | Strict schema and actual absence of fixture effect |
| Expired/tampered/wrong-scope grant, invalid identity | DENIED | No financial intent/effect | Different assertion and case-approval checks both enforced |
| Valid finance-granted CASE-204 $500 operation | CONFIRMED | One RF-1042 intent and mock provider effect | Fixed fixture approval, local one-time dispatch |
| Six concurrent requests with same grant | One confirmed, five denied | Exactly one mock refund | Single-worker SQLite claim and sequential E5 socket handling, not distributed fencing |
| Outage after E7 claim; retry attempt | UNKNOWN then UNKNOWN, no resend | DISPATCHED unresolved, mock provider empty | Never convert uncertain outcome into new dispatch |
| Contradictory mock E8 record after E7 dispatch claim | UNKNOWN | E7 remains DISPATCHED; conflicting provider row preserved | Conflict is uncertainty, never clean denial or a second transfer |
| Unavailable service or malformed IPC | Unavailable or denied | No inference of failure after an uncertain transport | No automatic network retry |
| Client closes before E5 writes reply | Next request remains serviceable | No operation for unauthorized request | Connection-level send errors contained |
| Incomplete frame / slow trickle | Worker resumes within total 0.75-second framing deadline | No operation created | Single-worker bounded delay, not flood resilience |
| Oversized frame | Rejected before approval processing | No operation created | Bounded memory and framing; no per-principal rate limiter |

The fixture does not prove production-grade OS confinement, finance approval issuer security, revocation, real provider idempotency or reconciled payment truth. Ch26 adds provider-specific contracts; Ch29/31 repeat adversarial verification with a stronger deployment threat model.


## Chapter 26 / Build 4 — provider contract and reconciliation

Run `python3 -m unittest discover -s examples/refund-reference-system/build4 -p 'test_*.py' -v`. Verify: E1 valid token without separate E5 finance approval creates no E7/E8 database; an authorized effect is recorded once under RF-1042; a lost acknowledgment leaves E7 UNKNOWN and an E8 confirmed effect; an E8 read-only lookup resolves the same operation; missing or contradictory provider data remains UNKNOWN without send; conflicting immutable provider fields and unsuitable capability declarations fail closed; hostile socket clients cannot permanently stall or terminate the E5 service. All fixture tests must pass with resource warnings treated as errors. Separate SQLite connections must be explicitly closed. **These test results do not establish real provider status consistency, settlement finality, cross-site exactly-once effects, independent OS identities or protected approval issuers.** See `build4/README.md` for the owner/evidence matrix.


## Build 5 (Chapter 27): optional E2 ownership evidence

Run `python3 -m unittest discover -s examples/refund-reference-system/build5 -p 'test_*.py' -v`. Assertions cover atomic concurrent lease competition, monotonic epoch on takeover, expired and stale-owner denial, durable one-time execute intent before E5 contact, crash-before-send preventing an execute replay, malformed E5 observations producing UNKNOWN, read-only reconciliation after lost acknowledgment, and real Build 4 E5 subprocess integration. **Trust boundary:** trusted execution (E5) still checks finance approval separately; E2 fencing applies to its own SQLite mutations and is **not** propagated to E5. E7 and mock E8 remain independently observable. Extra protection needs E5-side epoch enforcement, protected worker identities, reconciliation-only authority, and multi-site deployment evidence.
