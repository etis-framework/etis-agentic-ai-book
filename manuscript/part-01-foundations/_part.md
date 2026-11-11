# Part I — Foundations, Evolution, and Business Context

## The problem this part prepares you to solve

An enterprise can deploy a model that explains a refund policy in minutes. It cannot responsibly delegate a $500 refund merely because the model can generate a plausible explanation. The enterprise must decide who may act, which facts are authoritative, which operations are reversible, how failures are detected, and who is accountable when the result is uncertain. These are systems-engineering questions. They precede the selection of an agent framework.

Part I provides the conceptual foundation for answering them. It distinguishes the *capability* to propose an action from the *authority* to execute it; a generated plan from a durable workflow; retrieved information from authoritative business state; and a successful demonstration from evidence of production trust. The recurring refund case makes each distinction concrete. It is intentionally ordinary: the most revealing enterprise failures often occur in familiar workflows when exceptional conditions are ignored.

## What you should be able to do after Part I

1. Explain what changes when a software system can select steps dynamically, and what established engineering obligations remain unchanged.
2. Distinguish a model, agent, workflow, and complete agentic AI system without confusing the sophistication of a model with the trustworthiness of the system.
3. Identify where deterministic software, bounded reasoning, and human approval are each appropriate.
4. Describe the historical contributions of transactions, expert systems, planning, workflow, distributed systems, security, and operations to contemporary agent design.
5. Frame delegation in business terms: benefit, risk, cost, quality of service, and accountability.
6. State the evidence needed to justify an architecture and its release, including negative tests and recovery drills.

## The seven-chapter learning path

| Chapter | Question to answer | Engineering result |
|---|---|---|
| **1. Why Enterprise Agentic AI Needs Engineering** | What is the enterprise system responsible for beyond producing a plausible answer? | A first-cut delegation boundary and assurance questions |
| **2. A History of Automation, AI, and Enterprise Systems** | Which proven mechanisms should be inherited rather than reinvented? | A mapping from old disciplines to modern agent controls |
| **3. Enterprise Processes, Goals, and Bounded Autonomy** | What is a business goal, and who can authorize a consequential step? | A goal-to-action and decision-rights map |
| **4. What an Agent Is—and Is Not** | When is behavior agentic, and when is it ordinary automation? | A defensible system classification |
| **5. Business Cases, Value, and Lifecycle Economics** | Where does adaptability create enough value to justify complexity? | A benefit-and-total-cost comparison |
| **6. Uncertainty, Authority, and Enterprise Trust** | How do uncertainty and permission affect a design? | Explicit authority and uncertainty controls |
| **7. Engineering Principles and Requirements** | What must be specified before architecture and implementation? | Measurable requirements and evidence obligations |

Chapters 1–5 contain substantive draft material; Chapters 6–7 remain planned. The learning path states each chapter's editorial responsibility, not a claim that later draft chapters have already passed publication review.

## One case, progressively richer decisions

The $500 refund starts with a deterministic application: validate the payment, apply policy, record an intent, call a provider, and reconcile the outcome. We then ask whether AI can improve interpretation of an ambiguous customer request. If it can, the next question is not simply whether the agent can call a tool. It is whether the proposal is typed, authorized, bounded, logged, and recoverable. Later parts of the book will turn these questions into architecture contracts and a progressive reference implementation.

The reader should retain one principle throughout: **increase delegated discretion only when its benefit can be demonstrated and its consequences can be governed.** A narrower system that can be explained, tested, and recovered is often the more professional engineering choice.

## How to study this part

Read the prose for the argument, then use the diagrams to trace responsibility and the exercises to challenge assumptions. For each design decision, write down (a) the business objective, (b) what the system knows, (c) what it may do, (d) what could fail, and (e) the evidence needed to proceed. Those five questions recur throughout the ETIS Professional Series because trustworthy operation is demonstrated through engineering artifacts, not asserted through architectural labels.
