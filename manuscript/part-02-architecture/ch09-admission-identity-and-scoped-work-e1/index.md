# Chapter 9 — Admission, Identity, and Scoped Work (E1)

*Part II: Enterprise Reference Architecture*

> **Engineering proposition:** Admission does not give an agent authority; it establishes an authenticated, bounded work assignment that downstream controls can verify. A valid case identifier or useful recommendation is never a payment permission.

## Learning objectives

After this chapter, readers should be able to (1) separate authentication, case binding, delegation, and consequential authorization; (2) specify an admission contract for a customer-service case; (3) distinguish caller identity from an agent's workload identity; (4) enforce tenant, purpose, resource, tool, time, and budget scopes; (5) design rejection, revocation, and scope-change paths; and (6) demonstrate admission controls with negative tests and reconstructable evidence.

## 9.1 Admission is the first enforceable enterprise boundary

Chapter 8 derived nine logical responsibilities from Chapter 7's requirements. E1—**admission and identity**—is the entry point for work, but not the place where a refund becomes authorized. The input may be a customer's message, a case worker's request, or an authenticated enterprise event. Before an agent investigates, the enterprise must establish **who is requesting work, for which tenant and case, under whose delegated authority, for what purpose, and within what constraints**. Otherwise a system can correctly process the wrong customer's records.

The running example is unchanged. In `CASE-204`, a customer reports that a replacement shipment never arrived and asks for a **$500 refund**. Design A remains the deterministic comparison baseline; Design B is the *conditional initial production candidate* with model-assisted advice and independent review; Design C is an evaluated **read-only investigative agent**. All three require admission. None gives its reasoning component payment credentials. `RF-1042` remains the illustrative payment-operation identifier, created only on a separately authorized consequential path. At this point in the workflow, **no refund operation has been authorized or dispatched**.

Think of E1 as converting an incoming request into an **admitted work envelope**. It can admit the case for investigation, reject it, or require human resolution when identity or binding is uncertain. It cannot infer customer entitlement from a plausible story, accept an agent-generated account switch, or grant the trusted execution responsibility (E5) authority to issue a refund. Authentication identifies the caller; admission decides whether that caller may initiate this bounded kind of work. The trusted execution responsibility (E5) later checks payment-specific authority, current business facts, and approvals immediately before any consequential effect.

## 9.2 Four identities and two kinds of permission

A production system should not collapse the customer, human reviewer, application service, and agent into one undifferentiated “user.” For `CASE-204`, the **customer principal** is authenticated by an enterprise identity mechanism; the **case owner** may be a service employee or accountable workflow; the **workload principal** identifies the executing application or agent controller; and the **approver** is a person or delegated business authority, if approval is required. One individual or system may occupy more than one role, but each role has distinct authorization rules and an evidence trail.

Authentication answers “which principal presented these credentials?” Identity proofing, session assurance, and channel integrity determine how confidently the enterprise can rely on that claim. **Case binding** answers “does this principal have a justified relationship to this order and tenant?” A customer who correctly authenticates is not thereby entitled to every order that shares a familiar-looking identifier. A workload token authenticates the service making a call; it does not automatically transmit the customer's permissions. Delegation must be verified, constrained, and attributable at the resource boundary.

There are also two different permissions. **Admission permission** allows a scoped investigation, including selected read operations. **Consequential permission** allows the financial instruction only after trusted execution (E5) applies current policy, payment balance, approvals, operation identity, and other execution preconditions. The former is not a cached version of the latter. In Design B, an AI recommendation remains non-authoritative even when produced by authenticated enterprise software. In Design C, the investigator can select only approved read-only steps. Figure 9.1 locates this separation before any alternative investigation begins.

![Figure 9.1 — E1 authenticates and binds bounded work before any of the three investigation alternatives; admission is not the E5 financial authorization boundary.](assets/shared-figures/rendered/F09-01.png){#fig:f09-01 width=5.75in}

This is a **logical trust-boundary diagram**, not a requirement for separate microservices. E1 may share a process with the workflow coordinator, provided identity and scope are independently enforced at every sensitive downstream interface. The admission rules must be enforced by the surrounding application and its resource interfaces; simply describing those rules in a model prompt is insufficient.

## 9.3 The admitted-work contract

An admitted request needs a durable, inspectable form. The following is a **conceptual contract**, not a standardized token or a production-ready security credential. Values are illustrative. The authoritative issuer and relying services must validate authenticity, binding, expiration, revocation, and versioning using mechanisms appropriate to the deployment.

| Field | Meaning and invariant |
|---|---|
| `case_id: CASE-204` | Stable work reference; never sufficient authorization by itself |
| `tenant_id: retailer_a` | Tenant verified independently of customer-supplied text |
| `requester` / `auth_context` | Authenticated principal, method, assurance, and session reference |
| `subject_order` | Order/payment reference resolved through an authorized case-binding check |
| `purpose: investigate_missing_replacement` | Permitted business objective, not a broad “fix anything” goal |
| `permitted_reads` | Scoped order, shipment, and approved policy evidence |
| `permitted_outputs` | Typed assessment, proposed remedy, or escalation |
| `prohibited_effects` | Payment initiation, account alteration, policy or approval changes |
| `limits` / `expires_at` | Step, time, cost, and tool-use bounds; fail closed when invalid |
| `issuer` / `version` / `trace_id` | Who issued the scope, how it is verified, and how to reconstruct it |

The envelope belongs in **durable, authoritative workflow state**, not only in an LLM prompt or a mutable conversation summary. The coordination and ownership responsibility (E2) holds the admitted task and its owner; context and retrieval (E4) supplies scoped evidence; agent reasoning (E3) returns advice or a typed proposal. Each relevant read or tool interface must enforce its own authorization against trusted scope information. Admission and identity (E1) is therefore the start of an enforcement chain, not an all-purpose perimeter that eliminates downstream checks.

The envelope must express **both resource limits and action limits**. “May read order records” is insufficient if a caller can replace the order identifier with another customer's number. “May use a refund tool” is unsafe if one endpoint combines read and write operations behind an optional flag. Tool selection may be dynamic; permission cannot be dynamically invented. A new scope requires a trusted issuer and a recorded authorization decision.

## 9.4 A concrete admission sequence for CASE-204

Consider a customer asking, “The replacement never arrived. Please refund my $500.” A robust admission sequence is:

1. **Authenticate the channel and caller.** Establish the verified principal, session, tenant context, and assurance level; do not accept a customer-typed name as authentication.
2. **Resolve and bind the case.** Use trusted order/case lookup to confirm that the requester may access the cited replacement and payment. A matching order number alone is insufficient.
3. **Check admission policy.** Determine whether this principal, channel, tenant, purpose, and requested work class may start an investigation; consult current revocation and risk signals.
4. **Issue a bounded envelope.** Record permitted reads, outputs, deadlines, budgets, issuer, version, and trace identity outside model-controlled state.
5. **Create durable ownership.** Hand the admitted assignment to the coordination and ownership responsibility (E2), with a recoverable case owner and explicit denial/escalation outcomes.
6. **Enforce each subsequent access.** Read APIs validate tenant, case, resource binding, and allowed action independently; an agent cannot override them by changing prompts or tool arguments.

A denial is a correct terminal admission outcome when identity or entitlement cannot be established. It should not erase the customer's request: the system may route the request to an identity-verification or human-service path while keeping its reason and owner. A suspended session, conflicting tenant, guessed order identifier, expired scope, or revoked credential must not become a “best-effort” data read merely to improve response time.

A trusted admission decision (E1) does not certify that retrieved shipment data are accurate or that a refund is due. Those are later responsibilities. Conversely, an ambiguous complaint may still be admitted for a safe investigation even when the eventual remedy is uncertain. Admission asks whether it is permissible to **investigate**, not whether the customer should **receive money**.

## 9.5 Scope changes, stale authority, and rejection

The largest admission defects appear after the first successful check. A model asks to retrieve another order; a human reassigns a case; the user session expires; a tenant administrator revokes access; an agent discovers a relevant but out-of-scope document. The system must not treat the original envelope as permanent authority. Figure 9.2 distinguishes an ordinary permitted read from a denied or reissued scope and avoids depicting revocation as a payment operation.

![Figure 9.2 — Every proposed data access is checked against current scoped authority; a scope expansion is denied until a trusted issuer reauthorizes it.](assets/shared-figures/rendered/F09-02.png){#fig:f09-02 width=5.75in}

A **scope change** is not merely another agent plan step. The workflow must request approval from the designated policy authority or human owner, establish the new resource binding, issue a new versioned envelope, invalidate or fence stale scope where relevant, and record why it changed. A late-running investigator holding the former version must not continue accessing newly forbidden data. If an interface cannot enforce revocation immediately, the architecture must state its bounded exposure window, lease duration, and compensating containment; it must not claim instant revocation without proof.

Distinguish **identity revocation**, **work cancellation**, and **financial-effect containment**. Admission and identity (E1) can refuse new work or invalidate scoped access; coordination and ownership (E2) determines which pending investigations can stop and who owns recovery; trusted execution (E5) controls authorized payments. If `RF-1042` has already been dispatched, canceling an agent's scope does **not** imply that an external payment can be reversed. The operation may remain `UNKNOWN` following a lost acknowledgment, requiring reconciliation by trusted execution (E5), enterprise integration (E6), and durable operational state (E7)—not an admission reset or a new payment-operation identity.

## 9.6 Design alternatives and deployment consequences

For Design A, admission may lead directly into deterministic evidence checks. For Design B, it permits a model to interpret scoped customer correspondence, but the independent reviewer and trusted execution (E5) still govern financial action. For Design C, it permits bounded, dynamically chosen **read-only** steps with per-tool validation and investigation budgets. The A/B/C choice changes exposure to tool selection and information disclosure, not the monetary authority boundary.

There is no requirement to deploy admission and identity (E1) as its own server. In a modest application, authentication middleware, a case-binding service, and a governed admission module can coexist. At higher risk, separate-process isolation, a dedicated policy decision/enforcement service, tenant-specific execution contexts, or centrally managed admission may improve containment and auditability. Such separation can also increase latency and operational complexity. Choose topology by identity-risk scenarios, deployment ownership, tenancy, recovery, and assurance evidence—not because the reference diagram contains a box labeled E1.

An infrastructure-managed capability registry can tell the coordination responsibility (E2) which investigator implementation is eligible and healthy. **Registry presence is not permission to read `CASE-204`**. The coordinator may hand work to a replacement agent after failure, but the replacement must be authenticated as a workload, receive only the still-valid envelope, and obey the current ownership epoch. Chapter 10 develops task ownership and fencing; Chapter 11 specifies advisory output contracts. The admission and identity responsibility does not need to solve all of those mechanisms to establish their admission preconditions.

## 9.7 Evidence and failure-oriented acceptance

`DATA-01` requires tenant-scoped reads. `AUTH-01` excludes AI-originated payment capabilities. `POL-02` reserves current policy and approval checks for execution. `OPS-01` requires ownership, observability, and containment. Admission and identity (E1) contributes to these requirements but is **not** sole enforcer of `POL-02` or the payment recovery requirement `PAY-03`. A credible review links each admission invariant to its enforcing interface and an observed negative test.

| Test or challenge | Required observation |
|---|---|
| Customer supplies another tenant's order ID | Case binding denies access; no data disclosed |
| Agent fabricates a wider `permitted_reads` field | Tool gateway ignores untrusted field; denial is traced |
| Workload is authenticated but lacks customer delegation | Resource read denied despite valid service identity |
| Scope expires or is revoked during investigation | Subsequent access denied or bounded by documented lease semantics |
| Old worker returns after scope and owner change | Stale scope/epoch cannot commit a new case transition |
| Agent requests `issue_refund` at admission | No payment-capable tool or credential; rejected |
| Provider acknowledgment is lost after later authorized dispatch | `RF-1042` remains unchanged; trusted execution (E5), integration (E6), and durable state (E7) support reconciliation—not admission (E1) |

A QA report should identify the executing role and tenant, identity-provider and policy versions, relevant request/response traces, denied resource and tool paths, and responsible reviewer. Preserve enough evidence to reconstruct authorization decisions without turning logs into uncontrolled stores of private customer data. Negative testing must exercise actual deployed permissions and network routes; a prompt that politely declines a refund does not prove a missing payment credential.

The **release blocker** is an enforceable-boundary failure, not merely a low model score. If an agent can access a different tenant by changing its tool arguments, the investigation path is unsafe even when recommendations are accurate. If revoked scope remains effective beyond its documented limits, the assurance claim fails. If admission was denied but a subsequent component processed the work anyway, the system lacks end-to-end enforcement.

## 9.8 Engineering synthesis and bridge

Admission and identity (E1) turns a loosely expressed request into a **verified, bounded, durable work assignment**. It establishes caller identity, case relationship, tenant, purpose, permitted investigation, issuer, limits, and reviewability. It does not decide eligibility for a $500 refund, authorize payment, execute `RF-1042`, or transform a provider timeout into success. Those limits are central design features, not shortcomings.

The next question is how an admitted case remains owned while services, humans, and agents change. **Chapter 10** develops the coordinator, capability registry, durable ownership, handoffs, and fencing—building on the identity and scope contract established here, without moving the financial authority boundary away from trusted execution (E5).

## Chapter 9 — Engineering practice

1. **Specify.** Define an admission envelope for `CASE-204`. Distinguish caller identity, workload identity, case binding, and allowed investigation from refund approval.
2. **Attack.** Change the supplied order identifier to another tenant's record. Show the enforcing boundary and evidence required for `DATA-01` to pass.
3. **Revoke.** Expire an envelope midway through Design C's read-only investigation. Trace denied reads, stale workers, accountable handoff, and preserved audit evidence.
4. **Compare.** Determine how the admission scope (E1) differs across Designs A, B, and C without granting any agent financial credentials.
5. **Defend.** A vendor advertises “single sign-on for agents.” Identify the missing case-binding, delegation, resource, revocation, and downstream checks before accepting the claim.
6. **Recover.** Explain why canceling the investigator after a payment timeout cannot determine whether `RF-1042` completed, and assign the correct reconciliation owner.

**Review standard:** A defensible answer identifies the concrete principal, tenant, case, purpose, permissible tools, enforcer, negative test, and accountable owner. Merely adding an identity token to a model prompt or labeling an API “trusted” does not establish authorization.

**Sources and further reading:** The preceding chapters' security, workflow, distributed-systems, and assurance foundations remain applicable, including NIST AI RMF (2023), ISO/IEC/IEEE 29148:2018, and standard identity and access-control practice. This chapter's specific admission envelope and `CASE-204` tests are ETIS reference-design constructs; they are not claimed as normative provisions of those external sources.
