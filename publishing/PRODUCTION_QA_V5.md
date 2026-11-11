# ETIS V5 production acceptance and remaining limitations

## Changes in this revision
- Removed dedication and optional acknowledgments from the publishing assembly.
- Moved contents after copyright; replaced static draft navigation with a Word TOC field.
- Added substantive preliminary reader orientation and separated back-matter stubs.
- Introduced Roman preliminaries and Arabic pagination beginning at Chapter 1 using Word section properties.
- Eliminated the additional blank section-break paragraph that could strand chapter headings.
- Restructured Chapter 2 so inherited disciplines precede architectural synthesis and design review; expanded ACID at first use.
- Corrected Figure 2.4 to show trusted execution directly owning durable operation-state changes, while the provider adapter reports observations and the payment system remains authoritative.
- Applied Word comment-driven clarity edits to Chapter 1, including explaining E5, avoiding unexplained CAB-001, replacing “agency,” and moving Figure 1.1 into the refund example.

## Word for Mac acceptance tests (not certified by LibreOffice)
1. In Word choose References > Update Table > Update entire table to populate the TOC page numbers. Save the result.
2. Check Roman folios in front matter and Arabic page 1 on Chapter 1.
3. Confirm each Part/Chapter starts on an odd recto page; Word and LibreOffice can differ in oddPage section pagination.
4. Confirm no chapter heading is isolated from its first narrative paragraph.
5. Confirm every figure at actual 7×10 print size and inspect the provider/ledger relationship in Figure 2.4.
6. Confirm front matter and back matter contain no unintended dedication, acknowledgments, or obsolete figure-list stubs.

## Editorial debt deliberately not represented as complete
- All historical priority claims need verified primary/secondary sources and bibliography entries.
- Chapters 3–36 are stubs, and the index and appendices are controlled placeholders.
- Publisher, rights holder, ISBN, edition, and author byline must be confirmed.
- The source figure register and all 29 diagrams require complete technical and print QA before publication.
- A final professionally typeset PDF needs a separate print acceptance gate.

The build can validate section XML and figure embedding. It cannot prove Word-for-Mac recto pagination without a native Word render.
