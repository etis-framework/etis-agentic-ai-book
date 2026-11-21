# Chapter 33 — Release Engineering and Operational Readiness

Part VI: Governance, Economics, and Operations

> **Engineering proposition:** A release is not the promotion of a passing agent demonstration. It is a time-bounded, scope-limited authorization to expose a verified configuration to consequential work—with independent stop controls, observable evidence, and a safe way to withhold or withdraw *future* work.

## Learning objectives

After this chapter, the reader should be able to construct an agentic release candidate from independently identified model, prompt, tool, policy, code and connector versions; distinguish verification evidence from production authority; choose staged exposure for bounded autonomy; define operational readiness, failure gates, and accountable go/no-go decisions; respond to an unknown refund outcome without replay; and map each claim to existing companion fixtures and the production evidence they cannot provide.

## 33.1 Release the whole decision path, not just the model

The release unit for agentic artificial intelligence (AI) is **a governed system configuration**, not a model checkpoint. A model update can alter tool choice while leaving API signatures unchanged; a new retrieval corpus can change the evidence an agent considers; a tool allowlist can quietly widen autonomy; a policy hot reload can change a previously acceptable $500 request; and a payment-adapter change can alter the meaning of a timeout. Any of these can invalidate an earlier release argument. Chapter 31 established bounded claims and falsifiers; Chapter 32 assigned decision rights and emergency intervention. This chapter turns that evidence and authority into an **operable release contract**.

The running case is **CASE-204**, a customer complaint involving a possible **$500 refund**. **RF-1042** names the stable *trusted* refund operation only after independent authorization. **Design A** is the deterministic baseline; **Design B** combines bounded AI advice with independent business authorization and remains the conditional first-production candidate; **Design C** optionally adds bounded investigative agents without payment authority. These are architecture choices, not Builds 0–5. The six builds are separate Python teaching checkpoints, not one certified deployment.

The logical reference architecture divides admission and identity (E1), durable coordination and ownership (E2), untrusted agent reasoning (E3), context and provenance (E4), independently trusted execution (E5), controlled provider integration (E6), durable operational state (E7), authoritative external business truth (E8), and governance and assurance (E9). The advisory proposal (C04) is *not* the independent decision (C05). Durable intent (C06) precedes provider dispatch (C07). Status-only reconciliation (C08) consults existing E8 evidence; assurance collection (C09) never creates financial permission. These responsibilities are logical; production isolation, independent keys and enforcement must be verified. A deployment system that replaces E5 verification with an agent's approval label has changed architecture, even if all unit tests still run.

## 33.2 Release integrity, independent control, and authority boundaries

**Table 33.1 — Release candidate manifest: required fields and provenance**

| Field / decision | Required evidence and accountable owner | Existing companion illustration versus missing capability |
|---|---|---|
| `release_id`, source revision and artifact digest | Build/release engineering pins revision, dependencies and signed artifact provenance | `assurance/collect.py` hashes registered local sources; no signed release artifact or provenance attestation |
| Model, prompt and tool inventory | Agent platform owner records versions, permitted tools, evaluation cohort and prompt/config hashes | Builds 1–2 illustrate bounded advice/context; no deployable model registry or evaluated production prompt lock |
| Context corpus and data policy | Data owner records source, freshness, tenancy, sensitivity and rollback/reindex procedure | Build 2 provenance tests are local; no production corpus synchronization or retention service |
| E5 authorization and E6 adapter versions | Finance/security owners document scope, grant issuer/key policy, fail-closed behavior and connector contract | Build 3 local denial and Build 4 mock adapter; real approver revocation, credentials and provider settlement unproved |
| E2/E7 schema, owner fencing and migration plan | Operations owner records epoch compatibility, durable state migration and recovery checkpoints | Build 5 fences local E2; E5 does **not** independently enforce current-owner epoch |
| Verification claims, gaps and approvers | Independent assurance, security, finance and operations record executed evidence, exceptions and scope | `assurance/README.md` supplies bounded local evidence; does not issue release approval |
| Activation, telemetry, stop and restoration | Release/incident authorities name cohort, canary metrics, trip conditions, rollback owner, and replay prohibition | `operations/incident.py` is read-only; no live deploy, kill switch, production alerting or protected audit sink |

**This table specifies a production manifest, not a Python class or an existing repository file.** The companion implementation provides examples of hashes, grants, tests and state transitions; it does not implement `release_id`, production signing, cohort routing or an enterprise change-approval service. A reader must not mistake a table column for an implemented field. Pin the manifest in an independently protected release record. A rollback must restore compatible code/configuration *without rolling back authoritative E7 intent or E8 payment truth*.

![](assets/shared-figures/rendered/F33-01.png)

*Figure 33.1 — The governed release boundary. Candidate evidence informs, but does not grant, accountable activation. Advisory change is separated from independently controlled financial execution and operational truth.*

**Changing agents are changing release artifacts.** Changes to models, tool catalogs, prompt policies, retrieval indexes, persistent memory or learned behavior can alter an agent’s decision surface without changing its calling application. Treat each change as a versioned candidate requiring impact analysis, regression evidence, rollback/containment and accountable approval.

An agent may propose improvements but cannot expand its own tool grants, modify E5 policy, change its release cohort or replace evidence standards. Mechanisms that constrain execution, authorize effects, record actions or suspend operations must remain independently governed and verified. Independence must be demonstrated: agents must not be able to modify these controls, obtain their privileged credentials, manipulate authoritative inputs or bypass enforcement. Containment and termination must not depend on agent cooperation.

Online adaptation with consequential permissions remains a separately controlled production design problem; Builds 0–5 do not supply a safe self-modification mechanism.

## 33.3 Promotion gates must test invariants, not attractive averages

Promote through development, preproduction integration, and progressively exposed production cohorts only when each environment provides the evidence appropriate to the risk. In development use local, deterministic fixtures for typed contracts and negative authorization cases. In preproduction use representative tenant separation, identity/credential service behavior, deployment topology, provider contract sandboxes, migration rehearsal, failure injection and independent log collection. Production admission requires named authorities and live restrictions; passing preproduction is necessary evidence, not automatic entitlement.

**Table 33.2 — Minimum stage gates for consequential release**

| Gate | Falsifier to exercise | Pass evidence and restriction |
|---|---|---|
| Identity and delegated scope | Cross-tenant work, expired identity, prompt/tool instruction outside allowlist | E1/E2/E4 deny; exact policy version and principal in protected audit |
| Financial authorization | Valid but compromised agent token, wrong case/amount/recipient, stale grant | Independent E5/C05 denial; no E7 intent or E8 effect in tested boundary |
| Distributed ownership | Two coordinators or stale lease attempt to progress consequential action | E2 fenced locally **and** separately proven E5 current-owner epoch gate before Design C production |
| Unknown external effect | E6 sends RF-1042, E8 may commit, response is lost | Durable original E7 operation; `UNKNOWN`; status-only C08 inquiry, no C07 blind retry |
| Observation and intervention | Evidence sink down, anomalous denial rate, canary stop | Protected signals and independent E5/E6 route quarantine proven; observability failure visibly degrades release eligibility |
| Restoration and compatibility | Old/new schema overlap, grant policy changes, recovery operator replacement | Explicit state/version migration; approved restore scope; unresolved original effects never replayed |

A statistical model score, a high task-completion percentage or a green CI pipeline cannot compensate for a failed independent-financial-gate test. **Continuous integration (CI)** builds and checks candidate artifacts; **continuous delivery/deployment (CD)** is the controlled promotion mechanism, not a replacement for decision rights. When evidence is missing, record `NOT_IMPLEMENTED` or `EXTERNAL_EVIDENCE_REQUIRED` rather than issuing a synthetic pass. Chapter 31's claim–falsifier discipline remains the standard. Site reliability engineering treats progressive release, safe operational changes and post-change measurement as engineering disciplines (Beyer et al., 2016); the financial gates in Table 33.2 are ETIS design prescriptions rather than claims about that source.

## 33.4 Progressive activation is scoped autonomy, not just traffic splitting

A staged release should control *both* traffic exposure and **the permitted consequence**. Start with shadow or read-only proposals where production data policies allow them, then a narrowly selected staffed cohort with an E5-verified independent stop, then larger cohorts after evidence review. A shadow agent must not secretly invoke E6 or mutate E7 intent. A canary that routes only 1% of requests can still cause an unacceptable unauthorized payment; percentages are not risk limits. Configure tenant, case type, amount, agent tool scope, transaction ceiling, provider region, time window and maximum outstanding `UNKNOWN` cases explicitly. A service-level objective (SLO) may bound latency and availability, but the *no unauthorized or duplicate financial effect* invariant is not traded against an error budget.

**Illustrative release:** The team considers moving CASE-204 triage from Design A to Design B. The first production slice permits bounded advice, but all $500 refund proposals remain advisory C04 requests. Finance's separately verified case-bound approval and E5 enforcement remain unchanged. E7 still records RF-1042 before any E6 dispatch. The canary monitors denial outcomes, uncertain-effect queue age, source provenance and human review burden. Design C is withheld until actual E5 epoch validation, delegation controls and operator containment are demonstrated. In no phase does a higher model confidence expand financial authority.

Promotion must stop if a canary shows an unexpected E5 allow, changed grant-verification outcomes, new cross-tenant access, opaque evidence gaps, unbounded tool use, loss of reconciliation capability or an unresolved `UNKNOWN` backlog beyond policy. The release owner can *reduce* exposure immediately through preauthorized containment; widening exposure requires a new recorded decision. Release state should be `PREPARED`, `APPROVED`, `LIMITED`, `EXPANDING`, `PAUSED`, `RETIRED` or a similarly explicit deterministic state machine, with separately governed transitions and historical evidence. These are **proposed release states**, not statuses emitted by the Python examples.

![](assets/shared-figures/rendered/F33-02.png)

*Figure 33.2 — Controlled activation state machine. A pause blocks new consequential dispatch through the independent route; rollback changes future software exposure, not the history or uncertain status of RF-1042.*

## 33.5 Readiness is a tested operational capability

A release committee needs more than a dashboard screenshot. Identify the named owner for admission, agent runtime, context, E5 authorization, E6 provider adapter, E7 durable state, C08 reconciliation, security, finance and incident command. Confirm staffed on-call coverage, credential rotation and revocation, audited policy version changes, bounded queue limits, safe degradation, evidence retention, reconciliation deadline, schema migration, repair rehearsal and provider liaison. Define how to suspend *effectful* work without disabling the only authorized read-only recovery path. Chapter 30's **Runbook 30-A** covers containment/reconciliation; Chapter 32's **Runbook 32-A** covers governance restoration. Neither is an executable script.

NIST AI RMF 1.0 (2023) supplies a governance and risk-management context, not certification of a release or endorsement of the specific controls here. A readiness review must answer: Who can revoke a compromised agent or approver grant independently of that agent? Which E5/E6 control makes the payment path unavailable when telemetry fails? Can incident command identify every original operation with uncertain effect, rather than guessing from trace completion? Which source provides authoritative settlement and how does an operator preserve a contradictory observation? Who can deny a release after project management wants it launched? If any answer depends on asking the agent to behave, the system is not ready for consequential work.

## 33.6 Rollback, roll-forward and an uncertain refund

Consider a canary update to the provider adapter. E5 issued the authorized RF-1042 intent and E7 persisted it. E6 dispatched the request, E8 may have accepted it, but the acknowledgment disappeared. An operator sees `UNKNOWN` and the rollout's latency alarm. **Rollback can stop new requests and restore a previously verified adapter; it cannot make the original financial effect disappear.** Replaying RF-1042 under the old adapter might pay twice. The recovery operator uses the original operation identity to perform an authorized read-only C08 query, checks amount/currency/tenant and provider provenance, and preserves `UNKNOWN` on `NOT_FOUND`, contradictory or unavailable evidence. An independent finance owner decides any later compensation as a different authorized business transaction.

At the same time, pause new effectful cohorts at E5/E6, protect E7 state and E8 receipts, retain change/policy/lease epochs, then restore *future* traffic only under Chapter 32's accountable authorization. If rollback cannot safely read the migrated E7 schema, the operator must choose tested roll-forward or a guarded compatibility layer rather than rewriting durable history. Once restored, the prior canary and its unknown cases remain part of the assurance record. A local Build 4 recovery test verifies only its simulated environment; a provider SLA or exactly-once claim cannot be inferred from it.

![](assets/shared-figures/rendered/F33-03.png)

*Figure 33.3 — Lost-acknowledgment release decision. Stop future dispatch, reconcile the original RF-1042 read-only, and release only after separately authorized readiness review; never convert rollback into an effectful retry.*

## 33.7 Runbook 33-A — Controlled deployment halt and recovery

**Runbook 33-A** describes an illustrative procedure for controlled deployment halt and recovery. It defines operational responsibilities and decision points rather than executable automation. Organizations must adapt the procedure to their own deployment architecture, incident authority, and recovery capabilities.

1. **Declare the change and scope.** Release engineering records immutable candidate identity, active cohort, configuration/policy versions, evidence coverage, authorization owners, and a reversible *future-traffic* routing plan. Finance confirms E5 case approval is unchanged by deployment authority.
2. **Measure and challenge.** An independent on-call observer checks denied and allowed E5 verdicts, E2 epoch anomalies, C08 availability, E7/E8 discrepancies, missing audit events, queue age and human review saturation. Separate uncertain effects from ordinary application latency.
3. **Halt independently.** On a consequential-integrity or evidence gap, incident command invokes trusted E5/E6 route stop, freezes cohort expansion, pages finance/security and preserves E7 and E8 evidence. A prompt-level stop or agent memory edit is insufficient. Retain a separately authorized read-only inquiry route where safe.
4. **Reconcile before restoration.** Enumerate outstanding original operation identifiers, investigate each `UNKNOWN` through status-only C08, and do not infer safe replay from timeout or `NOT_FOUND`. Document discrepancies with an accountable owner and deadline.
5. **Choose rollback or roll-forward.** Validate schema/policy/grant compatibility, signing and key configuration, tool permissions and read-only recovery access. Neither option may erase durable history or create a new payment to repair monitoring.
6. **Approve and observe renewed scope.** Security, finance and operations produce release-specific evidence; the designated release authority approves a bounded future cohort, with stop controls tested and explicit remaining gaps. Post-incident review updates Chapter 31 evidence and Chapter 34 lifecycle cost analysis.

## 33.8 Companion evidence, verification and release limits

Begin with `examples/refund-reference-system/README.md` and `examples/refund-reference-system/IMPLEMENTATION_EVIDENCE_MAP.md`. The source/module diagrams and invocation commands are in `build0/README.md` through `build5/README.md`. The adversarial financial gate is in `build3/service.py`, `build3/test_gate.py` and `security/test_adversarial_cases.py`; original-operation state and reconciliation are in `build4/ledger.py`, `build4/test_provider.py` and `reliability/test_recovery_cases.py`; local coordinator fencing is in `build5/test_coordination.py`; read-only incident analysis is in `operations/incident.py` and `operations/test_incident.py`; local evidence collection is in `assurance/collect.py` and `assurance/test_collect.py`. The corresponding `security/README.md`, `reliability/README.md`, `operations/README.md` and `assurance/README.md` give runnable commands and limitations. Paths after this paragraph are relative to the companion root.

**Table 33.3 — Release claim to executable fixture and production gap**

| Release claim | Executable local evidence | Required external proof |
|---|---|---|
| Agent identity alone cannot approve $500 | `security/test_adversarial_cases.py`, `build3/test_gate.py` | Independent E5 verifier, real credential custody and revocation |
| Unknown RF-1042 does not justify another dispatch | `build4/test_provider.py`, `reliability/test_recovery_cases.py` | Real provider status contract and protected E7 state |
| Stale coordinator activity is fenced | `build5/test_coordination.py` | E5 current-owner epoch enforcement and distributed fencing |
| Incident classification is non-effectful | `operations/test_incident.py` | Live independent stop control, protected monitoring and on-call rehearsal |
| Local evidence claims are reproducible | `assurance/test_collect.py` and `assurance/collect.py` | Signed artifacts, controlled attestations, independent review and change record |

The tests are **not a deployment pipeline**, and none can demonstrate actual production activation, signed supply-chain provenance, canary routing or rollback control. Do not introduce a fictitious Build 6 to bridge this gap. The professional requirement is to state the missing system and evidence before requesting authorization. A passing test is a bounded claim about fixtures, not production certification.

## 33.9 Engineering review and exercises

Evaluate the release from five operational responsibilities rather than from an agent's answer alone: the implementing engineer checks manifest/version compatibility and executable falsifiers; the enterprise architect challenges E5/E6 independence and C04/C05/C07 routing; security/assurance tests real issuer revocation and protected evidence; site reliability engineering challenges stop, provider inquiry, state migration and on-call response; the finance/business owner checks authority, loss exposure and the cost of human review. **These are decision responsibilities, not an approval vote by the model.** Each can veto unsafe exposure within defined delegated rights. Human governance is enforced by the operating system, not by prose attached to a model output.

**Exercise 33.1 — Release argument.** Construct a manifest for moving CASE-204 from Design A to Design B. Mark each Table 33.1 field `IMPLEMENTED`, `LOCAL_FIXTURE_ONLY` or `EXTERNAL_EVIDENCE_REQUIRED`, and identify the authority that may refuse the change.

**Exercise 33.2 — Canary failure.** A 2% cohort yields an unexpected E5 allow, missing C09 events and a growing `UNKNOWN` backlog. Specify stop scope, evidence preservation, C08 workflow, named owners and exact conditions for future-work restoration. Explain why lowering the cohort to 0.1% is not a sufficient response.

**Exercise 33.3 — Recovery under change.** A rollback adapter cannot deserialize the new E7 record, while E8 reports `NOT_FOUND` for RF-1042. Decide what must remain blocked, what may be queried, and which evidence would justify roll-forward rather than financial replay.

**Release decision:** A trustworthy agentic system is not one whose model release looks successful. It is one whose versioned decision path can be limited, observed, independently denied, safely interrupted and accounted for when the real-world effect is still uncertain. Chapter 34 assesses whether those controls, residual risks and ongoing human obligations justify the system's lifecycle cost.
