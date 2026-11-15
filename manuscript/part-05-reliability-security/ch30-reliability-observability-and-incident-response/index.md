# Chapter 30 — Reliability, Observability, and Incident Response

Part V: Reliability, Security and Recovery

> **Engineering proposition:** A fast response without authoritative evidence can turn a recoverable ambiguity into a second financial loss. Reliability means completing justified work *and* refusing unjustified consequential work, while making the difference observable and operationally accountable.

## Learning objectives

After this chapter, the reader should be able to establish separate service objectives for advisory throughput and consequential correctness; design cross-domain signals that preserve causality without revealing secrets; map logical responsibilities to independently evaluated failure and trust boundaries; run a bounded incident from detection to evidence-qualified restoration; demonstrate non-effectful incident tooling against existing coordination and ownership (E2) and durable operational state (E7) fixtures; and state exactly what local negative tests cannot establish about production containment or payment settlement.

## 30.1 Reliability is an outcome, not simply uptime

Agentic AI adds a distinctive operational failure mode: a bounded investigator may choose a plausible *next step* based on uncertain, stale or malicious advice while an independent consequential boundary must refuse the same action. Therefore monitor **agent proposal health separately from trusted execution health**. The incident responder must be able to suspend delegation without rewriting durable financial truth or manufacturing another RF-1042 operation.

CASE-204 concerns a possible **$500** refund. If independently authorized, its stable consequential identity is **RF-1042**. Design A is the deterministic baseline; Design B adds bounded AI advice under independent review and trusted execution (the conditional initial production candidate); Design C optionally delegates bounded, read-only agent investigation without financial authority. All three retain independent trusted execution and authorization (E5). A high advisory-response percentage is useless if a retry after an E8 timeout makes a second refund. Conversely, holding a case in `UNKNOWN` while obtaining reliable E8 evidence can be a *correct* service outcome even if it delays completion.

Treat three objectives separately: **availability** (eligible low-risk requests receive a meaningful response), **integrity** (no unauthorized or duplicate consequential effect), and **recoverability** (an unresolved operation receives a timely accountable disposition). Integrity is an invariant and release condition; it is not traded away to rescue an availability chart. An incident page can be successfully acknowledged while the business case remains unresolved. Successful incident handling is not proof of successful settlement.

**Table 30.1 — Illustrative objectives and their evidence owners**

| Indicator | Example policy target, not measured performance | Measurement boundary and failure interpretation |
|---|---|---|
| Advisory availability | ≥99.5% of eligible scoped investigations get a bounded result within 5 minutes over 28 days | E1/E2 completion against admitted cohort; a policy denial is not a server outage |
| Safe disposition | 100% of consequential attempts have E5 verdict and original E7 intent evidence | E5/C05 decision with E7/C06; any uncorrelated effect is a stop-release incident, not an allowable error-budget burn |
| UNKNOWN detection | 99% of locally detectable uncertain outcomes enter a durable review queue within 2 minutes | Compare E7 status transition and incident intake timestamps; absence of telemetry is itself a coverage gap |
| Reconciliation responsiveness | 95% of reachable E8 inquiries receive a validated answer within 15 minutes | E8/C08 status only; an answer of `NOT_FOUND` does not prove non-effect or resolve the case |
| Operator acknowledgement | 95% of severity-1 pages acknowledged within 10 minutes | Paging system records, staffed rota, drills; neither acknowledgment nor closing a ticket settles RF-1042 |

These are **teaching targets to be negotiated**, not empirical ETIS benchmarks or contractual provider promises. Service-level objectives and error-budget thinking follow established site-reliability engineering practice (Beyer et al., 2016); the numbers and financial safety gates here are original ETIS teaching examples. The denominator excludes ineligible requests only under an explicit, audited admission policy; otherwise a team could improve a ratio by silently dropping difficult work. For a 28-day window, a 99.5% availability objective corresponds to a 0.5% eligible-request error allowance. A separate *zero-tolerance* financial correctness control cannot be offset by unused availability budget. Compare labor, availability loss, fraud exposure, reconciliation latency, and user harm when selecting objectives. Measure from trusted event time with clock-skew and missing-telemetry qualifiers; report sample size and exclusions.

## 30.2 Observe E1 through E9 without promoting telemetry into authority

Figure 30.1 shows the nine logical responsibilities of the ETIS reference architecture and three operational lenses. Admission and identity (E1) passes scoped work through the admission contract (C01) to coordination and ownership (E2). Work assignment (C02) reaches agent reasoning (E3); scoped context and provenance (E4, C03) support an **untrusted advisory action proposal (C04)**. Independent trusted execution (E5) and its authorization decision (C05) gate the financial effect. Durable operational state (E7) preserves intent and observations through the durable-intent contract (C06). Controlled enterprise integration (E6) dispatches through the provider contract (C07) to authoritative business systems (E8), whose reconciliation contract (C08) supports **read-only status inquiries**. Governance and assurance (E9) receives telemetry (C09) but cannot authorize payment merely by observing a signal.

![](assets/shared-figures/rendered/F30-01.png)

*Figure 30.1 — Operational responsibility, authoritative evidence and failure zones. The E5 enforcement barrier is separate from E2 ownership and E9 monitoring. Dashed lines depict observation, not payment permission; physical independence must be demonstrated at deployment time.*

An incident record needs a **trace identifier** for a bounded request, a stable *operation identity* for RF-1042, a causation/event identifier, a schema version, the responsible service, event time and ingestion time, policy decision category, E2 epoch and lease generation when known, E7 transition and sequence, E8 inquiry origin, and a confidence/provenance classification. Store tenant and case identifiers as least-privileged references or approved pseudonyms; restrict the join key. Never emit raw E1 tokens, E5 grants, signing keys, provider credentials, payment payloads, E4 sensitive documents, or personal data into routine logs. Hashing is not automatically anonymization; consider reidentification and correlation risk. Access to event stores, retention windows, alert routing, and deletion holds belong to independently controlled operations and governance policy.

Use **metrics** for rates and latency (lag, queue age, denial ratio, missing heartbeats), **traces** for correlation and causal edges across boundaries, and **structured events** for transition claims. A trace span reading `provider_request_sent` is evidence of *attempted communication*, not proof of money movement. Even a locally recorded `CONFIRMED` can be contradicted by later E8 evidence: Build 4 (`examples/refund-reference-system/build4/ledger.py`) preserves its earlier observation in local `operation_events` while conservatively changing current E7 state to `UNKNOWN`. The history is local SQLite evidence, **not** a protected immutable audit service. If E9 is down, E5 must not infer that an unlogged refund is safe; high-risk execution may need to fail closed according to a preapproved control, while low-risk investigation may continue under a bounded degraded-service policy.

**Table 30.2 — Signal, interpretation and action boundary**

| Signal | What it supports | What it cannot establish | Accountable next action |
|---|---|---|---|
| E2 expired epoch or competing owner | Local coordinator state has shifted | E5 has rejected the old caller | Fence E2 locally, quarantine consequential work pending trusted E5 ownership verification |
| E7 `UNKNOWN` after E6 timeout | Effect may have occurred | Payment failed or may be safely resent | Assign accountable owner; E8/C08 inquiry on RF-1042 only |
| E8 `NOT_FOUND` or outage | No conclusive confirmation currently available | Original effect never happened | Retain `UNKNOWN`; escalate retention/consistency uncertainty |
| E5 `DENIED` with valid E1 token | Identity alone did not authorize payment in tested path | E5 secret custody or enterprise compromise resistance | Investigate scope/intent; preserve denial; no alternate dispatch |
| Missing E9 events or diverging clocks | Monitoring and ordering confidence decreased | Downstream effect is absent | Declare evidence-gap incident; preserve E7/E8 independent records |

## 30.3 Failure domains, blast radius and reliability economics

The Chapter 28 logical-zone principle is nonnegotiable. Distributed uncertainty and competing observations are discussed by Kleppmann (2017) and Gray and Reuter (1992); the following operational classification is an original ETIS teaching design: responsibility separation, trust enforcement, and physical failure isolation are *different statements*. E1 and E3 might share a host and fail together. E5 and E7 might be on different hosts but share storage or an identity verifier. E8 may be externally hosted yet depend on the same network path as E9 export. A system diagram without dependency and credentials inventory cannot prove independent containment.

Evaluate six failure families: site/process/network loss; probabilistic or deterministic advisory failure; E2 coordination and stale-owner races; partial/unknown E6/E8 outcomes; policy/credential compromise; and provider dependencies including inconsistent status reads. For each family, name the trigger, detection latency, downstream blast radius, trusted containment, evidence-retention path, and restart criterion. For a single refund, a temporary human review may be cheaper than elaborate automatic replay. Across a large payment fleet, long-lived UNKNOWN queues produce liability, customer delay and investigation expense; automation should prioritize **safe read-only triage**, not shortcuts around E5.

Capacity-plan the observation system separately: bounded event queues, backpressure, durable intake for high-criticality transitions, outage alerts, clock-health checks, tenant-aware quotas and sampling rules that **never sample away required financial evidence**. Design independent paging and evidence custody for E5/E7 critical activity. “Two replicas” is not an availability argument if both share one secret store, cluster, operator credential, or upstream service. A resilience proposal should document expected incident frequency × loss, detection cost, recovery labor, and assurance cost, then test those assumptions.

## 30.4 Lost acknowledgment: the safe incident timeline

At time T0, E2's current owner has selected an authorized operation. E5 has independently validated a financial grant and recorded the pre-dispatch E7 intent for RF-1042. At T1, E6 sends the original request to simulated E8. E8 may commit a $500 effect, but its acknowledgment is lost. At T2, E7 records `UNKNOWN`; E2 may expire, and a replacement worker may inherit the case. Build 5's lease epoch fences E2's own state; **Build 4 E5 does not verify that epoch**. A production implementation must close that seam before describing end-to-end stale-owner fencing.

![](assets/shared-figures/rendered/F30-02.png)

*Figure 30.2 — Ambiguous financial effect after a lost acknowledgment. E7 and E8 histories may differ; a replacement owner must use the original RF-1042 on C08, never make a second C07 dispatch. Time flows downward.*

At T3, the on-call incident lead quarantines the affected consequential route without deleting local state. At T4, an authorized reconciliation principal requests E8 status for RF-1042 using C08. If E8 is unavailable, returns `NOT_FOUND`, or supplies inconsistent identity, amount, currency, version, or finality, the incident remains unresolved. A convincing `CONFIRMED` observation must be verified under the actual provider contract and independently reconciled against E7. The fixture does not establish external settlement, retention windows, or query consistency. At T5, the incident record names evidence reviewed, outstanding uncertainty, business owner and next decision deadline; restoration of normal dispatch cannot follow from a green dashboard alone.

## 30.5 Severity, authority and a runbook that can be executed

A severity model must cover business loss, exposure radius, containment urgency and evidence confidence. **SEV1**: suspected unauthorized/duplicate financial effect, compromised E5/E6 credential, or ability to bypass independent authorization; stop the route and page incident command, security, finance and provider liaison. **SEV2**: one or more consequential operations `UNKNOWN`, provider status unavailable, or material loss of protected evidence with no known unauthorized effect; contain the relevant workflow and assign reconciliation ownership. **SEV3**: bounded advisory slowdown or telemetry delay with independently verified financial controls intact; restore availability within an approved error-budget policy. Missing evidence can increase severity even before harm is proved. Promotion/de-escalation is an auditable human decision, not a model classification.

**Runbook 30-A — Contain and reconcile CASE-204 without replay**

1. **Detect and declare.** Record first signal, clock quality, trace/case correlation and severity; page a named incident commander and financial decision owner. Never interpret missing evidence as a negative payment result.
2. **Isolate.** Incident command disables or quarantines affected consequential requests at the *trusted* E5/E6 routing boundary; a model prompt or E2-only flag is insufficient. Preserve unaffected read-only investigation where policy permits. Do not revoke the only reconciliation identity without arranging an authorized replacement.
3. **Preserve.** Freeze/restrict E7 operation history and relevant E2 lease records, E5 denial/grant-decision metadata, E8 provider receipts, deployment/version evidence and protected E9 event exports. Use approved retention and chain-of-custody controls. Do not copy credentials into tickets or logs.
4. **Reconcile.** A separately scoped, authorized recovery operator queries the **existing** RF-1042 through C08, validates provider provenance and immutable operation attributes, records discrepancies and consults finance on ambiguous settlement. On outage, conflicting proof or `NOT_FOUND`, keep `UNKNOWN` and an owner/deadline. Never call C07 again merely to clear a queue.
5. **Restore.** E5 owner checks, credential custody, E7 history availability, E8 inquiry health and critical telemetry must meet the incident's explicit acceptance criteria. An authorized finance/business approver accepts the disposition; incident command controls route restoration. Any compensating payment is a *new*, separately authorized business process, not a hidden retry of RF-1042.
6. **Review.** Within a defined post-incident window, produce a blameless causal account with timestamps, decisions, gaps, customer exposure, risk-adjusted remediation owners and proof that action items were tested. Link the report to Chapter 31's release-evidence package.

For **stale E2 ownership**, stop before E5: reject local stale mutations, verify current epoch externally and do not trust Build 5's local test as E5 fencing. For **credential compromise**, security revokes and rotates real workload/provider credentials and validates the protected E5 principal; unavailability of a key verifier is not a waiver of authorization. For **audit/telemetry outage**, declare reduced observability, protect existing E7/E8 sources and activate independent evidence capture or fail-closed behavior as policy requires. For **E5 denial**, investigate the request and principal; never route through an alternative adapter. For **E8 outage**, status-only inquiry can be retried under an approved read budget, but consequential replay is prohibited.

![](assets/shared-figures/rendered/F30-03.png)

*Figure 30.3 — Deterministic incident disposition gates. Each branch has an accountable owner; unresolved evidence loops to inquiry and escalation, never to effectful resend.*

## 30.6 Execute a non-effectful incident drill

The accompanying `examples/refund-reference-system/operations/` fixture **reads existing Build 4 E7 and Build 5 E2 SQLite snapshots**, accepts explicitly synthetic E8 observations and ordered/redacted signal envelopes, and produces a repeatable incident *recommendation*. It deliberately has **no** E5 payment client, C07 adapter, E7 mutation function, credential issuer or provider network endpoint. The tests build their inputs using actual Build 4/5 modules, including a lost-acknowledgment case, then assert the observer (`examples/refund-reference-system/operations/incident.py`) leaves both databases and the simulated provider row count unchanged. A report of `CONFIRMED` is a simulator classification, not authority to settle a business case. No Build 6 is introduced.

The fixture rejects malformed and duplicate event identities; derives order from a trusted monotonic fixture sequence rather than arrival order; flags missing telemetry, stale ownership, untrusted E8 proof, verifier failure, and contradictory observations; and records a disposition with a named next-action role. An event gap must remain visible even when current provider observation appears favorable. Logs use a strict non-secret field allowlist, not post-hoc removal of arbitrary payloads. Run the operations suite and compare its falsifiers with Chapter 28 recovery and Chapter 29 actual E5 denial tests. **Passing the observer tests does not prove a protected audit stream, real token revocation, true process isolation, or a live provider response.**

**Table 30.3 — Local evidence and production gap**

| Executed fixture evidence | Narrow claim | Missing production proof |
|---|---|---|
| Build 4/5 lost-ack simulation + observer read-only database comparison | Incident classification cannot initiate an additional local effect | External provider effects, E5 endpoint policy and production reconciliation credentials |
| Out-of-order, duplicate, gap and redaction tests | Synthetic event timeline is deterministic, and allowlisted output excludes injected secrets | Protected clock, collector delivery and enterprise audit custody |
| Revoked-token/verifier-down signal injection | Operational recommendation is to contain and escalate, not to authorize | Actual identity-provider (IdP) revocation, key rotation and network/access isolation |
| E2 epoch mismatch with E7 UNKNOWN | Stale coordination is identified for escalation without replay | Independently enforced current-owner epoch at E5 |

## 30.7 Six perspectives and operational acceptance

**Implementing engineer:** inspect the read-only Structured Query Language (SQL) statements and allowlisted output in `operations/incident.py`, then run `operations/test_incident.py` to verify no new `provider_refunds` (Build 4 `adapter.py`) or `operation_events` (Build 4 `ledger.py`) row is introduced by observation. Resolve these paths relative to `examples/refund-reference-system/`. **Enterprise architect:** draw the real deployment, credential and shared-dependency map; show which E5 and E9 barriers survive a host or provider outage. **Advanced student:** explain why a reversed telemetry arrival order changes no durable truth, and why `NOT_FOUND` cannot become `FAILED`. **Security/assurance reviewer:** challenge an attacker-controlled event payload and valid E1 token, and demand independent E5 and credential-custody evidence. **Site-reliability engineering (SRE) / operator:** rehearse the timed sequence from detection through quarantine, authoritative read and owner handoff, including missing collector and partition scenarios. **Business owner:** decide how much customer delay is tolerable without accepting a possible double $500 payment, and name who is accountable for unresolved cases.

Release requires evidence for the target operating policy, not just code coverage: exercised failure injections, documented authority and escalation matrix, monitored service-level objective (SLO) denominators, operator training and on-call staffing, independent credential and audit protections, provider-specific C08 evidence, and tested E5 epoch controls. Chapters 28–30 supply local experiments and bounded design claims. **Chapter 31** evaluates their falsifiers, reproducibility and acceptance evidence; it must not inherit unsupported production guarantees.

**Companion implementation and evidence.** From repository root, start at `examples/refund-reference-system/operations/README.md`; run `python3 -m unittest discover -s examples/refund-reference-system/operations -p 'test_*.py' -v`. Inspect `operations/incident.py` for read-only classification, `operations/test_incident.py` for non-mutation and adversarial signal tests, `build4/ledger.py` for local E7 history, and `build5/coordinator.py` for local E2 epochs. Compare `reliability/` (Chapter 28) and `security/` (Chapter 29). These fixtures do **not** establish production credential isolation, protected audit, E5 epoch enforcement or external provider settlement.

## 30.8 Chapter exercises

1. Given 1,000 eligible refund investigations, 8 advisory timeouts and one unverified duplicate provider effect, calculate the advisory availability indicator and explain why the safety release gate still fails. Define denominator exclusions and missing-event treatment.
2. Create a deployment dependency graph showing E2, E5, E7, E8 and E9 sharing a single identity provider. Propose two fault-containment changes and justify their expense using a stated refund volume and incident cost.
3. For a lost RF-1042 acknowledgment followed by E8 `NOT_FOUND`, write the runbook's allowed next actions, evidence record, ownership and forbidden steps. Explain what extra provider contract would be needed to distinguish absence from delayed status.
4. Inject out-of-order events, a missing sequence and a false `CONFIRMED` claim into the Chapter 30 observer. Run the tests; defend why the event stream is neither trusted authorization nor final settlement evidence.
5. Conduct a tabletop exercise with separate incident commander, security lead, E5 operator and finance owner. Produce a recovery acceptance checklist and postmortem action that Chapter 31 could falsify.
