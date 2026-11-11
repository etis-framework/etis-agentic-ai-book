# Chapter 5 / Front Matter–Chapter 5 Integration Review

**Release candidate:** Chapter 5 development patch, 2026-11-11. **Status:** Source QA and LibreOffice print review completed; native Word-for-Mac visual acceptance remains open. This is a development chapter, **not publication freeze**.

## Authoritative inputs and reconciliation

- Source baseline: existing ETIS source archive plus **all version 2 consolidated Chapter 4 corrective patch files**, not the intermediate Chapter 4 development draft.
- The approved `BP-001.docx` assigns Chapter 5 to *Business cases, value and lifecycle economics* and prescribes the running refund-economics thread.
- Standard: `publishing/FIGURE_STANDARD_V9_MANDATORY.md`, source `5.75in` width, page size `7 x 10in`, semantic palette, independent control arrows, no crossovers, source master and rendered assets.
- Binding source budget: `publishing/SINGLE_VOLUME_BUDGET_V10.json` (chapter 5 cap 2,900 words, working target 550 pages, preferred max 575, planning limit 600, absolute max 700, 50 pages front/back matter reserve, 280 effective words/page estimate).
- Existing Chapter 4 corrective patch's substantive content and three approved replacement figures preserved. The earlier V2 patch had already corrected the closing OpenAI citation year to 2026; the Chapter 5 patch preserves that correction without modifying Chapter 4.

## Six-reader adversarial war game: front matter through Chapter 5

| Lens | Challenge and finding | Disposition |
|---|---|---|
| Executive / finance | An impressive speed demo is not a business case; require baseline, counterfactual, credible realization of benefits, fully loaded net value, and stop thresholds. Chapter 5 includes a three-design cost table and audited arithmetic; treats $500 refund as a liability, not a savings benefit. | Covered in 5.1–5.5, 5.7. |
| Enterprise architect | Does an agent silently become the authorization authority as the chapters progress? No. Initial production candidate remains Ch3 Design B, Ch4 Design C is evaluation-only, and all three Ch5 alternatives share trusted authority and governed execution. | Covered in 5.1–5.2 and Fig. 5.1. |
| Software engineer | Are technical and business denominators conflated? No. Cost-per-invocation is distinguished from fully loaded cost per correctly resolved case. Case mix and route selection are controlled. | Covered in 5.2–5.5 and exercises. |
| Security / privacy / governance | Could average expected benefit authorize unauthorized actions? No: hard constraints, disclosure, duplicate payment, independent approval, and pre-defined stop conditions remain independent gates. | Covered in 5.4, 5.6–5.7 and Fig. 5.2. |
| SRE / operations | Is a timeout counted as failed, allowing automatic retry? No: `UNKNOWN` remains unresolved until reconciliation; durable operation identity and change/rollback obligations retained. | Covered in 5.5–5.8. |
| Educator / early-career engineer | Can a reader reproduce the decision and detect counterfactual or case-mix bias? Yes: explicit costs and denominators, reproducible break-even arithmetic, decision-grade experiment, six exercises and review standard. | Covered in worked example and exercises. |

## Front-matter, Ch1–Ch5 drift audit

1. Introduction: demonstration vs operational proof and $500 refund uncertainty remain aligned.
2. Part I opener: now correctly says Chapters 1–5 drafted, Chapters 6–7 planned.
3. Ch1: engineering responsibility and verification precede agent capability; no modification required.
4. Ch2: inherited transactions and distributed uncertainty; no modification required (earlier Fig. 2.4 correction preserved).
5. Ch3: production starting point = **Design B, advisory AI plus independent review**; preserved.
6. Ch4: agent = permitted action selector, not payment authority; Design C framed as controlled alternative; verified that the V2 baseline already corrected the stale OpenAI year to 2026; no Chapter 4 source change required.
7. Ch5: evaluates A/B/C on equal case populations; never grants read/write payment authority to the investigating component; `UNKNOWN` is reconciled, never interpreted as failure or repeated with a new identity.
8. `book.yaml`: corrected stale **435** target to **550** and metadata to Chapters 1–5 drafted for review.

## Quantitative verification

- Chapter 5 source: **2,325 / 2,900 words**. Remaining chapter allowance: **575 words**; no pressure to fill.
- Ch1–Ch4 word counts remain 3,783 / 3,900; 5,269 / 5,400; 4,070 / 4,300; 2,985 / 3,000.
- Total extant chapter source: 20,302 words (includes 31 short future-chapter stubs). Not a percentage-of-finished-book estimate.
- 36 chapter allocations = **117,800 words**. At 280 effective words per page, a baseline of **420.7 pages** plus 50 reserved front/back gives **470.7 pages**, leaving approximately **79 pages** within the 550 working target for diagram/table/layout overhead. This is a rough *budget calculation*, not a pagination guarantee; the 79-page reserve may need adjustment if figure-heavy chapters accumulate.
- Illustrative refunds per year: 10,000. A: 10,000 × $8 = $80,000. B: 10,000 × $5.90 + $18,000 = $77,000. C: 10,000 × $5.50 + $48,000 = $103,000. B advantage $3,000; C disadvantage $23,000. Break-even B = 18,000 / 2.10 ≈ 8,571.43, requiring 8,572 cases; C = 48,000 / 2.50 = 19,200.
- Full assembled DOCX, including unwritten chapter placeholders: **125 pages when rendered with LibreOffice**. Chapter 5 begins on rendered PDF page 73; Chapter 6 begins page 82; Chapter 5 occupies nine rendered PDF pages including chapter start/page spacing. This assembled page count is **not the projected finished page count**.

## Figure QA

- **F05-01:** separate A/B/C lanes; arrows only travel within each alternative to independent decision/effect; no implied sequential maturity path. All outcomes evaluated under identical rules.
- **F05-02:** distinguishes independently validated benefit, incremental lifecycle cost, expected monetary loss, and *separate* hard constraints. The final design removed the semantic error of trying to subtract nonmonetary hard constraints.
- Both figures: authored in editable plain SVG at `5.75in` source width; rendered SVG and PNG present and reproducible using `make figures`; navy strokes, pale-blue process, amber independent decision/risk, green for **validated** benefits, clean straight arrows; no line crossings or collisions observed in standalone inspection or LibreOffice-rendered manuscript pages 75 and 77.
- `make book-docx` embeds the **exact PNG SHA-256 bytes** produced by the current masters; `check_ch05_acceptance.py` checks this against Word media.
- The annual economics table initially split over pages. A deterministic Word postprocessing rule now keeps its rows together; in LibreOffice print review the entire table is on page 78.
- Native Word for Mac layout was **not** executed; acceptance remains open until author views chapter 5 figures, captions, economics table and page breaks there.

## QA execution and remaining acceptance

Checks executed: `make figures`, `make check`, `make book-docx`, `make check-figures`, `make qa`, native SVG XML parsing, direct economics assertions, PNG/Word-image SHA matching, LibreOffice DOCX-to-PDF render, print-page review for F05-01/F05-02 and full comparison table, and baseline-safe installer preflight tests in local replicas.

Source bibliography: NIST AI RMF (2023, MAP 3); FinOps Foundation (Framework 2025 and Unit Economics capability); existing Bass/Clements/Kazman, Gray/Reuter, Kleppmann sources. Scenario numbers are **illustrative** and clearly marked. No vendor or production data was used as a claimed benchmark.

**Open review gate:** Microsoft Word for Mac may paginate differently than LibreOffice. Author should inspect chapter 5 pages and figure captions on the locally rebuilt `dist/etis-agentic-ai-book.docx`; do not freeze until this passes. Also, local `main` after the Chapter 4 merge must match the V2 baseline hashes; installer refuses unknown versions and never overwrites them blindly.
