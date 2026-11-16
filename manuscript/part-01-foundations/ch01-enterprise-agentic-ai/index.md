# Chapter 1 — Why Enterprise Agentic AI Needs Engineering

*Part I: Foundations, Evolution, and Business Context*

> **The organizing thesis:** Agentic AI extends enterprise computing. It does not replace the architectural disciplines that made enterprise systems reliable, secure, and accountable.

## Learning objectives

By the end of this chapter, you should be able to distinguish an AI capability from a production system, compare deterministic and agentic solutions to the same business problem, identify consequential effects and their owners, and state the evidence required to trust a delegated action. The chapter introduces the refund case that will be implemented and tested progressively in Part IV.

## The promise—and the engineering question

A new generation of software can interpret ambiguous requests, choose information to examine, formulate plans, and propose actions. Those capabilities can make complex work more responsive. They do not, by themselves, establish that a proposed action is permissible, that the data are correct, or that an external business effect actually occurred. This book is about engineering the complete system around those capabilities.

Consider a retailer handling a $500 refund. The customer asks for a remedy, not a particular database update. The company must understand the request, determine the relevant order and policy, decide what it may offer, and, if authorized, arrange an actual payment reversal. A model can assist with interpretation; a goal-directed agent can decide which permitted investigation steps to perform; a workflow can coordinate the case; a payment system can execute the financial effect. These are different responsibilities, even when they appear to a customer as one seamless interaction.

This example will grow with the book. We will begin with a conventional deterministic application, then add AI assistance, bounded agentic decision-making, enterprise context, controlled execution, and recovery. Each addition must justify its benefit and its new engineering burden. The reference implementation is a teaching system, not a claim that every enterprise should adopt exactly the same deployment topology. The runnable examples and automated tests are provided in the book's GitHub repository at **https://github.com/etis-framework/etis-agentic-ai-book** under `examples/refund-reference-system/`; *How to use this book* explains the learning path and edition-specific access.

## Who this book is for and how to read it

A developing software engineer can read Parts I and II in sequence, use the definitions and exercises, and implement the staged reference system in Part IV. An experienced engineer or architect can consult the design alternatives, contracts, failure models, and verification criteria directly. Security, operations, governance, and business readers will find explicit ownership and evidence requirements, rather than assurances based on the apparent sophistication of an AI demonstration.

Throughout the book, *software engineer* includes people designing, implementing, testing, securing, operating, or reviewing these systems; the specific responsibility matters more than a job title. We introduce acronyms in full on first use and use architectural domain names in prose. For example, the later reference architecture calls the independently controlled authorization-and-execution responsibility **trusted execution (E5)**. Such identifiers are introduced only after the underlying responsibility is explained.


## The enterprise obligation is larger than functional success

The refund is successful only if the right customer receives the right remedy under the right authority, the payment outcome is known or explicitly unresolved, and the enterprise can explain and recover the case. A demonstration that produces the right answer once does not establish reliability, availability, serviceability, recoverability, security, privacy, acceptable latency, economic value, or maintainability. Nor does it establish that the remedy is fair, compliant, and consistent with the organization's customer commitments.

These are design inputs. Architecture quality attributes and their tradeoffs are developed systematically by Bass, Clements, and Kazman (2021); operational reliability and service ownership are addressed by Beyer et al. (2016). A reliability requirement might demand that an acknowledged refund never be duplicated during retries. A privacy requirement might forbid sending an entire customer history to a model when one order record suffices. A serviceability requirement might require an operator to reconstruct the exact policy version and provider operation identity. An ethical business requirement might prohibit a technically permissible but misleading offer. Each requirement must eventually have an owner, a control, and evidence of satisfaction. The architecture chapters will derive those responsibilities rather than treat them as late-stage checklist items.

## A vocabulary to carry through the book

| Term | Working meaning | Refund illustration |
|---|---|---|
| **AI model** | A computational model providing capabilities such as classification, prediction, or language generation | Interprets a customer's complaint |
| **AI agent** | A goal-directed software component that selects among permitted steps using reasoning or decision logic | Chooses which order evidence to retrieve before proposing a remedy |
| **Agentic workflow** | A coordinated business process containing agent decisions, deterministic tasks, and possibly human approvals | Investigate, evaluate, approve, issue, and reconcile a refund |
| **Agentic AI system** | The complete production system, including agents, integration, identity, state, controls, and operations | The customer-service refund application and its supporting services |
| **Autonomy** | The discretion delegated to software over selection, sequencing, and execution of actions | Suggest a refund versus independently initiate one |

An agent need not use a large language model (LLM). Rules, search, planners, small language models (SLMs), LLMs, and hybrid methods can all support goal-directed behavior. A workflow is not automatically agentic because it invokes an LLM, and a system is not necessarily more capable or trustworthy because it has multiple agents.


> Agentic AI is an evolution of enterprise computing, not a replacement for its engineering foundations. Modern AI expands what systems can interpret, propose, and coordinate; trustworthy operation still depends on authority, state, reliability, security, and accountability.

## 1.1 A customer asks for a refund

To make these distinctions concrete, a customer contacts an online retailer: “The replacement never arrived. I have contacted you twice. Please make this right.” The company has a paid order, a shipment record, a prior service case, a refund policy, and an external payment provider. An experienced service representative can combine those facts, decide what is fair within policy, and either initiate a refund or escalate the request. The work seems straightforward until we ask which parts can safely be delegated to software.

![Figure 1.1 — Three approaches to the same refund problem; all retain enterprise controls.](assets/shared-figures/rendered/F01-01.png){#fig:f01-01 width=5.75in}

The work separates into five responsibilities. The first is interpretation. Does “make this right” mean replace the item, issue store credit, or refund the original payment? The second is evidence gathering: which order, which shipment, what earlier contacts, and which policy version apply? The third is judgment: what remedy is permitted and what requires approval? The fourth is a consequential effect: the payment provider may transfer $500 back to the customer. The fifth is assurance: how will the company know whether the transfer happened, and what will it do if the provider times out?

None of these steps is entirely new. Retailers have used customer-service applications, workflow engines, rules, payment APIs, and audit logs for years. What is new is that modern language-capable software can interpret open-ended requests and propose intermediate steps that once required a person or a carefully scripted decision tree. That capability is valuable precisely because business work is often expressed in human language and involves exceptions. It is risky precisely because interpretation and proposed actions are not the same as verified authority.

This book follows one such case from a conventional deterministic implementation to a carefully bounded agentic system. The goal is not to automate every step. It is to discover which steps should remain deterministic, where flexible reasoning adds measurable value, and what evidence is required before the enterprise can trust the resulting operation.

## 1.2 The business problem precedes the technology

Organizations do not purchase delegated decision-making as an end in itself. They want shorter handling times, fewer avoidable handoffs, improved customer outcomes, better employee leverage, and the ability to manage work that does not fit rigid scripts. Those outcomes compete with other business requirements: predictable cost, regulatory compliance, consistent customer treatment, service continuity, and reputational protection.

Consider two refund requests. One is a routine duplicate charge with a clear policy and a reliable payment reference. A deterministic rule and a well-tested workflow may resolve it with little ambiguity. The other combines conflicting shipment records, a customer complaint, and an exception policy written in prose. Flexible reasoning might help summarize the evidence and suggest a remedy. In both cases, however, the final payment instruction should pass through the same independently enforced controls.

This distinction matters to investment decisions. A sophisticated agent that handles a simple eligibility rule can cost more to operate and more to assure than the rules engine it replaces. Conversely, forcing every unusual customer case through an ever-growing decision tree can create maintenance costs and frustrating escalations. The economically sound architecture may be hybrid: deterministic transaction and policy enforcement, with bounded reasoning for interpretation and evidence synthesis.

## 1.3 The central engineering question

When software is allowed to choose among actions, engineering must separate three questions that are often blurred in demonstrations: What does the software believe should happen? What is it authorized to do? What actually happened in the outside world?

The first question concerns reasoning and evidence. A model might infer that a $500 refund is appropriate, but its conclusion could rely on an incorrect order, stale policy, or malicious text embedded in a retrieved message. The second question concerns authority. A customer-service agent might be permitted to recommend refunds but not approve exceptions or issue transfers above a threshold. The third concerns reality. A payment provider might complete a refund even though the requesting system never receives its acknowledgment.

Engineering discipline exists to prevent these questions from collapsing into one convenient tool call. A proposal should be represented as data, checked against authenticated identity and authoritative business facts, evaluated under an explicit policy version, and converted into an external effect only by a controlled execution path. The resulting operation needs a stable identity and a recoverable record of its progress.

![Figure 1.2 — A proposed remedy must cross independent authorization and effect boundaries.](assets/shared-figures/rendered/F01-02.png){#fig:f01-02 width=5.75in}

## 1.4 What is genuinely different about modern agentic systems?

The term agent has a longer history than large language models. This broad historical distinction is consistent with the agent and planning treatments in Russell and Norvig (2020). In artificial intelligence, autonomous systems, operations research, and distributed software, engineers have long built goal-directed programs that observe conditions, select actions, and revise plans. Modern generative models extend that lineage by interpreting natural-language tasks, synthesizing plans, generating structured outputs, and selecting among tools with less task-specific programming. Research demonstrations of interleaved reasoning and action and model-mediated tool use include Yao et al. (2023) and Schick et al. (2023); neither study establishes enterprise authorization or operational safety.

The practical shift is a larger and less predictable decision surface. Traditional software usually follows control paths explicitly encoded by developers, although complex distributed systems and machine-learning pipelines already have substantial uncertainty. A model-guided agent can produce a plausible plan that its developer did not enumerate. That can be a strength in ambiguous tasks, but it also creates verification problems: tool arguments can be invented, retrieved instructions can be misinterpreted as authority, and successive steps can amplify earlier mistakes.

This is not a claim that all modern agents are LLMs. An agent can use rules, search, planning algorithms, statistical models, small language models, large language models, or combinations. “Agentic” describes the system’s goal-directed decision and action behavior, not the size or marketing category of its model. Likewise, multiple agents are an architectural choice, not a requirement for sophistication.

## 1.5 A useful spectrum of delegation

At one end, software provides assistance: a human reads a summary, makes the decision, and initiates the action. Next, bounded automation executes a well-defined task under fixed rules. Farther along, a system can choose among permitted strategies, request information, and propose actions. At the highest end, a system may coordinate several specialized capabilities over a long-running task. These are not maturity levels that every enterprise must climb.

Each increase in delegation changes what must be specified and tested. A summarizer needs evidence quality and privacy controls. An advisory refund agent needs proposal schemas and evaluation. A refund executor needs independent authorization, durable operation identity, provider guarantees, and reconciliation. A multiagent coordinator additionally needs bounded delegation, task ownership, timeouts, and rules for resolving disagreement. Greater autonomy without corresponding controls merely transfers risk into a less visible part of the system.

![Figure 1.3 — Delegation increases discretion and changes the evidence required.](assets/shared-figures/rendered/F01-03.png){#fig:f01-03 width=5.75in}

## 1.6 A small failure with a large lesson

Imagine that the trusted refund service records an intended $500 refund and sends the request to the payment provider. The provider processes it, but the network connection fails before the acknowledgment arrives. The local service sees a timeout. Has the refund failed? No. The only supported conclusion is that the outcome is uncertain. The distinction between local observation and external effects is grounded in transaction and distributed-systems engineering (Gray and Reuter, 1992; Kleppmann, 2017).

If the service treats a timeout as failure and sends a new refund under a different operation identifier, the customer may receive $1,000. The model may have reasoned perfectly about the complaint. The failure arose in an established distributed-systems problem: partial knowledge of an external effect. The remedy is not a more capable model. It is durable intent, stable operation identity, provider idempotency where supported, status queries, reconciliation, and an accountable path for unresolved cases.

This example captures the book’s governing distinction: model capability and system trustworthiness are different properties. A compelling demonstration can show that a model reaches a useful answer. It cannot, by itself, establish that the system will remain safe through network partitions, retries, stale workers, changing policies, or adversarial inputs.

## 1.7 The enterprise system surrounding the agent

A production agent does not exist in a vacuum. It enters through an authenticated channel, receives a scoped task, consults data whose freshness and ownership matter, and uses enterprise interfaces whose effects can be consequential. It must be monitored by people who can investigate, stop, repair, and recover the service. Security and governance are therefore not post-processing activities attached to a model; they are responsibilities of the entire system. For external risk-management context, see NIST AI 100-1 (2023) and its generative-AI profile, NIST AI 600-1 (2024).

Later chapters organize these responsibilities into nine logical enterprise responsibilities: admission; coordination; reasoning; context; trusted execution; integration; durable operational state; authoritative business systems; and governance and assurance. The identifiers are a navigation aid, not an instruction to deploy nine microservices. We deliberately postpone the complete architecture diagram until the reader understands why these responsibilities must be distinguished.

For the refund case, the enterprise customer and payment systems retain the business truth. A context store can help interpret the complaint, but it cannot become the authoritative refund ledger. A coordinator can schedule work, but its registry cannot grant payment permission. A model can propose a refund, but it cannot authorize itself to make one. These separations are inherited from long-standing enterprise engineering, sharpened for systems whose reasoning is more variable.

## 1.8 Business economics must include failure and assurance

The business case for an agentic capability should compare it with the best practical deterministic or human-assisted alternative. Measure the cost per successfully resolved case, not merely the cost per model call. Include model inference, retrieval, integration, evaluation, human review, operational support, exception handling, and recovery. Also measure the effect on customer outcomes and employees: fewer handoffs are not a win if reviewers must correct more plausible-looking errors.

A simple illustrative calculation shows why. Suppose a workflow handles 10,000 cases a month and saves two minutes of human work on 70 percent of them. That yields roughly 233 hours of gross handling-time reduction. If the system then requires one minute of review on all 10,000 cases, the gross benefit falls by about 167 hours before adding infrastructure and incident costs. The precise economics will vary, but the method is stable: compare complete workflows and count shifted labor.

Trustworthy engineering is not opposed to business value. It makes value sustainable. A design that cannot prove whether a refund was issued may appear inexpensive until the first reconciliation incident. A design with no controlled rollback may ship quickly but impose a disproportionate recovery cost. Enterprise architecture must make those tradeoffs visible before procurement or deployment.

## 1.9 What the reader will build and learn

The book is organized as a progression from inherited engineering disciplines to a working, testable system. Part I develops the historical, conceptual, and economic foundations. Part II derives an enterprise reference architecture from explicit requirements. Part III compares implementation patterns and their tradeoffs. Part IV builds the refund system in stages, starting with deterministic behavior and adding bounded reasoning only where justified. Part V breaks the system deliberately through failure and adversarial tests. Part VI addresses oversight, release governance, operations, and lifecycle economics. Part VII provides contracts, exercises, checklists, and review artifacts.

Readers who are newer to enterprise computing can follow the narrative and reproduce the reference implementation. Experienced architects can use the component contracts, alternatives, failure models, and verification evidence as a design-review reference. Security and operations readers should be able to identify the controls they own and the evidence required to assess them. No one should have to accept an architecture merely because a diagram labels it “trusted.”




## 1.10 Questions that guide every design review

The recurring questions are deliberately older than generative AI: What business outcome are we pursuing? Which task genuinely benefits from flexible reasoning? Who owns the decision and the resulting effect? Which record is authoritative? What happens when a component fails or the outcome is unknown? What evidence would persuade a skeptical reviewer that the controls work? These questions connect the refund example to the architectural decisions developed in later chapters.

A design that answers them may use one advisory model, a bounded agent, or no AI at all. The choice should follow the business problem and the evidence—not a desire to maximize autonomy.

**Reading the review from different responsibilities.** The same refund proposal has different acceptance questions: the business owner asks what outcome is worth the risk; engineering asks whether the program and its tests meet the contract; security asks who can actually invoke payment; and operations asks how a lost acknowledgment is recovered. Later chapters turn these complementary professional review perspectives into explicit architecture evidence. They are not additional subsystems or a mandatory review committee.

## Worked design review: should an agent issue the refund?

**Situation.** A customer requests a $500 refund. The order service reports a captured payment of $500. The delivery service reports an unresolved delivery exception. A language model recommends a full refund and gives a persuasive explanation. The payment provider supports idempotency keys but may time out after accepting a request.

**Decision 1 — Where does flexible reasoning help?** The customer complaint is ambiguous, so a bounded reasoning component may summarize evidence and propose a remedy. The proposal must carry an order identifier, evidence references, proposed amount, and a reason. It is *not* a payment instruction.

**Decision 2 — Who may authorize the effect?** An independently enforced policy evaluates the authenticated principal, customer and tenant scope, captured amount, previous refunds, approval limits, and policy version. A model cannot grant itself an exception. If evidence conflicts or the amount exceeds delegated authority, the workflow routes the case to a person.

**Decision 3 — What happens before the network call?** The system creates a durable operation record with a stable identifier and an explicit state such as `AUTHORIZED`. The adapter uses that identifier according to the provider's documented idempotency contract. The operation record is not itself proof that the provider has paid the customer.

**Decision 4 — What happens on timeout?** The system marks the external outcome `UNKNOWN`, stops blind retries, and queries the provider or initiates reconciliation using the stable operation identity. It tells the customer that the result is being verified, not that the refund succeeded. An operator has a documented escalation path if the provider cannot resolve the ambiguity.

**Decision 5 — What evidence would justify release?** Require a policy-denial test, a duplicate-request test, a lost-acknowledgment test, a crash-and-resume test, an unauthorized cross-tenant access test, and a reconciliation drill. Record owners and acceptance criteria. A demonstration of the happy path satisfies none of these by itself.

**Architecture judgment.** This case supports a *hybrid* design: adaptive interpretation and recommendation, deterministic authority enforcement and durable execution. A fully autonomous refund agent would require additional benefits and evidence to justify its greater discretion.

## Engineering quality attributes are requirements, not adjectives

For the refund system, a design review should translate qualities into measurable obligations. The examples below are illustrative design targets, **not** universal service-level objectives or established industry benchmarks.

| Attribute | Example requirement | Evidence or test |
|---|---|---|
| Reliability | A repeated request with the same operation identity cannot create a second refund under the provider's documented guarantee | Duplicate and replay test |
| Availability | If model inference is unavailable, the case remains durable and can route to a deterministic or human path | Dependency-outage exercise |
| Serviceability | An operator can reconstruct policy version, authority decision, operation identity, and last observed provider result | Case reconstruction drill |
| Recoverability | A crash after provider dispatch does not silently convert an unknown result into success or a new payment attempt | Crash-and-restart test |
| Security | A model-proposed call cannot exceed the principal's approved refund scope | Privilege and cross-tenant denial tests |
| Privacy | Only necessary customer data reach the model and are retained according to policy | Data-flow review and retention test |
| Performance and cost | Tail latency and per-case costs remain within approved business budgets | Load test and cost telemetry |
| Maintainability | A provider contract change is isolated to a versioned adapter and contract tests | Adapter substitution exercise |
| Fairness and customer trust | Equivalent cases follow consistent policy; unresolved payment status is communicated accurately | Scenario evaluation and communications review |

**ETIS evidence trail.** A requirement should lead to a recorded design decision, a control in the execution path, a test result, a release decision, and operational observations. The artifact chain matters more than the tool used to produce it.

## Chapter 1 — Engineering practice

1. **Explain.** Distinguish an AI model, a goal-directed agent, an agentic workflow, and the complete enterprise system using the refund example. Identify one case where an LLM is useful but no agent is required.
2. **Analyze.** Compare deterministic and bounded-agentic approaches for (a) an unambiguous duplicate charge and (b) a complaint with conflicting delivery evidence. State the assumptions behind your comparison.
3. **Design.** Draw the major responsibilities needed to issue a refund without giving the model direct payment authority. Label the system of record and the durable workflow owner.
4. **Verify.** Define at least four observable pieces of evidence that would demonstrate the refund was correctly authorized and not duplicated.
5. **Defend.** A vendor promises an autonomous agent can replace the existing workflow engine. Identify the guarantees you would require before accepting that claim.

**Review standard:** A defensible response separates proposal from permission and external effect, identifies authoritative data, and explains failure handling. Merely listing products or technologies does not demonstrate engineering judgment.

## Further reading and historical bridge

Chapter 2 develops the engineering inheritance behind these controls. Its historical references are collected in the bibliography; the engineering conclusions remain subject to the cited sources and their stated scope.
