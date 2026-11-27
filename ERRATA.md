# First-edition errata — Engineering Agentic AI Systems

[Home](README.md) · [Issue tracker](https://github.com/etis-framework/etis-agentic-ai-book/issues) · [Release history](CHANGELOG.md)

**Applies to:** First Edition (2026), paperback ISBN **979-8-9966760-6-4**, hardcover ISBN **979-8-9966760-7-1**, companion baseline **`v1.0.0`**. This document is a controlled list of **confirmed** corrections to the printed edition or its matching companion. Absence of entries is not certification that no errors exist.

## Submit a reproducible correction

Open an [errata issue](https://github.com/etis-framework/etis-agentic-ai-book/issues/new?template=errata_report.yml) with edition, page/chapter or exact source path, printed/existing text or behavior, proposed correction, and supporting evidence. **Do not submit vulnerabilities publicly**; see [SECURITY.md](SECURITY.md). Avoid lengthy copyrighted passages.

## Confirmed errata

The following register distinguishes published companion corrections from verified changes awaiting a new release. No printed chapter changes are required.

| ID | Affected page / file | Description | Correction or workaround | Status | First fixed in |
|---|---|---|---|---|---|
| ETIS-E001 | Builds 2–4: identity and finance verifiers | Malformed non-ASCII signatures could escape typed denial; Build 3 worker could terminate | Validate ASCII before digest comparison; test denial and worker survival | Released | v1.0.1 |
| ETIS-E002 | Builds 3–4: IPC | Ambiguous or excessively nested JSON could evade controlled rejection | Strict decoding and bounded rejection | Released | v1.0.1 |
| ETIS-E003 | Build 4: adapter, ledger, service | Unresolved replay could report DENIED; read-only inquiries could create stores; malformed observations could raise unexpected errors | Preserve UNKNOWN, nonmutating inquiry and typed validation; close connections | Released | v1.0.1 |
| ETIS-E004 | Builds 1 and 5 | Valid long correlation identifiers and extreme lease timestamps could violate contracts | Bounded identifiers and timestamp validation | Released | v1.0.1 |
| ETIS-E005 | Chapter 28 reliability; Chapter 30 operations | Invalid states, confirmation before dispatch, empty telemetry | Typed rejection, escalation and explicit missing-evidence handling | Released | v1.0.1 |
| ETIS-E006 | Chapter 31 assurance | Skipped or incomplete test results, missing dependency hashes and source drift could undermine evidence | Require actual passing execution and stable source hashes | Released | v1.0.1 |
| ETIS-E007 | Companion release verification runner | Empty or skipped test suites could return success without complete execution | Require actual ordinary unittest results, minimum suite inventory and fresh completion records | Included in v1.1.0 | v1.1.0 |

## Change control

1. Triage and reproduce reports against the reported release tag, the immutable original baseline where relevant, and the matching printed edition.
2. Confirm whether the issue affects print text, companion behavior, or both.
3. Record a stable erratum ID, affected page/source, impact, correction, and status here.
4. Publish companion fixes in a **new** patch tag (`v1.0.1`, etc.); never move or rewrite the first-edition tag.
5. Treat future print-edition revisions separately from existing copies and point readers to applicable edition information.

Publishing an erratum does **not** alter the frozen first-edition manuscript automatically.
