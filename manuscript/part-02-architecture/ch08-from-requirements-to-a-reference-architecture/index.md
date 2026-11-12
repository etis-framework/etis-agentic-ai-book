# Chapter 8 — From Requirements to a Reference Architecture

*Part II: Enterprise Reference Architecture*

> **Engineering proposition:** A reference architecture is a map of responsibilities, contracts, and independently enforceable trust boundaries. It is not a vendor diagram, an agent framework, or proof that the system is safe.

## Learning objectives

By the end of this chapter, readers should be able to (1) translate Chapter 7's requirements into logical responsibilities and acceptance evidence; (2) distinguish a logical architecture from its physical deployment; (3) read the nine enterprise domains without mistaking their names for nine services; (4) identify the independent authorization and financial-effect boundary; (5) compare the architectural implications of Designs A, B, and C; and (6) critique an architectural view using negative paths and operational recovery.

## 8.1 The transition from obligation to structure

Chapter 7 established what must be true of a trustworthy system: `AUTH-01` excludes AI-originated payment capability; `DATA-01` demands tenant isolation; `POL-02` demands independent checks at execution; `PAY-03` treats an uncertain provider outcome as unresolved rather than failed; and `OPS-01` requires operable containment and recovery. Chapter 8 asks **where those obligations are enforced, what crosses each boundary, and what evidence can establish that enforcement works**. Later chapters make the interfaces and failure handling concrete. A diagram alone cannot satisfy any of these requirements.

The running case remains `CASE-204`: a customer reports a missing replacement and requests a **$500 refund**. Design A is a deterministic comparison baseline. Design B is the *conditional initial production candidate*: AI helps prepare an advisory proposal, while independent trusted workflow and authorized people or services decide and execute. Design C is an *evaluated, read-only investigator*, not a payment agent. `RF-1042` is an illustrative stable payment-operation identity; it does not establish a particular provider's idempotency guarantees.

A useful architecture must support all three designs without silently widening the AI's authority. The difference among A, B, and C lies primarily in how evidence is assembled and proposals are produced, not in who can issue the financial effect.

## 8.2 Three views of the same system

A **logical responsibility view** names the functions that must exist and the invariants they own. A **contract view** specifies typed inputs, outputs, identity, versioning, denial semantics, and ownership of a handoff. A **deployment view** places those responsibilities in processes, networks, accounts, databases, and operational teams. These views answer different questions. The same logical responsibility might be implemented in one process or several; co-location never removes the need for independently enforceable authorization. Architectural responsibility, contract, and deployment views follow established quality-attribute and design-view practice (Bass, Clements, and Kazman, 2021); the nine-domain grouping itself is an original ETIS synthesis.

The first view should be understandable without a cloud provider. The second should make failures and untrusted inputs visible. The third should be derived only after considering threat boundaries, scaling, failure domains, latency, recovery, and economics. Drawing nine boxes and deploying nine microservices is not architectural rigor; it is premature implementation commitment.

**Target-state roadmap.** The nine responsibility domains are one coherent logical architecture, not a staged installation plan. Figure 8.1 is the canonical Part II layered logical reference architecture: enterprise admission (E1), coordination with bounded advice and context (E2/E3/E4), independent trusted authorization and integration (E5/E6), and external systems with authoritative business truth (E8). Vertical E7 and E9 rails span these layers as durable-state and assurance responsibilities rather than additional processing stages. The diagram distinguishes logical interactions from permitted consequential authority; external payment effects remain outside the reasoning boundary. Section 8.3 defines each domain, Chapters 9–15 develop the contracts, and Chapter 16 examines physical placement without loosening those contracts. The figure is **a proposed architecture to verify**, not proof that a deployment is trusted.

![Figure 8.1 — Canonical layered target-state logical reference architecture. E1 through E9 are logical responsibilities rather than nine services or a call sequence. E7 and E9 span the layers; E5 independently guards E6 and external effects; E8 denotes authoritative business facts, not agent claims.](assets/shared-figures/rendered/F08-01.png){#fig:f08-01 width=5.75in}

**Read the four architectural layers from enterprise admission to externally grounded business truth, not as a required request sequence.** Admission binds the requester and case; the durable workflow owns the investigation and review; one of A, B, or C supplies structured evidence or a recommendation; the governed decision path checks authority; the operation journal and payment adapter control the actual attempt. Authoritative business records support policy checks, and assurance observes the process. Figure 8.1 maps the complete target-state architecture; Figure 8.2 then isolates the alternative investigation and consequential-effect boundaries.

**What is “untrusted” here?** It refers to the *authorization status of the generated information*, not the provenance of every line of the agent runtime. An enterprise may write and secure the agent controller itself. The model may nevertheless misunderstand a message, use stale context, invent a fact, or follow an instruction hidden in retrieved material. Even a correct proposal has no payment privilege. The trusted controller and execution path are conventional, governed software that must independently validate the proposal against authoritative facts. Deterministic code can have bugs, so “trusted” is a *testable control responsibility*, not a claim of infallibility.

Figure 8.2 isolates the alternative investigation designs within that responsibility map. It does not give the AI payment credentials, imply that A/B/C execute in sequence, or certify the implementation.

![Figure 8.2 — Alternative investigation designs produce non-authoritative evidence or proposals; independently controlled authorization and durable intent precede any external financial effect.](assets/shared-figures/rendered/F08-02.png){#fig:f08-02 width=5.75in}

The diagram's separation is not cosmetic. A read-only case tool must not hide a write parameter, and a model-selected name must not map to a privileged payment endpoint. **The agent cannot hold the provider payment key or reach an unguarded payment door**; even a valid service credential must not become refund authority. A workflow approval does not replace effect-time authorization. Deployments sharing a process still need credential isolation, protected entry points, and tested bypass denials. Chapter 13 makes those controls concrete.


The architecture distinguishes **observing** a case, **proposing** a decision, **authorizing** an effect, **recording** intent, and **observing** the effect's outcome. Those are different kinds of state. A model's explanation cannot convert one into another. The architecture must also keep the external provider's report separate from the enterprise's own authoritative case and operation records.

## 8.3 Nine domains, not nine mandatory services

The approved reference architecture groups responsibilities into nine enterprise domains. The identifiers are navigation aids; the names and responsibilities are what matter.

| Domain | Primary responsibility | Key boundary or evidence |
|---|---|---|
| **E1 — Admission and identity** | Authenticate principal, bind tenant and permitted goal | Rejection of invalid or out-of-scope work |
| **E2 — Coordination and ownership** | Own work, deadlines, dispatch, and recovery handoffs | Durable owner and fenced transition |
| **E3 — Agent reasoning** | Analyze scoped evidence and return typed proposals | No financial credential or effect route |
| **E4 — Context and retrieval** | Retrieve purpose-scoped, attributable evidence | Tenant scope, provenance, freshness |
| **E5 — Trusted execution** | Independently validate policy, approval, and preconditions | Denial or authorized durable intent |
| **E6 — Enterprise integration** | Isolate adapters and provider-specific semantics | Correlation, timeout, status query |
| **E7 — Durable operational state** | Preserve work, intent, attempts, and outcomes | Reconstructable state and operation identity |
| **E8 — Business truth** | Maintain authoritative business facts and case status | Distinguish claims from confirmed records |
| **E9 — Assurance and operations** | Audit, monitor, contain, and recover | Evidence, alerts, runbooks, accountable owners |

These domains must not be confused with a pipeline of nine successive model calls. E7 and E9 are cross-cutting responsibilities; E4 supplies evidence but cannot authorize effects; E8 holds business truth but does not turn a generated statement into truth. E5 remains the trusted action boundary even when implemented alongside another domain. In Figure 8.1 the architecture is read as relationships among responsibilities, not as a linear chain. Chapter 9 begins the detailed contract sequence at admission; Chapters 10–15 develop the remaining domains; Chapter 16 maps logical boundaries to deployment.

A sound decomposition allocates each requirement to an **enforcer**, an **observer**, and an **acceptance oracle**. For `AUTH-01`, E3's missing credential and absent payment-capable tool surface are structural enforcers; E5 and the gateway reject unauthorized calls; E9 records denials; negative tests verify these properties. Merely putting “no refunds” in the system prompt is not an enforcer.

## 8.4 A contract is more than a message schema

A contract identifies the producer and consumer, the authorized principal, the scope and versions, the permitted state transition, and what happens on rejection, delay, duplication, or missing acknowledgment. A typed proposal might include a case identifier, evidence references, a suggested disposition, a confidence or uncertainty description, and a producer version. It must not include an executable payment credential or masquerade as a signed approval. Messaging and integration contracts provide useful background (Hohpe and Woolf, 2003), while the particular ETIS boundaries remain design prescriptions.

A trusted effect request requires different evidence: the authorized principal, case and tenant, current policy and approval, amount, operation identity, durable intent, and an auditable outcome. The authorization decision must be revalidated at the consequential boundary rather than inferred from a previously successful read or from the proposal's plausibility.

| Chapter 7 obligation | Logical enforcer | Essential negative test |
|---|---|---|
| `DATA-01` | E1 scope binding plus E4/E8 scoped access | Cross-tenant retrieval and identifier substitution denied |
| `AUTH-01` | E3 capability isolation and E5 authorization | Agent attempts direct refund or tool escalation; denied |
| `POL-02` | E5 current policy, principal, and approval validation | Approval revoked or amount changed; execution denied |
| `PAY-03` | E5/E6 operation protocol with E7 durable journal | Lost acknowledgment; no blind new operation |
| `OPS-01` | E2/E7/E9 ownership, stop, and reconciliation controls | Operator can contain and trace an unresolved operation |

These allocations are architectural hypotheses until code, configuration, fault injection, and operational drills provide evidence. A failed negative test may reveal a missing boundary, an inadequate contract, or an implementation defect; it is not fixed by changing the caption.

## 8.5 The consequential-effect boundary

The most important cut in the refund architecture is between **non-authoritative advice** and **independently authorized consequential execution**. A recommendation is data supplied to a governed decision process, not executable permission. This is different from a simple “probabilistic code versus deterministic code” distinction: the agent runtime can contain trusted deterministic controllers, while a conventional program can be insecure or incorrectly authorized. The boundary is defined by **who may decide, enforce, persist, and dispatch**, and by the evidence of those actions.

For `CASE-204`, Design B's advisory model might propose a $500 refund with references to shipment, payment, and policy evidence. A reviewer or properly authorized workflow checks whether those references are correct and current. The review produces a separately attributable approval or denial. The trusted execution service must then recheck the applicable authorization, amount, scope, and operation state, rather than taking the recommendation or approval text at face value. A proposal never contains a payment-capable secret and has no direct route to the adapter.

The proposal may say that a $500 refund appears appropriate. A reviewer or separately authorized policy workflow may reject it, request more evidence, or authorize it under current rules. Only then may the trusted service record a durable operation intent and use the payment adapter. Neither the agent nor its retrieval tools should possess the capability to initiate that operation.

Figure 8.3 follows the consequential path **after an authorized reviewer or policy decision**, including the case that is easy to omit from a happy-path architecture: a provider acknowledgment can be lost after the provider has performed the effect. The local payment-operation state is then `UNKNOWN`, not `FAILED`; the broader case may remain `OUTCOME_UNKNOWN`. Reconciliation uses the same illustrative identity `RF-1042` and provider-supported correlation or status mechanisms. If the provider cannot establish the outcome, the workflow escalates to an accountable operator. No new operation is inferred to be safe merely because the first call timed out.

![Figure 8.3 — Distinct proposal, authorization, and payment-effect paths; lost acknowledgment enters UNKNOWN and requires reconciliation or escalation, not blind resubmission.](assets/shared-figures/rendered/F08-03.png){#fig:f08-03 width=5.75in}

An architecture review should ask who can bypass the gate, what credentials are reachable from the reasoning runtime, where the durable record is written relative to provider dispatch, and how the operator determines the next safe action after a crash. These questions apply even when a model is not used; the agentic component increases the range of proposals, not the permitted range of financial effects.

## 8.6 Compare A, B, and C without confusing alternatives with stages

**Design A** uses deterministic eligibility and evidence checks. It is a necessary performance, cost, and reliability baseline; it can still require the same trusted approval and payment controls. **Design B** adds advisory AI to summarize and explain evidence while keeping independent review and trusted execution. It remains the initial production candidate, conditional on measured quality and operating controls. **Design C** permits bounded, read-only investigation across approved sources, potentially improving ambiguous cases but increasing tool-selection, provenance, latency, and attack-surface risks. C is an alternative to evaluate against B, not the next automatic step after B.

All three share the consequential boundary. For B and C, evaluation should measure unsupported assertions, missed contradictions, reviewer burden, escalation behavior, tenant-scope violations, and incremental business value. The relevant architecture decision is not “which agent framework is strongest?” but “which minimal reasoning capability materially improves the outcome without eroding enforceable boundaries?” Chapter 17 will formalize that choice; Chapter 5's economic assumptions remain provisional until observed.

## 8.7 Architectural review before implementation

A reviewable architecture package contains: a responsibility map, a contract inventory, trust-boundary decisions, a requirement-to-enforcer trace, an explicit account of negative paths, and a deployment decision log listing assumptions not yet validated. For the refund case, reviewers should be able to locate the rejection path for a cross-tenant case, the denial of an agent-originated payment call, the treatment of stale approval, the durable record of `RF-1042`, and the operator's recovery route.

Architecture evidence and runtime evidence are not interchangeable. The figures in this chapter communicate intended separation; only subsequent implementation tests, access-policy inspection, provider fault injection, and operational exercises can demonstrate that the system enforces it. Do not mark an architecture accepted merely because a diagram has the right colored boxes.

**Architecture review verdict for the continuing case.** The design is acceptable as a *candidate logical decomposition*, not as an authorized production system. The minimum release-blocking tests include cross-tenant read denial; model-to-payment route denial; changed or revoked approval denial; stable-operation duplicate suppression under the documented provider contract; lost-acknowledgment reconciliation; and operator containment. If the provider cannot support authoritative status resolution, the system must preserve a human-owned unresolved state rather than claim completion.

The next eight chapters decompose the target-state logical architecture in Figure 8.1: admission (9), coordination (10), proposals (11), context (12), authorization (13), integration and business truth (14), state and assurance (15), and deployment boundaries (16). The later pattern, build, verification, and governance parts will use the same case and invariants rather than introducing a more permissive agent by stealth.

## Chapter exercises

1. **Trace.** For `AUTH-01`, name the enforcer, evidence artifact, adversarial test, and release consequence. Explain why a prompt is insufficient.
2. **Separate views.** Sketch one-process and multi-service deployments of the same nine logical responsibilities. Identify which trust controls must survive co-location.
3. **Compare alternatives.** Build a three-column decision record for Designs A, B, and C, including evidence quality, reviewer load, added tool risk, and incremental value.
4. **Fault-inject.** After a valid authorization and `RF-1042` dispatch, remove the provider acknowledgment. Specify durable observations, forbidden actions, reconciliation evidence, and escalation owner.
5. **Challenge.** A team proposes exposing the payment adapter as a read-only agent tool with an optional `execute=true` parameter. Identify the authority defect and redesign the interface.
6. **Defend.** Explain what an architecture diagram can prove, what it cannot prove, and the tests needed before a Chapter 13 execution design could be released.
