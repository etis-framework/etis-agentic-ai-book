# Chapter 28 — Distributed Failure and Recoverable Effects

Part V: Reliability, Security and Recovery

> **Engineering proposition:** An interrupted request does not imply an interrupted effect. A trustworthy workflow preserves one operation identity, separates local knowledge from provider truth, and authorizes recovery actions without guessing that an uncertain payment failed.

## Learning objectives

After this chapter, readers should be able to locate the main failure windows across coordination and ownership (E2), trusted execution and authority (E5), enterprise integration (E6), durable operational state (E7), and authoritative business systems (E8); explain why a worker's local history, the operation journal, and the provider record may disagree temporarily; distinguish safe read-only inquiry from replay of a consequential write; state the assumptions required for provider idempotency and status evidence; reason about stale ownership at the actual enforcement boundary; and defend a recovery decision with explicit negative evidence and accountable escalation records.

## 28.1 A correct refund can still have an unknown outcome

The case is **CASE-204**, a replacement complaint for which a **$500 refund** may be proposed. The independently approved consequential operation is **RF-1042**. Chapter 27's optional Build 5 coordinator can acquire bounded ownership, durably mark that an attempt may be in progress, call the Build 4 trusted-execution service, and recover after an ambiguous response. But Build 5 cannot establish financial truth from its own lease record. If a provider performs the refund and the acknowledgment disappears, durable operational state (E7) may record `UNKNOWN` while authoritative business systems (E8) hold the actual `CONFIRMED` effect. Both records can be internally honest while differing temporarily.

Any distributed system can lose a response after an external effect. Agentic systems add probabilistic proposals, delegated tool use and replacement workers whose fluent summaries can be mistaken for payment proof. The objective is **controlled uncertainty**, not automatic success: an unresolved review is preferable to an unauthorized second $500 credit. General transaction/distribution principles are drawn from Gray and Reuter and Kleppmann; CASE-204's policy is an ETIS construct.

Part IV established a local ownership protocol in coordination and ownership (E2) and an independently guarded trusted-execution service (E5). This chapter deliberately does **not** introduce a new Build 6 or an extra autonomous component. Instead, it stress-tests the existing example and states the additional production controls required to strengthen its guarantees.

## 28.2 Start with the whole logical architecture

Distributed-failure discussions become confusing when readers see only the payment call and not the responsibilities surrounding it. Figure 28.1 reuses the *layered orientation* of Chapter 8's target-state architecture and the *separation of protection zones* introduced in Chapter 16, but highlights the failure seams relevant to RF-1042. In this chapter, a **logical responsibility and failure zone** is a grouping of obligations connected through defined contracts and trust boundaries. It does **not** imply a separate machine, process, network, or independent failure domain. Figure 28.1 shows where information or authority must be controlled—not a physical deployment topology.

Three boundaries must be evaluated separately. A **responsibility boundary** identifies who owns a decision or durable fact. A **trust/enforcement boundary** identifies where unauthorized actions are independently rejected. A **failure/deployment boundary** identifies which implementations can crash, partition, stall, or lose communication independently. These boundaries can coincide, but **logical separation alone never proves failure isolation**. For example, two logical modules inside one process may crash together; separately hosted services may still depend on one shared database. This is an engineering judgment driven by transaction risk, recovery objectives, operational cost, and business impact—not a prescription to deploy nine services.

![](assets/shared-figures/rendered/F28-01.png)

*Figure 28.1 — Layered logical responsibility and failure zones. Like Figure 8.1, the diagram keeps durable operational state (E7) and governance and assurance (E9) cross-cutting. Unlike a deployment view, shaded zones group responsibilities, not machines. Three marked seams show where stale ownership, uncertain dispatch, and provider observation can diverge. See Figure 16.1 for physical protection-zone alternatives; those deployment choices are not guaranteed by this logical view.*

The shaded group outlines indicate *logical separation*. Arrows describe permitted direction of responsibility, not necessarily network traffic. In particular, the advisory action proposal (C04) cannot authorize RF-1042; the independent policy decision (C05) and durable intent (C06) must precede trusted dispatch (C07). The status inquiry/reconciliation contract (C08) does not imply permission to send a new payment. **UNKNOWN is not FAILED**, and missing evidence is never a new authorization. Verify the actual fault topology.

**Worked boundary examples — translating logical separation into real failure behavior**

| Architecture choice | What may fail together or become ambiguous | Required engineering judgment |
|---|---|---|
| Advisory reasoning and coordination share one process | A process crash stops both; no independent network partition occurs between them | Is one recovery restart acceptable for this low-consequence interaction? Keep advisory output untrusted regardless. |
| Coordinator and trusted execution run as separate processes on one host (as in teaching checkpoints) | An IPC reply can be lost or its caller can die; the shared host remains a common failure domain | Does the transaction risk justify independent E5 authorization, durable logs, and failure injection without claiming host isolation? |
| Coordination and durable state use different services but one database cluster | Both may become unavailable if the database fails, even on different hosts | Does the shared dependency meet recovery-time, recovery-point, and consistency requirements? |
| Trusted execution and provider integration are remote services | A provider may commit RF-1042 while the transport response is lost; the caller cannot infer failure | Is stable identity, provider lookup, verified idempotency retention, and accountable `UNKNOWN` handling sufficient? |
| Multiple sites or regions independently host workers | Partitioned workers may disagree about current ownership; a local lease cannot fence a remote privileged call | Does E5 enforce a current authoritative epoch, fail closed on uncertainty, and prevent adapter bypass? Build 5 does **not** implement this. |

These are **deployment examples**, not Build 5 resilience claims. Physical mapping follows business loss tolerance, recovery objectives, provider guarantees, and assurance evidence. Distributed failure concerns divergent knowledge, not merely machine count.

**Table 28.1 — Reader map: what each responsibility contributes to recoverability**

| Responsibility | Why it matters in failure and recovery |
|---|---|
| Admission and identity (E1) via the admission contract (C01) | Establishes the principal, tenant, and permitted work. A valid identity alone does not authorize a refund. |
| Coordination and ownership (E2) via the work-assignment contract (C02) | Decides which worker currently owns progress, records leases/epochs, and prevents stale owners from mutating coordination state. |
| Agent reasoning (E3) via the action-proposal contract (C04) | May suggest an action, but its output is advisory and cannot mint RF-1042 or prove provider truth. |
| Context retrieval and provenance (E4) via the context contract (C03) | Supplies bounded evidence and provenance. It helps explain a decision but does not create financial authority. |
| Trusted execution and authority (E5) via the authorization-decision contract (C05) | Enforces transaction-specific financial authorization before any consequential provider call. |
| Enterprise integration (E6) via the provider-dispatch contract (C07) | Sends the controlled provider request and may experience timeouts, duplicates, or lost acknowledgments. |
| Durable operational state (E7) via the operational-state contract (C06) | Preserves the local operation history, including `AUTHORIZED`, `DISPATCHED`, `UNKNOWN`, and `CONFIRMED`. |
| Authoritative business systems (E8) via the reconciliation contract (C08) | Holds provider observations such as whether RF-1042 is known, confirmed, or absent at query time. |
| Governance and assurance (E9) via the telemetry and evidence contract (C09) | Preserves traceability, escalation, review, and audit evidence needed for accountable recovery. |

A trustworthy reader should now have a stable mental model: **E2 decides who may continue**, **E5 decides whether a consequential action is authorized**, **E7 preserves local history**, **E6 carries the remote request**, and **E8 may know something E7 does not yet know**. E1, E3, E4, and E9 provide the conditions under which those decisions are lawful, reviewable, and explainable.

## 28.3 Three histories, not one transaction

Once the architecture is visible, the recovery problem becomes clearer. An incident investigator must separate three histories that are correlated by RF-1042 but not joined by one atomic commit:

1. **Work ownership history.** Coordination and ownership (E2) records who held the current lease or epoch, which worker believed it was responsible, and whether takeover was legitimate.
2. **Local operation history.** Trusted execution and authority (E5) plus durable operational state (E7) record the authorization decision, the local operation row, and whether the system believes dispatch may have started.
3. **External business history.** Enterprise integration (E6) and authoritative business systems (E8) record what the provider was asked to do and what the provider later reports as the business truth.

These histories are related but not interchangeable. A row in E2 is not proof of a payment. An E7 `UNKNOWN` record is not proof that no refund occurred. An E8 `CONFIRMED` record for the wrong operation, amount, tenant, or customer is not proof for RF-1042. Recovery begins by comparing the right histories, not by assuming they should already agree.

**Authoritative provider truth** means authority for a specified fact—accepted, posted, or settled—not every business outcome. Real integrations must document query consistency, provenance, finality, dispute handling, reference mapping, retention, and whether `NOT_FOUND` can later become `CONFIRMED`. Build 4's mock E8 observations do not prove real settlement or provider guarantees.

## 28.4 Crash windows are engineering requirements

A failure model must name the irreversible boundaries, not vaguely say "retry on error." Table 28.2 enumerates a conservative reference timeline for CASE-204. A crash can occur on either side of each step; a network partition may make E5 or E8 unreachable while their work continues elsewhere.

**Table 28.2 — Crash-point matrix for RF-1042**

| Window | Durable evidence potentially available | Safe next action; forbidden inference |
|---|---|---|
| Before E2 attempt intent | E2 remains `READY`; no E5 call from this path | A first attempt may still be considered under current ownership and current E5 approval. Do not infer absence of every outside call. |
| After E2 intent, before E5 IPC | E2 says `EXECUTE_IN_FLIGHT`; E7 may have no RF-1042 row yet | Treat the case as uncertain. A replacement worker may inspect evidence and reconcile, but absence of an E7 row does not automatically authorize new dispatch. |
| After E5 approval, before E7 dispatch claim | Finance evaluation may have succeeded; E7 intent may or may not exist | Inspect E7 plus provider history. Never reuse a prior grant as blanket replay permission. |
| After E7 claim, before E6 send | E7 says dispatch may have started; E8 may have no row yet | Reconcile or escalate. `NOT_FOUND` is not proof that blind resend is safe. |
| After E6 send and E8 effect, before response | E8 may hold RF-1042; E7 may still be `DISPATCHED` or `UNKNOWN` | Query by the original operation identity. Never mint another refund identifier. |
| After E7 confirmation, before E2 receipt | E7 and E8 may agree while E2 still appears in flight | Verify the trusted proof and close E2 under the current epoch. Do not dispatch again. |
| After lease expiry or partition | Two workers may believe they own work | Reject stale E2 mutations; for production, also require current-owner validation inside E5. |

The matrix intentionally separates *absence of evidence* from *evidence of absence*. Even a status endpoint returning `NOT_FOUND` may be stale, scoped incorrectly, temporarily unavailable, or subject to a finite retention window. No generic algorithm may infer effect nonoccurrence without an explicit provider guarantee, complete operational records, and a defined time boundary.

## 28.5 One failure chronology: lost acknowledgment and replacement ownership

Figure 28.2 shows a provider effect with a lost acknowledgment. The replacement worker must recover without another payment.

![](assets/shared-figures/rendered/F28-02.png)

*Figure 28.2 — Behavioral sequence: after independent authorization (E5), local intent (E7), and provider dispatch (E6), the provider (E8) records RF-1042. Its reply is lost. The original owner can fail and coordination (E2) may transfer ownership, but the new owner must inquire under the original identity and reconcile—not dispatch again. The E2 lease/epoch is not checked inside Build 4's E5 service.*

The dashed red segment in Figure 28.2 represents a **lost response after the external effect**, not an automatically failed payment. Although a logical boundary always exists between the roles, the failed message requires an actual asynchronous, IPC, or remote communication mechanism in the chosen deployment. The replacement worker does **less**, not more: read current evidence, compare identity and scope, then confirm the original operation or escalate. Uncertainty is preferable to an unauthorized duplicate refund.

## 28.6 Idempotency, duplicate suppression, and what exactly-once does not mean

A local transaction can atomically store an operation and dispatch claim, but not the remote provider's effect without a shared protocol. Build 4 has none. A **durable outbox** preserves intended messages, but redelivery requires documented provider deduplication and evidence semantics. Blind redispatch after a possible send remains forbidden.

An **idempotency key** identifies one logical operation within a provider-defined scope and retention period. It is meaningful only if the provider documents what counts as the same operation, how long the key is retained, what happens when a previous attempt is still processing, whether status lookup is read-only, how conflicting parameters are reported, and whether duplicates are rejected or collapsed. If those semantics are undocumented, the system should behave as though automatic replay is unsafe.

**Exactly once** is an unsafe shorthand. Build 5 provides local single-owner transitions in SQLite; Build 4 journals one operation and queries a simulated provider by stable identity. Neither proves exactly-once distributed execution across crashes, partitions, or provider retries. Claim only what each test demonstrates.

## 28.7 Fencing, stale ownership, and the real enforcement boundary

Build 5 uses **leases and epochs** so that a stale worker cannot continue mutating E2 coordination state after a takeover. The `DurableCoordinator` in `build5/coordinator.py` increments epochs and grants time-bounded ownership, and stale workers are rejected when they try to alter E2 rows. The `BoundedRunner` commits `EXECUTE_IN_FLIGHT` before the first IPC call. After a crash, a replacement uses only `reconcile`; a duplicate `execute` is not offered through that recovery route. Build 5 tests this local guarantee.

**Critical non-guarantee:** the Build 4 E5 interface does not consume, validate, or compare Build 5's E2 epoch. Therefore an old worker with a still-valid, separately issued finance grant might call E5 directly despite losing its E2 lease. E5's independent grant check and E7's one-time local claim reduce risk for the *same* operation, but they must not be described as E5-enforced stale-worker fencing or cross-operation containment. A production deployment must add a trusted, fail-closed current-owner or current-epoch check at E5 for ownership-sensitive commands, with replay protection, service identity, and no bypass path through the provider adapter.

Duplicate **delivery** is also different from duplicate **business effect**. Networks may repeat a message. Adapters may retry transport. Two services may race. An administrator may repeat a command during an incident. The desired invariant is that no unauthorized second refund is created. Achieving it requires independent authorization, stable identity, durable uniqueness, provider deduplication under a verified retention window, and reconciliation. No layer should assume the next layer supplies guarantees it has not documented.

## 28.8 Recovery decisions under ambiguous provider evidence

Figure 28.3 converts the architecture and sequence into an accountable recovery decision. The goal is not to maximize automation; it is to make the right thing reviewable and the wrong thing difficult.

![](assets/shared-figures/rendered/F28-03.png)

*Figure 28.3 — Recovery decision, distinct from the message sequence. Check current ownership, perform read-only inquiry for RF-1042, and validate matching, sufficiently final evidence. Confirmation closes the **existing** operation; absence, conflict, staleness, or unavailable evidence leaves `UNKNOWN` and requires escalation. A separate remedy is never an automatic retry and needs new E5 financial authority.*

A resolution record identifies the incident, RF-1042 and scope, finance decision/policy, E2 owner/epoch, E7 event IDs, authenticated E8 observations and retrieval times, contradictory evidence, read-only query, decision owner, escalation basis, customer impact, and proposed remedy. Distinguish **observation** from **interpretation**; never manufacture provider facts from LLM output.

If the provider proves no refund occurred and the business still owes $500, **any new consequential operation** needs fresh transaction-specific E5 approval, a distinct operation identity, and duplicate-risk analysis. A reversal or compensating payment is likewise a new privileged effect, not an informal database correction. The original `UNKNOWN` history should be retained even after the case is later closed. In the companion Build 4 ledger, transactional `operation_events` entries retain the sequence of local observations, including an earlier confirmation that a later contradictory E8 observation has placed in dispute. This is **local educational evidence**, not an independently protected production audit trail.

A compact guarantee inventory keeps the chapter honest:

- **Implemented in repository:** Build 5 prevents stale E2 owners from mutating coordination state; Build 4 requires an independent finance grant; Build 4 and Build 5 preserve a stable operation identity and support read-only reconciliation.
- **Simulated in repository:** provider observations, finance-grant issuer behavior, and incident evidence are deterministic fixtures rather than commercial contracts or operational infrastructure.
- **Not yet proven for production:** cross-site consensus, E5 validation of the current E2 epoch, real provider idempotency retention, settlement finality, independent key custody, incident thresholds, and operator role separation.

## 28.9 Executable negative evidence and multi-perspective review

The companion remains **Builds 0–5**, not Build 6. Chapter 28 adds typed, deterministic `recovery_cases.py` and `test_recovery_cases.py` under `examples/refund-reference-system/reliability/`. This **non-effectful decision fixture** models E2 intent, E7 history, and E8 observations without importing a dispatch API. Tests cover `NOT_FOUND`, conflicting proof, outages, a lost reply, and wrong-operation evidence. Builds 4–5 remain the executable sources for dispatch and reconciliation.

Failure-injection evidence must separately establish status-only takeover after a pre-E5 crash, E7 `UNKNOWN` versus E8 `CONFIRMED` after a lost reply, no new E6 send during reconciliation, single E2 acquisition under contention, rejection of stale E2 mutations, and E5 denial of an E1-only investigator's refund. A stale worker carrying a valid grant, a real multi-site partition, and provider retention guarantees are **not tested**. These remain production blockers.

The **multi-perspective architecture review** should ask the following questions.

**Implementing engineer.** What is the last committed write before each IPC? Which method proves that recovery performs inquiry rather than dispatch? Which tests demonstrate that a stale worker cannot mutate E2? The answer must point to code and tests, not a conceptual slide.

**Enterprise architect.** Does the E2 lease compose with E5 ownership enforcement? Not yet. The architecture must therefore show the missing trusted epoch-validation seam and state what happens if its authority store is partitioned. The current example must not be relabeled as distributed consensus.

**Evidence reasoning.** Given E2 `EXECUTE_IN_FLIGHT`, E7 `UNKNOWN`, and E8 `NOT_FOUND`, explain why a worker cannot conclude `FAILED`. Then compare that with an E8 `CONFIRMED` record for the wrong operation or amount. The objective is to reason from contracts and evidence, not from optimism.

**Security and assurance reviewer.** Can a valid agent token, stale lease, forged provider proof, or untrusted C04 text reach privileged E6 credentials? E5 must reject missing finance authorization. The stale-lease/E5 gap and real service isolation remain explicit open risks, not falsely claimed protections.

**Site reliability and operations reviewer.** How will an operator diagnose a crash after remote success, prove that the retained request key is still recognized, and restore service without paying twice? Name the telemetry, reconciliation evidence, quarantine trigger, and escalation owner. Chapter 30 expands these operational requirements.

**Business owner.** Who explains to the customer why a $500 refund is delayed? Under what evidence can it be described as completed? Who may approve a compensating action? A plausible screen summary is not a financial record.

Together, these reviews establish a constrained conclusion: the educational implementation supports a **bounded, testable recovery principle**, while production release remains conditional on independent approval infrastructure, a verified provider contract, execution-boundary fencing, operational ownership, and real incident evidence.

## 28.10 Engineering exercises and transition

1. **Crash chronology.** Insert a process death at each Table 28.2 boundary. Identify which E2, E7, and E8 evidence survives, the next safe read, and the prohibited write. Include a case in which the call never reached E5 but E2 already recorded intent.
2. **Provider contract challenge.** Assume the provider retains idempotency keys for 24 hours while incidents can remain unresolved for 72. Draft the recovery and escalation policy. Explain why an unconditional resend is dangerous.
3. **Fencing design review.** Add a conceptual E5 validation of a current owner epoch without giving E2 power to issue finance approvals. Define denial on stale, missing, or unverifiable epochs and propose an executable counterexample.
4. **Adjudication.** E7 reports `UNKNOWN`; E8 returns contradictory observations at two times. Prepare a case-disposition record, a customer communication, and the evidence needed before any independent remediation approval.

**Chapter synthesis.** Recoverability is the ability to reach an accountable disposition without treating lost communication as proof that an external effect did not occur. The system must conserve the original operation identity, keep observations distinct, refuse silent replay, and make unresolved cases visible. Chapter 29 now subjects these same boundaries to deliberate adversarial behavior; Chapter 30 operationalizes monitoring and incident handling, and Chapter 31 asks how much evidence is sufficient for release.

**Sources and limits.** Gray and Reuter (1992), Lamport (1978), Kleppmann (2017), and van der Aalst (2013) provide background on transactions, ordering, distributed failure, and workflows. The precise recovery decision policy, CASE-204/RF-1042 contract mapping, fixture semantics, and tests are original ETIS artifacts. Exact external source-to-page verification and any provider-specific contract evidence remain open publication gates.
