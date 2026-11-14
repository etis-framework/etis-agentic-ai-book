# Chapter 20 — State, Memory, and Knowledge Design

*Part III: Patterns and Architectural Decisions*

> **Engineering proposition:** Remembering something does not make it true, current, permissible to reuse, or authoritative. A trustworthy agentic system assigns separate owners and controls to transient reasoning context, derived memory, durable workflow state, organizational knowledge, and business systems of record.

## Learning objectives

By the end of this chapter, readers should be able to classify information by authority and lifetime; compare retrieval, case-scoped memory, and persistent state patterns; design provenance, freshness, correction, and revocation controls; separate durable operational state (E7) from authoritative business truth (E8); and specify negative tests for replay, tenant leakage, stale policy, and uncertain outcomes.

## 20.1 The information boundary after effect isolation

Chapter 19 established that a discoverable tool is not authorization: **trusted execution (E5)** and **enterprise integration (E6)** independently constrain financial effects. Chapter 20 asks a different question: **which information may a worker remember, reuse, or regard as authoritative?** Chapter 12 established **governed context and retrieval (E4)**; Chapter 15 established **durable operational state (E7)** and assurance. Here we compare information patterns and their authority boundaries. The full E1 through E9 responsibility map and C01–C09 contract names are in Chapter 8 and the Appendix; this chapter defines the relevant owners in place, without requiring separate services.

The same customer in `CASE-204` reports that a replacement has not arrived and requests a **$500 refund**. **Design A** uses deterministic evidence checks, **Design B** uses advisory interpretation with independent review and remains the conditional initial production candidate, and **Design C** optionally delegates a **read-only** investigation to a bounded agent. These are competing architectures, not progressive autonomy levels. A cached statement of shipment status cannot authorize payment. If a refund is independently approved, E5 establishes the trusted operation `RF-1042`; E6 manages its provider integration, E7 records the operation's known and unknown progress, and E8 supplies authoritative business facts. No memory tier can create `RF-1042` or turn `UNKNOWN` into `CONFIRMED`.

A design needs to distinguish **information content** (what an item says), **provenance** (who supplied it and when), **authority** (which system may establish a business fact), **scope** (which principal, case, or purpose may use it), and **lifetime** (when it expires or must be corrected). These attributes are independent. A fresh answer from an untrusted email is not authoritative; an authoritative record copied into an old summary can become stale.

## 20.2 Five information classes, five different obligations

The word *memory* can obscure incompatible guarantees. We retain Chapter 12's definitions but make the resulting architecture decision explicit. **Inference context** is the bounded information supplied to a particular model call; it can include trusted instructions and separately labeled untrusted evidence. **Agent working memory** is a temporary plan or scratchpad across permitted steps. **Derived case memory** is a retained summary, observation set, or decision aid linked to a case. **Organizational knowledge** comprises versioned policies, procedures, documents, and searchable indexes. **Durable operational state** (E7) records authoritative workflow ownership, tasks, epochs, approvals and financial-operation observations; **business truth** (E8) resides in designated customer, order, payment and provider systems. The last two are not agent memory.

| Information class | Owner and expected lifetime | Can establish | Must not establish |
|---|---|---|---|
| Inference context / scratchpad | E3 task; bounded step or session | Candidate reasoning steps | Policy, case ownership, financial outcome |
| Derived case memory | Governed case evidence store; explicit retention | Prior observations with source links | Freshness or business authorization by itself |
| Organizational knowledge and retrieval index | Domain/data owner via E4; versioned | Candidate applicable policy or reference | That an old copy is current or a fact is settled |
| Durable E7 state | E7 with E2/E5 controls; recoverable | Owner epoch, task transitions, recorded intent and observation | Provider business settlement without E8 evidence |
| Authoritative business state | E8 system of record | Captured/refunded balance and provider outcome within its contract | Agent task completion or free-form memory claims |

**Storage consolidation is not authority consolidation.** One database may hold case notes and durable state with distinct schemas, writers, access controls, validation and retention. Conversely, a vector database in a separate service does not become an authoritative system merely because it is operationally independent. Choose the simplest storage topology that enforces the necessary semantics (Kleppmann, 2017; Bass, Clements, and Kazman, 2021).

![Figure 20.1 — Information classes have distinct owners, authority, and correction paths.](assets/shared-figures/rendered/F20-01.png){#fig:f20-01 width=5.75in}

Figure 20.1 is an **authority and information-use map**, not a linear runtime sequence. E4 can return scoped evidence to E3; E7 and E8 remain separately controlled. The distinction between derived information and independently checked business facts is deliberate: relevance ranking, summary confidence, and model fluency are never proof of current authorization.

## 20.3 Compare retrieval, persistent memory, and direct authoritative reads

For a bounded complaint investigation, three patterns are plausible. **On-demand retrieval** reads current, scoped sources for each case or question. It minimizes retained derived state but may increase latency and query load. **Versioned case memory** caches a governed summary with links to its supporting originals; it can reduce repeated work but requires expiry, correction, scope binding, and invalidation. **Direct authoritative queries** obtain a fresh balance or payment status from E8 through permitted read interfaces; they are often required for consequential decisions but may have higher integration cost or provider latency. Retrieval-augmented generation (RAG) demonstrates a method for supplying documents to a model, not a guarantee that retrieved content is correct, authorized, or current (Lewis et al., 2020).

| Pattern | When it helps | Failure exposure | Required validation |
|---|---|---|---|
| Scoped retrieval each time | Frequently changing facts, low reuse | Source outages, ranking errors, cost | Identity/scope, freshness and source provenance |
| Governed case memory | Repeated investigations within one case | Stale or contaminated summaries, retention | Source-linked invalidation, version, purpose and TTL |
| Authoritative E8 read | Refundable amount and confirmed effect | Network uncertainty, provider semantics | Signed/authenticated source, version and observed status |

For Design B, the few necessary records can be retrieved and summarized for independent review; retaining model conversation history indefinitely adds risk without proven value. Design C may benefit from short-lived task scratch state to avoid duplicate investigative reads. Its scratchpad is not an E2 ownership lease, an E5 approval token, or an E7 operation ledger. The choice is measured against investigation quality, replay safety, latency, privacy, rework, and cost per acceptable completed case, not against the size of a vector index.

### Freshness is a requirement, not a timestamp alone

A timestamp describes when a source was observed; **fresh enough** depends on the decision. A policy excerpt can be unsuitable immediately after revocation, even if retrieved minutes ago. A shipment observation may be useful for investigation but insufficient to justify a payment when a newer delivery update exists. A payment balance must be checked under the E8 authority and consistency guarantees required at the E5 decision point. Every reused derived item should carry source ID and version, observed-at time, intended use, tenant/case scope, policy classification, and a validity or recheck rule. A confidence score does not substitute for any of them.

## 20.4 Correction, revocation, and deletion are different operations

**Correction** records a new supported interpretation and supersedes a wrong summary; it does not rewrite history to suggest the old summary never influenced a prior decision. **Invalidation** prevents further use of a superseded or untrusted derived item until revalidated. **Revocation** removes a principal or task's authority to access information, even if the underlying record remains valid. **Deletion** or retention expiry removes data according to legal and organizational obligations, subject to controlled evidence holds. These operations have separate owners and observable outcomes.

A case-memory entry should have an identifier, immutable source references or auditable source-version links, derived-content version, subject and tenant scope, classification, creation time, expiry and invalidation status. When an upstream record changes, the system must locate affected cached results, invalidate or refresh them, and decide whether an in-progress proposal needs review. For example, a shipment source now reports **delivered** after an earlier exception; the agent cannot simply reuse its old “not delivered” summary. E4 enforces access to the new source and its derived copies; E2 reopens or holds tasks when necessary; E5 rechecks current authoritative preconditions before any financial effect.

Revoking access does not erase data already disclosed to a model or an external processor. The system must stop new reads and new reuse, apply contractual retention and deletion controls where supported, preserve required incident evidence appropriately, and avoid promising retroactive forgetting. This is a concrete privacy and incident-response requirement, not a property automatically provided by a memory framework (NIST AI 100-1, 2023; Rose et al., 2020).

## 20.5 Recovery depends on state, not remembered prose

E2 retains **one logical coordinator owner** for `CASE-204` while physical coordinators may be replaced. E7 persists owner epoch, task status, accepted proposals, limits, cancellation and evidence references. A worker's note that “I own this task” cannot win against E7's authoritative epoch and compare-and-set enforcement (Chapters 10 and 15). A new owner must reject stale task results and reconstruct the outstanding work from durable state, not from an agent's conversational recollection.

Similarly, `RF-1042` belongs to the independently authorized consequential path. After possible provider dispatch, a lost acknowledgment means the local operation is `UNKNOWN` until reconciled under C07/C08 with E8 truth. A summary claiming “refund succeeded” neither closes the operation nor permits a new `RF-1043`. E7 records the observation and uncertainty; E8 supplies business evidence; E5/E6 determine whether any further action is independently permissible. The conceptual map does not claim one synchronous E1-to-E9 call sequence; E9 governance evidence is cross-cutting (Gray and Reuter, 1992; Kleppmann, 2017).

![Figure 20.2 — Stale case memory is invalidated while durable ownership and refund identity remain independent.](assets/shared-figures/rendered/F20-02.png){#fig:f20-02 width=5.75in}

Figure 20.2 is a **behavioral sequence** distinct from Figure 20.1's structural classification. It follows a changed shipment observation, cache invalidation, a rejected stale worker result, and protected refund-state reconciliation. The two changes are independent: superseded evidence can force a new investigation; it does not automatically mutate an already dispatched financial outcome.

## 20.6 Governance, observability, and an explicit state design decision

An architecture decision record should identify each information class's authoritative writer, readers, retention and permissible purpose, consistency assumptions, invalidation trigger, encryption and access policy, audit evidence, and recovery owner. It should record why an index, case memory, or direct read is needed and what smaller alternative was rejected. E9 governance must bind to E1/E4 read admission, E2/E7 workflow changes, E5 effect authorization, and operational containment, not merely receive logs after data has been exposed.

For `CASE-204`, the defensible initial choice is **scoped retrieval plus minimal derived summary for Design B**, while E7 and E8 remain authoritative for their respective state classes. Add persistent case memory only if repeat-use measurements show enough value to justify correction, tenancy isolation, retention, and operational cost. Optional Design C can use bounded ephemeral task state but must not acquire payment keys or authority. The decision should include an explicit policy for ambiguous or unavailable sources: hold, fetch another permitted source, or escalate, rather than fabricate a confident answer.

### Negative tests and acceptance evidence

| Failure injection | Expected invariant | Evidence |
|---|---|---|
| Cross-tenant retrieval or cached hit | Denied before disclosure, including index metadata | E1/E4 scoped denial trace |
| Injected instruction in policy excerpt | Treated as data; cannot change tools or E5 approval | Input provenance and tool-denial trace |
| Policy version revoked after caching | Invalidated or rechecked before new decision | Version/invalidation audit and held proposal |
| Shipment status changes mid-investigation | Stale summary not accepted as current fact | Source comparison and re-evaluation |
| Owner epoch changes with stale worker reply | E7 rejects stale state mutation | Epoch/fencing failure record |
| Provider times out after possible dispatch | `RF-1042` stays `UNKNOWN`; no new effect | Intent record, provider query, reconciliation evidence |
| Human cancels work or access expires | No new task reads or effect dispatch | Stop, revocation and in-flight outcome record |

Run these tests with source versions and controlled time; otherwise a passing happy-path run says little about revocation or races. Evaluating a model's answer is necessary but different from verifying access denial, state integrity, business effect and privacy compliance. Chapters 24 and 26 will implement relevant scoped context and reconciliation examples; Chapters 28–31 will test distributed failure, misuse, and end-state evidence. Those chapter references identify the intended implementation and verification work; only executable results, with their assumptions, constitute proof.

## Chapter 20 — Engineering practice

1. **Classify.** Label the authoritative owner, TTL, scope, provenance and correction path for order data, shipment evidence, model scratchpad, policy excerpt, E7 workflow epoch, and `RF-1042` status.
2. **Compare.** Defend on-demand retrieval versus governed case memory for Design B under changing shipment facts; quantify latency, privacy, support effort, and rework assumptions.
3. **Design.** Specify a case-memory record with source versions, tenant, purpose, invalidation, retention and denied reuse semantics. Explain why a vector embedding is not business truth.
4. **Trace.** After a policy revocation and coordinator replacement, show which derived items are invalidated and which durable records survive. Reject one stale worker update.
5. **Verify.** Construct negative tests for cross-tenant cache leakage, malicious retrieved text, conflicting E8 facts, and a lost provider acknowledgment. Identify the evidence needed to hold rather than release.

**Review standard:** Strong responses distinguish information relevance from business authority, derived memory from E7 ownership, a local observation from E8 truth, and proposal correlation from `RF-1042`. They select the minimum necessary persistence and define failure behavior that remains correct without trusting model recollection.

**Sources and further reading.** Kleppmann (2017) on consistency, data ownership, and distributed failure; Gray and Reuter (1992) on transaction/durable-state foundations; Lewis et al. (2020) on RAG; Bass, Clements, and Kazman (2021) on architecture tradeoffs; NIST AI RMF (2023) and Rose et al. (2020) on governance and access controls. These sources do not validate a particular ETIS memory schema, payment-provider behavior, or operational deployment. The classification, diagrams, and CASE-204 decision are original ETIS engineering synthesis; exact edition/page review remains open.
