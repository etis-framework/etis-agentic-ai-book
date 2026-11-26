# First-edition companion — version and release policy

[Home](README.md) · [GitHub Releases](https://github.com/etis-framework/etis-agentic-ai-book/releases) · [Release notes](RELEASE_NOTES_v1.0.0.md) · [Changelog](CHANGELOG.md) · [Errata](ERRATA.md)

**Edition:** `v1.0.0` is the immutable source version accompanying the first printed edition of *Engineering Agentic AI Systems* (2026). The GitHub Release and annotated tag are published **before** the Amazon book launch. The first-edition code is a credential-free, standard-library-only teaching fixture; it is not a real payment system, a provider certification, or a production deployment.

## Maintainer release sequence

1. Merge the final documentation PR, confirm the candidate `main` commit and clean working tree, and check that all four required Ubuntu/macOS Python CI jobs passed on that exact commit.
2. Run `python3 publishing/scripts/check_companion_release.py` in a fresh macOS/Linux checkout; inspect Builds 0–5 and Chapter 28–31 exercise guides. Native Windows `--portable` covers Builds 0–2 only.
3. Review the fixed release notes in [RELEASE_NOTES_v1.0.0.md](RELEASE_NOTES_v1.0.0.md), the rights boundary in [RIGHTS.md](RIGHTS.md), and secret-free sample files. The final KDP print viewer and manuscript are handled separately from the GitHub companion.
4. On the verified `main` commit, create and push the annotated **`v1.0.0`** tag once. Publish a GitHub Release from that tag, using the prepared release notes and leaving **Set as pre-release** unchecked.
5. Verify anonymous access to the GitHub Release, source ZIP, README, architecture SVGs, exercise tests, security reporting guidance and errata process **before** launching the book on Amazon.

## Version semantics

- **`v1.0.0`** is fixed to the first-edition source commit. Never move or recreate the tag to change its contents.
- **`v1.0.1` and later** may deliver explicitly documented corrections and errata, under new tags.
- **`main`** is the development branch and is not the edition-specific source once new commits arrive.
- Source ZIPs provided automatically by GitHub under the selected Release are the simplest version-pinned option for non-Git readers.

## Verified scope of this release

The companion runs six progressive Python builds (Chapters 22–27) plus Chapter 28 reliability, Chapter 29 security, Chapter 30 incident operations and Chapter 31 evidence exercises. The full verification workflow uses Ubuntu/macOS with Python 3.10 and 3.13. All payment/identity/provider operations use fictional local fixtures; the reference implementation does **not** claim hardened credential custody, provider settlement, complete E5-side lease fencing or external audit attestation.

## Maintenance release procedure (v1.0.1 and later)

1. Review the correction diff, errata, regression evidence and release notes; verify that frozen manuscript and figure assets are unchanged from the edition tag.
2. Run `make check-companion` and the applicable publication QA gates. Confirm the four CI jobs on the exact release commit before tagging.
3. Create a new annotated patch tag on the verified clean `main` commit. Publish its GitHub Release using the matching release notes; do not move `v1.0.0`.
4. Verify anonymous access to both release versions and source ZIPs. Recommend the corrected companion for exercises; retain the original for exact reproduction.

The Chapter 29 source planning exception is documented in [maintenance notes](RELEASE_NOTES_v1.0.1.md). It does not change the frozen manuscript, any budget, or the requirement for separate print QA. Generated index metadata corrections do not revise already printed copies.
