# Release policy — first edition

[Home](README.md) · [Releases](https://github.com/etis-framework/etis-agentic-ai-book/releases) · [Changelog](CHANGELOG.md) · [Errata](ERRATA.md)

The intended public first-edition release is **`v1.0.0`**, synchronized with the November 26, 2026 paperback publication. This file is **the procedure**, not proof that a tag or release already exists. Confirm actual remote tag, branch, CI and release state before publication.

## Release gate (maintainer)

1. Approve and merge the publication-only correction PR; confirm licensing and historical materials suitable for public exposure.
2. Make a **fresh clone** of the candidate commit; run `python3 publishing/scripts/check_companion_release.py` on **macOS/Linux**, review the GitHub Actions Ubuntu/macOS matrix, and record results. On Windows, `--portable` verifies only Builds 0–2 and is not a substitute for full testing.
3. Independently execute `python3 examples/refund-reference-system/assurance/collect.py --output <unique-absolute-path-outside-repo>` and verify its `production_certified=false` result and enumerated gaps.
4. Inspect Build 0–5 SVGs in GitHub, all landing-page links, negative tests, and chapter map. The original publication checks involving Word/DOCX remain a separate, already frozen manuscript process.
5. Confirm no secrets, accidental source drafts, personal information, unintended licensing grants, or OS metadata are tracked (`git ls-files`, `git status`, secrets review). If the repository is already public, resolve any inappropriate disclosures immediately; do not assume publication review has already occurred.
6. Merge to `main`, establish a clean, documented release commit SHA and CI result, and create an annotated tag **only once**: `git tag -a v1.0.0 -m "ETIS Agentic AI first-edition companion v1.0.0"`.
7. `git push origin main` (if not already pushed) and `git push origin v1.0.0`; publish a GitHub Release from the tag using the template in [CHANGELOG.md](CHANGELOG.md), explicitly explaining simulated vs real guarantees.
8. Confirm intended visibility and verify anonymous access (if public) to README, diagrams, source, release/tag, errata, license and tests. Verify the public site link.

## Version semantics

- `v1.0.0`: exact source version associated with the **first printed edition**; immutable.
- `v1.0.1`, etc.: backward-compatible companion documentation or code fixes with changelog and errata; new tags, never retag `v1.0.0`.
- `main`: ongoing development; may differ from printed examples.
- Material contract changes or a new edition require an explicit new compatibility assessment; no silent breaking changes under a patch release.

Maintainer release notes should state Python versions tested and include an explicit **not production-certified** caveat. Archive downloads supplied by GitHub for the exact tag are preferable to independently repackaged examples.
