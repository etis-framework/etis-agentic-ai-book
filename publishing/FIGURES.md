# Figures and publishing integration

- **Editable source:** `assets/shared-figures/sources/*.dot` (Graphviz).
- **Vector output:** `assets/shared-figures/rendered/*.svg` (preferred scalable master).
- **DOCX compatibility:** `assets/shared-figures/rendered/*.png` (180 dpi generated rendering). Markdown currently references PNG to ensure reliable embedding in Word; SVG remains the vector publication master.
- **Build:** `make figures` regenerates both formats; `make check` validates references; `make book-docx` generates `dist/etis-agentic-ai-book.docx`.
- **QA:** `python3 publishing/scripts/check_figures.py` checks embedded media for built DOCX files. Visually inspect print-size readability and layout before publication.
- **New figures:** F01-01 (engineering inheritance), F01-02 (workflow comparison), F02-01 (lost acknowledgment). They are **new instructional drafts**, not CAB-001-certified architecture diagrams.
- **Existing 22 CAB-001 figures:** retained, with SVG and PNG generated from DOT. Not automatically inserted; placement requires editorial approval.
- **Word warning:** The field-update prompt is a separate issue. These image references are embedded by Pandoc; the patch does not claim to resolve every Word field prompt.
