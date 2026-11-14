# ETIS Parts I–V End-to-End War-Game and Companion Assurance Review

**Baseline:** `da8c31501a6cb3f83bc0caf4719f15bd11042be2` (`main`, clean according to the supplied Git-state export).  
**Authoritative input:** `ETIS_CH28_FINAL_END_TO_END_WARGAME.tar.gz` and `ETIS_CH28_FINAL_GIT_STATE.txt`, supplied 14 November 2026.  
**Scope:** front matter, Parts I–IV/Chapters 1–27, Part V opener/Chapter 28, planned Chapters 29–36 for handoff correctness, back matter, CAB-001 catalog and contract map, figures, all six runnable Builds 0–5, the separate Chapter 28 recovery fixture, source/module README diagrams, publication scripts, source registers, index, glossary, and V12 budget.  
**Disposition:** targeted corrective patch prepared; no new executable effectful capability authorized. **Final full-book native Word and reference-pass gates remain open.**

## Executive findings and disposition

| ID | Severity | Observed evidence | Action / disposition |
|---|---|---|---|
| WG-01 | Medium, QA robustness | `make check` stopped in `check_code_listing_layout.py` when the uploaded Mac-generated archive contained non-UTF-8 AppleDouble `._*.md` data among manuscript Markdown glob results | Filter AppleDouble/`__MACOSX` metadata from the manuscript fence scan. Rechecked: 7 source code fences passed. No real Markdown files are skipped. |
| WG-02 | Medium, reader/assurance navigation | Existing tests for Ch28–31-relevant failures and adversarial denial are distributed across seven test directories, with no concise *named-test* cross-chapter handoff identifying exactly what they do **not** establish | Add `ASSURANCE_HANDOFF_CH28_CH31.md`, link from root companion README, `TESTING.md`, implementation evidence map; guard 18 real unittest names using AST in `check_assurance_handoff.py`, wired into `make check` |
| WG-03 | Low, documentation navigation | Companion README directory tree omitted `reliability/` and had inconsistent Build 4/5 tree indentation | Correct diagram/tree presentation without altering source modules |
| WG-04 | Low, metadata drift | Figure register retained an earlier narrow description for updated layered F28-01; historical topic traceability still described original Part III planning state | Align Chapter 28 register descriptions; add explicitly dated/conditional Chapters 28–31 handoff status and source-register entry |
| WG-05 | High, **production readiness** (not a current manuscript bug) | E2 lease/epoch is locally fenced but Build 4 E5 does not consume or validate that epoch; local same-UID tests cannot prove hostile-worker isolation | **Remain explicit open production gap.** Do not retrofit an untested E5 fence into the reference code under this editorial patch. Chapter 29 must require a negative stolen-token/hijacked-agent scenario; Chapter 31 must verify any new boundary. |
| WG-06 | High, **production readiness** (not a current manuscript bug) | Mock provider and local SQLite evidence cannot establish commercial processor retention, finality, remote consistency, multi-site replication, backup, key custody or independent operator authority | **Remain explicit open production gap.** Chapter 30 must exercise operational response/telemetry; Chapter 31 must require evidence for provider and recovery guarantees. |
| WG-07 | Publication gate | V12 allocation and word checks pass, but whole-volume Word-for-Mac rendered pages and independent exact external source-to-page verification are not certified | Mandatory final edition gate. Do not claim print production approval on the basis of Markdown or LibreOffice alone. |

The first four findings are corrected in the guarded patch. Findings WG-05–07 are *deliberately not marked fixed*: doing so would invent stronger guarantees or claim testing that did not occur.

## Cross-part reader-path war-game

**Part I — Foundations (Chapters 1–7).** The reader receives the system-versus-model thesis, purpose/boundary definition, economic choices, engineering judgment and reviews before seeing architecture. The chapters do not force the CASE-204 example into every opening; Chapters 2/3 establish examples that are subsequently carried forward. Source word and objective scans found seven developed Chapters 1–7, all with learning objectives. The distinct historical R-123 illustration remains explicitly separate in earlier review records. **Concern:** the choice between deterministic Design A, bounded-review Design B and optional investigation Design C must remain a business/evidence decision, not a staged autonomy ladder. No new manuscript correction justified by the current evidence.

**Part II — Reference Architecture (Chapters 8–16).** Figure 8.1 and the CAB-001 catalog are the logical anchor; the nine E-domains are not nine mandatory processes, and C01–C09 are architectural contracts rather than payment grants. Trusted execution/authority (E5) and durable operational state (E7) are not interchangeable with coordination (E2) or external business record (E8). The book correctly distinguishes C04 *advisory correlation* from RF-1042, and admission identity from transaction-specific authorization. **War-game attack:** read Chapter 8 and then jump directly to Chapter 28; the new full layered/zone-oriented Figure 28.1 provides a reasonable reorientation without copying Figure 8.1, and it does not make logical zoning equal hardware isolation. Existing semantic preflights passed. **Retained risk:** source-register claim-to-source passages and final 7×10 figure legibility still require production review.

**Part III — Patterns (Chapters 17–21).** The pattern trade-offs, fault models, risk-based enforcement, deterministic guardrails, and business economics connect the reference architecture to executable checkpoints without collapsing Design A/B/C into Builds 0–5. The traceability document includes older historical planned obligations; a current-status continuation is now added rather than falsifying historical review state. The contract-evidence chain from scope to proposal to trusted execution remains the critical conceptual gate.

**Part IV — Executable examples (Chapters 22–27).** Six distinct checkpoints are runnable. The architecture diagrams in each build README remain checked in and linked by relative `(architecture.svg)` paths. All checkpoints are educational slices rather than one composed pipeline. In particular, Build 5's E2-to-Build-4-E5 execution does not run Build 1/2 advisory/retrieval. A valid fixture E1 token without separate financial approval cannot create RF-1042. An E3 recommendation, even signed, carries no financial authority. The mock provider can commit before a reply is lost, with durable local UNKNOWN. The source-to-test handoff names these assertions and their exact tests; it does **not** claim real provider settlement or production security principal separation.

**Part V — Failure and recovery (Chapter 28).** The reader's mental model is a set of logical responsibilities, trust/enforcement boundaries and deployment-dependent failure domains. The architecture → failed message sequence → recovery decision diagrams are distinct views. Table 28.2 isolates crash windows; `NOT_FOUND` does not imply failed payment; a replacement owner uses status-only reconciliation after an uncertain attempt. The pure recovery fixture is explicitly non-effectful and not Build 6. The chapter's printed 7×10 pagination and figures were previously assessed on a development proof, but the current audit does not independently certify final native Word printing.

**Part V remaining (Chapters 29–31).** These are **not yet drafted**. The new assurance handoff does not confer completion by linking existing tests. The attack on E5 by a valid-token compromised investigator, protected E6 credential separation, incident operations/retention drills, and source/test-backed release evidence must be added, implemented as appropriate, and re-reviewed when those chapters are built.

**Parts VI–VII placeholders and book back matter.** Back-matter integrity checker passed: 28 developed chapters, 54 glossary terms, 44 indexed terms. Future chapters remain placeholders. Their status must not be silently promoted. The register descriptions and cited internal assurance evidence are updated; published pagination locators remain to be generated for the final layout.

## Six-lens adjudication

| Lens | Question / adversarial challenge | Observed support and limits | Result |
|---|---|---|---|
| Implementing engineer | Can I find the actual code and test for each claimed state transition, denial and lost acknowledgment? | Six build READMEs and source SVGs, Build 4/5 modules, pure recovery fixture; 18 named anchor checks added; executable tests individually pass | **Pass for educational scope**, not deployment implementation |
| Enterprise architect | Are E-domains logical responsibilities, C-contracts exchanges, and trust/failure zones distinct? Can E2 lease grant E5 finance authority? | CAB-001 catalog; Chapter 8; Chapter 28 layered view; build map; E2 epoch is not enforced inside E5 | **Pass with explicitly open execution-fence gap** |
| Advanced student | Does the sequence help me understand two truthful but different histories, `UNKNOWN` vs `FAILED`, and safe recovery? | Chapter 28 crash table and separated architecture/sequence/decision figures; Part V locally introduces roles; README tree fixed | **Pass on textual structure; final print legibility gate open** |
| Security / assurance | Can a compromised bounded investigator with a valid E1 token force a $500 payment or obtain E6 credentials? | Build 3 and Build 4 deny no-finance-grant requests; Build 1/2 data/proposal denial tests; no demonstrated hostile same-UID credential isolation or E5 epoch checking | **Fixture denial supported; production claim prohibited** |
| SRE / operations | Who owns `UNKNOWN` after an outage and what evidence closes it without blind replay? | Build 4/5 local crash/status tests; Chapter 28 evidence record; no deployed alerts, runbooks, operator recovery service, replicated E7, provider SLA | **Partly demonstrated; Chapter 30 obligations open** |
| Business owner | Can we prove only the original RF-1042 was paid, or explain why the answer is still unknown? | CASE-204 $500 stays fixed; provider observation can confirm the *fixture* effect; uncertain effects remain visible and may need a human decision | **Teaching case consistent; actual provider proof not available** |

## Companion test inventory and actual runs

- Build 0: **16 passed** (local durable intent, denial, concurrency, lost acknowledgment, conflict).
- Build 1: **15 passed** (strict untrusted advisory, malicious narratives, no financial capability).
- Build 2: **13 passed** (signed fixture claim, scoped context, forged/cross-tenant denial).
- Build 3: **18 passed** (separate-process E5 gate, valid token without approval, transport faults).
- Build 4: **25 passed** (provider contract validation, simulated E8, uncertain outcome, read-only reconciliation).
- Build 5: **22 passed** (SQLite E2 owner epochs, stale-epoch denial, crash/takeover, no re-execution by runner).
- Separate recovery fixture: **10 passed** (pure classification, no dispatch, conflicting/absent proof).

**Total: 119 unit tests passed in separate directory-scoped runs.** Build 3–5 were rerun individually after the interrupted combined run; tests in those directories were not skipped. The static assurance preflight checked **18 named unittest anchors** against Python AST method definitions and verified the six build README SVG embeddings.

**Uninterrupted `make check`: NOT CERTIFIED.** Two combined runs reached Build 3 but exceeded/interrupted within this execution environment even though individual Build 3 tests completed successfully in about 13 seconds. Consequently, report independent runs and static passes, not an invented green whole-command result. The Mac installation must rerun `make check` without interruption.

## Other QA evidence and limits

- Chapter entry/first-reference preflight: **28 developed chapters; PASS**.
- Professional review-perspectives preflight: **PASS**, with six-lens technical review recorded here.
- Companion architecture-documentation, companion code-quality and reader-access checks: **PASS**.
- Figure source/reference checks: **77 chapter image references verified; PASS**. Chapter 28 SVG geometry checks passed. This is not an independent pixel-level signoff of all 77 figures at Word-for-Mac print size.
- Back matter: **28 chapters / 54 glossary terms / 44 indexed terms; PASS**.
- Full book DOCX: generated successfully from the current repository with source-to-figure check. **Native Word-for-Mac pagination and print proof remain open**.
- V12: **485 chapter pages + 65 supporting = 550 target**, 575 preferred maximum, 600 planning limit, 700 absolute maximum. Allocations and word caps passed. **Actual complete-volume finished page measurements not available**.
- Citation preflights: PASS for checked mapping and structure. **External exact passage/edition verification still open**; the new handoff is internal evidence, not a scholarly citation.

## Patch scope and release decision

The attached guarded overlay changes eleven files: companion handoff and READMEs, implementation evidence map, figure and topic registers, source register, a new AST-based named-test checker, the Makefile QA hook and an AppleDouble exclusion in the source-code fence checker. The installer requires the original exact SHA-256 for every target and verifies all replacement hashes. It does not touch existing executable financial modules, CAB-001, chapter bodies or image masters. Local installer test succeeded, all eleven installed hashes matched and a repeat installation correctly refused without writes.

**Disposition for starting Chapter 29:** the scoped editorial/code-traceability findings are resolved in the patch, but merge acceptance requires a passing uninterrupted Mac `make check`, review of final printed figure/table pages and a conscious decision to carry production gaps as explicit Chapter 29–31 requirements. Do not label the companion production-ready and do not invent grant, provider or isolation guarantees. No new Build 6 is justified by the evidence audited here.
