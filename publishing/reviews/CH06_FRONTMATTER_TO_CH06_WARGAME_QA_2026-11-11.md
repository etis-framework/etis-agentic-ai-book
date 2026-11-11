# Chapter 6 — Front matter through Chapter 6: integration and production QA

**Review date:** 2026-11-11. **Reference baseline:** Chapter 5 corrected installer test copy, not a live GitHub branch checkout. **Acceptance:** substantive draft; NOT frozen pending author's native Word inspection.

## Source reconciliation and scope

- Chapter 6 approved title: **Uncertainty, Authority, and Enterprise Trust**; new substantive prose replaces its BP-001 placeholder.
- Part I opener now says Chapters **1–6** drafted, Chapter **7** planned; no rewriting of Chapters 1–5 was necessary to maintain the running example.
- Chapter 3 Design **B** remains the first production candidate (subject to pilot and control gates); Chapter 4 Design **C** is strictly read-only and investigative; Chapter 5 compares the economic variants; Chapter 6 adds uncertainty and authority discipline. No agent payment authority introduced.
- Original case `CASE-204`/$500 and illustrative operation ID `RF-1042` are unchanged; **UNKNOWN** is the operation-level state, **OUTCOME_UNKNOWN** is the case-level state. Provider behavior and idempotency are explicitly contract-dependent.
- Bibliography already contained all referenced Chapter 6 source identities, including NIST AI 100-1, NIST AI 600-1, OWASP agentic 2026 (released Dec 2025), Parasuraman 2000, Gray & Reuter 1992, Kleppmann 2017. Source-register chapter mapping added; no fabricated provider behavior.

## Six-lens adversarial reading — front matter to Chapter 6

| Lens | Challenge and defense | Disposition |
|---|---|---|
| Practitioner engineer | Can a timeout be misread as failed payment, inviting a duplicate? | No: separate payment state UNKNOWN, durable correlation, reconciliation and no assumed provider idempotency (§6.5, Fig 6.2) |
| Enterprise architect | Does a model score cross the authorization boundary? | No: assessment is an input; identity, policy and approval independently enforce the gate (§6.3, Fig 6.1) |
| Reliability / operations | Is an unresolved effect owned and recoverable? | UNKNOWN stays visible, same operation ID, operator escalation and supporting external evidence before closure (§§6.5, 6.7) |
| Security / governance | Can document text, credentials, or changing tools expand scope? | No: read-only bounded investigation; per-step identity, tenant, policy, expiry checks; no payment tools (§§6.3, 6.8) |
| Executive / finance | Does economic attractiveness confer deployment permission? | No: Chapter 5's comparative value is distinct from Chapter 6's hard gates, Design B conditional, C experimental (§§6.1, 6.9) |
| Instructor / critical reviewer | Is the argument assessable rather than aspirational? | Four uncertainty classes, falsifiable acceptance matrix, six exercises with negative tests; Chapter 7 will formalize requirements (§§6.2, 6.7, 6.9) |

**Editorial boundary:** Chapter 6 introduces the conceptual control-and-uncertainty register but leaves detailed formal requirements to Chapter 7, identity architecture and implementation to later parts. It avoids re-teaching the complete transactions chapter.

## Layout and figure gates (actual checks)

- Figure masters `F06-01.svg` and `F06-02.svg`; 5.75-inch declared width; hand-controlled orthogonal routes, no label crossing observed. Rendered SVG exact-byte copies; PNGs generated through `cairosvg` at 1800px width.
- Print layout: **7×10-inch**, LibreOffice conversion of the generated Word; **132 pages total**, including *planned* Chapters 7–36. Chapter 6 begins PDF page **82** and Chapter 7 begins PDF page **90**, so **eight pages** for Chapter 6. Figure 6.1 is on page 84; Figure 6.2 is on page 86. Their captions are together with their images. Page review on PDF pages 82–89; image/contact-sheet inspection.
- `make figures`, `make book-docx`, `make check`, `make check-figures`, `make qa`: PASS in the authoring repository; current Word ZIP includes exact SHA-256 of F06 PNGs.
- **Pending**: native Microsoft Word on Mac visual inspection; independent external technical/citation expert certification; actual later-chapter pagination cannot be established from stubs.

## Single-volume budget and pressure management

| Chapter | Actual words | Approved cap | Remaining |
|---|---:|---:|---:|
| 1 | 3,783 | 3,900 | 117 |
| 2 | 5,269 | 5,400 | 131 |
| 3 | 4,070 | 4,300 | 230 |
| 4 | 2,985 | 3,000 | 15 |
| 5 | 2,325 | 2,900 | 575 |
| 6 | 2,348 | 3,400 | 1,052 |

First six chapters total **20,780 substantive source words** against **22,900 allocated**; **2,120 words under cap**. The project-wide 36 chapter caps total **117,800 words**. At the planning assumption of **280 effective words per page**, plus **50 pages** reserved for front/back matter, the text allocation projects to approximately **471 pages** before extra figure/table/pagination overhead. A **550-page** working target leaves approximately **79 pages** for that overhead; preferred maximum 575, planning limit 600, absolute maximum 700. This is a *forecast*, not a confirmed finished book page count. Do not spend Chapter 6's word headroom to make it longer without content justification: Parts II–VI will require larger evidence and implementation allocations. Chapter 7 cap is **2,900 words**. Retain a running printed-page ledger for every chapter.

## Changes outside Chapter 6

The only earlier source change is the Part I status sentence (Chapters 1–6 drafted), along with the Makefile QA invocation and source-register mapping. No undisclosed edits to Chapters 1–5. The historical Chapter 4 and Chapter 5 native Word signoffs are not upgraded by this build; their previous statuses remain as recorded.

## Gates for the next release

1. Apply the hash-checked archive to the existing `docs/ch06-development` branch; **do not create a new branch**.
2. Run the Word build **before** acceptance/check when a stale `dist` file exists, then run all checks.
3. Inspect figures and surrounding pages at 100% in native Word for Mac before commit/PR; compare PDF page semantics as secondary evidence.
4. Keep Chapter 7 to its **2,900-word cap** and integrate the control-and-uncertainty register as measurable requirements rather than duplicating this conceptual chapter.
