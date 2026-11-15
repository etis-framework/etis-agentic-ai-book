# Chapters 28–31: executable assurance handoff (Builds 0–5)

**Evidence status: developed through Chapter 31; local fixture execution only, production acceptance open.** This is a reader navigation and assurance trace, not a new Build 6 or proof of a production refund platform. The only fixed business case is CASE-204, proposed **$500**, with trusted consequential operation **RF-1042**. Proposed action/correlation IDs are *not* the refund identity. ETIS reference architecture logical responsibilities (E1–E9) and contracts (C01–C09) remain authoritative; a Python module or OS process is not automatically an independent trust or failure domain.

## How to reproduce the existing evidence

From the repository root, run each directory independently. Each checkpoint's README embeds its actual source/module `architecture.svg`; the diagrams represent **different runnable slices**, not a single composed deployment.

```bash
python3 -m unittest discover -s examples/refund-reference-system/build0 -p 'test_*.py' -v
python3 -m unittest discover -s examples/refund-reference-system/build1 -p 'test_*.py' -v
python3 -m unittest discover -s examples/refund-reference-system/build2 -p 'test_*.py' -v
python3 -m unittest discover -s examples/refund-reference-system/build3 -p 'test_*.py' -v
python3 -m unittest discover -s examples/refund-reference-system/build4 -p 'test_*.py' -v
python3 -m unittest discover -s examples/refund-reference-system/build5 -p 'test_*.py' -v
python3 -m unittest discover -s examples/refund-reference-system/reliability -p 'test_*.py' -v
```

These commands run local test fixtures, not remote payment operations. Some Build 3–5 tests exercise a real local subprocess, not a separately protected OS security principal.

## Claim-to-test navigation

| Future reader focus | Existing executable evidence (exact unittest method) | What this establishes | Must **not** be inferred |
|---|---|---|---|
| Ch28: lost reply, reconcile original RF-1042 | `build0/test_refund.py::test_lost_ack_and_recovery`; `build4/test_provider.py::test_lost_ack_reconcile_via_service_no_second_send` | Simulated E8 effect may exist despite local uncertainty; read-only reconciliation does not resend | A real provider's deduplication, finality, or 24/7 status availability |
| Ch28: no blind retry after a missing observation | `build4/test_provider.py::test_outage_missing_record_stays_unknown`; `reliability/test_recovery_cases.py::test_not_found_never_declares_failure` | `NOT_FOUND` does not justify a new financial command | `NOT_FOUND` is authoritative proof of absence |
| Ch28: conflicting or mis-scoped provider truth | `build4/test_provider.py::test_provider_conflict_revokes_earlier_local_confirmation`; `reliability/test_recovery_cases.py::test_wrong_operation_proof_escalates` | An inconsistent fixture observation does not confirm the original operation | Real provider signatures, settlement, dispute finality or proof-of-nonpayment |
| Ch28/30: takeover after a possible attempt | `build5/test_coordination.py::test_crash_after_intent_before_e5_call_does_not_retry`; `build5/test_coordination.py::test_stale_owner_cannot_override_new_owner_reconcile` | A new owner follows the status-only path, and stale E2 writes are fenced locally | Build 4 E5 verifies an E2 epoch; it **does not** |
| Ch29: untrusted advisory is not a payment command | `build1/test_advisory.py::test_actual_build0_e5_denies_without_independent_approval`; `build3/test_gate.py::test_advisory_forgery_cannot_mint_operation` | Advisory C04 cannot substitute for independent trusted finance authorization in the fixture | Production privilege isolation or detection of every model-manipulation attack |
| Ch29: genuine E1 token without finance approval | `build3/test_gate.py::test_valid_agent_token_is_not_payment_approval`; `build4/test_provider.py::test_valid_token_without_approval_cannot_create_provider_or_ledger` | Even a valid *fixture* identity cannot create RF-1042 without independent E5 approval | Protection against hostile same-UID compromise, stolen finance grants or shared key custody |
| Ch29: untrusted source data and scope | `build2/test_scope.py::test_injection_is_data_not_authority`; `build2/test_scope.py::test_other_tenant_and_case_even_with_valid_signature` | Fixture context cannot turn instruction text or cross-tenant data into authority | A production RAG security posture, DLP or full adversarial evaluation |
| Ch30: transport and service failure | `build3/test_gate.py::test_aborted_client_does_not_terminate_service`; `build4/test_provider.py::test_stalled_connection_has_bounded_delay` | Local subprocess framing and timeout limits in tested cases | Multi-site SLOs, dashboards, paging, runbook execution or disaster recovery |
| Ch31: negative evidence and replay | `build4/test_provider.py::test_replayed_execute_does_not_call_provider_twice`; `build5/test_coordination.py::test_concurrent_acquire_has_one_winner` | Locally bounded uniqueness/replay and E2 acquisition controls | End-to-end exactly-once distributed transactions or release certification |

## Deeper war-game correction: preserving prior observation evidence

Build 4 now records each local E7 state transition in an ordered, transactional `operation_events` table alongside the existing `operations` row. In particular, `build4/test_provider.py::test_reconciliation_conflict_preserves_prior_confirmation_history` shows the current row can legitimately become `UNKNOWN` after a contradictory provider read **without erasing the earlier `CONFIRM` event**. `::test_lost_ack_and_reconciliation_preserve_all_local_transitions` checks the `PREPARE → DISPATCH_CLAIM → OBSERVE_UNKNOWN → CONFIRM` history and one mock E8 row. This is local non-tamper-evident fixture history—not secure E9 audit, independent provider proof, or an append-only immutable external ledger. Ch30 should extend it with independently protected, redacted, correlated operational evidence.

## Chapter 29–31 work: historical acceptance scope (read current implemented evidence below)

**Chapter 29 — Security and Adversarial Agent Behavior.** Run the explicit compromised/hijacked bounded-investigator scenario carrying a *valid E1/service token*: attempt the unauthorized CASE-204 $500 refund through trusted E5, then verify no RF-1042 is issued and no E6 payment credential is available to the investigator. The current grant-denial tests demonstrate the first *fixture* denial; direct protected-credential isolation, token theft/replay, OS-principal separation, and independently issued grants require additional architecture, fault models and adversarial tests. A signed advisory proposal is still only C04 data.

**Chapter 30 — Reliability, Observability, and Incident Response (implemented teaching fixture; production assurance remains open).** Convert Chapter 28's three histories into correlated telemetry, incident severity, explicit UNKNOWN queue ownership, quarantine/stop, human escalation and recovery drills. Demonstrate at least one runbook exercise with an evidentiary closure record rather than only assertions over status strings. Existing tests cover process-level failure, not on-call readiness, retention, replicated state, failover or recovery-time guarantees.

**Chapter 31 — Verification, Evaluation, and Evidence (now implemented as a bounded collector).** Assemble the exact test evidence and falsification conditions for each claimed guarantee. Include a deliberately denied valid-token investigator scenario, wrong-operation proof, provider `NOT_FOUND`, stale E2 epoch, repeated C07 dispatch attempt, and a versioned release evidence bundle. Clearly label what is deterministic, simulated, measured, and untested. A passing fixture test cannot certify a real provider contract, protected execution or independent financial decision issuer.

## Architecture gap that must remain visible

Build 5 fences E2 ownership transitions in one local SQLite authority. Build 4 E5 **does not consume the E2 epoch** and must not be described as enforcing current-owner fencing. The Build 5 refund scenario directly calls the Build 4 E5 subprocess with preassembled fixture identity/approval; it does **not** run the Build 1/2 E3/C04 and E4/C03 advisory/context pipeline. A production implementation has to choose and verify physical failure domains, trust separation, independent finance grant custody, E5 ownership validation, durable E7 recovery and the actual provider's E8 reconciliation contract. Make these engineering choices based on business impact and expected failure modes, not architectural shorthand.

## Chapter 29 implemented adversarial harness (post-Chapter 28)

`security/test_adversarial_cases.py` starts the **actual Build 3 E5 subprocess** and uses the real Build 2 fixture E1 assertion. Six tests cover denial of a genuine investigator token without finance approval, fake C04 fields, mistaken E1-to-finance-grant promotion, wrong scope/amount, tampered grant, and an independently approved positive control. Denials verify **absence of both local E7 and mock E8 files**. Run `python3 -m unittest discover -s examples/refund-reference-system/security -p 'test_*.py' -v`.

This is not Build 6 and does not prove sandboxed adversary principal isolation: the test harness itself holds fixture keys for setup, and its simulated E6/E8 do not access a real provider. E5 current-owner epoch fencing, credential isolation against a same-UID attacker, token revocation, independent approval custody, multi-site threats and protected E9 audit remain **unimplemented** and must be treated as production release blockers. Chapter 30 addresses non-effectful incident classification and the human response model; Chapter 31 must evaluate the complete claim/evidence matrix.

## Chapter 30 implemented read-only incident fixture — Chapter 31 inheritance

`operations/incident.py` reads actual Build 4 E7 and Build 5 E2 SQLite rows using URI `mode=ro` and receives synthetic E8 status; it has no C07 path. `operations/test_incident.py` runs 14 negative/operational checks against actual initialized Build 4/5 fixture databases. Nonmutation is checked on all three local databases; temporal gaps, duplicates, contradictory E8 evidence and compromised-credential **signals** produce bounded dispositions. In Chapter 31, verify the source and these named tests, and **falsify** any attempt to upgrade their conclusions to production claims. Remains unverified: independently protected E9 custody, live C08 settlement provenance, actual revocation, distributed failure isolation, provider contract, E5 owner epoch fencing and native 7×10 Word pagination.

## Chapter 31 implemented assurance harness and production disposition

`assurance/README.md` embeds the actual collector/module diagram; `assurance/collect.py` runs seven named existing methods in `security/`, `reliability/`, `build4/`, `build5/`, and `operations/`. `assurance/test_collect.py` has 12 negative and structural tests. The collector verifies source presence and SHA-256, observes exactly one executed unittest per registered claim, records a safe output digest without exporting raw stdout/stderr, refuses reuse of an existing report path, and fails closed on timeout or zero-test success. Example: `python3 examples/refund-reference-system/assurance/collect.py --output /tmp/etis-ch31-evidence.json`.

The collected JSON is **local reproducibility evidence only** and always states `production_certified: false`. `E5_EPOCH` and `PROTECTED_AUDIT` remain `NOT_IMPLEMENTED`; `CREDENTIAL_CUSTODY` and `PROVIDER_SETTLEMENT` remain `EXTERNAL_EVIDENCE_REQUIRED`; real representative `AGENT_EVALUATION` remains `SPECIFIED_ONLY`. Even seven passing tests do not demonstrate production release safety, provider finality, real issuer custody, isolated service principals, protected audit, independent attestation or model drift performance. Chapter 31 Tables 31.1–31.2 contain the author-facing falsification and status semantics.
