# Chapter 13 — Trusted Execution and Authority (E5)

*Part II: Enterprise Reference Architecture*

> **Engineering proposition:** A model-generated recommendation, a human approval, a durable operation record, and a confirmed financial effect are four different things. Trusted execution is the independently enforced path that decides whether a particular consequential operation is permissible, persists its intent, and preserves uncertainty until authoritative evidence resolves the outcome.

## Learning objectives

After this chapter, readers should be able to (1) explain the difference between authenticated admission, a reviewed proposal, authorization, and an external financial effect; (2) derive a trusted execution contract with decision evidence, separation of duties, and current business facts; (3) specify durable intent, a stable operation identity, and controlled dispatch without assuming an atomic transaction across a payment provider; (4) distinguish denial, approval, attempted dispatch, confirmed completion, and unknown outcome; (5) show why leases and fencing prevent stale workflow owners from changing trusted state but cannot independently deduplicate provider payments; and (6) explain credential custody and test direct-bypass, token misuse, revocation, concurrency, and recovery.

## 13.1 From supporting evidence to permissible action

Chapter 9 admitted and scoped `CASE-204`. Chapter 10 established durable coordination and workflow ownership; Chapter 11 constrained agent reasoning and proposals (E3) to evidence-bearing recommendations; Chapter 12 established the provenance and limits of context and retrieval (E4). We now cross the consequential boundary. **Trusted execution and authority (E5)** decides whether an independently reviewable proposal may become a financial operation. **Trusted** describes responsibility and enforceable controls, not a claim that implementation bugs or misuse are impossible.

For the missing-replacement **$500 refund**, **Design A** remains deterministic; **Design B**, advisory with independent review, is the conditional production candidate; **Design C** permits **read-only investigation**, not payment. All share the same financial boundary. `RF-1042` is the operation identity, not proof of payment.

The critical distinction is **four claims, four evidentiary standards**. A *proposal* says what should happen based on cited information. An *authorization decision* says that a named actor, policy, and current business state permit a specific effect. A *dispatch observation* records an attempted integration call. A *confirmed outcome* requires authoritative provider evidence. These claims must not be compressed into one `success` field. Valid structure does not prove correctness, authority, or provider success.

An **effect** is a change in business state, such as a refund. A **consequential operation** is a requested action capable of causing such a change. Trusted execution is conventional enforcement software, potentially in the same deployment as other responsibilities, constrained by independently controlled identity, policy, state, and interfaces. It need not be an AI agent; determinism alone is insufficient.

## 13.2 Locate the independent authority boundary

Figure 13.1 locates both the authorization boundary and the separately protected credential path to the payment provider. **Admission and identity (E1)** establishes who submitted work and under what scope. **Coordination and ownership (E2)** retains the case and its current owner. **Agent reasoning and proposals (E3)** supplies candidate advice; **context and retrieval (E4)** supplies scoped evidence. Neither can confer authority by setting a flag. **Governance and assurance (E9)** defines control policy and accountable decision rights. **Authoritative business systems (E8)** supply current captured-payment, refund-history, and eligibility facts. The trusted path checks these independently; prompts and cached observations are not approvals.

![Figure 13.1 — Agent advice cannot reach protected payment credentials or bypass the independently enforced financial boundary.](assets/shared-figures/rendered/F13-01.png){#fig:f13-01 width=5.75in}

**Authentication** establishes a principal's identity. **Authorization** determines whether that principal, acting in this role and case, may request a specified operation under current policy. **Approval** is a recorded decision by an authorized person or governance mechanism; its presence is one input to authorization, not proof of payment. A **policy decision point** evaluates the rules; a **policy enforcement point** prevents a forbidden action from crossing the controlled interface. Both may coexist if enforcement remains independent.

Trusted execution checks delegated authority, tenant and customer binding, payment, prior refunds, balance, policy, and case state. Customer requests and an agent-generated `approved: true` do not confer authority; an approval for another order or amount cannot be reused.

**Least privilege** limits rights to assigned responsibilities. **Separation of duties** divides approval, execution, and audit so one actor cannot both authorize and conceal an improper effect. Combined roles require compensating controls.

### Credentials, capabilities, and protected doors

A useful analogy is a **door controlled by a guard**. A **principal** is the human or workload seeking entry; a **credential** (such as a client certificate or access token) helps authenticate it. A **capability** is a bounded ability to call an operation. The **policy enforcement point** is the guard that actually blocks forbidden requests. The analogy has limits: holding a valid key to a building does not authorize every room or every action inside. Likewise, a valid service token does not authorize this customer's $500 refund. Authorization must bind the principal, tenant, case, payment, amount, policy, and approval at the moment of effect creation.

An **access token** may convey time-limited, audience- and scope-bound access; its claims and signature or other validity evidence require trusted validation. A **secret** or **private key** is protected credential material whose disclosure may enable impersonation or unauthorized calls. Agent-controlled reasoning may invoke approved read-only tools through a validating gateway, possibly using narrowly scoped credentials. It must not receive a raw payment credential, secret, or token that permits it to bypass trusted execution. The governed integration adapter may acquire short-lived provider credentials through workload identity and a secret manager or equivalent controlled mechanism, *after* trusted authorization and durable intent. A secret manager alone does not enforce refund policy.

**Custody is an architectural control, not a diagram label.** Deny agent workloads direct network routes and permissions to the provider; isolate secret access, tool registration, logs, and process permissions. Validate token issuer, audience, expiry, and relevant scopes at the receiving boundary, and apply transaction-specific policy independently. Use credential rotation or revocation, contain affected workloads, protect audit evidence, and reconcile uncertain dispatch before retry. If a stolen provider credential allows direct calls, the logical gate can be bypassed; provider-side restrictions, network controls, and incident response must limit that exposure. Chapter 16 compares isolation options.

## 13.3 Specify the effect authorization contract

A versioned **effect-intent contract** carries `case_id`, trusted principal and tenant, payment identifier, amount, currency, action, evidence, approval, policy, and request identity. This is an illustrative schema. The trusted service resolves identity, policy, and current facts independently; model-written roles, bearer tokens, or balances are never accepted as proof.

Distinguish three interfaces. First, `evaluate_refund` answers whether a proposed refund is currently permissible and why; it may return `DENY`, `REVIEW_REQUIRED`, or a time-bounded authorization decision. Second, `create_refund_intent` persists a uniquely identified permitted operation under a local transaction and protects against duplicate creation for the same underlying business request. Third, `dispatch_refund` drives a controlled integration adapter under an established operation identity. Implementations may combine calls while preserving these invariants.

**Time-of-check to time-of-use (TOCTOU)** describes the risk that the facts used to authorize an action change before the action occurs. For example, another process may issue a partial refund between balance inspection and intent creation. Trusted execution must use transactional predicates, a reservation, version comparison, or another established consistency mechanism to prevent an earlier eligibility result from authorizing an invalid later operation. A policy decision is likewise tied to a governed version and relevant approval period; expiration or revocation requires fresh evaluation.

An **idempotency key** is a stable request identity used by a component or external provider, subject to its documented contract, to recognize repeated attempts as the same intended operation. The book uses `RF-1042` as the stable *business operation identity*. An adapter may map that identity to a provider-specific key. A uniqueness constraint in the local ledger prevents duplicate local intents but **does not prove** that an external provider will perform at most one effect. Provider scope, key retention, amount matching, status lookup, and replay behavior must be examined before making any guarantee.

## 13.4 A decision that can be inspected and challenged

An authorization record binds the requested order, amount, currency, principal, tenant, case, policy, approvals, source versions, decision owner, and reason. **Evidence lineage** links the decision to authoritative facts and the reviewed proposal—not an unexplained model assertion.

Figure 13.2 shows the principal authorization gates. These are logical, not necessarily network, checks. The first gate rejects malformed or mismatched requests. The second checks identity, tenant, scope, and any required approval. The third independently revalidates authoritative financial facts and policy. Only the permitted branch may create durable financial intent; every other branch records a denial, hold, or review route without an external payment effect.

![Figure 13.2 — Independent identity, approval, and financial-fact gates terminate unsafe requests before durable intent.](assets/shared-figures/rendered/F13-02.png){#fig:f13-02 width=5.75in}

Denial is correct when authority is lacking. Missing data or policy-service failure means `HOLD` or escalation, never guessed permission. A model cannot silently change the amount. Return explicit reason codes without leaking other tenants' records.

Human review needs decision rights, underlying order and balance, policy version, contradictory evidence, and the proposal identified as *advice*. Approval binds a specific effect and remains subject to revocation at intent creation.

## 13.5 Persist intent before crossing the effect boundary

A **durable intent** is a transactionally stored record of an approved operation that survives a process crash. For `RF-1042`, the record includes the business target, requested amount, authorization reference, stable identity, and a state representing what the enterprise knows. Local atomicity can commit this intent and its uniqueness constraints together. It cannot atomically commit a remote provider payment unless that provider participates in an explicitly supported distributed transaction, which the reference design does not assume.

Before dispatch, the system must ensure that any required review and authorization are still valid and that one logical refund request maps to its intended stable operation identity. The **transactional outbox** pattern—persisting a dispatch instruction in the same local transaction as the intent—can help avoid losing a request between database commit and message delivery. It does not provide an unconditional exactly-once external effect. The integration adapter (E6) sends the provider request and records an observation; the authoritative payment provider and finance records (E8) determine the actual financial outcome. Chapter 14 develops those adapter and source-of-truth contracts; Chapter 15 develops the full durable state machine and assurance evidence.

A useful illustrative operation progression is `INTENT_RECORDED` → `DISPATCH_ATTEMPTED` → `CONFIRMED` or `UNKNOWN`, with separate `DENIED`, `HELD`, and `CANCELLED_BEFORE_DISPATCH` exits where appropriate. These states are illustrative. The durable **case** may separately be `OUTCOME_UNKNOWN` while the *financial operation* remains `UNKNOWN`. Cancellation of a queued request is not proof that a payment already accepted by the provider was reversed. An operator must not mark the financial operation `FAILED` merely because the network call timed out.

Failure before intent creation leaves no dispatchable operation. A failure after intent creation but before attempted dispatch can often resume the same queued work, after validating ownership and current policy. A failure after dispatch creates a more difficult question: the provider may have completed the effect and the acknowledgment may be missing. Preserve `RF-1042`, use documented provider status or idempotency interfaces, and reconcile without creating a new refund identity. Figure 13.3 makes these fault boundaries explicit.

![Figure 13.3 — The recovery action depends on where failure occurred; unknown provider results are reconciled under the same operation identity.](assets/shared-figures/rendered/F13-03.png){#fig:f13-03 width=5.75in}

## 13.6 Concurrency, fencing, and safe recovery

Chapter 10 introduced a **lease**, a time-bounded right to coordinate work, and an **ownership epoch**, a monotonically increasing generation number used to reject stale coordinators. A **fencing check** atomically compares the expected epoch with the authoritative current one before accepting a state transition. These controls protect workflow ownership and local state updates; they do **not** alone prevent two external provider requests from producing two refunds.

Suppose Coordinator A pauses while holding epoch 7. Its lease expires, and Coordinator B takes ownership at epoch 8. When A resumes, the durable state store rejects its stale update. The trusted dispatcher must also require current, independently enforced authority and guard the unique operation identity. Even if two delivery attempts occur, the system needs provider-specific idempotency guarantees or reconciliation to manage duplicate-effect risk. Fencing without an enforceable provider contract is not a financial correctness proof.

**Reconciliation** is the controlled process of comparing local operation observations with authoritative provider or financial-system evidence to determine the best supported outcome. A provider status of `PENDING` does not mean `CONFIRMED`; a timeout does not mean `FAILED`; a dashboard label does not override a provider ledger. If status cannot be resolved, retain `UNKNOWN`, notify an accountable operator, and use a documented incident or exception procedure. Where the provider offers no stable lookup, the enterprise must acknowledge a weaker assurance posture and may have to hold automatic retries pending manual review.

This also separates two kinds of retry. A timed-out *read-only investigation* may be restarted under the current case owner and permitted scope. A possibly completed *financial effect* cannot be retried under a new identity simply to make the workflow move forward. A second refund—even if a customer deserves the first—requires a distinct, independently authorized business decision and evidence that it is not duplicating an unresolved payment.

## 13.7 Deployment alternatives and governance consequences

Trusted execution is a logical responsibility, not necessarily a separate microservice. In-process enforcement must still isolate credentials, interfaces, and audit access from agent-controlled paths; higher-risk operations may warrant separate processes or remotely enforced gates. Choose the topology from assurance, latency, and operational evidence.

A model-facing component with payment credentials or direct provider access can invalidate the claimed trust boundary. The platform team should own trusted execution mechanisms, credential handling, operation-state controls, and enforcement instrumentation; the business domain should own refund rules, delegated limits, exceptions, and acceptable customer outcomes; security and assurance should review the boundary; operations should own monitoring, containment, and recovery. Roles can vary; accountability cannot be implicit.

Stronger isolation and review increase latency and cost but may prevent larger payment and trust losses. Compare total cost per correctly resolved case across Designs A, B, and C without relaxing the financial boundary.

## 13.8 Verification evidence and the Chapter 14 handoff

A production-readiness test set must try to defeat the boundary, not simply demonstrate a correct refund:

1. **Forged authority:** A model outputs `approved=true` or a customer email demands payment. The trusted gate denies the unauthorized operation.
2. **Wrong case or tenant:** A valid-looking proposal cites another customer's payment. Identity and resource binding reject it without exposing protected data.
3. **Amount and policy mismatch:** The requested $500 exceeds current refundable balance, an approval expires, or policy changes between review and intent creation. The trusted gate denies or re-evaluates.
4. **Concurrent intent:** Two workers seek to create the same logical refund. Local transactional uniqueness and authorization checks prevent competing local operations.
5. **Stale coordinator:** Epoch 7 attempts an authoritative update after epoch 8 takes over. The local store rejects it, with evidence of the fencing decision.
6. **Crash windows:** Fail before intent, after intent, before dispatch, and after dispatch. Resume the same operation safely and distinguish every observation from the external outcome.
7. **Lost acknowledgment:** The provider completes `RF-1042` but the response disappears. The local operation becomes `UNKNOWN`, and reconciliation queries the same identity rather than generating another payment.
8. **Provider limitation:** The provider lacks reliable idempotency or status lookup. Document the reduced guarantee and hold unsafe automatic retries.
9. **Direct-bypass test:** The agent attempts to call the payment provider directly or retrieve the provider credential. Network and identity controls deny access; the attempt is recorded without exposing secrets.
10. **Token and compromise test:** Present an expired, wrong-audience, wrong-scope, or revoked credential. Deny it. Simulate provider-credential exposure: revoke/rotate, contain, inspect audit records, and reconcile uncertain effects.
11. **Human intervention:** An operator suspends dispatch, inspects evidence, and escalates without claiming an external payment was reversed.

Retain policy and approval versions, authenticated decision context, authoritative record references, intent state, stable operation identity, adapter observations, negative-test results, and final reconciliation evidence. Sensitive details require purpose-bound visibility and retention. Policy-file validation does not replace negative tests, fault injection, or operator drills.

**Synthesis.** The first twelve chapters prepared the business case, bounded delegation, owned investigation, typed recommendations, and controlled evidence. Chapter 13 establishes the point where a proposal may—only after independent verification—become a recorded consequential operation. The architecture must retain the difference between *permission*, *attempt*, *observation*, and *external truth*. Chapter 14 turns to **enterprise integration and business truth (E6/E8)**: provider-specific contracts, authoritative records, failure semantics, and how the enterprise knows whether `RF-1042` actually changed financial state.

## Chapter 13 — Engineering practice

1. **Specify.** Design a versioned authorization request and decision envelope for `CASE-204`. Identify which fields come from trusted systems and which may originate in a model proposal.
2. **Trace.** Show the four evidence claims—proposal, authorization, dispatch, confirmation—and identify the source that can support each.
3. **Threat-model.** Test forged approval, direct provider access, leaked credentials, expired or wrong-audience tokens, and a wrong-tenant case. Name each enforcement point.
4. **Recover.** Draw the crash windows around durable intent and provider dispatch, then justify why `RF-1042` must be retained on uncertain outcomes.
5. **Concurrency.** Explain which risks epoch fencing addresses and which require local uniqueness, provider idempotency, and reconciliation.
6. **Defend.** Compare in-process and independently deployed trusted execution for a high-volume retailer. State the security, reliability, latency, cost, and operational evidence required to select a design.

**Review standard:** Strong work distinguishes authentication, authorization, credential custody, and effect; tests bypass and revocation; verifies authoritative facts; preserves operation identity; and models `UNKNOWN` honestly. A successful model recommendation or provider API response is insufficient by itself.

**Sources and further reading.** The reasoning inherits transaction processing (Gray and Reuter, 1992), distributed-system coordination and consistency (Kleppmann, 2017), workflow ownership (van der Aalst, 2013), and security/authorization principles discussed in Part I. The ETIS effect-intent contract, decision records, and `RF-1042` sequence are illustrative teaching constructs, not a certified payment implementation. Provider guarantees, organization-specific policy, and relevant regulatory requirements require direct verification before production use.
