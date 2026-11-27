# Contributing and reporting

[Home](README.md) · [Engineering standard](examples/refund-reference-system/ENGINEERING_STANDARD.md) · [Errata](ERRATA.md) · [Security](SECURITY.md)

Please open a descriptive issue before proposing changes to contracts, teaching guarantees, or public navigation. For a bug report, identify the **version/tag**, OS, Python version (native or container), Docker/Compose versions and image architecture if applicable, exact command, expected behavior, observed behavior, and smallest safe reproduction. Do not share real customer information, credentials, exploits, or private reports.

For code changes, preserve the frozen **CAB-001** architecture (E1–E9/C01–C09), CASE-204/$500/RF-1042 identity and independent transaction authorization. Update the matching build README, `architecture.svg`, tests, and traceability when applicable. Run `make check-companion` before proposing a PR, or run `python3 publishing/scripts/test_companion_release.py -v`, `python3 publishing/scripts/check_companion_release.py` and `python3 publishing/scripts/check_active_reader_links.py` separately if Make is unavailable. Use the [companion contribution policy](examples/refund-reference-system/CONTRIBUTING.md).

**Do not change book manuscript or print artifacts in companion corrections.** First-edition print errors go through [ERRATA.md](ERRATA.md). Historical editorial/QA documents are records, not current release instructions. Contributions are subject to [RIGHTS.md](RIGHTS.md); submitting a PR does not imply rights to republish the commercial book.
