# How to use this book

The book is a continuous engineering argument and a practical reference. Read Parts I and II in order if enterprise architecture is new to you. Experienced practitioners can use the contracts, alternatives, failure scenarios, and review checklists selectively, while retaining the assumptions established in the foundations.

**The learning path.** Begin with business requirements and inherited computing patterns; derive logical boundaries; compare deterministic, advisory, and bounded-agentic approaches; implement the refund case incrementally; test failure and abuse; and evaluate governance, economics, and operational readiness.

**Following a topic through the book.** Read a topic from its foundation through its reference-architecture contract, pattern tradeoff, implementation, negative tests, and operational governance. For a reader-facing navigation path, use Chapter 8 §§8.3–8.4 for the reference architecture, Chapters 9–16 for its enforcement boundaries, Chapters 17–21 for architectural choices and their governance, and the Appendix, **Architectural contract reader reference**, for a compact contract map.

**The architecture notation.** Later chapters introduce nine logical enterprise responsibilities (E1–E9) and nine cross-domain contracts (C01–C09). The responsibilities say what must be done; the contracts define handoff obligations, data, controls, and evidence. Chapter 8 §§8.3–8.4 explains both; the Appendix supplies a reader-oriented C01–C09 reference. The book gives readable responsibility and contract definitions in Chapter 8 and the Appendix; no external architecture file is required to follow the discussion. Chapter 35 provides the reader-facing schemas and reference artifacts needed to apply the contracts. The compact appendix map is a navigation aid, not an implementation schema. Identifiers support traceability, not permission or proof. They do not imply nine separate services or require multiple agents.

**The case and exercises.** The $500 refund is an illustrative running case, not a provider-specific production design. Early exercises ask readers to explain requirements and tradeoffs. Later work asks for schemas, code, policy checks, tests, incident evidence, and defended release decisions. Where a contract depends on a provider, verify its actual guarantees.

**Evidence discipline.** Distinguish a proposal from authorization, an attempted effect from a confirmed effect, and a demonstration from a validated operating system. Record assumptions, quality-attribute scenarios, threat boundaries, ownership, and recovery mechanisms. A plausible answer is not proof.

**Reader pathways.** Developing engineers should complete the exercises in sequence. Architects should focus on responsibility boundaries and alternative decisions. Security and privacy reviewers should trace authority, data use, and human recourse. Operations teams should emphasize unknown outcomes, failure injection, reconciliation, serviceability, and cost of ownership. Business leaders should ask what measurable value is created and which residual risks are explicitly accepted.


## The companion reference implementation

This book includes **runnable Python source code, tests, architecture figures, and reproducible exercises**, not merely pseudocode. The same fictional case, **CASE-204**, anchors the examples: a proposed **$500 refund** whose independently authorized payment operation is **RF-1042**. Readers can reproduce the baseline, explore denied actions and uncertain outcomes, and compare each added capability against the deterministic alternative.

**Find the code:** the official ETIS book repository is **https://github.com/etis-framework/etis-agentic-ai-book**. Open the **`examples/refund-reference-system/`** directory and read its `README.md` first. Direct directory link: **https://github.com/etis-framework/etis-agentic-ai-book/tree/main/examples/refund-reference-system**. Public access to the official repository will be enabled for the published edition; an edition-specific tag preserves the matching implementation. For an edition-specific reproduction, use the Git tag identified with that edition rather than assuming that the newest `main` branch matches printed examples. No paid service or payment credentials are necessary for Build 0.

| Reading path | Companion experience |
|---|---|
| Parts I–III | Follow the same case through requirements, E1–E9 responsibilities, C01–C09 contracts and Designs A/B/C; identify the controls that the code must preserve |
| Part IV, Chapters 22–27 | Run Builds 0–5 incrementally; compare source, figures, test cases, evidence and assumptions for each build |
| Part V, Chapters 28–31 | Challenge the implementation with failures, abuse cases, recovery and end-state verification |
| Parts VI–VII, Chapters 32–36 | Use operational and governance evidence, reusable contracts, review criteria and exercises to defend deployment decisions |

**Builds are teaching checkpoints, not autonomy levels.** Design A is deterministic; Design B adds bounded advisory assistance with independent review; Design C adds optional bounded investigation. The six builds do not demand a Design A → B → C production migration. Each example documents what it demonstrates and what remains outside its assurance boundary. In particular, the simulator's **E7 local operational record** and simulated **E8 provider record** are deliberately separate: a provider effect may occur before the application knows its outcome. Passing tests establishes only the stated scenario under the stated assumptions.

**Reproduction and accessibility.** Chapter 22 gives the first exact commands and shows how to inspect both records. The code README gives directory navigation, prerequisites and build-specific instructions; text and figures in this book explain the architecture without requiring access to a separate internal design document. Published editions identify a fixed source revision and an errata path.

**Reading command listings.** Fixed-width, lightly shaded listings show literal shell commands or configuration. A line ending in `\` is continued on the following indented line; paste the entire command together. Run commands from the repository root unless stated otherwise. No prompt character is part of the command.
