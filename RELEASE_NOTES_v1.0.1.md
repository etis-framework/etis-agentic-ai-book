# v1.0.1 — Companion adversarial validation and assurance maintenance

Published maintenance release for *Engineering Agentic AI Systems*, First Edition (2026). This is a companion maintenance release, not a new printed edition. The original v1.0.0 tag remains immutable.

## Corrections

- Reject malformed identity and finance signatures and ambiguous or deeply nested JSON with controlled denial; preserve E5 service availability.
- Preserve UNKNOWN on unresolved execution replay without resending; make status inquiry nonmutating and validate provider observations.
- Bound advisory identifiers and lease timestamps; close SQLite connections explicitly.
- Reject malformed recovery states, escalate confirmation without dispatch, and detect empty telemetry.
- Require actual successful test execution and stable dependency hashes for Chapter 31 evidence.
- Add 18 regression methods; see [current errata](https://github.com/etis-framework/etis-agentic-ai-book/blob/main/ERRATA.md) and [current changelog](https://github.com/etis-framework/etis-agentic-ai-book/blob/main/CHANGELOG.md).

Thanks to Sean for identifying the original non-ASCII identity signature defect that prompted the wider review.

## Verification and limitations

The maintenance release passed 171 local tests in ten suites and the architecture/documentation check on macOS with Python 3.14.7. Earlier Linux constituent-suite verification passed with Python 3.13.5. The merged release commit `d1591a61aa235a74ca0e2e7d0c478377a63f809d` passed the [four-job macOS/Ubuntu Python 3.10/3.13 CI run](https://github.com/etis-framework/etis-agentic-ai-book/actions/runs/45876023877). Local fixtures do not establish live-provider behavior, protected credentials, OS isolation, independent E5-side owner fencing, external audit custody or production certification. Native Windows supports only the documented portable subset.

## Frozen first-edition planning exception

The published Chapter 29 source has 3,654 words by the existing QA counting method, versus the historical 3,500-word limit (154 words over). Preserve the published chapter unchanged. The exception applies only to the exact source path and SHA-256 below, with the original cap and count. Any altered over-budget chapter fails the ordinary gate. The V10/V12 budgets and page-allocation limits remain unchanged. This is not a print-quality waiver.

- Path: `manuscript/part-05-reliability-security/ch29-security-and-adversarial-agent-behavior/index.md`
- SHA-256: `0fef0d48646ea87e99507e7706935758ecd63e762631144c04884dc961fbabb9`

Publication infrastructure also restores seven index-register entries and aligns stale source predicates. No manuscript or figure content is revised, and no KDP replacement is required.

## Reader selection

Download the v1.0.1 source ZIP or check out the tag for corrected exercises. Keep v1.0.0 for exact original first-edition source reproduction. Follow [current setup guide](https://github.com/etis-framework/etis-agentic-ai-book/blob/main/docs/GETTING_STARTED.md) and [release policy](https://github.com/etis-framework/etis-agentic-ai-book/blob/main/RELEASE.md).

The tagged source archives are immutable, so their original documentation may contain pre-publication wording. The current setup guide supersedes that wording; select the desired release tag explicitly.
