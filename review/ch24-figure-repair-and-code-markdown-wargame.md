# Chapter 24 revised-package review — Chapter 23/24 figures and companion assurance

**Scope:** Chapters 23–24 and their references, CAB-001 mappings in the manuscript, Build 0–2 executable source, educational READMEs and engineering-standard checklist. This record accompanies the Chapter 24 branch, not a claim of publication certification.

## Defect and remedy

The original Chapter 23 SVG marker used `markerWidth=12`, `markerHeight=12` with default `strokeWidth` marker units. At a four-unit stroke its arrowhead scaled to approximately 48 viewBox units, visually overwhelming the 7×10 print figure and overlapping node edges. F23-03 also placed arrowheads at intermediate elbow bends rather than only at actual targets. Chapter 24 hand-generated polygon arrows had some tips on target box outlines. These were reproducible **figure defects**, not substantive changes to the architecture.

All F23-01/02/03 masters now use a small fixed-size, `userSpaceOnUse` arrowhead and stop before receiver boundaries. F23-03 left and right denial branches are single elbow paths with their only arrowhead at the actual terminal target. The F23-01 dotted handoff to financial execution now terminates at an explicit red `X`, not a downward arrow implying a callable payment path. All F24-01/02/03 arrowheads were reduced and inset from their target boundaries, including the failure branches. The authoritative masters, publication SVGs and freshly generated PNGs were kept aligned. `check_ch23_ch24_arrow_geometry.py` is a reusable source/published-master and arrow-size/border-contact regression gate in `make check`; **it is not a substitute for manual raster inspection and native Word proofing**.

## Six-lens review — source and reader journey

1. **Implementing engineer:** Builds 0, 1 and 2 remain distinct executable checkpoints. Build 2's `identity.py`, `context.py`, `pipeline.py`, `demo.py`, and `test_scope.py` have typed data contracts, explicit exceptions, a credential-free CLI and deterministic tests; Build 1 import adaptation is documented. No new dependencies or unnecessary package framework were introduced by the figure correction.
2. **Enterprise architect:** The corrected arrows preserve E1/C01 identity assertion, E4/C03 scoped context, E3/C04 untrusted proposal, and the distinct E5/E6/E7/E8 consequential boundary. The revised F23-01 red `X` explicitly rejects any direct advisory financial handoff. A proposed decision is not a permission or business effect. Builds remain teaching checkpoints; Designs A/B/C remain alternatives.
3. **Advanced student:** The Build 2 README explains exact commands and expected positive/negative outcomes, provenance, fresh/stale and cross-tenant cases, and why `TRACE-204` / `ADV-TRACE-204` are not RF-1042. The source remains standard-library-only and independently runnable. The visual arrows now point at complete operations rather than crossing boundaries unclearly.
4. **Security/assurance:** Public HMAC fixture key and locally constructible `VerifiedScope` do **not** establish authentication, protected data access, cryptographic capability safety or isolation from arbitrary code in the same interpreter. The adversarial-valid-token refund denial remains a mandatory **Build 3** protected E5 test; Build 2 tests only the in-process educational boundary.
5. **SRE/operator:** `ScopeDenied`, `ContextUnavailable`, and rejected advisory content do not create or mutate an E7 financial `UNKNOWN`; only an unresolved consequential effect in the Build 0 sequence has that meaning. Build 2 does not dispatch to E6. The no-write test is a fixture observation, not proof against arbitrary malicious native code.
6. **Business owner:** CASE-204 is still the illustrative $500 proposed refund; RF-1042 remains an independently controlled consequential identity. Customer narrative and evidence metadata cannot approve a payment. The chapter states omissions, costs/risks and verification evidence before production adoption.

## Additional code/Markdown assurance notes

- The current Build 0, Build 1 and Build 2 tests must be executed in the target workspace; a test passing locally establishes only its stated fixture outcomes.
- `LocalAssertionAuthority` has a deterministic public educational signing key and explicit expiry. Production issuer assurance, replay detection, credentials, revocation and independent boundary enforcement are **omitted**, with E1/E5 ownership and next-stage tests documented in the Build 2 README.
- `CatalogRecord` and `FixtureCatalog` are fixture transport objects, not a hardened data store or proof of record authenticity. The retrieval gate validates source allowlist, tenant/case match, supported version, age and classification before calling the Build 1 adviser. Future E4 controls need independent access enforcement and provenance verification.
- Build 2's in-process import adaptation using `sys.path` is clearly described as an educational packaging compromise; it does not imply sandbox isolation. Its replacement in a later packaging pass is permissible, but not necessary to introduce now.
- README scenario outputs and command continuations were checked against the CLI/tests; no restructuring of working code was justified solely to enlarge the diff. No new simulated control is claimed as a real security guarantee.

## Open publication gates

Native Word for Mac 7×10 page and figure inspection, edition source-revision/tag pinning, final bibliography/source-to-claim audit, index/contents and print proof remain independent release requirements. This patch only asserts tested local software/figure gates; no certification is inferred.
