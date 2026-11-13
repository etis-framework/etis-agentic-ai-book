# CAB-001 architecture catalog (summary; authoritative source is metadata/approved/CAB-001.docx)

| ID | Responsibility |
|---|---|
| E1 | Engagement and admission |
| E2 | Coordination and control |
| E3 | Agent reasoning |
| E4 | Context and knowledge |
| E5 | Trusted execution |
| E6 | Enterprise integration |
| E7 | Durable operational state |
| E8 | Business systems of record |
| E9 | Governance and assurance |

Contracts C01–C09 remain defined by CAB-001. This summary is not a replacement for the approved baseline.

## C01–C09 cross-domain contracts (transcribed from approved CAB-001)

| ID | Boundary | Contract |
|---|---|---|
| C01 | E1 → E2 | Admission: workflow, tenant, principal, goal, scope, risk, policy, deadline |
| C02 | E2 → E3 | Work order: task, workflow, allowed tools, scoped context, deadline, version pins |
| C03 | E3 → E4 | Context query: tenant, identity, purpose, filters, freshness; provenance/classification response |
| C04 | E3 → E5 | Action proposal: operation, effect, rationale, evidence, amount, idempotency intent |
| C05 | E5 ↔ E9 | Decision: policy version, authorization disposition, reason, actor/scope |
| C06 | E5 ↔ E7 | Durable intent: unique operation, pre-dispatch persistence, state transition, fencing epoch |
| C07 | E5 → E6 → E8 | Provider dispatch: key, constrained request, status lookup, uncertain-result classification |
| C08 | E7/E5 ↔ E8 | Reconciliation: stable reference, confirmed/rejected/unknown classification |
| C09 | E1–E8 → E9 | Telemetry: correlation, versions, events, effect state, ownership, evidence retention |

These are approved logical contracts, **not** independently authenticated grants, nine service requirements, or a provider-specific guarantee. Consult `metadata/approved/CAB-001.docx` for the controlled field definitions.
