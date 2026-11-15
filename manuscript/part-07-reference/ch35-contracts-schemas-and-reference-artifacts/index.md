# Chapter 35 — Contracts, Schemas, and Reference Artifacts

Part VII: Reference and Application

> **Engineering proposition:** A reference architecture becomes usable only when every consequential claim has a named owner, a bounded contract, a testable denial or failure outcome, an evidence trail, and an explicit implementation limit. Neither an agent's plausible answer nor a successful demonstration can substitute for independent authorization.

## Learning objectives

After this chapter, the reader should be able to trace a business request through the nine logical architectural responsibilities; separate an advisory proposal from a trusted financial operation; interpret the nine cross-domain contracts without inventing integrated Python call paths; locate the exact companion implementation and negative tests for a specific assurance claim; design a reviewable decision/evidence record; and identify which safety claims remain unverified outside the educational fixtures.

## 35.1 Choose the right reference before implementing

The running case is **CASE-204**, where an investigator may recommend a **$500 refund**. A separate, independently authorized financial operation is identified as **RF-1042**. **Design A** is a deterministic case workflow. **Design B** combines bounded artificial-intelligence (AI) advice with independent trusted financial execution and is the conditional initial production candidate. **Design C** optionally adds specialist investigative agents, without changing who may spend money. These are alternative solution designs, not the six implementation stages. Builds 0–5 are separately runnable Python teaching checkpoints, not a complete enterprise transaction service.

The logical architecture assigns admission and identity (E1), durable coordination and owner fencing (E2), untrusted advisory reasoning (E3), scoped context and provenance (E4), independent trusted execution (E5), restricted provider integration (E6), durable operational state (E7), authoritative business/provider truth (E8), and governance and assurance (E9). Contracts C01–C09 describe the required handoffs; Chapter 8 develops their rationale, while Appendix A provides the full quick reference. A logical E5 box does not prove a separate security principal, external key custody or operating-system isolation.

Three reference layers must stay distinct. **Normative design obligations** describe what a production implementation must enforce. **Educational execution evidence** is the bounded behavior the checked-in Python tests actually exercise. **External assurance evidence** comes from independent production identity, finance approval, real payment-provider agreements, monitoring, audit custody and operating drills. A correct reader navigation path must identify which layer it reaches.

## 35.2 Contract-level handoffs and their failure meanings

**Table 35.1 — Contract lookup: sender, receiver and non-negotiable refusal or uncertainty**

| Contract | Architectural transfer | Required failure interpretation |
|---|---|---|
| C01 — Admission | E1 accepts identity, tenant, purpose and deadline for E2 | Invalid or out-of-scope identity is rejected; it is never a finance grant |
| C02 — Work order | E2 issues bounded owner/epoch task to E3 | Stale, expired or duplicate ownership cannot authorize new effects |
| C03 — Context query | E3 requests scoped E4 source material | Wrong-tenant, stale or unprovenanced material is refused or flagged |
| C04 — Proposal | E3 produces typed advisory input for E5 | Unknown fields, invented authority and unsupported claims are untrusted |
| C05 — Decision | E5 evaluates independent policy/approval with E9 requirements | Missing or mismatched case-specific grant means deny, even with valid agent token |
| C06 — Intent | E5 records trusted operation in E7 before dispatch | No durable, unique claim means no provider send |
| C07 — Effect | E5 invokes restricted E6 adapter toward E8 | Lost acknowledgment creates uncertainty, not permission to replay |
| C08 — Reconcile | E5/E7 inquire about the original effect at E8 | Absent or conflicting provider evidence remains `UNKNOWN` |
| C09 — Assurance | Evidence from admission, coordination, advice, context, execution, integration, state and provider truth supports E9 review | Missing or stale evidence blocks a claim; logging is not authorization |

The arrows identify *logical responsibilities*, not proof that each pair is connected in the companion runtime. C04 is deliberately an untrusted proposal, whereas C05 must decide with independent authority. The C04 `operation_id` is an advisory correlation label, **not** RF-1042 and not an E6 idempotency key. E5 creates or claims the trusted operation identity only after independent authorization. Figure 35.1 makes these distinctions visible without collapsing decisions and effects into one “agent tool” call.

![](assets/shared-figures/rendered/F35-01.png)

*Figure 35.1 — Contract and authority lookup: advisory recommendations stop at the independent E5 decision; E7 durable intent precedes the E6/E8 provider effect, and C08 never authorizes a fresh dispatch.*

## 35.3 A reference artifact is a typed claim, not a decorative JSON document

When designing a production contract, begin with the minimum identity and authority facts that a receiver can independently validate. **Table 35.2 is a proposed schema design crosswalk, not a Python class or unified API present in the companion tree.** Names are illustrative except where mapped to actual modules; fields must not be copied into production without domain-specific review.

**Table 35.2 — Suggested record families and exact educational evidence**

| Record family and key fields | Educational source or test | Not supplied by the educational code |
|---|---|---|
| Admission: principal, `tenant_id`, `case_id`, purpose, expiry | `build2/identity.py`; `build2/test_scope.py` | Enterprise issuer, revocation, hardware-backed identity |
| Advisory: source reference, typed proposal, confidence/evidence | `build1/contracts.py`; `build1/test_advisory.py` | Signed enterprise provenance and binding financial approval |
| Scoped context: source, tenant, freshness, selection reason | `build2/context.py`; `build2/pipeline.py` | Connected enterprise retrieval and independent source attestations |
| Finance approval: `approval_id`, `approver`, `policy_version`, `amount_cents`, expiry | `build3/contracts.py`; `build3/service.py`; `build3/test_gate.py` | Independent approval issuer, role revocation and protected key custody |
| Trusted operation: operation identity, intent state, provider observation | `build4/ledger.py`; `build4/workflow.py`; `build4/test_provider.py` | Distributed durable store and external settlement proof |
| Ownership: worker, lease, monotonic epoch and expiry | `build5/coordinator.py`; `build5/test_coordination.py` | **E5-side current-owner epoch validation** and multi-site fencing |
| Governance/release: accountable owner, review decision, scope, artifact digest | Chapter 32 Table 32.2; Chapter 33 Table 33.1; `assurance/README.md` | A runnable governance register, production approval state machine or signed release |

A production envelope for a *proposed* finance decision might record a tenant, case, requested amount, approving human principal, independent policy version, approval expiry, release scope and immutable evidence references. However, adding an `approver` string to an untrusted agent payload does not create a valid grant. The receiver must authenticate the independent issuer, authorize the exact action and enforce expiry, tenant, amount, audience and revocation policy. The local Build 3 signer is a test fixture; its keys are not protected from an attacker with equivalent host privileges.

**Contract review checklist:** identify the producing authority; define the receiver that can reject; type or constrain every identifier; state time, tenant and audience scope; define canonical error/unknown semantics; identify durable storage and its owner; describe evidence retention and visibility; name negative tests; and record what the test cannot establish. Without those details, a schema is merely an example payload.

## 35.4 Trace CASE-204 without inventing an integrated runtime

Start with the *logical* path: E1 admits a tenant- and case-scoped request (C01); E2 assigns bounded investigation (C02); E3 may seek scoped, attributed E4 context (C03), then emit a typed but untrusted recommendation (C04). E5 independently evaluates policy and any finance grant (C05). If denied, there must be **no RF-1042** and no provider dispatch. If approved, E5 owns the trusted operation identity, ensures E7 durable intent (C06), then allows E6 controlled provider dispatch (C07). A missing acknowledgment means E7 records an uncertain observation, and C08 inquires *read-only about the original operation*. C09 gathers correlated evidence without creating another financial authority.

The actual **Build 5** demonstrator does **not** execute that complete route. Its E2 coordinator calls a **Build 4** E5 subprocess using fixture identity and grant data; it does not run the earlier Build 1 advisory and Build 2 retrieval path as one combined program. Build 5's local epoch fencing protects E2 coordination, but E5 does not independently validate the current E2 ownership epoch. These two omissions prevent any honest “complete end-to-end enterprise agent system” claim.

**Table 35.3 — Reader's shortest runnable route from assertion to falsifier**

| Question | Run or inspect | Observe / reject |
|---|---|---|
| Does a model recommendation grant spending authority? | `build1/README.md`, `build1/test_advisory.py` | Extra authority fields rejected; no provider effects |
| Can a valid token view another tenant's case? | `build2/README.md`, `build2/test_scope.py` | Scope and freshness refusal in fixture |
| Can a compromised investigator obtain an unauthorized $500 refund? | `build3/README.md`, `build3/test_gate.py`, `security/test_adversarial_cases.py` | E5 independent no-grant denial; no operation or mock payment |
| Can a lost provider acknowledgment cause an automatic second refund? | `build4/README.md`, `build4/test_provider.py`, `reliability/test_recovery_cases.py` | Original-operation inquiry; no blind redrive |
| Can a stale worker locally take over work? | `build5/README.md`, `build5/test_coordination.py` | E2 lease/epoch denial; **not** E5-side epoch enforcement |
| Can incident tooling safely stop and classify effects? | `operations/README.md`, `operations/test_incident.py` | Bounded fixture classification; no live kill-switch assertion |
| Is a test bundle a release certificate? | `assurance/README.md`, `assurance/test_collect.py` | Reproducible local evidence only; production gates remain external |

All paths in this table are relative to `examples/refund-reference-system/`. The root `README.md`, `IMPLEMENTATION_EVIDENCE_MAP.md`, and each build's embedded `architecture.svg` are the authoritative code-reading entry points. Run the tests as documented in each local README. No new Build 6 or new run-time service is needed to use this chapter.

## 35.5 State, identity and recovery invariants

The trusted path must enforce four distinct invariants. **Identity** establishes who or what requested work, never by itself why money may be spent. **Authorization** establishes case/tenant/amount/policy-specific permission independently of the advisor. **Durable intent** establishes one trusted effect identity before attempting an external operation. **Reconciliation** consults the external system of record when effects and acknowledgments diverge. `UNKNOWN` is neither `FAILED` nor `SUCCEEDED`; changing software versions or electing a new coordinator does not settle that fact.

Figure 35.2 depicts the decision that a reviewer must follow when RF-1042's acknowledgment is lost. A new owner may be elected for coordination, but it can only perform status-only inquiry while original effect status is unresolved. A new payment requires a distinct, independently authorized business decision; it cannot be a retry of the original ambiguity. Chapter 28 gives the failure taxonomy; Chapter 30 covers incident command; Chapter 33 distinguishes release rollback from financial reversal.

![](assets/shared-figures/rendered/F35-02.png)

*Figure 35.2 — Unknown-outcome decision reference: preserve the original operation and seek authoritative provider evidence; pause or escalate rather than invent success, failure or a second dispatch.*

For a production deployment, independent E5 controls must reject stale owner epochs at the consequential boundary, not only in E2's local database. Provider idempotency retention, status lookup semantics, conflicting settlement evidence, backup and disaster recovery, privileged credentials and release suspension require contracts and operational drills outside this book's fixtures. The educational negative tests are necessary evidence for the *specific simulated mechanisms* they exercise; they are not production certification.

## 35.6 Assemble a defensible evidence bundle

A professional review should start with a falsifiable claim, not a screenshot of a green dashboard. Record: **(1)** the scoped claim and threat/failure model, **(2)** the exact source revision and fixture, **(3)** the command/test and observed result, **(4)** the negative condition and independent denial point, **(5)** the business-effect check, **(6)** the known unimplemented or simulated boundary, and **(7)** the person accountable for deciding whether more evidence is required. Chapter 31 develops the claim/falsifier method and `assurance/collect.py` collects bounded local outputs; Appendix C is the reference index.

For CASE-204, a legitimate *local claim* is: a valid agent identity without a separate Build 3 finance approval cannot create RF-1042 in the fixture. A stronger, unsupported claim is: no attacker with access to the host or provider can create an unauthorized real payment. Similarly, Build 4 can demonstrate no automatic double dispatch in its mock-provider environment, but cannot attest to a live provider's idempotency window. A reviewer's job is to keep those statements separate, including in executive reports.

**Table 35.4 — Minimum engineering evidence packet for a consequential operation**

| Evidence artifact | Who owns it | Question it must answer |
|---|---|---|
| Admission and authority result | Identity and finance control owners | Was the request scoped and independently authorized? |
| Advisory provenance and denial | Domain/AI engineer | What was recommended, with what sources, and what was rejected? |
| Durable operation identity and effect state | E5/E7 owner | Which original operation was claimed, and what is actually known? |
| Provider observation / unresolved exception | Integration and finance operations | Does external business truth support a definitive outcome? |
| Recovery, incident and release decision | SRE and accountable release authority | Was another effect prevented, and who may restore capability? |
| Test, source and limitation register | Assurance reviewer | What was reproduced, what could falsify it, and what remains unproved? |

The `assurance/` fixture can help organize local evidence; it does not create independent audit custody, signed deployment provenance or organizational signoff. In an enterprise, governance and assurance (E9) must connect claims to independently observed outcomes and owners, not merely aggregate agent self-reports.

## 35.7 Reference reading paths and engineering exercises

An **architecture-first reader** begins with Chapter 8 and Appendix A, then uses Table 35.1 to find receiving responsibilities. A **build-first engineer** starts at `examples/refund-reference-system/README.md`, follows the six build READMEs and checks the implementation evidence map before asserting integration. A **security-first reader** follows Chapters 25 and 29 to the valid-token no-grant tests. A **reliability-first reader** follows Chapters 26, 28 and 30 to original-operation inquiry and containment. A **governance-first reader** starts with Chapters 31–33 and the proposed decision and release artifacts. An **economics-first reader** enters Chapter 34 but must bring the Chapter 35 control gates into every cost comparison. None of these paths requires pretending that a missing module is implemented.

**Engineering exercises:** (1) Trace an invented `approver` field from E3 to E5; identify the earliest independent denial and the test that proves the *local* result. (2) Create a filled evidence packet for a lost RF-1042 acknowledgment with outcome `UNKNOWN`; forbid any second dispatch. (3) Map every C01–C09 contract to one of: demonstrated in the named build, fixture-only, or specified but absent from the Build 5 runtime. (4) Design one production-negative test for stale-owner E5 enforcement and state why passing Build 5's current local epoch test would not satisfy it.

**Part VII handoff.** Chapter 36 applies these lookup artifacts to integrated professional engineering decisions. The readiness standard is not that every artifact looks complete, but that every consequential statement has an authority boundary, falsifier, evidentiary scope and accountable owner. The reference remains useful precisely because it refuses to confuse a proposed enterprise contract with a demonstrated Python capability.
