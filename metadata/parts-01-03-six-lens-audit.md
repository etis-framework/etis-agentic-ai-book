# ETIS Parts I–III — Holistic Six-Lens Editorial and Architecture Audit

**Review date:** 2026-11-13. **Reviewed artifact:** `etis-agentic-ai-book(20261113-195403).docx`, 345 pages rendered in LibreOffice, plus 21 chapter source files, front matter, Part I–III introductions, glossary, architectural appendix, source register, curated bibliography, CAB-001 and V12 ledger. **Status:** substantial development drafts; **NOT certified or frozen as publication-ready Parts I–III**.

## Executive disposition

**Architecture:** no demonstrated structural drift from the approved nine E-domains and nine C-contracts. CASE-204 stays a $500 requested refund; A/B/C are alternative investigation designs; B remains a conditional initial production candidate; C is read-only; the financial identity RF-1042 is assigned only after independent authorization; provider timeout is UNKNOWN until reconciled; E7 workflow facts are not E8 business truth; E2 logical ownership is fenced. The C04 advisory `operation_id` and `idempotency intent` are not financial authority or a provider key. CAB-001 remains the engineering reference, **not** a book readers must possess to understand a passage.

**Reader experience:** first-use identifier comprehension was uneven at the Part III entry and Chapters 18–20. This patch introduces a compact part-level E/C refresher, concise function names where they matter first, and explicit self-contained references in the opening of Chapters 18–20. It does **not** inflate all 21 chapters with duplicated definitions. Chapters 8 and 21 remain the full maps at their intended pedagogical moments, plus the reader-facing contract appendix.

**Evidence and citations:** 29 source records existed in `references/bibliography.bib` before this pass; all are curated identification records, not automatically exact passage proofs. This patch adds NIST SP 800-162 (official updated 2019 ABAC definition) at Chapter 21's policy-decision discussion, with matching bibliography and source register entries. External verification sampled NIST SP 800-207; Parasuraman et al. (2000); Anthropic (2024); OpenAI (2026); τ-bench (2024); OWASP agentic-applications edition (published 2025 for 2026); MCP 2026-07-28; and NIST SP 800-162. **Do not represent this sample as a full source-page or licensed-standard audit.**

**Page budget:** the uploaded 7×10 Word manuscript rendered to 345 pages in LibreOffice; **297 pages** are currently occupied by Chapters 1–21 versus the **280 V12 chapter-page allocation**. Part I is especially over budget. This review deliberately does not compress foundational chapters without a substantive editorial redesign. Mac Word is authoritative for final printing and may paginate differently; the measured exceptions must be resolved, consciously reallocated, or formally approved before certification.

## Actual rendered page accounting (source-independent)

Document page positions were extracted from the supplied Word file after rendering to PDF for page-boundary measurement; a chapter's count ends at the next chapter heading. Introductory Part I–III pages and front/back support are excluded from this chapter-only accounting. These figures are **not** native Mac Word results.

| Chapter | Title | Observed pages | V12 allocation | Variance |
|---:|---|---:|---:|---:|
| 1 | Why Enterprise Agentic AI Needs Engineering | 17 | 15 | +2 |
| 2 | A History of Automation, AI, and Enterprise Systems | 24 | 18 | +6 |
| 3 | Enterprise Processes, Goals, and Bounded Autonomy | 20 | 15 | +5 |
| 4 | What an Agent Is—and Is Not | 14 | 12 | +2 |
| 5 | Business Cases, Value, and Lifecycle Economics | 11 | 11 | +0 |
| 6 | Uncertainty, Authority, and Enterprise Trust | 11 | 12 | -1 |
| 7 | Engineering Principles and Requirements | 16 | 12 | +4 |
| 8 | From Requirements to a Reference Architecture | 15 | 12 | +3 |
| 9 | Admission, Identity, and Scoped Work | 12 | 13 | -1 |
| 10 | Coordination, Registry, and Ownership | 14 | 14 | +0 |
| 11 | Agent Reasoning and Proposal Contracts | 13 | 14 | -1 |
| 12 | Context, Retrieval, and Memory | 13 | 14 | -1 |
| 13 | Trusted Execution and Authority | 14 | 15 | -1 |
| 14 | Enterprise Integration and Business Truth | 13 | 14 | -1 |
| 15 | Durable Operational State and Assurance | 12 | 14 | -2 |
| 16 | Trust Boundaries and Deployment Views | 16 | 13 | +3 |
| 17 | Choosing Deterministic, Agentic, and Hybrid Designs | 12 | 12 | +0 |
| 18 | Coordination and Delegation Patterns | 15 | 12 | +3 |
| 19 | Tools, Adapters, and Effect Isolation | 12 | 13 | -1 |
| 20 | State, Memory, and Knowledge Design | 11 | 13 | -2 |
| 21 | Architecture Decisions and Governance as Code | 12 | 12 | +0 |

| Part | Observed chapter pages | V12 chapter allocation | Variance |
|---|---:|---:|---:|
| I (1–7) | 113 | 95 | +18 |
| II (8–16) | 122 | 123 | -1 |
| III (17–21) | 62 | 62 | 0 |
| **Total (1–21)** | **297** | **280** | **+17** |

Part II and III aggregate alignment does **not** erase individual overages: Chapter 8 (+3), Chapter 16 (+3), and Chapter 18 (+3). Part I's largest deviations are Chapter 2 (+6), Chapter 3 (+5), and Chapter 7 (+4). Pages for the index, final references, actual illustration and caption spacing, and Chapters 22–36 are not resolved by this accounting. A 550-page final book cannot be certified by source word limits alone.

## Cumulative chapter-by-chapter narrative trajectory

| Ch. | Distinct contribution | Continuity/control checkpoint | Editorial / citation action |
|---|---|---|---|
| 1 | System rather than model is unit of trust; introductory case | Proposal ≠ permission ≠ effect | Strong orientation; +2 pages; test book's value proposition against Ch3 and Ch6 for repetitiveness |
| 2 | Historic transactions, workflows, search, distributed failure | R-123 diagram explicitly separate from RF-1042 | Broad but longest deviation (+6); condense before print, preserve historical sources and technical caveats |
| 3 | Business goals, delegation envelope, A/B/C decision | Design B is conditional, not outcome of an autonomy ladder | +5 pages; verify separate examples and avoid re-explaining Ch1's setup |
| 4 | Agent defined independently of LLM; bounded loop | No agent-issued payment authority | Source coverage appropriate for classical definition and modern vendor practices; +2 pages |
| 5 | Lifecycle business value and cost per acceptable completion | Avoid cost per model call as final metric | Meets current pages; numerical examples expressly illustrative |
| 6 | Uncertainty, authority, ethical/organizational trust | UNKNOWN cannot be reasoned into failure | Reinforces Ch2's distributed failure for a different purpose; avoid verbatim reiteration |
| 7 | Measurable requirements and evidence chains | AUTH/POL/DATA/PAY/OPS link to Ch8 | +4 pages; consolidate duplicate examples during print trim without losing acceptance criteria |
| 8 | One integrated E1–E9/C01–C09 reference architecture | Nine logical responsibilities ≠ nine services | Primary reference table appropriate; +3 pages must be adjudicated |
| 9 | Admission/authenticated delegation (E1) | Admission ≠ business/payment authorization | Good local identifier definitions and identity roles |
| 10 | Coordinator/registry and fenced owner (E2) | Registry ≠ permission; one logical owner | Technical implementation explanations belong here, not repeated in Ch18 |
| 11 | Advisory E3 schemas and proposed correlation | C04 fields ≠ RF-1042 | Explicit boundary is essential; do not remove approved C04 identifiers |
| 12 | Scope/provenance/limitations of E4 retrieval | Retrieved policy ≠ current entitlement | Ch20 should compare design options rather than repeat detailed retrieval contracts |
| 13 | E5 independent execution, credentials, authority | Key/token ≠ transaction-specific permission | Strong core; pending complete credential compromise negative-test in Ch29/31 |
| 14 | E6 provider adapter versus E8 business truth | External effect not inferred from HTTP success | Provider-specific promises must stay conditional |
| 15 | E7 durable state and E9 assurance | Fenced ownership/UNKNOWN and reconciliation | Reinforces not relocates financial truth; no extra general state engine |
| 16 | Physical deployment tradeoffs | Risk-based isolation without nine services | +3 pages; test diagrams and discussion for duplicate placement views |
| 17 | A/B/C decisions and economics | Alternatives are not implementation build stages | E7/E9 first-use clues okay; part-level refresher improves standalone reading |
| 18 | Coordination, specialism, hub/peer and recovery | E2 owner survives worker replacement; E5 gate independent | Now self-contained functional E labels; +3 pages needs chapter-page review |
| 19 | Tool/adapter contracts and effect isolation | E5/E6 authorizes, E8 reconciles, no blind retry | First important E2/E5–E8 references now named in prose |
| 20 | Ephemeral context, derived memory, E7 versus E8 | Memory never mints RF-1042 or upgrades UNKNOWN | First use named, preserves distinct Chapter 12 versus 20 purpose |
| 21 | ADR, policy-as-code, protected enforcement and evidence | Versioned policy ≠ real control; denial and rollback evidence | Nine-domain/contract map already in V2; adds NIST ABAC source for attributes |

## Six independent reading lenses

### 1. Implementing engineer — buildable explanation, then constraints
**Route:** Chapters 1, 3–4, 7 → 8 → 9–15 → 17–21 → planned 22–27. Reader must understand why every field in a proposal differs from an authorized operation, why E7 tracks RF-1042 while E8 owns financial truth, and how provider semantics affect retries. **Pass:** source chapters distinguish contracts, owners, versioning, and failure modes without equating a diagram with executable guarantees. **Risk:** practical field-level C01–C09 schemas and testable implementation remain future Chapter 35 and Part IV work; do not call those delivered. **Action:** first-use labels and Part III compact refresher.

### 2. Enterprise architect — quality attributes and independent design axes
**Route:** 2, 5–8 → 10, 13–16 → 17–21. Reader must distinguish responsibility, contract, and deployment, then evaluate generalist/specialist, hub/peer, deterministic/advisory/bounded, and risk-proportional isolation as **independent decisions**. **Pass:** no architectural service-count or agent-count mandate; Design B remains conditional; Part IV build stages explicitly distinct. **Risk:** Chapter 16 and 18 page excess; Chapter 21 ADR is a pedagogical sketch, not an approved enterprise implementation. **Action:** preserve design axes in Part III opening and chapter 18, avoid reprinting the catalog.

### 3. Advanced student — terminology and progressive conceptual load
**Route:** 1–7 sequentially → 8 (both maps) → each Chapter 9–16 named-domain treatment → Part III named refresher → 17–21. **Pass:** agent/model distinction and proposal/permission/effect separation are introduced conceptually before E/C identifiers. **Risk:** sections in later parts had first-use naked E labels that forced page flipping; multiple repetitions of the $500 case and system-not-model thesis can become tiresome. **Action:** localized reminders, not nine-by-nine tables in every chapter; Chapter 8 and Part III intro act as anchor locations.

### 4. Security / independent assurance reviewer — enforcement bypass, provenance, and claims
**Route:** 3, 6–9 → 11–16 → 18–21 → planned 29,31,32. **Pass:** proposal and context are untrusted for authorization; E5 is an independent gate; E4 applies tenant/purpose controls; E6 credentials are protected; C04 correlation is not trusted operation identity. **Risk:** test case for compromised investigator token versus privileged provider secret is a P29/P31 obligation, not existing proof. **Action:** maintain exact token/authority distinction and typed denial evidence; ABAC citation supports general attribute evaluation, not ETIS specifics.

### 5. SRE / operations reviewer — failure, recoverability, containability
**Route:** 1–2, 6–7 → 10, 14–16 → 18–21 → planned 26,28,30–31. **Pass:** external timeouts produce UNKNOWN; E2 ownership is replaceable but logically unique; E7 preserves authoritative local operation state; E8 reconciliation resolves external outcomes. **Risk:** provider-specific retention and status guarantees, actual runbooks, canary/rollback evidence and exercise logs are still to be built. **Action:** reference the decisive local section instead of repeating the full lost-acknowledgment scenario in each chapter.

### 6. Business owner / risk authority — value, accountability and recourse
**Route:** 1, 3, 5–7 → 8, 13–15 → 17, 21 → planned 32–34. **Pass:** comparisons use complete workflow cost and human consequences; unauthorized refund is a governance failure even when the model's answer is persuasive; original case conditions remain stable. **Risk:** Design B selection is illustrative and conditional—not backed by measured retail case outcomes; launch ROI, fairness/appeal and signed residual-risk acceptance are not complete. **Action:** keep hypothesis language explicit, avoid presenting governance documents as enforced controls.

## Repetition review: reinforce only when a new engineering burden is introduced

**Intentional reinforcement to retain:** proposal ≠ permission (Part I principle, Part II authority contract, Part III effect/policy gate); UNKNOWN ≠ FAILED (historical failure, E7 state design, adapter contract, governance evidence); A/B/C alternatives (each part's decision checkpoint). These are *invariant reminders*, not three independently developed architectures.

**Potential compression during page-budget reconciliation:** Chapter 2's late governance and data subsections versus Chapter 3/7 foundations; Chapter 3's second full worked design and exercises versus Ch1 case; Chapter 7 repeated examples; Chapter 16's multiple isolation views; Chapter 18 repeated full E-map/identifier explanations. Shorten recap text, not protected boundary semantics or negative-test obligations.

**Do not shorten away:** E5-versus-E3 trust distinction, C04 advisory identity versus RF-1042, E7/E8 truth, provider uncertain status, human oversight accountability, source provenance, and formal acceptance tests.

## Citation and bibliography review

- The manuscript uses descriptive author–year attributions. Primary works (Lamport, Garcia-Molina/Salem, Parasuraman et al., Lewis et al., Yao et al.) support specific historical or research ideas, **not** payment-provider semantics. NIST guidance supports governance and security concepts but does not approve the ETIS architecture. FinOps sources and Anthropic/OpenAI guidance are living or vendor sources, not empirical guarantees.
- `references/bibliography.bib`, the reader-facing bibliography, and `references/source-register.md` now include NIST SP 800-162 (updated 2019) for Chapter 21's attribute-based policy evaluation. Official NIST publication record verifies its scope: subject, object/resource, requested operation and environmental context, evaluated against policy. A full normative text/section verification remains open.
- The source register explicitly tracks edition/page and licensed-standard limitations; this is proper editorial transparency, **not an acceptable final-book substitute**. Before publication, every substantive historical priority, quoted standard, behavior claim and provider guarantee must have an edition, page/section or stable specification anchor and should be checked against the primary text.
- Official external checks during this pass: NIST SP 800-207 2020; NIST SP 800-162 updated 2019; Parasuraman et al. IEEE DOI; Anthropic Engineering 2024; OpenAI guide Jan 2026; Yao et al. τ-bench arXiv:2406.12045; OWASP Top 10 Agentic Applications 2026 (published Dec 2025); Model Context Protocol July 28, 2026. **These checks identify publications and general claim scope only.**
- Remaining gaps: full claim-to-page certification for all 21 chapters, fixed OWASP snapshot per citation, exact licensed ISO wording, and provider/implementation references when Part IV specifies a real adapter. Avoid making a retrospective citation audit sound like a comprehensive current survey.

## Figures and manuscript-format finding

The uploaded DOCX has 57 embedded images, corresponding to the 57 manuscript figure references in current automated checks; figure counts alone **do not** certify print readability. The prior Figure 20.1 label-size failure demonstrates why local 7×10 visual inspection matters. This audit inspects the provided page-content and placement record, but does not claim line-by-line publication visual certification of all 345 pages. Inspect each embedded figure, caption, multicolumn table and code block in native Word for Mac; stop on clipped connector labels, misleading flow arrows, orphaned table fragments, and unreadable footnotes.

## Acceptance dispositions and actionable queue

| Priority | Issue | Current disposition | Required closure evidence |
|---|---|---|---|
| P0 | Native print-page excess in Part I and Ch8/16/18 | OPEN | Mac Word confirmed chapter/page ledger; approve reallocations or targeted reductions |
| P0 | Source-rebuilt DOCX pagination differs materially from uploaded Word | OPEN | Restore/verify production style parity before accepting rebuilt page counts |
| P0 | Exact citation-to-claim proof for externally sourced/standards text | OPEN | Claim-level passages, edition/section, URL/DOI, reviewed source register |
| P0 | Reader dependency on private CAB-001 for finished explanation | PARTLY FIXED | Reader-facing Chapter 8 and Appendix self-sufficient; detailed field schemas published by Ch35 |
| P1 | Part III early E/C references cryptic to non-linear readers | PATCHED | Built book shows names within Part III entry and first substantive Chapter 18–20 use |
| P1 | Figure QA beyond structural checks | OPEN | Native Mac Word full-size review, especially F18/F20/F21 |
| P1 | Full-book repetition/flow, Part IV boundary | REVIEWED | Additional technical editorial read after Part IV develops executable proofs |
| P1 | RASR/RASER acronym equivalence in historical baselines | OPEN | Resolve quality-attribute acronym against approved CAB/series documentation; avoid mechanical renaming |
| P2 | Future Ch29/31 credential theft negative tests | PINNED | Distinguish agent access token from privileged provider secret; denial/containment/reconciliation evidence |
| P2 | Final author, ISBN, rights and publication metadata | OPEN | Publisher-approved front matter |

**Build parity warning:** The audited user-supplied Word document renders to **345** pages in the local LibreOffice measurement. The reconstructed source-based `make book-docx` output renders to **273** pages in the same engine, despite matching 1,676 body paragraphs, 47 tables, 57 embedded images and 7×10 geometry. Their style inventories differ (uploaded Word: 81 styles; reconstructed build: 70, with different heading-style definitions). Consequently the reconstructed build is useful for structural and figure-fingerprint QA but **not** an interchangeable pagination baseline. Do not substitute its 273-page count for the user's 345-page submission or certify the book budget by extrapolating that count. The production builder/style preservation needs a separate diagnosis before publication. The reported 297 chapter pages are derived solely from the supplied 345-page file.

**Sign-off rule:** Passing `make check`, citation key matching, or the six-lens *editorial* review is insufficient to freeze Parts I–III. Require explicit approval of unresolved P0/P1 items and a native Word page ledger. This patch changes reader wording, source records, and audit gates but does **not** assert completion of future chapters or source certifications.
