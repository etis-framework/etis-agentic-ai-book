# Chapter 10 — Coordination, Registry, and Ownership (E2)

*Part II: Enterprise Reference Architecture*

> **Engineering proposition:** A workflow has one authoritative logical owner at a time, even when many workers cooperate and physical coordinators are replaced. A capability registry helps route work; it never grants permission or becomes the workflow's record of truth.

## Learning objectives

After this chapter, readers should be able to (1) distinguish logical workflow ownership from the process currently executing it; (2) separate admission, capability discovery, task assignment, authoritative state, and financial authorization; (3) design deterministic coordinator decisions and bounded worker handoffs; (4) explain leases, epochs, and fencing under coordinator failure; (5) trace a lost acknowledgment without creating a second refund; and (6) specify operational tests and evidence for a recoverable coordination architecture.

## 10.1 From admitted work to accountable progress

The target-state map in Figure 8.1 locates E2 as accountable coordination, not payment authority. Chapter 9 established the authenticated, purpose-limited admission envelope for `CASE-204`. The customer reports a missing replacement and requests a **$500 refund**. Admission and identity (E1) establishes the tenant, principal, case binding, permitted investigation, and expiration. Yet admission does not answer a different question: **who is responsible for moving the case forward when several services, workers, or people participate, and who resumes it after a failure?** That is the work of coordination and ownership (E2).

The earlier architectural choice still holds. **Design A** is the deterministic baseline. **Design B**, model-assisted evidence synthesis with independent review, is the *conditional initial production candidate*. **Design C** is a separately evaluated, read-only investigation agent; its dynamic read choices do not give it payment authority. In every design, the workflow must retain accountable ownership, preserved evidence, valid scope, and an explicit completion or escalation state. `RF-1042` is the illustrative stable financial-operation identifier used **only after independent authorization**. E2 neither invents that authorization nor issues payment through an agent.

Consider an investigator that produces a sound recommendation but crashes before submitting it. Without a durable case owner, its work may disappear. Consider two coordinators that each believe they own the same case. Without exclusive logical ownership and fencing, both may advance conflicting decisions. Consider a registry that claims an investigator is healthy but whose credentials have been revoked. Discovery alone cannot establish eligibility. The architecture must make these distinctions enforceable rather than rhetorical.

## 10.2 Four distinct coordination responsibilities

**Workflow ownership** is accountability for the current case state and permitted transitions. The authoritative record of `CASE-204` includes its goal, admitted scope, stage, selected design, current task, decisions, responsible owner, deadlines, and evidence references. The durable operational state responsibility (E7) persists this record; the coordinator is the actor permitted to advance it under concurrency controls. The two responsibilities may share a process, but **a coordinator's memory or model conversation is not the authoritative record**.

**Task orchestration** selects the next *allowed* step: retrieve shipment data, request an advisory summary, route an exception for review, or hold pending evidence. A deterministic coordinator may use a state machine and an explicit transition table; a model or worker may suggest an investigation step but must not silently rewrite the workflow plan. **Capability discovery** locates a suitable registered worker for a permitted task. **Worker supervision** assigns the bounded task, observes timeouts and failure, and reassigns or escalates using current identity, scope, and ownership evidence.

A *logical coordinator* is the authoritative decision-making role for one workflow instance. Its *physical executor* is the process or node currently holding the ownership lease. An enterprise can run a horizontally scaled pool of coordinators while preserving **one logical owner for a case at a time**. This is not a requirement for one global singleton coordinator, nor for a supervising language model. It is a requirement that case transitions have a single authoritative serialization and fencing mechanism.

Figure 10.1 separates the durable state and registry from the replaceable coordinator and the bounded worker. It shows the financial boundary as independent because the coordinator may schedule a request for authorization, but cannot turn a proposal into permission.

![Figure 10.1 — A replaceable coordinator owns one logical case workflow; a capability registry discovers eligible workers, while durable state and trusted financial authorization remain separate.](assets/shared-figures/rendered/F10-01.png){#fig:f10-01 width=5.75in}

## 10.3 Registry presence is not trust

The **capability registry** answers: which implementations advertise the required capability, where are they reachable, and which appear ready under current operational criteria? A useful record includes capability identifier, version, supported contract, workload principal, tenant or domain eligibility, endpoint, health, registration provenance, lifecycle status, and relevant governance restrictions. Registry metadata is not a source of customer entitlement, approval, or payment truth.

Three registration patterns are reasonable. **Infrastructure-managed registration** is the preferred baseline where deployment and service discovery can publish identities and readiness from trusted infrastructure. **Authenticated self-registration** is feasible if the platform validates workload identity and enforces short-lived registrations and revocation. **Supervisor-mediated registration** can be useful when a controlled coordinator vets subordinate workers. These are alternatives, not three mandatory sequential steps. The choice depends on deployment topology, identity infrastructure, failure isolation, operational ownership, and threat model—not the number of agents.

Discovery must be followed by eligibility checks. The coordinator may discover a `refund-evidence-reader` that advertises shipment analysis. It still must verify the worker's active workload identity, the task contract, case-specific E1 scope, applicable tenant, purpose and budget, and current suspension state. The actual data interface independently enforces read access. A registry entry cannot grant access to the payment provider, and a healthy worker cannot approve a $500 refund merely because its registry record describes a financial-analysis capability.

Registry failure also has a defined result: retain the case and its deadline in durable state, use only a previously verified worker whose eligibility is still valid under policy, or escalate. Do not treat a stale registry cache as an unlimited permission grant. The registry may be rebuilt from infrastructure or authenticated lifecycle events; **it must not be the sole copy of a case's authoritative workflow history**.

## 10.4 The ownership protocol: leases, epochs, and fencing

A practical coordination system needs a durable compare-and-set or transactional ownership mechanism. The case record tracks an **owner identity**, a **monotonically increasing ownership epoch**, a **lease deadline**, and the last accepted case-state version. A physical coordinator obtains or renews its right to advance the case using authoritative state; work accepted under an older epoch must not overwrite the newer owner's transitions. The lease tells the platform *when ownership may be reconsidered*; the epoch provides the means to **reject stale actions**. An **epoch** is an increasing ownership-generation number: if coordinator A holds epoch 7 and B takes over at epoch 8, a write carrying 7 is stale even if A later resumes. The authoritative store must check the epoch atomically with the state change; an epoch mentioned only in a message is not protection. Lamport (1978) describes distributed event ordering; Kleppmann (2017) discusses consistency and coordination limits. Neither source certifies the ETIS epoch protocol.

A lease alone is insufficient. Coordinator A can pause during a network partition, lose its lease, and resume after coordinator B has taken over. A may still hold an old token in memory. Every authoritative case update must therefore compare the caller's epoch and expected state version with the current record, refusing stale writes. At other controlled effect boundaries, corresponding fencing or fresh authorization must prevent a stale worker from causing an unauthorized consequence. An epoch stored only in an agent prompt is not fencing.

The sequence in Figure 10.2 makes this concrete. The first coordinator holds epoch 7, then loses contact. A replacement acquires epoch 8 and resumes from durable evidence. When the former owner returns, its epoch-7 update is denied. The exact lease duration and clock assumptions are deployment choices; the invariant is **no stale owner can commit an authoritative transition**.

![Figure 10.2 — A coordinator replacement advances the ownership epoch; the durable state store rejects the former owner's stale transition.](assets/shared-figures/rendered/F10-02.png){#fig:f10-02 width=5.75in}

**Important boundary:** fencing the coordinator's case-state updates does not magically guarantee exactly-once effects at an external payment provider. The trusted execution responsibility (E5), enterprise integration (E6), and durable operational state (E7) must coordinate the operation identity and recovery checks. The provider's actual idempotency and status-query guarantees must be verified independently. Distinguish the **case ownership epoch** from the **financial operation identity** `RF-1042`; replacing the former does not create a new latter.

## 10.5 Task contracts, idempotent handoff, and bounded delegation

A task assignment should carry a stable `case_id`, `task_id`, expected case-state version, ownership epoch, authenticated workload target, permitted operation and inputs, E1 scope reference, deadline, budget, and trace identity. A worker response returns a typed observation or proposal with source references, its task identity, status, and uncertainty. The coordinator validates the response against the still-current case and scope before accepting a state transition. **A worker's completion message is not itself authoritative case completion**.

A bounded investigator may perform several read-only calls, but it cannot broaden scope, choose an unregistered write tool, grant its own approval, or replace the coordinator's durable plan with an undocumented conversation. The coordinator must treat unexpected tool names, expired envelopes, malformed responses, and excessive budgets as denial or escalation conditions. Repeated delivery of a task can occur after failure; tasks should therefore be deduplicated against stable identifiers and accepted results, with any non-repeatable operation isolated behind a stronger trusted boundary.

For Design B, the coordinator requests an evidence synthesis and routes its typed recommendation for independent review. For Design C, it may assign a bounded read-only investigation loop under the same admission envelope. For Design A, a fixed rules path can complete the investigation without AI. The coordinator remains deterministic at authoritative workflow transitions across all three; model reasoning belongs to bounded worker tasks where it delivers measurable value.

| Boundary | Authoritative decision | Required evidence |
|---|---|---|
| Admit `CASE-204` | Admission and identity (E1) | Principal, tenant, case binding, allowed scope |
| Assign investigation | Coordination and ownership (E2) | Current epoch, task identity, eligible worker, budget |
| Read case evidence | Context and retrieval (E4) / source interface | Tenant and resource authorization, provenance |
| Accept advisory result | Coordination (E2), with policy/review as needed | Typed proposal, current state, source trace |
| Permit the $500 payment | Trusted execution (E5) | Current policy, approval, balance, durable intent |
| Resolve uncertain provider result | Trusted execution/integration/state (E5/E6/E7) | Same `RF-1042`, authoritative provider evidence |

## 10.6 Failure trace: the owner changes while the refund is uncertain

Consider two separate faults in the same case. First, the investigator's worker becomes unreachable while gathering evidence. The coordinator may abandon that bounded task after its timeout, preserve existing observations, and assign an eligible replacement with the current case scope and epoch. It must not accept a late answer that tries to change the case from an earlier state. The customer case remains `CASE-204` throughout; worker replacement is not a new customer request.

Later, suppose an independently authorized trusted execution path has persisted the intent for **`RF-1042`**, dispatched the $500 refund to the provider, and lost the acknowledgment. The durable payment-operation state is **UNKNOWN**. The physical coordinator crashes. Its successor may regain responsibility for the case, inspect the durable operation record, and schedule reconciliation with the same operation identity. It **must not create `RF-1043` or repeat the payment as a fresh financial operation** merely to satisfy the customer-facing workflow. The correct path is an authoritative provider status query, an applicable idempotent recovery procedure under the verified provider contract, or human escalation if the outcome cannot be resolved.

Figure 10.3 distinguishes recoverable investigation work from uncertain financial effects. A lost investigator can be safely reassigned within scope; an unknown provider outcome cannot simply be treated as a failed task. The recovery procedure must preserve that difference even if the same orchestration platform schedules both kinds of activity.

![Figure 10.3 — Recovery policy depends on the effect boundary: reassign bounded investigation, but reconcile an unknown refund outcome under the original operation identity.](assets/shared-figures/rendered/F10-03.png){#fig:f10-03 width=5.75in}

The **customer-facing status** must also remain honest. The enterprise may say that the refund is being verified; it may not say “completed” solely because the coordinator recorded a dispatch attempt. The durable system must allow a human operator to locate the current owner, epoch, financial operation identity, provider observations, pending reconciliation, and escalation path.

## 10.7 Operating model and tradeoffs

A **centralized coordinator service** can simplify authority over transitions and common monitoring, but introduces dependency, capacity, and operational concentration risks. A **horizontally scaled coordinator pool** can improve availability when backed by durable ownership and fencing; it also requires disciplined leases, worker routing, duplicate-message handling, and coherent visibility. **Peer-to-peer agents** may appear flexible, but a peer network without a durable authoritative case owner obscures responsibility and makes recovery harder. Hub-and-spoke and peer communication can both be used for *advisory* work; neither can bypass the single logical case owner and independent trusted execution.

Generalist workers reduce capability-management overhead but may increase broad-tool exposure and evaluation scope. Specialists permit narrower tools and clearer domain ownership but add routing and handoff complexity. Choose the simplest design that demonstrably meets workload, latency, recovery, security, and cost requirements. Do not introduce multiple agents merely to reproduce steps that a conventional workflow engine performs reliably.

A practical enterprise division of responsibility places registry and orchestration infrastructure with the platform engineering function; domain teams own the permitted business workflow and outcomes; security and governance define enforceable scope and policy; operations owns monitoring, incident response, containment, and recovery. The platform may detect a failed process, but only the governed workflow recovery logic decides which work is safe to reassign or resume. Human command authority to suspend work must remain available independent of the agent's cooperation.

## 10.8 Verification, assurance, and bridge to Chapter 11

Test the state machine and ownership boundaries under realistic concurrency, not only successful task routing. A credible release gate includes the following negative and recovery scenarios:

1. **Double ownership:** Force two coordinators to acquire the same `CASE-204` concurrently. Exactly one epoch/versioned transition is accepted.
2. **Stale owner:** Pause epoch-7 coordinator, transfer to epoch 8, and resume the old process. Its case mutation is rejected.
3. **Registry deception:** Register a healthy but unauthorized workload or forge capability metadata. Discovery does not grant tenant reads or payment credentials.
4. **Revoked scope:** Revoke or expire the admitted envelope during Design C investigation. Subsequent reads fail or follow explicitly documented bounded lease semantics.
5. **Duplicate task delivery:** Deliver the same task twice and inject a late response after reassignment. The case accepts at most the valid current result under the defined task contract.
6. **Lost payment acknowledgment:** Dispatch `RF-1042` under legitimate independent approval, drop the response, and restart the coordinator. No new financial identity is created; reconciliation or escalation is traceable.
7. **Operator containment:** Suspend assignment during an incident, verify new tasks stop, and confirm existing financial outcomes remain subject to reconciliation rather than disappearing.

Collect the admission and policy versions, registry registration provenance, worker identity, task IDs, ownership epochs, state versions, accepted and rejected transitions, structured result references, timing, and responsible operator. Protect customer data in logs. These artifacts support reliability, serviceability, recoverability, security, and auditability claims; none alone proves that a payment provider delivered its contractual guarantees.

**Synthesis.** Coordination and ownership (E2) ensures that admitted work has a durable, accountable path forward. A capability registry finds *possible* workers; authenticated scope determines *eligible* work; the workflow owner determines *which step advances*; the durable store determines *which transition is authoritative*. Trusted execution retains authority over financial effects, and reconciliation retains authority over uncertain outcomes. **Chapter 11** now examines the proposal contract produced by agent reasoning (E3)—a result the coordinator may consume but never treat as self-authorizing.

## Chapter 10 — Engineering practice

1. **Specify.** Model `CASE-204` as durable case state with owner, epoch, task ID, current stage, E1 scope reference, and evidence trace. Identify which facts must survive a process crash.
2. **Design.** Compare infrastructure-managed, authenticated self-registration, and supervisor-mediated registry patterns. Defend one against identity spoofing and stale readiness.
3. **Trace.** Simulate an epoch-7 owner that returns after epoch 8 takes over. Identify which storage operations and effect interfaces must reject it.
4. **Recover.** Separate the safe retry of a read-only shipment lookup from the unsafe fresh issuance of an unknown `RF-1042` payment. Explain the provider-contract assumptions.
5. **Evaluate.** Compare one coordinator process with a horizontally scaled pool. Include availability, operational complexity, throughput, observability, and cost.
6. **Defend.** Explain why a model-based supervisor's promise to “remember the current owner” is not an enforceable ownership mechanism.

**Review standard:** A defensible answer identifies the authoritative owner and state store, the fencing enforcement point, registry provenance, scoped worker contract, failure transitions, and evidence of denied stale writes. A registry diagram or happy-path multiagent demonstration is not proof of recoverability.

**Sources and further reading:** The chapter builds on the book's workflow, distributed-systems, transaction, and security foundations, including van der Aalst (2013), Lamport (1978), Gray and Reuter (1992), Kleppmann (2017), and NIST AI RMF (2023). The concrete registry fields, epoch protocol, and `CASE-204` traces are ETIS reference-design constructs; they do not assert provider-specific guarantees.
