# V4 book production QA — November 2026

## Verified corrections
- Explicit ordered front matter; no automatic Pandoc `--toc` ahead of the title.
- Separate copyright, dedication, contents, preface, acknowledgments, introduction, and reader guide stubs.
- Separate back matter sources for appendices, glossary, references, lists, author biography, and index.
- Chapter and Part titles use dedicated `oddPage` section breaks rather than section properties attached to the preceding content paragraph. First text stays with heading.
- Build validated with seven embedded figures; 36 chapter inventory intact.

## Reader and publication war game — open items
1. The current chapters 1 and 2 are strong in the business-to-engineering progression, but Chapter 2's sections 2.13–2.19 read like a second chapter appended after an already completed conclusion at 2.12. In the next manuscript pass, integrate security, data, governance, and ACID into the earlier historical narrative; avoid repeated ACID and architecture claims.
2. Chapter 1's front-loaded 'who this book is for' passage overlaps the front-matter reader guide; decide whether to retain only a short bridge in Chapter 1.
3. History needs verified in-text sources and bibliography. Do not present draft source-register placeholders as publication-ready references.
4. Figure 2.4's arrow from provider adapter to durable state may misleadingly imply only adapter writes state; the prose clarifies broader durable workflow ownership. Review the relationship in the figure master before freezing.
5. The glossary, bibliography, figure/table lists, index, and legal pages are controlled stubs; they are not finished content.
6. Word-for-Mac recto pagination must be confirmed in Word itself: LibreOffice rendering does not reliably honor odd-page section parity. Do not infer recto success from a PDF exported by LibreOffice.
7. The contents list is intentionally a *draft navigation list without page numbers*. Final publication requires a real generated, page-numbered TOC from the frozen print pagination, not a manually maintained list.
8. Part openers are placeholders and currently consume pages; confirm their final design before assigning running heads, page numbering, and blank-verso conventions.
9. Front-matter folios (Roman numerals), main-text Arabic folios, running heads, print bleeds, and orphan/widow control are not yet certified for publication.
10. Copyright/ISBN/imprint and permissions are unapproved; never reuse other ETIS book ISBNs.

## Word-for-Mac acceptance test
Open the DOCX in Word for Mac. Inspect Chapter 1, Chapter 2, and at least one transition between Parts. Each Chapter title and its first body paragraph must be on the same page. Every Part and Chapter should start on an odd/right-hand page (blank versos permitted). Check no phantom blank rectos and no heading-only pages. Update layout and page counts after any change.
