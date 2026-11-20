# Read the implementation as an engineer: a guided source-and-test lab

**Audience:** engineers and advanced students who want to learn *why* each boundary exists, not just run a successful demo. **Prerequisites:** basic Python, functions/classes, dictionaries, exceptions, and SQLite concepts. Python 3.10+ standard library is sufficient. Work from the **repository root**. No credentials, paid API, network access, or payment account are required.

**Scope and safety:** These are independent educational checkpoints. They do not form one deployable end-to-end agent platform, make real financial transfers, certify secure key custody, or enforce a Build 5 ownership epoch inside E5. Build 5 calls the Build 4 fixture but does *not* compose the Build 1/2 reasoning/retrieval pipeline. Design A/B/C are architectural alternatives, not build numbers or an autonomy maturity ladder. Keep the same fictional CASE-204 ($500) and RF-1042 throughout.

## The repeatable reading method

For each checkpoint, follow the same seven steps:

1. **Predict.** State the allowed input, forbidden input, normal output, and what must never happen. Distinguish an *agent recommendation* from *business permission* and *confirmed external effect*.
2. **Draw.** Open that build's `README.md` and embedded `architecture.svg`. Follow each arrow back to a named source module; the diagram is a map, not an enforcement guarantee.
3. **Trace.** Start at the entry point in the table below. Follow functions in their actual call order. Record what each boundary can read, write, and authorize.
4. **Run.** Execute the tests from the repository root, then the documented demo. Use disposable databases and preserve terminal output if collecting evidence.
5. **Falsify.** Read the *negative* test and its assertion before running it. Predict the failure signal; a denial, unresolved state, or exception can be the correct outcome.
6. **Compare.** Inspect the simulated E7 local operational record and E8 provider record when the checkpoint creates them. A missing acknowledgment is not a failed payment.
7. **Defend.** Write one paragraph distinguishing observed fixture behavior from production obligations; identify which other component or human owns the latter.

## Follow the actual source, not just chapter order

Paths below are relative to `examples/refund-reference-system/`. Open each `README.md` first. Methods are exact names in checked-in source at the time of this edition; a later source revision may differ.

| Checkpoint | Follow this actual call path | Useful negative test | Evidence to examine | Not demonstrated |
|---|---|---|---|---|
| Build 0, Ch22 | `build0/refund.py`: `prepare` → `dispatch` → `reconcile` | `build0/test_refund.py::test_lost_ack_and_recovery` | Separate E7/E8 SQLite rows before and after reconciliation | Provider-backed production money movement |
| Build 1, Ch23 | `build1/model_interface.py` → `advisory.py` → `contracts.py` proposal parser | `build1/test_advisory.py::test_model_extra_fields_are_rejected` | Untrusted recommendation; no authorized RF-1042 | Model authenticity, financial authorization |
| Build 2, Ch24 | `build2/identity.py` scope verification → `context.py::retrieve` → `pipeline.py` → Build 1 advisory | `build2/test_scope.py::test_stale_future_and_wrong_version` | Fixture scope, freshness, provenance and review-only result | Real identity provider, persistent memory store |
| Build 3, Ch25 | `build3/client.py` → `service.py::read_frame` → `execute` → Build 0 E7/mock E8 | `build3/test_gate.py::test_valid_agent_token_is_not_payment_approval` | Valid identity *and* independent approval required before fixture effect | Hostile-code OS isolation, real secret custody |
| Build 4, Ch26 | `build4/service.py` E5 entry → `workflow.py::execute` → `ledger.py` / `adapter.py`; `reconcile` uses lookup only | `build4/test_provider.py::test_lost_ack_requires_authoritative_reconciliation` | Durable dispatch before mock provider call; UNKNOWN then lookup | Commercial provider idempotency or settlement guarantees |
| Build 5, Ch27 | `build5/coordinator.py::choose` → `runner.py::step` → Build 4 E5 fixture; successor reconciles | `build5/test_coordination.py::test_crash_after_intent_before_e5_call_does_not_retry` | E2 epoch/lease and intent state; no new financial operation on takeover | E5-side epoch fencing; complete Builds 1–5 integration |
| Reliability, Ch28 | `reliability/recovery_cases.py` → pure outcome decision | `reliability/test_recovery_cases.py::test_not_found_never_declares_failure` | Explicit unresolved decision; no effect capability | External provider query or remediation |
| Security, Ch29 | `security/test_adversarial_cases.py` drives actual Build 3 E5 subprocess | `test_valid_identity_without_finance_grant_denied_without_effect` | Denial despite a valid agent token, plus positive control | Independent protected credential custody |
| Operations, Ch30 | `operations/incident.py::assess` → `Finding.as_record` | `operations/test_incident.py::test_missing_telemetry_never_closes_case` | Read-only observations and an escalation label | Protected audit store or automatic intervention |
| Assurance, Ch31 | `assurance/collect.py` registry → subprocess test → hashed evidence | `assurance/test_collect.py::test_timeout_fails_without_output` | Named methods, source digests, test result and exclusions | Independent signed or production-certified evidence |

`test_file.py::test_name` is a **reader locator** in this table, not shell syntax for the standard-library unittest runner. To run one method, open the named test file and use its documented direct command; to run an entire build, use the command below. Some tests depend on local path setup, so the discovery form is the portable starting point.

```sh
python3 -m unittest discover -s examples/refund-reference-system/build2 -p 'test_*.py' -v
```

Change `build2` to another directory listed above. On macOS/Linux, run all ten companion suites from the **repository root** with `python3 publishing/scripts/check_companion_release.py` (on Windows, `py -3 publishing/scripts/check_companion_release.py --portable` runs Builds 0–2 only). `make check` is a separate book-production QA task and is not the reader's companion test command. Do not paste a financial test fixture into production or reuse its public educational keys.

## Protocol integration (architectural extension, not an executable build)

After Lab B, read [**PROTOCOL_BOUNDARY_STUDY.md**](PROTOCOL_BOUNDARY_STUDY.md). Map a host-owned MCP client to a server that advertises tools, reject discovery-as-permission, route every consequential proposal through independently enforced E5, and contrast tool calls with A2A peer task delegation. Trace the comparable negative assertions in Build 2, Build 3, and the Chapter 29 security fixture. No MCP/A2A protocol stack or compliance evidence is present in this source tree.

## Three guided traces with expected engineering conclusions

### Lab A — context engineering: evidence is never permission

1. Read `build2/identity.py` to find which verification step produces a `VerifiedScope` and which inputs are rejected. `VerifiedScope` is a *fixture verifier output*, not a cryptographic attestation from an enterprise identity provider.
2. In `build2/context.py`, identify the checks for `allowed_sources`, purpose/expiry, tenant/case lookup, `classification`, timezone, and `MAX_AGE_SECONDS`. Note the code checks source age using a provided clock; it does not poll a live system of record.
3. Run `test_stale_future_and_wrong_version`, `test_injection_is_data_not_authority`, and `test_other_tenant_and_case_even_with_valid_signature` through discovery. Explain why a signed claim does not authorize another tenant's evidence or a payment.
4. **Extend on paper:** propose a cross-session memory record carrying a poisoned “refund approved” summary. Define its tenant, source, creation and correction versions, expiration, deletion authority, and negative test. **Do not claim** that Build 2 contains that persistent memory store.

### Lab B — valid agent identity is insufficient for $500

1. Open `build3/service.py::execute`. Mark the separate `identity_authority.verify` and `verify_grant` checks. Which one supplies transaction-specific permission? Which component owns the mock payment handler?
2. Run Build 3's `--scenario compromised` demo and the test `test_valid_agent_token_is_not_payment_approval`. Inspect the *absence* of an effect; compare with `test_authorized_one_effect_and_replay_refused` to ensure the gate can also process an authorized fixture.
3. Explain why separate processes under one Unix user do not protect the private signing key from a same-UID attacker. Outline the production isolation/credential custody controls required beyond this example.

### Lab C — a timeout is not permission to retry

1. Read `build4/workflow.py::execute`: identify the durable `prepare` and `claim_dispatch` calls *before* the provider send.
2. Inject `lost-ack` with the Build 4 demo. Observe `UNKNOWN` locally and a simulated effect externally, then follow `reconcile` to a **status lookup**, not `send`.
3. Read `build5/runner.py::step`, especially `mark_execute_intent` before `e5_request`. The successor can only reconcile. But ask: could a compromised stale worker reach Build 4 E5 directly with previously valid material? The teaching system does **not** implement E5's current E2 epoch check.
4. Defend a production no-go decision until the provider's documented operation-key retention and status guarantees, E5 epoch fencing, and protected approval/credential custody have been demonstrated.

## How to interpret the test output

- **PASS** means a named local scenario met its Python assertions; it does not establish a real deployment quality attribute.
- **DENIED** may be the intended secure result. Do not change a negative test to force a positive financial outcome.
- **UNKNOWN** preserves uncertainty after a possible effect. Do not relabel it `FAILED` or manufacture a new operation key.
- **NOT_FOUND** from a simulated status lookup does not prove the original request never executed.
- **CONFIRMED** from mock E8 is fixture business truth only; actual provider settlement requires independent contract and reconciliation evidence.
- **Timeout / missing evidence** must fail closed or remain unresolved; a successful unit test of timeout handling is not an availability or incident-response service-level claim.

## Evidence packet students should submit

For one lab, provide: (1) chosen build, exact source revision and Python version; (2) an annotated call path citing filenames/functions; (3) one positive and two negative test names with observed results; (4) a timeline of what E2/E5/E7/E8 knows, where applicable; (5) a *non-guarantee* paragraph; and (6) a justified proceed/conditional/hold decision. Include *expected versus actual* observations, not just a green-test screenshot. An instructor can judge the reasoning without inventing a new agent framework.

See `ARCHITECTURE.md` for responsibilities/contracts, `IMPLEMENTATION_EVIDENCE_MAP.md` for exact implementation/limitation mapping, `TESTING.md` for the suite matrix, and `ASSURANCE_HANDOFF_CH28_CH31.md` for bounded assurance evidence. The source-backed diagrams in each build README must be updated if interfaces change.
