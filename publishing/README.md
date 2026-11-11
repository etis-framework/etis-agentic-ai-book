# Publishing pipeline

Pandoc is the primary assembler. `book.yaml` is the ordered manuscript manifest. Use `make chapter CH=01 FORMAT=docx` or `make book-docx`. PDF output requires an installed LaTeX engine; availability is checked before invoking it. Generated files are written to `dist/` and are not source of truth.

This scaffold supports DOCX builds, basic validation, and PDF when a compatible LaTeX engine is installed. It is **not** yet a final print-layout pipeline: cross-reference numbering, indexes, typography, figure semantics, and bibliography citation QA remain gated.


See `BOOK_PRODUCTION_QA_V4.md` for current publishing acceptance gates and unresolved print-layout requirements.
