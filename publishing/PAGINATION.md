# Pagination — first-edition print-layout conventions

The first-edition 7 × 10-inch layout places chapter and part openers on **odd-numbered (right-hand/recto) pages**. The source-to-DOCX publishing pipeline inserts Word `oddPage` section breaks after Pandoc assembly; Word can add a blank verso page to honor the next recto opening. Those blank pages are intentional and should not be removed merely to make pages consecutive.

The final reader-facing print page numbers, Roman-numeral front matter, running heads, tables, figures, contents and index are governed by the **author-approved Word/PDF interior supplied to KDP**, not by an intermediate generated file or GitHub CI. Differences between a generated DOCX and the approved KDP interior do not make the generated file the print authority.

**Maintainer reference:** `make book-docx` creates a reproducible source-derived DOCX for engineering inspection. Use Word in Print Layout to inspect section transitions. Companion-code verification (`python3 publishing/scripts/check_companion_release.py`) is a separate procedure and does not certify press-ready pagination.
