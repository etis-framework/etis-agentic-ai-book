# Part III — Patterns and Architectural Decisions

## From a reference architecture to defensible choices

Part II ended with a vendor-neutral, target-state logical reference architecture (Figure 8.1) and its possible deployment realizations (Chapter 16). It established **what must remain true**: authenticated and scoped work, one accountable workflow owner, advisory reasoning, provenance-bearing context, independent consequential authorization, controlled integration, durable state, authoritative business records, and observable assurance. Part III addresses a different question: **which design patterns are sufficient, and under which assumptions?** An architecture can be coherent while still being unnecessarily elaborate, financially unsustainable, or unsuitable for a particular provider or risk profile.

For `CASE-204`, the requested **$500 refund**, the three alternatives remain **Design A** (deterministic), **Design B** (advisory AI with independent review), and **Design C** (bounded read-only investigation agent). `RF-1042` remains the illustrative payment-operation identity once the trusted execution path is authorized. These are competing investigation designs, not stages in an autonomy ladder. In all three, the independent E5 boundary owns permission, E6 governs provider dispatch, E7 preserves uncertainty and recovery, E8 identifies authoritative business facts, and E9 supplies operating evidence. An AI component does not acquire provider credentials or financial authority by virtue of selecting a pattern.

## What you should be able to do after Part III

1. Select deterministic, advisory, bounded-agentic, or hybrid responsibilities using explicit task characteristics, consequence, expected value, and verification capacity.
2. Compare coordination and delegation patterns while preserving E2's one-logical-owner rule and independent E5 approval.
3. Select tool/adapter boundaries whose interface contracts and provider guarantees can actually be tested.
4. Distinguish ephemeral working context, governed retrieval, durable operational state, and authoritative business truth.
5. Record architectural decisions, their alternatives, assumptions, residual risks, and evidence thresholds; make governance enforceable in the delivered system.

## The five-chapter pattern roadmap

| Chapter | Design question | Reviewable outcome |
|---|---|---|
| **17 — Choosing deterministic, agentic and hybrid designs** | Where does flexible action selection justify its cost and assurance burden? | Decision matrix, candidate comparison and selection gate |
| **18 — Coordination and delegation patterns** | Which coordination arrangement maintains bounded delegation and one logical owner? | Ownership and handoff pattern decision |
| **19 — Tools, adapters and effect isolation** | How can a dynamic tool call remain outside consequential authority? | Contracted tool and protected adapter decision |
| **20 — State, memory and knowledge design** | What belongs in working context, durable state and authoritative records? | Data/state ownership decision |
| **21 — Architecture decisions and governance as code** | How are architectural assumptions and constraints made testable and reviewable? | Decision record with verifiable guardrails |

## One architecture; several pattern choices

The nine E1–E9 domains remain **logical responsibilities, not nine mandatory services or a prescribed call order**. The reference architecture is the consistency test for every pattern in Part III; it is not a catalog in which every listed mechanism must be deployed. In particular, increasing the capability of E3 reasoning must not create new E5 authority. E7 and E9 remain cross-cutting, and E8 business truth does not migrate into an agent's context store simply because that store is easier to query.

Part III works backward from evidence: define the outcome and risk, identify simpler alternatives, locate the relevant E-domain contracts, expose failure assumptions, and choose the smallest pattern whose guarantees can be demonstrated. Chapters 18–21 revisit those choices through coordination, adapters, state and governance. Part IV implements them; Parts V–VI test failure, security, operations and lifecycle economics. **A successful demonstration alone does not accept a pattern.**
