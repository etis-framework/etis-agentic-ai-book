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
- **Negative tests:** Ch20 §20.6 → planned Ch24 context implementation, Ch26 reconciliation, Ch28 recovery, Ch29 threat tests, Ch31 end-state verification. These are acceptance obligations, not completed implementation proof.
- **Pinned credential compromise obligation:** Ch13/Ch19 credential-door/key distinction → planned Ch29 compromised agent token vs privileged provider credential threat analysis and Ch31 independent denial, containment and provider reconciliation tests; this work is not silently closed by Chapter 20.
- **Sources:** Chapter 20 source-register rows map citations to claims; exact text/edition page verification remains open.
