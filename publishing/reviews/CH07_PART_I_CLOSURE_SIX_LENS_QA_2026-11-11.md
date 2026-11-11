# Chapter 7 and Part I — six-lens integration and QA record

**Review status:** Chapter 7 substantive draft; deterministic QA and LibreOffice print-layout review completed; native Microsoft Word for Mac editorial acceptance not performed. This document does not claim that an unpublished architectural implementation has passed these example requirements.

## Baseline and scope

Source baseline: local copy of Chapter 6 final installer-test result (the files from the Chapter 6 corrective patch). The actual user's remote GitHub HEAD was not fetched or inspected; SHA-256 installer preflight must verify the user's Chapter 7 branch before writes. Scope: front matter through Chapter 7, Part I opener, source register, figure masters, automatic checks and QA documentation. No changes to the substantive Chapters 1–6 prose or existing figures.

## Six-lens adversarial reading, front matter–Chapter 7

| Lens | Challenge asked | Result / disposition |
|---|---|---|
| Practitioner / implementation engineer | Is each requirement observable in controller code, tests, and runbooks, rather than a prompt? | AUTH-01, PAY-03 and the requirements record provide triggers, owner, observable denial or reconciliation, and failing conditions; detailed implementation deferred to Part II onward |
| Enterprise architect | Does Chapter 7 prematurely prescribe an agent framework or conflict with B/C choices? | Solution-neutral requirements; Design B is conditional production candidate, C is evaluated read-only; no agent payment capability |
| SRE / reliability and incident response | What happens after a lost provider acknowledgment; can operators determine external state? | `RF-1042` stable illustrative identity, payment-operation UNKNOWN, reconciliation/escalation, `OPS-01` and `PAY-03` fault tests; no new unapproved provider attempt |
| Security, privacy, governance | Do policy and tenant boundaries survive prompt injection, stale approval and cross-tenant retrieval? | `AUTH-01`, `POL-02`, `DATA-01`, deny trace, credential isolation and release blocking defects; NIST and ISO sources are contextual, not certification claims |
| Executive / finance | Does the gate honor the Chapter 5 economic case but prevent business benefit from overriding safety? | Separate business-value pilot and mandatory authority/isolation gate; quantified thresholds belong to enterprise owners, not the author |
| Instructor / critical reviewer | Can students distinguish requirements, test evidence, architecture intent, and observed operational state? | Two figures, two compact requirement matrices, six exercises, explicit distinction of diagram versus observed evidence |

## Running-example regression

- Customer, intent, and case unchanged: $500 refund, `CASE-204`.
- Design A: deterministic comparison baseline. Design B: conditional production candidate with advisory AI. Design C: evaluated read-only investigator, not autonomous payment agent.
- Trusted enterprise workflow owns eligibility policy verification, approval, durable intent, and payment adapter. Model output never grants financial rights.
- `RF-1042` remains *illustrative* stable provider-operation identity; no provider-specific idempotency guarantee asserted.
- Payment-operation `UNKNOWN` is distinct from case-level `OUTCOME_UNKNOWN`. Neither is silently interpreted as payment failure or permission to resubmit.
- Chapter 6 four uncertainty classes are converted to engineering contracts; Chapter 7 does not establish an additional conflicting uncertainty taxonomy.

## Earlier material changes

- Part I opener: status updated from Chapters 1–6 substantive/Chapter 7 planned to Chapters 1–7 substantive draft, without declaring final publication acceptance.
- Chapter 6 checker: its old Part I status assertion is made compatible with the newly drafted Chapter 7; no weakening of other Chapter 6 gates.
- Source register: explicit Chapter 7 source scope and original ETIS requirement identifiers.
- No prose changes in Chapters 1–6, and no change to the prior example's decision rights.

## Figures: mandatory V9 inspection

- `F07-01`: editable SVG master, exact 5.75-inch width; navy lines, pale blue process, amber independent authority, green evidence record; clean orthogonal routes, visible arrowheads, distinction between requirements and observed evidence. Visually inspected standalone and in print-layout PDF page 94.
- `F07-02`: editable SVG master, exact 5.75-inch width; evidence/control inputs, amber accountable release authority, green conditional GO, pale red HOLD (not green); orthogonal connectors and no label/arrow collision after correction. Visually inspected standalone and in PDF page 96.
- PNG compatibility render width 1800px; SVG source and rendered copy are byte-identical. DOCX media ZIP SHA-256 fingerprints compared to current PNGs by `check_ch07_acceptance.py`.
- Figures and captions printed together on their respective pages in LibreOffice conversion. Native Word for Mac **not tested here**.

## Page-budget ledger (7×10-inch)

| Measure | Value / status |
|---|---|
| Chapter 7 | 2,280 of 2,900 source words; 620 below cap |
| Chapters 1–7 | 23,060 of 25,800 allocated source words; 2,740 below cumulative cap |
| Printed Chapter 7 | PDF pages 90–98 inclusive = **nine pages** (Part II divider starts page 99) |
| Current manuscript including Chapters 8–36 placeholders | 140 pages; **not** a final-book projection |
| Whole-book allocated chapter words | 117,800; 36 chapters |
| Preferred finished-book target / preferred max / planning limit / absolute cap | 550 / 575 / 600 / 700 pages |
| Planning text-only conversion | 117,800 / 280 + 50 front/back reserve ≈ 471 pages before figure/table/pagination overhead |
| Target overhead capacity at full allocations | ≈ 79 pages; not a promise. At current Part I word saving, theoretical additional buffer ≈ 10 pages if later chapters stay on their allocations |

**Editorial risk:** chapters 8–36 still contain placeholders; later architecture and operating-system material could exceed source caps or acquire large diagrams/tables. The 79-page overhead allowance is global, not 79 pages available per part. Maintain an actual print-page ledger at each Part/Chapter milestone; require an explicit trade-off before adding substantial figures or length. Chapter 7's nine pages do not mean that a 550-page finished book is assured.

## Executed checks and qualifications

- `make figures`: completed; SVG masters copied and PNGs re-rendered.
- `make book-docx`: completed.
- `make check`, `make check-figures`, `make qa`: completed with no reported failure after the Chapter 6 checker status fix.
- `check_ch07_acceptance.py`: enforces words, continuity terms, 5.75-inch SVG, master/render identity, PNG signature, and exact embedded Word media hashes. These are mechanical checks, **not** image aesthetics or semantic proof.
- LibreOffice PDF: 140 pages, 7×10 inches. Chapter 7 pages 90–98 and figures on 94 and 96 visually reviewed.
- Native Word for Mac, exact publisher imposition, and full source-by-source citation verification remain outside the executed gates.

## Part I disposition

**Part I substantive draft is complete, not editorially frozen.** Release of Chapter 7 patch can proceed after local installer preflight and the author's native Word-for-Mac visual acceptance. Before Part II grows, ratify a part-by-part *printed page* allocation, not just aggregate word caps; Chapter 8 should inherit the Part I requirements baseline without repeating it.
