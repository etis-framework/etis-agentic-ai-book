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
