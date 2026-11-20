# Figure sources, generated renditions, and publishing integration

[Publishing overview](README.md) · [Repository home](../README.md)

Not all figures use the same editable master format. **Do not regenerate an SVG-authored diagram from an obsolete DOT file.**

- **DOT-authored figures:** editable Graphviz sources, when present, are in `assets/shared-figures/sources/*.dot`. The figure script uses DOT to produce renditions where no authoritative SVG master supersedes the DOT source.
- **SVG-authored figures:** editable SVG masters are in `assets/shared-figures/sources/*.svg` for some diagrams. For the seven early F01/F02 diagrams, their individual `*.README.md` files explicitly identify the SVG in `assets/shared-figures/rendered/` as the editable master. Inspect the figure-specific note before changing its source.
- **Output and compatibility:** `assets/shared-figures/rendered/*.svg` provides scalable vector artwork; `*.png` is used for Word-compatible image embedding. Source-linked assets and checked-in rendered artwork are different concerns.
- **Regeneration:** `make figures` invokes `publishing/scripts/figures.py`. It requires Graphviz (`dot`) for DOT masters and may require Python `cairosvg` for fresh PNG renditions of SVG masters. Regeneration can update committed art; review each diff rather than assuming byte-identical results.
- **Verification:** `make check` checks source references and figure constraints. `python3 publishing/scripts/check_figures.py --built` validates built DOCX image integration where applicable. Manual inspection at the actual 7 × 10 print size remains required.

CAB-001 architecture figures, pedagogical diagrams, and reference-build `architecture.svg` diagrams serve **different purposes**. A successful render does not prove architectural correctness or print certification. Preserve approved architecture semantics and the frozen print artifacts.
