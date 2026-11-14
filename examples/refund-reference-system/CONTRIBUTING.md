# Educational companion-code engineering standard

The mandatory, cross-build control requirements and acceptance matrix are in [`ENGINEERING_STANDARD.md`](ENGINEERING_STANDARD.md). Every change to a build is reviewed with its chapter, tests, figures, source assumptions and E1–E9/C01–C09 traceability. Use **fictional data** only.

1. **Teach the reasoning.** Clearly name functions, states and boundaries; explain *why* authorization, durable intent, reconciliation and denials matter. Avoid comments that merely restate obvious Python syntax.
2. **Document limits.** Label mocked identity, payment, provider uniqueness, concurrency and approval assumptions. A fixture is not production security.
3. **Preserve the running case.** CASE-204, $500 in integer cents and RF-1042 remain consistent. E7 local knowledge is distinct from E8 external truth.
4. **Test evidence, not just return values.** Maintain `TESTING.md` alongside executable cases; Include authorization denial, duplicate, lost acknowledgment, missing/conflicting provider, and restart scenarios where relevant; inspect persistent state.
5. **Make steps reproducible.** Provide exact root-relative commands, expected observations, safe cleanup and prerequisites in each build README. Tests should use disposable temporary stores.
6. **Synchronize the book.** Update manuscript navigation, architecture, canonical figure masters, source register, cross-chapter references and QA records in the same guarded patch.
7. **Release carefully.** Run chapter and book QA, inspect figures at actual 7×10 Word print size, report open gates, and publish immutable edition tags only after approval.
8. **Respect local environments.** Do not modify the reader's Python or Homebrew configuration. Build 0 uses the standard library; future dependencies must be isolated and pinned.

An implementing engineer, enterprise architect, advanced student, security reviewer, SRE and business owner must each be able to assess what the code *actually proves* and where it is only a teaching approximation.

## Build 1 contribution check

Keep Build 0 independently runnable and the Build 1 proposal parser fail-closed. Changes to C04 fields must update `contracts.py`, `advisory.py`, the injected-model negative tests, Chapter 23, figures 23.1–23.3 and the source-register/traceability material together. Do not add provider credentials, financial adapter imports or execution functions to `build1/`. For any future model adapter, pin optional versions, keep offline exercises reproducible, and document exceptions and what tests do **not** establish.

## Build 2 review discipline

Review any change to `build2/` with `ENGINEERING_STANDARD.md`, Chapter 24 and F24-01/02/03 open. Require typed denial of malformed identity scope, tamper/expiry, cross-tenant and source-scope violations, stale/invalid context, unavailable E4 dependency, untrusted narrative and repeated no-write proof. Check that fixture HMAC and `VerifiedScope` remain labeled **simulations**, and that Build 0/1 remain independently runnable. Any proposed live credentials or payment interface requires a new risk/ownership review, not a silent import into `pipeline.py`. Preserve edition-specific immutable source tagging.
