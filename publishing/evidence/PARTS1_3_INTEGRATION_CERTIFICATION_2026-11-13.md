# ETIS Parts I–III integration correction: Chapters 1–17

**Evidence baseline:** `ETIS_PARTS1_3_CERT_BASELINE.tar.gz` received 2026-11-13; source authority is that archive, not reconstructed previous patches. **Branch required for installation:** `work/parts1-3-integration-quality-certification`.

**Acceptance distinction:** Corrected architectural integration defects and executed repository QA are **not** certification of the book for publication. A source-page/edition audit and native Word for Mac print acceptance are still outstanding.

## Disposition register

| ID | Finding / scope | Resolution and evidence | Status |
|---|---|---|---|
| INT-01 | Figure 4.2's A/B/C labels collide with CASE-204 alternatives | Removed A/B/C from the SVG master, DOT explanatory source, and revised nearby prose; updated Chapter 4 semantic test | Corrected; automation and LibreOffice print checked |
| INT-02 | Figure 3.3 repeats “PERMIT” on a branch and action box | Preserved branch PERMIT; action box now TRUSTED EXECUTION; corresponding DOT reference also aligned | Corrected; print checked |
| INT-03 | Chapter 17 E3 phrasing could imply that Design A requires a model | Explicit deterministic implementation clarification in §17.5; running case and trusted boundary unchanged | Corrected |
| INT-04 | Front matter introduces C01–C09 but their meanings are not findable | Read CAB-001 approved contract table; added named C01–C09 table to Chapter 8 §8.4 and transcribed source summary into metadata/architecture-catalog.md. Front matter now locates the table | Corrected against approved CAB-001 |
| INT-05 | Duplicate foundational explanations | Reviewed chapter responsibilities and searched for verbatim paragraphs ≥50 words across developed chapters (none). Repeated invariants retained where progressing from requirements to enforcement; no wholesale shortening | Accepted with rationale; selective editorial judgment |
| INT-06 | Chapter 2 anticipates later material | Historical inheritance is its stated editorial responsibility; no reorganization justified without losing the reason later controls exist | Accepted; avoid repetition in future Part III chapters |
| INT-07 | Citation coverage and source specificity | Existing bibliography, BibTeX and source register retained; Chapter 3 mapping made explicit; Chapter 8 CAB provenance added; published-source support limitations preserved. Three official bibliographic records spot-checked externally, not all source passages | Partially corrected; exact source-page verification remains open |
| INT-08 | Earlier 295-page DOCX versus current pagination | Rebuilt authoritative archive with current scripts and rendered integrated 7×10 DOCX/PDF. Measured 234 PDF pages including all placeholder chapters and draft backmatter; developed Chapters 1–17 = 185 measured pages. Different source/version/renderer likely explains prior number, but not independently proven | Reconciled for this baseline; native Mac Word parity open |
| INT-09 | Individual V12 allocations | Chapter 3 =16/15 (+1); all other developed chapters within V12 allocations. Underruns offset the single-page overage at aggregate level; no arbitrary chapter compression | One documented exception, not falsely marked compliant |
| INT-10 | V12 whole-book forecast | 185 measured developed chapter pages + 255 remaining chapter allocation + 65 supporting reserve = 505 projected pages. Forecast assumes remaining chapters meet their allocations and supporting matter uses reserve | Forecast only, not finished-book measurement |
| INT-11 | Figure source/render/Word consistency | Regenerated SVG/PNG from source masters, completed automated figure identity checks and Word embedding checks; inspected corrected Figures 3.3, 4.2, Chapter 8's C01–C09 spread, and Chapter 17 at 7×10 | Automated pass, representative visual check; native Word review pending |
| INT-12 | Build failure on uploaded macOS archive | Generator now ignores `._*.dot` and `._*.svg` AppleDouble sidecar files, which are not source figures | Corrected and run through `make figures` |
| INT-13 | Insufficient automated integration protections | New `check_parts13_integration.py` added to `make check`; validates approved names, figure labels, CAB mapping, case identifiers, page plan, and embedded changed figures | Corrected and executed |
| INT-15 | Repository README and book.yaml still described Chapters 1–2 or 1–5 as the only developed content | Corrected repository metadata to the accepted 1–17 status and V12 locked plan; retained historical files under archive | Corrected |
| INT-14 | Unfinished author, index, glossary, permissions | No placeholder represented as production-ready; these remain publication tasks, not reasons to rewrite frozen developed chapters | Explicitly deferred to whole-book production |

## Chapter-specific six-lens disposition

| Chapter | Distinct role in progression | Six-lens concern / disposition |
|---|---|---|
| 1 | Enterprise engineering problem | Retain foundational obligations; no architecture drift |
| 2 | Historical inheritance | Distinct from later detailed mechanisms; no unsupported compression |
| 3 | Work, goals and authority | Clarified Figure 3.3; 16/15 pages recorded |
| 4 | Agent semantics and feedback | Figure 4.2 now generic patterns rather than CASE-204 alternatives |
| 5 | Lifecycle business economics | Continue counting complete workflows; unchanged |
| 6 | Uncertainty and trust | Distinguish source, decision and effect uncertainty; unchanged |
| 7 | Requirements and enforceable boundaries | Maintained policy/credential distinction; unchanged |
| 8 | Canonical target-state E1–E9 reference architecture | Added approved C01–C09 cross-domain contract inventory |
| 9 | Admission and identity E1 | Preserved tenant/principal scoping |
| 10 | Coordination E2 | Preserved logical ownership, registration and fencing |
| 11 | Reasoning E3 | Proposals remain advisory |
| 12 | Context E4 | Context retains provenance, not business truth |
| 13 | E5 independent effect authority | Credential protection untouched; source-word ceiling protected |
| 14 | E6/E8 provider integration and truth | Stable RF-1042, provider caveats and outcome reconciliation intact |
| 15 | E7/E9 durable recovery and assurance | UNKNOWN and recovered operation identity intact |
| 16 | Deployment views and Part II closure | Logical-to-physical mapping unchanged |
| 17 | Architectural alternatives and evidence gates | Clarified deterministic E3; A/B/C conditional selection unchanged |

**Six lenses:** (1) implementer — contracts are now discoverable; (2) enterprise architect — Figure 8.1 and CAB-001 define one logical design, not mandatory services; (3) advanced student — generic pattern labels no longer conflict with CASE-204 alternatives; (4) security/assurance — no agent credential custody or self-authorization introduced; (5) SRE — UNKNOWN, status query, and no blind resubmission retained; (6) business owner — Design B remains conditional, reviewed on economics and evidence rather than AI novelty.

## Citation evidence and non-certification

- Checked the manuscript's source register and BibTeX identities across Chapters 1–17. The repository already contains 28 bibliography records. The corrected source register explicitly adds Chapter 3 and CAB-001 provenance.
- The official NIST SP 800-207 catalog supports its author/date/DOI identity, and its zero-trust subject; it does not certify ETIS deployment.
- RFC 9110 §9.2.2 defines HTTP idempotent methods; it does **not** establish payment-provider refund deduplication or idempotency-key retention.
- PubMed DOI 10.1109/3468.844354 confirms the bibliographic identity of Parasuraman, Sheridan and Wickens (2000). This does not establish the ETIS design matrices.
- **Open:** exact source-page/section verification of the other cited research/books, licensed standards, living references, version pinning, provider-specific behavioral contracts, and final linked citation rendering. These are not silently marked passed.

## V12 measured chapter ledger — integrated 7×10 LibreOffice

| Ch | Pages | V12 | Difference |
|---:|---:|---:|---:|
| 1 | 13 | 15 | -2 |
| 2 | 18 | 18 | +0 |
| 3 | 16 | 15 | +1 |
| 4 | 11 | 12 | -1 |
| 5 | 9 | 11 | -2 |
| 6 | 8 | 12 | -4 |
| 7 | 9 | 12 | -3 |
| 8 | 11 | 12 | -1 |
| 9 | 9 | 13 | -4 |
| 10 | 11 | 14 | -3 |
| 11 | 11 | 14 | -3 |
| 12 | 10 | 14 | -4 |
| 13 | 11 | 15 | -4 |
| 14 | 10 | 14 | -4 |
| 15 | 9 | 14 | -5 |
| 16 | 9 | 13 | -4 |
| 17 | 10 | 12 | -2 |

**Measurement boundaries:** Chapter 7 ends PDF page 98, Part II introduction occupies 99–101, Chapter 8 starts 102. Chapter 16 ends page 192, Part III introduction occupies 193–194, Chapter 17 starts 195. Counts exclude the intervening Part openers. Total PDF 234 pages includes draft Chapters 18–36 placeholders and partial back matter; it is **not** the projected completed book length. The 65 supporting pages remain reserved, not measured.

## Remaining publication gates

1. Rebuild and inspect in Microsoft Word for Mac at native 7×10, including all 49 referenced figures, captions, tables, footers and section parity; LibreOffice alone is not final certification.
2. Source-by-source primary literature and licensed standard claim support; record exact edition/section and pin living guidance.
3. Complete back matter (author, index, glossary, permissions) after the final 36 chapters.
4. Reconcile remaining-chapter actual pages as completed; preserve V12 550 target, 575 preferred upper bound and 700 absolute maximum. Chapter 3's one-page variance remains explicitly open rather than silently changing V12.

## Executed tests

`make figures`, `make book-docx`, `make check`, `make check-figures`, `check_parts13_integration.py`, and `check_finished_page_ledger.py --actual-pages publishing/evidence/ACTUAL_PAGINATION_CH01_CH17_2026-11-13.json` were executed in this review environment and passed; the exact logs accompany the patch. A source-level no-verbatim-duplicate scan found no paragraphs ≥50 words repeated across developed chapters.
