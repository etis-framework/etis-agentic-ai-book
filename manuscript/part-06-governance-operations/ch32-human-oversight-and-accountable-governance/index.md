# Chapter 32 — Human Oversight and Accountable Governance

## Learning objectives

The reader should be able to allocate agent, transaction and release authority; design intervention and revocation; trace governance evidence; challenge compromised-agent scenarios; and distinguish fixture tests from production assurance.

## 32.1 The missing authority between verification and deployment

Chapter 31 established fixture-bounded assurance, not automatic release approval. **Human oversight is not the ability to read an agent's answer. It is the ability of an accountable person to constrain, interrupt, investigate, deny, and authorize a bounded consequential capability through controls the agent cannot bypass.** The work of this chapter is to make that statement architectural rather than aspirational.

CASE-204 remains a customer replacement complaint involving a possible **$500 refund**. RF-1042 is the stable identifier of the refund operation created under trusted financial control; it is not an identifier that the investigating agent can invent. The familiar alternatives remain **Design A**, a deterministic process; **Design B**, bounded artificial-intelligence (AI) advice combined with independent business authorization; and **Design C**, optional bounded investigative agents added to that same trusted authority boundary. Design B is the conditional initial production candidate, not an assertion that every enterprise should use an AI model. Designs are architecture alternatives; Builds 0–5 are implementation checkpoints. More autonomy does not create authority.

The reference architecture assigns admission and identity (E1), coordination/ownership (E2), advisory reasoning (E3), context/provenance (E4), trusted execution (E5), controlled provider integration (E6), durable operational state (E7), authoritative business truth (E8), and enterprise governance/assurance (E9) logical responsibilities. Chapter 8 defines their interfaces. **These are logical responsibilities, not necessarily separate servers or security principals.** The advisory action-proposal handoff (C04) carries a typed, untrusted request toward E5. The independent financial decision (C05) and durable intent (C06) precede controlled provider dispatch (C07). Read-only reconciliation of the original operation (C08) consults E8 evidence; the assurance/evidence handoff (C09) connects operational facts to accountable review. Real boundaries require deployment evidence.

![](assets/shared-figures/rendered/F32-01.png)

*Figure 32.1 — Three separate authorities. Agents and managers may request actions; independently enforced transaction control decides on financial effects; enterprise governance constrains software and operational capability. No approval record is an alternate payment route.*

## 32.2 Decision rights are a system design artifact

**Table 32.1 — Accountable decisions and enforcement for CASE-204**

| Decision | Accountable authority | Enforced or evidenced by | What does not confer this authority |
|---|---|---|---|
| Admit case investigation | Identity/workflow owner | E1 scope and E2 work-order limits | Customer narrative or retrieved document |
| Request additional evidence | Bounded investigator | E3/E4 tool allowlist, provenance and time/tenant limits | A general-purpose agent's self-declared role |
| Recommend $500 | Agent or deterministic rule | Typed advisory C04 proposal with source references | The proposal's confidence or suggested operation ID |
| Issue case-bound financial approval | Separately authorized finance/business approver | Trusted grant issuer, policy and E5 C05 validation | Agent token, chat assent or deployment approval |
| Create and dispatch RF-1042 | Independently controlled E5/E6 service | E5 validation, E7 durable claim, controlled E6 provider credentials | Human approval note by itself or E2 owner lease |
| Quarantine an unsafe route | Incident commander under emergency policy | Trusted E5/E6 disablement, evidence preservation | Prompt telling an agent to stop |
| Reconcile unknown effect | Authorized recovery operator | C08 status-only query on existing RF-1042, E7/E8 comparison | Reissuing a refund or assuming NOT_FOUND means FAILED |
| Authorize release or restoration | Designated release authority with security, finance and operations signoff | Deployment gate, recorded restrictions, independent stop controls | Green local tests, model score, or manager optimism |

## 32.3 Authority must follow the actual request path

The C04 advisory request may contain the case, desired amount, reason, evidence pointers and correlation identifier. It must never contain authoritative E5 credentials or cause E6 dispatch directly. E5 must independently validate the current permitted principal, tenant, exact case, amount/currency, approved recipient, policy/grant issuer, expiry and operation uniqueness. The grant and the operation are distinct artifacts. Where approval is denied, E7 must not create a financial intent and E8 must not receive a payment. **A signed or valid E1 access token authenticates a workload; it does not supply the missing transaction-specific business grant.**

Logical separation does not guarantee physical isolation. A finance rule in a second Python function within the investigator's own process can be bypassed if the same process can replace the rule, read its secret or call the provider directly. A true enforcement design specifies the privileged endpoint, service identities, provider-credential custody, deployment isolation, secret rotation, immutable decision evidence, and what happens when the verifier is unavailable. A timeout is not approval. E2's lease/epoch logic is likewise not enough: Build 5 fences local E2 updates, but the educational E5 service does **not** independently validate the current epoch. That unresolved seam blocks any production claim of end-to-end stale-owner containment.

## 32.4 Human intervention is a state transition, not a conversation

An **intervention** changes what the system can actually do. An approval, hold, cancellation, override or revocation must identify its scope and be checked at the appropriate enforcement boundary. The decision state should include `REQUESTED`, `AWAITING_REVIEW`, `APPROVED_FOR_REVIEWED_SCOPE`, `DENIED`, `EXPIRED`, `SUSPENDED` and `REVOKED` where applicable. These are governance concepts, not new state names implemented by the reference builds. They do not replace E7's financial states, especially `UNKNOWN` for a possibly completed external effect.

A reviewer interface should provide: the original case record, material sources and provenance, the agent's recommendation explicitly marked advisory, the authorized amount/currency and payee, discrepancies, policy version, unresolved external effects, alternative actions, and the audit consequences of approval. It should forbid silent approval by inactivity. A decision must bind a human/workload identity, role, tenant, case, action, limits, decision time, expiry, applicable policy, evidence reference, and unique decision identifier. A new amount, recipient, material case fact or policy revision requires re-evaluation; approval of $500 for CASE-204 is not approval of another case or a $700 replacement request.

**Table 32.2 — Proposed governance decision record (not an implemented companion schema)**

| Field | Required meaning | Enforcement/falsifier |
|---|---|---|
| `decision_id`, `actor`, `role` | Unique provenance and independent approver identity | Missing, shared or revoked identity blocks use |
| `tenant`, `case_id`, `action`, `amount`, `currency`, `recipient` | Exact authorized transaction context | Any mismatch denies at E5 |
| `policy_id`, `policy_version`, `effective_window` | Rules under which the decision was made | Expired or superseded policy is never silently accepted |
| `evidence_refs`, `exception_reason` | Inspectable support and explicit deviation | Inaccessible evidence or unsupported exception is review-required |
| `decision`, `issued_at`, `expires_at`, `revocation_ref` | Bound result and time/revocation semantics | Denial, expiry, revoked grant or unavailable check blocks use |
| `reviewer_separation`, `audit_ref` | Proof of authorized separation and trace | Self-approval or unprotected evidence fails assurance |

**Implementation crosswalk.** These are *proposed record fields*, not Python attributes to search for in a `GovernanceDecision` class. The closest runnable example is `examples/refund-reference-system/build3/contracts.py`: `issue_fixture_grant()` issues `approval_id` (a partial analog to `decision_id`), `approver` (partial `actor`), `tenant_id`, `case_id`, `amount_cents`, `policy_version`, `issued_at` and `expires_at`. Its `build3/service.py` validates the grant; `build3/test_gate.py` tests rejection. Build 4's `provider_contracts.py` and `ledger.py` separately represent operation `currency` and durable outcome. The fixture grant does **not** implement `role`, `recipient`, `policy_id`, `effective_window`, `evidence_refs`, `exception_reason`, a complete decision state, `revocation_ref`, `reviewer_separation` or `audit_ref`. Nor does it independently enforce those missing fields. Mapping is illustrative, not equivalence; adding production governance requires an independently protected issuer, verifier, revocation store and audit evidence.

![](assets/shared-figures/rendered/F32-02.png)

*Figure 32.2 — Intervention sequence. Human containment is enforced at the trusted route; recovery uses the existing operation identifier and independent provider evidence. Restoring service does not replay an unknown payment.*

## 32.5 Policy lifecycle: the version deployed matters

**Example change.** Finance proposes reducing automatic review eligibility from $500 to $250. An investigator prepared a $500 recommendation for CASE-204 under the previous policy. A deployment operator must not silently treat this recommendation as grandfathered approval. The business/policy owner decides explicit effective-time and in-flight semantics, the financial gate evaluates them, and the evidence trail records whether the original grant remains valid. Where safe continuity cannot be established, hold for human adjudication. A policy hot reload that changes a safety decision between E5 grant validation and E6 dispatch must be fenced by a defined transaction/version contract. Otherwise the system can truthfully log “policy passed” while executing under a later, different rule.

## 32.6 Adversarial CASE-204 decision walk-through

Start with a genuine, bounded investigator identity admitted through E1. An attacker compromises or hijacks this agent and supplies a valid agent/service token, then instructs it to issue a $500 CASE-204 refund. In Chapter 29's actual Build 3 subprocess test, this token does not supply the separately issued case-bound finance grant. E5 denies the attempt. Within the tested fixture, there is no E7 financial record or E8 simulated provider effect. This does not prove production credential isolation; fixtures use local issuers and mock payments. Finance, security and release owners must act on denials without exposing provider credentials.

Now suppose an agent proposes the same $500 refund and a manager types “approved.” The message is evidence of human intent only. Until the trusted grant issuer authenticates that manager, validates decision rights and issues a scope-bound grant accepted by E5, no payment may occur. If the manager has deployment authority but not finance authority, the gate must still deny. If the finance grant is valid for a different case or recipient, the gate must deny. If the policy verifier is unavailable, the gate must hold rather than fail open. Fixtures cover only some outcomes; Table 32.2 is a specification, not a runnable revocation system.

Finally consider Chapter 28's lost acknowledgment. E5 has already created RF-1042, E7 records durable intent, and E6 may have sent the approved request to E8; acknowledgment disappears. The local state is `UNKNOWN`, even if the provider committed the $500 refund. A new reviewer, incident commander, or replacement E2 owner cannot approve “retry” as a way around the uncertainty. An authorized recovery identity makes a **read-only C08 status query for RF-1042**, compares identity, amount, currency and finality to E7, and retains `UNKNOWN` when provider evidence is inconsistent, unavailable or `NOT_FOUND`. Any compensation needs separate authorization, not a disguised resend.

![](assets/shared-figures/rendered/F32-03.png)

*Figure 32.3 — Accountable decision gate. Advice, deployment approval and finance authorization are separate. Uncertain original effects never branch directly into new dispatch.*

## 32.7 Emergency suspension, recovery, and restoration

A **runbook** is a repeatable, role-assigned operational procedure with explicit stop conditions and evidence requirements. Chapter 30 introduced the incident-response pattern in **Runbook 30-A**. **32-A** means *the first runbook in Chapter 32*; it is a book-local reference, not a companion-code file, external standard or executable automation. This one extends incident containment to governance authorization and safe restoration.

**Runbook 32-A — Govern an unsafe consequential capability**

1. **Declare and assign.** The incident commander records the suspected bypass, exact service and tenant scope, signal confidence and a named finance decision owner. Security evaluates credential exposure. Declare degraded evidence explicitly if E9 telemetry is absent; absence of alerts is not absence of effects.
2. **Contain at the trusted boundary.** Disable the affected E5/E6 route or provider credential according to preauthorized emergency policy; do not rely on stopping E3 prompts or E2 work assignment. Preserve an independently authorized, read-only C08 recovery path if permitted. Stop both automated and manual unauthorized payment entry points.
3. **Preserve and reconcile.** Protect E7 intent/history, E8 receipts, E2 ownership records, E5 grant decisions, deployment/policy versions and protected evidence exports. Validate original-operation identity for each `UNKNOWN`; never issue a blind second C07 dispatch. Use explicit owner/deadline when external truth cannot be established.
4. **Determine scope and revocation.** Security records which agent/service credentials, approvers, signing keys and policy versions remain trustworthy. The finance owner reviews case-level exposure. An expired or compromised grant is not renewed by the mere passage of a new incident commander.
5. **Authorize restoration separately.** Operations demonstrates route controls, healthy authorization, evidence visibility and provider read-only inquiry; security verifies remediated trust roots; finance reviews unresolved cases; the designated release authority records the accepted rollout scope, canary/rollback conditions and time. **Restoration allows future eligible work; it does not replay RF-1042.**
6. **Reassess and learn.** Preserve a causal post-incident record, decisions and dissent, changed policies, tested remediation and triggered reassessment dates. Feed new failure cases into Chapter 31 assurance and Chapter 33 release/readiness controls.

## 32.8 Federated operating model and economic tradeoffs

A practical default is **federated governance**: enterprise owners define shared trust, identity, policy, assurance and incident standards; a platform team operates admission, coordination, trusted execution, registry, observability and evidence infrastructure; domain finance/business owners define transaction limits, review criteria and outcome liability; security independently challenges credential and authorization paths; site reliability engineering (SRE) owns operational readiness with incident command; and a release authority owns controlled activation. Central review can bottleneck; distributing E5 secrets invites bypass. Delegate work widely only where the independent control point and audit owner remain credible.

**Table 32.3 — What must be measured for a governance choice**

| Choice | Benefit sought | Failure/cost to evaluate | Non-negotiable gate |
|---|---|---|---|
| Design A deterministic flow | Predictability, low inference cost | Rule-maintenance burden and manual exception effort | Same financial and recovery authorization |
| Design B bounded advice | Faster triage, better context | Review workload, model error, provenance and evaluation spend | Untrusted C04; independent E5 |
| Design C optional agent investigation | Adaptive evidence gathering | Tool sprawl, delegation churn, context exposure and incident tracing | E1/E2/E4 scope; no agent payment authority |
| Central trusted finance gate | Consistent control and evidence | Latency, concentrated outage and shared-key risk | Tested fail-closed behavior and recovery |
| Human review of exceptions | Business judgment and accountability | Queue growth, review fatigue and inconsistent approvals | Exact scope, evidence and separation of duties |

## 32.9 Existing companion code: evidence, not a new build

Begin at `examples/refund-reference-system/README.md`, then consult `IMPLEMENTATION_EVIDENCE_MAP.md`. The six progressive stages are `build0/README.md` through `build5/README.md`; each describes its own source/module diagram. **The chapter specifies governance controls over existing builds; no additional build is provided.** For the actual compromised-investigator denial, follow `security/README.md` and the Build 3 trusted gate in `build3/README.md`. For lost-reply and no-redrive behavior use `build4/README.md`, `build5/README.md` and `reliability/README.md`. For read-only incident classification use `operations/README.md`; for a bounded, source-digest evidence bundle consult `assurance/README.md` and `assurance/collect.py`. Paths are repository-relative unless stated otherwise. The executable regression entry points are `security/test_adversarial_cases.py`, `reliability/test_recovery_cases.py`, `operations/test_incident.py`, `assurance/test_collect.py`, `build3/test_gate.py`, `build4/test_provider.py`, and `build5/test_coordination.py`. Run the README commands; this is not an integrated production runtime.

**Table 32.4 — Governance assurance trace (existing checks, no new effectful path)**

| Governance claim | Companion entry point | Locally observable property | Required production evidence |
|---|---|---|---|
| Underprivileged, valid-token investigator is denied | `security/README.md`; `build3/README.md` | Actual local E5 subprocess denial; absent simulated E7/E8 effect | Distinct security principals, grant issuance and provider secret custody |
| Original unknown financial effect cannot be blindly resent | `reliability/README.md`; `build4/README.md` | `UNKNOWN` and read-only original-operation inquiry in fixtures | Real provider status consistency, idempotency retention and settlement |
| Stale coordinator cannot update local E2 work | `build5/README.md` | Local lease/epoch fencing test | Current-owner/epoch validation independently at E5 |
| Observer does not create payment | `operations/README.md` | Read-only assessment and negative database-change assertions | Protected telemetry, operational disable route and response drill |
| Reproducible evidence is not release approval | `assurance/README.md`; `assurance/collect.py` | Registered tests and local source digests | Independent audit custody, signoff, live adversarial/model evaluation |
| Human intervention and policy revocation are independently enforced | **Not implemented** in companion | Design contract and falsifiers in Tables 32.1–32.2 only | Protected approver identity, live revocation, E5 binding, deployment kill switch |

**A deliberately failing production-acceptance question:** Can the local fixtures prove that a finance approver's role was revoked before an in-flight grant was consumed, or that a compromised E2 worker cannot reach E5? **No.** Those behaviors are specified, not implemented. Claiming otherwise would convert the absence of a test into fabricated assurance. Record `NOT_IMPLEMENTED` and `EXTERNAL_EVIDENCE_REQUIRED` with owners and stop conditions.

## 32.10 Governance review and acceptance test

Before approving an agentic refund workflow, require evidence in each of these areas:

- **Implementation:** Locate receiver-side E5 denial and demonstrate no E7/E8 effect; show the agent cannot reach the payment adapter or provider credentials.
- **Deployment architecture:** Trace identity, coordination, provenance, trusted execution, provider truth and governance across actual security boundaries, not merely boxes on a diagram.
- **Reasoning and verification:** Distinguish Design B from Build 1, manager assent from an E5 grant, and `UNKNOWN` from `FAILED`; supply a falsifier for each claim.
- **Adversarial security:** Challenge cross-tenant grants, policy versions, shared keys, revoked approvers, tainted sources and unavailable verification.
- **Operations:** Rehearse lost acknowledgment, quarantine, missing evidence, takeover and safe restoration without resending RF-1042.
- **Business accountability:** Document customer impact, reviewer capacity, financial liability, decision scope and value at risk; performance gains cannot waive financial controls.

**Exercises.** (1) *Design and defend:* create an authorization matrix for a $500 refund with a reviewer who may approve up to $250, then specify E5 denial and audit evidence. (2) *Falsify:* give a compromised Design C investigator a valid E1 token and forged manager-approval text; identify the independent tests and downstream non-effects required. (3) *Operate:* construct a five-event timeline where RF-1042 receives no acknowledgment, E2's owner changes and an incident commander orders restoration; write the permissible and forbidden transitions. (4) *Evaluate alternatives:* estimate reviewer load and total lifecycle costs for A/B/C under explicitly stated assumptions, without trading away mandatory authorization. (5) *Govern change:* propose a policy-version rollout with in-flight grants and define evidence invalidation, canary stop conditions and revocation review.

**Acceptance standard.** A Chapter 32 design passes only when every consequential decision has an authorized owner, an enforceable receiving-boundary check, case-specific scope, independently inspectable evidence, explicit denial/expiry/revocation behavior and a restoration path that cannot replay uncertain money. Local tests establish only their stated fixture properties; protected production authority, audit custody, provider behavior and controlled human intervention require separate evidence. Release and operational readiness must carry these decision rights into deployment; lifecycle evaluation must account for their continuing cost and risk.
