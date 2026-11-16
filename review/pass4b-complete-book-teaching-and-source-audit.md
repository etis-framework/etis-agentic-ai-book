# Pass 4B — Independent complete-book technical, industry and teaching audit

**Baseline:** the user-supplied `ETIS_PASS4_BASELINE.tar.gz`, with the already-developed Pass 4 guarded amendments applied as the pre-Pass-4B source. The original archive contains no `.git`; GitHub merge SHA is not independently verified in this container. Patch installer must compare exact per-file SHA-256 content against that effective baseline.

**Disposition:** educational/documentation and protocol-source amendments proposed; **not a print certification or production deployment certification**. This is an internal seven-perspective, eight-path adversarial review supported by programmatic checks and executable source, not seven independent outside people reading the manuscript.

## 1. Every chapter: purpose, continuity, and testable boundary

All 36 chapter files were inventoried and checked for structure, source/figure references, baseline identifiers and editorial drift; representative critical sections were read in detail. The coverage row shows the exact chapter involved and the principal engineering obligation tested. It does **not** claim a complete sentence-level independent factual proof for every paragraph.

| Chapter | Main thread and independent challenge |
|---|---|
| Chapter 1 — Why Enterprise Agentic AI Needs Engineering | System ≠ model; consequential-effect definition; CASE-204 introductions |
| Chapter 2 — A History of Automation, AI, and Enterprise Systems | Transaction, workflow, distributed-state inheritance and source attribution |
| Chapter 3 — Enterprise Processes, Goals, and Bounded Autonomy | Business delegation, A/B/C alternatives, scoped authority |
| Chapter 4 — What an Agent Is—and Is Not | Agent versus model/workflow; bounded loop and stop conditions |
| Chapter 5 — Business Cases, Value, and Lifecycle Economics | Business value and lifecycle economics, not inference cost alone |
| Chapter 6 — Uncertainty, Authority, and Enterprise Trust | Authority, uncertainty and enterprise trust |
| Chapter 7 — Engineering Principles and Requirements | Testable requirements and operational/economic quality attributes |
| Chapter 8 — From Requirements to a Reference Architecture | One reference architecture and C01–C09 contracts |
| Chapter 9 — Admission, Identity, and Scoped Work (E1) | E1 identity, scope, purpose, credential limitations |
| Chapter 10 — Coordination, Registry, and Ownership (E2) | E2 ownership and registry versus authorization |
| Chapter 11 — Agent Reasoning and Proposal Contracts (E3) | E3 advisory schema cannot mint trusted financial identity |
| Chapter 12 — Context, Retrieval, and Memory (E4) | E4 context construction, stale/poisoned memory and provenance |
| Chapter 13 — Trusted Execution and Authority (E5) | E5 independent approval and effect gate |
| Chapter 14 — Enterprise Integration and Business Truth (E6/E8) | E6 adapters; E8 external business truth |
| Chapter 15 — Durable Operational State and Assurance (E7/E9) | E7 durable intent; E9 evidence, UNKNOWN state |
| Chapter 16 — Trust Boundaries and Deployment Views | Logical deployment/trust boundaries and operating tradeoffs |
| Chapter 17 — Choosing Deterministic, Agentic, and Hybrid Designs | A/B/C selection; simplest adequate mechanism |
| Chapter 18 — Coordination and Delegation Patterns | Worker delegation and coordinator ownership, not peer free-for-all |
| Chapter 19 — Tools, Adapters, and Effect Isolation | Tool adapters plus MCP/A2A; no protocol-derived business approval |
| Chapter 20 — State, Memory, and Knowledge Design | Ephemeral memory, persistent derived state and correction lifecycle |
| Chapter 21 — Architecture Decisions and Governance as Code | Architecture/governance decisions require execution evidence |
| Chapter 22 — Build 0: Deterministic Refund Baseline | Build 0 fixed deterministic/refund workflow |
| Chapter 23 — Build 1: Bounded Advisory Reasoning | Build 1 typed review-only proposal and denied forged permissions |
| Chapter 24 — Build 2: Scoped Context and Identity | Build 2 identity and context fixture scope/freshness |
| Chapter 25 — Build 3: Trusted Consequential Execution | Build 3 independent signed finance grant and subprocess limitations |
| Chapter 26 — Build 4: Provider Integration and Reconciliation | Build 4 provider contract and original-operation reconciliation |
| Chapter 27 — Build 5: Optional Coordination and Production Hardening | Build 5 E2 lease fencing; absence of E5-side fencing |
| Chapter 28 — Distributed Failure and Recoverable Effects | Distributed failure classes and ambiguous effect resolution |
| Chapter 29 — Security and Adversarial Agent Behavior | Compromised valid-token investigator cannot authorize refund |
| Chapter 30 — Reliability, Observability, and Incident Response | Read-only incident observer; credible stop and escalation limits |
| Chapter 31 — Verification, Evaluation, and Evidence | Claim/falsifier matrix, 7-method collector, long-horizon evidence boundaries |
| Chapter 32 — Human Oversight and Accountable Governance | Accountable review owners and human stop/restore authority |
| Chapter 33 — Release Engineering and Operational Readiness | Release gates, progressive rollout and changing-agent controls |
| Chapter 34 — Economics, Risk, and Lifecycle Decisions | Cost per acceptable workflow and risk-adjusted economic decisions |
| Chapter 35 — Contracts, Schemas, and Reference Artifacts | Runnable/spec-only contracts, schemas and evidence crosswalk |
| Chapter 36 — Exercises, Reviews, and Adoption Roadmap | Professional scenarios, adoption/retirement and final assurance decision |

## 2. Seven internal perspectives — adversarial dispositions

| Internal lens | Hardest challenge | Evidence inspected / observed disposition | Residual limitation |
|---|---|---|---|
| Implementing engineer | Can source, call boundaries, test and errors be learned without guessing? | All ten README/test directories and six source diagrams; added `LEARNING_PATH.md`, with actual method links and three guided failure labs | Fixture comments are instructional, not production security design |
| Enterprise architect | Does the book introduce competing control planes or imply nine services? | E1–E9/C01–C09 and Ch8–21/35 mapping; no new architecture or module added | Real ownership/privilege/latency tradeoffs remain deployment-specific |
| Advanced student | Is each step predictable, executable, falsifiable and explainable? | Added predict/draw/trace/run/falsify/compare/defend sequence and evidence packet; tests name the intended failure | No statistical model evaluation dataset or integrated live agent runtime |
| Security and assurance | Can an agent holding a valid E1 token generate RF-1042 or forge E5 grant? | Build3 `execute` checks signed case-specific grant separately; Ch29 harness verifies negative/positive controls | Same-UID fixture, public educational keys, no independently protected audit or live secrets |
| SRE / operations | Does a lost acknowledgment become a new refund or false FAILED? | Build4 `execute/reconcile`, Build5 `runner.step`, operations/read-only evidence, Ch28–33 | Provider settlement, E5-side owner-epoch fencing and operational readiness are unproven externally |
| Business owner | Is the ROI denominator meaningful and are approval duties explicit? | Ch5/34 unit economics, Ch32 human review/Ch33 release; FinOps unit economics supports a general concept | All CASE-204 values and economic effects are hypothetical |
| State-of-the-art / industry | Are context engineering, persistent-memory attacks, trajectories, MCP/A2A and identity treated without trend-chasing? | Ch12/19/20/31/33 revised in Pass 4, official MCP/A2A spec/OWASP/NIST source metadata checked; no new framework dependency | No protocol conformance, continuous-agent evaluation, multimodal runtime, or autonomous self-change implementation |

**Cross-lens invariant:** E3 proposals and E4 context are untrusted for financial authorization; E5 alone enforces trusted consequential permission, E7 records durable intent, E8 is external truth, E2 coordinates but does not grant finance authority, E9 captures review evidence. A/B/C are alternatives; Builds 0–5 are teaching checkpoints. UNKNOWN cannot become FAILED merely because a network request timed out. 

## 3. Eight selective entry paths

| Path | Reading entry | Companion falsifier | Outcome and limitation |
|---|---|---|---|
| Architecture-first | Ch8→Ch9–16→Ch17–21→Ch35 | `IMPLEMENTATION_EVIDENCE_MAP.md` and Build3/4 trust boundary tests | Contract map coherent; not nine physical microservices |
| Build-first | Ch22–27→Appendix B→new `LEARNING_PATH.md` | Build0 lost-ack, Build1 forged-field, Build2 stale-source, Build3 valid-token tests | Progressive units runnable, **not** one integrated adaptive+financial runtime |
| Security-first | Ch9/13/19→Ch25/29→Ch31/32 | `security/test_adversarial_cases.py` valid-token denial | Authorization separate from identity; credentials not OS-protected |
| Reliability-first | Ch15/26→Ch28/30/33 | Build4 status lookup and `reliability/test_recovery_cases.py` | Unknown effect never blithely retried |
| Governance-first | Ch21/29→Ch32/33→Ch36 | Ch29 E5 denial/Ch31 scoped assurance | Release approval is not finance approval |
| Economics-first | Ch5/17→Ch34/36 | Hypothetical outcomes against observed test boundaries | Lifecycle denominator meaningful; no measured business ROI |
| Teaching-first | Ch1–4→Ch22–27→Ch31/35/36 | Three new educational source walkthroughs, named negative tests | Reproducible lessons; no invented agent/memory/model evaluation implementation |
| CASE-204/RF-1042 trace | Ch3/8→Ch11–15→Ch22–29→Ch31–36 | Build3 trusted RF-1042 creation and Build4 reconciler | Same $500 case and stable operation preserved |

## 4. Code and learning evidence

- Reviewed Python source/module listings in all six builds plus four QA fixtures, including the core E1/E4, E5, E7/E8, E2 and evidence-collector paths. Existing class/method-level docstrings are generally adequate for responsibility discovery, but the prior reader sequence relied on too many disconnected READMEs. **Corrected** with `LEARNING_PATH.md` and source-root/Appendix B navigation.
- Added only nonfunctional comments to `build2/context.py`, `build3/service.py`, `build4/workflow.py`, and `build5/runner.py`; no control behavior, schema, API, or trust boundary was changed. All six build SVGs were retained, because the module architecture is unchanged.
- The new checker verifies every guide-linked exact test method, each build diagram's XML, the six README checkpoints, security/recovery/operations/assurance tests, bibliography protocol URLs, and the non-composition/non-guarantee boundaries. A **source-linked walkthrough is not itself a new runtime test**.
- Existing assurance collector runs seven named methods and never grants general evidence certification; future longitudinal statistical evaluation is a real external dataset/operations obligation.

## 5. External citation audit — verified scope versus outstanding verification

| Source class | Verification in this pass | What the citation may support | What it cannot establish |
|---|---|---|---|
| MCP 2026-07-28 normative specification | Official dated specification page and protocol actors/tools; bibliography and BibTeX synchronized to specification, not release blog | Tool/resource integration protocol and transport-layer obligations | CASE-204 finance authorization or ISO/enterprise compliance |
| A2A released 1.0 specification | Official specification destination and protocol description checked; replaced promotional release announcement citation | Agent discovery, cross-agent task exchange, versioned interactions | Verified peer identity or entitlement to issue refund; version 1.0.0 pinned |
| OWASP Top 10 for Agentic Applications 2026 | Official resource dated Dec 9, 2025 | Threat categories and mitigation starting point | Security certification of fixture or precise E5 guarantees |
| NIST AI Agent Standards Initiative, Feb 17 2026 | Official NIST announcement checked | Current industry standards focus on interoperability/security/identity | A normative agent design standard or NIST endorsement of ETIS |
| Anthropic *Building effective agents* | Official Dec 19, 2024 article metadata checked | Engineering approaches and simplicity/evaluation tradeoffs | Production assurance for any particular implementation |
| OpenAI *A Practical Guide to Building Agents* | Official OpenAI listing checked, January 15, 2026 | Vendor implementation patterns, bounded tools and oversight examples | Certification of ETIS controls or an enterprise-specific external effect |
| FinOps Unit Economics | Foundation official capability guidance checked | Relating technology cost to attributable business units | Measured ETIS refund ROI or a guaranteed metric definition |
| NIST AI RMF/800-series, ISO/IEC, books, RFC 9110, papers | Bibliography and source-register mapping retained; RFC 9110's HTTP-method scope stated | General research, reliability, governance, architecture principles at claim-specific scope | Full licensed normative clause/page proof; payment-provider guarantees or independent audit acceptance |

**Citation audit verdict:** No verified public protocol source has been used as proof of actual payment authorization or settlement. The original ETIS architectural prescriptions are presented as such. The complete page-level verification of *all* historical, licensed, vendor and research citations remains an explicit publication source gate; this patch does not falsify that completion status. All newly changed external bibliographic records are mirrored in `references/bibliography.bib` and the source register.

## 6. Severity-ranked findings and patch closure

| Finding | Severity | Observed condition | Patch disposition |
|---|---|---|---|
| P4B-01 | Major (teaching) | Reader source path fragmented; code is readable but learners must assemble E1→E5→E7/E8 across independent demos themselves | **Corrected:** guided call paths, negative exercises, evidence packet and root/Appendix B navigation |
| P4B-02 | Moderate (readability) | Critical freshness, E5 authority, durable dispatch and E2 epoch limitations understandable from code but not consistently explained inline | **Corrected:** focused comments at exact branches, no behavior change |
| P4B-03 | Major (source quality) | Bibliography relied on MCP/A2A release announcements, which do not contain the normative full contract | **Corrected:** link normative specifications in reader bibliography/BibTeX and register version limitations |
| P4B-04 | Moderate (QA) | No executable checker protected source-to-test locators in educational walkthrough | **Corrected:** `check_pass4_teaching_and_sources.py` integrated into `make check` |
| P4B-05 | Publication blocking | Exact Word-for-Mac 7×10 page parity, final contents/index locators and all figure/table print inspection remain open | **Not changed:** Pass 5 print gate |
| P4B-06 | Source blocking | Complete edition/page verification for 32+ research/standards references and permissions remains open | **Not changed:** claim-specific source verification; do not assert all complete |
| P4B-07 | Production limitation | E5 has no current E2 owner-epoch enforcement; protected credentials, real provider status and immutable audit absent | **Not changed and disclosed:** no fictional Build 6 |
| P4B-08 | Release blocking | Print ISBNs, cover/spine, edition tag and retail-source handoff unassigned | **Not changed:** release pass |

**Hold conditions:** Any unresolved material authorization bypass, wrong operation identity, invented production claim, unverified source-specific legal assertion, broken companion locator, or false QA pass is a blocker. No new critical architecture drift was identified by the source-based review; that is not equivalent to proving the absence of defects in every future deployment.

## 7. Engineering publication and page budget

The reference architecture and six builds remain stable; technical chapter prose was not expanded in this patch. The only reader-facing manuscript change is a brief Appendix B pointer to the companion teaching guide and protocol bibliography refinement. This should not materially affect V12 chapter allocations, but the authoritative physical page count is determined only by native Word-for-Mac print proof. No chapter's finished-page allocation was silently altered. Source-generated pagination continues to require the final field-refresh and locator proof.

## 8. Next release gates

1. Run entire `make check`, `make book-docx` and `make check-figures` against the guarded patch; record actual counts and checks, including the new educational check.
2. Merge to protected `main` after local checks; preserve baseline SHA and verify branch cleanliness.
3. Pass 5: regenerate exact 7×10 Word/PDF, reconcile page counts, update TOC/index Roman/Arabic fields, inspect every figure/table in final print placement.
4. Verify exact cited source editions/pages, licensed ISO clauses and permissions before claims are locked; replace the A2A version 1.0.0 source if a later edition is adopted.
5. Pass 6: ISBNs, printing details, spine/cover, tagged immutable companion revision and final release decision.

## 9. Actual execution evidence — November 16, 2026

| Command or test | Observed result | Caveat |
|---|---|---|
| `make check` (final Pass 4B source) | **Exit 0**, complete uninterrupted run | Executes static gates and bounded local Python fixtures, not a live provider |
| Ten unittest suites: Build 0–5, reliability, security, operations, assurance | **153 of 153 passed** (16 + 15 + 13 + 18 + 27 + 22 + 10 + 6 + 14 + 12) | Tests are deterministic fixtures and simulated effects |
| `make book-docx` | **Exit 0**; full-book DOCX generated | Page fields, trim-size rendering and print proof require Word for Mac |
| `make check-figures` | **Exit 0**; 99 manuscript image references resolved | Automated existence checks do not replace visual inspection of actual physical pages |
| New guide/source acceptance | **Exit 0**, zero findings; all nine exact method locators resolve to real test definitions | Does not prove pedagogical effectiveness in a classroom |
| Guarded installer | SHA-256 preflight and actual application tested on **both** complete baseline modes; replacements matched hashes | Git SHA cannot be reconstructed because uploaded archive omitted `.git` |

These observations were produced against the extracted source and patched files in the execution environment. They do **not** certify source-page references, licensed standards, actual enterprise provider behavior, protected credentials/audit, or the final 7×10 physical volume.
