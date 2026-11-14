# Chapter 28 second incremental correction — logical failure zones and figure review

## Baseline / intent

This overlay requires the previously installed `ETIS_CH28_READER_FIRST_INCREMENTAL_SHA256` output, itself layered over the initial Chapter 28 guarded patch on the Chapter 28 branch. It is **not** a new draft against `main`. The installer checks the SHA-256 of every existing target, including updated figures and manuscript text, and rejects an altered target before writing. No Git state is changed by installation.

The change reorients Chapter 28's teaching sequence around **layered logical responsibility and failure zones**, using Figure 8.1 and Figure 16.1 as precedents, without implying nine services, nine machines or physically independent failure domains. All CAB-001 identities and the CASE-204 $500 / RF-1042 fixed operation are preserved. Design B remains conditional; Builds 0–5 remain independent educational checkpoints. E5 still does **not** enforce Build 5's E2 epoch.

## Reader-facing change

- Part V introduces responsibility/authority versus deployment/failure separation.
- §28.2 defines three boundaries: responsibility ownership, trust/enforcement, and failure/deployment. A new **worked deployment-examples table** covers co-process advisory work, distinct processes on one host, shared database dependencies, remote provider status ambiguity, and multi-site stale-ownership exposure. The business decision about required isolation is explicit, not left to reader inference.
- Figure 28.1 replaces the crowded earlier illustration with a layered Figure 8.1-inspired view, cross-cutting E7/E9 columns, three failure seams, and no chapter-purpose bubble. It is a logical zone view, not a hardware diagram.
- Figure 28.2 is a genuine message sequence through the five relevant responsibilities, showing a *lost reply after E8's effect*, `UNKNOWN`, replacement ownership, and read-only lookup with no second send.
- Figure 28.3 uses real decision diamonds and explicit `UNKNOWN` branches before confirming the existing RF-1042, with separate authorization for any new remedy.
- Glossary, working index and topic traceability now record all three boundary kinds and Figure 8.1 → Figure 16.1 → Figure 28.1 navigation.

## Executed checks and measurements

- `python3 publishing/scripts/check_ch28_acceptance.py` — PASS.
- `python3 publishing/scripts/check_ch28_figure_geometry.py` — PASS; three SVG masters, exact render mirrors, 5.75-inch print width, three distinct visual types and required labels. This is not a substitute for visual print inspection.
- `python3 publishing/scripts/check_chapter_first_references.py` — PASS through Chapter 28.
- `python3 publishing/scripts/check_professional_review_perspectives.py` — PASS after restoring the required reader-facing multi-perspective heading language.
- `python3 publishing/scripts/check_backmatter_integrity.py` — PASS; 54 glossary terms, 44 index entries.
- `python3 publishing/scripts/check_finished_page_ledger.py` — PASS; Chapter 28 source count at or below the existing 3,500-word cap; V12 allocations unchanged.
- Build 0, 1, 2, 3, 4, 5 and reliability `unittest discover` independently — PASS: 16 + 15 + 13 + 18 + 25 + 22 + 10 = **119 passing tests**.
- Chapter 28 DOCX generated, converted to a **7×10-inch** development proof, and the resulting PDF has **14 pages** against the V12 **17-page** Chapter 28 allocation. Figure pages 3, 8 and 11 were examined at print-size rendering. The initial E7 sidebar word-wrap defect was corrected after inspection. This does not certify native Word for Mac or integrated whole-book pagination.
- `make book-docx` — PASS in this environment.
- Full `make check` — **INCOMPLETE** in this environment: the final attempt progressed beyond Chapter 28, chapter-reference, geometry, and professional-review checks and was terminated at `check_companion_architecture_docs.py` by the execution limit. The independent regression tests above passed. Do not report full `make check` as passed until it finishes on the Mac.
- Exact third-party source-page claims / actual provider service guarantees were **not independently certified** by this editorial patch.

## Six-lens cross-book war-game (front matter through Chapter 28, future placeholders, back matter and source/traceability registers)

1. **Implementing engineer:** The figure does not claim that a line in a module diagram creates a network partition. It distinguishes E2-local lease fencing from the absent E5 epoch check. Existing E5/E7/E6 execution tests still pass; the new changes do not add executable behavior or an implicit Build 6.
2. **Enterprise architect:** Figure 28.1 preserves CAB-001's E1–E9 responsibility inventory and E7/E9 cross-cutting duties, with layer/zone framing linked back to Chapters 8 and 16. It explicitly distinguishes logical ownership, independently enforceable trust boundaries, and actual shared-fate infrastructure. No new contract directions are asserted by the stylized arrows.
3. **Advanced student:** Full logical overview precedes the zoomed-in failure chronology; numbered failure seams, concrete deployment scenarios, separate histories, and decision diamonds reduce mental translation of E/C shorthand. A student can explain why provider success plus lost reply implies uncertainty locally, not a failed payment.
4. **Security/assurance:** C04 advice remains non-authoritative; no drawing grants E3 credentials, turns E2 ownership into financial authorization, or claims a valid token alone authorizes a refund. Recovery status is read-only and any independent remedy requires E5 approval. Missing E5-consumed epoch remains a named production gap.
5. **SRE/operations:** Shared database and same-host failure dependence are visible choices. The recovery view distinguishes a transport loss from provider absence, status-inquiry unavailability, and a verified matching provider record; unknown outcomes require quarantine and escalation, not blind redrive.
6. **Business owner:** Physical separation is selected to meet loss tolerance, recovery objectives, operational cost, provider contracts and assurance; it is neither free nor universally required. An unresolved $500 credit is preferable to an unauthorized duplicate; human remediation has an owner and a new approval boundary.

### Remaining publication gates

Run uninterrupted `make book-docx` and `make check` on the actual Chapter 28 branch. Review native Word-for-Mac integrated 7×10 pagination, especially Figures 28.1–28.3 and the worked-example table; review current source-register publication facts/citation page claims; do not merge if layout or semantics differ. This overlay intentionally changes no business-logic implementation or CAB-001 architecture baseline.
