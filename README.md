# Engineering Agentic AI Systems

**Build, Secure, Verify, and Operate Trustworthy AI Agents**
*ETIS Professional Computing Series · First Edition (2026) · William T. O’Connell, Ph.D.*

[ETIS Framework](https://etisframework.org) · [Books](https://etisframework.org/Books/) · [Companion code](examples/refund-reference-system/README.md) · [First-edition releases](https://github.com/etis-framework/etis-agentic-ai-book/releases) · [Errata](ERRATA.md)

This is the source repository and **executable teaching companion** for the 503-page, 7 × 10-inch book (36 chapters, seven parts). It contains six progressive Python reference builds, actual source-module architecture diagrams, executable tests, and recovery, security, operations, and assurance exercises. **No payment service, paid AI API, API key, external provider, or package installation is required to run the companion tests.**

> **Engineering rule:** AI proposes; trusted controls independently authorize consequential execution. The CASE-204 **$500** fictional refund uses the stable operation identity **RF-1042**. Passing tests does **not** certify a production payment system or security boundary.

## Start here — no Git experience required

**Choose a version:** use the [latest stable companion release](https://github.com/etis-framework/etis-agentic-ai-book/releases) for corrected exercises. Docker support begins with `v1.1.0` (see [release notes](RELEASE_NOTES_v1.1.0.md)); `v1.0.1` is the corrected native-only baseline, and `v1.0.0` preserves exact original source reproduction. The printed book is unchanged.

**New to GitHub?** Read the [step-by-step setup guide](docs/GETTING_STARTED.md). It explains how to **download the first-edition ZIP without Git**, find the extracted folder, check Python, and run the first example. You do not need an AI account, payment provider, or Python packages.

### Option 1 — Docker (no host Python required)

Install Docker Desktop or Docker Engine with Compose V2, start it, and open a terminal in the extracted or cloned **v1.1.0 source folder**. From the repository root:

```bash
docker compose build companion
docker compose run --rm --no-deps -T companion
```

The default verification service runs in a disposable, non-root, read-only Linux container without external network access or a host source mount. It executes the full companion and infrastructure checks. See [container execution](docs/CONTAINER_EXECUTION.md) for interactive development, Windows, persistent exercise state, evidence export and troubleshooting. Docker support is separate from production isolation. The initial image pull/build requires network access.

### Option 2 — Native Python (unchanged)

**macOS/Linux readers who use Git** can run these commands after selecting the published v1.1.0 tag; maintainers testing an unreleased candidate should instead remain on their clean feature checkout:

```bash
git clone https://github.com/etis-framework/etis-agentic-ai-book.git
cd etis-agentic-ai-book
git checkout v1.1.0
python3 publishing/scripts/check_companion_release.py
```

**Windows:** use Docker Desktop in Linux-container mode for the container workflow, or run `py -3 publishing/scripts/check_companion_release.py --portable` for native Builds 0–2 and documentation checks only. The full native suites need macOS/Linux. The Python **standard library is sufficient**; no `pip install` is needed.

The checker reports `PASS` when its local fixture tests and checks succeed. An intentionally denied refund or unresolved provider acknowledgment can also be **correct** behavior within an individual exercise. A passing test is not production certification.

**Next:** [run Build 0's fictional lost-acknowledgment lesson](examples/refund-reference-system/build0/README.md), then [follow the six-build learning path](examples/refund-reference-system/LEARNING_PATH.md). Build 0 shows why E7 can record uncertainty even when mock E8 contains one confirmed RF-1042, and how reconciliation avoids a second effect.

## Find what you need

| I want to... | Go to |
|---|---|
| Run the examples | [Getting started](docs/GETTING_STARTED.md) · [Container execution](docs/CONTAINER_EXECUTION.md) · [Companion overview](examples/refund-reference-system/README.md) |
| Trace a chapter to source and tests | [Chapter-to-code map](docs/CHAPTER_MAP.md) · [Evidence map](examples/refund-reference-system/IMPLEMENTATION_EVIDENCE_MAP.md) |
| Understand architecture and contracts | [Architecture](examples/refund-reference-system/ARCHITECTURE.md) · [CAB-001 architecture catalog](metadata/architecture-catalog.md) |
| Learn by investigating failure | [Guided learning path](examples/refund-reference-system/LEARNING_PATH.md) · [Verification matrix](examples/refund-reference-system/TESTING.md) |
| Examine adversarial authorization | [Chapter 29 security](examples/refund-reference-system/security/README.md) |
| Collect bounded reproducible evidence | [Chapter 31 assurance](examples/refund-reference-system/assurance/README.md) |
| Report an error or security concern | [Errata](ERRATA.md) · [Security](SECURITY.md) · [Contributing](CONTRIBUTING.md) |
| Understand release compatibility | [Releases](RELEASE.md) · [Changelog](CHANGELOG.md) · [Rights](RIGHTS.md) |

## Six runnable builds

| Chapter | Checkpoint | Engineering subject | Start |
|---|---|---|---|
| 22 | Build 0 | Deterministic authorization, E7/E8, UNKNOWN and reconciliation | [Read and run](examples/refund-reference-system/build0/README.md) |
| 23 | Build 1 | Bounded **untrusted** advisory proposal | [Read and run](examples/refund-reference-system/build1/README.md) |
| 24 | Build 2 | Scoped identity and context provenance | [Read and run](examples/refund-reference-system/build2/README.md) |
| 25 | Build 3 | Independently checked E5 approval boundary | [Read and run](examples/refund-reference-system/build3/README.md) |
| 26 | Build 4 | Provider contracts, ambiguous effects, reconciliation | [Read and run](examples/refund-reference-system/build4/README.md) |
| 27 | Build 5 | Local ownership, fencing limits, and recovery | [Read and run](examples/refund-reference-system/build5/README.md) |

**Beyond the six builds:** [Chapter 28: reliability](examples/refund-reference-system/reliability/README.md) · [29: security](examples/refund-reference-system/security/README.md) · [30: incident operations](examples/refund-reference-system/operations/README.md) · [31: verification evidence](examples/refund-reference-system/assurance/README.md).

## Repository organization

- [`examples/refund-reference-system/`](examples/refund-reference-system/README.md): reader-focused runnable implementation, tests, architecture SVGs, and learning guides.
- [`manuscript/`](manuscript/): **frozen first-edition book sources**; not the preferred reader navigation experience.
- [`assets/`](https://github.com/etis-framework/etis-agentic-ai-book/tree/v1.0.0/assets): book figure sources and rendered artwork (full repository only).
- [`references/`](https://github.com/etis-framework/etis-agentic-ai-book/tree/v1.0.0/references): bibliography and source register (full repository only).
- [`metadata/`](metadata/): approved architecture and publication traceability.
- [`publishing/`](publishing/README.md): manuscript generation and QA, separate from companion tests. Historical root-level QA notes are preserved in [`publishing/reviews/legacy-qa/`](publishing/reviews/legacy-qa/README.md).
- [`review/`](https://github.com/etis-framework/etis-agentic-ai-book/tree/v1.0.0/review) and [`archive/`](https://github.com/etis-framework/etis-agentic-ai-book/tree/v1.0.0/archive): retained historical engineering/editorial materials (full repository only). Historical status statements in these folders are **not current publication status**.
- [`containers/`](containers/README.md), `Dockerfile`, `compose.yaml` and `.devcontainer/`: companion execution infrastructure, not a new reference build.

The compact verification image contains companion code, active reader guides and their selected local QA dependencies, not the full publication or historical archive. Full-repository-only links above deliberately point to the immutable first-edition source. Native CI continues to check the active documentation in the complete checkout.

## Versions, rights and scope

The **original first-edition companion is `v1.0.0`**; `v1.0.1` contains the verified code corrections, and `v1.1.0` adds containerized execution and verification infrastructure. Use the latest stable release for exercises. Download the [appropriate GitHub Release](https://github.com/etis-framework/etis-agentic-ai-book/releases) and use its immutable tag. Use `v1.0.0` only when exact original source reproduction is required; `main` can change later. See [release policy](RELEASE.md). The paperback ISBN is **979-8-9966760-6-4**; hardcover ISBN is **979-8-9966760-7-1**.

**The educational code is not production-ready.** The same-user subprocess fixture does not provide OS isolation, mock keys are not protected credentials, E2 fencing does not extend into E5, mock E8 is not a financial provider, and local evidence is not independently attested. Conceptual MCP/A2A discussions do **not** imply implemented MCP/A2A stacks. Review the [limits and proofs](docs/CHAPTER_MAP.md) before drawing architectural conclusions.

Software licensing and commercial textbook rights are **separate**: see [LICENSE](LICENSE) and [RIGHTS.md](RIGHTS.md). The manuscript and branding are **not** granted under the software license. Report factual book errors through [ERRATA.md](ERRATA.md); do not open a public issue containing secrets or a vulnerability exploit.
