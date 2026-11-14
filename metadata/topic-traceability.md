# Controlled topic traceability — Part III integration (2026-11-13)

**Purpose:** Preserve the reader's path: *introduce → define responsibility and contract → compare pattern → implement → test → operate/govern*. Existing citations below are verified against the supplied Chapter 18 V1 repository snapshot; later destinations are **planned obligations**, not claims of completed manuscript content. Resolve every future obligation at that chapter's acceptance gate. Never interpret a link as proof that enforcement works.

| Topic | Existing foundation (verified source locus) | Decision/application (verified) | Later planned obligation (unverified) | Evidence / invariant |
|---|---|---|---|---|
| E1–E9 / C01–C09 | Ch8 §§8.3–8.4, Fig 8.1; Ch9–16 | Part III introduction; Ch18 §18.1 | Ch19–20 contract application; Ch21 planned | CAB-001; logical domain ≠ deployable service |
| Logical ownership / fencing | Ch10 §§10.4–10.5, Fig 10.1; Ch15 | Ch18 §§18.2, 18.4, Fig 18.2 | Ch28 recovery; Ch31 verification | E2 one logical owner; E7 epoch/CAS; reject stale writes |
| Registry, admission and eligibility | Ch10 §§10.2–10.3, Fig 10.1; Ch9 | Ch18 §18.3 | Ch27 implementation; Ch31 tests | Registry ≠ identity grant, E7, or E10; check E1 scope and protected data access |
| Generalist/specialist vs deterministic worker | Ch4, Ch10 §10.7; Ch17 | Ch18 §18.2 lifecycle matrix | Ch27 scaling; Ch31 evaluation; Ch34 enterprise context | Measure deployment/version/evaluation/operating cost, not agent count |
| Hub versus peer advisory messages | Ch10 §10.7 | Ch18 §§18.2, 18.5 and Fig 18.1 | Ch29 security; Ch30 observability | Peer messages never transfer E2 ownership or E5 authority |
| Scoped delegation | Ch9, Ch10 §10.5; Ch13 | Ch18 §18.3 | Ch24 implementation; Ch29 threat tests | Envelope narrows scope; independent E4/E5 denial |
| Effect isolation / business truth | Ch13–16 | Ch18 §§18.3–18.4; Ch19 §§19.3–19.5, Figs 19.1–19.2 | Ch25–26 implementation; Ch28 reconciliation | CASE-204 $500; RF-1042; UNKNOWN ≠ FAILED; no blind retry |
| Lifecycle economics | Ch5; Ch16–17 | Ch18 §§18.2, 18.5–18.6 | Ch27 capacity; Ch30 operations; Ch34 economics | Cost per acceptable completed workflow, common-case benchmark |
| Human containment | Ch7, Ch10 §10.8, Ch15 | Ch18 §§18.5–18.6 | Ch30 incident response; Ch32 oversight | Stop is enforceable; in-flight external effects reconciled |

## Maintenance and acceptance

- When a later chapter is drafted, change its obligation to *verified* only after checking its exact section, figure, tests and citations.
- A change to CAB-001, a design label, or a contract requires a manuscript-wide impact review; a cross-reference addition alone does not.
- Each developed chapter's QA reports missing foundation, missing implementation, missing negative tests, absent source or untested operational assumption; do not silently close an evidence gap.
- For architectural claims, cite at the claim using the existing author–year convention and maintain matching entries in the back-of-book bibliography, `references/bibliography.bib`, and `references/source-register.md`.

## Whole-book conceptual-continuity review gate (Chapter 18 integration)

Before accepting each chapter, inspect front matter through that chapter as a *continuous reading experience* under six lenses: implementing engineer, enterprise architect, advanced student, security/assurance reviewer, SRE/operations engineer, and business owner. For each key concept record (1) first explanation, (2) current concise reminder or precise figure/table reference, (3) actual enforcement and authority, (4) CASE-204 identifier and state consistency, (5) supported claim/source, (6) negative test or evidence and owner, and (7) the **distinct new contribution** of the chapter. Technical checks do not certify comprehension; an actual editorial signoff remains mandatory.

| Review ID | Reader-visible risk | Resolved/controlled location | Open obligation |
|---|---|---|---|
| CCR-01 | E-domain versus C-contract conflation | Ch8 Tables 8.1/8.2; Ch18 §18.1; Appendix reference | Verify readers can distinguish responsibility, contract and deployment |
| CCR-02 | Printed reader relies on internal metadata/CAB | Front matter; Appendix contract map | Ch35 must publish detailed field-level contracts |
| CCR-03 | Advisory C04 correlation mistaken for financial operation RF-1042 | Ch8 §8.4, Ch11, Ch13, Ch18 and Appendix | Verify approved CAB-001 field naming in Chapter 35 schema review |
| CCR-04 | E7 workflow state confused with E8 business truth | Ch8 §8.3; Ch14; Ch15; Appendix | Ch26–28 reconciliation tests |
| CCR-05 | A/B/C alternatives mistaken for Part IV build stages | Ch17 §17.8 | Part IV introduction and Ch22–27 |
| CCR-06 | Key tables not navigable | Ch8 Tables 8.1–8.3 | Number future substantial architecture tables |
| CCR-07 | R-123 in Fig 2.3 interpreted as second CASE-204 refund | Ch2's explicit historical-example note | No change justified unless genuine reader confusion persists |
| CCR-08 | Claim-to-source proof overstated | Sources register and manuscript scope notes | Edition, page and latest-version verification pending |
| CCR-09 | Quality acronym RASR/RASER diverges | Intro and CAB quality definitions | Resolve against approved quality-attribute baseline before changing either |

**Acceptance policy:** unresolved protocol ambiguity is not a cosmetic editorial pass. A missing published contract is a publication dependency; a planned Chapter 35 cannot be cited as already delivered. Reject a chapter if important new identifiers are undefined, alternate designs are shown as a maturity sequence, permissions depend on model text, UNKNOWN becomes FAILED, or source claims lack matching support.

## Chapter 19 verified continuity extension (2026-11-13)

- **Tool discovery versus authority:** Ch10 §10.3 → Ch18 §18.3 → Ch19 §§19.1–19.3 and Figure 19.1; no registry/tool declaration grants E5 permission.
- **Adapter truth and operation identity:** Ch8 C04–C08, Ch11/13–15 → Ch19 §§19.4–19.5 and Figure 19.2; proposal correlation is not trusted RF-1042 or a provider key; UNKNOWN remains unresolved until evidence.
- **Negative-test chain:** Ch7 quality-attribute obligations, Ch13 bypass/fault tests → Ch19 §§19.6–19.7; destination controls, wrong-tenant reads, duplicate-effect behavior, provider status mapping and operator stop must be exercised.
- **Planned obligations:** Ch20 context/state/memory separation; Ch25–26 executable adapter/provider contracts; Ch28 effect recovery; Ch29 tool misuse; Ch31 end-state verification. Future destinations remain unverified until drafted.
- **Sources:** See Chapter 19 entries in references/source-register.md; exact edition/page audit is still open.

## Chapter 20 verified continuity extension (2026-11-13)

- **Memory classification:** Ch4/Ch12 §12.5 → Ch20 §§20.1–20.3, Figure 20.1. Ephemeral inference, derived case memory and organizational knowledge do not become E7 owner state or E8 business truth.
- **Freshness, privacy and revocation:** Ch9/Ch12 → Ch20 §§20.3–20.4. Source IDs and versions, tenant/case purpose, invalidation, correction, retention and revocation are distinct mechanisms; completed inference cannot be retroactively erased by revocation.
- **Durable recoverability:** Ch10/Ch15 → Ch20 §20.5, Figure 20.2. Ownership epochs and fenced E7 mutations survive worker replacement; RF-1042 remains unique and UNKNOWN is reconciled against E8 rather than inferred from agent memory.
- **Negative tests:** Ch20 §20.6 → Ch24 scoped-context fixture implementation, planned Ch26 reconciliation, Ch28 recovery, Ch29 threat tests, Ch31 end-state verification. These are acceptance obligations, not completed implementation proof.
- **Pinned credential compromise obligation:** Ch13/Ch19 credential-door/key distinction → planned Ch29 compromised agent token vs privileged provider credential threat analysis and Ch31 independent denial, containment and provider reconciliation tests; this work is not silently closed by Chapter 20.
- **Sources:** Chapter 20 source-register rows map citations to claims; exact text/edition page verification remains open.


## Chapter 21 verified continuity extension (2026-11-13)

- **Decision as enforceable contract:** Ch8 E1–E9 and C01–C09; Ch13 E5, Ch15 E7, Ch17 alternatives, Ch19 effect isolation, Ch20 information ownership → Ch21 §§21.1–21.4 and Figure 21.1. ADR-021 records a candidate decision, POL-021 records a proposed rule, but neither creates financial permission without independent E5/E6 enforcement.
- **Governance change lifecycle:** Ch7 release and evidence doctrine; Ch16 change/operations; Ch21 §21.5 and Figure 21.2. Approved rules, deployed digests, actual adapter privilege, release identity and rollback evidence must reconcile. No claim that an ADR, policy engine or dashboard is a control by itself.
- **CASE-204 invariant:** $500; Design B is conditional initial production candidate, A/C are alternatives; C04 advisory never mints RF-1042; E7 UNKNOWN cannot be upgraded without E8 reconciliation.
- **Negative test handoff:** Ch21 §21.6 G21-01–G21-07 → implemented Ch22–27 guarded teaching examples, Ch29 compromised-agent/privileged-provider distinction, Ch31 independent end-to-end assurance. Ch22–27 are now drafted and executable; Chapters 29 and 31 remain planned.
- **Source limitation:** Ch21 source-register mapping is claim-scoped; exact edition/page checks and Mac Word physical pagination are open.

## Holistic Parts I–III six-lens editorial review (2026-11-13)

See `metadata/parts-01-03-six-lens-audit.md` for the complete route map, citation evidence classifications, repetition and architectural drift review, and measured chapter pagination. This review supersedes any informal description of Parts I–III as *publication complete*. The parts are substantive development drafts until the identified page-budget exceptions, exact claim/source passage checks, and full-size native Word inspection are adjudicated.

**First-use rule:** Introduce E-domain/C-contract with its functional name the first time its specific authority matters in a part or chapter; after one concise explanation, identifiers suffice. Do not reprint the nine-by-nine catalog in every chapter. Part III's entry page serves as a self-contained functional refresher. If a reader must leave the chapter to establish the security meaning of an identifier, the prose is incomplete.

**Cross-part negative test:** A C04 advisory proposal (`operation_id` / `idempotency intent` permitted by CAB-001) cannot assign trusted `RF-1042`, establish E5 approval, reach provider credentials, or upgrade E7 UNKNOWN to CONFIRMED; E8 reconciliation and source evidence are required.

## Chapter 22 verified implementation trace (2026-11-13)

| Topic | Reading path | Executable evidence / remaining limitation |
|---|---|---|
| CASE-204, $500 and RF-1042 | Ch3 §3.9 → Ch8 §8.4 → Ch13–15 → Ch17 → Ch21 → Ch22 §§22.1, 22.3 | `build0/refund.py` fixed case, operation and 50000 cents; test stable identity; real policy fixture only |
| E1/E2 admission and ownership | Ch9–10 → Ch18 → Part IV opener → Ch22 §22.2 | Fixed principal/tenant and single controller; authentication and fencing **not implemented** |
| C04 advisory versus C05/C06 financial intent | Ch11/13 → Ch19/21 → Ch22 §§22.2–22.3 | No C03/C04 or E3/E4 at Build 0; proposal cannot mint operation identity |
| E5/E6 gate and adapter | Ch13–14 → Ch19/21 → Ch22 §§22.2–22.5 | `authorize`, `dispatch`, denial test; no production privilege isolation/credential custody |
| E7 versus E8, UNKNOWN | Ch15 → Ch20 → Ch22 §§22.3–22.5 | Two separate SQLite stores; lost-ack, no-redrive and reconciliation tests; no real provider assertions |
| Alternative A/B/C versus Build 0–5 | Ch3/17/21 → Part IV opener → Ch22 §§22.1, 22.7 | Build is a teaching sequence, C optional and B conditionally preferred |
| E9 verification and operations | Ch7/21 → Ch22 §§22.5–22.6 → Ch28–31 planned | 109 runnable Build 0–5 tests in the Chapter 27 working snapshot; native Word print, real provider contract, cross-site concurrency and source-page audit OPEN |

## Chapter 23 / Build 1 traceability

- E3/C04 bounded proposal: `build1/contracts.py`, `build1/advisory.py`, Chapter 23 §§23.2–23.4, F23-01 and F23-02.
- E1/E4 fixture scope/provenance: `WorkRequest`/`Evidence`, negative cross-tenant/stale tests, Chapter 23 §§23.3, 23.6. Protected variants deferred to Chapter 24.
- E5/E6 exclusion and E7/E8 no-write: `build1/test_advisory.py`, Chapter 23 §§23.5–23.6, F23-03. Shared-process limits explicitly documented; independent enforcement in Chapter 25.
- Valid-agent-token hijack regression: future Chapters 25, 29 and 31; Build 1 does not assert token enforcement.

## Chapter 24 / Build 2 continuity extension

| Obligation | Grounded implementation / manuscript | Remaining independent owner |
|---|---|---|
| E1/C01 simulated claim integrity versus authentication | Ch9/16/20 → Ch24 §§24.2–24.3; `build2/identity.py`; F24-01, F24-02; tamper/expiry tests | Enterprise E1 identity and protected verification, Ch25 boundary test |
| E4/C03 source, scope, classification and freshness | Ch12/20/23 → Ch24 §§24.4, 24.7; `build2/context.py`; F24-03; stale, cross-tenant, source denial tests | Real E4 access enforcement, source attestation, revocation, E9 audit |
| C04 remains untrusted, with no financial operation ID | Ch11/13/23 → Ch24 §§24.4–24.6; Build 1 unchanged, `build2/pipeline.py` adapter; no-write tests | Protected E5/E6 in Ch25; RF-1042 only trusted path |
| E7 knowledge, E8 business truth and UNKNOWN | Ch14–15/22 → Ch24 §§24.5–24.7; Build 0 tests unchanged | Provider contract and recovery Ch26, Ch28/31 |
| Design A/B/C not build maturity | Ch3/17/Part IV → Ch24 §§24.1, 24.9 | Evaluate net benefit rather than agent count |

All six reader lenses reviewed against CAB-001 terminology and the source-controlled companion. Native Word print and external source-to-claim verification remain publication gates, not completed assurance.

## Chapter 25 / Build 3 independent trusted request gate

- E1/C01 fixture token vs E5/C05 case-specific finance approval: Ch25 §§25.2–25.4, `build3/contracts.py`, `service.py`; F25-01, F25-03.
- Compromised **valid token** negative demonstration: Ch25 §§25.2, 25.6–25.7, `test_gate.py`, actual issuer/verifier assertion and absent E7/E8 databases. Ch29 and Ch31 must deepen threat assumptions and verification.
- E5/C05→E7/C06 local immutable RF-1042 and E6/C07→E8/C08 simulated external effect: Ch22/25, `build0/refund.py` invoked server-side; F25-02. UNKNOWN/reconciliation Ch26 remains open.
- E2 durable ownership, multi-worker leases, epochs/fencing intentionally absent until optional Ch27; real OS security and independent finance issuer not supplied by same-user fixture.
- Build 0–3 README `architecture.svg` figures map actual modules; no change to Designs A/B/C business alternatives.


## Chapter 26 / Build 4 — provider contract and reconciliation

| Obligation | Book/source evidence | Remaining production requirement |
|---|---|---|
| CASE-204 $500; stable RF-1042 | Ch26 §§26.1–26.3; `build4/provider_contracts.py`, `ledger.py`; F26-01/02 | Actual customer/payment identifiers and live authority |
| E5/C05 denies valid E1 token lacking finance approval | Ch25→26 §§26.2,26.6; `build4/service.py`, negative subprocess test | Independent E5 and finance issuer OS/credential isolation |
| E7/C06 intent and one dispatch claim | Ch26 §§26.3–26.4; `ledger.py`, replay tests | Durable outbox, E2 ownership fencing / multi-site failover |
| E6/C07 pinned provider semantics | Ch26 §§26.2,26.4; `provider_contracts.py`, `adapter.py`; F26-01 | Real provider contract, version, key scope/retention and failure tests |
| E8/C08 authoritative observation; UNKNOWN stays UNKNOWN absent proof | Ch26 §§26.5–26.6; `workflow.reconcile()`, conflict/status tests; F26-02/03 | Real provider lookup consistency, operator escalation, settlement provenance |
| Source-level architecture in companion README | `build4/architecture.svg`, `build4/README.md` | Actual deployment topology/security review and edition tag |
| Designs A/B/C remain alternatives | Ch3/17/22–26; Part IV intro | Measured benefit and risk-based design choice |

This mapping does not claim a production provider integration or an immutable external audit log; those remain open review gates.


## Chapter 27 / Build 5 — optional E2 coordination

| Obligation | Executable/manuscript evidence | Production assurance debt |
|---|---|---|
| E2/C02 durable work ownership | Ch27 §§27.2–27.4; `build5/coordinator.py`, F27-01/02 | Trusted multi-site store, service identities, clock/skew and failover semantics |
| Epoch fencing for E2 state | Ch27 §§27.3–27.5; `test_coordination.py` stale lease / racing owner tests | E5 MUST separately enforce current ownership for **end-to-end** effect fencing |
| One initial effect attempt and conservative handoff | Ch27 §§27.4–27.6; `runner.py` and crash-before-send tests | Durable E5/E7 acceptance protocol and operator recovery |
| E5/C05 independent finance authority | Ch25–27; real Build 4 E5 subprocess used by Build 5 demo | Independent issuer/key custody and identity isolation |
| E7/C06 operation and E6/E8/C07–C08 proof | Ch26–27; no re-execution after UNKNOWN, F27-02/03 | Real provider idempotency/lookup agreement and audited recovery |
| Companions and learning | `build5/README.md`, `architecture.svg`, tests and QA report | Print Word and real deployment certification remain open |

Build 5 is optional; Designs A/B/C remain alternatives and no C04 proposal can mint RF-1042.
