# Preface

The most consequential lesson of enterprise computing is that useful software is not necessarily dependable software. A demonstration can show a compelling capability in minutes; a production system must sustain its promises across failures, changing requirements, hostile inputs, partial information, human mistakes, and years of operation. The distance between those two achievements is where engineering lives.

Agentic artificial intelligence makes that distance especially visible. We can now build software that interprets an objective, chooses what to investigate, reasons about alternatives, and proposes a course of action. In some circumstances it can coordinate a sequence of actions with less prescriptive programming than earlier systems required. These are meaningful capabilities. They also create new ways for uncertain interpretation to cross into systems that hold money, customer records, access rights, operational infrastructure, and an organization's reputation.

The engineering question is therefore not whether an agent can complete a task during a demonstration. It is whether the enterprise can explain **what the system was permitted to do, what it actually did, what it knows about the outcome, what it cannot know, and how people can recover when something goes wrong**. If the answer depends on trusting a fluent explanation from a model, the system is not yet adequately engineered.

## A continuation of engineering history

This book does not begin by declaring traditional software engineering obsolete. Transaction processing, database integrity, message delivery, workflow engines, access control, distributed coordination, service management, safety engineering, and operational governance emerged because earlier systems encountered real failures. They remain relevant. Agentic capabilities change the origin and variability of some decisions; they do not abolish the need for authoritative records, bounded authority, concurrency control, observability, or accountability.

This is also not an argument that every workflow needs an agent. Sometimes a deterministic program is simpler, cheaper, easier to verify, and more appropriate. Sometimes a model should advise a human without acting. Sometimes bounded autonomous investigation creates genuine value. The architecture should follow the business requirement and its constraints, not the fashion of the technology.

## The system, not the model, is the unit of trust

The subtitle's four verbs describe responsibilities rather than a maturity ladder. **Build** includes the simplest adequate deterministic, advisory or bounded-agent design. **Secure** means consequential permissions remain independently enforced, even if an agent is compromised. **Verify** means a claim can be falsified with tests and evidence, not accepted because a demonstration looked convincing. **Operate** means uncertainty, recovery, incident response, governance and business accountability remain first-class design obligations. No single agent framework or language guarantees any of them.


The model may propose a refund, recommend a maintenance action, classify a suspicious transaction, or summarize a regulatory obligation. None of those proposals, by itself, constitutes permission to change an enterprise system. Permission must come from explicit policy and delegated authority. Consequential execution must be independently controlled. Durable records must survive interruption. External effects must be reconciled against systems of record. Human operators must have a credible path to intervene, investigate, and recover.

The same rigor applies to dimensions that are sometimes treated as nonfunctional afterthoughts: reliability, availability, serviceability, recoverability, security, privacy, performance, scalability, cost, maintainability, interoperability, compliance, and business or brand trust. These are requirements that shape the architecture from its first decision. They can conflict. A good engineer makes those tradeoffs explicit and supplies evidence rather than slogans.

## How the argument is developed

The book starts with the business problem and the historical patterns we inherit. It then derives logical responsibilities and interface contracts, explores architectural alternatives, builds a reference implementation in controlled increments, and subjects that system to failures, adversarial conditions, operational review, and economic scrutiny. A recurring $500 refund case provides continuity, but the principles extend to enterprise IT, regulated workflows, customer operations, and other consequential environments.

A distinctive feature of this book is that readers can **examine and run the engineering argument**. An accompanying, source-controlled Python reference implementation includes executable refund examples, negative tests, and recovery exercises. It lets readers inspect the difference between a system that produces a plausible answer and one whose authority and outcomes can be tested. The examples follow the same CASE-204 $500 refund through Part IV; access instructions are in *How to use this book* and the official book repository at https://github.com/etis-framework/etis-agentic-ai-book. The implementation is educational, not a production payment service.

The implementation is deliberately progressive. A deterministic baseline comes first. Agent reasoning is added only where it improves a defined outcome. Identity, scoped context, trusted execution, durable state, provider integration, and reconciliation follow as explicit engineering responsibilities. Multiagent coordination is an optional design choice, not a required badge of maturity.

The intended readers range from engineers entering enterprise development to architects and technical leaders responsible for systems that must operate under real constraints. The explanations develop concepts before introducing identifiers and contracts. The exercises increasingly ask for decisions, testable assumptions, failure analysis, and evidence. Readers should be able to challenge the designs, not merely reproduce them.

This book's governing proposition is simple: **AI can accelerate the production of artifacts, but trustworthiness must be engineered, verified, governed, and maintained over time.**
