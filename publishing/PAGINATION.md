# Pagination — recto chapter openings

For the 7 × 10 inch print edition, chapters and part openers begin on an **odd-numbered (right-hand/recto) page**. The generated DOCX receives Word `oddPage` section breaks after Pandoc assembly. Word may insert a blank verso page to achieve this. Do not delete these intentional blanks.

This is a print-layout convention, not a claim that front matter, folios, running heads, TOC, or PDF press files are finalized. Page numbering and separate front-matter roman numerals remain publication tasks.

Build: `make book-docx`. Inspect with Word in print layout. Section-break behavior should be confirmed in Word for Mac before print release.
