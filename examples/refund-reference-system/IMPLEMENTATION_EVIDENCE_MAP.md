# Part IV — Implementation, contracts, and verification evidence

This is a **source-accurate teaching map**, not a certification report. Chapter 8 owns the canonical reference architecture (CAB-001). The same CASE-204 customer case concerns a proposed $500 refund; **RF-1042 is created only by the trusted consequential path**. A C04 advisory `operation_id` is not RF-1042 or a payment-provider key. **Statuses are scoped to the indicated runnable checkpoint, not production compliance.**

## 1. Why six builds exist and how much they compose

| Checkpoint | Engineering problem that justifies it | Code run and actual composition | New evidence and negative test | Explicit omission |
|---|---|---|---|---|
| Build 0, Ch 22 | Deterministic correctness before AI | `build0/refund.py`, `test_refund.py`; self-contained fixture | Invalid payment inputs, duplicate dispatch, lost reply, E7/E8 divergence | Live identity, model and independent payment provider |
| Build 1, Ch 23 | Advice cannot create authority | `build1/advisory.py`, `contracts.py`, `model_interface.py`; independent of Build 0 | Forged finance fields rejected; E7/E8 unchanged (`test_advisory.py`) | Actual trusted financial execution |
| Build 2, Ch 24 | Identity, scope and provenance constrain advice | `build2/identity.py`, `context.py`, `pipeline.py` **calls Build 1 advisory** | Tampered/wrong-tenant fixture assertions; stale context; valid token without permission (`test_scope.py`) | Real IAM, signed source attestations and E5 invocation |
| Build 3, Ch 25 | A valid token does not authorize $500 | `build3/service.py`, `client.py` separate subprocess; Build 2 fixture token, Build 0 trusted simulator | Valid-token/no-grant E5 denial; malicious IPC framing (`test_gate.py`) | Independent hostile-OS identity and live provider |
| Build 4, Ch 26 | Effects and evidence can diverge | `build4/service.py`, `workflow.py`, `ledger.py`, `adapter.py`, `provider_contracts.py`; reuses E5 request semantics | Provider conflict, duplicate claim, lost acknowledgment, status-only reconciliation (`test_provider.py`) | Real provider status consistency and settlement |
| Build 5, Ch 27 | Optional durable worker ownership and safe takeover | `build5/coordinator.py`, `runner.py`, `demo.py` **calls Build 4 E5 subprocess** with Build 2 fixture identity | Stale/expired epoch, concurrent lease, crash/takeover, status-only reconciliation (`test_coordination.py`) | **No Build 1/2 advisory/retrieval in this runtime; no E5-enforced E2 epoch** |

The checkpoints produce **cumulative engineering knowledge**, not a mandatory architectural maturity sequence and not six consecutive releases of one fully assembled application. Design A (deterministic), Design B (advisory plus independent review), and Design C (optional bounded investigation) remain *alternatives*; Build 5 does not require Design C. Readers should run each checkpoint independently and inspect its README, `architecture.svg`, modules and test assertions.

### Executable evidence anchors (selected named tests)

Run the complete suite in each directory; the following names are audit entry points, not a replacement for the other cases.

| Build | Negative / recovery test methods in `test_*.py` | What to inspect |
|---|---|---|
| 0 | `test_two_concurrent_dispatchers_only_one_wins`; `test_lost_ack_and_recovery`; `test_conflicting_provider_record_cannot_be_accepted` | Local E7 claim, separate mock E8 truth and no fabricated success |
| 1 | `test_advisory_has_no_privileged_module_dependency`; `test_model_extra_fields_are_rejected`; `test_valid_advice_is_untrusted_and_not_operation` | Advisory-only module imports and forged fields |
| 2 | `test_forged_signature_and_malformed_tokens`; `test_other_tenant_and_case_even_with_valid_signature`; `test_repeated_review_does_not_write_fixture_financial_databases` | Fixture identity/scope failure and unchanged financial stores |
| 3 | `test_valid_agent_token_is_not_payment_approval`; `test_aborted_client_does_not_terminate_service`; `test_post_effect_reply_lost_does_not_redispatch` | Real E5 subprocess refusal and interrupted-client handling |
| 4 | `test_replayed_execute_does_not_call_provider_twice`; `test_lost_ack_requires_authoritative_reconciliation`; `test_idempotency_scope_must_be_documented` | Provider contract assumptions and status-only recovery |
| 5 | `test_expiry_permits_fenced_replacement`; `test_crash_after_intent_before_e5_call_does_not_retry`; `test_reconciliation_never_promotes_missing_evidence` | E2-local epochs, one attempt and inconclusive provider evidence |

## 2. Logical responsibilities and observed implementation

Interpretation key: **Executed** means an exercised, bounded code path; **fixture** means a simulated mechanism; **specified only** means described as an architectural obligation; **not implemented** means no corresponding runnable capability in the indicated path. Multiple descriptions may apply to different aspects of one domain.

| CAB responsibility | Executed or simulated teaching evidence | Still specified only / not implemented in Build 5 |
|---|---|---|
| E1 Admission and identity | `build2/identity.py` verifies local signed assertion fixture; `build4/service.py` checks supplied identity | No real enterprise issuer, credential custody, revocation or admission service |
| E2 Coordination and ownership | `build5/coordinator.py` owns local SQLite lease and monotonic epoch; `runner.py` chooses one attempt/reconciliation | No multi-site authority and **no E5 enforcement of worker epoch** |
| E3 Agent reasoning | `build1/advisory.py` runs a bounded, injected advisory mechanism; Build 2 composes it | **Not executed by the Build 5 refund call**; no live LLM claim |
| E4 Context and retrieval | `build2/context.py` scopes fixture sources with provenance; `pipeline.py` feeds Build 1 | **Not executed by the Build 5 refund call**; no real enterprise retrieval infrastructure |
| E5 Trusted execution | `build3/service.py`, `build4/service.py` reject no-grant requests; process-scoped enforcement | Not a protected hostile-host credential principal or genuine finance issuer |
| E6 Enterprise integration | `build4/adapter.py` tests a typed provider facade | Real network/settlement APIs and externally verified idempotency retention absent |
| E7 Durable operational state | `build4/ledger.py` and Build 0 ledger persist intent and atomic dispatch claim | Real distributed state availability, backups and recovery operations absent |
| E8 Authoritative business truth | `build4` mock provider SQLite is an independently observed *fixture* | Real provider, financial settlement and external audit evidence absent |
| E9 Governance and assurance | Test suites, negative cases, contract docs and review records are produced | **No running E9 service**, organizational controls, production monitoring or formal signoff |

## 3. Cross-domain contract status

| Contract | Executed / fixture scope | Outside fixture / not end-to-end |
|---|---|---|
| C01 Admission | Build 2 signed scope fixture; E5 consumes identity | No live enterprise admission/issuer or C01→E2 joined production request |
| C02 Work order | Build 5 E2 local lease, worker, epoch | No E2→E3 runtime task dispatch feeding Build 5 advice |
| C03 Context query | Build 2 E4 scoped fixture lookup | Not called in Build 5 payment path |
| C04 Action proposal | Build 1 typed advisory output; Build 2 composes it | Never an E5 financial grant; not consumed by Build 5 E5 runtime |
| C05 Decision | Build 3/4 E5 verifies separate local signed finance fixture | No independent finance issuer or real E9 policy service |
| C06 Durable intent | Build 0/4 E7 persists trusted RF-1042 and atomic claim | No distributed persistence guarantees |
| C07 Provider dispatch | Build 4 E6 typed adapter sends to mock E8 once | No real payment-provider contract or final settlement |
| C08 Reconciliation | Build 4 read-only status; Build 5 takeover only reconciles | No actual external provider adjudication service |
| C09 Telemetry and assurance | Negative tests/documented evidence and review material | Not a deployed enterprise audit/monitoring/governance pipeline |

## 4. Trace three consequential scenarios without inventing edges

**A. Authorized CASE-204, $500.** The actual Build 5 demonstration assembles a fixture request and obtains an E2 lease; E2 persists execute intent; E5 (Build 4 subprocess) independently validates a finance approval and fixture identity; E7 durably records RF-1042 and claims dispatch; E6 invokes mock E8; the provider record supports confirmation. **C03/C04 are not called during this Build 5 path.**

**B. Compromised investigator with a genuinely valid identity assertion.** Build 3/4 E5 refuses a request lacking the separate transaction approval; no RF-1042 operation or mock provider effect may be created. A signed C04 proposal does not change that result. Local fixture keys do not establish hostile same-UID security.

**C. Lost provider acknowledgment and E2 takeover.** The mock provider may record the RF-1042 effect while E7 has an UNKNOWN observation. Build 5's successor takes the lease at a larger E2 epoch and performs a **status-only C08 reconciliation**; it cannot issue another execute request through the runner. E5 itself does not fence the old worker's epoch, so that stronger production claim remains unproved.

A complete *logical* enterprise route would include admission (C01), E2 tasking (C02), E4 retrieval (C03), E3 advisory proposal (C04), independent E5 decision (C05), E7 intent (C06), E6 effect (C07), E8 reconciliation (C08) and E9 evidence (C09). **That is a reference-architecture trace, not the Build 5 executable call graph.**

## 5. Production-readiness decision: HOLD for real payments

Required accountable work includes independent E1 identity, an E5 finance approval issuer and credential isolation; E5-side E2 epoch fencing where multi-worker concurrency requires it; provider-certified idempotency scope, lookup, retention and settlement semantics under E6/E8; E7 backup, recovery and operator controls; E9 audit, telemetry, incident response, policy evolution, privacy controls, and human recourse. A read-only independently governed recovery authority is required after short-lived approval expires. Economics must compare Build 5 coordination against the simpler Build 4/Design B option before accepting its operational cost. These are **deployment requirements and evidence gaps**, not functionality granted by a green fixture test.
