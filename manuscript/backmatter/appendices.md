# Appendices

These appendices are quick-reference material for the architecture, companion code and assurance boundaries. Chapter 8 provides the full architectural explanation; the example README files provide executable instructions. Neither the identifiers nor the examples establish production authorization by themselves.

## Appendix A — Reference architecture and contracts

The reference architecture separates logical responsibilities from trust boundaries and deployment boundaries. The names below are stable throughout the book; a responsibility is **not** necessarily a separate process, host, security principal or provider service.

| Responsibility | Reader meaning |
|---|---|
| E1 — Admission and identity | Authenticate and scope the initiating principal, purpose and tenancy |
| E2 — Durable coordination and ownership | Assign bounded work; manage workflow owners and epochs |
| E3 — Advisory agent reasoning | Produce untrusted analysis and action proposals |
| E4 — Context and provenance | Supply constrained, attributed inputs with freshness evidence |
| E5 — Independent trusted execution | Evaluate financial authorization and control consequential operations |
| E6 — Controlled provider adapter | Translate approved operations into restricted provider requests |
| E7 — Durable operational state | Persist intent, state transitions and local observations |
| E8 — Provider and business truth | Supply authoritative external operation and settlement facts |
| E9 — Governance and assurance | Define policy, accountability, audit requirements and review evidence |

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

**Authority and identity.** Proposed `operation_id` in C04 is an *advisory correlation reference*; `idempotency intent` asks for duplicate-safe behavior. Neither is RF-1042 or a provider idempotency key, and neither grants financial authorization. After independent C05 authorization, E5 controls trusted operation identity (RF-1042 for the CASE-204 $500 refund). E7 records durable intent before E6 may dispatch; E8 supplies the authoritative external outcome. C08 performs read-only reconciliation of the original operation when an acknowledgment is lost. `UNKNOWN` is not permission to replay a payment. The two-way notation describes controlled request/response, not self-approval.

**Ownership and scope.** E2 coordinates work while E7 persists operational evidence; neither may bypass E5. Build 5 fences local E2 records by ownership epoch, but E5 does *not* independently enforce the current-owner epoch. Local SQLite and same-user subprocesses do not confer independent secret custody, protected external audit or a real provider's settlement guarantee.

## Appendix B — Companion implementation guide

The authoritative companion tree is `examples/refund-reference-system/` in the project repository, https://github.com/etis-framework/etis-agentic-ai-book. Start with `examples/refund-reference-system/README.md` and `IMPLEMENTATION_EVIDENCE_MAP.md`. Paths in the tables are **relative to that companion tree**, not to this manuscript file. These are repository-relative file identifiers suitable for both printed and digital editions; a published edition must provide a fixed public release tag.

**Progressive reference implementation (Chapters 22–27)**

| Chapter | Example and reader entry point | Learning objective |
|---|---|---|
| 22 | Build 0 — `build0/README.md` | Deterministic case flow; distinguish local intent from mock provider truth |
| 23 | Build 1 — `build1/README.md` | Typed, untrusted agent advice without consequential authority |
| 24 | Build 2 — `build2/README.md` | Bounded identity assertions, context selection and provenance |
| 25 | Build 3 — `build3/README.md` | Independent E5 denial and scoped authorization through a subprocess fixture |
| 26 | Build 4 — `build4/README.md` | Durable financial intent, versioned mock adapter and read-only reconciliation |
| 27 | Build 5 — `build5/README.md` | Optional E2 ownership, lease/epoch fencing and conservative recovery |

Each build includes a source/module architecture SVG embedded in its README and runnable tests. They are individually executable teaching checkpoints; **Build 5 does not run the full Build 1/2 advisory pipeline as one integrated runtime**. The sequence does not represent a production payment platform.

**Reliability, security, operations and assurance exercises (Chapters 28–31)**

| Chapter | Companion directory and reader entry point | Learning objective |
|---|---|---|
| 28 — Distributed failure and recovery | `reliability/README.md` | Classify uncertain effects; require original-operation reconciliation rather than blind replay |
| 29 — Adversarial agent behavior | `security/README.md` | Deny a valid-token compromised investigator lacking transaction-specific E5 authority |
| 30 — Observability and incident response | `operations/README.md` | Classify signals and recommend containment without creating another payment effect |
| 31 — Verification and evidence | `assurance/README.md` | Collect reproducible local test evidence and explicitly distinguish it from release certification |

The Chapter 28 reliability fixture is an analytical classifier; use Build 4/5 architecture diagrams to study the effectful runtime. The security, operations and assurance READMEs include their own source/module diagrams. For exact commands, test names, educational comments, simulation boundaries and evidence outputs, follow the corresponding README rather than treating this printed reference as an executable manual. Designs A (deterministic baseline), B (bounded AI advice with independent financial review), and C (optional bounded agent investigation) are alternatives, not mandatory sequential runtime stages.

**Release/readiness navigation (Chapter 33; no new build)**

| Release question | Existing companion entry point | What remains unimplemented |
|---|---|---|
| Finance gate survives deployment or token misuse | `build3/README.md`, `security/README.md` | Production issuer revocation, live E5 isolation and keys |
| Lost reply during rollback, no redrive | `build4/README.md`, `reliability/README.md` | Actual provider C08 evidence and controlled rollback |
| Coordinator ownership across upgrades | `build5/README.md` | E5 authoritative current-owner epoch validation |
| Halt, incident and protected signals | `operations/README.md` | Independent live stop path, canary telemetry and incident drill |
| Release claims and source digests | `assurance/README.md` | Signed deployment artifact, attestations, change authorization |

Table 33.1 describes a **proposed** release manifest. No `release_id` class, automated canary, production release state machine, route switch or rollback mechanism is supplied by the companion Python project.

**Lifecycle economics navigation (Chapter 34; no new build)**

| Lifecycle question | Companion evidence to inspect | Not provided by the companion |
|---|---|---|
| Safe vs unauthorized financial outcome | `build3/README.md`; `security/README.md` | Independent production approval/key custody or measured financial loss |
| Cost of uncertain provider outcome | `build4/README.md`; `reliability/README.md` | Real provider inquiry costs, settlement and population loss rates |
| Cost of coordination/recovery | `build5/README.md`; `operations/README.md` | Distributed E5 owner-epoch enforcement, staffing and live incident cost |
| Cost of assurance and ongoing governance | `assurance/README.md`; `operations/README.md` | Signed certification, true invoices, case-value attribution or ROI dashboard |

**Tables 34.1–34.4 are proposed engineering decision records.** Their illustrative figures are not executable Python output or observed effectiveness. Start with the companion root README and `IMPLEMENTATION_EVIDENCE_MAP.md`; every listed README contains evidence scope and limits.

## Appendix C — Evidence and assurance reference

The example tests establish narrow facts about *local simulated behavior*. They do not establish external settlement, general model quality, hostile-process containment or production certification. Chapter 31 supplies the claim/falsifier method; the companion evidence map supplies source-to-test navigation.

| Evidence or assurance question | Demonstrated fixture scope | External evidence still required |
|---|---|---|
| Was the original refund intent durable? | Build 4 local E7 state/history and tests | Verified provider contract, independent storage/operation reviews |
| Can stale work owners safely dispatch? | Build 5 local E2 lease/epoch fences | E5 enforcement of current owner/epoch at consequential boundary |
| Does a valid agent token authorize a refund? | Chapter 29 Build 3 E5 denial tests | Production credential custody, delegation, revocation and adversarial isolation |
| Can incident classification create another RF-1042 effect? | Chapter 30 read-only observer negative tests | Protected telemetry, containment integration and operational incident drills |
| Is the cross-chapter assurance bundle reproducible? | Chapter 31 registered tests and source digests | Independent attestation, protected E9 audit, agent evaluation and release signoff |

An absent signal is not evidence of no effect. Local hash checks are not protected audit trails. An `EXECUTED_PASS` in a development bundle is not a production approval; `NOT_IMPLEMENTED` and `EXTERNAL_EVIDENCE_REQUIRED` remain visible obligations. Production acceptance must identify accountable owners, evidence provenance, falsification criteria and recovery authority before any consequential financial capability is enabled.

**Governance and approval (Chapter 32).** A release decision and a human manager's message are neither case-bound finance grants nor provider credentials. Figure 32.1 distinguishes agent delegation, independently verified financial authority and enterprise release governance. Figures 32.2–32.3 show controlled containment, read-only reconciliation and transaction denial. Chapter 32 Tables 32.1–32.2 specify human roles and the governance-decision record as **design requirements**, not implemented fixture features. E5 independent approver revocation and owner-epoch validation, protected audit custody, a live route-disable control and real provider evidence remain external production gates.

**Chapter 32 companion navigation (existing fixtures, no Build 6)**

| Governance decision | Companion entry point | Actual boundary |
|---|---|---|
| Compromised valid-token investigator | `security/README.md`, `build3/README.md` | Build 3 actual E5 subprocess denies without case-bound finance grant |
| Unknown provider effect | `reliability/README.md`, `build4/README.md` | Simulated original-operation status lookup; no blind resend |
| Stale coordination owner | `build5/README.md` | Local E2 fencing only; E5 owner enforcement missing |
| Incident containment analysis | `operations/README.md` | Read-only local observation, **not** a live route-disable action |
| Assurance for review | `assurance/README.md` | Local source/test evidence, not signoff or protected E9 audit |

**Lifecycle investment and retirement (Chapter 34).** Cost per acceptable completed workflow includes review, assurance, monitoring, recovery, staffing, residual exposure and exit. The hypothetical comparison in Table 34.2 is not companion telemetry or a prediction of deployed benefits. Missing E5 enforcement or authoritative E8 evidence is a hard gate, not a risk price. Figure 34.3 and Table 34.4 prescribe accountable decisions, not an autonomous deployment controller.

**Release authorization (Chapter 33).** A passing local regression is not release approval. Tables 33.1–33.3 identify proposed manifest fields, release-stage gates and exact fixture evidence, separated from external implementation and production proof. Figures 33.1–33.3 distinguish candidate evidence from E5 authority and software rollback from irreversible/uncertain provider effects. Runbook 33-A is a manuscript-local operating procedure, not software.


**Chapter 35 — Contract lookup and executable falsifiers (no new build)**

| Reader need | Reference | Evidence boundary |
|---|---|---|
| Contract meanings and failures (C01–C09) | Chapter 35 Table 35.1; Appendix A | Logical handoffs; not one composed Python call graph |
| Proposed fields versus actual fixtures | Chapter 35 Table 35.2; `IMPLEMENTATION_EVIDENCE_MAP.md` | No production governance/release schema or protected E5 ownership epoch |
| Fast test/source navigation | Chapter 35 Table 35.3; `build0/README.md` through `build5/README.md` | Independent educational checkpoints; Build 5 omits Build 1/2 advisory pipeline |
| Evidence packet and review owner | Chapter 35 Table 35.4; `assurance/README.md` | Local bounded tests, not external settlement or release certification |


**Chapter 36 capstone navigation.** The integrated exercises in Chapter 36 draw on Builds 0–5 plus the reliability, security, operations and assurance fixture directories. Table 36.1 maps decisions to architectural and operating evidence; Table 36.3 records the minimum reviewable assurance packet. These are exercises, not another executable build or a certified release.
