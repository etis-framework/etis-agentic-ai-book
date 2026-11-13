# Chapter 23 / Build 1 — engineering review and QA record

**Baseline:** `main` at `6eb466c3da20cdc73b5d609d4144e00ac2063b65` per uploaded extraction record. This patch is not committed or merged.

## Scope and exercise review

- **Implementing engineer:** Strict immutable typed work/evidence/proposal contracts; no floats/booleans for money; `Protocol` model seam; no new dependencies. Failure injection and independently runnable Build 0 retained. Single-case fixtures remain intentionally fixed, not a general payments SDK.
- **Enterprise architect:** C02/C04 advisory separated from C05/C06/C07 and E5/E7/E6/E8. Correlation (`TRACE-204`) and proposal (`ADV-TRACE-204`) cannot be RF-1042. E1/E4 authenticity and distributed E2 fencing explicitly deferred.
- **Advanced student:** Offline demo, three dispositions, adversarial prose, exact commands, source order and expected JSON. 14 independent Build 1 unittest cases (including actual Build 0 E5 denial) and 16 preexisting Build 0 cases. The attacker-with-arbitrary-Python-execution case is *not* demonstrated.
- **Security and assurance:** Unknown/forged `approved` and `provider_key` proposal fields rejected. Valid agent identity token is not a transaction authorization; independent process/credential boundary required in Chapter 25 and security replay in Chapters 29/31. Import-only tests are explicitly not a sandbox.
- **SRE/operator:** Model exceptions become sanitized advisory unavailability; no blind financial retry; no E7/E8 mutation on advisory path. Real diagnostic event preservation, durable queues, and live provider reconciliation remain later build obligations.
- **Business owner:** `RECOMMEND_REVIEW` is not approval. Design B requires measured incremental value versus Design A, accounting for human review, errors, latency, privacy and system cost. Design C remains optional.

## Executed QA (Linux container; not native Word on Mac)

- Python 3 standard library tests for Builds 0 and 1: run via `make check`; latest Build 1 standalone 14/14 passes, and repository-wide check completes successfully after generating the full-book DOCX.
- `make book-docx` successfully generated a full-book DOCX and `check_figures.py --built` verified expected media presence/fingerprints.
- `make check` passed the existing chapter gates, new Chapter 23 gate, conceptual continuity, companion quality and V12 plan checks.
- Chapter 23 DOCX rendered in this environment as nine pages; **this is not the certified native Word finished-page count** (V12 allocation 14 pages). A contact-sheet and all three 1150px PNGs were visually inspected in the working environment.
- Figure masters `F23-01` architecture, `F23-02` behavior and `F23-03` decision are separate SVG/PNG assets. Semantic structure and local renders inspected; print-size inspection in native 7×10 Word remains open.

## Outstanding publication gates (not certified)

- Independently inspect every chapter and all figures at final 7×10 native Mac Word print size; verify complete-book page forecasts and manually verify chapter page breaks.
- Source-to-claim checks against primary material, editions, pages and exact external standards/guidance versions remain open.
- Final author technical approval and publication freeze, edition immutable tag, release testing and distribution decision remain open.
- Build 1 is a bounded educational fixture, not a production security control, live provider, model-evaluation result or financial service.
