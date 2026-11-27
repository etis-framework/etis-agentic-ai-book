# Change history

[Home](README.md) · [First-edition release notes](RELEASE_NOTES_v1.0.0.md) · [Release policy](RELEASE.md) · [Errata](ERRATA.md)

## v1.1.0 — Containerized development and reproducible execution

- Add digest-pinned, non-root Linux verification and development image targets; preserve all native execution paths.
- Add Docker Compose, Make convenience targets, and an optional VS Code Dev Container configuration.
- Separate read-only, offline, image-contained verification from editable development, persistent exercise state and evidence export.
- Preserve all ten fixture suites (171 baseline tests), seven existing runner regressions and the active reader-link gate; add container tooling regressions and multi-architecture CI acceptance.
- Harden runtime images: remove unnecessary packaging tools, omit Git from development, strip setuid/setgid bits from regular files under `/usr`, and remove `infocmp` from verification only.
- Pin signed Debian snapshot inputs and add multi-architecture vulnerability scanning, SBOMs, installed package inventories and runtime applicability evidence.
- Retain all raw scanner findings and enforce exact, time-limited maintainer dispositions; critical, new or changed unassessed high, high with a supported fix, and expired decisions for outstanding findings block. Weekly CI monitors the dependency baseline.
- Document container trust limitations, platform acceptance, state lifecycle and image maintenance. Thank Sean for proposing container-based execution.

### Repository maintenance included in v1.1.0

- Align reader navigation with the published corrected release and distinguish historical release records from active instructions.
- Fail closed when companion verification discovers or executes too few tests, skips tests, or fails to complete; report actual suite totals.
- Check active reader Markdown link targets, pin native CI actions, and ignore disposable exercise output.

## v1.0.1 — Companion adversarial validation and assurance maintenance (2026-11-26)

- Reject malformed identity and finance signatures and ambiguous JSON at the request boundary; preserve service availability and independent approval.
- Preserve unresolved financial outcomes on replay and make status inquiries nonmutating.
- Harden advisory identifiers, recovery evidence, lease timestamps and incident gap detection.
- Require actual successful execution and stable dependency hashes for assurance evidence; close SQLite resources explicitly.
- Add 18 adversarial regression methods without changing first-edition manuscript or architecture.
- Restore seven index-register entries and align stale publication QA predicates with the frozen edition. Document the exact Chapter 29 planning exception without changing the budget.
- Acknowledgment: Sean identified the original malformed identity-signature defect. See [maintenance release notes](RELEASE_NOTES_v1.0.1.md) and [errata](ERRATA.md).

## v1.0.0 — First-edition teaching companion (2026)

- Six progressive runnable standard-library Python builds, Chapters 22–27, for CASE-204 and RF-1042.
- Four additional educational exercise suites covering reliability (Chapter 28), adversarial authorization (Chapter 29), incident operations (Chapter 30) and reproducible assurance (Chapter 31).
- Source-backed architecture diagrams, guided code-reading paths, negative tests, bounded evidence collection and chapter-to-test navigation.
- Platform-specific quick start for macOS/Linux and the native-Windows portable subset; a version-pinned source ZIP route without Git.
- Ten-suite CI-backed companion verification, architecture-documentation checks, errata workflow and private vulnerability reporting guidance.

This release establishes **educational, locally simulated behavior**, not real-provider settlement, protected operational credentials, independent E5 epoch fencing, or production certification. See [full GitHub Release notes](RELEASE_NOTES_v1.0.0.md).

Future corrections will be recorded under a new version without modifying the immutable first-edition tag.
