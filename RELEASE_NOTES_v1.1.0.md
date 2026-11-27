# v1.1.0 — Containerized Development and Reproducible Execution

Companion enhancement for *Engineering Agentic AI Systems*, First Edition (2026). The printed book, reference architecture, trust contracts and existing v1.0.0/v1.0.1 tags remain unchanged. This is a minor companion release, not a new textbook edition.

## Reader benefits

- Run the six reference builds and Chapters 28–31 exercises in a version-pinned Linux container without installing Python on the host.
- Choose disposable verification or an editable development workspace; optionally use VS Code Dev Containers.
- Use direct Docker/Compose commands or convenient Make targets. Keep multi-step exercises in explicit project-scoped persistent state and export bounded Chapter 31 assurance JSON.
- Preserve native Python execution, the four native CI configurations, and the v1.0.1 behavioral regression baseline.

## Engineering and assurance

The verification image uses a digest-pinned official Python base, non-root execution, read-only source/root filesystem, no external network, dropped capabilities and no-new-privileges. It contains selected source and documentation dependencies for the existing checks rather than the publishing toolchain. Git/source control remains on the host; the development image intentionally excludes Git and pip, and remote VS Code Git integration is disabled. Interactive development is deliberately mutable; the optional IDE network overlay is not a release-verification environment.

The existing 171 fixture tests and seven infrastructure regressions remain, with additional container-tool regressions and AMD64/ARM64 runtime acceptance gates. See [container acceptance](https://github.com/etis-framework/etis-agentic-ai-book/blob/v1.1.0/containers/ACCEPTANCE.md) for required evidence and scope. No release/platform acceptance is asserted solely by this notes file; verify the final commit and actual CI/manual results before tagging.

No production credential isolation, live payment provider, E5-side epoch enforcement, external audit attestation, hardened hostile-code sandbox or production certification is established. A pin is not a vulnerability scan. The native Windows portable subset remains unchanged; full Docker Desktop/Windows compatibility requires actual Linux-container acceptance evidence.

## Start here

Download this release's Source code ZIP, extract it, and open a terminal at the repository root. Install Docker Desktop or Docker Engine with Compose V2, then run:

```sh
docker compose build companion
docker compose run --rm --no-deps -T companion
```

See the [container guide](https://github.com/etis-framework/etis-agentic-ai-book/blob/v1.1.0/docs/CONTAINER_EXECUTION.md), [Getting Started](https://github.com/etis-framework/etis-agentic-ai-book/blob/v1.1.0/docs/GETTING_STARTED.md) and [release policy](https://github.com/etis-framework/etis-agentic-ai-book/blob/v1.1.0/RELEASE.md). Retain v1.0.0 for exact original reproduction and v1.0.1 for the corrected native-only baseline. Build images locally; the release does not publish a bundled textbook image to a registry.

Thanks to Sean for recommending container-based development and verification.

Container supply-chain controls: see [container security policy](containers/SECURITY.md). Historical local ARM64 Docker Scout scans reported zero HIGH/CRITICAL findings, but the subsequent GitHub Actions run 23 reported 53 HIGH verification and 57 HIGH development package findings on each of AMD64 and ARM64 (15 distinct CVEs, zero CRITICAL). All functional, architectural, native and runtime gates in that run passed; the strict security gate blocked. The maintainer subsequently approved narrowly scoped time-bounded decisions for 200 residual-risk findings and 20 limited-absence observations (not OpenVEX), expiring December 27, 2026 at 00:00 UTC. No raw findings are suppressed. Re-evaluate the final commit using the revised gate before tagging. Earlier ARM64 IDE debugging was observed; post-hardening IDE and Windows acceptance must not be claimed without evidence. This release is educational, not a security-certified production environment.
