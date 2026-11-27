# Security policy

This repository contains **fictional educational code**; it is not an online payment service. Do not connect its fixed scenario or fixture keys to real credentials, live payment processors, or personal data. See the [chapter evidence map](docs/CHAPTER_MAP.md) for explicit gaps.

## Report privately

If you discover a vulnerability, **do not publish exploits, credentials, or sensitive details in a public issue**. Use GitHub's **Report a vulnerability** feature under this repository's **Security** tab for private disclosure. If the feature is temporarily unavailable, use the [ETIS website](https://etisframework.org) to locate an official contact route; never paste exploit details into a public issue or guess an email address.

## Supported versions

| Version | Status |
|---|---|
| First-edition `v1.x` | Published; use the most recent corrected release |
| Unreleased `main` | Development; no stability promise |
| Earlier drafts | Not supported |

We assess reports according to their actual impact and teaching boundaries. No claim of response SLA, protected keys, provider access, or production-grade isolation is made. Never put secrets into a sample issue or test fixture.

Container supply-chain controls: see [container security policy](containers/SECURITY.md) for pinned inputs, minimal dependencies, SBOMs, scanning and release gates. The v1.1.0 Linux AMD64/ARM64 container and four native macOS/Ubuntu CI jobs passed on the merged engineering baseline ([CI evidence](https://github.com/etis-framework/etis-agentic-ai-book/actions/runs/46041640893)). Container security PASS means compliance with bounded maintainer acceptance, not absence of vulnerabilities. See [v1.1.0 release notes](RELEASE_NOTES_v1.1.0.md) for residual risks, expiration and manual platform limitations.
