# Publishing source and QA — maintainer guide

[Repository home](../README.md) · [First-edition release policy](../RELEASE.md) · [Historical development reviews](reviews/README.md)

This directory holds the **source-based manuscript assembly tools**, figure processing, print-related checks, and dated development QA evidence for *Engineering Agentic AI Systems*. The frozen first-edition manuscript is maintained separately under `manuscript/`. **The public companion can be cloned and tested without building the book**; see [Getting Started](../docs/GETTING_STARTED.md).

## Current source-build entry points

From the repository root, on a development machine with the required publishing tools:

```sh
make book-docx
make check
```

`book.yaml` declares title, edition identity, and source assembly configuration. `publishing/scripts/build.py` assembles document formats, and `make check` runs **source, manuscript, figures, and companion engineering checks**. Generated artifacts belong in ignored `dist/` and are not authoritative source material. A local source-generated DOCX or PDF is **not automatically** the separately approved KDP print interior.

For the independently supported **companion-only** check, use `make check-companion` or `python3 publishing/scripts/check_companion_release.py` on macOS/Linux. This executes the ten local fixture suites without Word, Pandoc, Graphviz, or a payment service.

## Print production versus repository checks

The final 7 × 10-inch, 503-page interior was prepared and checked as an author-approved **Word-for-Mac / PDF publishing artifact**. The source build pipeline and static QA are reproducibility aids; they do not recreate all native Word layout operations, updated page-number fields, print-proof inspection, or KDP approval automatically. Do not treat a green `make check` as independent print certification.

See [Mac build instructions](BUILD_ON_MAC.md), [figure generation and source exceptions](FIGURES.md), and [pagination conventions](PAGINATION.md). Dated `BOOK_PRODUCTION_QA_V4.md`, `PRODUCTION_QA_V6.md`, certification passes, and files in [reviews](reviews/README.md) preserve **historical checkpoints**, not current unresolved release blockers by default. Validate any claim against the actual release candidate and its acceptance evidence.

The original GitHub `v1.0.0` launch and `v1.0.1` maintenance release are complete; subsequent companion publication and tagging remain separately governed by [RELEASE.md](../RELEASE.md). No tag or release is created by these instructions.
