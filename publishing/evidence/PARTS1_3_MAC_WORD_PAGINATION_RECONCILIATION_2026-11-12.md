# Parts I–III Mac Word pagination reconciliation — Chapters 1–17

## Measurement provenance and limits

The author measured chapter and part boundaries using Microsoft Word for Mac Navigation Pane on 2026-11-12, and supplied `ETIS_MAC_WORD_PAGINATION.docx` for source-content inspection. These are **user-measured native Word positions**, not an independent repeat measurement in this environment. The earlier LibreOffice pagination file `ACTUAL_PAGINATION_CH01_CH17_2026-11-13.json` is **retained as separate renderer evidence**; do not silently replace or combine the measurements.

Chapter 7 ends where Part II begins at page 113; Chapter 16 ends where Part III begins at page 219; Chapter 17 ends at the Chapter 18 placeholder on page 233. The Part II and Part III openings each consume four pages between part and chapter starts; they are supporting matter, not Chapter 7 or 16.

| Chapter | Word pages | Locked V12 allocation | Variance | Disposition |
|---:|---:|---:|---:|---|
| 1 | 14 | 15 | -1 | Within allocation |
| 2 | 20 | 18 | +2 | Exception retained |
| 3 | 18 | 15 | +3 | Exception retained |
| 4 | 14 | 12 | +2 | Exception retained |
| 5 | 10 | 11 | -1 | Within allocation |
| 6 | 10 | 12 | -2 | Within allocation |
| 7 | 10 | 12 | -2 | Within allocation |
| 8 | 12 | 12 | +0 | Within allocation |
| 9 | 10 | 13 | -3 | Within allocation |
| 10 | 12 | 14 | -2 | Within allocation |
| 11 | 12 | 14 | -2 | Within allocation |
| 12 | 12 | 14 | -2 | Within allocation |
| 13 | 12 | 15 | -3 | Within allocation |
| 14 | 10 | 14 | -4 | Within allocation |
| 15 | 11 | 14 | -3 | Within allocation |
| 16 | 11 | 13 | -2 | Within allocation |
| 17 | 10 | 12 | -2 | Within allocation |

- Completed chapters: **208 / 230** pages, **22 pages below** cumulative allocation.
- Explicit chapter exceptions: Chapter 2 **+2**, Chapter 3 **+3**, Chapter 4 **+2** (7 pages over individual ceilings in total).
- Remaining chapter allocations (18–36): **255** pages. Supporting material: **65 reserved** (not certified as actual).
- Conditional full-volume estimate: **208 + 255 + 65 = 528 pages**, assuming every unfinished chapter stays at allocation and supporting material uses the full 65-page reserve. This is **not a final print measurement**.

## Editorial disposition of Chapters 2–4

The 17-chapter war game identified repetition of inherited principles, but also distinct engineering duties. Chapter 2 provides historical technical foundations: transaction boundaries, expert systems, workflow, distributed uncertainty, integration, data, security, and operational governance. Chapter 3 translates those foundations into delegation, business authorization, case states, and Design A/B/C alternatives. Chapter 4 defines the agent mechanism and action-selection loop, including model-independent agents and constrained tooling. No passage was conclusively identified as dispensable without loss of the intended learning progression. **Do not shorten technical material solely to force these three chapters under their individual planning allotments.** Exceptions remain open, not reclassified as passes.

## Targeted Chapter 17 prose correction

Consolidated consecutive deterministic-E3 sentences in §17.5 into one clear statement without changing the architecture or the Design A/B/C contract.

## Remaining gates

1. Regenerate figures and the integrated Word manuscript; run the full existing QA suite and the Mac-pagination ledger preflight.
2. Inspect Figure 3.3, Figure 4.2, Figure 8.1, the C01–C09 table, Chapter 17 and page boundaries in native Microsoft Word for Mac.
3. Retain precise claim-level primary-source verification and completed full-volume supporting-matter pagination as publication gates.
4. Preserve the locked 550 target and the 485+65 V12 allocations; this file adds actual measurements, not a new allocation baseline.
