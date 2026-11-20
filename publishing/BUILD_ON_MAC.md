# Build the manuscript source on macOS — maintainer reference

[Publishing overview](README.md) · [Repository home](../README.md) · [Companion quickstart](../docs/GETTING_STARTED.md)

This replaces the obsolete **V6 patch extraction procedure**. The current repository already contains the integrated source files; do **not** apply old tar patches or assume historic generated Word files match the final KDP interior.

From the root of a clean checkout:

```sh
make book-docx
make check
open dist/etis-agentic-ai-book.docx
```

Manuscript assembly uses the repository's Pandoc/Word publishing toolchain; inspect `publishing/scripts/build.py` and `Makefile` for commands and local dependencies. If a tool is missing, install it for your local build environment rather than altering book source or silently skipping a check. Source builds write generated files into ignored `dist/`.

**Important:** The authoritative publication interior uses native Word-for-Mac layout work, updated TOC/index and page fields, and a separately reviewed export to PDF. A regenerated DOCX is **not** proof that those native operations or final pagination have been reproduced. Follow the author's print-production approval process before replacing any book file.

For **companion tests only**, no Pandoc, Word, or publishing dependencies are required:

```sh
python3 publishing/scripts/check_companion_release.py
```

This companion command supports macOS/Linux for the full ten-suite check. Use the `--portable` flag for the limited Windows subset, as documented in the [reader quickstart](../docs/GETTING_STARTED.md).
