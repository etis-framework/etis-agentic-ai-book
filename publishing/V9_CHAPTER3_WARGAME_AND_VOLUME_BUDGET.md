# V9 — Editorial war game and Chapter 3 comment disposition

## Reader-comment dispositions

1. **Figure typography:** Agree. All four Chapter 3 figures now use a common Arial node-face and 22–23 pt source labels, rather than inconsistent 18–21 pt settings. These are source sizes, not proof of final effective print sizes; inspect the embedded 5.75-inch figures at actual 7 × 10 trim.
2. **Small figures:** Agree. Rebuilt all four as taller print-first layouts, with shorter labels and less visual clutter. The prior left-to-right five-node chain compressed too much at 5.75 inches.
3. **E1–E9 shorthand:** Agree. Removed both Chapter 3 uses of E1–E9 and retained responsibility names. The numerical codes belong in the architecture reference/traceability register, not in narrative exposition.
4–5. **Figure consistency:** Agree. Same box, type, arrow, and color rules across four diagrams. A programmatic acceptance gate remains necessary before additional chapters.
6. **Code-like contract:** Agree with the intent: present it as an indented fixed-width code block, not a prose table. The Markdown source already uses a fenced YAML block. This revision explicitly identifies its typesetting and wrapping requirements. Verify Word's code-block style and line wrapping; changing the Markdown alone cannot certify the publisher's Word rendering.
7. **Bent arrows:** Agree. Figure 3.4 now uses orthogonal routing and a vertically ordered, shared execution destination. Routing may still include right-angle elbows because three alternatives converge on one shared gate; the critical question is whether edges remain unambiguous and non-overlapping at print size.

## Six-lens war game

- **Beginning engineer:** Chapter 3 has strong examples, but the reader needs a consistent progression from business outcome to requirements, autonomy allocation, enforcement, and evidence. Avoid premature architecture abbreviations.
- **Enterprise architect:** Maintain the distinction between logical responsibilities, deployable components, business authorities, and systems of record. Show trade-offs before reference patterns.
- **AI/agent engineer:** Preserve the distinction between model proposals and trusted tool execution; explain runtime constraints and failure modes with concrete traces.
- **Security and SRE:** Reuse the lost-acknowledgment/UNKNOWN example as a recurring invariant; do not re-explain transaction fundamentals in every chapter. Explicitly test prompt-injection boundaries and revocation.
- **University instructor:** Each chapter should teach one dominant concept, one developed example, one decision method, and exercises whose answers require engineering judgment rather than terminology recall.
- **ETIS editorial reviewer:** Preserve named evidence artifacts, quality attributes, decision ownership, and operational recoverability; maintain a cumulative concept register and source verification ledger.

## Thread-continuity contract

1. **Single running case:** $500 customer refund; stable operation identity, independent authorization, durable UNKNOWN and reconciliation remain invariant.
2. **Concept first, notation second:** Introduce the descriptive name at first use; reserve E-codes and C-codes for cross-reference tables and appendices.
3. **No repeated mini-chapters:** Define business process/autonomy in Chapter 3; agent mechanisms in Chapter 4; economics in Chapter 5; uncertainty/authority in Chapter 6; requirements in Chapter 7; architecture in Part II; implementation in Part IV; production operations in Parts V–VI.
4. **Same evidence spine:** decision record → contract → test → runtime observation → incident/recovery evidence.
5. **Scope discipline:** examples must explicitly distinguish illustrative assumptions from normative standards or verified product behavior.
6. **Figures as teaching tools:** one claim per figure, standard visual grammar, readable at actual printed width, and no unexplained identifiers.

## Single-volume budget (planning estimate, not a measured pagination result)

- 36 chapters averaging 4,000–4,600 words: 144,000–165,600 words.
- At an effective 300–350 words per 7 × 10 printed page (after headings/tables), core prose alone could occupy roughly 410–550 pages.
- Figures, exercises, references, front matter, and section-start whitespace may add 90–160 pages.
- **Working range: 500–710 pages.** An unconstrained 5,500–6,000 words per chapter could push toward 750–900 pages, making one-volume handling and cost increasingly unattractive.
- **Recommended design target: 560–650 pages**, soft ceiling 680 pages, and an editorial checkpoint at completion of Part I and Part II. This is a production target, not a claim about the current mostly-placeholder manuscript.
- Allocate roughly 150,000–160,000 main-text words across the 36 chapters, with chapter-specific budgets. Some architecture and implementation chapters deserve 5,000–6,000 words; shorter overview/reference chapters should compensate.

## Outstanding gates

- Word-for-Mac 7 × 10 print-size verification of all four figures and YAML block (including wrapped lines).
- Citation-level verification and authoritative 2025–2026 technical source update.
- Establish a machine-readable chapter/figure/terminology acceptance report, not just a written style standard.
- Check that the Chapter 3 code example and diagrams are not duplicated verbatim later in the book.
