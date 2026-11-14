# Chapter 5 — Business Cases, Value, and Lifecycle Economics

*Part I: Foundations, Evolution, and Business Context*

> **Engineering proposition:** An agentic design earns its place by improving a measured business outcome relative to a credible simpler alternative, after fully loaded costs, risks, and operating obligations are counted. Faster model output is not automatically greater enterprise value.

## Learning objectives

After this chapter, readers should be able to: (1) frame an agentic business case around a measurable outcome and counterfactual; (2) compare deterministic, advisory, and bounded-agent designs without changing their authorization boundary; (3) calculate expected net value and cost per *correctly resolved* case; (4) account for review, rework, exception, recovery, and change costs; (5) design a pilot with decision thresholds and evidence; and (6) determine when to expand, contain, or stop delegation.

## 5.1 Start with the outcome, not the technology

Chapters 1–4 established the system obligation, historical inheritance, decision rights, and the difference between a model and an agent. Economic judgment is the next gate. The enterprise should first state what is wrong with the existing process: delayed resolution, inconsistent evidence gathering, rework, customer dissatisfaction, or cost. The proposal is then a hypothesis: bounded interpretation or investigation might improve one of those outcomes **without weakening the controls that make the result legitimate**.

Use the running case without changing its facts. A customer reports that a replacement did not arrive and requests a **$500 refund**. The business verifies identity and entitlement, authorizes any payment, records durable intent, performs the payment through a controlled adapter, and reconciles uncertain outcomes. Chapter 3's **Design B—advisory AI with independent review—remains the initial production candidate**. Chapter 4's **Design C—bounded, read-only investigative agent—remains an evaluated alternative**, not a quietly approved deployment. Both produce evidence or a proposal; neither may independently issue the refund.

The most defensible business claim is not “the agent completed 80% of cases.” It is “the system increased the share of cases correctly resolved within the service target, with no material increase in unauthorized payments, unresolved exceptions, or customer harm, at an acceptable total cost.” NIST AI RMF (2023, MAP 3) calls for examining expected benefits, costs, scope, and oversight against suitable benchmarks. This chapter translates that discipline into investment choices.

## 5.2 Choose the right comparison

An agent should not be compared only with manual work or a deliberately weak process. Establish three alternatives using the *same case mix, quality standard, and trusted refund authority boundary*:

| Design | Scope of automation | Principal economic question |
|---|---|---|
| **A. Deterministic baseline** | Structured checks and governed workflow | How much value already exists without a model? |
| **B. Advisory AI** | AI interprets evidence and proposes; independent review remains | Does interpretation save enough effort without adding excessive rework? |
| **C. Bounded investigator** | Agent selects approved read-only investigation steps; independent review and execution remain | Is flexible evidence gathering worth additional control, test, and support burden? |

Segment by difficulty before comparing: routine structured cases, ambiguous correspondence, missing or contradictory records, and suspected fraud or abuse. Automation that excels on easy cases but degrades on exceptions can make the average look better while moving cost and risk to the hardest cases. Case assignment must be representative or explicitly stratified; otherwise a pilot can reward favorable routing rather than better engineering.

![Figure 5.1 — Compare three designs against the same business outcome and control boundary.](assets/shared-figures/rendered/F05-01.png){#fig:f05-01 width=5.75in}

## 5.3 Define value that can be verified

Measure *business outcomes*, *quality guardrails*, and *operating burden* separately. Outcome measures include correct resolutions per period, end-to-end time to a confirmed state, repeat contacts, and customer escalation. Guardrails include unauthorized refund attempts, eligibility errors, incorrect denials, privacy breaches, complaint rates, and unresolved provider outcomes. Burden includes reviewer minutes, investigation steps, tool calls, model consumption, and incident-response work. A confident proposal or a provider request accepted for processing is not a confirmed refund.

The denominator matters. **Cost per model invocation** is useful for technical tuning, but the investment measure is **fully loaded cost per correctly resolved case**. A case deferred to an operator or left `UNKNOWN` still consumes cost; it cannot be discarded from the numerator or denominator to improve the metric. FinOps Foundation (2025; Unit Economics capability) links technical spending to business outcomes and distinguishes narrow variable-cost accounting from fully loaded economics.

Define benefits once to avoid double counting. For example, fewer reviewer minutes may lower cost or free capacity; do not claim both full payroll savings and full capacity value unless the business can demonstrably realize both. Faster responses are valuable only if they improve a measurable customer or operating outcome. Financial error reduction, better compliance evidence, and fewer repeat contacts may be additional benefits, provided they are measured and not counted again under generic “quality improvements.”

## 5.4 Model lifecycle cost and expected net value

For a common period and case mix, calculate the annualized or pilot-period difference:

**Incremental net value = validated incremental benefit − incremental lifecycle cost − expected loss from incremental risk.**

Lifecycle cost includes design, integration, evaluation, security review, privacy work, model and tool usage, hosting, observation, human review, exceptions, training, supplier changes, monitoring, incidents, recovery drills, and eventual replacement or retirement. Fixed implementation cost must be amortized over an explicitly stated horizon; any comparison across different horizons must use a consistent discount convention. Cost that shifts to another team has not disappeared.

Risk is not captured by a single model-error percentage. A refund may be incorrectly recommended, incorrectly denied, duplicated, disclosed to the wrong person, or placed into an unrecognized pending state. For expected-value planning, **probability × severity** can provide a first estimate of monetary exposure, but rare catastrophic or legally unacceptable outcomes require independent hard constraints; they are not made permissible by an attractive average return. Where probability is poorly established, use scenario ranges and a stop rule rather than invented precision.

![Figure 5.2 — The refund investment model includes both realized benefit and the full cost of safe operation.](assets/shared-figures/rendered/F05-02.png){#fig:f05-02 width=5.75in}

## 5.5 Worked example: the $500 refund, without changing authority

The following numbers are **illustrative assumptions, not observed performance or vendor pricing**. Assume 10,000 comparable cases per year. The A baseline costs $8.00 in fully loaded handling per case. B reduces routine handling but retains review; its estimated per-case cost is $5.90, including model calls and reviewer work. C's flexible investigation appears to reduce reviewer effort further, but costs $5.50 per case after orchestration, monitoring, escalation, and recovery. Assume annual incremental fixed costs versus A of $18,000 for B and $48,000 for C. For comparison, count only directly evidenced savings here; customer-experience gains remain unmonetized.

| Annual measure | A: rules | B: advisory | C: bounded investigator |
|---|---:|---:|---:|
| Cases in common denominator | 10,000 | 10,000 | 10,000 |
| Fully loaded variable cost / case | $8.00 | $5.90 | $5.50 |
| Annual variable cost | $80,000 | $59,000 | $55,000 |
| Incremental fixed cost / year | — | $18,000 | $48,000 |
| Total annual cost | **$80,000** | **$77,000** | **$103,000** |
| Savings / (additional cost) vs A | — | **$3,000** | **($23,000)** |

This does **not** prove B should ship. Its $3,000 modeled saving is narrow; an increase in incorrect denials, repeat contacts, or review effort could erase it. Nor does C's lower variable cost make it better: on these assumptions it costs $23,000 more annually. The corresponding break-even volumes, if per-case savings persist and risk remains acceptable, are approximately **8,572 cases** for B ($18,000 ÷ $2.10) and **19,200 cases** for C ($48,000 ÷ $2.50). At the assumed 10,000-case demand, B *could* justify a controlled trial; C does not yet justify production on financial grounds. These are scenario calculations, not forecasts.

Importantly, the **$500** is the *requested transaction amount*, not the per-case automation cost or a model-created financial benefit. Correctly paying a legitimately owed refund is not new revenue. A duplicate $500 payment is an exposure. An AI system that appears to save $2 in handling while increasing preventable duplicate refunds can destroy its business case. Under an ambiguous provider timeout, both B and C must preserve the durable operation identity and return `UNKNOWN` for independent reconciliation; neither may infer failure and retry with a new payment identity.

## 5.6 Treat review and exceptions as design variables

Human review is neither free nor inherently reliable. Measure reviewer work at each decision boundary: what evidence must be inspected, what is checked mechanically, how long it takes, and whether reviewers can detect a persuasive but unsupported recommendation. A workflow that produces fluent summaries but forces reviewers to reconstruct the complete case may add labor. Conversely, structured evidence with source links and clearly stated uncertainty may accelerate competent review while preserving accountability.

The exception path is the economic stress test. Missing shipment evidence, disputed customer identity, revoked access, policy-version conflicts, provider timeouts, and appeals all require explicit routing. These cases consume capacity and may require senior judgment. Escalation is a valid outcome, not a failure to be hidden from the dashboard. Measure exception frequency, time in queue, reopen rate, and unresolved exposure alongside successful automated cases.

A small, high-performing model can be preferable to a flexible agent when the case fields are stable. A deterministic rule can be preferable to both. The choice should follow evidence, not a requirement to maximize autonomy. The cost of testing additional tool paths and combinations rises with permitted freedom even where the invocation price falls.

**A decision-grade business review is cross-functional.** The business owner tests whether shorter handling time improves acceptable outcomes; engineering tests reproducibility and maintainability; security/assurance estimates control and review costs; operations estimates incidents and unresolved work. Record disagreements as measurable assumptions in the pilot, not as a vote for a more autonomous model.

## 5.7 Run a decision-grade pilot

Before production, agree an evaluation charter with the process owner, finance, operations, security, privacy, and representatives of customer review. State the population and exclusion rules, counterfactual baseline, sample approach, observation period, metrics, and decision authority. Use historical replay and prospective shadow mode before any live consequential effect. Cases with known outcomes support initial accuracy testing; held-out and adversarial cases probe the exceptions. Observe reviewer behavior, not just model output.

A production pilot should use the *same independently controlled refund execution boundary* as the baseline. Compare A and B first. Treat C as a separate conditional experiment with its own hypothesis: that dynamically selected read-only investigation steps materially improve correct resolution or reviewer effort beyond B. Log tool choice, provenance, budget consumption, denial, and escalation. Define unacceptable outcomes in advance, including unauthorized financial action, cross-customer disclosure, duplicate payment, and inability to reconcile an unknown payment state. Any such breach triggers containment and review, regardless of average savings.

A useful acceptance record includes baseline characteristics; policy-version and case-mix controls; correctness, fairness, and privacy measures; fully loaded unit cost; confidence ranges or uncertainty bounds; incident and exception analysis; and decision rationale. A deployment gate should require evidence of both **business advantage** and **enforced authority**. The two are independent; economic attractiveness cannot substitute for authorization tests.

## 5.8 Change, scale, and exit economics

Economics change after launch. Case mix drifts; policy changes; vendor prices and service limits shift; model quality may change; new tools create new pathways; human reviewers become less practiced on rare failures. Each change can alter both the cost numerator and the correct-resolution denominator. Budget not only for initial integration but for evaluations on every material model, prompt, policy, data-source, or tool-contract change. Define a rollback to B or A if cost, guardrails, or recovery performance deteriorate. Use canary deployment and explicit ownership rather than silently extending agent permissions.

Lifecycle analysis also covers vendor concentration, data portability, provider unavailability, contract renewal, and retirement. Design for a replaceable investigator and a durable case record so that a new model need not become the owner of authorization or payment truth. Report recurring unit economics to a named business owner, not merely token cost to a platform team.

The same method generalizes beyond refunds, but not its risk model. A read-only research assistant has a different consequence profile. An IT change agent can cause outages; procurement approval can create commitments; clinical workflows have far greater stakes. The **comparison discipline** transfers, while authorization, loss scenarios, and acceptable evidence must be re-derived for each domain.

## 5.9 The gate to the next chapter

The business case is an explicit decision: keep A, pilot B, investigate C, or stop. It records what is known, what is assumed, and what additional evidence would reverse the choice. Chapter 6 will examine uncertainty, authority, and trust directly; Chapter 7 will translate their obligations into measurable requirements. We have not changed the refund transaction, authorized an agent to pay, or treated an uncertain provider response as a confirmed outcome. **Economic value must survive trustworthy execution, not bypass it.**

## Chapter 5 — Engineering practice

1. **Construct a comparison.** Define a fair A/B/C evaluation for the $500 case with a common denominator and segmented case mix. Identify one routing bias that would invalidate the result.
2. **Recalculate.** Confirm the table and break-even volumes. Add a plausible review-cost increase and decide whether B still has positive net value.
3. **Stress-test.** Model a scenario with duplicate-payment exposure and `UNKNOWN` outcomes. Identify a hard stop that cannot be traded away for faster handling.
4. **Design a pilot.** Specify three outcome measures, three safety guardrails, two exception metrics, and the minimum evidence needed to promote B to production.
5. **Defend a decision.** A model vendor halves token price but the new version increases contradictory evidence retrieval. Explain whether that changes the investment recommendation.
6. **Transfer.** Apply the method to an IT change request; identify which assumptions and control limits must change.

**Review standard:** A sound answer makes costs and denominators auditable, distinguishes assumptions from observations, retains independent financial authorization, and can defend a no-go decision when evidence is insufficient.

## Sources and further reading

NIST AI RMF 1.0 (2023), especially MAP 3, provides an established risk-and-benefit framing. The FinOps Foundation Framework (2025) and its Unit Economics guidance connect technology cost to business outcomes. Bass, Clements, and Kazman (2021) address quality-attribute tradeoffs; Kleppmann (2017) and Gray and Reuter (1992) inform recovery and transaction correctness. The scenario figures, assumed prices, and break-even calculations in this chapter are original ETIS illustrative examples, not findings attributed to those sources.
