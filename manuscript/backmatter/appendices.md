# Appendices

## Architectural contract reader reference (C01–C09)

The nine **E1–E9 logical responsibilities** in Chapter 8, Table 8.1, describe accountable work; the **C01–C09 cross-domain contracts** in Table 8.2 govern interactions between responsibilities. Neither list determines a service count, physical topology, or runtime call order. This reader map is an explanatory summary, **not a substitute for CAB-001's approved field-level definitions** or tested implementation schemas.

| Contract | Logical handoff | What an engineer must demonstrate |
|---|---|---|
| C01 — Admission | E1 → E2 | Verified principal and tenant; accepted goal, bounded scope, policy and expiration |
| C02 — Work order | E2 → E3 | Task identity, owner epoch, tool and cost limits, schema version, deadline and denial |
| C03 — Context query | E3 → E4 | Resource-level authorization, provenance, classification, freshness and safe denial |
| C04 — Action proposal | E3 → E5 | Proposed `operation_id` (advisory correlation), requested effect, amount, rationale, evidence and idempotency intent; **no financial authorization or provider key** |
| C05 — Decision | E5 ↔ E9 | Independent policy and approval outcome, actor, current version, reasons and evidence |
| C06 — Durable intent | E5 ↔ E7 | Trusted stable operation identity, uniqueness and fenced durable transition before dispatch |
| C07 — Provider dispatch | E5 → E6 → E8 | Bounded provider operation, authenticated adapter, provider-specific idempotency and uncertain results |
| C08 — Reconciliation | E7/E5 ↔ E8 | Correlate original operation with authoritative evidence; preserve UNKNOWN when inconclusive |
| C09 — Telemetry/assurance | E1–E8 → E9 | Correlate decisions, denial, cost, ownership, effect observations, privacy and accountability |

**Identifier rule.** CAB-001 C04 `operation_id` identifies a proposed action for review, while `idempotency intent` requests duplicate-safe behavior. Neither is RF-1042 or a provider idempotency key; only the separately authorized trusted path assigns and durably records RF-1042 and maps provider keys under the verified adapter contract.

**Reading the refund trace.** CASE-204 is admitted; its task may yield a Design B advisory recommendation or Design C bounded read-only evidence. C04 does not grant E3 a payment credential or the right to create `RF-1042`. After an independently evidenced C05 authorization, E5/E7 creates and durably records the stable payment operation under C06. E5/E6 may then dispatch under C07; if the provider acknowledgment is missing, E7 retains `UNKNOWN` until C08 obtains adequate E8/provider evidence or escalates. C09 assurance runs throughout rather than at the end. A single process may implement several logical responsibilities while preserving their enforcement and audit boundaries.

**Who owns which state?** E7 is authoritative for local workflow ownership, task transitions, operation intent and the application's knowledge of payment attempts. E8 supplies externally authoritative financial facts and business-case dispositions. E7 may update its local outcome only through verified reconciliation; these are complementary records, not conflicting owners of one field.

**Book path.** Chapter 3 introduces bounded delegation; Chapter 7 converts obligations to requirements; Chapter 8 allocates responsibilities and contracts; Chapters 9–16 explain enforcement and recovery; Chapters 17–21 compare architectural alternatives, tools, information ownership, and governance decisions. Chapters 22–36 remain planned implementation, assurance, operations, and reference work—not completed evidence. The full publishable field-level schema set belongs in Chapter 35 when that chapter is developed; until then, the reader map here is deliberately bounded.

## Remaining planned appendices

Reference implementation setup, deployment, and release-readiness checklists will be completed after their corresponding chapters. Their present absence does not imply completed evidence.
