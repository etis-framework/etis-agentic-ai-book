# Chapter 27 / Build 5 — Six-Lens War-Game, Code Review and QA

**Working state:** Developed against the complete Chapter 26 / Build 4 snapshot. All findings below pertain to this exact proposed Chapter 27 payload; release to `main` requires GitHub PR checks and the author's local Word for Mac inspection. The single bound 7×10 V12 plan remains locked at 550 target pages (575 preferred maximum; 600 planning limit; 700 absolute ceiling). **Not** a production payment or distributed-coordination certification.

## Baseline, invariants and dependencies

- Reconstructed post-Chapter 26 source from the prior chapter's repository and verified Build 4 patch. The exact merged `main` commit SHA was **not supplied**. The installer checks every affected file against the exact source-byte baseline and refuses any divergence; it does not assume an unverified Git SHA.
- CAB-001 E1–E9/C01–C09 remain logical responsibilities/contracts. E2 coordinates work; E5 independently evaluates real transaction-specific financial authority; E7 maintains one local RF-1042 dispatch intent; E6 drives the **simulated** provider; E8 holds only mock provider truth; E9 owns assurance evidence. An E2 lease is not an E5 grant or provider acknowledgment.
- CASE-204 retains the proposed $500 refund and RF-1042 remains the single trusted operation identity. E3/C04 advisory output has neither provider credentials nor the authority to create it. Designs A/B/C are **alternatives**; Design B remains a conditional initial production candidate. Build 5 is optional, never an autonomy-maturity requirement.
- Builds 0–4 remain separately runnable. Build 5 uses the actual Build 4 E5 server as a separate subprocess for integration tests; it does not modify prior Build 4 payment implementation.

## Six independent adversarial reader lenses

| Lens | Challenge asked | Verified evidence | Residual risk / owner |
|---|---|---|---|
| Implementing engineer | What happens if E5 responds incorrectly, the worker crashes between E2 intent and E5 transport, or two workers race? | `coordinator.py` commits one `EXECUTE_IN_FLIGHT` under `BEGIN IMMEDIATE`; `runner.py` never re-executes; tests cover 8 competing acquisitions, crash-before-call, crash-after-effect, wrong-operation response and state transitions | Protected store, availability, durable task queue and realistic service telemetry owned by platform engineering |
| Enterprise architect | Are the boundaries CAB-001 responsibilities or invented Python/security domains? | F27-01, source `architecture.svg` and README map E2/C02, E5/C05, E7/C06, E6/C07 and E8/C08; figure arrow returns through E5; independent finance grant remains unchanged | Real topology, authoritative store and E5-enforced ownership fencing need an explicit deployment architecture |
| Advanced student | Can a learner independently read the chapter and reproduce takeover without confusing it with permission? | Chapter objectives are descriptive, CASE-204/RF-1042 introduced, runnable four-scenario demo and exercises; 7×10 eight-page print-compatible preview with three diagrams | Source-edition tag and full learning-assessment validation at publication |
| Security / assurance | Does valid E1 identity or E2 lease allow a compromised investigator to create a refund? Does a stale E2 owner still reach E5? | Genuine E5 service subprocess and Build 3–4 authorization tests. E2 mutating calls reject stale epoch; README and manuscript explicitly state E5 **does not check E2 epoch** | **High priority before real production:** E5-side authoritative epoch enforcement, protected service identities, independent finance key custody and adversarial compromised-host tests |
| SRE / operations | Does lost acknowledgment lead to another provider send, and can one missing E8 status be mistaken for failure? | Build 5 runner stores E2 intent before E5 call, returns UNKNOWN on missing response and permits status-only reconciliation; Build 4 E7 one-time claim + mock E8 key uniqueness unchanged; provider outage remains unresolved | Scheduler, read-only recovery entitlement, alerting/backoff/escalation, multi-site failover and runbooks not implemented |
| Business owner | Why incur coordination cost, and what is claimed about customer funds? | Chapter 27 decision exercise compares simpler Build 4 with optional Build 5; mock E8 proof not settlement; no invented new payment ID or authority | Business requirements, measurable benefit, approved finance workflows, customer communication and residual-risk acceptance |

## Findings caught and corrected **before** packaging

1. **F27-01 misleading recovery arrow:** The first architecture figure appeared to route mock E8 status directly into E2 recovery. Redrawn to route observations **through E5**; caption explicitly identifies local-only E2 fencing.
2. **F27-03 premature E5 invocation:** Initial decision figure displayed E5 ahead of the `READY`/`UNRESOLVED` state branch. Redrawn to show lease validation, initial intent versus read-only reconciliation, then independent E5 gate. Labels enlarged for print-size readability.
3. **Unbound confirmation status:** Initial E2 runner accepted a bare `CONFIRMED` message. Now requires a typed dictionary carrying exactly CASE-204 and RF-1042 before recording observed confirmation. Added negative tests for absent/wrong operation proof and a post-effect crash handoff.
4. **Stale code documentation:** Companion root layout missed Build 5; `ARCHITECTURE.md` and first-reference standard lagged prior chapter status, and historical Parts I–III audit text could mislead without a status note. Updated reader navigation and status in the same patch.
5. **Chapter 26 gate brittle on chapter-status advancement:** `check_ch26_acceptance.py` required the exact status text “Chapters 1–26 developed,” causing the full run to fail after Chapter 27 was added. Updated to permit the newly valid Chapter 27 status without changing its architecture, test or figure requirements.
6. **Coordinator source/prose mapping:** Reworded Chapter 27 to name only the fields actually stored (case, fixed operation, worker, lease expiration, epoch, phase, last observation). No imaginary “approved class of work” is claimed.

## Actual executed evidence

- `PYTHONWARNINGS=error::ResourceWarning` independent Build 0: **16 passed**; Build 1: **15**; Build 2: **13**; Build 3: **18**; Build 4: **25**; Build 5: **22**. **Total 109** tests across separately executed suites. Builds 4–5 exercised actual E5 subprocesses. Fixture demos `approved`, `denied`, `lost-ack`, `outage` were executed by Build 5 integration tests.
- `check_ch27_acceptance.py`, `check_ch27_figure_geometry.py`, `check_chapter_first_references.py` (27 substantive chapters, zero issues), `check_companion_architecture_docs.py` (six embedded source SVGs and local links), `check_companion_code_quality.py`, `check_reader_companion_access.py`, `check_code_listing_layout.py` and `check_finished_page_ledger.py`: **passed** after final corrections.
- Chapter 27 source approximately **2,800 words**, below locked **3,500-word cap**. Rendered standalone 7×10 Word-compatible output: **8 pages**, under the **14-page Chapter 27 allocation**. This is a LibreOffice/Word-compatible preview, **not native Word for Mac certification**.
- `make book-docx` and `check_figures.py --built`: **passed**, with **74 embedded figure references**. Masters F27-01/02/03 and rendered SVGs are byte-identical; generated PNGs inspected; the source-level Build 5 SVG is checked in and embedded in its README. The two figures revised during QA were rerendered after correction.
- Complete `make check`: a first run failed on an **overly rigid Chapter 26 book-status gate**, which was fixed. A subsequent run was **terminated by execution limit at Chapter 24**, not completed. It must be run on the Mac before committing; do **not** claim a single completed full-suite pass.
- Native 7×10 Word for Mac print-size review, bibliography primary passage/page verification, final whole-book pagination and external provider/deployment acceptance **remain open**.

## Hard architectural boundary of this build

A malicious stale worker might still present an independently valid finance grant to E5. Build 5's E2 fencing only rejects stale mutations in its SQLite store. That is **not** a proof of exclusion at E5, and the fixture does not claim otherwise. An enterprise implementation must check trusted ownership at the consequential boundary (subject to accurate E2 authoritative state, transaction timing, revocation and actual provider semantics), in addition to transaction-specific business approval. If this is not implemented and demonstrated, any production-readiness claim must be **held**.

The implementation also intentionally does not implement multi-site consensus, authoritative clocks, per-worker OS identities, independent recovery-authorization roles, provider settlement, protected audit, scheduled retry/backoff, workload quotas or incident command. Each omission is named in the chapter and README. These cannot be silently inferred from passing local unit tests.

## Release disposition

**Conditional proceed to local QA and PR, not unconditional release.** Install against the exact post-Chapter 26 clean `main`, run `make book-docx` and `make check` to completion, inspect F27-01–03 in Word for Mac at trim size, verify the branch's staged changes, then merge through protected PR. The educational acceptance scope is satisfied by code/negative evidence, while the production security and publication claims remain explicitly bounded.
