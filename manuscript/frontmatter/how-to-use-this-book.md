# How to use this book

The book is a continuous engineering argument and a practical reference. Read Parts I and II in order if enterprise architecture is new to you. Experienced practitioners can use the contracts, alternatives, failure scenarios, and review checklists selectively, while retaining the assumptions established in the foundations.

**The learning path.** Begin with business requirements and inherited computing patterns; derive logical boundaries; compare deterministic, advisory, and bounded-agentic approaches; implement the refund case incrementally; test failure and abuse; and evaluate governance, economics, and operational readiness.

**Following a topic through the book.** Read a topic from its foundation through its reference-architecture contract, pattern tradeoff, implementation, negative tests, and operational governance. For a reader-facing navigation path, use Chapter 8 §§8.3–8.4 for the reference architecture, Chapters 9–16 for its enforcement boundaries, Chapters 17–18 for architectural alternatives, and the Appendix, **Architectural contract reader reference**, for a compact contract map. The production team also maintains a more detailed internal traceability ledger; references to planned chapters are not evidence of completed content.

**The architecture notation.** Later chapters introduce nine logical enterprise responsibilities (E1–E9) and nine cross-domain contracts (C01–C09). The responsibilities say what must be done; the contracts define handoff obligations, data, controls, and evidence. Chapter 8 §§8.3–8.4 explains both; the Appendix supplies a reader-oriented C01–C09 reference. CAB-001 retains approved field-level definitions for implementers, and this book does not claim that the abridged contract map replaces them. The identifiers support traceability and do not substitute for the stated contracts. They do not imply nine separate services or require multiple agents.

**The case and exercises.** The $500 refund is an illustrative running case, not a provider-specific production design. Early exercises ask readers to explain requirements and tradeoffs. Later work asks for schemas, code, policy checks, tests, incident evidence, and defended release decisions. Where a contract depends on a provider, verify its actual guarantees.

**Evidence discipline.** Distinguish a proposal from authorization, an attempted effect from a confirmed effect, and a demonstration from a validated operating system. Record assumptions, quality-attribute scenarios, threat boundaries, ownership, and recovery mechanisms. A plausible answer is not proof.

**Reader pathways.** Developing engineers should complete the exercises in sequence. Architects should focus on responsibility boundaries and alternative decisions. Security and privacy reviewers should trace authority, data use, and human recourse. Operations teams should emphasize unknown outcomes, failure injection, reconciliation, serviceability, and cost of ownership. Business leaders should ask what measurable value is created and which residual risks are explicitly accepted.

**Source and edition notes.** Historical citations, edition metadata, and implementation dependencies are controlled publication work. Verify them before relying on this draft as a definitive external reference.
