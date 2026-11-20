# Chapter 34 — Economics, Risk, and Lifecycle Decisions

Part VI: Governance, Economics, and Operations

> **Engineering proposition:** The economical agentic system is not the one with the lowest inference bill or the most autonomous agents. It is the least costly *defensible* configuration that produces acceptable outcomes under bounded authority, recoverable operations and accountable governance.

## Learning objectives

After this chapter, the reader should be able to calculate the cost per **acceptable completed workflow**; compare deterministic, advisory and bounded-agent architectures against one common case mix; model risk, human labor and operational uncertainty without implying statistical guarantees; establish evidence-based adoption, scaling and retirement gates; and identify which economic measurements exist in the companion code versus those requiring a real operating environment.

## 34.1 The unit of value is a defensible business outcome

An agent can generate an inexpensive recommendation that is wrong, unactionable, unauthorized or impossible to audit. Counting that as a completed workflow systematically rewards the wrong architecture. For **CASE-204**, a customer complaint may justify a **$500 refund**, but the financial operation **RF-1042** can be created only under independent trusted authorization. A completion is acceptable only when the enterprise can demonstrate bounded admission, an appropriately justified decision, a lawful financial effect *or a documented denial*, durable evidence and a reconcilable outcome. An unresolved `UNKNOWN` result is neither a successful refund nor a failed refund merely because the worker stopped running.

**Design A** is a deterministic case process; **Design B** combines bounded artificial-intelligence (AI) advice with independent financial authorization and is the conditional initial production candidate; **Design C** optionally adds specialist investigative agents while preserving that same trusted financial boundary. These are competing designs, not maturity stages. Builds 0–5 are six separate educational Python implementation checkpoints; they are not versions of Designs A/B/C or an integrated production service. A more elaborate design must earn its place on measured value, safety, and operability.

The logical architecture separates admission and identity (E1), durable coordination and ownership (E2), untrusted advisory reasoning (E3), bounded context and provenance (E4), independent trusted execution (E5), controlled provider integration (E6), durable operational state (E7), external provider/business truth (E8), and governance/assurance (E9). Chapter 8 defines contracts C01–C09. In particular, a C04 advisory proposal is not a C05 financial decision; E5 establishes C06 durable intent before C07 dispatch, and status-only C08 reconciliation consults E8 without blind replay. C09 evidence supports independent assurance, not permission to spend. These are logical responsibilities; deployment isolation is not established by the illustrative code.

## 34.2 Calculate complete lifecycle cost, not token cost

For a specified cohort, period, policy regime and acceptable-outcome definition, define:

**Cost per acceptable completed workflow = total period lifecycle cost ÷ number of acceptable completed workflows.**

The numerator includes engineering, integration, model/API or small-language-model (SLM) hosting, evaluation and regression, data curation, privacy and security, human approval, supervision, monitoring, incident response, reconciliation, provider charges, change management, platform capacity, compliance evidence, and retirement or migration. Include the cost of *denied* or escalated work in the numerator: those outcomes consume resources even when no refund is issued. The denominator excludes duplicate effects, unsupported auto-approvals, irreconcilable outcomes and abandoned investigations; legitimate denials count only if the declared service definition treats appropriately resolved denials as acceptable outcomes. **Do not manipulate the denominator by dropping expensive failed cases.** Report acceptance rate, case mix, time-to-resolution and unresolved backlog alongside unit cost.

**Table 34.1 — Lifecycle cost register for a governed refund workflow**

| Cost or exposure | Owner and measurement | Why token-only accounting misses it |
|---|---|---|
| Advisory inference and context | AI platform: model calls, input/output, context refresh, retries | Repeated or stale reasoning may be cheap but unhelpful |
| Independent E5/E6 control | Finance/security: grant issuance, key protection, adapter and settlement | The cost exists even with deterministic Design A |
| Human review and exception handling | Finance/operations: staffed minutes, escalations, rework | Human judgment is a scarce capacity, not a free fallback |
| E2/E7/E8 recovery | SRE/finance: owner fencing, storage, read-only inquiry and backlog | Lost acknowledgments require evidence, not another dispatch |
| Assurance, release and governance | QA/security/release owners: red-team, change reviews and attestation | Local green tests do not prove real production controls |
| Residual loss and capital exposure | Risk/business: bounded financial loss, incident and remediation | Expected loss is a scenario estimate, not a guaranteed bill |
| Sunset and portability | Platform/domain: migration, data retention and provider exit | Dependency lock-in turns a cheap pilot into an expensive estate |

Figure 34.1 separates a quoted model price from the larger decision cost. Costs are recorded by cohort and workload; shared-platform allocations must be stated rather than silently assigned to whichever design the committee prefers.

![](assets/shared-figures/rendered/F34-01.png)

*Figure 34.1 — Unit-cost architecture. Model inference is only one input; independent authorization, assurance, human review, recovery and exit expense contribute to cost per acceptable completed case.*

## 34.3 A transparent example for Designs A, B and C

**Table 34.2 — Illustrative monthly scenario; hypothetical assumptions, not observed results**

| Measure | Design A: deterministic | Design B: bounded advice | Design C: agent investigation |
|---|---:|---:|---:|
| Eligible incoming cases | 10,000 | 10,000 | 10,000 |
| Acceptable completed outcomes | 8,400 | 9,000 | 9,150 |
| Total lifecycle operating cost | $84,000 | $99,000 | $123,525 |
| Cost per acceptable completion | $10.00 | $11.00 | $13.50 |
| Incremental acceptable outcomes vs A | — | 600 | 750 |
| Incremental cost vs A | — | $15,000 | $39,525 |

Every number in Table 34.2 is an *assumption invented for decision practice*, not a measurement of the Python examples, a claim about actual AI effectiveness, or evidence that a refund was correctly authorized. The design teams must use the **same incoming population**, policy, adjudication standard and observation window. Here Design B buys 600 additional acceptable outcomes for $15,000: **$25 incremental cost per additional acceptable outcome**, relative to A. Design C buys 150 more than B for $24,525: **$163.50 per additional acceptable outcome**. The difference can be worthwhile for certain high-value exceptions, but is not justified by an assertion that “more agents are better.” If acceptable outcomes carry an attributable, conservatively estimated $40 of incremental business value apiece, B's 600 additional completions yield $24,000 of hypothetical benefit against $15,000 of cost; that comparison still excludes unmodeled risk and capital expenditure. C's additional 150 would yield only $6,000 against $24,525 under the same assumption.

The $500 CASE-204 refund amount is a **potential financial effect**, not a $500 benefit attributed to the agent or a per-workflow model cost. A refund is an authorized business obligation, not revenue created by automation. Value might instead arise from timely resolution, prevented rework, reduced handling effort, improved retention *if measured*, and documented risk avoidance. Never count a successful financial transfer as incremental profit merely because an AI system proposed it.

A decision-grade study requires cohort stratification: simple cases, missing-evidence cases, fraud indicators, mixed-tenancy access and interrupted external operations have different costs and failure hazards. Report distributions and confidence bounds when real observations permit; do not infer statistical confidence from the illustrative table. Compare performance against the strongest adequate deterministic/hybrid baseline, not against a deliberately weak manual process.

## 34.4 Quantify risk without pricing away an unenforced boundary

A simple model may represent expected loss as the sum of scenario likelihood times scenario impact, with confidence and evidence quality recorded separately. It is useful for prioritizing testing and capacity, **not permission to average away a control failure**. If an investigative agent with a valid E1 token can bypass E5 authorization and invoke E6 payment credentials, the release fails an architectural gate regardless of a favorable modeled expected loss. An observed duplicate payment, an unbounded cross-tenant read, or inability to stop effectful work independently is a no-go condition, not a tradeable discount.

**Table 34.3 — Risk scenarios and decision treatment**

| Scenario and possible impact | Evidence/containment obligation | Economic treatment |
|---|---|---|
| Compromised investigator attempts unauthorized $500 | Build 3 and security fixture deny at independent E5; prove production issuer/keys separately | Hard gate; scenario loss is not an authorization substitute |
| Lost E8 acknowledgment leaves RF-1042 `UNKNOWN` | E7 durable intent and original-operation C08 read-only inquiry; never blind retry | Price backlog labor, inquiry and exposure; unresolved is not completion |
| Stale owner races recovery | Build 5 local E2 fencing; current-owner E5 epoch control remains unimplemented | Hard gate for distributed effectful ownership; price real enforcement |
| Model/context drift increases inappropriate proposals | Track versioned cohorts, adjudication, denials and source freshness | Sensitivity case and retraining/evaluation budget |
| Human approval queue exceeds staffing | Time-in-queue, error rate, escalation owner and staffed capacity | Explicit headcount, delay and alternative service design |
| Release or provider change disables safe recovery | Chapter 33 readiness and Chapter 30/32 runbooks; original effects preserved | Include downtime, investigation and migration cost |

Finance should compare a *risk register* with guardrails, scenario ranges and accountable acceptance—not a single artificially precise score. NIST AI Risk Management Framework 1.0 provides a general risk-governance framing (NIST, 2023); it does not attest to these ETIS calculations or certify a financial payment path. Enterprise risk appetite, legal duties and finance authority are set by the organization and applicable law, not generated by an agent.

## 34.5 Sensitivity, capacity and the boundary of autonomy

Before expanding Design C, vary at least five uncertain assumptions: incoming case complexity, fraction requiring human escalation, false-approval or fraud cost, failure/reconciliation frequency, and agent/model infrastructure price. Add a sixth—availability of independent E5/E6 enforcement—to represent a binary release prerequisite rather than a continuously priced parameter. For each case recalculate acceptable throughput, human queue utilization, worst-case backlog age, unit economics and residual open control gaps.

A queue can defeat a nominally efficient model. Suppose a pilot receives 200 reviews per workday and each review requires six human minutes. That consumes **20 reviewer-hours per day** before breaks, vacations, disputes or second-person approvals. If staffed capacity is 16 effective reviewer-hours, the backlog grows by **four hours of work per day** even when every agent response arrives instantly. A governance design that shifts hidden labor onto finance is not economically efficient. Where risk requires separation of duties, the cost of an independent reviewer is part of the design, not a reason to remove the control.

The agent's value also depends on the *shape* of failures. Model-call errors can be retried safely within bounded advisory scope; disputed context may require provenance review; a possible provider-side effect cannot be treated as a retryable inference. Design the workload cost model around these distinct paths. Monitoring must count E5 denials, E7 `UNKNOWN`, C08 inquiries, C09 evidence gaps, queue age, false positives, adverse selection, and staffed operator interventions. No local companion fixture measures these as population statistics.

![](assets/shared-figures/rendered/F34-02.png)

*Figure 34.2 — Decision sensitivity. Increased agent autonomy is not automatically justified by higher throughput; staffing, control evidence, worst-case loss and recovery load constrain the admissible region.*

## 34.6 The portfolio decision: pilot, scale, restrict, replace or retire

Lifecycle governance is a repeated decision with explicit observation windows, owners and reversible scope. A **pilot** limits effectful exposure while measuring value and failure modes. **Scale** requires cohort-comparable evidence, stable E5/E6 enforcement, independent audit, staffed recovery and demonstrated economic benefit. **Restrict** if complex cases generate unsafe decisions, human-review saturation or unverifiable outcomes. **Replace** an AI component with a smaller model, deterministic rule or manual workflow when it delivers equal defensible outcomes at lower total cost. **Retire** when risk or dependency cost outweighs value, including the cost of preserving historical records and servicing in-flight uncertain outcomes. Retirement is not deletion of E7 history or cancellation of E8 financial truth.

**Table 34.4 — Stage decision and accountable evidence**

| Decision | Minimum evidence | Who may refuse |
|---|---|---|
| Pilot Design B | Independently denied unauthorized C04; evaluated common cases; bounded cohort and stop route | Finance, security, release authority |
| Scale a proven cohort | Reproducible outcomes, staffed review, protected C09 and observed provider recovery | Operations, finance, assurance |
| Admit Design C for exceptions | Incremental value beyond B, E2 fencing, bounded agent tool paths and adequate oversight | Architecture, security, business owner |
| Restrict or pause | E5 anomalies, missing telemetry, unresolved effects, policy drift or rising backlog | Incident command and designated control owners |
| Replace or retire | Comparable economics, migration plan, retention, credential revocation and open-operation disposition | Risk, finance, data owner and operations |

Figure 34.3 is a decision diagram, not an implemented auto-scaling policy. In particular, **no score may authorize release when required control evidence is missing**. Chapter 32 allocates decision rights; Chapter 33 requires a controlled release candidate and safe halt; Chapter 31 states what the verification evidence actually covers. Runbooks 30-A, 32-A and 33-A describe illustrative operational procedures; they are not executable automation supplied by the companion implementation.

![](assets/shared-figures/rendered/F34-03.png)

*Figure 34.3 — Lifecycle gate. First establish enforceable authority and reconcilable evidence; then evaluate incremental value, capacity and reversible exposure. Missing hard-gate evidence routes to restriction, not a favorable ROI score.*

## 34.7 Companion evidence and the unimplemented economics layer

Start at `examples/refund-reference-system/README.md` and `examples/refund-reference-system/IMPLEMENTATION_EVIDENCE_MAP.md`. The source/module diagrams and runnable commands are documented in `build0/README.md` through `build5/README.md`. Relative to that companion root: `build3/service.py` and `build3/test_gate.py` show the simulated financial denial boundary; `security/test_adversarial_cases.py` challenges a compromised investigator; `build4/ledger.py`, `build4/test_provider.py` and `reliability/test_recovery_cases.py` show local original-operation records and read-only inquiry; `build5/test_coordination.py` challenges local ownership; `operations/incident.py` and `operations/test_incident.py` demonstrate read-only incident analysis; `assurance/collect.py` and `assurance/test_collect.py` collect local bounded evidence. The `security/README.md`, `reliability/README.md`, `operations/README.md` and `assurance/README.md` describe those fixtures and limitations.

**There is no executable cost model, production invoice collector, benefits attribution, staff-capacity service, loss estimator, live release gate or integrated ROI dashboard in Builds 0–5.** Tables 34.1–34.4 and Figures 34.1–34.3 are *proposed management/engineering decision artifacts*, not Python fields, output files, or business results measured by the companion tests. To implement them in production, establish a governed case denominator, actual invoices and labor allocation, independent adjudication of acceptable outcomes, versioned risk/incident histories, human owner signoff, and privacy-preserving evidence custody. Do not create Build 6 merely to imply these guarantees.

A passing local regression cannot establish production isolation, provider settlement truth, actual economic return, or policy compliance. The key outstanding gap remains independent current-owner-epoch enforcement in E5 and real approval issuer/revocation, provider and audit controls; cost arithmetic cannot retire those obligations.

## 34.8 Professional challenge and Part VI synthesis

**Exercise 34.1 — Adversarial business case.** Recalculate Table 34.2 when B's acceptable completions fall to 8,600, human review adds $18,000 per month, and the incident/reconciliation budget doubles. State the denominator, each changed cost assumption, the incremental cost per acceptable outcome and whether the pilot should expand. Explain what additional production evidence would overturn the decision.

**Exercise 34.2 — Unsafe ROI claim.** An executive cites a 50% reduction in model-call cost and asks to bypass the E5 approval step for high-confidence cases. Write the release denial and an alternative architecture preserving E5 while reducing review burden. Identify which actual Build 3 negative test anchors the argument and which control cannot be certified from the fixture.

**Exercise 34.3 — Graceful retirement.** Design C is withdrawn after a provider migration; RF-1042 is still `UNKNOWN`. Describe which admission, coordination, advisory, context, trusted execution, provider, state, business-truth and governance responsibilities must remain available, who owns C08 read-only reconciliation, which secrets and permissions are revoked, and why deleting the agent does not resolve the refund.

The implementing engineer defends cost and tests; the enterprise architect challenges authority boundaries; security verifies independent denial; site reliability engineering prices recovery; the business owner defends value and oversight. None gives agents financial authority.

**Part VI conclusion:** Governance determines who can say yes, no, stop and resume; release engineering determines which version may operate and under what exposure; lifecycle economics decides whether preserving that authority and evidence is worth the result. **AI proposes; independently controlled systems enforce; people remain accountable.** Part VII consolidates the supporting contracts and evidence obligations.
