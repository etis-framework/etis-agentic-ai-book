# Container release acceptance — v1.1.0

[Home](../README.md) · [Container guide](../docs/CONTAINER_EXECUTION.md) · [Release policy](../RELEASE.md)

This is an acceptance procedure, **not evidence that a specific run has passed**. Keep logs with the candidate commit, image IDs, base index digests, host OS/architecture and Docker/Compose versions. Do not tag or mark a platform verified until its required tests complete. Test the same release commit after merge. Preserve the frozen manuscript, figure assets, architecture catalog, and existing v1.0.0/v1.0.1 tags.

## 1. Baseline and native regression

From the clean candidate checkout:

```sh
git status --short
git rev-parse HEAD
git diff --check v1.0.1 HEAD
git diff --exit-code v1.0.1 HEAD -- manuscript/ assets/ metadata/ book.yaml
make check-companion
make check-publication-pass04-protocols
```

Maintain the existing four native CI configurations (Python 3.10/3.13 × Ubuntu/macOS). The baseline is 171 ordinary fixture tests + seven runner regressions; additional container tooling tests are infrastructure regressions, not new payment/agent behavior. Run the full publication QA on the maintainer's native publishing toolchain as appropriate; no print revision is proposed. Do not weaken or skip a native gate to make a container green.

## 2. Base images and CI platform matrix

The pinned Python official image indexes were selected from Docker Hub's multi-platform metadata. Confirm the exact image index is retrievable and lists Linux AMD64 and ARM64, then build the actual target on each architecture. Inspect the Dockerfile for the precise pins and update them only through review and regression.

- Shared base: [Python 3.13.18-slim-trixie](https://hub.docker.com/_/python/tags?name=3.13.18-slim-trixie), index `sha256:7249d5587b78209a006dc4a3b5340678f84ea729239193aa559962cd8c1fce50`.

A digest is immutable content selection, not a security attestation. A public registry may remove an old manifest. If retrieval fails, stop and review replacement pins; never substitute a floating tag. Review current base-package vulnerabilities and the actual risk/mitigation of an offline educational fixture before release. No claim of vulnerability-free images is made.

| Environment | Required evidence |
|---|---|
| GitHub Linux AMD64 | Native runner, verification image build/run, all suites, six demos, denial and runtime negative controls, evidence export, dev workspace/volume lifecycle |
| GitHub Linux ARM64 | Same acceptance on native ARM64 (not only emulation or manifest inspection) |
| Docker Desktop on Apple Silicon macOS | Full verification, all six demos, evidence export, writable dev workspace, persistent state, IDE attach if claiming IDE support |
| Windows Docker Desktop (Linux containers) | Full verification, all six demos, direct commands without host Python/Make, PowerShell export, dev workspace/volume lifecycle, optional IDE attach |
| Native Windows | Existing portable Builds 0–2 only; do not claim full native support |

Intel Mac follows the AMD64 image path; record an actual Intel Docker Desktop run if claiming host-specific verification, rather than treating Linux CI as an Intel Mac test. The two Linux CI jobs must run on the corresponding native architectures. An unavailable runner or a timed-out job is incomplete, not a pass.

## 3. Disposable verification and negative controls

The host needs Docker and Compose; the following commands use no host Python:

```sh
docker compose config --quiet
docker compose build companion
docker compose run --rm --no-deps -T companion
docker compose run --rm --no-deps -T companion python3 containers/demo.py --build 0
docker compose run --rm --no-deps -T companion python3 containers/demo.py --build 1
docker compose run --rm --no-deps -T companion python3 containers/demo.py --build 2
docker compose run --rm --no-deps -T companion python3 containers/demo.py --build 3
docker compose run --rm --no-deps -T companion python3 containers/demo.py --build 4
docker compose run --rm --no-deps -T companion python3 containers/demo.py --build 5
```

Each build wrapper must return zero for its documented scenario. The verification service must show a fresh successful runtime preflight, infrastructure regressions, all ten suites with actual counts, and active reader-link PASS. No host source mount, Docker socket, exposed ports, privilege escalation or external network. Confirm source image contents exclude `.git`, full book artwork, historical archives, generated artifacts and local state. Native checks still run against the entire checkout; the image preserves the actual local reader-link dependencies rather than fake targets.

Linux may instantiate inactive tunnel devices in a network-disabled namespace. The runtime check queries interface flags and rejects any administratively enabled non-loopback link, regardless of its name or carrier status. Compose must still specify `network_mode: none`; inactive devices are not a reason to enable networking.

Negative controls (run individually, inspect exit codes; **nonzero is expected**):

```sh
docker compose run --rm --no-deps -T --user 0:0 companion
docker compose run --rm --no-deps -T companion python3 examples/refund-reference-system/build3/demo.py --scenario compromised
```

Root must fail the verification runtime guard (exit 1); compromised Build 3 must report DENIED without E7/mock E8 creation (exit 2). On POSIX also run the read-only source bind negative control; even a read-only mounted host source must not count as image-contained verification:

```sh
docker compose run --rm --no-deps -T -v "$PWD:/opt/etis:ro" companion
```

Expect runtime-preflight rejection. If a negative control passes unexpectedly, investigate before release. The checks detect specific configuration failures; they do not defend against a malicious administrator or modified verifier.

## 4. Persistent development and evidence lifecycle

On POSIX export `ETIS_DEV_UID=$(id -u)` and `ETIS_DEV_GID=$(id -g)` before building; PowerShell uses defaults (1000/1000). Use a new project name for acceptance so earlier exercise state is not reused. Run:

```sh
docker compose up -d --build --no-deps dev
docker compose exec -T dev python3 containers/dev_probe.py
docker compose exec -T dev python3 examples/refund-reference-system/build0/refund.py prepare --directory /state/acceptance-run
docker compose stop dev
docker compose rm -f dev
docker compose up -d --no-deps dev
docker compose exec -T dev python3 examples/refund-reference-system/build0/refund.py status --directory /state/acceptance-run
docker compose exec -T dev python3 examples/refund-reference-system/build0/refund.py dispatch-lost-ack --directory /state/acceptance-run
docker compose exec -T dev python3 examples/refund-reference-system/build0/refund.py reconcile --directory /state/acceptance-run
```

The persisted local state after recreation must still be AUTHORIZED. After the deliberate lost acknowledgment and reconciliation it must be CONFIRMED, with one mock provider record. Inspect the two SQLite stores with the original [Build 0 guide](../examples/refund-reference-system/build0/README.md). Verify no source files changed other than deliberately edited development files; remove only test probes you created. `docker compose down` retains state; `down --volumes` is destructive and only for the explicitly disposable acceptance project.

Export evidence via the platform-appropriate commands in [the container guide](../docs/CONTAINER_EXECUTION.md). Inspect JSON: seven distinct registered claims, each EXECUTED_PASS and one executed test, overall EXECUTED_PASS, `production_certified: false`, actual source SHA-256 values, explicit production gaps. Repeat to a fresh output directory; earlier reports must not be overwritten. Simulate failed export and confirm no successful JSON artifact is promoted. Evidence is a local fixture record, not host attestation.

## 5. IDE and reader acceptance

Use a clean extracted source ZIP (not a preconfigured Python environment) and verify the documented Docker-first route works. Confirm all original native commands still work. Open the candidate in VS Code with Dev Containers, reopen in the `dev` service, confirm the `etis` non-root user and `/workspace` interpreter, edit/revert a disposable test file, run the full companion tests and close/reopen. Confirm state survives and the IDE overlay does not modify the verification service's offline policy. Verify host Git status/diff and an edit/revert through the shared checkout; do not expect Git integration inside the remote window. Confirm Python debugging works without pip/ensurepip and record any extension-provisioned tools separately. VS Code downloads are optional tooling setup, not runtime dependencies. Validate the Windows PowerShell evidence export without host Python. Do not state these manual gates passed unless actually observed.

## 6. Supply-chain acceptance

Follow the [container security policy](SECURITY.md). Both architecture jobs must produce inventories, SBOMs and vulnerability reports for both final images. Scanner errors, critical findings, high findings with supported fixes, and high findings without an exact, unexpired maintainer-approved disposition block the candidate. Record local Scout results and resolve scanner disagreements before tagging. Confirm the clean-built development image has no Git executable or installed libexpat1 Debian package; the earlier purge experiment is not final image evidence. Review GNU tar CVE-2025-45582 and other remaining findings, including known exploited advisories, before release.

Additional exact-image acceptance: inspect both `*-hardening.txt` artifacts from each architecture. Both targets must have no regular setuid/setgid files under `/usr`; verification must have no `/usr/bin/infocmp` or `infocmp` on PATH. Development retains the terminfo CLI pending IDE compatibility assessment. Repeat native and container regressions, persistence and VS Code debugging after these image changes. This gate does not establish the absence of file capabilities, host vulnerabilities or all vulnerable code; it does not remove the raw HIGH/CRITICAL scanner findings.

## 7. Six-lens release review

| Lens | Required challenge |
|---|---|
| Implementing engineer | Build from clean source; rebuild after changes; no host Python; exact exit propagation |
| Enterprise architect | Preserve E1–E9/C01–C09 and CASE-204/RF-1042; no new execution authority or Build 6 |
| Advanced student | ZIP onboarding, original book commands, six demos, state persistence, expected DENIED/UNKNOWN outcomes |
| Security and assurance | Non-root, read-only, no egress/socket, digest pins, negative controls, no false green or misleading evidence |
| SRE/operations | Fresh containers, bounded verification, volume ownership, predictable cleanup, recovery and evidence export |
| Business owner | No paid provider, no unnecessary tooling, no KDP revision, clear limitations and support boundaries |

Release gates: review the exact PR diff and all native/container CI results; run required manual host/IDE acceptance; update release notes with observed results and residual limitations; merge and repeat verification on the actual main SHA; create an annotated v1.1.0 tag and publish the matching GitHub release. Never move older tags. No registry publication is part of this release.

Apply the [maintainer-controlled security policy](assurance/README.md). Both roles on both architectures must pass the current evaluator with complete raw reports, inventory, SBOM, hardening and applicability evidence. Preserve the raw high/critical exit status and full reports, even when the governed result passes. Review current Debian/upstream fixes, expiry, scope, and lower-severity risks before release. No OpenVEX publication or independent security attestation is claimed. Manual IDE and Windows results must be reported accurately; do not claim untested platform support.
