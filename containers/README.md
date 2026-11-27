# Container execution infrastructure

[Container guide](../docs/CONTAINER_EXECUTION.md) · [Acceptance and evidence](ACCEPTANCE.md) · [Repository home](../README.md)

This directory contains execution tooling, **not Build 6**. The unchanged companion source and tests remain under `examples/refund-reference-system/`.

- `verify.py`: fail-closed runtime preflight followed by container-tool regressions, existing runner regressions, ten fixture suites, architecture/documentation QA, and active reader-link QA.
- `demo.py`: convenience dispatcher for Builds 0–5 using their real existing CLI entry points. Build 0 uses a unique temporary state directory and checks the local status sequence.
- `export_evidence.py`: run the original Chapter 31 collector in a fresh temporary location, reject incomplete/failed reports, emit only successful bounded JSON to stdout. A fresh report is not an independent attestation.
- `dev_probe.py`: acceptance of non-root development mode and writable workspace/project state.
- `test_container_tools.py`: standard-library tests for the new tooling. They do not replace actual Docker runtime tests.
- `ACCEPTANCE.md`: reproducible runtime/platform gates and explicit limitations.

Both targets share one digest-pinned Trixie Slim Python base; development adds only Make, curl and the VS Code runtime library (and required transitive packages). Git runs on the host; no Git or libexpat1 Debian package is installed in the development target. See [container security policy](SECURITY.md). The compact verification context includes the actual three chapter files linked by active companion guides, the architecture catalog and the linked publication README records. It excludes generated outputs, artwork, authoring archives, Git history and local state. No empty placeholder files are used to satisfy link validation.

The source image is a local execution artifact; do not publish it to a registry or redistribute bundled book material. See [rights](../RIGHTS.md).
