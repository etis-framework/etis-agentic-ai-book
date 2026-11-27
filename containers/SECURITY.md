# Container supply-chain governance

[Acceptance](ACCEPTANCE.md) · [Repository security policy](../SECURITY.md)

Both targets use the same digest-pinned official Python Trixie Slim index. Signed Debian and security archives use a fixed timestamp (2026-11-27 00:00 UTC), including transitive dependencies. APT signature and integrity checks remain enabled; only historical snapshot freshness expiry is disabled for these repositories. Verify archive availability and installed versions on both architectures; never silently fall back to moving mirrors. This is controlled dependency selection, not bit-for-bit reproducibility.

| Additional input | Purpose |
|---|---|
| passwd, libzstd1 updates | Address reported shadow and zstd findings if snapshot provides fixes; verify versions and rescan |
| make | Development convenience |
| curl | IDE bootstrap |
| libstdc++6 | VS Code runtime requirement |

Git stays on the host. Installing Git brought in the Debian libexpat1 package and four scanner-reported high findings; omitting Git from the development build avoids those unnecessary dependencies. The build asserts Git is not executable on PATH and libexpat1 is not installed. This does not assert Python contains no XML parser: bundled components still require scanning. Remote VS Code Git integration is disabled.

Both images uninstall pip and remove ensurepip, including its embedded wheel. No third-party Python packages are required. Native host tooling remains unchanged. Test actual VS Code attachment, Python execution and debugging before claiming support; extension-provisioned tooling is outside the base image inventory.

## Additional hardening after independent CI scans

The November 27, 2026 Trivy 0.76.2 scans of both architectures reported 53 HIGH package findings in verification and 57 in development (zero CRITICAL). These are historical pre-hardening observations, not final acceptance. The raw reports remain authoritative scanner evidence; the earlier Scout results do not override them.

Both final targets remove setuid/setgid bits from regular files under `/usr` after package installation and user provisioning. This is defense in depth alongside non-root execution, dropped capabilities and no-new-privileges, not a claim that all privilege-escalation vulnerabilities are fixed. Verification additionally removes `/usr/bin/infocmp`, the specific CLI identified in [CVE-2025-69720](https://security-tracker.debian.org/tracker/CVE-2025-69720). Development retains it pending IDE compatibility assessment. The package database, libraries and historical image layers remain intact; the scanner can still report the associated source-package advisory. The CI scanner wrapper records exact-image hardening checks for both targets and fails on violations without suppressing vulnerability reports.

SQLite FTS5 and SESSION remain enabled, OpenSSL QUIC code and development curl remain installed. The stable package versions reported by Debian for [SQLite](https://security-tracker.debian.org/tracker/CVE-2026-119373), [ncurses](https://security-tracker.debian.org/tracker/CVE-2025-69720) and [OpenSSL](https://security-tracker.debian.org/tracker/CVE-2026-107494) do not resolve the respective reported vulnerabilities at the time of review. Do not mix stable and unstable repositories. No CVE is accepted or suppressed by this hardening change; supported fixes, applicability review and formal disposition remain required.

## Evidence and release policy

The Linux CI host tool scan-images.sh downloads Trivy 0.76.2, checks the published architecture-specific SHA-256 before extraction, and scans exact local Docker image IDs without pushing images. It records package inventories, CycloneDX SBOMs, all-severity JSON, scanner versions and high/critical gate results. Weekly CI refreshes advisory data. Archive evidence alongside the release commit. Scanner errors and all HIGH/CRITICAL findings (including unfixed) block this candidate. No blanket suppression or preapproved exceptions. Fixable high findings must be remediated. For unfixable findings, require maintainer review of advisory, exact package/version, target/architecture, applicability, mitigation, owner, expiry and upstream status before any narrow reviewed exception. Review known exploited findings irrespective of severity, unspecified findings and actionable medium/low findings. Resolve scanner disagreements; a scan is not proof of non-exploitability or production certification.

| Initial finding | Disposition required | Owner | Status |
|---|---|---|---|
| Vendored msgpack/urllib3 | Verify absence of installed and bundled copies; rescan | Maintainer | Pending |
| setuptools attribution | Inspect SBOM/filesystem; reconcile scanner evidence | Maintainer | Pending |
| shadow/libzstd | Verify fixed versions or assess remaining risk | Maintainer | Pending |
| New development dependencies | Scan final images and verify IDE | Maintainer | Pending |
| Git/Expat high findings (CVE-2026-111760, CVE-2026-105437, CVE-2026-118370, CVE-2026-117610) | Remove Git at build time; verify final package inventory and both architecture scans | Maintainer | Final ARM64 Scout scan clear; AMD64 and Trivy pending |
| GNU tar CVE-2025-45582 (medium, no fix reported by Scout) | Retain for archive/IDE tooling; avoid extracting untrusted archives; review upstream applicability and fixes | Maintainer | Pending review before release |
| Other distribution advisories | Review applicability, fixes and residual risk | Maintainer | Pending |

### Observed engineering baseline (ARM64, Docker Scout, 2026-11-27)

| Image | Critical | High | Medium | Low | Unspecified | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original verification | 0 | 19 | 18 | 47 | 3 | 87 |
| Original development | 1 | 54 | 67 | 258 | 30 | 410 |
| Hardened verification (08dcceafe08b) | 0 | 0 | 1 | 26 | 0 | 27 |
| Hardened development with Git (7ca28b3ef45b) | 0 | 4 | 6 | 54 | 0 | 64 |
| Experimental development after Git removal (56e15da45bc1) | 0 | 0 | 1 | 49 | 0 | 50 |
| Final verification (288c572aab91) | 0 | 0 | 1 | 26 | 0 | 27 |
| Final development (c60457c454e4) | 0 | 0 | 1 | 49 | 0 | 50 |

The first five rows are historical observations. The final two rows are clean-built ARM64 scan observations, not independent advisory validation. The experimental image retained its parent layers; the clean-built development target omits Git during installation. Final ARM64 Scout observations are complete; final committed-source scans on both architectures remain required. No risk acceptance is implied.

Reassess before release and on scheduled scan failure. Refresh base digest and snapshot through a reviewed change, repeat native/container gates and document residual risk and next review date. Never move published tags or publish an image containing book material.

### Draft disposition register and evidence reconciliation

The host scanner now also runs `containers/assurance/evaluate_security_gate.py`. See `containers/assurance/README.md` for the strict policy and approval boundary. All 220 historical high findings remain under investigation; no risk is accepted and no VEX statement is issued. The original scanner exit gate remains independently mandatory. The additional evaluator validates image/platform identity and Debian package inventory, hashes the evidence and rejects missing, inconsistent or unauthorized records. CI retains its output alongside original evidence. This is the first stage of governance, not authorization to waive findings.

### Exact-image applicability review

Patch C adds advisory-specific draft rationales and a bounded runtime observation to each scan. See `containers/assurance/README.md`. SQLite FTS5/SESSION and development curl remain present; package-level findings remain blocking. Both curl upstream advisories classify their respective issues as low severity and identify fixes in the 8.14.2 branch, but Debian backport status for the installed build remains unverified. Do not assume an upstream version comparison settles Debian patch status. All observations are review evidence only; no VEX or risk acceptance has been issued. The scanner publisher checksum comparison remains a separate outstanding verification requirement.

### Approved governed policy and protected release path

The approved policy is specified in [assurance/README.md](assurance/README.md#patch-d--approved-policy-protected-decision-implementation). Patch D implements a separate dual-signature, exact-evidence authorization evaluator with a maximum 30-day validity, fresh scan/review, protected revocation input and non-waivable critical/known-fix gates. It does not grant any individual approval. Ordinary CI stays strict until an independently controlled required release check is established and tested. No signing secrets or trust roots belong in the release candidate. Independent current upstream advisory review remains required; automated publisher reconciliation, external approval custody and required-check configuration are deployment gates, not claims of completed infrastructure.

The protected aggregate evaluator requires all four image scopes for the same candidate commit; individual PASS decisions do not authorize release. External authority deployment, upstream review, scanner provenance and OpenVEX validation remain mandatory outstanding controls. Candidate CI retains the strict gate.
