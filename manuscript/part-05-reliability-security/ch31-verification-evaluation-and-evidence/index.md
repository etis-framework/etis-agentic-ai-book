# Chapter 31 — Verification, Evaluation, and Evidence

## Learning objectives

By the end of this chapter, the reader should be able to: distinguish behavioral evaluation from enforcement verification; construct a risk-based, reproducible evidence package for an agentic workflow; trace each claimed invariant to positive, negative and falsification tests; identify the independent production evidence missing from educational fixtures; and defend an accountable release decision that can be revoked when evidence becomes stale.

## 31.1 From convincing demonstrations to defensible claims

CASE-204 is a fictional customer complaint involving a proposed **$500** refund. The stable consequential operation identity, **RF-1042**, belongs to independently trusted execution—not to an agent's generated explanation, a telemetry correlation identifier, or a test's display label. Chapter 28 showed why a lost acknowledgment does not prove failed payment. Chapter 29 challenged the approval boundary with a hijacked investigator possessing an otherwise valid service identity. Chapter 30 classified operational incidents without issuing a payment. **Chapter 31 asks what those experiments establish, how they can be falsified, and who is authorized to accept the remaining risk.**

The three architectures still differ. **Design A** is a deterministic workflow baseline; **Design B** introduces bounded artificial-intelligence (AI) advice reviewed by independently enforced trusted execution, and is the conditional first production candidate; **Design C** adds optional bounded investigative agents but no financial authority. A favorable model evaluation might justify better investigation efficiency for B or C. It cannot replace the authorization, state, and recovery proofs required by all three. Agentic systems multiply the observable paths—dynamic tool choices, delegation, source contamination, nondeterministic explanations, and replacement workers—without multiplying legitimate payment authority.

A **falsifier** must be clear enough to defeat a claim; passing examples alone do not suffice. An **assurance claim** is a narrowly stated property of a specified system, threat model, environment and period. An **evidence item** is a reproducible observation or inspected artifact relevant to that claim. A **falsifier** is an experiment or observation that would defeat it. Acceptance is a recorded human judgment over the entire package, not the Boolean result of a unit-test runner. Figure 31.1 separates these layers.

![](assets/shared-figures/rendered/F31-01.png)

The ETIS reference architecture assigns admission and identity (E1), coordination and ownership (E2), bounded advisory reasoning (E3), context and provenance (E4), independent trusted execution (E5), controlled provider integration (E6), durable operational state (E7), authoritative business truth (E8), and governance and assurance (E9) separate logical responsibilities. Chapter 8 and the architectural appendix define their canonical contracts. These are not nine mandatory processes or nine independently reliable sites. Verification must establish *actual* enforcement and failure boundaries, including shared secrets, hosts, databases and providers.

## 31.2 Make the claim smaller than the evidence

A claim must name its scope and its exclusion. In the companion system, the authorization-decision contract (C05) is independently checked by a local trusted-execution subprocess, while the provider-dispatch contract (C07) effects a **simulated** refund. The operational-state contract (C06) records local intent, attempts and historical observations; the read-only reconciliation contract (C08) consults simulated provider truth. The monitoring/evidence contract (C09) concerns reviewable operational records, but local SQLite history is not independently protected audit custody. An advisory action proposal (C04), however convincing, remains untrusted. Admission (C01), work assignment (C02), and context evidence (C03) establish scope and provenance; none authorizes money.

**Table 31.1 — Assurance claims and falsifiers for CASE-204**

| Claim and scope | Repeatable fixture evidence | A falsifier to seek | Production evidence still missing |
|---|---|---|---|
| Valid investigator token cannot grant $500 refund | Chapter 29 security harness, actual Build 3 E5 subprocess denial; absent local E7/E8 files | One unauthorized E5 acceptance or mock E8 row | Independent key custody, host isolation, genuine token revocation |
| Uncertain RF-1042 effect is never blindly replayed | Build 4 lost-reply tests; Chapter 28 recovery tests | A second C07 call after `UNKNOWN` or `NOT_FOUND` | Provider-specific idempotency retention, status consistency and settlement |
| Replacement worker cannot rewrite obsolete E2 state | Build 5 lease/epoch concurrency tests | Stale owner commits to the local E2 store | E5 independently consumes and enforces current-owner epoch |
| Incident analysis cannot issue a refund | Chapter 30 read-only observer; database digest comparison | New E7/E8 row caused by an observer assessment | Protected telemetry pipeline, privileged process isolation |
| Evaluated advice improves business outcomes | **Not established** by these fixtures | Regression, unsafe suggestion or unacceptable cost in representative data | Real-world evaluation dataset, drift and human-outcome review |

One passing positive control is valuable: it demonstrates that an authorized path can work. But a denial test is not merely its mirror image. Negative tests should attempt malformed requests, valid but underprivileged identities, stale ownership, wrong operation identity, contradictory payment evidence, missing telemetry, revoked credentials and unavailable verifiers. They should check **non-effects**, not only returned strings. A rejected proposal that nonetheless leaves a provider effect is a failed control.

## 31.3 Four evidence layers, four different questions

**Layer 1 — Structural and contract inspection.** Map the source modules, entry points, trust boundaries, data owners, credentials and independent control points. Inspect schemas and contracts for cross-tenant scope, original operation identity, lease epoch, record version, amount, currency, actor, policy decision and authoritative provider evidence. Tests cannot rescue a missing check at E5. Static import checks are useful regression guards, not proof that the operating system isolates identities.

**Layer 2 — Deterministic executable verification.** Use known inputs, fixed fixture provider behavior, explicit expected outputs and non-effect assertions. For RF-1042, inspect E7 transitions alongside the independent simulated E8 record; after lost acknowledgment, the local state may be `UNKNOWN` while the provider contains one payment. Chapter 28's `NOT_FOUND` tests require inquiry or escalation, never an inferred `FAILED`. Chapter 29's harness sends a genuine fixture identity assertion to the actual E5 subprocess without a separately approved financial grant. Chapter 30's read-only observer must leave both databases unchanged. A passing fixture proves precisely those exercised paths.

**Layer 3 — Agent behavior and adversarial evaluation.** Unlike deterministic financial enforcement, agent outputs are conditional on prompts, retrieved context, model/version, policy, tools and sampling choices. Evaluation needs representative tasks, contaminated documents, out-of-scope requests, latency and cost bounds, human scoring rules, and repeatability expectations. Record the model and prompt versions, permitted tools, retrieval snapshot, evaluator rubric, sample population, refusals, escalation, and every observed unsafe proposal. Prompt-injection resistance is *measured against the defined attack set*, never inferred from one successful refusal. If agent output cannot be reproduced, preserve input references and sanitized decision traces; never copy secrets or customer payloads into the evidence bundle.

**Layer 4 — Production and operational assurance.** Exercise actual workload identity and credential custody, E5 owner-epoch enforcement, independent finance-grant issuance, provider-specific read-only status guarantees, protected logs, backup/restore, incident commander authority, and canary/rollback procedures. Failure injection must include shared-dependency loss, partial effects and audit-collector outage. An unavailable provider or verifier is not a suitable signal to authorize another attempt. A release is blocked where safety-critical controls exist only as claims.

These layers are cumulative, not interchangeable. The same repository can pass 100% of its local assertions and still fail production admission because an attacker sharing the E5 process identity can access credentials or because the real provider cannot verify an RF-1042 settlement.

## 31.4 Reproducible evidence: provenance before pass rate

Figure 31.2 follows one negative case from setup through independently reviewed result. A reproducible bundle needs a test identifier, declared property, exact source and fixture digests, test command, execution time, Python/runtime description, result, sanitized output digest, expected non-effects, environmental limitations and accountable reviewer. **A percentage alone is neither traceability nor proof.** Preserve failures; do not silently replace an unsuccessful run with the best successful attempt.

![](assets/shared-figures/rendered/F31-02.png)

The educational evidence collector resides at `examples/refund-reference-system/assurance/collect.py` and is explained by `assurance/README.md` and its source architecture diagram. It invokes **existing** tests by exact unittest names, records source digests by hashing declared source files and produces a versioned JSON result with a local UTC time. The collector does not import the refund adapter, contain production credentials, sign evidence, attest the host, or authorize any refund. It is neither Build 6 nor an independent E9 audit service. A failing, missing, timed-out or interrupted test produces a nonpassing bundle. The collector uses a fixed registry and an allowlist for report fields rather than serializing raw assertions, tokens or arbitrary subprocess output.

**Table 31.2 — Evidence status vocabulary**

| Status | Meaning | Appropriate release interpretation |
|---|---|---|
| `EXECUTED_PASS` | Registered local assertion ran and returned success with expected test count | Narrow fixture property only |
| `EXECUTED_FAIL` | Test failed, errored, timed out or could not be completed | Block the associated claim |
| `SIMULATED` | Dependencies or provider behavior supplied by fixtures | Require a separate real-system gate |
| `SPECIFIED_ONLY` | Architecture or runbook contract exists without an executable enforcement test | Not an implemented guarantee |
| `NOT_IMPLEMENTED` | Required mechanism absent, including E5 owner-epoch check | Release blocker for applicable risk |
| `EXTERNAL_EVIDENCE_REQUIRED` | Independent contract, live audit or operational drill still needed | Do not substitute repository tests |

The distinction between an *observed local result* and *production acceptance* should survive every report export, management briefing and automated dashboard. A source digest proves which bytes the collector read; it does not establish that the runtime loaded only those bytes, that the machine was uncompromised, or that the output was stored immutably. A production program needs signed attestations, independent storage, access controls, retention and reviewer separation proportional to the business consequence.

## 31.5 Falsification matrix and stopping rules

Do not ask only, “Did the test pass?” Ask, “What outcome would force us to withdraw the claim?” The test plan must include the following independent negative paths:

1. **Advisory-to-finance confusion:** valid E1 identity plus forged C04 finance fields reaches E5; verify denial, no new E7 intent and no simulated E8 refund.
2. **Wrong authoritative evidence:** reconciliation supplies a different operation, amount, currency or tenant; verify no confirmation of RF-1042.
3. **Partial external result:** C07 acknowledgment disappears after a possible effect; verify original identity, `UNKNOWN`, status-only inquiry and no new payment.
4. **Ownership regression:** a superseded E2 epoch attempts to advance work; verify local rejection; separately record that E5 current-owner enforcement remains absent.
5. **Telemetry degradation:** sequence gaps, duplicate events, delayed observer, unavailable collector or contradictory E8 observations; verify classification remains unresolved and evidence loss visible.
6. **Credential incident:** revoked-token or verifier-unavailable signal results in quarantine recommendation; do not misreport that a real identity provider revoked a token.
7. **Release regression:** change the source, remove a test, corrupt an evidence manifest or trigger a timed-out command; confirm that verification cannot reuse a prior green result as current proof.

Figure 31.3 shows the release decision. **An unknown or missing safety-critical observation must not silently become acceptance.** For high-consequence effects, a failing protection, incomplete evidence lineage or unresolved external settlement contract blocks activation even if advisory quality, availability and cost targets look attractive.

![](assets/shared-figures/rendered/F31-03.png)

## 31.6 Evidence-driven release authority and economic judgment

The engineering owner may certify source/test reproducibility; the security owner evaluates identities, grants and containment; site-reliability engineering (SRE) reviews operating signals, incident readiness and recovery; the enterprise architect examines trust and deployment dependencies; the business/finance owner accepts policy and residual monetary exposure; the accountable release authority records the go/no-go decision. None of these human roles is automatically an E5 transaction-grant issuer. Approval of a deployment is not a substitute for individual financial authorization.

Separate **safety gates** from **performance objectives**. A model that reduces average CASE-204 investigation time by 40% may be economically attractive, but it does not compensate for one unbounded duplicate refund hazard. Conversely, overconservative controls may raise customer wait time and manual review cost. A responsible release decision quantifies volume, incident exposure, unresolved-case backlog, provider-query cost, false quarantine, latency, staff load and risk reduction; it never uses a weighted score to trade away a mandatory no-unauthorized-effect control.

The release record must specify artifact version, test results and exceptions, named approvers, allowed rollout population, alert thresholds, canary stop conditions, rollback authority, evidence retention, and the next reassessment date. If the real provider changes retention or status semantics, or the approval issuer rotates trust material, the prior evidence may no longer cover the deployed system. E9 governance is an operational mechanism for withdrawing authorization to proceed, not merely an end-of-project signature.

## 31.7 Companion implementation and evidence walk-through

Start at `examples/refund-reference-system/assurance/README.md`, then run `python3 -m unittest discover -s examples/refund-reference-system/assurance -p 'test_*.py' -v` to execute `assurance/test_collect.py`. The companion `assurance/collect.py` registry identifies exact runnable tests in `security/test_adversarial_cases.py` (valid-token E5 denial), `reliability/test_recovery_cases.py` (missing/wrong proof), `build4/test_provider.py` (single operation and no blind replay), `build5/test_coordination.py` (local epochs), and `operations/test_incident.py` (read-only incidents). Run its example command from the repository root to produce a local JSON evidence bundle. Evidence metadata and this chapter's falsifier matrix point to source methods, not to invented generalized guarantees.

**Professional review perspectives.** The implementing engineer audits registries, test names and non-effect assertions. The enterprise architect maps every unverified E5/E9 control to its actual deployment boundary. A falsification exercise establishes precisely which claim fails and which conclusions remain unsupported. The security reviewer stages the valid-token compromised-investigator attempt and demands independent grant custody evidence. The SRE/operator evaluates collector loss, ambiguous provider outcomes and restoration rehearsals. The business owner decides what unresolved refund exposure is acceptable and who is empowered to stop rollout. These are reader questions, not an assertion of independent publication certification.

**Limitations:** Tests run against local files and a simulated provider. Build 5 E2 epochs are not enforced by Build 4 E5. The collector measures subprocess outcomes, not real payment settlement, independent production identity, protected E9 evidence, complete model drift, red-team coverage or operator competence. A replayable test log is valuable engineering evidence; it is not an unconditional certificate of trustworthy agentic behavior.

## 31.8 Chapter exercises

1. For the six Table 31.1 claims, write one falsifier each and identify which claims cannot pass a production release gate even after every local test succeeds. Justify a test budget by risk rather than test count.
2. Modify a copy of the collector registry to refer to a nonexistent test. Predict the evidence status, run the negative test, and explain why a missing test must never inherit another test's green result.
3. Design a model/agent evaluation plan comparing Designs A, B and C under contaminated retrieval, valid-but-underprivileged identity, cost and escalation constraints. State the sample population, acceptance metrics and limits of statistical inference.
4. Draft a provider contract checklist for RF-1042: operation namespace, amount/currency identity, query consistency, idempotency retention, finality, settlement and dispute handling. Mark which clauses require external verification.
5. Assemble a mock release board: implementing engineer, architect, security, SRE and business owner. Present a versioned evidence bundle, list unimplemented safety controls, define conditional canary/stop rules and defend a no-go decision without describing a passing fixture as production certification.
