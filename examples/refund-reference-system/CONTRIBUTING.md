# Educational companion-code engineering standard

The mandatory, cross-build control requirements and acceptance matrix are in [`ENGINEERING_STANDARD.md`](ENGINEERING_STANDARD.md). Every change to a build is reviewed with its chapter, tests, figures, source assumptions and traceability to the nine logical enterprise responsibilities (E1–E9) and cross-domain contracts (C01–C09). Use **fictional data** only.

1. **Teach the reasoning.** Clearly name functions, states and boundaries; explain *why* authorization, durable intent, reconciliation and denials matter. Avoid comments that merely restate obvious Python syntax.
2. **Document limits.** Label mocked identity, payment, provider uniqueness, concurrency and approval assumptions. A fixture is not production security.
3. **Preserve the running case.** CASE-204, $500 in integer cents and RF-1042 remain consistent. Durable operational state (E7) is local knowledge, distinct from simulated authoritative payment truth (E8).
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

## Build 3 and architecture-diagram changes

Review `build3/README.md`, `architecture.svg`, Chapter 25 and F25-01/02/03 together. Check strict request and signed-grant contracts, validity of the *actual fixture token* in hostile-client tests, no E7/E8 creation on denial, replay refusal, UNKNOWN on outage, correct trust-boundary labeling, safe output, process lifecycle cleanup, and regression of Builds 0–2. A source-module diagram is **required** for every build directory and must be updated whenever APIs, dependencies, stores or enforcement boundaries change. A separate process using the same OS account is a teaching boundary, not a production security guarantee.


### Build 4/provider contribution requirement

Any change to the E6/C07 provider command, E8/C08 observation, E7/C06 state machine, or E5 request path must update the Build 4 module diagram, first-reference explanations and the corresponding negative/reconciliation evidence. A new provider capability is not accepted merely because an SDK exposes it: record vendor version, key scope, retention and failure semantics with externally verifiable contract evidence. A simulated provider is explicitly labeled and must never receive real credentials.
