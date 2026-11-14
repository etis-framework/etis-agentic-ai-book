# Appendices

## Architectural contract reader reference (C01–C09)

The nine **E1–E9 logical responsibilities** in Chapter 8, Table 8.1, describe accountable work; the **C01–C09 cross-domain contracts** in Table 8.2 govern interactions between responsibilities. Neither list determines a service count, physical topology, or runtime call order. This reader map is an explanatory summary, **not a substitute for the detailed reader-facing schemas in Chapter 35** or tested implementation contracts.

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

**Identifier rule.** Under C04, the advisory `operation_id` identifies a proposed action for review, while `idempotency intent` requests duplicate-safe behavior. Neither is RF-1042 or a provider idempotency key; only the separately authorized trusted path assigns and durably records RF-1042 and maps provider keys under the verified adapter contract.

**Reading the refund trace.** CASE-204 is admitted; its task may yield a Design B advisory recommendation or Design C bounded read-only evidence. C04 does not grant E3 a payment credential or the right to create `RF-1042`. After an independently evidenced C05 authorization, E5/E7 creates and durably records the stable payment operation under C06. E5/E6 may then dispatch under C07; if the provider acknowledgment is missing, E7 retains `UNKNOWN` until C08 obtains adequate E8/provider evidence or escalates. C09 assurance runs throughout rather than at the end. A single process may implement several logical responsibilities while preserving their enforcement and audit boundaries.

**Who owns which state?** E7 is authoritative for local workflow ownership, task transitions, operation intent and the application's knowledge of payment attempts. E8 supplies externally authoritative financial facts and business-case dispositions. E7 may update its local outcome only through verified reconciliation; these are complementary records, not conflicting owners of one field.

**Book path.** Chapter 3 introduces bounded delegation; Chapter 7 converts obligations to requirements; Chapter 8 allocates responsibilities and contracts; Chapters 9–16 explain enforcement and recovery; Chapters 17–21 compare architectural alternatives, tools, information ownership, and governance decisions. Chapters 22–27 turn these controls into six progressive implementation builds; Chapters 28–31 stress them through failure, attack and verification. Chapters 32–34 develop accountable governance and operations, while Chapters 35–36 supply detailed reference artifacts and review exercises. This compact contract map remains a navigation aid rather than a tested deployment schema.

## Companion implementation and edition access

The book's **runnable Python examples, build-specific README guides and automated tests** are maintained in the official repository: **https://github.com/etis-framework/etis-agentic-ai-book**. Start at **https://github.com/etis-framework/etis-agentic-ai-book/tree/main/examples/refund-reference-system** (`examples/refund-reference-system/README.md`). Chapter 22 walks through the first executable baseline; Chapter 23 demonstrates the independently runnable, untrusted Build 1 advisory path, with its exercise at `examples/refund-reference-system/build1/README.md`. The same fictional identifiers—CASE-204, $500 and RF-1042—carry across the builds; individual checkpoints are reproducible demonstrations rather than repeated real refunds.

The repository is private during manuscript development and will be publicly accessible for the published edition. Use the **edition's published Git tag** for an exact code-to-text match. The companion README routes readers to each build and documents the limits of its fixtures, evidence and tests. Neither publication nor passing tests makes the example a live payment platform.

## Practical reference materials

Chapter 35 supplies detailed contracts, schemas and reference artifacts; Chapter 36 provides exercises, engineering reviews and an adoption roadmap. The companion README supplies installation-free Build 0 reproduction steps and the applicable per-build commands.

**Build 2 note.** Chapter 24's E1/C01 *fixture* verification is not complete authentication; E4/C03's local source selection is not production context authorization; E3/C04 remains an untrusted proposal, never RF-1042 or E5 permission. The companion `build2/README.md` supplies the independently runnable no-credential scope and provenance tests. The compromised valid-token consequential denial still belongs to Chapter 25 and later adversarial verification.
