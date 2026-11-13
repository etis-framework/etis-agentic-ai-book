# Chapter 18 — integration review and QA evidence (2026-11-13)

## Controlled baseline

Source: uploaded `ETIS_CH18_BASELINE.tar.gz`, cross-checked against the granular handoff. `metadata/approved/CAB-001.docx`, `metadata/architecture-catalog.md`, Part III introduction, Chapters 8–17 and V12 ledger were used as controlled continuity anchors. This was an editorial/architectural review, **not** a new independent live GitHub synchronization. Chapter 18 remains branch work until native Mac acceptance and merge.

## Scope and architecture acceptance

Chapter 18 answers coordination/delegation choices after Chapter 17 selects task mechanisms, and before Chapter 19 protects tools/adapters. No change to CAB-001 domain ownership or C01–C09 contract semantics is proposed. CASE-204 stays a $500 refund; Design A deterministic, Design B advisory with independent review and conditionally preferred, Design C read-only investigation alternative. RF-1042 remains the stable consequential-operation identity **only after authorization**. Task IDs and ownership epochs are separately named. Provider result UNKNOWN means reconciliation, not blind retry.

## Six-lens adversarial read, from front matter through Chapter 18

| Lens | Attempt to falsify the chapter's continuity | Result and disposition |
|---|---|---|
| Implementing engineer | Could a reader build a mutable case owner in model memory, or let a worker commit its own result? | **Addressed in Chapter 18**: E7 atomic epoch/version checks, typed result acceptance, scoped task identities; prior Chapter 10 mechanisms are explicitly inherited. Concrete lease durations remain implementation decisions, deliberately not invented. |
| Enterprise architect | Does supervisor/peer topology create a new E-domain or conflate logical and physical deployment? | **Addressed**: Figure 18.1 compares alternatives under one E2 logical owner and E5 authority; explains topology/mechanism/deployment are orthogonal. C01–C09 remain logical contracts. |
| Advanced student | Are Design A/B/C accidentally a progression of increasing permission? Is added coordination automatically better? | **Addressed**: chapter opening and decision matrix retain alternatives, simpler baseline and measured cost/reversal conditions. Practical exercises ask for comparisons and negative cases. |
| Security/assurance | Can peer content masquerade as policy, a registry grant read permissions, or a delegated worker reach a refund write endpoint? | **Addressed**: independent E4/data checks, E5 authorization, protected credentials, deny/trace tests, explicit untrusted peer semantics and human quarantine. The external provider contract still needs final environment-specific validation. |
| SRE/operations | What if the original coordinator resumes after expiry, a worker responds late, or a provider acknowledgement disappears? | **Addressed**: Figure 18.2 separates epoch-7 denial from UNKNOWN RF-1042 recovery; includes reconciliation, no new refund ID, monitoring, runbooks and containment tests. Exactly-once provider delivery is not claimed. |
| Business owner | Does the design explain who is accountable, what the customer may be told, and when added complexity is economically justified? | **Addressed**: domain/platform/security/operations responsibilities, honest unresolved status, cost per acceptable completed workflow, and evidence-based choice. Business-specific acceptance thresholds must be supplied by implementing organizations. |

**Cross-chapter action:** No substantive corrections to frozen Chapters 1–17 or front matter were justified by this review. The bibliography's coverage statement and source register were extended to Chapter 18. The Chapter 17 acceptance test's legacy substring remains preserved to avoid breaking existing certification semantics.

## Executed checks

- `publishing/scripts/check.py`: PASS (structure).
- `publishing/scripts/check_figures.py` and `--built`: PASS after integrated DOCX build; both Chapter 18 figure PNG SHA-256 hashes embedded.
- `publishing/scripts/check_single_volume.py`: PASS, Chapter 18 **2783/3000** word cap.
- `publishing/scripts/check_finished_page_ledger.py`: PASS for V12 **12-page allocation** and 550-page target; not a print measurement.
- `publishing/scripts/check_ch17_acceptance.py`: PASS after bibliography scope compatibility maintained.
- `publishing/scripts/check_ch18_acceptance.py`: PASS for domain markers, CASE-204, citations, figure dimensions, legibility proxies, image fingerprints and locked V12 allocation.
- `publishing/scripts/check_parts13_integration.py`: PASS.
- `publishing/scripts/check_mac_word_ch01_ch17.py`: PASS for the *historical author-reported* 208 pages/230 allocations; **does not render or measure Chapter 18**.
- Both figure SVGs visually inspected at rasterized resolution. Figure 18.1 is a logical architecture comparison; Figure 18.2 is a failure/reassignment sequence. Masters use 5.75-inch width, 1140-unit canvas, Arial labels >=19 units; both PNGs generated and embedded. Print-size physical paper inspection on Mac remains open.
- Standalone Chapter 18 DOCX built with Pandoc, then rendered with LibreOffice as eight pages. Page-images/contact sheet inspected for table flow and figure placement; this **is not native Microsoft Word for Mac acceptance**.
- Integrated full-book DOCX built successfully. The whole `make check` sequence reached the Mac pagination evidence script; one attempt timed out at that point, so no uninterrupted full-run certification is claimed. Individual final gates were rerun successfully.

## Unresolved publication gates

1. Open native **Word for Mac** full manuscript and Chapter 18; record exact chapter start/end pages and verify Chapter 18 <=12 finished pages. The local 8-page LibreOffice result is an indicator only; use Word's actual 7x10 layout and styles.
2. Inspect F18-01 and F18-02 in Word at final printed size (not just PNG zoom), captions and flow, and run a complete physical print-layout check.
3. Validate exact claim-to-edition/page source support as part of publication-level citation audit. Existing sources were reused; a new edition/source verification was not performed.
4. Confirm patch preimages against the current live chapter branch and latest merged `main` before installing; repository tar is a snapshot, not a live Git ref.
5. Re-run `make check` in Mac environment after Word build; resolve any new errors before PR merge.

## Page-budget assessment

Approved Chapter 18 allocation: **12 pages**. Standalone Linux/LibreOffice result: **8 pages** including both figures and exercises, i.e. 4 pages below allocation **in that renderer only**. Previously author-measured Chapters 1–17: 208 pages against 230 allocated (22 pages headroom). A mixed-renderer implied book projection would be 524 pages with all later chapters at V12 allocation and all 65 supporting pages; **this is provisional and must not be represented as a validated Mac Word forecast**. Retain V12 ledger unchanged.
