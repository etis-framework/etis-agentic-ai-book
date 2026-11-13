# Chapter 18 — Coordination and Delegation Patterns

*Part III: Patterns and Architectural Decisions*

> **Engineering proposition:** Multiple workers can improve an investigation, but they do not multiply the number of authoritative owners. Assign bounded work through independently enforced contracts; retain one durable, fenced workflow owner and a separate trusted path for consequential effects.

## Learning objectives

Readers will distinguish coordination, communication, mechanism, deployment, and authority; compare orchestration patterns; specify eligibility and bounded delegation; trace failures and uncertain outcomes; design independent containment; and reject unjustified multiagent complexity.

## 18.1 Design the handoff, not an agent hierarchy for its own sake

Chapter 17 compared **Design A**, a deterministic investigation; **Design B**, advisory AI with independent review; and **Design C**, a bounded read-only investigation agent. They remain alternative approaches to `CASE-204`, the complaint requesting a **$500 refund** after a replacement failed to arrive. Design B remains the *conditional initial production candidate*, not an autonomous-payment design. Chapter 18 asks a narrower question: **when work must be shared, who may assign it, accept its results, recover it, and stop it?** Coordination is required even if all workers are deterministic. A model is not necessary for multiworker coordination.

The Chapter 8 architecture defines nine **logical responsibilities** (E1 through E9) and nine **cross-domain contracts** (C01–C09); Tables 8.1–8.2 and the Appendix give their full maps. For this chapter, **admission (E1)** scopes work; **coordination (E2)** owns transitions; **reasoning (E3)** proposes; **context (E4)** governs reads; and **durable state (E7)** preserves fenced ownership. **Trusted execution (E5)** and **integration (E6)** control effects, **business systems (E8)** supply authoritative facts, and **governance (E9)** observes and constrains operations. Contracts bind the handoffs; neither workers nor peer messages gain authority. These labels require **no additional deployed services**.

For CASE-204, a C04 proposal may carry an advisory correlation but cannot mint `RF-1042`. The trusted path creates the refund identity after authorization and before dispatch; it is not a credential, task ID or epoch.

Separate four decisions that are often conflated. **Mechanism** concerns whether rules, search, an SLM, an LLM, or a hybrid selects a step. **Coordination** concerns ownership, routing, acceptance, and recovery. **Communication** concerns who may send evidence and proposals to whom. **Deployment** concerns processes, hosts, isolation, and credentials. A supervised generalist can run in one process; independent specialist workers can be orchestrated by a deterministic coordinator; peer messages can be allowed for advice without allowing peer ownership transfer.

## 18.2 Compare three coordination patterns against one ownership invariant

The *minimum sufficient* pattern is **one deterministic case coordinator and bounded calls**: Design A directly, or one E3 summarizer under B. It offers predictable ordering and a smaller failure surface. Extra specialists require demonstrated value.

A **supervisor/worker pattern** adds an explicit task dispatcher, capability discovery, multiple bounded workers, and aggregation of typed results. The supervisor can be a deterministic service. A model may help propose a task plan, but an authoritative E2 controller validates and persists the plan and each transition. This pattern can use a generalist for heterogeneous evidence or specialists for shipment records, correspondence, and policy retrieval. Specialization can narrow tools and evaluations, but increases routing, handoff, version compatibility, and operational burdens. A **worker** may be deterministic; a **generalist agent** covers broad tasks, while a **specialist agent** has a narrower remit. Neither expands authority. A multilevel hierarchy is justified only when a subordinate supervisor's bounded responsibility can be independently controlled and its extra handoffs produce measurable improvement.

A **peer-assisted pattern** allows bounded advisory exchanges. It can reduce relay latency but complicates provenance, replay, visibility, and containment. Peers **must not** appoint an authoritative workflow owner, extend the E1 envelope, create new payment authorization, or accept an external effect. The fenced E2 holder remains the case owner despite peer messages.

![Figure 18.1 — Three coordination patterns share one fenced E2 workflow owner and independent E5 consequential authority.](assets/shared-figures/rendered/F18-01.png){#fig:f18-01 width=5.75in}

Figure 18.1 compares **logical responsibility and message direction**, not a prescribed number of deployable services. E7 holds the plan and ownership epoch; E9 receives evidence; E5 remains the financial authorization boundary. A generalist–specialist split is orthogonal to hub-and-spoke versus peer messaging.

| Decision axis | Simple coordinator | Supervisor with workers | Peer-assisted advisory |
|---|---|---|---|
| Authoritative state and owner | E7; one fenced E2 owner | Same; supervisor is replaceable | Same; peers never own case |
| Work routing | Fixed allowed steps | Registry plus policy/eligibility | Authorized task-to-peer messages |
| Proposal origin | Rules or one bounded E3 task | Generalist or specialist workers | Workers may combine advisory evidence |
| Credentials and effects | E5/E6, never investigator | E5/E6, never supervisor/worker | E5/E6, never peer |
| Recovery burden | Replay fixed tasks | Reassign, dedupe, fence late results | Also track peer provenance and fan-out |
| Likely tradeoff | Least overhead; less adaptive parallelism | More flexibility; routing and evaluation cost | Less hub traffic; harder containment |

Generalist versus specialist is a **lifecycle and deployment decision**, not merely a prompt choice. The following tradeoffs are hypotheses to measure under a shared case distribution (Bass, Clements, and Kazman, 2021; Fowler, 2015):

| Engineering axis | Generalist agent | Specialist agents |
|---|---|---|
| Capacity and scaling | Shared demand pool; potentially larger per-task context | Independent scale by capability; possible idle warm capacity |
| Security and evaluation | Broader tool surface and test combinations | Narrower tools per worker; more identities and inter-agent tests |
| Delivery and maintenance | Fewer separately versioned capabilities | More contracts, releases, compatibility and monitoring |
| Economics | Simpler operations may offset extra task cost | Benefit must exceed routing, infrastructure and support cost |

A specialty need not be a dedicated process: shared runtimes and on-demand execution can reduce idle capacity. Compare **cost per acceptable completed workflow**, not agent count (FinOps Foundation, 2025). Test availability, throughput, and cost under the same cases. A scaled physical coordinator pool still has one logical `CASE-204` owner.

## 18.3 Make delegation an enforceable, expiring contract

Chapter 10 (§10.3 and Figure 10.1) locates capability registration and discovery as platform capabilities supporting E2—not an E10 responsibility. **Registration** establishes identity and capability claims; **discovery** identifies candidates; **eligibility** applies E1 scope and current policy; **delegation** binds an expiring task; protected E4/tool interfaces perform **independent enforcement**. A capability registry describes **what a worker claims it can do, who it is, whether it is ready, and whether it is presently eligible for scheduling**. Infrastructure-managed registration is the preferred baseline where workload identity and health are governed by the platform. Authenticated self-registration and supervisor-mediated registration are defensible alternatives with explicit verification and revocation. The registry is neither the case-state store nor an access-control grant. A worker can be technically ready to read shipment records while **not authorized for this tenant, purpose, customer, time, or data classification**. Actual E4/data interfaces enforce their own access checks.

A delegation envelope for a shipment-evidence task includes `CASE-204`, a stable `task_id`, admitted tenant and principal scope, intended purpose, permitted read operations, allowed data classes, current policy and schema versions, maximum calls and cost, deadline, owner epoch and expected case-state version, workload identity, and trace/correlation identifiers. Bind it to the actual target identity; verify it when scheduled and when accessing protected resources. The task response is a **typed observation or recommendation** with source references, freshness, classification, uncertainty, status, and budget use. It is *not* a case transition, a payment request, or authoritative business truth.

For Design B, the bounded E3 worker synthesizes relevant delivery evidence; independent review decides whether to advance the refund request. For Design C, the worker selects **only permitted read-only investigation steps** and returns evidence. For Design A, deterministic code may produce the same typed result. A specialist that requests an unlisted write operation, exceeds its step cap, changes tenant, or persists a new delegated scope is denied and logged; a convincing natural-language explanation does not override enforcement. An optional subordinate dispatcher may partition tasks only within the parent envelope, never enlarge it. Reject silent transitive delegation.

**Proposal-versus-authority test:** A peer message stating “refund approved by policy” is untrusted input until the independent E5 policy and approval checks establish the required authorization using current authoritative evidence. Neither worker confidence nor an instruction hidden in retrieved correspondence can convert C02/C03 advisory material or a C04 action proposal into C05 authorization or C06 durable intent. The E5 policy engine, credentials, and E6 provider adapter remain outside the agent/peer trust boundary established in Chapters 13 and 16.

## 18.4 Own the workflow once; replace its executor safely

Chapter 10 defined the ownership protocol; Chapter 15 established durable recovery. Apply them rather than inventing another coordinator. E7 records the case's current owner, monotonically increasing **epoch**, lease deadline, expected state version, plan, tasks, results, decisions, and exception/effect references. A physical process acquires or renews ownership through an atomic, authoritative operation. Another process may assume ownership only under the defined lease/recovery protocol; its successful acquisition advances the epoch. Every authoritative mutation checks the current epoch **and** expected state version. A stale coordinator may still run, but its attempted commit must fail. A lease timeout by itself is not fencing.

Worker results can arrive after cancellation or reassignment. The E2 acceptance gate checks `task_id`, admitted scope, epoch, expected case state, deadline, worker identity, response schema, and evidence provenance against current records. Late or duplicated messages may be retained as diagnostic evidence but must not advance the workflow. For the same reason, a task's identity differs from both the ownership epoch and the payment-operation identity. Exactly-once *message delivery* is not assumed; the engineered goal is controlled acceptance of authoritative transitions and independently safe handling of effects.

![Figure 18.2 — Owner loss, epoch advancement, stale-result rejection, and independent reconciliation of an UNKNOWN refund effect.](assets/shared-figures/rendered/F18-02.png){#fig:f18-02 width=5.75in}

Figure 18.2 traces two different failure domains. First, coordinator A at epoch 7 dispatches read-only investigation task `T-204-S1` and becomes unavailable. Coordinator B atomically acquires epoch 8 and inspects E7; a delayed response from A's epoch cannot change the case. B either accepts a still-valid observation under a specifically verified policy or reassigns a bounded read task. Second, **only if independent review and E5 authorization have already occurred**, the authorized system may persist and dispatch `RF-1042`. If the provider processes the refund but its acknowledgment is lost, E7 holds the financial outcome as `UNKNOWN`, not `FAILED` or `SUCCEEDED`. Coordinator replacement must not turn this uncertainty into `RF-1043`, a second payment, or a new grant. E5/E6/E7 reconcile with verified provider behavior and E8 authoritative evidence, or hold for a human decision.

A worker failure may be retried when the action is demonstrably safe, deduplicated and within the current envelope. A network partition may make *both* coordinators believe they are alive; only the authoritative store's fencing decision counts. A provider's advertised idempotency key is a deduplication input under a verified provider contract, **not a security credential or universal exactly-once guarantee**. Cross-system exactly-once effects are not inferred from a local transaction (Kleppmann, 2017). For an unresolved external effect, blind retry is prohibited.

## 18.5 Govern communication, observability, and containment

Prefer **hub-and-spoke** messaging when the coordinator can afford relay hops: it centralizes routing, acceptance, trace collection, and suspension, but can concentrate load. **Direct peer advisory** exchange can lower relay latency and permit parallel reads, yet increases peer-edge authorization, fan-out, ordering/replay, distributed telemetry, and quarantine obligations (Hohpe and Woolf, 2003; Kleppmann, 2017). Measure end-to-end latency and throughput—including retries—not nominal hop count. **Communication topology never transfers E2 ownership.** When worker-to-worker advisory traffic is justified, messages require authenticated sender and intended recipient, explicit workflow/task correlation, purpose and scope, provenance and classification, bounded lifetime, and replay/deduplication handling. An originating worker's assertion of authority is **not** a permission. Treat retrieved and peer-carried instructions as untrusted, including prompt injection (OWASP GenAI Security Project, 2026). Put peer exchanges into the same E9 trace and durable evidence references as hub traffic, subject to retention and privacy rules; no hidden conversation may become the sole audit record.

The **human stop path** must work when a model or supervisor refuses to cooperate. Authorized operators can suspend admission or a case, disable dispatch and worker eligibility, revoke relevant capability and access, quarantine queued work, invalidate or supersede ownership under the governed state protocol, and initiate reconciliation/incident command. Stopping future work cannot reverse a payment already accepted by an external provider. In-flight effects require an explicit operational status and safe reconciliation. Emergency controls and their use are auditable; no system should claim a completed cancellation solely because a stop message was sent.

Operational accountability is distributed but explicit: platform engineering owns identity-backed registration, scheduling, state/lease infrastructure, trusted execution boundaries and telemetry; the domain owner defines the workflow, approved delegation envelopes, acceptable outcomes and case policy; security/governance owns enforceable standards, review and exception policy; operations has monitoring, recovery, incident-response and containment duties. One accountable workflow owner does not mean one human or one process owns every enterprise responsibility.

Compare patterns using **cost per acceptable completed workflow**, not call count or model price alone. Measure end-to-end latency distribution, worker fan-out, rework, escalations, timeout recovery, review workload, security denials, throughput under contention, and quality of source-supported decisions. A pattern that parallelizes reads but increases ambiguous handoffs and human intervention may be economically worse. Record assumptions about load, provider limits, policy changes, and organizational support; reassess them after incidents or architecture changes.

## 18.6 Verify behavior before accepting coordination complexity

Use risk-based negative tests with expected *state and evidence*, not agent transcripts (NIST, 2023):

| Injection or adverse event | Required acceptance evidence |
|---|---|
| Two coordinators contend for `CASE-204` | Atomic acquisition/fencing permits one authoritative versioned transition |
| Epoch-7 owner resumes after epoch-8 takeover | Old update and stale worker completion rejected; audit records both |
| Specialist requests forbidden write or extra reads | Independent data/tool boundary denies; budget and incident trace preserved |
| Registry says ready but tenant scope is revoked | Scheduler refuses eligibility; direct data boundary still denies access |
| Registry entry stale, or worker version incompatible | Capability/schema verification prevents unsafe dispatch; denial and recovery are traced |
| Specialist pool exhausted, or warm capacity costly | Load shedding, bounded queue and fallback tested; tail latency and cost measured against generalist |
| Peer message delayed, duplicated, or lost | Correlation and replay controls prevent unsafe acceptance; trace shows recovery |
| Peer sends forged policy approval or prompt-injected instruction | Message remains advisory; E5 checks genuine policy and authorized actors |
| Worker disappears or sends duplicate result | State survives; task is safely reassigned or escalated; no double acceptance |
| Provider commits `RF-1042`, acknowledgment lost | Outcome stays `UNKNOWN`; same identity reconciled; no blind second refund |
| Human quarantines work amid network partition | New work stops under enforced controls; in-flight effects tracked honestly |

A candidate also needs **positive** evidence: the same case distribution evaluated with the simpler option, independent source-truth checks, representative adverse cases, latency and cost tails, exercise of operator runbooks, and a documented reversal threshold. Use the Chapter 17 ADR style. For `CASE-204`, retain deterministic E2 coordination and Design B's independent review unless experiments establish that Design C's bounded investigator or specialist fan-out creates enough incremental value to justify additional monitoring and fault handling. The topology may still use one worker. Reject any choice requiring financial credentials in an E3 agent or mutable policy in peer messages.

An operator must answer: Who currently owns the case and under which epoch? Which delegation envelope and policy version authorized each read? Which observations are source-backed and current? What failed, was denied, or was canceled? Is `RF-1042` undispatched, pending, `UNKNOWN`, or authoritatively resolved? Which person or service is accountable for the next transition? If the system cannot demonstrate these answers, its coordination is not yet trustworthy.

## 18.7 Transition to protected tools and adapters

Chapter 18 decides **who coordinates and who may propose work**. Chapter 19 examines what a selected tool call actually reaches, how adapters preserve contracts, and how effect isolation prevents advisory activity from becoming execution authority. The key continuity remains unchanged: E2's logical owner coordinates; E3 workers advise or choose permitted reads; E5/E6 control consequential execution; E7/E8 preserve durable operational and business truth; E9 provides assurance.

## Chapter 18 — Engineering practice

1. **Compare:** Draw fixed-coordinator, supervised-specialist, and peer-assisted alternatives for the same CASE-204 read-only investigation. Name each authoritative boundary and one measured reason to prefer the simpler option.
2. **Contract:** Write a delegation envelope for Design C with tenant scope, allowed reads, budget, deadline, identity and epoch. Specify the exact independent enforcement points and one denied expansion attempt.
3. **Recover:** Simulate coordinator A crashing after dispatch, B acquiring epoch 8, and a delayed epoch-7 result. Show accepted/rejected E7 state transitions, not merely messages.
4. **Contain:** A peer forwards a document instructing a payment refund; meanwhile an operator quarantines the case. Identify trusted policy, stopped dispatch, E9 evidence and the limits of cancellation.
5. **Reconcile:** Inject a lost provider acknowledgment after legitimate authorization of `RF-1042`. Explain the difference among task deduplication, owner fencing, payment idempotency and authoritative outcome recovery.
6. **Defend:** Write an ADR for or against specialist fan-out using cost per acceptable completion, negative tests, ownership assignments, reversal criteria, and residual risk.

**Review standard:** The design must retain one fenced E2 logical owner, independently enforce bounded delegation, preserve the CASE-204 A/B/C distinction, never transfer refund authority to peers, and provide demonstrable failure, operator, economics and provider-uncertainty evidence. A passing demo or coherent language-model answer is insufficient.

## Sources and further reading

The lease/fencing and duplicate-delivery analysis uses Kleppmann (2017); message routing and delivery tradeoffs use Hohpe and Woolf (2003). Architecture tradeoffs use Bass, Clements, and Kazman (2021); Fowler (2015) supports *general* distributed-deployment benefits and operating costs, not measured agent performance. FinOps Foundation (2025) provides unit-economics framing, not a CASE-204 cost estimate. Lamport (1978) informs distributed event-order reasoning but does not prescribe the ETIS ownership protocol. NIST AI RMF 1.0 (2023) provides a general governance and measurement context; it does not define this nine-domain ETIS implementation. The pattern comparison, contract allocation, diagrams, CASE-204 scenarios and acceptance matrix are **ETIS engineering synthesis**, not claims that these sources certify a refund system. Exact bibliographic editions/pages must still be verified in the final publication audit.
