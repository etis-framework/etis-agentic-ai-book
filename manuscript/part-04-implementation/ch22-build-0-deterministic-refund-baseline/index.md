# Chapter 22 — Build 0: Deterministic Refund Baseline

*Part IV: Progressive Reference Implementation*

> **Engineering proposition:** Start with the smallest deterministic system that can distinguish a proposed refund, an authorized intent, an attempted payment, and a verified provider outcome. The implementation is useful only if a skeptical reader can reproduce its denials and unresolved cases.

## Learning objectives

After this chapter, readers should be able to: (1) map the deterministic baseline for the recurring $500 refund case to the relevant nine logical enterprise responsibilities without equating them with separate services; (2) distinguish a trusted test fixture from production identity and policy enforcement; (3) implement stable financial operation identity and local durable state; (4) trace a lost acknowledgment through UNKNOWN and safe reconciliation; (5) reproduce negative tests and explain their limits; and (6) decide what must be hardened before introducing an advisory model or live payment adapter.

## 22.1 Begin from the architecture, not an agent framework

Chapter 21 closed the pattern discussion with **ADR-021**, a decision record, and **POL-021**, an illustrative versioned policy. They make decisions reviewable; they do not issue a refund. Chapter 22 turns the architecture's most important financial boundary into an executable, deliberately small teaching fixture. **CASE-204** is still the customer complaint about a replacement that did not arrive; the possible remedy is a **$500 refund**. When issued, the stable operation identity is **RF-1042**. No new case, refund identity, or discretionary agent authority is introduced.

Three designs remain alternatives. **Design A** follows structured facts and deterministic rules. **Design B** adds an advisory model and an independent reviewer and remains the **conditional initial production candidate** for the ambiguous complaint under the book's stated assumptions. **Design C** permits a bounded read-only investigator only if it earns a separate business and assurance justification. This first implementation is a *Build 0 mechanism* most directly aligned with Design A; it is **not** a commitment to deploy A, a transition requirement from A to B to C, or a covert introduction of Design C. Later builds can reuse the controls whichever alternative is chosen.

We begin with deterministic code because the counterexamples are observable. An unauthorized tenant should be denied. A missing approval should not record a financial intent. A duplicate operation should not create a second provider effect. A lost acknowledgment should produce UNKNOWN and require reconciliation. Those assertions must be checked in software before model variability complicates diagnosis. Durable local transactions and the limits of external effects are established engineering problems (Gray and Reuter, 1992; Kleppmann, 2017); the ETIS fixture implements a narrow illustrative solution, not an industry-certified payment protocol.

## 22.2 What is implemented—and what remains a fixture

Figure 22.1 maps Build 0's concrete components onto the approved logical architecture. The CLI supplies fixed case and principal values as a stand-in for **admission and identity (E1)**; it performs no live authentication. A sequential controller stands in for **coordination and ownership (E2)**; it is not distributed or lease-fenced. **Agent reasoning (E3)** and **context and retrieval (E4)** are intentionally absent. A deterministic policy function models the independent gate owned by **trusted execution (E5)**. A simulated adapter separates **enterprise integration (E6)** from local operation state (**E7**) and the mock provider's business result (**E8**). Tests form an initial, narrow **governance and assurance (E9)** evidence trail. All are logical responsibilities, not a demand for nine processes.

![Build 0 separates local intent, independent authorization, and simulated provider truth.](assets/shared-figures/rendered/F22-01.png)

*Figure 22.1 — Build 0's limited trust boundaries. Fixed, trusted case inputs feed an independent deterministic authorization gate; E7 records operational knowledge; E6 calls an isolated simulated E8 provider. Neither an agent nor external payment authority exists in this fixture. The two databases are distinct so local state cannot be mistaken for provider truth.*

The corresponding approved contract path is **C01 admission**, **C02 work order**, **C05 decision**, **C06 durable intent**, **C07 provider dispatch**, **C08 reconciliation**, and **C09 telemetry/evidence**. **C03 context query** and **C04 action proposal** have no active implementation in Build 0. C04 never creates RF-1042: a proposal's correlation value, when added in Build 1, must not masquerade as payment-operation identity. The full reader-facing contract map remains in Chapter 8 and the appendix. The Build 0 simulator does not claim complete implementations of even the active contracts: identity, audit, leasing and production policy deployment will need separate evidence.

| Responsibility | Build 0 artifact | Explicit limit |
|---|---|---|
| E1 / E2 | CLI inputs and sequential controller | No authentication, distributed ownership or fencing |
| E3 / E4 | Not present | No agent, retrieval, prompt, or memory authority |
| E5 | `authorize()` | Fixed fixture policy, not a deployed policy decision service |
| E6 | `dispatch()` | In-process simulated adapter, no network or real credentials |
| E7 | `operations.sqlite3` | Durable local intent/state, not external business truth |
| E8 | `provider.sqlite3` | Separate simulated provider record, not an actual payment system |
| E9 | `test_refund.py` | Executable sample evidence, not full operational assurance |

## 22.3 Fix the case assumptions and operation identity

The reference fixtures use `CASE-204`, tenant `retailer_a`, principal `authenticated_customer_204`, amount `50000` integer cents, operation `RF-1042`, and policy `refund-policy-v12`. The approval flag is a **trusted test fixture**. It is not a customer-supplied parameter, a verified human approval, a model opinion, or a demonstration of real identity federation. The amount uses integer cents to avoid floating-point representation issues; the fixed policy and amount are teaching assumptions, not provider-specific limits.

The baseline's authoritative mock payment facts are intentionally simple: one case, one eligible $500 amount, one simulated provider, and one stable operation identifier. Under a real system, E5 would recheck authenticated delegated scope, current E8 facts, policy version, approval, available balance, revocation, and operation uniqueness inside a protected enforcement boundary. Chapter 25 develops that richer design; Chapter 26 models a **simulated** provider adapter's unknown-result protocol and reconciliation. **Neither chapter transfers permission to E3 or E4.**

Start at **https://github.com/etis-framework/etis-agentic-ai-book/tree/main/examples/refund-reference-system** and open `README.md` in the book's public GitHub repository (public when the book is released). The implementation source is at `examples/refund-reference-system/build0/refund.py`. Its small functions show the complete control sequence: `authorize()` checks exact fixture authority and amount, `prepare()` writes immutable local intent, `dispatch()` exercises an isolated provider, and `reconcile()` queries the separate simulated provider truth. The companion `test_refund.py` supplies repeatable negative and recovery tests. Both SQLite files persist across individual CLI invocations, making recovery observable across process restarts. A separate test matrix in the companion code documents fixture inputs, expected E7 and mock E8 evidence, and the limits of each result. They are separate authorities *within a simulation*; neither is a replacement for an external payment system.

A crucial limit must not disappear in a polished example: the local transition from AUTHORIZED to DISPATCHED is a sequential teaching operation, **not an atomic distributed lease or lock**. Running multiple workers without E2 ownership fencing and E5 concurrency controls is outside this chapter's guarantee. Similarly, the simulator's provider uniqueness constraint models only a chosen fixture behavior. A real provider's idempotency-key scope, retention, retries, query semantics and failure codes must be verified against its actual agreement, not inferred from this code or from HTTP method idempotency (Fielding, Nottingham, and Reschke, 2022, §9.2.2).

## 22.4 The financial state machine is not the case state machine

The *customer case* may remain open, awaiting review, resolved, or escalated while the *financial operation* has another status. For RF-1042, Build 0 uses AUTHORIZED, DISPATCHED, UNKNOWN, and CONFIRMED as local E7 statuses. These names describe what the application knows; they do not create the provider's result. In particular, DISPATCHED is not proof of settlement and UNKNOWN is not a synonym for FAILED. The simulated provider uses its own CONFIRMED record. Chapter 15 introduced this E7/E8 distinction; Chapters 19–20 applied it to adapters and information ownership.

![Build 0 state transitions preserve uncertainty and require observation before closure.](assets/shared-figures/rendered/F22-02.png)

*Figure 22.2 — Build 0's local operation-state transitions, not the entire customer case lifecycle. A lost acknowledgment or crash after dispatch leaves E7 unable to confirm the external effect. Only a provider status lookup with matching operation and amount can move the local record to CONFIRMED. The UNKNOWN state has no new-dispatch path.*

The implementation records durable intent **before** the simulated provider call. On a normal positive acknowledgment it records CONFIRMED. On a deliberately lost acknowledgment *after the mock provider committed*, it records UNKNOWN. If a crash occurs between provider commit and the final local record, the application can restart with DISPATCHED; it is still unresolved. In either condition, `reconcile()` reads the mock provider using RF-1042 and checks the case and amount. A matching CONFIRMED provider record permits a local confirmation. Missing, contradictory or unavailable evidence does **not** permit a new request: the operation remains UNKNOWN or DISPATCHED pending escalation and additional investigation.

This is intentionally conservative. An earlier successful payment does not become reversible because a local program has restarted. A new provider command with a fresh identifier would risk a second $500 effect. Real financial effects may have additional states such as accepted, pending, rejected, settled and disputed; those are omitted in Build 0 rather than silently flattened into CONFIRMED. Later adapter development must express and test those distinctions before claiming readiness.

## 22.5 Reproduce the evidence, including denials

Run the Build 0 baseline tests with only the host's existing Python standard library, from the repository root:

```sh
python3 -m unittest discover \
  -s examples/refund-reference-system/build0 \
  -p 'test_*.py' -v
```

The build-specific README also shows how to inspect E7 and simulated E8 records before and after reconciliation. Additional tests exercise two simultaneous local dispatch callers, malformed monetary and approval types, provider unavailability before commit, and contradictory mock-provider records. A conditional SQLite update allows only one local caller to claim `AUTHORIZED → DISPATCHED`; this is a teaching-level local safety property, **not** an E2 distributed ownership or E5 process-isolation guarantee. The companion `ENGINEERING_STANDARD.md` records the non-negotiable contracts and verification obligations for Builds 1–5. The tests use temporary isolated SQLite files; it has no network calls, customer data or external dependencies. To reproduce a restart-sized experiment, use the documented CLI sequence in `examples/refund-reference-system/build0/README.md`: `prepare`, `dispatch-lost-ack`, `status`, then `reconcile`, all with the same fresh `--directory`. Expect E7 UNKNOWN after the lost acknowledgment, an already committed mock E8 provider refund, and E7 CONFIRMED only after status lookup. Verify that `dispatch` refuses to act on an UNKNOWN operation. The record must keep RF-1042 throughout.

| Negative/positive case | Expected evidence | What it proves within the fixture |
|---|---|---|
| Correct fixed inputs and approval | One RF-1042, CONFIRMED, one mock provider record | Controlled happy path |
| Wrong tenant, principal, case, amount, policy or approval | `Denied`; no local intent and no provider row | Independent fixture authorization checks |
| Repeated preparation and attempted dispatch | Same RF-1042; no second mock provider record | Stable identity and local duplicate rejection |
| Lost acknowledgment after provider commit | E7 UNKNOWN; E8 mock CONFIRMED; direct resend denied | Local observation is not external truth |
| Provider lookup missing or conflicting | Unresolved status; no new dispatch | Missing evidence cannot authorize an effect |
| Restart after DISPATCHED | Read operation and query provider; never blind resend | Recoverability boundary, not crash-atomic guarantee |

These tests are source-controlled evidence for an intentionally bounded teaching system. **They do not establish production security, real money movement, real multi-process concurrency, provider idempotency guarantees or human approval integrity.** A meaningful release decision needs broader negative tests, real contract verification, operational logs, measurable recovery times, ownership fencing, adversarial testing, incident procedures and accountable human signoff. NIST AI RMF (2023) can inform risk governance; it does not attest to this implementation. Chapter 31 will formalize stronger integrated evidence.

## 22.6 Multi-perspective architecture review of the baseline

Use the same professional review perspectives that Chapter 7 introduced, but test only the claims this baseline makes. **Implementing engineer:** inspect `authorize()` and its fixture-only policy rules, and confirm that tests exercise the actual denial and durable-state paths. **Enterprise architect:** verify that the two databases represent E7 operational knowledge versus mock E8 provider truth, not a tenth logical domain or a required deployment topology. **Security and assurance:** demonstrate that direct imports and fixed fixture authorization are **not** an independently protected E5 boundary; a valid agent token must never confer refund authority in the later compromised-investigator test. **SRE/operations:** show that a timeout blocks blind resends until E8 evidence supports reconciliation. **Business owner:** require measured benefit and an accountable release decision before selecting Design B.

The continuing CASE-204 $500 case retains the same RF-1042 operation identity; Designs A/B/C are alternatives, not successive payments. A reader should reproduce that invariant through the exercises below. The review produces questions, evidence and unresolved limitations; it does not certify the fixture for live financial use.

## 22.7 Carry the baseline into Build 1 without changing authority

Chapter 23 can introduce bounded advisory interpretation as a **typed proposal**, with provenance, case correlation and possible abstention. The proposal must stay upstream of E5. It must not supply or mint RF-1042, override the policy fixture, write E7 operation status or call E6. Preserve every Build 0 denial and unknown-outcome test as a regression gate. If advisory quality deteriorates or raises cost and review burden without better outcomes, retain the deterministic alternative. Build 0 is a control baseline, **not a promise to automate the refund**.

**Engineering practice.** (1) Trace CASE-204 through C01, C02, C05–C09, identifying where C03/C04 are absent. (2) Modify a local *copy* of the test fixture to deny a policy version or reduce refundable balance; explain why E7 must remain empty. (3) Inject a lost acknowledgment and show distinct E7 and E8 records before and after reconciliation. (4) Explain why a second $500 operation identifier is unsafe even if the model's customer remedy is correct. (5) Design a concurrency/fencing negative test that this sequential baseline cannot pass, and identify the Chapter 25/26 controls required to pass it. (6) Defend proceed, conditional or hold for a proposed **live** payment pilot, using the demonstrated evidence and its explicit gaps.

**Review standard:** A defensible answer identifies each authority, state, and evidence boundary; distinguishes fixture assumptions from production guarantees; preserves the unchanged CASE-204/RF-1042 identity; and can reproduce both a policy denial and an unresolved provider outcome. Saying that the CLI worked once is not an adequate release argument.

**Sources and further reading.** Gray and Reuter (1992) on local transactional durability; Kleppmann (2017) on distributed uncertainty and data consistency; Fielding, Nottingham, and Reschke (2022, RFC 9110 §9.2.2) on HTTP method idempotency only; NIST AI RMF (2023) on governance framing. The Build 0 code, diagrams, state choices and fixed business policy are original ETIS teaching artifacts. None of these sources certifies a payment provider's contractual behavior. Exact source-page/edition verification remains an open publication gate.
