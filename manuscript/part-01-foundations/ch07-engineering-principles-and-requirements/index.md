# Chapter 7 — Engineering Principles and Requirements

*Part I: Foundations, Evolution, and Business Context*

> **Engineering proposition:** A trustworthy agentic system begins with testable obligations, not a list of desired AI capabilities. Requirements must make authority, evidence, failure behavior, and operational accountability observable before an architecture is selected.

## Learning objectives

By the end of this chapter, readers should be able to: (1) turn a business goal and delegation envelope into verifiable system requirements; (2) distinguish functional behavior, constraints, quality attributes, and evidence obligations; (3) trace a consequential action from authority to negative tests and an operational owner; (4) define measurable acceptance for uncertainty and external effects; (5) allocate requirements between model, controller, enterprise workflow, provider interface, and people; and (6) defend a release gate with evidence rather than a successful demonstration.

## 7.1 From trust principles to acceptance obligations

Chapters 1–6 established why enterprise agentic AI needs engineering, the historical mechanisms it inherits, the definition of bounded autonomy, the distinction between agent and workflow, the economic decision, and the separation of uncertainty from authority. The question now changes: **what must we be able to prove about the proposed system before building and releasing it?** Chapter 7 closes Part I with a practical requirements baseline. Part II will design the architecture that satisfies it.

Our running case is unchanged. A customer requests a **$500 refund** in `CASE-204`. **Design A** is a deterministic baseline; **Design B** is the initial *production candidate*, with AI in an advisory role and independently controlled execution; **Design C** is a bounded, read-only investigative agent whose incremental benefit must be evaluated. `RF-1042` is an illustrative stable payment-operation identity, not a promise of any provider-specific guarantee. A model can assemble a proposal. It cannot authorize or execute the payment. A lost provider acknowledgment creates payment-operation `UNKNOWN`, distinct from case-level `OUTCOME_UNKNOWN`.

A statement such as “the agent should be safe and auditable” is a design aspiration. A requirement identifies an observable behavior, a bounded condition, a measurable acceptance threshold or invariant, an owner, and evidence. ISO/IEC/IEEE 29148:2018 supplies established requirements-engineering context; the ETIS identifiers and templates below are an original teaching convention, not a quotation or mandatory format from that standard.

## 7.2 Seven engineering principles expressed as constraints

**Bounded authority.** Every tool call and consequential transition executes under an explicit principal, scope, policy version, and permission check. Model confidence never extends this scope.

**Evidence before effect.** Trusted inputs and policy checks support a typed proposal, but a verified authorization and durable intent precede the financial adapter.

**Fail into a defined state.** Missing evidence, denial, stale approval, and unknown external effects have specified outcomes and accountable owners. A timeout is not proof of failure.

**Independent verification.** Test behavior across normal, adversarial, contradictory, and interrupted paths; do not accept fluent explanations as verification.

**Least necessary delegation.** Begin with the smallest effective control surface. Design C is not inherently better than B because it takes more steps autonomously.

**Operational recoverability.** An incident responder can identify the last authorized action, preserve operation identity, stop further effects, and reconcile with authoritative sources.

**Traceable change.** A material change to prompts, model, tools, policy, data contract, or provider integration triggers impact analysis and targeted regression evidence.

These are engineering constraints, not seven additional subsystems. The architecture may satisfy several with one well-designed controller, but it must not silently replace an enforced control with an instruction to the model.

## 7.3 A requirement is a testable contract

Use a small, explicit record for each consequential requirement:

| Field | Required information |
|---|---|
| **ID and claim** | Stable requirement ID; one observable proposition |
| **Trigger and scope** | Case, tenant, principal, operation, version, and preconditions |
| **System obligation** | What must happen or must never happen |
| **Acceptance oracle** | Testable result and evidence location |
| **Owner and gate** | Accountable decision owner; failure consequence |

For example: **`AUTH-01` — The advisory or investigative component shall not possess a credential or callable path capable of initiating a refund.** A credential is like a key to a protected interface; the trusted authorization check is the guard that decides whether a particular operation is permitted. A valid key is not permission to issue this refund. Acceptance requires actual key-custody and direct-bypass checks, negative invocation tests, and runtime denial traces under deployed roles and network permissions. A prompt-injection test alone cannot prove safety if a privileged adapter remains reachable. Chapter 13 develops the mechanism.

A second example is **`PAY-03` — If the result of payment operation `RF-1042` is unknown, the workflow shall retain its operation identity, prevent an unapproved new financial attempt, and reconcile or escalate to a named owner.** Acceptance includes a lost-acknowledgment fault injection, durable journal inspection, provider-correlation evidence where supported, and an escalation trace. The requirement must be adapted to the selected provider's actual contract; “exactly once” cannot simply be asserted.

Distinguish four types in the specification: functional requirements describe permitted behavior; safety and security constraints prohibit unacceptable paths; quality attributes set measured targets such as timeliness or recoverability; assurance requirements define the evidence a reviewer must see. A test suite is a means of verification, not a substitute for a correctly stated obligation.

## 7.4 The refund requirements baseline

The initial baseline is deliberately compact. It captures the risks established in prior chapters while leaving detailed implementation to later parts.

| ID | Required behavior or invariant | Evidence / release consequence |
|---|---|---|
| `DATA-01` | Read access is scoped to `CASE-204` and the authorized tenant | Cross-tenant negative tests; any leak blocks release |
| `EV-02` | Each material factual assertion identifies source, version/freshness, and contradictions | Sampled provenance replay; unresolved conflicts reach review |
| `AUTH-01` | No AI-originated refund execution path or financial credential | Capability and negative authorization tests; violation blocks release |
| `POL-02` | Current identity, policy, amount, balance, and approval are checked at execution | Changed-policy and expired-approval tests; bypass blocks release |
| `PAY-03` | `UNKNOWN` preserves `RF-1042`, prohibits blind replacement, and reconciles/escalates | Fault injection and journal/provider trace; duplicate-risk blocks release |
| `OPS-01` | Operators can contain execution and recover an unresolved case | Stop drill, owner acknowledgment, audit trail; failed drill blocks expansion |
| `EVAL-01` | Pilots report errors and escalations by exception stratum, not only mean score | Versioned evaluation report and thresholds approved before pilot |
| `CHG-01` | Material changes invalidate affected claims until targeted re-verification | Change-impact record and regression evidence; missing evidence holds promotion |

The baseline does not invent universal numerical thresholds. For advisory summaries, the business and risk owners might set source-fidelity and escalation targets after a representative evaluation. For a payment-authority boundary, the expected number of successful unauthorized calls in the acceptance suite is **zero**, but a finite test cannot establish mathematical absence of every vulnerability. Combine testing with structural isolation, least privilege, configuration review, and monitoring. NIST AI RMF provides risk-management context, not a certification of these ETIS-specific numbers or artifacts.

## 7.5 Trace from goal to evidence, not from feature to demonstration

A good trace shows why a requirement exists, who can enforce it, how it is tested, what is retained, and what happens when it fails. It must include *negative* paths, not only the successful customer journey.

![Figure 7.1 — Trace one business goal to bounded decisions, requirements, controls, and acceptance evidence without granting the agent execution authority.](assets/shared-figures/rendered/F07-01.png){#fig:f07-01 width=5.75in}

For `CASE-204`, the business goal is timely, correct resolution without unauthorized or duplicate financial effects. The goal maps to decisions (eligibility, authorization, execution, reconciliation); each decision maps to an owner and an enforceable boundary. A requirement names the obligation at that boundary. A test injects a realistic fault or adversarial condition; its evidence becomes part of the release record. A broken link in this chain is a review finding. A model-generated traceability table can help produce the draft, but an engineer must validate every link to code, policy, and observed evidence.

A useful repository evidence record could connect `AUTH-01` to the tool-allowlist configuration, the negative-call test, an immutable run identifier, and a reviewer decision. The record should make explicit whether the evidence is **design evidence**, **test evidence**, or **production observation**. One type should not be mislabeled as another. A diagram that shows a trust boundary is design intent; a denial trace demonstrates one observed enforcement instance.

## 7.6 Establish acceptance before measuring the pilot

An evaluation without a previously defined denominator is easy to celebrate and hard to defend. Define case strata before running a pilot: ordinary eligible requests, ambiguous policy, contradictory sources, attempted prompt injection, stale approval, cross-tenant access, provider timeout, and unresolved external effect. For each, specify the expected state transition, permissible escalation, observed metric, and severity of an error.

A representative acceptance matrix should include success and failure outcomes. False approval and false denial are not symmetric; a duplicate financial effect differs from a delayed review. A useful result reports both task quality and boundary integrity. A 95% summary-quality score cannot compensate for one demonstrated unauthorized payment route. An evaluation of Design C must include its additional tool steps, latency, containment behavior, operating cost, and incremental value against B—not merely whether C appears more capable in a demonstration. Chapter 5's economic case and Chapter 6's uncertainty controls remain release inputs.

Where numeric thresholds are appropriate, record their rationale, sample size, data coverage, owner, and revision date. Use holdout and adversarial cases, repeat stochastic runs when variation matters, and replay identified defects. The NIST AI RMF (2023) and its Generative AI Profile (2024) provide a framework for measuring and managing risk, but neither selects the enterprise's refund loss tolerance for it.

## 7.7 Release gates and evidence ownership

![Figure 7.2 — Release decisions are grounded in distinct design, test, operational, and approval evidence; a failing critical boundary results in HOLD rather than automatic promotion.](assets/shared-figures/rendered/F07-02.png){#fig:f07-02 width=5.75in}

Treat release as a documented decision with non-negotiable constraints. A pilot may proceed only when the approved delegation envelope, access controls, negative tests, policy checks, reconciliation path, runbook, rollback or containment mechanism, and accountable decision owners are present. The actual deployment threshold depends on consequence; **critical authority or tenant-isolation defects hold release**, even when the AI output is persuasive and the business case is favorable.

Assign responsibilities without pretending every organization has the same job titles. The business owner establishes outcome and risk appetite. The policy or financial authority owner approves financial decision rights. Security reviews identity and isolation boundaries. Engineering owns requirements-to-control traceability and test evidence. Operations owns stop, escalation, reconciliation, and recovery readiness. A release authority records residual risks and the final go/hold decision. One person may occupy multiple roles, but the decision record must say which responsibility was exercised.

For a provider timeout, the evidence record is not “the workflow was retried and succeeded.” It must show the original `RF-1042` intent, attempt, unknown observation, blocked duplicate path, reconciliation result or escalation, and responsible owner. This makes the difficult edge case as reviewable as the happy path.

## 7.8 Requirements evolve; obligations must not disappear

Requirements are baselines, not permanent guesses. New policy, a changed model, a new provider API, evolving data retention needs, or field incidents may justify revision. A change request should identify impacted claims, affected interfaces, test coverage, approval authority, rollback readiness, and evidence that remains valid. Retirement of a control requires explicit review rather than deletion of an inconvenient failing test.

Avoid premature solution lock-in. “Use a five-agent framework” is an architecture choice, not a trustworthy system requirement. “No AI-originated call can initiate a refund” is an invariant that candidate designs must satisfy. This separation lets Part II compare architectures without losing the original business and safety obligations. Requirements should also remain operationally feasible: an unowned manual exception queue is not a recovery system.

## 7.9 The Part I exit decision

Part I is complete as a conceptual argument when the engineering team can state: **what value is sought; what uncertainty exists; who may act; which effects are controlled; how a failure is contained; and what evidence would justify release.** Chapter 7 turns those answers into a versioned baseline, not a claim that a production system has already passed its tests.

For the refund case, retain **Design B as the conditional production candidate** and **Design C as a separately evaluated, read-only alternative**. The authorization gate and provider payment adapter remain trusted enterprise components. No capability, confidence score, or positive demo changes that allocation. Part II begins with the architecture choices and trust boundaries needed to realize these requirements; later parts will add implementation, reliability, operations, and governance detail without rewriting this case's essential facts.

## Chapter 7 — Engineering practice

1. **Specify.** Write a trigger, enforceable obligation, acceptance oracle, and owner for `AUTH-01` and `PAY-03`; identify one test that cannot alone prove the invariant.
2. **Trace.** Connect the $500 refund goal to `DATA-01`, `POL-02`, and `OPS-01`, including negative evidence and the blocked-release consequence.
3. **Attack.** A customer email includes a tool-invocation instruction and a forged manager approval. Specify expected denials, retention, and escalation behavior.
4. **Reconcile.** Inject a timeout after `RF-1042` submission. Provide the evidence required to move payment-operation `UNKNOWN` to a supported terminal outcome; distinguish case `OUTCOME_UNKNOWN`.
5. **Evaluate.** Build a stratified B-versus-C pilot scorecard that includes financial risk, source fidelity, cross-tenant isolation, cost, review burden, and stopping behavior.
6. **Defend.** A pilot reduces resolution time by 20% but has one unresolved cross-tenant access defect. Write the release decision, owner, and evidence required to revisit it.

**Review standard:** Work is satisfactory when each consequential claim is testable, its owner is named, negative paths are covered, and the release consequence is unambiguous. A polished architecture diagram with no independently observed evidence is not a passing requirement.

## Sources and further reading

ISO/IEC/IEEE 29148:2018 provides requirements-engineering context. NIST AI RMF 1.0 (2023), NIST AI 600-1 (2024), provide governance and risk-management context. Gray and Reuter (1992) and Kleppmann (2017) provide the transaction and distributed-system foundations of the payment example. The ETIS identifiers, sample matrices, figure designs, and release gates in this chapter are original teaching examples and are not attributed as normative clauses to those references.
