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
