# Chapter 17 — Choosing Deterministic, Agentic, and Hybrid Designs

*Part III: Patterns and Architectural Decisions*

> **Engineering proposition:** Choose the least complex decision mechanism that meets the business outcome **and** can demonstrate its authority, failure, recovery, and economic obligations. Flexibility is a capability to justify, not an architecture milestone.

## Learning objectives

After this chapter, readers should be able to (1) distinguish task selection from consequential authority; (2) choose among deterministic, advisory, bounded-agentic, and hybrid arrangements; (3) develop a falsifiable selection scorecard, including lifecycle economics; (4) map the chosen approach onto Figure 8.1 without changing the nine domain contracts; (5) specify negative-path and provider-uncertainty acceptance evidence; and (6) record conditional selection, rejection, and reversal criteria in an architecture decision record.

## 17.1 The decision changes; the architectural obligations do not

Chapter 16 completed the transition from the **target-state logical reference architecture** to deployable protection boundaries. Figure 8.1 shows four responsibility layers and the cross-cutting E7 durable state and E9 assurance domains. Chapter 17 begins Part III by examining the choices *within* that architecture. It does not invent a new reference model or relocate authority. The fundamental question is not whether an enterprise can run an agent, but where a component that selects its next steps produces measurable value compared with an adequate simpler design.

The continuing case is `CASE-204`: a customer requests a **$500 refund** after a replacement does not arrive. **Design A** follows deterministic rules, **Design B** uses advisory AI with independent review, and **Design C** permits a bounded investigator to choose among approved read-only investigation steps. These are **alternatives**, not a cumulative implementation sequence. Under the assumptions introduced in Chapter 3, Design B is the *conditional initial production candidate*, pending comparative measurement and assurance. Design C is a separate pilot candidate, not a promotion to payment authority. `RF-1042` identifies the consequential refund operation **only after independent authorization**; it is not a tool permission or credential.

The distinction between selecting an investigation action and authorizing a financial effect is part of the ETIS architectural synthesis. Established human–automation research provides ways to allocate different functions to machines and people (Parasuraman, Sheridan, and Wickens, 2000); software architecture makes quality-attribute tradeoffs explicit (Bass, Clements, and Kazman, 2021). Neither source prescribes our particular E-domain arrangement.

## 17.2 Separate mechanisms from patterns

A **decision mechanism** selects an output or next step: explicit rules, search/planning, a small model, a large language model, or combinations. An **architecture pattern** assigns responsibilities among mechanisms, controllers, people, state stores and interfaces. A **deployment choice** determines where these responsibilities run and what isolation they have. The three choices interact, but they are not synonyms. A rules-based goal-directed agent is possible; a language model embedded in a fixed workflow need not control a multi-step task. Chapter 4 established that distinction using classical agent definitions (Russell and Norvig, 2020).

A deterministic workflow may still experience outages, faulty rules and partial external effects. A language model may provide useful extraction inside deterministic orchestration without controlling tool order. A bounded agent can choose which permitted evidence to retrieve but may not expand its delegation envelope. A **hybrid** arrangement deliberately places variable interpretation beside deterministic authority, state and recovery controls. Calling a design hybrid does not establish which component is trusted: the interfaces and enforcement tests must do that.

| Pattern | Selection responsibility | New evidence burden | Appropriate initial use |
|---|---|---|---|
| **Deterministic (A)** | Rules choose known steps and remedy | Rule coverage, policy versions, negative tests | Structured, stable, well-specified cases |
| **Advisory AI (B)** | Model interprets or recommends; reviewed workflow decides | Fidelity, provenance, human review quality, latency and cost | Ambiguous language with contained action selection |
| **Bounded agent (C)** | Agent chooses permitted investigation reads; trusted controller executes them | Trajectory limits, scope denials, stop/replay tests, cost variability | Evidence gathering where adaptive sequencing has measurable value |
| **Hybrid composition** | Explicit allocation of fixed and variable steps | End-to-end contracts and combined failure testing | Different tasks warrant different mechanisms |

A/B/C are **case-level comparison alternatives**. The fourth row describes a reusable composition principle, not a fourth refund candidate. It must not silently turn Designs A, B and C into sequential phases. Vendor guides distinguish predefined workflows from model-selected actions (Anthropic Engineering, 2024; OpenAI, 2026), but their examples are not independent evidence that a particular financial workflow is safe.

## 17.3 Apply a decision gate before introducing reasoning

Begin with the business obligation and an empirical baseline. Is the decision a repeatable function of structured, current facts? Can the legitimate outputs and exceptions be enumerated? Does its result require subjective interpretation of language, incomplete documents or competing explanations? Are failures cheaply reversible, or can a mistaken action transfer money or disclose customer information? Is the proposed output independently checkable? What is the cost of exceptions and of continued operation—not merely inference cost?

Figure 17.1 is a *decision aid*, not an automated classifier. Its default is to preserve an existing deterministic mechanism when that mechanism suffices. Ambiguity may justify advisory interpretation, but it does not automatically justify autonomous action selection. Only a measured advantage from choosing different permitted steps should move a candidate into a bounded-agent pilot. At each branch a consequence gate separately asks whether the selected output can directly affect enterprise state. If so, independent E5 approval and E6 execution remain mandatory.

![Figure 17.1 — Choose the simplest sufficient decision pattern; consequence authorization is an independent gate, not an autonomy level.](assets/shared-figures/rendered/F17-01.png){#fig:f17-01 width=5.75in}

For `CASE-204`, the payment amount and refundable balance must come from E8 authoritative systems through governed interfaces; they are not inferred from complaint prose. Evaluating a clearly stated refund threshold is generally deterministic. Summarizing contradictory delivery correspondence may justify advisory AI. Deciding which of several permitted shipment records to inspect next may justify a bounded agent only if its observed benefit exceeds the added uncertainty, latency, tooling and assurance cost. None of these grants a payment key, an E6 provider route or authority to change the refundable balance.

## 17.4 Compare benefits with the *whole-workflow* cost

Chapter 5 established cost per acceptable completed workflow as the primary economic lens. Reuse that metric instead of optimizing model-call cost. The numerator includes inference, retrieval, infrastructure, human review, failed and escalated cases, monitoring, security, regressions, incident response and reconciliation. The denominator counts only cases meeting defined business correctness and assurance criteria. An inexpensive hallucinated recommendation that triggers expensive review is not necessarily productive. FinOps unit economics guidance supports outcome-oriented measurement; the specific acceptance threshold remains a business decision (FinOps Foundation, 2025).

Set up a controlled comparison using the same case distribution for A, B and C. Record eligibility accuracy against authoritative facts, evidence fidelity, customer outcome, completed-cycle latency (including tails), number of human touches, unsafe-proposal rejection, tool calls, cost and escalation. Stratify routine cases, ambiguous correspondence, stale evidence, wrong-tenant records and provider failures. Do not choose from a single mean score: a design that improves routine throughput but fails a cross-tenant boundary is not acceptable.

**Illustrative arithmetic, not an industry estimate:** Suppose 1,000 ambiguous cases are sampled. B saves three minutes of investigation on 600 cases (1,800 minutes), but requires one minute of additional review on all 1,000 (1,000 minutes). That leaves 800 minutes of gross labor benefit before inference, evaluation, exception and recovery costs. If C saves an additional 250 minutes but introduces 400 minutes of trace review and failed-tool support, C loses on that measure. The point is not these numbers; it is the **counterfactual**, the complete cost boundary and the willingness to reject novelty when it fails the comparison.

## 17.5 Map the choice back onto Figure 8.1

Figure 17.2 shows that the alternatives change only the internal allocation of E2/E3/E4 investigation. The authoritative work owner E2 remains accountable for orchestration; E1 continues to bind principal and tenant; E4 enforces scoped provenance and freshness; E3 outputs remain typed **advisory** data. E5 revalidates authorization, holds the effective consequential gate and protects credential custody. E6 mediates provider-specific dispatch. E7 owns durable intent and unresolved state, E8 owns authoritative business facts, and E9 collects evidence and supplies operator controls. The vertical boundary is an engineering contract, not the visual suggestion that every domain must be a separate microservice.

![Figure 17.2 — Designs A, B and C vary the investigation responsibility, but converge on the same independent consequential boundary and reconciliation obligations.](assets/shared-figures/rendered/F17-02.png){#fig:f17-02 width=5.75in}

A logical responsibility does not require an AI model: in Design A, deterministic rules implement E3 investigation and decision logic, including the next lookup and permitted recommendation. In B, the model contributes a bounded interpretation to an independently reviewed workflow. In C, a model or other agent mechanism proposes read-only tool selections under a controller-enforced budget. In all cases, proposal acceptance and eventual payment execution are separate transitions. A payment provider may process `RF-1042` and lose its acknowledgment; the workflow then records `UNKNOWN`, not `FAILED`. A payment idempotency key identifies the operation for a provider-defined deduplication contract; **it is not a security credential** and cannot substitute for E5 policy approval. Chapter 14 establishes the provider contract and external-effect semantics, while Chapter 15 establishes durable recovery.

## 17.6 Define the evidence that would falsify the choice

A selection is provisional until its assumptions survive a representative test. At minimum, compare the variants on the same tasks; preserve case and tenant identity; reject out-of-scope tool choices; test missing, poisoned and stale retrieved data; exercise timeouts, cancellation and budget exhaustion; and confirm that E3 cannot reach E6 write endpoints or E5 payment credentials. Model evaluations should test factual grounding and behavior under repeated trials, while system tests verify actual state and policy compliance. The τ-bench research illustrates why final environment state and repeated outcomes matter for tool-agent evaluation, without constituting a production guarantee (Yao et al., 2024).

Treat uncertain financial execution as a **separate** fault test, not an agent-quality evaluation. Before dispatch, E5 must independently approve the current payment, amount, case, tenant, policy version, required reviews and stable operation identity. Simulate the provider committing the refund then dropping its acknowledgment. E7 retains `RF-1042` with `UNKNOWN` outcome. E6 must query or reconcile according to its verified provider contract; E8 must supply appropriate external evidence before a confirmed business conclusion. The coordinator cannot fabricate a second operation identity to force progress. E9 must reveal the hold, aging and accountable next action. A successful language-model response proves none of these properties.

Figure 17.3 links pattern selection to **decision evidence**. A denial, uncertain outcome or deliberate human hold can be a correct system result. Release-readiness evidence therefore includes negative tests, reconciliation drills, explicit owners and documented residual risks, not simply an accuracy score.

![Figure 17.3 — Accept a pattern only when business value and independent system-level boundary evidence pass their separate gates.](assets/shared-figures/rendered/F17-03.png){#fig:f17-03 width=5.75in}

## 17.7 Record a decision that can be revisited

An **architecture decision record (ADR)** is a durable explanation of a significant choice, its context, alternatives, rationale and consequences. For Chapter 17, the record must state what could disprove the selection. It is not a release authorization and does not replace operational tests. Use this compact working record for the unchanged case:

| ADR field | CASE-204 selection |
|---|---|
| Decision | **Conditional B** for ambiguous complaint interpretation; A for routine rule-driven work; C remains a pilot alternative |
| Expected benefit | Reduced investigation time without delegating payment authority |
| Constraints | E1 tenant scope; E2 ownership; E3 advisory outputs; E4 source controls; independent E5/E6; E7/E8/E9 evidence |
| Alternatives rejected for now | Universal model control; C without measured additional value; direct agent-to-provider path |
| Evidence required | Comparative task study, cost per acceptable completion, review fidelity, policy denials, fault injection, operator drill |
| Revisit trigger | Persistent reviewer overload, unacceptable latency/cost, stale evidence, new provider guarantees, failed negative tests |

If the evidence contradicts B's economic assumptions, select A for more case types or restrict AI to drafting. If C demonstrates durable improvement, evaluate the *additional* bounded tool-selection contract separately. Neither decision changes E5's authority or permits a worker to access payment credentials. Decisions should also be reviewed after provider-contract changes or production incidents; verification is ongoing, not a one-time diagram review.

## 17.8 Transition to coordination patterns

This chapter answered **which tasks justify adaptive selection**. It did not yet decide how an organization should arrange generalist and specialist workers, supervisor ownership, handoffs or agent registry registration. Chapter 18 compares those coordination and delegation patterns, holding the same E2 logical-owner and fencing requirements from Chapters 10 and 15. Chapters 19–21 will then examine tools and effect isolation, state and memory distinctions, and enforceable architecture decisions. Part III thus extends the Chapter 8 reference architecture by making explicit choices *within* its domains—not by replacing its trust boundaries.

## Chapter 17 — Engineering practice

1. **Classify.** For policy-threshold validation, complaint summarization, selection of follow-up shipment queries and financial dispatch, choose the simplest sufficient mechanism. Identify the authoritative facts and why a model would or would not help.
2. **Compare.** Construct a measured A/B/C experiment with at least two difficult-case strata. Define acceptable completion rather than measuring only answer quality.
3. **Map.** Annotate Figure 8.1 to show which of E2/E3/E4 differs under A, B and C and which E1/E5/E6/E7/E8/E9 guarantees may not change.
4. **Threat-model.** A bounded agent requests a payment tool absent from its permitted catalog. Specify the response, denial evidence and escalation, rather than a stronger prompt.
5. **Fault-inject.** The provider accepts `RF-1042` but its acknowledgment is lost. Specify the correct durable state, ownership, reconciliation and customer communication; explain why a new identity is unsafe.
6. **Defend.** Write an ADR selecting B or rejecting it under a changed cost distribution. Name one observed result that would reverse the decision and one control that remains non-negotiable.

**Review standard:** A strong answer separates task selection from authorization; compares the simplest viable alternative and the whole-workflow economics; preserves CASE-204 and `RF-1042`; and names falsifiable safety, failure, recovery and governance evidence. Calling an agent more capable is not a proof of business benefit or of consequential authority.

## Sources and further reading

Relevant external foundations include Parasuraman, Sheridan, and Wickens (2000) on function-specific automation, Russell and Norvig (2020) on agent mechanisms, Bass, Clements, and Kazman (2021) on architecture tradeoffs, Anthropic Engineering (2024) and OpenAI (2026) as vendor pattern guidance, FinOps Foundation (2025) on unit economics, and Yao et al. (2024) on tool-agent evaluation. The decision gate, E-domain mapping, illustrative metrics, and CASE-204 ADR are ETIS engineering synthesis; the cited publications do not certify a particular refund architecture.
