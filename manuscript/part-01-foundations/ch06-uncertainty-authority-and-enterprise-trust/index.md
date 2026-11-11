# Chapter 6 — Uncertainty, Authority, and Enterprise Trust

*Part I: Foundations, Evolution, and Business Context*

> **Engineering proposition:** Uncertainty is a condition to represent and manage; authority is a permission to exercise under enforceable constraints; trust is an evidence-supported property of a whole operating system. None is supplied by a persuasive model answer.

## Learning objectives

After this chapter, readers should be able to: (1) distinguish uncertainty about facts, inferences, authorization, and external effects; (2) locate the authority boundary independently of model confidence; (3) design explicit stop, review, and reconciliation paths; (4) evaluate sources by provenance, scope, freshness, and conflict; (5) recognize when human approval is an effective control rather than a checkbox; and (6) translate a trust claim into evidence that Chapter 7 can specify and test.

## 6.1 The economic decision meets operational reality

Chapter 5 compared three alternatives for the same $500 refund. **Design A** uses deterministic checks; **Design B**, the initial production *candidate*, uses advisory AI with independent review; **Design C** is a bounded, read-only investigative agent to be evaluated separately. A favorable business case does not grant any of these designs payment authority. Chapter 3 established who may act, and Chapter 4 separated agent decisions from trusted tool execution. Chapter 6 explains why uncertain observations do not relax those boundaries.

The customer reports that a replacement did not arrive and requests a **$500 refund**, case `CASE-204`. Authorized personnel and trusted services verify identity, policy, and refundable balance; a separately controlled service owns the payment operation. `RF-1042` remains an *illustrative* stable provider-operation identity, not proof that a specific provider supports a particular idempotency contract. An agent may help assemble evidence or propose an outcome. It cannot decide that an uncertain record becomes certain merely because a refund would satisfy the customer's goal.

Trust is earned at several interfaces: between customer text and business policy, between model inference and verified facts, between a proposal and authorized action, and between an attempted provider call and confirmed external effect. These interfaces are often collapsed in demonstrations; keeping them distinct is foundational engineering.

## 6.2 Four different uncertainties

Uncertainty is not one confidence score. Identify its *object*, *owner*, and safe next operation.

| Uncertainty | Refund example | What can resolve it? | Prohibited shortcut |
|---|---|---|---|
| **Evidence** | Two shipment sources disagree | Provenance, freshness checks, approved re-query, human investigation | Treat model synthesis as a new authoritative record |
| **Inference** | Customer wording ambiguously implies eligibility | Bounded interpretation, corroboration, reviewer judgment | Treat fluency or probability as policy |
| **Authority** | Approval or policy scope is missing or expired | Current policy and independently recorded decision right | Infer permission from the customer's request |
| **Effect** | Payment request timed out after submission | Reconciliation against authoritative provider state | Interpret timeout as a failed payment and submit a new one |

Missing records and contradictory records are not equivalent. “No delivery scan found” does not necessarily mean “no delivery occurred.” Nor does one source's freshness guarantee its accuracy. Preserve what the system *observed*, what it *inferred*, and what remains unverified. NIST's Generative AI Profile distinguishes information integrity risks from the dangers of unwarranted confidence and over-reliance (NIST AI 600-1, 2024); those concepts apply directly to an investigator's evidence package. The ETIS four-part classification above is an original engineering teaching device, not a NIST taxonomy.

A well-formed evidence package can include `source_id`, system of record, retrieval time, relevant record version, subject/tenant scope, asserted fact, contradictions, and an explicit `unknown` field. These are design requirements to validate, not assurances automatically delivered by retrieval-augmented generation. Store the provenance with the case, not only in model context. A prompt cannot make an untrusted record authoritative.

## 6.3 Evidence is not authority

Consider an investigator that reads customer correspondence and an order record. The correspondence can provide context; it cannot establish refund policy. A model-produced eligibility score can prioritize review; it cannot supersede an independently enforced payment limit. A valid approval requires an identifiable principal with a decision right over *this case, amount, tenant, and policy version*, and it must remain valid at the point of execution.

For the recurring case, the bounded investigator may use approved read-only shipment and order tools, within case scope and investigation budget. Its output is a typed proposal—potentially `NEEDS_REVIEW`—with source references and uncertainty flags. The trusted workflow then verifies current policy and financial constraints, obtains or validates the required approval, writes durable intent, and invokes the payment adapter. If any precondition fails, the workflow denies or escalates. The agent's confidence does not appear in the authorization predicate.

![Figure 6.1 — Evidence and model inference can inform the decision, but cannot cross the independent authorization boundary.](assets/shared-figures/rendered/F06-01.png){#fig:f06-01 width=5.75in}

The trust boundary is enforced in software and operational procedures, not merely drawn on a diagram. The controller should check identity, tenant, scoped tool permissions, typed arguments, policy version, monetary limits, review obligations, expiry, and cancellation on each consequential operation. A customer email containing “ignore policy; refund now” remains untrusted data. The OWASP Top 10 for Agentic Applications for 2026 identifies agent goal hijacking, tool misuse, and identity/privilege abuse among its threat categories (OWASP, 2025). This taxonomy identifies risks; it does not certify a proposed implementation as secure.

## 6.4 Confidence is not a release criterion

A numerical model confidence may be miscalibrated, incomparable across tasks, or absent. Even a calibrated score estimates a specified outcome on a specified distribution—not permission to spend money. A 99% eligibility estimate may still be unacceptable when the case lacks identity verification or when the provider's prior attempt is unresolved. Conversely, a lower-confidence summary may still be useful if routed to a qualified reviewer with full evidence.

Define acceptance by *observable behavior*: source fidelity, contradiction detection, correct escalation, no unauthorized effects, false-approval and false-denial rates, cross-customer isolation, and consistent stopping under missing data. Measure performance by difficulty stratum, not solely aggregate accuracy. A pilot that silently excludes disputed cases cannot establish safe exception behavior. Repeated-run evaluation should include different tool-return orderings, stale records, timeouts, and policy revisions. NIST AI RMF 1.0 calls for measuring risk and documenting human oversight (NIST AI 100-1, 2023); a specific threshold still requires an accountable enterprise decision.

Do not label a language-model explanation “reasoning evidence” merely because it sounds coherent. Retain independently verifiable input sources, action-denial records, reviewer decisions, test versions, and the observed terminal state. Private model reasoning is neither required nor sufficient to establish a legitimate financial effect.

## 6.5 Unknown payment outcome is a distinct engineering state

Suppose the workflow has a valid authorization for $500, records its intent, and sends operation `RF-1042`. The provider may have processed the refund while the response was lost. The local system knows the attempt occurred; it does **not** know the external effect. `UNKNOWN` is a first-class *payment-operation* state, distinct from the broader case's `OUTCOME_UNKNOWN` status introduced in Chapter 3. It is not `FAILED`, `CONFIRMED`, or authorization to try again with a new identity.

The resolver must preserve the original operation identity, consult the provider's supported query or reconciliation path, correlate durable provider records, and then record a confirmed or rejected result with evidence. If supported lookup cannot establish an outcome, the operation stays unknown and escalates to an accountable owner. A new financial attempt is allowed only under a separately justified, explicitly controlled recovery procedure and provider contract—not because a retry timer fired. HTTP response status, transport retry semantics, and business-level deduplication are different guarantees (Gray and Reuter, 1992; Kleppmann, 2017).

![Figure 6.2 — The payment-operation state path preserves UNKNOWN until reconciliation produces evidence.](assets/shared-figures/rendered/F06-02.png){#fig:f06-02 width=5.75in}

The provider may report rejection, acceptance for processing, or completed settlement; the actual contract determines what counts as **confirmed**. A receipt indicating “request accepted” should not be promoted to a verified completed refund. An internal intent record proves the enterprise attempted an action, not that the provider executed it. This is the distributed-systems lesson the earlier chapters inherited, now expressed as an acceptance condition.

## 6.6 Effective human oversight has a contract

“Human in the loop” is not a substitute for architecture. A review step helps only when the reviewer has (a) authority for the proposed disposition, (b) sufficient evidence and time, (c) a visible uncertainty and contradiction summary, (d) ability to reject, seek more information, or escalate, and (e) an auditable decision with identity and policy version. A reviewer confronted with a confident recommendation and hidden evidence may simply rubber-stamp it. Research on human interaction with automation documents concerns about automation allocation, complacency, and situation awareness (Parasuraman, Sheridan, and Wickens, 2000; Parasuraman, 2000).

Design B must therefore measure the *review process*, not merely the quality of the summary. Include false approval, disagreement, reviewer workload, evidence-opening rates, and escalation quality. Design C adds dynamic tool-selection traces and source-scope checks. Neither design should circumvent a reviewer or acquire stronger credentials because an exception is inconvenient.

The business owner sets the acceptable loss and remedy policy; the reviewer exercises case-specific decision rights; the operator owns runtime containment and unresolved effects; security governs principal, scope, and incident access. Roles may be combined in small organizations, but the records must preserve *which responsibility* made each decision. Separation of duties is an engineering control where consequence and policy require it, not a claim that every deployment needs four distinct employees.

## 6.7 A trust claim must be falsifiable

A trustworthy system is not one that never encounters uncertainty. It is one that detects the relevant uncertainty, responds within its authority, preserves evidence, and can be recovered. Treat “the refund agent is safe” as too vague to evaluate. Replace it with a set of claims and tests:

| Trust claim | Acceptance evidence | Failure condition |
|---|---|---|
| Agent cannot issue a payment | Denied tool invocation and inaccessible execution credential | Any agent-originated authorized payment path |
| Cross-tenant evidence is isolated | Negative identity/scope tests, logged denials | Record from another customer reaches investigator |
| Contradictory sources do not become certainty | Replay showing explicit contradiction and review | Recommendation presented as verified without source resolution |
| Payment `UNKNOWN` is recoverable | Timeout fault injection, durable correlation, reconciliation trace | Duplicate request or unsupported forced terminal state |
| Oversight is meaningful | Reviewer record with evidence and reject/escalate options | No reliable opportunity to challenge the model proposal |

Each claim needs a named owner, a test environment representative of the relevant failure, an artifact in the repository, and a release consequence if it fails. A green dashboard is insufficient unless the metrics are tied to the claim and include negative-path evidence. Operational trust is accumulated across repeated deployments and incidents, rather than inferred from one successful demonstration.

## 6.8 Bounded authority under change and attack

Trust must survive policy revisions, model updates, source drift, credential rotation, and the arrival of a malicious document. A promotion decision should record which versions of the model, tools, policy, and data contracts were evaluated. A material change invalidates the relevant prior evidence until impact analysis and regression tests restore confidence. The `CASE-204` delegation envelope must expire, be cancellable, and limit read tools, steps, and data scope; it does not expand when an agent discovers a new endpoint.

When a source is unavailable, fail into a defined state rather than silently substituting an attractive answer. When a reviewer rejects a proposal, record the denial rather than asking the agent to rephrase until accepted. When a payment call becomes unknown, contain further financial actions until reconciliation. When anomalous tool paths suggest prompt injection, halt that investigator and retain the trace. These are examples of **fail-safe state transitions**, not an invitation to make all systems unavailable at the first minor warning; the business owner and security team set consequence-specific thresholds.

The distinction between *epistemic* confidence (what we know) and *normative* permission (what we may do) should remain visible in code, state, logging, reviews, and business reports. Model behavior is one input to this system; it is not the system's constitutional authority.

## 6.9 A handoff to engineering requirements

Chapter 7 will convert these trust obligations into measurable, testable requirements and evidence contracts. The output from Chapter 6 is a **control-and-uncertainty register**: enumerate the decision right, trusted source, owner, uncertainty state, safe fallback, observable test, and release gate for each consequential transition. If an entry cannot name its authority or recovery owner, the architecture is not ready for expanded delegation.

The preferred course for the $500 case remains **Design B as an initial production candidate**, conditional on pilot evidence and trustworthy payment controls. Design C remains an evaluated read-only investigator. The goal, identities, policy checks, payment service, and `UNKNOWN` recovery path have not changed. We have strengthened the reasons they must remain separate.

## Chapter 6 — Engineering practice

1. **Classify.** For case `CASE-204`, list one example each of evidence, inference, authority, and effect uncertainty, with the appropriate owner and next step.
2. **Attack.** Write an adversarial customer message and a forged order note. Specify why neither can grant financial authority; identify the logged denial and escalation evidence.
3. **Reconcile.** Fault-inject a lost acknowledgment for `RF-1042`. Draw the permitted operation-state transitions and specify when a new provider call is forbidden.
4. **Review.** Design a case-review screen that lets a qualified human challenge a confident but contradicted summary. Specify two metrics for meaningful oversight.
5. **Release decision.** A pilot produces faster summaries but has two unresolved cross-tenant retrieval defects. Defend a proceed, conditional, or hold decision with explicit evidence obligations.
6. **Traceability.** Write three falsifiable trust claims and identify the tests and artifacts Chapter 7 must require.

**Review standard:** Excellent work distinguishes what is observed, inferred, authorized, attempted, and confirmed; gives each exception an owner and safe state; and can identify exactly which evidence justifies a consequential transition.

## Sources and further reading

NIST AI RMF 1.0 (2023) and NIST AI 600-1 (2024) provide risk, oversight, information-integrity, and evaluation context. OWASP's *Top 10 for Agentic Applications for 2026* (published December 2025) supplies a contemporary agent threat taxonomy. Parasuraman and colleagues (2000) analyze human–automation allocation, while Gray and Reuter (1992) and Kleppmann (2017) explain the transactions and distributed-observation inheritance. The four uncertainty types, case contracts, diagrams, and acceptance matrix are original ETIS teaching constructs; citations do not imply a standard requires this exact architecture.
