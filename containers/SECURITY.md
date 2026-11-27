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

SQLite FTS5 and SESSION remain enabled, OpenSSL QUIC code and development curl remain installed. The stable package versions reported by Debian for [SQLite](https://security-tracker.debian.org/tracker/CVE-2026-119373), [ncurses](https://security-tracker.debian.org/tracker/CVE-2025-69720) and [OpenSSL](https://security-tracker.debian.org/tracker/CVE-2026-107494) do not resolve the respective reported vulnerabilities at the time of review. Do not mix stable and unstable repositories. The hardening change itself does not suppress or remediate these CVEs; see the active policy below.

## Evidence and release policy

The host scanner checks pinned Trivy 0.76.2 archive SHA-256 values and retains inventories, SBOMs, unfiltered JSON, applicability evidence and the raw HIGH/CRITICAL gate output. Independent comparison to publisher checksums remains unverified. The active policy is [maintainer acceptance](assurance/README.md): critical, new/changed/unassessed high, high with a supported fix, invalid evidence and expired decisions block. The maintainer approved 200 bounded-risk and 20 limited-absence decisions for the exact 220 findings from run 23, expiring December 27, 2026 at 00:00 UTC. Limited absence is not an OpenVEX assertion. No findings are removed from raw reports. The dual-signature requirement is superseded; repository maintainer review is the authority, not independent attestation.

Weekly CI refreshes advisory data. Review vendor advisories and known-exploited/actionable lower-severity findings separately, revoke any decision for which a supported fix becomes available, and refresh dependencies through a reviewed change. Do not auto-renew approvals. GNU tar CVE-2025-45582 was reported medium by Scout; avoid untrusted archive extraction. A scan is not production certification.

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

The first five rows are historical observations. The final two rows are clean-built ARM64 scan observations, not independent advisory validation. The experimental image retained its parent layers; the clean-built development target omits Git during installation. These historical Scout results do not supersede Trivy run 23, which reported 53 HIGH verification and 57 HIGH development findings per architecture, zero CRITICAL.

Reassess before release and on scheduled scan failure. Refresh base digest and snapshot through a reviewed change, repeat native/container gates and document residual risk and next review date. Never move published tags or publish an image containing book material.
