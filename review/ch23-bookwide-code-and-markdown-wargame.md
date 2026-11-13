# Chapter 23 branch: book-wide listings and six-lens source review

## Scope and evidence

Reviewed the uploaded 373-page DOCX and the post-Chapter-23 source baseline; inventoried every triple-backtick manuscript block. Three blocks occur in the completed manuscript: a Chapter 3 illustrative YAML policy, Chapter 22 Build 0 testing, and Chapter 23 Build 1 commands. All are now styled through a shared DOCX path, including chapter-only builds. Long unit-test commands are intentional shell continuations; Chapter 23 demonstration calls use a shared `DEMO` variable in one pasteable block. A book-wide lint rejects lines exceeding 68 printed columns, as well as malformed shell continuations.

## Six-lens re-review

- **Implementing engineer:** Build 0 retains its independent commands. Build 1 accepts only bounded case, tenant, exact integer cents and evidence; no payment imports. Corrected a nested `source_ids` edge case: non-string/unhashable elements now fail with `InvalidAdvisory` (new executable negative test).
- **Enterprise architect:** E3/C04 remains proposal-only and cannot grant E5 authority; E7/E8 business-state separation and RF-1042 ownership remain unchanged. Static import separation is not a security sandbox.
- **Advanced student:** Monospaced/shaded listings, conservative width and explicit `\` continuation guidance improve reproduction in 7x10 print. Chapter 23 groups demonstration calls using `DEMO` and preserves the no-credential path.
- **Security / assurance:** Faked `approved`, wrong scope and malformed payloads are denied by the schema; the new malformed nested-source test closes an exception-type leak. This does not prove isolation against arbitrary malicious Python code or validate actual identity tokens.
- **SRE / operator:** No additional E7/E8 side effects, provider calls or retry paths. Model failures remain safe without permissive fallback. Operational telemetry and genuine process isolation are later-build obligations.
- **Business owner:** The $500 CASE-204 example and trusted RF-1042 identity are unchanged. A favorable recommendation remains subject to independent review and authorization. No new infrastructure cost or vendor dependency is introduced.

## Publication caveats

Automated DOCX output and runtime checks must be executed on the patch installation; native Word for Mac print inspection, figure masters at print size, full source-to-claim verification and final page ledger certification are separate open gates. Screen-shot review of the uploaded PDF-like DOCX content motivated this patch; it does not prove published-edition layout. All manuscript fences were inventoried, but future additions must pass the new lint.
