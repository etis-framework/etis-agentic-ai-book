# ETIS print-first figure standard — V3

Seven chapter figures are now authored as **editable SVG source masters** under `assets/shared-figures/sources/`, and exported to `assets/shared-figures/rendered/` as SVG and high-resolution PNG. The original CAB-001 figure assets remain unchanged.

- Figure labels are sized for the 7 × 10-inch trim; review at actual page size, not zoomed.
- Each figure has one main lesson. Captions provide the editorial interpretation; avoid large secondary legend boxes.
- Verify clearances between text, boxes, arrows, and lifelines. Sequence steps must remain unambiguous.
- Figure 2.4 is a simplified logical view, not a complete E1–E9 deployment diagram. Business system of record and durable operational state are different responsibilities.
- Review both figure semantics and rendering. The image-count check is necessary but not sufficient.
- `make check` validates source without requiring a recent build; `make book-docx` builds then validates embedded images.
- Chapter recto starts are enforced by odd-page section breaks, with no additional heading page break. Word for Mac remains the final authority for print pagination; check two-page spread view.
