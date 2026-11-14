# Appendices

## Architectural contract reader reference (C01–C09)

The logical responsibilities (E1–E9) and cross-domain contracts (C01–C09) are defined in Chapter 8. A responsibility describes accountable work; a contract defines an independently checkable handoff. The following compact map is for navigation, **not** a deployable schema or evidence that an interface is authorized. Several responsibilities may share one service without sharing authority.

| Contract | Logical handoff | Required evidence |
|---|---|---|
| C01 — Admission | E1 to E2 | Identity, tenant, accepted purpose, scope and expiry |
| C02 — Work order | E2 to E3 | Work identity, owner/epoch, limits, deadline and denial |
| C03 — Context query | E3 to E4 | Resource scope, provenance, freshness and refusal |
| C04 — Action proposal | E3 to E5 | Typed **advisory** request and evidence; no payment approval |
| C05 — Decision | E5 and E9 (two-way) | Independent policy/approval result and audit evidence |
| C06 — Durable intent | E5 and E7 (two-way) | Unique trusted operation ID and durable pre-dispatch claim |
| C07 — Provider dispatch | E5 to E6 to E8 | Provider contract, stable key and uncertain-result handling |
| C08 — Reconciliation | E7/E5 and E8 (two-way) | Provider observation or explicit unresolved outcome |
| C09 — Assurance | E1–E8 to E9 | Correlated decisions, ownership, effects and accountability |

**C04 field semantics and contract direction.** Proposed `operation_id` in C04 identifies an **advisory correlation reference**; `idempotency intent` expresses requested duplicate-safe behavior. Neither is RF-1042 or a provider idempotency key. “Two-way” denotes a controlled request/response or reconciliation relationship, **not** authority to self-approve. Following independent C05 authorization, E5 controls creation of RF-1042, the stable financial-operation identity, and E6 maps a provider idempotency key only under its verified contract. E7 persists intent and observations before possible E6 dispatch; E8 retains authoritative provider facts, which can differ from E7's current knowledge.

**E2 ownership versus E7 persistence.** Coordination and registry responsibility (E2) owns scheduling, leases, worker assignment and the logical right to advance the case workflow. Durable operational state (E7) supplies persisted workflow/operation evidence and atomic state transitions under the rules governing that ownership. Build 5's E2-owned coordination record is stored locally in SQLite as an educational fixture; this does not redefine E7 or grant E2 permission to issue a refund. E5 must independently enforce the consequential-operation boundary. Build 5's epoch checks protect E2-local mutations, **not** end-to-end E5 dispatch against a malicious stale process.

**CASE-204 trace.** The $500 proposed remedy may emerge from Design A's deterministic process, Design B's bounded advice, or Design C's optional bounded investigation. These are alternatives, not three mandatory sequential phases. E3/C04 cannot assign RF-1042. Following independent E5 authorization, durable intent precedes any E6 dispatch. On lost acknowledgment, E7 records UNKNOWN; C08 queries the provider's existing operation without creating a second refund. E9 evidence and governance apply throughout.

## Reader paths and companion implementation

Chapter 7 establishes requirements; Chapter 8 specifies responsibility and contract names; Chapters 9–16 explain their intended boundaries; Chapters 17–21 compare patterns and accountable decisions. Chapters 22–27 provide executable Builds 0–5. Chapters 28–34 are intended to examine failures, assurance, governance and economics. Chapters 35–36 are reserved for expanded schemas, reusable references and exercises; **those chapters are still planned in this working manuscript**, so this appendix is the current compact reader map, not their substitute.

The companion examples, source diagrams and negative tests live in the official repository at https://github.com/etis-framework/etis-agentic-ai-book, directory `examples/refund-reference-system/`. Begin with its `README.md`, then follow each build's README and embedded `architecture.svg`. The source is private during development; the published edition must identify a fixed Git tag and public access route. Each build is independently runnable as a teaching checkpoint, not a progressively certified payment platform.

**Build 0 — Deterministic baseline (Chapter 22).** Local E7 state and a separate mock E8 provider record distinguish intended action from observed external effect. See `build0/README.md`.

**Build 1 — Advisory proposal (Chapter 23).** E3/C04 produces a typed untrusted recommendation, with no authority to create RF-1042. See `build1/README.md`.

**Build 2 — Scoped identity and context (Chapter 24).** E1 fixture assertions and E4/C03 source selection illustrate bounded context, not production authentication or independent tenant isolation. See `build2/README.md`.

**Build 3 — Trusted execution (Chapter 25).** A separate E5 process rejects a valid-token compromised investigator without transaction-specific finance approval. Same-user process execution does not confer OS-level isolation. See `build3/README.md`.

**Build 4 — Provider integration and reconciliation (Chapter 26).** Versioned simulated provider contracts, durable intent, status-only inquiry and preservation of UNKNOWN illustrate idempotency and recovery limits. Actual financial networks, provider credentials, settlement guarantees and long-lived recovery authorization are omitted deliberately. Fault-injection request fields are test-only. See `build4/README.md`.

**Build 5 — Optional coordination (Chapter 27).** Durable E2 work ownership, lease/epoch fencing and conservative takeover add workflow control without expanding E3/E2 financial authority. Local fencing is not independently enforced by E5, and shared-UID fixtures do not model hostile process isolation. See `build5/README.md`.

**Build 0–5 coverage and limits.** The [companion implementation-to-evidence map](examples/refund-reference-system/IMPLEMENTATION_EVIDENCE_MAP.md) identifies executed modules and tests, simulations, specified-only contracts and unimplemented production obligations. Build 5 composes E2 with the Build 4 E5 process using an E1 fixture; it does **not** execute the Build 1/2 advisory/retrieval pipeline as a single runtime. This distinction applies even when the cumulative learning progression covers all nine logical responsibilities.

**Chapter 28 recovery evidence supplement.** The educational `examples/refund-reference-system/reliability/` contains a pure typed recovery classifier and 10 negative/failure tests. It intentionally has no source/module architecture SVG because it is a focused analytical fixture, not a numbered companion build or effectful runtime. For the actual architecture, follow Build 4 and 5 source diagrams. Chapter 28 Figure 28.1 maps the logical boundaries; no new provider or E5 epoch guarantee is implied.
